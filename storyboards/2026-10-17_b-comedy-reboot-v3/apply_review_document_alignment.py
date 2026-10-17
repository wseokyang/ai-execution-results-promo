from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
path=ROOT/'storyboards.json'
data=json.loads(path.read_text(encoding='utf-8'))
concepts={c['id']:c for c in data['concepts']}
c1=concepts['C01']
c1['continuity']['action_limits']='H는 웅크린 채 자발적으로 시범한다. W가 잡은 화면 오른쪽의 높은 옆판만 어깨 아래까지 접고 얼굴과 팔은 자유롭게 남긴다. H는 접힐 패널 가까이의 손을 먼저 거둔다. 새 전면 뚜껑을 만들어 닫거나 테이프를 사람에게 붙이지 않는다.'
for s in c1['shots']:
    if s['id'] in ['K05','K06']:
        for key in ['screen','first_frame','next_motion','continuity_in','continuity_out']:
            s[key]=s[key].replace('앞 덮개','화면 오른쪽의 높은 옆판').replace('전면 덮개','화면 오른쪽의 높은 옆판')
s=next(s for s in c1['shots'] if s['id']=='K06')
s['screen']='H가 접힐 옆판 가까이의 손을 잠깐 안으로 거둔다. W가 B3 화면 오른쪽의 높은 옆판을 H의 어깨 아래까지만 접고 바퀴 받침을 오른쪽 출고 통로로 민다. H는 카메라를 따라 광고 미소를 유지하며 작은 손하트를 끝까지 내민다.'
s['next_motion']='H가 옆판 가까이 손을 안으로 거둠 → W가 보이는 옆판을 한 번 접음 → W가 카트를 밀며 B3 오른쪽 퇴장 → H가 이동 중 손하트. H를 결박하거나 놀라게 하지 않음.'
c4=concepts['C04']
s=next(s for s in c4['shots'] if s['id']=='K07')
s['framing']='마술사와 모자를 카메라 쪽 전경으로 분리한 미디엄 와이드. 중후경의 관객 3명에서 A의 손잡이로 이어지는 시선 경로가 M의 몸통과 겹치지 않는다. M은 관객에게 관심을 끌려 하고 관객은 그를 지나 손을 본다.'
s['first_frame']='M은 관객 앞이지만 카메라 쪽으로 비껴 놓은 높이35cm 모자 위에 앉기 직전. 모자는 아직 눌리지 않았다. M은 관객을 향해 얼굴을 돌린다. 관객들은 M을 지나 중후경 A의 손과 나무 손잡이를 보며 약간 몸을 기울인다. 손잡이까지 열린 시선 경로와 모자 주름이 한 화면에 보인다.'
s['continuity_in']='K06에서 M이 든 모자를 관객 앞, 카메라 쪽으로 가져다 놓은 짧은 이동만 생략했다. 모자 크기·재질 동일. 이동 목적은 관객의 관심 회수이며 조수의 시연을 배우려는 행동이 아니다.'
c5=concepts['C05']
s=c5['shots'][-1]
for key in ['screen','framing','first_frame']:
    s[key]=s[key].replace('오른쪽58%', '오른쪽47%').replace('오른쪽 58%', '오른쪽 47%')
s['first_frame']+=' 실제 제목 조판은 화면 가로53% 지점부터 시작해 B의 몸·안내장과 겹치지 않는다.' if '가로53%' not in s['first_frame'] else ''
data['version']='pd-final-2.3-image-review-alignment'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Document alignment applied; selected image paths will be finalized after revised PNG review.')
