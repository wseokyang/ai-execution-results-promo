"""Group B V16 picture-only assembly from original Flow clips.

Latest V15 EDLs and scene-attached UI are retained. Editorial captions use the
shared QREW-derived lower-center compositor. No old captioned video is a source.
This file writes only C05/C06/C08/C09 inside its own V16 output folder.
"""
from pathlib import Path
import sys, json, hashlib, subprocess, importlib.util, ast, math, shutil
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
SB = OUT.parent
FF = SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SOURCE_NEW = SB/'2026-10-26_C08-C09-flow-v15'
V15_OLD = SB/'2026-10-26_screening-style-v15'
V15_NEW = SB/'2026-10-26_C08-C09-edit-v15'
W, H, FPS = 1280, 720, 24
sys.path.insert(0, str(OUT))
from style_api import compose_story, write_caption_metadata, SPEC

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def prepare_compositor(film):
    folder = OUT/film
    if film == 'C06':
        source = SB/'2026-10-23_C05-C06-edit-v03/render_films.py'
        code = source.read_text(encoding='utf-8').split('\ndef soundtrack(')[0]
        code = code.replace('from tinysoundfont import Synth', '# No soundtrack synthesis in picture compositor.')
        code = code.replace('OUT=Path(__file__).resolve().parent\nSB=OUT.parent',
            "OUT=Path(__file__).resolve().parent/'compositor_assets'\nOUT.mkdir(parents=True,exist_ok=True)\nSB=Path(__file__).resolve().parents[2]")
        assert "OUT.mkdir(parents=True,exist_ok=True)" in code
        target = folder/'ui_compositor.py'
        target.write_text('# V16 isolated UI-only source; all writes redirected inside C06.\n'+code, encoding='utf-8')
    elif film == 'C08':
        source = V15_NEW/'C08/render_c08_v15.py'
        code = source.read_text(encoding='utf-8')
        tree = ast.parse(code)
        definitions = [ast.get_source_segment(code, n) for n in tree.body
                       if isinstance(n, ast.FunctionDef) and n.name in ['star','ui_art','composite_ui']]
        assert len(definitions) == 3
        prefix = '''"""V16 isolated C08 scene UI. No source folder is written."""
from pathlib import Path
import sys,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
SB=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(SB/'2026-10-25_final-six-v13/C02/.deps'))
import av,numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
SOURCE=SB/'2026-10-26_C08-C09-flow-v15'
W,H=1280,720
def font(n):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',n)
Q={'K03':[(365,216),(693,200),(719,404),(393,440)],'K04':[(315,103),(638,58),(669,259),(358,325)]}
REF={}
for cut in ['K03','K04']:
 with av.open(str(SOURCE/f'C08_{cut}_take01.mp4')) as c:REF[cut]=next(c.decode(video=0)).to_ndarray(format='rgb24')
'''
        target = folder/'ui_compositor.py'
        target.write_text(prefix+'\n\n'+'\n\n'.join(definitions)+'\n', encoding='utf-8')
    else:
        return None, None
    provenance = dict(original_compositor=str(source.relative_to(SB)), original_sha256=sha(source),
                      isolated_copy=target.name, isolated_sha256=sha(target),
                      treatment='UI function bodies retained; output paths isolated; no original import executed.')
    dump(folder/'ui_provenance.json', provenance)
    return load_module(target, film+'_v16_isolated_ui'), provenance

def inputs(film):
    base = (V15_OLD if film in ['C05','C06'] else V15_NEW)/film
    manifest_path = base/'edit_manifest.json'
    old = json.loads(manifest_path.read_text(encoding='utf-8'))
    duration = old['duration_seconds']
    timeline = []
    for row in old.get('segments', old.get('timeline', [])):
        row = dict(row)
        if 'source' not in row:
            row['source'] = str((SOURCE_NEW/row['file']).relative_to(SB)).replace('\\','/')
        elif row['source']:
            row['source'] = row['source'].replace('\\','/')
        timeline.append(row)
    if film in ['C08','C09']:
        timeline.append(dict(cut='END',source=None,source_in=0,source_out=5,
                             start=timeline[-1]['end'],end=duration))
    ending_start = 41.75 if film == 'C05' else timeline[-1]['start']
    cues = []
    for c in old['captions']:
        cue = {k:v for k,v in c.items() if k not in ['pos','position','x','y','font_px','old_start','old_end']}
        cue['kind'] = 'endcard' if c['start'] >= ending_start else cue.get('kind','subtitle')
        cues.append(cue)
    ending_name = 'ending_art_v15.png' if film in ['C05','C06'] else 'ending_v15.png'
    ending_path = base/ending_name
    return old, timeline, cues, duration, ending_start, ending_path, manifest_path

def review_times(film, timeline, cues, duration):
    times = {0, duration-1/FPS}
    for c in cues:
        times.add((c['start']+c['end'])/2)
    for row in timeline:
        times.add(row['start'])
        if row['start']>0: times.add(row['start']-1/FPS)
    extras = {
        'C05':[13.5,17,21.5,22.5,23.5,24.5,27.5,37.5,41.75,43],
        'C06':[3.5,5.5,10.5,14.75,18.25,19.25,22,30.5,34,35.25,37,39.25,42.5],
        'C08':[6.5,8,10.5,11.5,12.5,13,14,23.5,27.5,31.5,38.5,43.5],
        'C09':[8.5,12.5,18,19.5,26.5,28.5,29.5,30.25,31.5,33.5],
    }
    times.update(extras[film])
    return {round(t*FPS) for t in times if 0 <= t < duration}

def verify_picture(path, film, timeline, cues, duration):
    previews = path.parent/'review_frames'
    previews.mkdir(exist_ok=True)
    idxs = review_times(film, timeline, cues, duration)
    frame_paths=[]; pts=[]; count=0; dims=set()
    with av.open(str(path)) as c:
        assert not c.streams.audio, 'Picture-only output must not contain audio'
        stream=c.streams.video[0]
        rate=str(stream.average_rate)
        for frame in c.decode(video=0):
            idx=count; count+=1; pts.append(float(frame.time)); dims.add((frame.width,frame.height))
            if idx in idxs:
                fp=previews/f'{idx/FPS:07.3f}s.png'
                frame.to_image().save(fp)
                frame_paths.append(fp)
    expected=round(duration*FPS)
    assert count==expected, (count,expected)
    assert dims=={(W,H)}
    step_error=max(abs(pts[i+1]-pts[i]-1/FPS) for i in range(count-1))
    assert abs(pts[0])<1e-8 and abs(pts[-1]-(duration-1/FPS))<1e-8 and step_error<1e-8
    label_font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
    sheets=[]
    # Small contact-sheet pages remain legible when opened by review tools.
    for offset in range(0,len(frame_paths),16):
        batch=frame_paths[offset:offset+16]
        sheet=Image.new('RGB',(1280,math.ceil(len(batch)/4)*204),(22,24,28)); d=ImageDraw.Draw(sheet)
        for i,p in enumerate(batch):
            x=(i%4)*320;y=(i//4)*204
            with Image.open(p) as im:sheet.paste(im.resize((320,180)),(x,y))
            d.text((x+7,y+183),film+' '+p.stem,font=label_font,fill='white')
        sp=path.parent/f'contact_sheet_{offset//16+1:02d}.jpg';sheet.save(sp,quality=90);sheets.append(sp.name)
    record=dict(file=path.name,sha256=sha(path),bytes=path.stat().st_size,frames=count,
                duration_seconds=duration,fps=rate,resolution=[W,H],audio_streams=0,full_decode='PASS',
                first_pts=pts[0],last_pts=pts[-1],max_pts_step_error=step_error,
                actual_realtime_playback_verified=False,actual_listening_verified=False,
                extracted_review_frames=[str(p.relative_to(path.parent)) for p in frame_paths],
                contact_sheets=sheets,visual_review='EXTRACTED_PENDING_ACTUAL_OPEN')
    dump(path.parent/'picture_qa.json',record)
    return record

def render(film):
    assert film in ['C05','C06','C08','C09']
    folder=OUT/film;folder.mkdir(parents=True,exist_ok=True)
    old,timeline,cues,duration,ending_start,ending_path,manifest_path=inputs(film)
    copy_ending=folder/'ending_art_v16.png'
    shutil.copyfile(ending_path,copy_ending)
    ending=Image.open(copy_ending).convert('RGBA' if film=='C05' else 'RGB')
    assert ending.size==(W,H)
    normalized_cues=write_caption_metadata(folder,cues,film)
    # Keep scene UI compositors independent from editorial subtitle layout.
    ui,ui_provenance=prepare_compositor(film)
    sources={r['source']:SB/r['source'] for r in timeline if r['source']}
    hashes={k:sha(p) for k,p in sources.items()}
    original_hashes=old.get('source_sha256',{})
    old_normalized={k.replace('\\','/'):v for k,v in original_hashes.items()}
    for k,h in hashes.items():
        match=old_normalized.get(k,old_normalized.get(Path(k).name))
        if match is not None:assert h==match,('Original source changed since V15',k)
    picture=folder/f'{film}_picture_v16.mp4'
    frame_audit=[];n=0
    with (folder/'picture_render_stderr.txt').open('wb') as log:
        enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720',
                              '-r','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','medium',
                              '-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)],
                             stdin=subprocess.PIPE,stderr=log)
        try:
            for row in timeline:
                expected=round((row['end']-row['start'])*FPS)
                assert n==round(row['start']*FPS),('EDL gap',film,row['cut'],n)
                ct=0; source_pts=[]
                if row['source'] is None:
                    for _ in range(expected):enc.stdin.write(ending.tobytes());n+=1;ct+=1
                else:
                    with av.open(str(sources[row['source']])) as c:
                        for f in c.decode(video=0):
                            st=float(f.time)
                            if st < row['source_in']-1e-7:continue
                            if st >= row['source_out']-1e-7:break
                            t=n/FPS; array=f.to_ndarray(format='rgb24')
                            if film=='C08' and row['cut'] in ['K03','K04']:
                                array=ui.composite_ui(array,row['cut'],st)
                            im=Image.fromarray(array)
                            if row.get('crop'):
                                im=im.crop(tuple(row['crop'])).resize((W,H),Image.Resampling.LANCZOS)
                            if film=='C06':im=ui.composite(im.convert('RGBA'),row['cut'],st,t,film)
                            im=compose_story(im,cues,t)
                            if film=='C05' and t>=ending_start:
                                im=im.convert('RGBA');im.alpha_composite(ending);im=im.convert('RGB')
                            enc.stdin.write(im.tobytes());n+=1;ct+=1;source_pts.append(st)
                assert ct==expected,(film,row['cut'],ct,expected)
                frame_audit.append(dict(cut=row['cut'],output_frame_start=n-ct,output_frames=ct,
                                        first_source_pts=source_pts[0] if source_pts else None,
                                        last_source_pts=source_pts[-1] if source_pts else None))
                print(f'{film} {row["cut"]} {ct} frames ({n}/{round(duration*FPS)})',flush=True)
        finally:
            enc.stdin.close();enc.wait()
    assert enc.returncode==0 and n==round(duration*FPS)
    assert hashes=={k:sha(p) for k,p in sources.items()},'Original changed while rendering'
    qa=verify_picture(picture,film,timeline,cues,duration)
    manifest=dict(film=film,version=16,file=picture.name,picture_file=picture.name,
                  duration_seconds=duration,fps=FPS,resolution=[W,H],timeline=timeline,
                  captions=normalized_cues,caption_style=SPEC,source_sha256=hashes,
                  source_of_picture='Original Flow MP4s with preserved scene UI; no baked-caption picture reused',
                  original_files_unchanged=True,source_audio='ALL EXCLUDED; new score owned by parent task',
                  action_stills_inserted=False,flow_credits_used=0,
                  base_manifest=str(manifest_path.relative_to(SB)),base_manifest_sha256=sha(manifest_path),
                  ending=dict(file=copy_ending.name,source=str(ending_path.relative_to(SB)),
                              sha256=sha(copy_ending),start=ending_start,end=duration,
                              live_action_background=film=='C05'),
                  ui_provenance=ui_provenance,picture_qa=qa,
                  status='PICTURE_COMPLETE_AUDIO_PENDING',
                  actual_realtime_playback_verified=False,actual_continuous_playback_verified=False,
                  actual_listening_verified=False)
    for key in ['limitations','known_editorial_compromises','causal_design','ui','screen_plane_quads','ui_foreground']:
        if key in old:manifest[key]=old[key]
    manifest['revision_scope']='Editorial captions moved to lower center; same latest approved motion timing, source trims, UI and endings.'
    dump(folder/'edit_manifest.json',manifest)
    dump(folder/'frame_audit.json',frame_audit)
    print('COMPLETE',film,qa['frames'],qa['sha256'],flush=True)

if __name__=='__main__':
    for film in sys.argv[1:] or ['C05','C06','C08','C09']:render(film)
