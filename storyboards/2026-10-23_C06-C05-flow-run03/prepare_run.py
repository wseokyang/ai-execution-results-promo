from pathlib import Path
import json, hashlib, shutil

run = Path(__file__).resolve().parent
repo = run.parents[1]
cache = Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v11-C06-C05-2026-10-23/run03')
for d in [run/'inputs',run/'submitted_prompts',run/'evidence',cache/'inputs',cache/'prompts']:
    d.mkdir(parents=True, exist_ok=True)
common = ' One continuous eight-second shot from this exact starting frame. Keep all identities, costumes, scale, architecture and props unchanged. Locked camera. No extra characters, new objects, dissolves, cuts, dialogue, voiceover, lip-sync or text. All captions will be added later. 16:9, 720p. '
jobs = [
('C05_K07',2,'C05/S07_v3.png','current_u2','Earpiece installation without crossing the muzzle',
 'The technician moves the existing single black earcup only the last few centimetres directly onto the circular red ear immediately behind it on the RIGHT side of the image. Keep the earcup on that exact ear, well behind the yellow eye. The earcup never crosses the face, eye, mouth or nose. Seat it gently, then withdraw the gloved hand downward by second three, leaving the earcup attached and its existing wire hanging. The puppet blinks once and holds still. Its long S-shaped neck, closed mouth and both hands supporting the roof remain fixed. Do not add a strap across the muzzle or rotate the head. Hold the completed placement for four seconds.',
 'Prior middle section looked like a muzzle cover, leaving only 2.25 seconds of clean ear placement. Secure a clean reveal and reaction.'),
('C05_K08',2,'@run01/frames/C05_K08_take01/06_1.500s.png','current_u2','Immediate regrip after the thumb response',
 'The hand at IMAGE LEFT is already giving a thumbs-up. Immediately put that SAME hand back against the underside of the porch by second two, opening it into a supporting palm. The other hand never loses contact. The roof settles only a few centimetres as the palm returns, then stays completely stable. For the remaining six seconds both palms stay firmly supporting the same roof. Keep the head, long S-folded neck and deeply bent knees unchanged. Only a tiny embarrassed eye movement is allowed. Never stand up, lift the building, bounce, give another thumbs-up, nod repeatedly, lower either arm again or move the ladder or jack. Keep the attached single earcup and existing people. The long ending must be a steady living hold for the later title.',
 'Prior ending stands up and raises the roof after 6s. Need complete gag followed by stable moving end-title plate.'),
('C05_K06',2,'C05/S06_v2.png','current_u2','Technician manually locks ladder caster',
 'The already fully extended wheeled ladder moves only a short distance as the same technician pushes its base into position. He stops it and visibly presses ONE caster brake with his shoe, then removes his foot. The ladder is now still. Keep the existing ladder length, rails, wheels and supports rigid and unchanged throughout; no new stabilizers unfold, no ladder extension, no automatic wheel or jack transformation. The technician does not climb in this shot. The puppet holds the roof with both palms and keeps the same folded neck and knees. No earcup or new equipment is revealed yet. Hold the parked ladder at the end.',
 'Prior take showed automatic support deployment and changing jack after 3.75s. Need manual parking action and clean transition to ear installation.'),
('C05_K02B_reverse',1,'C05/S03.png','current_u2','One outward step from the correct porch geometry',
 'Keep the same long S-folded neck, deeply bent knees and both raised hands, which do not touch the roof. The puppet makes only ONE small crouched sideways step toward IMAGE LEFT, moving slightly OUT from beneath the existing porch. One foot plants, then the other follows; the body translates as a rigid articulated costume, not a shape transformation. Do not straighten the neck, crawl, turn, grow or shrink. The roof, remaining columns and detached pillar stay completely fixed. There is only the single porch in the image. No camera movement or new foreground roof. Finish after this small outward step and hold. This is intentionally an OUTWARD step for a separately labelled reverse-playback editing experiment, not a full multi-action entry.',
 'Three full entry attempts failed. New mechanism starts at correct destination and asks one small outward step; reverse derivative only if footwork and environment remain credible.'),
('C05_K01',2,'C05/S01.png','current_u2','Sustained threat before reaching toward the pillar',
 'The giant red practical puppet holds its threatening open-mouth pose and slowly spreads its two arms outward for four seconds, claiming the entrance. Its feet stay planted, body remains upright and long neck stays straight at the same height. Then its eyes turn toward the front-left pillar and one hand reaches only halfway toward that pillar, stopping without touching it. Never grab the roof, lift the porch, remove the pillar, step beneath the roof, or begin the next action. Keep the distant people and intact building in their original positions. Preserve the dramatic low-angle sky and puppet fabric texture. No voice or vocalization is needed.',
 'Prior hook becomes roof grabbing after 3.5s while the planned caption runs to3.7s. Need readable four-second claim without early payoff.'),
('C06_K02',2,'C06/S02.png','current_u3','Table scare immediately becomes paper straightening',
 'The white-robed ghost gives the desk ONE brief sideways jolt during the first second using the two hands already at the desk edge. Immediately, the mustard-shirt employee calmly takes the existing uneven stack of papers and taps its bottom edge once on the desktop to square the stack, finishing by second three. The ghost stops and stares at the neatly aligned stack, realizing the scare helped the work. Keep the papers as one stack, with no flying, disappearing, duplicating or merging pages. No nodding sequence or extra action. Preserve the exact two faces, glasses, clothes, desk and room. Hold the awkward result for the final three seconds.',
 'Prior long pause weakens scare-to-help cause. Place the jolt and paper alignment next to each other.'),
('C06_K04_check',1,None,'current_u3','Employee makes one deliberate document check',
 'The mustard-shirt employee compares the same row of the paper with the adjacent blank monitor panel using one brief eye movement, then makes ONE short check with the pen already held above that paper. Lift the pen and withdraw the hand enough to reveal the marked area, then remain still for three seconds. Do not write a sentence, add pages, change the monitor, duplicate fingers or move the paper. Keep the rest of the scene motion minimal. The exact AI proposal, original-record labels and checkmark will be composited in post; do not generate readable writing. This is a practical confirmation step before leaving, not automatic completion of all work.',
 'Existing wide shot does not clearly convey source verification before leaving. Stable hand/paper/monitor insert needed for precise post-composite.'),
('C06_K09_reaction',1,None,'current_u3','A polite ghost smile slowly freezes',
 'The long-haired white-robed ghost starts with the tiny polite smile already in the image. As the unseen visitors settle in, that smile gradually freezes: the mouth corners flatten, the eyes briefly look toward them, and the face becomes quietly dismayed. Finish this subtle change by second three and hold the uncomfortable expression for four seconds. No new smile, laugh, speech, nod, broad grimace, head turn, camera movement or character appearance. Keep the same long dark hair, pale angular face, white robe and blue night-office lighting. The joke is that the ghost has lost its quiet evening again.',
 'Existing ending smile broadens and reads as welcoming. Need a clear, restrained dismayed reaction after seating.')]
queue=[]
for unit,take,rel,account,title,prompt,reason in jobs:
    dest = run/'inputs'/f'{unit}.png'
    if rel:
        src=(repo/'storyboards/2026-10-23_C06-C05-flow-run01'/rel.removeprefix('@run01/')) if rel.startswith('@run01/') else (repo/'storyboards/2026-10-23_v11-production-lock/images'/rel)
        shutil.copy2(src,dest); shutil.copy2(dest,cache/'inputs'/dest.name)
        sha=hashlib.sha256(dest.read_bytes()).hexdigest()
    else:
        src=run/'new_keyframes'/f'{unit}.png'; sha=None
    txt=prompt+common+f' Unit {unit}, take {take:02}.'
    pf=f'submitted_prompts/{unit}_planned.txt'
    (run/pf).write_text(txt+'\n',encoding='utf-8')
    (cache/'prompts'/f'{unit}.txt').write_text(txt,encoding='utf-8')
    queue.append({'unit_id':unit,'take':take,'account_alias':account,'title':title,'source_image':str(dest.relative_to(repo)),'source_origin':str(src.relative_to(repo)),'sha256':sha,'planned_prompt':pf,'regeneration_reason':reason,'status':'READY' if rel else 'WAITING_FOR_KEYFRAME'})
log={'run_id':run.name,'source_version':'V11 and actual run01 inserts','user_authorization':'User explicitly requested all remaining credits across five logged-in accounts be spent on needed detail shots and unsatisfactory scenes. Overrides prior20-only budget; no purchase or subscription changes.','balance_snapshot':{'current_u0':0,'current_u1':0,'current_u2':50,'current_u3':30,'current_u4':0},'budget':80,'queue':queue,'requests':[],'status':'PREPARING','flow_requests':0,'downloaded_originals':0}
lp=run/'generation_log.json'
if lp.exists():
    old=json.loads(lp.read_text(encoding='utf-8-sig'))
    assert not old['requests'], 'Do not replace a live run'
lp.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared',len(queue),'requests; budget80; six existing images, two pending new keyframes.')
