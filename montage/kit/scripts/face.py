import cv2, json, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
opts=vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path="/home/claude/proj/raw/face_landmarker.task"),
    output_facial_transformation_matrixes=True, output_face_blendshapes=True, num_faces=1, running_mode=vision.RunningMode.IMAGE)
lm=vision.FaceLandmarker.create_from_options(opts)
cap=cv2.VideoCapture("/home/claude/proj/raw/proxy5.mp4"); i=0; res=[]
while True:
    ok,f=cap.read()
    if not ok: break
    img=mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
    r=lm.detect(img); t=i/5.0
    if r.face_landmarks:
        L=np.array([[p.x,p.y] for p in r.face_landmarks[0]])
        M=np.array(r.facial_transformation_matrixes[0])
        R=M[:3,:3]; yaw=np.degrees(np.arctan2(R[0,2],R[2,2])); pitch=np.degrees(np.arcsin(-R[1,2]))
        bs={b.category_name:b.score for b in r.face_blendshapes[0]}
        eyeoff=max(bs.get('eyeLookOutLeft',0),bs.get('eyeLookOutRight',0),bs.get('eyeLookInLeft',0),bs.get('eyeLookInRight',0))
        down=(bs.get('eyeLookDownLeft',0)+bs.get('eyeLookDownRight',0))/2
        res.append(dict(t=t,face=1,cx=float(L[:,0].mean()),cy=float(L[:,1].mean()),w=float(L[:,0].max()-L[:,0].min()),yaw=float(yaw),pitch=float(pitch),eyeoff=float(eyeoff),down=float(down)))
    else: res.append(dict(t=t,face=0))
    i+=1
json.dump(res,open("/home/claude/proj/raw/face.json","w"))
print(i)
