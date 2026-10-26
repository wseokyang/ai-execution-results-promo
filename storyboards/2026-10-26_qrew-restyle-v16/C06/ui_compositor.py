# V16 isolated UI-only source; all writes redirected inside C06.
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
# No soundtrack synthesis in picture compositor.

OUT=Path(__file__).resolve().parent/'compositor_assets'
OUT.mkdir(parents=True,exist_ok=True)
SB=Path(__file__).resolve().parents[2]
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
dump(OUT/'composite_tracking.json',dict(projector=PROJECTOR_QUAD,wide=WIDE_QUAD,check=[CHECK_Q1,CHECK_Q2],paper=[PAPER_Q1,PAPER_Q2],sign_method='Per-frame cream-surface connected component inside x765:950,y420:590; corner extrema contracted 5%; ink only',seat=SIGN_SEAT,exit_monitor=[(1036,322),(1218,291),(1210,488),(1028,470)],product_mark_cleanup='Per-frame predicted local ROI, brightness/colour or dark contrast detection, adjacent texture or fitted surface gradient. Source Veo watermark retained.'))

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
 if st>=.5833:
  ts=[.5833,.625,.75,1,1.75,2.5,3.25,4.25,4.5]
  xs=[224,232,246,274,332,397,431,444,446]; ys=[378,375,365,339,317,313,327,343,345]
  x=round(float(np.interp(st,ts,xs))); y=round(float(np.interp(st,ts,ys)))
  roi=rgb[max(0,y-22):y+23,x-22:x+23,:3]
  yy,xx=np.where((roi.astype(float).mean(2)>120)&(roi[:,:,2]>130)&(roi[:,:,2].astype(float)>roi[:,:,0].astype(float)+8)&(roi[:,:,0].astype(float)<roi[:,:,1].astype(float)+12))
  if len(xx)>5:
   cx=x-22+int(np.median(xx)); cy=y-22+int(np.median(yy))
   if st<1: neutral_patch(im,cx,cy,10,7,20)
   else:
    patch=im.crop((cx-25,cy-12,cx-9,cy+12)).resize((26,30))
    mask=Image.new('L',(26,30)); ImageDraw.Draw(mask).ellipse((2,2,24,28),fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(1.5)); im.paste(patch,(cx-13,cy-15),mask)
  # The second visitor's dark mark sits within the blue laptop lid.
  ts=[.75,1,1.75,2.5,3.25,4.25,4.5]
  xs=[90,100,145,202,234,243,244]; ys=[322,321,306,298,301,304,305]
  x=round(float(np.interp(st,ts,xs))); y=round(float(np.interp(st,ts,ys)))
  roi=np.asarray(im)[y-16:y+17,x-16:x+17,:3].astype(float).mean(2)
  yy,xx=np.where(roi<np.median(roi)*.47)
  if len(xx)>5:
   cx=x-16+int(np.median(xx)); cy=y-16+int(np.median(yy))
   neutral_patch(im,cx,cy,12,12,22)
 return im

def neutral_patch(im,x,y,rx,ry,dx):
 # Fit the local surface gradient from a ring around the mark, rather than
 # copying a brighter neighbouring reflection onto the lid.
 ar=np.asarray(im).astype(float); pad=5
 yy,xx=np.mgrid[-ry-pad:ry+pad,-rx-pad:rx+pad]
 area=ar[y-ry-pad:y+ry+pad,x-rx-pad:x+rx+pad,:3]
 ring=(abs(xx)>rx*.85)|(abs(yy)>ry*.85)
 design=np.stack([xx,yy,np.ones_like(xx)],axis=-1)
 coeff=np.linalg.lstsq(design[ring],area[ring],rcond=None)[0]
 gy,gx=np.mgrid[-ry:ry,-rx:rx]
 fit=np.stack([gx,gy,np.ones_like(gx)],axis=-1)@coeff
 rgba=np.concatenate([np.clip(fit,0,255).astype('uint8'),np.full((2*ry,2*rx,1),255,dtype='uint8')],axis=2)
 patch=Image.fromarray(rgba)
 mask=Image.new('L',(rx*2,ry*2)); ImageDraw.Draw(mask).ellipse((1,1,rx*2-1,ry*2-1),fill=255)
 mask=mask.filter(ImageFilter.GaussianBlur(.7 if ry<7 else 1.2))
 im.paste(patch,(x-rx,y-ry),mask)

def clean_exit_laptop(im,st):
 x=round(float(np.interp(st,[1,1.25,1.5,6],[932,941,938,938])))
 y=round(float(np.interp(st,[1,1.25,1.5,6],[493,513,530,530])))
 ry=round(float(np.interp(st,[1,1.25,1.5,6],[12,8,4,4])))
 neutral_patch(im,x,y,13,ry,25)
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
   im=clean_exit_laptop(im,st)
  elif cut=='K07': im=clean_laptop_mark(im,st)
  elif cut=='K08':
   ink_on_paper(im,sign,sign_quad(im),neutral=False)
  elif cut=='K09_seat': ink_on_paper(im,sign,SIGN_SEAT,neutral=False)
 if c=='C05' and t>=33.5: im.alpha_composite(TITLES[c])
 return im
