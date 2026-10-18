"""Offline storyboard reader. Generated PNGs are never altered."""
from pathlib import Path
import json,html,hashlib,math
from PIL import Image,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def esc(v):return html.escape(str(v or '없음'))
def main():
    d=read('storyboards.json');m=read('scene_manifest.json')
    mapping={(x['concept_id'],x['cut_id']):x for x in m['images']}
    concepts=d['concepts'];assert len(concepts)==5
    overview=[];sections=[];checks=[]
    for c in concepts:
        cid=c['id']; retained=cid=='C03'; elapsed=0;cards=[]
        for s in c['shots']:
            assert s['start']==elapsed and s['end']-s['start']==s['duration']
            elapsed=s['end'];impath=mapping[cid,s['id']]['image_path'];p=R/impath
            assert p.is_file() and impath==s['image_file']
            with Image.open(p) as im:im.load();size=im.size;assert abs(size[0]/size[1]-16/9)<.08
            checks.append({'concept_id':cid,'cut_id':s['id'],'image':impath,'size':size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
            cards.append(f'''<article class="shot"><button class="frame" data-src="{esc(impath)}" data-caption="{cid} {s['id']}"><img src="{esc(impath)}" loading="lazy" alt="{cid} {s['id']} 첫 프레임"></button><div class="copy"><small>{s['id']} · {s['start']}–{s['end']}초</small><p class="action">{esc(s['screen'])}</p><p class="dialogue">{esc(s['dialogue'])}</p><details><summary>첫 프레임·이후 동작·제작 정보</summary><p><b>첫 프레임</b> {esc(s['first_frame'])}</p><p><b>이후 동작</b> {esc(s['next_motion'])}</p><p><b>자막</b> {esc(s['subtitle'])}</p><p><b>음향</b> {esc(s['sound'])}</p><p><b>구도·전환</b> {esc(s['framing'])} / {esc(s['transition'])}</p><p><b>연속성</b> {esc(s['continuity_in'])} → {esc(s['continuity_out'])}</p><a href="{esc(impath)}" download>PNG 원본</a></details></div></article>''')
        assert elapsed==c['duration_seconds'] and elapsed<=60
        hero=d['hero_cuts'][cid];pic=mapping[cid,hero]['image_path'];label='유지한 3안' if retained else '새로 만든 '+cid[-1]+'안'
        overview.append(f'<a class="concept-link" href="#{cid}"><img src="{esc(pic)}" alt="{esc(c["title"])}"><div><small>{label} · {elapsed}초</small><h2>{esc(c["title"])}</h2><p>{esc(c["logline"])}</p></div></a>')
        reveal=c.get('reveal_test',{})
        reveal_text=''.join(f'<p><b>{esc(k)}</b> {esc(v)}</p>' for k,v in reveal.items())
        sections.append(f'<section id="{cid}"><header><small>{label} · {esc(c["purpose"])} · {elapsed}초 / {len(c["shots"])}컷</small><h2>{esc(c["title"])}</h2><p class="logline">{esc(c["logline"])}</p></header><div class="shots">{"".join(cards)}</div><details class="concept-notes"><summary>이야기 판단과 행사 연결</summary>{reveal_text}<p>{esc(c["core_message"])}</p><p>{esc(c["final_action"])}</p><p>제작 난이도: {esc(c["difficulty"])}. {esc(c["difficulty_reason"])}</p></details><a class="back" href="#top">↑ 전체 안으로</a></section>')
    assert len(checks)==len(mapping) and len({x['sha256'] for x in checks})==len(checks)
    frozen=read('retained_concept_C03.json');current=next(c for c in concepts if c['id']=='C03');assert current==frozen
    for p in read('preservation_manifest.json')['images']:assert hashlib.sha256((R/p['copy']).read_bytes()).hexdigest()==p['sha256']
    old=R.parent/'2026-10-17_C01-voicefix-v07/C01_recut_v07_36s.mp4';assert hashlib.sha256(old.read_bytes()).hexdigest()=='b47a59928001291cbf9937e9eed609984725efa07c2deb0741deb5f6e6ca8b6c'
    assert not list(R.rglob('*.mp4')) and not list(R.rglob('*.wav'))
    nav=''.join(f'<a href="#{c["id"]}">{c["id"][-1]} · {esc(c["title"])}</a>' for c in concepts)
    css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f5f1e8;color:#20231f;font:15px/1.65 "Malgun Gothic",sans-serif}a{color:inherit}.hero{padding:48px max(24px,calc((100vw - 1300px)/2));background:#222922;color:#f7f1e5}.hero h1{font-size:52px;line-height:1.2;margin:14px 0}.hero small{color:#dbc18b}.hero p{max-width:900px}.nav{display:flex;gap:24px;overflow:auto;white-space:nowrap;position:sticky;top:0;background:#f5f1e8f5;padding:14px 24px;z-index:2;border-bottom:1px solid #cfc4b2;font-size:12px}.nav a{text-decoration:none}main{max-width:1350px;margin:auto;padding:30px 24px 70px}.overview{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.concept-link{text-decoration:none;background:white;border:1px solid #d2c7b5}.concept-link img{width:100%;aspect-ratio:16/9;object-fit:contain;display:block}.concept-link div{padding:18px}.concept-link h2{font-size:23px;line-height:1.3}.concept-link p{font-size:14px}small{color:#93412d;font-weight:700}section{padding-top:60px;scroll-margin-top:40px}section header{border-top:4px solid #20231f;padding:22px 0}section h2{font-size:38px;line-height:1.25;margin:10px 0}.logline{font-size:20px}.shots{display:grid;grid-template-columns:1fr 1fr;gap:22px}.shot{background:white;border:1px solid #d2c7b5}.frame{border:0;padding:0;width:100%;display:block;cursor:zoom-in;background:#20231f}.frame img{display:block;width:100%;aspect-ratio:16/9;object-fit:contain}.copy{padding:18px 22px}.action{font-size:17px}.dialogue{font-size:19px;white-space:pre-wrap;font-weight:700;color:#663d2b}details{border-top:1px solid #dfd5c4;padding-top:12px;margin-top:18px;font-size:13px}summary{cursor:pointer;font-weight:700}details p{white-space:pre-wrap}.back{display:block;margin:20px 0;font-size:12px}.notes{border-top:3px solid #20231f;padding-top:24px;margin-top:55px;font-size:13px}.notes a{margin-right:20px}dialog{max-width:96vw;max-height:96vh;border:0;padding:0;background:#171c17;color:white}dialog::backdrop{background:#000d}dialog img{max-width:94vw;max-height:86vh;display:block}dialog footer{display:flex;justify-content:space-between;padding:10px 15px}dialog button{cursor:pointer;border:0;padding:5px 15px}@media(max-width:850px){.overview{grid-template-columns:1fr 1fr}.shots{grid-template-columns:1fr}.hero h1{font-size:40px}}@media(max-width:520px){.overview{grid-template-columns:1fr}section h2{font-size:30px}}'''
    text=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>3안 유지 · 네 안 교체 / V5</title><style>{css}</style></head><body id="top"><header class="hero"><small>AI 실행 결과 발표 대회 · V5</small><h1>3안은 그대로.<br>나머지 네 이야기는 새로.</h1><p>「환경까지 가져왔습니다」의 콘티와 이미지 8장은 그대로 유지했습니다. 아래 1·2·4·5안은 새 시나리오와 컷별 첫 프레임입니다. 기존 완성 1번 동영상도 보존했습니다.</p><p>{len(checks)-8}장 새 첫 프레임 + 8장 유지 · 동영상·음원 생성 없음</p></header><nav class="nav">{nav}</nav><main><div class="overview">{''.join(overview)}</div>{''.join(sections)}<div class="notes"><p>실제 첫 프레임과 계획된 대사·다음 행동을 함께 보는 문서입니다. 영상 움직임·음성·관객 반응은 검증하지 않았습니다. 행사명·UI·자막은 후속 편집 정보입니다.</p><p>행사명: 2026년 품질팀 AI 실행 결과 발표 대회. 일시·장소·참석 방법·실제 성과·상금은 미확인으로 넣지 않았습니다. 인물과 사건은 허구이며 16:9·사내 시청은 제작 가정입니다.</p><p><a href="STORYBOARDS.md">전체 컷 표</a><a href="scene_manifest.json">이미지·정확한 프롬프트</a><a href="review_summary.json">검토와 수정 기록</a><a href="preservation_manifest.json">3안·기존영상 보존</a><a href="reference_diagnosis.json">이전안 진단</a></p></div></main><dialog id="viewer"><img id="full" alt="원본 첫 프레임"><footer><span id="caption"></span><button id="close">닫기 ×</button></footer></dialog><script>const v=document.querySelector('#viewer');document.querySelectorAll('[data-src]').forEach(b=>b.onclick=()=>{{document.querySelector('#full').src=b.dataset.src;document.querySelector('#caption').textContent=b.dataset.caption;v.showModal()}});document.querySelector('#close').onclick=()=>v.close();v.onclick=e=>{{if(e.target===v)v.close()}};</script></body></html>'''
    (R/'index.html').write_text(text,encoding='utf-8')
    out=R/'contact_sheets';out.mkdir(exist_ok=True);font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',20);title=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',27)
    for c in concepts:
        sheet=Image.new('RGB',(1312,80+math.ceil(len(c['shots'])/2)*392),'#f5f1e8');dr=ImageDraw.Draw(sheet);dr.text((18,20),f"{c['id']} · {c['title']} / {c['duration_seconds']}초",font=title,fill='#20231f')
        for i,s in enumerate(c['shots']):
            x=16+(i%2)*648;y=80+(i//2)*392
            with Image.open(R/s['image_file']) as src:im=ImageOps.contain(src.convert('RGB'),(632,355))
            sheet.paste(im,(x,y));dr.text((x,y+360),f"{s['id']} · {s['start']}–{s['end']}초",font=font,fill='#20231f')
        sheet.save(out/(c['id']+'_all_cuts.jpg'),quality=93)
    (R/'validation.json').write_text(json.dumps({'status':'passed','concepts':5,'total_images':len(checks),'new_images':len(checks)-8,'retained_images':8,'C03_structurally_unchanged':True,'C03_image_bytes_unchanged':True,'old_film_sha256_unchanged':True,'new_video_or_audio':False,'browser_render_qa':'not_performed; local file protocol blocked by Browser Use policy, no workaround attempted','images':checks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print({'gallery':'index.html','images':len(checks),'preservation':'passed'})
if __name__=='__main__':main()
