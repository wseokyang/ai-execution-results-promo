from pathlib import Path
import json, shutil, hashlib
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

q=read(R/'generation_requests/C05_K07_review_fix_v3.json')
q['source_generated_path']='C:/Users/wseok/.codex/generated_images/01a13daf-3732-7b90-99a8-92c605090d35/exec-845f1f22-ed5f-4df8-9073-90f50064e832.png'
dst=R/q['image_path']; src=Path(q['source_generated_path'])
if not dst.exists():shutil.copyfile(src,dst)
assert sha(src)==sha(dst)
put(R/'generation_requests/C05_K07_review_fix_v3.json',q)
a=read(R/'artist_C05_partC.json')
e=next(x for x in a['images'] if x['id']=='C05_K07')
if e['image_path']!='images/C05/S07_v3.png':
    old=dict(e);old.pop('attempts',None)
    interim=read(R/'generation_requests/C05_K07_review_fix.json')
    interim['sha256']=sha(R/interim['image_path'])
    interim['artist_review']={'opened_actual_image':True,'status':'superseded','notes':['귀 방향은 복구됐지만 컵이 주둥이 앞에 남아 다음 국소 수정으로 교체.']}
    e['attempts'] += [old,interim]
    for k in ['image_path','source_generated_path','prompt','referenced_image_paths']:e[k]=q[k]
    e['sha256']=e['source_sha256']=sha(dst)
    e['dimensions']=[1672,941]
    e['artist_review']={'opened_actual_image':True,'status':'candidate_after_cross_review_fix','notes':['실제 전체 생성 출력 확인. 주둥이 왼쪽·보이는 귀 오른쪽·같은 S자 목·양손 지붕 지지 유지.','이어컵이 노출된 귀 바로 옆에 있고 미장착. 기술자가 팔을 자연스럽게 뻗고 반대 손은 사다리를 잡음.','첫 수정에서 컵이 주둥이 앞에 남아 국소 수정 1회 추가. 두 이전 파일·정확 요청 보존. 독립 재확인 대기.']}
put(R/'artist_C05_partC.json',a)

d=read(R/'storyboards.json')
for c in d['concepts']:
    for s in c['shots']:
        for cue in s.get('caption_cues',[]):
            top=any(k in cue.get('placement','') for k in ['상단','top','upper'])
            cue['box']={'left_pct':7,'width_pct':86,('top_pct' if top else 'bottom_pct'):6}
        if c['id']=='C01' and s['id'] in ['K06','K07']:
            for cue in s['caption_cues']:
                cue['placement']='상단 벽. 아래 착지 자세·손·다리 비움.'
                cue['box']={'left_pct':7,'width_pct':86,'top_pct':5}
        if c['id']=='C01' and s['id']=='K09':
            for cue in s['caption_cues']:
                cue['box']={'left_pct':7,'width_pct':49,'top_pct':7}
        if c['id']=='C02' and s['id']=='K09':
            for cue in s['caption_cues']:
                cue['box']={'left_pct':25,'width_pct':50,'top_pct':1.5,'font_cqw':3.0}
        if c['id']=='C03' and s['id']=='K06':
            for cue in s['caption_cues']:
                cue['placement']='상단 왼쪽 x3~29%, y4%. 두 파일과 R 얼굴을 비움.'
                cue['box']={'left_pct':3,'width_pct':26,'top_pct':4,'font_cqw':3.1}
        if c['id']=='C04' and s['id']=='K01':
            for cue in s['caption_cues']:
                cue['placement']='상단 빈 목재. 아래 손·배·식사 쪽지를 비움.'
                cue['box']={'left_pct':7,'width_pct':86,'top_pct':4}
        if c['id']=='C04' and s['id']=='K09':
            for cue in s['caption_cues']:
                cue['box']={'left_pct':35,'width_pct':60,'top_pct':3,'font_cqw':3.0}
        if c['id']=='C05' and s['id']=='K07':
            s['first_frame']='주둥이 왼쪽·보이는 귀는 머리 오른쪽으로 와이드와 같은 축. TE가 검정 이어컵을 그 귀 바로 옆에 띄워 든 미장착 상태. 양손 지붕 지지 유지.'
            s['next_motion']='TE가 화면에 보이는 같은 귀에 이어컵과 뒤끈을 건다. 실체 공개 후 들리세요? 자막. 괴수 한 번 깜빡임. 발화 없음.'
            s['framing']='와이드와 같은 쪽에서 당긴 사다리 상부 미디엄. 주둥이 왼쪽·귀 오른쪽·같은 S목. 기술자와 양손 지붕 지지 일부.'
        if c['id']=='C05' and s['id']=='K08':
            for cue in s['caption_cues']:
                cue['placement']='38초 몸개그 완료 뒤 하단 명시 박스. 얼굴·귀·지붕·양손은 항상 비움. 바닥 일부를 덮는 제목판 허용.'
                cue['box']={'left_pct':7,'width_pct':86,'bottom_pct':2}
            s['framing']='외부 고정 와이드. 같은 S목·무릎·양손 지지. 몸개그 3초 후 하단 제목판을 사용해 지붕·손·얼굴을 보존한다.'
    for asset in c['text_assets']:
        if 'cues' in asset:
            shot=next(s for s in c['shots'] if s['id']==asset['cut'])
            asset['cues']=shot['caption_cues']
for u in d['generation_units']:
    c=next(c for c in d['concepts'] if c['id']==u['concept_id']);s=next(s for s in c['shots'] if s['id']==u['linked_shot'])
    if u['id']=='C05_K07':
        u['first_frame']=s['first_frame'];u['action']=s['next_motion'];u['framing']=s['framing']
        u['image_prompt_english']='Same-side medium close view matching S08_v2: muzzle points SCREEN LEFT, visible ear on SCREEN RIGHT behind eye, same S-folded neck. Technician holds one black wired earcup just off this SAME visible ear before fitting; both monster hands support roof. No mirror/reverse camera. No text.'
    if u['id']=='C05_K08':u['framing']=s['framing']
    if s.get('caption_cues'):u['caption_safe_zone']=' / '.join(dict.fromkeys(q['placement'] for q in s['caption_cues']))
    for scene in c['scene_list']:
        if scene['scene_id']==u['scene_id']:
            for k in ['first_frame','action','framing','caption_safe_zone']:
                if k in scene:scene[k]=u[k]
d['caption_style']['preview_layout']='各 caption_cues.box에 16:9 화면 대비 % 좌표를 지정. 행사명 5cqw, 보조 문구3cqw. PNG 원본 미변경. 실제 영상의 움직이는 손·얼굴은 후속 편집에서 다시 확인.'
put(R/'storyboards.json',d)
print('C05 S07_v3 preserved; explicit caption boxes applied.')
