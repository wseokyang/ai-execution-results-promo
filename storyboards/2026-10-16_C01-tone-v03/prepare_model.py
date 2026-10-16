"""Fetch official local inference weights; no remote inference or paid API."""
from pathlib import Path
import json, os
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
from huggingface_hub import HfApi, snapshot_download

repo = 'Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice'
dest = Path('C:/Users/wseok/.cache/codex-media-tools/models') / repo.split('/')[-1]
info = HfApi().model_info(repo)
print(json.dumps({'repository': repo, 'revision': info.sha, 'destination': str(dest)}), flush=True)
snapshot_download(repo, revision=info.sha, local_dir=dest,
                  allow_patterns=['*.json', '*.txt', '*.safetensors', '*.md', 'LICENSE*'], max_workers=4)
record = {'repository': repo, 'revision': info.sha, 'destination': str(dest),
          'files': [{'path': str(p.relative_to(dest)), 'bytes': p.stat().st_size}
                    for p in dest.rglob('*') if p.is_file() and '.cache' not in p.parts],
          'external_inference_calls': 0}
(Path(__file__).parent/'model_source.json').write_text(json.dumps(record, indent=2), encoding='utf8')
print('Model download complete', flush=True)
