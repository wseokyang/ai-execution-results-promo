from pathlib import Path
import json,hashlib,re,datetime,subprocess
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[2];V=Path(__file__).resolve().parent;P=ROOT/'storyboards/2026-10-25_C07-C10-rewrite-v13';CACHE=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-final-six-v13-2026-10-25')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];films=read(V/'delivery_manifest.json')['films'];g=read(V/'generation_log.json')['entries'];scenes=read(P/'scene_manifest.json')['scenes'];d=read(P/'storyboards.json')
for f in films:
 p=V/f['file']
 if sha(p)!=f['sha256'] or sha(CACHE/p.name)!=f['sha256']:errors.append('film_hash:'+str(p))
 if not f['duration_seconds']<60:errors.append('film_duration:'+f['concept_id'])
for e in g:
 if sha(V/e['original'])!=e['sha256'] or sha(CACHE/'originals'/Path(e['original']).name)!=e['sha256']:errors.append('original_hash:'+e['original'])
for s in scenes:
 p=P/s['actual_file']
 if sha(p)!=s['sha256'] or sha(CACHE/s['actual_file'])!=s['sha256']:errors.append('scene_hash:'+str(p))
 if not s.get('prompt'):errors.append('missing_prompt:'+s['scene_id'])
for c in d['concepts']:
 prev=0
 for shot in c['shots']:
  if abs(shot['start']-prev)>0.001 or abs(shot['duration']-(shot['end']-shot['start']))>0.001:errors.append('timeline:'+shot['id'])
  prev=shot['end']
 if prev!=c['expected_duration_seconds'] or prev>=60:errors.append('story_duration:'+c['id'])
docs=[ROOT/'README.md',ROOT/'콘티_바로보기.md',ROOT/'00_완성_영상.md',ROOT/'00_새7-10_콘티.md',ROOT/'00_V13_보완_검수.md',ROOT/'00_영상제작_현재상태.md',ROOT/'00_제작전_최종검토.md']+sorted(p for p in ROOT.glob('[0-1][0-9]_*.md') if p.name[:2] in [f'{i:02}' for i in range(1,11)])
links=0
for p in docs:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
  if link.startswith(('https:','http:','#','mailto:')):continue
  target=unquote(link.strip('<>').split('#')[0]);links+=1
  if not (p.parent/target).exists():errors.append('markdown_link:'+p.name+':'+target)
for p in CACHE.glob('*.html'):
 for link in re.findall(r'(?:src|href)="([^"]+)"',p.read_text(encoding='utf-8')):
  if link.startswith(('https:','http:','#','data:')):continue
  target=unquote(link.split('#')[0]);links+=1
  if not (p.parent/target).exists():errors.append('html_link:'+p.name+':'+target)
report={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'films':len(films),'preserved_raws':len(g),'selected_first_frames':len(scenes),'new_storyboards':len(d['concepts']),'local_links_checked':links,'errors':errors,'checks':'Six final/cache SHA; twelve raw/cache SHA;40 first-frame/cache SHA and prompts; shot time coverage; root Markdown and static HTML links. Earlier full media decoding/PTS validation retained.','not_checked':'Browser render (file URL policy block), realtime playback, actual listening, venue display.'}
(V/'reviews/delivery_package_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
