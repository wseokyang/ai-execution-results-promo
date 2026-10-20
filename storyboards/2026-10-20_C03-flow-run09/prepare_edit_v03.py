"""Create a separate editorial version; never modify prior edits or original media."""
from pathlib import Path
import shutil
P=Path(__file__).resolve().parent
old=P.parent/'2026-10-20_C03-edit-v02'
out=P.parent/'2026-10-20_C03-edit-v03'
out.mkdir(exist_ok=True)
s=(old/'render_edit.py').read_text(encoding='utf-8')
s=s.replace("R8 = '2026-10-20_C03-flow-run08'","R8 = '2026-10-20_C03-flow-run08'\nR9 = '2026-10-20_C03-flow-run09'")
s=s.replace("('K05', R3, 'C03_K05_take03.mp4', 1, 6.5),",
"""('K05_listen', R9, 'C03_K05_question_take05.mp4', 0, 1),
    ('K05', R3, 'C03_K05_take03.mp4', 1.25, 4.75),""")
s=s.replace('assert DURATION == 45.75','assert DURATION == 44.75')
s=s.replace('def shifted(t): return t+.5 if t>=5.5 else t',
"""def shifted(t):
    return t-.5 if t>=25.5 else (t+.5 if t>=5.5 else t)""")
s=s.replace("(20.30, 22.10, '이건 왜 보냈어요?')","(18.15, 19.95, '이건 왜 보냈어요?')")
s=s.replace("(22.25, 25.10, '안 됐던 것도 빠짐없이 달라면서요.')","(20.15, 23.00, '안 됐던 것도 빠짐없이 달라면서요.')")
s=s.replace('if t >= 40.75:','if t >= 39.75:')
s=s.replace('frame_count==1098','frame_count==1074').replace('assert n==1098','assert n==1074')
s=s.replace("2.4,4.2,20.65,.75,'R question, rear view'","2.4,4.2,18.65,.75,'R offscreen question J-cut over prior cuff picture'")
s=s.replace("0,2.7,22.75,.60","0,2.7,20.65,.60")
s=s.replace("0,5.75,26,1.15","0,5.75,25,1.15")
s=s.replace("add_audio(f'{R1}/C03_K05_take01.mp4'",
"""add_audio(f'{R3}/C03_K05_take03.mp4',0,1,20.5,.18,'ambient bridge under new silent listening picture')
add_audio(f'{R1}/C03_K05_take01.mp4'""")
s=s.replace('v02','v03')
s=s.replace('C03_review_edit_v03_46s.mp4','C03_review_edit_v03_45s.mp4')
s=s.replace('new_flow_requests=4,new_credits_used=30','new_flow_requests=2,new_credits_used=20')
s=s.replace('27.25–29.25s','26.25–28.25s').replace('40.75–45.75s','39.75–44.75s')
s=s.replace("'K05 question audio over clean rear-view file pickup; no voice speed alteration.'",
"""'K05 old question moved before the picture cut; new silent first1s is listening only, then existing clean pickup. No lipsync claim or voice speed alteration.',
                'K05 total picture trimmed by1s; all following segments and ending move1s earlier.'""")
s=s.replace("'K05 new synchronous shot held after two audio failures/refunds; existing clean picture and question audio retained.'",
"""'Run09 first partial-prompt output not used; full question output silent. Synchronous question improvement not achieved.'""")
s=s.replace("times=[shifted(t) for t in times]+[5.5,5.958,6,27.208,27.25,27.75,28.25,28.75,29.208,29.25]",
"""times=[shifted(t) for t in times]+[5.5,5.958,6,18.65,19,19.5,20.458,20.5,20.75,21,21.458,21.5,21.75,22.5,23.35,24.5,24.958,25,26.208,26.25,26.75,27.25,27.75,28.208,28.25]""")
(out/'render_edit.py').write_text(s,encoding='utf-8')
for name in ['transcribe_review.py','.gitignore']:
    if (old/name).exists():
        (out/name).write_text((old/name).read_text(encoding='utf-8').replace('v02','v03').replace('v03_46s','v03_45s'),encoding='utf-8')
print(out)
