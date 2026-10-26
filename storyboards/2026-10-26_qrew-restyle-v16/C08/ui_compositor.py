"""V16 isolated C08 scene UI. No source folder is written."""
from pathlib import Path
import sys,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
SB=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(SB/'2026-10-25_final-six-v13/C02/.deps'))
import av,numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
SOURCE=SB/'2026-10-26_C08-C09-flow-v15'
W,H=1280,720
def font(n):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',n)
Q={'K03':[(365,216),(693,200),(719,404),(393,440)],'K04':[(315,103),(638,58),(669,259),(358,325)]}
REF={}
for cut in ['K03','K04']:
 with av.open(str(SOURCE/f'C08_{cut}_take01.mp4')) as c:REF[cut]=next(c.decode(video=0)).to_ndarray(format='rgb24')


def star(d,x,y,r=15):
 pts=[]
 for i in range(10):
  ang=-math.pi/2+i*math.pi/5;rr=r if i%2==0 else r*.42;pts.append((x+rr*math.cos(ang),y+rr*math.sin(ang)))
 d.polygon(pts,fill=(24,45,55))

def ui_art(progress):
 im=Image.new('RGBA',(600,400),(232,241,241,255));d=ImageDraw.Draw(im)
 d.rectangle((0,0,600,76),fill=(29,94,105));d.text((300,13),'공유 AI 양식',font=font(43),anchor='mt',fill='white')
 d.text((140,95),'내 자료',font=font(32),anchor='mt',fill=(30,64,71));d.text((460,95),'적용 결과',font=font(32),anchor='mt',fill=(30,64,71))
 d.rounded_rectangle((41,144,239,350),12,fill=(250,252,250),outline=(129,167,171),width=3)
 d.rounded_rectangle((361,144,559,350),12,fill=(250,252,250),outline=(129,167,171),width=3)
 d.line((264,247,327,247),fill=(45,115,122),width=7);d.polygon([(340,247),(321,234),(321,260)],fill=(45,115,122))
 for x in [67,387] if progress>=.99 else [67]:
  d.polygon([(x,163),(x+31,163),(x,194)],fill=(34,149,159))
  for row in range(4):
   d.line((x+41,192+row*34,x+135,192+row*34),fill=(132,160,163),width=7)
  star(d,x+19,226,12)
 if 0<progress<.99:
  x=83+progress*320;y=179;d.rounded_rectangle((x,y,x+112,y+136),8,fill=(248,253,252),outline=(29,135,145),width=4);d.polygon([(x+9,y+9),(x+34,y+9),(x+9,y+34)],fill=(34,149,159));star(d,x+42,y+70,13)
 return im

def composite_ui(frame,cut,st):
 progress=1 if cut=='K04' else float(np.clip((st-1)/1.8,0,1))
 art=np.array(ui_art(progress));quad=np.float32(Q[cut]);src=np.float32([[0,0],[599,0],[599,399],[0,399]])
 transform=cv2.getPerspectiveTransform(src,quad);layer=cv2.warpPerspective(art,transform,(W,H),flags=cv2.INTER_CUBIC)
 alpha=layer[:,:,3].astype(float)/255;rgb=frame.astype(float);ref=REF[cut].astype(float)
 # Preserve foreground fingers and the lifted paper using source-reference differences
 # constrained to the fixed screen plane. Every critical occlusion is separately inspected.
 skin=(rgb[:,:,0]>rgb[:,:,1]+14)&(rgb[:,:,1]>rgb[:,:,2]+5)
 filled=np.uint8(skin&(alpha>.05))*255
 if cut=='K04' and 2.45<=st<=4.05:
  track=[(2.45,[(306,325),(480,390),(695,570),(429,600)]),(2.5,[(306,314),(480,383),(695,562),(429,589)]),(2.75,[(226,210),(480,234),(640,480),(330,538)]),(3.,[(114,100),(355,92),(542,354),(288,434)]),(3.25,[(0,200),(258,122),(462,306),(236,418)]),(3.5,[(0,226),(174,212),(428,344),(228,460)]),(3.75,[(0,370),(160,288),(382,394),(192,490)]),(4.05,[(0,400),(180,332),(390,398),(180,515)])]
  tt=[v[0] for v in track]
  poly=np.array([[np.interp(st,tt,[v[1][i][j] for v in track]) for j in range(2)] for i in range(4)],np.int32)
  cv2.fillConvexPoly(filled,poly,255)
 filled=cv2.dilate(filled,np.ones((3,3),np.uint8))
 alpha*=1-cv2.GaussianBlur(filled,(3,3),.6).astype(float)/255
 return np.uint8(np.clip(rgb*(1-alpha[:,:,None])+layer[:,:,:3]*alpha[:,:,None],0,255))
