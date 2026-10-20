"""Inspect already-downloaded originals; never alter the source video."""
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
for name in sys.argv[1:]:
    source = root / name
    out = root / 'frames' / source.stem
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    frame_count = 0
    with av.open(str(source)) as container:
        duration = container.duration / 1e6
        streams = [{'type': s.type, 'codec': s.codec_context.name,
                    **({'width': s.width, 'height': s.height,
                        'frame_rate': str(s.average_rate)} if s.type == 'video' else {})}
                   for s in container.streams]
        for frame in container.decode(video=0):
            frame_count += 1
            seconds = float(frame.pts * frame.time_base)
            if len(rows) < 32 and seconds >= len(rows) * 0.25:
                filename = f'{len(rows):02}_{seconds:.3f}s.png'
                frame.to_image().save(out / filename)
                rows.append({'file': filename, 'seconds': seconds})
    sheet = Image.new('RGB', (1600, 1600), '#181818')
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(rows):
        x, y = (i % 4) * 400, (i // 4) * 200
        with Image.open(out / row['file']) as image:
            sheet.paste(image.resize((320, 180)), (x, y))
        draw.text((x + 6, y + 182), f"{row['seconds']:.3f}s", fill='white')
    sheet.save(root / f'{source.stem}_contact.jpg', quality=94)
    (out / 'manifest.json').write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    result = {'file': name, 'bytes': source.stat().st_size,
              'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'duration_seconds': duration, 'streams': streams,
              'decoded_video_frames': frame_count, 'full_video_decode_pass': True,
              'audio_track_present': any(s['type'] == 'audio' for s in streams),
              'file_kind': 'edited_review_derivative' if '_state_edit_' in name else 'downloaded_original',
              'inspection_reencodes_file': False,
              'limitation': 'Technical decoding and extracted frames; not actual listening or continuous visual playback.'}
    (root / f'{source.stem}_inspection.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result), flush=True)
