"""Replace only the soft jack insert; preserve the established caption/audio timing."""
from pathlib import Path
import sys, json, hashlib, subprocess
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
from PIL import Image, ImageDraw, ImageFont

RUN=Path(__file__).resolve().parent
SB=RUN.parent
OUT=SB/'2026-10-25_C05-jack-edit-v06'
OUT.mkdir(exist_ok=True)
BASE=SB/'2026-10-24_C05-causal-edit-v05/C05_Q-AI_Fair_causal_edit_v05.mp4'
RAW=RUN/'C05_K04_jack_detail_take01.mp4'
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
DEST=OUT/'C05_Q-AI_Fair_causal_edit_v06.mp4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def audio_packets(p):
    with av.open(str(p)) as c:
        return [(x.pts,x.dts,str(x.time_base),hashlib.sha256(bytes(x)).hexdigest()) for x in c.demux(audio=0) if x.size]

source_hash={str(p.relative_to(SB)):sha(p) for p in [BASE,RAW]}
with av.open(str(RAW)) as c:
    replacement=[f.to_image() for f in c.decode(video=0) if 1.5-1e-6<=float(f.time)<3-1e-6]
assert len(replacement)==36
cmd=[str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-i',str(BASE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-preset','medium','-c:a','copy','-pix_fmt','yuv420p','-movflags','+faststart',str(DEST)]
with (OUT/'render_stderr.txt').open('wb') as err:
    enc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=err)
    with av.open(str(BASE)) as c:
        for i,f in enumerate(c.decode(video=0)):
            im=replacement[i-630] if 630<=i<666 else f.to_image()
            enc.stdin.write(im.convert('RGB').tobytes())
    enc.stdin.close();enc.wait()
assert enc.returncode==0 and i+1==1230
p=subprocess.run([str(FF),'-v','error','-i',str(DEST),'-f','null','-'],capture_output=True)
assert p.returncode==0,p.stderr
assert audio_packets(BASE)==audio_packets(DEST)
font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',17)
frames=OUT/'review_frames';frames.mkdir(exist_ok=True)
samples={round(t*24) for t in [25.75,26,26.208333,26.25,26.5,26.75,27,27.25,27.5,27.708333,27.75,28,28.5]}
thumbs=[];pts=[]
with av.open(str(DEST)) as c:
    for i,f in enumerate(c.decode(video=0)):
        pts.append(float(f.time))
        if i not in samples:continue
        im=f.to_image();im.save(frames/f'{i/24:06.3f}s.png')
        tile=Image.new('RGB',(320,205),(15,22,28));tile.paste(im.resize((320,180)),(0,25));ImageDraw.Draw(tile).text((8,3),f'{i/24:.3f}s',font=font,fill='white');thumbs.append(tile)
contact=Image.new('RGB',(1280,205*((len(thumbs)+3)//4)),(15,22,28))
for j,t in enumerate(thumbs):contact.paste(t,((j%4)*320,(j//4)*205))
contact.save(OUT/'jack_join_contact.jpg',quality=94)
assert len(pts)==1230 and max(abs(pts[j]-j/24) for j in range(len(pts)))<1e-5
assert source_hash=={str(p.relative_to(SB)):sha(p) for p in [BASE,RAW]}
dump(OUT/'edit_manifest.json',dict(film='C05',version=6,duration_seconds=51.25,fps=24,resolution=[1280,720],base_edit=str(BASE.relative_to(SB)),base_edl='2026-10-24_C05-causal-edit-v05/edit_manifest.json',replacement=dict(source=str(RAW.relative_to(SB)),source_in=1.5,source_out=3.0,timeline_in=26.25,timeline_out=27.75,crop=None),source_sha256=source_hash,caption_changes=None,audio='All base AAC packets, PTS and payloads preserved',purpose='Replace soft enlarged 384x216 insert with sharp original 1280x720 real jack movement',limitations=['Transport only; full stop, lifting and weight transfer not demonstrated','Existing partial turn/time ellipsis remains'],flow_credits_for_edit=0,originals_unchanged=True,review='PENDING',actual_listening_verified=False))
dump(OUT/'technical_validation.json',dict(file=DEST.name,sha256=sha(DEST),video_frames=len(pts),duration_seconds=51.25,full_decode='PASS',constant_video_pts=True,aac_packet_payloads_and_timestamps_identical=True,originals_unchanged=True))
print('DONE',DEST,sha(DEST))
