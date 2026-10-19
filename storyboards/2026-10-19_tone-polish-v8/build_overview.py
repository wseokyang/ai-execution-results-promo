from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parent
def main():
 d=json.loads((R/'storyboards.json').read_text(encoding='utf-8'));cs=d['concepts']
 sheet=Image.new('RGB',(1600,930),'#f3efe6');dr=ImageDraw.Draw(sheet)
 font=lambda n:ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',n)
 dr.rectangle((0,0,1600,120),fill='#252522');dr.text((28,20),'1·3·5안 유지 / 2·4안 대사·연출 보완',font=font(36),fill='#fff3df');dr.text((30,75),'V8 · 컷별 첫 프레임 · 동영상 생성 없음',font=font(20),fill='#efb573')
 for i,c in enumerate(cs):
  x=28+(i%3)*524;y=146+(i//3)*380
  s=next(s for s in c['shots'] if s['id']==d['hero_cuts'][c['id']])
  with Image.open(R/s['image_file']) as im:thumb=ImageOps.contain(im.convert('RGB'),(496,279))
  sheet.paste(thumb,(x,y));dr.text((x,y+286),f"{c['id'][-1]}  {c['title']}",font=font(25),fill='#252522')
  label='콘티·이미지 그대로 유지' if c['id'] in ['C01','C03','C05'] else '대사·연출 보완'
  dr.text((x,y+326),f"{label}  ·  {c['duration_seconds']}초",font=font(18),fill='#9c4a2a')
 dr.text((1080,635),'AI 실행 결과 발표 대회',font=font(24),fill='#252522');dr.text((1080,680),'전체 컷과 대사는 index.html',font=font(20),fill='#665f55');dr.text((1080,718),'첫 프레임의 다음 동작은',font=font(18),fill='#665f55');dr.text((1080,748),'각 컷의 펼침 정보에서 확인',font=font(18),fill='#665f55')
 sheet.save(R/'overview.png')
 print('overview.png')
if __name__=='__main__':main()
