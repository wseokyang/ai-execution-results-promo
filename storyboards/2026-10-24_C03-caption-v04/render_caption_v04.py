"""C03 revised review edit. Every picture segment is real Flow motion.

All original MP4s are read-only. Overlays and sound are new local derivatives.
No Flow/API calls. No playback/listening verification is implied by this script.
"""
from pathlib import Path
import sys, subprocess, json, hashlib, re, shutil
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
SB = OUT.parent
FF = SB / '2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SR, FPS, W, H = 48000, 24, 1280, 720
R1 = '2026-10-19_C03-flow-run01'
R2 = '2026-10-19_C03-flow-run02'
R3 = '2026-10-20_C03-flow-run03'
R5 = '2026-10-20_C03-flow-run05'
R6 = '2026-10-20_C03-flow-run06'
R8 = '2026-10-20_C03-flow-run08'
R9 = '2026-10-20_C03-flow-run09'
timeline = [
    ('K01', R8, 'C03_K01_take02.mp4', 0, 6),
    ('K02', R1, 'C03_K02_take01.mp4', 0, 4),
    ('K03', R1, 'C03_K03_take01.mp4', 0, 2.5),
    ('K03_done', R5, 'C03_K03_insert_take02.mp4', 6, 7),
    ('K04', R3, 'C03_K04_take02.mp4', 0, 3.5),
    ('K04_cuff', R6, 'C03_K04_insert_take05.mp4', 2.25, 5.75),
    ('K05_listen', R9, 'C03_K05_question_take05.mp4', 0, 1),
    ('K05', R3, 'C03_K05_take03.mp4', 1.25, 4.75),
    ('K06_before', R2, 'C03_K06_take01.mp4', 0, 1.25),
    ('K06_records', R8, 'C03_K06_insert_take01.mp4', 0, 2),
    ('K06_after', R2, 'C03_K06_take01.mp4', 3.25, 5.75),
    ('K07', R3, 'C03_K07_take02.mp4', 0, 6),
    ('K08', R3, 'C03_K08_take02.mp4', 0, 8),
]
segments, cursor = [], 0
for cut, run, name, start, end in timeline:
    segments.append(dict(cut=cut, source=f'{run}/{name}', source_in=start,
                         source_out=end, start=cursor, end=cursor + end-start))
    cursor += end-start
DURATION = cursor
assert DURATION == 44.75
def shifted(t):
    return t-.5 if t>=25.5 else (t+.5 if t>=5.5 else t)
extra_sources = [f'{R1}/C03_K05_take01.mp4', f'{R2}/VO_C03_S_take01.mp4',f'{R2}/C03_K06_take01.mp4']
sources = set([s['source'] for s in segments] + extra_sources)
hashes = {s: hashlib.sha256((SB/s).read_bytes()).hexdigest() for s in sources}

def run(args, **kwargs):
    p = subprocess.run([str(FF), *args], capture_output=True, **kwargs)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[-6000:])
    return p

def font(size, bold=False):
    return ImageFont.truetype(f'C:/Windows/Fonts/{"malgunbd" if bold else "malgun"}.ttf', size)

def center_text(d, xy, text, size, color='white', bold=False, **kwargs):
    d.text(xy, text, font=font(size,bold), fill=color, anchor='mt', **kwargs)

# V11 caption_cues are the sole text/timing source; no spoken audio is required.
v11=SB/'2026-10-23_v11-production-lock/storyboards.json'
concept=next(x for x in json.loads(v11.read_text(encoding='utf-8'))['concepts'] if x['id']=='C03')
caption_cues=[dict(c,cut=sh['id']) for sh in concept['shots'] for c in sh['caption_cues']]
caption_pngs=[]
for cue in caption_cues:
    if cue['kind']=='event': continue
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    size=40 if cue['kind']=='discovery' else 42
    lines=cue['text'].split('\n');lh=55
    tw=max(d.textlength(line,font=font(size,True)) for line in lines)
    hh=lh*len(lines)+20
    x=38 if cue['kind']=='discovery' else (W-tw)/2
    y=29 if cue['kind']=='discovery' else H-44-hh
    d.rounded_rectangle((x-17,y,x+tw+17,y+hh),12,fill=(9,19,28,220))
    for j,line in enumerate(lines):
        d.text((x+tw/2,y+10+j*lh+25),line,font=font(size,True),fill='white',anchor='mm')
    caption_pngs.append((cue['start'],cue['end'],im))

# Laptop diagram rendered into the visible screen, not a full-screen insert.
screen = Image.new('RGBA',(640,480),(234,242,243,255))
sd=ImageDraw.Draw(screen)
for x,label in [(160,'기준'),(480,'이번 결과')]:
    sd.text((x,28),label,font=font(40,True),fill=(23,65,73),anchor='mt')
    sd.rounded_rectangle((x-122,93,x+122,456),15,outline=(42,140,141),width=8)
    sd.ellipse((x-42,119,x+42,203),fill=(42,140,141))
    sd.line((x,238,x,311),fill=(42,140,141),width=15)
    sd.rectangle((x-42,347,x+42,431),fill=(42,140,141))
screen.save(OUT/'laptop_diagram.png')
# Inverse projective transform: output screen corners -> graphic corners.
dest = [(751,389),(952,397),(900,558),(699,537)]
src = [(0,0),(640,0),(640,480),(0,480)]
mat, vec = [], []
for (x,y),(u,v) in zip(dest,src):
    mat += [[x,y,1,0,0,0,-u*x,-u*y], [0,0,0,x,y,1,-v*x,-v*y]]
    vec += [u,v]
coeffs = np.linalg.solve(np.array(mat),np.array(vec))
screen_warp = screen.transform((W,H), Image.Transform.PERSPECTIVE, coeffs,
                               Image.Resampling.BICUBIC)

def symbol(d,x,y,kind,color,size=34):
    if kind=='circle':d.ellipse((x-size,y-size,x+size,y+size),fill=color)
    elif kind=='square':d.rectangle((x-size,y-size,x+size,y+size),fill=color)
    else:d.line((x-size,y,x-8,y+size*.65,x+size,y-size*.7),fill=color,width=13)
def arrow(d,x1,y1,x2,y2,color,width=6):
    d.line((x1,y1,x2,y2),fill=color,width=width)
    import math
    ang=math.atan2(y2-y1,x2-x1);r=15
    d.polygon([(x2,y2),(x2-r*math.cos(ang-.5),y2-r*math.sin(ang-.5)),(x2-r*math.cos(ang+.5),y2-r*math.sin(ang+.5))],fill=color)
def page_diagram(label,color,trial=False):
    # Exact V11 labels, shared input, distinct checking/correction order.
    # These symbols illustrate fictional records, not measured causal proof.
    im=Image.new('RGBA',(600,350),(239,242,244,255));d=ImageDraw.Draw(im)
    d.text((18,12),label,font=font(42,True),fill=(24,52,64,255))
    d.line((18,70,575,70),fill=(*color,255),width=5)
    teal=(35,130,137,255)
    symbol(d,300,139,'circle',teal,30)
    d.rounded_rectangle((251,91,349,188),12,outline=(232,178,35,255),width=8)
    syms=['circle','check','square'] if trial else ['circle','square','check']
    for x,k in zip([95,300,505],syms):symbol(d,x,264,k,(*color,255))
    arrow(d,140,264,248,264,(*color,255));arrow(d,345,264,453,264,(*color,255))
    if trial:
        d.line((505,310,505,333,300,333,300,313),fill=(*color,255),width=5)
        d.polygon([(300,307),(290,321),(310,321)],fill=(*color,255))
    return im
page_art=[page_diagram('시행착오 기록',(211,110,35),True),page_diagram('잘됐던 작업 기록',(35,130,137))]
for name,im in zip(['trial','success'],page_art):im.save(OUT/f'page_{name}.png')
# Manual endpoint fits from actual 0s/2s frames, with an intermediate 1s fit.
# Central paper areas only, avoiding hands, margins and binder rings.
page_tracks=[
 [(0,[(508,54),(805,101),(712,307),(418,244)]),
  (1,[(518,51),(809,95),(715,309),(425,251)]),
  (2,[(527,48),(812,89),(717,312),(430,257)])],
 [(0,[(878,398),(1152,472),(1088,649),(796,549)]),
  (1,[(880,404),(1154,480),(1088,654),(796,555)]),
  (2,[(882,411),(1155,487),(1088,660),(796,561)])]
]
def records_graphic(local):
    im=Image.new('RGBA',(W,H))
    for art,track in zip(page_art,page_tracks):
        tt=[x[0] for x in track]
        quad=[(float(np.interp(local,tt,[v[1][i][0] for v in track])),
               float(np.interp(local,tt,[v[1][i][1] for v in track]))) for i in range(4)]
        mat,vec=[],[]
        for (x,y),(u,v) in zip(quad,[(0,0),(600,0),(600,350),(0,350)]):
            mat += [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]
            vec += [u,v]
        coeff=np.linalg.solve(np.array(mat),np.array(vec))
        im.alpha_composite(art.transform((W,H),Image.Transform.PERSPECTIVE,
                           coeff,Image.Resampling.BICUBIC))
    return im
records_graphic(0).save(OUT/'records_diagram_overlay.png')
(OUT/'records_tracking.json').write_text(json.dumps({
    'source':f'{R8}/C03_K06_insert_take01.mp4','source_range':[0,2],
    'method':'Manually keyed inner-page plane quads with linear interpolation; final rendered samples must be checked',
    'page_tracks':page_tracks,'numbers_are_not_performance_claims':True},indent=2),encoding='utf-8')

# Wide-view continuity: use the same artwork on the actual visible pages.
# The gray page stays on the desk until the closed orange binder covers it.
def warp_page(art, quad):
    mat,vec=[],[]
    for (x,y),(u,v) in zip(quad,[(0,0),(600,0),(600,350),(0,350)]):
        x,y=x*3,y*3
        mat += [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]
        vec += [u,v]
    coeff=np.linalg.solve(np.array(mat),np.array(vec))
    return art.transform((W*3,H*3),Image.Transform.PERSPECTIVE,coeff,
                         Image.Resampling.BICUBIC).resize((W,H),Image.Resampling.LANCZOS)

wide_page_art=[]
for art in page_art:
    opaque=Image.new('RGBA',(600,350),(237,239,243,255))
    opaque.alpha_composite(art)
    wide_page_art.append(opaque)
gray_wide_quad=[(403,627),(589,612),(728,654),(533,674)]
orange_wide_tracks=[
 (3.25,[(482,391),(649,420),(582,453),(454,419)]),
 (3.417,[(474,399),(653,419),(584,446),(451,422)]),
 (3.583,[(473,408),(651,421),(592,439),(452,423)]),
 (3.708,[(474,416),(642,424),(590,434),(455,423)])]

def wide_records_graphic(frame, source_t):
    base=np.asarray(frame.convert('RGB'))
    out=Image.new('RGBA',(W,H))
    if source_t < 4.75:
        layer=warp_page(wide_page_art[1],gray_wide_quad)
        arr=np.array(layer)
        # Preserve foreground hands, orange binder and dark binding edges.
        rgb=base.astype(float)
        foreground=(rgb[:,:,0]>1.25*rgb[:,:,1])&((rgb[:,:,0]-rgb[:,:,2])>45)
        visible=~foreground
        arr[:,:,3]=(arr[:,:,3].astype(float)*visible).astype(np.uint8)
        out.alpha_composite(Image.fromarray(arr))
    if 3.25 <= source_t <= 3.708:
        tt=[r[0] for r in orange_wide_tracks]
        quad=[(float(np.interp(source_t,tt,[r[1][i][0] for r in orange_wide_tracks])),
               float(np.interp(source_t,tt,[r[1][i][1] for r in orange_wide_tracks]))) for i in range(4)]
        layer=warp_page(wide_page_art[0],quad)
        arr=np.array(layer)
        rgb=base.astype(float)
        foreground=(rgb[:,:,0]>1.25*rgb[:,:,1])&((rgb[:,:,0]-rgb[:,:,2])>45)
        visible=~foreground
        arr[:,:,3]=(arr[:,:,3].astype(float)*visible).astype(np.uint8)
        out.alpha_composite(Image.fromarray(arr))
    return out

(OUT/'wide_records_tracking.json').write_text(json.dumps({
 'source':f'{R2}/C03_K06_take01.mp4',
 'gray_quad':gray_wide_quad,'orange_tracks':orange_wide_tracks,
 'method':'Same artwork, opaque paper patch, manual plane fit; source color mask preserves foreground binder/hands.',
 'review_required':'Rendered continuity and masking checked separately; no new generated video.'
},indent=2),encoding='utf-8')


ending=Image.new('RGBA',(W,H));ed=ImageDraw.Draw(ending)
for y in range(270):
    alpha=round(215*(1+np.cos(np.pi*y/270))/2)
    ed.line((0,y,W,y),fill=(8,25,35,alpha))
center_text(ed,(640,31),'Q-AI Fair',68,'white',True)
center_text(ed,(640,126),'AI 실행의 과정까지, 함께 봐요.',39,(245,250,249),True)
ending.save(OUT/'ending_title.png')
# Keep title to the final frame, a 0.2s extension of V11's 44.55 end cue.
for cue in caption_cues:
    if cue['kind']=='event':cue['end']=DURATION
picture=OUT/'C03_Q-AI_Fair_edit_v04.mp4'
with (OUT/'render_stderr.txt').open('wb') as log:
    enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
        '-s','1280x720','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18',
        '-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)],
        stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
    frame_count=0
    try:
        for seg in segments:
            count=0
            with av.open(str(SB/seg['source'])) as container:
                for f in container.decode(video=0):
                    st=float(f.time)
                    if st<seg['source_in']-1e-5:continue
                    if st>=seg['source_out']-1e-5:break
                    local=st-seg['source_in'];t=seg['start']+local
                    im=f.to_image().convert('RGBA')
                    if seg['cut']=='K03':im.alpha_composite(screen_warp)
                    if seg['cut']=='K06_records':im.alpha_composite(records_graphic(local))
                    if seg['cut'] in ['K06_before','K06_after']:im.alpha_composite(wide_records_graphic(im,st))
                    if t>=38.75:im.alpha_composite(ending)
                    for a,b,cap in caption_pngs:
                        if a<=t<b:im.alpha_composite(cap)
                    enc.stdin.write(im.convert('RGB').tobytes());frame_count+=1;count+=1
            assert count==round((seg['source_out']-seg['source_in'])*FPS),(seg,count)
            print('picture',seg['cut'],count,flush=True)
    finally:enc.stdin.close();enc.wait()
assert enc.returncode==0 and frame_count==1074
run(['-v','error','-i',str(picture),'-f','null','-'])
assert hashes=={s:hashlib.sha256((SB/s).read_bytes()).hexdigest() for s in sources}
frames=OUT/'review_frames';frames.mkdir(exist_ok=True)
samples=set(range(0,1074,12))|{1073}
for seg in segments:
    samples|={round(seg['start']*FPS)+j for j in [-1,0,1]}
for cue in caption_cues:
    samples|={round(q*FPS)+j for q in [cue['start'],cue['end']] for j in [-1,0,1]}
samples={i for i in samples if 0<=i<1074}
thumbs=[];pts=[]
with av.open(str(picture)) as c:
    assert len(c.streams.audio)==0
    for i,f in enumerate(c.decode(video=0)):
        pts.append(float(f.time))
        if i not in samples:continue
        im=f.to_image();im.save(frames/f'{i/FPS:06.3f}s.png')
        card=Image.new('RGB',(320,208),(15,23,31));card.paste(im.resize((320,180)),(0,28))
        ImageDraw.Draw(card).text((8,3),f'{i/FPS:.3f}s',font=font(17,True),fill='white');thumbs.append(card)
assert len(pts)==1074 and np.allclose(np.diff(pts),1/FPS)
import math
for batch in range(math.ceil(len(thumbs)/20)):
    sub=thumbs[batch*20:(batch+1)*20];sheet=Image.new('RGB',(1280,208*math.ceil(len(sub)/4)),(15,23,31))
    for j,im in enumerate(sub):sheet.paste(im,((j%4)*320,(j//4)*208))
    sheet.save(OUT/f'review_contact_{batch+1:02d}.jpg',quality=95)
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def srt(t):
    ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
(OUT/'C03_captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt(q["start"])} --> {srt(q["end"])}\n{q["text"]}' for i,q in enumerate(caption_cues))+'\n',encoding='utf-8-sig')
oldedit=SB/'2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4'
dump(OUT/'edit_manifest.json',dict(file=picture.name,concept='C03 환경까지 가져왔습니다',duration_seconds=DURATION,fps=FPS,resolution=[W,H],timeline=segments,captions=caption_cues,source_sha256=hashes,original_files_unchanged=True,base_edit_sha256=hashlib.sha256(oldedit.read_bytes()).hexdigest(),caption_source=str(v11.relative_to(SB)),flow_requests=0,flow_credits_used=0,source_audio='Removed entirely; no audio stream',action_stills_inserted=False,changes=['V11 caption_cues; successful and unsuccessful work environments clearly separated','No glove-question caption; sender explicitly identified at K05','K03 matched reference/result geometry; K06 accurate file labels, shared input and different check/correction order','Q-AI Fair ending 38.75–44.75; last cue extended by0.2s to avoid tail flash'],limitations=['Actual continuous playback and listening not verified','Original glove removal and donning remain state edits, not newly generated continuous hand actions','K06 to K07 gathering of both files remains an accepted short ellipsis','Final user and audience reception unverified']))
dump(OUT/'technical_validation.json',dict(file=picture.name,sha256=hashlib.sha256(picture.read_bytes()).hexdigest(),bytes=picture.stat().st_size,frames=frame_count,duration_seconds=DURATION,fps=FPS,dimensions=[W,H],full_video_decode='PASS',audio_stream_count=0,video_pts_step_seconds=1/FPS,source_sha256_unchanged=True,actual_continuous_playback_verified=False,actual_listening_verified=False))
print('DONE',picture,frame_count,flush=True)
