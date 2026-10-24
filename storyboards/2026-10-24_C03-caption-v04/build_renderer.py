from pathlib import Path
root=Path(__file__).resolve().parent.parent
old=(root/'2026-10-20_C03-edit-v03/render_edit.py').read_text(encoding='utf-8-sig')
s=old[:old.index("ending=Image.new")]
s=s.replace('from tinysoundfont import Synth','')
a=s.index('captions = ['); b=s.index('# Laptop diagram',a)
s=s[:a]+'''# V11 caption_cues are the sole text/timing source; no spoken audio is required.
v11=SB/'2026-10-23_v11-production-lock/storyboards.json'
concept=next(x for x in json.loads(v11.read_text(encoding='utf-8'))['concepts'] if x['id']=='C03')
caption_cues=[dict(c,cut=sh['id']) for sh in concept['shots'] for c in sh['caption_cues']]
caption_pngs=[]
for cue in caption_cues:
    if cue['kind']=='event': continue
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    size=40 if cue['kind']=='discovery' else 42
    lines=cue['text'].split('\\n');lh=55
    tw=max(d.textlength(line,font=font(size,True)) for line in lines)
    hh=lh*len(lines)+20
    x=38 if cue['kind']=='discovery' else (W-tw)/2
    y=29 if cue['kind']=='discovery' else H-44-hh
    d.rounded_rectangle((x-17,y,x+tw+17,y+hh),12,fill=(9,19,28,220))
    for j,line in enumerate(lines):
        d.text((x+tw/2,y+10+j*lh+25),line,font=font(size,True),fill='white',anchor='mm')
    caption_pngs.append((cue['start'],cue['end'],im))

''' + s[b:]
a=s.index('screen = Image.new'); b=s.index('# Inverse projective',a)
s=s[:a]+'''screen = Image.new('RGBA',(640,480),(234,242,243,255))
sd=ImageDraw.Draw(screen)
for x,label in [(160,'기준'),(480,'이번 결과')]:
    sd.text((x,28),label,font=font(40,True),fill=(23,65,73),anchor='mt')
    sd.rounded_rectangle((x-122,93,x+122,456),15,outline=(42,140,141),width=8)
    sd.ellipse((x-42,119,x+42,203),fill=(42,140,141))
    sd.line((x,238,x,311),fill=(42,140,141),width=15)
    sd.rectangle((x-42,347,x+42,431),fill=(42,140,141))
screen.save(OUT/'laptop_diagram.png')
''' + s[b:]
a=s.index('def condition_graphic'); b=s.index('def page_diagram',a)
s=s[:a]+s[b:]
a=s.index('def page_diagram'); b=s.index('# Manual endpoint fits',a)
s=s[:a]+'''def symbol(d,x,y,kind,color,size=34):
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
''' + s[b:]
# The v03 per-page perspective fits and source-color foreground masks below
# are preserved. Their output now contains the unified V11 artwork.
append='''
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
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\\n',encoding='utf-8')
def srt(t):
    ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
(OUT/'C03_captions.srt').write_text('\\n\\n'.join(f'{i+1}\\n{srt(q["start"])} --> {srt(q["end"])}\\n{q["text"]}' for i,q in enumerate(caption_cues))+'\\n',encoding='utf-8-sig')
oldedit=SB/'2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4'
dump(OUT/'edit_manifest.json',dict(file=picture.name,concept='C03 환경까지 가져왔습니다',duration_seconds=DURATION,fps=FPS,resolution=[W,H],timeline=segments,captions=caption_cues,source_sha256=hashes,original_files_unchanged=True,base_edit_sha256=hashlib.sha256(oldedit.read_bytes()).hexdigest(),caption_source=str(v11.relative_to(SB)),flow_requests=0,flow_credits_used=0,source_audio='Removed entirely; no audio stream',action_stills_inserted=False,changes=['V11 caption_cues; successful and unsuccessful work environments clearly separated','No glove-question caption; sender explicitly identified at K05','K03 matched reference/result geometry; K06 accurate file labels, shared input and different check/correction order','Q-AI Fair ending 38.75–44.75; last cue extended by0.2s to avoid tail flash'],limitations=['Actual continuous playback and listening not verified','Original glove removal and donning remain state edits, not newly generated continuous hand actions','K06 to K07 gathering of both files remains an accepted short ellipsis','Final user and audience reception unverified']))
dump(OUT/'technical_validation.json',dict(file=picture.name,sha256=hashlib.sha256(picture.read_bytes()).hexdigest(),bytes=picture.stat().st_size,frames=frame_count,duration_seconds=DURATION,fps=FPS,dimensions=[W,H],full_video_decode='PASS',audio_stream_count=0,video_pts_step_seconds=1/FPS,source_sha256_unchanged=True,actual_continuous_playback_verified=False,actual_listening_verified=False))
print('DONE',picture,frame_count,flush=True)
'''
s=s+append
out=root/'2026-10-24_C03-caption-v04/render_caption_v04.py'
out.write_text(s,encoding='utf-8')
print(out)
