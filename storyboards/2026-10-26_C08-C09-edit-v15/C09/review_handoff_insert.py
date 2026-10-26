from pathlib import Path
import sys,math
OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(OUT.parent))
from media_common import *
file=OUT/'C09_K08_handoff_insert_candidate_v15.mp4';tiles=[]
with av.open(str(file)) as c:
 for i,f in enumerate(c.decode(video=0)):
  tile=Image.new('RGB',(384,242),(15,23,31));tile.paste(f.to_image().resize((384,216)),(0,26));ImageDraw.Draw(tile).text((6,2),f'original {1.5+i/24:.3f}s / frame {i}',font=font(16),fill='white');tiles.append(tile)
for j in range(math.ceil(len(tiles)/16)):
 sub=tiles[j*16:(j+1)*16];im=Image.new('RGB',(1536,242*math.ceil(len(sub)/4)),(15,23,31))
 for k,tile in enumerate(sub):im.paste(tile,(k%4*384,k//4*242))
 im.save(OUT/f'K08_insert_allframes_{j+1}.jpg',quality=94)
dump(OUT/'rear_review.json',dict(status='CANDIDATE_EDIT_PENDING_REPLACEMENTS',reviewed=['K06 take01','K07 take01','K08 take01','K09 take01','K10 take01'],accepted=['K06 take01','K10 take01'],rejected=['K07 take01 wrong pocket/hand','K09 take01 reverse/open-door departure'],K08=dict(source_interval=[1.5,3.25],crop=[330,215,810,485],frames=len(tiles),actual_action='Charger transfer and giver release',phone_disappearance_interval_excluded=True,hand_continuity_perfect=False,assumption='Brief close-up omits intervening phone handling; does not repair original physics',loss='Enlarged crop is visibly softer than wide source; no frozen frames or interpolation'),actual_continuous_playback_verified=False,actual_listening_verified=False))
print(len(tiles),'handoff frames extracted')
