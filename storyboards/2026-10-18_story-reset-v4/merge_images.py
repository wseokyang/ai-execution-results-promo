"""Merge artist records without changing their selected source images."""
from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parent
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    d=json.loads((R/'storyboards.json').read_text(encoding='utf-8-sig'))
    expected={(c['id'],s['id']):s for c in d['concepts'] for s in c['shots']}
    entries={}
    sources=[]
    for p in sorted(R.glob('image_manifest_artist*.json')):
        a=json.loads(p.read_text(encoding='utf-8-sig'))
        records=a['images']
        sources.append({'file':p.name,'entries':len(records)})
        for m in records:
            if m.get('selected',True) is False:continue
            key=(m['concept_id'],m['cut_id'])
            assert key not in entries,('duplicate selected',key)
            assert key in expected,key
            dest=R/m['image_path']
            assert dest.is_file(),dest
            with Image.open(dest) as im:
                im.load();m['width'],m['height']=im.size
                assert im.format=='PNG'
            m['sha256']=h(dest);m['bytes']=dest.stat().st_size
            source=Path(m.get('source_generated_path',m.get('generated_source_path','')))
            assert source.is_file(),source
            assert h(source)==m['sha256'],('source bytes altered',key)
            m['artist_manifest']=p.name
            m['final_storyboard_first_frame']=expected[key]['first_frame']
            m['final_storyboard_next_motion']=expected[key]['next_motion']
            assert expected[key]['image_file']==m['image_path'],key
            entries[key]=m
    assert set(entries)==set(expected),{'missing':sorted(set(expected)-set(entries))}
    out={'run_id':R.name,'path_base':'this folder','generation_tool':'built-in image_gen','selected_image_count':len(entries),'sources':sources,'images':[entries[k] for k in sorted(entries)]}
    (R/'scene_manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print({'selected':len(entries),'source_byte_equality':'passed'})
if __name__=='__main__':main()
