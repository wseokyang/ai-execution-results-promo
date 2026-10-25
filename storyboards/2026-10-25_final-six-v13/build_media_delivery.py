from pathlib import Path
import json,shutil,html,hashlib
ROOT=Path(__file__).resolve().parents[2];V=Path(__file__).resolve().parent
CACHE=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-final-six-v13-2026-10-25')
CACHE.mkdir(parents=True,exist_ok=True)
titles=['성공 자세 교정원','검은 점을 잡아라','환경까지 가져왔습니다','목마는 식사 중입니다','괴수는 퇴근할 수 없다','퇴근 좀 해주세요']
notes=['모니터·포스터에 같은 실영상 인물을 합성. 실제 퇴장→눕기→따라 하는 포즈로 연결.','제품 사진의 같은 검은 점·청소 전후와 두 수갑의 짧은 사슬, 촬영 사진을 맞춤.','장갑 확인 구간을 줄이고 겹치던 자막을 정리. 무음 영상.','쪽지 완전 투입·문서 합성·세 창문 열림·한 숟가락 추출 연결.','목 걸림→목 빼기→잭 운반→받침. 괴수 변형 테이크는 제외. 회전·손 이동은 컷어웨이 동안 시간 생략이며 연속 동작 촬영은 아님.','책상 첫 타격만 사용하고 효과음 시점을 손 접촉에 맞춤.']
films=[]
previous=json.loads((V/'delivery_manifest.json').read_text(encoding='utf-8-sig')) if (V/'delivery_manifest.json').exists() else {}
for i,title in enumerate(titles,1):
 cid=f'C{i:02}';folder=cid+('_r3' if i==5 else '')
 p=V/folder/f'{cid}_Q-AI_Fair_final_v13.mp4'
 t=json.loads((p.parent/'technical_validation.json').read_text(encoding='utf-8-sig'))
 if 'duration_seconds' not in t:t['duration_seconds']=t['duration']
 dst=CACHE/p.name;shutil.copy2(p,dst)
 assert hashlib.sha256(dst.read_bytes()).hexdigest()==hashlib.sha256(p.read_bytes()).hexdigest()
 films.append({'concept_id':cid,'title':title,'file':str(p.relative_to(V)).replace('\\','/'),'preview_copy':str(dst),'duration_seconds':t['duration_seconds'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'note':notes[i-1],'review_status':'final sample review in progress','audio_listening_verified':False})
for f in films:
 old=next((x for x in previous.get('films',[]) if x['concept_id']==f['concept_id'] and x['sha256']==f['sha256']),None)
 if old:f['review_status']=old['review_status']
same=bool(previous.get('films')) and all(any(x['concept_id']==f['concept_id'] and x['sha256']==f['sha256'] for x in previous['films']) for f in films)
(V/'delivery_manifest.json').write_text(json.dumps({'films':films,'raw_generation_log':'generation_log.json','status':previous.get('status','FINAL_QA_PENDING') if same else 'FINAL_QA_PENDING'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
css='body{margin:0;background:#10151c;color:#e8eef5;font:16px/1.6 system-ui,sans-serif}main{max-width:1150px;margin:auto;padding:32px 20px}h1{font-size:32px}h2{font-size:24px}a{color:#72dbd0}nav{display:flex;gap:20px;flex-wrap:wrap}article{margin:30px 0 48px;padding:24px;background:#1b2530;border-radius:16px}video{width:100%;background:#000}small,.muted{color:#b3c1cf}.tag{padding:3px 10px;border-radius:20px;background:#30465a}.notice{border-left:3px solid #eab86d;padding:10px 16px;background:#26313d}'
items=[]
for f in films:
 items.append(f'<article id="{f["concept_id"]}"><h2>{f["concept_id"]} · {html.escape(f["title"])}</h2><p><span class="tag">{f["duration_seconds"]:g}초</span> 1280 × 720 · 24fps</p><video controls preload="metadata" playsinline src="{f["concept_id"]}_Q-AI_Fair_final_v13.mp4"></video><p>{html.escape(f["note"])}</p><a download href="{f["concept_id"]}_Q-AI_Fair_final_v13.mp4">편집 MP4 내려받기</a></article>')
page='<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair · 1–6 최종 편집 V13</title><style>'+css+'</style><main><h1>Q-AI Fair · 1–6편</h1><p>2026-10-25 V13 · 화면과 자막 중심 · 필수 음성 대사 없음</p><nav>'+''.join(f'<a href="#{f["concept_id"]}">{f["concept_id"]}</a>' for f in films)+'<a href="originals.html">추가 생성 원본 12개</a><a href="storyboards.html">새 7–10 콘티</a></nav><p class="notice">최종 프레임·장면 접합·자막과 전체 파일 디코딩 검수. 실제 청취와 현장 상영 테스트는 확인하지 않았습니다. C03은 무음이며 나머지는 배경음악·효과음이 있습니다.</p>'+''.join(items)+'</main></html>'
(CACHE/'index.html').write_text(page,encoding='utf-8')
g=json.loads((V/'generation_log.json').read_text(encoding='utf-8-sig'))
rawdir=CACHE/'originals';rawdir.mkdir(exist_ok=True)
rawitems=[]
for e in g['entries']:
 src=V/e['original'];dst=rawdir/src.name;shutil.copy2(src,dst)
 assert hashlib.sha256(dst.read_bytes()).hexdigest()==e['sha256']
 note=e['review']['note'] if isinstance(e['review'],dict) else str(e['review'])
 rawitems.append(f'<article><h2>{html.escape(e["original"])}</h2><p>{e["status"]} · {e["model"]} · {e["cost_displayed"]}크레딧</p><video controls preload="none" src="originals/{src.name}"></video><p>{html.escape(note)}</p><a download href="originals/{src.name}">재인코딩하지 않은 원본 MP4</a></article>')
(CACHE/'originals.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><title>Flow 원본 12개</title><style>'+css+'</style><main><h1>Flow 추가 생성 원본 12개</h1><p><a href="index.html">6편 편집본으로</a> · 채택6 / 보류6 · 200크레딧 사용</p><p>보류 원본은 최종본에 사용하지 않았습니다. 원본 음성은 청취 검증하지 않았으며 최종편집에서 제거했습니다.</p>'+''.join(rawitems)+'</main></html>',encoding='utf-8')
print('Copied6finals+12unchangedoriginals. Cache:',CACHE)
