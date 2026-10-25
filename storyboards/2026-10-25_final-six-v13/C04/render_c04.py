"""C04 local post-production. Source files read-only; no network/Flow calls.
Ink is composited onto tracked paper and tablet planes, with original hands foreground.
"""
from pathlib import Path
import sys,json,hashlib,subprocess,math,re
OUT=Path(__file__).resolve().parent;SB=OUT.parent.parent;V=OUT.parent
sys.path.insert(0,str(V/'C02/.deps'))
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import cv2,av,numpy as np
from PIL import Image,ImageDraw,ImageFont
from tinysoundfont import Synth
F=SB/'2026-10-24_v12-C02-C04-C01-flow';R=SB/'2026-10-24_C01-C06-repair110'
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W,H,FPS,SR=1280,720,24,48000
WORK=OUT/'_work';WORK.mkdir(exist_ok=True);QA=OUT/'review_frames';QA.mkdir(exist_ok=True)
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def font(n):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',n)
def run(a,**kw):
 p=subprocess.run([str(FF),*map(str,a)],capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-3000:])
 return p
def loudness(p):
 x=run(['-hide_banner','-i',p,'-af','loudnorm=I=-23:TP=-3:LRA=11:print_format=json','-f','null','-'])
 y=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',x.stderr.decode(errors='replace'))[-1]);return {k:v for k,v in y.items() if k.startswith('input_')}
def quad(track,t):
 ts=[x[0] for x in track]
 return np.float32([[np.interp(t,ts,[v[1][i][j] for v in track]) for j in range(2)] for i in range(4)])
def pm(q):
 m=np.zeros((H,W),np.uint8);cv2.fillPoly(m,[np.int32(q)],255);return m
def ink(im,art,q,foreground=None):
 ah,aw=art.shape[:2];tr=cv2.getPerspectiveTransform(np.float32([[0,0],[aw-1,0],[aw-1,ah-1],[0,ah-1]]),np.float32(q))
 layer=cv2.warpPerspective(art,tr,(W,H),flags=cv2.INTER_CUBIC);alpha=layer[:,:,3].astype(float)/255
 if foreground is not None:alpha*=1-foreground.astype(float)/255
 return np.uint8(np.clip(im*(1-alpha[:,:,None])+layer[:,:,:3]*alpha[:,:,None],0,255))
def skin(im,threshold=19):
 r,g,b=[im[:,:,j].astype(float) for j in range(3)]
 m=np.uint8((r-g>threshold)&(r-b>33)&(g-b>7)&(r>90))*255
 return cv2.GaussianBlur(cv2.dilate(m,np.ones((3,3),np.uint8)),(3,3),.6)
def textart(size,lines,opaque=None):
 im=Image.new('RGBA',size,(0,0,0,0) if opaque is None else (*opaque,255));d=ImageDraw.Draw(im)
 for txt,x,y,fs,col in lines:d.text((x,y),txt,font=font(fs),fill=col,anchor='mt')
 return np.array(im)
BLACK=(32,39,42,240);MUTED=(80,84,88,235)
ART={
 'header':textart((850,95),[('AI 대조 · 확인 필요',425,10,63,(109,55,19,255))]),
 'left':textart((420,520),[('신고서',210,30,38,MUTED),('탑승자',210,125,93,BLACK),('없음',210,250,93,BLACK)]),
 'right':textart((420,520),[('첨부 요청',210,30,38,MUTED),('수저',210,125,93,BLACK),('요청',210,250,93,BLACK),('식사 · 물 · 수저',210,420,34,MUTED)]),
 'paper_white':textart((600,450),[('신고서',300,48,50,MUTED),('내부 탑승자',300,160,68,BLACK),('없음',300,270,76,BLACK)]),
 'paper_cream':textart((600,450),[('요청',300,48,52,MUTED),('식사 · 물',300,160,73,BLACK),('수저',300,270,78,BLACK)]),
 'note':textart((360,480),[('식사 · 물',180,65,48,BLACK),('수저',180,138,65,BLACK)])}
# Manual corner keys are tightened against actual source frames, not generic tracking.
TRACK={
 'tab':[(.5,[(397,228),(918,211),(967,524),(421,567)]),(2,[(410,240),(927,219),(977,535),(438,580)]),(3,[(409,242),(929,220),(980,536),(437,580)]),(4,[(407,243),(928,225),(979,539),(435,584)]),(5.5,[(410,247),(934,230),(981,546),(438,585)])],
 'pw':[(.5,[(402,357),(561,390),(514,499),(359,460)]),(1,[(399,370),(555,404),(505,517),(350,475)]),(1.25,[(400,389),(548,409),(507,510),(351,484)]),(1.5,[(409,400),(533,407),(515,493),(359,485)]),(1.75,[(419,414),(532,406),(484,498),(355,496)]),(2,[(420,419),(557,443),(479,521),(350,506)]),(2.25,[(416,424),(551,450),(477,523),(347,510)]),(2.5,[(418,427),(550,452),(478,523),(350,510)]),(3,[(417,427),(548,452),(474,526),(349,511)]),(3.5,[(411,426),(542,455),(468,526),(345,514)]),(4.5,[(407,422),(537,451),(467,521),(343,511)])],
 'pc':[(.5,[(554,417),(682,448),(639,575),(508,537)]),(1,[(568,461),(686,443),(627,547),(515,541)]),(1.25,[(562,473),(682,440),(592,523),(500,533)]),(1.5,[(565,426),(668,423),(587,529),(493,522)]),(1.75,[(539,423),(654,424),(579,530),(490,525)]),(2,[(499,432),(611,421),(557,530),(476,537)]),(2.25,[(470,425),(611,450),(512,545),(370,520)]),(2.5,[(449,423),(604,459),(500,547),(345,511)]),(3.5,[(432,425),(587,467),(478,555),(323,513)]),(4.5,[(429,421),(584,463),(478,550),(323,508)])],
 'note':[(.5,[(662,210),(837,231),(787,463),(613,441)]),(1,[(660,246),(830,264),(781,490),(610,472)]),(1.5,[(660,291),(833,312),(784,545),(611,523)]),(1.8,[(660,320),(831,341),(782,574),(611,552)])],
 'handoff':[(.5,[(626,351),(772,395),(745,451),(582,402)]),(1,[(645,369),(789,415),(768,454),(604,400)]),(1.5,[(680,367),(824,430),(797,453),(649,397)]),(1.75,[(707,389),(850,446),(835,456),(696,405)]),(1.833333,[(714,394),(857,452),(850,455),(710,398)])]
}
TABBASE=np.float32(TRACK['tab'][0][1]);PARTS={'header':[(493,231),(917,217),(925,269),(501,284)],'left':[(495,288),(695,281),(722,532),(517,545)],'right':[(713,279),(913,272),(949,515),(740,529)]}
def picture(im,shot,t):
 if shot=='K04':
  trans=cv2.getPerspectiveTransform(TABBASE,quad(TRACK['tab'],t));fg=skin(im)
  # White cuff follows below the hand: protect the physical sleeve, not a rectangle.
  x=np.interp(t,[.5,1,1.5,2,3,3.5,4,4.5,5.5],[745,651,657,659,655,702,779,822,846])
  y=np.interp(t,[.5,1,1.5,2,3,3.5,4,4.5,5.5],[690,549,540,532,535,550,574,591,589])
  cuff=pm([(x-68,y+8),(x-56,y-12),(x+25,y-30),(x+74,y+2),(x+110,720),(x-105,720)])
  fg=cv2.bitwise_or(fg,cuff)
  for k,q in PARTS.items():im=ink(im,ART[k],cv2.perspectiveTransform(np.float32(q)[None],trans)[0],fg)
 elif shot=='K05':
  pw=quad(TRACK['pw'],t);pc=quad(TRACK['pc'],t);fg=skin(im,45)
  glove=np.uint8(np.max(im,axis=2)<105)*255;fg=cv2.bitwise_or(fg,glove)
  # The cream request goes behind the white declaration as hands bring them together.
  cm=cv2.bitwise_or(fg,pm(pw)) if t>=1.75 else fg
  im=ink(im,ART['paper_cream'],pc,cm)
  # Remove invented source microprint. Reuse actual blank paper texture, keeping edges.
  q=np.float32(pw);center=q.mean(axis=0);inner=center+(q-center)*.93
  trans=cv2.getPerspectiveTransform(q,np.float32([[0,0],[599,0],[599,449],[0,449]]))
  plate=cv2.warpPerspective(im,trans,(600,450));plate=cv2.GaussianBlur(plate,(0,0),20)
  # White page is neutral; avoid skin/envelope from margins polluting the paper interior.
  col=np.median(plate[70:300,180:450].reshape(-1,3),axis=0)
  plate[:]=col;alpha=np.full((450,600),255,np.uint8);alpha[:6]=0;alpha[-6:]=0;alpha[:,:6]=0;alpha[:,-6:]=0;alpha=cv2.GaussianBlur(alpha,(13,13),2)
  pa=np.dstack([plate,alpha])
  if t>=1.625:im=ink(im,pa,inner,fg)
  im=ink(im,ART['paper_white'],pw,fg)
 elif shot=='NOTE' and t<1.84:
  # Envelope top edge occludes ink as the same note is pushed inside.
  clip=pm([(0,290),(560,326),(884,349),(1280,377),(1280,720),(0,720)])
  fg=cv2.bitwise_or(skin(im,62),clip);im=ink(im,ART['note'],quad(TRACK['note'],t),fg)
 elif shot=='K02' and t<1.875:im=ink(im,ART['paper_white'],quad(TRACK['handoff'],t),skin(im))
 return im
def timeline():
 rows=[('K01',F/'C04_K01_take01.mp4',0,3),('NOTE',V/'C04_K01_note_push_take01.mp4',.5,5.5),('K02',F/'C04_K02_take01.mp4',.5,4.5),('K03',F/'C04_K03_take01.mp4',0,3),('K04',F/'C04_K04_take01.mp4',.5,5.5),('K05',F/'C04_K05_take01.mp4',.5,4.5),('K07',F/'C04_K07_take01.mp4',0,5),('WINDOWS',V/'C04_K08_hinges_take01.mp4',1,4),('BOWLS',R/'C04_K08_three_visible_take01.mp4',2,4.25),('SPOON',R/'C04_K09_take02.mp4',.5,6),('END',None,0,4.75)]
 t=0;edl=[]
 for sh,p,a,b in rows:edl.append(dict(cut=sh,source=None if p is None else str(p.relative_to(SB)),source_in=a,source_out=b,start=t,end=t+b-a));t+=b-a
 return edl,t
def cap(text,pos='bottom'):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im);size=42;lh=55;lines=text.split('\n');tw=max(d.textlength(s,font=font(size)) for s in lines);hh=len(lines)*lh+20
 x=(W-tw)/2;y=38 if pos.startswith('top') else H-44-hh
 if pos=='top_right':x=W-tw-55;y=60
 d.rounded_rectangle((x-20,y,x+tw+20,y+hh),12,fill=(19,24,19,226))
 for j,s in enumerate(lines):d.text((x+tw/2,y+12+lh*j),s,font=font(size),fill='white',anchor='mt')
 return im
def ending():
 im=Image.new('RGB',(W,H),(28,27,22));d=ImageDraw.Draw(im)
 d.ellipse((1015,75,1175,235),fill=(118,75,156));d.ellipse((1050,48,1198,196),fill=(28,27,22))
 d.line((125,530,1155,530),fill=(139,119,76),width=2)
 d.text((640,183),'Q-AI Fair',font=font(85),fill=(250,247,231),anchor='mt')
 d.text((640,325),'AI 실행 사례, 지금 시작합니다.',font=font(42),fill=(250,247,231),anchor='mt')
 d.text((640,416),'품질팀 AI 성과 교류',font=font(28),fill=(191,181,159),anchor='mt')
 return im
def audio(duration,end):
 sf=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2');s=Synth(gain=-15,samplerate=SR);sid=s.sfload(str(sf));progs={0:42,1:43,2:70,3:0}
 for c,p in progs.items():s.program_select(c,sid,0,p)
 notes=[]
 def add(t,d,p,v,c):notes.append(dict(start=float(t),duration=d,pitch=p,velocity=v,channel=c))
 # Restrained, original mock-solemn pulse. Silence arrives at actual bowl extension.
 for i,t in enumerate(np.arange(.2,31.8,.8)):
  add(t,.55,[38,38,45,41,38,43,41,36][i%8],40,0)
  if i%4==0:add(t,1.5,[57,58,57,55][i//4%4],27,1)
 for t,p in [(36.65,50),(37.05,48),(37.65,43)]:add(t,.3,p,42,2)
 for p in [50,57,62]:add(end+.15,3.8,p,30,3)
 n=round(duration*SR);mix=np.zeros((n,2),np.float32);ev=[]
 for a in notes:ev.extend([(round(a['start']*SR),1,a),(min(n,round((a['start']+a['duration'])*SR)),0,a)])
 pos=0
 for idx,on,a in sorted(ev,key=lambda x:(x[0],x[1])):
  if idx>pos:mix[pos:idx]=np.frombuffer(s.generate(idx-pos),np.float32).reshape(-1,2);pos=idx
  (s.noteon(a['channel'],a['pitch'],a['velocity']) if on else s.noteoff(a['channel'],a['pitch']))
 if pos<n:mix[pos:]=np.frombuffer(s.generate(n-pos),np.float32).reshape(-1,2)
 mix*=.10/max(abs(mix).max(),1e-9)
 a,b=round(32*SR),round(36.6*SR);fade=round(.015*SR);mix[a-fade:a]*=np.linspace(1,0,fade)[:,None];mix[a:b]=0
 mix[:2400]*=np.linspace(0,1,2400)[:,None];mix[-24000:]*=np.linspace(1,0,24000)[:,None]
 p=WORK/'mix.wav';run(['-y','-v','error','-f','f32le','-ar',SR,'-ac',2,'-i','-','-c:a','pcm_f32le',p],input=mix.tobytes())
 dump(OUT/'audio_recipe.json',dict(source_audio='muted',music='Original local mock-solemn string pulse; silence at real bowls extension; quiet bassoon after single spoon appears',sfx='None: no invented physical impacts',soundfont=str(sf),soundfont_sha256=sha(sf),programs=progs,notes=notes,music_cut_seconds=32,actual_listening_verified=False))
 return p
def srt(t):
 z=round(t*1000);return f'{z//3600000:02d}:{z//60000%60:02d}:{z//1000%60:02d},{z%1000:03d}'
def main():
 edl,duration=timeline();assert duration<=60;end=edl[-1]['start']
 caps=[(.2,1.8,'숨소리도 내지 마라.','top'),(1.9,3,'꼬르륵…','top'),(3.2,6.8,'식사 · 물 · 수저 요청','bottom'),(8.25,11.8,'신고: 내부 탑승자 없음','bottom'),(12.2,14.8,'아무도 없는데, 웬 배식?','bottom'),(20.2,23.8,'이 말, 수저를 씁니까?','top'),(24.1,26,'안에는 아무도 없습니다.','bottom'),(37.05,39.5,'지휘관부터.','top_right')]
 ca=[(a,b,cap(txt,p)) for a,b,txt,p in caps];title=ending();sources={s['source'] for s in edl if s['source']};hashes={p:sha(SB/p) for p in sources}
 pic=WORK/'picture.mp4';n=0
 with (WORK/'render.log').open('wb') as log:
  enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',str(pic)],stdin=subprocess.PIPE,stderr=log)
  try:
   for seg in edl:
    count=0
    if not seg['source']:
     for k in range(round((seg['end']-seg['start'])*FPS)):enc.stdin.write(title.tobytes());n+=1;count+=1
    else:
     with av.open(str(SB/seg['source'])) as c:
      for f in c.decode(video=0):
       st=float(f.time)
       if st<seg['source_in']-1e-5:continue
       if st>=seg['source_out']-1e-5:break
       tt=seg['start']+st-seg['source_in'];im=Image.fromarray(picture(np.array(f.to_image()),seg['cut'],st)).convert('RGBA')
       for a,b,art in ca:
        if a<=tt<b:im.alpha_composite(art)
       enc.stdin.write(im.convert('RGB').tobytes());n+=1;count+=1
    assert count==round((seg['end']-seg['start'])*FPS),(seg,count)
    print(seg['cut'],count,flush=True)
  finally:enc.stdin.close();enc.wait()
 assert enc.returncode==0 and n==round(duration*FPS)
 wav=audio(duration,end);measured=loudness(wav);gain=min(-23-float(measured['input_i']),-3-float(measured['input_tp']))
 recipe=json.loads((OUT/'audio_recipe.json').read_text(encoding='utf8'));recipe.update(loudness_before_gain=measured,static_gain_db=gain,dynamic_normalization=False);dump(OUT/'audio_recipe.json',recipe)
 final=OUT/'C04_Q-AI_Fair_final_v13.mp4';run(['-y','-v','error','-i',pic,'-i',wav,'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',f'volume={gain}dB','-c:a','aac','-b:a','192k','-t',duration,'-movflags','+faststart',final])
 run(['-v','error','-i',final,'-f','null','-']);pts=[];tiles=[];picks=set(range(0,n,12))|{n-1}
 for seg in edl:picks|={round(seg['start']*FPS)+o for o in [-1,0,1]}
 with av.open(str(final)) as c:
  for i,f in enumerate(c.decode(video=0)):
   pts.append(float(f.time))
   if i in picks:
    im=f.to_image();im.save(QA/f'{i/FPS:06.3f}s.png');tile=Image.new('RGB',(320,204),(15,18,18));tile.paste(im.resize((320,180)),(0,24));ImageDraw.Draw(tile).text((8,3),f'{i/FPS:.3f}s',font=font(15),fill='white');tiles.append(tile)
 for k in range(math.ceil(len(tiles)/20)):
  ts=tiles[k*20:k*20+20];sheet=Image.new('RGB',(1280,204*math.ceil(len(ts)/4)))
  for j,im in enumerate(ts):sheet.paste(im,(j%4*320,j//4*204))
  sheet.save(OUT/f'review_contact_{k+1:02d}.jpg',quality=94)
 assert len(pts)==n and np.allclose(np.diff(pts),1/FPS)
 a=np.frombuffer(run(['-v','error','-i',final,'-vn','-ar',SR,'-ac',2,'-f','f32le','-']).stdout,np.float32);assert np.isfinite(a).all() and abs(a).max()<1
 ae=0;gaps=[];ac=0
 with av.open(str(final)) as c:
  for f in c.decode(audio=0):gaps.append(float(f.time)-ae);ae=float(f.time)+f.samples/f.sample_rate;ac+=1
 assert max(map(abs,gaps))<1/SR and abs(ae-duration)<=1024/SR
 assert hashes=={p:sha(SB/p) for p in sources}
 cs=[dict(start=a,end=b,text=txt,position=p) for a,b,txt,p in caps]+[dict(start=end,end=duration,text='Q-AI Fair\nAI 실행 사례, 지금 시작합니다.',position='ending')]
 (OUT/'C04_captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt(c["start"])} --> {srt(c["end"])}\n{c["text"]}' for i,c in enumerate(cs))+'\n',encoding='utf-8-sig')
 dump(OUT/'composite_tracking.json',dict(tracks=TRACK,tablet_parts=PARTS,method='Manual planes and original-colour foreground masks. Final rendered samples must be reviewed independently.',paper_words={'declaration':'신고서 / 내부 탑승자 없음','request':'요청 / 식사 · 물 · 수저'},tablet_words='AI 대조 · 확인 필요 / 신고서 탑승자 없음 / 첨부 요청 수저 요청',source_microprint='White K05 paper microprint is replaced with exact declaration, never claimed OCR.'))
 dump(OUT/'edit_manifest.json',dict(concept='C04 목마는 식사 중입니다',file=final.name,duration_seconds=duration,fps=FPS,resolution=[W,H],timeline=edl,captions=cs,source_sha256=hashes,source_audio='muted',source_files_unchanged=True,action_stills_inserted=False,actual_continuous_playback_verified=False,actual_listening_verified=False,status='SELF_QA_PENDING'))
 dump(OUT/'technical_validation.json',dict(file=final.name,sha256=sha(final),bytes=final.stat().st_size,video_frames=n,duration_seconds=duration,full_decode='PASS',video_pts_step_seconds=1/FPS,audio_peak=float(abs(a).max()),audio_nonfinite=0,audio_decode_frames=ac,audio_end_seconds=ae,max_audio_pts_gap_seconds=max(map(abs,gaps)),source_sha256_unchanged=True,actual_continuous_playback_verified=False,actual_listening_verified=False))
 print('DONE',duration,n,flush=True)
if __name__=='__main__':main()
