from pathlib import Path
P=Path(__file__).resolve().parent
scope={'__file__':str(P/'render_edit.py')}
code=(P/'render_edit.py').read_text(encoding='utf-8').split("picture = OUT/")[0]
exec(compile(code,'render_edit.py','exec'),scope)
Image=scope['Image']
out=P/'wide_overlay_preview'
out.mkdir(exist_ok=True)
for p in (P/'wide_tracking_frames').glob('*.png'):
 t=float(p.stem[:-1])
 im=Image.open(p).convert('RGBA')
 im.alpha_composite(scope['wide_records_graphic'](im,t))
 im.save(out/p.name)
sheet=Image.new('RGB',(1280,400*5),'#172026')
d=scope['ImageDraw'].Draw(sheet)
for i,p in enumerate(sorted(out.glob('*.png'))):
 x=(i%2)*640;y=(i//2)*400
 sheet.paste(Image.open(p).resize((640,360)),(x,y+30))
 d.text((x+10,y+6),p.stem,fill='white')
sheet.save(P/'wide_overlay_contact.jpg',quality=93)
