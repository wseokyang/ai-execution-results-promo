from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent;SB=OUT.parent
old=json.loads((SB/'2026-10-20_C03-edit-v03/edit_manifest.json').read_text(encoding='utf-8-sig'))
new=json.loads((OUT/'edit_manifest.json').read_text(encoding='utf-8-sig'))
checks={s:hashlib.sha256((SB/s).read_bytes()).hexdigest()==h for s,h in old['original_sha256'].items()}
old_film=SB/'2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4'
old_sha=hashlib.sha256(old_film.read_bytes()).hexdigest()
assert all(checks.values()) and old_sha==old['sha256']
assert old['timeline']==new['timeline']
v=json.loads((OUT/'technical_validation.json').read_text(encoding='utf-8'))
v.update(historical_v03_original_sha256_matches=True,historical_v03_film_sha256_matches=True,old_v03_sha256=old_sha,source_count_checked=len(checks),unique_action_source_count=len({s['source'] for s in new['timeline']}),timeline_identical_to_v03=True)
(OUT/'technical_validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
times=[.5,4.5,8,11,14.5,17.5,21,23.5,27,29,31.5,34.5,38,40,42.5,44.5]
sheet=Image.new('RGB',(1280,832),(15,23,31));font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',17)
for j,t in enumerate(times):
 im=Image.open(OUT/'review_frames'/f'{t:06.3f}s.png');card=Image.new('RGB',(320,208),(15,23,31));card.paste(im.resize((320,180)),(0,28));ImageDraw.Draw(card).text((8,3),f'{t:.3f}s',font=font,fill='white');sheet.paste(card,((j%4)*320,(j//4)*208))
sheet.save(OUT/'review_overview.jpg',quality=95)
print(json.dumps(v,ensure_ascii=False,indent=2))
