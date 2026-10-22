"""One-time archive navigation migration; media bytes remain unchanged."""
from pathlib import Path
from urllib.parse import unquote
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[2]
here=ROOT/'team/review-navigation'
moves=json.loads((here/'archive_moves.json').read_text(encoding='utf-8-sig'))
mapping={x['source_relative']:x['destination_relative']for x in moves}
for item in moves:
 p=ROOT/item['destination_relative']
 if item['kind']!='previous-guide':
  assert hashlib.sha256(p.read_bytes()).hexdigest().upper()==item['sha256'].upper()
  continue
 text=p.read_text(encoding='utf-8-sig')
 def replace(match):
  raw=match.group(1);target=raw.split('#',1)[0];suffix=('#'+raw.split('#',1)[1])if '#'in raw else''
  if not target or re.match(r'^[A-Za-z]+:',target)or target.startswith('/')or target.startswith('../../'):return match.group(0)
  if target=='콘티_바로보기.md' and p.name in ['README_before_v9.md','README_before_v10.md']:
   return ']('+('콘티_바로보기_V8.md'if p.name=='README_before_v9.md'else'콘티_바로보기_V9.md')+suffix+')'
  dst=mapping.get(target,target)
  if dst.startswith('archive/previous-guides/'):dst=dst[len('archive/previous-guides/'):]
  elif dst.startswith('archive/original-design/'):dst='../original-design/'+dst[len('archive/original-design/'):]
  elif (ROOT/target).exists():dst='../../'+target
  return ']('+dst+suffix+')'
 text=re.sub(r'\]\(([^)]+)\)',replace,text)
 p.write_text(text,encoding='utf8')
 item['archived_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
 item['change']='Only archive-relative navigation targets adjusted; narrative and images preserved'
(here/'archive_moves.json').write_text(json.dumps(moves,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for n in ['AGENTS.md','team/brief.toml']:
 p=ROOT/n;b=p.read_bytes()
 for src in ['AI실행결과발표대회_디자인3종.pptx','AI실행결과발표대회안.png']:
  old=('`'+src+'`'if n=='AGENTS.md'else'"'+src+'"').encode('utf8')
  new=('`archive/original-design/'+src+'`'if n=='AGENTS.md'else'"archive/original-design/'+src+'"').encode('utf8')
  assert b.count(old)==1,(n,src,b.count(old));b=b.replace(old,new)
 p.write_bytes(b)
archive='''# 이전 자료 보관

[최신 10안 검수로 돌아가기](../README.md)

현재 검수에는 루트의 **01–10번 스토리보드**만 보면 됩니다. 아래 자료는 이전 기획·작업 이력과 원자료입니다.

| 보관 자료 | 위치 |
|---|---|
| 초기 행사 장표·원안 PNG·PPTX | [original-design](original-design/) |
| 초기 장표 3종 미리보기 HTML | [index.html](original-design/index.html) |
| 이전 README와 V8/V9 이미지 콘티 | [previous-guides](previous-guides/) |
| 이전 콘티·Flow 원본·편집 영상·검수 기록 | [storyboards](../storyboards/) |
| 예전 Flow 업로드 패키지 | [flow_handoff](../flow_handoff/) |

초기 PNG·PPTX·HTML은 내용과 바이트를 바꾸지 않고 함께 옮겼습니다. 보관한 안내 문서는 상대 링크만 새 위치에 맞췄습니다. `storyboards/`의 기존 폴더와 영상 파일은 내부 연결을 보존하기 위해 기존 경로를 유지합니다.
'''
(ROOT/'archive/README.md').write_text(archive,encoding='utf8')
resume=ROOT/'RESUME_CODEX.txt';old=resume.read_bytes()
prefix='''[2026-10-23 Git 메인 검수용 정리 — V10 내용·이미지 불변]
사용자 요청: Git에서 검수하도록 이전 파일을 정리하고 최신 스토리보드 파일들을 메인에 배치. 루트 README.md가 검수 시작점, 01_성공_자세_교정원.md부터 10_개막을_허가하지_않는_기계.md까지 안별10문서에 모든88시작상태/자막정지예시/행동/자막시간/음향/전환 포함. 콘티_바로보기.md 최신88이미지 유지.
구형 README_before_v8/v9/v10 및 콘티_V8/V9는 archive/previous-guides/. 초기 디자인 PNG/PPTX/원안/index.html은 archive/original-design/로 바이트불변 이동. AGENTS.md와 team/brief.toml의 원자료2경로 갱신. storyboards/와 flow_handoff/는 경로 유지, 기존 완성영상/원본 불변.
최신 제작명세는 여전히 storyboards/2026-10-23_v10-ten-concepts/storyboards.json 및 scene_manifest.json. 루트 검수문서 갱신은 team/review-navigation/build_root_reviews.py 사용. V10 finish_package.py는 이전루트배치를 다시 만드는 이력스크립트이므로 재실행금지. 이번 작업은 파일정리·검수문서작성·Git반영만, Flow/영상/음원/이미지새생성/크레딧사용0. 예약PAUSED유지. 이동/링크 검증은 team/review-navigation/ 기록.

'''
resume.write_bytes(prefix.replace('\n','\r\n').encode('utf8')+old)
p=ROOT/'storyboards/2026-10-23_v10-ten-concepts/README.md'
intro='**최신 검수 시작점: [저장소 메인의 01–10번 안별 스토리보드](../../README.md).** 이 폴더는 제작 원본과 검수 이력 보관용입니다.\n\n'
p.write_text(intro+p.read_text(encoding='utf8'),encoding='utf8')
p=ROOT/'storyboards/2026-10-23_v10-ten-concepts/finish_package.py';text=p.read_text(encoding='utf8')
needle='R=Path(__file__).resolve().parent;ROOT=R.parents[1]'
text=text.replace(needle,needle+'\nif (ROOT/"team/review-navigation/root_review_manifest.json").exists():\n    raise SystemExit("Historical layout script: use team/review-navigation/build_root_reviews.py for the current review-first root.")')
p.write_text(text,encoding='utf8')
print('Archived guide links, operating source paths, archive index and resume updated')
