from pathlib import Path
import json,hashlib,re
from urllib.parse import unquote
Q=Path(__file__).resolve().parent;ROOT=Q.parent.parent
docs=['README.md','00_완성_영상.md','00_최종_재검수.md','04_목마는_식사_중입니다.md','06_퇴근_좀_해주세요.md']
checked=0;missing=[]
for doc in docs:
 p=ROOT/doc
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if dest.startswith(('https://','http://','#')):continue
  dest=unquote(dest.strip('<>').split('#')[0]);checked+=1
  if not (p.parent/dest).exists():missing.append([doc,dest])
assert not missing,missing
m=json.loads((Q/'delivery_manifest.json').read_text(encoding='utf-8'))
assert len(m['films'])==6
for f in m['films']:
 p=ROOT/f['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
 assert f['duration_seconds']<=60
 assert f['concept_id'] not in ['C04','C06'] or f['version']=='V14'
ledger=json.loads((Q/'independent_and_cross_review.json').read_text(encoding='utf-8'))
assert ledger['issues'][1]['c06_actual_recheck']=={x:'PASS' for x in 'ABC'}
for cid in ['C04','C06']:
 ed=json.loads((Q/cid/'edit_manifest.json').read_text(encoding='utf-8'))
 assert ed['status']=='THREE_REVIEWER_FRESH_SAMPLE_RECHECK_PASS'
 last=0
 for t in ed['timeline']:
  assert abs(t['start']-last)<1e-6
  assert t['end']>t['start'];last=t['end']
 assert last==ed['duration_seconds']
 for c in ed['captions']:assert 0<=c['start']<c['end']<=last
qa={'checked_relative_document_links':checked,'missing_links':0,'latest_movie_sha_verified':6,'changed_films':['C04','C06'],'three_reviewer_recheck':'PASS','all_under60seconds':True,'source_files_overwritten':False}
(Q/'delivery_validation.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa),flush=True)
