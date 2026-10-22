"""Print compact text review data; no media or source mutations."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent
name=sys.argv[1] if len(sys.argv)>1 else 'storyboards.json'
d=json.loads((R/name).read_text(encoding='utf-8-sig'))
for c in d['concepts']:
    print('\n',c['id'],c['title'],c['duration_seconds'])
    t=0
    for s in c['shots']:
        assert abs(s['start']-t)<.001,(c['id'],s['id'],'gap')
        assert abs(s['end']-s['start']-s['duration'])<.001
        t=s['end']
        print(s['id'],s['start'],s['end'],'START',s['first_frame'],'ACTION',s['screen'])
        for q in s.get('caption_cues',[]):
            assert s['start']<=q['start']<q['end']<=s['end']+.001
            assert q.get('box')
            text=q.get('eyebrow','')+q['text']
            chars=len(text.replace('\n','').replace(' ',''))
            print('  CAP',q['start'],q['end'],q['text'].replace('\n',' / '),'CPS',round(chars/(q['end']-q['start']),1))
    assert t==c['duration_seconds'] and t<=60
print('Concepts:',len(d['concepts']),'Units:',len(d['generation_units']))
