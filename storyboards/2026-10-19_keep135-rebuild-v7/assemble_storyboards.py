from pathlib import Path
import json

R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def main():
    new={c['id']:c for c in read('director_draft.json')['concepts']}
    cs=[]
    for cid in ['C01','C02','C03','C04','C05']:
        c=read('retained_concept_'+cid+'.json') if cid in ['C01','C03','C05'] else new[cid]
        elapsed=0
        for s in c['shots']:
            assert s['start']==elapsed and s['end']-s['start']==s['duration']
            elapsed=s['end']
        assert elapsed==c['duration_seconds'] and elapsed<=60
        cs.append(c)
    d={
        'run_id':R.name,'status':'full_storyboard_review_pending','concepts':cs,
        'hero_cuts':{'C01':'K08','C02':'K09','C03':'K02','C04':'K09','C05':'K07'},
        'scope':'V6 C01/C03/C05 unchanged; new C02/C04 storyboards and actual first frames only; no Flow/video/audio',
        'recommendations':{
            'attendance':'사전 참석 독려에는 C02의 수사극을 제안합니다. AI가 묶은 단서를 실제 확인한 과정을 보여주고, 결과만 보아서는 놓치는 원인을 함께 듣자는 이유로 연결합니다. 관객 반응을 측정한 판단은 아닙니다.',
            'opening':'행사장 시작 영상에는 사용자가 좋다고 한 C05 「괴수는 퇴근할 수 없다」를 유지해 제안합니다. 시작 전 안내와 이어폰 설치를 거쳐 AI 실행 사례 발표의 시작으로 이어집니다.'
        },
        'notes':[
            'C01/C03/C05는 V6 전체 객체와 채택25장 원본 바이트 유지. 기존 완성 C01 36초 v07 영상 별도 보존.',
            '신규2안은 허구의 활용 사례로 AI 산출물과 사람의 확인, 경험 공개를 이야기 안에서 연결한다.',
            '행사 일정·장소·실제 성과·상금은 만들지 않음. 16:9와 사내 시청은 제작 가정.',
            '동작·음성·립싱크·관객 반응은 이 단계의 검증 범위가 아님.'
        ]
    }
    (R/'storyboards.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print([(c['id'],c['duration_seconds'],len(c['shots'])) for c in cs])
if __name__=='__main__':main()
