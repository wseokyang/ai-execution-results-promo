from pathlib import Path
import sys,json
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw
r=Path(__file__).parent;out=r/'edit_probes'
jobs={
 'C01_fall_photo_imitation_join':[('C01_K06_take01.mp4',1.5,4.25,None),('C01_K07_take01.mp4',0,3.5,None),('C01_K08_take01.mp4',0,3,None)],
 'C01_K09_no_door_crop':[('C01_K09_take01.mp4',0,8,(288,80,1280,638))],
 'C04_K08_selected_windows':[('C04_K08_take02.mp4',1,3.25,(600,20,1112,308))]
}
rows=[]
for name,segments in jobs.items():
 frames=[]
 for file,start,end,crop in segments:
  with av.open(str(r/file)) as con:
   for i,f in enumerate(con.decode(video=0)):
    if round(start*24)<=i<round(end*24):
     im=f.to_image()
     if crop: im=im.crop(crop).resize((1280,720),Image.Resampling.LANCZOS)
     frames.append(im)
 dst=out/(name+'.mp4')
 with av.open(str(dst),'w') as con:
  st=con.add_stream('libx264',rate=24);st.width=1280;st.height=720;st.pix_fmt='yuv420p';st.options={'crf':'18'}
  for im in frames:
   for pkt in st.encode(av.VideoFrame.from_image(im)):con.mux(pkt)
  for pkt in st.encode():con.mux(pkt)
 picks=list(range(0,len(frames),12));sheet=Image.new('RGB',(1280,204*((len(picks)+3)//4)))
 for k,i in enumerate(picks):
  x=k%4*320;y=k//4*204;sheet.paste(frames[i].resize((320,180)),(x,y+24));ImageDraw.Draw(sheet).text((x+4,y+4),f'{i/24:.3f}s',fill='white')
 sheet.save(out/(name+'_contact.jpg'),quality=93)
 with av.open(str(dst)) as con:n=sum(1 for _ in con.decode(video=0))
 rows.append({'name':name,'source_segments':segments,'frames':n,'duration':n/24,'decode':'PASS','audio':'none','originals_reencoded':False,'status':'REVIEW_PENDING'})
(out/'final_probe_manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(rows)
