from pathlib import Path
import json
R=Path(__file__).resolve().parent
p=R/'image_cross_reviews.json'
d=json.loads(p.read_text(encoding='utf-8-sig'))
d['reviews']['B']={
 'IA-001':'동의. K07 발 멈춤과 미소 확대가 실제 시작 이미지와 맞음.',
 'IA-002':'동의. K08 재킷을 열고 안주머니 명함을 꺼내는 순서를 명시.',
 'IA-003/IC-001':'동의. K02 단일 도식 기준 후속 합성 필요. 현재 합성 완료 아님.',
 'IA-004':'부분 동의. 건축 업무 연상은 있으나 허구 표시 및 실제 행사 과제라고 부르지 않는 처리로 충분.',
 'IC-002':'동의. 내부 조건 기록을 열어 회색 기록과 대조.',
 'IC-003':'동의. 기다림 뒤 정답 절망·오답 환호는 후속 영상 검수 대상.',
 'A_on_IB-003':'현재 곡선도 충분하다는 이견 수용. 당김 대비는 개선 제안.',
 'required_regeneration':False,'new_required_issues':[]
}
d['reviews']['C']={
 'IA-001':'동의. 이미 돌아본 시작 상태에서 발 멈춤·표정 확대. 동작 되감기 방지.',
 'IA-002':'동의. 손으로 재킷을 열고 안주머니 카드. 새 이미지 불필요.',
 'IA-003/IB-001':'동의. K02 단일 도식 기준, 후속 합성 필요로 명시.',
 'IA-004':'부분 동의. 건축 연상은 있으나 허구 초기환경으로 수용 가능. 실제 AI 건축 성과라는 설명 금지.',
 'IB-002':'동의. 표지 줄무늬가 아니라 내부 조건 기록 비교로 인과를 전달.',
 'IB-003':'동의·보완. 현재 곡선 자체는 충분, 질문 뒤 곡선이 펴지는 대비.',
 'required_regeneration':False,'new_required_issues':[]
}
d['PD_resolution']={
 'state':'동작 기록 수정 및 후속 합성 사항 반영',
 'files':['storyboards.json','future_production_notes.json'],
 'K07':'이미 약간 돌아본 첫 프레임으로 수정. 발 멈춤·미소 확대와 손 컷 전환.',
 'K08':'재킷 먼저 열기 후 카드 꺼내기.',
 'C02_notebook':'K02 유일 기준. 현재 PNG 복원 도식 차이는 남으며 후속 합성 필요.',
 'C03_records':'허구 초기환경 소품 수용. 주황 파일 안쪽 조건 기록을 열어 회색 기록과 비교.',
 'scope':'실제 영상·합성·음성·관객 반응은 미검증.'
}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('A/B/C first 26 cross-review recorded.')
