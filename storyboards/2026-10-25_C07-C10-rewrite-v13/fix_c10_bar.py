from pathlib import Path
import json,copy
P=Path(__file__).resolve().parent
f=P/'storyboards_draft.json';d=json.loads(f.read_text(encoding='utf-8'))
(P/'storyboards_draft_after_director.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=d['concepts'][3]
def walk(x):
 if isinstance(x,str):
  for a,b in [('자유로운 것은 아래 두 모서리뿐.','하단 전체에 지름1cm·길이1.2m 경량 검정 가로봉을 봉제해 고정한다. 자유로운 것은 가로봉의 양끝이며 손으로 들 때 천은 위쪽으로 고르게 접힌다. 하단 전체가 직선이라 가운데가 늘어져 틈을 가리지 않는다.'),('두 하단 모서리','하단 가로봉 양끝'),('하단 두 모서리','하단 가로봉 양끝'),('아래 두 모서리','하단 가로봉 양끝'),('아래 모서리','아래 가로봉 끝'),('하단 모서리','하단 가로봉 끝'),('천 모서리','천 하단 가로봉 끝'),('자유 모서리','자유 가로봉 끝')]:x=x.replace(a,b)
  return x
 if isinstance(x,list):return[walk(v) for v in x]
 if isinstance(x,dict):return{k:walk(v) for k,v in x.items()}
 return x
c=walk(old);d['concepts'][3]=c
c['layout_plan']['cloth_geometry']['lower_hem_bar']='경량 검정 가로봉 지름0.01m 길이1.2m를 하단 전체에 봉제. 양끝을 잡아 수평으로 들면 천이 위로 고르게 접혀 가운데도1.12m, 낮추면 가운데도0.78m. 한끝만 들 때는 가로봉이 기울며 반대끝은 낮음. 윗가로대와 다른 부품.'
c['props'][1]+=' K02~05는 MG가 봉 한끝만 들어 봉이 기울고 반대끝은 낮다. K06 PR이 반대 봉끝을 넘긴 뒤 MG가 양끝을 같은 높이로 들어 봉 전체를 수평으로 만든다.'
c['shots'][5]['frame_end_description']+=' 하단 가로봉 전체가 수평1.12m이며 천의 중간도 같은 높이로 접혀 흰 틈을 가리지 않는다.'
c['shots'][9]['visual_action']='MG가 무릎을 굽히며 하단 가로봉 양끝을 함께1.12m에서0.78m로 낮춘다. 가로봉은 수평을 유지해 흰 틈 전체를 검정 천으로 덮고 그 자세를 유지한다.'
by={s['scene_id']:s for s in c['shots']}
for sc in c['scenes']:
 shot=by[sc['scene_id']]
 sc['representative_frame']=shot['frame_start_description'];sc['subsequent_motion']=shot['visual_action'];sc['required_end_state']=shot['frame_end_description'];sc['prop_reference']=copy.deepcopy(c['props'])
if 'scene_manifest' in d:
 for i,sc in enumerate(d['scene_manifest']):
  if sc.get('concept_id')=='C10':d['scene_manifest'][i]=copy.deepcopy(next(x for x in c['scenes'] if x['scene_id']==sc['scene_id']))
d['version']='V13_TEXT_REV03_BAR'
d['final_text_delta']='A-07 follow-up: stiff lower hem bar added to prevent center sag hiding the intended bright gap; C10 props/shots/scenes synchronized. Await final targeted reconfirm.'
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('updated C10 lower bar')
