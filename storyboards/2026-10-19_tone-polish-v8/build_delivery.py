"""Build an offline reading copy without altering original generated PNGs."""
from pathlib import Path
import json, html, hashlib, math
from PIL import Image, ImageOps, ImageDraw, ImageFont
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def prose(x):return ' / '.join(str(v) for v in x) if isinstance(x,list) else str(x or '없음')
def h(x):return html.escape(prose(x))
def md(x):return prose(x).replace('|','／').replace('\n','<br>')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 d=read('storyboards.json');cs=d['concepts'];m=read('scene_manifest.json');mapping={(e['concept_id'],e['cut_id']):e for e in m['images']}
 checks=[];sections=[];overview=[];rows=['# 1·3·5안 유지, 2·4안 대사·연출 보완 — V8','','V7 C01·C03·C05의 콘티와 채택 PNG 25장은 그대로 유지했습니다. 2·4안은 이야기와 AI 역할을 살려 대사·호흡·체면을 지키는 행동을 다듬었습니다. 기존 완성 C01 36초 동영상도 보존했습니다. 이번 결과는 시나리오와 컷별 첫 프레임입니다. Flow·동영상·음원 생성은 하지 않았습니다.','','| 안 | 제목 | 목적·추천 용도 | 형식·웃음 | 길이 | B급 강도 | 제작 난이도 |','|---|---|---|---|---|---|---|']
 for c in cs:rows.append('| '+' | '.join(map(md,[c['id'],c['title'],c['purpose'],c.get('comedy_engine',c.get('format')),str(c['duration_seconds'])+'초',str(c.get('bgrade_intensity',4))+'/5',c['difficulty']]))+' |')
 rows+=['','강도와 난이도는 제작 판단입니다. 관객 반응이나 특정 영상 도구의 성공을 검증한 수치가 아닙니다.','']
 for c in cs:
  cid=c['id'];kept=cid in ['C01','C03','C05'];label='그대로 유지' if kept else '대사·연출 보완';cards=[];elapsed=0
  rows+=['## '+cid+' · '+c['title'],'',c['logline'],'','핵심 메시지: '+c['core_message'],'','캐스팅: '+' / '.join(x['description'] for x in c['characters']),'','| 씬·컷 | 구간·길이 | 화면·행동·구도 | 화면 자막 | 대사 | 음악·효과음·정적 | 전환 | 의도 |','|---|---|---|---|---|---|---|---|']
  for s in c['shots']:
   assert s['start']==elapsed and s['end']-s['start']==s['duration'];elapsed=s['end'];p=R/s['image_file'];e=mapping[cid,s['id']];assert p.is_file() and e['image_path']==s['image_file']
   with Image.open(p) as im:im.load();size=im.size;assert abs(size[0]/size[1]-16/9)<.08
   if not kept:
    assert e['generation_tool']=='image_gen'
    assert e['artist_review']['opened_actual_image'] is True
    original=Path(e['source_generated_path']);assert original.is_file() and sha(original)==sha(p)
   checks.append({'concept_id':cid,'cut_id':s['id'],'image':s['image_file'],'size':size,'sha256':sha(p),'retained':kept})
   rows.append('| '+' | '.join(map(md,[s['scene_id']+'/'+s['id'],f"{s['start']}–{s['end']}초 ({s['duration']}초)",s['screen']+' / '+s['framing'],s['subtitle'],s['dialogue'],s['sound'],s['transition'],s['intent']]))+' |')
   cards.append(f'''<article><button class="frame" data-src="{h(s['image_file'])}" data-caption="{cid} {s['id']}"><img src="{h(s['image_file'])}" loading="lazy" alt="{cid} {s['id']} 첫 프레임"></button><div class="copy"><small>{s['id']} · {s['start']}–{s['end']}초</small><p class="action">{h(s['screen'])}</p><p class="dialogue">{h(s['dialogue'])}</p><details><summary>첫 프레임과 다음 행동</summary><p><b>첫 프레임</b> {h(s['first_frame'])}</p><p><b>이후 동작</b> {h(s['next_motion'])}</p><p><b>자막</b> {h(s['subtitle'])}</p><p><b>음향</b> {h(s['sound'])}</p><p><b>구도·전환</b> {h(s['framing'])} / {h(s['transition'])}</p><p><b>연속성</b> {h(s['continuity_in'])} → {h(s['continuity_out'])}</p><p><b>후속 제작 메모</b> {h(s.get('postproduction_notes'))}</p><a href="{h(s['image_file'])}" download>PNG 원본</a></details></div></article>''')
  assert elapsed==c['duration_seconds'] and elapsed<=60
  hero=next(s for s in c['shots'] if s['id']==d['hero_cuts'][cid])
  overview.append(f'<a class="concept" href="#{cid}"><img src="{h(hero["image_file"])}"><div><small>{cid[-1]}안 · {label} · {elapsed}초</small><h2>{h(c["title"])}</h2><p>{h(c["logline"])}</p></div></a>')
  cast=''.join(f'<li>{h(x["description"])}</li>' for x in c['characters'])
  sections.append(f'<section id="{cid}"><header><small>{cid[-1]}안 · {label} · {h(c["purpose"])} · {elapsed}초</small><h2>{h(c["title"])}</h2><p class="logline">{h(c["logline"])}</p><details><summary>등장인물·연출 기준</summary><ul>{cast}</ul><p>{h(c.get("visual_style"))}</p></details></header><div class="shots">{"".join(cards)}</div><details><summary>행사 연결·제작 메모</summary><p>{h(c["core_message"])}</p><p>{h(c["final_action"])}</p><p>{h(c["difficulty"])}: {h(c["difficulty_reason"])}</p></details><a class="back" href="#top">↑ 전체 안</a></section>')
  rows+=['','| 씬·컷 | PNG 원본 | 첫 프레임 | 후속 움직임 |','|---|---|---|---|']
  for s in c['shots']:rows.append('| '+' | '.join(map(md,[s['scene_id']+'/'+s['id'],f"[{s['id']}]({s['image_file']})",s['first_frame'],s['next_motion']]))+' |')
  rows+=['','후속 제작 메모:']+[s['id']+' — '+s['postproduction_notes'] for s in c['shots'] if s.get('postproduction_notes')]
  rows+=['','마지막 연결: '+c['final_action'],'','연속성: '+prose(c.get('continuity')),'','제작 난이도: '+c['difficulty']+' — '+c['difficulty_reason'],'']
 for cid in ['C01','C03','C05']:assert next(c for c in cs if c['id']==cid)==read('retained_concept_'+cid+'.json')
 for e in read('preservation_manifest.json')['images']:assert sha(R/e['copy'])==e['sha256']
 preservation=read('preservation_manifest.json');assert sha(Path(preservation['old_completed_film_path']))==preservation['old_completed_film_sha256']
 assert len(checks)==len(mapping) and len(set(x['sha256'] for x in checks))==len(checks)
 assert not list(R.rglob('*.mp4')) and not list(R.rglob('*.wav'))
 rec=d.get('recommendations',{})
 rows+=['## 용도 제안','',prose(rec.get('attendance')),'',prose(rec.get('opening')),'','## 사실·검수 범위','','행사명: **2026년 품질팀 AI 실행 결과 발표 대회**. AI 실행 경험과 활용 사례 공유. 정확한 일시·장소·참석/추천/신청 방법·성과 수치·상금은 미확인으로 넣지 않았습니다. 인물과 사건은 허구입니다. 16:9·사내 시청은 제작 가정입니다.','','[전체 이미지 콘티](index.html) · [정확한 프롬프트·이미지 매핑](scene_manifest.json) · [검토 기록](review_summary.json) · [보존 증명](preservation_manifest.json)','','실제 이미지를 검토했으며 동작·음성·립싱크·관객 반응은 검증하지 않았습니다.']
 (R/'STORYBOARDS.md').write_text('\n'.join(rows),encoding='utf-8')
 nav=''.join(f'<a href="#{c["id"]}">{c["id"][-1]} · {h(c["title"])}</a>' for c in cs)
 css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f3efe6;color:#22231f;font:15px/1.65 "Malgun Gothic",sans-serif}a{color:inherit}.hero{background:#252522;color:#fbf5e9;padding:44px max(24px,calc((100vw - 1312px)/2))}.hero h1{font-size:52px;line-height:1.18;margin:18px 0}.hero p{max-width:850px}.hero small{color:#ffb572}small{font-size:12px;font-weight:bold;color:#a14a25}.nav{display:flex;gap:24px;overflow:auto;white-space:nowrap;position:sticky;top:0;background:#f3efe6f5;padding:14px 24px;border-bottom:1px solid #ccc4b6;z-index:2;font-size:12px}.nav a{text-decoration:none}main{max-width:1360px;margin:auto;padding:30px 24px 70px}.overview{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.concept{text-decoration:none;background:white;border:1px solid #d8cebf}.concept img,.frame img{display:block;width:100%;aspect-ratio:16/9;object-fit:contain}.concept div{padding:18px}.concept h2{font-size:23px;line-height:1.3}.concept p{font-size:14px}section{padding-top:56px;scroll-margin-top:48px}section header{border-top:4px solid #252522;padding:20px 0}section h2{font-size:40px;line-height:1.25;margin:10px 0}.logline{font-size:20px}.shots{display:grid;grid-template-columns:1fr 1fr;gap:20px}article{background:white;border:1px solid #d8cebf}.frame{padding:0;border:0;display:block;width:100%;cursor:zoom-in;background:#242424}.copy{padding:18px 22px}.action{font-size:17px}.dialogue{font-size:19px;font-weight:bold;white-space:pre-wrap;color:#713c25}details{border-top:1px solid #ddd3c3;padding-top:12px;margin-top:16px;font-size:13px}details p{white-space:pre-wrap}summary{cursor:pointer;font-weight:bold}.back{display:block;margin:18px 0;font-size:12px}.notes{margin-top:50px;padding-top:20px;border-top:3px solid #252522;font-size:13px}.notes a{margin-right:20px}dialog{max-width:96vw;max-height:96vh;border:0;padding:0;background:#222;color:white}dialog::backdrop{background:#000d}dialog img{max-width:94vw;max-height:86vh;display:block}dialog footer{padding:10px;display:flex;justify-content:space-between}@media(max-width:850px){.shots{grid-template-columns:1fr}.overview{grid-template-columns:1fr 1fr}.hero h1{font-size:40px}}@media(max-width:520px){.overview{grid-template-columns:1fr}section h2{font-size:30px}}'''
 text=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>1·3·5안 유지 / 2·4안 톤 보완 · V8</title><style>{css}</style></head><body id="top"><header class="hero"><small>AI 실행 결과 발표 대회 · V8</small><h1>1·3·5안은 그대로.<br>2·4안은 더 진지하게, 더 뻔뻔하게.</h1><p>유지한 세 안의 콘티와 이미지 25장은 변경하지 않았습니다. 2·4안의 사건과 AI 활용 과정은 유지했습니다. 인물이 끝까지 체면을 지키는 대사와 반응을 보강했습니다.</p><p>2장 첫 프레임 보완 + 41장 재사용 · 영상·음원·Flow 실행 없음</p></header><nav class="nav">{nav}</nav><main><div class="overview">{''.join(overview)}</div>{''.join(sections)}<div class="notes"><p>{h(rec.get('attendance'))}</p><p>{h(rec.get('opening'))}</p><p>첫 프레임과 계획된 대사·다음 행동을 함께 보는 콘티입니다. 영상 움직임·음성·관객 반응을 검증한 결과가 아닙니다. 행사명·자막은 후속 편집용 정보입니다.</p><p>행사명: 2026년 품질팀 AI 실행 결과 발표 대회. 일시·장소·신청 방법·실제 성과·상금은 미확인입니다. 인물과 사건은 허구이며 16:9·사내 시청은 제작 가정입니다.</p><a href="STORYBOARDS.md">전체 컷 표</a><a href="scene_manifest.json">정확한 프롬프트·매핑</a><a href="review_summary.json">검토·수정</a><a href="preservation_manifest.json">1·3·5안 보존</a></div></main><dialog id="viewer"><img id="full" alt="원본 첫 프레임"><footer><span id="caption"></span><button id="close">닫기 ×</button></footer></dialog><script>const v=document.querySelector('#viewer');document.querySelectorAll('[data-src]').forEach(b=>b.onclick=()=>{{document.querySelector('#full').src=b.dataset.src;document.querySelector('#caption').textContent=b.dataset.caption;v.showModal()}});document.querySelector('#close').onclick=()=>v.close();v.onclick=e=>{{if(e.target===v)v.close()}};</script></body></html>'''
 (R/'index.html').write_text(text,encoding='utf-8')
 out=R/'contact_sheets';out.mkdir(exist_ok=True);font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',20);title=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',27)
 for c in cs:
  sheet=Image.new('RGB',(1312,80+math.ceil(len(c['shots'])/2)*392),'#f3efe6');dr=ImageDraw.Draw(sheet);dr.text((18,20),f"{c['id']} · {c['title']} / {c['duration_seconds']}초",font=title,fill='#22231f')
  for i,s in enumerate(c['shots']):
   x=16+(i%2)*648;y=80+(i//2)*392
   with Image.open(R/s['image_file']) as im:thumb=ImageOps.contain(im.convert('RGB'),(632,355))
   sheet.paste(thumb,(x,y));dr.text((x,y+360),f"{s['id']} · {s['start']}–{s['end']}초",font=font,fill='#22231f')
  sheet.save(out/(c['id']+'_all_cuts.jpg'),quality=93)
 put('validation.json',{'status':'passed','concepts':5,'total_images':len(checks),'new_images':2,'reused_images':41,'retained_images':25,'C01_C03_C05_objects_unchanged':True,'retained_image_bytes_unchanged':True,'new_PNGs_match_generated_original_bytes':True,'old_film_sha256_unchanged':True,'new_video_or_audio':False,'browser_render_qa':'not_performed; existing local-file automation restriction respected','images':checks})
 print({'images':len(checks),'preserved':25,'gallery':'index.html'})
if __name__=='__main__':main()
