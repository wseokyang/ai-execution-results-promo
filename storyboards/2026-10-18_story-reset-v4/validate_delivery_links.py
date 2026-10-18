"""Static document checks; not a rendered-browser or motion review."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
R=Path(__file__).resolve().parent
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set();self.buttons=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.add(d['id'])
        for k in ('src','href','data-src'):
            if d.get(k):self.links.append(d[k])
        if tag=='button' and 'data-src' in d:self.buttons+=1
p=Links();p.feed((R/'index.html').read_text(encoding='utf-8'))
local=[]
for url in p.links:
    u=urlsplit(url)
    if u.scheme or u.netloc:continue
    if u.path:
        path=R/unquote(u.path)
        assert path.is_file(),url
        local.append(url)
    elif u.fragment:assert u.fragment in p.ids,url
assert p.buttons==44,p.buttons
d=json.loads((R/'storyboards.json').read_text(encoding='utf-8'))
for c in d['concepts']:
    for sc in c['scenes']:
        for cut in sc['cut_ids']:
            s=next(x for x in c['shots'] if x['id']==cut)
            assert sc['image_file']==s['image_file'],(c['id'],cut)
            assert sc['first_frame']==s['first_frame'],(c['id'],cut)
            assert sc['next_motion']==s['next_motion'],(c['id'],cut)
v=json.loads((R/'validation.json').read_text(encoding='utf-8'))
v.update(html_local_links='passed',checked_local_links=len(local),lightbox_trigger_count=p.buttons,scene_shot_mapping='passed',source_png_byte_equality='passed_by_merge_images',browser_render_qa={'status':'not_performed','reason':'Browser Use security policy blocks local file protocol. No workaround attempted. Static file/link checks and actual image review performed.'})
(R/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'html_local_links':len(local),'image_buttons':p.buttons,'scene_mapping':'passed','browser_render':'not_performed'},ensure_ascii=False))
