from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8'))

def write(name,value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    recheck=read('image_revision_confirmation.json')
    assert recheck['status']=='three_reviewers_confirmed_required_resolved'
    assert set(recheck['reviewers'])=={'A','B','C'}
    assert all(not r['required_unresolved'] for r in recheck['reviewers'].values())
    manifest=read('scene_manifest.json')
    storyboard=read('storyboards.json')
    mapping={(e['concept_id'],e['cut_id']):e for e in manifest['images']}
    assert len(mapping)==39
    for c in storyboard['concepts']:
        for s in c['shots']:
            entry=mapping[(c['id'],s['id'])]
            s['image_file']=entry['image_path']
            entry.setdefault('artist_recorded_first_frame',entry.get('first_frame',''))
            entry.setdefault('artist_recorded_next_motion',entry.get('next_motion',''))
            entry['first_frame']=s['first_frame']
            entry['next_motion']=s['next_motion']
            entry['final_storyboard_first_frame']=s['first_frame']
            entry['final_storyboard_next_motion']=s['next_motion']
            entry['final_review']={'status':'accepted_after_independent_peer_cross_review','reviewers':['A','B','C'],'scope':'still first frame','notes_file':'review_summary.json'}
    storyboard['version']='pd-final-2.4-reviewed-image-paths'
    manifest['status']='complete_39_selected_first_frames_reviewed'
    write('storyboards.json',storyboard)
    write('scene_manifest.json',manifest)
    all_png=list((ROOT/'images').rglob('*.png'))
    write('review_summary.json',{
        'status':'planning_and_first_frame_images_complete',
        'storyboard':{'concepts':5,'cuts':39,'durations_seconds':[31,29,31,30,29],'reviewers':['A','B','C'],'independent_then_peer_cross_then_revision_confirmation':True,'record':'review_revision_confirmation.json'},
        'images':{'selected':39,'independent_reviewers':['A','B','C'],'each_reviewed_all_39_actual_selected_PNGs':True,'peer_cross_review_complete':True,'required_revision_recheck_complete':True,'all_png_including_history':len(all_png),'records':['image_review_round1.json','image_review_selection_round1.json','image_review_cross.json','image_revision_confirmation.json']},
        'required_image_repairs':[{'cuts':'C05 K01-K05','reason':'same public poster must exist before reveal','result':'same mint/magenta/black design, defocused at beginning'},{'cuts':'C04 K07','reason':'audience must continue watching assistant, not magician','result':'foreground magician/hat separated from attention corridor'},{'cuts':'C02 K06','reason':'simple tape contact must work in five-second beat','result':'two inward-facing tape tails; wrists and tails initially separated'}],
        'document_alignment':['C01 visible side panel and host hand withdrawal','C02 actor-right notebook coordinate','C04 foreground magician movement','C05 inner bag / outer flyer hand naming','C05 title left53% placement','all image_file values match selected manifest'],
        'optional_retained':[{'id':'C03 ending pose','decision':'retain chin-resting title-plate pose; does not undo role reversal'},{'id':'C03 sleeve stripe','decision':'fine two-line/one-line difference remains in K05/K06 versus adjacent shots; identity and handoff clear'}],
        'pd_reason':'Prioritize readable causes, changing events and reversals. Optional costume/pose polish does not justify disturbing usable frames.',
        'purpose_recommendations':{'attendance':'C04','event_opening':'C02','broad_overacting':'C01'},
        'unverified':['motion timing in actual video','pronunciation','lip-sync','measured audience humor response','future Flow generation success'],
        'event_unknowns':['exact date/time','venue','attendance route','awards','performance figures'],
        'flow_uploads':0,'new_video_audio_generation':0,'automation':'PAUSED','existing_C01':'preserved unchanged'
    })
    write('delivery_status.json',{'status':'complete','scope':'five new B-grade scenarios, full storyboards and actual independent first-frame PNG per cut','new_concepts':5,'selected_cut_images':39,'all_png_including_revision_history':len(all_png),'durations_seconds':[31,29,31,30,29],'entrypoint':'index.html','full_storyboards':'STORYBOARDS.md','image_mapping_and_prompts':'scene_manifest.json','review':'review_summary.json','validation':'validation.json','existing_C01_final_preserved':True,'video_generation':0,'audio_generation':0,'Flow_uploads':0,'Flow_credit_use':0,'automation_status':'PAUSED','resume_automation_only_after_separate_user_video_request':True})
    progress=read('progress.json')
    progress.update({'latest_stage':'delivery_complete','status':'complete','actual_new_images':39,'image_reviews_complete':True,'image_peer_cross_reviews_complete':True,'image_revision_confirmation_complete':True,'final_storyboard_cuts':39})
    write('progress.json',progress)
    readme=ROOT/'README.md'
    text=readme.read_text(encoding='utf-8')
    text=text.replace('**현재 상태: 콘티 3인 검수 완료, 실제 이미지 제작 중. 이미지 납품 완료 상태는 `delivery_status.json` 기준으로 확인한다.**','**완료: 신규 5안·39컷 콘티와 컷별 독립 첫 프레임 PNG 39장. 세 검수자의 독립·교차 검수 및 필수 수정 재확인을 마쳤다.**')
    text=text.replace('이미지 제작·검수 후 생성한다.','이미지를 클릭하면 원본이 확대된다.')
    text=text.replace('v2 수정 재확인 완료.','최종 채택 이미지 경로까지 정렬했다.')
    text=text.replace('제작 후 병합한다.','39개 컷의 최종 선택 파일을 담았다.')
    text=text.replace('검수 후 작성한다.','필수 지적의 처리와 선택 개선 사항을 구분한다.')
    text += '\n## 실제 이미지 검수와 수정\n\n세 명이 각각 채택 PNG 39장을 실제로 열고 다른 두 명의 지적을 교차 검증했다. 초반·후반의 안내장 그래픽 불일치(C05 5장), 마술사를 무시하는 시선 경로(C04 1장), 소매 테이프의 접촉 방향(C02 1장)을 수정한 뒤 세 명 모두 실제 수정본을 다시 확인했다. C01 옆판 접기와 최종 파일 경로도 콘티에 반영했다.\n\nC03 엔딩의 턱 괸 자세와 K05/K06 소매의 가는 두 줄 차이는 선택 개선으로 남겼다. 인물 식별·소품 인계·역할 반전·제목 가독성을 막지 않아 유지하며, 완벽한 의상 일치를 주장하지 않는다. 원본·수정 전 이미지는 모두 버전으로 보존했다.\n'
    readme.write_text(text,encoding='utf-8')
    project=ROOT.parent.parent
    root_readme=project/'README.md'
    text=root_readme.read_text(encoding='utf-8')
    text=text.replace('**새 시나리오 5개와 컷별 첫 프레임 이미지**를 제작 중입니다.','**새 시나리오 5개와 컷별 첫 프레임 PNG 39장**을 완성했습니다.')
    text=text.replace('세 검수자의 독립·상호 교차 검토와 수정 재확인을 마친 5안·39컷 콘티로 실제 첫 프레임 이미지를 제작 중입니다.','[이미지·대사 열람본](storyboards/2026-10-17_b-comedy-reboot-v3/index.html)과 [전체 콘티](storyboards/2026-10-17_b-comedy-reboot-v3/STORYBOARDS.md)를 저장했습니다. 콘티와 실제 PNG 39장 모두 세 검수자의 독립·상호 교차 검토와 필수 수정 재확인을 마쳤습니다.')
    text=text.replace('2. 최신 제작 준비본은 [Flow 전달 패키지](flow_handoff/2026-10-15_v2/index.html)입니다. HTML은 저장소를 내려받아 브라우저에서 열면 됩니다.','2. 최신 신규 기획은 [B급 5안·39컷 이미지 열람본](storyboards/2026-10-17_b-comedy-reboot-v3/index.html)입니다. HTML은 저장소를 내려받아 브라우저에서 엽니다. [이전 Flow 전달 패키지](flow_handoff/2026-10-15_v2/index.html)는 이력이며 현재 실행 큐가 아닙니다.')
    root_readme.write_text(text,encoding='utf-8')
    resume=project/'RESUME_CODEX.txt'
    old=resume.read_text(encoding='utf-8')
    history=old[old.index('이하 이전 결과 — 보존용 이력'):]
    intro='''최신 범위 — 2026-10-17 신규 B급 5안·39컷 첫 프레임 완료 / 영상 생성 중단 유지

- 사용자가 기존 기획의 재미를 반려해 새 시나리오 5개를 요청했다. 기존 완성 C01 36초 v07은 그대로 보존(SHA b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c 확인). 새 폴더의 C01~C05는 신규 1~5안이며 기존 완성 영상과 다르다.
- 최신 결과: storyboards/2026-10-17_b-comedy-reboot-v3/. index.html에서 실제 이미지와 대사·다음 동작을 함께 보고, STORYBOARDS.md에서 전체 콘티를 읽는다. 최종 storyboards.json의 image_file과 scene_manifest.json이 동일 채택 PNG를 가리킨다.
- 신규1 ‘이 상품은 배송이 어렵습니다’31초8컷, 신규2 ‘성공 장면 되감기’29초7컷, 신규3 ‘우승 소감이 끝나지 않는 이유’31초8컷, 신규4 ‘관객이 사라지는 마술’30초8컷, 신규5 ‘작전명: 공개 발표’29초8컷. 참석 독려는4안, 행사 시작은2안, 과장된 연기는1안을 추천한다.
- 연구·독립 작가8후보·5안선정·콘티3인독립/교차/수정재확인 완료. 실제 독립 첫 프레임 PNG39장 생성, 세 검수자가 각각39장 실제열람·교차검증. C05초반포스터5장/C04마지막시선1장/C02테이프1장 국소수정 후 세 명 모두 재확인. review_summary.json과 image_revision_confirmation.json 기준.
- C03엔딩 턱괸자세와 K05/K06의 가는두줄 소매 편차는 선택개선으로 유지. 영상의 실제 움직임·음성·립싱크·관객웃음·Flow성공은 검증하지 않았다. 엔딩PNG는 글자없는 배경판, HTML행사명은 별도조판예시. 모든안 엔딩6초.
- 행사 개최·이름은확인, 세부일시/장소/참석방법/상금/성과수치는미확인으로 넣지않음. qrew원참고분석문·대표프레임·콘티·편집기록 확인범위이며 전체영상연속감상/실음원청취 주장금지.
- ‘동영상은 만들지 말고’에 따라 ai-flow 예약은 PAUSED. 이번 Flow업로드/영상생성/음원생성/렌더링/Flow크레딧사용0. 별도 사용자 영상제작요청 전에 예약재개/업로드/생성 금지. 이전 생성큐는 이력이다.
- 원자료·이전패키지·기존영상은 덮어쓰지 않았다. 수정전 이미지도 버전보존. 파일수/PNG무결성/생성원본SHA/타임라인/HTML링크/기존C01보존검사는 validation.json을 확인한다.

'''
    resume.write_text(intro+history,encoding='utf-8')
    print('Final storyboard/manifest paths and completion records aligned.')

if __name__=='__main__':main()
