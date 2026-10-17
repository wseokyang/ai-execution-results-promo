"""Record small coordinate corrections, without changing story beats or timings."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
path = ROOT / 'storyboards.json'
data = json.loads(path.read_text(encoding='utf-8'))
c = next(x for x in data['concepts'] if x['id'] == 'C02')
c['characters'][0]['description'] = c['characters'][0]['description'].replace('왼쪽 겨드랑이', '배우 본인의 오른쪽 겨드랑이(정면 화면 왼쪽)')
shots = {s['id']: s for s in c['shots']}
shots['K01']['first_frame'] = 'P의 왼손과 B의 오른손이 머리 위에서 서로 10cm 떨어져 있다. P의 오른쪽 겨드랑이(정면 화면 왼쪽)에 노란 노트. D는 왼쪽에서 슬레이트를 들어 올리기 직전. 뒤의 넓은 종이 띠는 중앙이 찢어져 양끝이 아래로 처져 있다.'
shots['K01']['continuity_out'] = '두 배우가 어색한 역방향 자세. 노트는 P 본인의 오른쪽 옆구리(정면 화면 왼쪽)에 유지.'
shots['K02']['first_frame'] = shots['K02']['first_frame'].replace('T는 오른쪽 뒤에서 의자를 향해 정상 보폭으로 접근.', 'T는 화면 왼쪽 의자 옆까지 정상 보폭으로 접근해 의자를 잡으려 한다. 컷 사이 T의 접근 일부는 생략한다.')
shots['K03']['first_frame'] = shots['K03']['first_frame'].replace('왼쪽 겨드랑이', '오른쪽 겨드랑이(정면 화면 왼쪽)')
shots['K04']['screen'] = shots['K04']['screen'].replace('처음부터 왼쪽에 끼고 있던', '처음부터 본인의 오른쪽 옆구리에 끼고 있던')
shots['K04']['first_frame'] = shots['K04']['first_frame'].replace('왼쪽 겨드랑이의 닫힌 노란 노트에 오른손', '오른쪽 겨드랑이의 닫힌 노란 노트에 왼손')
data['version'] = 'pd-final-2.2-image-coordinate-alignment'
path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
brief = ROOT / 'image_review_brief.md'
text = brief.read_text(encoding='utf-8')
text = text.replace('- C02: 왼쪽 겨드랑이 노트,', '- C02: 배우 P의 오른쪽 겨드랑이(정면 화면 왼쪽) 노트,')
note = '\nC02 실제 기준 이미지가 모든 컷에서 노트를 P 본인의 오른쪽 옆구리에 유지하므로, 최종 콘티에서 배우의 손 명칭을 이에 맞췄다(P 왼손/B 오른손 하이파이브). K02의 T는 화면 왼쪽 의자 옆까지 접근한 시작이며, K01→K02 접근 일부를 생략하는 것으로 수용했다. 방향 이름만 정정하고 역연기/정방향 작업의 대비와 소품 소유는 유지한다.\n'
if note not in text:
    text += note
brief.write_text(text, encoding='utf-8')
record = {
    'status': 'pd_coordinate_alignment',
    'C05': 'A screen-left/B screen-right; inner bag hands A left/B right, outer flyer hands A right/B left.',
    'C02': 'Notebook under actor P right arm (screen-left); high-five P left/B right. T already approaches chair from screen-left in K02; brief approach is cut out.',
    'unchanged': ['story beats', 'durations', 'cut count', 'dialogue', 'prop ownership'],
    'basis': 'Artist observation and PD actual image inspection; reviewers receive corrected final storyboards.',
}
(ROOT/'pd_coordinate_alignment.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Final C02 coordinates aligned; director drafts preserved.')
