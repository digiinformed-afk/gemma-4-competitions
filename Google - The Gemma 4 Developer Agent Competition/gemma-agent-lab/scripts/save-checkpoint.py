"""Save an immutable, checksum-verified checkpoint of authored main-track work."""

from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
TOP_FILES = ('README.md', 'MAIN-TRACK-STATUS.md', 'server.mjs', 'package.json')
ARTIFACTS = ('submission.zip', 'scripted-smoke.json', 'main-track-pilot.ipynb')


def sources():
    paths = [ROOT / name for name in TOP_FILES]
    for folder in ('candidate', 'scripts', 'tests', 'dist'):
        paths.extend(path for path in (ROOT / folder).rglob('*')
                     if path.is_file() and '__pycache__' not in path.parts)
    paths.extend(ROOT / 'artifacts' / name for name in ARTIFACTS if (ROOT / 'artifacts' / name).is_file())
    return {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in sorted(paths)}


def verify(path, manifest):
    with zipfile.ZipFile(path) as archive:
        expected = sorted([*manifest, 'CHECKSUMS.json'])
        if sorted(archive.namelist()) != expected or archive.testzip():
            raise ValueError(f'Invalid checkpoint members: {path}')
        if json.loads(archive.read('CHECKSUMS.json')) != manifest:
            raise ValueError(f'Invalid checkpoint manifest: {path}')
        for name, digest in manifest.items():
            if sha256(archive.read(name)).hexdigest() != digest:
                raise ValueError(f'Checksum mismatch for {name}')


def save():
    files = sources()
    manifest = {name: sha256(data).hexdigest() for name, data in files.items()}
    record = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
    folder = ROOT / 'artifacts' / 'checkpoints'
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ('main-track-' + sha256(record).hexdigest()[:20] + '.zip')
    if not output.exists():
        with tempfile.NamedTemporaryFile(dir=folder, delete=False) as f:
            pending = Path(f.name)
        try:
            with zipfile.ZipFile(pending, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                for name, data in files.items():
                    archive.writestr(name, data)
                archive.writestr('CHECKSUMS.json', record)
            verify(pending, manifest)
            try:
                os.link(pending, output)
            except FileExistsError:
                pass
        finally:
            pending.unlink(missing_ok=True)
    verify(output, manifest)
    return output


if __name__ == '__main__':
    print(save())
