from pathlib import Path
import json
R=Path(__file__).resolve().parent;p=R/'storyboards.json';d=json.loads(p.read_text(encoding='utf8'))
for c in d['concepts']:
    if c['id']=='C10':
        c['continuity']=[x.replace('K04 과한 접합 띠의 늘어진 끈끈한 여유분이 트레이의 두 가위 닫힌 날 위에 붙는다.','K04 주 리본과 이미 잘려 분리된 짧은 접착 자투리가 트레이의 두 가위 닫힌 날을 붙인다. 가위와 주 리본 사이에는 연결이 없고 K06 이후에도 자투리와 가위는 트레이에 남는다.')for x in c['continuity']]
    if c['id']=='C09':
        c['continuity'].append('K08 투구에는 마지막 얇은 종이 자료 묶음만 들어간다. K09 인간이 꺼내는 것은 그 묶음의 자료 한 장이며 기존 수첩은 책상 위에 남는다.')
for c in d['concepts']:
    for s in c['shots']:
        for k in ['start','end','duration']:s[k]=round(s[k],2)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Global continuity synchronized with scene repairs.')
