"""Generate a local replacement from the already-synthetic Flow presenter voice."""
from pathlib import Path
import os, json, time, hashlib
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['HF_HUB_OFFLINE']='1'
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

root=Path(__file__).resolve().parent
model_dir=Path('C:/Users/wseok/.cache/codex-media-tools/models/Qwen3-TTS-12Hz-0.6B-Base')
torch.manual_seed(42)
torch.set_num_threads(8)
print({'torch':torch.__version__,'gpu':torch.cuda.get_device_name(0)},flush=True)
started=time.time()
model=Qwen3TTSModel.from_pretrained(str(model_dir),device_map='cuda:0',dtype=torch.float32,attn_implementation='eager')
print('model loaded',round(time.time()-started,2),flush=True)
text='제가 헤맨 과정도 같이 보여드릴게요.'
wavs,sr=model.generate_voice_clone(text=text,language='Korean',
    ref_audio=str(root/'D_reference_clean_from_K06.wav'),ref_text='다음 사례도 볼까요?',
    max_new_tokens=180)
out=root/'C01_K04_D_qwen_take01.wav'
sf.write(out,wavs[0],sr,subtype='PCM_16')
record={'file':out.name,'model':'Qwen/Qwen3-TTS-12Hz-0.6B-Base','mode':'voice_clone','local_only':True,'seed':42,'dtype':'float32','attention':'eager','text':text,'language':'Korean',
 'reference':{'file':'D_reference_clean_from_K06.wav','source':'storyboards/2026-10-16_flow-run-05/C01_K06_take01.mp4','in':4.5,'duration':1.8,'transcript':'다음 사례도 볼까요?','provenance':'Existing synthetic Flow character D, not a real person recording.'},
 'sample_rate':sr,'seconds':len(wavs[0])/sr,'elapsed_seconds':time.time()-started,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'review_status':'generated_candidate_not_listened_to_or_approved','paid_api_calls':0,'flow_credits_used':0,
 'sources':['https://github.com/QwenLM/Qwen3-TTS','https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base']}
(root/'voice_generation_log.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(record,ensure_ascii=False),flush=True)
