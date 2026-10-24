from pathlib import Path
import json

root = Path(__file__).parent
unit = 'C06_K02_impact'
prompt = ('The angry ghost has both existing hands raised above the desk. He brings BOTH palms down onto the EMPTY desktop ONCE, in one emphatic downward motion. The palms visibly contact the desk before a small desk vibration and a slight tremble of the nearby paper stack. The papers remain on the desk in the same general place. The ghost then keeps his hands on the desktop and stares at the employee with frustrated disbelief. The employee remains seated, calmly looking at the paperwork, with no startled reaction. The ghost never touches, lifts, flips or sorts any document. No second hit. Preserve all people, their hands, desk and objects. One continuous locked-camera 8-second 16:9 shot starting exactly from the supplied frame. No speech, voice-over, lip sync, generated text or music. Silent output acceptable. No cuts, dissolves, floating objects, morphs or extra limbs.')
queue = json.loads((root / 'queue.json').read_text(encoding='utf-8'))
if not any(x['unit'] == unit for x in queue):
    queue.append(dict(unit=unit, take=1, input=f'inputs/{unit}.png', reason='Clear cause: palms contact desk before small vibration; employee remains unimpressed', prompt=prompt, status='PREPARED_NOT_SUBMITTED'))
    (root / 'queue.json').write_bytes((json.dumps(queue, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
(root / 'submitted_prompts' / f'{unit}_take01.txt').write_bytes((prompt+'\n').encode('utf-8'))
print('Impact prompt prepared; no submission by this script')
