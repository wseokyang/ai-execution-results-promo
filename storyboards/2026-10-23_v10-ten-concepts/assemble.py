from pathlib import Path
import json
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=read(R/'existing_revised.json');n=read(R/'new_five_draft.json')
d['concepts']+=n['concepts'];d['generation_units']+=n['generation_units']
d['scope']='기존 C01~C05 이야기 보완과 신규 C06~C10 선택용 콘티·시작 이미지. 모든 자막은 후편집. Flow 실행 없음.'
d['status']='ten-concept text review draft'
d['notes']=['2026-10-23 최신 사용자: 총10안 선택, 화면+후처리 자막, 다양한 캐릭터. 영상은 후속 Flow.','기존 V9 이미지44장 중 새 동작 전 상태와 맞는 자료를 재사용. 새로운 안의 모든 씬 이미지는 실제 생성 후 별도 검수.','기존 완성 영상 및 V9 자료는 보존. C03 원본 재사용 우선. 정지 콘티 검수를 영상 생성 성공으로 해석하지 않음.']
d.pop('old_vs_new_summary',None)
d['recommendations']={'attendance':'선정·교차 검토 뒤 확정','opening':'선정·교차 검토 뒤 확정'}
castnotes=read(R/'CAST_CONTINUITY_NOTES.json')['observations']
for c in d['concepts']:
    for a in c['characters']:
        for x in castnotes:
            if x['concept_id']==c['id'] and x['character_id']==a['id']:a['description']+=' '+x['append']
    for s in c['shots']:
        s['next_motion']=s['screen']
        s['subtitle']=' / '.join(q['text'] for q in s.get('caption_cues',[])) or '없음'
    c['scene_list']=[{'scene_id':s['scene_id'],'cut':s['id'],'first_frame':s['first_frame'],'action':s['screen']} for s in c['shots']]
    extras=[x for x in c.get('text_assets',[]) if x.get('mode')!='후편집 화면 자막']
    c['text_assets']=[{'cut':s['id'],'mode':'후편집 화면 자막','cues':s['caption_cues']} for s in c['shots'] if s.get('caption_cues')]+extras
    if c['id']=='C01':c['three_act']=['0–6.5초: 코치가 성공 자세의 권위를 주장, 수강생이 몸을 맞춤.','6.5–18.5초: 실제 사진 원본 공개, 첫 수강생은 자세 대신 작업 과정에 관심.','18.5–37.5초: 코치는 착지까지 신교본으로 만들고 남은 수강생이 복제. 행사로 연결.']
    if c['id']=='C04':
        c['three_act']=['0–11초: 숨은 병사의 허기와 아무도 없다는 신고가 충돌.','11–25초: 수저 요청 모순 후보와 원문 확인, 배식 뚜껑 열기.','25–37초: 세 배식창 공개와 지휘관 자기 숟가락, 실제 행사 시작으로 연결.']
        c['continuity']=[x.replace('오른쪽 첨부 식사 / 물 / 수저를 큰 구절로 대조한다. AI 문서 대조·확인 후보 라벨만 쓴다.','오른쪽 첨부 수저 요청을 큰 구절로 대조한다. 작은 머리말 AI 대조·확인 필요를 같은 화면에 쓴다. 식사/물은 원문에만 남긴다.') for x in c.get('continuity',[])]
    if c['id']=='C05':c['three_act']=['0–15초: 입구 독점을 위해 기둥 제거→몸으로 가로막기→지붕을 받치는 기둥이 됨.','15–35초: 짧은 잭과 떠나지 못하는 대기, 궁금해진 행사, 구조 기대와 이어컵 설치 반전.','35–43초: 엄지 답신도 못 하고 다시 지지, 작은 끄덕임 뒤 행사 시작.']
    if c['id']=='C01':c['difference']='몸모양을 모방하는 교습과 실제 작업 경험에 관심을 갖는 선택. 코치는 사고까지 새 권위로 편입한다. 다른 안의 수사·배송·잠입·침입·괴담·결투·공연·외교·개막 의식과 구별되는 교습소 이야기.'
    if c['id']=='C05':c['difference']='입구를 독점하려던 위협자가 입구를 떠날 수 없는 구조 지지대가 된다. C03 배송기사의 작업 종료·안도와 달리 괴수는 끝까지 몸이 묶여 있고 새 관객이 된다. 사다리는 구조 기대에서 청취 지원으로 뜻이 바뀐다.'
put(R/'storyboards.json',d)
print(len(d['concepts']),'concepts',len(d['generation_units']),'units')
