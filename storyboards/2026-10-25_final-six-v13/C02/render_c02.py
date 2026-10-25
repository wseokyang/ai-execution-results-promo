"""C02 V13 derivative. Originals read-only. Screen/paper content is post-composited.
All generated voices are muted. No Flow or remote API calls from this script.
"""
from pathlib import Path
import sys, json, hashlib, subprocess, math, re
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT/'.deps'))
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import cv2, av, numpy as np
from PIL import Image,ImageDraw,ImageFont
from tinysoundfont import Synth
SB=OUT.parent.parent
F=SB/'2026-10-24_v12-C02-C04-C01-flow'
V=OUT.parent
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
FPS,W,H,SR=24,1280,720,48000
WORK=OUT/'_work';WORK.mkdir(exist_ok=True)
QA=OUT/'review_frames';QA.mkdir(exist_ok=True)
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(a,**kw):
 p=subprocess.run([str(FF),*map(str,a)],capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-3000:])
 return p
def loudness(p):
 result=run(['-hide_banner','-i',p,'-af','loudnorm=I=-23:TP=-3:LRA=11:print_format=json','-f','null','-'])
 full=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',result.stderr.decode(errors='replace'))[-1])
 return {**{k:v for k,v in full.items() if k.startswith('input_')},'method':'Analysis only. loudnorm output is discarded; final mix uses one static volume gain.'}
def font(n):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',n)
def raw(shot,t):
 with av.open(str(F/f'C02_{shot}.mp4')) as c:
  for i,f in enumerate(c.decode(video=0)):
   if i==round(t*FPS):return np.array(f.to_image())
 raise ValueError((shot,t))
def quad(track,t):
 ts=[v[0] for v in track]
 return np.array([[np.interp(t,ts,[v[1][i][j] for v in track]) for j in range(2)] for i in range(4)],np.float32)
def unwarp(im,q,size):
 w,h=size;dst=np.array([[0,0],[w-1,0],[w-1,h-1],[0,h-1]],np.float32)
 return cv2.warpPerspective(im,cv2.getPerspectiveTransform(np.float32(q),dst),(w,h),flags=cv2.INTER_CUBIC)
def poly_mask(points):
 m=np.zeros((H,W),np.uint8);cv2.fillPoly(m,[np.int32(points)],255);return m
def composite(im,art,q,foreground=None):
 ah,aw=art.shape[:2];src=np.float32([[0,0],[aw-1,0],[aw-1,ah-1],[0,ah-1]])
 oh,ow=im.shape[:2]
 tr=cv2.getPerspectiveTransform(src,np.float32(q))
 layer=cv2.warpPerspective(art,tr,(ow,oh),flags=cv2.INTER_CUBIC)
 alpha=cv2.warpPerspective(np.full((ah,aw),255,np.uint8),tr,(ow,oh),flags=cv2.INTER_LINEAR).astype(float)/255
 if foreground is not None:alpha*=1-foreground.astype(float)/255
 return np.uint8(np.clip(im*(1-alpha[:,:,None])+layer*alpha[:,:,None],0,255))

# Exact geometry keyed from original images. Every output frame is inspected via
# sample/edge-frame sheets; interpolation is not claimed to be solved tracking.
TRACKS={
 'K03':[(1.5,[(480,122),(1249,52),(1245,535),(465,475)]),(3.5,[(489,122),(1255,53),(1249,538),(478,477)]),(7.5,[(515,125),(1264,57),(1255,544),(501,483)])],
 'K04':[(1,[(987,208),(1165,193),(1155,404),(979,393)]),(4.5,[(1004,209),(1179,194),(1169,405),(994,395)]),(6,[(1013,209),(1188,194),(1177,405),(1003,395)]),(7,[(1018,210),(1193,195),(1182,406),(1008,396)])],
 'K05':[(0,[(985,208),(1162,192),(1153,401),(978,393)]),(2.5,[(990,209),(1168,194),(1157,402),(980,395)])],
 'K06':[(0,[(985,208),(1162,192),(1153,402),(978,394)]),(2,[(986,208),(1163,193),(1153,402),(978,394)])],
 'NEW':[(0,[(982,207),(1161,192),(1152,402),(974,394)]),(3,[(984,208),(1163,194),(1153,404),(976,395)]),(5,[(985,208),(1164,194),(1153,404),(976,395)])],
 'K07':[(1.5,[(1091,245),(1217,237),(1213,381),(1086,378)]),(3,[(1101,244),(1227,236),(1225,383),(1097,381)]),(4.25,[(1109,244),(1237,237),(1234,383),(1105,380)])],
 'K08':[(.25,[(529,258),(774,292),(764,465),(501,405)]),(.5,[(530,259),(778,289),(768,461),(504,407)]),(1.5,[(537,267),(795,274),(787,449),(519,419)]),(2,[(537,268),(796,274),(788,449),(522,423)]),(3.5,[(549,275),(797,276),(790,449),(541,430)])],
 'K09':[(4,[(536,305),(762,308),(758,445),(528,435)]),(5,[(536,306),(764,308),(759,445),(529,435)]),(6.5,[(535,305),(762,308),(758,445),(527,435)])]
}

# The same real display texture is used before/after. The clean version is an
# unmarked portion of that display, resampled as its white specimen surface.
dirty_src=raw('K04_take01',1)
texture=unwarp(dirty_src,TRACKS['K04'][0][1],(400,480))
clean=cv2.resize(texture[190:470,10:245],(400,480),interpolation=cv2.INTER_CUBIC)
yy,xx=np.mgrid[0:480,0:400]
spot=np.exp(-(((xx-310)/43)**2+((yy-106)/60)**2)/2)*.68
dirty=np.uint8(clean.astype(float)*(1-spot[:,:,None]))
rad=np.sqrt(((xx-205)/104)**2+((yy-254)/135)**2)
ring=np.exp(-((rad-1)/.25)**2/2)*.70
blocked=np.uint8(clean.astype(float)*(1-ring[:,:,None]))
for name,im in [('same_specimen_clean',clean),('same_specimen_dirty',dirty),('same_specimen_cuff',blocked)]:Image.fromarray(im).save(OUT/f'{name}.png')

# PD approved a continuity composite: use one sharp still already visible in the
# K08 source photograph on BOTH phone and paper. This is not a native capture
# of the low-resolution phone preview. Preserve the original 3s shutter blink.
PHONE_Q=[(323,341),(442,339),(441,416),(323,414)]
PHONE_TRACK=[(1.5,[(313,327),(431,326),(429,403),(312,400)]),(2.5,PHONE_Q),(3.5,[(322,341),(443,341),(443,420),(321,415)]),(4.25,[(323,342),(445,342),(446,422),(324,417)])]
photo=unwarp(raw('K08_take01',3.5),[(550,276),(796,277),(789,446),(542,428)],(600,380))
photo=composite(photo,blocked,[(503,141),(585,127),(582,233),(500,238)])
Image.fromarray(photo).save(OUT/'shared_photograph_from_K08.png')

def paper_hands(im,shot,t):
 m=np.zeros((H,W),np.uint8)
 if shot=='K08':
  # Each hand polygon hugs its actual paper-edge intersection. Larger glove
  # bodies remain naturally outside the composited inner photograph.
  dx=np.interp(t,[.25,.5,1.5,2,3.5],[0,0,5,9,20])
  dy=np.interp(t,[.25,.5,1.5,2,3.5],[0,0,6,10,14])
  top=np.array([(475,298),(505,296),(531,309),(542,320),(540,330),(530,340),(510,350),(480,359)],float)+[dx,dy]
  low=np.array([(475,410),(505,402),(525,402),(540,410),(550,419),(550,429),(537,438),(511,442),(482,449)],float)+[dx,dy]
  for p in [top,low]:m=cv2.bitwise_or(m,poly_mask(p))
 else:
  glove=[(458,409),(483,405),(509,408),(521,416),(549,425),(558,431),(554,439),(538,443),(511,443),(483,448),(459,440)]
  m=cv2.bitwise_or(m,poly_mask(glove))
  dx=np.interp(t,[4,4.25,4.5,4.75,5,5.5,6.5],[0,10,51,100,130,141,142])
  dy=np.interp(t,[4,4.25,4.5,4.75,5,5.5,6.5],[0,-4,-6,1,10,11,11])
  hand=np.array([(697,379),(681,368),(665,359),(652,345),(644,340),(639,342),(640,349),(651,366),(636,363),(615,353),(608,353),(606,357),(610,364),(632,374),(610,365),(604,368),(606,374),(631,388),(611,379),(605,381),(607,388),(636,406),(648,413),(638,417),(629,421),(627,427),(633,431),(646,427),(666,422),(688,414),(695,413),(770,439),(773,374)],float)+[dx,dy]
  # Retain a 2px soft safety margin, not a broad rectangle hiding replacement.
  m=cv2.bitwise_or(m,poly_mask(hand))
 return cv2.GaussianBlur(m,(3,3),.6)

def picture(im,shot,t):
 # PD correction: source K03 already compares DIFFERENT products with the same
 # spot position, consistent with K01's board. Preserve actual glove and UI.
 if shot=='K03':return im
 if shot=='K04':return composite(im,dirty if t<5 else clean,quad(TRACKS['K04'],t))
 if shot=='K05':return composite(im,clean,quad(TRACKS['K05'],t))
 if shot in ['NEW','NEW_REACT']:return composite(im,blocked,quad(TRACKS['NEW'],t))
 if shot=='K06':return composite(im,blocked,quad(TRACKS['K06'],t))
 if shot=='K07':
  im=composite(im,blocked,quad(TRACKS['K07'],t))
  if not 2.9583<=t<3.125:
   # Thumb is outside the chosen preview plane except for its right edge.
   m=np.zeros((H,W),np.uint8)
   rgb=im.astype(float);skin=(rgb[:,:,0]-rgb[:,:,1]>16)&(rgb[:,:,1]-rgb[:,:,2]>9)&(rgb[:,:,0]>95)
   m[350:430,435:480]=np.uint8(skin[350:430,435:480])*255
   im=composite(im,photo,quad(PHONE_TRACK,t),cv2.GaussianBlur(m,(3,3),.6))
  return im
 if shot in ['K08','K09']:return composite(im,photo,quad(TRACKS[shot],t),paper_hands(im,shot,t))
 return im

def previews():
 for shot,ts,take in [('K03',[1.5,3,3.5,5,7],'01'),('K04',[1,2,4.5,5.5,6.5],'01'),('K05',[0,2],'01'),('K06',[.5,1.5],'01'),('K07',[1.5,2.5,3.5,4],'02'),('K08',[.25,.5,1,1.5,2,2.5,3.5],'01'),('K09',[4,4.25,4.5,4.75,5,5.5,6.5],'01')]:
  for t in ts:
   im=picture(raw(f'{shot}_take{take}',t),shot,t)
   Image.fromarray(im).save(QA/f'comp_{shot}_{t:.3f}s.png')
 print('previews',flush=True)

if __name__=='__main__' and '--previews' in sys.argv:previews();sys.exit()

def build_timeline():
 selected=json.loads((OUT/'selected_new_clip.json').read_text(encoding='utf8'))
 new=V/selected['file']
 assert new.exists() and selected['approved'],'Awaiting reviewed and selected new original'
 assert new.name!='C02_K05_shortchain_take01.mp4','Rejected extra cuff ring'
 # Source trims may be adjusted only after actual new source review.
 rows=[('K01',F/'C02_K01_take01.mp4',0,3.5),('K02',F/'C02_K02_take01.mp4',0,2.75),
 ('K03',F/'C02_K03_take01.mp4',1.5,7.5),('K04',F/'C02_K04_take01.mp4',1,2.5),
 ('K04',F/'C02_K04_take01.mp4',4.5,7),('K05',F/'C02_K05_take01.mp4',0,2.5),
 ('NEW',new,selected['source_in'],selected['release_end']),('NEW_REACT',new,selected['release_end'],selected['source_out']),('K07',F/'C02_K07_take02.mp4',1.5,4.25),
 ('K08',F/'C02_K08_take01.mp4',.5,3.5),('K09',F/'C02_K09_take01.mp4',4,6.5),('END',None,0,4.75)]
 cursor=0;edl=[]
 for sh,p,a,b in rows:
  edl.append(dict(cut=sh,source=None if p is None else str(p.relative_to(SB)),source_in=a,source_out=b,start=cursor,end=cursor+b-a));cursor+=b-a
 return edl,cursor

def caption_art(text,pos='bottom'):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im);size=42;lines=text.split('\n');lh=55
 tw=max(d.textlength(s,font=font(size)) for s in lines);hh=lh*len(lines)+20;x=(W-tw)/2;y=38 if pos=='top' else H-44-hh
 d.rounded_rectangle((x-20,y,x+tw+20,y+hh),12,fill=(8,17,24,224))
 for j,s in enumerate(lines):d.text((640,y+12+lh*j),s,font=font(size),fill='white',anchor='mt')
 return im
def ending():
 im=Image.new('RGB',(W,H),(15,25,34));d=ImageDraw.Draw(im)
 for x,y in [(74,80),(1160,98),(90,590),(1168,605)]:d.ellipse((x-7,y-7,x+7,y+7),fill=(214,65,63))
 d.line((76,81,1160,98,90,590,1168,605),fill=(95,43,46),width=2)
 d.text((640,195),'Q-AI Fair',font=font(85),fill=(250,249,241),anchor='mt')
 d.text((640,334),'AI 실행의 과정까지, 함께 봐요.',font=font(43),fill=(231,234,231),anchor='mt')
 d.text((640,420),'품질팀 AI 성과 교류',font=font(28),fill=(154,181,187),anchor='mt')
 return im

def audio(duration,shutter_at,quiet_at,end_at):
 sf=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
 synth=Synth(gain=-15,samplerate=SR);sid=synth.sfload(str(sf));programs={0:43,1:45,2:0}
 for ch,p in programs.items():synth.program_select(ch,sid,0,p)
 notes=[]
 def note(t,d,p,v,ch):notes.append(dict(start=t,duration=d,pitch=p,velocity=v,channel=ch))
 for k,t in enumerate(np.arange(.35,end_at,.78)):
  if quiet_at-.15<t<quiet_at+.8:continue
  note(float(t),.30,[38,45,41,45,38,43,41,36][k%8],43,0)
  if k%4==2:note(float(t)+.15,.22,[62,65,69,67][k//4%4],34,1)
 for p in [50,57,62,65]:note(end_at+.12,2.1,p,32,2)
 for p in [50,57,62]:note(end_at+2.35,1.75,p,28,2)
 n=round(duration*SR);mix=np.zeros((n,2),np.float32);events=[]
 for no in notes:events.extend([(round(no['start']*SR),1,no),(min(n,round((no['start']+no['duration'])*SR)),0,no)])
 pos=0
 for idx,on,no in sorted(events,key=lambda a:(a[0],a[1])):
  if idx>pos:mix[pos:idx]=np.frombuffer(synth.generate(idx-pos),np.float32).reshape(-1,2);pos=idx
  (synth.noteon(no['channel'],no['pitch'],no['velocity']) if on else synth.noteoff(no['channel'],no['pitch']))
 if pos<n:mix[pos:]=np.frombuffer(synth.generate(n-pos),np.float32).reshape(-1,2)
 mix*=.1/max(1e-9,float(abs(mix).max()))
 # A single low-level camera click, matched to the real 3.0s phone blink.
 rng=np.random.default_rng(202602);dur=.09;ns=round(dur*SR);t=np.arange(ns)/SR
 click=(.45*np.sin(2*np.pi*1050*t)+rng.normal(size=ns)*.4)*np.exp(-t*65)
 click[:240]*=np.linspace(0,1,240);click[-240:]*=np.linspace(1,0,240);click*=.028/max(abs(click).max(),1e-9)
 j=round(shutter_at*SR);mix[j:j+ns]+=click[:,None]
 for a,b in [(quiet_at-.1,quiet_at+.65)]:
  aa,bb=round(a*SR),round(b*SR);f=round(.03*SR);mix[aa-f:aa]*=np.linspace(1,0,f)[:,None];mix[aa:bb]=0;mix[bb:bb+f]*=np.linspace(0,1,f)[:,None]
 mix[:2400]*=np.linspace(0,1,2400)[:,None];mix[-24000:]*=np.linspace(1,0,24000)[:,None]
 p=WORK/'mix.wav';run(['-y','-v','error','-f','f32le','-ar',SR,'-ac',2,'-i','-','-c:a','pcm_f32le',p],input=mix.tobytes())
 dump(OUT/'audio_recipe.json',dict(original_voices='muted',music='Original sparse pizzicato/double-bass local composition',soundfont=str(sf),soundfont_sha256=sha(sf),programs=programs,notes=notes,shutter=dict(at=shutter_at,cause='K07 source3.0s actual phone preview blink',duration=dur),cuff_click='omitted: no newly verified visible clasp closure',peak_before_aac=float(abs(mix).max()),actual_listening_verified=False))
 return p

def main():
 edl,duration=build_timeline();assert duration<=60
 # Caption timing derives from actual EDL; no narration is required.
 by={x['cut']:x for x in edl};newstart=by['NEW']['start'];reveal=by['NEW_REACT']['start'];photoat=by['K07']['start'];end=by['END']['start']
 caps=[(.3,3.3,'어딜 봐도, 같은 흔적.','bottom'),(3.75,6,'사진부터 보시죠.','bottom'),(6.5,9,'AI가 모은 후보 3장','bottom'),(9.25,12,'서로 다른 사진, 같은 자리.','bottom'),(12.4,14.15,'촬영창을 닦고…','bottom'),(14.3,16.1,'점이 사라졌다.','bottom'),(16.5,min(newstart+2.1,reveal-.15),'이제 못 움직여.','bottom'),(reveal+.1,reveal+1.4,'이번엔 수갑이…','bottom'),(photoat+.3,photoat+2.6,'새로운 사례 확보.','bottom'),(by['K09']['start']+.1,by['K09']['end']-.1,'이 사례는 직접 설명하시죠.','top')]
 caparts=[(a,b,caption_art(txt,pos)) for a,b,txt,pos in caps];title=ending()
 sources={r['source'] for r in edl if r['source']};hashes={s:sha(SB/s) for s in sources}
 pic=WORK/'picture.mp4';n=0
 with (WORK/'render.log').open('wb') as log:
  enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',str(pic)],stdin=subprocess.PIPE,stderr=log)
  try:
   for seg in edl:
    count=0
    if seg['source'] is None:
     for k in range(round((seg['end']-seg['start'])*FPS)):enc.stdin.write(title.tobytes());n+=1;count+=1
    else:
     with av.open(str(SB/seg['source'])) as c:
      for f in c.decode(video=0):
       st=float(f.time)
       if st<seg['source_in']-1e-5:continue
       if st>=seg['source_out']-1e-5:break
       tt=seg['start']+st-seg['source_in'];im=Image.fromarray(picture(np.array(f.to_image()),seg['cut'],st)).convert('RGBA')
       for a,b,art in caparts:
        if a<=tt<b:im.alpha_composite(art)
       enc.stdin.write(im.convert('RGB').tobytes());n+=1;count+=1
    assert count==round((seg['end']-seg['start'])*FPS),(seg,count)
    print(seg['cut'],count,flush=True)
  finally:enc.stdin.close();enc.wait()
 assert enc.returncode==0 and n==round(duration*FPS)
 wav=audio(duration,photoat+1.5,reveal,end)
 measured=loudness(wav);gain=min(-23-float(measured['input_i']),-3-float(measured['input_tp']))
 recipe=json.loads((OUT/'audio_recipe.json').read_text(encoding='utf8'));recipe.update(dict(loudness_before_gain=measured,static_gain_db=gain,target_lufs=-23,target_true_peak_ceiling_dbfs=-3,dynamic_normalization=False));dump(OUT/'audio_recipe.json',recipe)
 final=OUT/'C02_Q-AI_Fair_final_v13.mp4'
 run(['-y','-v','error','-i',pic,'-i',wav,'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',f'volume={gain}dB','-c:a','aac','-b:a','192k','-t',duration,'-movflags','+faststart',final])
 run(['-v','error','-i',final,'-f','null','-'])
 pts=[];tiles=[];joins=[r['start'] for r in edl];picks=set(range(0,n,12))|{n-1}
 for jt in joins:
  picks|={round(jt*FPS)+o for o in [-1,0,1]}
 with av.open(str(final)) as c:
  for i,f in enumerate(c.decode(video=0)):
   pts.append(float(f.time))
   if i in picks:
    im=f.to_image();im.save(QA/f'{i/FPS:06.3f}s.png');tile=Image.new('RGB',(320,204),(13,22,30));tile.paste(im.resize((320,180)),(0,24));ImageDraw.Draw(tile).text((8,3),f'{i/FPS:.3f}s',font=font(15),fill='white');tiles.append(tile)
 for k in range(math.ceil(len(tiles)/20)):
  ts=tiles[k*20:k*20+20];sheet=Image.new('RGB',(1280,204*math.ceil(len(ts)/4)))
  for j,im in enumerate(ts):sheet.paste(im,(j%4*320,j//4*204))
  sheet.save(OUT/f'review_contact_{k+1:02d}.jpg',quality=94)
 assert len(pts)==n and np.allclose(np.diff(pts),1/FPS)
 a=np.frombuffer(run(['-v','error','-i',final,'-vn','-ar',SR,'-ac',2,'-f','f32le','-']).stdout,np.float32)
 assert np.isfinite(a).all() and abs(a).max()<1
 audio_end=0.;audio_gaps=[];audio_frames=0
 with av.open(str(final)) as c:
  for f in c.decode(audio=0):
   audio_gaps.append(float(f.time)-audio_end);audio_end=float(f.time)+f.samples/f.sample_rate;audio_frames+=1
 assert max(map(abs,audio_gaps))<1/SR
 assert abs(audio_end-duration)<=1024/SR
 assert hashes=={s:sha(SB/s) for s in sources}
 def srt(t):
  z=round(t*1000);return f'{z//3600000:02d}:{z//60000%60:02d}:{z//1000%60:02d},{z%1000:03d}'
 cs=[dict(start=a,end=b,text=txt,position=p) for a,b,txt,p in caps]+[dict(start=end,end=duration,text='Q-AI Fair\nAI 실행의 과정까지, 함께 봐요.')]
 (OUT/'C02_captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt(c["start"])} --> {srt(c["end"])}\n{c["text"]}' for i,c in enumerate(cs))+'\n',encoding='utf-8-sig')
 dump(OUT/'composite_tracking.json',dict(tracks={k:v for k,v in TRACKS.items() if k!='K03'},phone_preview_source='PD-approved shared sharp photograph extracted from K08 source3.5s; copied to K07 phone and K08/K09 paper. This is a post-production continuity choice, not native camera capture.',phone_quad=PHONE_Q,comparison='K03 original different-product photos retained; all have identical spot position. K04 onward uses same white test specimen texture.',clean_event='K04source5s after button',foreground_method='keyed hand polygons; rendered sample inspection separately required',rejected_implementation='K03 screen replacement discarded: altered story logic and introduced glove matte defects'))
 dump(OUT/'edit_manifest.json',dict(concept='C02 검은 점을 잡아라',file=final.name,duration_seconds=duration,fps=FPS,resolution=[W,H],timeline=edl,captions=cs,source_sha256=hashes,source_audio='muted',source_files_unchanged=True,action_stills_inserted=False,phone_photo='PD-approved continuity composite: one source K08 sharp photograph is shared on K07 phone, K08 print, K09 print; native3s shutter blink retained.',actual_continuous_playback_verified=False,actual_listening_verified=False,status='SELF_QA_PENDING'))
 dump(OUT/'technical_validation.json',dict(file=final.name,sha256=sha(final),bytes=final.stat().st_size,video_frames=n,duration_seconds=duration,full_decode='PASS',video_pts_step_seconds=1/FPS,audio_peak=float(abs(a).max()),audio_nonfinite=0,audio_decode_frames=audio_frames,audio_end_seconds=audio_end,max_audio_pts_gap_seconds=max(map(abs,audio_gaps)),source_sha256_unchanged=True,actual_continuous_playback_verified=False,actual_listening_verified=False))
 print('DONE',final,duration,n,flush=True)

if __name__=='__main__':main()
