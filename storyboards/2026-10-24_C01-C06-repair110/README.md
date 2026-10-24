# 1~6번 동작 보완 · 110크레딧

2026-10-24 시작, 10-25 저장·검수. **110 전부 사용, 로그인 5계정 모두 실제 잔액 0 확인.** Lite10 × 성공11개. 보안 실패2회는 차감0이며 사용자 새로고침 뒤 한 번씩 정상 요청했다. 11개 원본 중 **5개는 선택 구간 채택, 6개는 보류**다.

원본은 모두 8초·1280×720·24fps이며 재인코딩하지 않았다. 다운로드/보관 SHA 일치, 전체 영상·오디오 디코딩 통과. 원본 음성은 필수 전달에 쓰지 않으며 실제 청취 검증은 하지 않았다.

- [5번 v06 전체 편집본](../2026-10-25_C05-jack-edit-v06/C05_Q-AI_Fair_causal_edit_v06.mp4): 51.25초, 흐릿한 확대 컷을 선명한 실제 잭 운반으로 교체.
- [6번 v06 전체 편집본](../2026-10-25_C06-impact-edit-v06/C06_Q-AI_Fair_edit_v06.mp4): 48.75초, 첫 타격만 반영하고 기존 효과음을 실제 손 접촉 6.125초에 이동.
- [1번 퇴장→낙하 연결 검토](edit_probes/C01_exit_to_fall.mp4) · [4번 세 인물→숟가락 연결 검토](edit_probes/C04_windows_to_spoon.mp4)

1·2·4번의 정확한 화면 합성·자막을 포함한 최종 편집은 남아 있다. 3번은 기존 caption-v04를 유지했다. 여섯 편 모두 완성본이라는 뜻은 아니다.

| 컷 | 원본과 검토 프레임 | 판정 | 이유 |
|---|---|---|---|
| C04_K08_detail take01 | [MP4 원본](C04_K08_detail_take01.mp4) · [프레임](C04_K08_detail_take01_contact.jpg) | 보류 | 중앙 창에 두 명, 총 네 인물과 그릇. 전체 공개 구간 미채택. |
| C01_K07 take02 | [MP4 원본](C01_K07_take02.mp4) · [프레임](C01_K07_take02_contact.jpg) | 보류 | 수강생이 무릎만 꿇고 눕지 않음. 코치 자세도 달라짐. |
| C04_K09 take02 | [MP4 원본](C04_K09_take02.mp4) · [프레임](C04_K09_take02_contact.jpg) | 채택 [0.5, 6]초 | 장군이 숟가락 한 개를 꺼냄. 왼손이 같은 숟가락에 닿는 동작은 수용. |
| C01_K05 take03 | [MP4 원본](C01_K05_take03.mp4) · [프레임](C01_K05_take03_contact.jpg) | 채택 [2.5, 7.25]초 | 두 사람이 실제 왼쪽 문으로 퇴장. 다음 착석·낙하는 시간 생략. |
| C01_K06_pose take01 | [MP4 원본](C01_K06_pose_take01.mp4) · [프레임](C01_K06_pose_take01_contact.jpg) | 보류 | 누운 자세를 유지하지 않고 일어나 무릎 꿇음. |
| C02_K05_release take01 | [MP4 원본](C02_K05_release_take01.mp4) · [프레임](C02_K05_release_take01_contact.jpg) | 보류 | 두 고리·손 놓기는 확보했으나 아래 고리가 렌즈 아래로 내려감. 기존 K06과 사슬 길이·고리 위치 불일치. |
| C05_K04_jack_detail take01 | [MP4 원본](C05_K04_jack_detail_take01.mp4) · [프레임](C05_K04_jack_detail_take01_contact.jpg) | 채택 [1.5, 3]초 | 선명한 잭의 왼쪽 운반. 정지·상승·하중 이전은 아님. |
| C04_K01_insert take01 | [MP4 원본](C04_K01_insert_take01.mp4) · [프레임](C04_K01_insert_take01_contact.jpg) | 보류 | 자기 종이는 왼손에 남고, 빈 오른손이 봉투에서 다른 종이를 꺼냄. 투입 미확보. |
| C01_K07_recline take01 | [MP4 원본](C01_K07_recline_take01.mp4) · [프레임](C01_K07_recline_take01_contact.jpg) | 보류 | 등을 내리지 않고 팔꿈치로 기대며 코치도 자세를 풂. 정확 모방 완성 미확보. |
| C04_K08_three_visible take01 | [MP4 원본](C04_K08_three_visible_take01.mp4) · [프레임](C04_K08_three_visible_take01_contact.jpg) | 채택 [2, 3.5]초 | 세 사람·그릇 세 개·숟가락 세 개 유지. 식사 유사 동작 제외. 창은 처음부터 열려 있음. |
| C06_K02_impact take01 | [MP4 원본](C06_K02_impact_take01.mp4) · [프레임](C06_K02_impact_take01_contact.jpg) | 채택 [0.75, 2.25]초 | 첫 책상 접촉만 사용, 두 번째 타격 제외. 진동·종이 튐 미확보. |

[전체 원본 재생 목록](originals.html) · [생성 로그](generation_log.json) · [잔액 장부](budget_ledger.json) · [검수·교차 처리](review_summary.json) · [입력 이미지 대응](scene_manifest.json)

기존 자세/수갑/봉투의 미해결 동작은 새 원본을 억지로 채택하지 않고 종전의 수용 구간과 시간 생략을 유지한다. 창 공개의 열림 자체, 잭의 상승·하중 이전, 괴수 완전 회전, 책상 진동·종이 튐을 추가 확보했다고 주장하지 않는다. 세 검수자의 실제 표본과 연결 검토 및 기술 검증이며, 전체 실시간 재생·실청취·현장 소음 테스트·관객 반응 검증은 아니다.
