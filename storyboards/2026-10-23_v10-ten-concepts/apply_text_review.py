from pathlib import Path
import json,copy
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=R/'storyboards.json';d=read(p)
assert not (R/'storyboards_before_text_review.json').exists(),'Do not rerun mutation.'
(R/'storyboards_before_text_review.json').write_bytes(p.read_bytes())
cs={c['id']:c for c in d['concepts']};us={u['id']:u for u in d['generation_units']}
def shot(cid,k):return next(s for s in cs[cid]['shots'] if s['id']==k)
def prompt_state(cid,k,state):
    u=us[cid+'_'+k];t=u['image_prompt_english'];a,b=t.split('EXACT SHOT START STATE:',1);_,end=b.split('Create one standalone',1)
    u['image_prompt_english']=a+'EXACT SHOT START STATE: '+state+'\n\nCreate one standalone'+end

# Concrete prop and metadata repairs.
cs['C04']['final_action']=cs['C04']['final_action'].replace('34–38.8','32–36.8')
s=shot('C10','K04');s['screen']=s['screen'].replace('늘어진 끈끈한 접합 띠 일부가 트레이의 두 가위 날 위에 붙는다.','주 리본과 이미 잘려 분리된 짧은 접합 테이프 자투리가 아래 트레이에 떨어져 닫힌 두 가위 날을 함께 붙인다. 주 리본에는 가위가 연결되지 않는다.')
s['continuity_out']='주 리본은 부드럽게 바닥으로 늘어짐. 별도로 잘린 짧은 접착 자투리와 두 가위는 트레이 위에 남음. 주 리본과 가위 사이 연결 없음.'
s=shot('C10','K05');s['first_frame']='긴 주 리본이 바닥에 늘어지고, 별도로 잘려 떨어진 짧은 빨간 접착 자투리가 트레이 위 두 가위의 닫힌 날을 함께 붙였다. 주 리본과 트레이 사이에 연결 띠는 없다. DV의 손가락은 정지 버튼 직전, MC는 가위 손잡이를 보고 있다.'
s['continuity_in']='주 리본과 별개의 자투리가 두 가위를 붙임. 가위를 들면 두 가위만 함께 들리고 주 리본은 움직이지 않음.'
prompt_state('C10','K05','The long soft main red ribbon droops onto the floor. On a separate shallow tray below, one SHORT SEVERED red adhesive offcut binds both CLOSED scissors blades together, handles visible. There is a clearly visible gap: absolutely no tape or ribbon connects the scissors tray to the main ribbon. DV finger hovers just before a large blank stop button. MC hesitates near the tool handles. Repair reel still poised. No jump rope setup yet.')
s=shot('C10','K06');s['first_frame']+=' 별개 접착 자투리로 붙은 가위 두 개는 뒤 트레이에 남고, 주 리본과 연결되지 않는다.'
s['continuity_in']='장치 정지 후 양끝 집게와 공급 연결을 풀어낸 준비 시간은 생략. 별개 자투리와 가위는 뒤 트레이에 남음. 두 사람은 자유 주 리본 끝만 잡음.'
prompt_state('C10','K06','After preparation, both ceremony post clamps are visibly open. Repair trolley parked idle behind right. MC holds both free ends of the long soft red MAIN ribbon and is about to pass one to DV empty hand. Ribbon fully disconnected from posts and reel, loose on floor. Behind them on the shallow tray remain the two closed scissors bonded by a SHORT SEVERED red adhesive scrap. Scissors and scrap are completely separate from the main ribbon, with a clear gap. Empty central walkway, no rope around bodies.')
s=shot('C09','K09');s['screen']=s['screen'].replace('수첩 하나를 뽑아 펼치자','얇은 자료 한 장을 뽑아 펼치자').replace('다음 페이지를 가리킨다','그 자료의 다음 항목을 가리킨다')
prompt_state('C09','K09','Same helmet-off AL and HU at low desk. Ivory open-top cylinder already filled with neatly standing THIN PAPER RECORD SHEETS, not notebooks. AL hand hovers just before pushing cylinder toward HU as a grand gift. HU has not yet pulled a sheet. Previously received worn notebook stays open on low desk outside the cylinder. Both service arms folded. Same purple facial proportions as prior shot, clean upper wall title space.')
s=shot('C05','K06');s['transition']='하부 고정 뒤, 작업 높이 조절과 등반을 마친 시간을 생략하여 K07의 귀 높이 설치 상태로 컷. 긴 사다리가 한 동작에서 자동 변형되는 생성은 요구하지 않음.'
s['continuity_out']='이 컷에서는 긴 길이를 유지. K06→K07 사이 작업 높이 조절·고정·등반 시간을 생략해 귀 높이의 최종 설치 상태로 연결.'
shot('C05','K07')['continuity_in']='K06 뒤 높이 조절·고정·등반을 마친 시간 생략. 귀 높이에 맞춘 같은 작업 사다리이며 단일 검정 유선 이어컵과 먼쪽 빨간 귀. S자 목·굽힌 무릎·양손 지지 유지.'
shot('C05','K08')['continuity_in']+=' 작업 사다리는 설치 높이 조절과 하강을 마친 귀 높이 상태다.'

# Make the dramatic intention visible while reducing procedural waits.
s=shot('C06','K04');s['screen']='WO가 AI 분류 제안의 한 항목과 원본의 같은 표시를 대조한다. GH는 끝난 줄 알고 쿠션을 베개처럼 얼굴 옆에 대며 눕기 준비를 하다, WO가 확인할 두 번째 표시로 손을 옮기자 바로 멈춘다. 마지막 확인 표시는 WO가 직접 한다. 한 묶음 외 다른 업무는 저절로 처리되지 않는다.'
s=shot('C07','K04');s['screen']='CW가 부드러운 줄 고리를 EX 발 앞 빈 바닥에 던진다. 사람에게 걸리지 않고 모래에 떨어진다. 줄을 놓은 오른손으로 EX 한 사람과 자기 앞 빈자리를 짧게 가리킨다. EX는 설명을 이어가며 고개만 끄덕인다.'
s=shot('C08','K03');s['screen']='ST가 버튼을 누르자 회전 세트가 약45도 돌아가기 시작한다. OP는 고정 앞무대에서 한 걸음 옮겨 자기 정면을 객석에 다시 맞추려 하지만 시선은 돌아가는 세트를 따라간다. 뒤 작업 책상 일부만 나타나며 전체는 다음 컷에 공개한다.'

# Precise postproduction clue, no fabricated metric or performance claim.
cs['C03'].setdefault('text_assets',[]).append({'cut':'K03/K06','mode':'후편집 소품 도식','content':'허구 사례용 큰 기호만 사용. K03 화면: 기준과 이번 결과 두 열에 같은 청록 원·세로선·사각형 배열과 일치 테두리. K06 회색/주황 안쪽 페이지 상단은 같은 원·세로선 입력기호, 하단은 회색 체크/주황 교정 화살표. 두 페이지의 같은 상단기호를 동시에 얇은 노랑 테두리로2초 강조해 비교 단서를 보여준다. 수치·실제 과제명·성과 주장 없음. 정확 문자는 잘됐던 작업 기록/시행착오 기록 라벨만.'})
shot('C03','K06')['postproduction_notes']+=' 양쪽 입력기호와 서로 다른 결과 표시의 정확 합성은 text_assets의 후편집 소품 도식을 따른다. 같은 조건의 다른 기록은 더 물어볼 단서이며 원인·일반 재현성을 입증한 것으로 말하지 않는다.'
shot('C03','K06')['framing']=shot('C03','K06')['framing'].replace('조건 1.5초','조건 비교2초')

# Editorial durations, not generated source length. Keep every start state.
lengths={'C06':[5,5,4,5,4,4,5,4,8],'C07':[5,5,4,4,4,6,4,5,6],'C08':[4,5,4,5,5,6,4,8],'C09':[4,4,5,4,5,4,5,5,9],'C10':[3,5,4,6,4,4,6,6,8]}
for cid,ds in lengths.items():
    c=cs[cid];t=0
    for s,nd in zip(c['shots'],ds):
        oldstart,oldlen=s['start'],s['duration']
        for q in s.get('caption_cues',[]):
            q['start']=round(t+(q['start']-oldstart)*nd/oldlen,2)
            q['end']=round(t+(q['end']-oldstart)*nd/oldlen,2)
        s.update(start=t,end=t+nd,duration=nd);t+=nd
    c['duration_seconds']=t
    c['three_act']=[c['three_act'][0].split('초: ',1)[-1],c['three_act'][1].split('초: ',1)[-1],c['three_act'][2].split('초: ',1)[-1]]
    c['timing_note']='호흡 검수 후 편집 길이를 압축. 정확 절대시간은 shots/caption_cues가 기준. Flow 원본은 후속 요청 시 개별 비용·길이 확인.'
q=shot('C10','K02')['caption_cues'][0];q.update(start=4.7,end=7.8,text='끊김 감지 → 자동 복구',eyebrow='AI 복구 시연 · 설정 켬')
shot('C10','K02')['screen']='3–4.5초: 보이는 롤의 접합 띠로 잘린 리본을 다시 잇는다. 4.5초: MC가 벌린 팔과 미소를 유지한 채 눈만 접합부로 내린다. 4.7초 뒤 짧은 시연 자막. 복구 동작을 먼저 보여준다.'

for c in d['concepts']:
    for s in c['shots']:
        s['next_motion']=s['screen'];s['subtitle']=' / '.join(q['text'] for q in s.get('caption_cues',[])) or '없음'
        if 'mute_readability'in s:s['mute_readability']['visible_cause_effect']=s['screen']
        for u in d['generation_units']:
            if u['concept_id']==c['id'] and u['linked_shot']==s['id']:
                # C05 K02A/B have distinct split actions, keep them.
                if u['id'] not in ['C05_K02A','C05_K02B']:
                    u['action']=s['screen'];u['first_frame']=s['first_frame'];u['framing']=s['framing']
                u['caption_safe_zone']=[{'text':q['text'],'box':q['box']}for q in s.get('caption_cues',[])]
    c['scene_list']=[{'scene_id':s['scene_id'],'cut':s['id'],'first_frame':s['first_frame'],'action':s['screen']} for s in c['shots']]
    extras=[x for x in c.get('text_assets',[])if x.get('mode')!='후편집 화면 자막']
    c['text_assets']=[{'cut':s['id'],'mode':'후편집 화면 자막','cues':s['caption_cues']}for s in c['shots']if s.get('caption_cues')]+extras
d['hero_cuts'].update(C06='K01',C07='K08',C08='K06',C09='K08',C10='K08')
d['recommendations']={'attendance':'C06 퇴근 좀 해주세요: 직원 퇴근이라는 절박한 목표에서 실제 사례를 배우러 가는 행동이 발생하고, 마지막 유령 상담 대기가 다시 행사 질문으로 연결된다. 창작적 추천이며 관객 반응 측정은 아니다.','opening':'C10 개막을 허가하지 않는 기계: 개막식 자체의 고장이 새 입장 의식을 만들며, 첫 발표자가 기록을 펴는 순간 실제 행사 시작으로 자연스럽게 넘어간다. 리본 동작은 생성 후 별도 확인.'}
d['status']='text revised; cross review and reconfirmation pending'
put(p,d)
print({c['id']:c['duration_seconds']for c in d['concepts']})
