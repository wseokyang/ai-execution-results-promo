from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def cell(value):
    if isinstance(value, (list, dict)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value or '없음').replace('|', '\\|').replace('\n', '<br>')


def main():
    data = json.loads((ROOT / 'storyboards.json').read_text(encoding='utf-8'))
    lines = [
        '# B급 코미디 신규 5안 · 컷별 제작 콘티', '',
        '기존 완성 C01 36초 영상은 그대로 보존한다. 이 문서의 신규 C01~C05는 새 기획의 로컬 번호이며 기존 완성 영상의 번호와 구별한다. 이번 범위는 시나리오·콘티·컷별 첫 프레임 이미지다. Flow 업로드와 영상·음원 생성은 하지 않았다.', '',
        '이미지는 각 컷의 시작 상태이며, 표의 화면 설명은 이후에 일어날 동작이다. 엔딩 PNG는 글자 없는 배경판이고, 정확한 행사명 조판 예시는 HTML 열람본에서 별도로 보여 준다.', '',
        '## 5안 비교', '',
        '| 신규 안 | 목적 | 형식 | 핵심 웃음 장치 | 길이 | B급 강도 | 제작 난이도 | 추천 용도 |',
        '| --- | --- | --- | --- | --- | --- | --- | --- |',
    ]
    for index, c in enumerate(data['concepts'], 1):
        lines.append('| ' + ' | '.join(cell(x) for x in [f"{index}. {c['title']}", c['purpose'], c['format'], c['comedy_engine'], f"{c['duration_seconds']}초 / {len(c['shots'])}컷", f"{c['bgrade_intensity']}/5", c['difficulty'], c['audience']]) + ' |')
    lines += ['', 'B급 강도와 제작 난이도는 기획 판단이다. 실제 관객 반응이나 향후 생성 성공률을 측정한 수치가 아니다.', '',
              '## 추천', '',
              '- **참석 독려: 신규 4안 「관객이 사라지는 마술」.** 관객이 자리를 옮기는 이유를 뒤늦게 공개해, 결과보다 직접 실행한 과정에 관심이 생긴다는 참석 동기를 행동으로 보여 준다.',
              '- **행사 현장 도입: 신규 2안 「성공 장면 되감기」.** 성공 화면에서 시행착오로 거슬러 가려는 소동이 “처음엔, 여기서 막혔습니다”라는 발표 첫 문장으로 이어져 실제 사례 발표로 넘기기 쉽다.',
              '- **과장된 B급 연기 우선: 신규 1안 「이 상품은 배송이 어렵습니다」.** 사람의 경험을 배송하려는 황당한 목표가 쇼호스트 본인의 출고로 돌아온다. 신규 3안은 과도한 축하 연기, 신규 5안은 진지한 첩보 연기와 동시 동작에 강점이 있다.', '']
    for index, c in enumerate(data['concepts'], 1):
        lines += [f"## 신규 {index}안 · {c['title']}", '', f"**한 줄 이야기:** {c['logline']}", '', f"**핵심 메시지:** {c['core_message']}", '',
                  f"**첫 훅:** {c['hook']}", '', f"**웃음 구조:** {c['comedy_engine']}", '', f"**마지막 연결:** {c['final_action']}", '',
                  f"**다른 안과의 차이:** {c['difference']}", '', f"**대상·상영 상황:** {c['audience']}", '',
                  '| 씬·컷 ID | 구간·길이 | 화면·인물 행동·구도 | 화면 자막 | 대사·내레이션 | 음악·효과음·정적 | 전환 | 웃음 또는 정보 전달 의도 |',
                  '| --- | --- | --- | --- | --- | --- | --- | --- |']
        for s in c['shots']:
            row = [f"{c['id']}-{s['scene_id']} / {s['id']}", f"{s['start']:g}~{s['end']:g}초 ({s['duration']:g}초)", s['screen'] + '\n구도: ' + s['framing'], s['subtitle'], s['dialogue'], s['sound'], s['transition'], s['intent']]
            lines.append('| ' + ' | '.join(cell(x) for x in row) + ' |')
        lines += ['', '### 컷별 첫 프레임과 후속 동작', '']
        for s in c['shots']:
            lines += [f"**{c['id']}-{s['id']} · {s['scene_id']}**", '', f"- 첫 프레임: {s['first_frame']}", f"- 다음 동작: {s['next_motion']}", f"- 진입 상태: {s['continuity_in']}", f"- 종료 상태: {s['continuity_out']}", f"- 기본 이미지 경로: `{s['image_file']}`. 최종 선택 파일은 `scene_manifest.json` 기준.", '']
        lines += ['### 인물·소품·화면 기준', '', '```json', json.dumps({'characters': c['characters'], 'visual_style': c['visual_style'], 'continuity': c['continuity']}, ensure_ascii=False, indent=2), '```', '', f"제작 난이도 근거: {c['difficulty_reason']}", '']
    lines += ['## 근거와 미확인 사항', '',
              '- 행사명은 **2026년 품질팀 AI 실행 결과 발표 대회**로 표기한다. 실제 개최는 사용자 확인을 따르며 `(안)`을 붙이지 않는다.',
              '- 행사 세부 일시·장소·참석 방법·상금·성과 수치는 확정 근거가 없어 넣지 않았다. 원자료의 작성일을 개최일로 사용하지 않는다.',
              '- qrew 참고는 원참고 분석문·대표 프레임·최종 스토리보드·편집 관련 기록을 확인한 범위다. 전체 영상 연속 감상이나 실제 음원 청취를 했다고 주장하지 않는다.',
              '- 연구 근거는 `research_notes.md`, 선정 이유는 `selected_concepts.json`, 실제 이미지 프롬프트·참조는 `scene_manifest.json`, 검수와 처리 결과는 `review_summary.json`에 기록한다.',
              '- 허구의 판매·촬영·스포츠·마술·첩보 상황이다. 실제 대회 운영 방식이나 우승 결과를 재현하는 장면이 아니다.', '']
    (ROOT / 'STORYBOARDS.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    print('STORYBOARDS.md: 5 concepts, full shot tables and first-frame continuity')


if __name__ == '__main__':
    main()
