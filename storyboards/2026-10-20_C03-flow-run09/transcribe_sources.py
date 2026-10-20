"""Local ASR aids edit timing; never certifies listening or pronunciation."""
from pathlib import Path
import sys,json,subprocess
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from faster_whisper import WhisperModel
import numpy as np
P=Path(__file__).resolve().parent
ff=P.parent/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=8,download_root='C:/Users/wseok/.cache/codex-media-tools/models',local_files_only=True)
target=P/'audio_transcription.json'
data=json.loads(target.read_text(encoding='utf-8')) if target.exists() else {'actual_listening':False,'method':'faster-whisper small CPU int8; explicit .5L+.5R downmix','files':{}}
for name in sys.argv[1:]:
 pcm=subprocess.run([str(ff),'-v','error','-i',str(P/name),'-vn','-af','pan=mono|c0=0.5*c0+0.5*c1','-ar','16000','-f','f32le','-'],capture_output=True,check=True).stdout
 segs,info=model.transcribe(np.frombuffer(pcm,np.float32),language='ko',beam_size=5,word_timestamps=True,vad_filter=True,condition_on_previous_text=False)
 rows=[]
 for s in segs:
  rows.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in (s.words or [])]})
 data['files'][name]=rows
 print(name,[(s['start'],s['end'],s['text']) for s in rows],flush=True)
 target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
