from pathlib import Path
import json
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 d=read('storyboards.json');cs={c['id']:c for c in d['concepts']}
 c=cs['C02'];s=c['shots'][-1]
 s['screen']='KN이 용 안에서 비장하게 큰 숨을 모아 분다. 용 입의 붉은 종이 세 줄은 초라하게 한 번 팔랑이고 다시 처진다. 기사는 포기하지 않고 다시 숨을 들이마신다. 행사명은 오른쪽 닫힌 목재 문 위 대비 패널에 2~3행으로 6초 유지한다. 기사 허리·두 다리와 왼쪽 종이 불꽃은 가리지 않는다.'
 s['framing']='외부 고정 측면 미디엄 와이드. 용 입의 종이와 밖에 남은 청록 허리·두 다리를 함께 잡는다. 자막 영역은 오른쪽 닫힌 목재 문의 안쪽 면(대략 화면 x 75~96%, y 22~67%). 짙은 반투명 패널 또는 어두운 그라데이션, 행사명 2~3행·6초. 빈 상단 석벽을 전제하지 않는다.'
 s['postproduction_notes']='행사명 3행 예: 2026년 품질팀 / AI 실행 결과 / 발표 대회. 보조 문구는 같은 패널 아래 작은 2행. 기사·불꽃 비침범을 우선하며 실제 합성 후 글자 크기와 대비를 재확인한다.'
 c['shots'][0]['postproduction_notes']='붉은 종이 띠는 의도적인 B급 단서로 유지. 초반 강한 역광·빠른 흔들림·굉음과 마지막 약한 팔랑임을 대비한다. 띠만 따로 확대하거나 오래 멈추지 않는다.'
 c=cs['C04'];s=c['shots'][-1]
 s['framing']='고정 내부 미디엄 와이드. 지도·세 얼굴·페달을 보존한다. 행사명은 화면 최상단의 어두운 목재 공간에 한 줄로 배치하고 얕은 어두운 그라데이션을 받친다. 세 사람의 머리와 얼굴을 덮지 않는다.'
 s['subtitle']='35–42초: 2026년 품질팀 AI 실행 결과 발표 대회. 보조 메시지는 내레이션으로 전달하고 화면의 추가 문장은 생략한다.'
 s['postproduction_notes']='제목을 최상단(대략 y 1~6%) 한 줄로 7초 유지. 실제 합성에서 720p 기준 가독성을 확인한다. 머리·얼굴·지도·페달 영역은 피하고 내레이션을 받는 별도 홍보 문구를 중복해서 쌓지 않는다.'
 c=cs['C05'];s=c['shots'][-1]
 s['framing']='외부 고정 와이드. K04 기준 크기·S자 목·굽힌 무릎을 유지한다. 밝은 지붕 하면과 대비되는 오른손의 손목·손가락 동작을 보이게 한다. 행사명은 발·전선·잭 아래의 하단 포장면에 어두운 그라데이션을 받쳐 배치한다. 얼굴·이어컵·양손을 덮지 않는다.'
 s['postproduction_notes']='행사명은 하단 포장면(대략 y 88~97%)에 한 줄로 6초. 시작 안내는 음성으로 전달하며 별도 보조 자막은 생략한다. 실제 합성 후 가독성·전선 및 작업자 발 비침범 확인. 손짓은 청취 확인에 대한 응답이다.'
 s['subtitle']='32–38초: 2026년 품질팀 AI 실행 결과 발표 대회. 34–38초 시작 안내는 음성으로 전달한다.'
 s['continuity_in']='K07의 이어컵 설치 완료 뒤 TE 하강·사다리 정리의 시간을 점프컷으로 생략한다. FM의 청취 확인 질문은 이 생략 뒤의 응답과 오프스크린 음성으로 연결한다. 질문을 하려는 손짓이 아님. 접힌 목·무릎·포치·전선·잭·누운 기둥 유지.'
 c['shots'][-2]['transition']='설치 완료 뒤 기사 하강·사다리 정리 시간을 생략하는 와이드 점프컷. FM 청취 확인 질문을 소리로 연결하되 반복하지 않는다.'
 c['shots'][-2]['postproduction_notes']='K07은 K06/K08 와이드와 반대 사선의 귀 높이 접사. 설치 대상은 K08에 보이는 한쪽 귀로 고정한다. 화면 좌우가 바뀐다고 실제 귀를 바꾸지 않는다. 실제 영상 제작에서는 전선·건물 방향까지 대조할 것. 정지 이미지 단계에서 귀 연결 동작 검증 완료라고 기록하지 않는다.'
 for cid in ['C02','C04','C05']:
  c=cs[cid]
  for scene in c.get('scene_list',[]):
   shot=next(s for s in c['shots'] if s['id'] in scene['linked_cuts'])
   scene['framing']=shot['framing'];scene['next_motion']=shot['next_motion']
   scene['continuity']=shot['continuity_in']+' / '+shot['continuity_out']
   if 'postproduction_notes' in shot:scene['postproduction_notes']=shot['postproduction_notes']
 for cid in ['C01','C03']:assert cs[cid]==read('retained_concept_'+cid+'.json')
 d['image_review_document_revision']='C-I001 closed in text; A/B/C confirmation pending'
 put('storyboards.json',d)
 put('image_revision_disposition.json',{'status':'document_revisions_applied_pending_three_confirmations','PNG_changes_after_independent_review':0,'retained_concepts_unchanged':['C01','C03'],'findings':[
 {'ids':['C-I001','A-I003','B-I003'],'disposition':'document_fixed','reason':'C02 K09 screen/framing and S09 scene now use right closed door contrast panel, 2–3 title lines, 6 seconds, knight/flames protected. C04/C05 actual overlay positions and duplicate subtitle removal also specified.','paths':['storyboards.json','STORYBOARDS.md','index.html']},
 {'ids':['A-I001','B-I002','C-I002'],'disposition':'intentional_B_grade_clue_retained_with_motion_note','reason':'Paper strips do not reveal apparatus or normal door. Preserve same physical prop and early/late light/motion contrast.'},
 {'ids':['A-I002','B-I001'],'disposition':'future_motion_continuity_note_added','reason':'Same ear and reverse-oblique close-up defined; installer descent and ladder adjustment omitted between shots. Actual moving continuity remains unverified.'}
 ],'limits':['No new PNG needed by the three independent/cross reviews','No actual text-composited movie, motion, audio or audience-response validation']})
 print('Image review document fixes applied; C01/C03 unchanged.')
if __name__=='__main__':main()
