"""Stream-copy approved V16 pictures, mux new music and inspect actual outputs."""
from pathlib import Path
import sys,json,hashlib,subprocess,re
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import numpy as np
import av
from create_scores import FF,DUR,SILENCE,measure
V=Path(__file__).resolve().parent
IDS=['C02','C03','C04','C05','C06','C08','C09']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True)
 if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-4000:])
 return p
def packets(path):
 with av.open(str(path)) as c:
  s=c.streams.video[0]
  return [(float(p.pts*p.time_base),float(p.dts*p.time_base),hashlib.sha256(bytes(p)).hexdigest()) for p in c.demux(s) if p.size and p.pts is not None]
def audio(path):
 b=run(['-v','error','-i',path,'-map','0:a:0','-f','f32le','-ac','2','-ar','48000','-']).stdout
 return np.frombuffer(b,np.float32).reshape(-1,2)
def audioqa(path,cid):
 a=audio(path); checks=[]
 for start,end in SILENCE[cid]:
  # Check the core, excluding AAC window and deliberate anti-click edges.
  x=a[round((start+.05)*48000):round((end-.05)*48000)]
  rms=float(np.sqrt(np.mean(x*x)))
  checks.append({'start':start,'end':end,'core_rms_dbfs':float(20*np.log10(max(rms,1e-12))),'pass':rms<10**(-70/20)})
 m=measure(path)
 return {'loudness':m,'samples':len(a),'peak_sample':float(np.max(np.abs(a))),
 'non_finite_samples':int(np.sum(~np.isfinite(a))), 'silence_windows':checks,
 'loudness_pass':-19.2<=m['input_i']<=-17.8,'true_peak_pass':m['input_tp']<=-2,
 'duration_pass':abs(len(a)/48000-DUR[cid])<.05,'actual_listening_performed':False}

def main():
 delivery=[]
 for cid in IDS:
  folder=V/cid; pic=folder/f'{cid}_picture_v16.mp4'; wav=V/'audio'/cid/f'{cid}_score_v16.wav'
  final=folder/f'{cid}_Q-AI_Fair_qrew_v16.mp4'
  run(['-v','error','-y','-i',pic,'-i',wav,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t',DUR[cid],'-movflags','+faststart',final])
  with av.open(str(final)) as c:
   s=c.streams.video[0]; pts=[float(f.pts*f.time_base) for f in c.decode(s)]
   width,height=s.width,s.height
  aq=audioqa(final,cid)
  q={'concept_id':cid,'file':final.name,'sha256':sha(final),'picture_sha256':sha(pic),'score_sha256':sha(wav),
   'duration':DUR[cid],'frames':len(pts),'size':[width,height],'fps':24,
   'full_video_decode_pass':len(pts)==round(DUR[cid]*24),'pts_contiguous_pass':bool(np.allclose(pts,np.arange(len(pts))/24,atol=1e-6)),
   'video_packets_identical_to_picture':packets(pic)==packets(final),'audio':aq,
   'realtime_continuous_playback_performed':False,'actual_listening_performed':False}
  q['pass']=all([q['full_video_decode_pass'],q['pts_contiguous_pass'],q['video_packets_identical_to_picture'],aq['loudness_pass'],aq['true_peak_pass'],aq['duration_pass'],aq['non_finite_samples']==0,*[v['pass'] for v in aq['silence_windows']]])
  (folder/'final_technical_qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
  if not q['pass']:raise AssertionError(q)
  delivery.append({'concept_id':cid,'path':str(final.relative_to(V)).replace('\\','/'),'seconds':DUR[cid],'sha256':q['sha256'],'qa':'PASS'})
  print(cid,'PASS',DUR[cid],aq['loudness'],flush=True)
 c7=audioqa(V/'audio/C07/C07_score_v16.wav','C07')
 (V/'audio/C07/audio_technical_qa.json').write_text(json.dumps(c7,ensure_ascii=False,indent=2),encoding='utf8')
 (V/'delivery_manifest.json').write_text(json.dumps({'version':'V16','films':delivery,'C07':'storyboard and audio demo only; no new video','flow_credits_spent':0,'paid_external_api_calls':0,'verification_scope':'Full decode, timestamps, video-packet identity, audio measurements, selected rendered frames; not realtime playback or listening.'},ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
