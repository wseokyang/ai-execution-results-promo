from pathlib import Path
import sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
p=Path(__file__).resolve().parent;want={round(t*24) for t in [13.25,13.5,17.25,17.5,18]}
with av.open(str(p/'C01_front_working.mp4')) as c:
 for i,f in enumerate(c.decode(video=0)):
  if i in want:f.to_image().save(p/f'repair_{i/24:.3f}.jpg')
