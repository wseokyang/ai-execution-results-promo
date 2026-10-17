from pathlib import Path
import json, hashlib
from html.parser import HTMLParser
from PIL import Image

ROOT = Path(__file__).resolve().parent
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    errors, checks, files = [], [], []
    data = json.loads((ROOT/'storyboards.json').read_text(encoding='utf-8'))
    manifest = json.loads((ROOT/'scene_manifest.json').read_text(encoding='utf-8'))
    entries = manifest['images']
    mapping = {(i['concept_id'], i['cut_id']): i for i in entries}
    if len(mapping) != len(entries): errors.append('Duplicate concept/cut entries')
    if len(data['concepts']) != 5: errors.append('Must contain exactly five new concepts')
    seen_paths, hashes = set(), set()
    total = 0
    for concept in data['concepts']:
        prior = 0
        for shot in concept['shots']:
            total += 1
            key = (concept['id'], shot['id'])
            if abs(shot['start']-prior) > .001: errors.append(f'{key}: timeline gap/overlap')
            if abs(shot['end']-shot['start']-shot['duration']) > .001: errors.append(f'{key}: duration mismatch')
            if shot['duration'] <= 0: errors.append(f'{key}: non-positive duration')
            for field in ['screen','framing','first_frame','next_motion','continuity_in','continuity_out','image_file']:
                if not shot.get(field): errors.append(f'{key}: missing {field}')
            prior = shot['end']
            if key not in mapping:
                errors.append(f'{key}: no generated image mapping')
                continue
            entry = mapping[key]
            relative = entry['image_path']
            if (ROOT/'delivery_status.json').exists() and shot['image_file'] != relative:
                errors.append(f'{key}: storyboard image_file does not match final selected manifest')
            path = (ROOT/relative).resolve()
            if not path.is_relative_to(ROOT): errors.append(f'{key}: image outside run folder')
            if relative in seen_paths: errors.append(f'{key}: shared file; every cut requires own image')
            seen_paths.add(relative)
            if not path.is_file():
                errors.append(f'{key}: missing {relative}')
                continue
            try:
                with Image.open(path) as image:
                    image.verify()
                with Image.open(path) as image:
                    width,height=image.size
                    fmt=image.format
                if abs(width/height-16/9)>.025: errors.append(f'{key}: aspect {width}x{height} is not 16:9')
                digest=sha(path)
                if digest in hashes: errors.append(f'{key}: duplicate image bytes')
                hashes.add(digest)
                source=Path(entry.get('source_generated_path',''))
                source_matches=source.is_file() and sha(source)==digest
                if not source_matches: errors.append(f'{key}: generated-source copy cannot be verified')
                files.append({'concept_id':key[0],'cut_id':key[1],'image_path':relative,'width':width,'height':height,'format':fmt,'bytes':path.stat().st_size,'sha256':digest,'generated_source_copy_matches':source_matches})
            except Exception as exc: errors.append(f'{key}: image decode error: {exc}')
            if not entry.get('prompt'): errors.append(f'{key}: missing actual prompt')
            if entry.get('generation_tool') != 'image_gen': errors.append(f'{key}: built-in generation provenance missing')
        if abs(prior-concept['duration_seconds'])>.001: errors.append(f'{concept["id"]}: total mismatch')
        if prior>60: errors.append(f'{concept["id"]}: exceeds 60 seconds')
        checks.append({'concept_id':concept['id'],'cuts':len(concept['shots']),'duration_seconds':prior})
    if total != len(entries): errors.append('Storyboard/manifest image count mismatch')
    preserved=json.loads((ROOT/'preserved_assets.json').read_text(encoding='utf-8'))['existing_final_film']
    actual=sha((ROOT/preserved['path']).resolve())
    if actual != preserved['sha256']: errors.append('Preserved C01 final film hash changed')
    videos=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.suffix.lower() in {'.mp4','.mov','.webm','.wav','.mp3'}]
    if videos: errors.append(f'Unexpected video/audio files in new planning run: {videos}')
    html_check={'checked':False}
    if (ROOT/'delivery_status.json').exists():
        class AssetParser(HTMLParser):
            def __init__(self):
                super().__init__(); self.paths=[]; self.shots=0
            def handle_starttag(self,tag,attrs):
                attrs=dict(attrs)
                if tag=='article' and attrs.get('class')=='shot': self.shots+=1
                for key in ('src','href','data-image'):
                    v=attrs.get(key,'')
                    if v and not v.startswith(('#','http:','https:','data:')):
                        self.paths.append(v.split('#')[0])
        parser=AssetParser()
        parser.feed((ROOT/'index.html').read_text(encoding='utf-8'))
        missing=sorted({p for p in parser.paths if not (ROOT/p).is_file()})
        if missing: errors.append(f'HTML references missing files: {missing}')
        if parser.shots != total: errors.append('HTML cut card count mismatch')
        html_check={'checked':True,'cut_cards':parser.shots,'local_paths':len(set(parser.paths)),'missing_files':missing}
    result={'status':'passed' if not errors else 'failed','concepts':checks,'cut_count':total,'selected_image_count':len(files),'unique_image_hashes':len(hashes),'files':files,'existing_C01_unchanged':actual==preserved['sha256'],'new_video_audio_files':videos,'html':html_check,'errors':errors}
    (ROOT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='files'},ensure_ascii=False))
    if errors: raise SystemExit(1)

if __name__=='__main__': main()
