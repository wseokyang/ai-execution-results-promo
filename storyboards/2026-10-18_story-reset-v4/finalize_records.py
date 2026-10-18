"""Publish completion records only after all three actual-image confirmations."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
ROOT=R.parent.parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    confirmations=read('image_final_confirmation.json')
    assert set(confirmations['reviewers'])=={'A','B','C'}
    assert all(v['status']=='confirmed_no_required_issue' for v in confirmations['reviewers'].values())
    d=read('storyboards.json'); m=read('scene_manifest.json')
    assert len(m['images'])==44
    assert all((R/i['image_path']).is_file() for i in m['images'])
    for i in m['images']:
        i['final_review']={'status':'accepted_for_storyboard_first_frame','reviewers':['A','B','C'],'records':['image_reviews_A.json','image_reviews_B.json','image_reviews_C.json','image_reviews_C04.json','image_reviews_C05.json','image_cross_reviews.json','image_cross_reviews_final.json','image_final_confirmation.json'],'limits':'정지 이미지와 계획 검토. 동작·음성·관객반응 미검증. 별도 표기한 UI/도식/자막은 후편집 대상.'}
    put('scene_manifest.json',m)
    d['version']='v4.2_storyboards_and_first_frames_reviewed'
    d['director_notes']['remaining']='콘티·44컷 실제 첫 프레임의 독립·교차 검수 및 수정 확인 완료. 영상 제작은 미실행. 후속 합성/동작 유의사항은 future_production_notes.json.'
    put('storyboards.json',d)
    summary={
      'status':'complete_for_requested_storyboards_and_first_frames',
      'preserved_film':'../2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4',
      'preserved_sha256':'b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c',
      'new_concepts':5,'selected_images':44,
      'concepts':[{'id':c['id'],'title':c['title'],'duration_seconds':c['duration_seconds'],'cuts':len(c['shots'])} for c in d['concepts']],
      'collaboration':'자료 조사→두 작가 독립 후보→PD5안선정→연출가전체콘티→서로다른3명독립/상호교차/수정확인→이미지3담당분담→실제이미지3명독립/교차/수정확인',
      'storyboard_records':'storyboard_reviews.json',
      'image_records':['image_reviews_A.json','image_reviews_B.json','image_reviews_C.json','image_reviews_C04.json','image_reviews_C05.json','image_cross_reviews.json','image_cross_reviews_final.json','image_final_confirmation.json'],
      'main_story_fixes':['C01 악마의 자발적 발표 욕구를 칭찬·자부심으로 연결','C02 막으려던 실패를 되살리는 목표 역전, 실행/폐기 인과 명료화','C03 실패 환경 배송 뒤 제출 대신 직접 들으러 가는 참석 행동','C04 옥상/모니터 컷 분리, 감독 의자 상실로 두 번째 주연의 등장 시각화','C05 두 번째 기록 출처·자기규칙 해제 순서 확보, 원인 없는 의자 이동 삭제'],
      'main_image_fixes':['C01 문·의자·직원·선 한 구도 및 빨간 조건 카드 등장 시점 보정','C03 파일을 함께 소지하는 상태 보정','C04 감독 손을 카메라에서 떨어뜨린 시작 상태 보정','C05 문·투사벽 배치 보정 및 프로젝터 광축 국소 수정'],
      'remaining_production_notes':['C02 노트의 복원 도식은 K02를 기준으로 후속 합성; 현재 생성 PNG의 배치 차이 남음','C03 표지 자체가 아닌 내부 조건 기록을 열어 비교; 도식 후편집','C04 대역의 실제 입력·감독의 다리 풀기와 의자 이전은 영상에서 호흡 확인','C05 표에는 숫자3, 설명은 화면자막; 표부착→사진→선절단','행사명·자막·UI는 별도 편집 정보이며 현재 PNG의 텍스트 완성본이 아님'],
      'user_creative_acceptance':'not_claimed','audience_response_measured':False,
      'not_performed':['Flow 업로드','동영상 생성','음원 생성','영상 렌더링','실제 음성/립싱크 검수','공개 게시'],
      'automation':'ai-flow PAUSED 직접 확인, 변경/재개 없음',
      'reference_scope':'reference/reference_audit.json의 실제 화면·자동자막·공식설명 범위. 전편 연속시청/실제 청취 주장 없음.',
      'ui_qa':'브라우저 도구가 file 프로토콜을 차단해 렌더/조작 검사는 미실행. 실제 이미지 검토와 정적 HTML 링크/구조 검증으로 대체. 우회하지 않음.'
    }
    put('review_summary.json',summary)
    put('delivery_status.json',{'status':'complete','scope':'5안 전체 콘티와 44컷 실제 첫 프레임 및 3인 독립·교차·수정확인','video':False,'user_creative_acceptance':'not_claimed'})
    put('progress.json',{'status':'complete','selected_images':44,'planned_cuts':44,'storyboard_reviews':'complete','image_reviews':'complete','video_generation':False,'flow_upload':False,'automation':'PAUSED'})
    p=R/'README.md';s=p.read_text(encoding='utf-8')
    s=s.replace('현재 진행 상태는 `progress.json`을 확인하세요.','**5안 콘티와 44컷의 실제 첫 프레임, 세 검수자의 독립·교차·수정 확인을 완료했습니다.**')
    s=s.replace('제작 후 `review_summary.json`, `validation.json`에서 검수와 파일 검증을 확인할 수 있습니다.','`review_summary.json`, `validation.json`에서 검수와 파일 검증을 확인할 수 있습니다. 현재 PNG는 컷 시작 이미지이며 행사명·UI·자막과 명시된 노트 도식 합성은 후속 편집 사항입니다.')
    p.write_text(s,encoding='utf-8')
    p=ROOT/'RESUME_CODEX.txt';s=p.read_text(encoding='utf-8-sig');marker='이하 이전 조사·제작 이력'
    history=s[s.index(marker):]
    prefix='''완료 — 2026-10-18 새 5안 V4 콘티·44컷 실제 첫 프레임·3인 교차 검수

- 최신 사용자: 기존 완성 1안 유지, 새 5안 다시 검토. 기존 C01 36초 v07은 변경하지 않았다. 동영상·음원 생성과 Flow 업로드는 금지, ai-flow PAUSED를 직접 확인했다.
- 최신 결과: storyboards/2026-10-18_story-reset-v4/. index.html 이미지·대사 열람본, STORYBOARDS.md 전체 컷 표, storyboards.json v4.2, scene_manifest.json 채택44장·정확프롬프트·참조·원본경로.
- 새 C01 계약이 끝나지 않는 악마 40초9컷 / C02 그 실수, 지우지 마세요 43초9컷 / C03 환경까지 가져왔습니다 42초8컷 / C04 이 장면은 제 경험에 없습니다 39초9컷 / C05 현장 보존 43초9컷. 기존 완성 영상 C01과는 별개다.
- 자료조사·두 작가 독립후보·5안선정·전체콘티·세 명 독립/교차/수정재확인 완료. 실제 이미지 44장 모두 세 명이 연락표와 각자 기록한 개별 PNG로 검토. review_summary.json, image_final_confirmation.json 기준. 사용자 취향 승인이나 관객 웃음 반응을 검증한 것은 아니다.
- 채택 이미지 경로는 storyboards.json 및 scene_manifest.json을 따름. 수정 전 PNG도 보존했다. K05_v3 등 이전 채택본을 임의로 사용하지 말 것. 내장 image_gen만 사용했고 동영상/음원/Flow 사용0.
- 후속 주의: C02 노트 도식은 K02 기준 합성 필요, C03 내부 조건기록 비교, C04 노트북 입력/다리풀기/의자 이전, C05 큰3+화면 설명·표부착→사진→절단. 텍스트와 도식 합성·실제 동작·음성은 미실행. future_production_notes.json 참조.
- 기존 완성 C01 SHA b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c 유지. 원자료·이전5안·이전패키지 보존. 브라우저 file 프로토콜 차단으로 HTML 실화면 자동검사는 미실행; 정적링크와 실제이미지 검증 완료.
- 로컬 배포: C:/Users/wseok/.codex/visualizations/2026/10/18/01a13daf-3732-7b90-99a8-92c605090d35/B_comedy_story_reset_v4/index.html. 전체 ZIP은 같은 상위 폴더의 B_comedy_story_reset_v4_full_package.zip. Git 최신 반영은 git log/remote 확인.

'''
    p.write_text(prefix+history,encoding='utf-8')
    p=ROOT/'README.md';s=p.read_text(encoding='utf-8-sig')
    start=s.index('## 최신 작업 · B급 새 기획 5안');end=s.index('## C01 최종 편집본',start)
    old=s[start:end].replace('## 최신 작업 · B급 새 기획 5안','## 이전 새 기획 V3 · 보존용 이력')
    new='''## 최신 작업 · 이야기부터 다시 만든 새 5안 V4

2026-10-18 사용자 요청에 따라 기존 완성 C01 36초 v07을 유지하고 **별도의 새 5안 콘티와 컷별 첫 프레임 PNG 44장**을 만들었습니다. [이미지·대사 열람본](storyboards/2026-10-18_story-reset-v4/index.html), [전체 컷 표](storyboards/2026-10-18_story-reset-v4/STORYBOARDS.md), [검수 기록](storyboards/2026-10-18_story-reset-v4/review_summary.json)을 확인하세요. 신규 C01~C05는 보존 영상의 버전명이 아닙니다.

돌고래유괴단 공식 작품과 제작자 설명을 조사한 범위 안에서 관계 역전·목표 전환·규모 확대·역할 교체·자기 규칙의 충돌로 구별했습니다. 세 검수자가 콘티와 실제 첫 프레임을 독립·교차 검토하고 수정본을 확인했습니다. 영상 움직임·음성·관객 반응·사용자 취향 승인을 검증한 것은 아닙니다. **Flow 자동 예약은 PAUSED, 영상·음원 생성과 Flow 업로드는 실행하지 않았습니다.**

'''
    s=s[:start]+new+old+s[end:]
    s=s.replace('2. 최신 신규 기획은 [B급 5안·39컷 이미지 열람본](storyboards/2026-10-17_b-comedy-reboot-v3/index.html)입니다.','2. 최신 신규 기획은 [새 5안·44컷 이미지 열람본](storyboards/2026-10-18_story-reset-v4/index.html)입니다.')
    s=s.replace('| `storyboards/2026-10-17_b-comedy-reboot-v3/` | 최신 요청의 새 B급 5안과 컷별 첫 프레임 제작·검수 기록 |','| `storyboards/2026-10-18_story-reset-v4/` | 최신 새 5안·44컷 첫 프레임·독립/교차 검수 |\n| `storyboards/2026-10-17_b-comedy-reboot-v3/` | 이전 5안·39컷 보존 이력. 최신 V4와 구별 |')
    p.write_text(s,encoding='utf-8')
    print('Completion records and root handoff updated after three confirmations.')
if __name__=='__main__':main()
