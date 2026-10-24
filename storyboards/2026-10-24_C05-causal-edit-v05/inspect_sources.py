from pathlib import Path
import sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent
SB=OUT.parent
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',17)
paths=[('N04','2026-10-24_C05-first-flow-run01/C05_N04_take01.mp4',.5,2),('jack','2026-10-23_C06-C05-flow-run01/C05_K04_take02.mp4',1,2.5)]
for name,p,a,b in paths:
 tiles=[]
 for i,f in enumerate(av.open(str(SB/p)).decode(video=0)):
  t=float(f.time)
  if t<a or t>=b or i%3:continue
  im=f.to_image()
  if name=='jack':im=im.crop((896,396,1280,612))
  im=im.resize((480,270))
  tile=Image.new('RGB',(480,300),(15,20,28));tile.paste(im,(0,30));ImageDraw.Draw(tile).text((5,4),f'{name} {t:.3f}s',font=font,fill='white');tiles.append(tile)
 sheet=Image.new('RGB',(1440,300*((len(tiles)+2)//3)),(15,20,28))
 for i,tile in enumerate(tiles):sheet.paste(tile,((i%3)*480,(i//3)*300))
 sheet.save(OUT/f'preflight_{name}.jpg',quality=94)
