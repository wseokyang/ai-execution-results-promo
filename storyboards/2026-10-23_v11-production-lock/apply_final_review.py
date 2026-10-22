"""Build V11 from preserved V10 data. Does not generate or modify source media."""
from pathlib import Path
import copy,json
R=Path(__file__).resolve().parent
SRC=R.parent/'2026-10-23_v10-ten-concepts'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
d=read(SRC/'storyboards.json'); m=read(SRC/'scene_manifest.json'); ov=read(SRC/'motion_overrides.json')
cs={c['id']:c for c in d['concepts']}
def shot(cid,k):return next(s for s in cs[cid]['shots'] if s['id']==k)
def action(cid,k,text):
 s=shot(cid,k);s['screen']=s['next_motion']=text
def cue(cid,k,text,start=None,end=None):
 s=shot(cid,k)
 if s['caption_cues']:q=s['caption_cues'][0]
 else:
  q={'kind':'character','placement':'하단의 인물 발·줄 동작을 가리지 않는 여백. 글은 후편집.','box':{'left_pct':7,'width_pct':86,'bottom_pct':6}}
  s['caption_cues']=[q]
 q['text']=text
 if start is not None:q['start']=start
 if end is not None:q['end']=end

# Existing strong concepts keep their premises. Clarify one performer's intention.
action('C02','K02','TE가 트레이를 멈추자 DE가 몸을 크게 가로질러 제품 반출을 지나치게 엄숙하게 막는다. IN이 모니터를 가리키면 DE는 막은 몸을 그대로 둔 채 고개만 돌린다. 윙크·발화 없음.')

# C07: one person's invitation moves the whole explanation circle; trim setup waits.
newtimes={'K04':(14,17),'K05':(17,20),'K06':(20,24),'K07':(24,28),'K08':(28,33),'K09':(33,39)}
for k,(a,b) in newtimes.items():
 s=shot('C07',k);delta=a-s['start']
 for q in s['caption_cues']:q['start']=round(q['start']+delta,2);q['end']=round(q['end']+delta,2)
 s.update(start=a,end=b,duration=b-a)
cs['C07']['duration_seconds']=39
action('C07','K04','CW가 줄 고리를 EX 발 앞 빈 바닥에 던진다. 빈 오른손으로 EX 한 사람만 가리킨 뒤 자기 앞 빈자리를 짚는다. EX가 고개를 한 번 끄덕인다. 줄은 누구의 몸에도 걸리지 않는다. 준비 대기 없이 동작을 연결한다.')
cue('C07','K04','당신만 이쪽으로.',14.2,16.8)
shot('C07','K04')['caption_cues'][0].update(speaker='CW',placement='빈 중앙 하늘. EX 발 앞 줄 낙하지점과 좌우 인물 얼굴을 비운다.',box={'left_pct':37,'width_pct':36,'top_pct':6,'font_cqw':3.3})
action('C07','K05','EX가 한 손에 든 열린 수첩을 CW 쪽으로 돌린다. Q1은 보던 페이지를 놓치지 않으려고 몸을 따라 돌리며 바로 앞 느슨한 줄을 가볍게 잡는다. Q2도 시선을 수첩에 둔 채 다른 구간을 잡는다. EX는 페이지를 넘기거나 추가 손으로 가리키지 않는다.')
cue('C07','K05','잠깐, 그다음은요?',17.15,19.85)
shot('C07','K05')['caption_cues'][0]['speaker']='Q1'
action('C07','K06','CW가 줄을 자기 쪽으로 안내한다. EX가 먼저 자기 발로 걷고 Q1·Q2가 수첩을 보려고 함께 걷는다. CW는 세 사람이 함께 오는 것을 보고 한 걸음 물러나며 느슨한 줄을 거둔다. 도착한 질문자 둘이 다시 시야를 가린다. CW가 틈으로 고개를 내밀다 멈추는 마지막 0.6초를 남긴다. 긴 이동의 중간 대기는 편집에서 덜어낸다.')
shot('C07','K06')['transition']='이동 중간 대기를 덜고 마지막 접근·재차 가림을 연결. 줄이 사람을 끌지 않는다. 0.6초 막힌 표정 뒤 K07 수첩 준비.'
cs['C07']['mute_readability']='당신만이라는 초대 → 수첩을 놓치기 싫어 모두 동행 → 자신도 수강. K04~K06은3/3/4초로 압축, 마지막 재차 가림을 보존.'

# C08: the cape physically rises into a fixed light path. One graphic, one glare change.
action('C08','K03','ST가 버튼을 누르자 회전 세트가 약45도 돌아가기 시작한다. 객석의 시선이 세트로 빠지는 순간 OP가 고정 앞무대에서 한 걸음 옮겨 자기 정면을 다시 내밀지만, 시선은 돌아가는 세트를 따라간다. 뒤 책상 일부만 나타나고 전체는 다음 컷에 공개한다.')
action('C08','K04','ST가 첫 시도·수정 표시·적용본의 세 카드를 차례로 짚는다. 동일한 세 단계 도해가 작업 화면에 이미 있지만 좌상 조명의 반사가 가운데 수정 흔적 일부를 가린다. ST가 읽기 불편한 곳으로 시선을 한 번 옮긴다. CO와 AU의 시선은 OP에서 작업 화면으로 이동한다.')
action('C08','K05','OP가 아무도 자기를 보지 않는 것을 눈으로 확인하고 한 걸음 앞으로 나서 망토를 거대한 부채처럼 펼친다. 검정 안감이 드러나고 ST가 그 넓은 어두운 면을 발견한다. 망토는 관객의 화면 시야를 막지 않는다. 이 컷에는 반사가 아직 남아 있다.')
action('C08','K06','ST가 자유 망토 끝을 조명 쪽으로 들어 올리고 OP도 따라 팔을 높인다. 검정 안감이 고정 좌상 조명과 작업 화면 사이 빛길에 들어선다. 후편집에서 천 뒤로 향하는 광선과 같은 도해 위 반사를 동시에 줄인다. 도해를 새로 켜거나 바꾸지 않는다. 화면이 선명해진 상태를 마지막1초 유지하며 관객의 화면 시야는 가리지 않는다.')
action('C08','K07','CO가 작업 화면을 지휘봉으로 정중하게 가리킨다. OP가 그 끝을 따라 보다가 이미 높아진 팔을 조금 더 벌려 망토를 팽팽하게만 한다. 차광된 빛과 같은 도해를 유지하며 두 번째 차광 효과를 만들지 않는다.')
for k in ['K04','K05','K06','K07','K08']:
 shot('C08',k)['post_composite']='동일 post_assets/C08_process.svg를 같은 화면 면에 합성. K04~K05 반사 유지. K06 천이 빛길에 들어오는 순간 천 뒤 광선과 화면 반사를 함께 감소. K07~K08 같은 차광 상태. 전체 인물·배경을 암전하거나 새 도해로 교체 금지.'

# C09: source plan is eight seconds; keep readable ending without stretch/freeze.
rule='자료를 받을 범위에서 빈 손바닥을 펼쳐 유지한 뒤 약0.4초 후 해당 팔 하나가 출발한다. 같은 작은 표시등을 후편집으로 같은 순서에 점등. 말·눈길만으로 호출하지 않는다. 한 숏 내 받침대 고정.'
for k in ['K01','K03','K04','K05','K08']:
 shot('C09',k)['motion_acceptance']=rule
action('C09','K04','AL이 기록 앞을 가리려고 빈 오른손바닥을 활짝 편다. HU가 손 옆으로 고개를 조금 기울여 기록을 계속 본다. 마지막 약0.4초에 손바닥을 유지하고 서비스 표시등만 후편집으로 켠다. 두 보조팔은 이 컷 끝까지 접힌 채 정지한다. 팔의 출발은 다음 K05에서 한 번만 보여준다.')
shot('C09','K04')['motion_acceptance']='손바닥→끝0.4초 유지→표시등만. K04 두 팔 완전 정지. K05의 한 번 출발과 컷을 걸쳐 연결.'
action('C09','K05','앞 컷의 손바닥 호출을 이어 AR_L이 시작 즉시 한 번 출발해 실제 수정 폴더를 집고 AL의 펼친 손 앞에 정중하게 내민다. AL은 가리는 손을 유지하려다 폴더를 받을 수밖에 없고 결과판과 기록을 양손에 나눠 든다. AR_R은 접힌 채 정지. 다시 손을 펴거나 두 번째 출발·대기를 반복하지 않는다.')
shot('C09','K05')['motion_acceptance']='K04 끝 호출에 이어 시작 즉시 L 한 번 출발. 같은 폴더·같은 손, R 정지. 호출 재연 없음.'
shot('C09','K01')['screen']+=' 열린 손을 먼저0.4초 보여준 뒤 팔이 출발한다.'
shot('C09','K01')['next_motion']=shot('C09','K01')['screen']
action('C09','K08','AL이 투구를 잡으려 원통 위 서비스 범위에 빈 손을 펼친다. 약0.4초 뒤 AR_R 하나가 남은 얇은 자료 묶음을 집어 그 손 앞으로 내민다. AL이 손을 빼면 R은 바로 아래 열린 원통 안에 자료를 세우고 물러난다. AL이 멈춘 손 그대로 천천히 팔을 본다. L과 추가 자료는 움직이지 않는다.')
action('C09','K09','36–37초 AL이 자료가 든 투구를 HU 쪽으로 조금 밀고 턱을 든다. 37–39초 HU가 원통 속 낱장 한 장을 뽑아 펼친다. 39–44초 AL은 새로 가리키는 동작 없이 같은 낱장을 함께 바라본다. 책상 위 기존 수첩·수정 폴더는 그대로 남는다.')
s=shot('C09','K09');s.update(end=44,duration=8);s['caption_cues'][0].update(start=39.0,end=43.8)
cs['C09']['duration_seconds']=44

# C10: retain the visible consequence, omit tiny adhesive mechanics from source request.
action('C10','K04','장치가 같은 롤에서 긴 접합 띠를 공급해 두 끝을 잇는다. 공급이 필요 이상으로 계속되어 주 리본이 큰 U자로 바닥까지 늘어진다. MC는 바닥으로 내려가는 리본을 보면서도 의전 미소를 유지한다. 자투리 절단·낙하·가위 접착 과정을 이 숏에 모두 만들지 않는다.')
shot('C10','K04')['continuity_out']='과잉 공급이 계속된 짧은 시간을 컷 사이 생략. K05 첫 상태에는 별도 짧은 접착 자투리가 두 가위 날에 이미 붙어 있다. 주 리본과 가위는 연결되지 않음.'
shot('C10','K05')['continuity_in']='장치의 과잉 공급 중 짧은 시간 생략 뒤, 원본 PNG처럼 두 가위 날에 별도 자투리가 붙은 결과 상태. 긴 주 리본과는 분리되어 있다.'
action('C10','K05','DV가 정지 버튼을 눌러 롤과 장치를 완전히 멈춘다. MC가 한 손잡이를 조금 들자 붙어 있는 다른 가위도 함께 들린다. MC는 더 쓰지 않고 그대로 내려놓고 바닥의 긴 리본으로 시선을 옮긴다. 함께 들리는 한 번의 움직임만 보이며 추가 분리 시도는 없다.')
shot('C10','K05')['framing']+=' 붙은 두 가위가 함께 들리는 순간에는 새 생성 없이 같은 원본의 짧은 편집 확대를 검토한다. 화질이 무너지면 결과 상태·시선 연결을 쓰고 별도 낙하 동작을 재생성하지 않는다.'

framing={('C06','K09'):'책상·접이식 의자·세 얼굴을 읽는 고정 와이드. 의자가 펴지고 앉는 몸개그 뒤 하단 제목판. 얼굴·의자 동작을 가리지 않으며 정확한 위치는 caption_cues.box.',('C07','K09'):'조금 넓어진 미디엄 와이드. 네 얼굴과 함께 보는 수첩을 유지하고 하단 제목판. 정확한 위치는 caption_cues.box이며 하늘 상단 제목 지시를 쓰지 않는다.',('C08','K08'):'OP의 과잉 의전 표정과 선명해진 동일 작업 도해를 함께 담는 고정 미디엄 와이드. 엄지 반응 뒤 하단 제목판. 망토·화면·얼굴을 비우며 위치는 caption_cues.box.'}
for (cid,k),text in framing.items():shot(cid,k)['framing']=text

# Synchronize all mirrors, while historical image-generation prompts remain untouched.
units={u['id']:u for u in d['generation_units']};ims={e['id']:e for e in m['images']}
for c in d['concepts']:
 ss={s['id']:s for s in c['shots']}
 for s in c['shots']:
  s['subtitle']=' / '.join(q['text'] for q in s['caption_cues']) or '없음'
 for a in c.get('text_assets',[]):
  if 'cues' in a and a['cut'] in ss:a['cues']=copy.deepcopy(ss[a['cut']]['caption_cues']);a['source_of_truth']='shots[].caption_cues'
 if c['id']=='C07':c['text_assets'].append({'cut':'K04','mode':'후편집 화면 자막','cues':copy.deepcopy(ss['K04']['caption_cues']),'source_of_truth':'shots[].caption_cues'})
 for sc in c['scene_list']:
  if sc['cut'] in ss:sc['action']=ss[sc['cut']]['next_motion']
 for u in [u for u in d['generation_units'] if u['concept_id']==c['id']]:
  s=ss[u['linked_shot']]
  if u['id'] not in ['C05_K02A','C05_K02B']:u['action']=s['next_motion'];u['framing']=s['framing']
  if u['id']=='C05_K02A':
   u['continuity_in']=s['continuity_in']
   u['continuity_out']='기둥은 왼쪽 바닥에 놓였고 괴수는 끝까지 직립·양손 자유·지붕 수평. 목·무릎 접기는 다음 B에서 시작. 포치 아래 진입하지 않음.'
  if u['id']=='C05_K02B':
   u['continuity_in']='A 채택 끝 상태를 이어 기둥은 왼쪽 바닥, 괴수는 밖에서 직립·양손 자유·지붕 수평. 이 상태부터 목·무릎을 접기 시작. 실제 제작에서는 채택 A의 종료 프레임을 B 시작에 우선 사용.'
   u['continuity_out']=s['continuity_out']
  u['editorial_used_seconds']=3 if u['id']=='C05_K02A' else 4 if u['id']=='C05_K02B' else s['duration']
  u['source_clip_seconds_planned']=8
  u['status']='V11 final review; NOT_SUBMITTED_TO_FLOW'
  e=ims[u['id']];e['next_motion']=u['action'];e['camera_notes']=u['framing'];e['editorial_used_seconds']=u['editorial_used_seconds'];e['reuse_source_v11']=f'{SRC.name}/{e["image_path"]}'
  if 'continuity_in' in u:e['continuity_in']=u['continuity_in'];e['continuity_out']=u['continuity_out']
  e['review_record']='review_summary.json';e['review_status']='V11 re-review pending reconfirmation; V10 provenance preserved'

ov.update({
 'C02_K02':'TE stops the tray. DE ceremoniously blocks the products with his whole body, far too seriously. When IN points at the monitor, DE keeps his blocking posture and turns only his head. No dialogue or wink.',
 'C07_K04':'CW drops a soft rope loop onto empty sand in front of EX, never around a body. With her free right hand she singles out EX, then points to the empty place beside herself. EX nods once. No waiting.',
 'C07_K05':'EX turns the open notebook toward CW. Q1 follows the page with his gaze and lightly holds the nearby slack rope; Q2 holds another slack section while watching the same notebook. Nobody is restrained. EX uses one hand to hold the book and does not grow another pointing hand.',
 'C07_K06':'CW guides the slack rope toward herself. EX walks voluntarily; Q1 and Q2 walk with the notebook to keep watching it. CW steps back as all three arrive. The two questioners block her view again; hold her failed attempt to look through for at least half a second. Keep a clear final approach for a four-second editorial selection. Do not drag anyone.',
 'C08_K03':'ST starts rotating the practical set. OP notices the audience gaze following it and steps once to reclaim their attention; their gaze continues toward the set. Reveal only part of the work area.',
 'C08_K04':'ST points to the three blank work cards. CO and AU look toward the screen rather than OP. Keep the same fixed upper-left light and visible screen glare. Exact process graphics will already exist from the start in post, not switch on during this shot.',
 'C08_K05':'OP notices nobody watching him, steps forward and spreads his large cape, exposing its black lining. ST notices that dark surface. Keep the existing screen glare. Never cover the audience view of the screen.',
 'C08_K06':'ST raises the free cape corner toward the fixed upper-left light. OP follows by raising his arms so the black lining enters the light path between lamp and screen. Keep the screen visible to the camera. Hold the high-cape end pose for at least one second. The editor will match the beam occlusion and screen reflection, while keeping the same exact graphic. Do not dim the whole room.',
 'C08_K07':'CO points his baton toward the work screen. OP follows it with his eyes, then only tightens the already raised cape slightly. Preserve the high black lining and fixed lighting geometry. Do not lower and raise the cape again.',
 'C09_K08':'AL opens an empty palm above the helmet inside the service area. After a brief half-second beat, only AR_R brings the remaining thin paper bundle toward that palm. AL withdraws his hand. R lowers the same bundle into the open helmet just below, releases it and retreats. AL freezes and looks at the arm. The other arm stays folded. No extra papers.',
 'C09_K09':'Within the first second AL slides the paper-filled helmet a little toward HU and raises his chin. Within the next two seconds HU removes and opens one thin sheet from inside that helmet. For the remaining five seconds both look at that same sheet without extra pointing or transfer. Existing notebook and folder stay on the table. Eight-second source, no freeze extension.',
 'C10_K04':'The visible reel feeds a long red repair strip and reconnects the two ribbon ends. Excess feeding continues and the main ribbon droops in a large soft U down to the floor. MC watches it while maintaining his ceremonial smile. Do not also attempt scrap cutting, falling, scissor gluing, or lifting in this shot. Those consequences belong to the next start state.',
 'C10_K05':'DV presses stop and the reel and repair head stop completely. The two closed scissors are already joined by a separate short tape scrap on the tray, not connected to the long ribbon. MC lifts one handle just a little so both scissors move together once, puts them back, and looks at the long ribbon. No attempt to pull them apart.'
})
for uid in ['C09_K01','C09_K03','C09_K04','C09_K05']:
 ov[uid]=units[uid]['action']+' '+rule
ov['C09_K04']='AL opens his empty right palm to block the notebook. HU leans slightly around the hand and keeps looking at it. Hold that open palm during the final 0.4 seconds. BOTH robot arms remain folded and completely still until this shot ends. The editor adds a small service indicator. Do not start, unfold, or move either arm here. The one arm departure belongs only to the next shot.'
ov['C09_K05']='Continue the existing open-palm request from the previous shot. AR_L starts immediately once, picks up the single correction folder and offers it in front of AL\'s already open right hand. AL reluctantly accepts it, now holding the result plaque in his left hand and the folder in his right. AR_R stays folded. No repeated palm gesture, second start, or extra delay.'
d.update(run_id=R.name,status='V11 final pre-production review, reconfirmation pending')
d['scope']='V10의10안·88시작 상태를 유지한 최종 제작 전 검토. 자막·인과·호흡·동작 명세 보완. 모든 자막은 후편집. Flow 실행 없음.'
d['caption_style']['source_of_truth']='shots[].caption_cues; text_assets.cues is a synchronized convenience copy. Use neither historical V10 mirrors nor image-generation prompt text for placement.'
d['notes']=['10안의 선택된88시작PNG를 V10에서 바이트 그대로 재사용. 새 이미지·Flow·영상·음원 생성0.','V11 수정: 자막 명세 동기화, C07 39초, C08 차광 인과, C09 44초, C10 복합동작 분리.','기존 완성 C01·C03 원본과 V10 전체 보존. 실제 움직임/최종 합성/현장 가독성/관객 반응은 영상 제작 뒤 검수.']
m.update(run_id=R.name,status='88 selected V10 starts reused; V11 motion specifications; no Flow submissions',new_images=0,reused_images=88)
put(R/'storyboards.json',d);put(R/'scene_manifest.json',m);put(R/'motion_overrides.json',ov)
print('Applied final-review delta and synchronized shot/unit/scene/manifest/caption mirrors.')
