"""Build reviewable storyboards from the approved source. No media generation."""
from pathlib import Path
import json, html

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
data=json.loads((OUT/'storyboards.json').read_text(encoding='utf-8'))
def esc(v): return str(v).replace('|','／').replace('\n','<br>')
def text(v): return html.escape(str(v))
root_names={'C01':'01_감독님_아직인데요.md','C07':'07_셰프님_그것도_주세요.md','C10':'10_지구_대표_질문_있습니다.md'}
htmls=[]
for c in data['concepts']:
    cid=c['id']
    manifest=json.loads((OUT/'manifests'/f'{cid}_images.json').read_text(encoding='utf-8'))
    selected={v['scene_id']:v for v in (manifest.get('images') or manifest['scenes'])}
    lines=[f"# {cid} · {c['title']}",'',c['one_line'],'',f"**{c['format']} · {c['duration_seconds']}초 · 동작 영상 {c['motion_clip_count']}개 + 후처리 엔딩 5초**",'',f"핵심 메시지: {c['core_message']}",'','음성 대사 없이 화면과 후처리 자막으로 전달합니다. 아래 이미지는 각 씬의 동작 전 첫 프레임입니다. Flow 영상은 아직 만들지 않았습니다.','', '## 등장인물','']
    for cast in c['cast']:
        lines += [f"- **{cast['id']}**: {cast['appearance']} {cast['costume']}"]
    lines += ['', '## 컷별 콘티','', '| 씬·컷 | 구간 | 화면·행동·구도 | 후처리 자막 | 대사·내레이션 | BGM·효과음·정적 | 전환 | 의도 |','|---|---|---|---|---|---|---|---|']
    for s in c['shots']:
        captions='<br>'.join(f"{q['start']}–{q['end']}초: {q['text']}" for q in s['caption_cues'])
        lines.append('| '+' | '.join(map(esc,[f"{s['scene_id']} / {s['id']}",f"{s['start']}–{s['end']}초",s['action']+' '+s['composition'],captions,'없음',s['music_sfx_silence'],s['transition'],s['intent']]))+' |')
    lines += ['', '## 씬별 첫 프레임','']
    cards=[]
    for s in c['shots']:
        if not s['image_generation_required']:continue
        rel=(ROOT/selected[s['scene_id']]['image_path']).relative_to(OUT).as_posix()
        lines += [f"### {s['scene_id']} · {s['start']}–{s['end']}초",'',s['frame_start'],'',f"![{cid} {s['scene_id']} 첫 프레임]({rel})",'',f"**동작:** {s['action']}",'',f"**후합성:** {' / '.join(s['post_composites']) or '자막 별도'}",'']
        cards.append(f'<article><h3>{text(s["scene_id"])} · {s["start"]}–{s["end"]}초</h3><img loading="lazy" src="{rel}"><p>{text(s["frame_start"])}</p><p><b>동작</b> {text(s["action"])}</p><p class="caption">'+text(' / '.join(q['text'] for q in s['caption_cues']))+'</p></article>')
    lines += ['## 기록','',f'[정확한 생성 프롬프트·참조·이미지 검수](manifests/{cid}_images.json) · [콘티 검토](review_rounds.json) · [실제 이미지 교차 검토](image_review.json)','','실제 관객 반응을 측정한 결과는 아닙니다. 영상의 손·소품·물리적 동작은 향후 생성 후 다시 확인합니다. 행사 일시·장소·신청·성과 수치를 창작하지 않았습니다.']
    md='\n'.join(lines)+'\n'
    (OUT/f'{cid}_storyboard.md').write_text(md,encoding='utf-8')
    # Root document points to the same images and records, so GitHub can render it.
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    root_md=md.replace('](images/',']('+prefix+'images/').replace('](manifests/',']('+prefix+'manifests/').replace('](review_rounds.json)',']('+prefix+'review_rounds.json)').replace('](image_review.json)',']('+prefix+'image_review.json)')
    (ROOT/root_names[cid]).write_text(root_md,encoding='utf-8')
    htmls.append(f'<section id="{cid}"><h2>{text(cid)} · {text(c["title"])}</h2><p>{text(c["one_line"])}</p><p>{c["duration_seconds"]}초 · {c["motion_clip_count"]}개 동작 컷</p><div class="grid">'+''.join(cards)+'</div></section>')
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair 새 1·7·10 콘티</title><style>body{margin:0;background:#101820;color:#eef2f5;font:17px/1.65 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:28px}nav{position:sticky;top:0;padding:12px;background:#17252f;z-index:3}a{color:#8ce1d2;margin-right:28px}h1,h2,h3{line-height:1.2}section{scroll-margin-top:70px;margin:30px 0 70px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:22px}article{background:#20313c;padding:18px;border-radius:12px}img{width:100%;height:auto;display:block}.caption{font-weight:700;color:#a9eddd;white-space:pre-line}p{margin:.6em 0}</style><header><h1>Q-AI Fair · 새 1·7·10 콘티</h1><p>27개 씬 첫 프레임. 화면+후처리 자막 중심 · 동영상 미생성.</p></header><nav><a href="#C01">1 감독님, 아직인데요</a><a href="#C07">7 셰프님, 그것도 주세요</a><a href="#C10">10 지구 대표, 질문 있습니다</a></nav><main>'''+''.join(htmls)+'</main></html>'
(OUT/'index.html').write_text(page,encoding='utf-8')
print('Built 3 full root storyboards, 3 local boards, and gallery')
