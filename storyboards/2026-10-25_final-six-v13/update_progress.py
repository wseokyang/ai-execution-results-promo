raise SystemExit('Historical intermediate updater. Do not overwrite final V13; use generation_log.json and task_status.json.')
from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
g=json.loads((P/'generation_log.json').read_text(encoding='utf-8'))
for e in g['entries']:
 u=e['unit_id']
 if u=='C01_K08_mirror':
  e.update(review='PD sample pass: trainee raises separate arm/leg to mirror coach; coach slightly changes leg angle, accepted natural adjustment. Use1–5.5s; exclude6.5+lowering.',status='ORIGINAL_PRESERVED_PD_CANDIDATE',recommended_interval=[1,5.5],end_frame='inputs/C01_K08_mirror_end.png',generation_mode='Frames start and end')
 if u=='C05_N07_both_palms':
  e.update(review='PD actual0.5s samples: low hand briefly touches ground then lifts; both palms under roof by5s. Use0.5–5.25s; exclude6.5+chest vapour. Roof static on remaining pillars; do not claim continuous load transfer.',status='ORIGINAL_PRESERVED_PD_CANDIDATE',recommended_interval=[.5,5.25],end_frame='inputs/C05_N07_both_palms_end.png',generation_mode='Frames start and end')
 if e.get('end_frame'):e['end_frame_sha256']=sha(P/e['end_frame'])
(P/'generation_log.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=json.loads((P/'task_status.json').read_text(encoding='utf-8'))
d['user_stated_credits']=250
d['known_balance_at_start']={'current_u0':50,'current_u1':0,'current_u2':50,'current_u3':50,'current_u4':50}
d['observed_start_total']=200
d['latest_observed_balances']={'current_u0':10,'current_u1':0,'current_u2':0,'current_u3':0,'current_u4':0}
d['balance_discrepancy_note']='User stated250. Actual five account panels observed total200 at respective first visit; do not invent missing50 or infer refresh time.'
d['requests']=[{k:e.get(k) for k in ['unit_id','take','asset_id','project_url','model','cost_displayed','balance_before','balance_after','status']} for e in g['entries']]
d['preserved_originals']=[{k:e.get(k) for k in ['original','asset_id','sha256','status']} for e in g['entries']]
d['observed_success_net_credits']=sum(e['charge_observed']-e['refund_observed'] for e in g['entries'])
d['pending_generation_requests']=0
d['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(P/'task_status.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('originals',len(g['entries']),'credits',d['observed_success_net_credits'])
