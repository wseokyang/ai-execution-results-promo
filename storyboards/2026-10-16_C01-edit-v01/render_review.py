"""C01 55-second review edit. Original Flow files remain byte-identical."""
from pathlib import Path
import subprocess, json, hashlib, wave, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SB = ROOT.parent
FF = SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
CACHE = ROOT/'.render'
CACHE.mkdir(exist_ok=True)
FONT = 'C:/Windows/Fonts/malgun.ttf'
BOLD = 'C:/Windows/Fonts/malgunbd.ttf'
clips = [
    ('C01_K01', '2026-10-16_flow-run-06', 'take02', 6),
    ('C01_K02', '2026-10-16_flow-run-06', 'take02', 8),
    ('C01_K03', '2026-10-16_flow-run-06', 'take02', 7),
    ('C01_K04', '2026-10-16_flow-run-05', 'take02', 6),
    ('C01_K05', '2026-10-16_flow-run-04', 'take01', 7),
    ('C01_K06', '2026-10-16_flow-run-05', 'take01', 8),
    ('C01_K07', '2026-10-16_flow-run-05', 'take01', 7),
]

def run(args):
    p = subprocess.run([str(FF), '-y', '-hide_banner', '-loglevel', 'error']+list(map(str,args)), capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode('utf8', errors='replace'))

def label(draw, xy, text, size, fill, bold=False):
    font = ImageFont.truetype(BOLD if bold else FONT, size)
    draw.text(xy, text, font=font, fill=fill, anchor='mm')

# Rasterize the established title layout at source-video resolution.
title = Image.new('RGBA', (1920,1080))
d = ImageDraw.Draw(title)
d.rounded_rectangle((70,242,1850,838), radius=24, fill=(9,18,28,224))
d.rectangle((900,312,1020,318), fill='#edc495')
label(d,(960,390),'2026년 품질팀',42,'#edc495')
label(d,(960,520),'AI 실행 결과 발표 대회',98,'white',True)
label(d,(960,683),'직접 해본 이야기를 나눕니다.',43,'#d9e1ea')
title.resize((1280,720),Image.Resampling.LANCZOS).save(ROOT/'title_overlay_720.png')

caption = Image.new('RGBA',(1280,720))
d=ImageDraw.Draw(caption)
d.rounded_rectangle((191,628,1089,690),radius=10,fill=(9,18,28,215))
label(d,(640,659),'직접 해본 AI 활용 경험을 나누는 자리',32,'white',True)
caption.save(ROOT/'context_caption_720.png')

manifest={'status':'review_edit_audio_and_lipsync_not_approved','resolution':[1280,720],'fps':24,'duration_seconds':55,'clips':[],
 'audio_scope':'Source audio retained, plus clearly identified local Microsoft Heami draft voice for offscreen D in K04. No listening or lipsync approval.',
 'pd_changes':['K02 uses full 8 seconds to avoid cutting the late ASR-detected word.','K07 uses 7 seconds and bucket-in-front callback; exact under-chin final pose not achieved.','Ending freezes the final included K07 frame for 6 seconds.'],
 'title_basis':'flow_handoff/2026-10-15_v2/post/C01/title_overlay.svg',
 'music':'No new music added in this review edit; dramatic music design remains pending.'}
cursor=0
segments=[]
for cid,folder,take,duration in clips:
    source=SB/folder/(cid+'_'+take+'.mp4')
    out=CACHE/(cid+'.mp4')
    args=['-i',source]
    vf=f'[0:v]trim=duration={duration},setpts=PTS-STARTPTS,fps=24,setsar=1[v]'
    af=f'[0:a]atrim=duration={duration},asetpts=PTS-STARTPTS,aresample=48000,apad,atrim=duration={duration}'
    if cid=='C01_K04':
        args+=['-i',ROOT/'C01_K04_D_heami_draft.wav']
        af+=',volume=0.32[amb];[1:a]loudnorm=I=-18:TP=-2:LRA=7,aresample=48000,adelay=1000|1000[voice];[amb][voice]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.89[a]'
    elif cid=='C01_K03':
        af+=',volume=0.7,afade=t=in:d=0.03,afade=t=out:st=6.95:d=0.05[a]'
    else:
        af+=f',loudnorm=I=-18:TP=-2:LRA=9,aresample=48000,afade=t=in:d=0.02,afade=t=out:st={duration-0.02}:d=0.02[a]'
    if cid=='C01_K06':
        args+=['-loop','1','-i',ROOT/'context_caption_720.png']
        vf=vf.replace('[v]','[base]')+';[base][1:v]overlay=0:0:shortest=1[v]'
    run(args+['-filter_complex',vf+';'+af,'-map','[v]','-map','[a]','-t',duration,'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',out])
    segments.append(out)
    manifest['clips'].append({'clip_id':cid,'source':str(source.relative_to(SB)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'in':0,'out':duration,'timeline_start':cursor,'timeline_end':cursor+duration})
    cursor+=duration

last=SB/'2026-10-16_flow-run-05/C01_K07_take01.mp4'
# Same final included frame; no jump back to a representative still.
freeze=ROOT/'ending_source_frame.png'
run(['-i',last,'-vf',"select='eq(n,167)'",'-frames:v','1',freeze])
ending=CACHE/'ending.mp4'
run(['-loop','1','-framerate','24','-i',freeze,'-loop','1','-i',ROOT/'title_overlay_720.png','-i',last,
 '-filter_complex','[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v];[2:a]atrim=start=7:end=8,asetpts=PTS-STARTPTS,volume=0.12,afade=t=out:st=0:d=0.8,apad,atrim=duration=6,aresample=48000[a]',
 '-map','[v]','-map','[a]','-t','6','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',ending])
segments.append(ending)
listing=CACHE/'segments.txt'
listing.write_text(''.join("file '"+p.name+"'\n" for p in segments),encoding='utf8')
output=ROOT/'C01_review_edit_v01_55s.mp4'
run(['-f','concat','-safe','0','-i',listing,'-c','copy','-movflags','+faststart',output])
manifest['ending']={'start':49,'end':55,'source_frame_index':167,'source_time_seconds':167/24,'seconds':6}
manifest['output']={'file':output.name,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
(ROOT/'edit_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
run(['-i',output,'-f','null','-'])
print(json.dumps(manifest['output'],ensure_ascii=False))
