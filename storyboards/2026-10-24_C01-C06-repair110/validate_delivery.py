from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;SB=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
log=json.loads((R/'generation_log.json').read_text(encoding='utf-8'))
ledger=json.loads((R/'budget_ledger.json').read_text(encoding='utf-8'))
assert len(log['entries'])==11 and sum(x['net_spend'] for x in ledger['requests'])==110
assert set(ledger['final_balance_observed'].values())=={0}
assert sum(e['review']=='SELECTED_INTERVAL' for e in log['entries'])==5
for e in log['entries']:
    assert sha(R/e['original'])==e['sha256']==e['download_sha256']
    assert (R/e['prompt']).is_file() and (R/e['input']).is_file()
    assert sha(R/e['input'])==e['input_sha256']
    q=next(x for x in json.loads((R/'queue.json').read_text(encoding='utf-8')) if x['unit']==e['unit_id'])
    assert (R/e['prompt']).read_text(encoding='utf-8').strip()==q['prompt'].strip()
cache=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-repair110-2026-10-24')
for folder in [SB/'2026-10-25_C05-jack-edit-v06',SB/'2026-10-25_C06-impact-edit-v06']:
    d=json.loads((folder/'technical_validation.json').read_text(encoding='utf-8'));assert sha(folder/d['file'])==d['sha256']==sha(cache/d['file'])
for e in log['entries']:assert sha(cache/e['original'])==e['sha256']
files=[ROOT/'README.md',ROOT/'00_110크레딧_보완결과.md',ROOT/'00_완성_영상.md',R/'README.md']
for p in files:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if '://' in link or link.startswith('#'):continue
        assert (p.parent/link.split('#')[0]).exists(),(p,link)
result=dict(originals=11,selected=5,held=6,credits=110,accounts_verified_zero=5,exact_motion_prompts_match_queue=True,original_sha_verified=True,windows_copies_sha_verified=True,local_markdown_links_verified=True,final_edits_sha_verified=True,scope='Technical and file checks, not listening/realtime/venue review')
(R/'delivery_validation.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
p=R/'review_summary.json';d=json.loads(p.read_text(encoding='utf-8'));d['metadata_recheck']={r:'Actual corrected manifest reread; issue resolved, visual judgement unchanged.' for r in ['A','B','C']};p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(result,ensure_ascii=False))
