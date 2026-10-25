from pathlib import Path
p=Path('storyboards/2026-10-25_final-six-v13/C01/render_c01.py')
s=p.read_text(encoding='utf-8-sig')
a=s.index('def actor_mask(');b=s.index('\nclass Plane:',a)
s=s[:a]+'''def region_rects(rects):
 m=np.zeros((H,W),np.uint8)
 for x1,y1,x2,y2 in rects:m[max(0,y1):min(H,y2),max(0,x1):min(W,x2)]=1
 return m>0

def actor_mask(rgb,key,t):
 hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV);r,g,b=np.moveaxis(rgb.astype(float),2,0)
 maroon=(r>g*1.5)&(r>b*1.3)&(r<165)&(g<100)
 yellow=(r>b*1.5)&(g>b*1.35)&(r>125)&(g>100)
 # Clothing colors never occur on the blue shirt/background poster.
 m=maroon|yellow
 skin=(r>g*1.10)&(g>b*1.07)&(r>65)
 dark=hsv[:,:,2]<100
 skin_boxes={
 'K01':[(282,100,370,231),(380,190,560,282),(688,243,777,330)],
 'K02':[(278,155,425,325),(434,271,818,433),(994,330,1127,470)],
 'K03':[(246,150,326,238),(232,266,380,331)],
 'K05':[(647,153,733,214),(617,279,763,365)],
 'K06':[(395,196,581,300),(640,250,764,344)],
 'POSE':[(610,255,719,355)],
 }
 hair_boxes={
 'K01':[(276,95,367,188),(694,217,790,323)],
 'K02':[(251,100,426,232),(997,283,1202,475)],
 'K03':[(231,117,318,199)],
 'K05':[(656,117,737,176)],
 'K06':[(650,216,776,308)],
 'POSE':[],
 }
 m|=skin&region_rects(skin_boxes.get(key,[]))
 m|=dark&region_rects(hair_boxes.get(key,[]))
 # Limit matching head patches to actor-side of the source portrait face.
 if key=='K05':
  # Face/head contour around real coach, not giant printed face behind her.
  actor=polygon([(662,121),(701,117),(723,127),(737,148),(731,171),(717,182),(714,202),(700,214),(676,203),(658,180),(651,158)])>0
  roi=region_rects([(647,110,741,220)])
  m[roi]=m[roi]&actor[roi]
  # Actual departing blue shirt. Keys follow his head and left shoulder before he
  # clears the poster edge, clipped beyond it by the replacement plane itself.
  pts=np.array([(356,126),(377,119),(398,128),(410,151),(406,169),(431,184),(445,222),(451,288),(439,308),(418,300),(406,288),(330,293),(310,252),(312,208),(336,184),(356,168)],float)
  # Camera/actor leftward movement, visible in source 2.5–3.5.
  dx=np.interp(t,[2.5,3,3.5,4,4.5],[0,-23,-56,-78,-95]);dy=np.interp(t,[2.5,3,3.5,4],[0,4,9,13])
  pts+=np.array([dx,dy]);m|=polygon(pts)>0
 if key=='POSE':
  # Raised shoe is white against gray. Read its contour only after the knee lift.
  if t>=2.3:
   # Foot moves from lower left up to poster lower-left. Dynamic threshold keeps
   # the actual shoe, and no broad rectangular piece of the old poster.
   shoe=(hsv[:,:,1]<55)&(hsv[:,:,2]>145)&region_rects([(270,220,433,340)])
   # Old poster's lower-left background can be gray; keep components touching
   # the real red leg at its nearest bright top boundary.
   num,lab,stats,cents=cv2.connectedComponentsWithStats(shoe.astype(np.uint8))
   for j in range(1,num):
    x,y,w,h,area=stats[j]
    if 100<area<6500 and h>14 and y>240:m|=lab==j
 m=cv2.morphologyEx(m.astype(np.uint8)*255,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
 return cv2.GaussianBlur(m,(3,3),.5).astype(float)/255
''' +s[b:]
s=s.replace("hroi[100:227,720:837]=True","hroi[113:219,725:833]=True")
s=s.replace("((rr>gg*1.1)&(gg>bb*1.05))","((rr>gg*1.1)&(gg>bb*1.05)&(np.indices((H,W))[0]>179))")
p.write_text(s,encoding='utf-8')
