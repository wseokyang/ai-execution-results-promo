from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def dump(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 d=read('image_manifest_C02.json');extras=read('image_manifest_C02_root_revisions.json')['images'];existing={e['image_path'] for e in d['images']}
 d['images'] += [e for e in extras if e['image_path'] not in existing]
 for e in d['images']:
  if e['cut_id']=='K08':e['selected']=e['image_path']=='images/C02/S08_v6.png'
  if e['cut_id']=='K09':e['selected']=e['image_path']=='images/C02/S09_v3.png'
 dump('image_manifest_C02.json',d)
 d=read('image_manifest_C05.json')
 for e in d['images']:
  if e['cut_id'] in ['K06','K07']:
   e['selected']=e['image_path'].endswith('_v2.png')
   if e['selected']:e['artist_review']['status']='cross_review_content_pass_mapping_selected'
   else:e['artist_review']['status']='superseded_due_to_background_bag_duplicate'
 dump('image_manifest_C05.json',d)
 for cid in ['C01','C02','C04','C05']:
  d=read(f'image_manifest_{cid}.json')
  for e in d['images']:
   p=R/e['image_path'];source=Path(e['source_generated_path'])
   e['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();e['source_copy_sha256_match']=hashlib.sha256(source.read_bytes()).hexdigest()==e['sha256'];assert e['source_copy_sha256_match']
   with Image.open(p) as im:im.load();e['width'],e['height']=im.size
  dump(f'image_manifest_{cid}.json',d)
 # A local artist copy exists for C02; keep it from advertising superseded selections.
 local=R/'images/C02/scene_manifest.json'
 if local.exists():dump('images/C02/scene_manifest.json',read('image_manifest_C02.json'))
 print('4 revised selections applied; original byte-copy hashes passed')
if __name__=='__main__':main()
