import render_c02 as r
import json, numpy as np, av
edl,duration=r.build_timeline();by={x['cut']:x for x in edl}
wav=r.audio(duration,by['K07']['start']+1.5,by['NEW_REACT']['start'],by['END']['start'])
m=r.loudness(wav);gain=min(-23-float(m['input_i']),-3-float(m['input_tp']))
rp=r.OUT/'audio_recipe.json';recipe=json.loads(rp.read_text(encoding='utf8'));recipe.update(loudness_before_gain=m,static_gain_db=gain,target_lufs=-23,target_true_peak_ceiling_dbfs=-3,dynamic_normalization=False);r.dump(rp,recipe)
final=r.OUT/'C02_Q-AI_Fair_final_v13.mp4'
r.run(['-y','-v','error','-i',r.WORK/'picture.mp4','-i',wav,'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',f'volume={gain}dB','-c:a','aac','-b:a','192k','-t',duration,'-movflags','+faststart',final])
r.run(['-v','error','-i',final,'-f','null','-'])
a=np.frombuffer(r.run(['-v','error','-i',final,'-vn','-ar',r.SR,'-ac',2,'-f','f32le','-']).stdout,np.float32)
assert np.isfinite(a).all() and abs(a).max()<1
pts=[]
with av.open(str(final)) as c:
 for f in c.decode(video=0):pts.append(float(f.time))
assert len(pts)==870 and np.allclose(np.diff(pts),1/24)
vp=r.OUT/'technical_validation.json';v=json.loads(vp.read_text(encoding='utf8'));v.update(sha256=r.sha(final),bytes=final.stat().st_size,audio_peak=float(abs(a).max()),loudness_after_static_gain=r.loudness(final),audio_remux_only=True,video_frame_count_reverified=870)
r.dump(vp,v);print(json.dumps(v,indent=2))
