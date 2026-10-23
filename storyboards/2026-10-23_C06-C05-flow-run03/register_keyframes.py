from pathlib import Path
import json, hashlib, shutil
run=Path(__file__).resolve().parent
cache=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v11-C06-C05-2026-10-23/run03')
log=json.loads((run/'generation_log.json').read_text(encoding='utf-8-sig'))
for q in log['queue']:
    if q['unit_id'] not in ['C06_K04_check','C06_K09_reaction']: continue
    src=run/'new_keyframes'/f"{q['unit_id']}.png"
    dst=run/'inputs'/src.name
    shutil.copy2(src,dst)
    shutil.copy2(src,cache/'inputs'/src.name)
    q.update(sha256=hashlib.sha256(src.read_bytes()).hexdigest(),status='READY',keyframe_review='Three independent reviewers and cross review: PASS. Movement unverified.')
(run/'generation_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review={'reviewers':['/root/final_review_a','/root/v10_review_b','/root/v10_review_c'], 'independent_complete':True,'cross_complete':True,'all_reviewers_opened_both_new_images_and_both_sources':True,'status':'PASS_INPUT_STILLS_ONLY', 'findings':{'C06_K09_reaction':'Same face, long hair, robe and night-office lighting. Small polite smile suitable as start. Visitor shoulder/hair partly visible; hands and full third-person continuity not verified.','C06_K04_check':'Same worker, mustard shirt, glasses, document and two monitor panels. Pen tip above paper and hand plausible. Exact document/UI to be composited later.'},'cross_note':'All three agreed to PD clarification on partial visible visitor shoulder only. No new mandatory still-image issue. Actual motion remains unverified.'}
(run/'keyframe_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Registered two reviewed keyframes')
