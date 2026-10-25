"""Publish local review records/navigation after three actual rechecks. No network operations."""
from pathlib import Path
import json,hashlib,shutil,re
Q=Path(__file__).resolve().parent;SB=Q.parent;ROOT=SB.parent;V=SB/'2026-10-25_final-six-v13'
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fmt(n):return f'{n:g}'
ledger=json.loads((Q/'independent_and_cross_review.json').read_text(encoding='utf-8'))
ledger['issues'][1]['c06_actual_recheck']={x:'PASS' for x in 'ABC'}
ledger['final_rechecks']={
 'C04':{'reviewers':['A','B','C'],'all_opened':['sequence8pages','note_detail2pages','J11files10uniquejoins'],'status':'PASS','sha256':'6b8f287ae0ead5525e960547ba7b0595530c8bff14c2552d86cf785e53fc99cb'},
 'C06':{'reviewers':['A','B','C'],'all_opened':['sequence9pages','caption_detail3pages','J16files'],'additional_full_resolution_pngs':{'A':3,'B':2,'C':2},'status':'PASS','sha256':'9f92483e60e79bae283f6f0f5fba625f4da43274a36392a7997797bf8a0f2c08'}}
ledger['status']='FRESH_THREE_INDEPENDENT_CROSS_REVIEW_AND_TWO_EDIT_RECHECKS_COMPLETE'
dump(Q/'independent_and_cross_review.json',ledger)
# Keep inherited V13 status clearly historical in the original review input.
inp=json.loads((Q/'review_input.json').read_text(encoding='utf-8'))
for x in inp['films']:
 if 'review_status' in x:x['previous_review_status']=x.pop('review_status')
dump(Q/'review_input.json',inp)
films=[]
old=json.loads((V/'delivery_manifest.json').read_text(encoding='utf-8'))['films']
for f in old:
 cid=f['concept_id'];changed=cid in ('C04','C06')
 p=Q/cid/f'{cid}_Q-AI_Fair_final_v14.mp4' if changed else V/f['file']
 if changed:
  ed=json.loads((p.parent/'edit_manifest.json').read_text(encoding='utf-8'))
  qa=json.loads((p.parent/'technical_qa.json').read_text(encoding='utf-8'))
  assert sha(p)==qa['sha256']==ledger['final_rechecks'][cid]['sha256']
  ed['status']='THREE_REVIEWER_FRESH_SAMPLE_RECHECK_PASS';ed['final_review_record']='../independent_and_cross_review.json';dump(p.parent/'edit_manifest.json',ed)
  dur=ed['duration_seconds']
 else:
  assert sha(p)==f['sha256'];dur=f['duration_seconds']
 films.append({'concept_id':cid,'title':f['title'],'file':p.relative_to(ROOT).as_posix(),'duration_seconds':dur,'sha256':sha(p),'version':'V14' if changed else 'V13','review_status':'FRESH_THREE_INDEPENDENT_AND_CROSS_VISUAL_SAMPLE_PASS','audio_listening_verified':False,'continuous_playback_verified':False})
dump(Q/'delivery_manifest.json',{'date':'2026-10-25','films':films,'method':'Actual final MP4s freshly decoded to every0.5s and boundary frames; updated NOTE/caption sequences every0.25s. Three independent reviews, cross review and changed-film rechecks. Not realtime continuous viewing or listening.','flow_requests':0,'credits_spent':0})
rows='\n'.join(f"| {f['concept_id']} {f['title']} | [최종 MP4]({f['file']}) | {fmt(f['duration_seconds'])}초 | {f['version']} |" for f in films)
(ROOT/'00_완성_영상.md').write_text('# Q-AI Fair · 1~6편 최신 최종 영상\n\n2026-10-25 마지막 재검수 반영. **4번과 6번은 V14**, 나머지 네 편은 재검수한 V13을 유지했습니다.\n\n| 번호·제목 | MP4 | 길이 | 버전 |\n|---|---|---:|---|\n'+rows+'\n\n4번은 쪽지 투입 전체 동작을 보존하며 1초 단축했습니다. 6번은 “고마워요” 자막을 파일 전달 장면으로 옮겼습니다. 모두 화면+후처리 자막 중심이며 필수 음성 대사는 없습니다. C03은 무음, 나머지는 BGM·효과음입니다.\n\nC05는 지붕 아래 진입→걸림→받침의 원인이 보입니다. 다만 잭 운반 컷 뒤 날씨·자세·지붕 파손이 달라지는 편집 흔적이 남습니다. 방향 전환과 손 이동은 시간 생략이며, 연속 하중 이전을 전부 보여 주지는 않습니다.\n\n검수는 **최종 MP4에서 새로 추출한 전 구간 0.5초 간격 프레임과 접합 전후 프레임**으로 수행했습니다. 세 명의 독립·교차 검토 및 수정본 재확인을 마쳤습니다. 실시간 연속 재생·실청취·현장 상영은 미검증입니다.\n\n[마지막 검수와 수정 내역](00_최종_재검수.md) · [이전 생성 원본과 크레딧 기록](00_V13_보완_검수.md) · [새 7~10 콘티](00_새7-10_콘티.md)\n',encoding='utf-8')
report='''# 1~6편 마지막 재검수 — V14

2026-10-25. 여섯 편 모두 화면과 자막으로 사건을 따라갈 수 있으며, 이번 시각 검수에서 완료를 막는 필수 문제는 발견하지 못했습니다. **4번의 호흡과 6번의 감사 자막 위치를 수정**했습니다. 나머지는 동작 완료와 개그를 알아보는 시간을 보존했습니다.

[최신 최종 MP4 6편](00_완성_영상.md)

| 편 | 최종 판단 | 이번 확인·조치 |
|---|---|---|
| 1 성공 자세 교정원 | 유지 · 35.625초 | 원본 사진의 낙상→강사의 착지 합리화→수강생의 자세 모방이 읽힌다. 모방 자세와 사진 촬영을 확인하는 말미는 유지했다. |
| 2 검은 점을 잡아라 | 유지 · 36.25초 | 같은 점→촬영창 청소→점 제거→수갑이 새 장애물이 되는 인과가 읽힌다. 18.75초 수갑 설치 완료의 짧은 상태 생략은 남는다. |
| 3 환경까지 가져왔습니다 | 유지 · 43초 | 성공 환경뿐 아니라 실패 환경까지 배달되는 확대가 읽힌다. 장갑 벗기/다시 끼기는 추가 배달에 다시 일하는 연결로 유지했다. |
| 4 목마는 식사 중입니다 | **수정 · 43.5초** | 쪽지 투입 5초를 4초로 압축. 같은 종이의 완전 투입과 빈손 회수를 모두 남겼다. 요청 자막은 2.88초 확보했다. |
| 5 괴수는 퇴근할 수 없다 | 유지 · 46.75초 / 편집 흔적 명시 | 기둥 제거→지붕 아래 진입→목 걸림→받침→수리공 도착이 보인다. 잭 운반 뒤 날씨·자세·지붕 파손의 차이는 남아 있다. 시간 생략으로 수용했으며 완전한 연속 동작이라고 판단하지 않았다. |
| 6 퇴근 좀 해주세요 | **수정 · 48.75초** | 직원이 종이를 정리할 때의 “고마워요”를 삭제하고, 파일을 귀신에게 맡기는 3.25~4.75초로 옮겼다. 학습→업무 확인→퇴근→질문자 때문에 휴식 실패 흐름은 유지했다. |

4번은 중간 동작을 잘라 붙이지 않고 해당 컷 전체만 1.25배속으로 바꿨다. 6번은 같은 원본의 같은 구간으로 이전 자막을 제거했으며 음원은 V13의 AAC 2,287패킷을 그대로 보존했다. 원본·V13 파일은 덮어쓰지 않았다. 이번 Flow 요청과 크레딧 사용은 0이다.

## 무엇을 실제로 확인했나

총괄과 세 독립 검수자가 각자 최종 MP4에서 새로 추출한 전 구간 0.5초 간격 순차 이미지 **47페이지**를 열었다. 세 검수자는 편집 접합 **67곳**의 앞뒤 프레임도 모두 열고, 의심 부위를 1280×720 PNG로 확대했다. 첫 의견을 서로 공유하지 않은 뒤 교차 검증했다. 수정한 4·6번은 새 렌더의 전 구간·접합·변경부 0.25초 간격 이미지로 세 명 모두 재확인했다.

기술 검사는 6개 V13 파일의 전체 6,117프레임 디코딩과 해시를 재확인했고, 새 4번 1,044프레임·6번 1,170프레임도 전체 디코딩·24fps 시간축 검사를 통과했다. 모두 1280×720, 60초 이내다. 4번 수정본은 -23.05 LUFS / -10.01 dBTP로 측정됐다. 이는 청취 평가가 아니다.

**실시간 연속 재생·실제 청취·현장 스크린 상영·관객의 웃음 반응은 검증하지 않았다.** 이번 결론은 새로 확인한 실제 영상 프레임과 자막, 접합, 기술 검사 범위의 판정이다.

## 남겨 둔 선택 사항

- 2번 18.75초 수갑 설치, 6번 6.5초 귀신의 상체 자세에는 짧은 상태 점프가 있다. 사건 이해를 막지 않으며, 추가 크롭으로 손·서류·두 인물의 관계를 잃는 위험을 감수하지 않았다.
- 5번의 잭 운반은 21.75~23.25초 시간 생략이다. 괴수의 연속 회전·손 위치 변경·하중 이전이 모두 확보됐다고 표현하지 않는다. 이전의 ‘왜 갑자기 지붕을 받치는가’는 이제 진입과 걸림 장면으로 설명되지만, 외형·광원의 연속성이 완벽한 영상은 아니다.
- 1번 포즈 확인, 3번 장갑, 5번 목을 뺀 뒤 버티는 시간을 더 줄이는 제안은 취향상의 선택으로 남겼다. 동작의 종점을 확인하는 시간도 필요하기 때문이다.

편집 판단으로는 6번이 행사에서 배운 방법을 실제로 쓰고 다시 공유한다는 목적을 가장 직접적으로 보여 준다. 4번은 문서 모순이 배식과 지휘관의 숟가락으로 이어져 화면 개그의 전개가 명확하다. 이는 시청자 반응을 측정한 순위가 아니다.

## 검수 기록과 화면 증빙

- [총괄 독립 관찰](storyboards/2026-10-25_final-watch-v14/pd_independent_notes.md)
- [세 검수자의 지적·교차 의견·처리표](storyboards/2026-10-25_final-watch-v14/independent_and_cross_review.json)
- [최신 파일·길이·SHA 매핑](storyboards/2026-10-25_final-watch-v14/delivery_manifest.json)
- [최초 여섯 편의 실제 순차·접합 이미지](storyboards/2026-10-25_final-watch-v14/contacts/)
- [4번 수정본 실제 이미지](storyboards/2026-10-25_final-watch-v14/C04/contacts/) · [기술 검사](storyboards/2026-10-25_final-watch-v14/C04/technical_qa.json)
- [6번 수정본 실제 이미지](storyboards/2026-10-25_final-watch-v14/C06/contacts/) · [기술 검사](storyboards/2026-10-25_final-watch-v14/C06/technical_qa.json)
'''
(ROOT/'00_최종_재검수.md').write_text(report,encoding='utf-8')
prev=Q/'previous_root_docs';prev.mkdir(exist_ok=True)
for cid,name in [('C04','04_목마는_식사_중입니다.md'),('C06','06_퇴근_좀_해주세요.md')]:
 olddoc=ROOT/name
 if not (prev/name).exists():shutil.copy2(olddoc,prev/name)
 f=next(x for x in films if x['concept_id']==cid);ed=json.loads((Q/cid/'edit_manifest.json').read_text(encoding='utf-8'))
 lines=[f"# {cid} · {f['title']}",'',f"**[최종 MP4]({f['file']}) · {fmt(f['duration_seconds'])}초 · 720p 24fps · V14**",'',
 '쪽지 투입·빈손 회수를 모두 보존하면서 해당 구간을 1초 줄였습니다.' if cid=='C04' else '“고마워요”를 파일 전달 완료에 맞춰 3.25~4.75초로 옮겼습니다. 원래 음악·효과음은 그대로입니다.','',
 '[전체 영상](00_완성_영상.md) · [마지막 검수](00_최종_재검수.md) · [원본·추가 생성 기록](00_V13_보완_검수.md)','','## 최종 편집 순서','','| 컷 | 본편 구간 | 원본 사용 구간 | 소스 |','|---|---:|---:|---|']
 for it in ed['timeline']:
  source=it.get('source') or '';si=it.get('source_in') or 0;so=it.get('source_out') or (it['end']-it['start'])
  s=source.replace('\\','/');link=f'[원본](storyboards/{s})' if s and (SB/s).exists() else '후처리 엔딩'
  speed=' · 1.25배속' if it.get('speed') else ''
  lines.append(f"| {it['cut']} | {fmt(it['start'])}–{fmt(it['end'])}s | {fmt(si)}–{fmt(so)}s{speed} | {link} |")
 lines+=['','## 화면 자막','','| 구간 | 자막 |','|---|---|']
 for c in ed['captions']:lines.append(f"| {fmt(c['start'])}–{fmt(c['end'])}s | "+c['text'].replace('\n','<br>')+' |')
 lines+=['','세 검수자의 수정본 시각 표본 재확인을 마쳤습니다. 실시간 연속 재생·실청취·현장 상영은 미검증입니다.','']
 olddoc.write_text('\n'.join(lines),encoding='utf-8')
readme=ROOT/'README.md';s=readme.read_text(encoding='utf-8')
for f in films:
 if f['version']!='V14':continue
 oldf=next(x for x in old if x['concept_id']==f['concept_id']);oldpath=(V/oldf['file']).relative_to(ROOT).as_posix();s=s.replace(oldpath,f['file'])
s=s.replace('| 44.5초 |','| 43.5초 |')
s=s.replace('2026-10-25 V13.','2026-10-25 V14 재검수 반영. 4번은 호흡을 1초 압축하고 6번은 감사 자막을 실제 행동에 맞춰 옮겼습니다. [마지막 검수 기록](00_최종_재검수.md).\n\n기존 V13 작업:')
readme.write_text(s,encoding='utf-8')
resume=ROOT/'RESUME_CODEX.txt';s=resume.read_text(encoding='utf-8')
prefix='''[2026-10-25 V14 최신 — 1~6 실제 최종 영상 마지막 재검수 및 4/6 국소 수정 완료]
사용자 최신요청:1~6을직접보며마지막검수. 현재최신진입점 README.md→00_완성_영상.md/00_최종_재검수.md. 정확파일매핑 storyboards/2026-10-25_final-watch-v14/delivery_manifest.json.
총괄+3독립검수자 실제새추출0.5초전구간47페이지,3인은67접합전부/확대PNG추가확인.독립→교차→수정본3인재확인완료.필수문제0,선택2건반영.실시간연속재생/실청취/현장상영/관객반응미검증.이를봤다/들었다고확대금지.
C04 최신Q/C04/C04_Q-AI_Fair_final_v14.mp4=43.5초1044f. V13쪽지3~8s전체를1.25배속3~7s로보존,전체1초단축.자막2.88초,빈손회수보존.원래BGM/SFX해당구간tempo수정/짧은램프. SHA6b8f287ae0ead5525e960547ba7b0595530c8bff14c2552d86cf785e53fc99cb.
C06 최신Q/C06/C06_Q-AI_Fair_final_v14.mp4=48.75초1170f.감사자막7.75~9.55→3.25~4.75파일전달로이동.옛자막은같은RAW4.25~7.5동작구도로제거.전체순서시간불변,AAC2287패킷V13바이트동일. SHA9f92483e60e79bae283f6f0f5fba625f4da43274a36392a7997797bf8a0f2c08.
C01/C02/C03/C05_r3는V13그대로유지(35.625/36.25/43/46.75초). C05진입걸림받침인과는읽히나21.75~23.25잭운반시간생략뒤날씨/자세/파손차이남음.연속회전/하중이전완전확보아님. C02수갑설치/C06상체점프는선택잔여. C01모방확인/C03장갑/C05받침호흡유지.
Q=storyboards/2026-10-25_final-watch-v14.원본/V13보존.이번Flow0/크레딧0/계정잔액재조회없음/예약변경없음/7~10변경없음.최신6MP4해시/두새파일전체디코딩/PTS/자막확인완료. Git push와remoteSHA확인은별도수행후보고.

'''
if not s.startswith('[2026-10-25 V14 최신'):resume.write_text(prefix+s,encoding='utf-8')
print('Published local V14 review/navigation. Git sync not yet asserted.',flush=True)
