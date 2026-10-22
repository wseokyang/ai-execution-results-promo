"""Record the actual completed three-reviewer reconfirmation and current handoff."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;ROOT=R.parents[1]
def read(p):return json.loads(p.read_text(encoding='utf8'))
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
resolved=['FA-001','FA-002','FA-003','FA-004','FB-001','FB-002','FB-003','FB-004','FB-005','FC-001','FC-002','FC-003','FC-004','FC-005','FC-006','PD-001','PD-002']
scoped=['C08 차광 실제 영상/합성','C09 한 팔 호출·동일 종이 이동','C05 A→B 실제 종료·시작 연결','C07 자발적 이동·다시 가림','C10 두 가위 반응·점프/착지','움직이는 화면의 자막 가림·무음 전체재생·상영 크기 가독성']
proofs=['post_assets/C08_process.png','post_assets/C08_light_path_plan.png','caption_proofs/C07_captions.jpg','caption_proofs/C07_K04_cue1.jpg','caption_proofs/C06_K09_cue1.jpg','caption_proofs/C08_K08_cue1.jpg']
reviewers={}
for key,agent in [('A','final_review_a'),('B','v10_review_b'),('C','v10_review_c')]:
 reviewers[key]={'agent':agent,'verdict':'제작 전 명세 검수 종결 가능. 선택 작품 제작 착수 권장. 남은 필수 명세 수정 없음.','resolved_or_production_specification_resolved':resolved,'suggestion_not_applied':['FA-005: C07 K02~03 추가단축은 제안으로 남김. K04~06 4초 단축 후 필요하지 않음.'],'actual_additional_images_opened':proofs+(['caption_proofs/C07_K05_cue1.jpg'] if key=='C' else []),'reconfirmation_rounds':'V11 재확인에서 FC005/006·FB005를 추가 발견하고 국소 수정 후 실제 파일 재확인까지 완료','unresolved_mandatory':[],'not_claimed':['actual moving video review','actual composited C08 success','audience testing','contest eligibility']}
reviewers['B']['extra_checks']='70개 자막 사본 일치,87컷 시간,88유닛 사용시간,전체88프롬프트 행동·카메라 필드 대조.'
reviewers['A']['extra_checks']='88선택PNG SHA256 V10일치 확인, 수정C05A/B프롬프트·유닛·manifest 추가 재확인.'
reviewers['C']['extra_checks']='88선택PNG SHA256 V10일치 확인, 새지적FC005/006 및 FB005 최종재확인.'
summary={'run_id':R.name,'status':'PREPRODUCTION_REVIEW_COMPLETE; VIDEO_PRODUCTION_NOT_STARTED','record_type':'Faithful summaries of actual agent replies, not verbatim transcripts.','stages':['same comprehensive brief','three independent reviews of all10 concepts/87shots/88 selected states','cross-review after first submissions','V11 specification edits and proof rendering','three reconfirmations','additional FC005/006 and FB005 fixed; all three reconfirmed'],'independent_record':'independent_reviews.json','cross_record':'cross_reviews.json','pd_record':'PD_DECISIONS.md','reviewers':reviewers,'remaining_mandatory_preproduction_issues':[],'planned_video_acceptance_checks':scoped,'new_keyframe_images':0,'selected_start_images_reused_from_v10':88,'code_rendered_postproduction_diagrams':['post_assets/C08_process.svg','post_assets/C08_process.png','post_assets/C08_light_path_plan.png'],'new_flow_requests':0,'new_credits_used':0,'new_video_audio_files':0,'duration_seconds':{c['id']:c['duration_seconds'] for c in read(R/'storyboards.json')['concepts']},'limitations':'정지 이미지·명세의 제작 준비 검토. 실제 동작·합성·음성·립싱크·최종 재생·관객 반응·출품 규정 검증 아님. C08 그림은 계획도. BGM/SFX는 역할만 명세했으며 특정 음원을 선정/청취/라이선스 확인하지 않음.','evidence_scope':'원자료 PPTX1~3 텍스트와 기존자료/레퍼런스분석을 읽고 해당 행사근거 확인. qrew/광고 전체영상이나 음원을 이번에 감상했다고 주장하지 않음.','recommendations':{'overall':'C06','live_opening':'C10','strong_visual_alternatives':['C01','C05'],'first_motion_check_required_before_full_batch':['C08','C09']}}
put(R/'review_summary.json',summary)
d=read(R/'storyboards.json');d['status']='V11 final pre-production review complete; user selection precedes Flow; no video generated'
for u in d['generation_units']:u['status']='V11 preproduction specification reviewed; NOT_SUBMITTED_TO_FLOW'
put(R/'storyboards.json',d)
m=read(R/'scene_manifest.json');m['status']='V11 final pre-production review complete;88 V10 starts reused; no Flow submissions'
for e in m['images']:e['review_status']='V11 three-reviewer preproduction reconfirmation complete; moving-video acceptance pending'
put(R/'scene_manifest.json',m)

brief='''# V11 최종 검토 공통 브리프

사용자 요청: “대회 나가는 거라고 생각하고 신중히 한번 더 검토. 이번 검토 뒤 제작 시작.” 현재10안 전체가 대상이다. 기존 콘셉트와 서로 다른 캐스트를 유지하면서 구체적인 약점만 고친다. 별도 출품 규정은 제공되지 않았다.

- Q-AI Fair, 화면+후처리 자막 중심. 음성 없이 사건과 행사 연결을 이해할 수 있어야 한다. BGM·효과음은 보조다.
- 과장된 장르를 진짜처럼 연출하고, 인물의 선택→상황 확대→반전→후폭풍이 있어야 한다. 이상한 소품만 놓는 기업 홍보를 통과시키지 않는다.
- 전10안의 첫 훅·웃음·목표/인과·행사 전달·차별성·사내 수용성·시간/자막·연속성·제작 가능성을 세 검수자가 동일 범위로 본다. 전문분야를 쪼개지 않는다.
- 행사명은 사용자 확정. 일정·장소·신청·실적·상금은 새로 만들지 않는다. 전체60초 이내, 행사명 읽기 시간을 확보한다.
- 독립 의견을 먼저 받은 뒤 교차 전달. 실제 PNG/자막 정지 예시를 열고 확인한다. 실제 동작·합성·관객 반응까지 검증했다고 쓰지 않는다.
- 원본 C01완성/C03영상/V10 자료를 보존한다. 재생성할 구체적 시작 상태 결함이 없으면88PNG 재사용. Flow/영상/음원/크레딧 사용은 이번 범위가 아니다.

근거: AGENTS.md, team/brief.toml 최신지시, RESUME_CODEX.txt, V10 storyboards/manifest/검수/제작 메모, 원자료 PPTX1~3 텍스트, 기존 qrew reference-v5 및 reference-v7-v8 분석. 새 영상 감상/실제 음원 청취/신규 플랫폼 기능 확인으로 확대 해석하지 않는다.
'''
(R/'BRIEF.md').write_text(brief,encoding='utf8')

resume=ROOT/'RESUME_CODEX.txt';t=resume.read_text(encoding='utf8')
head='''[2026-10-23 Q-AI Fair V11 — 10안 최종 제작 전 검토 완료]
최신 사용자: 대회 출품작 수준으로 신중한 최종검토, 검토 뒤 제작 시작 예정. 현재 작업은10안 최종검토·국소수정·Git반영까지이며 Flow/새시작이미지/동영상/음원/크레딧사용0. 사용자 선택 전 전체88단위 자동생성하지 않고 예약PAUSED유지.
최신명세 storyboards/2026-10-23_v11-production-lock/storyboards.json 및 scene_manifest.json. 루트00_제작전_최종검토.md에 수정·추천·안별리스크, 루트01~10 안별이미지콘티 및 콘티_바로보기.md가 V11. 기존V10전체 및 C01완성/C03기존영상 보존. 선택PNG88 바이트불변 재사용, 새그림은 코드로 만든 C08 후합성 도해/설계도일 뿐 새시작이미지나 실제영상 아님.
3명 각10안87컷/88시작상태/자막 독립→상호교차→V11수정→실제파일재확인. 재확인 중FC005(C07줄낙하지점자막가림),FC006(C09K04/05중복팔출발),FB005(C05A종료몸접기잘못승계) 추가발견·수정후3명재확인,남은필수명세문제0. review_summary.json/independent_reviews.json/cross_reviews.json/PD_DECISIONS.md 참조. 실제동영상·합성·현장가독성·관객반응·출품규정 검증은 아님.
주요변경: 자막사본24불일치와엔딩구도3곳 동기화; C07중반3/3/4초로전체39초/K04자막중앙하늘/Q1질문으로동행인과; C08관심회복동기+같은도해/천상승→천뒤광선·반사함께감소/선명1초; C09손바닥호출/K04끝0.4초두팔정지→K05즉시L한번/K09사용8초로총44초; C10접착과정생략·붙은가위한번들기유지; C05 A3+B4와유닛별연속성 분리.
길이 C01~C10=37.5/39/44.75/37/43/44/39/41/44/46초. 시작단위9/9/8/9/9/9/9/8/9/9=88, 편집87컷. 총괄추천 종합C06/현장개막C10, 시각강점C01/C05. C07상대적으로잔잔, C08차광 실제동작 먼저확인. 선택작품핵심동작부터 제작하며 C03기존원본재사용 우선.
flow_prompts88개는 미제출초안. 모든자막/행사명/정확문서후처리, 무음전달중심, 현재8초소스계획이며실제요청직전모델/비용/길이확인. 역사적imageprompt의구자막지시재사용금지. C05B는채택A실제끝프레임우선. root generator team/review-navigation/build_root_reviews.py는V11기준. 과거V10finish_package.py 재실행금지. Git동기화는실제remote확인후보고.

'''
if not t.startswith('[2026-10-23 Q-AI Fair V11'):resume.write_text(head+t,encoding='utf8')
print('Recorded all three final reconfirmations and updated current handoff.')
