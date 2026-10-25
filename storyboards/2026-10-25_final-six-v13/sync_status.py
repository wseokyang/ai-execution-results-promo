raise SystemExit('Historical intermediate updater. Do not restore incomplete balances/status over the final ledger.')
from pathlib import Path
import json,datetime
P=Path(__file__).resolve().parent
f=P/'task_status.json'
d=json.loads(f.read_text(encoding='utf-8'))
g=json.loads((P/'generation_log.json').read_text(encoding='utf-8'))
d['preserved_originals']=[{k:e.get(k) for k in ['unit_id','take','asset_id','model','charge_observed','refund_observed','balance_before','balance_after','status']} for e in g['entries']]
d['observed_success_net_credits']=sum((e.get('charge_observed') or 0)-(e.get('refund_observed') or 0) for e in g['entries'])
assert d['observed_success_net_credits']<=d['credit_budget']
d['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(d['observed_success_net_credits'],len(g['entries']))
