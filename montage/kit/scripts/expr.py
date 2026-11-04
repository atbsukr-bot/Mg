import cv2, numpy as np, mediapipe as mp, json
from mediapipe.tasks.python import vision, BaseOptions
lm=vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path="/home/claude/proj/raw/face_landmarker.task"),output_face_blendshapes=True,num_faces=1))
res=[]
for i in range(0,9715,8):
    img=cv2.imread(f"/home/claude/proj/app/public/frames/{i:05d}.jpg")
    sm=cv2.resize(img,(640,360))
    r=lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(sm,cv2.COLOR_BGR2RGB)))
    if not r.face_landmarks: continue
    b={x.category_name:x.score for x in r.face_blendshapes[0]}
    sharp=cv2.Laplacian(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),cv2.CV_64F).var()
    L=np.array([[p.x,p.y] for p in r.face_landmarks[0]])
    res.append(dict(i=i,jaw=b['jawOpen'],wide=(b['eyeWideLeft']+b['eyeWideRight'])/2,smile=(b['mouthSmileLeft']+b['mouthSmileRight'])/2,brow=b['browInnerUp'],blink=(b['eyeBlinkLeft']+b['eyeBlinkRight'])/2,sharp=sharp,w=float(L[:,0].max()-L[:,0].min())))
json.dump(res,open('/home/claude/proj/raw/expr.json','w'))
for k in ['jaw','wide','smile']:
    top=sorted([x for x in res if x['sharp']>60 and x['blink']<0.4],key=lambda x:-(x[k]+0.5*x['brow']+0.3*x['jaw']))[:6]
    print(k,[(x['i'],round(x['jaw'],2),round(x['wide'],2),round(x['smile'],2),int(x['sharp'])) for x in top])
