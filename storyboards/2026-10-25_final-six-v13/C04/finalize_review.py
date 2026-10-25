"""Run only after actual final-frame visual inspection. Records the limited scope."""
from render_c04 import *
p=OUT/'C04_Q-AI_Fair_final_v13.mp4'
tv=json.loads((OUT/'technical_validation.json').read_text(encoding='utf8'))
assert sha(p)==tv['sha256']
with av.open(str(p)) as c:
 tv.update(codecs={s.type:s.codec_context.name for s in c.streams},pixel_format=c.streams.video[0].codec_context.format.name)
tv['final_audio_analysis']=loudness(p);dump(OUT/'technical_validation.json',tv)
review={
 'concept':'C04 목마는 식사 중입니다','file':p.name,'sha256':tv['sha256'],
 'verdict':'SELF_VISUAL_SAMPLE_AND_TECHNICAL_PASS; independent review and actual continuous playback/listening remain',
 'actual_review_scope':{'full_decode':True,'source_frames_viewed':'K02/K04/K05/note at actual source keys, original action contact sheets for K01/K07/windows/bowls/spoon','rendered_frames_viewed':'Whole timeline 0.5s contact sheets plus every edit boundary -1/0/+1 frame, full-resolution note/tablet/document/causal-chain frames','dense_crops_viewed':'Note 3–4.625s at 0.125s cadence; declaration turn 8.75–9.417s at 1/12s; overlapping papers 20–23.75s at 0.25s','actual_continuous_playback':False,'actual_audio_listening':False,'venue_test':False},
 'checks':[
 {'id':'SELF-C04-01','status':'PASS_IN_VIEWED_SAMPLES','detail':'Same request enters crescent envelope; empty hand withdrawal preserved; inserted text goes behind envelope top, not onto its front.'},
 {'id':'SELF-C04-02','status':'PASS_IN_VIEWED_SAMPLES','detail':'Declaration and request contain same labels as AI comparison. AI flags a check, not a fabricated headcount or guaranteed result.'},
 {'id':'SELF-C04-03','status':'PASS_IN_VIEWED_SAMPLES','detail':'Original tablet finger and sleeve retained in front of text; large left/right labels readable in alternating uncovered periods.'},
 {'id':'SELF-C04-04','status':'PASS_IN_VIEWED_SAMPLES','detail':'Actual steam before window opening. Three hinged shutters open with exactly three people. Bowls extend and return before next wider view.'},
 {'id':'SELF-C04-05','status':'PASS_IN_VIEWED_SAMPLES','detail':'Commander reveals one spoon; caption follows visible spoon, source duplicate/late variants not used.'},
 {'id':'SELF-C04-06','status':'PASS_TECHNICAL','detail':'44.5 seconds, 1068 frames, 24fps, 720p H264/yuv420p, AAC. Full decode and PTS checks pass; no original hashes changed.'},
 {'id':'SELF-C04-07','status':'PASS_TECHNICAL_NOT_LISTENED','detail':'All original voices muted, own local music only, no invented impact SFX; finite audio samples and no full-scale clipping. Actual naturalness/listening remains unverified.'}],
 'fixed_during_self_review':[
 'K07 initial 0–2s plan would remove opening and steam cause; expanded to0–5 with PD confirmation.',
 'Bowls2–3.5 ended with arms far outside; extended to4.25 to retain return before wider shot.',
 'Cream paper erroneously included in skin mask: corrected thresholds separately for warm note and brighter document.',
 'Note ink could leak below envelope lip: corrected physical occlusion line and downward paper keys.',
 'Declaration turn used too-wide plane near1.75: tightened source keys through1.833 until reverse face.',
 'Occluded cream paper was squeezed to visible width: retained full paper plane and masked by foreground white page instead.'
 ],
 'remaining':['Independent reviewers have not yet returned on this final hash.','Actual continuous playback and music listening were not performed by this compositor; do not equate full decoding with listening.','Hidden corners of the overlapping request paper are inferred from visible edge motion; dense final crops show correct foreground occlusion, not a calibrated physical 3D solve.'],
 'deliverables':['C04_Q-AI_Fair_final_v13.mp4','edit_manifest.json','C04_captions.srt','composite_tracking.json','audio_recipe.json','technical_validation.json','COMPOSITING_NOTES.md','review_contact_01.jpg through review_contact_06.jpg','detail_note.jpg','detail_handoff.jpg','detail_papers.jpg']}
dump(OUT/'self_review.json',review)
m=json.loads((OUT/'edit_manifest.json').read_text(encoding='utf8'));m['status']='SELF_VISUAL_SAMPLE_TECHNICAL_PASS_PENDING_INDEPENDENT_AND_LISTENING';m['final_sha256']=tv['sha256'];dump(OUT/'edit_manifest.json',m)
print(json.dumps({'file':str(p),'duration':tv['duration_seconds'],'bytes':tv['bytes'],'sha256':tv['sha256'],'audio':tv['final_audio_analysis']},ensure_ascii=False))
