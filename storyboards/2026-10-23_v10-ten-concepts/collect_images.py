from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=read(R/'storyboards.json');units={u['id']:u for u in d['generation_units']}
images=read(R/'existing_images.json')['images']
for cid in ['C06','C07','C08','C09','C10']:
    p=R/f'artist_{cid}.json';a=read(p)
    for e in a['images']:
        e['new_in_v10']=True;e['artist_record']=p.name
        f=R/e['image_path'];assert f.exists(),f
        src=Path(e['source_generated_path']);assert src.exists(),src
        assert sha(src)==sha(f),e['id']
        e['sha256']=sha(f);e['source_sha256']=sha(src)
        with Image.open(f)as im:im.load();e['dimensions']=list(im.size)
        assert e['generation_tool']=='image_gen'
        assert e.get('artist_review',{}).get('opened_actual_image') is True
        images.append(e)
assert len({e['id']for e in images})==len(images)
assert {e['id']for e in images}==set(units),(set(units)-{e['id']for e in images})
for e in images:
    u=units[e['id']];u['image_file']=e['image_path'];u['status']='actual image; independent V10 image review pending'
    c=next(c for c in d['concepts']if c['id']==u['concept_id']);s=next(s for s in c['shots']if s['id']==u['linked_shot'])
    s['image_file']=e['image_path']
    s['image_files']=[x['image_path']for x in images if x['concept_id']==u['concept_id']and x.get('linked_cut',x.get('linked_shot'))==u['linked_shot']]
    e['next_motion']=u['action'];e['camera_notes']=u['framing']
counts={c['id']:sum(e['concept_id']==c['id']for e in images)for c in d['concepts']}
put(R/'scene_manifest.json',{'run_id':R.name,'event_name':'Q-AI Fair','status':'actual images assembled; independent V10 review pending','new_images':sum(e['new_in_v10']for e in images),'reused_images':sum(not e['new_in_v10']for e in images),'image_count_by_concept':counts,'images':images})
put(R/'storyboards.json',d)
print('Collected',len(images),'selected images',counts)
