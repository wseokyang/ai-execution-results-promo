from pathlib import Path
import json, shutil, hashlib
R=Path(__file__).resolve().parent
P=R.parent/'2026-10-18_keep3-rebuild-v5'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def put(n,d): (R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
d=read(P/'storyboards.json'); m=read(P/'scene_manifest.json')
d['event_facts']=read(P/'shared_brief.json')['event_facts']
kept=[c for c in d['concepts'] if c['id'] in ['C01','C03']]
images=[]; entries=[]
for c in kept:
    put('retained_concept_'+c['id']+'.json',c)
    for s in c['shots']:
        src=P/s['image_file']; dst=R/s['image_file']; dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dst); assert sha(src)==sha(dst)
        images.append({'concept_id':c['id'],'cut_id':s['id'],'source':str(src),'copy':s['image_file'],'sha256':sha(dst)})
    es=[dict(x,reused_from_run=P.name,new_generation_in_this_run=False) for x in m['images'] if x['concept_id']==c['id']]
    entries+=es
    put('image_manifest_retained_'+c['id']+'.json',{'images':es,'new_generation_in_this_run':False})
old=R.parent/'2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4'
assert sha(old)=='b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c'
put('preservation_manifest.json',{'retained_concepts':['C01','C03'],'source_run':P.name,'images':images,'old_completed_film_path':str(old),'old_completed_film_sha256':sha(old),'scope':'V5 C01·C03 콘티 객체와 채택 첫 프레임 17장 그대로 보존. C02·C04·C05만 신규 제작.'})
put('shared_brief.json',{'run_id':R.name,'latest_user_request':'1,3 빼고 다시 수정. 돌고래유괴단 감성이 전혀 없어. 그리고 등장인물의 외형을 좀 더 다양하게 해봐. 계속 동일한 남성 여성이 주인공으로 나오네. 1,3은 유지해.','retained':['C01','C03'],'rebuild':['C02','C04','C05'],'event_facts':d['event_facts'],'video_generation':False,'flow_upload':False,'max_seconds':60,'casting_requirement':'신규 3안의 주역 연령·체형·머리·얼굴 실루엣·앙상블을 구별한다. 외모 자체를 조롱하지 않는다. 아름다운 청년 남녀 고정 캐스팅을 반복하지 않는다.','creative_gate':['인물의 강한 욕망과 선택이 사건을 일으킨다','새 증거가 처음의 상황을 재해석한다','반전 이후 인물의 행동으로 예상 밖 사건이 더 생긴다','행사명을 가려도 시각 코미디로 읽힌다','기술적 정합성이나 검수 점수는 재미의 증거가 아니다'],'rejected_v5':['경호 대상이 바뀌었습니다','양보의 자동화','아빠가 벌써 온다'],'retained_inference':'C01의 잘못된 확신이 반증까지 흡수하는 캐릭터, C03의 추상 요구를 물리적 규모로 터뜨리는 사건을 사용자가 선택했다. 두 장치를 그대로 복제하라는 뜻은 아니다.'})
put('progress.json',{'stage':'independent_concepts','status':'in_progress','retained_images':17,'new_concepts_required':3,'Flow':'not_used'})
print('Frozen C01 and C03: 17 selected PNGs, original concept objects, old film hash confirmed.')
