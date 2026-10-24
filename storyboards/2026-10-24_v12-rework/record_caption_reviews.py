from pathlib import Path
import json
shared={'status':'PASS_WITH_OPTIONAL_NOTE','scope':'Actual extracted contact sheets and full PNGs; no continuous playback, audio listening or venue test','independent':{'A':['A-E01 C06 motivation resolved','A-E02 C03 cuff question/sender resolved','A-E03 environment/result/process resolved','A-E04 event resolved','A-E05 optional caption overhang 12.5-12.8s'],'B':['B-E01 C06 motivation resolved','B-E02 sender/question resolved','B-E03 environment/process resolved','B-E04 event resolved','B-E05 no blocking occlusion'],'C':['C-E01 C06 motivation resolved','C-E02 environment/question/sender resolved','C-E03 silent narrative/event resolved','C-E04 optional caption overhang12.5-12.8s']},'cross':{'A':'Agrees B/C; wording no occlusion amended to no obstruction of essential action/readability.','B':'Agrees A/C; optional overhang may remain.','C':'Agrees A/B; optional overhang may remain. Essential readability intact.'},'pd':'Current caption repair scope accepted. Optional0.3s overhang deferred to future edit. No new Flow clips required for C06/C03. Prior glove-state and file-pickup ellipses not newly solved.'}
for folder in ['2026-10-24_C06-caption-v05','2026-10-24_C03-caption-v04']:
 (Path('storyboards')/folder/'review_summary.json').write_text(json.dumps(shared,ensure_ascii=False,indent=2),encoding='utf-8')
r=Path('storyboards/2026-10-24_C05-first-flow-run01')
p=r/'review_summary.json';d=json.loads(p.read_text(encoding='utf-8-sig'))
d['N02_take02']={'status':'CONDITIONAL_INTERMEDIATE','pd_and_C':'Arms rise and grip front fascia/edge, not underside. Neck still trapped. Cannot cut directly to oldK04.'}
d['N03_take01']={'status':'CONDITIONAL_CANDIDATE','pd_C_director':'Actual neck lowered clear while frontedge held. Creative grip accepted, not underside support or physically verified loadtransfer. Need outward body turn before oldK04.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
