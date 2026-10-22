# V10 이미지 제작 공통 계약

총괄이 지정한 안·씬만 담당한다. 다른 담당자도 같은 작업 폴더를 사용하므로 타인의 수정과 원본을 되돌리거나 덮어쓰지 않는다. 하위 팀을 만들지 않는다.

`storyboards.json`의 해당 `concepts`와 `generation_units`를 모두 읽는다. 기준은 최종 교차 검토된 컷의 **동작 전 첫 상태**다. 마지막 반전을 첫 프레임에서 미리 보여주지 않는다. 캐릭터·복장·동선·손에 든 물건을 앞뒤 컷과 맞춘다. 전체 컷을 한 장의 콜라주로 대체하지 않는다.

imagegen 스킬을 읽고 기본 내장 `image_gen`으로 씬마다 실제 PNG를 생성한다. API/CLI 사용 금지. 16:9, 자막·말풍선·행사명·읽을 수 있는 문서 글·로고·워터마크 없음. 미래 자막 위치는 빈 공간으로 확보한다. 과장된 연기는 유지하되 외모를 조롱하지 않는다. 첫 기준 씬을 만든 뒤 실제 파일을 열고 후속 씬에 참조로 사용한다. 새 씬의 구도·장소·상태를 이전 씬 그대로 복제하지 않는다.

각 도구 호출이 완료되면 `generatedImage(result)`로 실제 결과를 반환한다. 실제 생성 파일을 `images/<Cxx>/<Sxx>.png`로 바이트 그대로 복사한다. 수정안은 `_v2` 등 새 파일명으로 저장하고 이전 생성물도 보존한다. 실제 이미지를 열어 첫 상태·인물·손·소품·공간·반전 선공개 여부를 검사한다. 문제를 단순히 프롬프트에 기록하는 것으로 완료 처리하지 않는다.

담당 기록 파일은 총괄이 지정한다. 구조는 다음과 같다.

```json
{"concept_id":"C06","images":[{"id":"C06_K01","concept_id":"C06","scene_id":"S01","linked_cut":"K01","image_path":"images/C06/S01.png","source_generated_path":"C:/Users/wseok/.codex/generated_images/actual.png","generation_tool":"image_gen","prompt":"실제 최종 제출 프롬프트 전문","referenced_image_paths":[],"artist_review":{"opened_actual_image":true,"notes":"확인한 내용 및 한계"},"review_status":"artist checked; independent review pending"}]}
```

재시도 시 선택본은 images에, 이전 시도와 수정 이유는 별도 `attempts`에 기록한다. 파일을 하나씩 저장하고 기록을 갱신하여 중단돼도 결과를 잃지 않는다. 수정을 다른 담당자가 마친 이미지에 적용할 필요가 있으면 총괄에게 알린다.

Flow 업로드·영상·음원·계정·크레딧·Git 작업은 하지 않는다. 완성 시 생성 수, 실제 기록 경로, 남은 문제를 반환한다. 정지 이미지 검토를 실제 동작의 성공으로 보고하지 않는다.
