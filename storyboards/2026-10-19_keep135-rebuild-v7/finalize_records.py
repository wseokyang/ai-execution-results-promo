"""Finalize only after all three reviewers have closed concrete required findings."""
from pathlib import Path
import json

R=Path(__file__).resolve().parent
ROOT=R.parent.parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    for name in ['storyboard_final_confirmation.json','image_final_confirmation.json']:
        confirmation=read(name)
        assert confirmation['status']=='all_three_confirmed'
        assert set(confirmation['reviewers'])=={'A','B','C'}
        assert all(not x['required_remaining'] for x in confirmation['reviewers'].values())
    v=read('validation.json');assert v['status']=='passed' and v['retained_images']==25
    d=read('storyboards.json');cs=d['concepts'];new=[c for c in cs if c['id'] in ['C02','C04']]
    d['status']='storyboards_and_first_frames_complete_user_creative_review_pending'
    put('storyboards.json',d)
    team=read('team_execution.json');team['status']='complete';team['image_review']='three independent reviews, peer cross checks, required finding closure';team['delivery']='local gallery, Markdown, selected PNGs, prompts and records complete; packaging verified separately'
    for stage in team['actual_collaboration']:
        if stage['stage']=='첫프레임생성':stage['status']='complete'
    if not any(x['stage']=='실제이미지독립·교차·필수지적확인' for x in team['actual_collaboration']):team['actual_collaboration'].append({'stage':'실제이미지독립·교차·필수지적확인','agents':['/root/v6_review_a','/root/v6_review_b','/root/v6_review_c'],'result':'image_review_A/B/C.json, image_cross_reviews.json, image_revision_disposition.json, image_final_confirmation.json'})
    put('team_execution.json',team)
    put('progress.json',{'status':'complete','stage':'storyboards_and_actual_first_frames','retained_images':25,'new_images':v['new_images'],'total_images':v['total_images'],'Flow':'not_used','new_video_or_audio':False})
    put('delivery_status.json',{'status':'complete','scope':'storyboards and actual per-cut first-frame PNGs; C01/C03/C05 preserved','new_images':v['new_images'],'retained_images':25,'video_audio_flow':False,'new_concepts_user_accepted':False})
    put('review_summary.json',{
        'status':'required_storyboard_and_image_findings_closed',
        'user_scope':'V6 C05 accepted; C01/C03/C05 unchanged; C02/C04 rewritten for concrete AI use and experience sharing; Trojan horse retained',
        'creative_changes':[
            'C02: AI가 다수 검사사진에서 묶은 유사 흔적을 사람이 겹쳐 확인하고 촬영창 청소·재촬영으로 원인을 확인. 공개 설명을 들은 형사가 증거 확보를 하다가 다음 문제의 원인이 됨.',
            'C04: AI가 내부 탑승자 없음 신고와 식사·물·수저 요청의 내용 충돌을 후보로 제시. 사람이 원문·실물을 확인하고 급식 수레로 확인하자 부인 뒤 그릇이 일제히 튀어나옴.',
            '기술 설명을 따로 늘리지 않고 증거 공개와 인물의 선택이 다음 사건을 만들도록 구성. 중복 설명 대사를 줄여 C02 35초, C04 34초로 정리.',
            'C01/C03/C05 전체 콘티 객체와 채택 PNG25장은 V6와 동일.'
        ],
        'concept_gate':'concept_gate_reviews.json','storyboard_review':'storyboard_final_confirmation.json',
        'image_reviews':['image_review_A.json','image_review_B.json','image_review_C.json'],
        'image_cross_check':'image_cross_reviews.json','image_disposition':'image_revision_disposition.json','image_final':'image_final_confirmation.json',
        'preservation':'preservation_manifest.json','reference_scope':'reference_diagnosis.json',
        'limits':['실제 정지 PNG와 계획 대사·행동 검토','동작·음성·립싱크·관객 반응 미검증','내부 검토 완료는 신규2안의 사용자 창작 수용을 뜻하지 않음','로컬 HTML 브라우저 자동 검수는 기존 제한을 존중해 수행하지 않음. 실제 PNG·문서·정적 링크 검사']
    })
    put('future_production_notes.json',{
        'scope':'향후 별도 영상 제작 요청 때 사용할 메모. 이번 영상·음원·Flow 실행 없음.',
        'notes':{c['id']:{s['id']:s.get('postproduction_notes','') for s in c['shots']} for c in cs},
        'constraints':['생성 원본 PNG를 바꾸지 않음','화면 자막·도식은 콘티의 후편집 지시와 실제 첫 프레임을 함께 확인','촬영창 얼룩·수갑 가림의 연출 결과는 향후 동작 제작 때 확인','AI 활용 사례는 허구이며 실제 사내 성과로 소개하지 않음','ai-flow 재개·크레딧 사용은 새 영상 제작 요청 전 금지']
    })
    rows=['# V7 — 1·3·5안 유지, 2·4안 다시 구성','','[전체 이미지 콘티](index.html) · [전체 컷 표](STORYBOARDS.md) · [정확한 프롬프트·씬 매핑](scene_manifest.json)','']
    for c in cs:rows.append(f"- {c['id']} 「{c['title']}」 {c['duration_seconds']}초 / "+('V6 콘티·이미지 그대로' if c['id'] in ['C01','C03','C05'] else f"새 이야기·첫 프레임 {len(c['shots'])}장"))
    rows+=['',f"새 첫 프레임 {v['new_images']}장과 보존 25장, 총 {v['total_images']}장입니다. 새 PNG는 내장 image_gen 생성 원본 바이트를 복사했으며 수정 이전 버전도 보존했습니다.",'','자료 재확인, 두 작가 독립 발상 4개씩, 카드 검토, 전체 콘티와 실제 이미지의 3인 독립·교차·필수 지적 확인을 마쳤습니다. 신규2안의 재미에 대한 사용자 승인을 뜻하지 않습니다.','','기존 완성 C01 36초 v07, 기존 콘티·배포 패키지·원자료는 보존했습니다. 이번 Flow 업로드·동영상·음원 생성·크레딧 사용은 없습니다. ai-flow PAUSED 유지.','','[검토 요약](review_summary.json) · [보존 증명](preservation_manifest.json) · [확인한 자료 범위](reference_diagnosis.json) · [기술 검증](validation.json)']
    (R/'README.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    labels=' / '.join(f"{c['id']} {c['title']} {c['duration_seconds']}초{len(c['shots'])}컷" for c in new)
    resume=f'''[2026-10-19 V7 최신 완료 — C01·C03·C05 유지 / C02·C04 AI 실행과 행사 연결 재작성]
최신 사용자: V6 C05 좋음, C02/C04는 AI 발표대회 관련성 부족. 트로이목마 한 안 유지 가능. C01/C03/C05 전체 콘티 객체와 채택25PNG는 V6와 바이트·객체 동일.
작업: storyboards/{R.name}/ (index.html, STORYBOARDS.md, scene_manifest.json, review_summary.json).
새 안: {labels}. 신규 실제 첫 프레임 {v['new_images']}장 + 보존25장 = {v['total_images']}장. 채택 경로는 scene_manifest/storyboards를 사용하며 수정 이전 PNG는 보존.
연구·두 작가 독립발상·3인 전체콘티 독립/교차/수정확인·실제PNG 독립/교차/필수지적확인 완료. 관객반응·새2안 사용자수용·실제동작·음성·립싱크 미검증. future_production_notes.json 확인.
Windows 검토본: C:/Users/wseok/.codex/visualizations/2026/10/19/01a13daf-3732-7b90-99a8-92c605090d35/B_comedy_keep135_rebuild_v7/index.html
같은 상위 폴더 B_comedy_keep135_rebuild_v7_full_package.zip. 패키지 검증 별도. Git 반영 상태는 git log/remote로 확인.
기존 완성 C01 36초 v07 SHA 유지. Flow·동영상·음원 생성0, ai-flow PAUSED 유지. 이번 시나리오/첫프레임 요청으로 이전 자동생성 큐를 재개하지 않는다.

이하 이전 작업 이력 — 최신 V7 지시 우선
'''
    resume_path=ROOT/'RESUME_CODEX.txt';data=resume_path.read_bytes()
    marker=b'[2026-10-19 V6 '
    if data.startswith('[2026-10-19 V7 '.encode()):data=data[data.index(marker):]
    resume_path.write_bytes(resume.replace('\n','\r\n').encode('utf-8')+b'\r\n'+data)
    rootreadme=ROOT/'README.md';data=rootreadme.read_bytes()
    latest=f'''## 최신: 2026-10-19 V7

사용자가 선택한 1·3·5안은 그대로 보존하고, 2·4안은 AI 활용과 결과 공유가 사건을 만드는 이야기로 다시 구성했습니다. 신규 {v['new_images']}장 + 보존25장. 영상·음원·Flow 생성 없음.

[V7 이미지 콘티](storyboards/{R.name}/index.html) · [전체 컷 표](storyboards/{R.name}/STORYBOARDS.md) · [검토 요약](storyboards/{R.name}/review_summary.json)

아래는 이전 버전 이력입니다. V6의 C02/C04는 사용자가 행사 관련성을 반려했으며 C05는 유지 대상으로 선택했습니다.

'''
    if not data.startswith('## 최신: 2026-10-19 V7'.encode()):rootreadme.write_bytes(latest.replace('\n','\r\n').encode()+data)
    brief=ROOT/'team/brief.toml';data=brief.read_bytes();key='[creative_direction_2026_10_19_keep_c01_c03_c05]'
    data=data.replace('# 최신 2026-10-18 사용자 피드백은 맨 아래 creative_direction_2026_10_18을 우선한다.'.encode(),'# 최신 지시는 맨 아래 creative_direction_2026_10_19_keep_c01_c03_c05를 우선한다.'.encode(),1)
    extra=f'''\n{key}
user_feedback = "V6 C05 좋음. C01/C03/C05 유지. C02/C04는 AI 발표대회 연결 부족으로 교체. 트로이목마는 C04에서 유지."
new_run = "storyboards/{R.name}"
retained = "V6 전체 콘티 객체3개·채택PNG25장. 기존 C01 36초v07 SHA 보존."
delivery = "{labels}. 신규{v['new_images']}장. 전체{v['total_images']}장."
creative_status = "콘티·실제 첫 프레임·3인 독립/교차/필수수정 검토 완료. 신규2안 사용자창작수용·관객재미 미확인."
scope = "시나리오와 컷별 첫프레임만. Flow·동영상·음원 금지. ai-flow PAUSED 유지."
'''
    if key.encode() not in data:brief.write_bytes(data+extra.replace('\n','\r\n').encode())
    print({'status':'complete','new_images':v['new_images'],'total_images':v['total_images']})
if __name__=='__main__':main()
