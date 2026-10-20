"""Persist reviewed edit metadata and project handoff; no browser/network operations."""
from pathlib import Path
import json, hashlib, shutil
out=Path(__file__).resolve().parent
project=out.parent.parent
video=out/'C03_review_edit_v01_45s.mp4'
m=json.loads((out/'edit_manifest.json').read_text(encoding='utf-8'))
m['sha256']=hashlib.sha256(video.read_bytes()).hexdigest()
m['bytes']=video.stat().st_size
m['review_record']='review_summary.json'
m['status']='first full review edit; three independent/cross visual sample reviews completed; actual listening pending'
m['limitations']=[
    'No actual listening, continuous playback, pronunciation or lip-sync verification claimed.',
    'Cuff 3.5s retained; shorten only if continuous playback demonstrates drag.',
    'No mandatory missing generation identified. Subsequent explicit user request for a spare is separate run07.'
]
(out/'edit_manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
preview=Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/edit-v01')
preview.mkdir(parents=True,exist_ok=True)
for n in ['C03_review_edit_v01_45s.mp4','index.html','README.md','edit_manifest.json','review_summary.json']:
    shutil.copyfile(out/n,preview/n)

def read_exact(path):
    with path.open('r',encoding='utf-8',newline='') as f: return f.read()
def write_exact(path,text):
    with path.open('w',encoding='utf-8',newline='') as f: f.write(text)

resume=project/'RESUME_CODEX.txt'
heading='[2026-10-20 C03 첫 전체 편집 v01 — 45.25초/3인 표본검수/실청취대기]'
entry="""[2026-10-20 C03 첫 전체 편집 v01 — 45.25초/3인 표본검수/실청취대기]
사용자 “그럼 이걸 바탕으로 영상 제작 시작할 수 있어?”에 따라 기존 원본으로 첫 전체 편집본 제작. 추가1컷이 가능하다고 했으나 편집상 필수 누락은 발견되지 않아 우선 생성0으로 완성. 이후 “한컷 그러면 하나 더 아무거나 만들어봐라” 명시 요청은 별도 run07로 진행한다. 기존 C01/V8기획43PNG/18원본 불변.
storyboards/2026-10-20_C03-edit-v01/C03_review_edit_v01_45s.mp4. 45.25초720p24fps/AAC/1086프레임 전체디코딩. 10편집구간으로8씬. K03탈착은run05맨손후상태6~7초, K04착용은run06커프2.25~5.75초로 생략연결. 전체탈착성공이 아님.
K05영상run03take03 1~6.5초, 질문음성run01take01 2.4~4.2초를전체20.15초에, 전화S답변run02VO0~2.7초를22.25초에 배치. 코일선/두전화기불량화면제외. K06내부페이지 비교26.75~28.50초=1.75초, K03동일결과도식2.5초. 도식총4.25초로PD조정. K06파일모으기→K07소지 시간생략. K08착석보존/행사명40.25~45.25초5초.
새짧은금관·비브라폰화음/천마찰만 로컬합성. 기존C01음악재사용없음/새음성합성없음/대사배속없음. 최종전사9문장검출,실청취아님. 최종PCMpeak0.836466/포화0,약-18.31LUFS·TP-1.45dBTP. 원본SHA불변.
세검수자 실제렌더표본 독립→교차→수정재확인완료. A/B/C-E01 초반콜아웃이조끼지시 문제를시작26.75초/내부페이지앵커로해결. A-E02엔딩그라디언트경계완화. 커프3.5초는선택리듬조정으로남김. 새로운필수시각결함/필수추가생성없음. review_summary.json.
실제청취·발음·말끝·음색·K05립싱크·전체연속재생호흡은미검증. 최종승인/완성본이라부르지않는다. Windows미리보기 C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/edit-v01/. 원본과검토본구분. 다음은사용자실제재생평가및별도승인run07예비컷검수. 구매/공개게시/예약재개없음.
"""
old=read_exact(resume)
if not old.startswith(heading):
    write_exact(resume,entry.replace('\n','\r\n')+'\r\n'+old)
readme=project/'README.md'
old=read_exact(readme)
start=old.index('최신 제작 상태:')
end=old.index('\r\n\r\n',start)
new='최신 제작 상태: [새 3번 「환경까지 가져왔습니다」 **45.25초 첫 전체 편집본**](storyboards/2026-10-20_C03-edit-v01/C03_review_edit_v01_45s.mp4). 기존 원본으로 편집·자막·짧은 음악·엔딩을 구성하고, 3인 독립·교차 화면 표본 검수와 국소 수정을 마쳤습니다. 실제 청취와 연속 재생 확인이 남아 있는 검토본입니다. [편집·검수 안내](storyboards/2026-10-20_C03-edit-v01/) · [직전 커프 보완 원본](storyboards/2026-10-20_C03-flow-run06/). 사용자 추가 요청에 따른 전화 예비 1컷은 [run07 기록](storyboards/2026-10-20_C03-flow-run07/generation_log.json)에서 별도로 관리합니다.'
write_exact(readme,old[:start]+new+old[end:])
brief=project/'team/brief.toml'
old=read_exact(brief)
if '[c03_edit_v01_2026_10_20]' not in old:
    write_exact(brief,old+'\r\n[c03_edit_v01_2026_10_20]\r\nstatus = "45.25초 첫 전체 검토본, 3인 실제 렌더 표본 독립·교차·수정재확인 완료. 실청취/연속재생은 미검증."\r\npath = "storyboards/2026-10-20_C03-edit-v01"\r\nscope = "8씬10편집구간, 기존18원본보존, 이편집 자체 Flow0. 사용자 후속예비1컷명시요청은run07별도."\r\n')

# Run07 now owns its completed generation log; never reset it from this edit script.
print('Historical v01 edit record saved. Newer handoff records may supersede this version.')
