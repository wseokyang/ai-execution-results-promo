from pathlib import Path
import json, hashlib, collections, re
from urllib.parse import unquote
from PIL import Image
R=Path(__file__).resolve().parent;S=R.parent/'2026-10-19_tone-polish-v8'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
snap=read(R/'source_snapshot.json');p=read(R/'production_plan.json');m=read(R/'clip_manifest.json')
assert sha(S/'storyboards.json')==snap['storyboards_sha256']
for i in snap['images']:assert sha(R/i['path'])==i['sha256'],i
assert len(p['cuts'])==43 and len(m['visual_units'])==44 and len(m['audio_reserve'])==3
counts=dict(collections.Counter(u['concept_id'] for u in m['visual_units']))
assert counts=={'C01':9,'C02':9,'C03':8,'C04':9,'C05':9}
assert set(c['id'] for c in p['cuts'])==set(u['cut_id'] for u in m['visual_units'])
assert len(set(u['id'] for u in m['visual_units']))==44
dims=collections.Counter()
for c in p['cuts']:
 with Image.open(R/c['source_image']) as im:
  im.verify()
 with Image.open(R/c['source_image']) as im:dims[str(im.size)]+=1
deps=[]
for u in m['visual_units']:
 assert u['generation_seconds'] in [4,6,8] and u['status']=='not_submitted'
 assert (R/'prompts'/(u['id']+'.txt')).is_file()
 if u['source_image']:assert (R/u['source_image']).is_file()
 else:deps.append({'id':u['id'],'status':u['input_state']})
assert {d['id'] for d in deps}=={'C01_K04','C05_K02B'}
assert 'K04로 컷' not in (R/'prompts/C01_K03.txt').read_text(encoding='utf-8')
assert '34초' not in (R/'prompts/C05_K08.txt').read_text(encoding='utf-8')
a=next(u for u in m['visual_units'] if u['id']=='C05_K02A');assert '접어' not in a['framing']
k=next(c for c in p['cuts'] if c['id']=='C04_K05')
assert k['speech'][0]['speaker']=='C04_RC' and k['speech'][0]['route']=='화면 내 해당 배우의 자연 발화'
assert 'C04_RC' not in k['silent_actors']
assert len(read(R/'voice_bible.json')['tail_sources'])==3
missing=[]
for target in re.findall(r'\]\(([^)]+)\)',(R/'FLOW_PREFLIGHT.md').read_text(encoding='utf-8')):
 if target.startswith(('https:','http:','#')):continue
 if not (R/unquote(target.split('#')[0])).exists():missing.append(target)
assert not missing,missing
old=R.parent/'2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4'
assert sha(old)=='b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c'
assert not any(x.suffix.lower() in ['.mp4','.wav','.mp3','.png'] for x in R.rglob('*'))
out={'status':'passed','checks':{'source_storyboards_bytes_unchanged':True,'selected_images_unchanged':43,'images_opened_for_integrity':43,'image_dimensions':dict(dims),'ratio_note':'PNG dimensions are near16:9 with rounding under0.2%; verify live upload crop does not cut hands or title space. Originals unchanged.','cut_coverage':43,'visual_units':44,'by_concept':counts,'audio_reserve':3,'tail_audio_sources':3,'draft_prompts':44,'no_broken_report_links':True,'known_prompt_conflicts_resolved':True,'previous_finished_film_unchanged':True,'new_media_generated':0,'flow_requests_submitted':0},'production_input_dependencies':deps,'limits':'Static artifacts and source integrity only. No actual generated motion, audio listening, lip sync, current account UI, cost or model availability test.'}
(R/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
