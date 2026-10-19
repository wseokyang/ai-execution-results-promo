from pathlib import Path
import json
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=read('storyboards.json');d['status']='storyboards_reviewed_image_production_in_progress';put('storyboards.json',d)
t=read('team_log.json')
for s in t['stages']:
 if s['stage'] in ['detailed_storyboards','full_storyboard_independent_cross_review']:s['status']='complete'
 if s['stage']=='full_storyboard_independent_cross_review':s.update(agents=['/root/v6_review_a','/root/v6_review_b','/root/v6_review_c'],artifacts=['storyboard_reviews.json','storyboard_cross_reviews.json','storyboard_final_confirmation.json'])
 if s['stage']=='actual_per_scene_first_frames':s.update(status='in_progress',agents=['/root/v6_artist_c02','/root/v6_artist_c04','/root/v6_artist_c05'],new_images_required=26)
put('team_log.json',t)
put('progress.json',{'stage':'actual_first_frame_production','status':'in_progress','retained_images':17,'new_images_required':26,'concept_seconds':{'C01':34,'C02':38,'C03':42,'C04':42,'C05':38},'Flow':'not_used'})
print('Storyboards accepted; image generation phase recorded.')
