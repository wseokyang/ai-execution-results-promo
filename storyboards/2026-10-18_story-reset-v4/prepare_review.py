from pathlib import Path
import json
R=Path(__file__).resolve().parent
d=json.loads((R/'director_draft.json').read_text(encoding='utf-8-sig'))
out={'instructions':'제목·의도·웃음 설명을 제외한 실제 화면과 대사. 먼저 이 이야기만 평가한 뒤 전체 콘티를 읽는다. 행사명은 [행사명]으로 가렸다.','concepts':[]}
for c in d['concepts']:
    last=0
    shots=[]
    for s in c['shots']:
        assert s['start']==last and s['end']-s['start']==s['duration'],(c['id'],s['id'])
        last=s['end']
        item={k:s[k] for k in ['id','scene_id','start','end','duration','screen','framing','subtitle','dialogue','sound','transition']}
        for k,v in item.items():
            if isinstance(v,str): item[k]=v.replace('2026년 품질팀 AI 실행 결과 발표 대회','[행사명]')
        shots.append(item)
    assert last==c['duration_seconds'] and last<=60
    out['concepts'].append({'id':c['id'],'duration_seconds':last,'shots':shots})
assert len(out['concepts'])==5
(R/'blind_storyboards.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
if not (R/'storyboards.json').exists():
    (R/'storyboards.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print([(c['id'],len(c['shots']),c['duration_seconds']) for c in d['concepts']])
