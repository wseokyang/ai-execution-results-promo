"""Publish current review navigation, without changing source media or historical packages."""
from pathlib import Path
import json,re,shutil
R=Path(__file__).resolve().parent;ROOT=R.parent.parent
F=ROOT/'storyboards/2026-10-24_v12-C02-C04-C01-flow';N=ROOT/'storyboards/2026-10-24_C05-first-flow-run01'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,s:p.write_text(s,encoding='utf-8')
old=['07_결투_시간을_뺏긴_여자.md','08_이_오페라는_끝났습니다.md','09_지구인은_질문이_많다.md','10_개막을_허가하지_않는_기계.md']
new=['07_훔칠_필요가_없었다.md','08_해동하자마자_발표.md','09_낙찰받으신_분이_공개합니다.md','10_청혼은_없었습니다.md']
archive=ROOT/'archive/v11-root-review';archive.mkdir(exist_ok=True)
for name in old:
 src=ROOT/name;dst=archive/name
 assert src.parent.resolve()==ROOT.resolve() and dst.parent.resolve().is_relative_to(ROOT.resolve())
 if src.exists() and not dst.exists():
  text=src.read_text(encoding='utf-8-sig')
  def fix(m):
   t=m.group(1)
   if t.startswith(('https:','http:','#')) or t in old:return m.group(0)
   return ']('+('../../'+t)+')'
  write(dst,'> 이전 V11 콘티. 최신 7~10번은 [메인 목록](../../README.md)에서 보세요.\n\n'+re.sub(r'\]\(([^)]+)\)',fix,text));src.unlink()
for name in ['README.md','00_완성_영상.md','00_영상제작_현재상태.md','콘티_바로보기.md']:
 p=ROOT/name;dst=archive/name
 if p.exists() and not dst.exists():shutil.copy2(p,dst)
first=['01_성공_자세_교정원.md','02_검은_점을_잡아라.md','03_환경까지_가져왔습니다.md','04_목마는_식사_중입니다.md','05_괴수는_퇴근할_수_없다.md','06_퇴근_좀_해주세요.md']
for p in [ROOT/f for f in first]:
 t=p.read_text(encoding='utf-8-sig')
 for a,b in zip(old,new):t=t.replace(a,b)
 note='> **V12 제작 상태:** [현재 원본·채택 구간·후처리](00_영상제작_현재상태.md)를 먼저 확인하세요. 아래 V11 콘티보다 실제 채택 구간과 최신 5·6·3번 편집 기록이 우선합니다.\n\n'
 if not t.startswith('> **V12 제작 상태:**'):t=note+t
 write(p,t)
entries=load(F/'generation_log.json')['entries'];nentries=load(N/'generation_log.json')['entries'];originals=[e for e in entries if e.get('original')]
edits=[('5번 · 괴수는 퇴근할 수 없다','storyboards/2026-10-24_C05-causal-edit-v05/C05_Q-AI_Fair_causal_edit_v05.mp4',51.25,'진입→걸림→잡기→목 빼기 추가. 작업자 삽입으로 회전 뒤 상태 연결.'),('6번 · 퇴근 좀 해주세요','storyboards/2026-10-24_C06-caption-v05/C06_Q-AI_Fair_edit_v05.mp4',48.75,'학습·적용 목적 자막 보강. 기존 원본·음악 재사용.'),('3번 · 환경까지 가져왔습니다','storyboards/2026-10-24_C03-caption-v04/C03_Q-AI_Fair_edit_v04.mp4',44.75,'Q-AI Fair·환경 비교·보낸 동료·기록 도해로 무대사 전환.')]
write(ROOT/'00_완성_영상.md','# Q-AI Fair · 최신 편집 검토본\n\n화면과 후처리 자막이 필수 정보를 맡습니다. 사용자 최종 승인본이라는 뜻은 아닙니다.\n\n| 작품 | MP4 | 길이 | 이번 변경 |\n|---|---|---:|---|\n'+'\n'.join(f'| {title} | [보기·원본 다운로드]({path}) | {dur}초 | {note} |' for title,path,dur,note in edits)+'\n\n모두720p·24fps. 5·6번 BGM/효과음은 보조이며 3번은 무음입니다. 원본 Flow MP4는 별도로 보존했습니다.\n\n5번의 완전한 회전·하중 전달은 연속 확보한 것이 아닙니다. 작업자 삽입 전후의 시간 생략을 수용한 편집입니다. 세 검수자의 실제 프레임 검수와 기술 디코딩을 마쳤으며, 전체 연속 재생·음향 실청취·현장 소음 테스트는 미검증입니다.\n\n1·2·4번은 원본 후보 확보 단계입니다. 아직 자막·화면 합성까지 된 완성 편집본이 아닙니다.\n\n[제작 상태·전체 원본](00_영상제작_현재상태.md) · [10안 콘티](README.md)\n')
notes={
 'C01':'9개 장면 원본 확보. K01/02 앞부분, K04 착지까지, K05 문 방향 안내만 사용. K06 4.25초 이후 추가 팔·K07 후기 소실 제외. K08 초반 모방 강조. K09 take02 채택 후보(문 고정, 팔 각도 소폭 변화). 포스터·모니터를 같은 K04 영상/착지 프레임으로 후합성해야 함.',
 'C02':'9개 장면 원본 확보. K04 [1,2.5]+[4.5,6] 검사창 닦기/버튼. K05 [0,3]→K06 [0,2] 설치 시간생략. K09 [4,6.5] 손바닥/사진 엔딩으로 수정. 같은 시료의 오염 후보→닦은 뒤 정상→수갑 장애 결과, 휴대폰/사진 후합성 필수.',
 'C04':'9개 장면 원본+K08 보완 take02 확보. K01 큰 취합 종이의 봉투 진입 뒤 재추출 제외. K06 원본 미채택, K07 닫힘 초반 부인→첫 개방. K08 take02 [1,3.25] 세 창 크롭 사용. K09 중간 두 숟가락 제외하고 후반 한 개 상태 사용. 문서·태블릿 후합성 필수.'}
text='# Q-AI Fair · V12 제작 상태\n\n2026-10-24. 최신 요청 범위: **5번 보완 → 6번 → 2번 → 4번 → 3번 → 1번**, 새7~10은 콘티·첫 이미지까지만. 6·3번은 필요한 수정이 자막/도해여서 기존 실제 원본을 재사용했습니다. 일부 보완 검수와 다운로드는 다음 장면 요청과 병행했습니다.\n\n'
text+=f'이번 저장한 새 Flow 원본은 **{len(originals)+len(nentries)}개**입니다. 5번 보완5개 + 2번9개 + 4번10개 + 1번10개. 성공 원본 수와 편집에 쓸 계획 컷 수는 다릅니다.\n\n'
text+='확인한 계정의 시작/종료 잔액: u0 **250→0**, u1 **50→0**, u2 **50→10**. 이 세 계정의 순사용은 **340**입니다. 다른 두 로그인 계정 잔액은 이번에 확인하지 않아 전체 계정 잔액으로 합산하지 않습니다. u2 UI 갱신 안내는 매일 오전10:43이며 자정으로 추정하지 않습니다. 구매·구독 변경·유료 업스케일·예약 재개는 없습니다.\n\nC01 첫 K01/K02와 K05는 오디오 생성 실패 후 환불 안내를 확인하고 무음 반환 설정으로 기술 재시도했습니다. C02 K07 첫 요청은 결과가 없고10반환이 잔액 대조로 추론됐으며, 명시적 환불 UI를 본 것으로 기록하지 않습니다. 새 요청 전 모델 Lite/8초/720p/16:9/x1/10크레딧과 잔액을 확인했습니다.\n\n'
for cid,note in notes.items():text+=f'## {cid}\n\n{note}\n\n'
text+='## 편집·검수 자료\n\n[5·6·3번 최신 편집본](00_완성_영상.md) · [1·2·4번 채택 구간·검수](storyboards/2026-10-24_v12-C02-C04-C01-flow/review_summary.json) · [시험 편집](storyboards/2026-10-24_v12-C02-C04-C01-flow/edit_probes/)\n\n원본은 재인코딩하지 않았습니다. 각 MP4 8초/720p/24fps의192프레임 디코딩과 SHA 일치를 확인했습니다. 오디오 트랙 존재는 청취 검증이 아닙니다. 원본 음성은 필수 전달에 사용하지 않습니다.\n\n## 이번 Flow 원본\n\n| 컷·테이크 | 원본 | 시각 검토 |\n|---|---|---|\n'
for folder,es in [(N,nentries),(F,originals)]:
 for e in es:
  if not e.get('original'):continue
  prefix=folder.relative_to(ROOT).as_posix();stem=Path(e['original']).stem
  text+=f'| {e["unit_id"]} take{e["take"]:02d} | [MP4]({prefix}/{e["original"]}) | [추출 프레임]({prefix}/{stem}_contact.jpg) |\n'
text+='\n[5번 정확 요청·비용·원본 기록](storyboards/2026-10-24_C05-first-flow-run01/generation_log.json) · [1·2·4번 기록](storyboards/2026-10-24_v12-C02-C04-C01-flow/generation_log.json)\n\n새7~10번은 각10씬, 총40개 첫 이미지를 실제 생성했습니다. 아직 새7~10번 Flow 영상은 없습니다.\n'
write(ROOT/'00_영상제작_현재상태.md',text)
titles=['성공 자세 교정원','검은 점을 잡아라','환경까지 가져왔습니다','목마는 식사 중입니다','괴수는 퇴근할 수 없다','퇴근 좀 해주세요','훔칠 필요가 없었다','해동하자마자 발표','낙찰받으신 분이 공개합니다','청혼은 없었습니다']
durations=['콘티37.5초','콘티39초','편집44.75초','콘티37초','편집51.25초','편집48.75초','39초','42초','38초','41초']
states=['원본9장면·후처리 대기','원본9장면·후처리 대기','자막 수정 편집본','원본9장면·후처리 대기','인과 보완 편집본','목적 자막 보완 편집본']+['새 콘티·첫 이미지10장']*4
readme='# Q-AI Fair · 최신 영상과 10안 콘티\n\n**[5·6·3번 최신 편집본](00_완성_영상.md)** · **[이번 Flow 원본34개와 채택 구간](00_영상제작_현재상태.md)** · **[전체 이미지 콘티](콘티_바로보기.md)**\n\n2026-10-24 V12. 5번의 지붕 받침 원인을 보완했고, 6·3번은 기존 원본으로 자막을 수정했습니다. 1·2·4번은 모든 계획 장면의 Flow 원본 후보를 확보했습니다. 이 세 편의 최종 화면 합성과 자막 편집은 남아 있습니다.\n\n**7~10번은 완전히 새로 썼습니다.** 품질팀의 AI 성과·활용 경험 교류를 화면과 자막으로 전하며, 참석 독려를 억지로 붙이지 않았습니다. 새 네 안의 Flow 영상은 아직 만들지 않았습니다.\n\n| 콘티 | 현재 상태 | 길이 |\n|---|---|---:|\n'
for i,(name,title,state,dur) in enumerate(zip(first+new,titles,states,durations),1):readme+=f'| [{i:02d}. {title}]({name}) | {state} | {dur} |\n'
readme+='\n새 네 이야기는 **잠입자→발표자 / 구조→시연 지원 / 경매사→청중 / 청혼→공동 검사**로 반전이 다릅니다. 인물의 나이·체형·헤어·복장·감정도 구분했습니다.\n\n검수 의견은 `안 번호 / 컷 번호 / 어색한 점`으로 남기면 됩니다. 자막은 후처리, BGM·효과음은 선택입니다. 첫 이미지는 실제 동작의 시작 상태이고 움직임 검증을 대신하지 않습니다.\n\n[이번 수정·검수 상세](storyboards/2026-10-24_v12-rework/README.md) · [최초 인과 감사와 처리 현황](00_장면연결_재검토.md)\n\n<details><summary>이전 자료</summary>\n\n[교체된 V11의 7~10번](archive/v11-root-review/) · [과거 원본과 버전](storyboards/) · [초기 디자인](archive/README.md)\n\n</details>\n'
write(ROOT/'README.md',readme)
gallery=['# Q-AI Fair · 전체 이미지 콘티','', '[최신 상태·콘티 목록](README.md)','', '1~6번은 기존 V11 기획을 기반으로 한 자료이며, 실제 선택 영상의 구간과 5번 인과 보완은 최신 제작 상태가 우선합니다. 7~10번은 새 V12의 선정 첫 이미지40장입니다. 자막은 후처리합니다.','']
for name,title in zip(first+new,titles):
 gallery += [f'## {title}', '',f'[컷별 동작·자막·음향 보기]({name})','']
 t=(ROOT/name).read_text(encoding='utf-8-sig')
 gallery+=re.findall(r'!\[[^\]]*\]\([^)]+\)',t)+['']
gallery+=['## 5번 인과 보완 입력','', '[실제 편집 흐름과 영상](storyboards/2026-10-24_C05-causal-edit-v05/README.md)','']
for p in sorted((N/'inputs').glob('*.png')):gallery += [f'![{p.stem}]({p.relative_to(ROOT).as_posix()})','']
write(ROOT/'콘티_바로보기.md','\n'.join(gallery)+'\n')
write(R/'README.md','# V12 · 인과 보완과 새7~10번\n\n[최신10안 목록](../../README.md) · [전체 실제 이미지](../../콘티_바로보기.md) · [명세](storyboards.json) · [40장 이미지/프롬프트 매핑](scene_manifest.json) · [검수 결과](reviews/final_review_summary.json)\n\n새4안39/42/38/41초, 각10씬. 실제 선정 PNG40장·이전 변형본·정확 제출 프롬프트/참조/해시 보존. 독립 A/B/C→상호교차→손/이동/리그/구도 명세 수정과 재확인. 자료판·폰 UI·자막은 이후 합성하며 실제 Flow 움직임은 아직 검증하지 않았다.\n\n기획 작가 두 명의 독립 발상, 연출가 상세 전개, 이미지 담당들의 씬별 내장 이미지 생성, 세 검수자의 실제 이미지 검토를 거쳤다. 특정 광고의 장면·인물·대사를 복제하지 않고 장르의 진지함, 목적의 전용, 사건 확대와 두 번째 반전을 사용했다. 웃음 평가는 주관적 창작 검토이며 관객 실측이 아니다.\n\nC05는새입력각도와실제연결클립으로보완, C06/C03은기존영상과후처리재사용. C02/C04/C01의정확채택구간은 [현재상태](../../00_영상제작_현재상태.md) 참조.\n')
note='> **V12 처리 완료·조건 갱신:** 5번 인과는 새 연결 영상·작업자 삽입으로 보완했습니다. 6·3번 자막은 수정 편집본, 1·2·4번은 원본 후보와 제외구간 확보 상태입니다. 예전7~10번은 새 콘티/40이미지로 교체했습니다. [최신 상태](00_영상제작_현재상태.md). 아래는 수정 전 감사 이력입니다.\n\n'
for fn in ['00_장면연결_재검토.md','00_제작전_최종검토.md']:
 p=ROOT/fn;t=p.read_text(encoding='utf-8-sig')
 if not t.startswith('> **V12 처리'):write(p,note+t)
print('Current root navigation and archival copies published.')
