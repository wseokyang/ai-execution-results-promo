from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent;P=R.parent/'2026-10-19_v8-flow-preflight';S=R.parent/'2026-10-19_tone-polish-v8'
if (R/'generation_log.json').exists():raise SystemExit('Run already initialized; preserve existing submission history and prompts. Use a new run for new initialization.')
stage=Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-19');stage.mkdir(parents=True,exist_ok=True)
(R/'prompts').mkdir(exist_ok=True)
data=json.loads((P/'clip_manifest.json').read_text(encoding='utf-8'))
queue=[]
for unit in data['visual_units']:
 if unit['concept_id']!='C03':continue
 cid=unit['id'];source=P/unit['source_image'];dest=stage/(cid+'.png');shutil.copy2(source,dest)
 text=(P/'prompts'/(cid+'.txt')).read_text(encoding='utf-8');text='\n'.join(text.splitlines()[2:])
 text='8초, 16:9, 720p. 한 개의 연속 숏.\n'+text
 text+='\n동작과 대사는 앞부분부터 자연스럽게 진행하고, 완료된 뒤에는 같은 구도를 유지하며 편집용 여유를 남긴다. 8초를 채우기 위해 말을 느리게 늘리거나 새 대사를 추가하지 않는다.\n'
 if cid=='C03_K03':text+='기사는 오른손 장갑 한 짝만 벗는다. 다음 컷에서 같은 오른손 장갑을 다시 낀다.\n'
 if cid=='C03_K04':text+='A 청록 방은 왼쪽 설치 완료, B 주황 방은 오른쪽으로 들어온다. 기사는 오른손 장갑 한 짝을 다시 낀다.\n'
 (R/'prompts'/(cid+'_take01_planned.txt')).write_text(text,encoding='utf-8')
 queue.append({'cut_id':cid,'take':1,'status':'not_submitted','input_image':'../'+S.name+'/'+str(source.relative_to(S) if source.is_relative_to(S) else Path(unit['source_image']).parts[-3]+'/'+Path(unit['source_image']).parts[-2]+'/'+Path(unit['source_image']).parts[-1]),'source_image':str(source.resolve()),'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'staging_image':str(dest),'planned_prompt_file':'prompts/'+cid+'_take01_planned.txt','planned_model':'Veo 3.1 - Lite','planned_seconds':8,'preflight_recommended_seconds':unit['generation_seconds'],'live_ui_quote_credits':10,'input_submitted':False,'generation_id':None,'original_mp4':None,'audio_verified':False})
log={'run_id':R.name,'concept':'C03 환경까지 가져왔습니다 (accepted V8, not legacy C03)','authorization':'2026-10-19 user: 3번부터 flow로 영상만들자','project_url':'https://flow.google.com/project/c105a8ef-b295-4fc4-907c-1eb8e025245d','project_title':'C03 환경까지 가져왔습니다 · V8 제작','account_label':'existing main Chrome PLUS account; no account switch','starting_credits':50,'last_observed_credits':50,'credits_spent_confirmed':0,'settings':{'model':'Veo 3.1 - Lite','mode':'Frames first only','ratio':'16:9','resolution':'720p','seconds':8,'outputs':1,'quoted_credits_per_request':10,'duration_deviation':'Actual Lite UI exposes no duration control; composer remains8s. Use8s sources and trim, rather than assume6s availability from docs.','silent_return_setting':'not yet inspected'},'status':'preparing; recaptcha connection warning seen before any generation request; one ordinary reload','planned_first_batch':['C03_K01','C03_K02','C03_K03','C03_K04','C03_K05'],'queue':queue,'audio_reserve':data['audio_reserve'][0],'events':[{'event':'created new dedicated project','generation_submitted':False},{'event':'observed50credit balance andLite10quote','generation_submitted':False},{'event':'reCAPTCHA service connection warning before submission; ordinary reload once','generation_submitted':False}],'automation_resumed':False,'purchases':0}
(R/'generation_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Saved queue and planned prompts,8 staged images. No generation submitted.')
