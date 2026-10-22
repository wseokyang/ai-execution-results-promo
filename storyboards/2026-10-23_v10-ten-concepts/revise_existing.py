from pathlib import Path
import json,copy,shutil
R=Path(__file__).resolve().parent
V9=R.parent/'2026-10-23_v9-caption-first'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=read(V9/'storyboards.json');d['run_id']=R.name
d['status']='existing five revised; new five and independent review pending'
cs={c['id']:c for c in d['concepts']}
def shot(cid,k):return next(s for s in cs[cid]['shots'] if s['id']==k)
def cue(cid,k,idx,text):shot(cid,k)['caption_cues'][idx]['text']=text
def shift_after(cid,cut,delta):
    active=False
    for s in cs[cid]['shots']:
        if active:
            s['start']+=delta;s['end']+=delta
            for q in s.get('caption_cues',[]):q['start']+=delta;q['end']+=delta
        if s['id']==cut:active=True
    cs[cid]['duration_seconds']+=delta

cue('C01','K01',0,'AI 잘 쓰는 사람은\n자세부터 다릅니다.')
s=shot('C01','K02');s['caption_cues']=[];s['end']=6.5;s['duration']=2.5
shift_after('C01','K02',-1.5)
cue('C02','K01',0,'제품은 다른데,\n흔적은 같다.')
cue('C02','K03',0,'AI가 모은 후보 3장')
cue('C02','K03',1,'겹치니, 전부 같은 자리.')
cue('C03','K03',0,'이번 결과도 같네.')
cue('C03','K07',0,'해본 사람에게\n물어봐야겠네요.')
s=shot('C04','K04');s['end']=16;s['duration']=5
s['caption_cues']=[{'start':11.2,'end':15.8,'text':'탑승자 없음\n↔ 수저 요청','kind':'evidence','placement':'상단 대비 박스. 손과 태블릿의 모순 두 항목을 가리지 않음. 작은 AI 대조 머리말과 하나의 시각 정보로 구성.','box':{'left_pct':7,'width_pct':86,'top_pct':6},'eyebrow':'AI 대조 · 확인 필요'}]
s['screen']='RC가 태블릿의 모순 후보 두 곳만 차례로 짚는다. 작은 머리말 AI 대조·확인 필요와 큰 대조 카드 탑승자 없음↔수저 요청을 동시에 유지. CM이 목마 쪽을 곁눈질한다. 발화 없음.'
s['intent']='이미 병사를 본 관객에게 정답을 길게 설명하지 않는다. 은폐를 깨는 수저 요청만 남겨 다음 말 농담과 배식 행동으로 넘긴다. AI 후보 뒤 원문·현장 확인은 유지.'
shift_after('C04','K04',-2)
cue('C05','K01',0,'이 입구는 내가 접수한다.')
s=shot('C05','K02')
s['screen']='A3초: 기둥을 빼 왼쪽 바닥에 놓고 손을 놓는다. B4초: 출입구를 자기 몸으로 가로막으려고 같은 크기로 목·무릎을 접어 빈자리로 들어가 양팔을 벌린다. 의기양양한 문지기 자세. 순간 축소나 이동 없음.'
s['intent']='입구를 독점하려는 자기 선택으로 지붕 아래 들어간다. 다음 컷에서 남을 막던 양팔이 자기 머리 위 지붕을 떠받치게 되는 반전.'
s=shot('C05','K05');s['screen']='앞 3.6초 양손 지지 유지하며 발표 예고 자막. 뒤 2.4초 눈만 문 쪽으로 이동하고 눈꺼풀이 조금 열림→고개를 기울이다 지붕이 조금 움직여 즉시 복귀. 개과천선이 아니라 기다리던 중 생긴 호기심. 필수 안내 음성 없음.'
shot('C05','K08')['continuity_in']='K07 들리세요? 자막 뒤 엄지 답신→지붕 재지지→끄덕임. 질문·답변 음성은 필요 없다. 같은 S목·같은 귀·동일 양손 지지 시작 상태.'
cs['C05']['logline']='출입구를 독점하려 기둥을 뽑은 괴수가 새 기둥이 되고, 구조용인 줄 알았던 사다리에서는 행사 청취용 이어폰이 올라온다.'
cs['C05']['comedy_engine']='입구를 막으려던 괴수가 입구를 떠날 수 없는 기둥이 됨→구조 사다리 기대가 이어폰 설치로 바뀜→응답하려 손을 떼는 것조차 실패하는 새 관객.'
cs['C05']['hook']='입구를 접수하겠다고 과시하며 앞 기둥으로 손을 뻗는 특촬 괴수.'
for c in d['concepts']:
    c['revision_group']='기존 보완'
    c['dialogue_policy']='대사/내레이션 생성 불필요. 이야기와 행사 정보는 화면+후처리 자막으로 완결. BGM/SFX는 보조.'
    oldextra=[x for x in c.get('text_assets',[]) if x.get('mode')!='후편집 화면 자막']
    for s in c['shots']:
        s['subtitle']=' / '.join(q['text'] for q in s.get('caption_cues',[])) or '없음'
    c['text_assets']=[{'cut':s['id'],'mode':'후편집 화면 자막','cues':s.get('caption_cues',[])} for s in c['shots'] if s.get('caption_cues')]+oldextra
    c['scene_list']=[{'scene_id':s['scene_id'],'cut':s['id'],'first_frame':s['first_frame'],'action':s['screen']} for s in c['shots']]
for u in d['generation_units']:
    s=shot(u['concept_id'],u['linked_shot'])
    u['status']='reuse V9 selected image; revised actions and captions pending V10 review'
    u['action']=s['screen']
    u['video_policy']='Future Flow only after user selection. Generate clean motion, no captions or exact writing; all text in post. Existing C03 footage reuse first.'
    if u['id']=='C05_K02A':u['action']='기둥을 빼 왼쪽 바닥에 놓고 손을 놓는다. 끝까지 직립, 지붕 수평, 두 손 자유.'
    if u['id']=='C05_K02B':u['action']='출입구를 자기 몸으로 막으려고 목·무릎을 접어 빈자리로 들어가 양팔을 벌린다. 다음 컷에서 양팔이 지붕 지지가 된다.'
m=read(V9/'scene_manifest.json')
for e in m['images']:
    p=R/e['image_path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(V9/e['image_path'],p)
    e['reuse_source']='../2026-10-23_v9-caption-first/'+e['image_path']
    e['new_in_v10']=False
    e['prior_review']=e.get('review_status')
    e['review_status']='V10 revised action/text check pending; V9 source retained'
    e['next_motion']=next(u['action'] for u in d['generation_units'] if u['id']==e['id'])
put(R/'existing_revised.json',d)
put(R/'existing_images.json',{'images':m['images']})
put(R/'existing_change_log.json',[
 {'id':'E-001','scope':'C02 K01','severity':'required','change':'현장마다→제품은 다른데 흔적은 같다. 동일 장비의 제품 사진이라는 원인 명확화.'},
 {'id':'E-002','scope':'C05 K08','severity':'required','change':'오프스크린 음성 잔존 지시 제거, 자막→몸짓 답신으로 통일.'},
 {'id':'E-003','scope':'C05 K01/K02','severity':'priority','change':'입구 독점 목표와 문지기 자세를 명시. 입구를 막던 인물이 못 떠나는 기둥이 되는 인과.'},
 {'id':'E-004','scope':'C04 K04','severity':'priority','change':'문서 설명7→5초. AI 대조 머리말+탑승자없음/수저요청의 한 화면. 전체39→37초.'},
 {'id':'E-005','scope':'C01 K01/K02','severity':'suggestion_adopted','change':'질문 반복 대신 코치의 확신. 비교 컷 무자막2.5초. 전체39→37.5초.'},
 {'id':'E-006','scope':'C01 K09','severity':'suggestion_not_adopted','change':'기존 간단한 행사 문구 유지. 추가 교훈 문장보다 바닥 자세의 후폭풍을 보게 함.'},
 {'id':'E-007','scope':'C02 K03','severity':'suggestion_adopted','change':'AI가 모은 후보3장/겹치니 전부 같은 자리로 단축. 원본 비교는 사람이 수행.'},
 {'id':'E-008','scope':'C03 K03','severity':'suggestion_adopted','change':'일반 재현 보장처럼 읽힐 문구를 이번 결과도 같네로 한정.'},
 {'id':'E-009','scope':'C03 K07','severity':'suggestion_adopted','change':'직접 봐야겠습니다→해본 사람에게 물어봐야겠네요. 방문 대상 명확화.'},
 {'id':'E-010','scope':'C05 K05','severity':'suggestion_adopted','change':'갑작스런 개과천선 없이 기다리던 중 작은 호기심 표정만.'}
])
print('Existing five revised; 44 exact source images copied, no regeneration.')
