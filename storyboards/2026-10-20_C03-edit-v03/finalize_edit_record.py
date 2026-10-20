"""Finalize the reviewed derivative; update handoff without changing any original."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
VIDEO=P/'C03_review_edit_v03_45s.mp4'
RUN=P.parent/'2026-10-20_C03-flow-run09'
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review=json.loads((P/'review_summary.json').read_text(encoding='utf-8'))
assert review['final_visual_status']=='PASS_sampled_with_editorial_limitations'
m=json.loads((P/'edit_manifest.json').read_text(encoding='utf-8'))
m.update(file=VIDEO.name,status='revised review edit; independent and cross visual sample review complete; actual listening pending',
 sha256=hashlib.sha256(VIDEO.read_bytes()).hexdigest(),bytes=VIDEO.stat().st_size,
 review_record='review_summary.json')
m['limitations']=[
 'No actual listening, continuous playback, pronunciation or lip-sync verification claimed.',
 'New synchronous question audio not achieved. Run09 partial-prompt reaction excluded; silent full-question first1s used only as listening.',
 'Question is a J-cut over cuff picture; speaker/referent comprehension needs actual viewing/listening.',
 'Small21.5s pose/phone change accepted as an editorial cut, not continuous same-take motion.',
 'Glove removal/insertion remain state ellipses; original full physical action not restored.',
 'Review edit, not user-approved final film.'
]
save(P/'edit_manifest.json',m)
readme='''# C03 「환경까지 가져왔습니다」 편집 v03

[44.75초 검토본 MP4](C03_review_edit_v03_45s.mp4) · [편집 기록](edit_manifest.json) · [검수](review_summary.json) · [이번 원본 2개](../2026-10-20_C03-flow-run09/)

그림자와 두 기록 비교 장면을 유지하고, 전화 장면을 질문 → 청취 → 파일 집기로 다시 연결했습니다. v02보다 1초 줄였습니다. 모든 동작 화면은 실제 Flow 영상입니다.

- 18.65–20.45초: 기존 질문 음성을 앞 장면 위로 먼저 들려줍니다.
- 20.5–21.5초: 새 무음 원본의 첫 1초를 통화 청취로 사용합니다.
- 21.5–25초: 기존 깨끗한 파일 집기 동작, 상대 답변은 20.65–23.35초입니다.
- 26.25–28.25초: 두 기록의 조건을 비교합니다. 앞뒤 와이드에도 같은 도식을 유지합니다.
- 39.75–44.75초: 행사명과 참석 권유를 5초 표시합니다.

1280×720·24fps·1074프레임 전체 디코딩, 원본 SHA 불변, PCM 포화0. 자동전사로 기존 9문장이 검출됐습니다. 세 검수자가 실제 렌더 표본을 독립·교차 확인했습니다.

**실제 청취·발음·립싱크·전체 연속 재생은 미검증이며 최종 승인본은 아닙니다.** 21.5초 자세/전화 형태의 작은 차이는 컷 전환으로 수용했습니다. 질문을 장갑 화면 위로 먼저 들려주는 전달력은 실제 재생 판단이 남습니다.

이번 20크레딧은 Lite 두 번으로 모두 사용해 잔액0입니다. 첫 요청은 줄바꿈 입력이 생성으로 처리돼 첫 문단만 제출됐고 본편에서 제외했습니다. 두 번째는 전체 질문 프롬프트를 제출했지만 무음 영상이 반환됐습니다. 따라서 새 질문 음성을 확보한 것은 아니며, 기존 원음과 새 청취 화면을 조합했습니다. 원본2개·실제 프롬프트·입력 오류·비용은 run09에 보존했습니다. v01/v02와 기존 기획·원자료는 변경하지 않았습니다.
'''
(P/'README.md').write_text(readme,encoding='utf-8')
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>C03 편집 v03</title><style>body{background:#142029;color:#edf5f6;font:18px/1.65 sans-serif;max-width:1080px;margin:32px auto;padding:16px}video{width:100%;background:#000}a{color:#8dd9ce}</style>
<h1>환경까지 가져왔습니다 · 편집 v03</h1><p>44.75초 · 질문→청취→파일 집기 · 실제 청취와 최종 승인 대기</p>
<video controls preload="metadata" src="C03_review_edit_v03_45s.mp4"></video>
<p><a download href="C03_review_edit_v03_45s.mp4">편집본 MP4 저장</a> · <a href="../run09/originals.html">추가 원본2개</a></p>
<p>그림자와 기록 비교를 유지하고 전화 장면을 다시 연결했습니다. 20크레딧 모두 사용, 잔액0. 새 질문 음성은 얻지 못해 기존 원음과 새1초 청취 화면을 조합했습니다.</p>
<p>첫 요청은 입력 중 조기 제출되어 본편 미채택, 두 번째는 무음으로 반환됐습니다. 세 명의 실제 표본 검수와 디코딩을 마쳤으며, 실제 청취·립싱크·연속 재생 확인은 남아 있습니다.</p></html>'''
(P/'index.html').write_text(html.replace('../run09/','../2026-10-20_C03-flow-run09/'),encoding='utf-8')
cache=Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/edit-v03')
cache.mkdir(parents=True,exist_ok=True)
for n in [VIDEO.name,'README.md','edit_manifest.json','review_summary.json','audio_transcription.json']:
    shutil.copy2(P/n,cache/n)
(cache/'index.html').write_text(html,encoding='utf-8')
assert hashlib.sha256((cache/VIDEO.name).read_bytes()).hexdigest()==m['sha256']
for name in ['README.md','review_summary.json']:
    shutil.copy2(RUN/name,cache.parent/'run09'/name)

def read_exact(p):
    with p.open('r',encoding='utf-8',newline='') as f:return f.read()
def write_exact(p,t):
    with p.open('w',encoding='utf-8',newline='') as f:f.write(t)
heading='[2026-10-20 C03 추가20 사용 run09 + 편집 v03 — 잔액0/원본23개]'
entry=heading+'''
최신 사용자 “20 다 사용해서 모자란 부분 다 완성하고 영상 편집까지 시작하자”가 이전20보존 권고보다 우선. 같은 user-selected Chrome PLUS 프로젝트 c105a8ef-b295-4fc4-907c-1eb8e025245d에서 Lite10×2, 실제20→10→0/환불0. 두 원본 저장 완료/진행중0. 임의계정전환·구매·업스케일·예약재개·공개게시 없음.
run09 첫 요청: multiline typeText 줄바꿈이 제출로 작동해 첫 문단만 접수(대사 지시 없음). 감지 즉시 사용자에게 입력 오류/10차감 보고. 반응 원본 C03_K05_reaction_take01.mp4(asset13df7133-2ab1-45e9-ab42-5d904802674f), AAC에 지정 외 문장 ASR 검출/실청취 아님. 전화 턱 아래 이동·지게차 등장. 영상과 음성 모두 본편 미채택. 정확 실제 프롬프트를 계획본과 별도 보존.
두 번째: 남은10으로 줄바꿈을 공백 처리한 전체 질문 프롬프트를 안전하게 붙여넣고 UI검증 뒤1회 제출. C03_K05_question_take05.mp4(asset6d10f57e-5fe8-40ea-be80-ad865f4aca69) 정상완료하되 “생성된 오디오 없음”, 실제 오디오트랙없음. 동시 질문 음성 개선 실패. 계획했던 새집기 요청은 미제출,기존run03집기 유지. 두 원본 각8초/720p24fps/192프레임 디코딩/다운로드SHA일치/재인코딩없음. 누적23원본.
3명 실제 두32표본+개별PNG 독립/교차: 코일선·두번째전화·추가손은 표본미발견. 새Q초반1초만 청취후보, 뒤돌아 오래 입열린 후반은미채택. 새청취는 파일집기전에만. review_summary.json과generation_log.json 참조. 무음반환 임시ON 후 실제OFF복구/증거PNG보존. 앞으로 프롬프트는 paste/단일문자열로 넣고 전체 UI검증전 생성금지.
최신 storyboards/2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4=44.75초/720p24fps/1074프레임. 기존질문원음18.65–20.45화면밖J컷, 새Q0–1초를20.5–21.5청취로 사용,run03집기1.25–4.75를21.5–25에배치. S답변20.65–23.35, K06이후1초앞당김. 기록근접26.25–28.25,행사명39.75–44.75의5초. 기존그림자/페이지합성/음악 유지, 새음성합성/대사배속없음.
실제 최종렌더 표본3인독립·교차완료.21.5초 작은자세/전화형태차이는 편집컷으로 수용. 질문이커프화면에서먼저들리는구간의화자/대상 이해는 실재생확인 필요. 디코딩·원본SHA·PCM포화0/9문장ASR 검출. 실제청취·발음·말끝·음색·립싱크·연속재생은미검증. 모든결함완전해결/새동시대사성공/사용자최종승인이라쓰지않는다. 장갑탈착은여전히중간동작생략의PD편집.
Windows미리보기 C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/edit-v03/index.html,원본run09/originals.html. 이전v01/v02/legacyC01/V8기획원본보존. 새구매나재생성없이 사용자의 실제 재생 피드백으로 후속국소수정. Git반영은실제remote검증후보고.
'''
old=read_exact(ROOT/'RESUME_CODEX.txt')
if not old.startswith(heading):write_exact(ROOT/'RESUME_CODEX.txt',entry.replace('\n','\r\n')+'\r\n'+old)
old=read_exact(ROOT/'README.md')
start=old.index('최신 제작 상태:');end=old.index('\r\n\r\n',start)
new='최신 제작 상태: [새 3번 「환경까지 가져왔습니다」 **44.75초 편집 v03**](storyboards/2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4). 전화 장면을 질문→청취→파일 집기로 정리하고 1초 단축했습니다. [편집·검수 안내](storyboards/2026-10-20_C03-edit-v03/) · [새 원본2개·실제 입력/생성 기록](storyboards/2026-10-20_C03-flow-run09/) · [이전 v02](storyboards/2026-10-20_C03-edit-v02/). 추가20 사용/잔액0. 새 질문 음성은 확보하지 못해 기존 원음과 새1초 청취 화면을 사용했습니다. 3인 실제 표본 검수 완료, 실제 청취·연속 재생이 남은 검토본입니다.'
write_exact(ROOT/'README.md',old[:start]+new+old[end:])
bp=ROOT/'team/brief.toml';old=read_exact(bp)
if '[c03_edit_v03_2026_10_20]' not in old:
    block='''
[c03_edit_v03_2026_10_20]
status = "추가20 Lite2회 모두사용/잔액0/원본23개. 첫부분프롬프트오제출 미채택,두번째전체질문 무음반환. 동시질문음성개선미달."
path = "storyboards/2026-10-20_C03-edit-v03"
generation_run = "storyboards/2026-10-20_C03-flow-run09"
edit = "44.75초/1074프레임.기존질문J컷→새1초청취→기존집기,후반1초당김.3인독립/교차실제표본검수.실청취/연속재생미검증."
scope = "원본재인코딩없음/v01v02/legacyC01/V8보존.무음반환OFF복구.구매·계정전환·예약재개·공개게시없음."
'''
    write_exact(bp,old+block.replace('\n','\r\n'))
print(json.dumps({'video':str(VIDEO),'bytes':m['bytes'],'sha256':m['sha256'],'duration':m['duration_seconds']},ensure_ascii=False))
