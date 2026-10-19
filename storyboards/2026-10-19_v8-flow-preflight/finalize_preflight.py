from pathlib import Path
import json
R=Path(__file__).resolve().parent;ROOT=R.parent.parent
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=json.loads((R/'pd_disposition.json').read_text(encoding='utf-8'))
p['count_decision']['tail_reuse']='C01K03 tail->K04P; C04K06 tail->K01CM; C05K04 tail->K07FM. Only exact natural cues actually obtained. C04K05 now native RC speech; K04tail deleted because mouth is visible. Tail failure may need another source beyond47.'
p['decisions'] += [
 {'ids':['A-P007','B-P008','C-012'],'action':'C01K03 retains one fixed8s shot, transition only in post. C05K08 uses local2s, not absolute34s.'},
 {'ids':['A-P008','B-P008','C-011'],'action':'C05K02A framing explicitly upright column removal only. B retains body-fold/entry.'},
 {'ids':['C-010'],'action':'Visible RC speaks natively inC04K05; removed from silent list; deletedK04tail; actual lip/timbre comparison still required.'}
]
p['status']='three-reviewer independent/cross/correction verification complete; no mandatory unresolved planning issue; actual Flow/audio/motion untested'
put('pd_disposition.json',p)
put('progress.json',{'status':'complete','scope':'production preflight only','source_concepts_accepted_by_user':5,'editing_cuts':43,'visual_sources':44,'conditional_audio_sources':3,'planning_budget':47,'new_draft_visual_prompts':44,'reviewers_confirmed':3,'mandatory_unresolved':0,'video_audio_flow_executed':False,'automation_resumed':False})
resume=ROOT/'RESUME_CODEX.txt'
prefix='''[2026-10-19 V8 다섯 안 사용자 수용 / Flow 제작 전 최종 점검 완료]
최신 사용자: 지금 5안 모두 괜찮아 보임. 오늘 저녁 영상 작업을 앞두고 첫 프레임·대사·음성·배경음과 작품별 영상 수 검토 요청. 새 이야기·이미지는 만들지 않는다.
기준 원안: storyboards/2026-10-19_tone-polish-v8/의 5안·43장. 모든 원안 객체·채택 PNG 바이트와 기존 별도 C01 36초 영화 SHA 유지.
최신 제작 지시: storyboards/2026-10-19_v8-flow-preflight/FLOW_PREFLIGHT.md, production_plan.json, clip_manifest.json, voice_bible.json, music_plan.json, prompts/. 기존 원안에 남은 실제 첫 상태·동작·음향 충돌은 이 오버레이를 우선.
수량: 편집43컷 / 화면원본44개=C01성공자세9,C02검은점9,C03환경8,C04목마9,C05괴수9. C05K02 제거A/몸접기B 분리 권장. C01K04모니터인서트는1개대체라 추가계산금지. 전화/안내 예비음성3개 포함47개 계획. 재시도·음성 확보 실패는 별도이며47개보장상한아님.
제작 전 의존성: C01K04원본PNG의 모니터 내부만 추출·원근보정·확인(현재파생PNG없음). C05K02B는 실제채택A마지막프레임으로 시작(현재없음). 준비완료로오인금지.
중요 보정: C01K05이미선L1/K03같은8초숏/K06착지뒤말; C03K06펜없음·내부조건기록비교/K07패널이미열림; C04K05입보이는RC직접말, K08첫그릇창밖순간음악컷; C05K06사다리이미펼침/K07FM화면밖·TE무언/K08국소2초.
꼬리음성3곳: C01K03→K04P, C04K06→K01CM, C05K04→K07FM. C04K04꼬리음성계획은삭제했으므로낡은검토안사용금지. 실제 자연스러운 원음이 있을 때만 재사용. 목소리묘사는동일화자보장아님. BGM은작품별후편집, 생성요청에는음악없음.
세 명의 전체독립검토→교차검증→구체충돌수정→최종재확인완료, 필수미해결0. 실제영상동작·한국어발음·음색·립싱크·관객반응은미검증. validation.json은파일/해시/43컷44매핑/링크검사.
이번 Flow업로드·영상/음원생성·크레딧사용0, 예약재개안함. 오늘저녁이라는말로자동예약/기존큐재개금지. 생성실행요청시현재UI모델/길이/비용/잔액을먼저확인. Lite선호유지, Fast자동승격금지. 과거10/20크레딧은현재견적아님.
Git루트README와콘티_바로보기.md에제작점검링크추가. Git반영상태는실제log/remote확인.

이하 이전 작업 이력 — 최신 V8 제작 점검 지시 우선

'''
old=resume.read_text(encoding='utf-8')
if not old.startswith('[2026-10-19 V8 다섯 안 사용자 수용'):resume.write_text(prefix+old,encoding='utf-8')
brief=ROOT/'team/brief.toml';b=brief.read_text(encoding='utf-8')
b=b.replace('# 최신 지시는 맨 아래 creative_direction_2026_10_19_tone_polish_v8을 우선한다.','# 최신 제작 검토는 맨 아래 production_preflight_2026_10_19를 우선한다. 승인 콘티는 V8이다.')
if '[production_preflight_2026_10_19]' not in b:
 b+='''
[production_preflight_2026_10_19]
user_feedback = "V8 다섯 안 모두 괜찮음. 오늘 저녁 제작을 앞두고 첫 프레임·대사·음성·배경음·영상 수 전체 검토 요청."
source = "storyboards/2026-10-19_tone-polish-v8"
production_overlay = "storyboards/2026-10-19_v8-flow-preflight/FLOW_PREFLIGHT.md"
counts = "편집43컷, 화면44개=9/9/8/9/9, 조건부 음성예비3개로47개계획. 재시도별도."
delivery = "실제 첫 상태·화자·동작·음악지시 보정,44제작프롬프트초안,3인독립/교차/수정재확인완료. 기존5안·43PNG바이트불변."
scope = "검토·준비만. Flow·영상·음원·크레딧사용0,예약재개안함. 실제발음·립싱크·동작은생성후검수."
'''
brief.write_text(b,encoding='utf-8')
print('Final status, PD decisions, resume and brief updated.')
