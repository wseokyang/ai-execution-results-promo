"""Record observed UI outcomes and byte-preserved downloads, without service calls."""
from pathlib import Path
import json, hashlib, shutil
P=Path(__file__).resolve().parent
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=json.loads((P/'generation_log.json').read_text(encoding='utf-8'))
rows=[
 ('C03_K05_reaction_take01','13df7133-2ab1-45e9-ab42-5d904802674f','Woman_holding_phone_at_desk_20261020182926.mp4'),
 ('C03_K05_question_take05','6d10f57e-5fe8-40ea-be80-ad865f4aca69','Woman_speaking_on_phone_20261020183037.mp4')
]
for req,(stem,asset,download) in zip(m['requests'],rows):
    original=P/(stem+'.mp4')
    src=Path('C:/Users/wseok/Downloads')/download
    meta=json.loads((P/(stem+'_inspection.json')).read_text(encoding='utf-8'))
    assert hashlib.sha256(src.read_bytes()).hexdigest()==meta['sha256']
    req.update(status='completed_downloaded',asset_id=asset,original=original.name,
      technical=meta,download_sha256_matches=True,original_reencoded=False,
      review_status='see review_summary.json')
m.update(status='two_outputs_preserved_reviewed_separately',ending_credits=0,
         total_deduction=20,total_refund=0,net_credits_used=20,
         cumulative_c03_originals=23,active_generation_count=0,
         silent_fallback_restored_off=True,
         proof='proof/completed_and_mute_off.png')
m['plan_change']='First partial prompt submitted on typeText newline. Last10 reassigned to full question only; planned new pickup not submitted. Existing run03 clean pickup retained.'
m['quality_outcomes']=[
 'Reaction has unrequested ASR speech and phone lowers to chin; original preserved, audio excluded.',
 'Question returned video without audio; no synchronous question voice success.',
 'Partial first1.25s listening picture considered for edit; full acceptance governed by review.'
]
save(P/'generation_log.json',m)
cache=Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/run09')
cache.mkdir(parents=True,exist_ok=True)
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>C03 run09 원본</title><style>body{background:#142029;color:#edf5f6;font:18px/1.6 sans-serif;max-width:1000px;margin:32px auto;padding:16px}video{width:100%}a{color:#8dd9ce}</style>
<h1>C03 추가 원본 · run09</h1><p>Lite10 ×2 · 20→10→0 · 두 원본 그대로 보존. 최종 채택과 생성 완료는 다릅니다.</p>
<h2>01 · 부분 프롬프트로 생성된 반응</h2><p>줄바꿈 입력이 제출로 처리돼 대사 지시 없이 접수됐습니다. 지정하지 않은 음성, 전화 위치 변화로 본편 미채택.</p>
<video controls preload="metadata" src="C03_K05_reaction_take01.mp4"></video><p><a download href="C03_K05_reaction_take01.mp4">원본 MP4 저장</a></p>
<h2>02 · 질문 영상 — 음성 없음</h2><p>전체 질문 프롬프트로 생성했지만 오디오 없이 반환됐습니다. 첫1.25초의 청취 모습만 부분 활용 대상으로 검토했습니다.</p>
<video controls preload="metadata" src="C03_K05_question_take05.mp4"></video><p><a download href="C03_K05_question_take05.mp4">원본 MP4 저장</a></p>
<p>8초 /720p /24fps. 입력 오류와 실제 제출 프롬프트는 generation_log.json에 기록했습니다.</p></html>'''
(P/'originals.html').write_text(html,encoding='utf-8')
for n in [r[0]+'.mp4' for r in rows]+['originals.html','generation_log.json']:
    shutil.copy2(P/n,cache/n)
print('Preserved2 originals;20 used;0 remaining;23 cumulative.')
