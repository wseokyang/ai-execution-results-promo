from pathlib import Path
import json,shutil
r=Path(__file__).parent;p=r/'generation_log.json';d=json.loads(p.read_text(encoding='utf-8-sig'))
for e in d['entries']:
    if e['unit_id'] in ['C01_K01','C01_K02'] and e['take']==1:
        e.update(status='FAILED_AUDIO_GENERATION',error_visible='오디오를 생성할 수 없습니다',refund_notice_visible=True,refund_expected=10,refund_observation='Both failed 10-credit requests; later account balance restored to20. Collective return20 confirmed, individual transaction page not opened.',audio_return_setting_at_submission=False,original=None)
        shutil.copyfile(r/e['prompt'],r/'submitted_prompts'/f"{e['unit_id']}_take02.txt")
d['audio_return_setting_change']={'value':True,'reason':'No essential speech per user brief; enable silent return to avoid audio-only failure. Switch Value1 observed after UI update.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
