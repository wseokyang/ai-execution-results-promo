from pathlib import Path
import json,hashlib,datetime,argparse
a=argparse.ArgumentParser()
a.add_argument('unit'); a.add_argument('--take',type=int,default=1); a.add_argument('--before',type=int,required=True); a.add_argument('--after',type=int); a.add_argument('--project',required=True);a.add_argument('--account',default='current_u0');a.add_argument('--status',default='SUBMITTED_RESULT_PENDING');v=a.parse_args()
r=Path(__file__).parent;p=r/'generation_log.json'
d=json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else {'run_id':r.name,'entries':[],'priority':['C02','C04','C01']}
e=next((e for e in d['entries'] if e['unit_id']==v.unit and e['take']==v.take),None)
if e is None:
 e={'unit_id':v.unit,'take':v.take,'input':f'inputs/{v.unit}.png','prompt':f'submitted_prompts/{v.unit}_take{v.take:02d}.txt'}
 d['entries'].append(e)
e.update({'status':v.status,'balance_before':v.before,'account_alias':v.account,'project_url':v.project,'model':'Veo 3.1 Lite','cost_displayed':10,'duration_requested':8,'resolution_requested':'720p','ratio_requested':'16:9','outputs':1,'input_sha256':hashlib.sha256((r/e['input']).read_bytes()).hexdigest(),'submitted_at_recorded':datetime.datetime.now(datetime.timezone.utc).isoformat()})
if v.after is not None: e['balance_after']=v.after
d['status']='IN_PROGRESS';p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=r/'queue.json';q=json.loads(p.read_text(encoding='utf-8-sig'))
next(x for x in q['entries'] if x['unit']==v.unit)['status']=v.status
p.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
