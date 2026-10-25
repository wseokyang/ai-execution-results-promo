from pathlib import Path
import re
V=Path(__file__).resolve().parent;P=V/'C05_r3';P.mkdir(exist_ok=True)
s=(V/'C05_r2/render_c05.py').read_text(encoding='utf-8')
s=s.replace(" ('N08_turn_initiation',V,'C05_N08_longneck_take01',.5,2.75,None),\n",'')
s=s.replace("(26.5,28.8,'조금만 더 잡아주세요.')","(24.25,26.55,'조금만 더 잡아주세요.')").replace("(29.2,32.6,'잠시 후, AI 실행 사례 공개')","(26.95,30.35,'잠시 후, AI 실행 사례 공개')").replace("(39.1,41.1,'들리세요?')","(36.85,38.85,'들리세요?')")
s=s.replace('(24.2,1.15,','(21.95,1.15,').replace('(34,2,','(31.75,2,').replace('(41.75,.42,','(39.5,.42,')
s=s.replace('round(24*SR)','round(21.75*SR)').replace('(24-8.5)','(21.75-8.5)').replace('[8.5,24]','[8.5,21.75]').replace('26.25–','21.75–').replace('24–49','21.75–46.75').replace('8.5–24','8.5–21.75')
s=s.replace('cursor==49','cursor==46.75').replace('expected=1176','expected=1122').replace('start=44,end=49','start=41.75,end=46.75').replace('if t>=44:','if t>=41.75:')
s=s.replace('turn initiation with existing roof contact → worker jack cutaway and temporal ellipsis → original long-neck front support','worker jack cutaway covering a clear temporal ellipsis → original long-neck front support')
s=re.sub(r"limitations=\[.*?\],status=", "limitations=['Full outward turn and continuous hand transfer NOT captured. N03 neck withdrawal is followed by an actual worker jack cutaway, then the original long-neck front support. This is a temporal ellipsis, not a continuous action.','N05–N08 variants excluded entirely for character/anatomy/support/dissolve defects.','Jack shot establishes transport only, not a verified stop/lift action.','All source speech removed; actual listening not verified.'],status=",s)
(P/'render_c05.py').write_text(s,encoding='utf-8');(P/'.gitignore').write_text('review_frames/\nC05_picture.mp4\n*.wav\n__pycache__/\n',encoding='utf-8')
print(P/'render_c05.py')
