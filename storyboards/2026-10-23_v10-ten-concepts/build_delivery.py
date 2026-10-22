"""Read-only delivery rendering. Upload PNG bytes are never changed."""
from pathlib import Path
import json,html,hashlib,sys,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
ROOT=R.parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def txt(v):
    if isinstance(v,list):return ' / '.join(map(txt,v))
    if isinstance(v,dict):return json.dumps(v,ensure_ascii=False)
    return str(v or '')
def h(v):return html.escape(txt(v),quote=True)
def md(v):return txt(v).replace('|','／').replace('\n','<br>')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def style(q):
    b=q.get('box',{'left_pct':7,'width_pct':86,'bottom_pct':6})
    a='top' if 'top_pct'in b else 'bottom'
    return f'left:{b["left_pct"]}%;width:{b["width_pct"]}%;{a}:{b[a+"_pct"]}%;font-size:{b.get("font_cqw",3.3)}cqw;--title-size:{b.get("title_cqw",5)}cqw;padding:{b.get("padding_pct",1)}% 1.3%'
def main():
    d=read(R/'storyboards.json');m=read(R/'scene_manifest.json');cs=d['concepts'];units=d['generation_units'];ims={x['id']:x for x in m['images']}
    assert len(cs)==10
    rows=['# Q-AI Fair · 10안 선택용 콘티 V10','','영상은 후속 Flow에서 생성하고 자막·행사명·정확한 글은 후편집합니다. 이번 패키지는 선택용 콘티와 실제 시작 이미지이며 Flow 요청·크레딧 사용·영상 및 음원 생성은 없습니다.','','| 안 | 제목 | 목적 | 형식 | 웃음의 변화 | 길이 | B급 강도 | 난이도 | 시작 상태 |','|---|---|---|---|---|---:|---:|---|---:|']
    full=['# 전체 이미지 콘티 · Q-AI Fair 10안','','기존 C01~C05를 보완하고 C06~C10을 추가했습니다. 모든 PNG는 자막 없는 업로드용 첫 상태입니다. 아래 글은 별도 후편집 자막입니다.','','[10안 비교·컷 표](STORYBOARDS.md) · [인터랙티브 자막 보기](index.html) · [캐스팅](CASTING.md) · [검수 기록](review_summary.json)','']
    cast=['# 10안 캐스팅 구분','','나이·체형·얼굴형·머리·의상·실루엣과 연기 온도를 함께 구분합니다. 외형은 웃음의 대상이 아닙니다. 기존 주요 인물은 유지하고 새 안에 같은 기본 얼굴을 반복하지 않습니다.','','| 안 | 인물·외형 | 연출 구분 |','|---|---|---|']
    cards=[];sections=[];checks=[];timing={};count={};overview_images=[]
    for c in cs:
        us=[u for u in units if u['concept_id']==c['id']];count[c['id']]=len(us)
        rows.append('| '+' | '.join(map(md,[c['id'],c['title'],c['purpose'],c['format'],c['comedy_engine'],str(c['duration_seconds'])+'초',c['bgrade_intensity'],c['difficulty'],len(us)]))+' |')
    for c in cs:
        cid=c['id'];ss={s['id']:s for s in c['shots']};us=[u for u in units if u['concept_id']==cid]
        rows+=['','## '+cid+' · '+c['title'],'',c['logline'],'','**핵심 메시지:** '+c['core_message'],'','**첫 장면:** '+txt(c['hook']),'','**다른 안과의 차이:** '+txt(c['difference']),'','| 씬·컷 | 구간·길이 | 화면·행동·구도 | 후편집 자막 | 대사·내레이션 | 음악·효과음·정적 | 전환 | 웃음·정보 의도 |','|---|---|---|---|---|---|---|---|']
        t=0
        for s in c['shots']:
            assert abs(s['start']-t)<.001,(cid,s['id'],'gap')
            assert abs(s['end']-s['start']-s['duration'])<.001
            t=s['end']
            for q in s.get('caption_cues',[]):
                assert s['start']<=q['start']<q['end']<=s['end']+.001,(cid,s['id'],q)
                assert q.get('box'),(cid,s['id'],'missing caption box')
            qs=' / '.join(f"{q['start']}–{q['end']}초: "+(q.get('eyebrow','')+' · ' if q.get('eyebrow') else '')+q['text'] for q in s.get('caption_cues',[])) or '무자막'
            rows.append('| '+' | '.join(map(md,[s['scene_id']+'/'+s['id'],f"{s['start']}–{s['end']}초 ({s['duration']}초)",s['screen']+' / '+s['framing'],qs,s['dialogue'],s['sound'],s['transition'],s['intent']]))+' |')
        assert t==c['duration_seconds'] and t<=60
        timing[cid]=t
        full+=['','## '+cid,'','**'+c['title']+'**','',c['logline'],'']
        frames=[];contact=[]
        for u in us:
            e=ims[u['id']];s=ss[u['linked_shot']];p=R/e['image_path']
            assert p.exists(),p
            im=Image.open(p);im.load();assert abs(im.width/im.height-16/9)<.08
            checks.append({'id':u['id'],'path':e['image_path'],'sha256':sha(p),'size':list(im.size),'new_in_v10':e.get('new_in_v10',True)})
            contact.append((u['id'],im.copy()))
            btn=''.join(f'<button class="cue" data-text="{h(q["text"])}" data-kind="{h(q.get("kind",""))}" data-eyebrow="{h(q.get("eyebrow",""))}" data-style="{h(style(q))}">{q["start"]}–{q["end"]}초 · {h(q["text"])}</button>' for q in s.get('caption_cues',[]))
            frames.append(f'<article id="{u["id"]}"><div class="stage"><img src="{h(e["image_path"])}" alt="{u["id"]} 시작 상태" loading="lazy"><div class="caption"></div></div><div class="copy"><small>{u["id"]} · {s["start"]}–{s["end"]}초</small><h3>{h(u["first_frame"])}</h3><p><b>다음 동작</b> {h(u["action"])}</p><div class="buttons"><button class="cue" data-text="" data-style="">자막 없는 원본</button>{btn}</div><details><summary>구도·소리·제작 메모</summary><p>{h(u["framing"])}</p><p>{h(s["sound"])}</p><p>{h(u.get("caption_safe_zone"))}</p><p>{h(s.get("continuity_in"))}</p><p>{h(s.get("continuity_out"))}</p></details><a href="{h(e["image_path"])}" download>시작 PNG 원본</a></div></article>')
            full += [f'### {u["id"]} · {s["start"]}–{s["end"]}초','',f'![{u["id"]}]({e["image_path"]})','','**첫 상태:** '+u['first_frame'],'','**후속 동작:** '+u['action'],'','**후편집 자막:** '+(' / '.join(q['text'] for q in s.get('caption_cues',[])) or '무자막'),'']
        cw,ch=560,350;sheet=Image.new('RGB',(cw*3,ch*math.ceil(len(contact)/3)), '#172020');dr=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',20)
        for i,(name,im) in enumerate(contact):
            x,y=(i%3)*cw,(i//3)*ch
            thumb=ImageOps.contain(im,(cw-16,ch-42));sheet.paste(thumb,(x+(cw-thumb.width)//2,y+4));dr.text((x+12,y+ch-30),name,fill='white',font=font)
        (R/'contact_sheets').mkdir(exist_ok=True);sheet.save(R/f'contact_sheets/{cid}_all_starts.jpg',quality=93)
        cp=' / '.join(x['description'] for x in c['characters'])
        cast.append('| '+' | '.join(map(md,[cid+' '+c['title'],cp,c.get('visual_style')]))+' |')
        hero=ims[us[0]['id']]['image_path'];new=int(cid[1:])>=6
        overview_images.append((cid,c['title'],t,len(us),R/hero))
        cards.append(f'<div class="overview-card"><a href="#{cid}"><img src="{h(hero)}"><div><small>{"신규" if new else "기존 보완"} · {cid} · {t}초 · {len(us)}시작 상태</small><h2>{h(c["title"])}</h2><p>{h(c["logline"])}</p></div></a><label><input type="checkbox" class="pick" value="{cid}" data-title="{h(c["title"])}" data-count="{len(us)}"> 비교 후보로 표시</label></div>')
        sections.append(f'<section id="{cid}"><header><small>{cid} · {h(c["purpose"])} · {t}초 · {len(us)}시작 상태</small><h2>{h(c["title"])}</h2><p class="logline">{h(c["logline"])}</p><p>{h(c["core_message"])}</p><details><summary>캐릭터·연출·차별점</summary><p>{h(cp)}</p><p>{h(c["visual_style"])}</p><p>{h(c["difference"])}</p></details></header><div class="shots">{"".join(frames)}</div><a class="back" href="#top">↑ 10안 비교로</a></section>')
    ow,oh=900,590;ov=Image.new('RGB',(ow*2,oh*5),'#f1eee5');od=ImageDraw.Draw(ov);oft=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',30);osf=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',21)
    for i,(cid,title,t,n,p) in enumerate(overview_images):
        x,y=(i%2)*ow,(i//2)*oh
        with Image.open(p)as im:th=ImageOps.contain(im,(ow-24,490));ov.paste(th,(x+(ow-th.width)//2,y+10))
        od.text((x+18,y+505),cid+'  '+title,fill='#203c32',font=oft)
        od.text((x+18,y+548),('기존 보완'if int(cid[1:])<6 else'신규')+f'  ·  {t}초  ·  {n}시작 상태',fill='#4e594f',font=osf)
    ov.save(R/'overview_10.jpg',quality=94)
    rec=d.get('recommendations',{})
    rows+=['','## 제작 범위와 추천','','**참석 독려 추천:** '+rec.get('attendance',''),'','**현장 도입 추천:** '+rec.get('opening',''),'','정확한 행사 일시·장소·참석 방법·성과 수치는 미확인입니다. 등장인물과 장면은 허구입니다. 영상 생성 후에는 실제 움직임·자막 읽기·호흡을 따로 검수합니다. 이미지 수는 성공 영상 수나 필요한 크레딧 수가 아닙니다. C03은 기존 원본 재사용을 먼저 검토합니다.','','[전체 이미지](ALL_IMAGES.md) · [캐스팅](CASTING.md) · [후편집·Flow 제작 메모](PRODUCTION_NOTES.md)']
    (R/'STORYBOARDS.md').write_text('\n'.join(rows),encoding='utf-8');(R/'ALL_IMAGES.md').write_text('\n'.join(full),encoding='utf-8');(R/'CASTING.md').write_text('\n'.join(cast),encoding='utf-8')
    readme=['# Q-AI Fair · V10 선택용 패키지','','**[전체 88장 이미지 콘티 보기](ALL_IMAGES.md)** · [10안 비교와 컷 표](STORYBOARDS.md) · [자막 미리보기 HTML](index.html)','','![10안 한눈에 보기](overview_10.jpg)','','기존 C01–C05는 보완하고 신규 C06–C10을 추가했습니다. 신규 시작 PNG 44장과 기존 V9에서 바이트 그대로 가져온 44장을 포함합니다. 모든 자막·행사명·정확한 문서 글자는 별도 후편집입니다. 이번 패키지에서는 Flow·영상·음원 생성을 실행하지 않았습니다.','','| 자료 | 용도 |','|---|---|','| [STORYBOARDS.md](STORYBOARDS.md) | 10안 비교, 컷별 시간·행동·자막·음향·전환 |','| [ALL_IMAGES.md](ALL_IMAGES.md) | GitHub에서 모든 채택 시작 이미지를 바로 보기 |','| [index.html](index.html) | 자막 위치 전환과 후보 표시. 이미지 폴더와 함께 내려받아 열기 |','| [CASTING.md](CASTING.md) | 10안의 인물 외형과 연출 구분 |','| [PRODUCTION_NOTES.md](PRODUCTION_NOTES.md) | Flow 동작과 후편집 합성의 분담 |','| [review_summary.json](review_summary.json) | 독립·교차 검수의 실제 범위와 남은 제작 확인 |','| [scene_manifest.json](scene_manifest.json) | 채택 PNG, 원본 경로, 실제 제출 프롬프트와 참조 |','| [storyboards.json](storyboards.json) | 최신 전체 콘티의 기계 판독 명세 |','','`selection_cards.json`, `new_five_draft.json`, `storyboards_before_text_review.json`은 발상·수정 이력입니다. **최신 채택본은 storyboards.json과 scene_manifest.json**을 사용합니다. images 폴더의 미채택 버전까지 전부 제작 큐로 세지 않습니다. flow_prompts는 후속 동작 초안이며 아직 제출하지 않았습니다.','','길이·크레딧·실제 영상 성공은 첫 이미지 수로 확정하지 않습니다. 선택된 안만 후속 제작하고, 기존 C03 영상은 재사용을 먼저 검토합니다.']
    (R/'README.md').write_text('\n'.join(readme)+'\n',encoding='utf-8')
    css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f1eee5;color:#24261f;font:15px/1.65 "Malgun Gothic",sans-serif}a{color:inherit}.hero{padding:44px max(24px,calc((100vw - 1350px)/2));background:#1d322e;color:white}.hero h1{font-size:48px;line-height:1.15;max-width:1000px;margin:18px 0}.hero p{max-width:980px}.hero small{color:#c6f69c}small{font-size:12px;font-weight:700;color:#49644a}.nav{position:sticky;top:0;z-index:10;display:flex;gap:20px;overflow:auto;white-space:nowrap;background:#f1eee5f5;border-bottom:1px solid #c5c5b8;padding:13px 24px;font-size:12px}.nav a{text-decoration:none}main{max-width:1400px;margin:auto;padding:30px 24px 70px}.overview{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.overview-card{background:white;border:1px solid #cecec2}.overview-card a{text-decoration:none}.overview-card img{width:100%;display:block;aspect-ratio:16/9;object-fit:contain}.overview-card a div{padding:17px}.overview-card h2{font-size:23px;line-height:1.3}.overview-card label{display:block;padding:12px 17px;background:#e5eddd;border-top:1px solid #ccd7bf;cursor:pointer;font-weight:700}.selection{margin:25px 0;padding:18px;background:#e1e8d9;border:1px solid #b6c4a9}.selection p{margin:5px 0}section{padding-top:50px;scroll-margin-top:50px}section header{border-top:4px solid #1d322e;padding:20px 0}section h2{font-size:37px;line-height:1.25;margin:10px 0}.logline{font-size:20px}.shots{display:grid;grid-template-columns:1fr 1fr;gap:20px}article{scroll-margin-top:76px;background:#fff;border:1px solid #cecec2;min-width:0}.stage{position:relative;aspect-ratio:16/9;background:#171717;overflow:hidden;container-type:inline-size}.stage img{width:100%;height:100%;object-fit:contain;display:block}.caption{position:absolute;white-space:pre-line;text-align:center;font-weight:800;line-height:1.4;color:white;background:#000c;padding:1% 1.3%;text-shadow:0 1px 2px #000;pointer-events:none}.caption:empty{display:none}.caption strong{display:block;font-size:var(--title-size,5cqw);line-height:1.2;margin-bottom:.4cqw}.caption em{display:block;font-size:2.3cqw;font-style:normal;color:#d5efd1;margin-bottom:.5cqw}.copy{padding:18px 22px}.copy h3{font-size:17px;font-weight:500}.buttons{display:flex;gap:7px;flex-wrap:wrap}button{cursor:pointer;font:12px/1.4 "Malgun Gothic",sans-serif;border:1px solid #bdc9b4;border-radius:4px;padding:7px 10px;background:#f0f6eb;text-align:left}button.active{background:#315039;color:white}details{margin:16px 0;border-top:1px solid #ddd;padding-top:12px;font-size:13px}summary{cursor:pointer;font-weight:bold}.copy>a,.back{font-size:13px}.back{display:block;margin-top:18px}.notes{margin-top:40px;border-top:3px solid #1d322e;padding-top:20px}.notes a{margin-right:16px}@media(max-width:900px){.shots{grid-template-columns:1fr}.overview{grid-template-columns:1fr 1fr}.hero h1{font-size:38px}}@media(max-width:560px){.overview{grid-template-columns:1fr}section h2{font-size:29px}}'''
    script='''document.querySelectorAll('.cue').forEach(b=>b.addEventListener('click',()=>{const a=b.closest('article'),c=a.querySelector('.caption');c.replaceChildren();c.style.cssText=b.dataset.style||'';if(b.dataset.eyebrow){const e=document.createElement('em');e.textContent=b.dataset.eyebrow;c.append(e)}const t=b.dataset.text||'';if(b.dataset.kind==='event'){const lines=t.split('\\n'),s=document.createElement('strong');s.textContent=lines.shift();c.append(s,document.createTextNode(lines.join('\\n')))}else c.append(document.createTextNode(t));a.querySelectorAll('.cue').forEach(x=>x.classList.remove('active'));b.classList.add('active')}));function selected(){return [...document.querySelectorAll('.pick:checked')]}function update(){const p=selected();document.getElementById('chosen').textContent=p.length?p.map(x=>x.value+' '+x.dataset.title).join(' / '):'아직 표시한 안이 없습니다.';document.getElementById('quantity').textContent=p.length?'선택안의 시작 상태 합계 '+p.reduce((n,x)=>n+Number(x.dataset.count),0)+'개. 실제 Flow 요청 수·기존 영상 재사용 여부는 선택 후 확정합니다.':''}document.querySelectorAll('.pick').forEach(x=>x.addEventListener('change',update));document.getElementById('save-choice').addEventListener('click',()=>{const t='Q-AI Fair V10 선택 메모\\n'+selected().map(x=>x.value+' '+x.dataset.title).join('\\n')+'\\n※ 이 파일을 저장해도 자동 생성 요청은 제출되지 않습니다.';const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/plain;charset=utf-8'}));a.download='Q-AI-Fair-choice.txt';a.click();URL.revokeObjectURL(a.href)});'''
    script+='''document.querySelectorAll('article').forEach(a=>{const b=[...a.querySelectorAll('.cue')].find(b=>b.dataset.text);if(b)b.click()});'''
    nav=''.join(f'<a href="#{c["id"]}">{int(c["id"][1:])} · {h(c["title"])}</a>' for c in cs)
    page=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair · 10안 선택 V10</title><style>{css}</style></head><body><div class="hero" id="top"><small>Q-AI FAIR · V10 · STORY BEFORE VIDEO</small><h1>10개의 이야기.<br>어느 반전으로 시작할까요?</h1><p>기존 1–5안 보완 + 신규 6–10안. 화면과 후처리 자막으로 이해하는 선택용 콘티입니다. 캐릭터·상황·반전은 안별로 구분했습니다.</p><p>PNG와 Flow 영상에는 자막을 굽지 않습니다. 아래 자막 버튼은 후편집 위치 확인용입니다. 이번 작업에서 Flow 생성·크레딧 사용은 없습니다.</p></div><nav class="nav">{nav}</nav><main><div class="overview">{"".join(cards)}</div><div class="selection"><b>마음에 드는 안을 비교 후보로 표시하세요</b><p id="chosen">아직 표시한 안이 없습니다.</p><p id="quantity"></p><button id="save-choice">선택 메모 저장</button><p>표시는 이 페이지에서만 작동합니다. 영상 생성 요청은 제출되지 않습니다.</p></div>{"".join(sections)}<div class="notes"><a href="STORYBOARDS.md">10안 컷 표</a><a href="ALL_IMAGES.md">전체 이미지 콘티</a><a href="CASTING.md">캐스팅 구분</a><a href="PRODUCTION_NOTES.md">제작 메모</a><a href="review_summary.json">검수 기록</a><p>행사명 외 세부 일정·장소·참석 방법·실제 성과 수치는 미확인. 허구 장면입니다. 정지 콘티 검수는 실제 영상의 움직임·관객 반응 검증이 아닙니다.</p></div></main><script>{script}</script></body></html>'
    (R/'index.html').write_text(page,encoding='utf-8')
    preserved=[]
    for x in read(R/'preservation_baseline.json'):
        assert sha(ROOT/x['path'])==x['sha256'],x['path'];preserved.append(x['path'])
    put(R/'validation.json',{'concept_count':len(cs),'images':checks,'image_counts':count,'durations':timing,'preserved_count':len(preserved),'flow_requests':0,'video_audio_files_in_run':len(list(R.rglob('*.mp4')))+len(list(R.rglob('*.wav'))),'scope':'File, timing and image decoding checks. Independent content/image review is recorded separately.'})
    print('Built 10 concepts,',len(checks),'images; preserved',len(preserved),'source files')
if __name__=='__main__':main()
