from pathlib import Path
import json, hashlib, shutil
from PIL import Image
d=Path(__file__).resolve().parent
run=d.parent.parent
rec=json.loads((d/'image_prompt_record.json').read_text(encoding='utf-8'))
sb=json.loads((run/'storyboards.json').read_text(encoding='utf-8'))
c=next(c for c in sb['concepts'] if c['id']=='C05')
shots={s['scene_id']:s for s in c['shots']}
entries=[]
for key,source in rec['sources'].items():
    target=d/(key+'.png')
    if not target.exists(): shutil.copyfile(source,target)
    raw=target.read_bytes(); sh=hashlib.sha256(raw).hexdigest()
    assert sh==hashlib.sha256(Path(source).read_bytes()).hexdigest()
    scene=key.split('_')[0]; selected=rec['selected'].get(scene)==key
    w,h=Image.open(target).size
    shot=shots[scene]
    entries.append(dict(concept_id='C05',cut_id=shot['id'],scene_id=scene,linked_cuts=[shot['id']],image_path='images/C05/'+target.name,prompt=rec['prompts'][key],reference_images=rec['references'].get(key,[]),source_generated_path=source,generation_tool='image_gen',selected=selected,width=w,height=h,sha256=sh,source_copy_sha256_match=True,artist_review=dict(opened_actual_image=True,status='artist_inspected_pending_independent_review' if selected else 'superseded',notes=rec.get('notes',{}).get(key,[])),followup_motion=shot['next_motion']))
(run/'image_manifest_C05.json').write_text(json.dumps(dict(concept_id='C05',status='ready_for_independent_image_review' if len(rec['selected'])==8 else 'generation_in_progress',generated_scene_count=len(rec['selected']),total_scene_count=8,images=entries),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'saved':len(entries),'selected':len(rec['selected'])}))
