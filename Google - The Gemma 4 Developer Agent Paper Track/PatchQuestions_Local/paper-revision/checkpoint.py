"""Save a member-hashed, content-addressed recovery archive."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent / 'public/project'


def main():
    entries = {}
    for base, prefix in [(ROOT, 'paper-revision'), (PAPER, 'paper')]:
        for p in sorted(base.rglob('*')):
            rel = p.relative_to(base)
            if not p.is_file() or any(part in {'checkpoints', '__pycache__', 'kernel-runtime', 'notebook-work'} for part in rel.parts):
                continue
            if p.suffix in {'.zip', '.pyc'}:
                continue
            entries[prefix + '/' + rel.as_posix()] = p.read_bytes()
    manifest = [{'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for name, data in sorted(entries.items())]
    raw = json.dumps(manifest, sort_keys=True, indent=2).encode()
    key = hashlib.sha256(raw).hexdigest()[:20]
    folder = ROOT / 'checkpoints'
    folder.mkdir(exist_ok=True)
    target = folder / f'paper-{key}.zip'
    if not target.exists():
        with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED) as z:
            for name, data in sorted(entries.items()):
                z.writestr(name, data)
            z.writestr('CHECKPOINT-MANIFEST.json', raw)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for item in manifest:
            assert hashlib.sha256(z.read(item['path'])).hexdigest() == item['sha256']
    (ROOT / 'LATEST-CHECKPOINT.txt').write_text(target.name + '\n', encoding='utf-8')
    print(json.dumps({'checkpoint': str(target), 'files': len(entries), 'verified': True}))


if __name__ == '__main__':
    main()
