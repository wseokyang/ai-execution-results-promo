from pathlib import Path
import json, hashlib
R=Path(__file__).resolve().parent
ROOT=R.parents[1]
V9=ROOT/'storyboards/2026-10-23_v9-caption-first'
paths=[p for p in V9.rglob('*') if p.is_file()]
paths += [ROOT/'storyboards/2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
baseline=[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p)} for p in paths if p.exists()]
(R/'preservation_baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
print('Preservation baseline:',len(baseline),'files')
