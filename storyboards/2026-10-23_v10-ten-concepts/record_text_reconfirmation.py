from pathlib import Path
import json
R=Path(__file__).resolve().parent
p=R/'text_review.json';d=json.loads(p.read_text(encoding='utf8'))
d['status']='Three independent detailed reviews, cross review and all-three revised-text reconfirmation completed; image review separate'
d['final_durations']=[37.5,39,44.75,37,43,44,43,41,45,46]
d['cross_and_reconfirmation']={
 'A':{'agent':'/root/v10_review_a','peer_issues_reviewed':['B-001','B-002','B-003','B-004','B-005','B-006','B-007','C-001','C-002','C-003','C-004','C-005'],'decision':'All required issues and accepted suggestions resolved; image production may start.','nuances':['B-003 symptom agreed; A treated hook timing as improvement, B as selected-card requirement. Same correction adopted.','B-005 needs a consequence for monopolizing, not added humiliation; blocked view suffices.','A additionally opened only5 existing PNGs: C03 S03/S06 and C05 S06_v2/S07_v3/S08_v2. This is not44-image review.'],'verification':'Actual shot/start/prompt agreement, continuous timings and caption bounds; no new image/motion inspection.'},
 'B':{'agent':'/root/v10_review_b','peer_issues_reviewed':['A-001','A-002','A-003','A-004','A-005','A-006','A-007','C-001','C-002','C-003','C-004','C-005'],'decision':'All required issues and accepted suggestions resolved; image production may start.','nuances':['Initially found unusable-scissors motivation but missed tape-to-main-ribbon attachment; agrees A/C repair.','C-002 more precisely identifies no-height-change instruction conflict than B-I02 tidying suggestion.','B-X01 found old top-level C10 continuity sentence; re-opened current file after normalization and confirmed separately severed offcut.'],'verification':'44/43/41/45/46 revised times, caption bounds, first5seconds reveal, source clue graphic specification.'},
 'C':{'agent':'/root/v10_review_c','peer_issues_reviewed':['A-001','A-002','A-003','A-004','A-005','A-006','A-007','B-001','B-002','B-003','B-004','B-005','B-006','B-007'],'decision':'All required issues and accepted suggestions resolved; image production may start.','nuances':['C09 cannot prove literal teleporting notebook from wording alone; inconsistent prop type still risks generation error and is correctly fixed.','C03 blank plates are not errors; precise compositing specification resolves planning gap, not actual compositing quality.','C05 ordinary descent after installation alone was insufficient for K06-to-K07; new pre-install height adjustment omission resolves.'],'verification':'All10 totals and caption bounds, screen/action agreement, preserved humor mechanisms. No new images or motion inspected.'}
}
for label in ['A','B','C']:
    for issue in d[label]['issues']:issue['pd_status']='adopted and text resolved; see PD_DECISIONS.md and cross_and_reconfirmation'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=R/'storyboards.json';s=json.loads(p.read_text(encoding='utf8'));s['status']='text independently cross-reviewed and reconfirmed; actual new images in production'
for u in s['generation_units']:u['review_status']='text passed; image review pending'
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Three text reconfirmations recorded.')
