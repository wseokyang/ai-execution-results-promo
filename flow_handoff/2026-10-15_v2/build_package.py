#!/usr/bin/env python3
"""Build a portable local Flow handoff. Does not call Flow or render video."""
import argparse, csv, hashlib, html, json, shutil, struct, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
SOURCE = PROJECT / 'storyboards/2026-10-15_absurd-v2'

def read(path):
    return json.loads(Path(path).read_text())

def write(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def save(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

def table(path, rows, fields):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)

def stamp(t):
    n = round(t * 1000)
    return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'

def short(t):
    return f'{int(t)//60:02}:{int(t)%60:02}'

def srt(rows):
    return '\n\n'.join(f'{i+1}\n{stamp(r[0])} --> {stamp(r[1])}\n{r[2]}' for i,r in enumerate(rows)) + '\n'

def png_info(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    w,h = struct.unpack('>II', data[16:24])
    return dict(width=w, height=h, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))

CAST = {
 'C01': 'A is the short-haired man in a white shirt. B is the bob-haired woman in a navy cardigan. C is the middle-aged cleaner in a lime work vest. D is the calm female presenter in a charcoal jacket. Keep only the cast visible in this shot. Preserve the yellow bucket with black handle, gray mop and existing room. A\'s original handkerchief passes to C; B later uses her OWN separate handkerchief. Never conjure a third one.',
 'C02': 'A is the white-shirted man in charcoal trousers and black socks. B is the blue-shirted woman in gray trousers and gray socks. C is the green-vested worker wearing his own black work shoes. D is the beige-jacketed female usher. Autonomous shoes are exactly one black Oxford pair, one white sneaker pair and one brown loafer pair. No added faces or limbs. Beige sack, red drawcord; chair and shoe fronts face the stage.',
 'C03': 'A is the beige-shirted human with a white mug. B is the blue-gray alien commander in a purple uniform with exactly FOUR arms. C is the pale gray technician in a black uniform with TWO arms. Preserve their faces, limb attachment points, costumes, spacecraft wall design and props. No additional alien audience or changing species.',
 'C04': 'The employee is the same short black pixie-haired woman in a pale gray shirt. Original cardboard robots: A red antenna and very short cardboard CLAWS; B blue antenna and ordinary hands; C yellow antenna and broad cardboard shoulders. Flat duplicates are exactly three copies of A with deliberate green edges. Preserve the visible cast, faces, tape seams and antenna colors; no polished metal redesign or extra arms.',
 'C05': 'The employee is the same man in a beige knit. Ghost A has a long wig and red pin, B a short wig and blue pin, C a crooked wig and yellow pin. Preserve their faces and deliberately crude green keying edges. In office ghost scenes C\'s neon green-and-pink tracksuit and WHITE sneakers are fully hidden by white cloth except during the explicit reveal. At the final audience scene preserve the visible dark jackets and wigs.'
}
STYLE = {
 'C01':'Expensive live-action melodrama advertisement: sincere exaggerated emotion, warm directional side light, deep cinematic shadows, shallow focus. No laugh-track wink.',
 'C02':'Expensive live-action absurd chase advertisement: tactile shoes, serious action-film lighting and convincing physical weight, comic events played straight.',
 'C03':'Expensive cinematic science-fiction advertisement, tangible spaceship materials and restrained dramatic lighting; absurd human behavior within a serious alien invasion.',
 'C04':'Deliberately low-budget live-action B-commercial: handmade cardboard, visible tape, intentionally crude flat keying, exaggerated performances and mundane fluorescent office light. Do not beautify away the cheap effects.',
 'C05':'Deliberately low-budget live-action B-commercial: cheap floating keying, mismatched cutout scales, obvious green fringes and shameless overacting. Keep the absurd story and intentional poor compositing.'
}
SPEAKERS = {'A':'A','B':'B','C':'C','D':'D','D · 화면 밖':'D, the offscreen presenter','직원':'the employee','직원 · 화면 밖':'the offscreen employee','발표자 · 문 안쪽':'the offscreen speaker inside the hall','로봇들':'the original robots together','복제들':'the flat duplicates together','마지막 복제':'the last flat duplicate'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--zip', action='store_true')
    args=parser.parse_args()
    source=read(SOURCE/'storyboards.json')
    old={c['id']:c for c in source['concepts']}
    motions=read(ROOT/'authoring/motion_specs.json')
    dialogue=read(ROOT/'authoring/dialogue_cues.json')
    drafts=[read(ROOT/f) for f in ['draft_C01_C02.json','draft_C03.json','draft_C04_C05.json']]
    jobs={}
    for d in drafts[:2]:
        for c in d['concepts']:
            for j in c['new_start_images']:
                jobs[j['id']]=dict(j, source_path=j['planned_path'])
    for j in drafts[2]['new_images']:
        jobs[j['id']]=dict(j, source_path=str(ROOT/j['proposed_path']))
    references={}
    for scene in read(SOURCE/'scene_manifest.json')['scenes']:
        src=SOURCE/scene['image_path']
        rel=f"references/{scene['concept_id']}/{src.name}"
        (ROOT/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,ROOT/rel)
        references[(scene['concept_id'],scene['scene_id'])]=rel
    assets={}
    missing=[]
    concepts=[]
    allclips=[]
    def asset(cid, aid=None, existing=None):
        if aid:
            src=Path(jobs[aid]['source_path'])
            kind='new_start_frame'
        else:
            src=Path(existing)
            aid=f'{cid}_R_{src.stem}'
            kind='approved_representative_reused_as_start'
        rel=f'upload_frames/{cid}/{aid}.png'
        if aid not in assets:
            a=dict(id=aid,path=rel,kind=kind,source_path=str(src.relative_to(PROJECT)),exists=src.exists())
            if src.exists():
                (ROOT/rel).parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(src,ROOT/rel)
                a.update(png_info(ROOT/rel))
            else: missing.append(str(src))
            assets[aid]=a
        return assets[aid]

    for draft in drafts:
      for c in draft['concepts']:
        cid=c['id']; original=json.loads(json.dumps(old[cid]))
        # Keep the original source file untouched; the handoff describes final blocking.
        if cid=='C01':
            original['cuts'][6]['visual']=original['cuts'][6]['visual'].replace('A가 작은 손수건을 접는다.', 'B가 자기 손수건 H2를 접는다. C는 A에게 받은 H1을 유지한다.')
        if cid=='C03':
            original['cuts'][1]['visual']='네 팔 지휘관 B가 A를 압박한다. 스캐너는 이미 A 위에 정렬돼 있고 C는 작동 버튼 직전까지 준비한다. 실제 작동광과 짬뽕 공개는 다음 컷.'
            original['cuts'][1]['audio']='낮고 엄숙한 외계 음성과 우주선의 대기음. 작동 기계음은 아직 없다.'
            original['cuts'][1]['transition']='C의 버튼 직전 손에서 같은 빈 패널 구도로 컷.'
            original['cuts'][2]['audio']='스캐너가 켜지는 기계음 → 거창한 분석 완료음 → 국물 보글거리는 소리. 위협적인 음악은 아직 남아 있다.'
            original['cuts'][6]['visual']='A의 질문에 B의 위쪽 한 팔이 올라가면 다른 위쪽 손이 높은 위치에서 그 손목을 붙잡아 정지시킨다. 아직 내리지 않는다. 아래 두 팔은 필기한다.'
        cutbyid={x['id']:x for x in original['cuts']}
        clips=[]
        for raw in c.get('clips',c.get('generation_clips',[])):
            isb='start_asset' in raw
            im=raw['start_asset'] if isb else raw['image']
            if isb:
                ids=raw['original_cut_ids'];tc=raw['edit_timecode'];start,end=tc['start_seconds'],tc['end_seconds']
                if im['mode']=='new_image': a=asset(cid,aid=im['asset_id'])
                elif im['mode']=='existing_image': a=asset(cid,existing=im['path'])
                else:
                    missing.append('Unresolved start dependency: '+raw['id']);continue
                action=raw['primary_action'];notes=raw['edit_notes']
            else:
                ids=raw['source_cut_ids'];start,end=raw['edit_start'],raw['edit_end']
                a=asset(cid,aid=im.get('new_start_asset_id'),existing=im.get('existing_image_path'))
                action=raw['core_action'];notes=raw.get('secondary_motion_timing','')+' '+raw.get('continuity_note','')
            duration=end-start
            cues=[dict(start=s,end=e,speaker=sp,text=tx) for s,e,sp,tx in dialogue[cid] if start<=s<end]
            for q in cues: assert q['end']<=end,(raw['id'],q)
            refs=sorted(set(references[(cid,cutbyid[i]['scene'])] for i in ids))
            base=(f'Create one continuous 8-second landscape 16:9 shot from the attached FIRST FRAME. Preserve its initial composition, visible identities and wardrobe.\n\nSTYLE: {STYLE[cid]}\nCONTINUITY: {CAST[cid]}\n\nACTION: {motions[raw["id"]]}\n\nTIMING: The final edit uses {duration} seconds of this shot. Complete the important action and reaction within the first {duration} seconds; use any remaining time up to 8 seconds for a natural held end pose or small continuing motion. Do not postpone the payoff into the discarded tail. No cuts, montage, slow motion or replay.\n\nNo generated captions, subtitles, event title, logos or watermark. Any pictured blank screen stays unlettered. Do not replace the scene with a title card. Keep camera movement limited to the action instructions above.')
            native=[]
            for q in cues:
                native.append(f'At about {q["start"]-start:.1f}–{q["end"]-start:.1f}s, {SPEAKERS[q["speaker"]]} says in Korean exactly: “{q["text"]}”')
            audio=('\n\nAUDIO: Natural ambience and action sounds, no music or extra voices. '+ ('Perform these short lines in order, preserving the pauses and speaker identity. Offscreen lines must stay offscreen.\n'+'\n'.join(native) if native else 'No spoken words in this shot.'))
            silent='\n\nAUDIO ALTERNATIVE: No intelligible speech, no narration and no music. Use expressive acting with quiet mouth movements suitable for later Korean dubbing. Natural movement sounds only. Dialogue will be added in the edit; do not invent speech.'
            prompt_path=f'prompts/{cid}/{raw["id"]}_korean_dialogue.txt'
            motion_path=f'prompts/{cid}/{raw["id"]}_motion_only.txt'
            save(prompt_path,base+audio+'\n');save(motion_path,base+silent+'\n')
            clip=dict(id=raw['id'],concept_id=cid,source_cut_ids=ids,edit_start=start,edit_end=end,edit_seconds=duration,requested_generation_seconds=8,model_preset='Veo 3.1 Fast',mode='Frames',first_frame=a['path'],asset_id=a['id'],end_frame=None,ingredients=[],reference_only=refs,start_state=raw['start_state'],end_state=raw['end_state'],action=action,camera=raw['camera'],continuity=raw['continuity'],edit_notes=notes.strip(),prompt_native=prompt_path,prompt_motion_only=motion_path,dialogue=cues,planned_source_in=0,planned_source_out=duration,trim_status='planned_only_adjust_after_actual_generation',generation_status='not_uploaded_not_generated',qa=[raw['end_state'],'핵심 동작이 선택 구간 안에 완료','첫 프레임과 인물·복장·소품 수량 일치','화면 자막·로고·새 인물 없음','대사 화자·순서 확인, 부정확하면 별도 더빙','움직임이 틀린 부분을 무리한 배속으로 숨기지 않음'])
            clips.append(clip);allclips.append(clip)
            clip['suggested_download_name']=raw['id']+'_take01.mp4'
        end=original['cuts'][-1]
        post=[]
        if cid=='C05':
            post.append(dict(id='C05-E00',kind='empty_wall_hold',start=35,end=37,seconds=2,source='references/C05/S03.png',crop_pixels=dict(x=1460,y=420,width=210,height=118),audio='완전 정적: 말·음악·효과음 모두 중지',notes='인물·손·그림자 없는 빈 벽. 2초 유지 뒤 C의 노크로 전환. 이 크롭은 후편집용이며 Flow 입력이 아니다.'))
        post.append(dict(id=cid+'-E01',kind='endcard',start=end['start'],end=end['end'],seconds=6,overlay=f'post/{cid}/title_overlay.svg',standalone=f'post/{cid}/endcard.svg',preferred_background='이 안의 마지막 생성 클립에서 검수된 최종 프레임',fallback='같이 제공한 독립 타이틀 카드 사용',caption=end['caption'],notes='행사명 6초 온전히 유지. C02는 주인이 앉기 전 기존 대표 이미지로 되돌리지 않는다. 일시·장소·신청 URL 미확정으로 삽입하지 않음.'))
        concepts.append(dict(id=cid,title=c['title'],duration_seconds=original['duration'],style=original['style_label'],clips=clips,post_edit=post,source_cuts=original['cuts']))

    # Explicit edit crops: pixel coordinates refer to the prepared still (1672 x 941),
    # and are normalized when used against generated video of another resolution.
    crops={
      'C05-F01':[dict(start=0,end=5,x=540,y=0,w=520,h=293,purpose='A만 공개, B/C 숨김')],
      'C05-F02':[dict(start=5,end=8,x=55,y=150,w=490,h=276,purpose='B 첫 공개'),dict(start=8,end=10,x=890,y=250,w=500,h=281,purpose='C 첫 공개'),dict(start=10,end=11,x=0,y=0,w=1672,h=941,purpose='전체 합성 공개')],
      'C05-F08':[dict(start=37,end=43,x=1020,y=140,w=650,h=366,purpose='C와 빈 벽. 정확한 신규 이미지·영상에서 손/얼굴 위치 재확인')],
      'C05-F09':[dict(start=43,end=45.7,x=810,y=270,w=420,h=236,purpose='C 얼굴만: 가슴과 놀란 A/B 숨김'),dict(start=45.7,end=46.9,x=20,y=270,w=450,h=253,purpose='A의 누가? 얼굴만'),dict(start=46.9,end=49,x=0,y=0,w=1672,h=941,purpose='내 생각!에서 처음 자기 가슴 지목 공개')]
    }
    for c in allclips:
        c['edit_crops']=crops.get(c['id'],[])
        if c['edit_crops']: c['crop_note']='정지 이미지 기준 가안. 생성 결과의 얼굴·손 위치가 바뀌면 같은 공개 순서로 재조정. 원본 영상 폭/1672, 높이/941로 좌표 환산.'

    def svg(cid,caption,overlay=False):
        lines=caption.splitlines(); tag,main,cta=lines[0],lines[1],lines[2]
        accent={'C01':'#edc495','C02':'#a2ded1','C03':'#a9c7ff','C04':'#f3ff71','C05':'#c8ff72'}[cid]
        bg='<rect width="1920" height="1080" fill="#09121c"/>' if not overlay else '<rect x="70" y="242" width="1780" height="596" rx="24" fill="#09121c" fill-opacity="0.88"/>'
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><title>{html.escape(caption)}</title>{bg}<g font-family="Noto Sans CJK KR, Noto Sans KR, sans-serif" text-anchor="middle"><rect x="900" y="312" width="120" height="6" fill="{accent}"/><text x="960" y="406" fill="{accent}" font-size="42">{html.escape(tag)}</text><text x="960" y="555" fill="white" font-size="98" font-weight="700">{html.escape(main)}</text><text x="960" y="699" fill="#d9e1ea" font-size="43">{html.escape(cta)}</text></g></svg>'''
    timeline=[];dialogue_rows=[];caption_rows=[];logs=[]
    for concept in concepts:
        cid=concept['id']
        for c in concept['clips']:
            timeline.append(dict(concept=cid,id=c['id'],kind='Flow clip',start=c['edit_start'],end=c['edit_end'],seconds=c['edit_seconds'],input=c['first_frame'],planned_trim_in=0,planned_trim_out=c['edit_seconds'],note=c['edit_notes']))
            logs.append(dict(clip_id=c['id'],prompt_variant='korean_dialogue',model='Veo 3.1 Fast',requested_seconds=8,output_count=1,status='NOT_STARTED',actual_duration='',source_file='',source_in='',source_out='',accepted='',notes=''))
        for p in concept['post_edit']:
            timeline.append(dict(concept=cid,id=p['id'],kind=p['kind'],start=p['start'],end=p['end'],seconds=p['seconds'],input=p.get('standalone',p.get('source')),planned_trim_in='',planned_trim_out='',note=p['notes']))
            if p['kind']=='endcard':
                save(p['standalone'],svg(cid,p['caption']));save(p['overlay'],svg(cid,p['caption'],True))
        for s,e,sp,tx in dialogue[cid]:dialogue_rows.append(dict(concept=cid,start=s,end=e,speaker=sp,text=tx))
        save(f'post/{cid}/dialogue_optional_subtitles.srt',srt([(s,e,tx) for s,e,sp,tx in dialogue[cid]]))
        caps=[(x['start'],x['end'],x['caption']) for x in concept['source_cuts'] if x['caption']]
        save(f'post/{cid}/planned_captions.srt',srt(caps))
        for s,e,tx in caps:caption_rows.append(dict(concept=cid,start=s,end=e,text=tx))
        table(f'post/{cid}/sound_and_transitions.tsv',[dict(cut=x['id'],start=x['start'],end=x['end'],sound=x['audio'],transition=x['transition']) for x in concept['source_cuts']],['cut','start','end','sound','transition'])
    timeline.sort(key=lambda x:(x['concept'],x['start']))
    table('edit_timeline.tsv',timeline,['concept','id','kind','start','end','seconds','input','planned_trim_in','planned_trim_out','note'])
    table('dialogue.tsv',dialogue_rows,['concept','start','end','speaker','text'])
    table('captions.tsv',caption_rows,['concept','start','end','text'])
    table('generation_log_template.tsv',logs,list(logs[0]))
    table('upload_order.tsv',[dict(order=i+1,concept=c['concept_id'],clip=c['id'],first_frame=c['first_frame'],prompt=c['prompt_native'],alternate_prompt=c['prompt_motion_only'],model=c['model_preset'],mode='Frames · first only',generation_seconds=8,edit_seconds=c['edit_seconds'],output_count=1) for i,c in enumerate(allclips)],['order','concept','clip','first_frame','prompt','alternate_prompt','model','mode','generation_seconds','edit_seconds','output_count'])
    ready=not missing
    review_path=ROOT/'review_summary.json'
    review=read(review_path) if review_path.exists() else {'status':'pending'}
    manifest=dict(status='ready_for_local_review' if ready else 'building_assets',created_date='2026-10-15',scope='Local files only; no Flow upload, video generation, credits or account changes',settings=dict(mode='Frames',input='first_frame_only',model_proposal='Veo 3.1 Fast',fallback='Veo 3.1 Lite if available',aspect_ratio='16:9',requested_seconds=8,outputs_per_clip=1,account_options_verified=False,native_resolution='select available UI option; do not confuse upscale with native output',audio='Korean dialogue prompt + motion-only alternate; exact speech and silence not guaranteed'),counts=dict(concepts=len(concepts),clips=len(allclips),new_start_assets=sum(a['kind']=='new_start_frame' for a in assets.values()),unique_upload_images=len(assets),reference_images=len(references),post_edit_segments=sum(len(c['post_edit']) for c in concepts)),assets=list(assets.values()),concepts=concepts,review=review,missing=missing)
    if ready and review.get('status')=='complete':manifest['status']='ready_for_flow_upload'
    write('handoff_manifest.json',manifest)
    # Only selected copies belong in the upload folder; originals remain in source folders.
    selected={a['path'] for a in assets.values()}
    for copied in (ROOT/'upload_frames').glob('*/*.png'):
        if str(copied.relative_to(ROOT)) not in selected:
            copied.unlink()
    write('edit_crops.json',dict(coordinate_reference=[1672,941],shots=crops))
    write('asset_checksums.json',{a['path']:a.get('sha256') for a in assets.values()})
    generation_records={}
    for filename in ['image_manifest_C01_C02.json','image_manifest_C03.json','image_manifest_C04_C05.json']:
        if (ROOT/filename).exists():generation_records[filename]=read(ROOT/filename)
    write('image_generation_records.json',dict(tool='built-in image_gen',note='생성 프롬프트·원본 출처 기록. 실행 입력은 handoff_manifest.json의 상대 경로를 사용.',records=generation_records))
    checks=[]
    assert len(allclips)==41, len(allclips)
    assert set(motions)=={c['id'] for c in allclips}, 'Missing/extra motion prompts'
    for c in concepts:
        seg=sorted([r for r in timeline if r['concept']==c['id']],key=lambda r:r['start'])
        cursor=0
        for r in seg:
            assert r['start']==cursor,(c['id'],r)
            cursor=r['end']
        assert cursor==c['duration_seconds'] and cursor<60
        checks.append(f"{c['id']}: {cursor}s, contiguous edit timeline, 6s endcard")
    for a in assets.values():
        if a['exists']: assert abs(a['width']/a['height']-16/9)<0.02, a
    checks+=['41 unique clip IDs and matching English action specs','All generation requests 8 seconds; all planned clip trims <=8 seconds','Korean dialogue cues fit their clip intervals','No Ingredients inputs or required previous-video frame dependency','All selected start frames have SHA-256 and PNG dimension checks' if ready else 'Some images still being generated']
    validation=dict(status='pass' if ready else 'pending_assets',checks=checks,missing=missing,not_validated=['No actual Flow video generated','Actual animation, dialogue pronunciation, lip sync, generation time and credit cost','Actual output crop positioning and final edit pacing'],review_status=review.get('status','pending'))
    write('validation_report.json',validation)
    write('delivery_status.json',dict(local_inputs_ready=ready,ready_for_flow_upload=ready and review.get('status')=='complete',review_status=review.get('status','pending'),flow_uploaded=False,flow_video_generated=False,video_rendered=False,audio_generated=False,counts=manifest['counts']))
    save('README.txt',readme(manifest))
    save('sources.txt',SOURCES)
    save('index.html',render(manifest))
    if args.strict:
        assert ready,missing
        assert review.get('status')=='complete', 'Three-person cross-review is incomplete'
        assert len(assets)==35, len(assets)
    if args.zip:
        assert ready
        archive=ROOT/'AI_대회_Flow_업로드직전_패키지.zip'
        include=['upload_frames','references','prompts','post','index.html','README.txt','sources.txt','handoff_manifest.json','edit_crops.json','asset_checksums.json','image_generation_records.json','upload_order.tsv','edit_timeline.tsv','dialogue.tsv','captions.tsv','generation_log_template.tsv','validation_report.json','delivery_status.json','review_summary.json','review_plan.json']
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=4) as z:
            for name in include:
                p=ROOT/name
                files=p.rglob('*') if p.is_dir() else [p]
                for f in files:
                    if f.is_file():z.write(f,Path('Flow_handoff')/f.relative_to(ROOT))
        print('ZIP',archive.stat().st_size)
    print(json.dumps(dict(counts=manifest['counts'],missing=missing,validation=validation['status']),ensure_ascii=False))

SOURCES='''Official Google sources checked 2026-10-15 (public documentation only; user account not inspected).
https://support.google.com/flow/answer/16353334?hl=en — Frames start/end vs Ingredients reference inputs; complementary prompts.
https://support.google.com/flow/answer/16352836?hl=en — Model feature table; Veo 3.1 Fast/Lite Frames 4/6/8 seconds.
https://support.google.com/flow/answer/16353544?hl=en — Supported countries/languages and recommendation for English prompts.
https://support.google.com/flow/answer/16526234?hl=en — Plan-dependent upscaling and credits. Some Quality/Extend rows differ from the feature table; this package avoids those dependencies.
https://blog.google/innovation-and-ai/products/veo-updates-flow/ — Veo native audio.
https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/ — Resolution/upscale distinction.

Local creative source: storyboards/2026-10-15_absurd-v2/storyboards.json and selected scene_manifest.json, all five concepts reviewed previously.
Current handoff makes only production blocking changes documented in review_summary.json. It does not establish any unconfirmed event date, venue, attendance URL, award or numerical outcome.
Image mode: built-in image_gen; new start variants generated from the selected V2 representative images. Original images preserved.
'''

def readme(m):
    n=m['counts']
    return f'''AI 실행 결과 발표 대회 · Flow 업로드 직전 패키지
2026-10-15 / 5안 전체 / 로컬 준비

index.html을 브라우저로 여세요. 컷별 시작 이미지·프롬프트·대사·편집 구간을 한곳에서 확인할 수 있습니다.
새 시작 이미지 {n['new_start_assets']}장 + 재사용 시작 이미지 {n['unique_upload_images']-n['new_start_assets']}장 = 입력 PNG {n['unique_upload_images']}장.
이 입력들을 공유하여 총 {n['clips']}개 클립을 생성할 계획입니다. 대표 참고 이미지 21장은 references에 별도 보관했습니다.
전체 길이: C01 52초 / C02 54초 / C03·C04·C05 각 55초. 모두 마지막 행사명 6초 포함.

다음 실제 작업
1. upload_order.tsv에서 안과 컷을 선택합니다. 순서대로 만들되 모든 컷의 시작 이미지는 이미 로컬에 준비됩니다.
2. Flow에서 Video > Frames를 선택하고, 해당 first_frame PNG 한 장만 시작 프레임에 넣습니다.
3. 제안 설정: Veo 3.1 Fast / 가로 16:9 / 8초 / 결과 1개. 계정에서 Fast가 없으면 지원되는 Lite를 검토합니다. 계정 옵션·해상도·크레딧은 실제 UI에서 확인합니다.
4. 해당 *_korean_dialogue.txt 전체를 붙여넣습니다. 후시 더빙 중심이면 *_motion_only.txt를 대신 사용합니다. 두 프롬프트를 동시에 붙이지 않습니다.
5. 생성 결과에서 첫 상태·인물·소품·개그의 완료 시점을 확인합니다. generation_log_template.tsv에 실제 파일·트림·채택 여부를 기록합니다.
6. edit_timeline.tsv 길이로 편집합니다. 8초 생성은 원본 길이이고 최종 사용 길이는 3~8초로 다릅니다. 0초부터의 트림은 계획값이며 실제 동작을 보고 조정합니다. 핵심 행동이 안 나왔으면 단순 배속으로 해결하지 않습니다.
7. 후편집 엔딩은 post/<안>/title_overlay.svg를 마지막 검수 프레임에 합성해 6초 유지합니다. 독립 endcard.svg도 있어 배경 프레임 없이 사용할 수 있습니다. SVG 한글은 Noto Sans CJK KR/Noto Sans KR 계열 폰트가 필요합니다.

입력 구분
upload_frames: 실제 업로드할 시작 PNG. 클립 여러 개가 같은 이미지를 공유할 수 있습니다.
references: 연출·의상·목표 상태를 볼 참고 PNG. 이 기본 작업에서 Ingredients나 끝 프레임으로 일괄 업로드하지 않습니다.
post: 후편집 자막 SRT, 선택적 대사 자막 SRT, 음향·전환 표, 엔딩 SVG. Flow 이미지 입력이 아닙니다.
prompts: 영어 행동 지시 + 정확한 한국어 대사 버전, 동작만 버전. 실제 음원 파일은 만들지 않았습니다.

개그를 지키는 편집
C01: 손수건 H1은 A→C, H2는 B 소유. 마지막 A는 양동이를 들고 B가 자기 손수건을 접습니다.
C02: 세 켤레의 포획 성공을 먼저 보여준 뒤 자루가 달아납니다. 끝에서는 주인 둘이 실제로 빈 좌석에 앉아야 합니다.
C03: 짬뽕은 인간 스캔, 탕수육은 지휘관 스캔. K07은 높은 위치의 손목 붙잡기에서 끝나 K08로 이어집니다.
C04: 첫 출력물이 움직여야 증식의 원인이 보입니다. 실제 넘어짐→기상→추종을 유지하고 A의 짧은 집게팔을 늘리지 않습니다.
C05: F01 A만, F02 B/C 순서로 크롭 공개. F03에서 천을 먼저 날리지 않습니다. 35~37초 빈 벽은 완전 정적으로 2초 유지합니다. F09는 C 얼굴→A 얼굴→‘내 생각!’에서 가슴 지목 공개입니다. edit_crops.json의 좌표는 정지 이미지 기준이며 영상에서 재확인합니다.

오디오·자막
대사의 화자와 구간은 dialogue.tsv가 기준입니다. 한국어 발음·정확한 문장·목소리 일관성·무음 출력은 생성 결과를 확인해야 합니다. 부정확하면 해당 음성을 버리고 동일 대본을 더빙합니다. 복잡한 음악·효과음은 sound_and_transitions.tsv대로 후편집합니다.
행사명·‘실행 사례’ 등 정확한 글자는 생성 화면에 맡기지 않고 별도 자막을 사용합니다. planned_captions.srt와 SVG 엔딩을 같은 구간에 중복 노출하지 마세요. 대사 자막 SRT는 선택 사항입니다.

준비 완료 범위
이미지·프롬프트·대본·편집 설계·로컬 검수까지. Flow 업로드, Flow 프로젝트 생성, 영상·음원 생성, 최종 영상 렌더링은 실행하지 않았습니다.
일시·장소·신청 URL은 미확정이라 넣지 않았습니다. 행사명에는 (안)을 붙이지 않습니다.
문서 검증 결과: validation_report.json / 3명 독립·교차검수 기록: review_summary.json.
Google 공식 근거와 확인일: sources.txt.
'''

def render(m):
    esc=html.escape
    status='로컬 입력 준비 완료' if not m['missing'] else '시작 이미지 제작 중'
    review=m['review'].get('status','pending')
    out=['''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 실행 결과 발표 대회 · Flow 준비</title><style>
*{box-sizing:border-box}body{margin:0;background:#0b1017;color:#eaf0f7;font:15px/1.7 "Noto Sans CJK KR","Noto Sans KR",sans-serif}main{max-width:1320px;margin:auto;padding:42px 32px}a{color:#a8d8fa}h1{font-size:35px;line-height:1.35;margin:10px 0}h2{font-size:28px;margin:50px 0 10px}h3{font-size:20px;margin:0}p{margin:9px 0}nav{position:sticky;top:0;background:#111b28ef;padding:14px 32px;z-index:2;display:flex;gap:26px;flex-wrap:wrap;border-bottom:1px solid #354052}.badge{font-size:12px;color:#88e6c0;text-transform:uppercase;letter-spacing:.1em}.stats{display:flex;gap:12px;flex-wrap:wrap;margin:25px 0}.stats span,.box{background:#17212d;padding:14px 20px;border:1px solid #2c3c50;border-radius:10px}.stats b{font-size:24px;display:block}article{border:1px solid #324156;border-radius:14px;margin:24px 0;background:#111a25;overflow:hidden}.head{display:flex;justify-content:space-between;padding:18px 22px;background:#182435}.grid{display:grid;grid-template-columns:50% 50%}.frame img{display:block;width:100%;aspect-ratio:16/9;object-fit:contain;background:#000}.frame p{padding:0 18px 10px;font-size:12px;color:#9baec2}.details{padding:18px 22px}.muted{color:#a4b4c6}.key{font-size:12px;color:#83b8df;display:block;margin-top:12px}.links{display:flex;gap:14px;flex-wrap:wrap}.prompt{padding:0 22px 18px}details{margin-top:12px}summary{cursor:pointer;color:#b9dcfc}textarea{width:100%;height:240px;background:#0b111a;color:#dce7f5;border:1px solid #39516b;padding:14px;border-radius:7px;font:13px/1.5 monospace}button{background:#bceacf;color:#102d21;border:0;padding:9px 15px;border-radius:6px;cursor:pointer;font-weight:bold;margin:10px 8px 0 0}.end{display:grid;grid-template-columns:45% 55%;gap:22px;align-items:center;margin:22px 0}.end img{width:100%}.refs{display:flex;gap:10px}.refs img{width:140px;aspect-ratio:16/9;object-fit:cover}table{border-collapse:collapse;width:100%}td,th{padding:8px;text-align:left;border-bottom:1px solid #2c3c50}li{margin:7px 0}@media(max-width:800px){main{padding:20px}.grid,.end{grid-template-columns:1fr}h1{font-size:28px}nav{gap:16px;padding:10px}.head{display:block}}@media print{nav,button,textarea{display:none}body{background:white;color:black}article{break-inside:avoid}.grid{grid-template-columns:45% 55%}main{padding:0}.prompt{display:none}}</style><nav>''']
    out+=['<a href="#'+c['id']+'">'+c['id']+' '+esc(c['title'])+'</a>' for c in m['concepts']]
    out.append('</nav><main><div class="badge">PRE-UPLOAD PACKAGE · 2026.10.15</div><h1>AI 실행 결과 발표 대회<br>Flow에 넘기기 직전까지</h1>')
    n=m['counts']
    out.append(f'<p class="muted">{status} · 교차검수 {esc(review)} · Flow 업로드·영상 생성 전</p><div class="stats"><span><b>5안</b>각 52~55초</span><span><b>{n["clips"]}개</b>8초 생성 클립 계획</span><span><b>{n["unique_upload_images"]}장</b>업로드용 시작 PNG</span><span><b>{n["new_start_assets"]}장</b>새로 만든 시작 상태</span></div>')
    out.append('<div class="box"><b>다음 작업은 각 컷의 시작 PNG 한 장 + 프롬프트를 Flow에 넣는 것입니다.</b><p>제안 설정: Frames · 시작만 · Veo 3.1 Fast · 가로 16:9 · 8초 · 결과 1개. 계정의 실제 옵션은 미확인입니다. 생성 8초와 편집 사용 길이를 구분하세요.</p><p>참고 이미지는 연출 확인용입니다. 기본 입력에 Ingredients나 끝 프레임을 더하지 않습니다. 한글 행사명·정확한 자막은 후편집합니다.</p></div>')
    out.append('<p class="links"><a href="README.txt">작업 안내</a><a href="upload_order.tsv">업로드 순서</a><a href="edit_timeline.tsv">편집 타임라인</a><a href="dialogue.tsv">대사 큐</a><a href="handoff_manifest.json">전체 명세</a><a href="validation_report.json">파일 검증</a><a href="review_summary.json">3명 교차검수</a><a href="sources.txt">공식 근거</a></p>')
    out.append('<p class="muted">프롬프트의 한국어 대사는 생성 결과에서 정확성을 확인하고, 필요하면 동작 전용 버전 + 별도 더빙을 사용합니다. 미확정 일시·장소·신청 링크는 넣지 않았습니다.</p>')
    for concept in m['concepts']:
        cid=concept['id']
        out.append(f'<section id="{cid}"><div class="badge">{cid} · {concept["duration_seconds"]} seconds</div><h2>{esc(concept["title"])}</h2><p class="muted">{esc(concept["style"])} · 본편 {concept["duration_seconds"]-6}초 + 엔딩 6초</p>')
        for c in concept['clips']:
            out.append(f'<article id="{c["id"]}"><div class="head"><h3>{c["id"]}</h3><span>{short(c["edit_start"])}–{short(c["edit_end"])} · 편집 {c["edit_seconds"]}초 / 생성 8초</span></div><div class="grid"><div class="frame"><a href="{c["first_frame"]}"><img loading="lazy" src="{c["first_frame"]}" alt="{c["id"]} 시작 이미지"></a><p>실제 업로드 파일: {c["first_frame"]}</p></div><div class="details">')
            out.append('<span class="key">시작 → 끝</span><p>'+esc(c['start_state'])+'</p><p>→ '+esc(c['end_state'])+'</p><span class="key">핵심 행동</span><p>'+esc(c['action'])+'</p><span class="key">카메라</span><p>'+esc(c['camera'])+'</p>')
            if c['dialogue']:
                out.append('<span class="key">대사 · 완성본 기준</span>')
                for q in c['dialogue']:out.append(f'<p>{q["start"]:g}–{q["end"]:g}s · {esc(q["speaker"])}: {esc(q["text"])}</p>')
            out.append('</div></div><div class="prompt">')
            for key,label in [('prompt_native','한국어 대사 포함 프롬프트'),('prompt_motion_only','동작 전용 · 후시 더빙용')]:
                tid=c['id']+'_'+key
                out.append(f'<details><summary>{label}</summary><textarea id="{tid}" readonly>{esc((ROOT/c[key]).read_text())}</textarea><button onclick="copyText(\'{tid}\',this)">복사</button><a href="{c[key]}">TXT 열기</a></details>')
            out.append('<details><summary>편집·검수 메모 / 참고 이미지</summary><p>'+esc(c['edit_notes'])+'</p>')
            if c['edit_crops']:
                out.append('<p><b>공개 순서를 지키는 후편집 크롭</b></p>')
                for cr in c['edit_crops']:out.append(f'<p>{cr["start"]}–{cr["end"]}s: {esc(cr["purpose"])} · x{cr["x"]}, y{cr["y"]}, {cr["w"]}×{cr["h"]}</p>')
                out.append('<p class="muted">1672×941 정지 이미지 기준 가안. 생성 영상의 얼굴·손 위치에 맞춰 재확인합니다.</p>')
            out.append('<ul>'+''.join('<li>'+esc(q)+'</li>' for q in c['qa'])+'</ul><div class="refs">'+''.join(f'<a href="{r}"><img loading="lazy" src="{r}" alt="연출 참고"></a>' for r in c['reference_only'])+'</div></details></div></article>')
        for p in concept['post_edit']:
            if p['kind']=='endcard':out.append(f'<div class="end"><img src="{p["standalone"]}" alt="엔딩 타이틀"><div><b>{short(p["start"])}–{short(p["end"])} · 후편집 엔딩 6초</b><p>{esc(p["notes"])}</p><p><a href="{p["overlay"]}">합성용 타이틀 SVG</a> · <a href="{p["standalone"]}">독립 엔딩 SVG</a></p><p><a href="post/{cid}/planned_captions.srt">자막 SRT</a> · <a href="post/{cid}/dialogue_optional_subtitles.srt">대사 SRT</a> · <a href="post/{cid}/sound_and_transitions.tsv">음향·전환</a></p></div></div>')
            else:out.append('<div class="box"><b>35–37초 · 빈 벽만 2초</b><p>'+esc(p['notes'])+'</p><p>references/C05/S03.png에서 x1460, y420, 210×118. 말·음악·효과음 모두 중지.</p></div>')
        out.append('</section>')
    out.append('''<p class="muted">실제 영상의 재미·대사·움직임은 Flow 생성 후 확인할 항목입니다. 이 패키지는 입력 파일과 편집 설계의 준비 결과입니다.</p></main><script>async function copyText(id,b){const t=document.getElementById(id);let ok=false;try{await navigator.clipboard.writeText(t.value);ok=true}catch(e){t.focus();t.select();ok=document.execCommand('copy')}b.textContent=ok?'복사됨':'선택됨 · Ctrl+C';if(ok)setTimeout(()=>b.textContent='복사',1400)}</script></html>''')
    return ''.join(out)

if __name__=='__main__':main()
