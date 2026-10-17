from pathlib import Path
import json
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
def main():
    data=json.loads((ROOT/'storyboards.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'scene_manifest.json').read_text(encoding='utf-8'))
    paths={(i['concept_id'],i['cut_id']):i['image_path'] for i in manifest['images']}
    target=ROOT/'contact_sheets'
    target.mkdir(exist_ok=True)
    font_path='C:/Windows/Fonts/malgun.ttf'
    font=ImageFont.truetype(font_path,20)
    heading=ImageFont.truetype(font_path,30)
    for index,c in enumerate(data['concepts'],1):
        if sys.argv[1:] and c['id'] not in sys.argv[1:]:
            continue
        if any((c['id'],s['id']) not in paths or not (ROOT/paths[(c['id'],s['id'])]).exists() for s in c['shots']):
            print(f"{c['id']}: not complete yet; no placeholder sheet created")
            continue
        cell_w,cell_h,gap=640,405,16
        rows=(len(c['shots'])+1)//2
        sheet=Image.new('RGB',(cell_w*2+gap*3,90+rows*(cell_h+gap)), '#f6f1e7')
        draw=ImageDraw.Draw(sheet)
        draw.text((gap,20),f"신규 {index}안 · {c['title']} / {c['duration_seconds']}초",font=heading,fill='#20201d')
        for n,s in enumerate(c['shots']):
            x=gap+(n%2)*(cell_w+gap); y=90+(n//2)*(cell_h+gap)
            path=ROOT/paths[(c['id'],s['id'])]
            with Image.open(path) as im:
                thumb=ImageOps.contain(im.convert('RGB'),(cell_w,360))
            sheet.paste(thumb,(x+(cell_w-thumb.width)//2,y+(360-thumb.height)//2))
            draw.text((x,y+367),f"{s['scene_id']} · {s['id']}  {s['start']:g}–{s['end']:g}초 | 첫 프레임",font=font,fill='#20201d')
        sheet.save(target/f"{c['id']}_all_cuts.jpg",quality=93)
        print(f"{c['id']}: {len(c['shots'])} actual first-frame thumbnails")

if __name__=='__main__': main()
