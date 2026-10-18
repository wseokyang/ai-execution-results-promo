"""Create a verified offline copy and ZIP; preserve the source package."""
from pathlib import Path
import json
import hashlib
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
BASE = Path('C:/Users/wseok/.codex/visualizations/2026/10/18/01a13daf-3732-7b90-99a8-92c605090d35')
DEST = BASE / 'B_comedy_story_reset_v4'
ZIP = BASE / 'B_comedy_story_reset_v4_full_package.zip'

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda:stream.read(1024*1024),b''):
            h.update(part)
    return h.hexdigest()

def main():
    status=json.loads((ROOT/'delivery_status.json').read_text(encoding='utf-8'))
    validation=json.loads((ROOT/'validation.json').read_text(encoding='utf-8'))
    assert status['status']=='complete' and validation['status']=='passed'
    files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.zip'}]
    BASE.mkdir(parents=True,exist_ok=True)
    for source in files:
        target=DEST/source.relative_to(ROOT)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
        assert digest(source)==digest(target)
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4) as archive:
        for source in files:
            archive.write(source,'B_comedy_story_reset_v4/'+source.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
    report={'folder':str(DEST),'html':str(DEST/'index.html'),'zip':str(ZIP),'files':len(files),'zip_bytes':ZIP.stat().st_size,'zip_sha256':digest(ZIP),'copy_hashes':'passed','zip_crc':'passed'}
    (BASE/'B_comedy_story_reset_v4_package_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
