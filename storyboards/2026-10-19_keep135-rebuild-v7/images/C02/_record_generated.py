import json, pathlib, shutil, hashlib, sys
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[2]
e=json.load(sys.stdin)
target=root/e["image_path"]
target.parent.mkdir(parents=True,exist_ok=True)
assert not target.exists(), target
shutil.copyfile(e["source_generated_path"],target)
e["width"],e["height"]=Image.open(target).size
e["sha256"]=hashlib.sha256(target.read_bytes()).hexdigest()
e["source_copy_sha256_match"]=e["sha256"]==hashlib.sha256(pathlib.Path(e["source_generated_path"]).read_bytes()).hexdigest()
sb=json.loads((root/"storyboards.json").read_text(encoding="utf-8-sig"))
shot=next(s for c in sb["concepts"] if c["id"]=="C02" for s in c["shots"] if s["id"]==e["cut_id"])
e["followup_motion"]=shot["next_motion"]
m=root/"image_manifest_C02.json"
data=json.loads(m.read_text(encoding="utf-8")) if m.exists() else {"concept_id":"C02","expected_images":9,"images":[]}
data["images"].append(e)
data["completed_images"]=sum(1 for x in data["images"] if x["selected"])
m.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"path":str(target),"sha256":e["sha256"],"count":data["completed_images"]}))
