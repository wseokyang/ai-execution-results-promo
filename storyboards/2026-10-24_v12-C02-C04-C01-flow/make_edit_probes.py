from pathlib import Path
import sys,json,subprocess
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw
r=Path(__file__).parent; out=r/'edit_probes';out.mkdir(exist_ok=True)
jobs={'C02_K05_K06_join': [('C02_K05_take01.mp4',0,3),('C02_K06_take01.mp4',0,2)],
      'C02_K04_clean_button': [('C02_K04_take01.mp4',1,2.5),('C02_K04_take01.mp4',4.5,6)],
      'C02_K09_revised_ending': [('C02_K09_take01.mp4',4,6.5)]}
records=[]
for name,segments in jobs.items():
    dst=out/(name+'.mp4'); frames=[]
    for file,start,end in segments:
        with av.open(str(r/file)) as con:
            for i,f in enumerate(con.decode(video=0)):
                if round(start*24)<=i<round(end*24): frames.append(f.to_image())
    with av.open(str(dst),'w') as con:
        st=con.add_stream('libx264',rate=24);st.width=1280;st.height=720;st.pix_fmt='yuv420p';st.options={'crf':'18'}
        for im in frames:
            for pkt in st.encode(av.VideoFrame.from_image(im)):con.mux(pkt)
        for pkt in st.encode():con.mux(pkt)
    pick=sorted(set(list(range(0,len(frames),12))+[71,72,73] if len(frames)>73 else list(range(0,len(frames),6))))
    pick=[i for i in pick if i<len(frames)]
    contact=Image.new('RGB',(1280,204*((len(pick)+3)//4)),(12,20,26));draw=ImageDraw.Draw(contact)
    for k,i in enumerate(pick):
        x=(k%4)*320;y=(k//4)*204;contact.paste(frames[i].resize((320,180)),(x,y+24));draw.text((x+4,y+4),f'{i/24:.3f}s',(255,255,255))
    contact.save(out/(name+'_contact.jpg'),quality=92)
    with av.open(str(dst)) as con: n=sum(1 for f in con.decode(video=0))
    records.append({'name':name,'source_segments':segments,'frames':n,'duration':n/24,'audio':'none','status':'EDIT_PROBE_REVIEW_PENDING','note':'Real generated source intervals only; no image animation, interpolation, reverse or speed change.'})
(out/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(records)
