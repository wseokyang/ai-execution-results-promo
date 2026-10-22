"""Code-rendered diagrams and typography for postproduction planning, not generated footage."""
from pathlib import Path
import sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image,ImageDraw,ImageFont,ImageFilter
R=Path(__file__).resolve().parent;O=R/'post_assets';O.mkdir(exist_ok=True)
def font(n):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',n)
graphic=Image.new('RGB',(1200,480),'#101822');g=ImageDraw.Draw(graphic)
labels=['입력','확인·수정','적용'];colors=['#d9e2ea','#ffd27d','#b7e8c5']
for i in range(3):
 x=25+i*400
 g.text((x+175,55),labels[i],font=font(46),fill='white',anchor='mm')
 g.rounded_rectangle((x+50,112,x+300,420),radius=13,fill=colors[i])
 for row in range(4):g.rounded_rectangle((x+80,152+row*56,x+267,169+row*56),radius=4,fill='#526170')
 if i==1:
  g.line((x+69,195,x+280,234),fill='#b44242',width=13);g.line((x+69,234,x+280,195),fill='#b44242',width=13)
 if i==2:g.line((x+85,371,x+119,396,x+192,326),fill='#217248',width=18)
 if i<2:g.polygon([(x+337,245),(x+370,245),(x+370,230),(x+393,255),(x+370,280),(x+370,265),(x+337,265)],fill='#c4d3dc')
graphic.save(O/'C08_process.png')
# One reusable exact SVG, not a claim of a real AI outcome.
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480"><rect width="1200" height="480" fill="#101822"/>']
for i in range(3):
 x=25+i*400
 parts.append(f'<text x="{x+175}" y="70" text-anchor="middle" font-family="Malgun Gothic,sans-serif" font-size="46" font-weight="700" fill="white">{labels[i]}</text><rect x="{x+50}" y="112" width="250" height="308" rx="13" fill="{colors[i]}"/>')
 for row in range(4):parts.append(f'<rect x="{x+80}" y="{152+row*56}" width="187" height="17" rx="4" fill="#526170"/>')
 if i==1:parts.append(f'<path d="M{x+69} 195 L{x+280} 234 M{x+69} 234 L{x+280} 195" stroke="#b44242" stroke-width="13"/>')
 if i==2:parts.append(f'<path d="M{x+85} 371 L{x+119} 396 L{x+192} 326" stroke="#217248" stroke-width="18" fill="none"/>')
 if i<2:parts.append(f'<path d="M{x+337} 255 H{x+382} M{x+369} 237 L{x+389} 255 L{x+369} 273" fill="none" stroke="#c4d3dc" stroke-width="12"/>')
(O/'C08_process.svg').write_text(''.join(parts)+'</svg>',encoding='utf8')
canvas=Image.new('RGB',(1600,1000),'#f3f1e9');dr=ImageDraw.Draw(canvas)
dr.text((60,38),'C08  망토의 용도가 바뀌는 순간',font=font(40),fill='#17352c')
dr.text((60,100),'후편집 설계도 · 실제 생성 영상이나 완성 합성의 증빙이 아닙니다.',font=font(25),fill='#53625d')
for row in range(2):
 y=195+row*370
 dr.text((60,y), '전: 같은 도해 위 반사가 남음' if row==0 else '후: 천 뒤 광선과 반사만 함께 감소',font=font(31),fill='#17352c')
 dr.ellipse((95,y+85,175,y+165),fill='#ffd15f',outline='#c09730',width=4)
 dr.text((130,y+185),'고정 조명',font=font(22),fill='#30443d',anchor='mm')
 cape=(560,y+205,605,y+310) if row==0 else (560,y+65,605,y+310)
 dr.rectangle(cape,fill='#17232b');dr.text((580,y+335),'검정 안감',font=font(23),fill='#30443d',anchor='mm')
 dr.line((175,y+130,560 if row else 945,y+150 if row else y+194),fill='#c9a23a',width=10)
 thumb=graphic.resize((510,204));canvas.paste(thumb,(960,y+73))
 if row==0:
  overlay=Image.new('RGBA',(510,204));od=ImageDraw.Draw(overlay);od.ellipse((-90,-65,410,200),fill=(255,255,255,205));overlay=overlay.filter(ImageFilter.GaussianBlur(24));canvas.paste(overlay,(960,y+73),overlay)
 else:
  dr.line((610,y+155,935,y+194),fill='#c7c9c3',width=3)
  dr.text((785,y+218),'차단된 빛길',font=font(21),fill='#6e7973',anchor='mm')
 dr.text((1215,y+310),'도해 파일·위치·크기 동일',font=font(24),fill='#30443d',anchor='mm')
dr.text((60,945),'천 진입 → 차단과 반사 감소를 동기화 → 선명한 상태 1초 유지',font=font(27),fill='#17352c')
canvas.save(O/'C08_light_path_plan.png')
print('Built reusable process graphic and light-path plan; source PNGs untouched.')
