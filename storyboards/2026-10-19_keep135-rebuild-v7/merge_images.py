from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 d=read(R/'storyboards.json');entries=[]
 for c in d['concepts']:
  fn=('image_manifest_retained_' if c['id'] in ['C01','C03','C05'] else 'image_manifest_')+c['id']+'.json'
  doc=read(R/fn);es=doc['images']
  for s in c['shots']:
   selected=[x for x in es if x['cut_id']==s['id'] and x.get('selected',True)]
   assert len(selected)==1,(c['id'],s['id'],len(selected))
   e=selected[0];p=R/e['image_path'];assert p.is_file()
   e['first_frame']=s['first_frame'];e['next_motion']=s['next_motion'];e['linked_cuts']=[s['id']];e['selected']=True
   with Image.open(p) as im:im.load();e['width'],e['height']=im.size
   e['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();assert e['prompt']
   if s.get('postproduction_notes'):e['postproduction_notes']=s['postproduction_notes']
   if c['id'] in ['C02','C04']:
    e['generation_record_followup_motion']=e.get('generation_record_followup_motion',e.get('followup_motion'))
    e['followup_motion']=s['next_motion']
    e['motion_instruction_source']='current storyboards.json; source image manifest preserves generation-time notes'
   s['image_file']=e['image_path']
   for scene in c.get('scenes',[])+c.get('scene_list',[]):
    if s['id'] in scene.get('linked_cuts',[]):scene['image_file']=e['image_path']
   entries.append(e)
 (R/'scene_manifest.json').write_text(json.dumps({'run_id':R.name,'images':entries,'ratio':'16:9','new_video_or_audio':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 # Retained objects must not gain or lose fields from merging.
 for cid in ['C01','C03','C05']:assert next(c for c in d['concepts'] if c['id']==cid)==read(R/('retained_concept_'+cid+'.json'))
 (R/'storyboards.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print({'selected_images':len(entries)})
if __name__=='__main__':main()
