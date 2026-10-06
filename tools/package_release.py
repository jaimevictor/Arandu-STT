"""Package the existing HA App repository, excluding private/runtime files."""
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2.0.0'


def main():
    dest = ROOT / 'dist'
    dest.mkdir(exist_ok=True)
    archive = dest / f'arandu-stt-{VERSION}.zip'
    included = []
    top_level = ['README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'repository.yaml', 'CHANGELOG.md', '.gitignore', '.gitattributes']
    files = [ROOT/file for file in top_level]
    for directory in ('arandu_stt', '.github', 'tools'):
        files.extend((ROOT/directory).rglob('*'))
    ignored_parts = {'__pycache__', '.git', '.venv', 'models', 'hub', '.idea'}
    ignored_names = {'arandu_ha_inventory.json', 'metrics.jsonl', 'options.json', '.env'}
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in sorted(files):
            relative = path.relative_to(ROOT)
            if not path.is_file() or set(relative.parts) & ignored_parts or path.name in ignored_names or path.suffix in {'.pyc', '.log', '.onnx'}:
                continue
            output.write(path, f'arandu-stt-{VERSION}/' + relative.as_posix())
            included.append(relative.as_posix())
    with zipfile.ZipFile(archive) as check:
        if check.testzip() is not None:
            raise RuntimeError('Archive verification failed')
        expected = f'arandu-stt-{VERSION}/arandu_stt/config.yaml'
        if expected not in check.namelist():
            raise RuntimeError('HA App metadata missing from release')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.sha256').write_text(digest + '  ' + archive.name + '\n', encoding='ascii')
    print(f'{archive}\nfiles={len(included)} bytes={archive.stat().st_size} sha256={digest}')


if __name__ == '__main__':
    main()
