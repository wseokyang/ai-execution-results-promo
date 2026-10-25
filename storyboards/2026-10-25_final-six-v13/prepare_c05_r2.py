from pathlib import Path
import re
V=Path(__file__).resolve().parent
P=V/'C05_r2';P.mkdir(exist_ok=True)
s=(V/'C05/render_c05.py').read_text(encoding='utf-8')
s=s.replace("('N05_hand_transfer',V,'C05_N05_hand_transfer_take01',1.5,5,None),\n ('N06_pivot',V,'C05_N06_pivot_take01',1,5.5,None),\n ('N07_both_palms',V,'C05_N07_both_palms_take01',.5,5.25,None)","('N08_turn_initiation',V,'C05_N08_longneck_take01',.5,2.75,None)")
s=s.replace("(37,39.3,'조금만 더 잡아주세요.')","(26.5,28.8,'조금만 더 잡아주세요.')").replace("(39.7,43.1,'잠시 후, AI 실행 사례 공개')","(29.2,32.6,'잠시 후, AI 실행 사례 공개')").replace("(49.6,51.6,'들리세요?')","(39.1,41.1,'들리세요?')")
s=s.replace('(34.7,1.15,','(24.2,1.15,').replace('(44.5,2,','(34,2,').replace('(52.25,.42,','(41.75,.42,')
s=s.replace('34.5','24').replace('59.5','49').replace('54.5','44').replace('expected=1428','expected=1176')
s=s.replace('one hand under roof → outward pivot → both palms raised under roof → worker jack insert','turn initiation with existing roof contact → worker jack cutaway and temporal ellipsis → original long-neck front support')
s=re.sub(r"limitations=\[.*?\],status=", "limitations=['N08 only0.5–2.75s initiation used. Full outward turn and continuous hand transfer NOT captured. Worker cutaway bridges a temporal ellipsis into the original front support.','Rejected N05/N06/N07 short-neck body variants excluded entirely. N08 later dissolve and unsupported posture excluded.','Jack shot establishes transport only, not a verified stop/lift action.','All source speech removed; actual listening not verified.'],status=",s)
(P/'render_c05.py').write_text(s,encoding='utf-8')
(P/'.gitignore').write_text('review_frames/\nC05_picture.mp4\n*.wav\n__pycache__/\n',encoding='utf-8')
print(P/'render_c05.py')
