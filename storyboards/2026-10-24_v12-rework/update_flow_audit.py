from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
r=root/'storyboards/2026-10-24_v12-C02-C04-C01-flow'
p=r/'generation_log.json'; d=json.loads(p.read_text(encoding='utf-8-sig'))
for e in d['entries']:
    if e['unit_id']=='C02_K07' and e['take']==1:
        e.update(status='NO_RESULT_CREDIT_RETURN_INFERRED',refund_observed=None,refund_inferred=10,
            reconciliation_note='K07 only missing among 9 requests. Later balance 120 rather than arithmetic 110; 110 was not directly observed. Ten-credit return and attribution to K07 are inferred, not an explicit refund notice. No error cause shown.')
    if e['unit_id']=='C02_K09':
        e.update(charge_observed=None,charge_expected=10,balance_observation_note='120 before request and 120 after reconciliation include inferred credit return from missing K07. This is not evidence of a free K09 request.')
checks={
'C02_K01':'Photograph/cord actions visible. Candidate; text/graphics remain post-production.',
'C02_K02':'Detective blocks technician and inspector directs attention. Candidate subject to edit continuity.',
'C02_K03':'Mouse/pointing action and monitor present. Actual graphics need post-production.',
'C02_K04':'Cloth contacts orange-edged protective window; monitor remains marked pending later scan. Exact monitor overlay required.',
'C02_K05':'Cuff fastening visible, but free cuff ends hanging below window whereas K06 starts with ring over window. Mandatory continuity review before final edit; not unconditional pass.',
'C02_K06':'Button press/monitor attention visible; opening cuff position differs from prior clip. Exact screen overlay required.',
'C02_K07':'Take02 phone rises, framing and photography gesture visible. Candidate; phone screen continuity review remains.',
'C02_K08':'Photo placement/pinning visible; surrounding board unchanged in sampled frames.',
'C02_K09':'Two people point to board/photo, ending area available. Candidate.'}
for e in d['entries']:
    if e.get('original') and e['unit_id'] in checks:
        e['pd_sample_review']=checks[e['unit_id']]
        e['review_scope']='16 half-second sampled frames/contact sheet; selected frames as needed. Not full playback or audio listening. Independent reviewers pending.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=r/'queue.json'; q=json.loads(p.read_text(encoding='utf-8-sig'))
for unit in q['entries']:
    matches=[e for e in d['entries'] if e['unit_id']==unit['unit'] and e.get('original')]
    if matches:
        unit['status']='ORIGINAL_PRESERVED_REVIEW_PENDING'; unit['selected_take_candidate']=matches[-1]['take']
p.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
p=root/'storyboards/2026-10-24_C05-first-flow-run01/generation_log.json';d=json.loads(p.read_text(encoding='utf-8-sig'))
for e in d['entries']:
    if e['unit_id']=='C05_N04':
        e['review']='HOLD_FULL_CLIP_PARTIAL_TURN_ONLY'
        e['pd_sample_review']='0–2.0s partial outward turn candidate. At ~3.0–3.5s long neck morphs into extra-arm-like shape; later hands release. Never use as a verified complete turn. Director recommends a real worker/jack insert to cover remaining orientation adjustment, followed by existing K04; render review required.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Reconciliation and sampled reviews recorded; no source media changed.')
