"""Automatic transcription only; not listening or pronunciation certification."""
from pathlib import Path
import sys, json, subprocess
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from faster_whisper import WhisperModel
import numpy as np
root=Path(__file__).resolve().parent
source=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'C03_review_edit_v02_46s.mp4'
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=8,
                  download_root='C:/Users/wseok/.cache/codex-media-tools/models',
                  local_files_only=True)
ff=root.parent/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
pcm=subprocess.run([str(ff),'-v','error','-i',str(source),
    '-vn','-af','pan=mono|c0=0.5*c0+0.5*c1','-ar','16000','-f','f32le','-'],
    capture_output=True,check=True).stdout
segments,info=model.transcribe(np.frombuffer(pcm,np.float32),
    language='ko',beam_size=5,word_timestamps=True,vad_filter=True,
    condition_on_previous_text=False)
items=[]
for s in segments:
    row={'start':s.start,'end':s.end,'text':s.text,
         'words':[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability}
                  for w in (s.words or [])]}
    items.append(row)
    print(row['start'],row['end'],row['text'],flush=True)
(source.parent/'audio_transcription.json').write_text(json.dumps({
    'method':'local faster-whisper small int8; explicit0.5L+0.5R mono downmix',
    'file':source.name,
    'actual_listening':False,'pronunciation_pass':None,'segments':items
},ensure_ascii=False,indent=2),encoding='utf-8')
