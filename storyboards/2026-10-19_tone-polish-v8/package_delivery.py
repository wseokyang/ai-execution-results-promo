from pathlib import Path
import json,hashlib,shutil,zipfile
R=Path(__file__).resolve().parent
B=Path('C:/Users/wseok/.codex/visualizations/2026/10/19/01a13daf-3732-7b90-99a8-92c605090d35')
D=B/'B_comedy_tone_polish_v8';Z=B/'B_comedy_tone_polish_v8_full_package.zip'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert json.loads((R/'delivery_status.json').read_text(encoding='utf-8'))['status']=='complete'
 assert json.loads((R/'validation.json').read_text(encoding='utf-8'))['status']=='passed'
 files=[p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.zip'}]
 for p in files:
  q=D/p.relative_to(R);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(p)==sha(q)
 with zipfile.ZipFile(Z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in files:z.write(p,D.name+'/'+p.relative_to(R).as_posix())
 with zipfile.ZipFile(Z) as z:assert z.testzip() is None
 result={'folder':str(D),'html':str(D/'index.html'),'zip':str(Z),'files':len(files),'zip_bytes':Z.stat().st_size,'zip_sha256':sha(Z),'copy_hashes':'passed','zip_crc':'passed'}
 (B/'B_comedy_tone_polish_v8_package_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
