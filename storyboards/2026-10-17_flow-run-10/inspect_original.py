"""Preserve the completed download and extract review frames; never reencode the original."""
from pathlib import Path
import hashlib, json, shutil, sys
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
import numpy as np
from PIL import Image, ImageDraw

R = Path(__file__).resolve().parent
source = Path('C:/Users/wseok/Downloads/C05-F06_take02_·_Lite_·_질문에_20261017124130.mp4')
original = R / 'C05-F06_take02.mp4'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
assert source.is_file() and source.suffix == '.mp4'
if original.exists():
    assert sha(original) == sha(source), 'Do not overwrite a different original'
else:
    shutil.copy2(source, original)
assert sha(original) == sha(source)

out = R / 'review_frames'
out.mkdir(exist_ok=True)
container = av.open(str(original))
stream = container.streams.video[0]
metadata = {
    'original_file': original.name, 'source_download': str(source),
    'bytes': original.stat().st_size, 'sha256': sha(original),
    'download_and_preserved_hash_equal': True, 'reencoded': False,
    'container_seconds': container.duration / av.time_base,
    'video_seconds': float(stream.duration * stream.time_base),
    'width': stream.width, 'height': stream.height,
    'fps': float(stream.average_rate), 'video_codec': stream.codec_context.name,
    'audio_track': bool(container.streams.audio),
    'audio_streams': [{'codec': s.codec_context.name, 'sample_rate': s.rate,
                       'channels': s.codec_context.channels} for s in container.streams.audio],
    'actual_listening_by_assistant': False,
}
targets = [x / 2 for x in range(16)] + [7.958]
sampled = []
count = 0
idx = 0
for frame in container.decode(video=0):
    count += 1
    t = float(frame.pts * frame.time_base)
    if idx < len(targets) and t + .001 >= targets[idx]:
        path = out / f'frame_{idx:02d}_{t:.3f}s.jpg'
        frame.to_image().save(path, quality=94)
        sampled.append({'file': path.name, 'seconds': t})
        idx += 1
container.close()
metadata['decoded_video_frames'] = count
metadata['video_decode_pass'] = True
metadata['sampled_frames'] = sampled
if metadata['audio_track']:
    ac = av.open(str(original))
    peak, total, energy = 0., 0, 0.
    for frame in ac.decode(audio=0):
        arr = frame.to_ndarray().astype(np.float64)
        peak = max(peak, float(np.max(np.abs(arr))))
        energy += float(np.sum(arr * arr))
        total += arr.size
    ac.close()
    metadata.update(audio_decode_pass=True, decoded_audio_peak=peak,
                    decoded_audio_rms=float((energy / max(total, 1)) ** .5))
for start in range(0, len(sampled), 9):
    chunk = sampled[start:start + 9]
    sheet = Image.new('RGB', (1280, 3 * 264), '#181818')
    draw = ImageDraw.Draw(sheet)
    for j, item in enumerate(chunk):
        im = Image.open(out / item['file']).resize((420, 236))
        x, y = (j % 3) * 428, (j // 3) * 264
        sheet.paste(im, (x, y + 24))
        draw.text((x + 6, y + 5), f"{item['seconds']:.3f}s", fill='white')
    sheet.save(out / f'sheet_{start // 9 + 1:02d}.jpg', quality=94)
(R / 'media_inspection.json').write_bytes((json.dumps(metadata, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
preview = Path('C:/Users/wseok/.codex/visualizations/2026/10/16/01a13daf-3732-7b90-99a8-92c605090d35')
shutil.copy2(original, preview / original.name)
print(json.dumps(metadata, ensure_ascii=False, indent=2))
