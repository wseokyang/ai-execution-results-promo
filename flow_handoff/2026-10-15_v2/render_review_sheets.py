#!/usr/bin/env python3
"""Read-only browser contact sheets for image QA; never changes source PNGs."""
import html,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'handoff_manifest.json').read_text())
out=ROOT/'review_sheets';out.mkdir(exist_ok=True)
assets=data['assets'];pages=[]
for number,i in enumerate(range(0,len(assets),4),1):
    cards=[]
    for a in assets[i:i+4]:
        clips=[c for co in data['concepts'] for c in co['clips'] if c['asset_id']==a['id']]
        desc=clips[0]['start_state']
        cards.append(f'<div class="card"><b>{a["id"]}</b><span>{html.escape(", ".join(c["id"] for c in clips))}</span><img src="../{a["path"]}"><p>{html.escape(desc)}</p><small>{a["path"]}</small></div>')
    path=out/f'sheet_{number:02}.html'
    path.write_text('<meta charset="utf-8"><style>body{background:#0c1420;color:#eef5ff;font:17px/1.4 "Noto Sans CJK KR",sans-serif;margin:24px}.grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px}.card{min-width:0;background:#172334;padding:14px;border:1px solid #456;border-radius:10px}b{display:block;font-size:24px}span,small{overflow-wrap:anywhere;display:block;color:#9bc4e7}img{width:100%;aspect-ratio:16/9;object-fit:contain;display:block;margin-top:12px;background:black}p{height:64px;margin:10px 0;font-size:17px}</style><div class="grid">'+''.join(cards)+'</div>')
    png=path.with_suffix('.png')
    env=dict(os.environ,LD_LIBRARY_PATH='/home/wooseok/wsy/motion/qrew_old/tools/chromium-libs/usr/lib/x86_64-linux-gnu')
    cmd=['/home/wooseok/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1900,1440',f'--screenshot={png}',path.as_uri()]
    subprocess.run(cmd,env=env,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    pages.append(dict(page=number,png=str(png.relative_to(ROOT)),assets=[a['id'] for a in assets[i:i+4]]))
(out/'index.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
print(f'{len(pages)} review sheets, {len(assets)} images (check manifest for any pending source files).')
