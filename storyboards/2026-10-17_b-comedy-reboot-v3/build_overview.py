from pathlib import Path
import json
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent


def main():
    data=json.loads((ROOT/'storyboards.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'scene_manifest.json').read_text(encoding='utf-8'))
    mapping={(x['concept_id'],x['cut_id']):x['image_path'] for x in manifest['images']}
    font='C:/Windows/Fonts/malgun.ttf'
    title=ImageFont.truetype(font,29)
    label=ImageFont.truetype(font,24)
    small=ImageFont.truetype(font,20)
    sheet=Image.new('RGB',(1680,930),'#f6f1e7');draw=ImageDraw.Draw(sheet)
    draw.text((24,18),'B급 코미디 신규 5안 · 컷별 첫 프레임',font=title,fill='#20201d')
    draw.text((24,62),'기존 완성 1번 영상 보존 / 신규 39컷 / 동영상 생성 없음',font=small,fill='#666456')
    for n,c in enumerate(data['concepts']):
        x=24+(n%3)*552;y=110+(n//3)*400
        path=ROOT/mapping[(c['id'],'K01')]
        with Image.open(path) as im: thumb=ImageOps.contain(im.convert('RGB'),(528,297))
        sheet.paste(thumb,(x+(528-thumb.width)//2,y+(297-thumb.height)//2))
        draw.text((x,y+307),f"{n+1:02d}  {c['title']}",font=label,fill='#20201d')
        draw.text((x,y+345),f"{c['duration_seconds']}초 · {len(c['shots'])}컷 · {c['purpose']}",font=small,fill='#666456')
    x,y=1128,550
    for i,t in enumerate(['각 그림은 첫 장면의 시작 상태입니다.','뒤에 일어날 동작과 대사는','HTML 열람본에서 함께 볼 수 있습니다.','','실제 PNG를 축소 배치한 미리보기이며','독립 원본은 images/에 있습니다.']):
        draw.text((x,y+i*39),t,font=small,fill='#666456')
    out=ROOT/'contact_sheets';out.mkdir(exist_ok=True)
    sheet.save(out/'five_concepts_overview.jpg',quality=94)
    print('contact_sheets/five_concepts_overview.jpg')


if __name__=='__main__':main()
