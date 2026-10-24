from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=json.loads((OUT/'edit_manifest.json').read_text(encoding='utf-8'))
m['status']='Rendered; editor sample inspection and technical checks passed; independent A/B/C judgement pending'
dump(OUT/'edit_manifest.json',m)
v=json.loads((OUT/'technical_validation.json').read_text(encoding='utf-8'))
v['audio_padding_note']='ffmpeg raw decode includes 672 trailing AAC decoder-padding samples; MP4 presentation/decode timestamps contain 2,460,000 samples and end at exactly 51.25s.'
v['loudness_report_note']='loudness.input_* are measured delivered-file values. output_*/normalization_type are analysis-filter simulation, NOT processing applied to the final. Final mix uses fixed gain only.'
dump(OUT/'technical_validation.json',v)
dump(OUT/'editor_review.json',dict(
 reviewer='v12_c05_editor (execution editor; not independent A/B/C)',
 scope='Actual saved PNG/JPEG inspection; no real-time playback or listening',
 opened_files=['preflight_N04.jpg','preflight_jack.jpg','worker_crop_all_frames_01.jpg']+[f'join_contact_{i:02d}.jpg' for i in range(1,4)]+[f'review_contact_{i:02d}.jpg' for i in range(1,8)]+['review_frames/16.250s.png','review_frames/24.750s.png','review_frames/26.208s.png','review_frames/27.750s.png'],
 checked={'worker_crop':'All 36 cropped action frames inspected in the full-frame contact sheet; jack, wheels, gloved hands remain in crop. Head intentionally outside insert framing.','joins':'Every segment boundary sampled at preceding, first and next frame. Critical 16.25/19.25/24.75/26.25/27.75 examined.','captions':'All six overlays inspected at samples; no clipping, event title held 5s.','chain':'Entrance and roof-edge grasp now shown. Complete outward rotation remains an ellipsis covered by worker cutaway.'},
 issues=[{'id':'EDIT-01','severity':'creative limitation','finding':'N04 partial turn and later front view differ in neck silhouette and grip orientation. No complete turn claim.','status':'Documented for independent reviewers; not marked physically continuous'},
 {'id':'EDIT-02','severity':'quality tradeoff','finding':'1.5s jack insert scales a 384×216 crop; softer than wide source.','status':'Accepted for draft, all action remains visible'},
 {'id':'EDIT-03','severity':'verification limit','finding':'No real-time playback or subjective sound check performed.','status':'Pending user/parent workflow'}],
 verdict='Conditional causal-repair review candidate; render complete, final independent approval not claimed',
 originals_unchanged=True,actual_realtime_playback_verified=False,actual_listening_verified=False))
