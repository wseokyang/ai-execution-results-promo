"""Preserve a downloaded Flow original and extract review frames. Never re-encode originals."""
from pathlib import Path
import argparse, sys, json, hashlib, shutil, datetime
from fractions import Fraction
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image, ImageDraw

p=argparse.ArgumentParser()
p.add_argument('download'); p.add_argument('unit'); p.add_argument('--take',type=int,default=1)
p.add_argument('--out',default=str(Path(__file__).resolve().parent))
p.add_argument('--asset',required=True); p.add_argument('--title',required=True)
p.add_argument('--before',type=int,required=True); p.add_argument('--after',type=int,required=True)
p.add_argument('--model',default='Veo 3.1 Lite'); p.add_argument('--cost',type=int,default=10)
p.add_argument('--project',required=True); p.add_argument('--account',required=True)
a=p.parse_args(); src=Path(a.download); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
name=f'{a.unit}_take{a.take:02d}'; dest=out/f'{name}.mp4'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
if dest.exists():
    assert sha(src)==sha(dest), 'Existing take differs; never overwrite'
else: shutil.copy2(src,dest)
frames=out/'frames'/name; frames.mkdir(parents=True,exist_ok=True)
thumbs=[]; count=0; times=[]
with av.open(str(dest)) as con:
    v=con.streams.video[0]; w,h=v.width,v.height; fps=str(v.average_rate)
    audio=bool(con.streams.audio)
    for f in con.decode(video=0):
        t=float(f.time); times.append(t)
        if count%12==0:
            im=f.to_image(); im.save(frames/f'{count//12:02d}_{t:.3f}s.png')
            small=im.resize((320,180)); card=Image.new('RGB',(320,202),(20,30,36))
            card.paste(small,(0,22)); ImageDraw.Draw(card).text((6,4),f'{t:.3f}s',fill='white'); thumbs.append(card)
        count+=1
sheet=Image.new('RGB',(1280,202*((len(thumbs)+3)//4)))
for i,im in enumerate(thumbs): sheet.paste(im,((i%4)*320,(i//4)*202))
sheet.save(out/f'{name}_contact.jpg',quality=92)
log=out/'generation_log.json'
d=json.loads(log.read_text(encoding='utf-8-sig')) if log.exists() else {'run_id':out.name,'entries':[]}
e=next((x for x in d['entries'] if x['unit_id']==a.unit and x['take']==a.take),None)
if e is None:
    e={'unit_id':a.unit,'take':a.take}; d['entries'].append(e)
e.update(status='ORIGINAL_PRESERVED_REVIEW_PENDING',asset_id=a.asset,flow_title=a.title,
    source_file=src.name,original=dest.name,sha256=sha(dest),download_sha256=sha(src),
    balance_before=a.before,balance_after=a.after,net_balance_change=a.after-a.before,
    charge_observed=a.cost if a.before-a.after==a.cost else None,refund_observed=0,
    model=a.model,cost_displayed=a.cost,account_alias=a.account,project_url=a.project,
    actual_duration=times[-1]+float(1/Fraction(fps)),frame_count=count,width=w,height=h,fps=fps,
    audio_track_present=audio,decode='all video frames decoded; audio not listened',review='PENDING',
    preserved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
prompt=out/'submitted_prompts'/f'{name}.txt'; inp=out/'inputs'/f'{a.unit}.png'
if prompt.exists(): e['prompt']=str(prompt.relative_to(out)).replace('\\','/')
if inp.exists() and 'input' not in e:
    e['input']=str(inp.relative_to(out)).replace('\\','/');e['input_sha256']=sha(inp)
d['last_balance_observed']=a.after
log.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(e,ensure_ascii=False))
