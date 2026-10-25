from pathlib import Path
p=Path('storyboards/2026-10-25_final-six-v13/C01/render_c01.py');s=p.read_text(encoding='utf-8')
s=s.replace('maroon=(r>g*1.5)&(r>b*1.3)&(r<165)&(g<100)','maroon=(hsv[:,:,0]>160)&(hsv[:,:,1]>75)&(hsv[:,:,2]<185)')
s=s.replace('yellow=(r>b*1.5)&(g>b*1.35)&(r>125)&(g>100)','yellow=(hsv[:,:,0]>16)&(hsv[:,:,0]<40)&(hsv[:,:,1]>80)&(r>125)&(g>100)&(np.indices((H,W))[0]>230)')
s=s.replace('(714,202),(700,214),(676,203)','(714,202),(732,230),(668,230),(676,203)')
s=s.replace('(439,308),(418,300),(406,288),(330,293)','(448,332),(418,332),(406,332),(330,332)')
s=s.replace("np.ones((3,3),np.uint8))\n return cv2.GaussianBlur(m,(3,3),.5)","np.ones((5,5),np.uint8))\n return cv2.GaussianBlur(m,(3,3),.5)")
s=s.replace("(np.indices((H,W))[0]>179)","(np.indices((H,W))[0]>179)&(np.indices((H,W))[1]<810)")
p.write_text(s,encoding='utf-8')
