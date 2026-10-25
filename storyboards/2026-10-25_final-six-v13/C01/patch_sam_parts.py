from pathlib import Path
p=Path('storyboards/2026-10-25_final-six-v13/C01/segment_foreground.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace('def keep_components(mask,points):','''def extra_parts(key,t):
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
  return [([hc[0]-64,hc[1]-68,hc[0]+58,hc[1]+100],[[hc[0]-12,hc[1]+33],[hc[0]+8,hc[1]-25]],[])]
 return []

def keep_components(mask,points):''')
s=s.replace("out=np.isin(lab,list(ids)).astype(np.uint8)*255\n # No skin", "out=np.isin(lab,list(ids)).astype(np.uint8)*255\n contours,_=cv2.findContours(out,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)\n cv2.drawContours(out,contours,-1,255,cv2.FILLED)\n # No skin")
s=s.replace('for box,pos,neg in specs(key,i/FPS):','for box,pos,neg in specs(key,i/FPS)+extra_parts(key,i/FPS):')
p.write_text(s,encoding='utf-8')
