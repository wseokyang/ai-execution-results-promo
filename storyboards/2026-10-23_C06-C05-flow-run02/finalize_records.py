"""Reconcile completed run metadata without changing original video bytes."""
from pathlib import Path
import hashlib
import json

run = Path(__file__).resolve().parent
repo = run.parents[1]
cache = Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-v11-C06-C05-2026-10-23/run02')
log_path = run / 'generation_log.json'
log = json.loads(log_path.read_text(encoding='utf-8-sig'))
for request in log['requests']:
    inspection = json.loads((run / (Path(request['original_file']).stem + '_inspection.json')).read_text(encoding='utf-8-sig'))
    source = run / request['original_file']
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest == inspection['sha256'] == request['original_sha256']
    assert digest == hashlib.sha256(Path(request['download_source_path']).read_bytes()).hexdigest()
    assert digest == hashlib.sha256((cache / source.name).read_bytes()).hexdigest()
    for field, hash_field in [('input_image', 'input_sha256'), ('end_image', 'end_sha256')]:
        assert hashlib.sha256((repo / request[field]).read_bytes()).hexdigest() == request[hash_field]
    assert (run / request['prompt_file']).read_text(encoding='utf-8-sig').strip() == request['prompt'].strip()
    request['technical_inspection'] = inspection
    request['asset_id_basis'] = 'Observed Flow editor URL /edit/<asset_id>'
    request['generation_id_note'] = 'Internal generation job ID not exposed; visible asset_id and editor URL recorded instead.'
    request['asset_url'] = request['project_url'] + '/edit/' + request['asset_id']
    request['original_preservation'] = 'Download, repository and preview copy SHA-256 identical. No re-encoding.'
    request['status'] = 'COMPLETED_ORIGINAL_PRESERVED'
    request['review_status'] = 'See review_summary.json for visual sample review and edit conditions.'
    if request['unit_id'] == 'C06_K05':
        request.pop('credit_reset_observed_during_request', None)
        request['balance_increase_observed'] = True
        request['renewal_inferred_not_ledger_verified'] = True
        request['billing_note'] = 'UI balance observations were 20 before preparation and 40 after successful generation. Daily renewal notice showed 11:21. The quoted fee immediately before submission was 10. Renewal or refreshed balance is inferred; exact replenishment and debit were not separately observed.'
for q in log['queue']:
    q['status'] = 'COMPLETED_ORIGINAL_PRESERVED'
log.update({
    'status': 'COMPLETED_TWO_REQUESTS_NO_MORE_SUBMISSIONS',
    'budget_used_by_quoted_successful_requests': 20,
    'ending_balance_observed': 30,
    'balance_observations': [20, 40, 30],
    'actual_total_ledger_debit': None,
    'billing_summary': 'Two successful requests quoted 10 each, totaling the authorized 20. First request overlaps a balance increase; second request observed 40 to 30. This historical ending balance was subsequently spent under explicit all-remaining-credits authorization in run03.',
    'pending_requests': 0,
    'refunds_observed': 0,
    'cumulative_originals_with_run01': {'total': 25, 'C06': 11, 'C05': 14},
    'final_films_created': 0,
    'verification': 'Both files: 8 seconds, 1280x720, 24fps, 192 decoded video frames, H264 and AAC. Visual sample review only; no actual audio listening or continuous playback claimed.'
})
log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
manifest_path = run / 'input_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
used = {Path(r[f]).name for r in log['requests'] for f in ['input_image', 'end_image']}
for item in manifest:
    item['used_in_submitted_request'] = item['file'] in used
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Verified two originals, four submitted input frames, exact prompts, preview copies and ledger notes.')
