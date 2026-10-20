"""Review-only editorial alternative. Source MP4s remain byte-identical."""
from pathlib import Path
import subprocess
import json
import hashlib

root = Path(__file__).resolve().parent
storyboards = root.parent
ff = storyboards / '2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
sources = [storyboards / '2026-10-19_C03-flow-run01/C03_K03_take01.mp4',
           root / 'C03_K03_insert_take02.mp4',
           storyboards / '2026-10-20_C03-flow-run03/C03_K04_take02.mp4',
           root / 'C03_K04_insert_take04.mp4']
output = root / 'C03_K03_K04_state_edit_review_7p5s.mp4'
before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
graph = (
    '[0:v]trim=start=0:end=2.5,setpts=PTS-STARTPTS[v0];'
    '[1:v]trim=start=6:end=6.75,setpts=PTS-STARTPTS[v1];'
    '[2:v]trim=start=0:end=3.5,setpts=PTS-STARTPTS[v2];'
    '[3:v]trim=start=6:end=6.75,setpts=PTS-STARTPTS[v3];'
    '[v0][v1][v2][v3]concat=n=4:v=1:a=0,format=yuv420p[v];'
    '[0:a]atrim=start=0:end=3.25,asetpts=PTS-STARTPTS,aresample=48000[a0];'
    '[2:a]atrim=start=0:end=4.25,asetpts=PTS-STARTPTS,aresample=48000,volume=0.7[a2];'
    '[a0][a2]concat=n=2:v=0:a=1[a]'
)
command = [str(ff), '-y', '-v', 'error']
for source in sources:
    command += ['-i', str(source)]
command += ['-filter_complex', graph, '-map', '[v]', '-map', '[a]',
            '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-r', '24',
            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(output)]
subprocess.run(command, check=True)
subprocess.run([str(ff), '-v', 'error', '-i', str(output), '-f', 'null', '-'],
               capture_output=True, check=True)
assert before == {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
record = {
    'status': 'review-only editorial alternative, not final adoption',
    'output': output.name, 'nominal_duration_seconds': 7.5,
    'video_timeline': [
        {'at': 0, 'source': str(sources[0]), 'in': 0, 'out': 2.5},
        {'at': 2.5, 'source': str(sources[1]), 'in': 6, 'out': 6.75},
        {'at': 3.25, 'source': str(sources[2]), 'in': 0, 'out': 3.5},
        {'at': 6.75, 'source': str(sources[3]), 'in': 6, 'out': 6.75}],
    'audio': 'Existing K03 0-3.25s then existing K04 0-4.25s. K04 gain0.7 to allow decoder peak headroom. No new insert audio, BGM or voice synthesis.',
    'action_change': 'Omit removal/wearing mechanics; show completed states across hard cuts. Does not claim either generated action succeeded.',
    'original_sha256': before, 'originals_unchanged': True,
    'render_full_decode_pass': True,
    'limitations': ['Actual audio listening and continuous playback review not done by this script.',
                   'C03 full film and graphic overlays remain unfinished.',
                   'Prior K03 ASR includes 정확히 같이 나오네요; preserved original phrase, not newly synthesized.']
}
(root / 'edit_manifest.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(output, flush=True)
