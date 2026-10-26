from pathlib import Path
import sys, json, math
OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(OUT.parent))
from media_common import *
SOURCE=SB/'2026-10-26_C08-C09-flow-v15'
review=OUT/'source_review';review.mkdir(exist_ok=True)
reports=[]
previous={x['file']:x for x in json.loads((OUT/'source_metadata.json').read_text(encoding='utf8'))} if (OUT/'source_metadata.json').exists() else {}
for p in sorted(SOURCE.glob('C09_K*_take*.mp4')):
    if p.name in previous and previous[p.name]['sha256']==sha(p) and (OUT/f'{p.stem}_contact.jpg').exists():
        reports.append(previous[p.name]);continue
    tiles=[];times=[]
    with av.open(str(p)) as c:
        st=c.streams.video[0];audio=len(c.streams.audio)
        for i,f in enumerate(c.decode(video=0)):
            times.append(float(f.time))
            if i%12:continue
            im=f.to_image();im.save(review/f'{p.stem}_{i/24:04.2f}s.png')
            tile=Image.new('RGB',(384,244),(15,23,31));tile.paste(im.resize((384,216)),(0,28));ImageDraw.Draw(tile).text((8,3),f'{i/24:.2f}s',font=font(18),fill='white');tiles.append(tile)
        reports.append(dict(file=p.name,sha256=sha(p),frames=len(times),duration=len(times)/float(st.average_rate),fps=float(st.average_rate),resolution=[st.width,st.height],audio_streams=audio,full_video_decode='PASS',actual_listening_verified=False,actual_continuous_playback_verified=False))
    sheet=Image.new('RGB',(1536,244*math.ceil(len(tiles)/4)),(15,23,31))
    for i,im in enumerate(tiles):sheet.paste(im,(i%4*384,i//4*244))
    sheet.save(OUT/f'{p.stem}_contact.jpg',quality=94)
dump(OUT/'source_metadata.json',reports)
print(len(reports),'source movies inspected')
