"""Generate a direction-controlled K04 audition locally on CPU."""
from pathlib import Path
import os, json, time, hashlib
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'
import torch
import soundfile as sf
import numpy as np
from qwen_tts import Qwen3TTSModel

root = Path(__file__).resolve().parent
model_dir = Path('C:/Users/wseok/.cache/codex-media-tools/models/Qwen3-TTS-12Hz-1.7B-CustomVoice')
torch.set_num_threads(8)
torch.manual_seed(42)
started = time.time()
print('Loading instruction-capable model on CPU, float32', flush=True)
model = Qwen3TTSModel.from_pretrained(str(model_dir), device_map='cpu', dtype=torch.float32, attn_implementation='eager')
print('Loaded in', round(time.time()-started, 2), 'seconds', flush=True)
text = '제가 헤맨 과정도, 같이 보여드릴게요.'
direction = ('한국어로 사내 발표 중인 성인 여성의 자연스러운 대화체. '
             '자기가 시행착오를 겪은 경험을 동료에게 편안하고 담담하게 설명한다. '
             '평소 대화보다 조금 여유 있는 속도로, 약 3.5~4초에 걸쳐 말한다. '
             '제가 헤맨 과정도 뒤에는 짧게 숨을 쉬고, 같이 보여드릴게요는 한 호흡으로 자연스럽게 연결한다. '
             '단어마다 끊어 읽지 않고 사람처럼 부드러운 리듬과 작은 억양 변화를 준다. '
             '중간 음역으로 말하며 말끝을 편안하게 내려놓는다. '
             '웃거나 울지 않으며 광고 성우나 기계 안내 방송처럼 또박또박 과장하지 않는다.')
wavs, sr = model.generate_custom_voice(text=text, language='Korean', speaker='Sohee', instruct=direction,
                                      max_new_tokens=150)
out = root/'C01_K04_D_natural_take01.wav'
if not np.isfinite(wavs[0]).all():
    raise ValueError('Non-finite synthesis output; refusing PCM conversion.')
peak = float(np.max(np.abs(wavs[0])))
if peak >= 1.0:
    raise ValueError(f'Float output peak {peak} risks PCM clipping; review before saving.')
sf.write(out, wavs[0], sr, subtype='PCM_16')
record = {'file': out.name, 'model': 'Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice',
          'model_source': 'model_source.json', 'speaker': 'Sohee', 'mode': 'custom_voice_with_instruction',
          'local_only': True, 'device': 'cpu', 'dtype': 'float32', 'attention': 'eager', 'seed': 42,
          'text': text, 'instruct': direction, 'language': 'Korean',
          'sample_rate': sr, 'seconds': len(wavs[0])/sr, 'elapsed_seconds': time.time()-started,
          'float_peak_before_PCM': peak, 'float_samples_finite': True,
          'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
          'reason': 'User rejected v02 as too fast or mechanical; direct performance control instead of matching only timbre.',
          'voice_identity': 'Stock synthetic Sohee voice; not a clone of the K06 synthetic presenter. K06 retained as user accepted.',
          'review_status': 'generated_candidate_not_listened_to_or_approved',
          'paid_api_calls': 0, 'flow_credits_used': 0,
          'sources': ['https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice', 'https://github.com/QwenLM/Qwen3-TTS']}
(root/'voice_generation_log.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(record, ensure_ascii=False), flush=True)
