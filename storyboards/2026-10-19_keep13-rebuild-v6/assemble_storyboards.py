from pathlib import Path
import json
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8'))
def main():
 draft=read('director_draft.json');new={c['id']:c for c in draft['concepts']};cs=[]
 for cid in ['C01','C02','C03','C04','C05']:
  c=read('retained_concept_'+cid+'.json') if cid in ['C01','C03'] else new[cid]
  elapsed=0
  for s in c['shots']:
   assert s['start']==elapsed and s['end']-s['start']==s['duration'];elapsed=s['end']
  assert elapsed==c['duration_seconds'] and elapsed<=60
  cs.append(c)
 d={'run_id':R.name,'status':'full_storyboard_review_pending','concepts':cs,'hero_cuts':{'C01':'K08','C02':'K08','C03':'K02','C04':'K08','C05':'K07'},'scope':'V5 C01/C03 unchanged; new C02/C04/C05 storyboards and first frames only; no Flow/video/audio','recommendations':{'attendance':'사전 참석 독려에는 새 C04 「잠입 성공」을 우선 제안합니다. 잠입 계획과 실제 결과의 차이가 연속 사건으로 커지고, 실행한 사람의 이야기를 듣자는 이유로 이어집니다. 사용자 선택이나 관객 반응을 확인한 판단은 아닙니다.','opening':'행사장 시작 영상에는 새 C05 「괴수는 퇴근할 수 없다」를 제안합니다. 시작 전 안내와 이어폰 설치를 거쳐 마지막에 실제 AI 실행 사례 발표의 시작으로 연결합니다.'},'notes':['C01/C03는 V5 전체 객체와 채택17장 원본 바이트 유지. 기존 완성 C01 36초 v07 영상은 별도 보존.','새3안의 인물·사건은 허구이며 행사 일정·장소·성과·상금은 만들지 않음.','16:9와 사내 시청은 제작 가정. 동작·음성·립싱크·관객 반응 검증은 이 단계 범위가 아님.']}
 (R/'storyboards.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print([(c['id'],c['duration_seconds'],len(c['shots'])) for c in cs])
if __name__=='__main__':main()
