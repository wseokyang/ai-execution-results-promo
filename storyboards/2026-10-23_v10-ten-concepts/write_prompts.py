from pathlib import Path
import json,csv
R=Path(__file__).resolve().parent
d=json.loads((R/'storyboards.json').read_text(encoding='utf-8'))
cs={c['id']:c for c in d['concepts']}
overrides=json.loads((R/'motion_overrides.json').read_text(encoding='utf-8'))
out=R/'flow_prompts';out.mkdir(exist_ok=True)
rows=[]
for u in d['generation_units']:
    c=cs[u['concept_id']];s=next(s for s in c['shots'] if s['id']==u['linked_shot'])
    prompt=('Future production draft; do not submit before the user selects this concept.\n'
      'Use the designated PNG as the starting frame, preserving the same character identities, costumes, scale, left-right staging and props. '
      'One continuous shot matching the camera instruction below. Widescreen 16:9. The intended source clip is 8 seconds; the editor will trim the selected motion to the storyboard timing. '
      'No spoken dialogue, voice-over or lip-sync performance. No subtitles, captions, titles, logos, watermarks or legible interface/document writing. '
      'All exact typography and narrative captions will be composited in post. Silent facial and body acting must convey the action. '
      'Do not reveal the next shot\'s payoff early or add new characters.\n\n'
      f'Concept: {c["id"]} {c["title"]}\nUnit: {u["id"]}\n'
      f'Start state: {u["first_frame"]}\nPhysical action: {overrides.get(u["id"],u["action"])}\nCamera: {u["framing"]}\n'
      f'Incoming continuity: {s.get("continuity_in","")}\nOutgoing continuity: {s.get("continuity_out","")}\n'
      f'Acting/style: {c.get("visual_style","")}\n'
      'Caption-safe coordinates only, do NOT render any lettering: '+str([q['box'] for q in s.get('caption_cues',[])])+'\n'
      'Continuity notes describe the editor\'s story connection, not extra on-screen text or extra actions. Preserve clean plates for all typography.\n')
    (out/(u['id']+'.txt')).write_text(prompt,encoding='utf-8')
    rows.append({'concept_id':c['id'],'unit_id':u['id'],'start_image':u['image_file'],'prompt_file':'flow_prompts/'+u['id']+'.txt','editorial_cut':u['linked_shot'],'editorial_cut_seconds':s['duration'],'duration_note':'K02A and K02B share this editorial duration; split after motion selection' if u['id'].startswith('C05_K02') else 'source clip trim target; verify after generation','status':'NOT_SUBMITTED','policy':'reuse existing C03 footage first' if c['id']=='C03' else 'await user concept selection'})
with (R/'production_units.tsv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
print('Prepared',len(rows),'future prompts; no Flow actions')
