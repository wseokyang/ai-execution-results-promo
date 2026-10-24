from pathlib import Path
import json,shutil
r=Path(__file__).parent;p=r/'generation_log.json';d=json.loads(p.read_text(encoding='utf-8-sig'))
e=next(e for e in d['entries'] if e['unit_id']=='C01_K05' and e['take']==1)
e.update(status='FAILED_AUDIO_GENERATION',error_visible='오디오를 생성할 수 없습니다',refund_notice_visible=True,refund_observed=10,refund_observation='After five10-credit requests from50, account balance10 observed with only K05 failed. UI explicitly says refund.',audio_return_setting_at_submission=False,original=None)
shutil.copyfile(r/e['prompt'],r/'submitted_prompts/C01_K05_take02.txt')
d['current_u1_silent_return_enabled']=True
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
