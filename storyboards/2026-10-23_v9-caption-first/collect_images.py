from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
d=read(R/'storyboards.json'); images=[]
for p in sorted(R.glob('artist_*.json')):
    for e in read(p)['images']:
        e=dict(e);e['artist_record']=p.name
        assert hashlib.sha256((R/e['image_path']).read_bytes()).hexdigest().lower()==e['sha256'].lower()
        images.append(e)
assert len(images)==44,(len(images),'images available')
assert len({e['id'] for e in images})==44
m={e['id']:e for e in images}
for u in d['generation_units']:
    u['image_file']=m[u['id']]['image_path'];u['status']='generated; independent image review pending'
for c in d['concepts']:
    for s in c['shots']:
        units=[u for u in d['generation_units'] if u['concept_id']==c['id'] and u['linked_shot']==s['id']]
        s['image_files']=[u['image_file'] for u in units];s['image_file']=units[0]['image_file']
    for s in c['scene_list']:
        u=next(u for u in d['generation_units'] if u['concept_id']==c['id'] and u['scene_id']==s['scene_id'])
        s['image_file']=u['image_file']
data={'run_id':d['run_id'],'event_name':'Q-AI Fair','status':'44 new generated candidates; independent review pending','new_images':44,'reused_images':0,'image_count_by_concept':{c['id']:sum(e['concept_id']==c['id'] for e in images) for c in d['concepts']},'images':sorted(images,key=lambda e:e['id']),'source_policy':'Each selected PNG exactly matches its built-in image_gen output; no resize or re-encode. Previous V8 files are reference inputs only.','flow_requests':0}
(R/'scene_manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(R/'storyboards.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Collected 44 selected new image files.')
