from pathlib import Path
import json,hashlib,datetime,shutil
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;F=ROOT/'storyboards/2026-10-24_v12-C02-C04-C01-flow';N=ROOT/'storyboards/2026-10-24_C05-first-flow-run01';E=ROOT/'storyboards/2026-10-24_C05-causal-edit-v05'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
scope='Actual contact sheets and selected individual PNGs, storyboard/provenance records; not continuous playback, listening, venue test or measured audience response.'
review={'date':'2026-10-24','status':'STILLS_AND_SELECTED_SOURCE_INTERVALS_ACCEPTED_WITH_POSTPRODUCTION_REQUIREMENTS','scope':scope,'reviewers':['/root/causal_review_a','/root/causal_review_b','/root/causal_review_c'],'independent':{
 'A':['C05 A-E06 causal repair accepted; worker insert is time ellipsis, not complete rotation/load transfer.','C02 A-V01–03 probes accepted; monitor composite and revised palm/photo ending mandatory.','C04 A-V04 envelope late re-extraction, A-V05 already-open K06, A-V06 duplicated spoons, A-V07 three-window crop.','C01 A-V08 ghosting, A-V09 exact pose drift, A-V10 return into room: selected intervals only.','C07 A-I01 exposed rail fixed in six rig_v3 edits; A-I02 actual still/action alignment; C09 A-I03 cart diagram throughout; C10 A-I04 right-hand ring alignment.'],
 'B':['C05 B-V01–03 cause and time ellipsis accepted, softer crop/sky/fascia optional.','C02 B-V04 cuff morph excluded by probe; B-V07 monitor composite still required.','C04 B-V05 early-open K06 excluded, B-V06 fourth figure excluded by three-window crop.','C07 B-V08 manifest alignment; C09 B-V09 same diagram from uncover; C10 B-V10 face reaction moved to next wide.','C01 B-V11 third arm at5–6s, B-V12 ghosting after6s, B-V13 floating door, B-V14 no actual exit, B-V15 changing pose.'],
 'C':['C05 C-V01 causal repair/time ellipsis accepted; C-V02 softness/fascia optional.','C04 C-V03 fourth person/crop late shutter morph, C-V04 lid chronology.','C01 C-V05 late ghosting, C-V06 detached door.','C02 C-V07 monitor composite mandatory, C-V08 revised ending alignment.','C09 C-I01 small board graphic continuity; C10 C-I02 right-hand ring; C08 C-I03 move screen-right/back; C09 C-I04 gaze toward new speaker.']},
 'cross':{
 'A':{'agrees':['C05 time ellipsis','C02 three probes','C04 K06 exclusion/short window crop','C07–10 selected40 no mandatory regeneration'],'corrections':['Withdrew suggestion to use C01 K06 5–6s after seeing third arm.','Withdrew description of K09 as ordinary door opening after detached-door PNG evidence.'],'preference':'Prefers K07 first1.2s, but accepts source join story with posture-reset ellipsis.'},
 'B':{'agrees':['C05 A/C cause and time ellipsis','C04 K01 late re-extraction exclude','C04 K09 use6s onward, not claim extraction action','C04 short crop','40stills/action alignment'],'disagreement':'K07 first1.2s is not mandatory. Existing3.5s keeps observer decision to crouch; posture-reset ellipsis accepted.'},
 'C':{'agrees':['C05 A/B causal acceptance','C02 selected probes and composite requirement','C04 short crop and K06 exclusion','C01 actual join probe'],'missed_then_confirmed':['Third arm C01 K06 5.5s','C04 K01 late re-extraction','C04 K09 two spoons']}}
 ,'final_recheck':{'A':'C01 K09take02 door solid at2/5/7.5s, three people maintained;0–7s acceptable with slight arm-angle drift. C10 right-hand transition and C08 direction verified.','B':'K09take02 door restored at0/6/7.5s; matching floor-pose meaning persists. C04 short crop and C01 join actual probes accepted. C10/C08 final text verified.','C':'K09take02 contact and0/3.5/7.5s show door attached, no extra arms/ghosting in samples. C10/C08 last text issues resolved.'},
 'pd_decisions':['Preserve all originals and earlier storyboards. Select source intervals; do not pass whole flawed raw videos.','C01 K07 up to3.5s accepted for observer crouch; exact-pose gag can be emphasized in K08first1s. K09take02 chosen for title hold; slight angle drift accepted.','C04 K06 omitted; use K07closed start for denial caption then actual opening. K08take02 only cropped1–3.25s. K09use6–8s after spoon duplication.','C02 final photo action becomes palm/turn and caption 이 사례는 직접 설명하시죠.','C05 complete causal repair edit accepted subject to time-ellipsis and playback/listening limitations.','NewC07–10 images/action plan accepted; do not launch Flow until requested.'],
 'remaining':['C01 portrait/monitor matching K04, final captions and edit','C02 monitor/photo comparisons and final captions/edit','C04 document/tablet/captions and final edit','NewC07–10 actual motion and precise graphic composites','Final playback/listening/venue readability and user approval']}
(R/'reviews').mkdir(exist_ok=True);save(R/'reviews/final_review_summary.json',review);save(F/'review_summary.json',review)
save(E/'review_summary.json',{'status':'CAUSAL_REPAIR_ACCEPTED_WITH_EDIT_ELLIPSIS','scope':scope,'independent':{k:review['independent'][k][0] for k in 'ABC'},'cross':{k:'Agrees other two: entry/catch/grip/neck withdrawal establish cause; worker insert permits time ellipsis. No full rotation/load-transfer claim.' for k in 'ABC'},'pd':'Current51.25s cut accepted for user review; optional softer worker insert and long neck-release pacing retained. No additional source required.','file':'C05_Q-AI_Fair_causal_edit_v05.mp4','sha256':hashlib.sha256((E/'C05_Q-AI_Fair_causal_edit_v05.mp4').read_bytes()).hexdigest()})
notes={
 ('C01_K01',2):'Use0–4s hand correction; later gestures unnecessary.',('C01_K02',2):'Use0–2.5s pose correction; later palms/prayer excluded.',('C01_K03',1):'Actual key contact about1.5–3s; monitor needs selectedK04 insert.',('C01_K04',1):'Use landing through4–4.5s; later crossleg reposition excluded.',('C01_K05',2):'Use door guidance0–3.5s; actual exit not obtained; later return excluded. Time ellipsis toK06.',('C01_K06',1):'Use1.5–4.25s; third-arm5–6s excluded. Chair morphology remains optional continuity issue.',('C01_K07',1):'Use0–3.5s or shorter photo moment; ghosting6s onward excluded.',('C01_K08',1):'Initial0–1s strongest exact imitation, up to3s similar-pose movement accepted.',('C01_K09',1):'HOLD detached door. Crop probe also failed late door exclusion.',('C01_K09',2):'Use0–7s ending candidate. Door restored, small arm-angle drift accepted. Not perfectly motionless.',
 ('C02_K04',1):'Use1–2.5s protective window wipe +4.5–6s button. Exclude wiping white sample.',('C02_K05',1):'Use0–3s→K06 0–2s installation time ellipsis; late extra cuff rings excluded.',('C02_K06',1):'Use0–2s afterK05; monitor obstruction composite mandatory.',('C02_K09',1):'Use4–6.5s palm/photo action. Revised ending caption; original aborted-photo-removal action not obtained.',
 ('C04_K01',1):'Envelope insertion cue5.5–6s;7s re-extraction excluded. Do not claim all three slips inserted.',('C04_K06',1):'HOLD already-open lid defeats first reveal. UseK07 closed start+opening.',('C04_K08',1):'HOLD wrong cast and six bowls.',('C04_K08',2):'Only1–3.25s crop x600 y20 w512 h288. Exclude fourth side person and late shutters morph.',('C04_K09',1):'Use6–8s single spoon state. Middle duplicated spoons excluded; extraction action not claimed.'}
d=load(F/'generation_log.json')
for e in d['entries']:
 if e.get('original'):
  msg=notes.get((e['unit_id'],e['take']),'Candidate accepted in visual sample review; final editing/graphics/captions not completed.')
  e['review']=msg;e['status']='HOLD_WHOLE_CLIP' if msg.startswith('HOLD') else 'CANDIDATE_WITH_EDIT_CONDITIONS'
  e['review_record']='review_summary.json';e['listened']=False
d['status']='ALL27_UNITS_HAVE_ORIGINAL_CANDIDATES_EDIT_CONDITIONS_RECORDED';d['pending_requests']=0
d['account_balance_summary']={'current_u0':{'start':250,'end':0},'current_u1':{'start':50,'end':0},'current_u2':{'start':50,'end':10,'reset_ui':'매일 오전10:43'},'other_signed_in_accounts':'NOT_CHECKED'}
d['total_net_spend_across_observed_accounts_including_C05']=340;d['last_balance_observed']=10
d['account_summary_note']='Do not add per-entry before/after blindly across accounts or overlapping refunds. C01K01/K02 audio failures returned20 together; C01K05 refund10 observed; C02K07 refund10 is inferred reconciliation, not explicit refund UI.'
save(F/'generation_log.json',d)
q=load(F/'queue.json')
if isinstance(q,dict):
 q['status']='ALL27_SOURCE_UNITS_GENERATED_WITH_EDIT_CONDITIONS';q['review_record']='review_summary.json';save(F/'queue.json',q)
d=load(N/'generation_log.json');d['status']='FIVE_ORIGINALS_PRESERVED_CAUSAL_EDIT_V05_REVIEWED';d['pending_requests']=0
for e in d['entries']:
 if e['unit_id']=='C05_N02' and e['take']==1:e['status']='HOLD_ROOF_DETACHES';e['review']='Whole roof detachment; unselected.'
 else:
  e['status']='PARTIAL_INTERVAL_SELECTED_IN_V05';e['review']='Exact chosen interval in ../2026-10-24_C05-causal-edit-v05/edit_manifest.json. N04 late neck morphology excluded; only0.5–2s used.'
save(N/'generation_log.json',d)
for name in ['storyboards.json','scene_manifest.json']:
 d=load(R/name)
 if name=='storyboards.json':
  d['status']='STORYBOARDS_AND40_FIRST_IMAGES_CROSS_REVIEWED';d['final_review']='reviews/final_review_summary.json'
  for c in d['concepts']:
   c['review_status']='THREE_REVIEWERS_RECHECKED_STILLS_AND_PLAN'
   for s in c['scene_list']:s['review_status']='THREE_REVIEWERS_RECHECKED_STILL_ONLY'
 else:
  for s in d['scenes']:s['review_status']='THREE_REVIEWERS_RECHECKED_STILL_ONLY'
 save(R/name,d)
brief=load(R/'brief.json');brief['status']='REQUESTED_SOURCE_GENERATION_AND_NEW4_STORYBOARDS_DELIVERED_WITH_EDIT_CONDITIONS';brief['unverified']=['정확일시/장소/참석방법/성과수치','새7~10 실제영상','1/2/4 최종합성·자막·편집','연속재생·실청취·현장검증'];brief['flow_observation']=load(F/'generation_log.json')['account_balance_summary'];brief['progress']={'C05':'causal edit v05,51.25s reviewed','C06':'caption v05,48.75s reviewed','C03':'caption v04,44.75s reviewed','C02_C04_C01':'27units generated;29originals, selection/trim/crop conditions recorded','C07_C10':'4 rewritten stories,40selected images,3independent/cross/recheck complete;Flow0'};save(R/'brief.json',brief)
resume=ROOT/'RESUME_CODEX.txt';old=resume.read_text(encoding='utf-8-sig');old=old[old.find('[2026-10-24 최신 10안 장면 연결 재검토'):]
header='''[2026-10-24 V12 최신 납품 — 원본 생성·새4안 이미지 완료,1/2/4최종편집 남음]
사용자 요청: 이미지 인과보완 및 Flow5보완→6→2→4→3→1, 별개7~10전체재작성·첫이미지. 새7~10Flow금지. Q-AI Fair=품질팀AI성과·활용경험교류,화면+후처리자막/무대사. 예약PAUSED유지.
메인README.md와00_영상제작_현재상태.md,00_완성_영상.md가 최신진입점. 이전7~10루트문서는archive/v11-root-review로보존. 최신새07~10제목은훔칠필요가없었다/해동하자마자발표/낙찰받으신분이공개합니다/청혼은없었습니다.
새원본34개=storyboards/2026-10-24_C05-first-flow-run01의5+2026-10-24_v12-C02-C04-C01-flow의29. 2번9,4번10,1번10;계획단위27개모두영상후보있음. 모두8s720p24fps192프레임디코딩/원본SHA동일. 진행중0. 새영상원본재인코딩없음.
u0시작250→0,u1시작50→0,u2시작50→10,관측3계정순340. 다른2계정잔액이번미확인. u2갱신안내매일오전10:43. C02K07첫결과없음/10반환은대조추론,명시환불UI아님. C01K01/K02오디오실패20반환및K05실패10반환후무음반환ON으로1회기술재시도성공. 정확계정프로젝트ID/asset/프롬프트/해시/잔액generation_log참조,중복요청금지. 구매/구독/유료API없음.
C05 causal-edit-v05=51.25s:진입→목걸림→테두리잡기→목빼기→부분회전→작업자잭삽입→정면받침. 세검수자독립/교차수용. 완전회전/하중이전연속확보아님,작업자삽입시간생략. N02take01roofdetachHOLD,N04후반목변형HOLD;실제구간EDL준수.
C06 caption-v05=48.75s목적자막보강,원본/기존AAC재사용. C03 caption-v04=44.75s환경/보낸동료/기록도해/Q-AI Fair,무음. 모두3인표본교차+디코딩완료,연속재생/실청취/현장검증/사용자최종승인아님.
C02 K04[1,2.5]+[4.5,6],K05[0,3]→K06[0,2],K09[4,6.5]새손바닥엔딩. 모니터같은시료청소전후/수갑장애,사진/폰합성필수. C04 K06미채택,K07닫힘0~2s부인→첫열림,K08take02[1,3.25]x600y20w512h288크롭,K09[6,8]한숟가락. K01후기재추출제외,작은종이모두삽입성공주장금지.
C01 K06[1.5,4.25]→K07[0,3.5]→K08[0,3]실제probe3인수용,정확포즈개그K08초반1s강조. K06후기세팔/K07후기소실제외. K05문방향안내까지만사용,실퇴장미확보. K09take01문분리HOLD,새take02asset98f47a9c-c6e7-425f-a5a7-42464f0f417f[0,7]후보3인수용,문고정/소폭팔각도변경수용. 모니터/포스터K04실영상합성·자막·최종편집남음.
새7~10:storyboards/2026-10-24_v12-rework/storyboards.json,scene_manifest.json,각artistmanifest와reviews/final_review_summary.json.39/42/38/41s각10씬40실제PNG. C07rig_v3노출수평레일제거6장,상단밖두케이블/당김/8슬롯/허리명찰. C08왼사진목표/열풍기왼바닥/조작RL왼손/오른쪽뒤이동. C09카트K04공개부터모든판+B1판동일도해후합성필수. C10오른손고리→같은손폰, S09낮은미디엄/S10얼굴반응. 3인독립→교차→최종명세/40이미지재확인완료. 실제움직임검증아님,새4안Flow미실행.
Git반영은push성공과remoteSHA확인후보고. 최종파일원본/기획보존. 생성자막금지/필수대사없음 유지. 새원본추가생성은기존검수지정구간/후처리로해결할수있는지먼저판단.

'''
write=lambda p,t:p.write_text(t,encoding='utf-8');write(resume,header+old)
proof=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v12-2026-10-24/flow_C01_last3_completed.jpg');shutil.copy2(proof,F/'flow_completed_proof.jpg')
print('Review results, selection conditions, final mappings and resume synchronized.')
