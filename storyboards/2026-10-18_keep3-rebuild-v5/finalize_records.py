from pathlib import Path
import json
R=Path(__file__).resolve().parent;ROOT=R.parent.parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def dump(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 final=read('image_final_confirmation.json')
 assert set(final['reviewers'])=={'A','B','C'}
 assert all(x['required_unresolved']==0 for x in final['reviewers'].values())
 d=read('storyboards.json');assert next(c for c in d['concepts'] if c['id']=='C03')==read('retained_concept_C03.json')
 d['status']='complete_storyboards_and_selected_first_frames'
 d['notes']=[
  'C03는 V4 전체 객체와 선택8장의 바이트를 유지. 새 C01/C02/C04/C05만 재기획/생성했다. 기존 완성 C01 36초 v07은 별도 보존.',
  '시간/컷: C01 34초9컷, C02 33초9컷, 유지 C03 42초8컷, C04 35초9컷, C05 31초8컷. 새4안 엔딩6초, C03 엔딩5초.',
  '최종 선택경로는 image_file과 scene_manifest.json이 같다. 실제 이미지별 원본·참조·정확프롬프트·검수는 각 manifest 참조. 수정전 PNG도 보존했다.',
  'C02 최종 S08_v6/S09_v3: 관객 등너머 축, 노트북 테이블왼끝/스타시선틈, 팬4명표시면앞쪽. C05 최종 S06_v2/S07_v2: 후경중복가방제거. C04좌측힌지PD수용.',
  '행사 개최/이름과 AI 실행과제·활용경험공유 목적은 원자료 확인. 정확일시·장소·참석/추천/신청방법·실제발표자/성과/상금은 미확인.',
  '인물·소품·사건은 허구. 16:9와사내시청은제작가정. 실제직원이나제품로고를재현하지않음.',
  '자료조사·두작가독립발상·콘셉트및전체콘티3인독립/교차검토·실제이미지3인독립/교차/수정확인완료. 이미지수·내부합의·주관점수는관객재미나사용자승인증거가아님.',
  '정지이미지는후속동작시작프레임. 영상움직임·음성·립싱크·최종자막·관객반응은미검증. Flow/영상/음원생성은하지않았다. 상세후속메모는 future_production_notes.json.'
 ]
 dump('storyboards.json',d)
 p=read('progress.json');p.update(status='complete',stage='storyboards_and_actual_images_delivered',new_images=35,retained_images=8,video_generation=False,flow_upload=False);dump('progress.json',p)
 t=read('team_log.json');t['images']='35 new selected first frames + 8 unchanged C03; correction sources preserved';t['image_review']='3 independent actual-pixel reviews + peer cross-check + concrete revision confirmation complete';dump('team_log.json',t)
 dump('delivery_status.json',{'status':'complete','scope':'4 rebuilt scenarios and actual per-cut first frames, C03 preserved','concepts':5,'selected_images':43,'new_images':35,'retained_images':8,'new_video':False,'new_audio':False,'flow_upload':False,'credits_used':0,'automation':'PAUSED retained','audience_or_user_creative_approval':False})
 p=ROOT/'README.md';s=p.read_text(encoding='utf-8-sig');start=s.index('## 진행 중 · 3안 유지, 나머지 네 안 교체 V5');end=s.index('## 이전 V4',start)
 new='''## 최신 · 3안 유지, 나머지 네 안 교체 V5

사용자가 유지한 V4 C03 「환경까지 가져왔습니다」의 콘티와 PNG 8장은 그대로 보존하고, C01/C02/C04/C05의 시나리오와 컷별 첫 프레임 35장을 새로 만들었습니다. [이미지·대사 열람본](storyboards/2026-10-18_keep3-rebuild-v5/index.html), [전체 컷 표](storyboards/2026-10-18_keep3-rebuild-v5/STORYBOARDS.md), [검토·수정 기록](storyboards/2026-10-18_keep3-rebuild-v5/review_summary.json)을 확인하세요.

새 안은 **성공 자세 교정원(34초), 경호 대상이 바뀌었습니다(33초), 양보의 자동화(35초), 아빠가 벌써 온다(31초)**입니다. 세 검수자가 실제 이미지를 독립·교차 검토했습니다. 이 검토는 관객 웃음 반응이나 사용자 창작 승인의 증거가 아닙니다. 기존 완성 C01 36초 v07은 그대로이며, **동영상·음원 생성과 Flow 업로드는 하지 않았습니다. ai-flow PAUSED 유지.**

'''
 p.write_text(s[:start]+new+s[end:],encoding='utf-8')
 p=ROOT/'RESUME_CODEX.txt';s=p.read_text(encoding='utf-8-sig');end=s.index('이하 V4 제작 이력')
 head='''완료 — 2026-10-18 V5: V4 C03 유지, 나머지 네 안 교체 및 실제 첫 프레임

- 최신 사용자 요청: V4 3번만 유지, 나머지 네 안은 재미와 반전이 부족해 전면 재작성. 기존 V4/C01/C02/C04/C05 창작 반려 이력은 유지한다. 내부 검수 완료를 재미나 사용자 취향 승인의 증거로 제시하지 않는다.
- 최신 결과: storyboards/2026-10-18_keep3-rebuild-v5/. index.html 이미지·대사 열람본, STORYBOARDS.md 전체 컷 표, storyboards.json 최종 콘티, scene_manifest.json 선택43장/정확프롬프트/원본·참조 경로. README.md와 review_summary.json을 먼저 읽는다.
- 새 C01 성공 자세 교정원 34초9컷 / C02 경호 대상이 바뀌었습니다 33초9컷 / 유지 C03 환경까지 가져왔습니다 42초8컷 / 새 C04 양보의 자동화 35초9컷 / 새 C05 아빠가 벌써 온다 31초8컷. 새 이미지35장, 유지8장. 수정 전 생성 원본도 보존했으므로 selected 경로를 따른다.
- C03 전체 객체와 채택8장 바이트는 V4와 동일. 기존 완성 C01 36초v07 SHA b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c 유지. 원자료/이전패키지 덮어쓰기 없음.
- 연구·두 작가 독립 발상·콘셉트 검토·전체 콘티·세 명 독립/교차 수정 확인 완료. 실제 이미지 검토 범위/개별 경로/수정 처리/수용 차이는 image_review_A/B/C.json, image_cross_reviews.json, image_revision_disposition.json, image_final_confirmation.json에 기록. 실제 움직임·음성·립싱크·관객 반응은 미검증.
- C04는 첫 생성의 좌측 힌지로 PD 변경 수용. 이후 문 제거/전경 오른쪽 이동/빈 통로를 유지한다. C05는 운반·악기 수납·가방 올리기 준비를 점프컷으로 생략하며 개의 가방 예고시선을 추가하지 않는다. 향후 제작 메모는 review_summary.json을 읽는다.
- 동영상·음원 생성, Flow 업로드, 크레딧 사용0. ai-flow PAUSED 유지. 별도 영상제작 요청 전에 재개/생성 금지.
- 로컬 배포: C:/Users/wseok/.codex/visualizations/2026/10/18/01a13daf-3732-7b90-99a8-92c605090d35/B_comedy_keep3_rebuild_v5/index.html. 전체 ZIP은 같은 상위 폴더 B_comedy_keep3_rebuild_v5_full_package.zip. Git 최신 반영은 git log/remote로 확인.
- HTML 브라우저 자동 렌더 검사는 file 프로토콜 정책 차단으로 미실행; 우회하지 않음. 실제 PNG 열람·정적 링크·타임라인·보존 해시·패키지 복사 해시/ZIP CRC로 검증.

'''
 p.write_text(head+s[end:],encoding='utf-8')
 p=ROOT/'team/brief.toml';s=p.read_text(encoding='utf-8-sig')
 if 'delivery_status_v5 =' not in s:s+='\ndelivery_status_v5 = "콘티·실제 첫 프레임 완료. 35장 신규+8장 C03 유지. 실제 관객 반응·사용자 창작 승인은 미확인. Flow/영상/음원 금지 유지."\n'
 p.write_text(s,encoding='utf-8')
 print('final records updated')
if __name__=='__main__':main()
