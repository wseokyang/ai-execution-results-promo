import render_films as r
from PIL import Image, ImageDraw
cases=[('K03',1,'C06_K03_take01',1.5,10),('K04_wide',1,'C06_K04_take01',2,15.75),('K04_check',3,'C06_K04_check_take02',1.25,17.25),('K04_check',3,'C06_K04_check_take02',2.75,18.75),('K04_check',3,'C06_K04_check_take02',4.5,20.5),('K08',1,'C06_K08_take01',1.25,33.25),('K08',1,'C06_K08_take01',2.75,34.75),('K08',1,'C06_K08_take01',4,36),('K09_seat',1,'C06_K09_take01',4,41.75)]
cases += [('K05',2,'C06_K05_take03',1.25,21),('K07',1,'C06_K07_take01',1,29.75),('K07',1,'C06_K07_take01',2.5,31.25),('K07',1,'C06_K07_take01',4.25,33)]
out=r.OUT/'composite_previews'; out.mkdir(exist_ok=True)
for cut,run,name,st,t in cases:
 with r.av.open(str(r.SB/r.RUN[run]/(name+'.mp4'))) as c:
  for f in c.decode(video=0):
   if abs(float(f.time)-st)>.01: continue
   im=r.composite(f.to_image().convert('RGBA'),cut,st,t,'C06')
   for a,b,tx,pos in r.CAPTIONS['C06']:
    if a<=t<b: im.alpha_composite(r.caption(tx,pos))
   im.convert('RGB').save(out/f'{cut}_{st:.2f}.jpg',quality=96); break
print(out)
