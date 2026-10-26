from pathlib import Path
import json,hashlib,sys,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av,numpy as np
R=Path(__file__).resolve().parent;SB=R.parent;ROOT=SB.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
d=json.loads((R/'delivery_manifest.json').read_text(encoding='utf8'))
checked={};comparisons=[]
for item in d['films']:
 cid=item['concept_id'];folder=R/cid;m=json.loads((folder/'edit_manifest.json').read_text(encoding='utf8'));base=ROOT/m['base_file'];current=folder/m['file']
 original=json.loads((base.parent/'edit_manifest.json').read_text(encoding='utf8'))
 for rel,expected in original.get('source_sha256',{}).items():
  if rel in checked:continue
  p=SB/rel
  assert p.exists(),p
  actual=sha(p);assert actual==expected,(rel,actual,expected)
  checked[rel]=actual
 # Validate unchanged action frames at spaced timestamps outside newly authored overlay zones.
 times=list(range(0,int(item['duration_seconds'])-6,3))
 inds={round(t*24) for t in times};before={};after={}
 for path,dest in [(base,before),(current,after)]:
  with av.open(str(path)) as c:
   for i,f in enumerate(c.decode(video=0)):
    if i in inds:dest[i]=f.to_ndarray(format='rgb24')
 diffs={}
 for i in inds:
  a=before[i].astype(float);b=after[i].astype(float)
  # C03 top overlay moved. Exclude only its 26.25-28.85 interval, still comparing other pixels.
  if cid=='C03' and 26.25<=i/24<28.85:a=a[200:];b=b[200:]
  diffs[str(i/24)]=float(np.abs(a-b).mean())
 assert max(diffs.values())<2.5,(cid,diffs)
 comparisons.append(dict(concept_id=cid,mean_absolute_pixel_difference_by_time=diffs,threshold=2.5,meaning='Frames correspond to same action/timing. Differences below threshold are expected from one additional encoding; not a perceptual listening or continuous-playback test.'))
 q=json.loads((folder/'technical_qa.json').read_text(encoding='utf8'));q['source_asset_hashes_verified']=True;q['action_frame_sample_comparison']=diffs
 dump(folder/'technical_qa.json',q)
 item['sha256']=q['sha256'];item['technical_qa']=str((folder/'technical_qa.json').relative_to(ROOT))
 d['qa']=[json.loads((R/x['concept_id']/'technical_qa.json').read_text(encoding='utf8')) for x in d['films']]
dump(R/'source_preservation_validation.json',dict(asset_count=len(checked),sha256=checked,result='PASS',same_action_sample_comparisons=comparisons))
dump(R/'delivery_manifest.json',d)
print('PRESERVED',len(checked),'assets; comparisons pass')
