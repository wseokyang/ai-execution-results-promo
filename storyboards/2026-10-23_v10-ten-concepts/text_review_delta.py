from pathlib import Path
import json
R=Path(__file__).resolve().parent;p=R/'storyboards.json';d=json.loads(p.read_text(encoding='utf8'))
cs={c['id']:c for c in d['concepts']}
def s(cid,k):return next(s for s in cs[cid]['shots']if s['id']==k)
s('C06','K04')['caption_cues'][0]['text']='이 한 건만 확인하면 끝.'
s('C07','K06')['screen']='CW가 줄을 한 번 당겨 방향을 만든다. EX가 설명을 계속하며 CW 쪽으로 걸어오고 Q1/Q2도 수첩을 보려고 함께 걷는다. 도착한 Q1/Q2가 다시 CW 앞을 가려, CW는 빈틈으로 고개를 내밀다 멈춘다. 기대하던 둘만의 자리는 설명회 맨 앞자리가 된다.'
s('C09','K01')['screen']+=' HU의 시선은 하사되는 결과판을 지나 받침대의 낡은 기록으로 향한다.'
for x in cs['C03']['text_assets']:
    if x.get('mode')=='후편집 소품 도식':x['content']='허구 사례용 큰 기호만 사용. K03 화면: 기준/이번 결과 두 열에 같은 청록 원·세로선·사각형 배열과 일치 테두리. K06 회색/주황 안쪽 페이지 상단에는 같은 청록 원 입력기호. 하단 회색은 원→사각형→체크, 주황은 원→체크→사각형 및 교정 화살표로 확인·수정 순서 차이를 단순 시각화. 양쪽 공통 상단기호에 노랑 테두리2초. 수치·실제 과제명·성과 주장이 아니며 원인 입증도 아님. 정확 문자는 잘됐던 작업 기록/시행착오 기록 라벨만.'
for c in d['concepts']:
    for sh in c['shots']:
        sh['next_motion']=sh['screen'];sh['subtitle']=' / '.join(q['text']for q in sh.get('caption_cues',[]))or'없음'
        for q in sh.get('caption_cues',[]):
            q['start']=round(q['start'],2);q['end']=round(q['end'],2)
        if 'mute_readability'in sh:sh['mute_readability']['visible_cause_effect']=sh['screen']
        for u in d['generation_units']:
            if u['concept_id']==c['id']and u['linked_shot']==sh['id']:
                if u['id']not in ['C05_K02A','C05_K02B']:u['action']=sh['screen']
                u['caption_safe_zone']=[{'text':q['text'],'box':q['box']}for q in sh.get('caption_cues',[])]
    c['scene_list']=[{'scene_id':sh['scene_id'],'cut':sh['id'],'first_frame':sh['first_frame'],'action':sh['screen']}for sh in c['shots']]
    extras=[x for x in c['text_assets']if x.get('mode')!='후편집 화면 자막']
    c['text_assets']=[{'cut':sh['id'],'mode':'후편집 화면 자막','cues':sh['caption_cues']}for sh in c['shots']if sh.get('caption_cues')]+extras
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('B refinements and precise clue graphics synchronized.')
