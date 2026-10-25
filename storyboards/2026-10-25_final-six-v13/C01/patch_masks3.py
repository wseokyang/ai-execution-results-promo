from pathlib import Path
p=Path('storyboards/2026-10-25_final-six-v13/C01/render_c01.py');s=p.read_text(encoding='utf-8');a=s.index('def actor_mask(');b=s.index('\nclass Plane:',a)
s=s[:a]+'''def solid_component(binary, min_area=500, largest=False):
 n,lab,stats,_=cv2.connectedComponentsWithStats(binary.astype(np.uint8))
 out=np.zeros((H,W),np.uint8)
 ids=[i for i in range(1,n) if stats[i,cv2.CC_STAT_AREA]>=min_area]
 if largest and ids:ids=[max(ids,key=lambda i:stats[i,cv2.CC_STAT_AREA])]
 for i in ids:
  contour,_=cv2.findContours((lab==i).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  cv2.drawContours(out,contour,-1,255,cv2.FILLED)
 return out>0

def actor_mask(rgb,key,t):
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
''' +s[b:];p.write_text(s,encoding='utf-8')
