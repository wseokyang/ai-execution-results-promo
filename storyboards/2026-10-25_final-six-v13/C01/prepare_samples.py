from pathlib import Path
import sys
sys.path[:0]=['C:/Users/wseok/.cache/codex-media-tools/opencv','C:/Users/wseok/.cache/codex-media-tools/faster-whisper']
import av,cv2,numpy as np
from PIL import Image
ROOT=Path.cwd();OUT=ROOT/'storyboards/2026-10-25_final-six-v13/C01';OUT.mkdir(exist_ok=True)
for name in ['C01_K01_take02','C01_K02_take02','C01_K03_take01','C01_K06_take01']:
 p=ROOT/'storyboards/2026-10-24_v12-C02-C04-C01-flow'/f'{name}.mp4'
 with av.open(str(p)) as c:
  for f in c.decode(video=0):
   if abs(float(f.time)*2-round(float(f.time)*2))<1e-5 and float(f.time)<=4:
    im=f.to_image();im.thumbnail((640,360));im.save(OUT/f'{name}_{float(f.time):.1f}.jpg')
print('ready')
