"""C01 compositing and final edit. Original Flow files remain byte-identical.
No generated dialogue is used. Poster/monitor are postproduction surfaces, not action replacements.
"""
from pathlib import Path
import sys,json,subprocess,hashlib,math,importlib.util,zipfile
sys.path[:0]=['C:/Users/wseok/.cache/codex-media-tools/opencv','C:/Users/wseok/.cache/codex-media-tools/faster-whisper']
import av,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent;V=OUT.parent;SB=V.parent
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
F=SB/'2026-10-24_v12-C02-C04-C01-flow';R=SB/'2026-10-24_C01-C06-repair110'
W,H,FPS,SR=1280,720,24,48000
FONT='C:/Windows/Fonts/malgun.ttf';BOLD='C:/Windows/Fonts/malgunbd.ttf'
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(p):
 with av.open(str(p)) as c:return [f.to_ndarray(format='rgb24') for f in c.decode(video=0)]
def at(fr,t):return fr[min(len(fr)-1,max(0,round(t*FPS))) ]
def polygon(points):
 m=np.zeros((H,W),np.uint8);cv2.fillPoly(m,[np.array(points,np.int32)],255);return m
QUADS={
 'K01': [[339,0],[874,10],[873,321],[339,320]],
 'K02': [[417,-1],[1122,-1],[1123,461],[416,460]],
 'K03': [[-90,-8],[475,15],[474,345],[-90,347]],
 'K05': [[340,0],[874,10],[873,321],[338,320]],
 'K06': [[340,0],[874,10],[873,320],[339,319]],
 'POSE': [[340,0],[874,10],[873,320],[339,319]],
}
MONITORS={
 'K03':[[800,80],[1195,27],[1197,300],[800,305]],
 'K05':[[1124,107],[1310,64],[1310,290],[1124,294]],
 'K06':[[1174,90],[1322,54],[1321,293],[1174,294]],
 'POSE':[[1174,90],[1322,54],[1321,293],[1174,294]],
}
# Geometrically restricted foreground windows. Exact source colors separate the real
# maroon/yellow actor, skin and dark hair from the pale blue printed image.
ROIS={
 'K01':[(260,82,382,242),(365,180,570,310),(667,205,803,350)],
 'K02':[(245,88,440,330),(413,260,830,460),(990,270,1220,500)],
 'K03':[(215,110,387,350)],
 'K05':[(610,110,775,340)],
 'K06':[(375,180,800,345)],
 'POSE':[(600,280,735,360),(320,275,410,355)],
}
def region_rects(rects):
 m=np.zeros((H,W),np.uint8)
 for x1,y1,x2,y2 in rects:m[max(0,y1):min(H,y2),max(0,x1):min(W,x2)]=1
 return m>0

def solid_component(binary, min_area=500, largest=False):
 n,lab,stats,_=cv2.connectedComponentsWithStats(binary.astype(np.uint8))
 out=np.zeros((H,W),np.uint8)
 ids=[i for i in range(1,n) if stats[i,cv2.CC_STAT_AREA]>=min_area]
 if largest and ids:ids=[max(ids,key=lambda i:stats[i,cv2.CC_STAT_AREA])]
 for i in ids:
  contour,_=cv2.findContours((lab==i).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  cv2.drawContours(out,contour,-1,255,cv2.FILLED)
 return out>0

def actor_mask(rgb,key,t):
 exact=OUT/'foreground_masks'/key/f'{round(t*FPS):04d}.png'
 if exact.exists():return np.array(Image.open(exact)).astype(float)/255
 hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV);r,g,b=np.moveaxis(rgb.astype(float),2,0)
 maroon=(hsv[:,:,0]>160)&(hsv[:,:,1]>100)&(hsv[:,:,2]<185)
 yellow=(hsv[:,:,0]>16)&(hsv[:,:,0]<40)&(hsv[:,:,1]>80)&(r>125)&(g>100)&(np.indices((H,W))[0]>230)
 m=solid_component(maroon,1000,True)
 if key in ['K01','K02','K05']:m|=solid_component(yellow,1000,True)
 head_centers={
 'K01':([0,1,2,3.75],[(329,146),(391,142),(421,154),(427,149)]),
 'K02':([0,1,2.25],[(355,178),(364,180),(369,183)]),
 'K03':([0,4],[(282,158),(282,158)]),
 'K05':([2.5,4.5,7.25],[(695,146),(697,151),(705,152)]),
 'K06':([1.5,2,2.5,2.75,3,3.5,4],[(609,200),(540,151),(503,130),(485,190),(492,340),(625,485),(696,520)]),
 }
 skin=(r>g*1.08)&(g>b*1.055)&(r>65)
 if key in head_centers:
  tt,pp=head_centers[key];cx=float(np.interp(t,tt,[q[0] for q in pp]));cy=float(np.interp(t,tt,[q[1] for q in pp]))
  # The actual red headband/black bun and face are separate components from the print.
  hair=region_rects([(round(cx-55),round(cy-61),round(cx+51),round(cy+21))])
  face=region_rects([(round(cx-48),round(cy-3),round(cx+38),round(cy+95))])
  if key=='K05':face=region_rects([(round(cx-47),round(cy),round(cx+13),round(cy+82))])
  m|=solid_component(((hsv[:,:,2]<100)|maroon)&hair,12)
  m|=solid_component(skin&face,12)
 hands={
 'K01':[(375,183,566,295),(687,241,778,340)],
 'K02':[(433,190,827,435),(996,327,1134,500)],
 'K03':[(231,263,382,334)],
 'K05':[(617,279,763,365)],
 'K06':[],
 'POSE':[(610,255,719,355)],
 }
 m|=solid_component(skin&region_rects(hands.get(key,[])),15)
 if key=='K01':m|=solid_component((hsv[:,:,2]<100)&region_rects([(694,217,791,325)]),12)
 if key=='K02':m|=solid_component((hsv[:,:,2]<100)&region_rects([(997,283,1202,500)]),12)
 if key=='K05':
  pts=np.array([(356,126),(377,119),(398,128),(410,151),(406,169),(431,184),(445,222),(451,288),(448,332),(418,332),(406,332),(330,332),(310,252),(312,208),(336,184),(356,168)],float)
  dx=np.interp(t,[2.5,3,3.5,4,4.5],[0,-23,-56,-78,-95]);dy=np.interp(t,[2.5,3,3.5,4],[0,4,9,13]);pts+=np.array([dx,dy]);m|=polygon(pts)>0
 if key=='POSE' and t>=2.3:
  shoe=(hsv[:,:,1]<55)&(hsv[:,:,2]>145)&region_rects([(270,220,433,340)])
  num,lab,stats,cents=cv2.connectedComponentsWithStats(shoe.astype(np.uint8))
  for j in range(1,num):
   x,y,w,h,area=stats[j]
   if 100<area<6500 and h>14 and y>240:m|=lab==j
 m=cv2.morphologyEx(m.astype(np.uint8)*255,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
 return cv2.GaussianBlur(m,(3,3),.5).astype(float)/255

class Plane:
 def __init__(self,first,quad,occlusion=None):
  self.quad=np.float32(quad);self.ref=cv2.cvtColor(first,cv2.COLOR_RGB2GRAY)
  mask=polygon(quad)
  if occlusion is not None:mask[occlusion>0]=0
  self.sift=cv2.SIFT_create(nfeatures=1800,contrastThreshold=.025)
  self.kp,self.des=self.sift.detectAndCompute(self.ref,mask)
  self.matcher=cv2.BFMatcher(cv2.NORM_L2);self.last=self.quad.copy();self.stats=[]
 def track(self,rgb):
  kp,d=self.sift.detectAndCompute(cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY),None)
  good=[]
  if self.des is not None and d is not None:
   good=[a for a,b in self.matcher.knnMatch(self.des,d,k=2) if a.distance<.69*b.distance]
  quad=self.last.copy();inliers=0
  if len(good)>=8:
   src=np.float32([self.kp[m.queryIdx].pt for m in good]);dst=np.float32([kp[m.trainIdx].pt for m in good])
   mat,sel=cv2.findHomography(src,dst,cv2.RANSAC,2.0);inliers=int(sel.sum()) if sel is not None else 0
   if mat is not None and inliers>=7:
    candidate=cv2.perspectiveTransform(self.quad[None],mat)[0]
    if np.max(np.abs(candidate-self.quad))<170 and cv2.contourArea(candidate)>cv2.contourArea(self.quad)*.65:
     quad=candidate;self.last=quad
  self.stats.append({'matches':len(good),'inliers':inliers,'quad':quad.round(2).tolist()});return quad

def warp(art,quad,fg=None):
 ah,aw=art.shape[:2];M=cv2.getPerspectiveTransform(np.float32([[0,0],[aw-1,0],[aw-1,ah-1],[0,ah-1]]),np.float32(quad))
 layer=cv2.warpPerspective(art,M,(W,H),flags=cv2.INTER_LINEAR)
 alpha=cv2.warpPerspective(np.ones((ah,aw),np.float32),M,(W,H),flags=cv2.INTER_LINEAR)
 if fg is not None:alpha*=1-fg
 return layer,alpha[:,:,None]
def overlay(rgb,art,quad,fg=None):
 layer,a=warp(art,quad,fg);return np.uint8(np.clip(rgb.astype(float)*(1-a)+layer.astype(float)*a,0,255))
def text_layer(text,pos='bottom',size=42):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im);font=ImageFont.truetype(BOLD,size)
 lines=text.split('\n');heights=[d.textbbox((0,0),l,font=font)[3] for l in lines];spacing=10
 height=sum(heights)+spacing*(len(lines)-1)+26
 y=H-height-30 if pos=='bottom' else 25
 d.rounded_rectangle((W*.13,y,W*.87,y+height),radius=12,fill=(9,16,25,210))
 yy=y+8
 for l,h in zip(lines,heights):
  width=d.textlength(l,font=font);d.text(((W-width)/2,yy),l,font=font,fill='white');yy+=h+spacing
 return im

SOURCE={
 'K01':F/'C01_K01_take02.mp4','K02':F/'C01_K02_take02.mp4','K03':F/'C01_K03_take01.mp4','K04':F/'C01_K04_take01.mp4',
 'K05':R/'C01_K05_take03.mp4','K06':F/'C01_K06_take01.mp4','POSE':V/'C01_K06_pose_bridge_take01.mp4',
}
TIMELINE=[('K01',0,3.75),('K02',0,2.25),('K03',1,3.5),('K04',.875,4.5),('K05',2.5,7.25),('K06',1.5,4),('POSE',.5,4)]
# --front contains only the known front portion, clearly not a final delivery.
# Final tail is supplied by tail_plan.json after successful new source review.
if (OUT/'tail_plan.json').exists() and '--front' not in sys.argv:
 tail=json.loads((OUT/'tail_plan.json').read_text(encoding='utf-8-sig'))
 for q in tail:
  SOURCE[q['cut']]=V/q['source'];TIMELINE.append((q['cut'],q['source_in'],q['source_out']))
  if q.get('poster_quad'):QUADS[q['cut']]=q['poster_quad']
  if q.get('monitor_quad'):MONITORS[q['cut']]=q['monitor_quad']
  ROIS[q['cut']]=q.get('foreground_rois',[])
CAPS=[(.25,3.65,'AI 잘 쓰는 사람은\n자세부터 다릅니다.','bottom'),(6.25,8.3,'그 사진의 원본','bottom'),(12.325,16.65,'자세 말고,\n어떻게 일했는지요.','bottom'),(19.65,22.75,'착지까지가 비법입니다.','top')]

def ending_card():
 im=Image.new('RGB',(W,H),(10,33,39));d=ImageDraw.Draw(im)
 d.line((90,138,1190,138),fill=(68,189,167),width=4)
 def line(text,y,size,color='white'):
  ft=ImageFont.truetype(BOLD,size);x=(W-d.textlength(text,font=ft))/2;d.text((x,y),text,font=ft,fill=color)
 line('자세 말고, 일하는 방법을 나눕니다.',190,41)
 line('Q-AI Fair',302,90,(109,231,200))
 line('품질팀 AI 성과 교류회',455,34,(230,239,237))
 d.line((90,578,1190,578),fill=(68,189,167),width=4)
 return im

def main():
 if not (OUT/'foreground_masks').exists() and (OUT/'foreground_masks.zip').exists():
  with zipfile.ZipFile(OUT/'foreground_masks.zip') as z:
   assert all(q.filename.startswith('foreground_masks/') and (OUT/q.filename).resolve().is_relative_to(OUT) for q in z.infolist())
   z.extractall(OUT)
 preview='--preview' in sys.argv
 hashes={str(p.relative_to(SB)):sha(p) for p in SOURCE.values()}
 base=decode(SOURCE['K04']);portrait=at(base,0)[35:310,425:865].copy();Image.fromarray(portrait).save(OUT/'exact_source_portrait.png')
 cursor=0;segments=[]
 for key,a,b in TIMELINE:segments.append({'cut':key,'source':str(SOURCE[key].relative_to(SB)),'source_in':a,'source_out':b,'start':cursor,'end':cursor+b-a});cursor+=b-a
 final=len(TIMELINE)>7
 if final:segments.append({'cut':'END','source':None,'source_in':0,'source_out':5,'start':cursor,'end':cursor+5});cursor+=5
 total=cursor;caplayers=[(a,b,text_layer(s,p)) for a,b,s,p in CAPS]
 picture=OUT/('C01_front_working.mp4' if len(TIMELINE)==7 else 'C01_picture.mp4')
 enc=None
 if not preview:
  enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 tracks={};n=0
 cachepath=OUT/'composite_tracking.json'
 oldtracks=json.loads(cachepath.read_text(encoding='utf-8')) if cachepath.exists() else {}
 def tracked(key,kind,plane,rgb,i,a,b):
  q=oldtracks.get(key,{}).get(kind,[])
  if len(q)==round((b-a)*FPS):
   entry=q[i-round(a*FPS)];plane.stats.append(entry);return np.float32(entry['quad'])
  return plane.track(rgb)
 for seg in segments:
  if seg['cut']=='END':
   end=ending_card();ids=[0,60,119] if preview else range(120)
   for i in ids:
    if i==0:end.save(OUT/'proof_END.jpg',quality=95)
    if enc:enc.stdin.write(end.tobytes())
    n+=1
   tracks['END']={'poster':[],'monitor':[]};continue
  key=seg['cut'];fr=base if key=='K04' else decode(SOURCE[key]);a=seg['source_in'];b=seg['source_out']
  pm=Plane(fr[0],QUADS[key],actor_mask(fr[0],key,0)) if key in QUADS else None
  mm=Plane(fr[0],MONITORS[key]) if key in MONITORS else None
  ids=range(round(a*FPS),round(b*FPS))
  if preview:ids=sorted(set([round(a*FPS),round((a+b)*.5*FPS),round(b*FPS)-1]))
  for i in ids:
   st=i/FPS;t=seg['start']+st-a;original=fr[i];rgb=original.copy()
   if pm:rgb=overlay(rgb,portrait,tracked(key,"poster",pm,original,i,a,b),actor_mask(original,key,st))
   if mm:
    if key=='K03':
     art=portrait if st<2.625 else at(base,st-2.625)
     # The real head crosses left edge of screen during the button press.
     hroi=np.zeros((H,W),bool);hroi[113:219,725:833]=True
     rr,gg,bb=np.moveaxis(original.astype(float),2,0)
     hmask=(((original.max(2)<95)|((rr>gg*1.1)&(gg>bb*1.05)&(np.indices((H,W))[0]>179)&(np.indices((H,W))[1]<810)))&hroi).astype(np.float32)
    else:art=at(base,0);hmask=None
    rgb=overlay(rgb,art,tracked(key,"monitor",mm,original,i,a,b),actor_mask(original,key,st))
   im=Image.fromarray(rgb).convert('RGBA')
   for ca,cb,layer in caplayers:
    if ca<=t<cb:im.alpha_composite(layer)
   if preview or i in [round(a*FPS),round(b*FPS)-1]:im.convert('RGB').save(OUT/f'proof_{key}_{st:.3f}.jpg',quality=95)
   if enc:enc.stdin.write(im.convert('RGB').tobytes())
   n+=1
  tracks[key]={'poster':pm.stats if pm else [],'monitor':mm.stats if mm else []}
  print(key,'complete',flush=True)
 if enc:
  enc.stdin.close();err=enc.stderr.read();enc.wait();assert enc.returncode==0,err.decode(errors='replace')
  assert n==round(total*FPS),(n,total)
 dump(OUT/('composite_tracking_preview.json' if preview else 'composite_tracking.json'),tracks)
 dump(OUT/'edit_manifest.json',{'title':'성공 자세 교정원','film':'C01','duration_seconds':total,'fps':FPS,'resolution':[W,H],'timeline':segments,'captions':[dict(start=a,end=b,text=s,position=p) for a,b,s,p in CAPS],'source_sha256':hashes,'source_audio':'muted','poster_reference':'K04 exact first frame crop_xywh [425,35,440,275]','status':'FRONT_WORKING_PENDING_NEW_TAIL' if len(TIMELINE)==7 else 'RENDER_PENDING_INDEPENDENT_REVIEW','limitations':['Sample review only, no continuous playback claim','Audio has not been listened to'],'action_stills_inserted':False,'ending_graphic_seconds':5 if final else 0,'ending_text':['자세 말고, 일하는 방법을 나눕니다.','Q-AI Fair','품질팀 AI 성과 교류회'] if final else []})
 assert hashes=={str(p.relative_to(SB)):sha(p) for p in SOURCE.values()}
 print('DONE',total,flush=True)
if __name__=='__main__':main()
