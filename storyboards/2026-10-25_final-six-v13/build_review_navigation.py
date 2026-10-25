from pathlib import Path
import json,html,shutil,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[2]
V=Path(__file__).resolve().parent
P=ROOT/'storyboards/2026-10-25_C07-C10-rewrite-v13'
CACHE=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-final-six-v13-2026-10-25')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def mdtext(x):
 if x is None:return ''
 if isinstance(x,list):return '<br>'.join(mdtext(a) for a in x)
 if isinstance(x,dict):return mdtext(x.get('text',json.dumps(x,ensure_ascii=False)))
 return str(x).replace('|','／').replace('\n','<br>')
def caps(q):return '<br>'.join(f'{x["start"]:g}–{x["end"]:g}s {mdtext(x["text"])}' for x in q)
def archive(p):
 arc=ROOT/'archive/v12-before-final-v13';arc.mkdir(exist_ok=True)
 if (arc/'archive_complete.txt').exists():return
 assert p.resolve().parent==ROOT.resolve() and arc.resolve().is_relative_to(ROOT.resolve())
 if p.exists() and not (arc/p.name).exists():
  txt=p.read_text(encoding='utf-8-sig').replace('](storyboards/','](../../storyboards/').replace('](archive/','](../../archive/')
  (arc/p.name).write_text(txt,encoding='utf-8')
d=read(P/'storyboards_draft.json')
entries=[]
for name in ['artist_C07_C08_manifest.json','artist_C09_manifest.json','artist_C10_manifest.json']:
 m=read(P/name);entries.extend(m.get('entries',m.get('scenes',[])))
by={}
for e in entries:
 file=e.get('file',e.get('relative_image_path'))
 if not file:file=Path(e.get('actual_image_path',e.get('actual_path',e.get('image_path')))).relative_to(P).as_posix()
 by[(e['concept_id'],e['scene_id'])]={**e,'file':file.replace('\\','/')}
assert len(by)==40
sceneout=[]
for c in d['concepts']:
 for s in c['scenes']:
  e=by[(c['id'],s['scene_id'])];fp=P/e['file'];assert fp.exists()
  sceneout.append({**s,'actual_file':e['file'],'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'prompt':e.get('prompt',''),'reference_images':e.get('reference_images',[]),'image_status':'GENERATED','review_status':'SEE reviews/final_image_review.json'})
final_image_review=P/'reviews/final_image_review.json'
image_done=final_image_review.exists() and read(final_image_review).get('status')=='PASS_WITH_DOCUMENTED_FUTURE_VIDEO_CHECKS'
d['status']='TEXT_AND_40_FIRST_FRAMES_REVIEWED' if image_done else '40_ACTUAL_FIRST_FRAMES_READY_FOR_FINAL_IMAGE_REVIEW'
d['scene_manifest']=sceneout
dump(P/'storyboards.json',d)
dump(P/'scene_manifest.json',{'run':P.name,'event':'Q-AI Fair','scenes':sceneout,'count':40,'flow_generated':False})
films=read(V/'delivery_manifest.json')['films']
oldfiles=sorted(ROOT.glob('[0-9][0-9]_*.md'))+[ROOT/'README.md',ROOT/'콘티_바로보기.md']
for p in oldfiles:archive(p)
old7=['07_훔칠_필요가_없었다.md','08_해동하자마자_발표.md','09_낙찰받으신_분이_공개합니다.md','10_청혼은_없었습니다.md']
for name in old7:
 p=ROOT/name
 if p.exists():
  dest=ROOT/'archive/v12-before-final-v13'/name
  assert dest.exists() and p.resolve().parent==ROOT.resolve() and dest.resolve().is_relative_to(ROOT.resolve())
  p.unlink() # Preserved in archive above and Git history; exact root file only, never recursive.
rootnames=['01_성공_자세_교정원.md','02_검은_점을_잡아라.md','03_환경까지_가져왔습니다.md','04_목마는_식사_중입니다.md','05_괴수는_퇴근할_수_없다.md','06_퇴근_좀_해주세요.md']
allimgs=['# Q-AI Fair · 최신 전체 이미지 콘티','', '1~6번은 실제 최종 편집본에서 뽑은 검수 화면, 7~10번은 새 영상용 첫 프레임입니다.','', '[6편 MP4](00_완성_영상.md) · [새 7~10 상세 콘티](00_새7-10_콘티.md)','']
videodoc=['# Q-AI Fair · 1~6편 최종 편집 V13','','2026-10-25. 모두 60초 이내, 화면+후처리 자막으로 전달하며 필수 음성 대사는 없습니다.','', '| 번호·제목 | MP4 | 길이 |','|---|---|---:|']
rows=[]
for i,f in enumerate(films):
 cid=f['concept_id'];fp=V/f['file'];folder=fp.parent
 mp=folder/'edit_manifest.json'
 if not mp.exists():mp=folder/'source_edit_manifest.json'
 ed=read(mp)
 timeline=ed.get('timeline',ed.get('segments',[]))
 link=rel(fp)
 videodoc.append(f'| {cid} {f["title"]} | [최종 MP4]({link}) | {f["duration_seconds"]:g}초 |')
 doc=[f'# {cid} · {f["title"]}', '',f'**[최종 MP4]({link}) · {f["duration_seconds"]:g}초 · 720p 24fps · V13**','',f['note'],'','[전체 영상](00_완성_영상.md) · [원본·추가 생성 기록](00_V13_보완_검수.md)','', '## 최종 편집 순서','', '| 컷 | 본편 구간 | 원본 사용 구간 | 소스 |','|---|---:|---:|---|']
 for t in timeline:
  src=t.get('source');srcstr=(f'[원본](storyboards/{str(src).replace(chr(92),"/")})' if src else '후처리 엔딩')
  doc.append(f'| {t.get("cut","")} | {t.get("start",0):g}–{t.get("end",0):g}s | {t.get("source_in",0):g}–{t.get("source_out",0):g}s | {srcstr} |')
 doc+=['','## 화면 자막','']
 cap=ed.get('captions',[])
 if cap and isinstance(cap[0],dict):
  doc+=['| 구간 | 자막 |','|---|---|']+[f'| {x.get("start",0):g}–{x.get("end",0):g}s | {mdtext(x.get("text",""))} |' for x in cap]
 else:
  ss=next(iter(folder.glob('*captions.srt')),None)
  if ss:doc+=[f'[자막 타임코드]({rel(ss)})']
 contacts=sorted(folder.glob('review_contact_*.jpg'))
 doc+=['','## 실제 편집본 검수 화면','']
 for p in contacts:doc += [f'![{cid} actual final frame samples]({rel(p)})','']
 doc+=['검수 범위: 실제 추출 프레임·접합 표본, 자막, 전체 파일 디코딩·시간축·원본 해시. 실시간 연속 재생·실청취·현장 상영 테스트를 마쳤다는 의미는 아닙니다.','']
 (ROOT/rootnames[i]).write_text('\n'.join(doc),encoding='utf-8')
 allimgs += [f'## [{cid} · {f["title"]}]({rootnames[i]})','']
 if contacts:allimgs+=[f'![{cid} final preview]({rel(contacts[0])})','']
 rows.append(f'| [{cid} {f["title"]}]({rootnames[i]}) | [최종 MP4]({link}) | {f["duration_seconds"]:g}초 |')
newnames={};newdoc=['# 새 7~10번 · V13 콘티','','화면+후처리 자막으로 전달합니다. 필수 음성 대사 0. 각10씬 첫 이미지 총40장, 아직 Flow 영상은 생성하지 않았습니다.','', '| 안 | 장르·사건 | 길이 | 시작 이미지/예상 기본 생성 |','|---|---|---:|---:|']
htmlparts=[]
for c in d['concepts']:
 cid=c['id'];filename=cid[1:]+'_'+re.sub(r'[?]','',c['title']).replace(' ','_')+'.md';newnames[cid]=filename
 dur=c['expected_duration_seconds']
 newdoc.append(f'| [{cid} {c["title"]}]({filename}) | {c["one_line"]} | {dur:g}초 | 10장 / 최소10단위 |')
 doc=[f'# {cid} · {c["title"]}','',c['one_line'],'',f'**{dur:g}초 · 10씬 · 화면+자막 · 필수 음성 대사 없음 · Flow 미생성**','','[새 4안 비교](00_새7-10_콘티.md) · [전체 이미지](콘티_바로보기.md)','',f'**전달할 내용:** {c["core_message"]}','',f'**반전:** {c["reversal"]}','',f'**후폭풍:** {c["ending_connection"]}','', '## 등장인물','']
 for a in c['cast']:doc += [f'- **{a["id"]}**: {a["appearance"]} {a["costume"]}']
 doc+=['','## 컷별 콘티','','| 씬·컷 | 구간·길이 | 화면·행동·구도 | 후처리 자막 | 대사·내레이션 | BGM·효과음 | 전환 | 웃음·정보 의도 |','|---|---|---|---|---|---|---|---|']
 for s in c['shots']:doc.append(f'| {s["scene_id"]} / {s["id"]} | {s["start"]:g}–{s["end"]:g}s ({s["duration"]:g}s) | {mdtext(s["visual_action"])}<br>{mdtext(s["composition"])} | {caps(s["caption_cues"])} | 없음 | {mdtext(s["music_sfx_silence"])} | {mdtext(s["transition"])} | {mdtext(s["intent"])} |')
 doc += ['','## 씬별 실제 첫 프레임','', '이미지는 동작 직전 상태입니다. 행사명·문서·폰 UI·자막은 영상 생성 뒤 별도 합성합니다.','']
 h=[f'<section id="{cid}"><h2>{cid} · {html.escape(c["title"])}</h2><p>{html.escape(c["one_line"])}</p><p>{dur:g}초 · 10씬 · 무대사</p>']
 allimgs += [f'## [{cid} · {c["title"]}]({filename})','',c['one_line'],'']
 for s in c['shots']:
  e=by[(cid,s['scene_id'])];imagepath=rel(P/e['file'])
  doc += [f'### {s["id"]} · {s["start"]:g}–{s["end"]:g}초','',f'![{s["id"]} 첫 프레임]({imagepath})','',f'**시작:** {s["frame_start_description"]}','',f'**동작:** {s["visual_action"]}','',f'**끝 상태:** {s["frame_end_description"]}','',f'**후처리:** {mdtext(s.get("post_composites",[])) or "자막 외 없음"}','']
  allimgs += [f'**{s["id"]} · {s["start"]:g}–{s["end"]:g}초** — {s["visual_action"]}','',f'![{s["id"]}]({imagepath})','',f'자막: {caps(s["caption_cues"]) or "없음"}','']
  dst=CACHE/e['file'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/e['file'],dst)
  h.append(f'<article><h3>{s["id"]} · {s["start"]:g}–{s["end"]:g}초</h3><img loading="lazy" src="{e["file"]}"><p>{html.escape(s["visual_action"])}</p><p class="caption">{html.escape(" / ".join(x["text"] for x in s["caption_cues"])) or "자막 없음"}</p><details><summary>시작·끝·후처리</summary><p>시작: {html.escape(s["frame_start_description"])}</p><p>끝: {html.escape(s["frame_end_description"])}</p><p>{html.escape(str(s.get("post_composites",[])))}</p></details></article>')
 if cid=='C10':
  proof=P/'caption_previews/C10_S10_caption_layout_v2.png'
  doc+=['','### 엔딩 자막 실제 배치 확인본','',f'![좌상단 자막 배치]({rel(proof)})','', '이 파일은 후처리 위치 확인용이며 Flow 시작 이미지로 사용하지 않습니다.','']
  dst=CACHE/'caption_previews'/proof.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(proof,dst)
  h.append('<article><h3>엔딩 자막 실제 배치 확인본</h3><img src="caption_previews/C10_S10_caption_layout_v2.png"><p>후처리 위치 확인용. Flow 시작 이미지로 사용하지 않습니다.</p></article>')
 h.append('</section>');htmlparts+=h
 doc+=['','## 제작 메모','',f'난이도: {c["production_difficulty"]["level"]}. {c["production_difficulty"]["reason"]}','',c['production_difficulty']['fallback'],'',f'[정확 프롬프트·이미지 매핑]({rel(P/"scene_manifest.json")})','', '시작 이미지 검수는 실제 영상의 동작 성공·관객 반응 검증을 대신하지 않습니다.','']
 (ROOT/filename).write_text('\n'.join(doc),encoding='utf-8')
 rows.append(f'| [{cid} {c["title"]}]({filename}) | 새 콘티·첫 이미지10장 / Flow 미생성 | {dur:g}초 |')
newdoc+=['','각 안 기본10개 영상 단위입니다. 실제 동작이 한 번에 성립하지 않으면 분할 생성이 필요할 수 있으므로 성공 수·크레딧을 보장하지 않습니다.','', '**참고 방식:** 장르를 진짜처럼 시작하고, 인물의 욕망 충돌→행동→두 번째 반전→후폭풍을 응용했습니다. 특정 광고의 인물·대사·음악·장면을 복제하지 않았습니다.','',f'[전체 제작 명세]({rel(P/"storyboards.json")}) · [이미지·프롬프트 매핑]({rel(P/"scene_manifest.json")})','']
(ROOT/'00_새7-10_콘티.md').write_text('\n'.join(newdoc),encoding='utf-8')
(ROOT/'콘티_바로보기.md').write_text('\n'.join(allimgs),encoding='utf-8')
videodoc += ['','C05는 목을 빼는 장면과 정면에서 받치는 장면 사이에 실제 작업자의 잭 운반을 넣어 시간을 생략했습니다. 연속 회전·손 위치 변경·하중 이전을 모두 촬영한 것은 아닙니다.','', '세 명의 독립 검수자가 실제 프레임과 접합을 확인하고 의견을 교차 검토했습니다. 전체 파일 디코딩·시간축·자막·원본 보존도 확인했습니다. **실청취·실시간 연속 재생·현장 상영 테스트는 미확인**입니다. C03은 무음, 나머지는 BGM·효과음이며 원본 음성은 제거했습니다.','', '[이번 생성 원본과 크레딧 기록](00_V13_보완_검수.md) · [새 7~10 콘티](00_새7-10_콘티.md)','']
(ROOT/'00_완성_영상.md').write_text('\n'.join(videodoc),encoding='utf-8')
css='body{margin:0;background:#10151c;color:#e8eef5;font:16px/1.65 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:30px 20px}nav{display:flex;gap:24px;position:sticky;top:0;background:#10151ced;padding:16px;flex-wrap:wrap}a{color:#72dbd0}section{margin:55px 0}article{padding:22px;background:#1c2733;border-radius:14px;margin:24px 0}img{width:100%;height:auto;border-radius:8px}.caption{color:#ffe2a0;font-size:21px}details{color:#b8c8d8}'
(CACHE/'storyboards.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair · 새7–10콘티 V13</title><style>'+css+'</style><main><h1>새7–10 · 이야기와 첫 프레임</h1><p>40장 · 자막은 후처리 · 필수 음성 대사 없음 · Flow 미생성</p><nav><a href="index.html">1–6 최종 영상</a>'+''.join(f'<a href="#{c["id"]}">{c["id"]} {html.escape(c["title"])}</a>' for c in d['concepts'])+'</nav>'+''.join(htmlparts)+'</main></html>',encoding='utf-8')
readme=['# Q-AI Fair · 1~6편 최종 영상 / 새 7~10 콘티','','**[1~6 최종 MP4 보기](00_완성_영상.md)** · **[새 7~10 콘티](00_새7-10_콘티.md)** · **[전체 이미지 보기](콘티_바로보기.md)** · **[보완·검수·크레딧](00_V13_보완_검수.md)**','','2026-10-25 V13. 1~6편은 실제 Flow 영상에 후처리 자막과 필요한 화면 합성을 완료했습니다. 7~10편은 이전 이야기를 교체하고 씬별 시작 이미지40장을 새로 만들었습니다. 새7~10 Flow는 아직 실행하지 않았습니다.','','| 작품 | 최신 결과 | 길이 |','|---|---|---:|',*rows,'','실제5계정 시작 관측 합계200크레딧으로 추가 원본12개를 보존했고,6개를 채택·6개는 결함으로 보류했습니다. 확인한5계정 잔액은 모두0입니다. 사용자 말씀250과 실제 관측200의 차이50은 확인되지 않아 사용했다고 기록하지 않았습니다.','','C05의 회전·손 이동은 작업자 컷 동안의 시간 생략입니다. 원본의 외형·팔 변형을 억지로 연결하지 않았습니다. 모든 영상은 화면+자막 중심이며, 청취·현장 상영 검증 범위는 [검수 기록](00_V13_보완_검수.md)에 구분했습니다.','','<details><summary>이전 버전과 원본</summary>','','[교체 전 루트 문서](archive/v12-before-final-v13/) · [모든 원본·버전](storyboards/) · [초기 자료](archive/README.md)','','</details>','']
(ROOT/'README.md').write_text('\n'.join(readme),encoding='utf-8')
print('Built root6film docs +4storyboards +40imageindex +Windows gallery.')
