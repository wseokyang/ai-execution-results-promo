"""Automatic completeness check, not listening or a naturalness judgment."""
from pathlib import Path
import sys, subprocess, json
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import numpy as np
from faster_whisper import WhisperModel

root = Path(__file__).resolve().parent
ff = root.parent/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
voice = root/'C01_K04_D_natural_take01.wav'
p = subprocess.run([str(ff), '-v', 'error', '-i', str(voice), '-f', 'f32le', '-ar', '16000', '-ac', '1', '-'], capture_output=True, check=True)
samples = np.frombuffer(p.stdout, dtype=np.float32)
model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=8,
                     download_root='C:/Users/wseok/.cache/codex-media-tools/models')
segments, info = model.transcribe(samples, language='ko', beam_size=5, vad_filter=True, word_timestamps=True, condition_on_previous_text=False)
rows = [{'start': s.start, 'end': s.end, 'text': s.text,
         'words': [{'start': w.start, 'end': w.end, 'word': w.word, 'probability': w.probability} for w in s.words or []]} for s in segments]
record = {'file': voice.name, 'method': 'local faster-whisper small CPU int8', 'segments': rows,
          'limitation': 'Automatic transcription only. Does not verify naturalness, acting, voice continuity, or exact pronunciation.'}
(root/'voice_asr.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(record, ensure_ascii=False), flush=True)
