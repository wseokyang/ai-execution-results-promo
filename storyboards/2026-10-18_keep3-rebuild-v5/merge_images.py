from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 d=read(R/'storyboards.json'); entries=read(R/'image_manifest_retained_C03.json')['images']; expected={(c['id'],s['id']):s for c in d['concepts'] for s in c['shots']}
 for cid in ['C01','C02','C04','C05']:
  m=read(R/f'image_manifest_{cid}.json')
  entries += [e for e in m['images'] if e.get('selected',True)]
 assert len(entries)==len(expected)
 seen=set()
 for e in entries:
  k=e['concept_id'],e['cut_id']; assert k in expected and k not in seen;seen.add(k);s=expected[k]
  assert e['image_path']==s['image_file'];p=R/e['image_path'];assert p.exists()
  with Image.open(p) as im:im.load();e['width'],e['height']=im.size;assert abs(im.width/im.height-16/9)<.08
  e['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
  assert e.get('prompt') and e.get('source_generated_path')
  if e['concept_id']!='C03':
   assert e.get('generation_tool')=='image_gen';e['new_generation_in_this_run']=True
  e['first_frame']=s['first_frame'];e['next_motion']=s['next_motion'];e['scene_id']=s['scene_id'];e['linked_cuts']=[s['id']]
  e['review_status']='three_independent_reviews_cross_check_and_revision_confirmation_complete' if (R/'image_final_confirmation.json').exists() else 'independent_image_review_pending'
 entries.sort(key=lambda x:(x['concept_id'],x['cut_id']))
 result={'run_id':R.name,'ratio':'16:9','new_video_or_audio':False,'images':entries,'scope':'4 rebuilt concepts plus 8 byte-identical retained C03 images. Actual independent PNG per cut. Text is post-production information.'}
 (R/'scene_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'selected_images':len(entries),'new':len(entries)-8,'retained':8}))
if __name__=='__main__':main()
