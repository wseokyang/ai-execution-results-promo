# 시작 이미지 제작 계약

최종 `storyboards.json`의 `generation_units`가 입력이다. 이미지 담당자는 총괄이 지정한 안만 소유한다. 같은 작업 폴더에서 다른 담당자도 일하므로 타인의 파일을 바꾸거나 되돌리지 않는다. 하위 팀을 만들지 않는다.

1. `imagegen` 스킬을 읽고 내장 `image_gen`으로 이미지 하나당 요청 하나를 실행한다. 이미 존재하는 PNG를 복사하는 것으로 새 생성을 대체하지 않는다. API/CLI 전환은 승인되어 있지 않다.
2. 참조 파일은 사용 전에 `view_image`로 실제 열어 본다. 승인된 인물·복장·공간의 개성을 유지하고, 같은 안의 새 기준 이미지도 실제 참조해 연속성을 맞춘다.
3. 16:9 가로 화면, 단일 영화 프레임. 대사·행사 제목·자막·워터마크·컷 번호·콜라주 금지. 문서/모니터의 정확한 글과 도식은 별도 후편집할 수 있는 평평한 면을 확보한다.
4. 각 단위의 **동작 직전 첫 상태**를 만든다. 인물이 이미 쓰러져 있거나 목마가 이미 열려 있는 등 반전 이후 상태로 바꾸지 않는다. 인물, 손, 소품의 개수와 이동 경로를 확인한다.
5. 결과를 실제 열어 보고 필요한 국소 오류는 내장 도구로 수정한다. 파일 복사 외 재인코딩·리사이즈·사진 편집으로 생성물을 대체하지 않는다. 첫 결과와 수정 결과를 모두 보존한다.
6. 새 PNG는 `images/Cxx/Sxx.png`로 저장한다. C05 K02는 `S02A.png`, `S02B.png`. 재생성 수정은 `_v2` 등 새 이름을 붙인다. `source_generated_path` 원본과 복사본의 SHA256이 같아야 한다.
7. 각 안의 기록 파일은 `artist_Cxx.json` 하나다. 다른 안의 기록이나 통합 manifest는 수정하지 않는다. 진행될 때마다 저장하여 중단 후 이어갈 수 있게 한다.

기록 형식:

```json
{
  "concept_id": "C01",
  "expected_images": 9,
  "images": [{
    "id": "C01_K01",
    "concept_id": "C01",
    "scene_id": "S01",
    "linked_cut": "K01",
    "image_path": "images/C01/S01.png",
    "source_generated_path": "C:/.../generated_images/...png",
    "generation_tool": "image_gen",
    "prompt": "exact submitted prompt",
    "referenced_image_paths": ["actual path used"],
    "next_motion": "...",
    "camera_notes": "...",
    "sha256": "...",
    "dimensions": [1536,864],
    "artist_review": {"opened_actual_image": true, "status": "candidate", "notes": ["actual observations"]},
    "attempts": []
  }]
}
```

주의: C01 K04는 전체 체육관이나 모니터 테두리가 없는 **모니터 내부용 동영상 시작 화면**을 독립 생성한다. P의 외형·셔츠·자세·의자·매트가 동일해야 한다. 나중에 모니터 안에 합성한다.

C05 K02B는 기둥을 바닥에 내려놓았고 아직 몸을 접지 않은 독립 기준 이미지로 새로 만든다. 실제 후속 Flow 제작에서는 채택된 K02A의 끝 프레임과 대조하여 그 실제 끝 프레임을 시작으로 쓰거나 보정해야 한다. 이 기준 PNG만으로 A→B 연속성 검증을 완료했다고 쓰지 않는다.

Flow·음원·영상 생성·로그인·크레딧 확인은 이번 이미지 담당 범위에 없다. 완료를 기다리는 동안 모든 이미지를 성공했다고 미리 보고하지 않는다.
