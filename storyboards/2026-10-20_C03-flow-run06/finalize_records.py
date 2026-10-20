"""Finalize records for a completed one-request run; no browser or media mutation."""
from pathlib import Path
import hashlib
import html
import json
import shutil
import tomllib
from html.parser import HTMLParser

RUN = Path(__file__).resolve().parent
ROOT = RUN.parent.parent
CACHE = Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/run06')
STEM = 'C03_K04_insert_take05'
def load(name):
    return json.loads((RUN / name).read_text(encoding='utf-8-sig'))
def save(name, obj):
    (RUN / name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

meta = load(STEM+'_inspection.json')
review = load('review_summary.json')
assert len(review['video_cross_reviews']) == 3
log = load('generation_log.json')
assert len(log['requests']) == 1
request = log['requests'][0]
assert sha(RUN / (STEM+'.mp4')) == meta['sha256'] == sha(Path(request['download_source']))
assert meta['decoded_video_frames'] == 192 and meta['full_video_decode_pass']
request.update({'status':'completed_original_preserved_cuff_adjustment_candidate', 'technical_metadata':meta,
                'original_reencoded':False, 'download_sha256_matches':True,
                'submitted_prompt_exact':(RUN/request['prompt_file']).read_text(encoding='utf-8-sig'),
                'input_start_sha256':sha(RUN/request['input_start']), 'review_record':'review_summary.json'})
log.update({'status':'complete_one_requested_attempt_reviewed_and_preserved', 'ending_credits':0,
            'net_credits_used':10,'refunds_observed':0,'new_originals':1,'c03_total_originals':18,
            'pending_generation_requests':0,'final_ui_settings':{'model':'Veo 3.1 Lite','silent_fallback':False,'composer':'empty'},
            'final_ui_evidence':'completed_ui.jpg','final_film_complete':False,
            'quality_decision':review['pd_video_decision']})
save('generation_log.json',log)
im = load('image_manifest.json')
assert sha(RUN/'images/C03/K04_finish_insert01.png') == im['sha256']
im['review_status']='PD accepted shorter cuff-adjustment scope; three actual-image independent/cross reviews complete'
im['review_record']='review_summary.json'
im['remaining_uncertainties']=['Image depicts already-worn gloves, not a half-inserted hand.','Motion candidate received sampled visual review; continuous-playback timing remains unverified.']
save('image_manifest.json',im)

shutil.copy2(RUN/'frames'/STEM/'12_3.000s.png',RUN/(STEM+'_poster.png'))
readme='''# C03 커프 정돈 보완 run06

사용자의 **“10크레딧 남았으니까 한번 더 시도해봐”** 요청으로 Lite 1회 추가했습니다. **10→0크레딧**, 실패·환불·중복 요청 없음. 새 원본 1개, C03 원본 누적 18개입니다.

[8초 원본 재생·다운로드](originals.html) · [원본 MP4](C03_K04_insert_take05.mp4)

**‘오른손 장갑 커프를 당겨 정돈하고 놓는 동작’의 사용 후보를 확보했습니다.** 세 검수자가 실제 0.25초 간격 표본과 개별 PNG를 독립 검토하고 상호 교차했습니다. 2.5–3.25초에 천 가장자리가 소매 쪽으로 이동해 손목 피부를 덮고, 약 5–5.25초에 두 손이 떨어집니다. 표본에서 이전의 장갑 합침·갑작스러운 재질 생성은 발견하지 못했습니다.

편집 추천은 **2.25–5.75초, 약 3.5초**입니다. 이번에는 원본만 보존했으며 이 구간의 별도 편집본을 만들지는 않았습니다. 실시간 호흡·연속재생은 미검증입니다.

## 변경한 입력

내장 imagegen으로 새 첫 프레임 1장을 만들었습니다. 두 손은 이미 장갑을 착용하고 오른손목 피부가 드러나며, 왼손이 오른장갑 커프를 잡습니다. 처음 계획한 손등 노출보다 짧은 동작이어서 프롬프트도 '이미 낀 장갑의 커프 정돈'으로 좁혔습니다. 시작 이미지 1장만 사용, 종료 이미지 없음, 16:9/720p/8초/x1/Lite10. 무대사 인서트의 무음 반환은 일시 ON 후 OFF로 복구했습니다.

![사용한 첫 프레임](images/C03/K04_finish_insert01.png)

## 판정의 한계

전체 장갑 삽입·탈착 성공은 아닙니다. K03에서 맨손이 된 다음 이 상태로 갈 때는 착용 시작 과정의 생략 편집이 필요합니다. K03 물리적 탈착, C03 전체 편집 및 다른 컷의 음성 검증은 아직 남아 있습니다. 이전 7.5초 편집 대안도 수정하지 않았습니다.

원본은 8초/1280×720/24fps/H264이며 **오디오 트랙이 없습니다**. 192프레임 디코딩 통과, 다운로드 파일과 SHA256 일치, 원본 재인코딩 없음.

[생성 ID·정확한 프롬프트·입력·차감](generation_log.json) · [3인 독립·교차 검수](review_summary.json) · [이미지 생성 프롬프트](image_prompt.txt) · [이미지 기록](image_manifest.json)

기존 V8·legacy C01·이전 원본을 보존했습니다. 구매·계정 전환·업스케일·예약 재개·공개 게시 없음.

![Flow 완료 화면](completed_ui.jpg)
'''
(RUN/'README.md').write_text(readme,encoding='utf-8')
page=f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>C03 커프 정돈 보완 · run06</title><style>body{{font-family:system-ui,sans-serif;background:#11151d;color:#edf1f7;max-width:1040px;margin:40px auto;padding:0 20px;line-height:1.7}}a{{color:#90ccff}}video,img{{max-width:100%;border-radius:12px}}video{{width:100%;background:#000}}.note{{background:#20332e;border-left:4px solid #83d1b2;padding:16px}}details{{margin:24px 0}}</style><h1>C03 · 장갑 커프 정돈 보완</h1><p>2026-10-20 · Lite 1회 · 사용10 / 잔액0 · 새 원본1개</p><p class="note"><strong>커프 정돈 동작은 시각 표본 검수 통과.</strong> 천의 경계가 손목을 덮고 손을 놓는 흐름을 확인했습니다. 맨손부터 장갑을 끼우는 전체 동작은 아닙니다.</p><video controls playsinline preload="metadata" poster="{STEM}_poster.png" src="{STEM}.mp4"></video><p><a download href="{STEM}.mp4">8초 원본 MP4 다운로드</a> · <a href="{STEM}_contact.jpg">검수 표본 보기</a></p><p>1280×720 / 24fps / 무음 원본. 추천 사용 구간 2.25–5.75초(아직 트림하지 않음). 3명 독립·교차 표본 검수 완료. 연속 재생의 호흡은 미검증입니다.</p><p>기존 맨손 장면과 연결할 때 착용 시작은 컷 사이에서 생략해야 합니다. C03 최종 완성본은 아닙니다.</p><details><summary>이번에 사용한 첫 프레임</summary><img src="images/C03/K04_finish_insert01.png" alt="이미 낀 장갑의 커프를 잡은 두 손"></details><p><a href="README.md">제작 기록</a> · <a href="generation_log.json">생성 로그</a> · <a href="review_summary.json">검수 기록</a> · <a href="completed_ui.jpg">Flow 완료 화면</a></p></html>'''
(RUN/'originals.html').write_text(page,encoding='utf-8')

path=ROOT/'README.md'
raw=path.read_bytes().decode('utf-8-sig')
nl='\r\n' if '\r\n' in raw else '\n'
lines=raw.splitlines()
idx=[i for i,s in enumerate(lines) if s.startswith('최신 제작 상태:')]
assert len(idx)==1
lines[idx[0]]='최신 제작 상태: [새 3번 「환경까지 가져왔습니다」 커프 정돈 보완 원본·검수](storyboards/2026-10-20_C03-flow-run06/). **새 원본 1개 / 전체 원본 18개 / 이번 사용 10·현재 계정 잔액 0**. 새 첫 프레임에서 이미 낀 장갑의 커프를 당기는 동작으로 줄여, 3인 시각 표본 검수상 사용 후보를 확보했습니다. 전체 삽입·탈착 성공이나 C03 최종 완성은 아닙니다. [8초 원본 보기](storyboards/2026-10-20_C03-flow-run06/originals.html) · [이전 7.5초 편집 대안](storyboards/2026-10-20_C03-flow-run05/originals.html).'
path.write_bytes((nl.join(lines)+nl).encode('utf-8'))

resume=ROOT/'RESUME_CODEX.txt'
heading='[2026-10-20 C03 커프 정돈 run06 — 추가1회/시각표본사용후보/잔액0]'
old=resume.read_bytes()
if not old.decode('utf-8-sig').startswith(heading):
    intro=heading+'''
최신 사용자 “10크레딧 남았으니까 한번 더 시도해봐”가 이전 중단 권고보다 우선하여 Lite1회 추가 승인. 같은 /u/3 계정/프로젝트 ae9e0683-9828-484b-a182-68bb08987cdb. 실제잔액10→0, 환불0, 중복0. 화면갱신문구 '매일 오전11:11' 관측이며 자정갱신추정금지.
run06=storyboards/2026-10-20_C03-flow-run06. 내장imagegen새첫PNG1장: 양손이미장갑/오른손목피부/왼손이오른커프집기. 원안손등중간노출보다커프손목가까워 '착용마무리·커프정돈'으로PD축소. 3명 실제PNG 독립/교차PASS 뒤 firstframe만/16:9/720p/8초/x1/Lite10. 종료이미지없음. 정확프롬프트/입력해시/시각은generation_log.json. 무음반환임시ON후OFF실제복구.
원본 C03_K04_insert_take05.mp4, assetID1bb48bb9-ed0f-4c72-b540-5f075a9ef700, 8초1280x72024fpsH264/오디오트랙없음.192프레임디코딩·다운로드SHA일치. SHA d6c31fdef71a05c75bcc07c63ad64f0d18fb201b3e4b88fce4c96414af33f0cc. 원본재인코딩없음. 총C03원본18개.
3명실제32표본+개별PNG독립/교차검수상 커프정돈PASS사용후보.2.5~3.25초천경계소매쪽이동/손목덮기,약5~5.25초손분리,2손2장갑유지. 이전빈장갑합침/피부재질변형미발견. PD권장2.25~5.75초(3.5초)이나트림본은아직미생성. 연속재생호흡미검증. 전체맨손삽입·탈착문제해결로기록금지;K03탈착은여전히HOLD,맨손→커프정돈은중간과정생략편집필요. 기존run05편집대안불변/C03전체편집미완성.
원본페이지 run06/originals.html 및 C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/run06/originals.html. 로컬HTML정적링크검사만/UI렌더확인아님. Git반영은실제remote확인후보고. 현재입력창비움/Lite/무음반환OFF. 구매·업스케일·계정전환·예약재개·공개게시없음. 기존V8/legacyC01/이전원본보존. 아래run05잔액10/17원본보다위기록우선.

'''
    resume.write_bytes(intro.replace('\n','\r\n').encode('utf-8')+old)
brief=ROOT/'team/brief.toml'
data=brief.read_bytes()
if b'[production_C03_2026_10_20_cuff_finish]' not in data:
    addition='''

[production_C03_2026_10_20_cuff_finish]
user_request = "남은10크레딧으로1회더시도 명시승인."
run = "storyboards/2026-10-20_C03-flow-run06"
status = "새부분착용PNG1장/커프정돈동작Lite10한번, 실제10→0, 원본1개보존/누적18."
review = "3인실제PNG·영상표본독립/교차완료. 커프천이손목덮고손놓기PASS후보. 권장2.25~5.75초, 아직트림하지않음. 전체삽입·탈착해결아님/연속재생미검증."
scope = "C03전체미완성, 기존run05편집대안불변. 무음반환OFF복구, 구매·계정전환·예약재개·공개게시없음."
'''
    brief.write_bytes(data+addition.replace('\n','\r\n').encode('utf-8'))
tomllib.loads(brief.read_text(encoding='utf-8-sig'))

files=['originals.html','README.md','generation_log.json','review_summary.json','completed_ui.jpg',STEM+'.mp4',STEM+'_poster.png',STEM+'_contact.jpg','images/C03/K04_finish_insert01.png']
for name in files:
    dest=CACHE/name
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(RUN/name,dest)
    assert sha(dest)==sha(RUN/name)
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,val in attrs:
            if key in ['src','href','poster']:
                assert (RUN/val).is_file(),val
                assert (CACHE/val).is_file(),val
Links().feed(page)
for path in RUN.rglob('*.json'):
    json.loads(path.read_text(encoding='utf-8-sig'))
print(json.dumps({'original_preserved':True,'frames_decoded':192,'audio':False,'credits':0,'reviews':'3 independent + 3 cross','candidate':'cuff adjustment only','static_links_valid':True},ensure_ascii=False))
