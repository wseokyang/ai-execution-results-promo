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
from tinysoundfont import Synth

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
timeline = [
    ('K01', R8, 'C03_K01_take02.mp4', 0, 6),
    ('K02', R1, 'C03_K02_take01.mp4', 0, 4),
    ('K03', R1, 'C03_K03_take01.mp4', 0, 2.5),
    ('K03_done', R5, 'C03_K03_insert_take02.mp4', 6, 7),
    ('K04', R3, 'C03_K04_take02.mp4', 0, 3.5),
    ('K04_cuff', R6, 'C03_K04_insert_take05.mp4', 2.25, 5.75),
    ('K05', R3, 'C03_K05_take03.mp4', 1, 6.5),
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
assert DURATION == 45.75
def shifted(t): return t+.5 if t>=5.5 else t
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

captions = [
    (0, 2.55, '결과 말고, 어떻게 했는지도요.'),
    (5.5, 7.65, '작업 환경, 도착했습니다.'),
    (9.5, 11.3, '정확히 같이 나오네요.'),
    (13.70, 15.35, '아직 하나 더요.'),
    (20.30, 22.10, '이건 왜 보냈어요?'),
    (22.25, 25.10, '안 됐던 것도 빠짐없이 달라면서요.'),
    (27.85, 29.60, '반품… 잠깐.'),
    (31.25, 33.50, '이건 직접 들어야겠네요.'),
    (33.75, 35.80, '제가 갈게요.'),
]
captions=[(shifted(a),shifted(b),line) for a,b,line in captions]
caption_pngs = []
for start, end, line in captions:
    im = Image.new('RGBA', (W,H))
    d = ImageDraw.Draw(im)
    box = d.textbbox((0,0), line, font=font(32, True))
    tw = box[2]-box[0]
    d.rounded_rectangle(((W-tw)/2-24, 638, (W+tw)/2+24, 697), 13,
                        fill=(12,19,24,185))
    center_text(d, (W/2,645), line, 32, bold=True)
    caption_pngs.append((start,end,im))

# Laptop diagram rendered into the visible screen, not a full-screen insert.
screen = Image.new('RGBA', (640,480), (230,236,236,255))
sd = ImageDraw.Draw(screen)
for y, label in [(35,'참고'), (255,'실행 결과')]:
    sd.text((35,y),label,font=font(32,True),fill=(39,69,73))
    for i in range(3):
        x=40+i*185
        sd.rounded_rectangle((x,y+65,x+145,y+155),12,
                             fill=(65,131,139), outline=(39,89,98),width=3)
        sd.line((x+28,y+111,x+55,y+137,x+112,y+82),fill=(245,255,252),width=9)
sd.line((30,235,610,235),fill=(183,200,201),width=3)
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

def condition_graphic(local):
    """Paired internal-record callout. Leader anchors follow visible pages."""
    im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    orange_pts=[(1.25,515,418),(1.5,516,381),(2.0,540,387),(2.5,542,400),(3.0,550,417)]
    px=float(np.interp(local,[p[0] for p in orange_pts],[p[1] for p in orange_pts]))
    py=float(np.interp(local,[p[0] for p in orange_pts],[p[2] for p in orange_pts]))
    orange=(241,144,52,255); teal=(44,135,147,255)
    d.line([(px,py),(740,554),(850,554)],fill=(255,255,255,235),width=6)
    d.line([(px,py),(740,554),(850,554)],fill=orange,width=3)
    d.line([(564,646),(754,650),(850,650)],fill=(255,255,255,235),width=6)
    d.line([(564,646),(754,650),(850,650)],fill=teal,width=3)
    for (x,y),col in [((px,py),orange),((564,646),teal)]:
        d.ellipse((x-7,y-7,x+7,y+7),fill=col,outline='white',width=2)
    d.rounded_rectangle((838,485,1240,696),18,fill=(248,250,248,246),
                        outline=(209,221,222,255),width=2)
    d.text((862,499),'같은 조건',font=font(29,True),fill=(25,52,60))
    for y,label,col in [(546,'시행착오 기록',orange),(625,'내 작업 기록',teal)]:
        d.text((862,y),label,font=font(22,True),fill=(40,62,69))
        for i,h in enumerate([11,24,16]):
            x=1067+i*47
            d.rounded_rectangle((x,y+27-h,x+31,y+27),3,fill=col)
        d.rounded_rectangle((1056,y-6,1207,y+36),6,outline=col,width=2)
    return im
condition_graphic(1.5).save(OUT/'condition_callout_preview.png')

def page_diagram(label,color):
    im=Image.new('RGBA',(600,350))
    d=ImageDraw.Draw(im)
    d.text((18,14),label,font=font(38,True),fill=(30,49,58,255))
    d.line((18,70,575,70),fill=(*color,255),width=5)
    d.text((18,94),'같은 조건',font=font(45,True),fill=(25,54,64,255))
    for i,(lab,h) in enumerate(zip(['입력','설정','환경'],[55,100,72])):
        x=30+i*185
        d.rounded_rectangle((x,270-h,x+112,270),8,fill=(*color,235))
        d.text((x+16,284),lab,font=font(30,True),fill=(36,57,64,255))
    return im

page_art=[page_diagram('시행착오 기록',(212,111,31)),
          page_diagram('내 작업 기록',(40,122,134))]
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

ending=Image.new('RGBA',(W,H))
ed=ImageDraw.Draw(ending)
for y in range(390):
    alpha=round(212*(1+np.cos(np.pi*y/390))/2)
    ed.line((0,y,W,y),fill=(8,25,35,alpha))
center_text(ed,(640,30),'2026년 품질팀',25,(222,238,239),True)
center_text(ed,(640,73),'AI 실행 결과 발표 대회',49,'white',True,
            stroke_width=1,stroke_fill=(10,30,40,180))
center_text(ed,(640,153),'어떻게 해냈는지, 과정까지 함께 들어보세요.',27,
            (246,249,247),False)
ed.line((548,209,732,209),fill=(118,214,208),width=3)
ending.save(OUT/'ending_title.png')

picture = OUT/'C03_picture_v02.mp4'
log=(OUT/'render_stderr.txt').open('wb')
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
                if st < seg['source_in']-1e-5: continue
                if st >= seg['source_out']-1e-5: break
                local=st-seg['source_in']; t=seg['start']+local
                im=f.to_image().convert('RGBA')
                if seg['cut']=='K03':
                    im.alpha_composite(screen_warp)
                if seg['cut']=='K06_records':
                    im.alpha_composite(records_graphic(local))
                if seg['cut'] in ['K06_before','K06_after']:
                    im.alpha_composite(wide_records_graphic(im,st))
                if t >= 40.75:
                    im.alpha_composite(ending)
                for a,b,cap in caption_pngs:
                    if a <= t < b:
                        im.alpha_composite(cap)
                enc.stdin.write(im.convert('RGB').tobytes())
                frame_count+=1; count+=1
        assert count==round((seg['source_out']-seg['source_in'])*FPS), (seg,count)
        print('picture',seg['cut'],count,flush=True)
finally:
    enc.stdin.close()
    enc.wait()
    log.close()
assert enc.returncode==0 and frame_count==1098

# Source audio only; no speech synthesis and no dialogue speed changes.
def decode_audio(relative,start,end):
    result=run(['-v','error','-i',str(SB/relative),'-vn','-af',
        f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS',
        '-ar',str(SR),'-ac','2','-f','f32le','-']).stdout
    a=np.frombuffer(result,dtype=np.float32).reshape(-1,2).copy()
    n=round((end-start)*SR)
    a=np.pad(a,((0,max(0,n-len(a))),(0,0)))[:n]
    # Short fades protect edit boundaries without changing whole phonemes.
    fade=min(round(.008*SR),len(a)//2)
    a[:fade]*=np.linspace(0,1,fade)[:,None]
    a[-fade:]*=np.linspace(1,0,fade)[:,None]
    return a

mix=np.zeros((round(DURATION*SR),2),np.float32)
audio_events=[]
def add_audio(relative,start,end,at,gain=1.0,role='original sync'):
    a=decode_audio(relative,start,end)*gain
    lo=round(at*SR); hi=min(len(mix),lo+len(a))
    mix[lo:hi]+=a[:hi-lo]
    audio_events.append(dict(source=relative,source_in=start,source_out=end,
                             at=at,gain=gain,role=role))

gains={'K01':.85,'K02':.65,'K03':.85,'K04':.65,'K05':.18,
       'K07':.75,'K08':.9}
for seg in segments:
    if seg['cut'] in gains:
        add_audio(seg['source'],seg['source_in'],seg['source_out'],seg['start'],
                  gains[seg['cut']])
add_audio(f'{R1}/C03_K03_take01.mp4',4.5,5.5,12.5,.3,'nonverbal ambient bridge')
add_audio(f'{R3}/C03_K04_take02.mp4',4.5,8,17,.22,'nonverbal ambient bridge')
add_audio(f'{R1}/C03_K05_take01.mp4',2.4,4.2,20.65,.75,'R question, rear view')
add_audio(f'{R2}/VO_C03_S_take01.mp4',0,2.7,22.75,.60,'offscreen telephone S')
add_audio(f'{R2}/C03_K06_take01.mp4',0,5.75,26,1.15,'K06 original continuous dialogue under insert')

# New, sparse score composed for this film only. No borrowed song or demo MIDI.
sf=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
synth=Synth(gain=-15,samplerate=SR)
sid=synth.sfload(str(sf))
synth.program_select(0,sid,0,61)  # brass section
synth.program_select(1,sid,0,11)  # vibraphone
notes=[]
def note(t,d,pitch,v=48,ch=0):
    notes.append(dict(start=shifted(t),duration=d,pitch=pitch,velocity=v,channel=ch))
for p in [48,55,60,64]: note(7.55,.55,p,48)
for p in [60,64,67]: note(11.35,.32,p,35,1)
note(13.08,.12,48,48); note(13.29,.12,55,48)
for p in [55,60,64]: note(35.85,.7,p,36,1)
for t,p in [(40.25,60),(40.55,64),(40.85,67),(41.3,72)]:
    note(t,.85,p,36,1)
events=[]
for n in notes:
    events += [(round(n['start']*SR),1,n),
               (round((n['start']+n['duration'])*SR),0,n)]
events.sort(key=lambda v:(v[0],v[1]))
score=np.zeros_like(mix); pos=0
for idx,on,n in events:
    if idx>pos:
        score[pos:idx]=np.frombuffer(synth.generate(idx-pos),np.float32).reshape(-1,2)
        pos=idx
    if on: synth.noteon(n['channel'],n['pitch'],n['velocity'])
    else: synth.noteoff(n['channel'],n['pitch'])
score[pos:]=np.frombuffer(synth.generate(len(score)-pos),np.float32).reshape(-1,2)
score*=.07/max(1e-9,float(np.abs(score).max()))
score[round(14*SR):round(36.3*SR)]=0
score[-SR:]*=np.linspace(1,0,SR)[:,None]
mix+=score
# Small procedural fabric rub for the otherwise silent cuff insert.
rng=np.random.default_rng(103)
cloth=np.zeros(round(DURATION*SR),np.float32)
for t,dur,gain in [(16.8,.65,.003),(18.9,.25,.002)]:
    n=round(dur*SR)
    noise=rng.normal(0,1,n+8)
    filtered=np.convolve(noise,np.ones(9)/9,'valid')
    env=np.sin(np.linspace(0,np.pi,n))**2
    start=round(shifted(t)*SR)
    cloth[start:start+n]+=filtered[:n]*env*gain
mix+=cloth[:,None]
# Fade out only atmosphere under the already completed final action.
mix[-round(.25*SR):]*=np.linspace(1,0,round(.25*SR))[:,None]
assert np.isfinite(mix).all()
for name,audio in [('C03_mix_float.wav',mix),('C03_original_sparse_score.wav',score)]:
    run(['-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-',
         '-c:a','pcm_f32le',str(OUT/name)],input=audio.tobytes())

def loudness(path):
    p=run(['-hide_banner','-i',str(path),'-af',
           'loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',p.stderr.decode(errors='replace'))[-1])
measurement=loudness(OUT/'C03_mix_float.wav')
normalizer=(f'loudnorm=I=-18:TP=-1.5:LRA=11:measured_I={measurement["input_i"]}:'
            f'measured_TP={measurement["input_tp"]}:measured_LRA={measurement["input_lra"]}:'
            f'measured_thresh={measurement["input_thresh"]}:offset={measurement["target_offset"]}:linear=true')
final=OUT/'C03_review_edit_v02_46s.mp4'
run(['-y','-v','error','-i',str(picture),'-i',str(OUT/'C03_mix_float.wav'),
     '-map','0:v:0','-map','1:a:0','-c:v','copy',
     '-af',normalizer+',alimiter=limit=0.89:level=false:latency=true',
     '-c:a','aac','-b:a','256k','-ar',str(SR),'-ac','2','-t',str(DURATION),
     '-movflags','+faststart',str(final)])
run(['-v','error','-i',str(final),'-f','null','-'])
decoded=np.frombuffer(run(['-v','error','-i',str(final),'-vn','-ar',str(SR),
    '-ac','2','-f','f32le','-']).stdout,np.float32)
assert np.isfinite(decoded).all() and np.abs(decoded).max()<1
assert hashes=={s:hashlib.sha256((SB/s).read_bytes()).hexdigest() for s in sources}

# Review evidence comes from actual final MP4, not source mockups.
frames_dir=OUT/'review_frames'; frames_dir.mkdir(exist_ok=True)
times=sorted(set([0,1,2,4.5,5.458,5.5,7.5,9.458,9.5,10.5,11.958,
    12,12.958,13,14.5,16.458,16.5,17.5,19.5,19.958,20,20.5,21.5,22.5,24.5,
    25.458,25.5,26.25,26.708,26.75,27,27.75,28.25,28.458,28.5,29.5,30.5,31.208,31.25,
    32.5,34.5,36.5,37.208,37.25,39.5,40.208,40.25,41.5,42.75,43.5,45.208]))
times=[shifted(t) for t in times]+[5.5,5.958,6,27.208,27.25,27.75,28.25,28.75,29.208,29.25]
frame_indexes={round(t*FPS):t for t in times}
thumbs=[]
with av.open(str(final)) as c:
    n=0
    for i,f in enumerate(c.decode(video=0)):
        n+=1
        if i in frame_indexes:
            im=f.to_image()
            name=f'{i/FPS:06.3f}s.png'
            im.save(frames_dir/name)
            thumb=im.resize((320,180))
            card=Image.new('RGB',(320,208),(15,23,31)); card.paste(thumb,(0,28))
            ImageDraw.Draw(card).text((10,4),f'{i/FPS:.3f}s',font=font(18),fill='white')
            thumbs.append(card)
assert n==1098
for batch in range((len(thumbs)+15)//16):
    subset=thumbs[batch*16:(batch+1)*16]
    contact=Image.new('RGB',(1280,208*((len(subset)+3)//4)),(15,23,31))
    for j,im in enumerate(subset): contact.paste(im,((j%4)*320,(j//4)*208))
    contact.save(OUT/f'review_contact_{batch+1:02d}.jpg',quality=94)

for n in ['GeneralUser-GS-LICENSE.txt']:
    shutil.copyfile(SB/'2026-10-17_C01-sound-v04'/n,OUT/n)
sound_sources=json.loads((SB/'2026-10-17_C01-sound-v04/score_sources.json').read_text(encoding='utf-8'))
sound_sources['usage']='New original sparse brass/vibraphone cues for C03. C01 music, melodies and demo MIDI are not reused.'
(OUT/'score_sources.json').write_text(json.dumps(sound_sources,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'original_score_notes.json').write_text(json.dumps(notes,indent=2),encoding='utf-8')
record=dict(status='revised review edit; final user viewing/listening pending',
    concept='V8 C03 환경까지 가져왔습니다',file=final.name,duration_seconds=DURATION,
    dimensions=[W,H],fps=FPS,decoded_frames=n if isinstance(n,int) else frame_count,
    timeline=segments,captions=captions,audio_events=audio_events,original_sha256=hashes,
    original_files_unchanged=True,new_flow_requests=4,new_credits_used=30,
    graphics={'K03':'Same three boxes, reference/result, laptop perspective composite for 2.5s',
              'K06':'New real motion closeup with diagrams on both inner pages, 27.25–29.25s',
              'ending':'40.75–45.75s fixed event title and attendance invitation'},
    pd_changes=['Removal action replaced by 1s bare-hand end state; insertion omitted before cuff adjustment.',
                'K05 question audio over clean rear-view file pickup; no voice speed alteration.',
                'New K01 physical shadow and upward reaction used through6s.',
                'New K06 inner-page insert replaces2s within original scene; original voice unchanged.',
                'K06 gathering files to K07 held files is a temporal ellipsis.'],
    technical={'full_decode_pass':True,'frames':frame_count,'originals_unchanged':True,
               'decoded_pcm_peak':float(np.abs(decoded).max()),'full_scale_samples':int((np.abs(decoded)>=1).sum()),
               'pre_master_loudness':measurement,'final_loudness':loudness(final)},
    limitations=['No actual listening, continuous playback, pronunciation or lip-sync verification claimed.',
                 'Three reviewer final-render sample reviews pending.',
                 'K05 new synchronous shot held after two audio failures/refunds; existing clean picture and question audio retained.'])
(OUT/'edit_manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
preview=Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/edit-v02')
preview.mkdir(parents=True,exist_ok=True)
shutil.copyfile(final,preview/final.name)
print(json.dumps({'output':str(final),'duration':DURATION,'frames':frame_count,
                  'peak':float(np.abs(decoded).max()),'bytes':final.stat().st_size},ensure_ascii=False),flush=True)
