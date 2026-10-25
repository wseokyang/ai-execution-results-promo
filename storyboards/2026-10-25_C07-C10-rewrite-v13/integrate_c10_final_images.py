from pathlib import Path
import json, hashlib, sys
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
m=read(P/'artist_C10_manifest.json')
fix=read(P/'artist_C10_curtain_fix.json')
for e in fix['scenes']:
 s=next(x for x in m['scenes'] if x['scene_id']==e['scene_id'])
 s.setdefault('previous_selected',[])
 if isinstance(s['previous_selected'],dict): s['previous_selected']=[s['previous_selected']]
 if s['actual_path'] != e['actual_path']:
  s['previous_selected'].append({k:s.get(k) for k in ['actual_path','sha256','prompt','reference_images']})
 s.update(actual_path=e['actual_path'],relative_image_path=Path(e['actual_path']).relative_to(P).as_posix(),sha256=e['sha256'],prompt=e['final_prompt'],reference_images=e['reference_images'],source_generated_image=e['source_generated_image'],review_status='CORRECTED; THREE_REVIEWER_FINAL_RECHECK_PENDING',review_notes=e['review_notes'])
 assert hashlib.sha256(Path(s['actual_path']).read_bytes()).hexdigest()==s['sha256']
m['known_limitations']=['Still first-frame review; actual Flow action and final video composition remain unverified.','C10 final image corrections and caption proof are awaiting independent final reconfirmation.']
(P/'artist_C10_manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
canvas=Image.new('RGB',(1440,5*440),(22,22,22));draw=ImageDraw.Draw(canvas)
for i,s in enumerate(m['scenes']):
 im=Image.open(s['actual_path']).convert('RGB'); im.thumbnail((710,404))
 x=(i%2)*720;y=(i//2)*440
 canvas.paste(im,(x,y+25));draw.text((x+8,y+5),s['scene_id']+' '+Path(s['actual_path']).name,fill='white')
canvas.save(P/'contact_C10.jpg',quality=92)
print('C10 selection updated; contact sheet rebuilt')
