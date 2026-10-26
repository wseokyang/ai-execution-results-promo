"""Build latest delivery navigation; does not render or regenerate media."""
from pathlib import Path
import json, hashlib, html, re

E=Path(__file__).resolve().parent
ROOT=E.parent.parent
F=ROOT/'storyboards/2026-10-26_C08-C09-flow-v15'
S=ROOT/'storyboards/2026-10-26_screening-style-v15'
N=ROOT/'storyboards/2026-10-26_C01-C07-C10-rewrite-v15'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def md(p,t):p.write_text(t.strip()+'\n',encoding='utf-8')

films=read(S/'delivery_manifest.json')['films']
for f in films:
    f['file']=f['file'].replace('\\','/')
    f['technical_qa']=f['technical_qa'].replace('\\','/')
for cid,title in [('C08','구조는 끝났습니다'),('C09','나 없이도 괜찮겠어요?')]:
    m=read(E/cid/'edit_manifest.json')
    films.append({'concept_id':cid,'title':title,'file':rel(E/cid/m['file']),
        'duration_seconds':m['duration_seconds'],'sha256':m['technical_qa']['sha256'],
        'technical_qa':rel(E/cid/'technical_qa.json'),
        'actual_listening_verified':False,'actual_continuous_playback_verified':False})
for f in films:
    p=ROOT/f['file']; assert p.exists()
    assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],f['file']
assert [f['concept_id'] for f in films]==['C02','C03','C04','C05','C06','C08','C09']
save(E/'delivery_manifest.json',{'version':'V15','date':'2026-10-26','films':films,
    'screening_basis':'화면과 후처리 자막. 생성 음성 제외, BGM/효과음은 보조.',
    'review_records':[rel(S/'cross_review.json'),rel(E/'cross_review.json')],
    'actual_listening_verified':False,'actual_continuous_playback_verified':False})

# Preserve the previous root navigation before replacing it. No original media is changed.
A=ROOT/'archive/v14-root-before-v15'; A.mkdir(parents=True,exist_ok=True)
oldnames=['README.md','00_완성_영상.md','00_새7-10_콘티.md','콘티_바로보기.md',
    '00_영상제작_현재상태.md','00_최종_재검수.md',
    '01_성공_자세_교정원.md','07_불량도_이직합니다.md','10_비법_공개_금지.md']
for name in oldnames:
    target=A/name
    if not target.exists():
        src=ROOT/name
        if src.exists():
            t=src.read_text(encoding='utf-8')
            t=re.sub(r'\]\((?!https?:|#)([^)]+)\)',lambda m:'](../../'+m.group(1)+')',t)
            target.write_text(t,encoding='utf-8')

rows=['| 작품 | 상영용 MP4 | 길이 |','|---|---|---:|']
for f in films:
    rows.append(f"| {f['concept_id']} · {f['title']} | [영상 열기]({f['file']}) | {f['duration_seconds']:g}초 |")
table='\n'.join(rows)
md(ROOT/'00_완성_영상.md',f'''# Q-AI Fair · 최신 7편 V15

2026-10-26 기준 상영 선택작은 **2·3·4·5·6·8·9번**입니다. 기존 1번은 선택에서 제외했고, 새 1·7·10번은 콘티 단계입니다. 원본과 이전 편집본은 보존했습니다.

{table}

GitHub에서 재생기가 없으면 파일 화면의 다운로드 버튼으로 원본 편집 MP4를 받으세요. 모두 1280×720, 24fps, 화면+후처리 자막 중심이며 음성 대사를 듣지 않아도 이야기가 이어지도록 구성했습니다.

- **8번:** 구조대 투입 → 공유 AI 양식 적용·사람 확인 → 벽돌 일자리 반전. 벽돌 삽입·손 떼기와 같은 벽돌 미세 수정을 새 테이크로 보완했습니다.
- **9번:** 휴가 인사 → 탑승 → 다시 호출 → 충전기 반환 → 버스만 출발. 실제 탑승·전달·떠나는 버스를 사용했습니다. 주머니에서 꺼내는 과정과 문 닫힘·출발 시작은 편집에서 생략했습니다. 전달은 실제 움직이는 1.75초 확대 컷이라 주변 컷보다 선명도가 낮습니다.
- **2~6번:** 엔딩 행사 설명·자막 대비·안전영역·음량을 통일했습니다. 3번에 BGM을 추가했습니다. 5번의 기존 자세·날씨 변화는 작업자 컷을 통한 시간 생략으로 남아 있습니다.

**검수 범위:** 세 검수자의 실제 추출 프레임·접합·자막 검토, 전체 디코딩·시간축·음량·해시 확인을 완료했습니다. 실제 청취, 실시간 연속 재생과 현장 상영은 검증하지 않았습니다. 청감까지 완전 검수했다는 의미는 아닙니다.

[제작·검수 상세](00_V15_제작_검수.md) · [25개 Flow 원본]({rel(F/'README.md')}) · [7편 파일·SHA 목록]({rel(E/'delivery_manifest.json')}) · [새 1·7·10 콘티](00_새1-7-10_콘티.md)
''')

newboards=[('C01','감독님, 아직인데요','01_감독님_아직인데요.md',37.5,10,'성급한 축하를 멈춘 뒤, 마지막 꽃가루가 감독에게 돌아오는 광고 촬영장 코미디.'),
    ('C07','셰프님, 그것도 주세요','07_셰프님_그것도_주세요.md',32.6,9,'완성된 결과보다 실패·수정 기록을 탐내는 미식 심사위원들의 의자 경쟁.'),
    ('C10','지구 대표, 질문 있습니다','10_지구_대표_질문_있습니다.md',38,8,'외계인의 첫 질문은 첫 오류 줄. 인간의 수정 기록은 더 크게 쏟아진다.')]
brows=['| 새 안 | 이야기 | 길이 / Flow 동작 컷 |','|---|---|---|']
for cid,title,name,secs,n,desc in newboards:
    brows.append(f'| [{cid} · {title}]({name}) | {desc} | {secs:g}초 / {n}개 |')
btable='\n'.join(brows)
md(ROOT/'00_새1-7-10_콘티.md',f'''# 새 1·7·10 콘티 · V15

기존 세 이야기를 교체했습니다. 각 안의 컷 표, 후처리 자막, 음악·효과음, 전환, 모든 씬 첫 프레임은 아래 문서에서 바로 볼 수 있습니다. **총 27개 개별 첫 프레임이며 이 세 안의 Flow 영상은 아직 생성하지 않았습니다.**

{btable}

각 안은 5초 엔딩을 포함합니다. 모든 설명은 화면과 후처리 자막으로 전달하고 음성 대사는 넣지 않습니다. 인물의 체형·연령·헤어·의상과 장르를 세 안 사이에서 구분했습니다. 실제 인물·광고 장면을 복제하지 않고 장르의 진지함, 사건 확대, 두 번째 반전을 활용한 독립 이야기입니다.

[전체 첫 프레임 보기](콘티_바로보기.md) · [이미지·프롬프트 대응표]({rel(N/'scene_manifest.json')}) · [콘티 검토]({rel(N/'review_rounds.json')}) · [이미지 교차 검토]({rel(N/'image_review.json')})

7번은 ‘잠시 후’ 이후의 테이블·의자 위치를 통일했고, 10번 마지막 장면의 케이스 지지팔을 수정했습니다. 1번은 축포 방향과 발판을 밟는 순서까지 후속 동작 명세에 적었습니다. 이미지 검수는 실제 영상의 물리적 동작 성공을 보장하지 않습니다.
''')

md(ROOT/'README.md',f'''# Q-AI Fair · 최신 영상 7편과 새 콘티 3안

**[상영용 7편](00_완성_영상.md)** · **[새 1·7·10 콘티](00_새1-7-10_콘티.md)** · **[전체 첫 프레임 보기](콘티_바로보기.md)** · **[제작·검수](00_V15_제작_검수.md)**

2026-10-26 V15. **8·9번 Flow 생성·자막·BGM 편집을 완료**했습니다. 상영 선택작은 **2·3·4·5·6·8·9**입니다. 이 7편의 행사명, 엔딩 설명, 자막과 음량을 재점검했습니다.

{table}

## 새로 작성한 1·7·10번

{btable}

세 안의 첫 프레임 27장을 생성하고 교차 검수했습니다. 이 세 안은 **콘티·이미지 단계**입니다.

이번 Flow 원본은 **25개(계획 20컷 + 보완 5테이크)**, 실제 사용 **250크레딧**, 확인한 **5개 계정 잔액 모두 0**입니다. 계정별 갱신 시각은 달랐으며, 자정 갱신이나 전액 소진이 초기화 조건이라는 뜻은 아닙니다. [원본·정확한 프롬프트·차감 기록]({rel(F/'README.md')})

추출 프레임·자막·접합 및 디코딩·음량 수치는 검수했습니다. **실제 청취와 실시간 연속 재생은 미검증**입니다. 9번의 일부 동작 생략과 5번의 기존 연속성 한계는 [검수 기록](00_V15_제작_검수.md)에 공개했습니다.

<details><summary>이전 버전과 원자료</summary>

[이전 루트 안내](archive/v14-root-before-v15/) · [모든 원본·편집 버전](storyboards/) · [초기 원자료](archive/README.md)

</details>
''')

md(ROOT/'00_V15_제작_검수.md',f'''# V15 제작·검수 기록

최신 상영 세트: **C02/C03/C04/C05/C06/C08/C09**. 새 C01/C07/C10은 콘티와 첫 프레임만 제작했습니다. 자동 생성 예약은 PAUSED 상태를 유지했습니다.

## 실제 생성·크레딧

- C08 10컷 + 2개 보완 테이크, C09 10컷 + 3개 보완 테이크: 총 25개 원본 MP4.
- 매 요청 Veo 3.1 Lite, 10크레딧, 16:9, 720p, 8초, x1을 확인했습니다. 전체 250크레딧 차감, 5개 계정 각각 50→0을 관측했습니다. 실패·환불 0, 구매·구독 변경·유료 업스케일 0입니다.
- 25개 원본을 재인코딩 없이 저장했고, 정확한 프롬프트·입력 이미지·생성 ID·잔액·해시를 [generation_log]({rel(F/'generation_log.json')})에 남겼습니다. 계획 20컷을 처음부터 모두 성공한 것으로 기록하지 않습니다.
- 원본 전체 8초/192프레임/1280×720/24fps 영상 디코딩을 확인했습니다. 원본 오디오는 편집에서 모두 제외했습니다.

## 자막·BGM 정리

- 화면과 후처리 자막이 서사를 전달합니다. 행사명은 Q-AI Fair, 설명은 ‘품질팀 AI 성과 교류회’입니다. 행사 일시·장소·숫자는 만들지 않았습니다.
- 엔딩 유지 시간은 기존 편 4.75~6초, 새 8·9번 각 5초입니다. 본문 42px 기준, 고대비 글자/배경과 안전영역을 사용했습니다. 작품별 장르 색은 보존했습니다.
- C03에는 새 로컬 실내악 BGM을 추가했습니다. C02/C04는 기존 AAC를 보존했고 C05/C06은 각각 -1.15/-1.99dB 조정했습니다. C08/C09는 새 로컬 기악 BGM과 필요한 최소 효과음으로 편집했습니다.
- 통합 음량은 일곱 편 모두 약 -23 LUFS이고 실제 최대 피크는 -3dBTP보다 낮습니다. 전체 음향 디코딩과 시간축 공백, 비정상 수치, 말단 길이도 확인했습니다. **음량 지표는 실제 음색·효과음 청취 판단을 대신하지 않습니다.**

## 동작 검수와 남긴 한계

| 안 | 반영 / 판단 |
|---|---|
| C02 | 엔딩 장식선이 글자를 가로지르지 않게 테두리로 이동. 기존 수갑 동작의 미세한 형태 변화는 유지. |
| C03 | 발견 자막의 글자/박스 좌표를 구분해 기록. 새 BGM과 엔딩 설명 대비 확인. |
| C04 | 최신 V14 호흡과 숟가락 동작 유지, 자막·엔딩 재확인. |
| C05 | 작업자 컷으로 이어지는 기존 시간 생략 유지. 완전한 몸 회전·하중 이전이 연속으로 생성됐다는 뜻은 아니며 자세·날씨 차이가 남음. |
| C06 | 최신 V14 감사 자막 위치 및 타격 시점 유지, 음량 재조정. |
| C08 | 벽돌 빈자리 삽입 후 손 떼기와 동일 벽돌 미세 수정은 take02로 교체. UI 위 손/종이 가림과 확인 자막, 엔딩 표본 확인. |
| C09 | take02 탑승 완료. K07 주머니 인출 오류는 source4.5–6.5초의 이미 든 충전기 공개만 사용. K08 실제 전달 source1.5–3.25초를 확대 사용하며 여성 오른손 수령·해상도 손실을 기록. K09 문 닫힘/출발 초반은 제외하고 source3.5–6.5초의 멀어지는 버스만 사용. |

세 독립 검수자가 실제 렌더 추출 프레임과 자막·주요 접합을 본 뒤 서로 지적을 교차 검증했습니다. [기존 2~6 검수]({rel(S/'cross_review.json')}) · [새 8·9 검수]({rel(E/'cross_review.json')})

실시간 전체 연속 재생, 실제 청취, 현장 상영과 관객 반응은 검증하지 않았습니다. 로컬 영상의 자동 브라우저 관찰이 URL 정책에 막힌 것을 다른 경로로 우회하지 않았습니다. 따라서 ‘모든 소리와 움직임이 완벽하다’는 최종 상영 보증은 하지 않습니다.

## 새 1·7·10

3인 콘티 독립·교차 검토 후 개별 첫 프레임 27장을 제작했습니다. 이미지 교차에서 C07의 테이블/의자 위치와 C10 마지막 지지팔을 찾아 수정했습니다. [새 콘티](00_새1-7-10_콘티.md) · [이미지 기록]({rel(N/'image_review.json')})
''')

gallery=['# Q-AI Fair · 검수할 콘티와 첫 프레임','','[최신 영상 7편](00_완성_영상.md) · [새 1·7·10 컷 표](00_새1-7-10_콘티.md)','','이 문서는 최신 새 세 안의 실제 씬 이미지를 모두 보여 줍니다. 2·3·4·5·6·8·9번은 위 영상 링크가 최신 편집 결과입니다.']
for cid,title,name,secs,count,desc in newboards:
    mm=read(N/'manifests'/f'{cid}_images.json')
    gallery += ['',f'## [{cid} · {title}]({name})','',desc,'']
    for im in mm.get('images',mm.get('scenes',[])):
        gallery += [f"### {im['scene_id']}",'',f"![{cid} {im['scene_id']}]({im['image_path']})",'']
md(ROOT/'콘티_바로보기.md','\n'.join(gallery))

for name in ['00_영상제작_현재상태.md','00_최종_재검수.md']:
    md(ROOT/name,f'''# 최신 상태 안내

2026-10-26 최신 결과는 **[상영용 7편](00_완성_영상.md)**, **[V15 제작·검수](00_V15_제작_검수.md)**, **[새 1·7·10 콘티](00_새1-7-10_콘티.md)**입니다.

[이 문서의 이전 기록](archive/v14-root-before-v15/{name})
''')
md(ROOT/'00_새7-10_콘티.md', '''# 콘티 최신 위치

8·9번은 [영상 제작을 완료](00_완성_영상.md)했습니다. 7·10번은 1번과 함께 다시 작성했으며 [새 1·7·10 콘티](00_새1-7-10_콘티.md)에서 볼 수 있습니다.

[교체 전 7~10 콘티](archive/v14-root-before-v15/00_새7-10_콘티.md)
''')
for old,new in [('01_성공_자세_교정원.md','01_감독님_아직인데요.md'),('07_불량도_이직합니다.md','07_셰프님_그것도_주세요.md'),('10_비법_공개_금지.md','10_지구_대표_질문_있습니다.md')]:
    md(ROOT/old,f'# 교체된 이전 안\n\n[새 콘티 보기]({new}) · [이전 내용 보존본](archive/v14-root-before-v15/{old})')

for cid,name in [('C08','08_구조는_끝났습니다.md'),('C09','09_나_없이도_괜찮겠어요.md')]:
    p=ROOT/name;txt=p.read_text(encoding='utf-8')
    start='<!-- V15 LATEST -->';end='<!-- /V15 LATEST -->'
    if start in txt:txt=txt.split(end,1)[1].lstrip()
    f=next(f for f in films if f['concept_id']==cid)
    note=f'{start}\n**2026-10-26 V15 영상 완성:** [최신 MP4]({f["file"]}) · **{f["duration_seconds"]:g}초** · [실제 편집 구간]({rel(E/cid/"edit_manifest.json")}). 아래는 생성 전 콘티이며 최신 사용 길이·테이크는 편집 기록이 우선합니다. [검수 범위와 한계](00_V15_제작_검수.md)\n{end}\n\n'
    p.write_text(note+txt,encoding='utf-8')

cards=[]
for f in films:
    src=Path(f['file']).relative_to('storyboards').as_posix()
    src='../'+src
    cards.append(f'<article><h2>{f["concept_id"]} · {html.escape(f["title"])}</h2><video controls preload="metadata" src="{src}"></video><p>{f["duration_seconds"]:g}초 · <a href="{src}" download>MP4 다운로드</a></p></article>')
(E/'index.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair 최신 7편</title><style>body{background:#111b24;color:#edf2f7;font:18px/1.6 system-ui;margin:24px}main{max-width:1400px;margin:auto}article{margin:32px 0}video{width:100%;max-height:75vh;background:#000}a{color:#9ce4d7}</style><main><h1>Q-AI Fair · 상영용 7편 V15</h1><p>화면+후처리 자막. 실제 청취·실시간 연속재생 검증은 미완료.</p>'+''.join(cards)+'</main></html>',encoding='utf-8')
print('Built latest 7-film navigation, 3-board index, full image gallery and review report.')
