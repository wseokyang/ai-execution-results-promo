from pathlib import Path
P=Path(__file__).resolve().parent
SB=P.parent
out=P/'C03';out.mkdir(exist_ok=True)
src=(SB/'2026-10-24_C03-caption-v04/render_caption_v04.py').read_text(encoding='utf-8')
src=src.replace('SB = OUT.parent','SB = OUT.parent.parent').replace("'C03_K04_insert_take05.mp4', 2.25, 5.75","'C03_K04_insert_take05.mp4', 3.75, 5.5").replace('assert DURATION == 44.75','assert DURATION == 43.0')
old="caption_pngs=[]"
new="""# V13: tighten the cuff hesitation by1.75s; retain all actual actions.
for cue in caption_cues:
    if cue['start']>=20.5:
        cue['start']-=1.75;cue['end']-=1.75
    if cue['kind']=='evidence':cue['end']=12.4
caption_pngs=[]"""
src=src.replace(old,new).replace('C03_Q-AI_Fair_edit_v04.mp4','C03_Q-AI_Fair_final_v13.mp4').replace('1074','1032').replace('1073','1031').replace('if t>=38.75','if t>=37.0')
src=src.replace("'Q-AI Fair ending 38.75–44.75; last cue extended by0.2s to avoid tail flash'","'V13 cuff hold trimmed1.75s; all later captions retimed. Q-AI Fair ending37.0–43.0; evidence caption ends12.4 before insert'")
(out/'render_c03.py').write_text(src,encoding='utf-8')
print(out/'render_c03.py')

