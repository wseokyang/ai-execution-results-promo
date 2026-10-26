"""Shared local-only media helpers. Callers own their output paths."""
from pathlib import Path
import sys,json,hashlib,subprocess,re,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
from tinysoundfont import Synth
SB=Path(__file__).resolve().parent.parent; ROOT=SB.parent
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W,H,FPS,SR=1280,720,24,48000
SF=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(n):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',n)
def run(args,**kw):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-5000:])
 return p

def caption(text,pos='bottom',x=None,y=None,size=42):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im);lines=text.split('\n');lh=55;tw=max(d.textlength(s,font=font(size)) for s in lines);hh=lh*len(lines)+20
 if x is None:x=(W-tw)/2
 if y is None:y=43 if pos=='top' else H-44-hh
 d.rounded_rectangle((x-20,y,x+tw+20,y+hh),12,fill=(8,17,24,225))
 for j,s in enumerate(lines):d.text((x+tw/2,y+12+j*lh),s,font=font(size),anchor='mt',fill='white')
 return im

def ending(tagline,accent=(198,89,30)):
 im=Image.new('RGB',(W,H),(15,25,34));d=ImageDraw.Draw(im)
 d.line((168,528,1112,528),fill=accent,width=2)
 d.text((640,188),'Q-AI Fair',font=font(72),anchor='mt',fill=(250,249,241))
 d.text((640,318),tagline,font=font(40),anchor='mt',fill=(240,244,241))
 d.text((640,412),'품질팀 AI 성과 교류회',font=font(36),anchor='mt',fill=(211,226,228))
 return im

def loudness(p):
 r=run(['-hide_banner','-i',p,'-af','loudnorm=I=-23:TP=-3:LRA=11:print_format=json','-f','null','-'])
 d=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr.decode(errors='replace'))[-1])
 return {k:float(v) for k,v in d.items() if k.startswith('input_')}

def synthesize(notes,programs,duration,wav,rests=(),effects=()):
 s=Synth(gain=-15,samplerate=SR);sid=s.sfload(str(SF))
 for ch,p in programs.items():s.program_select(ch,sid,0,p)
 n=round(duration*SR);mix=np.zeros((n,2),np.float32);events=[]
 for no in notes:
  events.extend([(round(no['start']*SR),1,no),(min(n,round((no['start']+no['duration'])*SR)),0,no)])
 pos=0
 for idx,on,no in sorted(events,key=lambda a:(a[0],a[1])):
  idx=min(n,idx)
  if idx>pos:mix[pos:idx]=np.frombuffer(s.generate(idx-pos),np.float32).reshape(-1,2);pos=idx
  (s.noteon if on else s.noteoff)(no['channel'],no['pitch'],*([no['velocity']] if on else []))
 if pos<n:mix[pos:]=np.frombuffer(s.generate(n-pos),np.float32).reshape(-1,2)
 for a,b in rests:
  aa,bb=round(a*SR),round(b*SR);fade=round(.03*SR)
  mix[max(0,aa-fade):aa]*=np.linspace(1,0,min(fade,aa))[:,None];mix[aa:bb]=0;mix[bb:min(n,bb+fade)]*=np.linspace(0,1,min(fade,n-bb))[:,None]
 for event in effects:
  # Optional small, short texture; never a voice. Its actual visual trigger must be recorded by caller.
  ns=round(event.get('duration',.08)*SR);t=np.arange(ns)/SR;f=event.get('frequency',950)
  x=np.sin(2*np.pi*f*t)*np.exp(-t*50);x[:min(240,ns)]*=np.linspace(0,1,min(240,ns));x[-min(240,ns):]*=np.linspace(1,0,min(240,ns));x*=event.get('peak',.01)
  j=round(event['at']*SR);mix[j:j+ns]+=x[:,None]
 mix[:2400]*=np.linspace(0,1,2400)[:,None];mix[-36000:]*=np.linspace(1,0,36000)[:,None]
 run(['-y','-v','error','-f','f32le','-ar',SR,'-ac',2,'-i','-','-c:a','pcm_f32le',wav],input=mix.tobytes())
 m=loudness(wav);gain=min(-23-m['input_i'],-3.3-m['input_tp']);return gain,m

def mux(picture,wav,output,duration,gain):
 run(['-y','-v','error','-i',picture,'-i',wav,'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',f'volume={gain}dB','-c:a','aac','-b:a','192k','-t',duration,'-movflags','+faststart',output])

def technical_qa(video,out,duration,boundaries=()):
 out=Path(out);frames=out/'review_frames';frames.mkdir(exist_ok=True);run(['-v','error','-i',video,'-f','null','-']);pts=[];tiles=[];count=round(duration*FPS)
 picks=set(range(0,count,12))|{count-1}
 for t in boundaries:picks|={round(t*FPS)+j for j in [-1,0,1]}
 with av.open(str(video)) as c:
  assert len(c.streams.video)==1 and len(c.streams.audio)==1
  for i,f in enumerate(c.decode(video=0)):
   pts.append(float(f.time))
   if i not in picks:continue
   im=f.to_image();im.save(frames/f'{i/FPS:06.3f}s.png');tile=Image.new('RGB',(320,204),(15,23,31));tile.paste(im.resize((320,180)),(0,24));ImageDraw.Draw(tile).text((8,2),f'{i/FPS:.3f}s',font=font(15),fill='white');tiles.append(tile)
 for j in range(math.ceil(len(tiles)/12)):
  sub=tiles[j*12:(j+1)*12];sheet=Image.new('RGB',(1280,204*math.ceil(len(sub)/4)),(15,23,31))
  for k,im in enumerate(sub):sheet.paste(im,(k%4*320,k//4*204))
  sheet.save(out/f'contact_{j+1:02d}.jpg',quality=94)
 assert len(pts)==count and np.allclose(np.diff(pts),1/FPS)
 end=0;gaps=[];peak=0
 with av.open(str(video)) as c:
  for f in c.decode(audio=0):
   gaps.append(float(f.time)-end);end=float(f.time)+f.samples/f.sample_rate;a=f.to_ndarray();assert np.isfinite(a).all();peak=max(peak,float(abs(a).max()))
 assert peak<1 and max(map(abs,gaps))<1/SR and abs(end-duration)<=1024/SR
 m=loudness(video);assert -24<=m['input_i']<=-22 and m['input_tp']<=-3
 q=dict(file=Path(video).name,sha256=sha(video),bytes=Path(video).stat().st_size,duration_seconds=duration,frames=count,fps=FPS,resolution=[W,H],audio_rate=SR,audio_channels=2,full_decode='PASS',audio_peak=peak,audio_end=end,max_audio_pts_gap=max(map(abs,gaps)),loudness=m,actual_listening_verified=False,actual_continuous_playback_verified=False,visual_review='PENDING')
 dump(out/'technical_qa.json',q);return q
