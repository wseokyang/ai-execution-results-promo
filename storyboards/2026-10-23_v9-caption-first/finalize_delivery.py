from pathlib import Path
import json, shutil, hashlib, subprocess, sys
R=Path(__file__).resolve().parent
ROOT=R.parents[1]
REL='storyboards/'+R.name
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write_crlf(p,s):p.write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
ir=read(R/'image_review.json')
assert all(x!='pending' for x in ir['final_reconfirmation'].values())
ir['status']='passed_after_independent_cross_review_and_reconfirmation'
for issue in ir['issues']:
    if issue['status']=='resolved_pending_final_checks':issue['status']='resolved'
put(R/'image_review.json',ir)
v=read(R/'review_summary.json')
v['image_status']=ir['status'];v['image_review']=ir;v['image_review_file']='image_review.json'
put(R/'review_summary.json',v)
d=read(R/'storyboards.json')
d['status']='44 new first-frame images and caption-first storyboard reviewed; no Flow execution'
for u in d['generation_units']:
    u['status']='first-frame image reviewed; video generation not executed in this run'
    if u['concept_id']=='C03':u['video_policy']='Reuse existing C03 originals/edit first; this new PNG does not request regeneration.'
    if u['id']=='C05_K02B':u['video_policy']='Planning first-frame candidate. After actual K02A is accepted, use its actual end frame for continuation.'
put(R/'storyboards.json',d)
m=read(R/'scene_manifest.json');m['status']='44 selected new images independently reviewed, cross-checked and corrected'
m['generated_png_files_including_superseded']=len(list((R/'images').rglob('*.png')))
for e in m['images']:
    e['review_status']='reviewed_after_three_independent_reviews_and_cross_check'
    e['review_record']='image_review.json'
put(R/'scene_manifest.json',m)
subprocess.run([sys.executable,'-X','utf8',str(R/'build_delivery.py')],check=True)
validation=read(R/'validation.json')
validation['browser_render_qa']=ir['pd_actual_preview']
validation['independent_image_review']='A/B/C + cross + correction + A/B/C re-confirmation completed'
validation['selected_pngs']=44
validation['preserved_generated_pngs']=m['generated_png_files_including_superseded']
put(R/'validation.json',validation)

notes='''# 제작 연결 메모 · V9

이번 납품은 44장 시작 이미지와 화면+자막 콘티입니다. Flow 업로드·영상 생성·크레딧 사용은 0입니다. 기존 완성 C01과 C03 v03·원본은 보존했습니다.

| 안 | 시작 이미지 | 편집 컷 | 계획 길이 |
|---|---:|---:|---:|
| C01 성공 자세 교정원 | 9 | 9 | 39초 |
| C02 검은 점을 잡아라 | 9 | 9 | 39초 |
| C03 환경까지 가져왔습니다 | 8 | 8 | 44.75초 |
| C04 목마는 식사 중입니다 | 9 | 9 | 39초 |
| C05 괴수는 퇴근할 수 없다 | 9 | 8 | 43초 |

C05 K02를 기둥 빼기 A / 몸 접기 B로 나눠 43개 편집 컷에 44개 시작 상태를 준비했습니다. 실제 영상에서는 A의 채택된 끝 프레임을 B에 우선 사용합니다. 각각 8초가 생성된다고 모든 8초를 편집에 쓰는 계획은 아닙니다.

사용자가 언급한 5계정·25회는 다음 영상 제작의 예상 예산입니다. 이번에는 로그인·잔액·모델 비용을 확인하지 않았습니다. 전체44개를 25회로 무조건 완성한다고 약속하지 않습니다. 기존 C03 8컷은 재사용부터 검토하므로 새 이미지8장이 새 영상8개 지시는 아닙니다. 음성 전용 예비3개는 필수 생성 큐에서 제외합니다.

## 후편집할 것

- 전체: Q-AI Fair 및 모든 자막은 별도 층. caption_cues의 시간과 box 좌표를 사용하며 PNG 원본에는 굽지 않습니다. BGM·효과음은 보조이고 대사 청취가 필수 정보가 되지 않습니다.
- C01: K04는 모니터 내부용 독립 동작 영상입니다. 모니터 면의 후반 합성이 필요합니다. 포스터와 원본 자세가 연결돼야 합니다.
- C02: 모니터의 AI 후보 → 사람이 원본 겹침 → 청소/재촬영 → 수갑 가림을 구분합니다. K07 채택 순간을 추출해 작은 전화 화면과 K08/K09 인화사진에 같은 순간으로 합성합니다. 현재 작은 전화 속 손 자세 차이는 이 후반 작업 항목으로 남겼습니다.
- C03: 노트북 결과와 회색/주황 파일 안쪽 기록을 합성합니다. 라벨은 ‘잘됐던 작업 기록’/‘시행착오 기록’. 기존 v03의 ‘내 작업 기록’ 라벨은 추후 별도 편집 버전에서 바꿉니다. 장갑 탈착 전체 재생성을 필수로 삼지 않습니다.
- C04: 신고서 ‘내부 탑승자 없음’, 첨부 ‘식사·물·수저 요청’, ‘AI 문서 대조 · 확인 필요’를 정확히 합성합니다. 병사 창문 공개 전에는 그릇과 손을 미리 보이지 않습니다.
- C05: K07은 S07_v3 사용. 주둥이 왼쪽·보이는 귀 오른쪽·같은 S목을 유지합니다. K08 몸개그35–38초 뒤 제목38–42.8초. 하단 제목판은 바닥 일부를 덮어도 되지만 지붕 지지 손·얼굴·이어컵을 보존합니다.

추천: 참석 독려는 C03(기록을 들고 본인이 찾아가는 선택), 현장 시작은 C04(밥그릇 반전 뒤 첫 사례 시작). C05는 큰 화면에서 괴수의 크기 대비가 잘 보이는 도입에 적합합니다.

실제 동영상에서 손·소품 움직임과 자막 읽기 속도를 다시 검수해야 합니다. 정지 콘티 검수를 영상 생성 성공이나 관객 반응 검증으로 해석하지 않습니다. 일정·장소·신청 링크·성과 수치는 미확인입니다.
'''
(R/'PRODUCTION_NOTES.md').write_text(notes,encoding='utf-8')
(R/'README.md').write_text('''# Q-AI Fair · 화면+자막 V9

**5안의 시작 이미지 44장을 전부 새로 생성했습니다.** 수정 전 생성물까지 PNG 55장을 보존하고, 실제 채택44장은 scene_manifest에 구분했습니다. 세 검수자가 5안 전체를 독립 검토·교차 검증하고 이미지/배치 수정본을 재확인했습니다.

- [전체 44장 이미지 콘티 보기](ALL_IMAGES.md)
- [자막 버튼이 있는 HTML 미리보기](index.html) — 폴더를 내려받아 열기
- [시간·화면·자막·음향 컷 표](STORYBOARDS.md)
- [컷별 PNG·정확한 생성 프롬프트·참조·해시](scene_manifest.json)
- [실제 이미지 검수](image_review.json) · [전체 검수](review_summary.json)
- [제작 연결·후편집 사항](PRODUCTION_NOTES.md) · [파일/보존 검증](validation.json)

기존 C01 완성 영상과 C03 v03·원본, V8 기획/이미지는 보존했습니다. 이번 작업은 Flow 실행·새 영상·새 음원·크레딧 사용이 없습니다.
''',encoding='utf-8')

for source,dest in [('README.md','README_before_v9.md'),('콘티_바로보기.md','콘티_바로보기_V8.md')]:
    if not (ROOT/dest).exists():shutil.copyfile(ROOT/source,ROOT/dest)
guide=(R/'ALL_IMAGES.md').read_text(encoding='utf-8')
guide=guide.replace('](images/',']('+REL+'/images/')
for f in ['index.html','STORYBOARDS.md','scene_manifest.json','review_summary.json']:
    guide=guide.replace(']('+f+')',']('+REL+'/'+f+')')
guide+='\n\n[제작 연결·후편집 메모]('+REL+'/PRODUCTION_NOTES.md) · [이전 V8 전체 이미지](콘티_바로보기_V8.md)\n'
write_crlf(ROOT/'콘티_바로보기.md',guide)
readme=f'''# Q-AI Fair · 홍보영상

최신 콘티는 **화면+자막 V9**입니다. 소음이 있는 상영 환경에 맞춰 승인된 5안의 핵심 정보가 음성 없이 전달되도록 보완하고 **시작 이미지44장(9·9·8·9·9)을 새로 생성·검수**했습니다. 이전 완성 영상과 원본은 보존했습니다.

## [전체 44장 이미지 콘티 바로보기 →](콘티_바로보기.md)

| 찾는 자료 | 바로가기 |
|---|---|
| 모든 이미지와 자막·다음 동작 | [V9 전체 이미지]({REL}/ALL_IMAGES.md) |
| 시간·대사 방침·음악·전환 전체 컷 표 | [V9 컷 표]({REL}/STORYBOARDS.md) |
| 자막 배치 버튼이 있는 HTML | [V9 HTML]({REL}/index.html) |
| 실제44개 PNG와 정확한 생성 기록 | [씬 매핑]({REL}/scene_manifest.json) · [이미지 폴더]({REL}/images/) |
| 검수·후속 합성 항목 | [3인 검수]({REL}/image_review.json) · [제작 메모]({REL}/PRODUCTION_NOTES.md) |
| 보존한 기존 C03 44.75초 검토 편집 | [C03 v03 MP4](storyboards/2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4) |
| 이전에 완성한 1번 영상 | [C01 36초 최종 MP4](storyboards/2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4) |
| 이전 기획과 작업 이력 | [V8 전체 이미지](콘티_바로보기_V8.md) · [이전 README](README_before_v9.md) |

V9은 시작 이미지와 콘티 납품입니다. Flow 업로드·영상 생성·크레딧 사용은0입니다. 기존 C03 영상은 재사용을 우선 검토하고, 새 C03 이미지8장을 영상8컷 재생성 요청으로 보지 않습니다. C05 K02A/B를 분리해 43개 편집컷·44개 시작 상태입니다.

HTML은 이미지 폴더와 함께 내려받아 열면 자막 배치를 볼 수 있습니다. GitHub에서 바로 읽으려면 **전체 이미지 콘티** 링크를 이용하세요. 이 저장소는 비공개로 유지합니다. 정확한 행사 일정·장소·신청 방법은 미확인입니다.
'''
write_crlf(ROOT/'README.md',readme)
resume='''[2026-10-23 Q-AI Fair 화면+자막 V9 — 새 시작 이미지44장/3인 교차검수/Flow0]
최신 사용자: 시끄러운 환경이므로 화면+자막으로 내용 전달, BGM·효과음 보조 허용. 행사명은 Q-AI Fair. 5계정으로25컷 예상하지만 이번에는 우선 모든 컷 시작 이미지를 다시 생성해 보고하라고 요청. Flow업로드/생성/잔액확인/계정전환/크레딧사용/예약재개/영상·음원렌더 없음. 이전 생성 승인을 근거로 이번 이미지 검토 전에 Flow를 자동 실행하지 않는다.
storyboards/2026-10-23_v9-caption-first 가 최신 제작 명세. 기존 승인5안의 이야기·캐스팅 유지, 음성의 필수정보를 화면+자막으로 이동. C01성공자세교정원9장39초/C02검은점을잡아라9장39초/C03환경까지가져왔습니다8장44.75초/C04목마는식사중입니다9장39초/C05괴수는퇴근할수없다9장43초. 43편집컷/44시작상태. C05K02A기둥빼기/B몸접기; 실제영상B는 채택A끝프레임 우선.
내장image_gen으로 전44선택이미지 새 생성. 수정전포함55PNG 원본바이트보존,정확프롬프트/참조/해시/파일 scene_manifest 및artist기록. 이미지 원본에 자막·행사명 굽지 않음. 기존V8기획/PNG와완성legacyC01/C03v03불변해시확인. 새C03이미지8장은 기존영상8개 재생성 지시 아님. 기존C03부분편집·자막변경으로 재사용 우선.
텍스트3인독립→교차→수정→3인재확인, 실제44이미지도동일절차완료. C05K07은 S07_v3 채택(주둥이왼쪽/귀오른쪽/같은S목/이어컵미장착/양손지붕지지),구형S07/S07v2보존.40개자막큐 box명시. C03K06상단왼쪽, C04K01상단목재, C05K08몸개그35–38후하단제목38–42.8. 행사명5cqw/설명3cqw. 실제검수범위와브라우저확인은image_review에구분.
후속필요: C01모니터합성,C02사진/모니터정확비교와K07실제촬영순간을휴대폰/인화면에합성,C03파일안쪽라벨‘잘됐던작업기록’/‘시행착오기록’및기존v03구라벨교체,C04정확문서UI. 소리는필수정보아님,음성전용예비3개는필수큐제외. 실제영상의동작·자막읽기·현장가독성은이미지검수로완료주장금지.
사용자보기: 루트 콘티_바로보기.md 또는 run/ALL_IMAGES.md(전체44장), run/index.html(자막버튼), STORYBOARDS.md,PRODUCTION_NOTES.md. 기존V8안내는콘티_바로보기_V8.md/README_before_v9.md보존. Git동기화는실제remote확인후보고.
'''
p=ROOT/'RESUME_CODEX.txt';old=p.read_text(encoding='utf-8-sig')
if not old.startswith('[2026-10-23 Q-AI Fair 화면+자막 V9'):
    write_crlf(p,resume+'\n'+old)
p=ROOT/'team/brief.toml';s=p.read_text(encoding='utf-8-sig')
s=s.replace('진행 중: 콘티 검수 및 이미지 재생성 전. 완료 여부는 이 run의 최종 validation/review 기록 확인.','완료: 새 시작 이미지44장, 텍스트/실제이미지3인독립·교차·수정재확인. Flow0. 후속영상의움직임/자막합성은별도검수.')
write_crlf(p,s)
print('Final image package and resume documentation saved.')
