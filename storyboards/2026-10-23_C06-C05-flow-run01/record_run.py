import argparse, datetime, hashlib, json, pathlib, shutil

root = pathlib.Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('action', choices=['submit','download'])
p.add_argument('unit')
p.add_argument('--account', default='current_u4')
p.add_argument('--project', default='https://flow.google.com/u/4/project/f39087d0-f9af-4536-914d-bfad137c481b')
p.add_argument('--before', type=int)
p.add_argument('--after', type=int)
p.add_argument('--title')
p.add_argument('--asset')
p.add_argument('--file')
p.add_argument('--take', type=int, default=1)
p.add_argument('--prompt-file')
p.add_argument('--reason')
a=p.parse_args()
logpath=root/'generation_log.json'
log=json.loads(logpath.read_text(encoding='utf-8-sig'))
q=next(x for x in log['queue'] if x['unit_id']==a.unit)
if a.action=='submit':
    assert not any(x['unit_id']==a.unit and x['take']==a.take for x in log['requests']), 'Already submitted'
    prompt=(root/(a.prompt_file or q['planned_prompt'])).read_text(encoding='utf-8-sig').strip()
    pf=f'submitted_prompts/{a.unit}_take{a.take:02}.txt'
    (root/pf).write_text(prompt+'\n',encoding='utf-8')
    r=dict(unit_id=a.unit,take=a.take,account_alias=a.account,project_url=a.project,
           recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           status='ACCEPTED',ui_title=a.title,prompt_file=pf,prompt=prompt,
           input_image=q['source_image'],input_sha256=q['sha256'],
           model='Veo 3.1 - Lite',requested_duration_seconds=8,
           requested_resolution='720p',aspect_ratio='16:9',outputs=1,
           quoted_cost=10,start_balance=a.before,after_submission_balance=a.after,
           observed_debit=a.before-a.after,refund=0,generation_id=None,
           original_file=None,review_status='PENDING_VISUAL_REVIEW')
    if a.reason: r['regeneration_reason']=a.reason
    log['requests'].append(r)
    q['status']='ACCEPTED'
else:
    r=next(x for x in log['requests'] if x['unit_id']==a.unit and x['take']==a.take)
    src=pathlib.Path(a.file)
    assert src.suffix.lower()=='.mp4' and src.is_file()
    dest=root/f'{a.unit}_take{a.take:02}.mp4'
    digest=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    if not dest.exists(): shutil.copy2(src,dest)
    assert digest(src)==digest(dest)
    r.update(status='DOWNLOADED',asset_id=a.asset,ui_title=a.title or r['ui_title'],
             original_file=dest.name,download_source_path=str(src),
             original_sha256=digest(dest),original_bytes=dest.stat().st_size)
    q['status']='DOWNLOADED'
log['flow_requests']=len(log['requests'])
log['downloaded_originals']=sum(x['status']=='DOWNLOADED' for x in log['requests'])
logpath.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(a.action,a.unit,log['downloaded_originals'],'originals',len(log['requests']),'requests')
