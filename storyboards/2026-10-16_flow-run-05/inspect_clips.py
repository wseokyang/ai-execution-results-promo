from pathlib import Path
import sys, subprocess, json, hashlib
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'2026-10-15_flow-pilot-01'/'.tools'))
import imageio_ffmpeg
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
result=[]
for cid,take in [('C01_K06','take01'),('C01_K07','take01'),('C01_K04','take02')]:
    clip=root/(cid+'_'+take+'.mp4')
    if not clip.exists(): continue
    reader=imageio_ffmpeg.read_frames(str(clip))
    meta=next(reader)
    reader.close()
    step=max(1,round(meta['fps']/2))
    frames=root/'frames'/cid
    frames.mkdir(parents=True,exist_ok=True)
    info=subprocess.run([ffmpeg,'-hide_banner','-i',str(clip)],capture_output=True,encoding='utf-8',errors='replace').stderr
    (root/(cid+'_media_info.txt')).write_text(info,encoding='utf-8')
    subprocess.run([ffmpeg,'-y','-hide_banner','-loglevel','error','-i',str(clip),'-vf',f"select='not(mod(n,{step}))',scale=480:-1",'-vsync','vfr','-frames:v','16',str(frames/'frame_%02d.jpg')],check=True)
    paths=sorted(frames.glob('frame_*.jpg'))
    w,h=Image.open(paths[0]).size
    sheet=Image.new('RGB',(w*4,(h+26)*4),'#171717')
    draw=ImageDraw.Draw(sheet)
    for n,p in enumerate(paths):
        x=n%4*w; y=n//4*(h+26)
        sheet.paste(Image.open(p),(x,y))
        draw.text((x+8,y+h+5),f'{cid} | {n*step/meta['fps']:.1f}s',fill='white')
    sheet.save(root/(cid+'_contact_sheet.jpg'),quality=92)
    result.append({'clip_id':cid,'file':clip.name,'bytes':clip.stat().st_size,'sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'duration_seconds':meta['duration'],'resolution':list(meta['size']),'fps':meta['fps'],'audio_stream_present':'Audio:' in info,'sample_times_seconds':[n*step/meta['fps'] for n in range(len(paths))],'contact_sheet':cid+'_contact_sheet.jpg','review_scope':'16 sampled frames at 0.5-second intervals; not continuous playback or lip-sync validation'})
(root/'media_inspection.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
