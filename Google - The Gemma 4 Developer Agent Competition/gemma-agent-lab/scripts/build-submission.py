"""Build an untouched control or add a repair policy to the sample root agent."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import shutil
import stat
import sys
import tempfile
import zipfile


MAX_BYTES = 3 * 1024**3
EXTENSIONS = {'.yaml', '.yml', '.md', '.txt', '.py', '.json', '.safetensors'}
ROOT_NAMES = {'agent.yaml', 'agent.yml', 'root_agent.yaml', 'root_agent.yml'}
DEFAULT_POLICY = Path(__file__).resolve().parents[1] / 'candidate' / 'instruction.md'
POLICY_MEMBER = 'prompts/root-repair-policy.md'


def reject_link(path):
    flags = path.lstat()
    if stat.S_ISLNK(flags.st_mode) or getattr(flags, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError(f'Links and reparse points are unsupported: {path}')


def members(root):
    def raise_error(error):
        raise error

    reject_link(root)
    if not root.is_dir():
        raise ValueError(f'Expected a sample directory: {root}')
    paths = []
    names = set()
    size = 0
    for directory, dirs, files in os.walk(root, onerror=raise_error):
        for name in dirs + files:
            path = Path(directory) / name
            reject_link(path)
            if '\\' in name or ':' in name:
                raise ValueError(f'Invalid archive filename: {name}')
            relative = path.relative_to(root).as_posix()
            if relative.casefold() in names:
                raise ValueError(f'Case-colliding archive filename: {relative}')
            names.add(relative.casefold())
        for name in files:
            path = Path(directory) / name
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                raise ValueError(f'Unsupported sample member: {path.relative_to(root)}')
            size += path.stat().st_size
            paths.append(path.relative_to(root))
    if size > MAX_BYTES:
        raise ValueError('Uncompressed contents exceed 3 GiB')
    if {p.as_posix() for p in paths} & ROOT_NAMES != {'agent.yaml'}:
        raise ValueError('Supply the sample directory containing one root agent.yaml')
    return sorted(paths, key=lambda p: p.as_posix())


def scalar_line(value):
    """Decode common single-line YAML strings; fail closed on other syntax."""
    if value.startswith('"'):
        result, end = json.JSONDecoder().raw_decode(value)
        rest = value[end:]
    elif value.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'(.*)", value)
        if not match:
            raise ValueError('Unsupported quoted root instruction')
        result, rest = match.group(1).replace("''", "'"), match.group(2)
    else:
        result = re.split(r'\s+#', value, maxsplit=1)[0].strip()
        if not result or result[0] in '!&*{}[],@`#|>%' or re.search(r':(?:\s|$)', result):
            raise ValueError('Unsupported root instruction scalar')
        return result
    if rest and not re.fullmatch(r'\s+(?:#.*)?', rest):
        raise ValueError('Unexpected content after quoted root instruction')
    return result


def add_policy(root, policy):
    root_yaml = root / 'agent.yaml'
    config = root_yaml.read_bytes().decode('utf-8')
    keys = list(re.finditer(r'^instruction[ \t]*:[ \t]*(?P<value>[^\r\n]*)', config, re.M))
    if len(keys) != 1:
        raise ValueError('Expected one top-level instruction in agent.yaml')
    key = keys[0]
    value = key['value'].rstrip()
    policy_text = policy.read_text(encoding='utf-8').strip()
    if not policy_text or '\x00' in policy_text:
        raise ValueError('Candidate instruction must contain nonempty UTF-8 text')

    newline = '\r\n' if '\r\n' in config else '\n'
    # YAML block scalars can remain in their original style. More-indented lines
    # preserve the new Markdown line breaks even when the original was folded.
    block = re.fullmatch(r'[|>](?P<mods>[+-]?[1-9]?|[1-9][+-]?)(?:[ \t]+#.*)?', value)
    if block:
        body_start = key.end()
        boundary = re.search(r'^(?=\S)', config[body_start:], re.M)
        body_end = body_start + boundary.start() if boundary else len(config)
        body = config[body_start:body_end]
        explicit = re.search(r'[1-9]', block['mods'])
        content = re.search(r'^( +)\S', body, re.M)
        indent = int(explicit[0]) if explicit else (len(content[1]) if content else 2)
        padding = ' ' * (indent + (2 if value.startswith('>') and content else 0))
        addition = newline.join(padding + line if line else '' for line in policy_text.splitlines())
        updated = config[:body_end].rstrip('\r\n') + newline * 2 + addition + newline + config[body_end:]
    else:
        # Include/plain/quoted values are constrained to one physical line here.
        tail = config[key.end():].splitlines()[1:]
        next_content = next((line for line in tail if line.strip() and not line.lstrip().startswith('#')), '')
        if next_content.startswith((' ', '\t')):
            raise ValueError('Unsupported multiline scalar; use a YAML block or !include')
        include = re.match(r'!include[ \t]+(.+)$', value)
        if include:
            target = scalar_line(include[1])
            path = PurePosixPath(target)
            if (not path.parts or path.is_absolute() or PureWindowsPath(target).drive or
                    '\\' in target or '..' in path.parts or path.suffix.lower() not in {'.md', '.txt'}):
                raise ValueError(f'Expected a relative Markdown/text instruction include: {target}')
            original = (root / path).read_bytes().decode('utf-8')
        else:
            original = scalar_line(value)
        combined = root / POLICY_MEMBER
        if combined.exists():
            raise ValueError(f'Reserved overlay file already exists: {POLICY_MEMBER}')
        combined.parent.mkdir(parents=True, exist_ok=True)
        combined.write_bytes((original + '\n\n' + policy_text + '\n').encode('utf-8'))
        updated = config[:key.start('value')] + '!include ' + POLICY_MEMBER + config[key.end():]
    root_yaml.write_bytes(updated.encode('utf-8'))


def validate_official(root, required):
    try:
        from adk_submission import validate_directory
        from swegemma.config import build_submission_limits
    except ModuleNotFoundError as error:
        if error.name not in {'adk_submission', 'swegemma'} or required:
            raise
        return 'unavailable'
    limits, _constraints = build_submission_limits()
    validate_directory(root, limits=limits)
    return 'passed'


def build(sample, output, policy, require_official=False):
    reject_link(sample)
    sample = sample.resolve(strict=True)
    output = output.absolute()
    if output.suffix.lower() != '.zip' or output.resolve().is_relative_to(sample):
        raise ValueError('Output must be a .zip outside the sample directory')
    source_paths = members(sample)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        for relative in source_paths:
            dest = stage / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(sample / relative, dest)
        if policy is not None:
            add_policy(stage, policy)
        paths = members(stage)
        official = validate_official(stage, require_official)
        with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as handle:
            pending = Path(handle.name)
        try:
            with zipfile.ZipFile(pending, 'w') as archive:
                for relative in paths:
                    entry = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.create_system = 3
                    entry.external_attr = 0o100644 << 16
                    entry.file_size = (stage / relative).stat().st_size
                    with (stage / relative).open('rb') as source, archive.open(entry, 'w') as dest:
                        shutil.copyfileobj(source, dest, length=1024 * 1024)
            with pending.open('rb') as saved:
                digest = hashlib.sha256()
                for chunk in iter(lambda: saved.read(1024 * 1024), b''):
                    digest.update(chunk)
            os.replace(pending, output)
        finally:
            pending.unlink(missing_ok=True)
    return {'output': str(output), 'sha256': digest.hexdigest(), 'files': len(paths),
            'variant': 'policy' if policy is not None else 'baseline', 'official_validation': official}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', required=True, type=Path, help='directory containing the sample agent.yaml')
    parser.add_argument('--output', required=True, type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--instruction', type=Path, default=DEFAULT_POLICY, help='text appended to root instructions')
    group.add_argument('--baseline', action='store_true', help='package the sample unchanged')
    parser.add_argument('--require-official-validation', action='store_true')
    args = parser.parse_args()
    try:
        report = build(args.sample, args.output, None if args.baseline else args.instruction,
                       args.require_official_validation)
    except (ValueError, OSError, ImportError) as error:
        sys.exit(f'Build failed: {error}')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
