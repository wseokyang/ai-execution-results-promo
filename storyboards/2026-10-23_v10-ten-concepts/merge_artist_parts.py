from pathlib import Path
import json
R=Path(__file__).resolve().parent
for cid in ['C09','C10']:
    ps=[R/f'artist_{cid}_part1.json',R/f'artist_{cid}_part2.json']
    parts=[json.loads(p.read_text(encoding='utf-8-sig'))for p in ps]
    ims=[x for a in parts for x in a['images']]
    assert len(ims)==9 and len({x['id']for x in ims})==9,(cid,len(ims))
    out={'concept_id':cid,'merged_by':'PD','source_records':[p.name for p in ps],'images':sorted(ims,key=lambda x:x['id']),'rejected_attempts':[x for a in parts for x in a.get('rejected_attempts',a.get('attempts',[]))]}
    (R/f'artist_{cid}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('C09/C10 artist parts merged; originals retained.')
