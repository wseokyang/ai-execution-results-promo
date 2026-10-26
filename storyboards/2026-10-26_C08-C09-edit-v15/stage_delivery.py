"""Stage only this delivery's assets and navigation; leave prior work untouched."""
from pathlib import Path
import subprocess,json
E=Path(__file__).resolve().parent;ROOT=E.parent.parent
dirs=[ROOT/'storyboards'/n for n in [
 '2026-10-26_C01-C07-C10-rewrite-v15','2026-10-26_C08-C09-edit-v15',
 '2026-10-26_C08-C09-flow-v15','2026-10-26_screening-style-v15']]
files=[]
for folder in dirs:
    for p in folder.rglob('*'):
        if not p.is_file():continue
        parts=p.relative_to(folder).parts
        if any(x in parts for x in ['__pycache__','review_frames','source_review']):continue
        if 'Zone.Identifier' in p.name or 'picture' in p.name.lower():continue
        if p.name in ['render_stderr.txt','PREPARATION_STATUS.md','source_metadata_partial.json']:continue
        if p.suffix=='.mp4' and folder==E and 'screening_v15' not in p.name:continue
        if p.suffix not in ['.json','.md','.html','.py','.txt','.srt','.png','.jpg','.mp4','.wav']:continue
        files.append(p)
names=['README.md','RESUME_CODEX.txt','00_완성_영상.md','00_새1-7-10_콘티.md','00_V15_제작_검수.md',
 '콘티_바로보기.md','01_감독님_아직인데요.md','07_셰프님_그것도_주세요.md','10_지구_대표_질문_있습니다.md',
 '01_성공_자세_교정원.md','07_불량도_이직합니다.md','10_비법_공개_금지.md',
 '00_새7-10_콘티.md','00_영상제작_현재상태.md','00_최종_재검수.md',
 '08_구조는_끝났습니다.md','09_나_없이도_괜찮겠어요.md']
files += [ROOT/n for n in names]
files += list((ROOT/'archive/v14-root-before-v15').glob('*.md'))
files=sorted(set(files))
assert all(p.exists() for p in files)
large=[str(p.relative_to(ROOT)) for p in files if p.stat().st_size>=100*1024*1024]
assert not large,large
paths=[p.relative_to(ROOT).as_posix() for p in files]
cache=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-V15-delivery-2026-10-26');cache.mkdir(parents=True,exist_ok=True)
lst=cache/'git_paths.nul';lst.write_bytes(b'\0'.join(p.encode('utf-8') for p in paths)+b'\0')
safe='%(prefix)///wsl.localhost/Ubuntu-24.04/home/wooseok/wsy/samsung_related/slide/AI실행결과발표대회_디자인3종'
subprocess.run(['git','-c','safe.directory='+safe,'add','--pathspec-from-file='+str(lst),'--pathspec-file-nul'],cwd=ROOT,check=True)
print(json.dumps({'staged_files_selected':len(paths),'bytes':sum(p.stat().st_size for p in files),'largest_mib':max(p.stat().st_size for p in files)/1048576},ensure_ascii=False))
