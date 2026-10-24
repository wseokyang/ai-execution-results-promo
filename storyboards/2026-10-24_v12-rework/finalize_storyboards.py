"""PD integration. Preserve draft and artist provenance; publish selected stills and current actions."""
from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parent; ROOT=R.parent.parent
load=lambda f:json.loads((R/f).read_text(encoding='utf-8-sig'))
d=load('storyboards_draft.json');d['status']='FINAL_STORYBOARD_AND_FIRST_IMAGES_RECHECK';d['revision']='V12 selected-image alignment'
d['verification_scope']='Actual stills and caption/action plan. New C07–C10 Flow motion, final captions, playback and audience response are not verified.'
cs={c['id']:c for c in d['concepts']}
def replace_tree(x,pairs):
 if isinstance(x,str):
  for a,b in pairs:x=x.replace(a,b)
  return x
 if isinstance(x,list):return [replace_tree(v,pairs) for v in x]
 if isinstance(x,dict):return {k:replace_tree(v,pairs) for k,v in x.items()}
 return x
cs['C07']=replace_tree(cs['C07'],[('6슬롯','8슬롯'),('가슴 장비','허리 하네스'),('관통 레일','상단 화면 밖으로 이어지는 두 수직 케이블'),('천장 레일','화면 밖 이동 리그')])
c=cs['C07'];s=c['shots'];v=c['visual_bible']
v['space']='A 전실과 B 시연실 사이 폭넓은 문은 항상 열려 있다. 인물의 두 발 장구에 연결된 두 수직 케이블은 화면 상단 밖으로 이어진다. 상부 이동 리그는 노출하지 않는다. 인물과 두 케이블이 함께 이동하며 문틀과 충돌하거나 벽에 연결되지 않는다. 화면 오른쪽 입장/왼쪽 퇴장.'
s[2].update(frame_start_description='TH는 청록 샘플을 오른손에 쥐고 왼손으로 고정 받침대의 왼쪽 위 모서리를 잡았다. 몸은 받침대 오른쪽, 열린 문 앞 A 쪽이며 문을 아직 넘지 않았다.',action='TH가 왼손으로 고정 받침대 모서리를 자기 몸 쪽으로 당겨 몸을 열린 문 방향으로 이동시킨 뒤 손을 놓는다. 받침대는 움직이지 않고 인물과 두 수직 케이블이 함께 오른쪽으로 이동한다. TH만 계획 밖 이동에 놀란다. 밀기 동작으로 바꾸지 않는다.',camera='35mm 측면 추적. 당김→손 놓기→같은 열린 문 통과를4초에 연결. 이동은1m 이내. 상부 리그와 문틀 충돌은 화면에 만들지 않는다.',comedy_intent='도망치려던 사람의 진지한 선택이 공개 시연실 입장으로 뒤집힌다. 고정 받침대를 당기는 방향과 몸의 이동을 일치시킨다.')
s[8].update(action='TH가 사례판에서 손을 놓으면 HO가 반대쪽 가장자리로 손을 다시 잡은 뒤 판만180도 돌려 빨간 삼각형을 위로 보낸다. TH는 방금 판을 놓은 같은 손으로 돌아간 판의 지점을 찾아 검지를 옮긴다. TH 몸은 계속 거꾸로, HO는 진지하게 판을 받친다.',camera='50mm 판 중심 미디엄. 전달과 반대쪽 재그립2초, 회전2초, 같은 손의 방향 수정과 역상 몸/바른 판 대비2초.')
s[9]['frame_start_description']='HO는 바로 세운 판을 들고, 거꾸로 TH는 방금 판을 놓은 손의 검지가 판 옆에 머문다. 두 샘플·허리 명찰·열린 문은 그대로다.'
cs['C08']=replace_tree(cs['C08'],[('판 오른쪽 상단 사진','판 왼쪽 사진 상단'),('열풍기는 시작 시 RL 오른손, S03 이후 오른쪽 바닥','열풍기는 시작 시 RL 오른손, S03 이후 화면 왼쪽 RL 발 근처 바닥'),('열풍기를 오른쪽 바닥에','열풍기를 화면 왼쪽 RL 발 근처 바닥에'),('흰 판 PR 왼손→S08 RL 양손','흰 판 PR 왼손→S08 후반 전달→S09~10 RL 양손')])
c=cs['C08'];s=c['shots']
s[3]['action']+=' 샘플을 놓은 뒤 PR은 등 쪽인 화면 오른쪽 뒤로 한 걸음 물러나 오른팔을 앞으로 뻗을 준비를 한다.'
s[4]['frame_start_description']='PR은 등 쪽인 화면 오른쪽 뒤로 한 걸음 물러나 오른팔을 앞으로 뻗어 작업등 손잡이10cm 앞에 둔다. 등은 얼굴 방향, 샘플은 어둡다. 흰 판은 왼손.'
s[6]['action']+=' RL이 작업등에 닿을 수 있도록 화면 오른쪽으로 두 걸음 이동한다.'
s[7]['frame_start_description']='RL 왼손은 작업등 손잡이10cm 앞. 등은 정면 하향, PR 흰 판은 왼손. RL은 빈손으로 접근했고 오른손도 비어 있다. 천 탭은 판 아래오른쪽에 고정.'
s[7]['action']=s[7]['action'].replace('RL이 등 머리를','RL이 왼손으로 등 머리를')
s[8]['frame_start_description']='RL은 얼음 밖 줄 끝에서 같은 흰 판을 양손에 든다. 천 탭은 아래오른쪽에 정지. RA는 화면 왼쪽 RL 발 근처 바닥의 열풍기 손잡이 앞에 손을 둔다.'
s[8]['action']='RA가 바닥의 열풍기를 집어 들고 화면 오른쪽 RL의 자료판 쪽으로 이동해 천 탭 아래를 향한다. 탭만 가볍게 펄럭인다. RL이 얼음 없는 자기 판 아래를 보고 RA에게 고개를 돌린다.4.5초. 열풍기가 순간이동하거나 천 탭 위치가 바뀌지 않는다.'
c=cs['C09'];s=c['shots']
s[0]['frame_start_description']=s[0]['frame_start_description'].replace('오른손','왼손')
s[7]['frame_start_description']=s[7]['frame_start_description'].replace('오른손','왼손')
s[3]['action']+=' 카트가 공개되는 끝부터 동일한 비교판 도해를 후합성한다.'
s[6]['action']=s[6]['action'].replace('내려놓는다','평평하게 내려놓는다')+' B1과 B2는 새 발표자인 BW 쪽으로 시선을 돌린다. 새 받침대는 생기지 않는다.'
c['production_notes']['required_post_composite']='카트 판은 K04 덮개 해제 직후부터 K10까지 같은 보라 기어/원자료→AI 요약 도해로 후합성. S05/S06 빈 면과 S07 이후 풍경 임시이미지도 모두 교체. B1 판 S02/S03도 같은 도해로 통일. 생성된 풍경판을 최종 정보로 사용하지 않는다.'
c=cs['C10'];s=c['shots'];c['visual_bible']['props']+=' 흰 L형 샘플은 약6cm의 평평한 단순 L. 컵/그릇/큰 지그재그 부품으로 바꾸지 않는다.'
c['visual_bible']['continuity']=c['visual_bible']['continuity'].replace('고리 상자→WM 왼손→접시','고리 상자→WM 오른손→접시')
s[1]['action']='MN이 상자를 열어 은색 고리를 보여준다. WM 오른손이 고리로 향하고 왼손은 무릎으로 내린다.3.5초, 준비 합6.5초.'
s[1]['transition']='WM 오른손이 고리에 닿기 직전, 같은 손의 근접으로 컷.'
s[2]['frame_start_description']='열린 상자 안 고리, WM 오른손 엄지·검지 접촉 직전. 왼손은 무릎. 조명은 접시 중앙오른쪽을 비춤.'
s[3]['frame_start_description']='WM 오른손 고리는 빈 접시 위, 폰은 테이블에 있다. MN은 빈손으로 내려다본다. 기둥 수직.'
s[3]['action']='WM이 오른손의 고리를 접시에 놓고 같은 오른손으로 폰을 들어 맞춘다. 빈 왼손으로 후보 표시 후합성 화면과 실물의 같은 부분을 비교한다.4초. 손 사이에 고리를 전달하지 않는다.'
s[7]['frame_start_description']='조명은 낮은 결합부에서 왼쪽으로 기울고 빛이 접시를 벗어난 상태. 두 손은 같은 낮은 연결부 양쪽에 공기 간격을 남긴다. 승인 이미지처럼 연결부 일부가 보이며, 기울어진 상부 기둥은 꺾이지 않은 한 직선이다.'
s[7]['action']=s[7]['action'].replace('넓은 구도로 컷','낮은 미디엄 구도로 컷')
s[8].update(frame_start_description='50mm 낮은 미디엄. MN 오른손과 WM 왼손은 낮은 조인트 위·아래에 닿기 직전. 기울어진 직선 상부 기둥, 고리와 평평한 L이 있는 접시를 유지. 머리와 등 머리는 프레임 밖이어도 된다.',action='두 손이 서로 대신 같은 낮은 결합부 위·아래를 잡는다. WM이 하부를 지지하고 MN이 상부의 직선 기둥 전체를 수직으로 되돌린다(첫3초). 빛이 접시의 두 샘플로 돌아온다(다음1초). 남은3.5초 두 손이 고정부를 계속 지지하고 샘플의 안정된 빛을 보여준다. 얼굴 반응은 다음 와이드로 넘긴다.',camera='승인된50mm 낮은 미디엄. 낮은 조인트·직선 기둥 방향·두 손·샘플의 빛에 집중. 머리/등 머리/웨이터 표정 동시 노출은 요구하지 않는다.')
s[9]['action']='두 사람은 조인트를 계속 받친 채 눈을 한번 맞추고 작게 웃는다. WT가 폰 화면과 실물을 비교한다.36초부터 행사 정보5초 고정. 지지손은 놓지 않는다.'
d['concepts']=[cs[k] for k in ['C07','C08','C09','C10']]
man={};man['C07']={e['scene_id']:e for e in load('artist_C07_manifest.json')['images']}
rig={e['scene_id']:e for e in load('artist_C07_rig_revision.json')['images']}
man['C08']={e['scene_id']:e for e in load('artist_C08_manifest.json')['entries']}
man['C09']={e['scene_id']:e for e in load('artist_C09_manifest.json')['scene_to_cut_mapping']}
man['C10']={e['scene_id']:e for e in load('artist_C10_manifest.json')['entries']}
scenes=[]
for c in d['concepts']:
 for shot,sc in zip(c['shots'],c['scene_list']):
  e=man[c['id']][shot['scene_id']];rr=rig.get(shot['scene_id']) if c['id']=='C07' else None
  path=rr['selected_image_path'] if rr else e.get('image_path',e.get('path',e.get('actual_image_path')))
  path=path.replace(str(R.relative_to(ROOT)).replace('\\','/')+'/','')
  src=R/path;assert src.exists(),src
  prompt=(rr.get('exact_submitted_prompt') if rr else None) or e.get('final_prompt',e.get('prompt',''))
  refs=(rr.get('actual_reference_image_paths') if rr else None) or e.get('actual_reference_image_paths',e.get('referenced_image_paths',[]))
  rec={'concept_id':c['id'],'scene_id':shot['scene_id'],'linked_cuts':[shot['cut_id']],'actual_image_path':path,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'prompt':prompt,'references':refs,'next_motion_camera':shot['action']+' / '+shot['camera'],'review_status':'THREE_REVIEWERS_RECHECK_PENDING','motion_verified':False,'source_manifest':f'artist_{c["id"]}_manifest.json','revision_manifest':'artist_C07_rig_revision.json' if rr else None}
  scenes.append(rec);sc.update(planned_image_path=path,actual_image_path=path,image_status='ACTUALLY_GENERATED',representative_frame=shot['frame_start_description'],next_motion_camera=rec['next_motion_camera'],review_status=rec['review_status'],continuity_requirements=c['visual_bible']['continuity'],image_prompt_en=prompt)
  # Old draft directional comments are historical; current locked fields above govern.
  shot['continuity_in']=shot['frame_start_description'];shot['continuity_out']=shot['action']
  shot['speech']='없음. 핵심 정보는 화면과 후처리 자막으로 전달.'
 assert c['shots'][0]['start']==0 and c['shots'][-1]['end']==c['duration_seconds']
 assert all(a['end']==b['start'] for a,b in zip(c['shots'],c['shots'][1:]))
 c['review_status']='FINAL_IMAGE_ALIGNMENT_RECHECK'
d['pd_alignment_note']='Exact submitted image prompts remain provenance, even if wording differs from accepted result. For future Flow, current shot action/camera/selected PNG override draft and historical prompt direction.'
(R/'storyboards.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(R/'scene_manifest.json').write_text(json.dumps({'run_id':R.name,'scenes':scenes,'scene_count':40,'flow_executed':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
names=['07_훔칠_필요가_없었다.md','08_해동하자마자_발표.md','09_낙찰받으신_분이_공개합니다.md','10_청혼은_없었습니다.md']
for c,name in zip(d['concepts'],names):
 lines=['[전체 검수 목록](README.md)',f'# {c["id"][1:]}. {c["title"]}','',f'**{c["one_line"]}**','',f'{c["duration_seconds"]}초 · 10씬 / 시작 이미지10장 · 무대사 · 자막 후처리 · Flow 미생성','',f'**핵심 메시지:** {c["core_message"]}','',f'**반전:** {c["reversals"]}','', '첫 이미지는 동작 전 상태입니다. 영상 동작·후합성·최종 편집 검증까지 끝난 것은 아닙니다.','', '## 인물과 연출','','\n\n'.join(f"- **{a['id']}**: {a['appearance']}. {a['wardrobe']}. {a['performance']}" for a in c['char_visual_bible']),'']
 for shot in c['shots']:
  rec=next(x for x in scenes if x['concept_id']==c['id'] and x['scene_id']==shot['scene_id'])
  lines += [f'## {c["id"]}_{shot["cut_id"]} · {shot["start"]}–{shot["end"]}초','',f'![{c["id"]}_{shot["scene_id"]} 시작 상태]({R.relative_to(ROOT).as_posix()}/{rec["actual_image_path"]})','',f'**첫 상태:** {shot["frame_start_description"]}','',f'**동작:** {shot["action"]}','', '**후처리 자막:** '+(' / '.join(f'{q["start"]}–{q["end"]}초: '+q['text'].replace('\n',' / ') for q in shot['caption_cues']) or '없음'),'', '| 항목 | 내용 |','|---|---|',f'| 대사·내레이션 | 없음 |',f'| 음악·효과음·정적 | {shot["sound"]} |',f'| 구도 | {shot["camera"]} |',f'| 전환 | {shot["transition"]} |',f'| 웃음·정보 의도 | {shot["comedy_intent"]} |','']
 lines += ['## 제작 메모','']+[f'- **{k}:** {v}' for k,v in c['production_notes'].items()]+['',f'[전체 명세·프롬프트]({R.relative_to(ROOT).as_posix()}/storyboards.json) · [실제 이미지 매핑]({R.relative_to(ROOT).as_posix()}/scene_manifest.json)']
 (ROOT/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Published four storyboards, 40 selected still mappings. Pending final cross review.')
