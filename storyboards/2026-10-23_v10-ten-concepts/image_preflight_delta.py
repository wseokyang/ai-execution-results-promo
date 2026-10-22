"""Align planning text to selected actual first frames; never modify PNG bytes."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
d=json.loads((R/'storyboards.json').read_text(encoding='utf8'))
def get(cid,kid):
    c=next(c for c in d['concepts']if c['id']==cid)
    return next(s for s in c['shots']if s['id']==kid),next(u for u in d['generation_units']if u['id']==cid+'_'+kid)
s,u=get('C06','K09')
s['first_frame']='팻말이 책상에 서 있다. G3의 닫힌 회색 노트북은 책상 왼쪽에 내려놓았다. G3가 접힌 의자의 양쪽을 잡고 펴기 직전이고 G2는 옆에서 남색 노트북을 안고 차례를 기다린다. GH는 정중한 미소를 유지하려 한다.'
s['continuity_in']='팻말·두 노트북·접힌 의자. G3가 회색 노트북을 책상 왼쪽에 내려놓는 시간은 컷 사이에 생략한다. 인원은 GH+G2+G3 정확히 셋.'
u['first_frame']=s['first_frame']
s,u=get('C07','K04')
s['first_frame']=s['first_frame'].replace('수첩을 한 손에 든 채','수첩을 두 손으로 받친 채')
s['continuity_out']='줄 고리는 EX 앞 모래에 놓여 있고 어느 몸에도 걸리지 않음. 다음 컷 전 EX가 수첩에서 한 손을 떼고 줄 끝을 집는 시간은 생략.'
u['first_frame']=s['first_frame']
s,u=get('C10','K03')
s['screen']='MC가 벌린 큰 정원 가위를 패치 쪽으로 짧게 오른쪽으로 옮긴 뒤 같은 리본을 한 번 넓게 자른다. 리본 두 끝이 더 멀리 벌어지고 MC는 가위를 닫아 트레이 쪽으로 내린다. 장치가 움직이는 과정은 다음 컷에 둔다.'
u['action']=s['screen']
(R/'storyboards.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Aligned C06 laptop placement, C07 notebook grip, C10 pre-cut hand travel to selected images.')
