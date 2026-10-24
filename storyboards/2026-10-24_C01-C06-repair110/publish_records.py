from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent;SB=R.parent;ROOT=SB.parent
def dump(p,v):p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def write(p,s):p.write_bytes((s.rstrip()+'\n').encode())
C5=SB/'2026-10-25_C05-jack-edit-v06';C6=SB/'2026-10-25_C06-impact-edit-v06'
p=C6/'edit_manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
if 'previous_version_v05_change' not in m:
    m['previous_version_v05_change']={k:m.pop(k) for k in ['changed_interval_seconds','changed_frame_indices_inclusive','replacement_method'] if k in m}
m.update(changed_interval_seconds=[5,6.5],changed_frame_indices_inclusive=[120,155],replacement_method='Replace36 picture frames with original C06_K02_impact_take01 source0.75–2.25s; established audio reconstructed with desk cue shifted to6.125s.',status='A/B/C final visual sample and cue-record recheck accepted; listening and continuous playback not verified')
dump(p,m)
p=C5/'edit_manifest.json';m=json.loads(p.read_text(encoding='utf-8'));m['review']='A/B/C final join samples accepted; source limitations retained';dump(p,m)
p=R/'review_summary.json';m=json.loads(p.read_text(encoding='utf-8'));m['C06_final_render_recheck']={r:'Actual render/contact and caption samples accepted. Cue record6.125s agrees with contact. Listening and realtime playback not verified. Inherited v05 metadata moved into previous_version_v05_change.' for r in ['A','B','C']};m['metadata_correction']='All3 identified inherited v05 changed_interval/replacement_method. PD moved them into explicit previous-version history and set current5–6.5s/frames120–155.';dump(p,m)
for out,film,change in [(C5,'C05','26.25–27.75초의 흐릿한 확대를 실제1280×720 잭 운반으로 교체. 길이·자막·기존AAC패킷 불변.'),(C6,'C06','5–6.5초에 실제 첫 타격을 교체하고 기존 책상 효과음만5.55→6.125초 이동. 전체길이·자막 유지.')]:
    review=dict(reviewers=['A','B','C'],scope='Actual rendered frame samples and join boundaries; no continuous playback, listening or venue test',result='VISUAL_SAMPLE_ACCEPTED',change=change,source_review='../2026-10-24_C01-C06-repair110/review_summary.json',audio_listening_verified=False)
    dump(out/'review_summary.json',review)
    write(out/'README.md',f'# {film} 최신 v06 편집 검토본\n\n{change}\n\n[MP4 보기]({"C05_Q-AI_Fair_causal_edit_v06.mp4" if film=="C05" else "C06_Q-AI_Fair_edit_v06.mp4"}) · [기술 검증](technical_validation.json) · [편집 기록](edit_manifest.json) · [검수](review_summary.json)\n\n세 검수자의 실제 표본·경계 검토와 전체 디코딩을 마쳤다. 연속 재생·실청취·현장소음 테스트·사용자최종승인은 아직 아니다. 기존 원본과 모든 이전 편집본은 보존했다.\n')
newdoc='''# 1~6번 보완 결과 · 110크레딧 전부 사용

2026-10-25. **남은40까지 모두 사용했고, 로그인된 5계정의 실제 잔액은 전부0입니다.** 이번 보완 전체는 Lite10×11개 원본이며, 보안 실패2회는 차감0입니다. 구매·구독변경·유료업스케일은 없습니다.

| 작품 | 검토·보완 결과 | 바로 보기 |
|---|---|---|
| 1번 | 두 사람의 실제 문밖 퇴장 확보. 자세 완성 재시도는 기대기/자세 변경으로 보류하고 기존 선택 유지. | [퇴장→낙하 연결 검토본](storyboards/2026-10-24_C01-C06-repair110/edit_probes/C01_exit_to_fall.mp4) |
| 2번 | 수갑 손 놓기는 확보했으나 고리 위치가 기존 컷과 달라 신규 보류. 기존 선택 유지. | [보류 원본과 이유](storyboards/2026-10-24_C01-C06-repair110/README.md) |
| 3번 | 현재 자막 v04에서 추가 생성이 필요한 핵심 결함을 찾지 않아 유지. | [현재 편집본](storyboards/2026-10-24_C03-caption-v04/C03_Q-AI_Fair_edit_v04.mp4) |
| 4번 | 정확히 세 사람의 그릇 내밀기, 장군의 숟가락 한 개 꺼내기 확보. 새 봉투 투입은 실패해 보류. | [새 연결 검토본](storyboards/2026-10-24_C01-C06-repair110/edit_probes/C04_windows_to_spoon.mp4) |
| 5번 | 선명한 잭 운반으로 저해상도 확대 컷 교체. **v06 전체편집51.25초**. | [새 전체 편집본](storyboards/2026-10-25_C05-jack-edit-v06/C05_Q-AI_Fair_causal_edit_v06.mp4) |
| 6번 | 실제 첫 책상 타격만 채택. 효과음6.125초로 이동. **v06 전체편집48.75초**. | [새 전체 편집본](storyboards/2026-10-25_C06-impact-edit-v06/C06_Q-AI_Fair_edit_v06.mp4) |

원본11개 중 **5개 선택 구간 채택·6개 보류**입니다. 보류 원본도 삭제하거나 재인코딩하지 않았습니다. [11개 원본 전체와 컷별 판정](storyboards/2026-10-24_C01-C06-repair110/README.md) · [정확한 잔액 장부](storyboards/2026-10-24_C01-C06-repair110/budget_ledger.json)

세 명이 실제 추출 프레임을 독립 검토하고 서로의 지적을 대조한 뒤 새 연결과 5·6번 렌더를 재확인했습니다. 원본·편집본 전체 디코딩도 통과했습니다. **연속 재생·실청취·현장 소음 테스트는 미검증**입니다.

1·2·4번은 최종 화면 합성·자막 편집이 남아 있습니다. 이번 생성으로 자세 모방/수갑 위치/봉투 투입의 모든 동작을 완벽히 해결한 것은 아니며, 기존의 수용 구간과 시간 생략을 유지합니다. 5번의 완전 회전·하중 이전, 6번의 종이 튐·책상 진동은 확보됐다고 주장하지 않습니다.
'''
write(ROOT/'00_110크레딧_보완결과.md',newdoc)
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=s.replace('**[5·6·3번 최신 편집본](00_완성_영상.md)** · **[이번 Flow 원본34개와 채택 구간](00_영상제작_현재상태.md)**','**[110크레딧 보완 결과·원본11개](00_110크레딧_보완결과.md)** · **[5·6·3번 최신 편집본](00_완성_영상.md)** · **[전체 제작 상태](00_영상제작_현재상태.md)**')
s=s.replace('2026-10-24 V12. 5번의 지붕 받침 원인을 보완했고, 6·3번은 기존 원본으로 자막을 수정했습니다. 1·2·4번은 모든 계획 장면의 Flow 원본 후보를 확보했습니다. 이 세 편의 최종 화면 합성과 자막 편집은 남아 있습니다.','2026-10-25 최신. **110크레딧을 전부 사용했고 로그인5계정 실제 잔액0을 확인했습니다.** 새 원본11개 중5개 구간을 채택했습니다. 5번은 선명한 잭 운반, 6번은 첫 책상 타격과 효과음 위치를 반영한 v06이 최신입니다. 1·4번 새 연결 검토본도 있습니다. 1·2·4번의 최종 화면 합성과 자막 편집은 남아 있습니다.')
s=s.replace('| 인과 보완 편집본 |','| 잭 선명도 보완 v06 |').replace('| 목적 자막 보완 편집본 |','| 타격·효과음 보완 v06 |');write(p,s)
p=ROOT/'00_완성_영상.md';s=p.read_text(encoding='utf-8').replace('2026-10-24_C05-causal-edit-v05/C05_Q-AI_Fair_causal_edit_v05.mp4','2026-10-25_C05-jack-edit-v06/C05_Q-AI_Fair_causal_edit_v06.mp4').replace('2026-10-24_C06-caption-v05/C06_Q-AI_Fair_edit_v05.mp4','2026-10-25_C06-impact-edit-v06/C06_Q-AI_Fair_edit_v06.mp4').replace('진입→걸림→잡기→목 빼기 추가. 작업자 삽입으로 회전 뒤 상태 연결.','v06: 기존 인과 보완 유지, 흐릿한 확대 대신 선명한 실제 잭 운반.').replace('학습·적용 목적 자막 보강. 기존 원본·음악 재사용.','v06: 첫 책상 타격만 교체, 실제 접촉6.125초로 효과음 이동. 목적 자막 유지.');write(p,s)
p=ROOT/'00_영상제작_현재상태.md';s=p.read_text(encoding='utf-8');s=s.replace('# Q-AI Fair · V12 제작 상태','# Q-AI Fair · 최신 제작 상태\n\n**2026-10-25: [110크레딧 보완 결과](00_110크레딧_보완결과.md)가 최신입니다.** 새 원본11개, 선택5/보류6. 로그인5계정 잔액0을 실제 확인했습니다. 5·6번 v06 전체편집 및1·4번 연결검토본을 반영했습니다. 1·2·4번의 최종 합성·자막 편집은 남아 있습니다.\n\n## 이전 V12 제작 이력 — 아래 잔액과 선택은 보완 전 기록');write(p,s)
for name,old,new in [('05_괴수는_퇴근할_수_없다.md','v04 37.75초','v06 51.25초'),('06_퇴근_좀_해주세요.md','v04 48.75초','v06 48.75초')]:
    p=ROOT/name;s=p.read_text(encoding='utf-8').replace(old,new);write(p,s)
p=ROOT/'RESUME_CODEX.txt';s=p.read_text(encoding='utf-8');prefix='''[2026-10-25 최신 110크레딧 동작 보완 완료]
사용자요청:1~6검토/110전부사용/마지막40전부사용. newrun=storyboards/2026-10-24_C01-C06-repair110(시작일기준). Lite10성공11원본,보안실패2각차감0/사용자새로고침후1회정상요청. 총110순사용. u2 10→0,u3 50→0,u4 50→0;u0/u1도직접재조회0. 5계정0은2026-10-25 00:27~00:30KST실제관측. 자정갱신/전부써야리셋주장금지. 구매/구독/유료API/업스케일없음. 예약PAUSED유지. C07~10Flow없음.
원본11모두8s1280×72024fps192f,오디오트랙있음,다운로드와SHA일치/전체영상음향디코딩PASS/재인코딩0. 원본실청취없음. 정확assetID/프롬프트/계정/잔액은generation_log와budget_ledger. 모든성공요청중복금지. 마지막2다운로드버튼파일미생성→사용자저장조치후완료(중복다운로드는새생성아님).
채택5: C01K05take03[2.5,7.25]실퇴장;C04K09take02[.5,6]한숟가락추출;C04K08three_visible[2,3.5]세인물그릇내밀기(식사/재수납제외/열림동작아님);C05K04jack_detail[1.5,3]선명왼쪽운반;C06K02impact[.75,2.25]첫타격만(2.5재상승3초재타격제외,진동/종이튐미확보). 나머지6HOLD:첫창공개4인물,서서눕기실패,코치누운포즈일어남,수갑아랫고리렌즈아래/긴사슬,K01종이빈손넣고큰종이꺼냄,half-recline등안내리고코치자세변경. 이6을채택했다고쓰지말것. 기존수용구간유지.
새전체편집 C05=2026-10-25_C05-jack-edit-v06/C05_Q-AI_Fair_causal_edit_v06.mp4 51.25s1230f:26.25~27.75선명잭교체,기존AACpacket/PTS동일. C06=2026-10-25_C06-impact-edit-v06/C06_Q-AI_Fair_edit_v06.mp4 48.75s1170f:5~6.5타격교체,손접촉원본1.875=본편6.125에기존효과음이동,나머지효과·음악유지재구성. 최종전체decode/PTS/음량peak통과,실청취미검증. 메타데이터v05변경이력과v06변경5~6.5/frames120~155구분수정.
세검수자독립→교차→실제3연결probe+C05전체v06표본→C06최종v06표본재확인완료. C01/C04probes는newrun/edit_probes에있고최종자막본아님. C01/C02/C04정확모니터·포스터·문서·태블릿합성과최종자막편집남음. C03기존caption-v04유지. C05완전회전·하중이전/잭정지상승미확보,수용시간생략유지. 연속재생·실청취·현장테스트·사용자최종승인아님.
메인00_110크레딧_보완결과.md/00_완성_영상.md/README가최신진입점. Windows원본및새5/6v06= C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-repair110-2026-10-24/ . Git은push+remoteSHA확인후보고.

''';write(p,prefix+s)
# Normalize only this run's textual production records; originals stay untouched.
for folder in [R,C5,C6]:
    for p in folder.rglob('*'):
        if p.is_file() and p.suffix in ['.json','.py','.md','.txt','.html']:
            p.write_bytes(p.read_text(encoding='utf-8').replace('\r\n','\n').encode())
print('Latest root navigation and completion records updated')
