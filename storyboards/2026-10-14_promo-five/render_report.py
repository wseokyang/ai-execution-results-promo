"""Render the reviewed storyboard data as a self-contained local HTML report."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parent
esc = lambda v: html.escape(str(v))
data = json.loads((ROOT / 'storyboards.json').read_text())
review_path = ROOT / 'review_summary.json'
review = json.loads(review_path.read_text()) if review_path.exists() else {'status': '검수 진행 중', 'summary': []}
history_path = ROOT / 'review_history.json'
history = json.loads(history_path.read_text()) if history_path.exists() else {}
manifest_path = ROOT / 'scene_manifest.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'scenes': []}
images = {(s['concept_id'], s['scene_id']): s for s in manifest['scenes']}
for auxiliary in ['scene_manifest_C05_handoff.json', 'scene_manifest_C05.json']:
    auxiliary_path = ROOT / auxiliary
    if auxiliary_path.exists():
        for scene in json.loads(auxiliary_path.read_text()).get('scenes', []):
            images[(scene['concept_id'], scene['scene_id'])] = scene

def image_path(concept_id, scene_id):
    row = images.get((concept_id, scene_id), {})
    path = row.get('image_path', '')
    if not path:
        return None
    resolved = Path(path) if Path(path).is_absolute() else ROOT / path
    return resolved.relative_to(ROOT).as_posix() if resolved.exists() else None

def figure(concept, scene):
    path = image_path(concept['id'], scene['id'])
    pic = f'<a href="{esc(path)}" target="_blank"><img src="{esc(path)}" alt="{esc(scene["keyframe"])}" loading="lazy"></a>' if path else '<div class="pending">대표 이미지 준비 중</div>'
    return f'<figure>{pic}<figcaption><b>{esc(scene["id"])}</b> {esc(scene["keyframe"])}<small>영상화 메모 · {esc(scene["motion"])}</small></figcaption></figure>'

cards, sections = [], []
for c in data['concepts']:
    first = image_path(c['id'], c['scenes'][0]['id'])
    preview = f'<img src="{esc(first)}" alt="{esc(c["title"])}">' if first else '<div class="pending">이미지 준비 중</div>'
    cards.append(f'<a class="card" href="#{esc(c["id"])}">{preview}<div><span class="eyebrow">{esc(c["id"])} · {esc(c["purpose"])} · {c["duration"]}초</span><h2>{esc(c["title"])}</h2><p>{esc(c["logline"])}</p><small>웃음 장치 · {esc(c["humor"])}</small><small>병맛 강도 {c["intensity"]}/5 · 제작 난이도 {esc(c["difficulty"])}</small></div></a>')
    rows = []
    for shot in c['cuts']:
        rows.append('<tr>' + ''.join([
            f'<td><b>{esc(shot["id"])}</b><small>{esc(shot["scene"])}</small></td>',
            f'<td class="time">{shot["start"]}–{shot["end"]}초<small>{shot["end"]-shot["start"]}초</small></td>',
            f'<td>{esc(shot["visual"])}<small>전환 · {esc(shot["transition"])}</small></td>',
            f'<td>{esc(shot["caption"])}<small>대사 · {esc(shot["dialogue"])}</small></td>',
            f'<td>{esc(shot["audio"])}<small>의도 · {esc(shot["intent"])}</small></td>',
        ]) + '</tr>')
    gallery = ''.join(figure(c, s) for s in c['scenes'])
    variants = ''.join(f'<p><b>{esc(k)}</b>{esc(v).replace(chr(10), "<br>")}</p>' for k,v in c.get('ending_variants', {}).items())
    sections.append(f'''<section id="{esc(c['id'])}" class="concept">
    <div class="section-head"><span class="number">{esc(c['id'])}</span><div><p class="eyebrow">{esc(c['purpose'])} · 전체 {c['duration']}초 · 제작 난이도 {esc(c['difficulty'])}</p><h2>{esc(c['title'])}</h2><p class="lead">{esc(c['logline'])}</p></div></div>
    <div class="notes"><p><b>첫 화면</b>{esc(c['hook'])}</p><p><b>웃기는 이유</b>{esc(c['humor'])}</p><p><b>행사와 연결</b>{esc(c['why_event'])}</p><p><b>추천 용도</b>{esc(c['recommendation'])}</p></div>
    <div class="gallery"{' style="grid-template-columns:repeat(2,minmax(0,1fr))"' if len(c['scenes']) == 4 else ''}>{gallery}</div>
    <div class="notes">{variants}</div>
    <div class="table-wrap"><table><thead><tr><th>컷 / 씬</th><th>시간</th><th>화면·행동</th><th>자막·대사</th><th>음향·의도</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
    </section>''')

review_list = ''.join(f'<li>{esc(x)}</li>' for x in review.get('summary', []))
unknown_list = ''.join(f'<li>{esc(x)}</li>' for x in data['unconfirmed'])
document = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 실행 결과 발표 대회 · 홍보영상 5안</title><style>
:root{--ink:#222320;--muted:#696c66;--paper:#f5f3ec;--line:#deded3;--orange:#df4c2c}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:'Noto Sans CJK KR','Noto Sans KR',Arial,sans-serif;line-height:1.65}main{max-width:1540px;margin:auto;padding:54px 38px}header{border-top:5px solid var(--ink);padding-top:28px;padding-bottom:32px}.eyebrow{text-transform:uppercase;letter-spacing:.06em;font-size:12px;font-weight:750;color:var(--orange)}h1{font-size:clamp(32px,4vw,60px);letter-spacing:-.05em;line-height:1.18;margin:15px 0 22px}h2{font-size:28px;line-height:1.3;letter-spacing:-.035em;margin:10px 0 14px}p{margin:0 0 12px}.lead{font-size:19px;max-width:1000px}.pills{display:flex;gap:8px;flex-wrap:wrap}.pill{border:1px solid var(--line);padding:6px 13px;border-radius:3px;font-size:13px}nav{display:flex;gap:8px;flex-wrap:wrap;position:sticky;top:0;background:#f5f3ecf5;backdrop-filter:blur(8px);padding:14px 0;z-index:10;border-block:1px solid var(--line)}nav a,button{background:var(--ink);color:white;padding:8px 13px;text-decoration:none;border:0;border-radius:3px;font:inherit;font-size:12px;cursor:pointer}nav button{margin-left:auto}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:28px}.card{display:block;background:white;color:inherit;text-decoration:none;border:1px solid var(--line)}.card>img,.card>.pending{width:100%;aspect-ratio:16/9;object-fit:cover}.card>div:not(.pending){padding:22px}.card h2{font-size:23px}.card small{color:var(--muted)}.concept{scroll-margin-top:90px;border-top:2px solid var(--ink);padding-top:34px;margin-top:64px}.section-head{display:flex;gap:24px;align-items:flex-start}.number{font-size:48px;line-height:1.1;font-weight:850;color:var(--orange)}.notes{display:grid;grid-template-columns:1fr 1fr;gap:14px 30px;margin:22px 0}.notes p{background:white;padding:16px 20px;border-left:3px solid var(--orange);font-size:14px}.notes b{display:block;font-size:12px;margin-bottom:5px;color:var(--orange)}.gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:24px 0}figure{margin:0;background:white;border:1px solid var(--line)}figure img{width:100%;aspect-ratio:16/9;object-fit:contain;display:block;background:#ddd}figcaption{padding:13px 15px;font-size:13px}small{display:block;font-size:12px;margin-top:7px;color:var(--muted)}.pending{aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;background:#e9e7de;color:var(--muted)}.table-wrap{overflow:auto}table{border-collapse:collapse;width:100%;min-width:1000px;background:white;font-size:13px}th{text-align:left;background:var(--ink);color:white;font-size:12px;padding:12px 14px}td{vertical-align:top;border-bottom:1px solid var(--line);padding:14px;line-height:1.65}td:nth-child(1){width:80px}td:nth-child(2){width:94px}td:nth-child(3){width:34%}.time{white-space:nowrap}.review{padding:28px 32px;background:#e8ece1;margin-top:45px}.review h2{font-size:24px}footer{margin-top:35px;border-top:1px solid var(--line);padding-top:24px;color:var(--muted);font-size:13px}a{color:var(--orange)}@media(max-width:1000px){.grid,.gallery{grid-template-columns:1fr 1fr}}@media(max-width:650px){main{padding:24px 18px}.grid,.gallery,.notes{grid-template-columns:1fr}.section-head{gap:15px}.number{font-size:34px}nav button{margin-left:0}}@media print{body{background:white}main{padding:0}nav{display:none}.concept{break-before:page;margin-top:0}.gallery{grid-template-columns:repeat(3,1fr)}.table-wrap{overflow:visible}table{min-width:0;font-size:9px}td,th{padding:7px}.card,.concept,figure{break-inside:avoid}a{color:inherit;text-decoration:none}}
</style><main>'''
document += f'''<header><p class="eyebrow">2026 · 품질팀 · CREATIVE STORYBOARD REVIEW</p><h1>성과는 진지하게.<br>소개는 좀 이상하게.</h1><p class="lead">AI 실행 결과 발표 대회 홍보영상 5안 · 컷별 스토리보드와 씬 대표 이미지</p><div class="pills"><span class="pill">개최 확정</span><span class="pill">모든 안 60초 이내</span><span class="pill">3명 독립·교차 검수</span><span class="pill">Flow 영상 제작 전</span></div></header>'''
document += '<nav>' + ''.join(f'<a href="#{esc(c["id"])}">{esc(c["id"])} {esc(c["title"])}</a>' for c in data['concepts']) + '<button onclick="window.print()">인쇄 / PDF 저장</button></nav>'
document += '<div class="grid">' + ''.join(cards) + '</div>'
document += f'<aside class="review"><p class="eyebrow">편집 검수 결과</p><h2>{esc(review["status"])}</h2><ul>{review_list}</ul><small>평가는 에이전트 3명의 편집 판단입니다. 실제 관객 시사·반응 측정 결과는 아닙니다.</small></aside>'
if history.get('findings'):
    details = ''.join(f'<tr><td>{esc(x["id"])}</td><td>{esc(x["at"])}</td><td>{esc(x["issue"])}</td><td>{esc(x["fix"])}</td></tr>' for x in history['findings'])
    document += f'<details style="margin-top:20px"><summary style="cursor:pointer;padding:12px 0;font-weight:700">검수자가 짚은 30개 지적과 수정 방향 보기</summary><p style="font-size:13px">아래는 초안에 대한 지적입니다. 최종 스토리보드는 같은 목적의 수정을 반영했으며 세 명이 재확인했습니다. 실제 이미지 검수 상태는 위 요약과 동봉 기록에 따릅니다.</p><div class="table-wrap"><table><thead><tr><th>ID</th><th>위치</th><th>초안의 문제</th><th>수정 방향</th></tr></thead><tbody>{details}</tbody></table></div></details>'
document += ''.join(sections)
document += f'<footer><b>제작 전에 채울 행사 정보</b><ul>{unknown_list}</ul><p>대표 이미지는 장면·구도 검토용입니다. 자막과 행사 정보는 후속 편집에서 합성합니다. 현장 상영본과 참석 독려본의 마지막 문구는 각 스토리보드에 맞춰 사용합니다.</p><p>동봉 파일: <a href="storyboards.json">스토리보드 데이터</a> · <a href="scene_manifest.json">씬 이미지 매핑</a> · <a href="review_summary.json">검수 요약</a> · <a href="production_brief.json">제작 브리프</a></p></footer></main></html>'
document = document.replace('@media print{', '@page{size:A3 portrait;margin:12mm}@media print{')
(ROOT / 'index.html').write_text(document)
print(ROOT / 'index.html')
