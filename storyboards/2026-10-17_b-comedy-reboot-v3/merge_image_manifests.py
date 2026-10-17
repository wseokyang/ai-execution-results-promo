from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def main():
    entries = []
    sources = []
    for name in ('image_manifest_artist1.json', 'image_manifest_artist2.json', 'image_manifest_artist3.json'):
        path = ROOT / name
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        source_entries = data.get('entries', data.get('images', []))
        sources.append({'file': name, 'entry_count': len(source_entries)})
        for original in source_entries:
            entry = dict(original)
            relative = entry['image_path'].replace('\\', '/')
            prefix = 'storyboards/' + ROOT.name + '/'
            if relative.startswith(prefix):
                relative = relative[len(prefix):]
            entry['image_path'] = relative
            entry['artist_manifest'] = name
            entries.append(entry)
    grouped = {}
    for entry in entries:
        key = entry['concept_id'], entry['cut_id']
        grouped.setdefault(key, []).append(entry)
    selected, alternatives = [], []
    for key, variants in sorted(grouped.items()):
        def revision(e):
            try:
                return int(e.get('revision', 1))
            except (ValueError, TypeError):
                return 1
        variants.sort(key=revision)
        selected.append(variants[-1])
        alternatives.extend(variants[:-1])
    result = {
        'run_id': ROOT.name,
        'scope': 'five new concepts, actual first-frame image per cut',
        'path_base': 'this run folder',
        'sources': sources,
        'selected_image_count': len(selected),
        'images': selected,
        'superseded_variants': alternatives,
        'status': 'artist_outputs_merged_pending_final_review',
        'ending_policy': 'raw PNG is a text-free background plate; HTML title is a separate placement preview',
        'flow_uploads': 0,
        'new_videos': 0,
    }
    (ROOT / 'scene_manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'selected_images': len(selected), 'superseded_variants': len(alternatives), 'sources': sources}, ensure_ascii=False))


if __name__ == '__main__':
    main()
