"""Publish local review package and repository navigation; never posts publicly."""
from pathlib import Path
import json, shutil, hashlib, html
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
WIN=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-C05-C06-edits-2026-10-23')
WIN.mkdir(parents=True,exist_ok=True)
clips={'C05':('괴수는 퇴근할 수 없다','C05_Q-AI_Fair_edit_v02.mp4',38.5),'C06':('퇴근 좀 해주세요','C06_Q-AI_Fair_edit_v03.mp4',50)}
cards=[]; copied=[]
for c,(title,name,duration) in clips.items():
 src=OUT/c/name; dst=WIN/name; shutil.copy2(src,dst)
 digest=hashlib.sha256(src.read_bytes()).hexdigest()
 assert digest==hashlib.sha256(dst.read_bytes()).hexdigest()
 technical=json.loads((OUT/c/'technical_validation.json').read_text(encoding='utf-8'))
 assert technical['sha256']==digest
 copied.append(dict(film=c,file=name,local_path=str(dst),sha256=digest,bytes=dst.stat().st_size))
 poster_src=OUT/c/'review_frames'/('28.500s.png' if c=='C05' else '00.500s.png')
 shutil.copy2(poster_src,WIN/f'{c}_poster.png')
 cards.append(f'<section><h2>{c[1:]} · {html.escape(title)}</h2><p>{duration:g}초 · 720p · 자막·BGM·효과음 포함</p><video controls preload="metadata" poster="{c}_poster.png" src="{name}"></video><p><a href="{name}" download>편집본 MP4 저장</a></p></section>')
viewer='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair · 5번·6번 편집본</title><style>body{margin:0;background:#0b121b;color:#f5f8fa;font:18px/1.65 "Malgun Gothic",sans-serif}main{max-width:1160px;margin:48px auto;padding:0 24px}h1{font-size:40px;letter-spacing:-1.2px}p{color:#b5c7d1}section{margin:40px 0 64px}video{display:block;width:100%;border-radius:14px;background:#000;box-shadow:0 14px 60px #0007}a{color:#8ce6d4}small{color:#9dafbb}</style><main><h1>Q-AI Fair · 5번·6번 편집본</h1><p>화면과 자막으로 내용을 전달합니다. 음악·효과음은 보조입니다.</p>'''+''.join(cards)+'''<small>Flow 동작 원본을 편집한 별도 파일입니다. 기존 원본은 보존했습니다.</small></main></html>'''
(WIN/'index.html').write_text(viewer,encoding='utf-8')
(OUT/'delivery_manifest.json').write_text(json.dumps(dict(files=copied,viewer=str(WIN/'index.html')),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
ignore='**/review_frames/\ncomposite_previews/\n**/*_picture.mp4\n**/*_mix.wav\n**/*_score.wav\n**/render_stderr.txt\ndrafts/\n'
for ver in ('v01','v02','v03'):
 folder=OUT.parent/f'2026-10-23_C05-C06-edit-{ver}'
 (folder/'.gitignore').write_text(ignore+('**/*.mp4\n' if ver!='v03' else ''),encoding='utf-8')
for c in clips:
 p=OUT/c/'edit_manifest.json'; data=json.loads(p.read_text(encoding='utf-8'))
 data['status']='Edited delivery; three independent and cross visual sample reviews completed. Not user final approval.'
 data['continuous_playback_or_listening_verified']=False
 if c=='C05': data['package_note']='C05 final v02 bytes copied unchanged into delivery package v03.'
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(copied,ensure_ascii=False,indent=2))
