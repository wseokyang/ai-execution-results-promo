"""Verify saved originals and build the review handoff. Never transcode originals."""
from pathlib import Path
import hashlib
import html
import json
import shutil

run = Path(__file__).resolve().parent
repo = run.parents[1]
cache = Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v11-C06-C05-2026-10-23')

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

log = read(run / 'generation_log.json')
reviews = read(run / 'review_summary.json')
assert reviews['three_reviewer_cross_review_complete']
by_file = {r['file']: r for r in reviews['clips']}
observed_titles = {
    'C06_K02': 'Ghost jolts desk of employee',
    'C06_K09_reaction': 'Ghost reaction in office',
    'C06_K04_check': 'Employee checking paper with pen',
}
preview = cache / 'run03'
preview.mkdir(parents=True, exist_ok=True)
for r in log['requests']:
    assert (run / r['prompt_file']).read_text(encoding='utf-8-sig').strip() == r['prompt'].strip()
    assert digest(repo / r['input_image']) == r['input_sha256']
    if not r['original_file']:
        assert r['status'] == 'FAILED_AUDIO_REFUNDED' and r['refund'] == 10
        continue
    src = run / r['original_file']
    check = read(run / (src.stem + '_inspection.json'))
    assert digest(src) == r['original_sha256'] == check['sha256']
    assert digest(src) == digest(Path(r['download_source_path']))
    shutil.copyfile(src, preview / src.name)
    assert digest(src) == digest(preview / src.name)
    r['technical_inspection'] = check
    r['status'] = 'COMPLETED_ORIGINAL_PRESERVED'
    r['review_status'] = by_file[src.name]['status']
    r['review_record'] = 'review_summary.json'
    r['asset_url'] = r['project_url'] + '/edit/' + r['asset_id']
    r['asset_id_basis'] = 'Observed Flow editor URL /edit/<asset_id>'
    r['generation_id_note'] = 'Internal job ID not exposed; observed asset ID and editor URL recorded.'
    r['original_preservation'] = 'Downloads, repository and preview copy SHA-256 identical. No re-encoding.'
    if r['unit_id'] in observed_titles:
        r['ui_title'] = observed_titles[r['unit_id']]
    if r['unit_id'] == 'C06_K04_check' and r['take'] == 2:
        r['silent_return_during_request'] = True
        r['recovery_prompt_diff'] = 'Same motion instructions; take number changed from 01 to 02. Silent-return setting enabled after verified audio failure/refund.'
    shutil.copyfile(run / (src.stem + '_contact.jpg'), preview / (src.stem + '_contact.jpg'))
for q in log['queue']:
    q['status'] = 'COMPLETED_ORIGINAL_PRESERVED'
    q['successful_take'] = next(r['take'] for r in log['requests'] if r['unit_id'] == q['unit_id'] and r['original_file'])
log.update({
    'status': 'COMPLETED_EIGHT_ORIGINALS_ALL_AVAILABLE_CREDITS_USED',
    'flow_requests': 9, 'successful_outputs': 8, 'downloaded_originals': 8,
    'failed_refunded_requests': 1, 'pending_requests': 0,
    'gross_observed_debit': 90, 'refunds_observed': 10, 'net_observed_cost': 80,
    'ending_balance_snapshot': {f'current_u{i}': 0 for i in range(5)},
    'ending_balance_observed_total': 0,
    'balance_observations_by_account': {
        'current_u2': [50, 40, 30, 20, 10, 0],
        'current_u3': [30, 20, 10, 0, 10, 0],
    },
    'reset_note': 'Account-specific renewal notices differ. Zero balance is observed, not a verified prerequisite for renewal.',
    'silent_return_restored_off': True,
    'silent_return_verification': 'After setChecked(false) reported an asynchronous state-change error, a fresh read of the visible switch returned aria-checked=false.',
    'download_resolution': 'Download-complete event timed out but actual completed MP4 files appeared in Downloads. All three C06 files were subsequently copied and hash-verified. No pending download.',
    'download_attempt_notes': 'Ordinary Flow reload and original-size menu used. Page-assets bundle failed and produced no file. No alternative-browser or direct-network workaround used.',
    'browser_limit_at_finish': 'After all originals saved and silent-return OFF verified, browser tool requested Chrome extension update while attempting final screenshot/tab marking. No further browser action was attempted.',
    'cumulative_originals_run01_to_run03': {'total': 33, 'C06': 14, 'C05': 19},
    'final_films_created': 0,
})
assert sum(r['observed_debit'] for r in log['requests']) == 90
assert sum(r['refund'] for r in log['requests']) == 10
save(run / 'generation_log.json', log)

manifest = read(run / 'new_keyframes/image_manifest.json')
for im in manifest['images']:
    im.setdefault('artist_review_status_at_creation', im['review_status'])
    im['review_status'] = 'PASS_THREE_INDEPENDENT_AND_CROSS_REVIEW'
    im['pd_review_record'] = '../keyframe_review.json'
    im['motion_review_record'] = '../review_summary.json'
save(run / 'new_keyframes/image_manifest.json', manifest)

for folder in [repo / 'storyboards/2026-10-23_C06-C05-flow-run02', run]:
    data = read(folder / 'generation_log.json')
    local_cache = cache / folder.name.rsplit('-', 1)[-1]
    local_cache.mkdir(parents=True, exist_ok=True)
    cards = []
    for r in data['requests']:
        if not r.get('original_file'):
            continue
        filename = r['original_file']
        for suffix in ['.mp4', '_contact.jpg']:
            n = Path(filename).stem + suffix
            shutil.copyfile(folder / n, local_cache / n)
        cards.append('<article><h2>' + html.escape(Path(filename).stem) + '</h2>'
                     '<video controls preload="metadata" src="' + filename + '"></video>'
                     '<p><a download href="' + filename + '">원본 MP4 저장</a> · '
                     '<a href="' + Path(filename).stem + '_contact.jpg">32개 검수 표본</a></p></article>')
    page = '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair 추가 원본</title><style>body{margin:32px auto;max-width:1100px;padding:0 20px;background:#111827;color:#e5e7eb;font-family:system-ui}a{color:#93c5fd}article{margin:28px 0;padding:20px;background:#1f2937;border-radius:16px}video{width:100%;max-height:620px}h2{font-size:20px}</style><h1>Q-AI Fair · 추가 생성 원본</h1><p>재인코딩하지 않은 Flow 원본입니다. 자막·음악·전체 편집 전이며, 생성 성공과 최종 채택은 다릅니다. <a href="README.md">검수·사용 조건</a></p>' + ''.join(cards) + '</html>'
    (folder / 'originals.html').write_text(page, encoding='utf-8')
    (local_cache / 'originals.html').write_text(page, encoding='utf-8')
    for n in ['README.md', 'review_summary.json', 'generation_log.json']:
        shutil.copyfile(folder / n, local_cache / n)
print('Verified 8 new originals; 90 debit - 10 refund = 80 net; 5 observed balances zero. No original re-encoding.')
