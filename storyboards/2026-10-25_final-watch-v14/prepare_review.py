from pathlib import Path
import sys,json,math,hashlib
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
Q=Path(__file__).resolve().parent;V=Q.parent/'2026-10-25_final-six-v13'
FONT=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',19)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
manifest={'source_version':'V13 final MP4s','method':'Every0.5s final decoded video frame, and each edit boundary at -2,-1,0,+1,+2 frames. Actual PNGs and sequential contact sheets. Not realtime viewing or listening.','films':[]}
for f in read(V/'delivery_manifest.json')['films']:
 cid=f['concept_id'];src=V/f['file'];ed=read(src.parent/'edit_manifest.json');out=Q/'frames'/cid;out.mkdir(parents=True,exist_ok=True);contacts=Q/'contacts'/cid;contacts.mkdir(parents=True,exist_ok=True)
 targets=set(range(0,round(f['duration_seconds']*24),12));joins={}
 timeline=ed.get('timeline',ed.get('segments',[]))
 for j,t in enumerate(timeline[1:],1):
  center=round(t['start']*24);ids=[center+k for k in [-2,-1,0,1,2] if center+k>=0];targets.update(ids);joins[f'J{j:02}_{t["start"]:06.3f}']=ids
 targets.add(round(f['duration_seconds']*24)-1);written={int(p.stem.split('_')[0]):p for p in out.glob('*.png')};deltas=[];last=None;pts=[]
 if not targets.issubset(written):
  written={}
  with av.open(str(src)) as c:
   for i,fr in enumerate(c.decode(video=0)):
    ts=float(fr.pts*fr.time_base);pts.append(ts);im=fr.to_image()
    small=np.asarray(im.resize((80,45))).astype(np.int16)
    if last is not None:deltas.append(float(np.abs(small-last).mean()))
    last=small
    if i in targets:
     p=out/f'{i:04}_{ts:07.3f}.png';im.save(p);written[i]=p
 frame_count=round(f['duration_seconds']*24)
 def sheet(ids,path,columns=3,tw=480):
  th=round(tw*720/1280);cellh=th+28;rows=math.ceil(len(ids)/columns);can=Image.new('RGB',(columns*tw,rows*cellh),(15,18,23));dr=ImageDraw.Draw(can)
  for n,idx in enumerate(ids):
   x=(n%columns)*tw;y=(n//columns)*cellh
   im=Image.open(written[idx]);im.thumbnail((tw,th));can.paste(im,(x,y+28));dr.text((x+5,y+2),f'{cid} {idx/24:.3f}s | frame{idx}',fill='white',font=FONT)
  can.save(path,quality=93)
 seq=[i for i in sorted(written) if i%12==0 or i==frame_count-1];pages=[]
 for n in range(0,len(seq),12):
  p=contacts/f'sequence_{n//12+1:02}.jpg';sheet(seq[n:n+12],p);pages.append(str(p.relative_to(Q)))
 joinpages=[]
 for name,ids in joins.items():
  p=contacts/f'{name}.jpg';sheet(ids,p,columns=5,tw=384);joinpages.append(str(p.relative_to(Q)))
 cap=ed.get('captions',[])
 e={**f,'source_absolute':str(src),'frame_count':frame_count,'last_pts':pts[-1] if pts else None,'pts_gaps':sum(abs(b-a-1/24)>1e-4 for a,b in zip(pts,pts[1:])) if pts else None,'metrics_note':'None means reused complete PNG extraction from this run; earlier V13 full decoding/PTS record retained.','sequence_pages':pages,'boundary_pages':joinpages,'individual_frames':str(out.relative_to(Q)),'timeline':timeline,'captions':cap,'mean_visual_delta':sum(deltas)/len(deltas) if deltas else None,'observed_identical_frame_pairs':sum(d==0 for d in deltas) if deltas else None}
 assert hashlib.sha256(src.read_bytes()).hexdigest()==f['sha256']
 manifest['films'].append(e);print(cid,frame_count,'frames',len(pages),'sequence sheets',len(joinpages),'joins',flush=True)
(Q/'review_input.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Review input complete',flush=True)
