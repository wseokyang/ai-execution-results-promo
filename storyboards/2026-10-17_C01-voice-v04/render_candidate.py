"""Render a Flow voice audition in the existing K04 edit, preserving video packets."""
from pathlib import Path
import subprocess, json, hashlib, shutil, sys

root=Path(__file__).resolve().parent
sb=root.parent
ff=sb/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
run=sb/'2026-10-17_flow-run-07'
take=int(sys.argv[1])
tag=f'take{take:02d}'
inspection=json.loads((run/f'C01_K04_D_voice_{tag}_inspection.json').read_text(encoding='utf8'))
words=[w for s in inspection['segments'] for w in s['words']]
if not words:
    raise RuntimeError('No recognized speech; inspect before rendering.')
start=max(0,words[0]['start']-0.20)
end=min(8,words[-1]['end']+0.40)
bound_file=root/'voice_trim_bounds.json'
bounds=json.loads(bound_file.read_text(encoding='utf8')) if bound_file.exists() else {}
trim_basis='all recognized words plus 0.20s before/0.40s after; source origin retained when earlier'
if tag in bounds:
    start,end=bounds[tag]['source_seconds']
    trim_basis=bounds[tag]['reason']
duration=end-start
if duration>4.8:
    raise RuntimeError('Complete speech and margins exceed slot; do not cut or speed up speech.')
voice=run/f'C01_K04_D_voice_{tag}.mp4'
segment=root/f'C01_K04_Flow_{tag}_segment.wav'
subprocess.run([str(ff),'-y','-v','error','-i',str(voice),'-vn','-af',f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS',
                '-c:a','pcm_f32le','-ar','48000',str(segment)],check=True)
source=sb/'2026-10-16_C01-edit-v01/C01_review_edit_v01_55s.mp4'
ambient=sb/'2026-10-16_flow-run-05/C01_K04_take02.mp4'
out=root/f'C01_review_edit_v04_{tag}_55s.mp4'
filt=(
 '[0:a]atrim=0:21,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[pre];'
 '[0:a]atrim=start=27:end=55,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[post];'
 '[1:a]atrim=0:6,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=0.32[amb];'
 '[2:a]loudnorm=I=-18:TP=-2:LRA=7,aresample=48000,aformat=channel_layouts=stereo,adelay=1000|1000[voc];'
 '[amb][voc]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.89:level=false:latency=true,atrim=duration=6[mid];'
 '[pre][mid][post]concat=n=3:v=0:a=1[a]')
subprocess.run([str(ff),'-y','-v','error','-i',str(source),'-i',str(ambient),'-i',str(segment),'-filter_complex',filt,
               '-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',
               '-t','55','-movflags','+faststart',str(out)],check=True)
def packets(path):
    p=subprocess.run([str(ff),'-v','error','-i',str(path),'-map','0:v:0','-c','copy','-f','framehash','-'],capture_output=True,check=True)
    return [[x.strip() for x in l.split(',')] for l in p.stdout.decode().splitlines() if l and not l.startswith('#')]
a,b=packets(source),packets(out)
assert len(a)==len(b)==1320
shift=int(b[0][2])-int(a[0][2])
for x,y in zip(a,b):
    assert x[0]==y[0] and x[3:]==y[3:]
    assert int(y[1])-int(x[1])==shift and int(y[2])-int(x[2])==shift
assert abs(shift/12288)<0.002
subprocess.run([str(ff),'-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
excerpt=root/f'C01_K04_Flow_{tag}_context_25s.mp4'
subprocess.run([str(ff),'-y','-v','error','-ss','17','-i',str(out),'-t','25','-c:v','libx264','-preset','veryfast','-crf','18',
                '-c:a','aac','-b:a','192k','-movflags','+faststart',str(excerpt)],check=True)
subprocess.run([str(ff),'-v','error','-i',str(excerpt),'-f','null','-'],capture_output=True,check=True)
record={'status':'voice_comparison_candidate_not_final','take':take,'source_original':str(voice.relative_to(sb)),
        'original_sha256':inspection['sha256'],'source_audio_trim_seconds':[start,end],'trim_basis':trim_basis,
        'placement_seconds':[22,22+duration],'recognized_speech_in_full_edit':[22+words[0]['start']-start,22+words[-1]['end']-start],
        'voice_speed_change':False,'voice_pitch_change':False,'intermediate_wav':'pcm_f32le to preserve AAC decoder overshoots before normalization',
        'audio_mix':'existing K04 ambience0.32; voice loudnorm-18LUFS; limiter0.89 no automatic boost; AAC192k',
        'video_packet_count':1320,'video_payload_and_relative_timing_identical':True,'mux_timestamp_shift_seconds':shift/12288,
        'full_decode_pass':True,'context_decode_pass':True,'actual_listening':False,
        'new_voice_user_acceptance':('selected by user: 세 번째로 진행' if take==3 else 'comparison only; take03 subsequently selected'),
        'originals_reencoded':False,'BGM_added':False,
        'files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [out,excerpt,segment]]}
(root/f'edit_manifest_{tag}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
preview=Path('C:/Users/wseok/.codex/visualizations/2026/10/16/01a13daf-3732-7b90-99a8-92c605090d35')
for p in [out,excerpt,segment,voice]:
    shutil.copyfile(p,preview/p.name)
print(json.dumps(record,ensure_ascii=False),flush=True)
