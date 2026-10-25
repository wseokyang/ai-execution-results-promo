import render_c02 as r
from pathlib import Path
import av,numpy as np
from PIL import Image,ImageDraw
out=r.OUT/'tail_composite_probe.mp4'
segments=[('K07','K07_take02',1.5,4.25),('K08','K08_take01',.5,3.5),('K09','K09_take01',4,6.5)]
thumb=[];n=0
with av.open(str(out),'w') as c:
 st=c.add_stream('libx264',rate=24);st.width=1280;st.height=720;st.pix_fmt='yuv420p';st.options={'crf':'18'}
 for sh,file,a,b in segments:
  with av.open(str(r.F/f'C02_{file}.mp4')) as src:
   for frame in src.decode(video=0):
    t=float(frame.time)
    if t<a-1e-5:continue
    if t>=b-1e-5:break
    im=Image.fromarray(r.picture(np.array(frame.to_image()),sh,t))
    for p in st.encode(av.VideoFrame.from_image(im)):c.mux(p)
    if n%6==0:
     card=Image.new('RGB',(426,265),(13,22,30));card.paste(im.resize((426,240)),(0,25));ImageDraw.Draw(card).text((5,2),f'{sh} source {t:.3f}s',font=r.font(15),fill='white');thumb.append(card)
    n+=1
 for p in st.encode():c.mux(p)
for j in range(0,len(thumb),12):
 batch=thumb[j:j+12];sheet=Image.new('RGB',(1278,265*((len(batch)+2)//3)))
 for k,im in enumerate(batch):sheet.paste(im,(k%3*426,k//3*265))
 sheet.save(r.OUT/f'tail_probe_{j//12+1:02d}.jpg',quality=94)
print(n)
