import argparse, json, hashlib
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('cut'); p.add_argument('--before',type=int); p.add_argument('--after',type=int)
p.add_argument('--project'); p.add_argument('--alias'); p.add_argument('--frame'); p.add_argument('--take',type=int,default=1)
p.add_argument('--id'); p.add_argument('--download'); p.add_argument('--status'); p.add_argument('--note')
p.add_argument('--end')
a=p.parse_args(); root=Path(__file__).parent; f=root/'generation_log.json'
j=json.loads(f.read_text(encoding='utf-8-sig'))
r=next((x for x in j['generation_requests'] if x['cut_id']==a.cut and x['take']==a.take),None)
if r is None:
    assert a.before is not None and a.after is not None and a.project and a.alias and a.frame
    r=dict(cut_id=a.cut,take=a.take,project_url=a.project,account_alias=a.alias,model='Veo 3.1 Lite',credits_displayed=10,balance_before=a.before,balance_after=a.after,credits_charged=a.before-a.after,refund_observed=0,status='submitted_result_pending',first_frame=a.frame,prompt_file=f'prompts/{a.cut}_take{a.take:02}.txt',duration_requested=8,resolution_requested='720p',aspect_ratio='16:9',output_count=1)
    cache=Path('C:/Users/wseok/.cache/codex-flow/C08-C09-v15-2026-10-26')/f'{a.cut}_take{a.take:02}.txt'
    (root/r['prompt_file']).write_bytes(cache.read_bytes())
    j['generation_requests'].append(r)
if a.id:r['generation_id']=a.id
if a.status:r['status']=a.status
if a.note:r['review_note']=a.note
if a.end:r.update(last_frame=a.end,input_mode='first_and_last_frames')
if a.download:
    src=Path('C:/Users/wseok/Downloads')/a.download
    dest=root/f'{a.cut}_take{a.take:02}.mp4'
    assert src.is_file() and src.stat().st_size>10000
    dest.write_bytes(src.read_bytes())
    r.update(original_file=dest.name,downloaded_as=src.name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='completed_downloaded_review_pending')
f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(a.cut,r['status'],r.get('balance_after'))
