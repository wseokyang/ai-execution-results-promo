from pathlib import Path
import json
from PIL import Image,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
d=json.loads((R/'storyboards.json').read_text(encoding='utf-8-sig'))
m=json.loads((R/'scene_manifest.json').read_text(encoding='utf-8-sig'))
mapping={(x['concept_id'],x['cut_id']):x['image_path'] for x in m['images']}
font='C:/Windows/Fonts/malgun.ttf'
H=ImageFont.truetype(font,36);T=ImageFont.truetype(font,22);S=ImageFont.truetype(font,17)
im=Image.new('RGB',(1536,842),'#f3efe6');draw=ImageDraw.Draw(im)
draw.text((24,16),'3번 유지 · 나머지 네 이야기는 새로',font=H,fill='#252720')
draw.text((26,65),'V5 · 컷별 실제 첫 프레임과 시나리오',font=S,fill='#67645b')
for i,c in enumerate(d['concepts']):
 x=24+(i%3)*504;y=112+(i//3)*354
 with Image.open(R/mapping[c['id'],d['hero_cuts'][c['id']]]) as src:pic=ImageOps.contain(src.convert('RGB'),(480,270))
 im.paste(pic,(x+(480-pic.width)//2,y+(270-pic.height)//2))
 draw.text((x,y+277),f"{i+1:02d}  {c['title']}",font=T,fill='#252720')
 draw.text((x,y+311),f"{'유지' if c['id']=='C03' else '새 안'} · {c['duration_seconds']}초 · {len(c['shots'])}컷",font=S,fill='#7e3324')
draw.text((1040,530),'3번 콘티·이미지 그대로',font=T,fill='#252720')
draw.text((1040,576),'기존 완성 1번 영상 보존',font=S,fill='#67645b')
draw.text((1040,612),'동영상 생성 없음',font=T,fill='#7e3324')
im.save(R/'overview.jpg',quality=94)
