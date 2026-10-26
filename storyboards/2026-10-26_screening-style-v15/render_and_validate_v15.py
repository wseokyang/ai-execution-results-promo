"""Reproducible local V15 styling pass. No browser, paid API, or original mutation.
Run C03/render_c03_picture_v15.py first, then this script. Output scoped to own folder.
"""
from pathlib import Path
import sys,json,subprocess,hashlib,re,math,copy,concurrent.futures
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
from tinysoundfont import Synth
OUT=Path(__file__).resolve().parent; ROOT=OUT.parent.parent; SB=OUT.parent
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W,H,FPS,SR=1280,720,24,48000
D=json.loads((SB/'2026-10-25_final-watch-v14/delivery_manifest.json').read_text(encoding='utf8'))
FILMS={x['concept_id']:x for x in D['films'] if x['concept_id'] in ['C02','C03','C04','C05','C06']}
START={'C02':31.5,'C03':37,'C04':38.75,'C05':41.75,'C06':44}
TAG={'C02':'AI 실행의 과정까지, 함께 봐요.','C03':'AI 실행의 과정까지, 함께 봐요.','C04':'AI 실행 사례, 지금 시작합니다.','C05':'AI 실행의 과정까지, 함께 봐요.','C06':'직접 해본 방법을 함께 봐요.'}
DESCRIPTION='품질팀 AI 성과 교류회'

def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def font(n):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',n)
def run(args,**kw):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-4000:])
 return p

def loudness(p):
 r=run(['-hide_banner','-i',p,'-af','loudnorm=I=-23:TP=-3:LRA=11:print_format=json','-f','null','-'])
 d=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr.decode(errors='replace'))[-1])
 return {k:float(v) for k,v in d.items() if k.startswith('input_')}

def card(cid):
 bg=(28,27,22) if cid=='C04' else (15,25,34)
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
 if cid=='C04':
  d.ellipse((1015,75,1175,235),fill=(118,75,156));d.ellipse((1050,48,1198,196),fill=bg)
  d.line((125,530,1155,530),fill=(139,119,76),width=2)
 elif cid=='C02':
  for x,y in [(74,80),(1160,98),(90,590),(1168,605)]:d.ellipse((x-7,y-7,x+7,y+7),fill=(214,65,63))
  d.line((76,81,1160,98,1168,605,90,590,76,81),fill=(62,37,40),width=1)
 else:
  d.line((175,528,1105,528),fill=(56,91,100),width=2)
 d.text((640,188),'Q-AI Fair',font=font(72),anchor='mt',fill=(250,249,241))
 d.text((640,318),TAG[cid],font=font(40),anchor='mt',fill=(240,244,241))
 d.text((640,412),DESCRIPTION,font=font(36),anchor='mt',fill=(211,226,228))
 return im

def c05_overlay():
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 d.rounded_rectangle((157,483,1123,684),18,fill=(9,18,24,236))
 d.text((640,495),'Q-AI Fair',font=font(68),anchor='mt',fill='white')
 d.text((640,580),TAG['C05'],font=font(36),anchor='mt',fill=(245,249,249))
 d.text((640,634),DESCRIPTION,font=font(34),anchor='mt',fill=(219,237,239))
 return im

def packet_hash(path):
 h=hashlib.sha256()
 with av.open(str(path)) as c:
  for p in c.demux(audio=0):
   if p.size:h.update(bytes(p))
 return h.hexdigest()

def render_picture(cid):
 folder=OUT/cid;src=ROOT/FILMS[cid]['file'];pic=folder/(cid+'_picture_v15.mp4')
 if cid=='C03':
  assert pic.exists();return pic
 finalcard=card(cid) if cid!='C05' else c05_overlay()
 finalcard.save(folder/'ending_art_v15.png')
 orig_end=[]
 if cid=='C05':
  raw=SB/'2026-10-23_C06-C05-flow-run03/C05_K08_take02.mp4'
  with av.open(str(raw)) as c:
   orig_end=[f.to_image() for f in c.decode(video=0) if 1.75-1e-6<=float(f.time)<6.75-1e-6]
  assert len(orig_end)==120
 with (folder/'render_stderr.txt').open('wb') as log:
  proc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-threads','2','-pix_fmt','yuv420p',str(pic)],stdin=subprocess.PIPE,stderr=log)
  n=0
  try:
   with av.open(str(src)) as c:
    for i,f in enumerate(c.decode(video=0)):
     if i>=round(START[cid]*FPS):
      if cid=='C05':
       im=orig_end[i-round(START[cid]*FPS)].convert('RGBA');im.alpha_composite(finalcard);im=im.convert('RGB')
      else:im=finalcard
     else:im=f.to_image()
     proc.stdin.write(im.tobytes());n+=1
  finally:proc.stdin.close();proc.wait()
 assert proc.returncode==0 and n==round(FILMS[cid]['duration_seconds']*FPS)
 return pic

def score_c03():
 duration=43.;sf=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
 s=Synth(gain=-15,samplerate=SR);sid=s.sfload(str(sf));programs={0:43,1:45,2:70,3:0}
 for ch,p in programs.items():s.program_select(ch,sid,0,p)
 notes=[]
 def add(t,d,p,v,ch):notes.append(dict(start=round(t,4),duration=d,pitch=p,velocity=v,channel=ch))
 rests=[(12.35,13.6),(18.75,19.5),(28.65,29.2)]
 # A restrained absurd-logistics chamber march. Each arrival has a distinct response.
 for k,t in enumerate(np.arange(.25,36.5,.8)):
  if any(a<=t<b for a,b in rests):continue
  add(float(t),.35,[38,45,41,45,36,43,40,43][k%8],34,0)
  if k%2==0:add(float(t)+.12,.22,[62,65,69,67][k//2%4],26,1)
 for t,p in [(1.6,57),(2.4,60),(3.2,58),(6.15,62),(6.95,65),(7.75,69),(14,61),(14.8,64),(15.6,68),(19.65,60),(20.45,58),(21.25,57)]:add(t,.48,p,29,2)
 for t,ps in [(23.5,[53,60,65]),(26.75,[55,62,65]),(29.3,[50,57,62]),(32.1,[53,60,65]),(35.1,[55,62,67]),(37.1,[50,57,62,65]),(40,[50,57,62])]:
  for p in ps:add(t,1.55 if t<37 else 2.,p,29,3)
 n=round(duration*SR);mix=np.zeros((n,2),np.float32);events=[]
 for no in notes:
  events.extend([(round(no['start']*SR),1,no),(min(n,round((no['start']+no['duration'])*SR)),0,no)])
 pos=0
 for idx,on,no in sorted(events,key=lambda a:(a[0],a[1])):
  if idx>pos:mix[pos:idx]=np.frombuffer(s.generate(idx-pos),np.float32).reshape(-1,2);pos=idx
  (s.noteon if on else s.noteoff)(no['channel'],no['pitch'],*([no['velocity']] if on else []))
 if pos<n:mix[pos:]=np.frombuffer(s.generate(n-pos),np.float32).reshape(-1,2)
 for a,b in rests:
  aa,bb=round(a*SR),round(b*SR);f=round(.03*SR)
  mix[aa-f:aa]*=np.linspace(1,0,f)[:,None];mix[aa:bb]=0;mix[bb:bb+f]*=np.linspace(0,1,f)[:,None]
 mix[:2400]*=np.linspace(0,1,2400)[:,None];mix[-36000:]*=np.linspace(1,0,36000)[:,None]
 wav=OUT/'C03/C03_original_score_v15.wav'
 run(['-y','-v','error','-f','f32le','-ar',SR,'-ac',2,'-i','-','-c:a','pcm_f32le',wav],input=mix.tobytes())
 measured=loudness(wav);gain=min(-23-measured['input_i'],-3-measured['input_tp'])
 dump(OUT/'C03/audio_recipe.json',dict(music='Original local sparse chamber march; contrabass/pizzicato/bassoon/piano. No physical effect or voice inserted.',soundfont=str(sf),soundfont_sha256=sha(sf),programs=programs,notes=notes,rests_seconds=rests,fade_in_seconds=.05,fade_out_seconds=.75,source_speech='not included',loudness_before_gain=measured,static_gain_db=gain,actual_listening_verified=False))
 return wav,gain

def captions_and_manifest(cid,final,base,gain):
 original=json.loads((base.parent/'edit_manifest.json').read_text(encoding='utf8'))
 m=copy.deepcopy(original);m.update(file=final.name,version=15,base_file=str(base.relative_to(ROOT)),base_sha256=sha(base),actual_listening_verified=False,actual_continuous_playback_verified=False,flow_credits_used=0,status='V15_TECHNICAL_AND_VISUAL_SAMPLE_REVIEW_PENDING',new_style=dict(font='Malgun Gothic Bold',body_px=42,end_title_px=68 if cid=='C05' else 72,event_definition_px=34 if cid=='C05' else (35 if cid=='C03' else 36),event_name='Q-AI Fair',event_definition=DESCRIPTION),audio_change=dict(source_audio_policy='All original spoken audio remains excluded',gain_db=gain,bgm='new local chamber score' if cid=='C03' else 'existing genre-specific BGM and effects retained',actual_listening_verified=False),v15_changes=['Common event definition and larger readable final typography','Original action sequence, source timings and total duration retained'])
 if cid=='C03':
  m['source_audio']='Original generated voices excluded; new local instrumental score';m['v15_changes']+=['Discovery caption shifted to x64/y43 and set42px','New local chamber score']
 for c in m.get('captions',[]):
  if c.get('start')==START[cid]:c['text']='Q-AI Fair\n'+TAG[cid]+'\n'+DESCRIPTION
  if cid=='C03' and c.get('kind')=='discovery':c['box']=dict(text_left_px=64,box_left_px=47,top_px=43);c['font_px']=42;c['placement']='상단 왼쪽: 글자 시작 x64px, 배경박스 왼쪽 x47px, 박스 위 y43px. 두 파일과 R 얼굴을 비움.'
 m['limitations']=list(dict.fromkeys(m.get('limitations',[])+['V15 is not realtime playback or actual listening certified; numerical tests and inspected frame samples only.']))
 dump(final.parent/'edit_manifest.json',m)
 def ts(t):
  z=round(t*1000);return f'{z//3600000:02d}:{z//60000%60:02d}:{z//1000%60:02d},{z%1000:03d}'
 (final.parent/(cid+'_captions_v15.srt')).write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["text"]}' for i,c in enumerate(m.get('captions',[])))+'\n',encoding='utf-8-sig')
 return m

def validate(cid,final,base):
 expected=FILMS[cid]['duration_seconds'];run(['-v','error','-i',final,'-f','null','-'])
 measured=loudness(final);pts=[];tiles=[];folder=final.parent;frames=folder/'review_frames';frames.mkdir(exist_ok=True)
 picks=set(range(0,round(expected*FPS),12))|{round(expected*FPS)-1}
 for t in [START[cid],26.25,28.85] if cid=='C03' else [START[cid]]:
  picks|={round(t*FPS)+d for d in [-1,0,1]}
 with av.open(str(final)) as c:
  assert len(c.streams.video)==1 and len(c.streams.audio)==1
  for i,f in enumerate(c.decode(video=0)):
   pts.append(float(f.time))
   if i not in picks:continue
   im=f.to_image();im.save(frames/f'{i/FPS:06.3f}s.png');tile=Image.new('RGB',(320,204),(15,23,31));tile.paste(im.resize((320,180)),(0,24));ImageDraw.Draw(tile).text((8,2),f'{cid} {i/FPS:.3f}s',font=font(15),fill='white');tiles.append(tile)
 for j in range(math.ceil(len(tiles)/12)):
  sub=tiles[j*12:(j+1)*12];sheet=Image.new('RGB',(1280,204*math.ceil(len(sub)/4)),(15,23,31))
  for k,im in enumerate(sub):sheet.paste(im,(k%4*320,k//4*204))
  sheet.save(folder/f'contact_{j+1:02d}.jpg',quality=94)
 # Trailer-like thumbnail uses an actual video frame rather than invented art.
 with av.open(str(final)) as c:
  for i,f in enumerate(c.decode(video=0)):
   if i==round(min(6,expected/4)*FPS):f.to_image().save(folder/'thumbnail.jpg',quality=94);break
 end=0.;gaps=[];peak=0.;finite=True
 with av.open(str(final)) as c:
  for f in c.decode(audio=0):
   gaps.append(float(f.time)-end);end=float(f.time)+f.samples/f.sample_rate
   a=f.to_ndarray();finite=finite and np.isfinite(a).all();peak=max(peak,float(np.abs(a).max()))
 assert len(pts)==round(expected*FPS) and np.allclose(np.diff(pts),1/FPS)
 assert finite and peak<1 and max(map(abs,gaps))<1/SR and abs(end-expected)<=1024/SR
 assert -24<=measured['input_i']<=-22 and measured['input_tp']<=-3
 assert sha(base)==FILMS[cid]['sha256']
 unchanged_packet=packet_hash(final)==packet_hash(base) if cid in ['C02','C04'] else None
 if unchanged_packet is not None:assert unchanged_packet
 q=dict(file=final.name,sha256=sha(final),bytes=final.stat().st_size,duration_seconds=expected,video_frames=len(pts),video_fps=24,resolution=[W,H],audio_streams=1,audio_rate=SR,audio_channels=2,full_decode='PASS',max_audio_gap_seconds=max(map(abs,gaps)),audio_end_seconds=end,audio_peak_linear=peak,nonfinite_samples=0,loudness=measured,original_base_hash_unchanged=True,original_audio_packets_identical=unchanged_packet,actual_continuous_playback_verified=False,actual_listening_verified=False,visual_sample_review='PENDING')
 dump(folder/'technical_qa.json',q)
 print('VALIDATED',cid,measured,flush=True);return q

def process(cid):
 info=FILMS[cid];base=ROOT/info['file'];assert sha(base)==info['sha256']
 pic=render_picture(cid);final=OUT/cid/(cid+'_Q-AI_Fair_screening_v15.mp4')
 if cid=='C03':audio,gain=score_c03()
 else:audio=base;gain={'C05':-1.15,'C06':-1.99}.get(cid,0.)
 args=['-y','-v','error','-i',pic,'-i',audio,'-map','0:v:0','-map','1:a:0','-c:v','copy']
 if cid in ['C02','C04']:args+=['-c:a','copy']
 else:args+=['-af',f'volume={gain}dB','-c:a','aac','-b:a','192k']
 args+=['-t',info['duration_seconds'],'-movflags','+faststart',final];run(args)
 captions_and_manifest(cid,final,base,gain);return validate(cid,final,base)

if __name__=='__main__':
 ids=sys.argv[1:] or list(FILMS)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(process,ids))
 allqa=[json.loads((OUT/c/'technical_qa.json').read_text(encoding='utf8')) for c in FILMS if (OUT/c/'technical_qa.json').exists()]
 dump(OUT/'delivery_manifest.json',dict(version='V15',films=[dict(concept_id=c,title=FILMS[c]['title'],file=str((OUT/c/(c+'_Q-AI_Fair_screening_v15.mp4')).relative_to(ROOT)),duration_seconds=FILMS[c]['duration_seconds'],sha256=json.loads((OUT/c/'technical_qa.json').read_text(encoding='utf8'))['sha256'],actual_listening_verified=False,actual_continuous_playback_verified=False) for c in FILMS if (OUT/c/'technical_qa.json').exists()],qa=allqa,flow_requests=0,credits_spent=0,originals_preserved=True))
