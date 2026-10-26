"""C08 assembly. --preview creates compositor samples. --draft is visibly tracked as nonfinal.
Final rendering requires approved replacement K08/K10 in edit_plan.json.
"""
from pathlib import Path
import sys,json,subprocess,math
OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(OUT.parent))
from media_common import *
sys.path.insert(0,str(SB/'2026-10-25_final-six-v13/C02/.deps'))
import cv2
SOURCE=SB/'2026-10-26_C08-C09-flow-v15'
plan=json.loads((OUT/'edit_plan.json').read_text(encoding='utf8'));EDL=plan['timeline'];by={s['cut']:s for s in EDL};duration=EDL[-1]['end']+5
Q={'K03':[(365,216),(693,200),(719,404),(393,440)],'K04':[(315,103),(638,58),(669,259),(358,325)]}
REF={}
for cut in ['K03','K04']:
 with av.open(str(SOURCE/f'C08_{cut}_take01.mp4')) as c:REF[cut]=next(c.decode(video=0)).to_ndarray(format='rgb24')

def star(d,x,y,r=15):
 pts=[]
 for i in range(10):
  ang=-math.pi/2+i*math.pi/5;rr=r if i%2==0 else r*.42;pts.append((x+rr*math.cos(ang),y+rr*math.sin(ang)))
 d.polygon(pts,fill=(24,45,55))

def ui_art(progress):
 im=Image.new('RGBA',(600,400),(232,241,241,255));d=ImageDraw.Draw(im)
 d.rectangle((0,0,600,76),fill=(29,94,105));d.text((300,13),'공유 AI 양식',font=font(43),anchor='mt',fill='white')
 d.text((140,95),'내 자료',font=font(32),anchor='mt',fill=(30,64,71));d.text((460,95),'적용 결과',font=font(32),anchor='mt',fill=(30,64,71))
 d.rounded_rectangle((41,144,239,350),12,fill=(250,252,250),outline=(129,167,171),width=3)
 d.rounded_rectangle((361,144,559,350),12,fill=(250,252,250),outline=(129,167,171),width=3)
 d.line((264,247,327,247),fill=(45,115,122),width=7);d.polygon([(340,247),(321,234),(321,260)],fill=(45,115,122))
 for x in [67,387] if progress>=.99 else [67]:
  d.polygon([(x,163),(x+31,163),(x,194)],fill=(34,149,159))
  for row in range(4):
   d.line((x+41,192+row*34,x+135,192+row*34),fill=(132,160,163),width=7)
  star(d,x+19,226,12)
 if 0<progress<.99:
  x=83+progress*320;y=179;d.rounded_rectangle((x,y,x+112,y+136),8,fill=(248,253,252),outline=(29,135,145),width=4);d.polygon([(x+9,y+9),(x+34,y+9),(x+9,y+34)],fill=(34,149,159));star(d,x+42,y+70,13)
 return im

def composite_ui(frame,cut,st):
 progress=1 if cut=='K04' else float(np.clip((st-1)/1.8,0,1))
 art=np.array(ui_art(progress));quad=np.float32(Q[cut]);src=np.float32([[0,0],[599,0],[599,399],[0,399]])
 transform=cv2.getPerspectiveTransform(src,quad);layer=cv2.warpPerspective(art,transform,(W,H),flags=cv2.INTER_CUBIC)
 alpha=layer[:,:,3].astype(float)/255;rgb=frame.astype(float);ref=REF[cut].astype(float)
 # Preserve foreground fingers and the lifted paper using source-reference differences
 # constrained to the fixed screen plane. Every critical occlusion is separately inspected.
 skin=(rgb[:,:,0]>rgb[:,:,1]+14)&(rgb[:,:,1]>rgb[:,:,2]+5)
 filled=np.uint8(skin&(alpha>.05))*255
 if cut=='K04' and 2.45<=st<=4.05:
  track=[(2.45,[(306,325),(480,390),(695,570),(429,600)]),(2.5,[(306,314),(480,383),(695,562),(429,589)]),(2.75,[(226,210),(480,234),(640,480),(330,538)]),(3.,[(114,100),(355,92),(542,354),(288,434)]),(3.25,[(0,200),(258,122),(462,306),(236,418)]),(3.5,[(0,226),(174,212),(428,344),(228,460)]),(3.75,[(0,370),(160,288),(382,394),(192,490)]),(4.05,[(0,400),(180,332),(390,398),(180,515)])]
  tt=[v[0] for v in track]
  poly=np.array([[np.interp(st,tt,[v[1][i][j] for v in track]) for j in range(2)] for i in range(4)],np.int32)
  cv2.fillConvexPoly(filled,poly,255)
 filled=cv2.dilate(filled,np.ones((3,3),np.uint8))
 alpha*=1-cv2.GaussianBlur(filled,(3,3),.6).astype(float)/255
 return np.uint8(np.clip(rgb*(1-alpha[:,:,None])+layer[:,:,:3]*alpha[:,:,None],0,255))

CAPS=[]
def cap(cut,a,b,text,pos='bottom',x=None,y=None):
 seg=by[cut];CAPS.append(dict(start=seg['start']+a,end=seg['start']+b,text=text,pos=pos,x=x,y=y,font_px=42))
cap('K01',.2,2.55,'누가 좀 도와줘요.','top',690,43)
cap('K03',.1,3.4,'공유 사례 → 내 업무에 적용','top',64,43)
cap('K04',.1,2.,'원본과 대조해 직접 확인.')
cap('K04',2.5,5.1,'확인한 문서는 완료 트레이로.')
cap('K06',.1,3.4,'끝났는데요.','top')
cap('K07',.1,3.7,'여기는\n아직이네요.','top',520,43)
cap('K08',.2,1.7,'잠시 후','top',64,43)
cap('K09',1.5,4.5,'이 한 장만, 다시요.')
CAPART=[(c['start'],c['end'],caption(c['text'],c['pos'],c['x'],c['y'])) for c in CAPS]
end=ending('한 사람의 방법을, 함께 쓰는 실력으로.')
end.save(OUT/'ending_v15.png')

def build_score():
 notes=[]
 def add(t,d,p,v,ch):notes.append(dict(start=round(t,4),duration=d,pitch=p,velocity=v,channel=ch))
 # Grand but sparse brass/strings act, then dry bassoon/pizzicato repair miniature.
 programs={0:48,1:61,2:43,3:70,4:45,5:0}
 landing=by['K05']['start']+4.05
 for t in np.arange(.15,2.65,.8):add(float(t),.35,45,22,4)
 for k,t in enumerate(np.arange(by['K02']['start'],landing,.54)):
  add(float(t),.4,[38,38,45,41,38,43,45,48][k%8],38,2)
  if k%2==0:
   for p in [50,57,62]:add(float(t),.8,p,31,0)
  if k%4==0:
   for p in [62,65,69]:add(float(t),.7,p,39,1)
 # After the landing, the gap is the joke, not a shouted response.
 for k,t in enumerate(np.arange(by['K07']['start']+.15,by['K09']['start']+1.3,.8)):
  add(float(t),.28,[50,57,53,57][k%4],29,4)
  if k%3==0:add(float(t)+.12,.4,[62,65,60][k%3],26,3)
 for t in [by['K10']['start']+.2,by['K10']['start']+2.,by['K10']['end']+.2,by['K10']['end']+2.6]:
  for p in [50,57,62]:add(t,1.6,p,29,5)
 wav=OUT/'C08_original_score_v15.wav';rests=[(landing,by['K07']['start']), (by['K09']['start']+1.4,by['K10']['start'])]
 # No invented crack/impact. The picture carries those events. Only this visible button gets a quiet click.
 effects=[dict(at=1.15,duration=.07,frequency=1100,peak=.006,visual_cause='K01 single finger button depression')]
 gain,measurement=synthesize(notes,programs,duration,wav,rests,effects)
 dump(OUT/'audio_recipe.json',dict(programs=programs,notes=notes,rests_seconds=rests,effects=effects,soundfont=str(SF),soundfont_sha256=sha(SF),source_audio='ALL GENERATED AUDIO EXCLUDED',music='Original local brass/strings rescue cue followed by small bassoon/pizzicato repair cue',static_gain_db=gain,loudness_before_gain=measurement,actual_listening_verified=False))
 return wav,gain

def preview():
 folder=OUT/'composite_previews';folder.mkdir(exist_ok=True)
 for cut in ['K03','K04']:
  with av.open(str(SOURCE/f'C08_{cut}_take01.mp4')) as c:
   for i,f in enumerate(c.decode(video=0)):
    if i not in [12,36,60,72,84,96,120]:continue
    st=float(f.time);im=Image.fromarray(composite_ui(f.to_ndarray(format='rgb24'),cut,st));im.save(folder/f'{cut}_{st:04.2f}s.png')
 print('PREVIEW_READY',flush=True)

def main(draft=False):
 if not draft:assert all(s['approved_for_final'] for s in EDL),'K08/K10 replacement approval required; cannot finalize known-defective takes'
 assert duration<=60
 hashes={s['file']:sha(SOURCE/s['file']) for s in EDL}
 pic=OUT/'C08_picture_v15.mp4';n=0
 with (OUT/'render_stderr.txt').open('wb') as log:
  enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-threads','2','-pix_fmt','yuv420p',str(pic)],stdin=subprocess.PIPE,stderr=log)
  try:
   for seg in EDL:
    ct=0
    with av.open(str(SOURCE/seg['file'])) as c:
     for f in c.decode(video=0):
      st=float(f.time)
      if st<seg['source_in']-1e-6:continue
      if st>=seg['source_out']-1e-6:break
      t=seg['start']+st-seg['source_in'];array=f.to_ndarray(format='rgb24')
      if seg['cut'] in Q:array=composite_ui(array,seg['cut'],st)
      im=Image.fromarray(array).convert('RGBA')
      for a,b,art in CAPART:
       if a<=t<b:im.alpha_composite(art)
      enc.stdin.write(im.convert('RGB').tobytes());n+=1;ct+=1
    assert ct==round((seg['end']-seg['start'])*24)
    print('RENDERED',seg['cut'],ct,flush=True)
   for i in range(120):enc.stdin.write(end.tobytes());n+=1
  finally:enc.stdin.close();enc.wait()
 assert enc.returncode==0 and n==round(duration*24)
 wav,gain=build_score();name='C08_internal_assembly_v15.mp4' if draft else 'C08_Q-AI_Fair_screening_v15.mp4';final=OUT/name;mux(pic,wav,final,duration,gain)
 caps=CAPS+[dict(start=EDL[-1]['end'],end=duration,text='Q-AI Fair\n한 사람의 방법을, 함께 쓰는 실력으로.\n품질팀 AI 성과 교류회')]
 def ts(t):
  m=round(t*1000);return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
 (OUT/'C08_captions_v15.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["text"]}' for i,c in enumerate(caps))+'\n',encoding='utf-8-sig')
 q=technical_qa(final,OUT,duration,[s['start'] for s in EDL]+[EDL[-1]['end']])
 assert hashes=={s['file']:sha(SOURCE/s['file']) for s in EDL}
 dump(OUT/'edit_manifest.json',dict(concept_id='C08',file=name,duration_seconds=duration,timeline=EDL,captions=caps,source_sha256=hashes,source_audio='ALL EXCLUDED',original_files_unchanged=True,action_stills_inserted=False,end_card_seconds=5,ui='One shared-template UI; current paper is applied to own work, no automatic verification check',screen_plane_quads=Q,ui_foreground='Keyed foreground-paper polygon + skin mask on fixed screen plane; sample review required',status='INTERNAL_DRAFT_K08_K10_NOT_ACCEPTED' if draft else 'TECHNICAL_PASS_VISUAL_REVIEW_PENDING',pending_required_fixes=plan['pending_required_fixes'] if draft else [],actual_listening_verified=False,actual_continuous_playback_verified=False,technical_qa=q))
 print('DONE',name,duration,q['sha256'],flush=True)

if __name__=='__main__':
 if '--preview' in sys.argv:preview()
 else:main('--draft' in sys.argv)
