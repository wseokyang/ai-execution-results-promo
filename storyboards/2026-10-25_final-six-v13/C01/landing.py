from pathlib import Path
import sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;f=p.parents[1]/'2026-10-24_v12-C02-C04-C01-flow'
for key,a,b in [('K04',3.25,4),('K06',3,3.75)]:
 with av.open(str(f/f'C01_{key}_take01.mp4')) as c:frames=[q.to_image() for q in c.decode(video=0)]
 ids=list(range(round(a*24),round(b*24),3));sheet=Image.new('RGB',(384*len(ids),242),(20,20,20))
 for j,i in enumerate(ids):
  im=frames[i];im=im.resize((384,216));sheet.paste(im,(j*384,26));ImageDraw.Draw(sheet).text((j*384+5,5),f'{key} {i/24:.3f}',fill='white')
 sheet.save(p/f'{key}_landing_strip.jpg')
