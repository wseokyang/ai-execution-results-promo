"""Verify deliverable files and links, not perceptual listening/playback."""
from pathlib import Path
import json,hashlib,re,urllib.parse
E=Path(__file__).resolve().parent;ROOT=E.parent.parent
N=ROOT/'storyboards/2026-10-26_C01-C07-C10-rewrite-v15'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
issues=[];tested=[]
for f in load(E/'delivery_manifest.json')['films']:
    p=ROOT/f['file']; assert p.exists(),p
    assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
    assert f['duration_seconds']<=60
    tested.append({'file':f['file'],'sha256':f['sha256'],'duration_seconds':f['duration_seconds']})
for cid in ['C08','C09']:
    m=load(E/cid/'edit_manifest.json');last=0
    for row in m['timeline']:
        assert row['start']==last,(cid,row)
        assert abs((row['end']-row['start'])-(row['source_out']-row['source_in']))<1e-6
        last=row['end']
    assert last+5==m['duration_seconds']
    for cue in m['captions']:
        assert 0<=cue['start']<cue['end']<=m['duration_seconds'],(cid,cue)
scenes=load(N/'scene_manifest.json')['scenes'];assert len(scenes)==27
for s in scenes:
    p=ROOT/s['image_path'];assert p.exists()
    assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256']
for c in load(N/'storyboards.json')['concepts']:
    prev=0
    for shot in c['shots']:
        assert abs(shot['start']-prev)<1e-6,(c['id'],shot['id'])
        prev=shot['end']
    assert abs(prev-c['duration_seconds'])<1e-6
names=['README.md','00_완성_영상.md','00_새1-7-10_콘티.md','00_V15_제작_검수.md','콘티_바로보기.md',
    '01_감독님_아직인데요.md','07_셰프님_그것도_주세요.md','10_지구_대표_질문_있습니다.md',
    '00_새7-10_콘티.md','00_영상제작_현재상태.md','00_최종_재검수.md',
    '08_구조는_끝났습니다.md','09_나_없이도_괜찮겠어요.md']
docs=[ROOT/n for n in names]+list(N.glob('*_storyboard.md'))
links=0
for doc in docs:
    for dest in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
        if dest.startswith(('http:','https:','#')):continue
        dest=urllib.parse.unquote(dest.strip('<>').split('#')[0])
        if not dest:continue
        links+=1
        if not (doc.parent/dest).exists():issues.append({'document':str(doc.relative_to(ROOT)),'missing':dest})
assert not issues,issues
result={'seven_films_hash_duration_verified':tested,'selected_images_hash_verified':27,
    'new_storyboard_timelines_contiguous':True,'C08_C09_edit_and_caption_timings_verified':True,
    'local_markdown_links_checked':links,'missing_links':issues,
    'actual_listening_verified':False,'continuous_playback_verified':False}
(E/'delivery_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS: 7 media hashes, 27 selected images, new timelines/captions and',links,'local links.')
