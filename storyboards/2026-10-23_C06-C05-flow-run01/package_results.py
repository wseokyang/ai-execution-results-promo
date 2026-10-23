"""Package preserved Flow originals and explicit editorial review decisions."""
import hashlib, html, json, pathlib, shutil

run = pathlib.Path(__file__).resolve().parent
repo = run.parent.parent
cache = pathlib.Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v11-C06-C05-2026-10-23')
log = json.loads((run/'generation_log.json').read_text(encoding='utf-8'))
review = json.loads((run/'review_summary.json').read_text(encoding='utf-8'))
decisions = {x['unit_id']: x for x in review['decisions']}
accounts = {}
for r in log['requests']:
    p = run/r['original_file']
    source = pathlib.Path(r['download_source_path'])
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    assert source.exists() and hashlib.sha256(source.read_bytes()).hexdigest() == digest
    r.setdefault('original_sha256', digest)
    r.setdefault('original_bytes', p.stat().st_size)
    assert hashlib.sha256(p.read_bytes()).hexdigest() == r['original_sha256']
    inspection = json.loads((run/(p.stem+'_inspection.json')).read_text(encoding='utf-8'))
    assert inspection['full_video_decode_pass']
    r['technical_inspection'] = inspection
    r['generation_id'] = r['asset_id']
    r['generation_id_basis'] = 'Flow visible asset edit URL; no separate backend job ID inspected'
    d = decisions[r['unit_id']]
    selected = d['selected_take'] == r['take']
    r['review_status'] = d['status'] if selected else 'SUPERSEDED_OR_PARTIAL_ALTERNATE'
    r['review_note'] = d['note'] if selected else '보완 후보와 비교할 이전 원본. 단독 전체 채택 아님. review_notes.md 참조.'
    accounts[r['account_alias']] = r['after_submission_balance']
    shutil.copyfile(p, cache/p.name)
log.update(status='SOURCE_GENERATION_COMPLETE_WITH_EDITORIAL_CONDITIONS',
           source_units=len(decisions), basic_requests=18, corrective_requests=5,
           observed_total_debit=sum(r['observed_debit'] for r in log['requests']),
           observed_total_refund=sum(r['refund'] for r in log['requests']),
           ending_balances=accounts, remaining_credits=sum(accounts.values()),
           pending_requests=0, final_edited_films=0,
           renewal_note='Account-specific UI notices differed. Do not assume midnight reset.',
           remaining_credits_reason='All units have source candidates. Repeated defects are not retried again today; remaining continuity and timing require an actual edit, not speculative generations.',
           automation_status='PAUSED_UNCHANGED')
(run/'generation_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header = '# 6번·5번 Flow 원본 · V11\n\n**기본 18컷 + 보완 5테이크 = 원본 23개.** 6번 10개, 5번 13개를 보존했습니다. 모두 8초·1280×720·24fps·Veo 3.1 Lite입니다. 230크레딧 사용, 마지막 계정 20크레딧 잔여, 나머지 네 계정 0. 진행 중 요청은 없습니다.\n\n자막·Q-AI Fair 행사명·화면 문서·BGM을 넣기 전 **동작 원본**입니다. 원본의 생성 오디오도 그대로 보존했으며 실제 청취 검증은 하지 않았습니다. 최종 사용 음향은 편집 단계에서 결정합니다.\n\n**주의:** 5번 K02B의 완전한 처마 아래 진입, 6번 K05의 왼쪽 문 통과는 지시대로 확보되지 않았습니다. 몸 접고 접근→다음 컷, 오른쪽 화면 밖 이동→유령 혼자 남음으로 시간·공간을 생략하는 편집 후보입니다. 전체 영상이 무결하게 완성됐다는 뜻은 아닙니다.\n\n[검수·편집 조건](review_notes.md) · [구조화 검수](review_summary.json) · [요청·비용·원본 해시 기록](generation_log.json) · [로컬에서 여는 원본 재생 페이지](originals.html)\n\n'
md = [header, '| 컷 | 채택 후보 원본 | 사용 구간 후보(원본 초) | 검수·남은 편집 |\n|---|---|---|---|\n']
cards=[]
for concept,title in [('C06','06 · 퇴근 좀 해주세요'),('C05','05 · 괴수는 퇴근할 수 없다')]:
    cards.append(f'<h2 id="{concept}">{title}</h2>')
    for d in sorted([x for x in review['decisions'] if x['unit_id'].startswith(concept)],key=lambda x:x['unit_id']):
        name=f"{d['unit_id']}_take{d['selected_take']:02}.mp4"
        md.append(f"| {d['unit_id']} | [take{d['selected_take']:02}]({name}) | {d['range_candidate']} | {d['note']} |\n")
        cards.append(f'<article><h3>{d["unit_id"]} · take{d["selected_take"]:02}</h3><video controls muted preload="metadata" src="{name}"></video><p>{html.escape(d["note"])}</p><p class="range">편집 구간 후보: {html.escape(d["range_candidate"])}</p><a href="{name}" download>원본 다운로드</a></article>')
md.append('\n## 모든 테이크 원본\n\n')
cards.append('<h2>이전 테이크도 모두 보존</h2><ul>')
for r in sorted(log['requests'],key=lambda r:(r['unit_id'],r['take'])):
    f=r['original_file']
    md.append(f'- [{f}]({f}) · [32표본 연락판]({pathlib.Path(f).stem}_contact.jpg)\n')
    cards.append(f'<li><a href="{f}">{f}</a></li>')
cards.append('</ul>')
md.append('\n원본은 재인코딩하지 않았고, 다운로드와 저장본 SHA-256을 대조했습니다. 23개 전편 영상 디코딩 성공. 검수는 세 명의 0.25초 간격 추출 프레임 독립·교차 검수이며 연속 재생·음향·최종 자막 가독성 검증과 구분합니다. 개별 PNG는 로컬 frames/에 보존하고 Git에는 연락판과 재생성 스크립트를 보관합니다.\n')
(run/'README.md').write_text(''.join(md),encoding='utf-8')
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair · 6번·5번 Flow 원본</title><style>body{margin:0;background:#101419;color:#f3f5f7;font:17px/1.6 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:32px}h1{font-size:34px}h2{margin-top:64px;border-top:1px solid #495360;padding-top:24px}a{color:#9ad9ff}article{padding:24px;margin:22px 0;background:#1d2631;border-radius:16px}video{width:100%;max-height:580px;background:#000}.range{color:#b2c4d5}.note{padding:20px;background:#352e1b;border-left:4px solid #e9c369}nav{display:flex;gap:22px}</style><main><h1>6번 → 5번 · Flow 원본</h1><p>23개 원본 · 기본 18컷 + 보완 5테이크 · 230크레딧 사용 / 20 잔여</p><nav><a href="#C06">6번</a><a href="#C05">5번</a><a href="https://github.com/wseokyang/ai-execution-results-promo">GitHub</a></nav><p class="note">자막·BGM·화면 합성 전의 원본입니다. 플레이어는 무음으로 시작합니다. 5번 K02B의 완전 진입과 6번 K05의 문 통과는 아직 지시대로 구현되지 않아 짧은 부분 사용과 장면 생략이 필요합니다. 아래 사용 구간은 편집 후보이며 완성 편집본이 아닙니다.</p>'''+''.join(cards)+'</main></html>'
(run/'originals.html').write_text(page,encoding='utf-8')
(cache/'originals.html').write_text(page,encoding='utf-8')
shutil.copyfile(cache/'flow_completed.jpg',run/'evidence/flow_completed.jpg')
print(json.dumps({'originals':len(log['requests']),'credits_used':log['observed_total_debit'],'remaining':log['remaining_credits'],'mp4_bytes':sum(r['original_bytes'] for r in log['requests'])},ensure_ascii=False))
