import sys,json,hashlib
from pathlib import Path
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image,ImageOps,ImageDraw
p=Path(__file__).resolve().parents[2]
m=p/'artist_C10_manifest.json'
d=json.loads(m.read_text('utf-8'))
source=json.loads((p/'storyboards_draft.json').read_text('utf-8-sig'))
scenes={s['scene_id']:s for s in source['scene_manifest'] if s['concept_id']=='C10'}
canvas=Image.new('RGB',(1280,1900),(22,23,28))
draw=ImageDraw.Draw(canvas)
for i,s in enumerate(d['scenes']):
    f=Path(s['actual_path'])
    im=Image.open(f)
    s['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
    s['dimensions']=list(im.size)
    s['subsequent_motion']=scenes[s['scene_id']]['subsequent_motion']
    s['camera_notes']=scenes[s['scene_id']]['camera']
    s['required_end_state']=scenes[s['scene_id']]['required_end_state']
    tile=ImageOps.contain(im.convert('RGB'),(620,349))
    x=(i%2)*640+10; y=(i//2)*380+24
    canvas.paste(tile,(x,y))
    draw.text((x,y-18),s['scene_id']+' / '+f.name,fill='white')
canvas.save(p/'contact_C10.jpg',quality=92)
m.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf-8')
print('10 images / contact / hashes / motion notes saved')
