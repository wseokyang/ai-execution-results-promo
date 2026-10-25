from pathlib import Path
import sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw,ImageFont
O=Path(__file__).parent;S=O.parent.parent;F=S/'2026-10-24_v12-C02-C04-C01-flow';V=O.parent;R=S/'2026-10-24_C01-C06-repair110'
q=O/'source_review';q.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',18)
for shot,p,ts in [('K02',F/'C04_K02_take01.mp4',[.5,1,1.5,2,2.5,3,3.5,4,4.5]),('K04',F/'C04_K04_take01.mp4',[.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5]),('K05',F/'C04_K05_take01.mp4',[.5,1,1.25,1.5,1.75,2,2.25,2.5,3,3.5,4,4.5]),('NOTE',V/'C04_K01_note_push_take01.mp4',[.5,1,1.5,2,3,4,5,5.5]),('BOWLS',R/'C04_K08_three_visible_take01.mp4',[2,2.5,3,3.5,4]),('SPOON',R/'C04_K09_take02.mp4',[.5,1,2,3,4,5,6])]:
 tiles=[]
 with av.open(str(p)) as c:
  for i,f in enumerate(c.decode(video=0)):
   if i not in [round(t*24) for t in ts]:continue
   im=f.to_image();im.save(q/f'{shot}_{i/24:.3f}.png')
   tile=Image.new('RGB',(640,390));tile.paste(im.resize((640,360)),(0,30));ImageDraw.Draw(tile).text((8,4),f'{shot} {i/24:.3f}',font=font,fill='white');tiles.append(tile)
 sheet=Image.new('RGB',(1280,390*((len(tiles)+1)//2)))
 for i,im in enumerate(tiles):sheet.paste(im,(i%2*640,i//2*390))
 sheet.save(q/f'{shot}.jpg',quality=94)
