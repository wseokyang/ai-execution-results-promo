"""Persist observed Flow results; no network/browser actions."""
from pathlib import Path
import json, hashlib, shutil
P=Path(__file__).resolve().parent
def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
log=json.loads((P/'generation_log.json').read_text(encoding='utf-8'))
log.update(status='two_originals_preserved_visual_reviewed_two_audio_failures_refunded',
           ending_credits=20,last_observed_credits=20,total_deductions=70,
           refunds_observed=40,net_credits_used=30,new_originals=2,
           c03_total_originals=21,pending_generation_requests=0,
           silent_fallback_restored_off=True)
for req in log['requests']:
    if 'original_mp4' in req:
        raw=P/req['original_mp4']
        assert digest(raw)==digest(Path(req['download_source']))==req['technical_metadata']['sha256']
        req.update(status='completed_visual_sample_candidate',
                   original_reencoded=False,download_sha256_matches=True,
                   review_record='review_summary.json')
log['remaining_credit_decision']={
    'credits':20,
    'reason':'K05 audio generation failed twice with separate verified20 refunds; no third repeated request. Existing clean pickup and question VO remain usable in edit. Director and visual sample review found no other concrete missing shot justifying a substitute spend.',
    'user_all50_request_fully_spent':False,
    'next':'Keep20. Reassess only if actual viewing/listening identifies a specific defect; no automatic repetitive K05 request.'
}
save(P/'generation_log.json',log)
review={
 'run_id':P.name,'status':'visual sample candidates; integrated edit reviewed separately',
 'method':'Three distinct reviewers independently opened actual32-frame contacts and individual PNGs, then cross-checked other findings.',
 'independent':[
  {'reviewer':'A','K01':'A-R08-V01..04: surface cast shadow PASS; use0–6/6.25; partial overhead underside is optional observation; props stable.',
   'K06':'A-R08-V05..07: first0–2 stable two pages/two hands; separate tracked graphics and matching wide content required.'},
  {'reviewer':'B','K01':'B-R08-V01..04: surface shadow PASS; use0–5.75/6; partial underside noted; full room not revealed.',
   'K06':'B-R08-V05..07: first0–2 stable; two diagrams must remain readable at least1.5s.'},
  {'reviewer':'C','K01':'C-R08-01..03: shadow PASS. Corrected initial no-object claim: small edge at2s, gray underside4s, upper band6s. Complete out-of-frame prompt not met.',
   'K06':'C-R08-04..05: first0–2 stable, two pages independently tracked; blank original alone not discovery.'}
 ],
 'cross_review':{
  'A':'Agrees B/C physical shadow and first2s K06; partial underside accepted only with explicit PD change.',
  'B':'Agrees A/C usage windows and page tracking; record partial reveal honestly.',
  'C':'Agrees A/B; retracts complete non-exposure claim; accepts partial underside as anticipatory cue.'
 },
 'pd_resolution':{
  'K01':'Adopt0–6s. Partial underside is accepted as an approaching-object cue; room-wide reveal still occurs at K02. Not full prompt compliance.',
  'K05':'No output on either new Fast request. HOLD retry after two audio failures/refunds. Existing run03 clean picture and run01 question VO retained.',
  'K06':'Adopt0–2s at edit27.25–29.25. Add same diagrams to closeup and visible surrounding wide pages. Actual final render reviews in edit-v02.',
 },
 'limitations':['Sampled frames, not continuous playback','No actual listening or pronunciation/lip-sync certification','Original AAC presence is not proof of correct speech'],
 'edit':'../2026-10-20_C03-edit-v02/C03_review_edit_v02_46s.mp4'
}
save(P/'review_summary.json',review)
(P/'README.md').write_text('''# C03 run08 — 그림자·기록 비교 보완

50크레딧으로 시작, **순사용30 / 잔액20**. 총4요청 중2성공, 전화 컷2회는 오디오 생성 실패로 각각20환불. 같은 실패를 세 번째 반복하지 않았습니다.

| 컷 | 결과 | 원본 |
| --- | --- | --- |
| K01 take02 · Fast20 | 표면 그림자 개선,0–6초 채택. 상단 물체 하부 일부는 예고로 수용 | [8초 MP4](C03_K01_take02.mp4) |
| K05 planned take05 · Fast20×2 | 오디오 실패2회/환불40, 산출물 없음 | [정확한 제출·차감 기록](generation_log.json) |
| K06 insert take01 · Lite10 | 두 기록 페이지 근접,0–2초에 후편집 도식 | [8초 MP4](C03_K06_insert_take01.mp4) |

[수정 편집본45.75초](../2026-10-20_C03-edit-v02/C03_review_edit_v02_46s.mp4) · [검수](review_summary.json) · [첫 프레임 검수](first_frame_review.json)

원본2개는 다운로드 바이트와 SHA256 일치, 재인코딩 없음. 각8초/1280×720/24fps/H264/AAC,192프레임 디코딩. 누적 C03 원본21개. 3인 실제 프레임 독립·교차 검수이며, 실제 청취·연속 재생 검증은 아닙니다.

남은20은 보존합니다. 기존 K05의 깨끗한 파일 집기 화면과 질문 음성을 편집에 유지했고, 다른 필수 생성 공백은 발견하지 못했습니다. 무음 반환은 K06에만 임시ON한 뒤 실제OFF 복구했습니다.
''',encoding='utf-8')
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><title>C03 run08 원본</title>
<style>body{background:#151d24;color:#edf4f5;font:18px/1.6 sans-serif;max-width:1000px;margin:40px auto;padding:0 20px}video{width:100%}a{color:#83deda}</style>
<h1>C03 보완 원본 2개</h1><p>8초 원본 그대로. 순사용30 / 잔액20. 전화 컷2회는 오디오 실패·환불되어 새 원본이 없습니다.</p>
<h2>K01 · 그림자 보완</h2><video controls preload="metadata" src="C03_K01_take02.mp4"></video><p><a download href="C03_K01_take02.mp4">원본 다운로드</a> · 편집에서는0–6초 사용</p>
<h2>K06 · 기록 비교 근접</h2><video controls preload="metadata" src="C03_K06_insert_take01.mp4"></video><p><a download href="C03_K06_insert_take01.mp4">원본 다운로드</a> · 편집에서 첫2초에 도식을 합성합니다.</p>
<p>실제 청취·최종 승인은 남아 있습니다. 원본과 후편집본을 구분합니다.</p></html>'''
(P/'originals.html').write_text(html,encoding='utf-8')
cache=Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/run08')
cache.mkdir(parents=True,exist_ok=True)
for name in ['C03_K01_take02.mp4','C03_K06_insert_take01.mp4','originals.html','README.md','generation_log.json','review_summary.json','K06_completed_ui.png']:
    shutil.copy2(P/name,cache/name)
    assert digest(P/name)==digest(cache/name)
print('run08 finalized: original2 / net30 / refunded40 / balance20 / total21')
