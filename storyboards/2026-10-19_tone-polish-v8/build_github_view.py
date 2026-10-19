from pathlib import Path
import json

R=Path(__file__).resolve().parent
ROOT=R.parent.parent
PREFIX=R.relative_to(ROOT).as_posix()

def main():
    status=json.loads((R/'delivery_status.json').read_text(encoding='utf-8'))
    assert status['status']=='complete'
    d=json.loads((R/'storyboards.json').read_text(encoding='utf-8'))
    rows=['# 전체 이미지 콘티 · V8','',
          '**1·3·5번은 그대로 유지하고, 2·4번의 대사와 연출을 다듬었습니다.**',
          '새 5안의 첫 프레임 43장과 각 컷의 대사·다음 행동입니다. 이번 수정은 콘티 단계이며, 이전에 완성한 1번 영상은 별도로 보존했습니다.','',
          '[1번](#c01) · [2번](#c02) · [3번](#c03) · [4번](#c04) · [5번](#c05)','',
          f'[HTML 원본과 이미지 폴더]({PREFIX}/) · [전체 컷 표]({PREFIX}/STORYBOARDS.md) · [검토 기록]({PREFIX}/review_summary.json)','',
          '2번: 진지한 체포극과, 자기 사진을 떼려다가 반듯하게 펴 주는 체면 유지.',
          '4번: 숨소리까지 금지한 잠입 작전과, 들킨 뒤에도 “지휘관부터.”라고 명령하는 태도.','']
    count=0
    for c in d['concepts']:
        rows += ['## '+c['id'],'',f"**{c['id'][-1]}번 · {c['title']} · {c['duration_seconds']}초**",'',c['logline'],'']
        for s in c['shots']:
            path=PREFIX+'/'+s['image_file']
            assert (ROOT/path).is_file()
            rows += [f"### {c['id']} {s['id']} · {s['start']}–{s['end']}초",'',
                     f"![{c['id']} {s['id']} 첫 프레임]({path})",'',
                     '**대사:** '+s['dialogue'],'',
                     '**다음 행동:** '+s['next_motion'],'',
                     '**소리·호흡:** '+s['sound'],'']
            count+=1
    assert count==43
    rows += ['---','',
             '새로 보완한 이미지는 C02 K01·C04 K09 두 장입니다. 다른 41장은 V7 원본을 재사용했습니다.',
             '행사명은 2026년 품질팀 AI 실행 결과 발표 대회입니다. 미확정 일시·장소·신청 방법·실적·상금은 넣지 않았습니다.',
             '인물과 사건은 허구이며 실제 동작·음성·립싱크·관객 반응을 검증한 결과는 아닙니다.']
    (ROOT/'콘티_바로보기.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    old=ROOT/'README_before_v8.md'
    if not old.exists():old.write_bytes((ROOT/'README.md').read_bytes())
    overview=PREFIX+'/overview.png'
    readme=f"""# AI 실행 결과 발표 대회 · 영상 기획

## [전체 이미지 콘티 바로보기 →](콘티_바로보기.md)

최신 **V8**입니다. 위 링크에서 **43장의 이미지와 대사**를 함께 읽을 수 있습니다.
1·3·5번은 유지했고, 2·4번은 대사·호흡과 인물의 체면을 지키는 행동을 보완했습니다.

![최신 5안 개요]({overview})

| 찾는 자료 | 바로가기 |
| --- | --- |
| 이미지와 대사를 한 화면에서 보기 | [전체 이미지 콘티](콘티_바로보기.md) |
| 이전에 전달한 형태의 HTML 원본 | [V8 index.html]({PREFIX}/index.html) |
| PNG 원본·HTML·프롬프트 전체 | [V8 폴더]({PREFIX}/) |
| 시간·자막·음향까지 포함한 컷 표 | [전체 컷 표]({PREFIX}/STORYBOARDS.md) |
| 바로 이전 V7 HTML | [V7 index.html](storyboards/2026-10-19_keep135-rebuild-v7/index.html) |
| 이전에 완성한 1번 영상 | [36초 최종본 MP4](storyboards/2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4) |
| 이전 버전과 원자료 안내 | [이전 README 기록](README_before_v8.md) |

HTML은 원본 파일로 보관합니다. 브라우저에서 열 때는 해당 버전의 폴더를 이미지 폴더와 함께 내려받아 index.html을 여세요. 저장소 안에서 바로 읽으려면 맨 위 **전체 이미지 콘티 바로보기**를 이용하세요.

비공개 저장소를 유지합니다. 이번 작업은 콘티와 첫 프레임까지이며 Flow 업로드·동영상·음원 생성은 하지 않았습니다.
"""
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
    assert (ROOT/'콘티_바로보기.md').read_text(encoding='utf-8').count('![')==43
    print({'github_view':'콘티_바로보기.md','inline_images':count,'README':'direct entry updated','history':'README_before_v8.md'})

if __name__=='__main__':main()
