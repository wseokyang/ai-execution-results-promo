from pathlib import Path
import sys
sys.path[:0]=['C:/Users/wseok/.cache/codex-media-tools/opencv','C:/Users/wseok/.cache/codex-media-tools/faster-whisper']
import cv2,numpy as np,av
from PIL import Image
from render_c01 import *
pose=decode(SOURCE['POSE'])[0]
quad=QUADS['POSE'];M=cv2.getPerspectiveTransform(np.float32(quad),np.float32([[0,0],[999,0],[999,599],[0,599]]));clean=cv2.warpPerspective(pose,M,(1000,600))
Image.fromarray(clean).save(OUT/'clean_oldposter.png')
for key in ['K01','K02','K03','K05','K06']:
 fr=decode(SOURCE[key]);ix=60 if key=='K05' else 0;rgb=fr[ix]
 template,a=warp(clean,QUADS[key]);diff=np.max(np.abs(rgb.astype(float)-template.astype(float)),axis=2)
 z=np.uint8(np.clip(diff*4,0,255));Image.fromarray(z).save(OUT/f'diff_{key}.png')
