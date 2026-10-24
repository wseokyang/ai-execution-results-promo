from pathlib import Path
import json,hashlib,datetime
r=Path('storyboards/2026-10-24_C05-first-flow-run01');p=r/'generation_log.json';d=json.loads(p.read_text(encoding='utf-8-sig'))
d['status']='N04_SUBMITTED_RESULT_PENDING'
d['entries'].append({'unit_id':'C05_N04','take':1,'input':'inputs/C05_N04.png','input_sha256':hashlib.sha256((r/'inputs/C05_N04.png').read_bytes()).hexdigest(),'source':'N03take01 actual frame7.5s','prompt':'submitted_prompts/C05_N04_take01.txt','status':'SUBMITTED_RESULT_PENDING','balance_before':180,'model':'Veo 3.1 Lite','cost_displayed':10,'duration_requested':8,'resolution_requested':'720p','ratio_requested':'16:9','outputs':1,'submitted_at_recorded':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repair_reason':'Outward body/face turn only; edge grip accepted as creative change, no repeated underside correction','credit_note':'C02K01,K02,K03 interleaved whileN03review caused210->180; refreshedC05tabbeforeactualbalancecheck'})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
