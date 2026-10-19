from pathlib import Path
import json
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    d=read('storyboards.json')
    if not (R/'storyboards_before_review.json').exists():put('storyboards_before_review.json',d)
    cs={c['id']:c for c in d['concepts']};c2={s['id']:s for s in cs['C02']['shots']};c4={s['id']:s for s in cs['C04']['shots']}
    c2['K01']['screen']=c2['K01']['screen'].replace('같은 제품 사진과','서로 다른 제품 사진과',1)
    c2['K02']['sound']='추격 박자만 빠지고 낮은 스릴러 베이스는 유지한다. 트레이가 멈추는 금속 소리. K05의 수갑 클릭 뒤 음악 중단과 강도를 구별한다.'
    c2['K08']['postproduction_notes']+=' V8 호흡: 3초 안에서 사진을 붙인 손이 물러난 뒤 중앙 사진이 약0.8~1초 읽히게 둔다. 새 대사·행동을 추가하지 않는다.'
    c4['K09']['sound']='컷 시작0~1.7초: 망토에서 숟가락을 꺼내며 CM의 “지휘관부터.” 약1.2초. 1.7~2.3초 턱·시선 유지, GU의 답은 없음. 2.3~5.3초(전체30.3~33.3초): 첫 사례 시작 안내 약3초. 끝0.7초는 그릇·공간음. 제목은28–34초 전체6초, 두 발화는 겹치지 않는다.'
    c4['K09']['postproduction_notes']=c4['K09']['postproduction_notes'].replace('컷 시작2초 안에 끝내고','컷 시작1.7초까지 마치고 턱·시선을 잠깐 유지한 뒤')
    for c in d['concepts']:
        if c['id'] in ['C01','C03','C05']:assert c==read('retained_concept_'+c['id']+'.json')
    put('storyboards.json',d)
    put('storyboard_revision_disposition.json',{'PD':'/root','required_findings':0,'decisions':[{'id':'A-001','decision':'applied','reason':'같은 사진벽이라는 공간 뜻을 제품 종류로 오해하지 않게 명료화'},{'id':'B-001','decision':'applied','reason':'K02 낮은 베이스 유지로 K05 음악절단만 더 선명하게'},{'id':'C-001','decision':'applied_as_production_note','reason':'3초 내 사진 읽는0.8~1초, 새컷/길이변경없음'},{'id':'C-002','decision':'applied','reason':'1.7초까지 짧은발화,2.3초까지 시선호흡.총6초유지'}]})
    print('Four optional reviewer notes applied without structural change.')
if __name__=='__main__':main()
