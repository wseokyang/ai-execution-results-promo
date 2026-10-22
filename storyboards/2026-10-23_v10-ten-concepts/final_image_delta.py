"""PD resolutions of the independent image reviews; preserves every source PNG."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def put(p,x):(R/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
d=read('storyboards.json');m=read('scene_manifest.json')
cs={c['id']:c for c in d['concepts']}
def shot(cid,kid):return next(s for s in cs[cid]['shots'] if s['id']==kid)
def box(cid,kid,b,text=None):
 q=shot(cid,kid)['caption_cues'][0];q['box']=b
 q['placement']='실제 첫 PNG 위 정지 자막 검수 좌표. 얼굴·손·반전 소품을 피하며 동작 영상 생성 뒤 경로를 다시 확인한다.'
 if text:q['text']=text
def bottom(cid,kid,event=False):
 box(cid,kid,{'left_pct':7,'width_pct':86,'bottom_pct':2 if event else 3,'font_cqw':2.7 if event else 3.1,'title_cqw':4,'padding_pct':0.6})
box('C06','K04',{'left_pct':50,'width_pct':43,'top_pct':4,'font_cqw':3.0})
bottom('C06','K09',True)
for kid in ['K01','K02','K03','K05','K07']:bottom('C07',kid)
bottom('C07','K09',True)
bottom('C08','K01')
box('C08','K02',{'left_pct':43,'width_pct':45,'top_pct':5,'font_cqw':3.1})
bottom('C08','K04')
box('C08','K05',{'left_pct':43,'width_pct':43,'top_pct':5,'font_cqw':3.0})
box('C08','K07',{'left_pct':48,'width_pct':38,'top_pct':5,'font_cqw':2.8})
bottom('C08','K08',True)
for kid,text in [('K02','어떤 순서로\n해봤나요?'),('K04','결과만 보셔도\n됩니다.'),('K06','수정한 쪽도\n궁금한데요.')]:
 box('C09',kid,{'left_pct':36,'width_pct':28,'top_pct':3,'font_cqw':3.0},text)
box('C09','K09',{'left_pct':7,'width_pct':86,'top_pct':2,'font_cqw':2.7,'title_cqw':4,'padding_pct':0.6})
for kid,text in [('K02','끊김 감지 →\n자동 복구'),('K03','더 큰 가위면\n됩니다.'),('K05','복구 시연,\n여기까지.'),('K06','개막은\n해야죠.')]:
 box('C10',kid,{'left_pct':43,'width_pct':31,'top_pct':3,'font_cqw':2.8,'padding_pct':0.6},text)
shot('C10','K06')['caption_cues'][0]['box'].update(left_pct=39,width_pct=28)
bottom('C10','K09',True)
axis='카메라는 무대 안쪽에서 후경 입구를 보는 같은 축을 유지한다. MC는 화면 왼쪽, DV와 정지 장치는 오른쪽. P1은 후경 대기 위치에서 리본을 넘어 카메라 쪽 전경 발표 위치로 이동한다. K09에서 180도 역방향으로 카메라를 바꾸지 않는다.'
c=cs['C10'];c['continuity'][4]='K06 이후 열린 기둥은 무대 양옆 바깥. '+axis+' 리본은 몸·목·손목에 감지 않는다.'
s=shot('C10','K06');s['transition']='같은 축으로 후경 입구에서 대기하는 첫 발표자에게 컷.'
s['framing']+=' 손에서 끝을 건네는 상반신 중심 연결로 짧게 사용하고, 줄의 전체 길이는 K07 와이드 기준으로 맞춘다. K06에서 길어지는 변형을 생성하지 않는다.'
shot('C10','K07')['first_frame']=shot('C10','K07')['first_frame'].replace('중앙 앞에는','리본 뒤 후경 입구 쪽에는')
s=shot('C10','K08');s['screen']=s['screen'].replace('무대 안쪽으로 착지한다','카메라 쪽 전경 발표 위치로 착지한다')
s['continuity_out']='P1은 리본 앞 카메라 쪽 전경 발표 위치에 정상 착지. 리본 정지·느슨함. 폴더는 가슴에 남음.'
s=shot('C10','K09');s['first_frame']=s['first_frame'].replace('이미 무대 안쪽에 착지해','이미 리본 앞 카메라 쪽 전경 발표 위치에 착지해')
s['framing']='같은 축의 미디엄 와이드. 전경 P1 기록과 얼굴, 후경 P2 무릎 준비가 보임. 앞 3초 동작을 보여준 뒤 하단 제목판을 표시해 얼굴과 무릎을 가리지 않는다.'
for kid in ['K07','K08','K09']:
 s=shot('C10',kid)
 s['continuity_in']+=' '+axis
 s['framing']+=' '+axis
mobile='두 황동 의전 팔은 컷 사이 준비 시간에 위치를 조정할 수 있는 이동식 받침대 장치다. 활동 컷과 휴지 컷 사이 재배치 시간은 생략한다. 한 연속 숏 안에서는 시작 PNG의 받침대 위치를 고정하고 관절만 움직인다. 순간 이동이나 바닥을 미끄러지는 자동 이동을 요청하지 않는다.'
c=cs['C09']
c['characters'][2]['description']=c['characters'][2]['description'].replace('자료 받침대 왼쪽 바닥에 고정된','자료 받침대 왼편 이동식 의전 받침대에 부착된')
c['characters'][3]['description']=c['characters'][3]['description'].replace('같은 받침대 오른쪽의','오른편 이동식 의전 받침대의')
if mobile not in c['continuity']:c['continuity'].append(mobile)
for s in c['shots']:
 s['continuity_in']+=' '+mobile
 s['framing']+=' 한 숏 내 두 받침대의 위치는 시작 PNG 그대로 고정.'
for c in d['concepts']:
 for s in c['shots']:
  s['next_motion']=s['screen']
  if 'mute_readability'in s:s['mute_readability']['visible_cause_effect']=s['screen']
  for x in c.get('scene_list',[]):
   if x['cut']==s['id']:x.update(first_frame=s['first_frame'],action=s['screen'])
  for u in d['generation_units']:
   if u['concept_id']==c['id'] and u['linked_shot']==s['id']:
    u.update(first_frame=s['first_frame'],action=s['screen'],framing=s['framing'])
    u['caption_safe_zone']='정확한 후편집 위치는 연결 컷 caption_cues.box 기준. 원본 PNG에는 자막을 넣지 않음.'
    for e in m['images']:
     if e['id']==u['id']:
      e.update(next_motion=s['screen'],camera_notes=s['framing'])
      if c['id']=='C09':e['pd_continuity_override']=mobile+' 실제 이미지 생성 때 제출한 프롬프트는 이력으로 그대로 보존.'
      if c['id']=='C10':e['pd_continuity_override']=axis+' 실제 이미지 생성 때 제출한 프롬프트는 이력으로 그대로 보존.'
put('storyboards.json',d);put('scene_manifest.json',m)
with (R/'PD_DECISIONS.md').open('a',encoding='utf8')as f:
 f.write('\n\n## 최종 이미지 독립검수 반영\n\n- I-B-001 / I-C-001: C10 입장축을 후경 입구→카메라 쪽 전경으로 통일. 180도 반대 컷 설명은 채택하지 않음.\n- I-C-002: C10 K03 가위를 오른쪽 패치로 짧게 옮기는 지시를 shots, scene_list, generation_units, manifest에 동기화.\n- I-A-001 / I-B-002: C09 의전 팔을 재배치 가능한 받침대로 설정. 컷 사이 준비 생략, 한 숏 내 받침대 고정. 실제 제출 이미지 프롬프트는 역사로 보존.\n- I-A-002: C10 K06은 상반신 손전달 중심으로 짧게 연결하고 리본 전체 길이는 K07 기준. 길이 변형 동작 요청 금지.\n- I-B-003 / I-PD-001: 신규 컷별 자막 좌표·글자 크기를 실제 이미지에 맞춰 수정. C10 가운데 벽, C07 하단, C06/C07/C08/C10 마지막은 동작 이후 하단 제목판. 업로드 PNG 원본은 불변.\n')
print('Applied image-review continuity and caption resolutions; original PNGs untouched')
