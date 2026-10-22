"""Build reading copies; never alter the generated upload PNGs."""
from pathlib import Path
import json, html, hashlib, math, sys
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
from PIL import Image, ImageOps, ImageDraw, ImageFont

R = Path(__file__).resolve().parent
ROOT = R.parents[1]
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(p, d): Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def prose(x):
    if isinstance(x,dict): return str(x.get('visible_cause_effect',x))
    return ' / '.join(map(str,x)) if isinstance(x,list) else str(x or '')
def h(x): return html.escape(prose(x))
def md(x): return prose(x).replace('|','／').replace('\n','<br>')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cue_style(q):
    b=q.get('box',{})
    if not b:return ''
    v=['right:auto','bottom:auto','left:'+str(b['left_pct'])+'%','width:'+str(b['width_pct'])+'%']
    anchor='top' if 'top_pct' in b else 'bottom'
    v += [anchor+':'+str(b[anchor+'_pct'])+'%']
    if 'font_cqw' in b:v.append('font-size:'+str(b['font_cqw'])+'cqw')
    return ';'.join(v)

def main():
    d=read(R/'storyboards.json'); cs=d['concepts']; units=d['generation_units']
    m=read(R/'scene_manifest.json'); images={e['id']:e for e in m['images']}
    assert len(units)==len(images)==44
    checks=[]; sections=[]; overview=[]
    rows=['# Q-AI Fair · 화면+자막 콘티 V9','','승인된 다섯 이야기의 설정·증거·선택을 화면+자막으로 전달하도록 보완하고 시작 이미지 44장을 새로 생성했습니다. 원본 PNG에는 자막을 넣지 않습니다. 아래 자막은 후편집 지시입니다. Flow 영상 생성·크레딧 사용은 없습니다.','','| 안 | 제목 | 목적·용도 | 형식 | 웃음 장치 | 길이 | B급 강도 | 난이도 | 시작 이미지 |','|---|---|---|---|---|---|---|---|---|']
    image_rows=['# 전체 이미지 콘티 · Q-AI Fair V9','','모든 시작 이미지가 포함된 GitHub 읽기용 문서입니다. HTML 원본은 내려받아 열면 자막 배치도 확인할 수 있습니다.','','[자막 배치 미리보기](index.html) · [전체 컷 표](STORYBOARDS.md) · [이미지·정확한 프롬프트](scene_manifest.json) · [검수 기록](review_summary.json)','']
    for c in cs:
        cu=[u for u in units if u['concept_id']==c['id']]
        rows.append('| '+' | '.join(map(md,[c['id'],c['title'],c['purpose'],c['format'],c['comedy_engine'],str(c['duration_seconds'])+'초',c['bgrade_intensity'],c['difficulty'],len(cu)]))+' |')
    for c in cs:
        cid=c['id']; shots={s['id']:s for s in c['shots']}; cu=[u for u in units if u['concept_id']==cid]
        rows+=['','## '+cid+' · '+c['title'],'',c['logline'],'','핵심 메시지: '+c['core_message'],'','| 씬·컷 | 구간·길이 | 화면·행동·구도 | 화면 자막 | 대사·내레이션 | 음악·효과음·정적 | 전환 | 의도 |','|---|---|---|---|---|---|---|---|']
        elapsed=0
        for s in c['shots']:
            assert abs(s['start']-elapsed)<.001 and abs(s['end']-s['start']-s['duration'])<.001
            elapsed=s['end']
            cue=' / '.join(f"{q['start']}–{q['end']}초: {q['text']}" for q in s.get('caption_cues',[])) or '무자막'
            rows.append('| '+' | '.join(map(md,[s['scene_id']+'/'+s['id'],f"{s['start']}–{s['end']}초 ({s['duration']}초)",s['screen']+' / '+s['framing'],cue,s['dialogue'],s['sound'],s['transition'],s['intent']]))+' |')
        assert abs(elapsed-c['duration_seconds'])<.001 and elapsed<=60
        image_rows+=['','## '+cid+' · '+c['title'],'',c['logline'],'']
        cards=[]
        for u in cu:
            e=images[u['id']]; p=R/e['image_path']; s=shots[u['linked_shot']]
            assert p.exists(); im=Image.open(p); im.load(); size=im.size
            assert abs(size[0]/size[1]-16/9)<.08
            assert e['generation_tool']=='image_gen'
            assert e['artist_review']['opened_actual_image'] is True
            original=Path(e['source_generated_path'])
            assert original.exists() and sha(original)==sha(p)
            checks.append({'id':u['id'],'image':e['image_path'],'size':size,'sha256':sha(p)})
            cues=s.get('caption_cues',[])
            cuebuttons=''.join(f'<button class="cue" data-text="{h(q["text"])}" data-placement="{h(q.get("placement","bottom"))}" data-kind="{h(q.get("kind",""))}" data-style="{h(cue_style(q))}">{q["start"]}–{q["end"]}초 · {h(q["text"])}</button>' for q in cues)
            cards.append(f'''<article><div class="stage"><img src="{h(e['image_path'])}" alt="{u['id']} 새 시작 이미지" loading="lazy"><div class="caption bottom"></div></div><div class="copy"><small>{u['id']} · {s['start']}–{s['end']}초</small><h3>{h(u['first_frame'])}</h3><p><b>다음 동작</b> {h(u['action'])}</p><div class="cues"><button class="cue" data-text="" data-placement="bottom">원본</button>{cuebuttons}</div><details><summary>구도·음향·후편집 메모</summary><p>{h(u['framing'])}</p><p>자막 안전 영역: {h(u['caption_safe_zone'])}</p><p>음향: {h(s['sound'])}</p><p>{h(s.get('mute_readability'))}</p></details><a class="download" href="{h(e['image_path'])}" download>시작 PNG 원본</a></div></article>''')
            image_rows += [f"### {u['id']} · {s['start']}–{s['end']}초",'',f"![{u['id']} 새 시작 이미지]({e['image_path']})",'','**첫 상태:** '+u['first_frame'],'','**다음 동작:** '+u['action'],'','**자막:** '+(' / '.join(f"{q['start']}–{q['end']}초 {q['text']}" for q in cues) or '무자막'),'','**음향:** '+prose(s['sound']),'']
        hero=images[cu[0]['id']]['image_path']
        overview.append(f'<a class="overview-card" href="#{cid}"><img src="{h(hero)}"><div><small>{cid} · 새 이미지 {len(cu)}장 · {c["duration_seconds"]}초</small><h2>{h(c["title"])}</h2><p>{h(c["logline"])}</p></div></a>')
        cast=' / '.join(x['description'] for x in c['characters'])
        sections.append(f'<section id="{cid}"><header><small>{cid} · {h(c["purpose"])} · {c["duration_seconds"]}초</small><h2>{h(c["title"])}</h2><p class="logline">{h(c["logline"])}</p><details><summary>인물·연출 기준</summary><p>{h(cast)}</p><p>{h(c.get("visual_style"))}</p></details></header><div class="shots">{"".join(cards)}</div><a class="back" href="#top">↑ 전체 안</a></section>')
    assert len({x['sha256'] for x in checks})==44
    oldhash={x['sha256'] for x in read(R/'preservation_baseline.json')}
    assert not oldhash.intersection(x['sha256'] for x in checks)
    preserved=[]
    for e in read(R/'preservation_baseline.json'):
        assert sha(ROOT/e['path'])==e['sha256']; preserved.append(e['path'])
    legacy=read(ROOT/'storyboards/2026-10-19_tone-polish-v8/preservation_manifest.json')
    assert sha(legacy['old_completed_film_path'])==legacy['old_completed_film_sha256']
    preserved.append(legacy['old_completed_film_path'])
    assert not list(R.rglob('*.mp4')) and not list(R.rglob('*.wav'))
    rows+=['','## 제작 범위와 확인 사항','','43개 편집 컷을 44개 시작 이미지로 준비했습니다. C05 K02A/B는 기둥 빼기와 몸 접기의 서로 다른 시작 상태입니다. 기존 C03 v03 원본·편집은 재사용 우선입니다. 이번 신규 이미지 8장이 기존 C03 영상 8컷 재생성 지시는 아닙니다.','','행사명 Q-AI Fair 외 정확한 일정·장소·신청·혜택·성과 수치는 미확인입니다. 화면과 인물은 허구입니다. 음향은 선택 사항이며 필수 전달을 맡지 않습니다. 실제 영상화 뒤에는 움직임·자막 가독성·호흡을 별도 확인합니다.','','[모든 실제 이미지](ALL_IMAGES.md) · [자막 배치 보기](index.html) · [검수 기록](review_summary.json) · [제작 브리프](BRIEF.md)']
    (R/'STORYBOARDS.md').write_text('\n'.join(rows),encoding='utf-8')
    (R/'ALL_IMAGES.md').write_text('\n'.join(image_rows),encoding='utf-8')
    nav=''.join(f'<a href="#{c["id"]}">{c["id"][-1]} · {h(c["title"])}</a>' for c in cs)
    css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#efece4;color:#222;font:15px/1.65 "Malgun Gothic",sans-serif}a{color:inherit}.hero{background:#202925;color:#fff;padding:46px max(24px,calc((100vw - 1350px)/2))}.hero h1{font-size:48px;line-height:1.18;margin:16px 0}.hero p{max-width:960px}.hero small{color:#b7edb6}small{font-size:12px;font-weight:700;color:#47694b}.nav{display:flex;gap:23px;overflow:auto;white-space:nowrap;position:sticky;top:0;background:#efece4f5;padding:14px 24px;border-bottom:1px solid #c6c3b9;z-index:10;font-size:12px}.nav a{text-decoration:none}main{max-width:1400px;margin:auto;padding:30px 24px 70px}.overview{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.overview-card{text-decoration:none;background:#fff;border:1px solid #cecabe}.overview-card img{display:block;width:100%;aspect-ratio:16/9;object-fit:contain}.overview-card div{padding:18px}.overview-card h2{font-size:23px;line-height:1.3}section{padding-top:52px;scroll-margin-top:50px}section header{border-top:4px solid #202925;padding:20px 0}section h2{font-size:38px;line-height:1.25;margin:10px 0}.logline{font-size:20px}.shots{display:grid;grid-template-columns:1fr 1fr;gap:20px}article{background:white;border:1px solid #cecabe;min-width:0}.stage{position:relative;aspect-ratio:16/9;background:#141414;container-type:inline-size;overflow:hidden}.stage img{display:block;width:100%;height:100%;object-fit:contain}.caption{position:absolute;left:7%;right:7%;text-align:center;color:#fff;font-weight:800;font-size:3.4cqw;line-height:1.4;white-space:pre-line;padding:1.2% 2%;background:#000b;text-shadow:0 1px 2px #000;pointer-events:none}.caption:empty{display:none}.caption.bottom{bottom:6%}.caption.top{top:6%}.caption.middle{top:38%}.copy{padding:18px 22px}.copy h3{font-size:17px;font-weight:500}.cues{display:flex;flex-wrap:wrap;gap:7px}.cue{border:1px solid #c4ccbc;background:#f0f6eb;padding:7px 10px;border-radius:4px;cursor:pointer;font:12px/1.4 inherit;text-align:left}.cue.active{background:#314a35;color:#fff}details{border-top:1px solid #ddd5c4;padding-top:12px;margin-top:16px;font-size:13px}summary{cursor:pointer;font-weight:700}.download{display:inline-block;margin-top:15px;font-size:13px}.back{display:block;margin-top:20px}.notes{margin-top:45px;border-top:3px solid #202925;padding-top:20px}.notes a{margin-right:18px}@media(max-width:850px){.shots{grid-template-columns:1fr}.overview{grid-template-columns:1fr 1fr}.hero h1{font-size:38px}}@media(max-width:520px){.overview{grid-template-columns:1fr}section h2{font-size:29px}}'''
    css+=' .caption.event{font-size:3cqw;padding:.6% 1.2%;line-height:1.3}.caption.event strong{font-size:5cqw;line-height:1.2;display:block;margin-bottom:.4cqw}'
    page=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair · 화면+자막 V9 · 시작 이미지 44장</title><style>{css}</style></head><body id="top"><header class="hero"><small>Q-AI Fair · V9</small><h1>소리를 놓쳐도,<br>반전은 놓치지 않게.</h1><p>다섯 이야기의 시작 이미지 44장을 새로 생성했습니다. 자막 버튼으로 문구와 대략적인 배치를 확인하세요. PNG 원본에는 글을 굽지 않았습니다.</p><p>정지 프레임에서 자막 배치만 보는 화면입니다. 후속 행동·전체 자막 타이밍은 아래 컷 표에 따릅니다. Flow 영상 생성·크레딧 사용 없음.</p></header><nav class="nav">{nav}</nav><main><div class="overview">{''.join(overview)}</div>{''.join(sections)}<footer class="notes"><p>첫 프레임의 검수는 실제 동작 성공·현장 가독성·관객 반응을 검증한 것이 아닙니다. 기존 C03 영상은 재사용 우선이며, C03 새 이미지 8장이 영상 재생성 지시는 아닙니다.</p><a href="ALL_IMAGES.md">GitHub용 전체 이미지</a><a href="STORYBOARDS.md">전체 컷 표</a><a href="scene_manifest.json">프롬프트·매핑</a><a href="review_summary.json">검수 기록</a><a href="BRIEF.md">제작 브리프</a></footer></main><script>document.querySelectorAll('.cue').forEach(b=>b.onclick=()=>{{const a=b.closest('article'),c=a.querySelector('.caption');let p=b.dataset.placement||'';c.className='caption '+(/상단|top|upper/.test(p)?'top':/중앙|middle|center/.test(p)?'middle':'bottom');c.setAttribute('style',b.dataset.style||'');c.textContent=b.dataset.text;if(b.dataset.kind==='event'){{c.classList.add('event');let lines=b.dataset.text.split('\\n');c.textContent='';let t=document.createElement('strong');t.textContent=lines.shift();c.appendChild(t);c.appendChild(document.createTextNode(lines.join('\\n')))}};a.querySelectorAll('.cue').forEach(x=>x.classList.remove('active'));b.classList.add('active')}});</script></body></html>'''
    (R/'index.html').write_text(page,encoding='utf-8')
    out=R/'contact_sheets';out.mkdir(exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',22); title=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',29)
    for c in cs:
        cu=[u for u in units if u['concept_id']==c['id']]
        sheet=Image.new('RGB',(1312,80+math.ceil(len(cu)/2)*392),'#efece4');dr=ImageDraw.Draw(sheet)
        dr.text((18,20),f"{c['id']} · {c['title']} / 새 시작 이미지 {len(cu)}장",font=title,fill='#222')
        for i,u in enumerate(cu):
            x=16+i%2*648;y=80+i//2*392
            im=Image.open(R/images[u['id']]['image_path']).convert('RGB');thumb=ImageOps.contain(im,(632,355))
            sheet.paste(thumb,(x,y));dr.text((x,y+359),u['id'],font=font,fill='#222')
        sheet.save(out/(c['id']+'_all_starts.jpg'),quality=94)
    put(R/'validation.json',{'status':'passed','new_images':44,'reused_images':0,'concepts':5,'source_bytes_match':True,'prior_files_unchanged':len(preserved),'flow_requests':0,'new_video_or_audio':False,'browser_render_qa':'not yet recorded','images':checks})
    print('Built 44-image gallery, full Markdown, contact sheets, byte and timing validation.')

if __name__=='__main__': main()
