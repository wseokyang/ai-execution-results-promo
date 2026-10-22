"""Check the deliverable's timing, media preservation, source mapping and local links."""
from pathlib import Path
import json,csv,hashlib,re
from urllib.parse import unquote,urlsplit
R=Path(__file__).resolve().parent;ROOT=R.parents[1];SRC=R.parent/'2026-10-23_v10-ten-concepts'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=read(R/'storyboards.json');m=read(R/'scene_manifest.json');old=read(SRC/'scene_manifest.json')
issues=[]
def check(ok,detail):
 if not ok:issues.append(detail)
cs={c['id']:c for c in d['concepts']};us={u['id']:u for u in d['generation_units']};ims={e['id']:e for e in m['images']};oldims={e['id']:e for e in old['images']}
check(len(cs)==10 and len(us)==88 and sum(len(c['shots']) for c in cs.values())==87,'Wrong concept/shot/unit counts')
durations={};cue_count=0;mirror_count=0
for cid,c in cs.items():
 cursor=0;ss={s['id']:s for s in c['shots']}
 for s in c['shots']:
  check(abs(s['start']-cursor)<1e-6,f'{cid}/{s["id"]}: gap/overlap')
  check(abs(s['end']-s['start']-s['duration'])<1e-6,f'{cid}/{s["id"]}: duration')
  cursor=s['end']
  for q in s['caption_cues']:
   cue_count+=1
   check(s['start']<=q['start']<q['end']<=s['end'],f'{cid}/{s["id"]}: cue outside shot')
   b=q['box'];check(0<=b['left_pct'] and b['left_pct']+b['width_pct']<=100,f'{cid}/{s["id"]}: horizontal bounds')
 for a in c.get('text_assets',[]):
  if 'cues' in a:
   mirror_count+=len(a['cues']);check(a['cues']==ss[a['cut']]['caption_cues'],f'{cid}/{a["cut"]}: stale caption mirror')
 check(cursor==c['duration_seconds'] and cursor<=60,f'{cid}: total duration')
 durations[cid]=cursor
check(durations==dict(zip(cs,[37.5,39,44.75,37,43,44,39,41,44,46])),'Unexpected duration totals')
rows={r['unit_id']:r for r in csv.DictReader((R/'production_units.tsv').open(encoding='utf-8-sig'),delimiter='\t')}
for uid,u in us.items():
 e=ims[uid];s=next(s for s in cs[u['concept_id']]['shots'] if s['id']==u['linked_shot'])
 check(e['next_motion']==u['action'] and e['camera_notes']==u['framing'],uid+': unit/manifest action mismatch')
 check(0<float(rows[uid]['editorial_used_seconds'])<=float(rows[uid]['source_clip_seconds_planned'])==8,uid+': source plan too short')
 check(float(rows[uid]['editorial_used_seconds'])==u['editorial_used_seconds'],uid+': TSV use length')
 check(sha(R/e['image_path'])==sha(SRC/oldims[uid]['image_path']),uid+': source PNG changed')
 check(e['prompt']==oldims[uid]['prompt'],uid+': historical image prompt changed')
 check((R/rows[uid]['prompt_file']).is_file(),uid+': missing prompt')
 if uid in ('C05_K02A','C05_K02B'):
  check(e['continuity_in']==u['continuity_in'] and e['continuity_out']==u['continuity_out'],uid+': split continuity mirrors')
  t=(R/rows[uid]['prompt_file']).read_text(encoding='utf8')
  check('Outgoing continuity: '+u['continuity_out'] in t,uid+': split continuity prompt')
check(us['C05_K02A']['editorial_used_seconds']+us['C05_K02B']['editorial_used_seconds']==7,'C05 split sum')
baseline=read(R/'preservation_baseline.json')
for e in baseline:check(sha(ROOT/e['path'])==e['sha256'].lower(),'Preserved source changed: '+e['path'])
media=list(R.rglob('*.mp4'))+list(R.rglob('*.wav'))+list(R.rglob('*.mp3'))
check(not media,'Unexpected new audiovisual files')
link_count=0
files=list(R.glob('*.md'))+list(R.glob('*.html'))+[ROOT/'README.md',ROOT/'콘티_바로보기.md',ROOT/'00_제작전_최종검토.md']+list(ROOT.glob('[0-9][0-9]_*.md'))
for p in set(files):
 t=p.read_text(encoding='utf8')
 targets=re.findall(r'\]\(([^)]+)\)',t) if p.suffix=='.md' else re.findall(r'(?:src|href)=["\']([^"\']+)',t)
 for url in targets:
  url=url.strip('<>');parts=urlsplit(url)
  if parts.scheme or not parts.path or '${' in url:continue
  link_count+=1;check((p.parent/unquote(parts.path)).exists(),f'Broken link {p.relative_to(ROOT)} -> {url}')
result={'status':'PASS' if not issues else 'FAIL','concepts':len(cs),'editorial_shots':87,'source_units':len(us),'caption_cues':cue_count,'synchronized_caption_mirrors':mirror_count,'durations':durations,'selected_pngs_identical_to_v10':88,'preserved_files_checked':len(baseline),'local_links_checked':link_count,'flow_requests':0,'new_video_audio_files':len(media),'issues':issues,'scope':'Data/paths/hashes/timing checks. Actual image inspection and independent editorial judgments are recorded in review_summary.json. No actual moving-video or browser-render validation claimed.'}
(R/'preproduction_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2));assert not issues
