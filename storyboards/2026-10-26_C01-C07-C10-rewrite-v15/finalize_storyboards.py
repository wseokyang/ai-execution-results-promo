"""Align the reviewed storyboard with selected actual images. No generation."""
from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent; ROOT=OUT.parent.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=load(OUT/'storyboards.json')
required=load(OUT/'image_review.json')
assert required['status']=='COMPLETE_WITH_DOCUMENTED_VIDEO_CONDITIONS'
d['scope']='C01/C07/C10 새 콘티 3안·27개 실제 씬 첫 프레임. Flow 영상 미생성.'
d['review_status']='3명 콘티 독립/교차/수정 확인 및 실제 이미지 독립/교차/수정 재확인 완료'
normalized=[]
for c in d['concepts']:
    cid=c['id'];mfile=OUT/'manifests'/f'{cid}_images.json';m=load(mfile)
    ims=m.get('images',m.get('scenes',[]));by={v['scene_id']:v for v in ims}
    c['status']='STORYBOARD_AND_ACTUAL_IMAGES_REVIEWED_FLOW_NOT_STARTED'
    for s in c['shots']:
        sid=s['scene_id']
        if s['image_generation_required']:
            im=by[sid];p=ROOT/im['image_path'];assert p.exists()
            im['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
            im['review_status']='three_independent_reviews_cross_checked_and_required_fixes_rechecked'
            s['selected_first_frame']=im['image_path']
            normalized.append({'concept_id':cid,'scene_id':sid,'linked_cuts':[s['id']],
                'image_path':im['image_path'],'sha256':im['sha256'],
                'prompt':im.get('prompt',im.get('final_prompt')), 'reference_images':im.get('reference_images',im.get('reference_image_paths',[])),
                'motion_camera_notes':im.get('motion_camera_notes',im.get('future_motion_notes')),
                'review_status':im['review_status'],'source_manifest':str(mfile.relative_to(ROOT)).replace('\\','/')})
        if cid=='C01' and sid=='S02':
            s['action']='D가 축포를 자신의 위쪽 공간으로 짧게 세운 뒤 한 번 발사한다. 큰 색종이 조각이 오른쪽 촬영 공간에만 터지고 가라앉는다. 왼쪽 Q의 책상은 깨끗하게 남는다.'
        if cid=='C01' and sid=='S07':
            s['frame_start']+=' 청소가 끝난 받기는 같은 자리에 돌려 놓아 낮은 입구가 D 쪽을 향하고, 높은 뒤벽은 화면 왼쪽이다.'
        if cid=='C01' and sid=='S08':
            s['action']='S가 연결된 노즐을 받기의 높은 뒤벽 위로 짧게 내려 위치를 잡는다. 바람이 같은 종이 더미를 지나 D 쪽 낮은 입구로 나갈 방향이며 아직 OFF다. 장비를 새로 조립하지 않는다.'
        if cid=='C01' and sid=='S09':
            s['action']='S가 발판 옆의 오른발을 짧게 옮겨 발판에 접촉한 뒤 누른다. 송풍이 켜지면 받기 위 종이가 낮은 입구를 지나 D에게만 날아가 머리·수트에 달라붙는다. 같은 발로 끄고 종이가 가라앉는다. 양손은 노즐을 유지한다.'
        if cid=='C01' and sid=='S10':
            s['frame_start']='Q 앞에 기존 노트북과 같은 청색 탭 확인 원문 P가 있다. 펜은 Q의 해부학적 오른쪽 펜받침(이 카메라에서 화면 왼쪽)에 내려놓여 있다. Q 오른손은 비고, 왼손은 책상 원문의 탭 끝을 잡아 들어 보이기 직전이다. D 뒤오른쪽 꽃가루/빈 축포 유지.'
        if cid=='C07' and sid=='S05':
            s['frame_start']='잠시 후. 세 심사위원의 의자는 긴 심사 테이블 옆 열린 바닥으로 이미 옮겨져 같은 후방 출발선에 있다. 테이블은 옆으로 비켜 있고 의자와 카트 사이를 가로막지 않는다. CH는 카트 뒤 양손 손잡이. 카트 오른쪽 서빙영역은 같은 흰 기록통을 닫힌 돔으로 덮고, 왼쪽은 빈 돔 받침이다.'
            s['action']='CH가 열린 바닥의 세 심사위원을 향해 카트를 짧게 밀어 정중히 멈춘다. 카트·테이블·의자의 상대 방향은 이후 S09까지 유지한다.'
            s['frame_end']='카트가 열린 바닥의 심사위원 앞에서 정지. 의자는 같은 후방 출발선, 긴 테이블은 통로 옆. 오른쪽 돔 닫힘/왼쪽 돔받침 비어 있음.'
        if cid=='C07' and sid in ['S06','S07','S08','S09']:
            s['composition']+=' S05 이후 같은 열린 바닥 배치. 긴 심사 테이블은 옆으로 비켜 있고 의자→카트 이동 통로에 없다. 카메라가 바뀌어도 누구도 테이블 뒤로 돌아가지 않는다.'
        if cid=='C07' and sid=='S07':
            s['frame_start']='중앙 JA 의자는 S05에서 정한 열린 바닥의 출발선. 양손 좌판 양옆, 발은 바닥. 뒤의 JB·JC도 같은 출발선에 정지. 공개된 기록통은 앞 카트 오른쪽, 돔은 카트 왼쪽 받침.'
        if cid=='C10' and sid=='S08':
            s['composition']='HU 상체 앞 3/4와 AL을 함께 보는 미디엄. HU 해부학적 왼팔이 열린 케이스를 지지하고 오른손은 비워 아래로 내려 동작 시작 전임이 분명하다. AL도 왼팔 원통 지지/빈 오른손. 각자 자기 문서를 상대에게 돌리기 전, 서로를 바라본다.'
    if cid=='C10':
        c['space_axis']=str(c['space_axis']).replace('건조한','반사가 있는').replace('건조','반사') if isinstance(c['space_axis'],str) else c['space_axis']
        c['selected_image_environment']='반사가 있는 야간 착륙장 바닥. 현재 비나 강풍은 없으며 이미지 8장 내 바닥 상태를 유지한다.'
    if cid=='C07':
        c['space_axis']='밤의 고급 레스토랑 심사실. K01~K04는 긴 흰 테이블 뒤에서 관객 기준 JB 왼쪽/JA 중앙/JC 오른쪽. K05의 명시적 잠시 후 전환에서 세 의자는 테이블 옆 열린 바닥의 같은 후방 출발선으로 옮겨져 있다. 카트는 세 의자 앞이며 긴 테이블은 옆으로 비켜 통로를 가로막지 않는다. K05~K09는 이 공간 기준과 인물 순서를 유지한다. 카트 오른쪽 서빙영역 기록통, 왼쪽 돔 받침. 인양된 초안통과 돔은 준비 시간 생략을 통해 카트로 이동한다.'
        for row in c['continuity_table']:
            if row['prop']=='의자':
                row['from']='K01~K04 심사 테이블 뒤→K05 잠시 후에 테이블 옆 열린 바닥 같은 출발선(JB왼/JA중앙/JC오른)'
                row['forbidden']+='·K05 이후 테이블 뒤로 순간 이동'
    c.setdefault('production_conditions',[])
    c['production_conditions']=['실제 선택 이미지에서 동작을 시작하고 완료 상태까지 생성한 뒤 손·소품·접지 검수. 생성 성공은 아직 미확인.',
        '빈 화면·문서의 지정 내용은 후합성. 생성 이미지에 쓰인 글자로 행사 정보를 대신하지 않음.',
        '화면+후처리 자막으로 이해되어야 함. 생성 음성대사는 사용하지 않음.']
    # Keep schema aliases and scene mapping in sync with the actual selected frames.
    for s in c['shots']:
        s['screen_action']=s['action']
        s['frame_start_description']=s['frame_start']
        s['frame_end_description']=s['frame_end']
        s['future_motion_notes'].update({'camera':s['composition'],'start':s['frame_start'],
            'main':s['action'],'end':s['frame_end']})
        if s['scene_id'] in by:
            im=by[s['scene_id']]
            s['first_frame_prompt_en']=im.get('prompt',im.get('final_prompt'))
            assert s['first_frame_prompt_en'],(cid,s['scene_id'])
            im['motion_camera_notes']=s['future_motion_notes']
            next(x for x in normalized if x['concept_id']==cid and x['scene_id']==s['scene_id'])['motion_camera_notes']=s['future_motion_notes']
    shots_by_scene={s['scene_id']:s for s in c['shots']}
    for scene in c['scene_list']:
        sid=scene['scene_id'];s=shots_by_scene[sid]
        scene['representative_frame']=s['frame_start']
        scene['motion_camera_notes']=s['future_motion_notes']
        if sid in by:
            scene['actual_file']=by[sid]['image_path']
            scene['image_status']='GENERATED_AND_THREE_REVIEWER_CROSS_CHECKED'
    m['independent_review_status']='COMPLETE_THREE_REVIEWERS_INDEPENDENT_CROSS_AND_CORRECTION_RECHECK'
    m['review_status']='ACTUAL_SELECTED_IMAGES_CROSS_REVIEWED_FUTURE_FLOW_MOTION_NOT_VERIFIED'
    save(mfile,m)
assert len(normalized)==27
save(OUT/'storyboards.json',d)
save(OUT/'scene_manifest.json',{'run_id':OUT.name,'scene_count':27,'scenes':normalized,
    'flow_generated':False,'image_review':'image_review.json'})
print('Aligned 3 reviewed storyboards and 27 selected image mappings.')
