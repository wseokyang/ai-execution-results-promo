from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent;P=R.parent/'2026-10-19_keep13-rebuild-v6';ROOT=R.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=read(P/'storyboards.json');m=read(P/'scene_manifest.json');images=[]
for c in d['concepts']:
 if c['id'] not in ['C01','C03','C05']:continue
 put('retained_concept_'+c['id']+'.json',c)
 for s in c['shots']:
  a=P/s['image_file'];b=R/s['image_file'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b);assert sha(a)==sha(b)
  images.append({'concept_id':c['id'],'cut_id':s['id'],'source':str(a),'copy':s['image_file'],'sha256':sha(b)})
 es=[dict(e,reused_from_run=P.name,new_generation_in_this_run=False) for e in m['images'] if e['concept_id']==c['id']]
 put('image_manifest_retained_'+c['id']+'.json',{'images':es,'new_generation_in_this_run':False})
old=R.parent/'2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4';assert sha(old)=='b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c'
put('preservation_manifest.json',{'retained_concepts':['C01','C03','C05'],'source_run':P.name,'images':images,'old_completed_film_path':str(old),'old_completed_film_sha256':sha(old),'scope':'V6 C01·C03·C05 콘티 객체와 채택 PNG25장 그대로 보존. C02·C04만 새 제작.'})
brief={'run_id':R.name,'latest_user_request':'5번 좋네. 2번이랑 4번은 다시해줘. 이거 두개는 ai 발표대회랑 무슨 관계가 있는지 잘 모르겠음. 근데 하나는 트로이목마 컨셉을 유지해도 좋을것 같아.','retained':['C01','C03','C05'],'rebuild':['C02','C04'],'trojan_horse':'C04는 트로이목마 핵심 이미지를 유지하되 AI 실행 경험과 사례 공유가 이야기의 원인·전개·결말에 필요하도록 새로 구성. 놀이기구→퍼레이드의 은유만으로 연결하지 않음.','event_facts':read(P/'shared_brief.json')['event_facts'],'video_generation':False,'audio_generation':False,'flow_upload':False,'max_seconds':60,'casting_requirement':'기존 다양성 요구 유지. 중장년의 나이·체형·헤어·얼굴 및 인물 관계를 구별. 반복 청년 남녀 캐스팅을 피하며 외모 자체를 웃음 대상으로 삼지 않는다.','creative_gate':['신규2안에서는 행사 제목을 가려도 AI로 실제 무슨 일을 했는지 시청자가 알 수 있어야 함','구체적인 입력/실행/확인/결과 중 필요한 행위를 화면 사건으로 구현. 모두를 설명하는 튜토리얼은 아님','발표·공유가 마지막 붙임 문구가 아닌 인물 목표·질문·선택 또는 사건 해결의 필연적 일부','AI를 다른 일반 도구로 바꾸거나 마지막 행사 타이틀을 떼도 그대로인 무관한 장르극은 탈락','첫 설정 이후 새 사건과 두 번째 예상 전복, 대사 없이 읽히는 그림','기술 정합성·검수 합의를 재미 또는 사용자 수용의 증거로 쓰지 않음'],'rejected_v6':{'C02':'공주 시험장치/기사 송풍 개그와 AI 기록 정리·발표가 서로 없어도 성립','C04':'놀이기구/퍼레이드 개그에 AI 활용이 없고 마지막 경험 은유만 붙음'},'preserved_exception':'사용자가 좋다고 한 C05를 새 두 안의 기준으로 재작성하지 않는다. 보존 C01/C03도 수정하지 않는다.'}
put('shared_brief.json',brief);put('progress.json',{'status':'in_progress','stage':'reference_and_independent_concepts','retained_images':25,'new_concepts_required':2,'Flow':'not_used'})
note='[2026-10-19 V7 진행 중 — 1·3·5 유지 / 2·4 행사 연결 재작성]\n사용자는 V6 C05를 좋다고 평가했고 C02/C04의 AI 발표대회 관련성을 지적했다. C01/C03/C05 콘티와 채택25PNG를 그대로 보존한다. C04는 트로이목마 개념을 살려 새 이야기로 구성한다. 새2안은 AI로 한 구체적 실행과 결과/공유가 사건에 필요해야 한다.\n작업: storyboards/2026-10-19_keep135-rebuild-v7/. 현재 분석·발상 중이며 아직 납품 완료 아님. 컷별 첫 프레임까지 진행, Flow·영상·음원 생성 금지. 기존 V6와 완성 영상 보존.\n\n'
p=ROOT/'RESUME_CODEX.txt';b=p.read_bytes();p.write_bytes(note.encode('utf-8')+b)
print('V7 bootstrapped: C01/C03/C05 and 25 selected PNG bytes preserved.')
