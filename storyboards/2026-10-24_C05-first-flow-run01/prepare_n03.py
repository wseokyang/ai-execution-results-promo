from pathlib import Path
import json,hashlib,shutil
r=Path('storyboards/2026-10-24_C05-first-flow-run01')
src=r/'frames/C05_N02_take02/15_7.500s.png'
dest=r/'inputs/C05_N03.png'
shutil.copy2(src,dest)
shutil.copy2(src,Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v12-2026-10-24/C05_N03.png'))
(r/'submitted_prompts/C05_N03_take01.txt').write_text("8-second continuous locked-camera continuation of the supplied frame. The red fabric creature is trapped with its bent neck under the attached concrete porch, holding the FRONT FACE of the roof. It changes that grip, without lifting the roof. First both hands slide vertically DOWN the front fascia. When the fingers reach the lower edge, both wrists turn so the palms face UP, and the flat palms tuck just UNDER the concrete slab. The elbows bend below the roof. Show the palms pressing the horizontal ceiling underside, with every finger below the slab. ONLY AFTER this underside support is established, the creature ducks its long neck DOWN a little, freeing the neck from contact while its hands keep supporting the same stationary roof. It stays crouched facing the same way. Hold the clear neck gap and two supporting palms at the end. The roof remains fixed to the building and the right column; never lift, remove, rotate, break or drop it. No body turn, no extra limbs, no dialogue, voice, text, subtitles or music.",encoding='utf-8')
p=r/'generation_log.json'; d=json.loads(p.read_text(encoding='utf-8-sig'))
d['status']='N03_PREPARED_NOT_SUBMITTED'
d['balance_end_observed']=220
for e in d['entries']:
 if e['unit_id']=='C05_N02' and e['take']==2:
  e['review']='HOLD_AS_FINISHED_SUPPORT; usable only as arms-rising intermediate. Actual palms on fascia, neck trapped. C independent review agrees. No roof detachment observed.'
d['entries'].append({'unit_id':'C05_N03','take':1,'input':'inputs/C05_N03.png','input_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':'N02take02 actual frame 7.500s','prompt':'submitted_prompts/C05_N03_take01.txt','status':'PREPARED_NOT_SUBMITTED','balance_before':220,'model':'Veo 3.1 Lite','cost_displayed':10,'duration_requested':8,'resolution_requested':'720p','ratio_requested':'16:9','outputs':1,'repair_reason':'Distinct continuation: move grip from fascia to underside then lower neck; N02 not regenerated.'})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
