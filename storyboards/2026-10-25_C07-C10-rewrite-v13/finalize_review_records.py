from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=ROOT/'storyboards/2026-10-25_final-six-v13'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
agents=['/root/causal_review_a','/root/causal_review_b','/root/v13_review_c']
fixed=['images/C10/S02_v4.png','images/C10/S03_v3.png','images/C10/S04_v3.png','images/C10/S05_v2.png','images/C10/S06_v2.png','caption_previews/C10_S10_caption_layout_v2.png']
review={'status':'PASS_WITH_DOCUMENTED_FUTURE_VIDEO_CHECKS','scope':'PD digest of completed actual three-agent image independent review, cross review, local corrections, and final reconfirmation. Not verbatim transcript.','reviewers':agents,'independent_image_count_per_reviewer':40,'independent_contact_count_per_reviewer':4,'cross_review_completed':True,'final_reconfirmation':{a:'PASS: final front-curtain corrections and exact Q-AI Fair caption proof opened; previous 40-image decisions retained.' for a in agents},'fixed_files':[{'file':f,'sha256':hashlib.sha256((P/f).read_bytes()).hexdigest()} for f in fixed],'dispositions':[{'issues':['IA001','IB001','IC001'],'status':'RESOLVED','treatment':'S02-S04 all workbench feet placed inside turntable with rear rim behind.'},{'issues':['IA002','IB002','IC002'],'status':'RESOLVED','treatment':'S05-S06 remove curtain below lower bar and separate free-bar grip from vertical pole.'},{'issues':['IA005','IB002-front','IC004'],'status':'RESOLVED','treatment':'S02_v4/S03_v3/S04_v3 remove all pleated fabric below diagonal bar and beyond high hand.'},{'issues':['IA003','IB005','IC003','IB006'],'status':'RESOLVED_POST_LAYOUT','treatment':'Actual upper-left three-line caption proof v2 with exact Q-AI Fair; no face/hand/white-gap overlap.'},{'issues':['IA004','IB004'],'status':'OPTIONAL_ACCEPTED_BY_PD','treatment':'C09 ribbon changes attachment near handle; same grey suitcase/yellow identifier and charger payoff remain readable.'},{'issues':['IB003'],'status':'FUTURE_VIDEO_CHECK','treatment':'C10 actual knee bend/arm lowering must retain face above fixed top while fully covering white gap. Not verified by stills.'}],'unresolved_required_image_findings':[],'flow_executed_for_C07_C10':False,'not_verified':['Actual turning/hand-off/lowering motion','Final video compositing and realtime playback','Human listening and venue readability','Audience laughter/user acceptance'],'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
save(P/'reviews/final_image_review.json',review)
t=read(P/'reviews/text_final_review.json')
for e in t['dispositions']:e['status']='TEXT_RECONFIRMED; MOTION_REMAINS_TO_BE_GENERATED'
t['final_changes']='REV03_BAR rigid lower hem and subsequent external caller badge/title placement confirmed. All three reviewers reconfirmed no required unresolved text issue; actual motion is separate.'
t['final_reconfirmation']={a:'No unresolved required text finding in existing independent/cross/recheck scope.' for a in agents}
save(P/'reviews/text_final_review.json',t)
for name in ['artist_C07_C08_manifest.json','artist_C09_manifest.json','artist_C10_manifest.json']:
 m=read(P/name);m['review_status']='THREE_INDEPENDENT_CROSS_FINAL_IMAGE_REVIEW_PASS'
 for e in m.get('scenes',m.get('entries',[])):e['review_status']='THREE_REVIEWERS_FINAL_SELECTED_FIRST_FRAME_PASS'
 if name=='artist_C10_manifest.json':m['known_limitations']=['Actual rotation, free-bar handoff, and lowering while retaining face/covering gap must be verified in future generated videos.','Caption proof is post-production placement, not a first frame.']
 save(P/name,m)
d=read(P/'storyboards_draft.json');d['status']='TEXT_AND_40_FIRST_FRAMES_REVIEWED';save(P/'storyboards_draft.json',d)
status=read(V/'task_status.json');status['final_review_status']='All six final MP4s passed three independent/cross/final frame-sample reviews. No required unresolved finding; listening/realtime/venue unverified.';status['new_concepts_status']='C07-C10 text and all40 actual first frames reviewed; no Flow generation.';save(V/'task_status.json',status)
r=ROOT/'RESUME_CODEX.txt';old=r.read_text(encoding='utf-8-sig');marker='[2026-10-25 과거 110크레딧'
assert marker in old
head='''[2026-10-25 V13 — 1~6 최종 편집·7~10 전면 재작성 및 40첫이미지 검수 완료]
최신 범위: Q-AI Fair 품질팀 AI 성과·실제활용경험 교류. 화면+후처리자막/필수음성대사없음. C07~10 Flow미실행. 예약PAUSED유지. 공개게시·구매없음.
검수 시작: 루트 README.md → 00_완성_영상.md / 00_새7-10_콘티.md / 콘티_바로보기.md. 구루트문서는 archive/v12-before-final-v13 보존.

1~6 최종: storyboards/2026-10-25_final-six-v13/C01,C02,C03,C04,C05_r3,C06 의 Cxx_Q-AI_Fair_final_v13.mp4. 35.625/36.25/43/44.5/46.75/48.75초,720p24fps. C03무음, 나머지원음제거+BGM/SFX. 3인독립→교차→최종추출프레임/접합/자막재확인 필수문제0. 전체디코딩/PTS/SHA검사완료. 실제실시간연속재생/실청취/현장테스트/사용자채택미확인. delivery_manifest.json와 reviews/final_film_review.json 우선.
C05 최종은 C05_r3만. N05~N08외형/추가팔/지지해제/디졸브로전부HOLD. N03목빼기→21.75~23.25초실제잭운반→기존긴목정면받침의시간생략. 연속회전/손이동/하중이전/잭상승확보주장금지. 폐기중간C05/C05_r2는로컬보존/Git제외.
C01동일인물모니터·포스터합성+퇴장/포즈/실눕기/모방. C02동일점/2수갑/동일사진합성. C04쪽지완전투입/문서/3경첩창/한숟가락. C03장갑구간및자막단축. C06기존v06바이트동일재포장/타격효과음6.125초.

이번추가Flow:12성공원본모두그대로저장,채택6/HOLD6,실제관측200크레딧전부사용. 사용자250과차이50미해명. 최초 u0/u2/u3/u4각50,u1=0. 종료5계정모두0직접관측. 실패/환불0,접수중0. generation_log.json의ID/정확프롬프트/입력/잔액/원본SHA우선. 성공중복제출금지. 계정정보스크린샷로컬만/Git제외.

새7~10: storyboards/2026-10-25_C07-C10-rewrite-v13. 불량도이직합니다40.5초/구조는끝났습니다40.5초/나없이도괜찮겠어요34초/비법공개금지42초. 각10씬 총40PNG. 두작가독립발상→선정→연출→텍스트3인독립교차수정→실제이미지3인독립교차국소수정최종재확인완료. storyboards.json/scene_manifest.json최신. 실제Flow동작/최종영상합성/관객반응은미검증.
선택수정본 C07S01v2/S03v2,C08S09v3,C09S07v2,C10S02v4/S03v3/S04v3/S05v2/S06v2,나머지각Sxx.png. 정확manifest우선. C10작업대판내접지/천하단자유봉/손지주분리수정. caption_previews/C10_S10_caption_layout_v2.png는Q-AI Fair좌상단후자막배치증빙이며Flow시작이미지로쓰지말것. K10얼굴유지하며흰틈완전덮기는향후동작검증. C09발신자는폰뒤UI금지/외부편집배지. 가방리본부착위치작은차이는PD선택유지.

Windows수동미리보기 C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-final-six-v13-2026-10-25/index.html,storyboards.html,originals.html. fileURL자동열기는브라우저URL정책차단/우회금지. 정적링크검사와파일검증만. Git최신main/원격SHA는실제조회로확인.
역사적update_progress.py/update_pd_reviews.py/sync_status.py는이전잔액/중간검수로덮어쓰지않도록실행차단. 최종manifest기준build_review_navigation.py만최신루트재생성가능. 기존자료덮어쓰기금지.

'''
r.write_text(head+old[old.index(marker):],encoding='utf-8')
print('All final review records and resume synchronized')
