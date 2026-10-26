"""V16 full-frame, QREW-derived lower-center subtitle compositor.

Film graphics stay attached to their objects. This is only for editorial captions.
"""
from pathlib import Path
import sys,json,hashlib,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image,ImageDraw,ImageFont,ImageFilter
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
W,H,FPS=1280,720,24
FONT_PATH=OUT/'fonts/Pretendard-SemiBold.ttf'
SPEC={
 'name':'QREW latest full-frame lower-center, adapted for lowest safe placement',
 'resolution':[W,H], 'full_frame_preserved':True, 'black_matte':False,
 'font':'Pretendard SemiBold', 'font_size_px':38, 'center_x':640,
 'one_line_baseline_y':684,'two_line_baselines_y':[641,684],
 'stroke_width_px':3,'stroke_color':'#000000','text_color':'#FAFAFA',
 'shadow_offset_px':[0,2],'shadow_blur_px':8,'maximum_text_width_px':1100,
 'individual_background_box':False,'maximum_lines':2,
 'ending_card_policy':'Keep existing full-frame event end cards; do not restyle them as dialogue.',
 'source':'QREW latest Journey/Expert/Interrogation filmCaption, 57px at1080p; explicit user asks lower placement.'
}
_font=None
_art={}
def font():
 global _font
 if _font is None:_font=ImageFont.truetype(str(FONT_PATH),SPEC['font_size_px'])
 return _font
def _wrap_line(text):
 d=ImageDraw.Draw(Image.new('L',(1,1))); result=[]; remain=text.strip()
 while remain:
  if d.textlength(remain,font=font())<=SPEC['maximum_text_width_px']:
   result.append(remain);break
  end=1
  while end<len(remain) and d.textlength(remain[:end+1],font=font())<=SPEC['maximum_text_width_px']:end+=1
  space=remain.rfind(' ',0,end+1)
  if space>max(3,end//2):end=space
  result.append(remain[:end].strip());remain=remain[end:].strip()
 return result
def caption_art(text):
 if text in _art:return _art[text]
 lines=[x for line in text.split('\n') for x in _wrap_line(line)]
 if len(lines)>2:raise ValueError('Caption exceeds two lines; split into timed cues: '+text)
 ys=[SPEC['one_line_baseline_y']] if len(lines)==1 else SPEC['two_line_baselines_y']
 shadow=Image.new('RGBA',(W,H));d=ImageDraw.Draw(shadow)
 for line,y in zip(lines,ys):d.text((640,y+SPEC['shadow_offset_px'][1]),line,font=font(),anchor='ms',fill=(0,0,0,190),stroke_width=4,stroke_fill=(0,0,0,150))
 art=shadow.filter(ImageFilter.GaussianBlur(SPEC['shadow_blur_px']));d=ImageDraw.Draw(art)
 for line,y in zip(lines,ys):d.text((640,y),line,font=font(),anchor='ms',fill=(250,250,250,255),stroke_width=3,stroke_fill=(0,0,0,245))
 _art[text]=art;return art
def compose_story(im,cues,t):
 out=im.convert('RGBA')
 if out.size!=(W,H):raise ValueError('Expected unmodified1280x720story raster')
 active=[c for c in cues if c['start']-1e-8<=t<c['end']-1e-8 and c.get('kind','subtitle') not in ['endcard','ending','brand']]
 if len(active)>1:
  texts=list(dict.fromkeys(c['text'] for c in active))
  text='\n'.join(texts)
 elif active:text=active[0]['text']
 else:return out.convert('RGB')
 out.alpha_composite(caption_art(text));return out.convert('RGB')
def write_caption_metadata(folder,cues,film):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
 clean=[]
 for c in cues:
  x=dict(c)
  if x.get('kind') not in ['endcard','ending','brand']:
   x.update({'pos':'bottom_center','x':640,'y':684,'font_px':38,'style':'qrew_full_frame_lower_center'})
   caption_art(x['text'])
  clean.append(x)
 (folder/'caption_manifest.json').write_text(json.dumps(clean,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 def ts(t):
  m=round(t*1000);return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
 (folder/f'{film}_captions_v16.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["text"]}' for i,c in enumerate(clean))+'\n',encoding='utf-8-sig')
 return clean
if __name__=='__main__':
 (OUT/'caption_style.json').write_text(json.dumps(SPEC,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(SPEC,ensure_ascii=False))
