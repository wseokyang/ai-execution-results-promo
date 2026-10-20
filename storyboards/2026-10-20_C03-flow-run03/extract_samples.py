"""Extract review samples from originals, without altering/re-encoding originals."""
from pathlib import Path
import sys, json
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
for name in sys.argv[1:]:
    source = root / name
    out = root / 'frames' / source.stem
    out.mkdir(parents=True, exist_ok=True)
    targets = [i * 0.5 for i in range(16)]
    rows = []
    with av.open(str(source)) as container:
        for frame in container.decode(video=0):
            time = float(frame.pts * frame.time_base)
            if len(rows) < len(targets) and time >= targets[len(rows)]:
                filename = f'{len(rows):02d}_{time:.3f}s.png'
                frame.to_image().save(out / filename)
                rows.append({'file': filename, 'actual_seconds': time})
    sheet = Image.new('RGB', (1280, 800), '#181818')
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(rows):
        x, y = (i % 4) * 320, (i // 4) * 200
        with Image.open(out / row['file']) as image:
            sheet.paste(image.resize((320, 180)), (x, y))
        draw.text((x + 6, y + 183), f"{row['actual_seconds']:.3f}s", fill='white')
    sheet.save(root / (source.stem + '_contact.jpg'), quality=92)
    (out / 'manifest.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    print(f'{source.name}: {len(rows)} sampled frames; audio not heard', flush=True)
