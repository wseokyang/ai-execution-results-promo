from pathlib import Path
import json
R=Path(__file__).resolve().parent
d=json.loads((R/'storyboards.json').read_text(encoding='utf-8'))
cs={c['id']:c for c in d['concepts']}; us={u['id']:u for u in d['generation_units']}
def shot(cid,k):return next(s for s in cs[cid]['shots'] if s['id']==k)

# A/B/C independent findings: make visible evidence and subsequent choice agree.
s=shot('C03','K06');s['caption_cues'][0]['text']='안 된 과정에도\n단서가 있네?'
s['mute_readability']='동료가 보낸 성공 기록과 시행착오 기록의 안쪽 페이지를 비교해 질문할 단서를 찾는다. 수신자 자신의 기록과 대조했다고 주장하지 않는다.'
s['postproduction_notes']='회색=잘됐던 작업 기록, 주황=시행착오 기록으로 후편집 라벨을 통일. 기존 v03의 내 작업 기록 표기는 새 자막 편집에서 교체할 대상이며 현재 MP4 자체는 보존한다.'
s=shot('C03','K07');s['next_motion']='직접 만나 확인하겠다는 자막에 기사가 두 방을 보며 벨트를 조인다. 직원은 두 파일을 한 팔에 유지하고 전화기를 든 손도 그대로 둔 채 몸을 출구로 돌린다. 이번에는 본인이 가겠다는 자막 뒤 기사의 손이 멈춘다.';s['screen']=s['next_motion'];us['C03_K07']['action']=s['next_motion']

s=shot('C04','K04');s['caption_cues']=s['caption_cues'][:2];s['caption_cues'][1]['text']='탑승자 없음\n↔ 식사·물·수저 요청';s['caption_cues'][1]['end']=17.9
s['postproduction_notes']='AI 라벨→큰 원문 두 구절을 순차 합성한다. UI를 읽는 동안 동일 내용을 별도 장문 하단 자막으로 중복하지 않는다. 농담 자막은 K05로 넘긴다.'
s=shot('C04','K05');s['caption_cues']=[{'start':18.2,'end':20.8,'text':'이 말, 수저를 씁니까?','kind':'character','placement':'원문·손·초승달 표식을 가리지 않는 상단 여백'}]
shot('C04','K03')['caption_cues'][0]['text']='아무도 없는데, 웬 배식?'

s=shot('C01','K04');s['caption_cues']=[];s['intent']='사진과 같은 자세의 크롭 없는 착지 전 상태에서 시작해, 의자 밀림과 낮은 착지를 실제 움직임으로 공개한다. 관객이 먼저 원인을 알아채게 한다.';s['continuity_in']='사진과 같은 상체·오른손 자세의 크롭 없는 착지 전 상태. 골반은 아직 의자 가장자리에 있고 발·바퀴·매트가 보임.'
s['screen']='사진과 같은 자세로 시작한 P의 의자가 옆으로 밀려, 두꺼운 매트에 낮게 풀썩한다. 움직임은 모니터 내부에만 합성한다. 착지 후 설명 자막 없이 반응을 읽히며 정지 박자를 둔다.';s['next_motion']=s['screen'];us['C01_K04']['action']=s['next_motion']
shot('C01','K01')['caption_cues'][0]['text']='AI 성공자의 자세를\n그대로 따라 하면?'
shot('C01','K02')['caption_cues'][0].update(text='AI 성공자의 자세를\n그대로 따라 하면?',end=5.8)
u=us['C02_K01'];u['image_prompt_english']=u['image_prompt_english'].replace('Different product photos have the same blurry mark in the same upper-right image location.','The crowded wall mixes many varied product photographs, including clean photographs. Only a few have a similar blurry occlusion in an upper-right image location; they are not already sorted or aligned as a solved comparison.')
shot('C05','K08')['caption_cues'][0]['start']=38
shot('C05','K08')['screen']='35–38초 오른손 엄지 답신 시도→지붕 흔들림→다시 잡기→작은 끄덕임. 38–42.8초 손 고정 상태에 행사명·시작 문구. 필수 안내 음성 없음.'
shot('C05','K08')['next_motion']=shot('C05','K08')['screen'];us['C05_K08']['action']=shot('C05','K08')['next_motion']
shot('C05','K08')['postproduction_notes']='35–38초에는 엄지 시도→재지지→작은 끄덕임의 시각적 박자에 집중. 행사명과 시작 안내는 38–42.8초 유지. 실제 동작이 늦으면 트림을 조정하되 자막을 반전 위에 먼저 덮지 않는다.'

cs['C02']['final_action']='형사가 현장 사진을 떼려 할 때 직접 설명하라는 화면 자막과 포인터가 붙는다. 형사는 사진을 반듯하게 펴는 손으로 위장한다. 34–38.8초 행사명과 과정 공유 초대를 후편집한다.'
cs['C03']['final_action']='성공과 시행착오의 기록을 질문 자료로 챙겨 직접 찾아간다. 작은 파일과 거대한 두 환경의 대비를 남기고 화면 자막으로 Q-AI Fair 참석을 연결한다.'
cs['C04']['final_action']='CM이 자기 숟가락을 꺼낸 뒤 지휘관부터 자막. 34–38.8초 Q-AI Fair와 AI 실행 사례, 지금 시작합니다를 화면에 제시해 첫 사례로 넘긴다. 필수 발화 없음.'
cs['C05']['final_action']='엄지 시도와 재지지 뒤 고개만 끄덕이는 몸개그를 먼저 보여준다. 38–42.8초 Q-AI Fair와 AI 실행 사례, 지금 시작합니다를 화면에 표시한다. 극중 이어컵 청취와 실제 관객의 자막 이해는 구분한다.'
cs['C03']['existing_media_policy']='기존 v03 44.75초 영상과 원본을 재사용 우선한다. 장갑 전체 탈착·턱끈 조작·동시 한국어 발화 성공을 새 필수 조건으로 되살리지 않는다. 새로운 화면 자막과 회색/주황 기록 라벨은 이후 별도 버전 편집에서 교체. 이번에는 원본과 v03 MP4를 수정하지 않는다.'
cs['C03']['difference']='주간 산업 현장의 큰 공간과 두 번의 배송. 조건 기록은 큰 도식으로 비교하고, 참석 선택은 작은 파일과 거대한 공간의 대비로 보여준다.'

for c in d['concepts']:
    cid=c['id'];c.pop('scenes',None)
    # Single canonical scene mapping derived from the actual production units.
    c['scene_list']=[]
    for u in [x for x in d['generation_units'] if x['concept_id']==cid]:
        s=shot(cid,u['linked_shot'])
        cont=s['continuity_in']+' → '+s['continuity_out']
        if u['id']=='C05_K02A':cont='온전한 앞왼쪽 기둥, 괴수 직립 → 기둥은 왼쪽 바닥, 괴수 직립, 양손 자유, 지붕 수평. 몸 접기·진입은 B에만.'
        if u['id']=='C05_K02B':cont='기둥 왼쪽 바닥, 괴수 직립 → 무릎과 긴 목을 접어 빈 기둥 자리 진입, 양팔 승리 자세. 실제 제작 시작은 채택 A의 끝 프레임과 대조.'
        c['scene_list'].append({'concept_id':cid,'scene_id':u['scene_id'],'linked_cuts':[u['linked_shot']],'image_file':u['image_file'],'first_frame':u['first_frame'],'next_motion':u['action'],'framing':u['framing'],'continuity':cont,'text_policy':'정확한 글은 caption_cues와 text_assets 기준 후편집'})
    for s in c['shots']:
        s['subtitle']=' / '.join(q['text'] for q in s['caption_cues']) or '없음'
        s['mute_readability']={'required_information':[q['text'] for q in s['caption_cues']], 'visible_cause_effect':s['screen'], 'audio_required':False, 'verification':'텍스트 구성 검토. 실제 영상 무음 연속 재생은 이후 확인.'}
    c['text_assets']=[{'cut':s['id'],'mode':'후편집 화면 자막','cues':s['caption_cues']} for s in c['shots'] if s['caption_cues']]
    if cid=='C02':c['text_assets'].append({'cut':'K03/K04/K06','mode':'후편집 모니터 그래픽','exact':['AI 유사 흔적 후보','원본 겹침','청소 전','같은 조건 · 재촬영'],'rule':'AI는 후보만 제안. 원본 겹침과 같은 조건 재촬영은 사람이 확인. 정확도·성과 수치 없음.'})
    if cid=='C03':c['text_assets'].append({'cut':'K06','mode':'후편집 안쪽 페이지 라벨','exact':['잘됐던 작업 기록','시행착오 기록'],'rule':'내 작업 기록/내 조건이라는 설명을 사용하지 않는다. 두 기록의 조건과 질문할 부분을 비교한다.'})
    if cid=='C04':c['text_assets'].append({'cut':'K02/K04/K05','mode':'후편집 원문과 UI','exact':['내부 탑승자 없음','식사','물','수저','AI 문서 대조','확인 필요'],'rule':'후보와 원문/현장 확인을 구별. 글을 순차 제시하며 긴 대사 자막과 중복하지 않는다.'})
    if cid=='C05':c['continuity']=[x.replace('K05 실내 방송은 아직 시작 전 안내. K08 청취 준비가 끝난 후에만 AI 실행 사례 발표 시작을 말한다.','K05 화면 안내는 아직 시작 전 예고. K08 몸개그 뒤 화면 자막으로 AI 실행 사례 시작을 알린다.') for x in c['continuity']]
d['caption_style']['timing']='짧은 문구 약2초 이상, 긴 문구3–5초. 결정적 동작 중 새 정보 금지. 시간은 각 concept의 절대 초이며 정지 미리보기 뒤 실제 영상에서도 확인한다.'
d['status']='text changes applied; awaiting independent cross-review confirmation'
(R/'storyboards.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Applied A/B/C findings and rebuilt all scene/text mappings from canonical shots.')
