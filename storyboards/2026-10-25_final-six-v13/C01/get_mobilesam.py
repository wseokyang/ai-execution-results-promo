from pathlib import Path
import urllib.request,zipfile
p=Path('C:/Users/wseok/.cache/codex-media-tools/mobilesam');p.mkdir(exist_ok=True)
z=p/'source.zip'
if not z.exists():urllib.request.urlretrieve('https://github.com/ChaoningZhang/MobileSAM/archive/refs/heads/master.zip',z)
with zipfile.ZipFile(z) as f:f.extractall(p)
print([str(x) for x in p.glob('MobileSAM-*/weights/*')])
