"""Build review-first GitHub entry files from the approved V11 data, without media changes."""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[2]
BASE=Path('storyboards/2026-10-23_v11-production-lock')
R=ROOT/BASE
d=json.loads((R/'storyboards.json').read_text(encoding='utf8'))
m=json.loads((R/'scene_manifest.json').read_text(encoding='utf8'))
ims={x['id']:x for x in m['images']}
def rel(p):return (BASE/p).as_posix()
def md(s):return str(s or '').replace('|','／').replace('\n','<br>')
def flat(s):return str(s or '').replace('\n',' / ')
def name(c):return f'{int(c["id"][1:]):02}_{c["title"].replace(" ","_")}.md'
files={c['id']:name(c)for c in d['concepts']}
rows=['# Q-AI Fair · 최신 10안 검수','','**[00. 제작 전 최종 검토와 추천](00_제작전_최종검토.md)** — 이번 수정과 안별 강점·남은 제작 확인을 먼저 보세요.','','**아래 01–10번 파일만 보시면 됩니다.** 각 파일에 컷별 이미지·동작·자막·음향·전환을 모았습니다. 현재 검수 기준은 **V11 · 2026-10-23**입니다.','','| 안별 스토리보드 | 구분 | 용도 | 길이 | 시작 이미지 |','|---|---|---|---:|---:|']
for c in d['concepts']:
 us=[u for u in d['generation_units']if u['concept_id']==c['id']]
 rows.append('| ['+f'{int(c["id"][1:]):02}. {c["title"]}'+']('+files[c['id']]+') | '+('신규'if int(c['id'][1:])>=6 else'기존 보완')+' | '+c['purpose']+f' | {c["duration_seconds"]}초 | {len(us)}장 |')
rows+=['','[88장 전체 이미지 한 번에 보기](콘티_바로보기.md) · [10안 한눈에 보기]('+rel(Path('overview_10.jpg'))+')','','검수 의견은 **안 번호 / 컷 번호 / 어색한 점**으로 남기면 됩니다. 예: `06 / K07 / 방문 유령이 왜 왔는지 더 바로 알면 좋겠음`.','','- 소리가 없어도 화면과 자막으로 이야기와 반전이 이해되는지 봐 주세요.','- 이미지의 얼굴·손·소품과 자막이 서로 방해하는지, Q-AI Fair로 이어지는 이유가 자연스러운지 봐 주세요.','- 이미지들은 동작의 시작 상태입니다. 실제 움직임·편집 호흡은 이후 영상 제작 단계에서 확인합니다.','','이번 검수본은 10안·87편집 컷·88시작 이미지입니다. 모든 자막은 후처리하며 BGM·효과음은 보조입니다. **이번 V11 작업에서 추가 영상은 생성하지 않았습니다.**','','<details>','<summary>보관 자료·제작 원본 찾기</summary>','','- [이전 안내·초기 디자인 보관](archive/README.md)','- [최신 V11 제작 원본·검수 기록]('+BASE.as_posix()+'/README.md)','- [과거 콘티·영상 원본](storyboards/) — 이번 검수에 볼 필요 없음','- [이전 완성 1번 영상](storyboards/2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4)','- [C03 기존 검토 편집](storyboards/2026-10-20_C03-edit-v03/C03_review_edit_v03_45s.mp4)','','</details>']
(ROOT/'README.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
total=0
for ci,c in enumerate(d['concepts']):
 cid=c['id'];us=[u for u in d['generation_units']if u['concept_id']==cid];ss={s['id']:s for s in c['shots']}
 nav='[검수 목록으로](README.md)'
 if ci:nav+=' · [← 이전 안]('+files[d['concepts'][ci-1]['id']]+')'
 if ci<9:nav+=' · [다음 안 →]('+files[d['concepts'][ci+1]['id']]+')'
 out=[nav,'',f'# {int(cid[1:]):02}. {c["title"]}','','**'+c['logline']+'**','',f'**{cid} · V11 · {c["purpose"]} · {c["duration_seconds"]}초 · {len(us)}개 시작 이미지**','','**전달할 내용:** '+c['core_message'],'','**웃음의 전개:** '+c['comedy_engine'],'','화면과 후처리 자막으로 전달하는 검수용 콘티입니다. 아래 이미지는 동작의 시작 상태이며, 자막이 있는 컷은 그 첫 이미지 위에 자막 위치를 얹은 정지 예시입니다. 실제 동작 완료 화면이나 생성 영상은 아닙니다.','','<details>','<summary>등장인물·연출 보기</summary>','']
 for ch in c['characters']:out.append('- **'+ch['id']+'**: '+ch['description'])
 out+=['','**형식:** '+c['format'],'','**연출:** '+str(c['visual_style']),'','</details>','','## 컷별 스토리보드','']
 for u in us:
  s=ss[u['linked_shot']];e=ims[u['id']];qs=s.get('caption_cues',[]);total+=1
  interval=f'{s["start"]}–{s["end"]}초 · {s["duration"]}초'
  if u['id']=='C05_K02A':interval='4–7초 · 3초 (K02 앞부분)'
  if u['id']=='C05_K02B':interval='7–11초 · 4초 (K02 뒷부분)'
  out += ['### '+u['id']+' · '+interval,'']
  proof=Path(f'caption_proofs/{cid}_{s["id"]}_cue1.jpg')
  preview=proof if qs and(R/proof).exists() else Path(e['image_path'])
  out += ['!['+u['id']+(' 자막 위치 검토용 첫 이미지'if preview==proof else' 첫 이미지')+']('+rel(preview)+')','', '**첫 상태:** '+u['first_frame'],'','**이어질 동작:** '+u['action'],'']
  if 'continuity_in' in u:
   out+=['**앞 컷 연결:** '+u['continuity_in'],'','**이 단위의 종료 상태:** '+u['continuity_out'],'']
  if qs:
   out+=['**후처리 자막**','']
   for q in qs:
    txt=(q.get('eyebrow','')+' / 'if q.get('eyebrow')else'')+flat(q['text'])
    out.append(f'- **{q["start"]}–{q["end"]}초:** '+txt)
   out+=['']
   for qi in range(1,len(qs)):
    more=Path(f'caption_proofs/{cid}_{s["id"]}_cue{qi+1}.jpg')
    if (R/more).exists():out+=['<details>','<summary>이 컷의 다음 자막 배치 보기</summary>','',f'![{u["id"]} 다음 자막]('+rel(more)+')','','</details>','']
  else:out+=['**후처리 자막:** 없음. 행동과 표정으로 전달.','']
  out+=['**웃음·정보 의도:** '+s['intent'],'','<details>','<summary>대사·음악·효과음·구도·전환</summary>','','| 항목 | 내용 |','|---|---|', '| 대사·내레이션 | '+md(s['dialogue'])+' |','| 음악·효과음·정적 | '+md(s['sound'])+' |','| 구도 | '+md(u['framing'])+' |','| 전환 | '+md(s['transition'])+' |','','[자막 없는 시작 PNG 원본]('+rel(Path(e['image_path']))+')','','</details>','']
 out+=['---','',nav,'','정확한 행사 날짜·장소·참석 방법은 아직 기입하지 않았습니다. 실제 영상 제작 뒤 움직이는 소품·자막 가림·읽는 시간·편집 호흡을 재확인합니다.']
 (ROOT/files[cid]).write_text('\n'.join(out)+'\n',encoding='utf8')
assert total==88
(ROOT/'team/review-navigation/root_review_manifest.json').write_text(json.dumps({'source':BASE.as_posix(),'version':'V11','concepts':[{'id':c['id'],'file':files[c['id']],'start_images':sum(u['concept_id']==c['id']for u in d['generation_units'])}for c in d['concepts']],'selected_start_images':total,'review_pages_include':'every actual selected start image or separately rendered caption proof, exact caption timings, next action, intent, dialogue, sound, camera and transition','media_changed':False},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Built README and10 root review storyboards covering88 selected start states')
