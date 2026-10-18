from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
R=Path(__file__).resolve().parent
class Scan(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set();self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ['href','src','data-src']:
   if a.get(k):self.refs.append(a[k])
  if tag=='img' and a.get('src'):self.images.append(a['src'])
p=Scan();p.feed((R/'index.html').read_text(encoding='utf-8'))
checked=[]
for ref in p.refs:
 u=urlsplit(ref)
 if u.scheme or u.netloc:continue
 if not u.path:
  assert not u.fragment or u.fragment in p.ids,ref
 else:assert (R/unquote(u.path)).exists(),ref
 checked.append(ref)
d=json.loads((R/'validation.json').read_text(encoding='utf-8-sig'))
d['html_link_checks']={'status':'passed','local_references':len(checked),'image_references':len(p.images),'concept_sections':all(x in p.ids for x in ['C01','C02','C03','C04','C05']),'browser_render':'not performed; no policy workaround'}
(R/'validation.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(d['html_link_checks']))
