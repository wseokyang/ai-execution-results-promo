"""Reconcile preserved generation records with the reviewed edit decisions."""
from pathlib import Path
import json,hashlib
F=Path(__file__).resolve().parent; E=F.parent/'2026-10-26_C08-C09-edit-v15'
log=json.loads((F/'generation_log.json').read_text(encoding='utf-8'))
selected={}
for cid in ['C08','C09']:
    m=json.loads((E/cid/'edit_manifest.json').read_text(encoding='utf-8'))
    for row in m['timeline']:
        if row.get('file') and row['file'].endswith('.mp4'):
            selected[row['file']]={'source_in':row['source_in'],'source_out':row['source_out'],
                'edit_start':row['start'],'edit_end':row['end'],'crop':row.get('crop'),
                'edit_manifest':f'storyboards/{E.name}/{cid}/edit_manifest.json'}
rejected={
    'C08_K08_take01.mp4':'벽돌이 빈 칸에 들어가지 않고 다른 벽돌과 겹침. take02 사용.',
    'C08_K10_take01.mp4':'교정할 벽돌을 아래로 빼고 합쳐지는 형태 변화. take02 사용.',
    'C09_K04_take01.mp4':'발을 버스 안에 넣은 뒤 되돌아와 탑승을 끝내지 못함. take02 사용.',
    'C09_K07_take01.mp4':'충전기 인출 손·주머니 방향 불일치. take02의 공개된 구간만 사용.',
    'C09_K09_take01.mp4':'문 열림 상태와 버스 이동 방향 부정합. take02의 떠나는 후반만 사용.'}
partial={
    'C09_K07_take02.mp4':'인출은 여전히 반대 주머니로 손이 가는 결함. source4.5–6.5의 오른손에 이미 든 충전기 공개만 사용. 인출 동작 성공 아님.',
    'C09_K08_take01.mp4':'이전 폰 소실 구간을 제외하고 source1.5–3.25 실제 전달 42프레임을 [330,215,810,485] 크롭. 여성 오른손 수령과 확대 선명도 손실이 남음.',
    'C09_K09_take02.mp4':'초기 문 미닫힘 이동/축 모호함을 제외. source3.5–6.5 이미 떠나는 후면만 사용. 문 닫힘·초기 출발 성공 아님.'}
for r in log['generation_requests']:
    fn=r['original_file'];p=F/fn
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest==r['technical_validation']['sha256']
    r['status']='completed_downloaded_preserved'
    if fn in selected:
        r['review_status']='selected_partial_with_documented_omission' if fn in partial else 'selected_interval_visual_reviewed'
        r['selected_interval']=selected[fn]
        r['review_note']=partial.get(fn,'편집 기록의 선택 구간에서 필요한 동작과 전후 연결을 실제 추출 프레임으로 확인. 전체 8초가 무결하다는 의미는 아님.')
    else:
        assert fn in rejected,fn
        r['review_status']='rejected_for_final_edit';r['review_note']=rejected[fn]
    r['actual_listening_verified']=False
    r['continuous_playback_verified']=False
    r['source_audio_used_in_edit']=False
obs=log['account_observations']
for u,purl,notice in [
    ('u3','https://flow.google.com/u/3/project/9ec66691-04b1-4d69-802c-fccee9804efd','매일 11:21 표시; 이 요약에는 오전/오후 미기록'),
    ('u4','https://flow.google.com/u/4/project/c814d669-12b7-4857-90b8-d88ea3f15137','매일 10:01 표시; 이 요약에는 오전/오후 미기록')]:
    if not any(x['alias'].endswith(u) for x in obs):obs.append({'alias':f'2026-10-26_observed_{u}',
        'opening_balance':50,'closing_balance':0,'requests':5,'credits_used':50,'failures':0,
        'project_url':purl,'refresh_notice_summary':notice})
assert len(log['generation_requests'])==25 and len(selected)==20 and len(obs)==5
log['editorial_summary']={'planned_cuts':20,'preserved_takes':25,'selected_take_intervals':20,
    'rejected_takes':5,'partially_selected_with_documented_omissions':3,
    'all_originals_unchanged':True,'cross_review':f'storyboards/{E.name}/cross_review.json'}
(F/'generation_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('25 preserved takes reconciled: 20 selected intervals, 5 rejected; 5 accounts observed zero.')
