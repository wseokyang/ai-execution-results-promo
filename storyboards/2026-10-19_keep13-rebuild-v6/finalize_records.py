"""Run only after actual-image independent/cross review and closure."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parent.parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 f=read('image_final_confirmation.json');assert f['status']=='all_required_closed'
 v=read('validation.json');assert v['status']=='passed' and v['retained_images']==17 and v['new_images']==26
 assert read('link_validation.json')['status']=='passed'
 d=read('storyboards.json');d['status']='complete_storyboards_and_selected_first_frames';put('storyboards.json',d)
 m=read('scene_manifest.json')
 for e in m['images']:e['review_status']='independent_actual_image_review_cross_check_and_required_closure_complete'
 put('scene_manifest.json',m)
 t=read('team_log.json')
 for s in t['stages']:
  s['status']='complete'
  if s['stage']=='actual_image_independent_cross_review':s.update(agents=['/root/v6_review_a','/root/v6_review_b','/root/v6_review_c'],artifacts=['image_review_A.json','image_review_B.json','image_review_C.json','image_cross_reviews.json','image_revision_disposition.json','image_final_confirmation.json'])
 put('team_log.json',t)
 put('progress.json',{'status':'complete','stage':'storyboards_and_actual_first_frames_delivered','new_selected_images':26,'retained_images':17,'total_selected_images':43,'video_audio_generation':False,'Flow':'not_used'})
 put('delivery_status.json',{'status':'complete','scope':'5 detailed storyboards and 43 actual first frames; C01/C03 retained unchanged, C02/C04/C05 rebuilt','selected_images':43,'new_selected_images':26,'retained_images':17,'old_completed_C01_film_preserved':True,'Flow_upload':False,'video_generation':False,'audio_generation':False,'audience_humor_validation':False,'creative_acceptance':'user retained C01/C03; new C02/C04/C05 awaiting user judgment, not claimed accepted'})
 put('review_summary.json',{'status':'required_storyboard_and_image_findings_closed','creative_changes':['초기 박수·항복 카드는 이전 반려 구조를 반복한다는 3인 검토로 폐기','C02 구출 오해 뒤 기사가 송풍기를 자청. C04 잠입 성공→놀이기구 노동→탈출이 퍼레이드. C05 파괴자가 기둥→구조를 기대한 사다리에서 이어폰 설치','신규 캐스트: 노년 여성 기술자/마른 콧수염 기사/삭발 여성 조수, 중장년 남성 3인, 빨간 특촬 괴수와 시설 작업자','C02 기계 정체 조기 노출 숨김·중반 4초 압축, C04 지도와 레버를 다루는 손 역할·시야·전달 정리, C05 크기·자세·응답 동기·시점 정리'], 'storyboard_review':'storyboard_final_confirmation.json','image_reviews':['image_review_A.json','image_review_B.json','image_review_C.json'],'cross_check':'image_cross_reviews.json','image_disposition':'image_revision_disposition.json','image_final':'image_final_confirmation.json','preservation':'preservation_manifest.json','reference_scope':'reference_diagnosis.json','limits':['정지 이미지와 계획 대사 검토','실제 영상 움직임·음성·립싱크·관객 반응 미검증','내부 점수와 합의는 재미나 사용자 승인의 증거가 아님','로컬 HTML 브라우저 자동 검수는 기존 제한을 존중해 수행하지 않았고 PNG·문서·정적 링크를 확인']})
 put('future_production_notes.json',{'scope':'후속 영상 기획용 메모. 현재 Flow 실행 금지','all':['행사명·자막은 후편집. 확정되지 않은 날짜·장소·신청·성과·상금 추가 금지','이미지는 동작 시작 프레임. 실제 음성 속도·대사·손동작·카메라·립싱크는 후속 영상에서 검증 필요'],'C02':['초반 용의 외피/낮은 창 정보 숨김을 지키고 K04에서 기계 구조 공개','기사의 자청 선택과 마지막 수동 송풍 대비를 유지'],'C04':['병사는 낮은 관측구로 역광 그림자만, 현대 축제 전체는 관객만 본다','아이 하차 완료 뒤 주행. 지도/연필/레버/페달의 손발 역할 분리'],'C05':['8m 괴수/5m 포치/접힌 머리 4.5m·귀 4.2m 기준으로 일관성','이어폰은 S07 최초 공개, 마지막 손짓은 들림 응답 시도','시작 전 안내→청취 준비→발표 시작 순서']})
 notes=read('future_production_notes.json');notes['image_review_cut_notes']={c['id']:{s['id']:s['postproduction_notes'] for s in c['shots'] if s.get('postproduction_notes')} for c in d['concepts'] if c['id'] in ['C02','C04','C05']};put('future_production_notes.json',notes)
 (R/'README.md').write_text('''# V6 — 1·3안 유지, 새 2·4·5안

[전체 이미지 콘티](index.html) · [컷 표](STORYBOARDS.md) · [이미지·정확한 프롬프트](scene_manifest.json)

- C01 「성공 자세 교정원」 34초 / V5 그대로
- C02 「공주를 구하지 마세요」 38초 / 새 시나리오·9장
- C03 「환경까지 가져왔습니다」 42초 / V5 그대로
- C04 「잠입 성공」 42초 / 새 시나리오·9장
- C05 「괴수는 퇴근할 수 없다」 38초 / 새 시나리오·8장

새 첫 프레임 26장과 유지한 17장, 총 43장입니다. 각 PNG는 내장 image_gen 생성 원본 바이트를 복사했습니다. 씬·컷별 실제 경로·정확한 프롬프트·참조·SHA·검수는 manifest에 기록했습니다. 수정 이전 버전은 별도 파일로 남겼습니다.

자료 재분석, 두 작가 독립 발상, 카드 게이트와 전면 교체, 3인 전체 콘티 독립·교차·수정 확인, 3인 실제 이미지 독립·교차·필수 지적 처리를 거쳤습니다. 사용자에게 새 세 안의 재미가 수용되었다고 기록하지 않습니다.

기존 완성 C01 36초 v07 동영상과 기존 패키지는 보존했습니다. 이번에 Flow 업로드·동영상·음원 생성은 하지 않았습니다. 원본 행사 자료와 qrew 자산도 변경하지 않았습니다.

[검토 요약](review_summary.json) · [보존 검증](preservation_manifest.json) · [레퍼런스 확인 범위](reference_diagnosis.json) · [검증 결과](validation.json)
''',encoding='utf-8')
 latest='''[2026-10-19 V6 최신 완료 — C01·C03 유지 / C02·C04·C05 새 콘티·이미지]
작업: storyboards/2026-10-19_keep13-rebuild-v6/ (index.html, STORYBOARDS.md, scene_manifest.json)
V5 C01 성공 자세 교정원 34초와 C03 환경까지 가져왔습니다 42초는 콘티 객체·채택17PNG 원본 바이트 그대로 보존. 기존 완성 C01 36초 v07 영화도 SHA 일치.
새 C02 공주를 구하지 마세요 38초9컷, C04 잠입 성공 42초9컷, C05 괴수는 퇴근할 수 없다 38초8컷. 신규 실제 첫 프레임26장 + 유지17장 =43장. 캐스팅은 노년 공주/삭발 조수/마른 콧수염 기사, 장년 남성3인, 빨간 특촬 괴수/장년 시설작업자로 구별.
초기 박수/항복 카드는 독립 검토에서 반려하고 전면 교체했다. 콘티·실제 이미지3인독립/교차/필수수정확인 완료. 상세 기록은 review_summary.json. 실제 동작·음성·립싱크·관객 반응 미검증; 새3안의 사용자 창작 수용을 주장하지 않는다.
Windows 검토본: C:/Users/wseok/.codex/visualizations/2026/10/19/01a13daf-3732-7b90-99a8-92c605090d35/B_comedy_keep13_rebuild_v6/index.html
동일 위치의 B_comedy_keep13_rebuild_v6_full_package.zip. 패키지 검증 파일 별도.
Flow·동영상·음원 생성0. ai-flow PAUSED 유지. 이번 사용자 지시는 시나리오와 첫 프레임만이며 이전 자동생성 큐를 재개하지 않는다.

'''
 p=ROOT/'RESUME_CODEX.txt';old=p.read_bytes()
 if not old.startswith(latest.encode('utf-8')):p.write_bytes(latest.encode('utf-8')+old)
 p=ROOT/'README.md';old=p.read_bytes();header='''## 최신: 2026-10-19 V6

사용자가 유지한 V5의 1·3안을 그대로 두고, 2·4·5안의 시나리오와 첫 프레임을 새로 만들었습니다. 신규 26장 + 보존 17장. 영상·음원·Flow 생성 없음.

[V6 전체 컷 표](storyboards/2026-10-19_keep13-rebuild-v6/STORYBOARDS.md) · [V6 이미지 콘티](storyboards/2026-10-19_keep13-rebuild-v6/index.html) · [검토 요약](storyboards/2026-10-19_keep13-rebuild-v6/review_summary.json)

'''
 if not old.startswith(header.encode('utf-8')):p.write_bytes(header.encode('utf-8')+old)
 p=ROOT/'team/brief.toml';old=p.read_bytes()
 section='''
[creative_direction_2026_10_19_keep_c01_c03]
user_feedback = "V5 1·3안 유지. 2·4·5안은 돌고래유괴단 감성 부족으로 재작성, 등장인물 외형 다양화."
retained = "V5 C01·C03 콘티와 채택 PNG17장, 기존 C01 36초 v07 영화 SHA 보존."
new_run = "storyboards/2026-10-19_keep13-rebuild-v6"
delivery = "C02 공주38초9컷 / C04 목마42초9컷 / C05 괴수38초8컷, 신규26장. 전체5안43장."
creative_status = "콘티·실제첫프레임 제작과3인검토완료. 신규3안 사용자창작수용·관객재미는미확인. 초기박수/항복안은카드게이트에서폐기."
scope = "Flow·동영상·음원 생성 금지. ai-flow PAUSED. 기존기획·패키지·원자료덮어쓰지않음."
'''
 if b'[creative_direction_2026_10_19_keep_c01_c03]' not in old:p.write_bytes(old+section.encode('utf-8'))
 print('Final records and handoff updated after actual image review closure.')
if __name__=='__main__':main()
