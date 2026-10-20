from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent
P.joinpath('prompts').mkdir(exist_ok=True)
P.joinpath('images').mkdir(exist_ok=True)
R8=P.parent/'2026-10-20_C03-flow-run08'
shutil.copy2(R8/'images/C03/K05_smartphone_v2.png',P/'images/C03_K05_smartphone.png')
for name in ['inspect_media.py','transcribe_sources.py']:
    shutil.copy2(R8/name,P/name)
prompt='''8-second realistic live-action shot continuing from the first frame. Fixed camera, the same woman and room. Her left hand keeps the same flat black cordless smartphone at her left ear. Her right hand rests on the same closed orange folder on the desk.
In a calm natural Korean female conversational voice, she asks once: "이건 왜 보냈어요?" Begin after a brief pause, finish the short question naturally, then close her mouth and listen. Keep her head orientation and both hands steady. No additional words, no file handling, no phone cable, no other people. Quiet room ambience, no music, no captions.'''
(P/'prompts/C03_K05_question_take05_planned.txt').write_text(prompt,encoding='utf-8')
log={
 'run_id':P.name,'status':'prepared',
 'user_authorization':'20 다 사용해서 모자란 부분 다 완성하고 영상 편집까지 시작하자',
 'supersedes':'Previous preserve20 recommendation; user explicitly reauthorizes20 spend. New split-shot Lite workflow, not same failed Fast request.',
 'project_url':'https://flow.google.com/project/c105a8ef-b295-4fc4-907c-1eb8e025245d',
 'account_label':'Current user-selected PLUS account; no agent switching',
 'starting_credits':20,'last_observed_credits':20,
 'plan':[{'cut':'C03_K05_question','take':5,'model':'Veo3.1 Lite','cost':10},
         {'cut':'C03_K05_pickup','take':1,'model':'Veo3.1 Lite','cost':10}],
 'input_start':'images/C03_K05_smartphone.png',
 'input_sha256':hashlib.sha256((P/'images/C03_K05_smartphone.png').read_bytes()).hexdigest(),
 'settings_observed':{'mode':'Frames first only','ratio':'16:9','resolution':'720p','seconds':8,'outputs':1,'model':'Veo3.1 Lite','cost':10,'silent_fallback':True},
 'reason':'Improve synchronous question picture and same-phone same-angle file pickup. Voice fallback may produce no audio; actual result must be verified.',
 'requests':[],
 'constraints':'No new purchase, account switching, paid upscale, public post, automation resume. Restore silent fallbackOFF. Preserve all originals and prior edits.'
}
(P/'generation_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('run09 prepared, two Lite10 shots planned')
