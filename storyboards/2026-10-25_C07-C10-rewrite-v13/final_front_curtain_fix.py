from pathlib import Path
import json,hashlib,shutil,sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
f=read(P/'artist_C10_front_curtain_fix.json');m=read(P/'artist_C10_manifest.json')
for e in f['entries']:
 dst=P/e['file'];shutil.copy2(e['source_generated_image'],dst)
 e['sha256']=hashlib.sha256(dst.read_bytes()).hexdigest()
 s=next(x for x in m['scenes'] if x['scene_id']==e['scene_id'])
 old={k:s.get(k) for k in ['actual_path','sha256','prompt','reference_images']}
 prev=s.get('previous_selected',[])
 if not isinstance(prev,list):prev=[prev]
 if s['actual_path']!=str(dst):prev.append(old)
 s.update(previous_selected=prev,actual_path=str(dst),relative_image_path=e['file'],sha256=e['sha256'],prompt=e['prompt'],reference_images=e['reference_images'],source_generated_image=e['source_generated_image'],review_status='FRONT_CURTAIN_FIXED_RECHECK_PENDING')
save(P/'artist_C10_manifest.json',m);save(P/'artist_C10_front_curtain_fix.json',f)
im=Image.open(P/'images/C10/S10.png').convert('RGB');draw=ImageDraw.Draw(im)
for text,y,size in [('신기한 결과에서,',50,36),('써볼 수 있는 방법으로.',100,36),('Q-AI Fair',153,50)]:
 font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',size)
 draw.text((84,y),text,font=font,fill='white',stroke_width=1,stroke_fill='white')
im.save(P/'caption_previews/C10_S10_caption_layout_v2.png')
save(P/'caption_previews/layout_manifest.json',{'source':'images/C10/S10.png','proof':'caption_previews/C10_S10_caption_layout_v2.png','text':['신기한 결과에서,','써볼 수 있는 방법으로.','Q-AI Fair'],'font':'Malgun Gothic Bold','sizes':[36,36,50],'positions':[[84,50],[84,100],[84,153]],'flow_start_frame':False,'purpose':'Post-production subtitle placement proof, IB006 hyphen restored'})
print('3 corrected source images + exact Q-AI Fair subtitle proof written')
