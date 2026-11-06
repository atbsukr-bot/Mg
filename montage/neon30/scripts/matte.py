# Person matte per frame: Mask2Former panoptic "person" at 960x540, refined to the image edges with a guided filter,
# light temporal smoothing. Writes work/m2/%05d.png
import torch,numpy as np,cv2,glob,os
from transformers import AutoImageProcessor, Mask2FormerForUniversalSegmentation
torch.set_num_threads(4)
name='facebook/mask2former-swin-tiny-coco-panoptic'
proc=AutoImageProcessor.from_pretrained(name); m=Mask2FormerForUniversalSegmentation.from_pretrained(name).eval()
os.makedirs('m2',exist_ok=True); prev=None
for i,fp in enumerate(sorted(glob.glob('f/*.jpg'))):
    if os.path.exists(f'm2/{i:05d}.png'):
        prev=cv2.imread(f'm2/{i:05d}.png',0).astype(np.float32)/255; continue
    f=cv2.imread(fp); small=cv2.resize(f,(960,540))
    inp=proc(images=cv2.cvtColor(small,cv2.COLOR_BGR2RGB),return_tensors='pt')
    with torch.no_grad(): out=m(**inp)
    r=proc.post_process_panoptic_segmentation(out,target_sizes=[(540,960)],label_ids_to_fuse={0})[0]
    seg=r['segmentation'].numpy(); ids=[s['id'] for s in r['segments_info'] if s['label_id']==0]
    mk=cv2.resize(np.isin(seg,ids).astype(np.float32),(1920,1080))
    a=np.clip(cv2.ximgproc.guidedFilter(f,(mk*255).astype(np.uint8),12,1e-4).astype(np.float32)/255,0,1)
    if prev is not None: a=np.where(np.abs(a-prev)<0.25,prev*0.4+a*0.6,a)   # damp flicker, keep real motion
    prev=a; cv2.imwrite(f'm2/{i:05d}.png',(a*255).astype(np.uint8))
print('done',i+1)
