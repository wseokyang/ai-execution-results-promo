from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[2];V=Path(__file__).resolve().parent
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
files=[s.decode('utf-8') for s in git('diff','--cached','--name-only','--diff-filter=ACMR','-z').split(b'\0') if s]
sizes=sorted([(p,(ROOT/p).stat().st_size) for p in files],key=lambda x:x[1],reverse=True)
forbidden=[p for p in files if any(x in p for x in ['/review_frames/','/foreground_masks/','Zone.Identifier','flow_completed','/__pycache__/']) or p.lower().endswith('.wav') or '/2026-10-25_final-six-v13/C05/' in '/'+p or '/2026-10-25_final-six-v13/C05_r2/' in '/'+p]
large=[p for p,n in sizes if n>=100*1024*1024]
unrelated=[p for p in files if '/' in p and not p.startswith(('storyboards/2026-10-25_final-six-v13/','storyboards/2026-10-25_C07-C10-rewrite-v13/','archive/v12-before-final-v13/'))]
mp4=[p for p in files if p.endswith('.mp4')]
errors=[]
if forbidden:errors.append({'forbidden':forbidden})
if large:errors.append({'too_large':large})
if unrelated:errors.append({'unrelated':unrelated})
if len(mp4)!=18:errors.append({'unexpected_mp4_count':len(mp4)})
print(json.dumps({'staged_added_modified':len(files),'mp4_count':len(mp4),'total_MiB':round(sum(n for _,n in sizes)/1048576,1),'largest_file':sizes[0],'forbidden':len(forbidden),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
