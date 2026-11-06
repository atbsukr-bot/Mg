# Person mask per frame (mediapipe selfie multiclass), temporally smoothed. Saves work/m/%05d.png
import mediapipe as mp, numpy as np, cv2, glob, os
from mediapipe.tasks.python import vision, BaseOptions
seg=vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path='work/selfie.tflite'), output_confidence_masks=True,
    running_mode=vision.RunningMode.VIDEO))
os.makedirs('work/m',exist_ok=True); prev=None
for i,f in enumerate(sorted(glob.glob('work/f/*.jpg'))):
    im=cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2RGB)
    r=seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB,data=im), int(i*1000/30))
    m=1-r.confidence_masks[0].numpy_view().astype(np.float32)   # 0 = background class
    m=cv2.resize(m,(1920,1080),interpolation=cv2.INTER_LINEAR)
    m=prev*0.35+m*0.65 if prev is not None else m; prev=m
    cv2.imwrite(f'work/m/{i:05d}.png',(np.clip(m,0,1)*255).astype(np.uint8))
print('masks',i+1)
