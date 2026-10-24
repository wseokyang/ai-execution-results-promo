from pathlib import Path
import sys,json,subprocess,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;SB=R.parent;O=R/'edit_probes';O.mkdir(exist_ok=True)
F=SB/'2026-10-24_v12-C02-C04-C01-flow'
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',16)
def contact(path,out,step=6):
    tiles=[]
    with av.open(str(path)) as con:
        for i,f in enumerate(con.decode(video=0)):
            if i%step:continue
            im=f.to_image();tile=Image.new('RGB',(320,205),(12,22,31));tile.paste(im.resize((320,180)),(0,25));ImageDraw.Draw(tile).text((8,3),f'{i/24:.3f}s',font=font,fill='white');tiles.append(tile)
    im=Image.new('RGB',(1280,205*math.ceil(len(tiles)/4)),(12,22,31))
    for i,t in enumerate(tiles):im.paste(t,((i%4)*320,(i//4)*205))
    im.save(out,quality=94)
plans={
 'C01_exit_to_fall':[(R/'C01_K05_take03.mp4',2.5,7.25),(F/'C01_K06_take01.mp4',1.5,4.25)],
 'C04_windows_to_spoon':[(R/'C04_K08_three_visible_take01.mp4',2,3.5),(R/'C04_K09_take02.mp4',.5,6)],
 'C06_impact_to_sort':[(SB/'2026-10-24_C06-caption-v05/C06_Q-AI_Fair_edit_v05.mp4',4,5),(R/'C06_K02_impact_take01.mp4',.75,2.25),(SB/'2026-10-24_C06-caption-v05/C06_Q-AI_Fair_edit_v05.mp4',6.5,9.75)]
}
manifest={}
for name,segs in plans.items():
    cmd=[str(FF),'-y','-v','error'];filters=[];cursor=0;items=[]
    for i,(p,a,b) in enumerate(segs):
        cmd+=['-i',str(p)];filters.append(f'[{i}:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,setsar=1[v{i}]');items.append(dict(source=str(p.relative_to(SB)),source_in=a,source_out=b,start=cursor,end=cursor+b-a));cursor+=b-a
    filters.append(''.join(f'[v{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=1:a=0[v]')
    dest=O/f'{name}.mp4';cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)]
    p=subprocess.run(cmd,capture_output=True);assert p.returncode==0,p.stderr
    contact(dest,O/f'{name}_contact.jpg',12)
    manifest[name]=dict(duration=cursor,segments=items,audio='muted',status='join review pending; not final caption edit')
(O/'manifest.json').write_bytes((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
# Dense samples locate the first visible palm contact, not sound quality.
tiles=[]
with av.open(str(R/'C06_K02_impact_take01.mp4')) as c:
    for i,f in enumerate(c.decode(video=0)):
        if i<36 or i>54:continue
        im=f.to_image();t=Image.new('RGB',(320,205),(12,22,31));t.paste(im.resize((320,180)),(0,25));ImageDraw.Draw(t).text((8,3),f'{i/24:.3f}s / frame{i}',font=font,fill='white');tiles.append(t)
im=Image.new('RGB',(1280,205*math.ceil(len(tiles)/4)),(12,22,31))
for i,t in enumerate(tiles):im.paste(t,((i%4)*320,(i//4)*205))
im.save(O/'C06_contact_timing.jpg',quality=95)
print('DONE probes')
