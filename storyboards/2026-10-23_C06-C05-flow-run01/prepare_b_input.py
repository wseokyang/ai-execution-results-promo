import hashlib, json, pathlib
root=pathlib.Path(__file__).resolve().parent
p=root/'generation_log.json'
d=json.loads(p.read_text(encoding='utf-8'))
q=next(q for q in d['queue'] if q['unit_id']=='C05_K02B')
q['reference_plan_image']=q['source_image']
q['source_image']='storyboards/2026-10-23_C06-C05-flow-run01/input_frames/C05_K02B_from_K02A_take01_7.750s.png'
f=root/'input_frames/C05_K02B_from_K02A_take01_7.750s.png'
q['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
q['upload_path']='C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v11-C06-C05-2026-10-23/'+f.name
q['input_source_video']='C05_K02A_take01.mp4'
q['input_source_time_seconds']=7.75
q['note']='A/B/C independently confirmed 7.750s extracted frame satisfies B starting state. Not the final decoded frame. Preserve chipped porch edge and debris.'
old=root/q['planned_prompt']
new=root/'submitted_prompts/C05_K02B_from_A_planned.txt'
prompt=old.read_text(encoding='utf-8').strip()+' The supplied image is the approved 7.750-second frame of the preceding source video. Preserve the existing chipped front-left porch edge and small concrete debris exactly; do not restore the removed pillar or repair the edge. Keep the detached pillar on the far left ground. Fixed camera, same monster body and neck length, no shrinking. The giant visibly bends its knees and long neck to fit under the lower porch.'
new.write_text(prompt+'\n',encoding='utf-8')
q['planned_prompt']='submitted_prompts/'+new.name
pathlib.Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v11-C06-C05-2026-10-23/'+new.name).write_text(prompt+'\n',encoding='utf-8')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(q['source_image'],q['sha256'])
