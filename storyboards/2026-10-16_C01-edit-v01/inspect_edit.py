from pathlib import Path
import sys,subprocess,json,hashlib,shutil
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'2026-10-15_flow-pilot-01/.tools'))
import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
clip=root/'C01_review_edit_v01_55s.mp4'
r=imageio_ffmpeg.read_frames(str(clip)); meta=next(r); r.close()
times=[0,5.9,6,13.9,14,20.9,21,26.9,27,33.9,34,41.9,42,48.9,49,51,54.9]
frames=root/'review_frames'; frames.mkdir(exist_ok=True)
sheet=Image.new('RGB',(4*480,5*296),'#171717'); d=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    dest=frames/f'{t:04.1f}s.jpg'
    subprocess.run([ff,'-y','-v','error','-ss',str(t),'-i',str(clip),'-frames:v','1','-vf','scale=480:-1',str(dest)],check=True)
    x=i%4*480;y=i//4*296
    sheet.paste(Image.open(dest),(x,y));d.text((x+8,y+275),f'{t:.1f}s',fill='white')
sheet.save(root/'edit_contact_sheet.jpg',quality=92)
info=subprocess.run([ff,'-hide_banner','-i',str(clip)],capture_output=True).stderr.decode('utf8',errors='replace').replace('\r\n','\n')
(root/'media_info.txt').write_text(info,encoding='utf8')
decode=subprocess.run([ff,'-v','error','-i',str(clip),'-f','null','-'],capture_output=True)
audio=subprocess.run([ff,'-hide_banner','-i',str(clip),'-vn','-af','volumedetect','-f','null','-'],capture_output=True).stderr.decode('utf8',errors='replace').replace('\r\n','\n')
(root/'audio_levels.txt').write_text(audio,encoding='utf8')
result={'duration_seconds':meta['duration'],'fps':meta['fps'],'resolution':meta['size'],'audio_track': 'Audio:' in info,'decode_exit_code':decode.returncode,'decode_errors':decode.stderr.decode('utf8',errors='replace').replace('\r\n','\n'),'samples_seconds':times,'review_scope':'sampled visual frames and technical decode only; not listening/lipsync approval'}
(root/'render_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
preview=Path('C:/Users/wseok/.codex/visualizations/2026/10/16/01a13daf-3732-7b90-99a8-92c605090d35')
for f in [clip,root/'edit_contact_sheet.jpg']:
    shutil.copyfile(f,preview/f.name)
print(json.dumps(result,ensure_ascii=False))
