from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
import json
R=Path(__file__).resolve().parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ['href','src','data-src']:
   if a.get(k):self.refs.append(a[k])
def main():
 p=Parser();p.feed((R/'index.html').read_text(encoding='utf-8'));bad=[];local=0
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme:continue
  if u.path:
   local+=1
   if not (R/unquote(u.path)).is_file():bad.append(ref)
  elif u.fragment and u.fragment not in p.ids:bad.append(ref)
 assert not bad,bad
 report={'status':'passed','references':len(p.refs),'local_file_references':local,'anchors':len(p.ids),'browser_rendered':False,'scope':'HTML source links and assets checked; no local-file browser automation workaround'}
 (R/'link_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(report)
if __name__=='__main__':main()
