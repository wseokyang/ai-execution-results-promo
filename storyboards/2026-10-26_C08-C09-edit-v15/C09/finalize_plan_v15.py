from pathlib import Path
import json
P=Path(__file__).resolve().parent/'edit_plan.json';d=json.loads(P.read_text(encoding='utf8'));by={s['cut']:s for s in d['timeline']}
by['K04'].update(source_in=.5,source_out=6.,approved_for_final=True,review='Take02 completes one-way boarding: both man and suitcase inside by 5.5 seconds. Keep through 6 seconds, no return to pavement.')
by['K07'].update(source_in=4.5,source_out=6.5,approved_for_final=True,review='Only already-held charger in right hand and offering gesture retained. Incorrect cross-body pocket retrieval at earlier times is excluded; PD approved editorial omission, not a repaired retrieval claim.')
by['K09'].update(source_in=3.5,source_out=6.5,approved_for_final=True,review='Use only rear-facing bus receding continuously into street depth and clearing frame. Initial open-door movement/axis instability excluded. Door closing and initial departure are editorially omitted, not claimed verified.')
t=0
for s in d['timeline']:s['start']=t;t+=s['source_out']-s['source_in'];s['end']=t
d['status']='ALL_SELECTED_INTERVALS_APPROVED_PENDING_FINAL_RENDER_BOUNDARIES';d['pending_required_fixes']=[]
d['known_editorial_compromises'] += [
 {'cut':'K07','issue':'Take02 still extracts charger cross-body from wrong side before retained interval.','treatment':'Retain source4.5-6.5, charger already held in right hand. Question begins1.25seconds before this cut. Pocket retrieval omitted with PD approval.'},
 {'cut':'K09','issue':'Take02 opens with unclosed door movement/axis ambiguity.','treatment':'Retain source3.5-6.5, bus rear already receding. Departure start/door closing omitted with PD approval.'}]
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('final selected duration',t+5)
