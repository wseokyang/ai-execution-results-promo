"""Build the offline storyboard gallery from selected original first frames."""
from pathlib import Path
import json
import html
import hashlib
import math
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))

def esc(value):
    if isinstance(value, (list, dict)):
        value = json.dumps(value, ensure_ascii=False, indent=2)
    return html.escape(str(value or ''))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    data, manifest = read('storyboards.json'), read('scene_manifest.json')
    concepts = data['concepts']
    mapping = {(x['concept_id'], x['cut_id']): x for x in manifest['images']}
    assert len(concepts) == 5
    checks, summaries, sections = [], [], []
    for n, c in enumerate(concepts, 1):
        elapsed = 0
        cards = []
        for s in c['shots']:
            assert abs(s['start'] - elapsed) < .001, (c['id'], s['id'], 'gap')
            assert abs(s['end'] - s['start'] - s['duration']) < .001
            elapsed = s['end']
            m = mapping[(c['id'], s['id'])]
            p = ROOT / m['image_path']
            assert p.is_file() and s['image_file'] == m['image_path']
            with Image.open(p) as im:
                im.load()
                width, height = im.size
                assert abs(width / height - 16 / 9) < .08
            checks.append({'concept_id': c['id'], 'cut_id': s['id'], 'path': m['image_path'], 'size': [width, height], 'sha256': sha(p)})
            frame = f"{n}안 {s['id']} · {s['start']:g}–{s['end']:g}초"
            cards.append(f'''<article class="shot" id="{c['id']}-{s['id']}">
              <button class="frame" data-src="{esc(m['image_path'])}" data-caption="{esc(frame)}"><img loading="lazy" src="{esc(m['image_path'])}" alt="{esc(frame)} 첫 프레임"><span>첫 프레임 · 확대</span></button>
              <div class="shot-copy"><div class="eyebrow">{esc(s['scene_id'])} / {esc(s['id'])} <span>{s['start']:g}–{s['end']:g}초 · {s['duration']:g}초</span></div>
              <h3>{esc(s['screen'])}</h3><p class="framing">{esc(s['framing'])}</p>
              <dl><dt>대사</dt><dd>{esc(s['dialogue']) or '없음'}</dd><dt>자막</dt><dd>{esc(s['subtitle']) or '없음'}</dd><dt>음향</dt><dd>{esc(s['sound'])}</dd><dt>전환</dt><dd>{esc(s['transition'])}</dd></dl>
              <details><summary>시작 상태와 다음 동작</summary><p><b>첫 프레임</b> {esc(s['first_frame'])}</p><p><b>이후 동작</b> {esc(s['next_motion'])}</p><p><b>연속성</b> {esc(s['continuity_in'])} → {esc(s['continuity_out'])}</p><p><b>의도</b> {esc(s['intent'])}</p><a href="{esc(m['image_path'])}" download>PNG 원본</a></details></div></article>''')
        assert abs(elapsed - c['duration_seconds']) < .001 and 0 < elapsed <= 60
        hero_cut = {'C01':'K03','C02':'K03','C03':'K02','C04':'K01a','C05':'K06'}[c['id']]
        first = mapping[(c['id'], hero_cut)]['image_path']
        summaries.append(f'''<a class="overview-card" href="#{c['id']}"><img src="{esc(first)}" alt="신규 {n}안"><div><small>신규 {n:02d} · {esc(c['purpose'])}</small><h2>{esc(c['title'])}</h2><p>{esc(c['logline'])}</p><footer>{c['duration_seconds']}초 · {len(c['shots'])}컷 · {esc(c['format'])}</footer></div></a>''')
        sections.append(f'''<section class="concept" id="{c['id']}"><header class="concept-head"><small>신규 {n:02d} / {esc(c['purpose'])}</small><h2>{esc(c['title'])}</h2><p class="logline">{esc(c['logline'])}</p><p><b>핵심 메시지</b> {esc(c['core_message'])}</p><p><b>이야기 전개</b> {esc(c['three_act'])}</p><p><b>웃음 구조</b> {esc(c['comedy_engine'])}</p><div class="tags"><span>{c['duration_seconds']}초</span><span>{len(c['shots'])}컷</span><span>B급 강도 {c['bgrade_intensity']}/5</span><span>제작 난이도 {esc(c['difficulty'])}</span></div><details><summary>연출·인물·행사 연결 기준</summary><p>{esc(c['visual_style'])}</p><pre>{esc(c['characters'])}</pre><p>{esc(c['continuity'])}</p><p>{esc(c['final_action'])}</p><p>{esc(c['difference'])}</p><p>{esc(c['difficulty_reason'])}</p></details></header><div class="shots">{''.join(cards)}</div><a class="back" href="#top">↑ 5안 비교</a></section>''')
    assert len(mapping) == len(checks)
    assert len({x['sha256'] for x in checks}) == len(checks), 'Each cut requires its own selected generated first frame'
    assert not any(ROOT.rglob('*.mp4')) and not any(ROOT.rglob('*.wav'))
    old = ROOT.parent / '2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4'
    assert sha(old) == 'b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c'
    status = read('delivery_status.json') if (ROOT / 'delivery_status.json').exists() else {'status':'in_progress'}
    status_line = '콘티·첫 프레임·교차 검수 완료' if status['status'] == 'complete' else '제작·검수 중'
    nav = ''.join(f'<a href="#{c["id"]}">{i:02d} {esc(c["title"])}</a>' for i, c in enumerate(concepts, 1))
    rec = data.get('recommendations', {})
    recommendation = ''.join(f'<p><b>{esc(k)}</b> {esc(v)}</p>' for k,v in rec.items())
    document = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>새 5안 · 이야기부터 다시 / V4</title><style>
    :root{--paper:#f3efe6;--ink:#22231f;--red:#b73924;--gold:#dfb96c}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.7 'Malgun Gothic',system-ui,sans-serif}a{color:inherit}.hero{padding:60px max(24px,calc((100vw - 1300px)/2));background:#202320;color:#faf5e9}.hero small{color:var(--gold);letter-spacing:.15em}.hero h1{font-size:clamp(36px,5vw,68px);line-height:1.18;letter-spacing:-.06em;margin:20px 0}.hero p{max-width:900px;color:#d6d5ca}.status{display:inline-block;border:1px solid #817e6e;padding:5px 12px;font-size:12px}.nav{position:sticky;top:0;z-index:2;display:flex;gap:24px;overflow:auto;white-space:nowrap;padding:14px 24px;background:#f3efe6f5;border-bottom:1px solid #c6bdac}.nav a{text-decoration:none;font-size:12px;font-weight:700}main{max-width:1350px;margin:auto;padding:34px 24px 70px}.overview{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.overview-card{background:#fff;text-decoration:none;border:1px solid #d0c7b7}.overview-card img{width:100%;aspect-ratio:16/9;object-fit:contain;display:block;background:#171a17}.overview-card>div{padding:18px 22px}.overview-card small,.concept-head>small{color:var(--red);font-weight:800}.overview-card h2{font-size:24px;line-height:1.35;letter-spacing:-.05em}.overview-card p{font-size:14px}.overview-card footer{font-size:12px;color:#666}.recommendation{margin-top:35px;padding:20px 25px;border-left:4px solid var(--red);background:#eae2d3}.concept{padding-top:65px;scroll-margin-top:40px}.concept-head{border-top:4px solid var(--ink);padding:24px 0}.concept-head h2{font-size:42px;line-height:1.2;letter-spacing:-.05em;margin:10px 0}.logline{font-size:20px;max-width:1000px}.concept-head p{white-space:pre-wrap}.tags{display:flex;gap:10px;flex-wrap:wrap}.tags span{padding:3px 10px;border:1px solid #b5a992;font-size:12px}.shots{display:grid;grid-template-columns:1fr 1fr;gap:24px}.shot{background:white;border:1px solid #d0c7b7;scroll-margin-top:70px}.frame{display:block;position:relative;width:100%;border:0;padding:0;background:#171a17;cursor:zoom-in}.frame img{width:100%;aspect-ratio:16/9;object-fit:contain;display:block}.frame span{position:absolute;bottom:9px;left:12px;background:#101510c9;color:white;font-size:10px;padding:3px 8px}.shot-copy{padding:18px 22px}.eyebrow{font-weight:800;color:var(--red);font-size:12px}.eyebrow span{float:right;color:#6a665d;font-weight:400}h3{font-size:17px;line-height:1.7}.framing{font-size:12px;color:#686155}dl{display:grid;grid-template-columns:52px 1fr;gap:8px 12px;font-size:13px}dt{font-weight:700}dd{margin:0;white-space:pre-wrap}details{border-top:1px solid #ddd5c7;margin-top:18px;padding-top:12px;font-size:12px}summary{cursor:pointer;font-weight:700}details p,pre{white-space:pre-wrap}pre{font-family:inherit;font-size:12px}.back{display:block;margin-top:22px;font-size:12px}.notes{margin-top:65px;padding-top:22px;border-top:3px solid var(--ink);font-size:13px}.notes a{margin-right:20px}dialog{max-width:96vw;max-height:96vh;padding:0;border:0;background:#151915;color:white}dialog::backdrop{background:#000d}dialog img{display:block;max-width:94vw;max-height:85vh;object-fit:contain}dialog footer{padding:10px 16px;display:flex;justify-content:space-between;gap:20px;font-size:13px}dialog button{background:#eee;border:0;padding:5px 15px;cursor:pointer}@media(max-width:900px){.overview{grid-template-columns:1fr 1fr}.shots{grid-template-columns:1fr}}@media(max-width:550px){.overview{grid-template-columns:1fr}.concept-head h2{font-size:32px}.shot-copy{padding:15px}.eyebrow span{float:none;display:block}}@media print{.nav,.back,dialog{display:none}.hero{background:white;color:black;padding:25px}.hero p{color:black}.shots{display:block}.shot{break-inside:avoid;margin-bottom:15px}.concept{break-before:page}.frame img{max-height:280px}.shot-copy{padding:10px}details{display:none}}
    </style></head><body id="top">'''
    document += f'''<header class="hero"><small>AI 실행 결과 발표 대회 · STORY RESET V4</small><h1>설정 다음에,<br>무슨 일이 벌어지는가.</h1><p>기존 1번 완성 영상은 보존하고, 별도의 새 5안을 이야기와 연출부터 다시 구성했습니다. 그림은 각 컷의 시작 상태이며, 그 뒤에 벌어질 사건은 아래 콘티에 적었습니다.</p><span class="status">{status_line} · 5안 / {len(checks)}컷 · 동영상 생성 없음</span><p style="font-size:12px">이미지·대본의 검토 결과입니다. 실제 영상의 움직임·음성이나 관객 반응을 검증한 결과는 아닙니다.</p></header><nav class="nav">{nav}</nav><main><div class="overview">{''.join(summaries)}</div><div class="recommendation">{recommendation}</div>{''.join(sections)}<section class="notes"><h2>자료와 검수 기록</h2><p>행사명: 2026년 품질팀 AI 실행 결과 발표 대회. 세부 일시·장소·참석 방법·상금·실제 성과 수치는 미확인으로 넣지 않았습니다. 16:9·사내 시청은 제작 가정입니다. 화면 속 사건과 인물은 허구입니다.</p><p>자막·행사명·대사는 후속 편집 정보이며 원본 PNG와 분리했습니다. 전체 60초 이내입니다. Flow 예약은 PAUSED를 유지합니다.</p><p><a href="storyboards.json">전체 콘티</a><a href="scene_manifest.json">첫 프레임·프롬프트·참조</a><a href="review_summary.json">검수와 수정</a><a href="shared_brief.json">공통 브리프</a><a href="validation.json">파일 검증</a></p></section></main><dialog id="viewer"><img id="full" alt="첫 프레임 원본"><footer><span id="caption"></span><button id="close">닫기 ×</button></footer></dialog><script>const v=document.querySelector('#viewer'),f=document.querySelector('#full'),c=document.querySelector('#caption');document.querySelectorAll('[data-src]').forEach(b=>b.onclick=()=>{{f.src=b.dataset.src;c.textContent=b.dataset.caption;v.showModal()}});document.querySelector('#close').onclick=()=>v.close();v.onclick=e=>{{if(e.target===v)v.close()}};</script></body></html>'''
    document = document.replace('<a href="storyboards.json">전체 콘티</a>', '<a href="STORYBOARDS.md">전체 컷 표</a><a href="storyboards.json">구조화 콘티</a><a href="reference/README.md">참고 작품과 적용 범위</a>')
    (ROOT / 'index.html').write_text(document, encoding='utf-8', newline='\n')
    out = ROOT / 'contact_sheets'
    out.mkdir(exist_ok=True)
    font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 20)
    header = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 28)
    for n,c in enumerate(concepts,1):
        sheet = Image.new('RGB', (1312, 80 + math.ceil(len(c['shots'])/2)*392), '#f3efe6')
        draw = ImageDraw.Draw(sheet)
        draw.text((16,20), f"신규 {n}안 · {c['title']} / {c['duration_seconds']}초",font=header,fill='#22231f')
        for i,s in enumerate(c['shots']):
            x,y = 16+(i%2)*648,80+(i//2)*392
            with Image.open(ROOT/mapping[(c['id'],s['id'])]['image_path']) as im:
                thumb=ImageOps.contain(im.convert('RGB'),(632,355))
            sheet.paste(thumb,(x+(632-thumb.width)//2,y))
            draw.text((x,y+360),f"{s['id']} · {s['start']:g}–{s['end']:g}초 / 첫 프레임",font=font,fill='#22231f')
        sheet.save(out/f"{c['id']}_all_cuts.jpg",quality=93)
    validation={'status':'passed','concepts':len(concepts),'cuts':len(checks),'unique_images':len(checks),'old_C01_sha256_unchanged':True,'new_video_or_audio':False,'images':checks}
    (ROOT/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'passed','concepts':5,'cuts':len(checks),'html':'index.html'},ensure_ascii=False))

if __name__ == '__main__':
    main()
