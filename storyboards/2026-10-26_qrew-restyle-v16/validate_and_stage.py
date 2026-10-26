from pathlib import Path
import json,re,hashlib,shutil,subprocess,sys
V=Path(__file__).resolve().parent; ROOT=V.parent.parent
helpers=V/'source_helpers';helpers.mkdir(exist_ok=True)
shutil.copy2(ROOT/'storyboards/2026-10-26_screening-style-v15/C03/render_c03_picture_v15.py',helpers/'render_c03_picture_v15.py')
(helpers/'README.md').write_text('C03 V15 UI compositor source snapshot, preserved byte-for-byte. The V16 group renderer reads only its safe prefix and redirects all output paths. Do not execute this historical helper as a standalone render.\n',encoding='utf8')
entry_names=['README.md','RESUME_CODEX.txt','00_완성_영상.md','00_V16_자막_음악_검토.md','07_셰프님_그것도_주세요.md','08_구조는_끝났습니다.md','09_나_없이도_괜찮겠어요.md']
docs=[ROOT/n for n in entry_names if n.endswith('.md')]+list((ROOT/'archive/v15-root-before-v16').glob('*.md'))+list(V.rglob('*.md'))
links=[];bad=[]
for p in docs:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  if target.startswith(('http:','https:','#','file:','mailto:')):continue
  target=target.split('#')[0].strip('<>')
  path=(p.parent/target).resolve();links.append([str(p.relative_to(ROOT)),target])
  if not path.exists():bad.append([str(p.relative_to(ROOT)),target])
assert not bad,bad
dm=json.loads((V/'delivery_manifest.json').read_text(encoding='utf8'));checked=[]
for f in dm['films']:
 p=V/f['path'];h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==f['sha256']
 q=json.loads((p.parent/'final_technical_qa.json').read_text(encoding='utf8'));assert q['pass']
 checked.append({'id':f['concept_id'],'sha256':h,'pass':True})
for p in V.rglob('*.json'):json.loads(p.read_text(encoding='utf8'))
report={'local_markdown_links_checked':len(links),'broken_links':bad,'final_video_hashes':checked,'json_parse_pass':True,'all_original_flow_files_unchanged':'source hashes checked by picture render QA','actual_listening':False,'realtime_continuous_playback':False}
(V/'delivery_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
full={'C02':'12.500s.png','C03':'27.000s.png','C04':'20.500s.png','C05':'027.500s.png','C06':'010.500s.png','C08':'027.500s.png','C09':'008.500s.png'}
files=[ROOT/n for n in entry_names]+list((ROOT/'archive/v15-root-before-v16').glob('*'))
for p in V.rglob('*'):
 if not p.is_file() or '__pycache__' in p.parts:continue
 if p.name.endswith('.pyc') or '_raw_v16.wav' in p.name or '_picture_v16.mp4' in p.name or 'stderr' in p.name:continue
 if 'review_frames' in p.parts and full.get(p.parent.parent.name)!=p.name:continue
 files.append(p)
assert all(p.stat().st_size<99*1024*1024 for p in files)
unique=sorted(set(str(p.relative_to(ROOT)).replace('\\','/') for p in files))
(V/'package_files.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
unique.append(str((V/'package_files.json').relative_to(ROOT)).replace('\\','/'))
print('Validated links',len(links),'deliverable files',len(unique),'MiB',round(sum((ROOT/p).stat().st_size for p in unique)/1024**2,1))
if '--stage' in sys.argv:
 safe='%(prefix)///wsl.localhost/Ubuntu-24.04/home/wooseok/wsy/samsung_related/slide/AI실행결과발표대회_디자인3종'
 for start in range(0,len(unique),30):
  subprocess.run(['git','-c','safe.directory='+safe,'add','--',*unique[start:start+30]],cwd=ROOT,check=True)
 print('Staged only V16 selected outputs and navigation')
