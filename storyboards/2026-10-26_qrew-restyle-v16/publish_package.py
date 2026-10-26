"""Prepare local review copies and repo navigation; never upload or publish externally."""
from pathlib import Path
import json,shutil,re,hashlib,html
V=Path(__file__).resolve().parent;ROOT=V.parent.parent
OUT=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-V16-delivery-2026-10-26')
OUT.mkdir(parents=True,exist_ok=True)
TITLES={'C02':'검은 점을 잡아라','C03':'환경까지 가져왔습니다','C04':'목마는 식사 중입니다','C05':'괴수는 퇴근할 수 없다','C06':'퇴근 좀 해주세요','C07':'셰프님, 그것도 주세요','C08':'구조는 끝났습니다','C09':'나 없이도 괜찮겠어요?'}
MUSIC={'C02':'100 BPM 누아르 수사극. 증거가 뒤집히는 두 순간에 음악 정지.','C03':'108 BPM 산업 리듬. 배송과 함께 층을 쌓고 발견 이후 화성을 전환.','C04':'72 BPM 군사 잠입 → 28초 정적 → 31초부터 90 BPM 식당 왈츠.','C05':'80 BPM 괴수 영화 → 작업자가 나타나는 21.75초부터 100 BPM 정비 리듬.','C06':'96 BPM 고딕 업무 리듬 → 잠깐의 라운지 → 질문자가 오면 음악 정지.','C07':'90 BPM 격식 있는 미식 왈츠. 의자 경쟁 22.3–27.6초는 음악 없음.','C08':'업무 음악 → 15.5초 영웅 등장 음악 → 23.1초 정지 → 수리 리듬.','C09':'76 BPM 진지한 이별 피아노. 충전기 질문 26.25초에 음악 정지.'}
dm=json.loads((V/'delivery_manifest.json').read_text(encoding='utf8'))
for f in dm['films']:
 f['title']=TITLES[f['concept_id']];f['music_direction']=MUSIC[f['concept_id']]
 src=V/f['path'];dst=OUT/src.name;shutil.copy2(src,dst)
 assert hashlib.sha256(dst.read_bytes()).hexdigest()==f['sha256']
 f['local_review_copy']=str(dst)
(V/'delivery_manifest.json').write_text(json.dumps(dm,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
# Metadata-only wording correction. Music samples and rendered pictures do not change.
wrong='The reply adds another layer of industrial pulse; tension continues into the delivered records.'
right='A thin industrial pulse continues under the reply, leading into the delivered records.'
for p in [V/'create_scores.py',V/'prepare_review_docs.py',V/'audio/C03/score_manifest.json']:
 t=p.read_text(encoding='utf8');p.write_text(t.replace(wrong,right),encoding='utf8')
cards=[];rows=[]
for f in dm['films']:
 cid=f['concept_id'];name=Path(f['path']).name
 cards.append(f'<section id="{cid}"><h2>{cid[1:]} · {html.escape(TITLES[cid])}</h2><p>{MUSIC[cid]}</p><video controls preload="metadata" playsinline src="{name}"></video><p>{f["seconds"]}초 · <a href="{name}" download>편집본 MP4</a></p></section>')
 rows.append(f'| {cid} · {TITLES[cid]} | [새 영상](storyboards/{V.name}/{f["path"]}) | {f["seconds"]:g}초 |')
shutil.copy2(V/'audio/C07/C07_music_preview_v16.mp3',OUT/'C07_music_preview_v16.mp3')
cards.append('<section id="C07"><h2>07 · 셰프님, 그것도 주세요 — 음악 데모</h2><p>실제 영상은 아직 없습니다. 자막·음악 제작 지시를 검토했습니다.</p><audio controls preload="metadata" src="C07_music_preview_v16.mp3"></audio></section>')
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Q-AI Fair · V16 자막·음악 수정</title><style>body{margin:0;background:#101417;color:#e9ecef;font-family:system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:32px 24px}h1{font-size:30px}p{line-height:1.7;color:#c7ced2}a{color:#8dd9e7}nav{display:flex;gap:16px;flex-wrap:wrap;padding:20px 0;position:sticky;top:0;background:#101417;z-index:2}section{padding:22px 0 36px;border-top:1px solid #364047;scroll-margin-top:80px}video{display:block;width:100%;max-height:75vh;background:#000}audio{width:100%}.note{padding:16px 20px;background:#20292f;border-radius:10px}</style><main><h1>Q-AI Fair · V16</h1><p>화면 맨 하단 중앙 자막 · 작품별 새 기악 BGM · 기존 Flow 영상 편집 유지</p><nav>'''+''.join(f'<a href="#{c}">{c[1:]}번</a>' for c in ['C02','C03','C04','C05','C06','C08','C09','C07'])+'''</nav><p class="note">7편의 자막·음악을 교체했습니다. 7번은 콘티와 음악 데모만 있습니다. 검수는 실제 추출 프레임·큐·전체 디코딩·음량 수치 기준이며 실제 청취와 실시간 연속 재생은 미검증입니다.</p>'''+''.join(cards)+'''<p>이전 편집본과 Flow 원본은 별도 보존했습니다. 새 Flow 크레딧 사용 0.</p></main><script>document.querySelectorAll('video,audio').forEach(x=>x.addEventListener('play',()=>document.querySelectorAll('video,audio').forEach(y=>{if(y!==x)y.pause()})));</script></html>'''
(OUT/'index.html').write_text(page,encoding='utf8')
# Repo version has repo-relative sources rather than cached copies.
repo_page=page
for f in dm['films']:repo_page=repo_page.replace(Path(f['path']).name,f['path'])
repo_page=repo_page.replace('src="C07_music_preview_v16.mp3"','src="audio/C07/C07_music_preview_v16.mp3"')
(V/'index.html').write_text(repo_page,encoding='utf8')
table='| 작품 | V16 MP4 | 길이 |\n|---|---|---:|\n'+'\n'.join(rows)
scope='실제 추출 프레임의 가독성·자막·정보 보존, 음악 큐와 장면의 대응, 최종 파일 전체 디코딩·시간축·음량·정적 구간을 확인했습니다. **실제 청취, 실시간 연속 재생과 현장 상영은 미검증**입니다. 음색의 자연스러움이나 취향 만족까지 확인했다는 의미는 아닙니다.'
complete='# Q-AI Fair · 자막·음악 수정 V16\n\n2026-10-26. **2·3·4·5·6·8·9번 7편의 자막과 음악을 교체**했습니다. 7번은 실제 영상이 없어 콘티·음악 데모를 검토했습니다.\n\n'+table+'\n\nGitHub에서 재생기가 없으면 파일 화면의 다운로드 버튼으로 MP4를 받으세요. 모두 1280×720, 24fps입니다.\n\n- **자막:** 화면 크기를 유지하고, 박스 없이 맨 하단 중앙의 흰색 글자·검정 외곽선으로 통일했습니다. 문서·모니터 속 글자와 별도 엔딩 카드는 구분했습니다.\n- **음악:** 기존 BGM을 재사용하지 않고 각 이야기의 장르·반전 타이밍에 맞춰 새로 작곡·합성했습니다. 음성 대사와 가사는 없습니다.\n- **7번:** [음악 데모·새 자막 적용표](storyboards/'+V.name+'/C07/README.md). 실제 영상은 미생성입니다.\n\n'+scope+'\n\n5번의 작업자 컷 뒤 자세·날씨 변화, 9번의 인계 손 방향과 확대 선명도 한계는 기존 영상에 남아 있습니다. 이번 자막·음악 수정으로 동작을 고쳤다는 뜻은 아닙니다.\n\n[변경·검수 상세](00_V16_자막_음악_검토.md) · [7편 파일·해시](storyboards/'+V.name+'/delivery_manifest.json) · [새 1·7·10 콘티](00_새1-7-10_콘티.md) · [이전 V15 안내](archive/v15-root-before-v16/00_완성_영상.md)\n'
(ROOT/'00_완성_영상.md').write_text(complete,encoding='utf8')
readme='# Q-AI Fair · 최신 영상 V16\n\n**[새 자막·음악 7편 보기](00_완성_영상.md)** · **[변경·검수](00_V16_자막_음악_검토.md)** · **[새 1·7·10 콘티](00_새1-7-10_콘티.md)** · **[첫 프레임 보기](콘티_바로보기.md)**\n\n2026-10-26 V16. QREW 최종본을 참고한 **하단 중앙 흰색 외곽선 자막**과 **작품별 새 기악 음악**으로 2·3·4·5·6·8·9번을 다시 편집했습니다. 음악은 각 장면의 긴장·반전에 맞춰 전환하고 멈춥니다.\n\n'+table+'\n\n**7번은 아직 실제 영상이 없습니다.** [콘티 자막 적용표와 새 음악 데모](storyboards/'+V.name+'/C07/README.md)를 준비했습니다. 새 1·7·10번의 기존 첫 프레임 27장은 보존했습니다.\n\n'+scope+'\n\n이번 수정은 **Flow 생성·크레딧 사용 0, 외부 유료 API 사용 0**입니다. 계정 잔액은 이번에 다시 조회하지 않았습니다. 이전 Flow 원본·편집본은 보존했습니다.\n\n<details><summary>이전 버전과 원자료</summary>\n\n[이전 V15 안내](archive/v15-root-before-v16/) · [25개 Flow 원본](storyboards/2026-10-26_C08-C09-flow-v15/README.md) · [모든 제작 버전](storyboards/) · [초기 원자료](archive/README.md)\n\n</details>\n'
(ROOT/'README.md').write_text(readme,encoding='utf8')
music_table='| 작품 | 새 음악 구성 |\n|---|---|\n'+'\n'.join(f'| {cid} · {TITLES[cid]} | {MUSIC[cid]} |' for cid in TITLES)
qa=json.loads((V/'C08/final_technical_qa.json').read_text(encoding='utf8'))
review='# V16 · 하단 중앙 자막과 음악 재구성\n\n'+music_table+'\n\n## 자막\n\n실제 QREW 최종 5편과 편집 코드를 확인했습니다. 최신 최종본은 전체 화면 위 흰색 외곽선 자막이며, 과거 일부 버전의 검은 띠와 구별했습니다. Pretendard SemiBold 57px@1080p를 38px@720p로 적용했습니다. 원전 기준선956/1080을 그대로 복사하지 않고 사용자의 ‘맨 하단’ 요청에 맞춰 **기준선684/720**으로 내렸습니다. 두 줄은641/684, 외곽선3px·약한 그림자, 최대2줄입니다. 자막 때문에 화면을 자르거나 줄이지 않았습니다. 문서·모니터·기록통 표찰은 물체에 붙이며 엔딩 카드는 별도입니다.\n\n## 음악\n\n8개 새 기악곡을 로컬 수학적 악기 합성으로 작곡했습니다. 기존 QREW에서 악기 합성 함수만 참조했고, 기존 멜로디·음원·가사를 복사하지 않았습니다. 음성·가사는 없습니다. [악기 함수 출처](storyboards/'+V.name+'/dsp_provenance.json)와 [실제 음표·큐](storyboards/'+V.name+'/audio/)를 기록했습니다. 이 음악은 외부 음악 생성 모델의 결과라고 주장하지 않습니다.\n\nC04는 28–31초 정적 후 식당 왈츠, C08은 영웅 등장15.5초 강화/23.1초 정지, C09는 충전기 질문26.25초에 음악과 잔향을 함께 멈춥니다. 매 컷마다 타격음을 붙이지 않았습니다. C06 책상 접촉6.125초에만 단일 접촉 강조음을 배치했습니다. C07은 아직 실제 영상이 없어 의자·돔·종이 접촉 효과음을 확정하지 않았습니다.\n\n## 검수·수정\n\n세 검수자가 각각 실제 추출 프레임과 전체 자막·편집표·음악 큐를 독립 검토한 뒤 교차 확인했습니다. 새 하단 자막의 화면 이탈·가독성 관련 필수 결함은 없었습니다. 다음 기록을 수정하고 세 명 모두 재확인했습니다.\n\n- C02 14.9–20.75초, C03 19.5–23.25초 큐 설명 공백 보완. 음원은 이미 존재했습니다.\n- C07 일반 자막4개를 하단 중앙으로 명시하고 물체 표찰·엔딩을 분리.\n- C07 K07 전환의 오래된25.5초를 실제 다음컷 시작24.2초로 정정.\n- C04/C07 계획 대비 실제 편성 변경을 별도 기록.\n\n최종 MP4 7편의 전체 영상 디코딩·24fps 시간축·무음 picture와 동일한 비디오 패킷·정적 구간 핵심RMS·오디오 길이를 확인했습니다. 최종 음량은 **-18.51~-18.90 LUFS**, 최대 true peak **-2.97 dBTP**입니다. 자막과 화면의 실제 검수에 사용한 picture는 최종 mux와 패킷 단위로 동일합니다.\n\n'+scope+'\n\nC05 작업자 인서트 뒤 자세/날씨 변화, C09 전화 손→충전기 수령 손 변화/확대 선명도는 기존 한계로 남습니다. 이번 변경으로 해결했다고 기록하지 않습니다. 원본과 V15 편집본은 보존했습니다.\n\n[수정본 7편](00_완성_영상.md) · [기술 검사와 리뷰 기록](storyboards/'+V.name+'/review_summary.json) · [C07 최신 적용표](storyboards/'+V.name+'/C07/README.md)\n'
(ROOT/'00_V16_자막_음악_검토.md').write_text(review,encoding='utf8')
summary={'scope':'C02,C03,C04,C05,C06,C08,C09 picture captions and new scores; C07 storyboard/audio demo only','independent_reviewers':['v16_review_a','v16_review_b','v16_review_c'],'workflow':['independent inspection','cross review','metadata corrections','three independent rechecks'],'unresolved_mandatory_findings':[], 'resolved_findings':{'A-001/B-001/C-002':'C02/C03 missing cue descriptions added; no missing audio','A-002/B-002':'C07 bottom-center captions override and prop labels/endcard separated','C-001':'C07 K07 transition corrected to24.2','B-003':'C04/C07 actual arrangements vs preliminary plan documented'},'retained_observations':{'A-003':'C05 weather/axis transition and C09 hand/crop source limitations retained','C-003':'C03 27s caption covers some records, but preceding24.5s close-up supplies that information'},'evidence':{'A':'21 contact sheets,8 full frames,4 C07 source images','B':'7 contact sheets,7 subtitle fullframes,7 endframes; additional C03 24.5/27 comparison','C':'21 contact sheets,7 fullframes,4C07 source images'},'technical_qa':{f['concept_id']:json.loads((V/f['concept_id']/'final_technical_qa.json').read_text(encoding='utf8'))['pass'] for f in dm['films']},'verification_limits':{'actual_listening':False,'realtime_continuous_playback':False,'onsite_screening':False,'audience_response':False},'new_flow_credits':0,'external_paid_api_calls':0}
(V/'review_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
# Mark latest film links on the existing C08/C09 storyboard entrypoints.
for cid in ['C08','C09']:
 for p in ROOT.glob(cid[1:]+'_*.md'):
  text=p.read_text(encoding='utf8')
  if 'V16 최신 편집본' not in text:
   text=text.replace('\n\n','\n\n**[V16 최신 편집본 — 하단 중앙 자막·새 음악](storyboards/'+V.name+'/'+cid+'/'+cid+'_Q-AI_Fair_qrew_v16.mp4)**\n\n',1)
   p.write_text(text,encoding='utf8')
resume='''[2026-10-26 V16 최신 — QREW형 하단중앙 자막·새음악 수정 완료]
최신요청: 2~9 음악/자막 전면 재검토. 실제영상 C02/C03/C04/C05/C06/C08/C09 7편을 원본Flow부터재합성, 기존컷시간/UI/엔딩보존. C07은 실제영상없으므로 콘티자막지시/음악데모만, 새Flow없음. 예약PAUSED유지. 기존V15/원본불변. Flow0/크레딧0/외부유료API0. 현재잔액재조회없음.
V=storyboards/2026-10-26_qrew-restyle-v16. 각Cxx/Cxx_Q-AI_Fair_qrew_v16.mp4 최신. 길이 C02=36.25,C03=43,C04=43.5,C05=46.75,C06=48.75,C08=53,C09=44. 720p24fps. delivery_manifest.json 파일/해시,각final_technical_qa.json PASS. Windows동일사본 C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-V16-delivery-2026-10-26/index.html.
실제QREW최종5편qrew-v3-video와motion/ad/shared/filmic.js확인. 검은띠는구버전, 이번fullframe흰색outline38px/x640/기준선684(2줄641,684). 원전기준선956/1080보다사용자맨하단요청으로더내림. 박스/상단badge없음,UI오브젝트/별도endcard유지. style_api.py공통.
음악8개새작곡/수학적악기합성. QREW악기함수만AST선별재사용,dsp_provenance.json출처; 기존멜로디/음원재사용없음. audio/Cxx/*score_v16.wav PCM24,mp3미리듣기. 음악생성모델로만들었다고주장금지. C08hero15.5/stop23.1,C09stop26.25. 최종7편-18.51~-18.90LUFS,TP최대-2.97. 정적핵심RMS/영상전체디코드/PTS/picture패킷동일성PASS. 원본음성없음.
3인독립→교차→기록수정→3인재확인. 필수미해결0. 실제이미지/큐/코드/측정검수이며 실청취/실시간연속재생/현장상영/관객반응은미검증. 새음악음색/취향합격주장금지. C05날씨축/C09수령손/crop한계여전,음악자막으로해결한척금지.
C07/V16 storyboard_v16.json/caption_manifest.json/prop_labels.json우선. 일반자막4하단,수정초안물체표찰,엔딩전체카드. K07→K08전환24.2(구25.5오타정정). 음악demo32.6,의자/dome/paperFoley는실제영상후. V15첫이미지그대로. 기존1/10콘티변경없음.
최신진입README→00_완성_영상/00_V16_자막_음악_검토. 이전루트안내archive/v15-root-before-v16. Git상태는원격SHA확인후별도보고. 이번파일만stage,기존10/24~25untracked중간파일건드리지않음.

'''
p=ROOT/'RESUME_CODEX.txt';old=p.read_text(encoding='utf8')
if not old.startswith('[2026-10-26 V16 최신'):p.write_text(resume+old,encoding='utf8')
print('Prepared',OUT/'index.html')
