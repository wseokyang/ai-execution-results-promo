from pathlib import Path
import json,sys,hashlib
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
p=P/'storyboards_draft.json'
d=json.loads(p.read_text(encoding='utf-8-sig'))
old='검정폰전화화면 발신자 동료. 상단전화아이콘. 실제번호없음.'
new='검정폰은 뒷면이 카메라를 향한다. 전화 화면을 뒷면에 붙이지 않는다. 휴대폰 옆 빈 공간에 편집용 수신 배지 [전화 아이콘 · 동료]를 12.5~14.95초 후합성. 실제번호없음.'
def rec(x):
 if isinstance(x,str):return x.replace(old,new).replace('전화 수신 화면이 켜지기 직전','수신 반응이 시작되기 직전(휴대폰 옆 편집 배지로 표시)')
 if isinstance(x,list):return [rec(v) for v in x]
 if isinstance(x,dict):return {k:rec(v) for k,v in x.items()}
 return x
d=rec(d)
d.setdefault('image_stage_pd_changes',[]).append({'id':'PD-C09-IMAGE-01','scene':'C09_S05','change':'관측된 폰 뒷면을 유지하고 수신자 동료는 외부 편집 배지로 표시. 화면 방향을 조작하지 않는다. 무음 인과 유지.'})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=json.loads((P/'artist_C09_manifest.json').read_text(encoding='utf-8-sig'))
for e in m['entries']:
 e['sha256']=hashlib.sha256((P/e['file']).read_bytes()).hexdigest()
im=Image.new('RGB',(1000,5*310),(12,20,27));draw=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',24)
for i,e in enumerate(m['entries']):
 x=(i%2)*500;y=(i//2)*310
 z=Image.open(P/e['file']).convert('RGB');z.thumbnail((490,276))
 im.paste(z,(x,y+30));draw.text((x+7,y+2),'C09 '+e['scene_id'],fill='white',font=font)
im.save(P/'contact_C09.jpg',quality=90)
(P/'artist_C09_manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('C09 10 PNG saved, contact generated, caller badge spec synced')
