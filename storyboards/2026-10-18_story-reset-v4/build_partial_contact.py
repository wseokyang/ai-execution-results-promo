"""Review actual available selected PNGs; never create substitute first frames."""
from pathlib import Path
import json,sys,math
from PIL import Image,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
d=json.loads((R/'storyboards.json').read_text(encoding='utf-8-sig'))
ids=set(sys.argv[1:]);out=R/'contact_sheets';out.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',20)
for c in d['concepts']:
    if ids and c['id'] not in ids:continue
    assert all((R/s['image_file']).is_file() for s in c['shots']),c['id']
    sheet=Image.new('RGB',(1312,70+math.ceil(len(c['shots'])/2)*392),'#f3efe6');dr=ImageDraw.Draw(sheet)
    dr.text((16,20),f"{c['id']} · {c['title']} / 실제 첫 프레임",font=font,fill='#22231f')
    for i,s in enumerate(c['shots']):
        x,y=16+(i%2)*648,70+(i//2)*392
        with Image.open(R/s['image_file']) as im:thumb=ImageOps.contain(im.convert('RGB'),(632,355))
        sheet.paste(thumb,(x+(632-thumb.width)//2,y))
        dr.text((x,y+360),f"{s['id']} · {s['start']}–{s['end']}초 / {Path(s['image_file']).name}",font=font,fill='#22231f')
    sheet.save(out/f"{c['id']}_all_cuts.jpg",quality=95)
    print(c['id'],len(c['shots']))
