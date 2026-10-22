"""Final record after A/B/C independent, cross and revised-proof responses."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
rv=read('image_review.json')
reasons={
 'I-A-001':'All agree base positions vary. A treated selection-phase severity as advisory; B required reconciling fixed-base production instructions. PD chose movable stands, offscreen repositioning between shots, fixed within each shot.',
 'I-A-002':'All agree short-U/full-U continuous wide edit could expose a jump. Accept upper-body K06 handoff and K07 total length reference; actual motion continuity still needs verification.',
 'I-B-001':'All agree P1 moves from rear waiting area toward camera; same MC-left/DV-right axis retained.',
 'I-B-002':'All agree fixed-floor description conflicts with selected images; resolved together with I-A-001 without regenerating PNGs.',
 'I-B-003':'All agree broad top captions obstruct important faces. Actual derivative caption proofs show shot-specific safe positions.',
 'I-C-001':'All agree C10 K07-K09 are not reverse-angle shots. Canonical direction and all delivery fields corrected.',
 'I-C-002':'All agree rightward scissor travel before cutting must propagate to all planning/production fields; verified synchronized.',
 'I-PD-001':'All agree final title must not cover reaction. C10 lower title after action; C04 K04 information plate inside blank tablet. Perspective tracking still future work.',
 'I-A-003':'Cross-review addition: stale manifest camera_notes synchronized. C05 K02A/B intentionally remain separate unit-specific starts/actions/cameras, sharing 3+4=7 editorial seconds.'}
rv['cross_review']=[{'issue_id':i,'peer_reasoning':v,'pd_resolution':'resolved at storyboard/image preparation phase','unverified':'actual generated motion, edited timing and venue readability'}for i,v in reasons.items()]
for who in 'ABC':
 rv['final_reconfirmation'][who]={'agent':'/root/v10_review_'+who.lower(),'received':True,'actual_caption_proofs_opened':[f'caption_proofs/C{i:02}_captions.jpg'for i in range(1,11)],'peer_reports_read':True,'remaining_required_issues':0,'selection_stage_complete':True,'C05_K02AB_separate_units_reconfirmed':True,'browser_render_not_claimed_by_reviewer':True}
rv['reviews']['A']['additional_cross_originals_seen']=['images/C05/S02A.png','images/C05/S02B_v3.png']
rv['reviews']['A']['total_original_detail_count_after_cross']=37
rv['status']='Completed: three independent all-88 image reviews, mutual cross review, revised text and caption-proof reconfirmation by all three'
put('image_review.json',rv)
d=read('storyboards.json');m=read('scene_manifest.json');us={u['id']:u for u in d['generation_units']}
for e in m['images']:
 assert e['next_motion']==us[e['id']]['action'] and e['camera_notes']==us[e['id']]['framing'],e['id']
 assert hashlib.sha256((R/e['image_path']).read_bytes()).hexdigest()==e['sha256'].lower()
 e['review_status']='Three independent selected-image reviews + cross/reconfirmation complete; suitable for concept selection. Motion not generated.'
m['status']='88 selected starts reviewed; user concept selection pending; no Flow submissions'
d['status']='Ten complete concept storyboards and88 actual selected start images ready for user selection; no Flow generation'
for c in d['concepts']:
 c['status']='text and selected-image independent/cross review complete; awaiting user concept selection'
 for s in c['shots']:
  if 'mute_readability'in s:s['mute_readability']['verification']='텍스트·실제 첫 이미지·정지 자막 증빙 검토 완료. 실제 무음 영상 연속 재생과 현장 가독성은 생성·편집 후 확인.'
for u in d['generation_units']:
 u['status']='selected actual PNG ready; NOT_SUBMITTED_TO_FLOW';u['review_status']='A/B/C independent + cross + revised-proof reconfirmation complete'
put('storyboards.json',d);put('scene_manifest.json',m)
summary={'run_id':d['run_id'],'event_name':'Q-AI Fair','ready_for_user_selection':True,'status':'storyboard and start-image delivery complete; user choice and actual video production are later stages','counts':{'concepts':10,'editorial_cuts':sum(len(c['shots'])for c in d['concepts']),'selected_start_images':88,'new_generated_selected_PNGs':44,'V9_byte_reused_selected_PNGs':44,'flow_requests':0,'credits_spent':0,'video_or_audio_generated':0},'concepts':[{'id':c['id'],'title':c['title'],'seconds':c['duration_seconds'],'start_images':sum(u['concept_id']==c['id']for u in d['generation_units'])}for c in d['concepts']],'text_review':'text_review.json','existing_image_review':'existing_image_review.json','final_image_review':'image_review.json','scope_of_actual_review':'Each A/B/C inspected all88 selected images in full-size contact sheets, with individual original-detail checks, then all10 caption-proof sheets. Root additionally rendered/tested local HTML. No actual generated motion or audience reaction was tested.','remaining_required_storyboard_image_issues':[],'future_verification':['Selected Flow model/cost/real balance before each request. No accounts accessed in this run.','Reuse existing C03 footage before any new requests.','Actual rope rotation/jump, service-arm transfer and cape movement; first PNGs do not guarantee generation success.','Actual video caption timing, moving-object clearance, exact screen/page compositing and perspective tracking.','Venue reading distance and audience comedy response.','Exact event date, venue, participation method and performance figures remain unconfirmed.'],'preserved':'Legacy C01 final movie, C03v03 and source videos, V8/V9 and original reference assets unchanged;99 baseline source hashes checked in validation.json','automation':'Remains PAUSED. No resume or schedule change.','recommendations':d['recommendations']}
put('review_summary.json',summary)
put('ui_qa.json',{'surface':'actual local HTML via cua_repl in-app browser','observed_article_count':88,'observed_concept_sections':10,'caption_box_outside_stage':0,'completed_image_load_failures_observed':0,'tested_selection':['C06','C10'],'observed_selection_image_total':18,'selection_reset_confirmed':True,'actual_render_samples':['C03 first shots','C04 K04 tablet information plate','C10 K09 lower title'],'all_caption_proofs':'caption_proofs/C01_captions.jpg through C10_captions.jpg, opened by PD andA/B/C','limits':'PIL proof font metrics may slightly differ from browser; moving-video clearance not checked. Test selection does not submit requests.'})
print('Final independent/cross/reconfirmation records complete; all88 selected PNG hashes unchanged')
