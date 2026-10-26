"""Rebuild C02/C03/C04 pictures from untouched Flow originals for V16.

This script owns only C02, C03 and C04 output folders. It never writes to
earlier runs. Existing picture/final MP4s are not used as captioned sources.
Audio is composed and muxed by the parent task separately.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, math, subprocess, sys
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/opencv')
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parent
SB=BASE.parent
ROOT=SB.parent
V13=SB/'2026-10-25_final-six-v13'
V15=SB/'2026-10-26_screening-style-v15'
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
W,H,FPS=1280,720,24
FILMS=('C02','C03','C04')

def dump(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(args,**kw):
    p=subprocess.run([str(FF),*map(str,args)],capture_output=True,**kw)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[-6000:])
    return p

def load_compositor(cid,out):
    """Execute only the historical compositor prefix with all output paths redirected.

    The prefix has needed graphic initialization, but no final-render loop or
    audio call. Original module text is read-only and kept as provenance.
    """
    if cid=='C03':
        source=V15/cid/'render_c03_picture_v15.py'
        if not source.exists():source=BASE/'source_helpers/render_c03_picture_v15.py'
        marker='\nending=Image.new'
    else:
        source=V13/cid/f'render_{cid.lower()}.py'
        marker='\ndef previews():' if cid=='C02' else '\ndef timeline():'
    text=source.read_text(encoding='utf-8')
    assert marker in text
    prefix=text.split(marker,1)[0]
    prefix=prefix.replace('OUT=Path(__file__).resolve().parent','OUT=NEW_OUT')
    prefix=prefix.replace('OUT = Path(__file__).resolve().parent','OUT = NEW_OUT')
    prefix=prefix.replace('SB=OUT.parent.parent','SB=SOURCE_SB')
    prefix=prefix.replace('SB = OUT.parent.parent','SB = SOURCE_SB')
    prefix=prefix.replace('V=OUT.parent','V=SOURCE_V13')
    assets=out/'compositor_assets';assets.mkdir(parents=True,exist_ok=True)
    ns={'__file__':str(source),'__name__':f'v16_compositor_{cid}',
        'NEW_OUT':assets,'SOURCE_SB':SB,'SOURCE_V13':V13}
    exec(compile(prefix,str(source)+'[safe_prefix]','exec'),ns)
    assert ns['OUT']==assets and ns['SB']==SB
    return ns,{'source_script':str(source.relative_to(ROOT)).replace('\\','/'),
               'source_sha256':sha(source),
               'loaded_prefix_sha256':hashlib.sha256(prefix.encode()).hexdigest(),
               'output_redirected_to':str(assets.relative_to(ROOT)).replace('\\','/'),
               'original_script_executed_whole':False}

def load_spec(cid):
    d=json.loads((V15/cid/'edit_manifest.json').read_text(encoding='utf-8'))
    edl=[dict(s) for s in d['timeline']]
    for s in edl:
        if s['source']:s['source']=s['source'].replace('\\','/')
    duration=float(d['duration_seconds'])
    caps=[]
    for old in d['captions']:
        c={k:old[k] for k in ('start','end','text')}
        event=old.get('kind')=='event' or old.get('position')=='ending' or old['text'].startswith('Q-AI Fair\n')
        c['kind']='endcard' if event else old.get('kind','subtitle')
        c['position']='existing_full_frame_ending' if event else 'bottom_center'
        c['previous_caption_metadata']=old
        caps.append(c)
    assert abs(edl[-1]['end']-duration)<1e-6
    for a,b in zip(edl,edl[1:]):assert abs(a['end']-b['start'])<1e-6
    return d,edl,caps,duration

def load_style():
    p=BASE/'style_api.py'
    if not p.exists():raise RuntimeError('Parent-owned style_api.py must be finalized before rendering')
    spec=importlib.util.spec_from_file_location('v16_style_api_a',p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    assert callable(module.compose_story)
    return module

def ending_art(cid):
    name='ending_title.png' if cid=='C03' else 'ending_art_v15.png'
    return Image.open(V15/cid/name).convert('RGBA'),V15/cid/name

def compositor_frame(cid,ns,frame,seg,source_t):
    if cid in ('C02','C04'):
        return Image.fromarray(ns['picture'](np.array(frame.convert('RGB')),seg['cut'],source_t)).convert('RGBA')
    im=frame.convert('RGBA')
    if seg['cut']=='K03':im.alpha_composite(ns['screen_warp'])
    if seg['cut']=='K06_records':im.alpha_composite(ns['records_graphic'](source_t-seg['source_in']))
    if seg['cut'] in ('K06_before','K06_after'):im.alpha_composite(ns['wide_records_graphic'](im,source_t))
    return im

def fps_sample_indices(source_count,speed):
    """Use FFmpeg's own fps filter to reproduce the V14 1.25x frame selection.

    A 1x1 gray16 source encodes the source-frame number losslessly. No action
    frame is interpolated and source timestamps remain available for tracking.
    """
    raw=np.arange(source_count,dtype='<u2').tobytes()
    p=run(['-v','error','-f','rawvideo','-pixel_format','gray16le','-video_size','1x1',
           '-framerate',FPS,'-i','-','-vf',f'setpts=(PTS-STARTPTS)/{speed},fps={FPS}',
           '-pix_fmt','gray16le','-f','rawvideo','-'],input=raw)
    ids=np.frombuffer(p.stdout,dtype='<u2').astype(int).tolist()
    assert len(ids)==round(source_count/speed)
    assert all(0<=i<source_count for i in ids)
    return ids

def source_frames(seg):
    source=SB/seg['source']
    frames=[]
    with av.open(str(source)) as c:
        assert float(c.streams.video[0].average_rate)==FPS
        for f in c.decode(video=0):
            st=float(f.time)
            if st<seg['source_in']-1e-6:continue
            if st>=seg['source_out']-1e-6:break
            frames.append((st,f.to_image()))
    expected=round((seg['source_out']-seg['source_in'])*FPS)
    assert len(frames)==expected,(source,len(frames),expected)
    speed=float(seg.get('speed',1))
    indices=list(range(len(frames))) if speed==1 else fps_sample_indices(len(frames),speed)
    assert len(indices)==round((seg['end']-seg['start'])*FPS)
    return frames,indices

def srt_time(t):
    n=round(t*1000)
    return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'

def write_srt(out,cid,caps):
    text='\n\n'.join(f'{i+1}\n{srt_time(c["start"])} --> {srt_time(c["end"])}\n{c["text"]}' for i,c in enumerate(caps))+'\n'
    (out/f'{cid}_captions_v16.srt').write_text(text,encoding='utf-8-sig')

def picture_qa(path,out,duration,edl,caps):
    run(['-v','error','-i',path,'-f','null','-'])
    n=round(duration*FPS);picks=set(range(0,n,12))|{n-1}
    for t in [s['start'] for s in edl]+[c['start'] for c in caps]+[c['end'] for c in caps]:
        picks.update(round(t*FPS)+k for k in (-1,0,1))
    frames_dir=out/'review_frames';frames_dir.mkdir(exist_ok=True)
    tiles=[];pts=[]
    font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',15)
    with av.open(str(path)) as c:
        assert len(c.streams.audio)==0
        for i,f in enumerate(c.decode(video=0)):
            pts.append(float(f.time))
            if i in picks:
                im=f.to_image();im.save(frames_dir/f'{i/FPS:06.3f}s.png')
                tile=Image.new('RGB',(320,204),(12,18,25));tile.paste(im.resize((320,180)),(0,24))
                ImageDraw.Draw(tile).text((7,2),f'{i/FPS:.3f}s',font=font,fill='white');tiles.append(tile)
    assert len(pts)==n and np.allclose(np.diff(pts),1/FPS)
    for j in range(math.ceil(len(tiles)/12)):
        group=tiles[j*12:(j+1)*12];sheet=Image.new('RGB',(1280,204*math.ceil(len(group)/4)),(12,18,25))
        for k,tile in enumerate(group):sheet.paste(tile,(k%4*320,k//4*204))
        sheet.save(out/f'contact_{j+1:02d}.jpg',quality=93)
    q={'file':path.name,'sha256':sha(path),'duration_seconds':duration,'video_frames':n,
       'fps':FPS,'resolution':[W,H],'full_video_decode':'PASS','audio_streams':0,
       'video_pts_step_seconds':1/FPS,'actual_continuous_playback_verified':False,
       'actual_listening_verified':False,'visual_review':'PENDING_ACTUAL_IMAGE_INSPECTION'}
    dump(out/'picture_technical_qa.json',q)
    return q

def process(cid,prepare=False):
    assert cid in FILMS
    out=BASE/cid;out.mkdir(parents=True,exist_ok=True)
    old,edl,caps,duration=load_spec(cid)
    ns,provenance=load_compositor(cid,out)
    art,art_path=ending_art(cid);art.save(out/'ending_art_v16.png')
    source_set={s['source'] for s in edl if s['source']}
    hashes={s:sha(SB/s) for s in sorted(source_set)}
    original_files={str((V15/cid/'edit_manifest.json').relative_to(ROOT)):sha(V15/cid/'edit_manifest.json'),
                    str(art_path.relative_to(ROOT)):sha(art_path)}
    write_srt(out,cid,caps)
    dump(out/'caption_manifest.json',caps)
    prepared={'film':cid,'duration_seconds':duration,'timeline':edl,'captions':caps,
              'source_sha256':hashes,'compositor_provenance':provenance,
              'original_reference_sha256':original_files,'source_audio':'ALL EXCLUDED',
              'action_stills_inserted':False,'existing_picture_mp4_used_as_source':False}
    if prepare:
        prepared['status']='COMPOSITOR_AND_EDL_PREPARED_STYLE_CONFIRMATION_PENDING'
        dump(out/'prepared_manifest.json',prepared)
        print('PREPARED',cid,duration,flush=True);return
    style=load_style()
    caps=style.write_caption_metadata(out,caps,cid)
    prepared['captions']=caps
    style_hash=sha(BASE/'style_api.py')
    pic=out/f'{cid}_picture_v16.mp4';n=0;speed_maps=[]
    with (out/'picture_render_stderr.txt').open('wb') as log:
        enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
            '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18',
            '-preset','medium','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(pic)],
            stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
        try:
            for seg in edl:
                count=round((seg['end']-seg['start'])*FPS)
                if not seg['source']:
                    for _ in range(count):enc.stdin.write(art.convert('RGB').tobytes());n+=1
                else:
                    frames,indices=source_frames(seg)
                    if seg.get('speed',1)!=1:speed_maps.append({'cut':seg['cut'],'speed':seg['speed'],'source_indices':indices})
                    for k,idx in enumerate(indices):
                        st,frame=frames[idx];t=seg['start']+k/FPS
                        im=compositor_frame(cid,ns,frame,seg,st)
                        if cid=='C03' and t>=37:
                            im.alpha_composite(art);im=im.convert('RGB')
                        else:im=style.compose_story(im,caps,t).convert('RGB')
                        enc.stdin.write(im.tobytes());n+=1
                    del frames
                print('RENDERED',cid,seg['cut'],count,flush=True)
        finally:enc.stdin.close();enc.wait()
    assert enc.returncode==0 and n==round(duration*FPS),(cid,enc.returncode,n)
    q=picture_qa(pic,out,duration,edl,caps)
    assert hashes=={s:sha(SB/s) for s in hashes}
    assert original_files=={s:sha(ROOT/s) for s in original_files}
    prepared.update({'file':pic.name,'picture_sha256':q['sha256'],'picture_technical_qa':q,
        'version':'V16','status':'PICTURE_RENDERED_TECHNICAL_PASS_VISUAL_REVIEW_PENDING',
        'source_files_unchanged':True,'speed_frame_selection':speed_maps,
        'subtitle_style_module_sha256':style_hash,
        'actual_continuous_playback_verified':False,'actual_listening_verified':False})
    dump(out/'picture_manifest.json',prepared)
    print('PICTURE_DONE',cid,duration,q['sha256'],flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true')
    parser.add_argument('films',nargs='*',default=list(FILMS))
    args=parser.parse_args()
    for cid in args.films:process(cid,args.prepare)
