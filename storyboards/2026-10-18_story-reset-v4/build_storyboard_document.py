"""Readable production document. Images and prompts remain separate originals."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
def t(v):
    if isinstance(v,(dict,list)): v=json.dumps(v,ensure_ascii=False)
    return str(v or '없음').replace('|','/').replace('\n','<br>')
def main():
    d=json.loads((R/'storyboards.json').read_text(encoding='utf-8-sig'))
    rows=['# 새 5안 스토리보드 · V4','', '기존 C01 36초 완성본을 보존한 별도 신규안입니다. 이 문서는 콘티·첫 프레임 제작 범위이며 영상 생성은 하지 않았습니다.','', '| 안 | 제목 | 목적 | 형식 | 핵심 웃음 | 길이 | 강도 | 난이도 | 추천 용도 |','|---|---|---|---|---|---|---|---|---|']
    for c in d['concepts']:
        rows.append('| '+' | '.join(t(v) for v in [c['id'],c['title'],c['purpose'],c['format'],c['comedy_engine'],str(c['duration_seconds'])+'초',str(c['bgrade_intensity'])+'/5',c['difficulty'],c['audience']])+' |')
    rows+=['','## 추천','']
    for k,v in d['recommendations'].items(): rows+=['- **'+k+':** '+t(v)]
    for c in d['concepts']:
        rows+=['','## '+c['id']+' · '+c['title'],'',c['logline'],'','**핵심 메시지:** '+c['core_message'],'','**첫 훅:** '+c['hook'],'','**전개:** '+t(c['three_act']),'','**마지막 연결:** '+c['final_action'],'','**차이:** '+c['difference'],'','**제작 판단:** '+c['difficulty_reason'],'','| 씬·컷 ID | 구간·길이 | 화면·인물 행동·구도 | 화면 자막 | 대사·내레이션 | 음악·효과음·정적 | 전환 | 웃음 또는 정보 전달 의도 |','|---|---|---|---|---|---|---|---|']
        for s in c['shots']:
            rows+=['| '+' | '.join(t(v) for v in [s['scene_id']+'/'+s['id'],f"{s['start']:g}–{s['end']:g}초 / {s['duration']:g}초",s['screen']+' / '+s['framing'],s['subtitle'],s['dialogue'],s['sound'],s['transition'],s['intent']])+' |']
        rows+=['','### 컷별 첫 프레임 대응','', '| 컷 | 실제 이미지 | 시작 상태 | 이후 동작 |','|---|---|---|---|']
        for s in c['shots']: rows+=['| '+s['id']+' | ['+s['image_file']+']('+s['image_file']+') | '+t(s['first_frame'])+' | '+t(s['next_motion'])+' |']
    rows+=['','## 사실·가정·확인 범위','','- 행사명: **2026년 품질팀 AI 실행 결과 발표 대회**. 개최 사실은 확인했습니다.','- 정확한 일시·장소·참석/추천/신청 방법·실제 과제·성과 수치·상금은 미확인으로 창작하지 않았습니다.','- 화면 속 인물과 사건은 허구입니다. 사내 시청·16:9는 제작 가정입니다.','- 참고 작품은 공식 설명·제작자 발언·일부 화면·자동자막을 확인했습니다. 전편 연속 감상·실제 음성 청취 또는 관객 반응 검증을 뜻하지 않습니다.','- 검수는 대본과 정지 첫 프레임에 대한 편집 판단입니다. 실제 영상 움직임·대사·립싱크 검증은 아닙니다.','- 프롬프트·참조 원본·후속 움직임은 scene_manifest.json, 수정 및 교차 의견은 review_summary.json에 기록합니다.','']
    (R/'STORYBOARDS.md').write_text('\n'.join(rows),encoding='utf-8')
if __name__=='__main__': main()
