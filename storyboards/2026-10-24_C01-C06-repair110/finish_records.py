from pathlib import Path
import json,hashlib,shutil,html,subprocess
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;SB=R.parent
CACHE=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-repair110-2026-10-24')
def dump(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def write(p,s):p.write_bytes((s.rstrip()+'\n').encode())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selected={
 'C01_K05':([2.5,7.25],'두 사람이 실제 왼쪽 문으로 퇴장. 다음 착석·낙하는 시간 생략.','edit_probes/C01_exit_to_fall.mp4'),
 'C04_K09':([.5,6],'장군이 숟가락 한 개를 꺼냄. 왼손이 같은 숟가락에 닿는 동작은 수용.','edit_probes/C04_windows_to_spoon.mp4'),
 'C05_K04_jack_detail':([1.5,3],'선명한 잭의 왼쪽 운반. 정지·상승·하중 이전은 아님.','../2026-10-25_C05-jack-edit-v06/C05_Q-AI_Fair_causal_edit_v06.mp4'),
 'C04_K08_three_visible':([2,3.5],'세 사람·그릇 세 개·숟가락 세 개 유지. 식사 유사 동작 제외. 창은 처음부터 열려 있음.','edit_probes/C04_windows_to_spoon.mp4'),
 'C06_K02_impact':([.75,2.25],'첫 책상 접촉만 사용, 두 번째 타격 제외. 진동·종이 튐 미확보.','../2026-10-25_C06-impact-edit-v06/C06_Q-AI_Fair_edit_v06.mp4')}
held={
 'C04_K08_detail':'중앙 창에 두 명, 총 네 인물과 그릇. 전체 공개 구간 미채택.',
 'C01_K07':'수강생이 무릎만 꿇고 눕지 않음. 코치 자세도 달라짐.',
 'C01_K06_pose':'누운 자세를 유지하지 않고 일어나 무릎 꿇음.',
 'C02_K05_release':'두 고리·손 놓기는 확보했으나 아래 고리가 렌즈 아래로 내려감. 기존 K06과 사슬 길이·고리 위치 불일치.',
 'C04_K01_insert':'자기 종이는 왼손에 남고, 빈 오른손이 봉투에서 다른 종이를 꺼냄. 투입 미확보.',
 'C01_K07_recline':'등을 내리지 않고 팔꿈치로 기대며 코치도 자세를 풂. 정확 모방 완성 미확보.'}
log=json.loads((R/'generation_log.json').read_text(encoding='utf-8'))
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
assert len(log['entries'])==11
for e in log['entries']:
    unit=e['unit_id'];p=R/e['original'];assert sha(p)==e['sha256']==e['download_sha256']
    dec=subprocess.run([str(FF),'-v','error','-i',str(p),'-f','null','-'],capture_output=True);assert dec.returncode==0,(unit,dec.stderr)
    e['decode']='PASS: complete video and audio decode; audio not listened'
    e['status']='ORIGINAL_PRESERVED_REVIEWED'
    e['review']='SELECTED_INTERVAL' if unit in selected else 'HOLD_NOT_SELECTED'
    e['review_reason']=selected[unit][1] if unit in selected else held[unit]
    e['selected_interval_seconds']=selected[unit][0] if unit in selected else None
    e['actual_listening_verified']=False
    e['original_reencoded']=False
log.update(successful_originals=11,selected_originals=5,held_originals=6,net_credits_used=110,scope='C01–C06 source and existing edit review; C01/C02/C04 did not have complete caption/composite edits',audio_note='Original audio is preserved but not required for meaning and is muted in derived edits/probes')
dump(R/'generation_log.json',log)
queue=json.loads((R/'queue.json').read_text(encoding='utf-8'))
for q in queue:q['status']='ORIGINAL_PRESERVED_REVIEWED';q['asset_id']=next(e['asset_id'] for e in log['entries'] if e['unit_id']==q['unit'])
dump(R/'queue.json',queue)
order=['C04_K08_detail','C01_K07','C04_K09','C01_K05','C01_K06_pose','C04_K01_insert','C02_K05_release','C05_K04_jack_detail','C04_K08_three_visible','C01_K07_recline','C06_K02_impact']
requests=[]
for unit in order:
    e=next(x for x in log['entries'] if x['unit_id']==unit)
    if unit in ['C04_K08_detail','C05_K04_jack_detail']:
        requests.append(dict(unit=unit,status='FAILED_ABNORMAL_ACTIVITY_RECAPTCHA',account=e['account_alias'],before=e['balance_before'],after=e['balance_before'],net_spend=0,refund_observed=0,recovery='User explicitly refreshed; one normal subsequent request accepted. No bypass.'))
    requests.append(dict(unit=unit,take=e['take'],asset_id=e['asset_id'],account=e['account_alias'],before=e['balance_before'],after=e['balance_after'],net_spend=10,cost_displayed=10,refund_observed=0,status='ORIGINAL_SAVED'))
dump(R/'budget_ledger.json',dict(authorized_total=110,require_all_spent=True,started_local='2026-10-24T23:57:00+09:00',start_observed={'current_u2':10,'current_u3':50,'current_u4':50},requests=requests,confirmed_net_spend=110,security_failures_without_charge=2,final_balance_observed={f'current_u{i}':0 for i in range(5)},final_balance_observation_local='2026-10-25 00:27–00:30 Asia/Seoul',final_verification='Actual account panels, not historical balance inference',renewal_notes='u4 daily 10:01 observed. Do not assume midnight reset or that spending all is a reset condition.',purchases=0,subscription_changes=0,paid_upscales=0,external_paid_apis=0,automation='PAUSED unchanged'))
review=dict(scope='Three distinct reviewers independently inspected actual contacts and selected PNGs, then exchanged findings and rechecked join probes; continuous viewing, audio listening and venue testing not verified.',reviewers=['/root/causal_review_a','/root/causal_review_b','/root/causal_review_c'],all_six_review={'C01':'Actual exit and pose matching reviewed; select exit, retain accepted existing pose ellipsis. Monitor/portrait composites and final caption edit remain.','C02':'Cuff release candidate does not improve current join; retain previous source intervals. Exact monitor/sample/photo composites and final captions remain.','C03':'Current caption-v04 retained; no high-value generation repair identified.','C04':'Replace cropped three-person view and spoon extraction; retain old paper/first-opening intervals. Document/tablet and final captions remain.','C05':'Replace 384x216 enlarged crop with sharp original jack movement in full v06 edit.','C06':'Replace weak threat with first actual palm contact in full v06; retime existing desk effect to 6.125s.'},selected={k:dict(interval=v[0],reason=v[1],artifact=v[2]) for k,v in selected.items()},held=held,cross=[dict(issue='C06 second hit',A_initial='0.75–3.5 candidate',B_and_C='Hands rise again at2.5 and contact at3; exclude',PD='0.75–2.25 only; A rechecked and accepted first-hit-only probe'),dict(issue='C01 recline',A='1.5–2.5 partial-gesture insertion may be tried',B_and_C='No benefit over existing K07→K08',PD='Do not add; exact matching pose not achieved'),dict(issue='C04 three visible',A_and_C='2–4',B='2–3.5',PD='Use common safe 2–3.5, exclude eating/retraction'),dict(issue='C02 release',all='Two rings and release exist, but optical obstruction and chain continuity fail',PD='Keep previous selected source; new raw retained HOLD')],final_probe_recheck={r:'C01 exit→fall, C04 bowls→spoon, C06 first contact→sorting and C05v06 jack joins visually accepted with time ellipses; no newly identified mandatory visual defect.' for r in ['A','B','C']},C06_final_render_recheck='pending last three responses',actual_audio_listening=False,measured_audience_response=False,remaining=['C01/C02/C04 final exact composites, captions and edit','Original audio not used for meaning','Full realtime playback, listening and venue readability test','C01 matching-action, C02 cuff exact continuity and C04 paper insertion not solved by new takes; accepted earlier interval/ellipsis retained'])
dump(R/'review_summary.json',review)
generated={
 'C04_K08_detail.png':('exec-81cd912f-d140-4eec-9cd4-d2b8544527ce.png','Existing C04_K08.png','Close view of three closed side-hinged shutters. One left vertical hinge per shutter, no people visible; retain horse wood and purple crescent.'),
 'C02_K05_release.png':('exec-565655f3-3513-403c-aead-ceff1b9fdde0.png','Existing C02_K06.png','Upper cuff fixed to black handle; detective supports lower ring beside orange window. Exactly two rings and one chain; preserve cast/workbench.'),
 'C05_K04_jack_detail.png':('exec-a9e495a1-410a-469f-9a8e-9c44541b3540.png','C05_K04_take02 frame0','Sharp close view of older worker holding low red wheeled jack with both gloved hands. Space to move left, wet pavement and building unchanged.'),
 'C04_K08_three_visible.png':('exec-0cc6ca50-eab3-4d9c-b11c-9c6581a17408.png','New C04_K08_detail + existing C04_K09','Three opened windows, exactly one older gray-haired woman left, slim young man center, curly stocky man right. One bowl and spoon each. Ready to lean forward.'),
 'C01_K07_recline.png':('exec-b74bb30a-d410-4026-9d26-aeda4ce0fcee.png','Rejected preparation exec-0005da74-b694-476b-a4ef-66a9aca270ad.png, prior C01 setup','Teal trainee half reclining on elbows behind motionless coach, separate parallel bodies head right feet left; room to lower shoulders. Photographer stays crouched.'),
 'C06_K02_impact.png':('exec-5dda4d86-c8cd-4529-bc07-a4ef5cbcdd70.png','C06_K02_take01 frame0','Angry ghost both hands raised before one desk strike, seated employee indifferent. Keep empty impact area, desk and papers; no added writing.')}
image_entries=[]
for q in queue:
    p=R/q['input'];g=generated.get(p.name)
    image_entries.append(dict(unit=q['unit'],file=q['input'],sha256=sha(p),source='builtin image_gen' if g else 'existing input/frame reused',generated_file=g[0] if g else None,reference=g[1] if g else 'See preparation scripts',generation_spec=g[2] if g else None,prompt_record_note='Image requirements reconstructed from production notes; exact original image tool payload not retained. Exact submitted motion prompt is saved separately.',motion_prompt=f'submitted_prompts/{q["unit"]}_take{q["take"]:02d}.txt',input_review='A/B/C actual image samples accepted before use; this is not motion success'))
dump(R/'scene_manifest.json',dict(entries=image_entries,rejected_preparation_variant='exec-0005da74-b694-476b-a4ef-66a9aca270ad.png: insufficient lie-down space; not uploaded',image_count_generated_and_used=6,all_existing_inputs_preserved=True))
rows=[]
for e in log['entries']:
    sel=selected.get(e['unit_id']);st='채택 '+str(sel[0])+'초' if sel else '보류'
    rows.append(f'| {e["unit_id"]} take{e["take"]:02d} | [MP4 원본]({e["original"]}) · [프레임]({Path(e["original"]).stem}_contact.jpg) | {st} | {e["review_reason"]} |')
write(R/'README.md',f'''# 1~6번 동작 보완 · 110크레딧

2026-10-24 시작, 10-25 저장·검수. **110 전부 사용, 로그인 5계정 모두 실제 잔액 0 확인.** Lite10 × 성공11개. 보안 실패2회는 차감0이며 사용자 새로고침 뒤 한 번씩 정상 요청했다. 11개 원본 중 **5개는 선택 구간 채택, 6개는 보류**다.

원본은 모두 8초·1280×720·24fps이며 재인코딩하지 않았다. 다운로드/보관 SHA 일치, 전체 영상·오디오 디코딩 통과. 원본 음성은 필수 전달에 쓰지 않으며 실제 청취 검증은 하지 않았다.

- [5번 v06 전체 편집본](../2026-10-25_C05-jack-edit-v06/C05_Q-AI_Fair_causal_edit_v06.mp4): 51.25초, 흐릿한 확대 컷을 선명한 실제 잭 운반으로 교체.
- [6번 v06 전체 편집본](../2026-10-25_C06-impact-edit-v06/C06_Q-AI_Fair_edit_v06.mp4): 48.75초, 첫 타격만 반영하고 기존 효과음을 실제 손 접촉 6.125초에 이동.
- [1번 퇴장→낙하 연결 검토](edit_probes/C01_exit_to_fall.mp4) · [4번 세 인물→숟가락 연결 검토](edit_probes/C04_windows_to_spoon.mp4)

1·2·4번의 정확한 화면 합성·자막을 포함한 최종 편집은 남아 있다. 3번은 기존 caption-v04를 유지했다. 여섯 편 모두 완성본이라는 뜻은 아니다.

| 컷 | 원본과 검토 프레임 | 판정 | 이유 |
|---|---|---|---|
{chr(10).join(rows)}

[전체 원본 재생 목록](originals.html) · [생성 로그](generation_log.json) · [잔액 장부](budget_ledger.json) · [검수·교차 처리](review_summary.json) · [입력 이미지 대응](scene_manifest.json)

기존 자세/수갑/봉투의 미해결 동작은 새 원본을 억지로 채택하지 않고 종전의 수용 구간과 시간 생략을 유지한다. 창 공개의 열림 자체, 잭의 상승·하중 이전, 괴수 완전 회전, 책상 진동·종이 튐을 추가 확보했다고 주장하지 않는다. 세 검수자의 실제 표본과 연결 검토 및 기술 검증이며, 전체 실시간 재생·실청취·현장 소음 테스트·관객 반응 검증은 아니다.
''')
cards=''.join(f'<article><h2>{html.escape(e["unit_id"])} take{e["take"]:02d}</h2><p>{html.escape(e["review"]+": "+e["review_reason"])}</p><video controls preload="metadata" src="{e["original"]}" poster="{Path(e["original"]).stem}_contact.jpg"></video><p><a href="{e["original"]}" download>원본 MP4</a></p></article>' for e in log['entries'])
write(R/'originals.html','<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>1~6편 보완 원본11</title><style>body{background:#111c23;color:#eef6ff;font-family:system-ui;margin:3vw}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:24px}article{background:#21333f;padding:18px;border-radius:12px}video{width:100%}a{color:#8ee0dd}p{line-height:1.7}</style><h1>1~6편 보완 원본 11개</h1><p>110크레딧 사용 · 5계정 잔액0 · 채택5/보류6. 아래는 편집 전 생성 원본입니다.</p><main>'+cards+'</main></html>')
# Preserve generated originals in a Windows path for local playback; no encoding.
for e in log['entries']:
    for name in [e['original'],Path(e['original']).stem+'_contact.jpg']:shutil.copyfile(R/name,CACHE/name)
shutil.copyfile(R/'originals.html',CACHE/'originals.html')
for source in [SB/'2026-10-25_C05-jack-edit-v06/C05_Q-AI_Fair_causal_edit_v06.mp4',SB/'2026-10-25_C06-impact-edit-v06/C06_Q-AI_Fair_edit_v06.mp4']:shutil.copyfile(source,CACHE/source.name)
print('Records written; final C06 review responses still to record')
