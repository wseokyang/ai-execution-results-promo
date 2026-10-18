from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent
P=R.parent/'2026-10-18_story-reset-v4'
ROOT=R.parent.parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=json.loads((P/'storyboards.json').read_text(encoding='utf-8'))
c=next(x for x in d['concepts'] if x['id']=='C03')
put('retained_concept_C03.json',c)
imgs=[]
for source in sorted((P/'images/C03').glob('*.png')):
    dest=R/'images/C03'/source.name;dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,dest);assert digest(source)==digest(dest)
    imgs.append({'source':str(source),'copy':dest.relative_to(R).as_posix(),'sha256':digest(dest),'selected':dest.relative_to(R).as_posix() in {s['image_file'] for s in c['shots']}})
m=json.loads((P/'scene_manifest.json').read_text(encoding='utf-8'))
entries=[x for x in m['images'] if x['concept_id']=='C03']
for x in entries:x.update(reused_from_run=P.name,new_generation_in_this_run=False)
put('image_manifest_retained_C03.json',{'artist':'retained_from_v4','new_generation_in_this_run':False,'images':entries})
old=R.parent/'2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4'
assert digest(old)=='b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c'
put('preservation_manifest.json',{'retained_concept':'C03 환경까지 가져왔습니다','source_run':P.name,'concept_sha256':hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'images':imgs,'old_completed_film_sha256':digest(old),'scope':'C03 콘티와8개채택PNG 그대로 재사용. 기존완성C01영상도보존. 새로만들안은C01/C02/C04/C05.'})
put('shared_brief.json',{'run_id':R.name,'latest_user_request':'3번 하나 빼고 다 별로야. 3번을 남기고 나머지 다 다시 만들어봐. 재미도 없고 반전도 없잖아.','scope':{'retained':'V4 C03','rebuild':['C01','C02','C04','C05'],'first_frame_per_cut':True,'video_generation':False,'flow_upload':False,'preserve_old_completed_C01':True},'event_facts':d['event_facts'],'assumptions':{'audience':'품질팀내부시청가정','ratio':'16:9','max_seconds':60},'creative_gate':['초반관객이믿는상황과예상결말을분리','뜻밖의새증거는실제화면에보여야함','그뒤에다시새로운사건이나반응으로웃음이커지는지','행사명을가려도짧은코미디로성립하는지','설명가능한장치·연속성·검수인원수를재미의증거로쓰지않음'],'not_reuse':['악마계약','시간여행/실패복원','액션재연/대역','보존규칙','V3홈쇼핑/되감기/시상소감/관객마술/가방첩보'],'retained_inference':'C03의환경요구→사무실실물배송은화면에서의미와규모가즉시읽힌다. 모든신규안을배송/거대소품으로복제하라는뜻은아님.','reference_scope':'V4 reference 조사범위와qrew원자료를참고. 새전체광고시청·음원청취주장없음.'})
put('progress.json',{'status':'in_progress','stage':'independent_concept_writing','retained_concept':'C03','new_concepts_required':4,'video_generation':False,'flow_upload':False})
print('C03 copied byte-for-byte; original film hash unchanged.')
if not (R/'reference').exists():
    shutil.copytree(P/'reference',R/'reference')
