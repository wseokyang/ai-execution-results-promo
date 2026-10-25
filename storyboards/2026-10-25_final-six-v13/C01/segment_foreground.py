"""Local foreground segmentation only; no source/action/image synthesis.
Model: official MobileSAM vit_t, CUDA. Cache is outside repository.
"""
from pathlib import Path
import sys, warnings, json, time
warnings.filterwarnings('ignore')
sys.path[:0]=['C:/Users/wseok/.cache/codex-media-tools/opencv','C:/Users/wseok/.cache/codex-media-tools/mobilesam/MobileSAM-master','C:/Users/wseok/.cache/codex-media-tools/faster-whisper']
import torch,cv2,numpy as np,av
from PIL import Image
from mobile_sam import sam_model_registry,SamPredictor
from render_c01 import OUT,SOURCE,TIMELINE,FPS,W,H,QUADS,MONITORS
m=sam_model_registry['vit_t'](checkpoint='C:/Users/wseok/.cache/codex-media-tools/mobilesam/MobileSAM-master/weights/mobile_sam.pt').to(device='cuda').eval();pred=SamPredictor(m)
MASK=OUT/'foreground_masks';MASK.mkdir(exist_ok=True)
def interpolate(t,tt,pp):return [float(np.interp(t,tt,[p[j] for p in pp])) for j in range(len(pp[0]))]
def specs(key,t):
 if key=='K01':
  head=interpolate(t,[0,1,2,3.75],[(330,170),(393,169),(424,184),(430,179)])
  return [([130,80,572,655],[[340,390],head],[[750,130],[550,160],[450,70]]),([365,185,800,650],[[610,417],[738,275]],[[790,150],[600,200],[500,150]])]
 if key=='K02':
  head=interpolate(t,[0,2.25],[(372,244),(396,261)])
  return [([0,80,835,720],[[300,420],[510,390],head],[[760,240],[1000,180],[570,130]]),([365,185,1226,720],[[1000,550],[1080,390]],[[850,230],[1000,150],[740,270]])]
 if key=='K03':return [([190,100,405,680],[[290,420],[290,200]],[[370,115],[180,235]]),([510,35,870,690],[[670,300],[630,520]],[[1060,150],[920,230]])]
 if key=='K05':
  red=interpolate(t,[2.5,7.25],[(695,320),(707,320)])
  result=[([600,100,800,595],[red],[[810,120],[500,210]])]
  if t<4.75:
   x=float(np.interp(t,[2.5,3,3.5,4,4.5],[382,378,365,320,295]));result.append(([x-85,105,x+88,585],[[x,235],[x,155]],[[500,180],[510,280]]))
  return result
 if key=='K06':
  point=interpolate(t,[1.5,2,2.5,3,3.5,4],[(610,350),(530,330),(514,270),(505,350),(555,540),(490,580)])
  return [([120,65,815,705],[point],[[795,110],[420,65],[900,300]])]
 if key=='MIRROR':return [([90,220,790,700],[[520,590],[681,542],[440,450],[682,302],[391,292]],[[780,120],[600,170],[850,300]]),([270,240,900,550],[[710,491],[837,482]],[[600,170],[900,300]])]
 if key=='POSE':return [([95,215,815,705],[[525,589],[687,541]],[[780,130],[600,175],[850,300]])]
 return []
def extra_parts(key,t):
 if key=='MIRROR':return [([349,230,435,345],[[391,287]],[]),([650,260,711,350],[[679,305]],[]),([470,240,570,345],[[520,289]],[])] if t>=2.6 else [([349,230,435,345],[[391,287]],[]),([650,260,711,350],[[679,305]],[])]
 if key=='K01':
  head=interpolate(t,[0,1,2,3.75],[(330,146),(391,142),(421,154),(427,149)])
  return [([684,210,800,350],[[738,275],[755,246]],[]),([375,180,575,307],[[490,240],[455,220]],[]),([head[0]-60,head[1]-65,head[0]+50,head[1]+100],[[head[0],head[1]+35],[head[0],head[1]-16]],[])]
 if key=='K02':
  hand=interpolate(t,[0,.5,1,1.5,2.25],[(497,337),(517,321),(530,293),(548,273),(555,272)])
  return [([994,279,1208,526],[[1080,389],[1135,358],[1094,318]],[]),([425,185,681,405],[hand],[])]
 if key=='K03':return [([231,114,339,253],[[288,188],[274,146]],[])]
 if key=='K05':return [([643,110,755,237],[[682,174],[707,143]],[])]
 if key=='K06':
  hc=interpolate(t,[1.5,2,2.5,2.75,3,3.25,3.5,3.75,4],[(609,200),(514,194),(503,130),(499,130),(498,212),(518,290),(569,396),(655,501),(696,520)])
  return [([hc[0]-64,hc[1]-68,hc[0]+58,hc[1]+100],[[hc[0]-12,hc[1]+33],[hc[0]+8,hc[1]-25]],[[hc[0]-35,hc[1]-55]]),([hc[0]-105,hc[1]+40,hc[0]+115,min(715,hc[1]+280)],[[hc[0]+8,min(700,hc[1]+95)]],[])]
 return []

def keep_components(mask,points):
 n,lab,stats,_=cv2.connectedComponentsWithStats(mask.astype(np.uint8))
 ids=set()
 for x,y in points:
  idx=int(lab[min(H-1,max(0,round(y))),min(W-1,max(0,round(x)))]);
  if idx:ids.add(idx)
 if not ids and n>1:ids={int(1+np.argmax(stats[1:,cv2.CC_STAT_AREA]))}
 out=np.isin(lab,list(ids)).astype(np.uint8)*255
 # Preserve real gaps between bent arms and finger webs.
 out=cv2.morphologyEx(out,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
 # No skin/blue-print island can survive merely because its color is similar.
 return out
preview='--preview' in sys.argv
records=[]
for key,a,b in TIMELINE:
 if key not in QUADS and key not in MONITORS:continue
 if '--tail' in sys.argv and key!='MIRROR':continue
 if '--repair' in sys.argv and key not in ['K05','K06']:continue
 target=MASK/key;target.mkdir(exist_ok=True)
 ids=set(range(round(a*FPS),round(b*FPS)))
 if preview:ids=set([round(a*FPS),round((a+b)*.5*FPS),round(b*FPS)-1])
 t0=time.time()
 with av.open(str(SOURCE[key])) as c:
  for i,f in enumerate(c.decode(video=0)):
   if i not in ids:continue
   dest=target/f'{i:04d}.png'
   if dest.exists() and not '--force' in sys.argv:continue
   rgb=f.to_ndarray(format='rgb24');pred.set_image(rgb);out=np.zeros((H,W),np.uint8);scores=[]
   for box,pos,neg in specs(key,i/FPS)+extra_parts(key,i/FPS):
    coords=np.array(pos+neg);labels=np.array([1]*len(pos)+[0]*len(neg))
    with torch.inference_mode():masks,score,logit=pred.predict(point_coords=coords,point_labels=labels,box=np.array(box),multimask_output=False)
    part=keep_components(masks[0],pos);out=cv2.bitwise_or(out,part);scores.append(float(score[0]))
   out=cv2.dilate(out,np.ones((3,3),np.uint8),iterations=1);out=cv2.GaussianBlur(out,(3,3),.55)
   Image.fromarray(out).save(dest)
   records.append({'cut':key,'frame':i,'scores':scores})
   if preview:
    show=rgb.copy();show[out<128]=(show[out<128]*.25).astype(np.uint8);Image.fromarray(show).save(OUT/f'sam_{key}_{i/FPS:.3f}.jpg')
 print(key,'masks',len(ids),'seconds',round(time.time()-t0,2),flush=True)
(OUT/'segmentation_validation.json').write_text(json.dumps({'method':'MobileSAM local CUDA prompted real foreground only; connected components restricted to actor seeds; 1px dilation,0.55px feather','model':'official vit_t mobile_sam.pt','action_generated':False,'preview_only':preview,'records':records},indent=2),encoding='utf-8')

