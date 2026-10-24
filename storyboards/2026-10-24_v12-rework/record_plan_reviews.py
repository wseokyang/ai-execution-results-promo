from pathlib import Path
import json,datetime
p=Path('storyboards/2026-10-24_C05-first-flow-run01/generation_log.json');d=json.loads(p.read_text(encoding='utf-8-sig'));d['status']='N03_SUBMITTED'
e=next(e for e in d['entries'] if e['unit_id']=='C05_N03');e['status']='SUBMITTED_RESULT_PENDING';e['submitted_at_recorded']=datetime.datetime.now(datetime.timezone.utc).isoformat()
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=Path('storyboards/2026-10-24_v12-rework/reviews/independent_and_cross_summary.json')
reviews={
'A':{'A-N01':'필수: 네안준비운반시간압축','A-N02':'필수: C08초후같은자료판타겟','A-N03':'필수: C10실제지지부불안정원인','A-N04':'개선: AI사례다양화','A-N05':'개선: 나도사례꺼내기반복'},
'B':{'B-N01':'필수: C07손5cm간격10cm하강비접촉충돌','B-N02':'필수: C10손접근원인','B-N03':'필수: C08준비압축','B-N04':'필수: C09낙찰운반압축','B-N05':'개선: AI사례반복','B-N06':'개선: C07첫10초단축','B-N07':'필수명세: C08천탭선등록'},
'C':{'C-N01':'필수: C07첫반전왕복압축','C-N02':'필수: C09운반착석압축','C-N03':'필수: C10조명문제시선손복구','C-N04':'개선: AI반복','C-N05':'개선: C08준비목적충돌','C-N06':'개선: C10삼각대설치압축'}
}
o={'stage':'independent then cross review, before revision','scope':'draft JSON, 40 start-frame descriptions; no actual new images or videos yet','independent':reviews,'cross':{'A':'B/C全同意; C08 21s includes thaw, preparation alone15s; C10 low-clamp hold must solve low support wobble, not upper hinge sag. A-N02 retained.','B':'A/C全同意; C10 initial10s genre setup not necessarily failure but6-8s recommended; preserve actual pickup/return/contact; C08 shared conditions vs C10 adds alternative sample.','C':'A/B同意; newly adopts A-N02 B-N01 B-N07; preparation gag reactions must not be omitted.'},'pd_decision':'Keep all4 concepts. Apply all causal/physical/timing fixes and selected diversity improvements; preserve 10 distinct starts per concept and 5s endcard. Director revising exact draft file, not yet resolved.'}
p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
