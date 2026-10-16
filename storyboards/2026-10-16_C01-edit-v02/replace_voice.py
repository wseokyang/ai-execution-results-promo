"""Replace only K04 audio; copy the approved v01 video bitstream unchanged."""
from pathlib import Path
import subprocess,json,hashlib,shutil,wave

root=Path(__file__).resolve().parent
sb=root.parent
ff=sb/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
source=sb/'2026-10-16_C01-edit-v01/C01_review_edit_v01_55s.mp4'
ambient=sb/'2026-10-16_flow-run-05/C01_K04_take02.mp4'
voice=root/'C01_K04_D_qwen_take01.wav'
with wave.open(str(voice)) as w:
    seconds=w.getnframes()/w.getframerate()
if seconds>4.8:
    raise ValueError(f'Voice is {seconds:.3f}s, longer than the 4.8s slot; review timing first instead of cutting speech.')
out=root/'C01_review_edit_v02_55s.mp4'
filt=(
 '[0:a]atrim=0:21,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[pre];'
 '[0:a]atrim=start=27:end=55,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[post];'
 '[1:a]atrim=0:6,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=0.32[amb];'
 '[2:a]loudnorm=I=-18:TP=-2:LRA=7,aresample=48000,aformat=channel_layouts=stereo,adelay=1000|1000[voc];'
 '[amb][voc]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.89:level=false:latency=true,atrim=duration=6[mid];'
 '[pre][mid][post]concat=n=3:v=0:a=1[a]')
args=[str(ff),'-y','-hide_banner','-loglevel','error','-i',str(source),'-i',str(ambient),'-i',str(voice),
       '-filter_complex',filt,'-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t','55','-movflags','+faststart',str(out)]
p=subprocess.run(args,capture_output=True)
if p.returncode:raise RuntimeError(p.stderr.decode('utf8',errors='replace'))

def video_digest(path):
    p=subprocess.run([str(ff),'-v','error','-i',str(path),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-'],capture_output=True,check=True)
    return p.stdout.decode().strip()
old_hash=video_digest(source);new_hash=video_digest(out)
assert old_hash==new_hash,'Video packets changed unexpectedly'
def timed_video_packets(path):
    p=subprocess.run([str(ff),'-v','error','-i',str(path),'-map','0:v:0','-c','copy','-f','framehash','-'],capture_output=True,check=True)
    return '\n'.join(line for line in p.stdout.decode().splitlines() if line and not line.startswith('#'))
old_packets=timed_video_packets(source);new_packets=timed_video_packets(out)
old_rows=[[x.strip() for x in row.split(',')] for row in old_packets.splitlines()]
new_rows=[[x.strip() for x in row.split(',')] for row in new_packets.splitlines()]
assert len(old_rows)==len(new_rows)
timestamp_shift=int(new_rows[0][2])-int(old_rows[0][2])
for a,b in zip(old_rows,new_rows):
    assert a[0]==b[0] and a[3:]==b[3:],'Packet data or duration changed'
    assert int(b[1])-int(a[1])==timestamp_shift and int(b[2])-int(a[2])==timestamp_shift,'Relative frame timing changed'
assert abs(timestamp_shift/12288)<0.002,'Unexpectedly large mux timestamp shift'
decode=subprocess.run([str(ff),'-v','error','-i',str(out),'-f','null','-'],capture_output=True)
assert decode.returncode==0,decode.stderr
info=subprocess.run([str(ff),'-hide_banner','-i',str(out)],capture_output=True).stderr.decode('utf8',errors='replace')
(root/'media_info.txt').write_bytes(info.replace('\r\n','\n').encode('utf8'))
record={'status':'replacement_voice_review_pending','file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'base_edit':str(source.relative_to(sb)),'video_bitstream_sha256_before':old_hash,'video_bitstream_sha256_after':new_hash,'video_bitstream_identical':True,'video_relative_packet_timing_identical':True,'video_mux_timestamp_shift_seconds':timestamp_shift/12288,'video_packet_count':len(new_packets.splitlines()),
 'audio_edit':{'clip':'K04','timeline_region':[21,27],'new_voice':voice.name,'voice_start':22,'voice_end':22+seconds,'ambient_source':str(ambient.relative_to(sb)),'voice_seconds':seconds},
 'unchanged_content':'All visual cuts, captions, ending and dialogue outside K04 retained. Audio track encoded to AAC; original source files untouched.',
 'validation':{'full_decode_exit_code':decode.returncode,'listening':'not performed by assistant','user_confirmed_previous_K02_K06':'natural and intact','new_voice_user_approval':'pending'},
 'additional_Flow_credits':0,'paid_api_calls':0}
(root/'edit_manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
preview=Path('C:/Users/wseok/.codex/visualizations/2026/10/16/01a13daf-3732-7b90-99a8-92c605090d35')
for p in [out,voice]:shutil.copyfile(p,preview/p.name)
print(json.dumps(record,ensure_ascii=False))
