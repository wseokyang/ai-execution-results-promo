"""Inspect the derived six-second framing candidate, not the untouched original."""
from pathlib import Path
import sys, json, hashlib
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parent
p=R/'C05-F06_crop_review_6s.mp4'
out=R/'crop_review_frames'; out.mkdir(exist_ok=True)
targets=[0,.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,5.958]
rows=[]; idx=0; count=0; edge_tiles=[]
c=av.open(str(p)); s=c.streams.video[0]
for f in c.decode(video=0):
    count+=1; t=float(f.pts*f.time_base)
    edge_tiles.append(f.to_image().crop((1200,0,1280,720)).resize((40,360)))
    if idx<len(targets) and t+.001>=targets[idx]:
        name=f'frame_{idx:02d}_{t:.3f}s.jpg'
        f.to_image().save(out/name,quality=94)
        rows.append({'file':name,'seconds':t}); idx+=1
c.close()
for start in range(0,len(edge_tiles),48):
    sheet=Image.new('RGB',(768,1140),'#181818'); d=ImageDraw.Draw(sheet)
    for j,tile in enumerate(edge_tiles[start:start+48]):
        x=(j%16)*48; y=(j//16)*380
        sheet.paste(tile,(x,y+20)); d.text((x,y+4),str(start+j),fill='white')
    sheet.save(out/f'all_frame_right_edges_{start//48+1:02d}.jpg',quality=96)
for start in range(0,len(rows),9):
    chunk=rows[start:start+9]; sheet=Image.new('RGB',(1280,792),'#181818'); d=ImageDraw.Draw(sheet)
    for j,row in enumerate(chunk):
        x=(j%3)*428; y=(j//3)*264
        sheet.paste(Image.open(out/row['file']).resize((420,236)),(x,y+24))
        d.text((x+6,y+5),f"{row['seconds']:.3f}s",fill='white')
    sheet.save(out/f'sheet_{start//9+1:02d}.jpg',quality=94)
data={'file':p.name,'source':'C05-F06_take02.mp4','source_seconds':[0,6],
      'crop_pixels':[0,40,960,540],'output_resolution':[1280,720],'fps':24,
      'duration_seconds':6,'decoded_frames':count,'decode_pass':True,
      'audio_removed_for_visual_review_only':True,
      'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
      'ffmpeg_filter':'crop=960:540:0:40,scale=1280:720',
      'review_status':'pending_three_independent_cross_reviews','sampled_frames':rows}
manifest=R/'crop_review_manifest.json'
if manifest.exists():
    prior=json.loads(manifest.read_text(encoding='utf-8-sig'))
    if prior.get('sha256')==data['sha256']:
        for key in ('review_status','original_wide_accepted','right_edge_inspection','render_args'):
            if key in prior: data[key]=prior[key]
manifest.write_bytes((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print('Cropped render decoded and sampled:',count,'frames;',len(rows),'samples')
