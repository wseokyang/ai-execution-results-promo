from pathlib import Path
import sys,json,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image,ImageDraw,ImageFont,ImageOps
r=Path(__file__).resolve().parent;d=json.loads((r/'storyboards.json').read_text(encoding='utf8'));out=r/'caption_proofs';out.mkdir(exist_ok=True)
for c in d['concepts']:
 frames=[]
 for s in c['shots']:
  for i,q in enumerate(s.get('caption_cues',[])):
   im=Image.open(r/s['image_file']).convert('RGBA').resize((1280,720));b=q['box'];bw=1280*b['width_pct']/100;pad=1280*b.get('padding_pct',1)/100;inner=bw-1280*.026
   lines=[]
   def add(t,size,lh=1.4,col='white'):
    f=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',round(size*12.8));line=''
    for part in t.split('\n'):
     for ch in part:
      if line and f.getlength(line+ch)>inner:lines.append((line,f,round(size*12.8*lh),col));line=''
      line+=ch
     lines.append((line,f,round(size*12.8*lh),col));line=''
   if q.get('eyebrow'):add(q['eyebrow'],2.3,col='#d5efd1')
   t=q['text'].split('\n')
   if q.get('kind')=='event':add(t.pop(0),b.get('title_cqw',5),1.2)
   add('\n'.join(t),b.get('font_cqw',3.3))
   bh=sum(v[2]for v in lines)+2*pad;x=1280*b['left_pct']/100;y=720*b['top_pct']/100 if 'top_pct'in b else 720*(1-b['bottom_pct']/100)-bh
   overlay=Image.new('RGBA',im.size);dr=ImageDraw.Draw(overlay);dr.rectangle((x,y,x+bw,y+bh),fill=(0,0,0,204));cy=y+pad
   for t,f,lh,col in lines:dr.text((x+bw/2,cy+lh/2),t,font=f,fill=col,anchor='mm');cy+=lh
   im=Image.alpha_composite(im,overlay).convert('RGB');name=f'{c["id"]}_{s["id"]}_cue{i+1}';im.save(out/(name+'.jpg'),quality=93);frames.append((name,im))
 cw,ch=640,390;sheet=Image.new('RGB',(cw*2,ch*math.ceil(len(frames)/2)),'#172020');dr=ImageDraw.Draw(sheet);f=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',18)
 for i,(name,im)in enumerate(frames):
  x=i%2*cw;y=i//2*ch;sheet.paste(im.resize((640,360)),(x,y));dr.text((x+12,y+365),name,font=f,fill='white')
 sheet.save(out/(c['id']+'_captions.jpg'),quality=94)
print('Caption proof derivatives generated; source PNGs unchanged. PIL approximates browser font metrics; this command does not render-check HTML.')
