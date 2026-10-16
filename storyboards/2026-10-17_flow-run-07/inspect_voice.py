"""Inspect saved Flow originals. ASR is not an auditory quality judgment."""
from pathlib import Path
import sys, subprocess, json, hashlib
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import numpy as np
import av
from faster_whisper import WhisperModel

root = Path(__file__).resolve().parent
ff = root.parent/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
paths = [root/name for name in sys.argv[1:]]
if not paths:
    paths = sorted(root.glob('C01_K04_D_voice_take*.mp4'))
if not paths:
    raise RuntimeError('No completed originals saved; do not inspect browser temporary downloads.')
model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=8,
                     download_root='C:/Users/wseok/.cache/codex-media-tools/models')
for path in paths:
    with av.open(str(path)) as c:
        streams = [{'type': s.type, 'codec': s.codec_context.name,
                    'duration_seconds': float(s.duration*s.time_base) if s.duration is not None else None,
                    **({'width': s.width, 'height': s.height, 'frame_rate': str(s.average_rate)} if s.type == 'video' else {})}
                   for s in c.streams]
        duration = c.duration/1e6
    decoded = subprocess.run([str(ff), '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True, check=True)
    pcm = subprocess.run([str(ff), '-v', 'error', '-i', str(path), '-f', 'f32le', '-ar', '16000', '-ac', '1', '-'], capture_output=True, check=True)
    samples = np.frombuffer(pcm.stdout, dtype=np.float32)
    segments, info = model.transcribe(samples, language='ko', beam_size=5, vad_filter=True,
                                      word_timestamps=True, condition_on_previous_text=False)
    rows = [{'start': s.start, 'end': s.end, 'text': s.text,
             'words': [{'start': w.start, 'end': w.end, 'word': w.word, 'probability': w.probability}
                       for w in s.words or []]} for s in segments]
    subprocess.run([str(ff), '-y', '-v', 'error', '-i', str(path), '-vn', '-c:a', 'copy', str(path.with_suffix('.m4a'))], check=True)
    # Float WAV preserves AAC decoder overshoots without clipping to integer full scale.
    subprocess.run([str(ff), '-y', '-v', 'error', '-i', str(path), '-vn', '-c:a', 'pcm_f32le', '-ar', '48000', str(path.with_suffix('.wav'))], check=True)
    subprocess.run([str(ff), '-y', '-v', 'error', '-ss', '3', '-i', str(path), '-frames:v', '1', str(path.with_suffix('.png'))], check=True)
    result = {'file': path.name, 'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'duration_seconds': duration, 'streams': streams, 'decode_pass': True,
              'decoded_pcm_finite': bool(np.isfinite(samples).all()), 'decoded_pcm_peak': float(np.max(np.abs(samples))),
              'derived_wav_format': 'pcm_f32le, decoder overshoots preserved',
              'asr_model': 'faster-whisper small CPU int8', 'segments': rows,
              'limitation': 'Automatic transcription and technical inspection only. No actual listening, pronunciation, speaker identity, naturalness, or lip-sync verification.'}
    path.with_name(path.stem+'_inspection.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(result, ensure_ascii=False), flush=True)
