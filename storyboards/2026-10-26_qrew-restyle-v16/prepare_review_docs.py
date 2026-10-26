from pathlib import Path
import json,copy,re
from style_api import write_caption_metadata
V=Path(__file__).resolve().parent;ROOT=V.parent.parent
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for cid,a,b,desc in [('C02',14.9,20.75,'The detective regains confidence; investigation groove resumes before the cuff reversal.'),('C03',19.5,23.25,'A thin industrial pulse continues under the reply, leading into the delivered records.')]:
 p=V/'audio'/cid/'score_manifest.json';x=json.loads(p.read_text(encoding='utf8'))
 if not any(c['start']==a for c in x['cues']):x['cues'].append({'start':a,'end':b,'description':desc})
 x['cues'].sort(key=lambda c:c['start']);save(p,x)
 p=V/'audio'/cid/'score_manifest.json'
 for left,right in zip(x['cues'],x['cues'][1:]):assert left['end']==right['start']
archive=ROOT/'archive/v15-root-before-v16';archive.mkdir(exist_ok=True)
for name in ['README.md','00_완성_영상.md','콘티_바로보기.md','07_셰프님_그것도_주세요.md','08_구조는_끝났습니다.md','09_나_없이도_괜찮겠어요.md']:
 p=ROOT/name
 if p.exists() and not (archive/name).exists():
  t=p.read_text(encoding='utf8')
  t=re.sub(r'\]\((?!https?://|#)([^)]+)\)',lambda m:'](../../'+m.group(1)+')',t)
  (archive/name).write_text(t,encoding='utf8')
old=json.loads((ROOT/'storyboards/2026-10-26_C01-C07-C10-rewrite-v15/storyboards.json').read_text(encoding='utf8'))
c=copy.deepcopy(next(x for x in old['concepts'] if x['id']=='C07'))
folder=V/'C07';folder.mkdir(exist_ok=True)
captions=[];props=[]
for s in c['shots']:
 if s['id']=='C07_K07':s['transition']=s['transition'].replace('25.5초','24.2초')
 for cue in s['caption_cues']:
  if s['id']=='C07_K03':
   cue['kind']='prop_label';cue['placement']='기록통에 붙는 표찰. 일반 자막과 분리하여 물체에 추적 합성.';props.append(dict(cue))
  elif s['id']=='C07_K10':cue['kind']='endcard';cue['placement']='기존 별도 전체 화면 엔딩 카드';captions.append(dict(cue))
  else:
   cue.update({'kind':'subtitle','placement':'하단 중앙, 1280×720 기준 x640 / 기준선684, 38px 흰색·검정 외곽선3px; 박스 없음'})
   captions.append(dict(cue))
 s['video_generation_required']=False
 s['status']='기존 첫 프레임 보존. 이번 작업은 자막·음악 계획 검토, Flow 영상 생성 없음.'
c['caption_style']='V16 공통 하단 중앙. 소품 표찰과 별도 엔딩 제외. caption_manifest.json 우선.'
c['music_direction']='V16 90 BPM 3박자 새 기악곡 데모. 0–11초 격식 있는 왈츠(4.8–6.3초 완전 정적),11–15초 현악 발견,15–22.3초 확대 재현,22.3–27.6초 음악 없음,27.6–32.6초 마무리. 실제 효과음은 영상 확보 후 접점에 맞춰 추가. 현재 음악 데모에는 의자 드르륵/돔/종이 접촉음을 넣지 않음.'
c['status']='V16 자막·음악 검토본; 실제 영상 미생성'
c['source_storyboard']='storyboards/2026-10-26_C01-C07-C10-rewrite-v15/storyboards.json'
c['audio_demo']='storyboards/2026-10-26_qrew-restyle-v16/audio/C07/C07_music_preview_v16.mp3'
for s in c['shots']:
 s['music_sfx_silence']='V16 music_direction 및 audio/C07/score_manifest.json을 적용. 실제 접촉 효과음은 영상 생성 후 관측된 접점에만 배치.'
save(folder/'storyboard_v16.json',c);save(folder/'prop_labels.json',props)
write_caption_metadata(folder,captions,'C07')
note='''# C07 · V16 자막·음악 적용표

실제 영상은 아직 없습니다. 기존 첫 프레임과 이야기는 보존하고, 앞으로 제작할 자막·음악 지시를 정리했습니다.

| 구간 | 내용 | 적용 |
|---|---|---|
| 0.4–3.8초 | 오늘의 완성작입니다. | 하단 중앙 |
| 4.5–7.8초 | 그래서… 어떻게요? | 하단 중앙 |
| 8.2–10.8초 | 수정 초안 | 기록통 표찰, 물체에 추적 합성 |
| 11.3–14.8초 | 셰프님. 이것도 주세요. | 하단 중앙 |
| 15.2–16.7초 | 잠시 후 | 하단 중앙 |
| 27.6–32.6초 | 결과만큼 궁금한, 그 과정. / Q-AI Fair / 품질팀 AI 성과 교류회 | 별도 전체 화면 엔딩 |

하단 중앙 규격: 720p 기준 Pretendard SemiBold 38px, 흰색, 검정 외곽선 3px, x640/기준선684. 박스 없음. 실제 영상에서 물체 가림을 다시 확인합니다.

음악: 90 BPM 격식 있는 왈츠 → 수정 기록 발견의 현악 → 과하게 진지한 재서빙 → 의자 경쟁에서 완전 정적 → 정중한 마무리. 데모의 정적은 4.8–6.3초와 22.3–27.6초입니다. 돔·종이·의자 효과음은 실제 동작을 확보한 후 접점에만 넣습니다. 현재 데모에는 해당 Foley가 없습니다.

K07→K08 하드 컷은 **24.2초**입니다. 예전 전환 메모의 25.5초는 오래된 표기였습니다. 전체 32.6초는 유지합니다.

[음악 데모](../audio/C07/C07_music_preview_v16.mp3) · [최신 자막표](caption_manifest.json) · [전체 제작 지시](storyboard_v16.json)
'''
(folder/'README.md').write_text(note,encoding='utf8')
p=ROOT/'07_셰프님_그것도_주세요.md';t=p.read_text(encoding='utf8')
banner='**V16 최신 자막·음악:** [하단 중앙 적용표·음악 데모](storyboards/2026-10-26_qrew-restyle-v16/C07/README.md). 아래 이전 음향 지시보다 이 적용표가 우선합니다. 실제 영상은 미생성입니다.\n\n'
if 'V16 최신 자막·음악' not in t:t=t.replace('\n\n','\n\n'+banner,1)
t=t.replace('같은 행동의 JB 컷으로 25.5초 하드 컷.','같은 행동의 JB 컷으로 24.2초 하드 컷.')
p.write_text(t,encoding='utf8')
save(V/'music_implementation_notes.json',{'authoritative_audio':'audio/Cxx/score_manifest.json + create_scores.py','planning_document':'music_cue_plan.json is the direction-stage plan; actual implementation differences below.','changes':[{'concept_id':'C07','planned':'6.3–11 sparse piano','implemented':'Formal waltz continues through11, with full gate4.8–6.3.','reason':'Maintain the serious tasting ceremony before the records receive grander treatment; no unverified Foley.'},{'concept_id':'C04','planned':'Progressive transition into dining waltz','implemented':'Full dining waltz begins31 after complete silence28–31.','reason':'A decisive genre reversal matches the bowl reveal.'}],'metadata_corrections':['C02 cue14.9–20.75 and C03cue19.5–23.25 added; audio unchanged.'],'actual_listening_performed':False})
print('Review documentation corrections ready')
