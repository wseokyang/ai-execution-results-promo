# C01 · 55초 편집본 v02 · 발표자 음성 교체

[교체 편집본](C01_review_edit_v02_55s.mp4) · [새 음성 원본 WAV](C01_K04_D_qwen_take01.wav)

사용자는 v01의 K02·K06 대사와 말끝이 자연스럽다고 직접 확인했고, K04 Microsoft Heami 임시 목소리는 교체를 요청했다. 이 두 답변을 다른 대사의 청취·전체 립싱크 승인으로 확대하지 않는다.

K04 화면 밖 발표자 D의 “제가 헤맨 과정도 같이 보여드릴게요.”를 기존 Flow 합성 발표자 음성을 참고한 로컬 Qwen3-TTS 0.6B-Base 출력으로 교체했다. 새 음성은 24kHz 모노 PCM WAV, 2.48초이며 편집본 22.000–24.480초에 배치했다. 속도나 피치를 강제로 변경하지 않았다. 새 목소리는 사용자에게 샘플을 전달했고 수용 여부를 기다린다.

영상 스트림은 v01에서 그대로 복사했다. 컷·자막·엔딩의 압축 영상 패킷 SHA256이 이전과 동일하며 전체 디코딩에 성공했다. 오디오 트랙은 K04 21–27초의 기존 주변 소리에 새 대사를 혼합한 뒤 AAC로 인코딩했다. 그 밖의 대사 내용과 길이는 유지한다. 기존 v01과 모든 Flow 원본은 보존했다.

음성 참조는 run05 `C01_K06_take01.mp4`의 4.5–6.3초, 이미 합성된 허구의 발표자 D다. 로컬에서만 처리했으며 Flow 추가 생성·크레딧 사용·외부 유료 API 호출은 없다. 참조 음성이 1.8초로 짧아 음색 일치·자연스러움은 결과 청취로 판단해야 한다. 자동 전사는 새 문장의 모든 단어를 검출했지만 실제 청취나 품질 승인을 대신하지 않는다.

로컬 도구는 별도 캐시 환경 `C:/Users/wseok/.cache/codex-media-tools/qwen-tts-env`에 설치했다. 모델도 같은 캐시의 models 아래에 있으며 저장소에 포함하지 않는다. GTX1660SUPER에서 FP16 샘플링이 실패해 FP32로 바꾼 뒤 합성에 성공했다. 출력 전 실패 시도는 `voice_attempts.json`에 기록한다.

재현 자료:

- `generate_voice.py`, `voice_generation_log.json`, `local_voice_requirements.txt`
- `replace_voice.py`, `edit_manifest.json`, `media_info.txt`
- `user_feedback.json`, `voice_asr.json`, `reference_asr.json`

모델·API 근거: [공식 저장소](https://github.com/QwenLM/Qwen3-TTS), [공식 모델 카드](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base). Qwen3-TTS 코드와 공개 모델은 Apache-2.0이다.
