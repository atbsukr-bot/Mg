"""Which camera is the owner looking at? v2 (owner's rule: the shot must always be the camera he is looking into).

v1 sampled keyframes only (cam1 mezz has a keyframe every ~8 s, so its scores were stale) and used Haar detector
confidence. v2 decodes every frame at 5 fps from both cameras and measures real head pose + eye direction with the
MediaPipe face landmarker: for each camera, off = |yaw| + |pitch|/2 + 25 * eye-sideways. The camera with the smaller
`off` is the one he is looking into. Writes work/gaze.json: [[t_master, "c1"|"c2", off1, off2], ...] every 0.2 s.
usage: python3 scripts/gaze2.py [t0 t1]   (model: env FACE_MODEL, default scratch face_landmarker.task)
"""
import json, os, subprocess, sys
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(ROOT, 'scripts', os.environ.get('EP002_CFG', 'sources.json'))))
SRC = os.environ.get('EP002_SRC', '/tmp/claude-0/-home-user-Mg/1696909f-e6cb-52b7-9a07-e6b6a363bb06/scratchpad/src')
MODEL = os.environ.get('FACE_MODEL', '/tmp/claude-0/-home-user-Mg/6b885ee5-64fa-4664-a9b8-4ec136511f44/scratchpad/face_landmarker.task')
FPS = 5
W, H = 640, 360


def landmarker():
    o = vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=MODEL), output_facial_transformation_matrixes=True,
                                     output_face_blendshapes=True, num_faces=1, running_mode=vision.RunningMode.IMAGE)
    return vision.FaceLandmarker.create_from_options(o)


def scores(path, t0, t1, raw):
    """off-axis score per frame (None = no face) for camera-local [t0, t1)"""
    lm = landmarker()
    pre = ['-noautorotate'] if raw else []
    p = subprocess.Popen(['ffmpeg', '-v', 'quiet', *pre, '-ss', f'{t0:.3f}', '-i', path, '-t', f'{t1 - t0:.3f}', '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={W}:{H},format=rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    out = []
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        r = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.frombuffer(buf, np.uint8).reshape(H, W, 3)))
        if not r.face_landmarks:
            out.append(None)
            continue
        R = np.array(r.facial_transformation_matrixes[0])[:3, :3]
        yaw = np.degrees(np.arctan2(R[0, 2], R[2, 2])); pitch = np.degrees(np.arcsin(-R[1, 2]))
        bs = {b.category_name: b.score for b in r.face_blendshapes[0]}
        # eyes turned sideways: one eye looks in while the other looks out
        side = max(bs['eyeLookInLeft'] + bs['eyeLookOutRight'], bs['eyeLookOutLeft'] + bs['eyeLookInRight']) / 2
        out.append(float(abs(yaw) + abs(pitch) / 2 + 25 * side))
    return out


if __name__ == '__main__':
    off = cfg['sync']['cam1']                       # master = cam1 + off
    end1 = cfg['cam1_dur'] + off
    t0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    t1 = float(sys.argv[2]) if len(sys.argv) > 2 else end1
    s1 = scores(os.path.join(SRC, cfg['cam1_file']), max(0.0, t0 - off), min(cfg['cam1_dur'], t1 - off), False)
    s2 = scores(os.path.join(SRC, cfg['cam2_file']), t0, t1, True)
    n = min(len(s2), len(s1) if t0 - off >= 0 else len(s2))
    out = []
    for k in range(len(s2)):
        t = round(t0 + k / FPS, 2)
        a = s1[k] if k < len(s1) and t <= end1 else None
        b = s2[k]
        if a is None and b is None:
            lab = None
        elif a is None:
            lab = 'c2'
        elif b is None:
            lab = 'c1'
        else:
            lab = 'c2' if b < a else 'c1'
        out.append([t, lab, None if a is None else round(a, 1), None if b is None else round(b, 1)])
    # fill gaps and drop single-sample flickers (one look = at least 0.4 s)
    for i in range(len(out)):
        if out[i][1] is None:
            out[i][1] = out[i - 1][1] if i else 'c1'
    lab = [o[1] for o in out]
    for i in range(1, len(lab) - 1):
        if lab[i] != lab[i - 1] and lab[i] != lab[i + 1]:
            lab[i] = lab[i - 1]
    for o, l in zip(out, lab):
        o[1] = l
    json.dump(out, open(os.path.join(ROOT, 'work', 'gaze.json'), 'w'))
    print(sum(1 for o in out if o[1] == 'c2'), 'of', len(out), 'samples looking at cam2')
