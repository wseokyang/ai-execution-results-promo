"""Q-AI Fair C05/C06: actual Flow motion + post captions + original music.
All source files remain read-only. No Flow or paid API calls.
"""
from pathlib import Path
import sys, json, hashlib, subprocess, re, shutil, math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from tinysoundfont import Synth

OUT=Path(__file__).resolve().parent
SB=OUT.parent
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SF=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
FPS,W,H,SR=24,1280,720,48000
RUN={i:f'2026-10-23_C06-C05-flow-run0{i}' for i in (1,2,3)}
TIMELINES={
 'C05':[
 ('K01',3,'C05_K01_take02',0,4),('K02A',1,'C05_K02A_take01',1.25,5.75),
 ('K02B',1,'C05_K02B_take02',.5,1.75),('K03',1,'C05_K03_take02',0,3),
 ('K04_jack',1,'C05_K04_take02',1,3.25),('K04_plead',1,'C05_K04_take02',4.5,7.25),
 ('K05',1,'C05_K05_take02',.5,6),('K06',3,'C05_K06_take02',.5,3.5),
 ('K07',3,'C05_K07_take02',1,5.5),('K08_thumb',1,'C05_K08_take01',.5,1.5),
 ('K08_return',3,'C05_K08_take02',0,6.75)],
 'C06':[
 ('K01',1,'C06_K01_take01',0,5),('K02_attack',1,'C06_K02_take01',1,2.5),
 ('K02_sort',1,'C06_K02_take01',4.25,7.5),('K03',1,'C06_K03_take01',1.25,5.75),
 ('K04_wide',1,'C06_K04_take01',.5,3.5),('K04_check',3,'C06_K04_check_take02',1.25,4.75),
 ('K05',2,'C06_K05_take03',1,6),('K06',1,'C06_K06_take01',.75,3.75),
 ('K07',1,'C06_K07_take01',0,4.5),('K08',1,'C06_K08_take01',1.25,5.75),
 ('K09_seat',1,'C06_K09_take01',0,4.75),('K09_reaction',3,'C06_K09_reaction_take01',1.5,4.25),
 ('END',0,'',0,4.75)]}
CAPTIONS={
 'C05':[(.6,3.7,'이 입구는 내가 접수한다.','bottom'),(15.25,17.55,'조금만 더 잡아주세요.','bottom'),
 (17.95,21.35,'잠시 후, AI 실행 사례 공개','bottom'),(29.1,31.1,'들리세요?','bottom')],
 'C06':[(.3,2.4,'제발 퇴근 좀 해.','top_left'),(7.75,9.55,'고마워요.','bottom'),
 (9.88,14,'AI로 기록을 정리한 과정','bottom'),(14.45,20.45,'이 한 건만 확인하면 끝.','bottom'),
 (20.91,23.47,'오늘 남은 일, 끝.','bottom'),(26,28.1,'드디어, 내 시간.','top'),
 (29.75,33,'방금 나간 사람,\n어떻게 내보냈어요?','top'),(34.5,37.5,'질문은 Q-AI Fair에서.','bottom')]}
CAPTIONS['C05']=[(a-.5 if a>=23.75 else a,b-.5 if b>=23.75 else b,tx,pos) for a,b,tx,pos in CAPTIONS['C05']]

def dump(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,**kwargs):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True,**kwargs)
 if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-7000:])
 return p
def font(s,bold=True): return ImageFont.truetype(f'C:/Windows/Fonts/{"malgunbd" if bold else "malgun"}.ttf',s)
def text(d,xy,tx,s,fill='white',anchor='mm',bold=True): d.text(xy,tx,font=font(s,bold),fill=fill,anchor=anchor)
def caption(tx,position):
 im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im); lines=tx.split('\n'); size=42
 widths=[d.textlength(x,font=font(size)) for x in lines]; tw=max(widths); hh=len(lines)*55+20
 x=90 if position=='top_left' else (W-tw)/2
 y=32 if position.startswith('top') else H-48-hh
 d.rounded_rectangle((x-23,y,x+tw+23,y+hh),12,fill=(7,14,22,218))
 for j,line in enumerate(lines): text(d,(x+tw/2,y+10+j*55+25),line,size)
 return im

def warp(art,quad):
 mat=[]; vec=[]
 for (x,y),(u,v) in zip(quad,[(0,0),(art.width,0),(art.width,art.height),(0,art.height)]):
  mat.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]); vec.extend([u,v])
 co=np.linalg.solve(np.array(mat),np.array(vec))
 return art.transform((W,H),Image.Transform.PERSPECTIVE,co,Image.Resampling.BICUBIC)
def between(t,a,b,q1,q2):
 f=np.clip((t-a)/(b-a),0,1); return (np.array(q1)*(1-f)+np.array(q2)*f).tolist()

ASSETS=OUT/'graphics'; ASSETS.mkdir(exist_ok=True)
projector=Image.new('RGBA',(1100,470),(218,236,245,255)); d=ImageDraw.Draw(projector)
text(d,(550,75),'Q-AI Fair',90,(24,53,72))
d.line((75,146,1025,146),fill=(105,145,164),width=3)
for x,head,num in [(285,'AI 기록 분류','01  02  03'),(825,'원문 대조','01  02  03')]:
 d.rounded_rectangle((x-210,193,x+210,409),18,fill=(239,246,249),outline=(129,170,180),width=3)
 text(d,(x,254),head,55,(25,67,83)); text(d,(x,340),num,43,(40,117,126))
text(d,(550,303),'→',62,(31,96,112))
projector.save(ASSETS/'C06_projector.png')

def monitor(done=False):
 im=Image.new('RGBA',(800,500),(218,231,236)); d=ImageDraw.Draw(im)
 for x,head in [(200,'AI 정리'),(600,'원문 대조')]:
  text(d,(x,66),head,48,(22,49,62))
  for j in range(3):
   col=(212,236,228) if j==0 else (236,242,245)
   d.rounded_rectangle((x-165,122+j*99,x+165,203+j*99),9,fill=col)
   text(d,(x,163+j*99),('기록 ' if x==200 else '원문 ')+f'{j+1:02d}',38,(28,76,88))
 if done: text(d,(600,455),'확인 완료',35,(37,109,80))
 return im
MON={False:monitor(False),True:monitor(True)}
for done,im in MON.items(): im.save(ASSETS/f'C06_monitor_{"checked" if done else "compare"}.png')
paper=Image.new('RGBA',(800,300)); d=ImageDraw.Draw(paper)
text(d,(190,65),'원문 01',48,(49,72,72))
for j in range(3): d.line((50,135+j*39,310,135+j*39),fill=(70,96,99,180),width=8)
paper.save(ASSETS/'C06_paper_ink_only.png')
sign=Image.new('RGBA',(800,240)); d=ImageDraw.Draw(sign)
text(d,(400,71),'질문은',61,(32,37,34)); text(d,(400,166),'Q-AI Fair에서.',69,(23,39,37))
sign.save(ASSETS/'C06_sign_ink_only.png')

def title(c):
 im=Image.new('RGBA',(W,H),(10,19,29,255) if c=='C06' else (0,0,0,0)); d=ImageDraw.Draw(im)
 if c=='C05':
  d.rounded_rectangle((228,547,1052,695),18,fill=(9,18,24,229))
  text(d,(640,591),'Q-AI Fair',65); text(d,(640,657),'AI 실행 사례, 지금 시작합니다.',36,(223,242,241))
 else:
  d.line((536,234,744,234),fill=(105,210,195),width=4)
  text(d,(640,321),'Q-AI Fair',100); text(d,(640,431),'직접 해본 방법을 함께 봐요.',43,(224,237,239))
 return im
TITLES={c:title(c) for c in TIMELINES}
for c,im in TITLES.items(): im.save(ASSETS/f'{c}_ending.png')

# Tracked corners were read from the actual selected source frames.
PROJECTOR_QUAD=[(676,101),(1234,44),(1234,277),(676,302)]
WIDE_QUAD=[(962,292),(1190,257),(1179,507),(952,478)]
CHECK_Q1=[(800,80),(1250,10),(1233,395),(785,350)]
CHECK_Q2=[(806,80),(1260,3),(1244,405),(790,353)]
PAPER_Q1=[(600,547),(688,527),(853,568),(766,596)]
PAPER_Q2=[(607,548),(695,528),(860,570),(773,599)]
SIGN_TRACK=[
 (1.25,[(785,408),(931,414),(928,464),(782,457)]),
 (2,[(785,434),(932,438),(928,488),(782,482)]),
 (2.75,[(787,477),(932,480),(929,531),(783,525)]),
 (3.5,[(787,510),(928,515),(925,565),(784,559)]),
 (5.75,[(787,510),(928,515),(925,565),(784,559)])]
SIGN_SEAT=[(827,515),(937,518),(932,560),(823,556)]
dump(OUT/'composite_tracking.json',dict(projector=PROJECTOR_QUAD,wide=WIDE_QUAD,check=[CHECK_Q1,CHECK_Q2],paper=[PAPER_Q1,PAPER_Q2],sign=SIGN_TRACK,seat=SIGN_SEAT))

def ink_on_paper(im,art,quad,neutral=True):
 layer=warp(art,quad)
 if neutral:
  rgb=np.asarray(im)[:,:,:3].astype(np.float32); a=np.array(layer)
  # Preserve hands/pen/ink and table foreground, not an opaque pasted rectangle.
  mx=rgb.max(2); mn=rgb.min(2)
  mask=np.clip((28-(mx-mn))/8,0,1)*np.clip((mn-105)/30,0,1)
  a[:,:,3]=(a[:,:,3]*mask).astype('uint8'); layer=Image.fromarray(a)
 im.alpha_composite(layer)

def sign_quad(im):
 rgb=np.asarray(im)[420:590,765:950,:3].astype(float)
 rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
 mask=(rr>150)&(gg>130)&(bb>90)&((rr-gg)<40)&((gg-bb)<45)&((rr-bb)>15)
 seen=np.zeros_like(mask); candidates=[]
 for sy,sx in np.argwhere(mask):
  if seen[sy,sx]: continue
  stack=[(int(sy),int(sx))]; seen[sy,sx]=True; points=[]
  while stack:
   y,x=stack.pop(); points.append((y,x))
   for ny,nx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
    if 0<=ny<mask.shape[0] and 0<=nx<mask.shape[1] and mask[ny,nx] and not seen[ny,nx]:
     seen[ny,nx]=True; stack.append((ny,nx))
  yy,xx=np.array(points).T
  if len(xx)<2200: continue
  bw=xx.max()-xx.min()+1; bh=yy.max()-yy.min()+1
  if bw<95 or bh<28 or len(xx)/(bw*bh)<.65: continue
  candidates.append((len(xx),xx+765,yy+420))
 if not candidates: raise ValueError('Unable to track C06 sign')
 _,xx,yy=max(candidates,key=lambda x:x[0]); pts=np.column_stack((xx,yy))
 quad=np.array([pts[np.argmin(xx+yy)],pts[np.argmax(xx-yy)],pts[np.argmax(xx+yy)],pts[np.argmin(xx-yy)]],float)
 center=quad.mean(0); return (center+(quad-center)*.95).tolist()

def clean_laptop_mark(im,st):
 # Tiny decorative generated product marks only; the source Veo watermark remains.
 rgb=np.array(im)
 if st>=.75:
  ts=[.75,1,1.75,2.5,3.25,4.25,4.5]
  xs=[250,274,332,397,431,444,446]; ys=[355,339,317,313,327,343,345]
  x=round(float(np.interp(st,ts,xs))); y=round(float(np.interp(st,ts,ys)))
  roi=rgb[max(0,y-22):y+23,x-22:x+23,:3]
  yy,xx=np.where((roi[:,:,0]>150)&(roi[:,:,1]>155)&(roi[:,:,2]>160))
  if len(xx)>5:
   cx=x-22+int(np.median(xx)); cy=y-22+int(np.median(yy))
   patch=im.crop((cx-25,cy-12,cx-9,cy+12)).resize((26,30))
   mask=Image.new('L',(26,30)); ImageDraw.Draw(mask).ellipse((2,2,24,28),fill=255)
   mask=mask.filter(ImageFilter.GaussianBlur(1.5)); im.paste(patch,(cx-13,cy-15),mask)
 return im

def composite(im,cut,st,t,c):
 if c=='C06':
  if cut=='K03': im.alpha_composite(warp(projector,PROJECTOR_QUAD))
  elif cut=='K04_wide':
   im.alpha_composite(warp(MON[False],WIDE_QUAD))
  elif cut=='K04_check':
   im.alpha_composite(warp(MON[st>=2.75],between(st,1.25,4.75,CHECK_Q1,CHECK_Q2)))
   ink_on_paper(im,paper,between(st,1.25,4.75,PAPER_Q1,PAPER_Q2))
  elif cut=='K05':
   im.alpha_composite(warp(MON[True],[(1036,322),(1218,291),(1210,488),(1028,470)]))
  elif cut=='K07': im=clean_laptop_mark(im,st)
  elif cut=='K08':
   ink_on_paper(im,sign,sign_quad(im),neutral=False)
  elif cut=='K09_seat': ink_on_paper(im,sign,SIGN_SEAT,neutral=False)
 if c=='C05' and t>=33.5: im.alpha_composite(TITLES[c])
 return im

def soundtrack(c,duration,segments):
 n=round(duration*SR); synth=Synth(gain=-12,samplerate=SR); sid=synth.sfload(str(SF))
 instruments={0:61,1:48,2:45,3:70,4:11}
 for ch,program in instruments.items(): synth.program_select(ch,sid,0,program)
 notes=[]
 def note(t,d,p,v=50,ch=0): notes.append(dict(start=t-.5 if c=='C05' and t>=23.75 else t,duration=d,pitch=p,velocity=v,channel=ch))
 def chord(t,d,pitches,v=45,ch=0):
  for p in pitches: note(t,d,p,v,ch)
 if c=='C05':
  chord(0,3.3,[33,40,45],41,1); chord(4,4.3,[33,40,48],39,1)
  for i,p in enumerate([45,45,52,48,47,45,40,43,45,52,48,47]): note(.6+i*.62,.24,p,48,0)
  chord(8.5,.8,[40,47,52],54,0)
  for i,p in enumerate([48,55,51,55,46,53,48,55]): note(12.9+i*.58,.18,p,46,3)
  for i,p in enumerate([48,52,55,59,55,52]): note(18+i*.68,.28,p,42,2)
  for t,p in [(23.9,45),(24.5,48),(25.1,52),(25.7,57)]: note(t,.42,p,48,0)
  chord(34.15,2.1,[48,55,60,64],40,4); chord(36.1,2.2,[48,55,60,67],35,1)
 else:
  chord(0,3.4,[33,40,46],35,1)
  note(5.05,.25,40,50,3); note(6.7,.25,43,42,3); note(8,.2,48,37,3)
  for i,p in enumerate([48,55,60,57,52,55,60,64,62,59,55,52,48]): note(9.85+i*.7,.24,p,38,2)
  chord(20.9,1.3,[48,55,60],36,4)
  for t,p in [(23.25,52),(24,55),(25.9,60),(26.55,64),(27.15,67)]: note(t,.45,p,37,4)
  chord(28.9,3,[33,40,46],34,1)
  for t,p in [(33.4,43),(34.4,48),(35.5,46),(37.85,40)]: note(t,.25,p,40,3)
  chord(42.5,2.2,[33,40,46],30,1)
  chord(45.4,2,[48,55,60,64],36,4); chord(47.2,2.3,[48,55,60],32,1)
 events=[]
 for no in notes:
  events.extend([(round(no['start']*SR),1,no),(min(n,round((no['start']+no['duration'])*SR)),0,no)])
 events.sort(key=lambda x:(x[0],x[1])); score=np.zeros((n,2),np.float32); pos=0
 for idx,on,no in events:
  if idx>pos: score[pos:idx]=np.frombuffer(synth.generate(idx-pos),np.float32).reshape(-1,2); pos=idx
  (synth.noteon(no['channel'],no['pitch'],no['velocity']) if on else synth.noteoff(no['channel'],no['pitch']))
 if pos<n: score[pos:]=np.frombuffer(synth.generate(n-pos),np.float32).reshape(-1,2)
 score*=.14/max(1e-9,float(np.abs(score).max()))
 for a,b in ([(9.75,10.2),(26.25,26.7)] if c=='C05' else [(3.6,4.1),(28.1,28.75)]):
  ia,ib=round(a*SR),round(b*SR); fade=round(.025*SR)
  score[max(0,ia-fade):ia]*=np.linspace(1,0,fade)[:,None]; score[ia:ib]=0
  score[ib:ib+fade]*=np.linspace(0,1,fade)[:,None]
 mix=score.copy(); rng=np.random.default_rng(510 if c=='C05' else 610); fx=[]
 def effect(t,d,kind,gain=.1):
  if c=='C05' and t>=23.75: t-=.5
  count=round(d*SR); x=np.arange(count)/SR; noise=rng.normal(0,1,count+31)
  smooth=np.convolve(noise,np.ones(32)/32,'valid')[:count]
  if kind=='thud': wave=(np.sin(2*np.pi*(70*x-20*x*x))*.65+smooth*.35)*np.exp(-x*15)
  elif kind=='click': wave=(np.sin(2*np.pi*1250*x)+smooth)*np.exp(-x*60)
  elif kind=='paper': wave=smooth*np.sin(np.linspace(0,np.pi,count))**2
  elif kind=='creak': wave=np.sin(2*np.pi*(230*x+120*x*x))*np.sin(np.linspace(0,np.pi,count))**2*.45+smooth*.12
  else: wave=smooth*np.sin(np.linspace(0,np.pi,count))
  wave*=gain; at=round(t*SR); end=min(n,at+count); mix[at:end]+=wave[:end-at,None]
  fx.append(dict(at=t,duration=d,kind=kind,gain=gain))
 if c=='C05':
  for args in [(4.6,.4,'creak',.08),(7.8,.36,'thud',.2),(9.78,.45,'creak',.14),(13.3,.1,'click',.09),(14.1,.1,'click',.08),(24.2,.5,'paper',.05),(32.8,.5,'creak',.12)]: effect(*args)
 else:
  for args in [(3.2,.3,'paper',.09),(5.55,.3,'thud',.16),(7.9,.4,'paper',.12),(18.2,.15,'paper',.1),(24.6,.3,'thud',.12),(35.5,.1,'click',.07),(40.8,.15,'click',.1)]: effect(*args)
 mix[:round(.04*SR)]*=np.linspace(0,1,round(.04*SR))[:,None]
 for a in (score,mix): a[-round(.5*SR):]*=np.linspace(1,0,round(.5*SR))[:,None]
 out=OUT/c; out.mkdir(exist_ok=True)
 for name,a in [('score',score),('mix',mix)]: run(['-y','-v','error','-f','f32le','-ar',SR,'-ac',2,'-i','-','-c:a','pcm_f32le',out/f'{c}_{name}.wav'],input=a.tobytes())
 dump(out/'audio_recipe.json',dict(source_audio='Muted; no essential spoken narration',music='Original local composition',soundfont=str(SF),soundfont_sha256=hashlib.sha256(SF.read_bytes()).hexdigest(),programs=instruments,notes=notes,effects=fx,actual_listening_verified=False))
 return out/f'{c}_mix.wav'

def loudness(path):
 p=run(['-hide_banner','-i',path,'-af','loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
 return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',p.stderr.decode(errors='replace'))[-1])
def srt_time(t):
 ms=round(t*1000); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'

def render(c):
 out=OUT/c; out.mkdir(exist_ok=True); segs=[]; cursor=0
 for cut,r,name,a,b in TIMELINES[c]:
  segs.append(dict(cut=cut,source=f'{RUN[r]}/{name}.mp4' if r else None,source_in=a,source_out=b,start=cursor,end=cursor+b-a)); cursor+=b-a
 duration=cursor; expected=round(duration*FPS); assert duration<=60
 sources={s['source'] for s in segs if s['source']}; hashes={s:hashlib.sha256((SB/s).read_bytes()).hexdigest() for s in sources}
 caps=[(a,b,caption(tx,pos)) for a,b,tx,pos in CAPTIONS[c]]
 cap_data=[dict(start=a,end=b,text=tx,position=pos,font_px=42) for a,b,tx,pos in CAPTIONS[c]]
 cap_data.append(dict(start=33.5 if c=='C05' else 45.25,end=duration,text='Q-AI Fair\n'+('AI 실행 사례, 지금 시작합니다.' if c=='C05' else '직접 해본 방법을 함께 봐요.'),position='ending'))
 (out/f'{c}_captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt_time(q["start"])} --> {srt_time(q["end"])}\n{q["text"]}' for i,q in enumerate(cap_data))+'\n',encoding='utf-8-sig')
 dump(out/'edit_manifest.json',dict(film=c,duration_seconds=duration,fps=FPS,resolution=[W,H],segments=segs,captions=cap_data,source_sha256=hashes,flow_credits_used=0,source_audio='muted',generated_action_replaced_with_stills=False,end_card=(c=='C06'),status='render awaiting independent review'))
 picture=out/f'{c}_picture.mp4'
 with (out/'render_stderr.txt').open('wb') as err:
  enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=err)
  fc=0
  try:
   for s in segs:
    count=0; needed=round((s['source_out']-s['source_in'])*FPS)
    if not s['source']:
     for j in range(needed): enc.stdin.write(TITLES[c].convert('RGB').tobytes()); fc+=1; count+=1
    else:
     with av.open(str(SB/s['source'])) as con:
      for f in con.decode(video=0):
       st=float(f.time)
       if st<s['source_in']-1e-5: continue
       if st>=s['source_out']-1e-5: break
       t=s['start']+st-s['source_in']; im=composite(f.to_image().convert('RGBA'),s['cut'],st,t,c)
       for a,b,cap in caps:
        if a<=t<b: im.alpha_composite(cap)
       enc.stdin.write(im.convert('RGB').tobytes()); fc+=1; count+=1
    assert count==needed,(s,count,needed)
    print(c,'picture',s['cut'],count,flush=True)
  finally: enc.stdin.close(); enc.wait()
 assert enc.returncode==0 and fc==expected
 mix=soundtrack(c,duration,segs); m=loudness(mix)
 norm=f'loudnorm=I=-18:TP=-1.5:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true'
 final=out/f'{c}_Q-AI_Fair_edit_v02.mp4'
 run(['-y','-v','error','-i',picture,'-i',mix,'-map','0:v','-map','1:a','-c:v','copy','-af',norm+',volume=-0.4dB,alimiter=limit=0.80:level=false:latency=true','-c:a','aac','-b:a','256k','-ar',SR,'-ac',2,'-t',duration,'-movflags','+faststart',final])
 run(['-v','error','-i',final,'-f','null','-'])
 decoded=np.frombuffer(run(['-v','error','-i',final,'-vn','-ar',SR,'-ac',2,'-f','f32le','-']).stdout,np.float32)
 assert np.isfinite(decoded).all() and float(np.abs(decoded).max())<1
 assert hashes=={s:hashlib.sha256((SB/s).read_bytes()).hexdigest() for s in sources}
 frames=out/'review_frames'; frames.mkdir(exist_ok=True)
 samples=set(range(0,expected,12))|{round(s['start']*FPS)+j for s in segs for j in (-1,0,1)}|{expected-1}
 samples={x for x in samples if 0<=x<expected}; thumbs=[]; frame_count=0
 with av.open(str(final)) as con:
  for i,f in enumerate(con.decode(video=0)):
   frame_count+=1
   if i not in samples: continue
   im=f.to_image(); im.save(frames/f'{i/FPS:06.3f}s.png')
   card=Image.new('RGB',(320,208),(15,23,31)); card.paste(im.resize((320,180)),(0,28))
   ImageDraw.Draw(card).text((8,3),f'{i/FPS:.3f}s',font=font(17),fill='white'); thumbs.append(card)
 assert frame_count==expected
 for batch in range(math.ceil(len(thumbs)/20)):
  subset=thumbs[batch*20:(batch+1)*20]; sheet=Image.new('RGB',(1280,208*math.ceil(len(subset)/4)),(15,23,31))
  for j,im in enumerate(subset): sheet.paste(im,((j%4)*320,(j//4)*208))
  sheet.save(out/f'review_contact_{batch+1:02d}.jpg',quality=94)
 info=dict(file=final.name,duration_seconds=duration,frames=frame_count,resolution=[W,H],fps=FPS,full_av_decode='PASS',originals_unchanged=True,sha256=hashlib.sha256(final.read_bytes()).hexdigest(),bytes=final.stat().st_size,audio_pcm_peak=float(np.abs(decoded).max()),final_loudness=loudness(final),actual_continuous_playback_verified=False,actual_listening_verified=False)
 dump(out/'technical_validation.json',info); print(c,'DONE',info['sha256'],flush=True)

if __name__=='__main__':
 for c in (sys.argv[1:] or ['C05','C06']): render(c)
