from pathlib import Path
import json
R=Path(__file__).resolve().parent
def prose(x):return ' / '.join(str(v) for v in x) if isinstance(x,list) else str(x or '없음')
def md(x):return prose(x).replace('|','／').replace('\n','<br>')
def main():
 d=json.loads((R/'storyboards.json').read_text(encoding='utf-8-sig'))
 rows=['# 3안 유지 · 네 안 교체 — V5','', 'V4 3안 「환경까지 가져왔습니다」의 콘티와 채택 이미지 8장은 그대로 유지했습니다. 새 1·2·4·5안과 기존 완성 C01 동영상은 서로 다른 작업물입니다. 동영상·음원 생성과 Flow 업로드는 하지 않았습니다.','', '## 비교','', '| 안 | 제목 | 목적 | 형식·웃음 | 길이 | B급 강도 | 제작 난이도 |','|---|---|---|---|---|---|---|']
 for c in d['concepts']: rows.append('| '+ ' | '.join(map(md,[c['id'],c['title'],c['purpose'],c.get('comedy_engine',c.get('format')),str(c['duration_seconds'])+'초',str(c.get('bgrade_intensity',4))+'/5',c['difficulty']]))+' |')
 rows+=['','제작 난이도는 계획 단계 판단이며 Flow 기능·생성 성공·실제 관객 반응을 보장하지 않습니다.','','## 용도 제안','','참석 독려에는 유지한 **C03 「환경까지 가져왔습니다」**를 우선합니다. 성공 결과뿐 아니라 실행 조건까지 보러 온다는 이유가 사건과 직접 연결됩니다. 새 네 안 중에서는 **C01 「성공 자세 교정원」**이 겉모습을 흉내 내기보다 당사자의 작업 이야기를 듣자는 초대를 가장 분명하게 만듭니다.','','행사 현장 도입에는 **C05 「아빠가 벌써 온다」**를 제안합니다. 가족의 과장된 후폭풍에서 실제 AI 활용 사례 소개로 넘어갈 수 있고 31초로 짧습니다. **C02**는 관심이 유명인에서 실행 경험자에게 옮겨가는 장면을 발표자 소개에 연결하기 좋습니다. 이는 편집 판단이며 사용자의 선택이나 관객 반응을 확인했다는 뜻은 아닙니다.','']
 for c in d['concepts']:
  rows+=['## '+c['id']+' · '+c['title'],'',c['logline'],'','핵심 메시지: '+c['core_message'],'','마지막 연결: '+c['final_action'],'','| 씬·컷 ID | 구간·길이 | 화면·인물 행동·구도 | 화면 자막 | 대사·내레이션 | 음악·효과음·정적 | 전환 | 웃음 또는 정보 전달 의도 |','|---|---|---|---|---|---|---|---|']
  for s in c['shots']:
   rows.append('| '+' | '.join(map(md,[s['scene_id']+'/'+s['id'],f"{s['start']}–{s['end']}초 ({s['duration']}초)",s['screen']+' / '+s['framing'],s['subtitle'],s['dialogue'],s['sound'],s['transition'],s['intent']]))+' |')
  rows+=['','### 첫 프레임과 후속 동작','','| 씬·컷 | 실제 PNG | 첫 프레임 | 다음 움직임 |','|---|---|---|---|']
  for s in c['shots']:rows.append('| '+' | '.join(map(md,[s['scene_id']+'/'+s['id'],f"[{s['id']}]({s['image_file']})",s['first_frame'],s['next_motion']]))+' |')
  rows+=['','연속성: '+prose(c.get('continuity','개별 컷 기준 참조.')),'','제작 난이도: '+c['difficulty']+' — '+c['difficulty_reason'],'']
 rows+=['## 전달 정보와 확인 범위','','행사명은 **2026년 품질팀 AI 실행 결과 발표 대회**입니다. AI 실행 과제와 활용 역량 향상 경험을 공유하는 목적을 반영했습니다. 정확한 일시·장소·참석/추천/신청 방법·실제 발표 과제·성과 수치·상금은 미확인입니다. 인물과 과장된 사건은 허구입니다. 품질팀 내부 시청과 16:9는 제작 가정입니다.','','독립 생성 PNG와 정확한 프롬프트·참조 이미지·후속 동작은 [scene_manifest.json](scene_manifest.json), 검토 의견과 처리 근거는 [review_summary.json](review_summary.json)에 있습니다. 대표 이미지는 움직임·대사·립싱크의 완성본이 아닙니다. 새 음성을 듣거나 실제 관객 반응을 측정하지 않았습니다.','','[전체 이미지 콘티](index.html) · [3안·기존 영상 보존](preservation_manifest.json) · [레퍼런스 확인 범위](reference/V5_REFERENCE_SCOPE.md)','']
 (R/'STORYBOARDS.md').write_text('\n'.join(rows),encoding='utf-8')
if __name__=='__main__':main()
