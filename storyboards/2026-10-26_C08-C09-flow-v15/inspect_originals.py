from pathlib import Path
import sys,json,hashlib,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent
font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',18)
reports=[]
for p in sorted(OUT.glob('C*_take*.mp4')):
    samples=[]; times=[]
    with av.open(str(p)) as c:
        st=c.streams.video[0]; audio=len(c.streams.audio)
        for i,f in enumerate(c.decode(video=0)):
            times.append(float(f.time))
            if i%12==0:
                im=f.to_image(); card=Image.new('RGB',(384,244),(15,20,25));card.paste(im.resize((384,216)),(0,28));ImageDraw.Draw(card).text((8,3),f'{float(f.time):.2f}s',font=font,fill='white');samples.append(card)
        meta=dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),frames=len(times),duration_seconds=round(len(times)/float(st.average_rate),4),fps=float(st.average_rate),resolution=[st.width,st.height],audio_streams=audio,full_video_decode='PASS',actual_listening_verified=False,continuous_playback_verified=False)
    sheet=Image.new('RGB',(384*4,244*math.ceil(len(samples)/4)),(15,20,25))
    for i,im in enumerate(samples):sheet.paste(im,((i%4)*384,(i//4)*244))
    sheet.save(OUT/(p.stem+'_contact.jpg'),quality=93)
    reports.append(meta)
(OUT/'technical_validation.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(reports,ensure_ascii=False,indent=2))
