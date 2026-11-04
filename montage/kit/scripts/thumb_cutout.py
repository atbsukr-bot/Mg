# usage: python3 thumb_cutout.py <frame_index>  -> app/public/t3_person.png (subject+guitar with alpha) + t3_bg.jpg (soft blurred bg)
import sys, cv2, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
# model: https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite
seg=vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=BaseOptions(model_asset_path='/home/claude/proj/raw/selfie.tflite'),output_confidence_masks=True))
i=int(sys.argv[1]); P='/home/claude/proj/app/public/'
pre=sys.argv[2] if len(sys.argv)>2 else 't3'   # output name prefix
img=cv2.imread(P+f'frames/{i:05d}.jpg')
r=seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)))
m=1-r.confidence_masks[0].numpy_view(); m=cv2.GaussianBlur(m,(9,9),0)
a=(np.clip((m-0.3)/0.4,0,1)*255).astype(np.uint8)
cv2.imwrite(P+pre+'_person.png',np.dstack([img,a]))
cv2.imwrite(P+pre+'_bg.jpg',cv2.GaussianBlur(img,(0,0),7),[cv2.IMWRITE_JPEG_QUALITY,95])
