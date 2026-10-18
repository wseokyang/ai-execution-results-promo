from pathlib import Path
import json,copy,re
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def write(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=read('storyboards.json')
assert d['status']=='text_review_pending'
write('storyboards_before_text_revision.json',d)
cs={c['id']:c for c in d['concepts']}
def shot(cid,n):return next(s for s in cs[cid]['shots'] if s['id']==f'K{n:02d}')
def setshot(cid,n,**kw):shot(cid,n).update(kw)
setshot('C01',2,dialogue='T: “AI 잘 쓴 사람의 각도.”',screen='T가 큰 포스터 속 P의 어깨 각도를 짚는다. L1이 똑같이 과하게 기울자 T가 엄숙히 손끝까지 고친다.',next_motion='L1이 상체 각도를 조금 더 기울이고 손끝을 편다. T가 엄숙히 한 번 고개를 끄덕인다.')
setshot('C01',4,
 screen='포스터와 큰 모니터를 한 화면에서 비교한다. 원본의 첫 자세는 포스터와 같다. 다음 순간 바퀴 의자가 옆으로 빠지며 P의 몸이 매트 쪽으로 풀썩 낮아진다. 멋있게 뻗은 손은 균형을 잡으려던 손이었다.',
 first_frame='왼쪽 포스터는 하늘색 셔츠 P의 비스듬한 상체와 오른손만 크롭한다. 오른쪽 모니터의 더 넓은 원본은 같은 사람·같은 순간·같은 손모양이며, 그 아래 비스듬히 빠지기 시작한 바퀴 의자와 매트가 처음 보인다. P는 아직 바닥에 앉기 전이다.',
 next_motion='고정된 큰 모니터 안에서 의자가 옆으로 밀려 빠지고 P가 매트에 낮게 풀썩한다. 오른손이 균형을 잡다 내려간다. 포스터는 움직이지 않아 원인과 크롭의 차이가 보인다.',
 continuity_out='사진의 전체 맥락을 실제 동작으로 확인. P는 매트에 낮아졌고 의자는 옆으로 밀림.')
setshot('C01',6,
 screen='T는 의자 끝에서 사진의 손모양을 잡다가 의자가 빠지며 매트에 벌렁 눕는다. 몸이 우스꽝스럽게 뒤집혔는데도 오른팔과 굽힌 무릎을 꼿꼿이 유지하며 원래 계획한 마지막 단계인 척한다.',
 next_motion='의자가 옆으로 밀리자 T의 몸이 매트에 낮게 풀썩 뒤집힌다. 곧바로 오른팔과 굽힌 무릎을 굳혀 의도한 자세인 척한다. 충격 자체보다 멈춰서 권위를 지키는 표정에 집중한다.',
 continuity_out='T는 매트에 등을 대고 무릎 하나를 굽혀 올린 과장된 자세. 오른팔은 여전히 사진처럼 들려 있음.')
setshot('C01',7,
 screen='A가 매트에 벌렁 누운 T를 아주 진지하게 촬영한다. T는 오른팔과 굽힌 무릎을 고정한 채 턱만 들어 사진을 의식한다. 뒤의 L2가 자기 무릎과 T를 번갈아 본다.',
 first_frame='T는 등을 매트에 대고 한 무릎을 굽혀 올린 채 오른팔을 들고 있다. A는 무릎을 꿇고 카메라를 향한다. L2는 아직 서 있지만 T의 굽힌 무릎을 유심히 보고 있다.',
 next_motion='A가 셔터를 누른다. T는 자세를 더 굳히고 L2가 그 옆 매트로 몸을 낮추기 시작한다.',
 framing='고정 낮은 미디엄 와이드. 뒤집힌 코치의 온몸과 카메라, 서 있는 L2의 비교 시선을 함께.',
 continuity_in='K06의 벌렁 누운 T, 오른팔·한 무릎 고정.',continuity_out='조수는 사고를 새 교본으로 촬영. L2가 옆에서 같은 자세로 내려감.')
setshot('C01',8,
 screen='T와 L2가 나란히 매트에 누워 오른팔과 한 무릎을 들어 같은 이상한 자세를 취한다. L2가 코치를 흘끗 보고 발끝까지 맞추자 T가 만족스럽게 눈으로 승인한다.',
 first_frame='두 사람은 이미 나란히 매트에 등을 댄 채 오른팔과 한 무릎을 들고 있다. L2의 발끝 각도만 T와 다르다. A는 둘을 함께 촬영한다.',
 next_motion='L2가 발끝을 T와 같은 방향으로 꺾는다. T가 눈으로 만족을 표시하고 A의 셔터가 한 번 울린다.',
 continuity_in='새 교본 촬영을 본 L2가 T 옆에 같은 자세로 누운 시간 생략.',continuity_out='둘은 뒤집힌 자세마저 완벽하게 복제한 채 고정.')
setshot('C01',9,
 screen='넓은 체육관. 매트의 T·L2는 나란히 뒤집힌 자세를 고집하고 A는 새 교본을 촬영한다. 두 사람이 떠난 왼쪽 문이 닫힌다. 비어 있는 좌상단 벽에 행사명을 6초 유지한다.',
 first_frame='K08의 나란히 누운 T·L2와 조수. 팔과 굽힌 무릎 자세 유지, 좌상단 벽은 텍스트 없는 여백.',
 continuity_in='K08의 뒤집힌 두 인물·사진 촬영 유지.')
cs['C01']['continuity'][2]='원본의 P와 교습소 코치가 같은 상체 사진의 맥락을 다르게 다룬다. 원본은 의자가 빠진 낮은 풀썩, 코치는 벌렁 누운 우스꽝스러운 결과까지 의도한 단계라고 우긴다. 두꺼운 매트와 가벼운 의자, 통증보다 허세 연기.'
cs['C01']['final_action']='코치와 남은 수강생이 매트 위에 나란히 뒤집힌 자세를 고집하고 조수가 새 교본을 찍는다. 실제 작업 이야기를 들으러 떠난 인물과 대비하며 참석을 초대한다.'
cs['C01']['reveal_test']['마지막그림']='사고로 벌렁 누운 코치의 팔·굽힌 무릎·발끝까지 따라 한 제자, 그 둘을 엄숙하게 찍는 조수.'

setshot('C02',6,next_motion='ST가 훅을 풀려는 순간 F2가 짧게 돌아본다. ST는 손을 거두고 그대로 한쪽 무릎을 바닥에 댄다. 벨트는 풀지 않는다.',screen='ST가 쉽게 풀리는 훅에 손을 대려 한다. 팬 F2가 한 번 돌아보자 자기가 지키겠다고 한 체면 때문에 손을 거두고 즉시 몸을 낮춘다. 빈 옆 통로는 테이블까지 이어진다.')
setshot('C02',8,next_motion='ST가 BG에게 계속하라는 작은 고갯짓을 한다. 뒤쪽을 향한 경호 손바닥은 그대로 유지한다.',screen='ST는 맨 앞 바닥에 쪼그려 앉아 노트북을 올려다본다. 뒤쪽으로는 여전히 경호하듯 손바닥을 편 채 아무 일 없다는 듯 계속하라고 한다.')

setshot('C04',1,subtitle='첫 2초 후편집 작은 표기: ‘가상의 AI 비서 테스트’',next_motion='비서들이 레버를 잡자마자 동시에 멈추고 먼저 가라는 자유로운 손바닥을 서로 내민다. K02의 과한 정중 동작으로 바로 이어진다.')
setshot('C04',8,
 screen='HY가 문을 놓으려고 무릎을 크게 굽히지만 HB는 자기 쪽을 허리 높이에 받치고 있다. 문짝이 눈에 띄게 비스듬해진다. 서로 먼저 하라는 인사를 주고받다가 HY가 도로 일어서 문이 수평으로 돌아온다.',
 first_frame='가로로 들던 문이 HY 쪽으로 이미 기울기 시작한다. HY는 무릎을 굽히고 HB는 똑바로 서서 반대 끝을 허리 높이에 받친다. 자세 차이와 큰 문 대각선이 한눈에 읽힌다.',
 next_motion='HY가 무릎을 더 굽혀 문을 크게 기울인다. HB가 계속 버티며 먼저 하라고 인사하자 HY가 도로 일어나 수평으로 돌아온다. 한 번만 실패한다.',
 continuity_out='문을 없앴지만 내려놓는 순서도 양보하여 두 사람은 계속 문을 든 채 남음.')

# C05: remove advance bag-gaze and the transport procedure; keep sudden return.
setshot('C05',5,
 screen='부모는 신나게 합주하고 아이들은 소파에서 축 늘어진다. G는 연주자들만 무심하게 본다. 회색 가방은 앞서 둔 현관 쪽에 남아 있지만 이 컷에서 시선이나 카메라로 강조하지 않는다.',
 next_motion='부모의 짧은 합주에 아이들 어깨가 더 처진다. G는 공연 쪽 시선을 유지한다. 가방을 보는 예고 동작은 없다.',
 first_frame='G는 전경에서 공연을 보고 있다. 회색 가방은 현관 아래 원래 위치, 중앙 D의 오른쪽에는 큰 버건디 케이스. 이 컷은 합주 반응만 보여준다.',
 continuity_out='관객은 개의 다음 행동을 아직 알지 못함. 다음 컷에서 가방 반환을 갑자기 공개.')
old7=shot('C05',7)
old7.update(screen='갑자기 D의 발앞까지 온 G가 회색 노트북가방을 코로 밀어 발에 붙인다. 아코디언이 뚝 멎고 D가 내려다본다.',next_motion='G가 마지막 짧은 거리를 밀어 가방을 D의 발에 붙인다. D는 연주를 멈추고 내려다본다. 수납·무릎으로 올리기는 다음 컷 사이 생략.',continuity_in='운반 과정은 생략. K02에 소개한 회색 가방이 개와 함께 아빠 발앞에 도착한 상태를 갑자기 공개.',continuity_out='음악 중단. 다음 컷에서는 악기가 오른쪽 케이스에 있고 회색 가방은 무릎 위에 놓인 시간 생략.')
old8=shot('C05',8)
old8.update(continuity_in='가방을 올리고 악기를 내려놓는 준비는 생략. K02의 은색 노트북이 동일 회색 가방에서 나온다.',next_motion='D가 이미 벌어진 가방에서 노트북을 꺼내 그 위에 펼친다. G는 한 번만 악기에서 노트북으로 고개를 돌려 응시한다. “이건 끝났는데?”는 동작 중 말한다.')
cs['C05']['shots']=[s for s in cs['C05']['shots'] if s['id']!='K06']
for i,s in enumerate(cs['C05']['shots'],1):s.update(id=f'K{i:02d}',scene_id=f'S{i:02d}',image_file=f'images/C05/S{i:02d}.png')
cs['C05']['continuity'][4]='개가 가방을 운반하는 과정과 가방을 미리 보는 동작은 생략한다. K06에서 회색가방을 발앞에 미는 행동이 갑자기 공개되고, K07에서 같은 노트북을 펼친 뒤 개가 응시한다. 노트북 자체를 물거나 뛰는 동작 없음.'
cs['C05']['comedy_engine']='침입 대비로 보이는 가족 행동 → 아빠의 아코디언 → 엄마의 합주 공범 공개 → 갑자기 업무 가방을 돌려주는 개와 노트북 응시'
d['hero_cuts']['C05']='K04'

timing={'C01':[3,3,3,5,4,4,3,3,6],'C02':[4,4,6,3,3,2,3,2,6],'C04':[3,4,3,4,3,5,4,3,6],'C05':[4,5,3,3,3,3,4,6]}
for cid,ts in timing.items():
 c=cs[cid];end=0
 for s,seconds in zip(c['shots'],ts):
  s.update(start=end,end=end+seconds,duration=seconds);end+=seconds
  if '초:' in s['subtitle']:s['subtitle']=re.sub(r'^\d+–\d+초:',f"{s['start']}–{s['end']}초:",s['subtitle'])
 c['duration_seconds']=end
 c['scene_list']=[{'concept_id':cid,'scene_id':s['scene_id'],'linked_cuts':[s['id']],'representative_frame':s['first_frame'],'framing':s['framing'],'continuity':s['continuity_in']+' / '+s['continuity_out'],'aspect_ratio':'16:9','reference_cut':s['reference_cut'],'next_motion':s['next_motion'],'image_file':s['image_file'],'text_policy':'행사명·자막은 후편집. 생성 이미지에는 글자·로고 없음.'} for s in c['shots']]
cs['C01']['three_act']=['0–9초: 상체만 잘린 사진을 성공 비법으로 엄숙히 교정한다.','9–18초: 원본의 의자 밀림을 보고 첫 수강생은 실제 이야기를 들으러 간다.','18–34초: 코치는 사고까지 비법이라 우기고 새 교본과 모방자가 생긴다.']
cs['C02']['three_act']=['0–8초: 팬들이 스타가 아닌 경호원을 따라간다.','8–20초: AI 작업 이야기가 시작되고 스타는 보호선을 친 뒤 내용을 엿본다.','20–33초: 자기 선 아래로 기어들어 맨 앞에서 계속 경호하는 척한다.']
cs['C04']['three_act']=['0–10초: 문을 잡은 AI 비서들이 서로 양보하다 멈춘다.','10–22초: 주인도 같은 동작을 한 뒤 문을 탓하며 떼어낸다.','22–35초: 비서는 통과하고 사람들은 문을 놓는 순서까지 양보하며 남는다.']
cs['C05']['three_act']=['0–9초: 침입 대비처럼 보이는 준비 뒤 평범한 아빠와 업무용 가방을 소개한다.','9–18초: 아빠의 공연, 엄마의 반주 공범을 차례로 공개한다.','18–31초: 개가 갑자기 업무 가방을 돌려주고 아빠 무릎은 노트북이 차지한다.']
assert cs['C03']==read('retained_concept_C03.json')
d['status']='text_revision_cross_confirmation_pending'
write('storyboards.json',d)
write('blind_storyboards.json',{'instruction':'행동/대사먼저. C03보존확정.','concepts':[{'id':c['id'],'duration_seconds':c['duration_seconds'],'shots':[{k:s[k] for k in ['id','scene_id','start','end','screen','framing','subtitle','dialogue','sound','transition']} for s in c['shots']]} for c in d['concepts']]})
write('text_revision_disposition.json',{'changes':{'A-S01/B-S01':'원본첫프레임을사진과같은순간으로, 의자밀림/풀썩을실제후속동작으로.','A-S02/C-S03':'초반교정6초/촬영+모방6초. 뒤집힌몸자세까지새교본으로삼는과장복원. AI잘쓴사람의각도대사로주제연결.','A-S03/B-S03/C-S04':'진입준비19→10초. 팬의짧은돌아보기로체면확인.','A-S04/B-S04/C-S01':'2cm삭제. 큰무릎굽힘과문대각선의한번실패.','A-S05/B-S02/C-S02':'가방응시/운반컷삭제. 발앞반환갑자기공개→노트북공개7초. 수납준비생략.','A-S06':'첫3초안레버접촉/양보시작. 허구AI테스트짧은후편집표기.','C-S05':'운반거리자체생략. 앞위치/반환소품동일성유지.','B-G13':'노트북이같은회색가방에서다시나오고개응시/끝났는데반응유지.'},'counts':{c['id']:{'seconds':c['duration_seconds'],'cuts':len(c['shots'])} for c in d['concepts']},'C03':'structurally unchanged','actual_audience_test':False})
print(json.dumps({c['id']:(c['duration_seconds'],len(c['shots'])) for c in d['concepts']}))
