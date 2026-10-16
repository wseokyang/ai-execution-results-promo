from pathlib import Path
import sys,json,os,time,subprocess
sys.path.insert(0,r'C:\Users\wseok\.cache\codex-media-tools\faster-whisper')
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
from faster_whisper import WhisperModel
import numpy as np
root=Path(__file__).resolve().parent
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=8,download_root=r'C:\Users\wseok\.cache\codex-media-tools\models')
files=[root.parent/'2026-10-16_flow-run-03'/'C01_K02_take01.mp4',root.parent/'2026-10-16_flow-run-04'/'C01_K05_take01.mp4',root/'C01_K06_take01.mp4',root/'C01_K07_take01.mp4',root/'C01_K04_take02.mp4']
results=[]
for path in files:
    ffmpeg=root.parent/'2026-10-15_flow-pilot-01' /'.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
    decoded=subprocess.run([str(ffmpeg),'-v','error','-i',str(path),'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True,check=True).stdout
    samples=np.frombuffer(decoded,dtype=np.float32)
    segments,info=model.transcribe(samples,language='ko',beam_size=5,vad_filter=True,word_timestamps=True,condition_on_previous_text=False)
    row={'file':str(path),'model':'faster-whisper small CPU int8','scope':'automatic transcription only; not listening, speaker verification, or lipsync approval','segments':[{'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in (s.words or [])]} for s in segments]}
    results.append(row)
    (root/'audio_transcription.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(row,ensure_ascii=False),flush=True)
