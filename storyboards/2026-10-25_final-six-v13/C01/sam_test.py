import sys,time
sys.path[:0]=['C:/Users/wseok/.cache/codex-media-tools/opencv','C:/Users/wseok/.cache/codex-media-tools/mobilesam/MobileSAM-master']
import torch,cv2,numpy as np
from PIL import Image
from mobile_sam import sam_model_registry,SamPredictor
from pathlib import Path
p=Path(__file__).resolve().parent;root=p.parents[1]
print('cuda',torch.cuda.is_available(),flush=True)
m=sam_model_registry['vit_t'](checkpoint='C:/Users/wseok/.cache/codex-media-tools/mobilesam/MobileSAM-master/weights/mobile_sam.pt');m.to(device="cuda");m.eval()
predictor=SamPredictor(m)
im=np.array(Image.open(root/'2026-10-24_v12-C02-C04-C01-flow/frames/C01_K02_take02/00_0.000s.png'))
t=time.time();predictor.set_image(im);print('encoder',time.time()-t,flush=True)
mask=np.zeros(im.shape[:2],bool)
for box,points in [([0,85,826,720],[[327,238],[491,382],[295,451]]),([368,200,1226,720],[[742,468],[1070,377],[491,344]])]:
 a,s,l=predictor.predict(point_coords=np.array(points),point_labels=np.ones(len(points)),box=np.array(box),multimask_output=False);mask|=a[0];print(s,time.time()-t,flush=True)
Image.fromarray(np.uint8(mask)*255).save(p/'sam_testmask.png')
im[~mask]=(im[~mask]*.3).astype(np.uint8);Image.fromarray(im).save(p/'sam_test.jpg')

