"""Copy the completed planning package to a Windows-readable preview folder."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
PREVIEW = Path('C:/Users/wseok/.codex/visualizations/2026/10/16/01a13daf-3732-7b90-99a8-92c605090d35')
DEST = PREVIEW / 'B_comedy_reboot_v3'
ARCHIVE = PREVIEW / 'B_comedy_reboot_v3_full_package.zip'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda: f.read(1024*1024), b''):
            h.update(part)
    return h.hexdigest()

def main():
    validation = json.loads((ROOT/'validation.json').read_text(encoding='utf-8'))
    status = json.loads((ROOT/'delivery_status.json').read_text(encoding='utf-8'))
    assert validation['status'] == 'passed' and status['status'] == 'complete'
    files = [p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc', '.zip'}]
    for source in files:
        target = DEST / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        assert digest(source) == digest(target), str(target)
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=4) as output:
        for source in files:
            output.write(source, 'B_comedy_reboot_v3/' + source.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(ARCHIVE) as check:
        assert check.testzip() is None
    report = {'folder':str(DEST), 'html':str(DEST/'index.html'), 'zip':str(ARCHIVE), 'files':len(files), 'archive_bytes':ARCHIVE.stat().st_size, 'archive_sha256':digest(ARCHIVE), 'copy_hash_check':'passed', 'zip_crc_check':'passed'}
    (PREVIEW/'B_comedy_reboot_v3_package_verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
