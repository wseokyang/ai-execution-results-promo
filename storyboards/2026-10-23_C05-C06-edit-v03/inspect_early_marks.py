import render_films as r
from PIL import Image,ImageDraw
cards=[]
with r.av.open(str(r.SB/r.RUN[1]/'C06_K07_take01.mp4')) as con:
 for f in con.decode(video=0):
  t=float(f.time)
  if t<.5: continue
  if t>1.25: break
  im=r.clean_laptop_mark(f.to_image().convert('RGBA'),t)
  card=Image.new('RGB',(420,340),(10,18,25)); card.paste(im.crop((185,285,325,390)).resize((420,315)),(0,25))
  ImageDraw.Draw(card).text((10,2),f'source {t:.3f} / output {t+28.75:.3f}',font=r.font(17),fill='white'); cards.append(card)
out=r.OUT/'early_mark_check.jpg'; sheet=Image.new('RGB',(420*4,340*((len(cards)+3)//4)),(10,18,25))
for i,card in enumerate(cards): sheet.paste(card,((i%4)*420,(i//4)*340))
sheet.save(out,quality=95)
print(out)
