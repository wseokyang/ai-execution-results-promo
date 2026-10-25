"""Package final C01 captions, reproducible masks and factual local QA record."""
from pathlib import Path
import sys,json,zipfile,hashlib
from render_c01 import OUT,dump,sha
man=json.loads((OUT/'edit_manifest.json').read_text(encoding='utf-8'))
assert man['ending_graphic_seconds']==5, 'Final tail has not been rendered'
qa=json.loads((OUT/'technical_validation.json').read_text(encoding='utf-8'))
assert qa['sha256']==sha(OUT/'C01_Q-AI_Fair_final_v13.mp4')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
sub=man['captions']+[dict(start=man['duration_seconds']-5,end=man['duration_seconds'],text='\n'.join(man['ending_text']))]
(OUT/'C01_captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(q['start'])} --> {stamp(q['end'])}\n{q['text']}" for i,q in enumerate(sub))+'\n',encoding='utf-8')
maskfiles=sorted((OUT/'foreground_masks').rglob('*.png'))
with zipfile.ZipFile(OUT/'foreground_masks.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in maskfiles:z.write(p,p.relative_to(OUT).as_posix())
dump(OUT/'mask_manifest.json',dict(method='Local MobileSAM vit_t segmentation of original actual foreground only. Connected components restricted to manually inspected actor seed positions; thin feather.',action_synthesis=False,files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha(p)) for p in maskfiles],archive='foreground_masks.zip',archive_sha256=sha(OUT/'foreground_masks.zip')))
print('packaged',len(maskfiles),'masks, duration',man['duration_seconds'])
