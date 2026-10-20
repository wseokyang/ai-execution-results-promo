"""Package the already-generated run05 files; never contacts Flow or changes media."""
import hashlib
import html
import json
import shutil
import tomllib
from pathlib import Path
from html.parser import HTMLParser

RUN = Path(__file__).resolve().parent
ROOT = RUN.parent.parent
CACHE = Path('C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/run05')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

log = read_json(RUN / 'generation_log.json')
review = read_json(RUN / 'review_summary.json')
edit = read_json(RUN / 'edit_manifest.json')
for req in log['requests']:
    stem = Path(req['original_mp4']).stem
    meta = read_json(RUN / f'{stem}_inspection.json')
    original = RUN / req['original_mp4']
    assert sha(original) == meta['sha256'] == sha(Path(req['download_source']))
    assert meta['full_video_decode_pass'] and meta['decoded_video_frames'] == 192
    req['status'] = 'completed_original_preserved_physical_action_hold'
    req['technical_metadata'] = meta
    req['original_reencoded'] = False
    req['download_sha256_matches'] = True
    req['input_start_sha256'] = sha(RUN / req['input_start'])
    req['input_end_sha256'] = sha(RUN / req['input_end'])
    req['submitted_prompt_exact'] = (RUN / req['prompt_file']).read_text(encoding='utf-8-sig')
    req['actual_audio_listening'] = False
    req['review_record'] = 'review_summary.json'
    req['state_only_used_seconds'] = [6, 6.75]
    req['defect'] = ('Wrong glove removal, finger material disappearance and swapped glove states; no physical right-glove removal.'
                     if req['cut_id'] == 'C03_K03' else
                     'Separate glove merges into left glove, then right hand becomes gloved without insertion.')
log.update({
    'status': 'closed_two_originals_quality_hold_review_edit_available',
    'ending_credits': 10,
    'net_credits_used': 30,
    'refunds_observed': 0,
    'generation_requests': 2,
    'pending_generation_requests': 0,
    'new_originals': 2,
    'c03_total_originals': 17,
    'final_ui_settings': {'model': 'Veo 3.1 Lite', 'silent_fallback': False, 'composer': 'empty'},
    'final_ui_evidence': 'completed_ui.jpg',
    'credit_observation': 'Actual UI balance observed 40,30,10; final10 reconfirmed. No reset assumed.',
    'method_change_outcome': 'Both endpoint images were accepted. Lite removal and Fast wearing completed technically but did not produce valid physical actions. No reverse derivative and no further retry.',
    'editorial_alternative': 'C03_K03_K04_state_edit_review_7p5s.mp4',
    'final_film_complete': False,
    'review': 'Three independent and cross reviews completed; actual sample images inspected. No actual audio listening or continuous-playback claim.'
})
write_json(RUN / 'generation_log.json', log)

edit_meta = read_json(RUN / 'C03_K03_K04_state_edit_review_7p5s_inspection.json')
assert sha(RUN / edit['output']) == edit_meta['sha256']
assert edit_meta['full_video_decode_pass'] and edit_meta['decoded_video_frames'] == 180
for src, digest in edit['original_sha256'].items():
    assert sha(Path(src)) == digest
edit.update({
    'review_status': 'Three-reviewer independent and cross sampled visual review passed for a review-only alternative; final adoption pending.',
    'review_record': 'review_summary.json',
    'technical_metadata': edit_meta,
    'physical_actions_solved': False,
    'actual_audio_listening': False,
    'continuous_playback_review': False,
    'user_accepted': False
})
write_json(RUN / 'edit_manifest.json', edit)

entries = [
    ('C03_K03_K04_state_edit_review_7p5s', '7.5초 편집 대안 · 검토용', '장갑 변형을 빼고 맨손·빈 장갑 → B 공개 → 양손 장갑 상태로 연결했습니다. 실제 탈착 과정은 생략했으며 C03 최종본이 아닙니다.', '00_0.000s.png'),
    ('C03_K03_insert_take02', 'K03 탈착 보완 원본 · Lite 10', '8초 원본 그대로. 반대 손의 장갑을 벗기고 재질이 바뀌므로 동작 사용 보류. 6–6.75초의 정상 후상태만 편집 대안에 사용했습니다.', '24_6.000s.png'),
    ('C03_K04_insert_take04', 'K04 착용 보완 원본 · Fast 20', '8초 무음 원본 그대로. 빈 장갑이 합쳐진 뒤 오른손에 장갑이 생겨 동작 사용 보류. 6–6.75초의 양손 장갑 상태만 편집 대안에 사용했습니다.', '24_6.000s.png')
]
cards = []
for stem, title, description, poster_frame in entries:
    poster = f'{stem}_poster.png'
    shutil.copy2(RUN / 'frames' / stem / poster_frame, RUN / poster)
    cards.append(f'<article><h2>{html.escape(title)}</h2><p>{html.escape(description)}</p><video controls playsinline preload="metadata" poster="{poster}" src="{stem}.mp4"></video><p><a download href="{stem}.mp4">MP4 다운로드</a> · <a href="{stem}_contact.jpg">검수 표본</a></p></article>')
gallery = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>C03 장갑 보완 run05 · 원본과 편집 대안</title><style>
body{font-family:system-ui,sans-serif;background:#11151d;color:#edf1f7;max-width:1050px;margin:40px auto;padding:0 20px;line-height:1.7}h1{line-height:1.3}a{color:#8ec9ff}article{border:1px solid #344355;border-radius:16px;padding:20px;margin:28px 0;background:#19222d}video{display:block;width:100%;max-height:70vh;background:#000}.note{padding:16px;border-left:4px solid #ffcf76;background:#292519}small{color:#abb9ca}
</style><h1>C03 「환경까지 가져왔습니다」<br>장갑 보완 · run05</h1><p>2026-10-20 · 새 원본 2개 · 30크레딧 사용 · 현재 계정 잔액 10</p><p class="note">장갑을 실제로 벗고 끼는 동작은 두 원본 모두 실패했습니다. 맨 위 영상은 변형 구간을 제외한 <strong>7.5초 편집 대안</strong>입니다. 3명 독립·교차 표본 검수에서 상태 연결을 확인했지만 실제 청취·립싱크·실시간 호흡은 미검증이며, C03 최종 완성본이 아닙니다.</p>'''
gallery += '\n'.join(cards)
gallery += '<p>기존 대사를 유지하고 K04 구간 음량만 조정했습니다. 새 음악·음성 합성은 없습니다. 생성 원본은 재인코딩하지 않았습니다.</p><p><a href="README.md">기록</a> · <a href="generation_log.json">생성 로그</a> · <a href="review_summary.json">독립·교차 검수</a> · <a href="edit_manifest.json">편집 구간</a> · <a href="completed_ui.jpg">Flow 완료 화면</a></p></html>'
(RUN / 'originals.html').write_text(gallery, encoding='utf-8')

readme = '''# C03 장갑 보완 run05 — 원본 2개와 7.5초 편집 대안

**장갑 탈착 동작은 미해결입니다.** 시작·끝 이미지를 함께 지정해 Lite 탈착 1회와 Fast 착용 1회를 생성했지만, 두 영상 모두 장갑 재질 변형이 남았습니다. 추가 요청을 멈추고 현재 계정의 **10크레딧을 보존**했습니다.

[원본·편집 대안 재생 페이지](originals.html)

| 파일 | 모델·비용 | 실제 결과 |
| --- | --- | --- |
| [K03 insert take02 원본](C03_K03_insert_take02.mp4) | Lite 10 · 40→30 | 8초 720p 24fps, AAC 트랙 있음. 반대 손 탈착·재질 변형으로 동작 HOLD |
| [K04 insert take04 원본](C03_K04_insert_take04.mp4) | Fast 20 · 30→10 | 8초 720p 24fps, 오디오 없음. 빈 장갑 합침·재질 생성으로 동작 HOLD |
| [7.5초 검토용 편집](C03_K03_K04_state_edit_review_7p5s.mp4) | 로컬 편집 · 추가 크레딧 0 | 7.5초 720p 24fps, 기존 음성 유지. 상태 변화만 보여주는 대안 |

## 편집 대안

기존 K03 0–2.5초 → 새 탈착본 6–6.75초 → 기존 K04 take02 0–3.5초 → 새 착용본 6–6.75초. 실제 동영상의 정상 후상태 부분을 연결했으며, 움직이는 정지 이미지로 대체하지 않았습니다. 두 장갑 동작의 성공을 뜻하지 않습니다.

오디오는 기존 K03 0–3.25초와 기존 K04 0–4.25초를 사용했습니다. K04 gain 0.7 외 새 합성·음악은 없으며, 새 인서트의 소리는 사용하지 않았습니다. 실제 청취, 발음, 립싱크, 0.75초 구간의 실시간 가독성과 코미디 호흡은 미검증입니다.

## 확인한 범위

세 검수자가 실제 추출 프레임을 독립 검토한 뒤 다른 두 의견을 교차 검증했습니다. 원본 두 개는 물리적 행동 HOLD, 편집 대안은 표본상 새 필수 시각 결함 없음입니다. 이는 최종 채택이나 C03 완성 승인이 아닙니다. 원본 각 192프레임과 편집본 180프레임 디코딩을 통과했고, 다운로드·보존 원본의 SHA256이 일치합니다.

[생성 ID·제출 프롬프트·입력 이미지·차감](generation_log.json) · [검수 ID와 처리](review_summary.json) · [편집 구간·원본 해시](edit_manifest.json)

현재 C03 원본은 총 **17개**입니다. 전체 편집, K05/K06 연결, 음성 및 행사명 가독성 검증이 남았습니다. 같은 손 동작의 무변경 반복 생성은 하지 않습니다. 현 UI는 Lite, 무음 반환 OFF, 입력창 비움으로 마쳤습니다. 계정 전환·구매·업스케일·예약 재개·공개 게시 없음. 기존 V8와 legacy C01, 이전 원본은 보존했습니다.

![Flow 완료 화면](completed_ui.jpg)
'''
(RUN / 'README.md').write_text(readme, encoding='utf-8')

# Preserve existing root-document line endings and all prior handoff content.
root_readme = ROOT / 'README.md'
text = root_readme.read_bytes().decode('utf-8-sig')
newline = '\r\n' if '\r\n' in text else '\n'
lines = text.splitlines()
latest = '최신 제작 상태: [새 3번 「환경까지 가져왔습니다」 장갑 재보완 원본·검수](storyboards/2026-10-20_C03-flow-run05/). **새 원본 2개 / 전체 원본 17개 / 이번 작업 사용 30·현재 계정 잔액 10**. Lite 탈착과 Fast 착용 모두 손·장갑 변형이 남아 동작은 보류했습니다. 변형을 제외하고 전후 상태를 연결한 **7.5초 검토용 편집 대안**을 함께 저장했습니다. 실제 탈착 동작 성공이나 C03 최종 완성을 의미하지 않습니다. [편집 대안·원본 보기](storyboards/2026-10-20_C03-flow-run05/originals.html).'
indices = [i for i, line in enumerate(lines) if line.startswith('최신 제작 상태:')]
assert len(indices) == 1
lines[indices[0]] = latest
root_readme.write_bytes((newline.join(lines) + newline).encode('utf-8'))

resume = ROOT / 'RESUME_CODEX.txt'
old = resume.read_bytes()
heading = '[2026-10-20 C03 장갑 재보완 run05 — 원본2/동작HOLD/7.5초편집대안/잔액10]'
if not old.decode('utf-8-sig').startswith(heading):
    intro = heading + '''
최신 사용자 “보완 다시 해봐”에 따라 입력·모델을 바꿔 재시도. 같은 /u/3 현재 계정, 프로젝트 https://flow.google.com/u/3/project/ae9e0683-9828-484b-a182-68bb08987cdb . 사용자 동의 완료 상태를 유지했고 임의 계정 전환 없음.
run05=storyboards/2026-10-20_C03-flow-run05. 시작·끝 프레임 모두 지정, 8초/16:9/720p/x1. K03_insert_take02 Lite10 실제40→30, K04_insert_take04 Fast20 실제30→10. 두 요청 기술 완료/환불0/접수 중0. 동일 요청 중복 없음. 원본2개 모두 그대로 저장, 다운로드 SHA 일치 및 각192프레임 디코딩. 생성ID·정확프롬프트·입력해시·시각은 generation_log.json.
K03은 반대 장갑 탈착과 재질 변형/상태 교환, K04는 빈 장갑 합침 및 오른맨손→장갑 재질 생성. 두 물리적 행동 모두 HOLD. 역재생하지 않음. 3명 실제 표본 독립검수/상호교차/PD처리 완료, review_summary.json 기준. 입력 시작/끝 이미지는 기존run04에서 재사용했고 새 이미지 생성 없음.
검토용 C03_K03_K04_state_edit_review_7p5s.mp4: 기존K03 0–2.5→새K03 6–6.75→기존run03K04 0–3.5→새K04 6–6.75. 변형 과정 생략, 실제영상의 맨손·빈장갑→B공개→양장갑 상태 연결. 원안 탈착 성공/최종 채택 아님. 기존 대사 유지, K04 gain0.7, 새음원/BGM0. 7.5초720p24fps/AAC/180프레임 디코딩, 원본 해시 보존. 3명 렌더 표본 검수 및 교차상 새 필수 시각 결함 없음. 0.75초 실시간 가독성/호흡·실청취·발음·립싱크는 미검증.
C03 원본 총17개(이전15+이번2). 편집 대안은 파생본이며 원본 개수에 더하지 않는다. C03 전체는 미완성; K05/K06 연결, 음성·행사명 가독성·전체 편집 남음. 같은 손 동작 반복은 멈추고10 보존. 마지막 실제 UI 잔액10, Lite 선택/무음반환OFF/입력창비움. 구매·업스케일·계정전환·예약재개·공개게시 없음. 기존legacyC01/V8/이전원본 보존.
원본/검토본 페이지 run05/originals.html. Windows C:/Users/wseok/.cache/codex-flow/C03-v8-2026-10-20/run05/originals.html. 로컬HTML은 정적링크 검사만, UI렌더 확인 아님. Git 반영은 실제 remote 검증 후 보고. 아래run04 잔액40/15원본 상태보다 이 기록 우선.

'''
    resume.write_bytes(intro.replace('\n', '\r\n').encode('utf-8') + old)

brief = ROOT / 'team' / 'brief.toml'
brief_data = brief.read_bytes()
section = '[production_C03_2026_10_20_glove_retry]'
if section not in brief_data.decode('utf-8-sig'):
    addition = '''

[production_C03_2026_10_20_glove_retry]
user_request = "보완 다시 해봐. 같은 계정에서 방법을 바꾼 장갑 동작 재보완."
run = "storyboards/2026-10-20_C03-flow-run05"
status = "시작·끝 프레임 지정 Lite10 탈착 + Fast20 착용, 원본2개 보존. 실제40→30→10. 총17원본. 두 물리적 동작은 HOLD."
review = "3명 실제 표본 독립·교차 검수. 반대 손 탈착/빈 장갑 합침/재질 변형. 전후 상태만 연결한 7.5초 검토 편집은 표본상 사용후보, 원안 동작 성공·최종 C03 완료 아님."
scope = "10 보존, 반복 생성 중단. 실제청취·실시간 호흡·립싱크 및 전체 편집 미완료. Lite/무음반환OFF 복구. 기존원본/V8/legacyC01 보존. 구매·예약재개·공개게시 없음."
project_url = "https://flow.google.com/u/3/project/ae9e0683-9828-484b-a182-68bb08987cdb"
'''
    brief.write_bytes(brief_data + addition.replace('\n', '\r\n').encode('utf-8'))
tomllib.loads(brief.read_text(encoding='utf-8-sig'))

# Cache is a local display mirror; only explicitly enumerated run05 deliverables.
CACHE.mkdir(parents=True, exist_ok=True)
files = ['originals.html', 'README.md', 'generation_log.json', 'review_summary.json', 'edit_manifest.json', 'completed_ui.jpg']
for stem, *_ in entries:
    files += [f'{stem}.mp4', f'{stem}_poster.png', f'{stem}_contact.jpg']
for name in files:
    shutil.copy2(RUN / name, CACHE / name)
    assert sha(RUN / name) == sha(CACHE / name)

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src', 'poster'):
                self.paths.append(value)
links = Links()
links.feed(gallery)
for target in (RUN, CACHE):
    for rel in links.paths:
        assert (target / rel).is_file(), str(target / rel)
for item in RUN.rglob('*.json'):
    read_json(item)
print(json.dumps({'originals_preserved':2,'edit_seconds':7.5,'net_credits':30,'balance':10,'local_links':len(links.paths),'cache_files_verified':len(files),'json_toml_valid':True},ensure_ascii=False))
