"""Finalize reviewed derivative and update project handoff; originals remain read-only."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
VIDEO=P/'C03_review_edit_v02_46s.mp4'
def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review=json.loads((P/'review_summary.json').read_text(encoding='utf-8'))
assert review['final_visual_status']=='PASS_sampled_after_local_composite_fixes'
m=json.loads((P/'edit_manifest.json').read_text(encoding='utf-8'))
m.update(status='revised review edit; three independent/cross visual sample reviews complete; actual listening pending',
         sha256=hashlib.sha256(VIDEO.read_bytes()).hexdigest(),bytes=VIDEO.stat().st_size,
         review_record='review_summary.json')
m['graphics']['K06']='New real0–2s closeup, separately tracked diagrams at27.25–29.25s; same artwork composited on surrounding visible wide pages, with supersampling and foreground masks.'
m['limitations']=[
 'No actual listening, continuous playback, pronunciation or lip-sync verification claimed.',
 'K01 underside partially visible; accepted as anticipatory cue, not complete non-exposure.',
 'K05 new synchronous shot failed twice; retained existing clean pickup picture and existing question VO.',
 'Cuff3.5s retained as optional pacing choice; no mandatory missing generation identified in visual samples.'
]
save(P/'edit_manifest.json',m)
(P/'README.md').write_text('''# C03 「환경까지 가져왔습니다」 수정 편집 v02

[45.75초 검토본 MP4](C03_review_edit_v02_46s.mp4) · [편집 기록](edit_manifest.json) · [독립·교차 검수](review_summary.json) · [새 Flow 원본2개](../2026-10-20_C03-flow-run08/)

새 K01의 표면 그림자로 기존 화면을 교체하고, K06의 두 기록을 비교하는 실제 근접 영상을 넣었습니다. 도식은 두 내부 페이지와 앞뒤 와이드의 종이에 맞춰 합성했습니다. 모든 동작 화면은 실제 생성 영상이며, 정지 이미지 움직임으로 대체하지 않았습니다.

- 45.75초 /1280×720 /24fps /H264+AAC /1098프레임 전체 디코딩.
- 행사명과 참석 권유는40.75–45.75초,5초 유지.
- K05는 기존 깨끗한 파일 집기 화면+질문 원음+전화 답변을 유지합니다.
- 장갑 탈착은 전후 상태와 커프 정돈으로 생략 연결했습니다. 원안 전체 탈착 동작이 복구된 것은 아닙니다.
- 짧은 금관·비브라폰 음악은 v01에서 만든 오리지널 구성입니다. 새 음성 합성·대사 배속은 없습니다.

세 명이 실제 렌더 프레임을 독립 검토하고 의견을 교차 검증했습니다. 전후 페이지 내용 불일치와 축소 합성의 글자 끊김을 수정했습니다. **실제 청취·연속 재생·발음·립싱크 최종 확인은 남아 있습니다.** 자동전사9문장 검출은 청취 검증이 아닙니다.

이번 run08은50으로 시작해30 순사용, 잔액20입니다. 전화 컷 Fast2회가 모두 오디오 오류로 실패하여40을 환불받았습니다. 같은 요청을 세 번째 반복하지 않았고, 다른 필수 생성 공백을 발견하지 못해20을 보존했습니다. v01과 모든 원본은 별도로 유지합니다.
''',encoding='utf-8')
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>C03 수정 편집 v02</title>
<style>body{background:#121b22;color:#e9f2f3;font:18px/1.65 sans-serif;max-width:1080px;margin:36px auto;padding:0 20px}video{width:100%;background:#000}a{color:#86d8cf}p{max-width:900px}</style>
<h1>환경까지 가져왔습니다 · 수정 편집 v02</h1><p>45.75초 · 그림자와 기록 비교 보완 · 실제 청취·최종 승인 대기</p>
<video controls preload="metadata" src="C03_review_edit_v02_46s.mp4"></video>
<p><a download href="C03_review_edit_v02_46s.mp4">편집본 MP4 저장</a> · <a href="../run08/originals.html">새 Flow 원본2개</a></p>
<p>0–6초: 표면 그림자 /27.25–29.25초: 두 기록 비교 /마지막5초: 행사명과 참석 권유. 전화 장면은 기존 원음과 깨끗한 화면을 유지했습니다.</p>
<p>세 명의 실제 프레임 검수와 기술 검사를 마쳤습니다. 실제 음성·립싱크·연속 재생 호흡 확인은 남아 있습니다. 순사용30, 잔액20. 전화 컷2회는 오디오 생성 실패·환불되었습니다.</p></html>'''
(P/'index.html').write_text(html.replace('../run08/','../2026-10-20_C03-flow-run08/'),encoding='utf-8')
cache=Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/edit-v02')
cache.mkdir(parents=True,exist_ok=True)
for name in [VIDEO.name,'README.md','edit_manifest.json','review_summary.json','audio_transcription.json']:
    shutil.copy2(P/name,cache/name)
(cache/'index.html').write_text(html,encoding='utf-8')
assert hashlib.sha256((cache/VIDEO.name).read_bytes()).hexdigest()==m['sha256']

def read_exact(path):
    with path.open('r',encoding='utf-8',newline='') as f:return f.read()
def write_exact(path,text):
    with path.open('w',encoding='utf-8',newline='') as f:f.write(text)
heading='[2026-10-20 C03 그림자·기록 보완 run08 + 수정 편집 v02 — 순사용30/잔액20]'
entry=heading+'''
최신 사용자: 50크레딧 계정으로 처음 그림자를 재작업하고 부족한 부분을 완성하도록 승인. 현재 Chrome 주계정 PLUS의 기존 프로젝트 https://flow.google.com/project/c105a8ef-b295-4fc4-907c-1eb8e025245d 사용. 임의 계정 전환 없음. 정확한 갱신 시각은 확인되지 않았으며 자정으로 가정하지 않는다.
run07 K05take04 Lite10은10→0으로 완료됐지만1초부터 코일선이 다시 생겨3인 표본검수 HOLD. 원본은 보존. 이어 run08 첫 프레임3장 새로 제작/3인 독립·교차검수: K01 no-sky, K05 flat-smartphone, K06 두 기록 근접. 기존 V8 43PNG/5안/legacy C01/이전 원본은 불변.
run08 실제4요청: K01 Fast20 50→30 성공; K05 Fast20 30→10→30 오디오 실패/20환불; 단순화 프롬프트로 기술복구1회 Fast20 30→10→30 같은 오디오 실패/20환불; K06 Lite10 30→20 성공. 총차감70/환불40/순사용30/종료잔액20 실제 확인. 진행중0. 같은 오류2회 뒤 K05 세 번째 반복 없음. 모든50소진 완료라고 쓰지 않는다.
원본 C03_K01_take02.mp4(asset171024a1-3b32-4fd9-a3ce-0aaa9b485644), C03_K06_insert_take01.mp4(asset1f9ecb3b-6891-4d2b-92d7-5170f171e671). 각각8초720p24fps H264/AAC,192프레임 디코딩/다운로드 SHA 일치/재인코딩 없음. 정확 제출 프롬프트·입력해시·차감·환불·검수는 storyboards/2026-10-20_C03-flow-run08/generation_log.json. 누적 C03 원본21개. K05take05는 산출물이 없으므로 원본으로 세지 않는다.
K01 표면 그림자와 올려다보는 반응을0–6초 채택. 상단 구조물 하부 일부가 실제 보이므로 완전 미노출 성공이 아니다. PD가 사무실 전체 공개 전 예고로 수용. K06 첫2초를 전체27.25–29.25초에 사용,두 내부 페이지+앞뒤 와이드에 동일 도식 합성. 원본에 도식이 생성된 것은 아니다.
최신 편집 storyboards/2026-10-20_C03-edit-v02/C03_review_edit_v02_46s.mp4:45.75초/720p24fps/1098프레임, 전체 디코딩 및 원본 SHA 불변.3명 실제 렌더 표본 독립·교차·수정 재확인. 전후 페이지 불일치 및 합성 인쇄 끊김을 국소 수정. K03장갑탈착은 후상태, K04커프정돈은 중간과정 생략으로 유지. K05 기존 깨끗한 집기 화면과 질문 원음/전화 답변 유지. 엔딩40.75–45.75초5초. 새 대사 합성·배속 없음.
실제 청취·발음·말끝·음색·립싱크·전체 연속 재생 호흡은 미검증. 자동전사9문장 검출을 청취로 쓰지 않는다. 아직 최종 승인 영화가 아니라 수정 검토본이다. 실제 재생에서 구체적 결함이 확인될 때 추가20 사용처를 판단한다. 현재 다른 필수 생성 공백은 발견되지 않아20 보존. 소진만을 위한 다른 컷 생성/같은 K05 반복 금지.
무음 반환은 비대사 K06에만 임시ON 후 실제OFF 복구. 구매·구독변경·업스케일·외부유료API·예약재개·공개게시 없음. Windows 미리보기 C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/edit-v02/index.html, 원본은 run08/originals.html. Git 반영은 실제 remote 확인 후 보고.
'''
old=read_exact(ROOT/'RESUME_CODEX.txt')
if not old.startswith(heading):write_exact(ROOT/'RESUME_CODEX.txt',entry.replace('\n','\r\n')+'\r\n'+old)
old=read_exact(ROOT/'README.md')
start=old.index('최신 제작 상태:');end=old.index('\r\n\r\n',start)
new='최신 제작 상태: [새 3번 「환경까지 가져왔습니다」 **45.75초 수정 편집 v02**](storyboards/2026-10-20_C03-edit-v02/C03_review_edit_v02_46s.mp4). 그림자와 두 기록 비교를 보완하고, 3인 독립·교차 실제 프레임 검수를 마쳤습니다. 실제 청취·연속 재생 확인이 남은 검토본입니다. [편집·검수 안내](storyboards/2026-10-20_C03-edit-v02/) · [새 원본2개·생성 기록](storyboards/2026-10-20_C03-flow-run08/) · [이전45.25초 v01](storyboards/2026-10-20_C03-edit-v01/). run08 순사용30/잔액20: 전화 컷2회는 오디오 오류·환불되어 기존 화면과 음성을 유지했습니다.'
write_exact(ROOT/'README.md',old[:start]+new+old[end:])
bp=ROOT/'team/brief.toml';old=read_exact(bp)
if '[c03_edit_v02_2026_10_20]' not in old:
    block='''
[c03_edit_v02_2026_10_20]
status = "그림자·기록 근접 새 원본2개,45.75초 수정 검토본.3인 독립·교차 실제 표본검수와 국소 합성 수정 완료. 실제 청취/연속재생은 미검증."
path = "storyboards/2026-10-20_C03-edit-v02"
generation_run = "storyboards/2026-10-20_C03-flow-run08"
credits = "50시작/차감70/오디오 실패2회 환불40/순사용30/종료20. 총4요청 중2성공. K05 반복 중단, 다른 필수 누락 미발견으로20보존."
scope = "C03원본21개. 기존기획43PNG/legacyC01/이전원본/v01보존. 무음반환OFF복구. 구매·계정전환·예약재개·공개게시없음."
'''
    write_exact(bp,old+block.replace('\n','\r\n'))
print(json.dumps({'file':str(VIDEO),'sha256':m['sha256'],'bytes':m['bytes'],'duration':m['duration_seconds']},ensure_ascii=False))
