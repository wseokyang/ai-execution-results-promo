"""Run only after final image review. Preserve prior deliveries and history bytes."""
from pathlib import Path
import json,shutil,re,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parents[1]
d=json.loads((R/'storyboards.json').read_text(encoding='utf8'))
v=json.loads((R/'validation.json').read_text(encoding='utf8'))
review=json.loads((R/'review_summary.json').read_text(encoding='utf8'))
assert review.get('ready_for_user_selection')is True
assert v['concept_count']==10 and len(v['images'])==88
for src,dst in [('README.md','README_before_v10.md'),('콘티_바로보기.md','콘티_바로보기_V9.md')]:
    target=ROOT/dst
    if not target.exists():shutil.copy2(ROOT/src,target)
base='storyboards/'+R.name
overview=(R/'ALL_IMAGES.md').read_text(encoding='utf8')
for rel in ['images/','STORYBOARDS.md','index.html','CASTING.md','review_summary.json']:
    overview=overview.replace(']('+rel,']('+base+'/'+rel)
(ROOT/'콘티_바로보기.md').write_text(overview,encoding='utf8')
rows=['# Q-AI Fair · 10안 선택용 콘티 V10','','**기존 1–5안 보완 + 신규 6–10안**입니다. 화면과 후처리 자막으로 이야기를 전달합니다. 새5안의 시작 PNG44장을 실제 생성했고, 내용에 맞는 기존44장을 재사용했습니다. 이전 영상과 원본은 보존했습니다.','','## [전체 88장 이미지 콘티 바로보기 →](콘티_바로보기.md)','','![10안 한눈에 보기]('+base+'/overview_10.jpg)','','| 안 | 제목 | 편집 길이 | 시작 이미지 |','|---|---|---:|---:|']
for c in d['concepts']:
    n=sum(u['concept_id']==c['id']for u in d['generation_units'])
    rows.append(f'| {c["id"]} | [{c["title"]}]({base}/ALL_IMAGES.md#{c["id"].lower()}) | {c["duration_seconds"]}초 | {n}장 |')
rows+=['','| 찾는 자료 | 링크 |','|---|---|',f'| 전체 컷 표·음향·전환 | [10안 STORYBOARDS]({base}/STORYBOARDS.md) |',f'| 이미지와 자막 배치 버튼 | [HTML 전체]({base}/index.html) · [Git에서 전체 이미지 읽기]({base}/ALL_IMAGES.md) |',f'| 실제 PNG·정확 생성 기록 | [이미지]({base}/images/) · [scene_manifest]({base}/scene_manifest.json) |',f'| 외형 다양화·검수 | [캐스팅]({base}/CASTING.md) · [3인 교차 검수]({base}/review_summary.json) |',f'| 제작 준비와 기존 합성 항목 | [제작 메모]({base}/PRODUCTION_NOTES.md) · [제작 단위]({base}/production_units.tsv) |','| 기존 C03 검토 편집 | [C03 v03 44.75초](storyboards/2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4) |','| 이전 완성 1번 영상 | [C01 36초 최종 MP4](storyboards/2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4) |','| 보존한 이전 안내 | [V9 전체 이미지](콘티_바로보기_V9.md) · [V9 README](README_before_v10.md) · [V8 전체 이미지](콘티_바로보기_V8.md) |','','HTML은 이미지 폴더와 함께 내려받아 여세요. GitHub에서는 전체 이미지 문서를 바로 읽을 수 있습니다. 최신 기준은 V10의 storyboards.json과 scene_manifest.json입니다. 초안·수정 스크립트는 이력으로 보존합니다.','','**이번 Flow 요청·크레딧 사용·영상·음원 생성은0입니다.** 사용자가 안을 고른 뒤 실제 계정 잔액과 모델 비용을 확인합니다. 시작 이미지 수는 성공 영상 수나 필요한 크레딧 수가 아닙니다. 기존 C03은 원본 재사용을 우선합니다. 모든 자막과 정확한 글은 후편집하며 실제 영상 동작·상영 가독성은 생성·편집 후 확인합니다. 행사 날짜·장소·참석 방법은 미확인입니다.']
(ROOT/'README.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
resume=ROOT/'RESUME_CODEX.txt';old=resume.read_bytes()
marker='[2026-10-23 Q-AI Fair V10 — 기존5보완+새5/총10안/시작88장]'
if marker.encode('utf8')not in old:
    prefix=marker+'\r\n최신사용자: Flow영상에자막생성금지, 모든자막후처리. 기존1~5내용보완+신규5추가하여총10안중선택, 캐릭터외형다양화, 돌고래유괴단식장르진정성/인물선택/반전/후폭풍을선호. 현재Flow·영상·음원·크레딧사용0, 예약PAUSED유지. 선택전자동영상생성금지.\r\n최신명세 '+base+'/storyboards.json 및 scene_manifest.json. 편집87컷/시작88상태. 기존C01~05는37.5/39/44.75/37/43초, 신규C06퇴근좀해주세요44초9장/C07결투시간을뺏긴여자43초9장/C08이오페라는끝났습니다41초8장/C09지구인은질문이많다45초9장/C10개막을허가하지않는기계46초9장. 새44PNG내장image_gen실제생성+기존V9선택44바이트재사용. 새캐스트는기본얼굴반복없이얼굴·머리·체형·복장·연기구분. 원본C01/C03v03/V9보존.\r\n텍스트3인독립/교차/수정3재확인 및 실제이미지검수는 review_summary.json,image_review.json 기준. 모든자막/행사명/정확문서는후편집, 소음환경화면+자막전달. 실제움직임·최종합성·관객반응까지완료한것아님. Flow초안은선택뒤입력프레임/잔액/비용/복잡도재확인, 기존C03원본재사용우선.\r\n사용자보기: 콘티_바로보기.md(전체88이미지), V10/index.html(자막버튼/후보표시), STORYBOARDS.md/CASTING.md/PD_DECISIONS.md/PRODUCTION_NOTES.md. Windows미리보기 C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v10-2026-10-23/index.html. 이전V9안내는README_before_v10.md/콘티_바로보기_V9.md보존. Git동기화는실제remote확인후보고.\r\n\r\n'
    resume.write_bytes(prefix.encode('utf8')+old)
brief=ROOT/'team/brief.toml';old=brief.read_bytes()
if b'[ten_concepts_v10_2026_10_23]'not in old:
    appendix='\r\n[ten_concepts_v10_2026_10_23]\r\nuser_request = "기존5보완+새5추가,총10안선택.화면+후처리자막,캐릭터외형다양,진지한장르와행동반전.이번영상생성없음."\r\nrun = "'+base+'"\r\ncounts = "87편집컷/88시작상태;신규44+V9재사용44.9/9/8/9/9/9/9/8/9/9."\r\ndurations = "37.5/39/44.75/37/43/44/43/41/45/46초"\r\nstatus = "10안선택용콘티/실제첫이미지/3인검수완료;세부상태review_summary.json기준.실제영상움직임과관객반응미검증."\r\nscope = "Flow/영상/음원/크레딧0.선택전영상생성없음.기존C01완성본/C03v03/원자료보존.예약PAUSED."\r\n'
    brief.write_bytes(old+appendix.encode('utf8'))
dest=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v10-2026-10-23')
shutil.copytree(R,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
print('Finished root navigation, history and Windows gallery:',dest)
