"""Copy instrument primitives only from read-only user QREW source.
No existing melody, arrangement, completed recording, or note list is reused.
"""
from pathlib import Path
import ast,hashlib,json
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
Q=(ROOT/'../../../motion/qrew_old').resolve()
sets=[('v8-recut/create_audio.py',['axis','hz','fade','noise','kick','snare','hat','rim','conga','funk_bass','clav','electric_key','brass_stab']),
      ('v5-fullvideo/create_audio.py',['strings','low_blast','kettle','pluck','chime']),
      ('v6/create_audio.py',['submarine','suspended_tone','depth_pulse'])]
code=['"""Mathematical instrument primitives adapted from user-owned QREW DSP; no source score events."""',
      'import numpy as np','SR=48000','RNG=np.random.default_rng(261016)']
records=[]
for rel,names in sets:
 p=Q/rel;src=p.read_text(encoding='utf-8');tree=ast.parse(src)
 found={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
 for name in names:code.append(ast.unparse(found[name]))
 records.append({'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'functions':names,
   'scope':'instrument DSP definitions only; no existing musical events or audio'})
(OUT/'dsp_primitives.py').write_text('\n\n'.join(code)+'\n',encoding='utf-8')
(OUT/'dsp_provenance.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared 21 instrument/helper functions; no existing music copied.')
