from pathlib import Path
import sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
source=P.parent/'2026-10-19_C03-flow-run02/C03_K06_take01.mp4'
times=[0,.5,1,1.208,3.25,3.75,4.25,4.75,5.25,5.708]
folder=P/'wide_tracking_frames'
folder.mkdir(exist_ok=True)
with av.open(str(source)) as c:
 for f in c.decode(video=0):
  t=float(f.time)
  for a in times:
   if abs(t-a)<.015:
    f.to_image().save(folder/f'{a:.3f}s.png')
ims=sorted(folder.glob('*.png'))
sheet=Image.new('RGB',(1280,400*5),'#172026')
d=ImageDraw.Draw(sheet)
for i,p in enumerate(ims):
 im=Image.open(p).resize((640,360))
 x=(i%2)*640;y=(i//2)*400
 sheet.paste(im,(x,y+30));d.text((x+10,y+6),p.stem,fill='white')
sheet.save(P/'wide_pages_contact.jpg',quality=93)
print(str(P/'wide_pages_contact.jpg'))
