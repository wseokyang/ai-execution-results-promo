"""Record observed Flow success without claiming a pending download is saved."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json

root=Path(__file__).resolve().parent
project=root.parent.parent
stamp=datetime.now(timezone(timedelta(hours=9))).isoformat()
p=root/'generation_log.json'
d=json.loads(p.read_text(encoding='utf8'))
d.update(status='voice_take01_generated_download_confirmation_pending',successful_outputs=1,downloaded_originals=0)
c=d['clips'][0]
c.update(generation_id='c76d6589-f550-4052-9a97-a7bab749e6ad',
         result_url=d['project_url']+'/edit/c76d6589-f550-4052-9a97-a7bab749e6ad',
         ui_title='C01_K04_D_voice_take01 · Lite · 편안한 발표',
         status='generation_success_download_confirmation_pending',
         ui_duration_seconds=8,observed_completion_at_kst=stamp,
         download={'ui_option':'720p 원본 크기','clicked':True,'status':'Chrome temporary file; user save/keep confirmation requested',
                   'temporary_file':'C:/Users/wseok/Downloads/18b7683e-01d1-4104-b08e-dd293265db58.tmp',
                   'final_path':None,'sha256':None},
         review={'actual_audio_listening':False,'asr': 'pending_completed_download','audio_track': 'unverified_until_original_saved'},
         proof='voice_take01_complete.png')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')

v3=project/'storyboards/2026-10-16_C01-tone-v03'
for name in ['user_feedback.json','edit_manifest.json','voice_generation_log.json','delivery_files.json']:
    p=v3/name
    d=json.loads(p.read_text(encoding='utf8'))
    d['current_voice_status']='provisional_fallback_pronunciation_improvement_requested'
    if name=='user_feedback.json':
        d['new_voice_approval']='initially_accepted_then_pronunciation_improvement_requested'
        d['flow_regeneration_needed']='user_requested_voice_source_audition_only; existing_motion_cuts_preserved'
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
p=v3/'README.md'
s=p.read_text(encoding='utf8')
s=s.replace('**K04 새 음성을 채택**했다.','**K04 새 음성을 일시 채택**했다. 이후 사용자가 발음이 아쉽다며 Flow 음성 생성을 요청하여, 현재 v03은 비교·복귀용 후보이고 발음 개선은 다시 진행 중이다. [최신 Flow 음성 후보](../2026-10-17_flow-run-07/README.md)를 우선 확인한다.')
p.write_text(s,encoding='utf8')

(root/'README.md').write_text('''# C01 K04 발표자 음성 · Flow Lite 비교

사용자는 v03의 발음 개선을 요청했고, 이번 음성 비교에는 Fast20보다 Lite10씩 최대5회 방식을 선택했다. 모든 반복이 필수는 아니며 결과를 확인한 뒤 필요한 경우에만 조정한다. 기존 C01의 7개 동작 컷은 재생성하지 않는다.

- 계정04 프로젝트: https://flow.google.com/project/1d89ebc4-606d-43e7-80be-6e6f4bcb2d63
- 첫 입력: 기존 C01_N07.png. 오른쪽 무대 D만 “제가 헤맨 과정도 같이 보여드릴게요.”를 말하도록 요청했다.
- Veo 3.1 Lite / Frames 시작만 / 16:9 / 720p / 8초 / x1 / 무음 반환 OFF.
- take01 생성 성공. 실제 잔액50→40, 차감10, 환불0. 추가 요청 없음.
- 생성ID c76d6589-f550-4052-9a97-a7bab749e6ad. [Flow 결과](https://flow.google.com/project/1d89ebc4-606d-43e7-80be-6e6f4bcb2d63/edit/c76d6589-f550-4052-9a97-a7bab749e6ad).
- **720p 원본 다운로드 확인 대기**. Chrome에 임시 파일만 보인다. 사용자에게 저장/유지 확인을 요청했다. 로컬 MP4 저장·오디오 검수 완료로 보고하지 않는다. 같은 요청을 다시 생성하지 않는다.

[완료 화면](voice_take01_complete.png) · [실제 제출 프롬프트](C01_K04_D_voice_take01_prompt.txt) · [생성 기록](generation_log.json) · [기존 대사 기술 검토](existing_dialogue_review.json).

현재 검수는 저장된 자동전사와 실제 트림 길이 비교이다. 직접 청취나 발음·자연스러움·립싱크 확인을 대신하지 않는다. 기존 K02·K06은 사용자가 자연스럽다고 확인했으므로 유지한다. 채택 K01·K05·K07에는 추가 생성이 필요한 확정 대사 누락/잘림 증거가 없었다. K05의 추가 음절은 ASR 불확실성으로 남긴다.

`inspect_voice.py`는 다운로드가 완료된 원본만 읽어 전체 디코딩·메타데이터·ASR을 기록하고 원본 AAC 추출 및 WAV/프레임을 만든다. 원본 MP4는 재인코딩하지 않는다. v03과 이전 원본은 보존한다. BGM 작업은 사용자 음성 우선 요청으로 준비 단계에서 보류했다.
''',encoding='utf8')

p=project/'RESUME_CODEX.txt'
raw=p.read_bytes()
old='실제50→40 차감 확인, 아직 완료/원본 저장 전.'.encode('utf8')
new='실제50→40 차감 확인. 생성은 성공(ID c76d6589-f550-4052-9a97-a7bab749e6ad, UI 8초). 720p 원본 다운로드 클릭 후 Chrome 임시 파일 상태로 사용자 저장/유지 확인 대기이며 로컬 원본/음성 검수 전이다.'.encode('utf8')
assert old in raw
p.write_bytes(raw.replace(old,new,1))
p=project/'README.md'
raw=p.read_bytes()
header=('## 최신 진행 · 2026-10-17 Flow 발표자 음성\r\n\r\n'
        '[K04 발표자 음성 take01](storyboards/2026-10-17_flow-run-07/README.md)을 Lite10으로 생성했습니다. 잔액50→40. Flow 생성은 완료됐고 Chrome 다운로드 확인 대기입니다. 기존11개 원본은 보존했으며 새 원본 저장·음성 검수 완료로 보고하지 않습니다. v03은 발음 개선 요청에 따라 비교용 후보로 남겼습니다.\r\n\r\n').encode('utf8')
needle=b'## '
i=raw.index(needle)
p.write_bytes(raw[:i]+header+raw[i:])
print('Recorded successful generation and pending original download; v03 latest status reconciled.')
