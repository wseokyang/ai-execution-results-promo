from pathlib import Path
import json, shutil, hashlib
P=Path(__file__).resolve().parent
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log=json.loads((P/'generation_log.json').read_text(encoding='utf-8'))
meta=json.loads((P/'C03_K05_take04_inspection.json').read_text(encoding='utf-8'))
log.update(status='completed_original_preserved_visual_hold',ending_credits=0,
           net_credits_used=10,refunds_observed=0,new_originals=1,c03_total_originals=19,pending_generation_requests=0)
req=log['requests'][0]
req.update(status='completed_visual_hold',asset_id='0feaa025-4f16-459c-8789-90638fb897ff',
           original_mp4='C03_K05_take04.mp4',download_source='C:/Users/wseok/Downloads/Woman_speaking_on_phone_20261020152831.mp4',
           technical_metadata=meta,original_reencoded=False,download_sha256_matches=True,review_record='review_summary.json')
log['quality_decision']={'status':'HOLD_direct_picture_adoption','reason':'At 1.0s a coiled telephone cable appears and persists. The question ASR interval 0.75–2.05s crosses the defect. Keep edit v01 unchanged.',
 'audio':'ASR has target question 0.75–2.05s and uncertain extra recognition 6.22–6.90s. No actual listening or lip-sync verification.'}
save(P/'generation_log.json',log)
review={'run_id':P.name,'actual_review':'Three distinct reviewers opened 32-frame contact sheet and individual actual frames, with run03 clean take comparison.',
 'independent':[
 {'reviewer':'A','issues':[{'id':'A-R07-01','priority':'required_before_adoption','result':'HOLD','detail':'Cable appears at 1.0s and persists; clean opening cannot contain full question.'},{'id':'A-R07-02','priority':'optional','detail':'Head direction jump to desk-facing pickup needs edit check.'},{'id':'A-R07-03','priority':'unverified','detail':'Audio and lip sync not listened/verified.'}]},
 {'reviewer':'B','issues':[{'id':'B-R07-01','priority':'required_before_adoption','result':'HOLD','detail':'Black coil between phone and desk from 1.0s.'},{'id':'B-R07-02','priority':'optional','detail':'New head turn and old pickup direction differ.'},{'id':'B-R07-03','priority':'unverified','detail':'ASR alone not speech approval.'}]},
 {'reviewer':'C','issues':[{'id':'C-R07-01','priority':'required_before_adoption','result':'HOLD','detail':'Coil during question interval.'},{'id':'C-R07-02','result':'PASS_sampled','detail':'Two hands, one phone, closed folder fixed.'},{'id':'C-R07-03','priority':'optional','detail':'Head direction continuity.'}]}],
 'cross_review':{'A':'Agrees B/C cable HOLD; audio-only possible after listening, not synchronous picture solution.',
 'B':'Agrees A/C cable HOLD; do not claim silent tail from prompt or ASR.',
 'C':'Agrees A/B direct-picture HOLD; keep current edit; new smartphone first frame instead of identical retry.'},
 'pd_resolution':'Preserve raw; no replacement in v01. Latest explicit 50-credit user request authorizes run08 with changed first frame.',
 'limitations':['sampled frames, not continuous playback','no actual listening','no certified pronunciation or lip sync']}
save(P/'review_summary.json',review)
(P/'README.md').write_text('# C03 run07 — 전화 질문 예비 컷\n\nLite 10크레딧, 실제 10→0. 원본 8초/720p/24fps, 재인코딩 없음.\n\n[원본 MP4](C03_K05_take04.mp4) · [검수](review_summary.json) · [생성 기록](generation_log.json)\n\n1초부터 코일 전화선이 생겨 본편 화면 채택 보류. 기존 45.25초 v01 유지. 자동전사는 실제 청취가 아니다.\n',encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>C03 run07 원본</title><style>body{background:#151b20;color:white;font:18px sans-serif;max-width:1000px;margin:40px auto}video{width:100%}</style><h1>C03 K05 take04 · 원본</h1><p>8초 / Lite10 / 잔액0. 1초부터 전화선이 생겨 화면 채택 보류. 최종 편집본이 아닙니다.</p><video controls src="C03_K05_take04.mp4"></video><p><a href="C03_K05_take04.mp4" download>원본 다운로드</a></p>'
(P/'originals.html').write_text(html,encoding='utf-8')
cache=Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/run07')
cache.mkdir(parents=True,exist_ok=True)
for n in ['C03_K05_take04.mp4','originals.html','completed_ui.png']:
 shutil.copy2(P/n,cache/n)
assert hashlib.sha256((cache/'C03_K05_take04.mp4').read_bytes()).hexdigest()==meta['sha256']
print('run07 finalized; raw preserved; direct picture HOLD')
