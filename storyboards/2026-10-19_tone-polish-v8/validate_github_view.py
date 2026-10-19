from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parent.parent
def main():
    text=(ROOT/'콘티_바로보기.md').read_text(encoding='utf-8')
    paths=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text)
    assert len(paths)==43 and all((ROOT/p).is_file() for p in paths)
    expected=[R.relative_to(ROOT).as_posix()+'/'+s['image_file'] for c in json.loads((R/'storyboards.json').read_text(encoding='utf-8'))['concepts'] for s in c['shots']]
    assert paths==expected
    for cid in ['C01','C02','C03','C04','C05']:assert '\n## '+cid+'\n' in text
    assert '[전체 이미지 콘티 바로보기 →](콘티_바로보기.md)' in (ROOT/'README.md').read_text(encoding='utf-8')
    report={'status':'passed','inline_images':43,'image_order_matches_storyboards':True,'broken_image_paths':[],'readme_entry':True,'scope':'source and local image paths; remote commit checked separately','sha256':hashlib.sha256((ROOT/'콘티_바로보기.md').read_bytes()).hexdigest()}
    (R/'github_view_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(report)
if __name__=='__main__':main()
