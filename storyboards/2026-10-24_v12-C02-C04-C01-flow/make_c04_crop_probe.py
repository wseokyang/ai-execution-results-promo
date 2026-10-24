from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw
r=Path(__file__).parent;out=r/'edit_probes';src=r/'C04_K08_take02.mp4'
frames=[]; crop=(600,20,1112,308)
with av.open(str(src)) as con:
 for f in con.decode(video=0): frames.append(f.to_image().crop(crop).resize((1280,720),Image.Resampling.LANCZOS))
dst=out/'C04_K08_three_windows_crop.mp4'
with av.open(str(dst),'w') as con:
 st=con.add_stream('libx264',rate=24);st.width=1280;st.height=720;st.pix_fmt='yuv420p';st.options={'crf':'18'}
 for im in frames:
  for pkt in st.encode(av.VideoFrame.from_image(im)):con.mux(pkt)
 for pkt in st.encode():con.mux(pkt)
sheet=Image.new('RGB',(1280,816));d=ImageDraw.Draw(sheet)
for k,i in enumerate(range(0,len(frames),12)):
 x=k%4*320;y=k//4*204;sheet.paste(frames[i].resize((320,180)),(x,y+24));d.text((x+3,y+4),f'{i/24:.2f}s',fill='white')
sheet.save(out/'C04_K08_three_windows_crop_contact.jpg',quality=94)
(out/'C04_crop_manifest.json').write_text(json.dumps({'source':src.name,'crop_xywh':[600,20,512,288],'output':dst.name,'duration':8,'frames':len(frames),'audio':'none','purpose':'Editorial insert of three front windows. Exclude unintended fourth side figure. Original preserved. Full 8s probe, not final edit selection.','status':'REVIEW_PENDING'},ensure_ascii=False,indent=2),encoding='utf-8')
print(dst)
