from pathlib import Path
from PIL import Image
import json, hashlib, shutil
R=Path(__file__).resolve().parent

def read(n): return json.loads((R/n).read_text(encoding='utf-8-sig'))
def put(n,d): (R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    d=read('storyboards.json'); entries=[]
    for c in d['concepts']:
        es=read('image_manifest_'+c['id']+'.json')['images']
        for s in c['shots']:
            selected=[x.copy() for x in es if x['cut_id']==s['id'] and x.get('selected',True)]
            assert len(selected)==1,(c['id'],s['id'],len(selected))
            e=selected[0];p=R/e['image_path'];assert p.is_file()
            e.update(first_frame=s['first_frame'],next_motion=s['next_motion'],linked_cuts=[s['id']],selected=True)
            with Image.open(p) as im: im.load();e['width'],e['height']=im.size
            e['sha256']=sha(p);assert e['prompt']
            e['generated_this_run']=e.get('generated_this_run',False)
            if s.get('postproduction_notes'): e['postproduction_notes']=s['postproduction_notes']
            if c['id'] in ['C02','C04']:
                e['generation_record_followup_motion']=e.get('generation_record_followup_motion',e.get('followup_motion'))
                e['followup_motion']=s['next_motion']
                e['motion_instruction_source']='current storyboards.json; original prompt preserved verbatim'
            s['image_file']=e['image_path']
            for scene in c.get('scenes',[])+c.get('scene_list',[]):
                if s['id'] in scene.get('linked_cuts',[]): scene['image_file']=e['image_path']
            entries.append(e)
    assert len(entries)==43 and sum(e['generated_this_run'] for e in entries)==2
    for cid in ['C01','C03','C05']:
        assert next(c for c in d['concepts'] if c['id']==cid)==read('retained_concept_'+cid+'.json')
    for e in entries:
        if not e['generated_this_run']:
            source=R.parent/e['reused_from_run']/e['reused_image_path']
            assert sha(source)==e['sha256']
    aux='images/C02/S07_document_photo.png'
    shutil.copy2(R.parent/'2026-10-19_keep135-rebuild-v7'/aux,R/aux)
    put('scene_manifest.json',{'run_id':R.name,'images':entries,'ratio':'16:9','new_images':2,'reused_images':41,'new_video_or_audio':False,'auxiliary_assets':[{'path':aux,'usage':'K07에서 한 번 촬영한 사진을 K08/K09에 재사용하는 참고; 별도 첫 프레임이 아님'}]})
    put('storyboards.json',d)
    print({'selected_images':43,'new_images':2,'reused_images':41})

if __name__=='__main__':main()
