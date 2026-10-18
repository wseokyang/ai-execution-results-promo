from pathlib import Path
import json
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def write(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 d=read('director_draft.json'); frozen=read('retained_concept_C03.json')
 assert {c['id'] for c in d['concepts']}=={'C01','C02','C04','C05'}
 concepts=sorted(d['concepts']+[frozen],key=lambda x:x['id'])
 keys=['id','scene_id','start','end','duration','screen','framing','subtitle','dialogue','sound','transition','intent','first_frame','next_motion','continuity_in','continuity_out','reference_cut','image_file']
 for c in concepts:
  end=0
  for s in c['shots']:
   assert all(k in s for k in keys),(c['id'],s['id'],[k for k in keys if k not in s])
   assert s['start']==end and s['duration']==s['end']-s['start'];end=s['end']
  assert end==c['duration_seconds'] and end<=60
 heroes=d.get('hero_cuts',{});heroes['C03']='K02'
 assert set(heroes)=={c['id'] for c in concepts}
 write('storyboards.json',{'run_id':R.name,'status':'text_review_pending','concepts':concepts,'hero_cuts':heroes,'C03_preserved_from':'2026-10-18_story-reset-v4','scope':'4 rebuilt concepts, retained C03, actual first frames to follow; no video/audio generation','notes':d.get('notes',[])})
 write('blind_storyboards.json',{'instruction':'제목/의도/웃긴이유를보지않고 실제행동·대사먼저읽는다. C03은보존확정.','concepts':[{'id':c['id'],'duration_seconds':c['duration_seconds'],'shots':[{k:s[k] for k in ['id','scene_id','start','end','screen','framing','subtitle','dialogue','sound','transition']} for s in c['shots']]} for c in concepts]})
 print(json.dumps({c['id']:{'seconds':c['duration_seconds'],'shots':len(c['shots'])} for c in concepts}))
if __name__=='__main__':main()
