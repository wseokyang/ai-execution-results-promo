from pathlib import Path
import json
out=Path(__file__).resolve().parent
q=json.loads((out/'technical_qa.json').read_text(encoding='utf8'))
q['visual_review']='PASS_SELECTED_INTERVALS_WITH_DOCUMENTED_EDITORIAL_OMISSIONS'
(out/'technical_qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
m=json.loads((out/'edit_manifest.json').read_text(encoding='utf8'))
m['status']='RENDERED_TECHNICAL_AND_SAMPLED_VISUAL_PASS_WITH_DOCUMENTED_OMISSIONS'
m['technical_qa']=q;m['visual_review_record']='final_visual_review.json'
(out/'edit_manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('review complete',q['sha256'])
