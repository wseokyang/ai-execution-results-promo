from pathlib import Path
import json
R=Path(__file__).resolve().parent
p=R/'image_reviews_C04.json';d=json.loads(p.read_text(encoding='utf-8'))
d['reviews']['C']={
 'status':'pass_no_required_image_revision',
 'contact_sheet':'contact_sheets/C04_all_cuts.jpg',
 'individual_pngs':['K01b.png','K02.png','K07.png','K08_v2.png'],
 'findings':[
  {'id':'IC-004','cut':'C04 K02','severity':'future_production_note','issue':'닫힌 노트북 열기→입력. 입력 손과 집중 얼굴을 함께 볼 시간 필요.'},
  {'id':'IC-005','cut':'C04 K07','severity':'suggestion','issue':'감독은 다리를 꼬고 앉음. 다리 풀기→몸 앞으로→일어나기→대역이 의자 가져가기 순서. 전달은 대사와 겹쳐 실제6초는 영상검수.'},
  {'id':'IC-006','cut':'C04 K01b','severity':'future_production_note','issue':'모니터 내 하네스 대역 움직임 합성 시 테두리·전경 인물 유지. 현재 정지 이미지로 움직임 검증 안 함.'}
 ],
 'observed':'액션에서 촬영 공개로 전환, 인물·옷·파일 구별. K07 감독검정의자→K08 대역점유/감독서있음 명확. 행사명여백 적합.',
 'first26_notes_confirmed':True,
 'limits':'정지 이미지·연출 계획 검수. 동작·음성·실제 반응 미검증.'
}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('C04 A/B/C independent reviews saved.')
