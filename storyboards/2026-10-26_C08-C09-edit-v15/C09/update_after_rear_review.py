from pathlib import Path
import json
P=Path(__file__).resolve().parent/'edit_plan.json'
d=json.loads(P.read_text(encoding='utf8'));by={s['cut']:s for s in d['timeline']}
by['K06'].update(source_in=.5,source_out=5.75,approved_for_final=True,review='0.5-second actual frames: suitcase reaches pavement by 3 seconds, both feet by 4 seconds. Phone begins entering left pocket around 5 seconds. Cut before unrelated later jacket gestures.')
by['K07'].update(file='C09_K07_take02.mp4',approved_for_final=False,review='Take01 rejected for wrong-side pocket/hand continuity. Replacement pending visual review.')
by['K08'].update(source_in=1.5,source_out=3.25,approved_for_final=True,crop=[330,215,810,485],review='Use only actual moving close-up handoff insert. Phone disappearance occurs before retained range and is excluded. Receiver secures charger and giver visibly releases. Right-hand receipt remains a documented editorial compromise; no claim of corrected original physics.')
by['K09'].update(file='C09_K09_take02.mp4',approved_for_final=False,review='Take01 rejected for reverse motion/open-door departure. Replacement must close doors before rolling forward.')
by['K10'].update(source_in=.75,source_out=5.5,approved_for_final=True,review='Woman walks behind man and exits left by about 4.5 seconds; man stays with suitcase, bus absent.')
t=0
for s in d['timeline']:s['start']=t;t+=s['source_out']-s['source_in'];s['end']=t
d['status']='WAITING_FOR_REPAIRED_K04_K07_K09'
d['pending_required_fixes']=['K04 take02 complete boarding review','K07 take02 correct pocket/hand retrieval review','K09 take02 closed-door forward departure review']
d['known_editorial_compromises']=[{'cut':'K08','issue':'Take01 phone disappears before retained interval; charger received by different hand from planned continuity.','treatment':'Actual moving hand insert 1.50-3.25 seconds, crop [330,215,810,485], then wide shot. This omits defective interval; it does not repair the original file. Final boundary review required.'}]
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('provisional duration',t+5)
