from pathlib import Path
import urllib.request, hashlib, json
root=Path(__file__).resolve().parent
cache=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3')
cache.mkdir(parents=True,exist_ok=True)
revision='684543d5e5efaef08d02be50dcda8d552478fa60'
base=f'https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/{revision}/'
items=[]
for name,remote in [('LICENSE.txt','documentation/LICENSE.txt'),('GeneralUser-GS.sf2','GeneralUser-GS.sf2')]:
    dest=cache/name
    if not dest.exists(): urllib.request.urlretrieve(base+remote,dest)
    items.append({'file':name,'source':base+remote,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size})
(root/'GeneralUser-GS-LICENSE.txt').write_bytes((cache/'LICENSE.txt').read_bytes())
record={'soundfont':'GeneralUser GS 2.0.3','author':'S. Christian Collins','repository':'https://github.com/mrbumpy409/GeneralUser-GS','revision':revision,'cache_path':str(cache),'files':items,'usage':'Original note sequence composed for C01; no existing song or demo MIDI used. SoundFont not redistributed in the project.','engine':'tinysoundfont 0.3.7 (MIT), installed from PyPI; offline rendering only, no audio-device playback.'}
(root/'score_sources.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(record,ensure_ascii=False),flush=True)
