"""Which camera is the owner looking at? (owner's rule: when he looks at cam2, the cut uses cam2)

Samples a frame every STEP seconds from each camera and scores how frontal the face is
(OpenCV frontal-face detector confidence; a turned head drops out of the frontal detector and
shows up in the profile detector). Writes work/gaze.json: [[t_master, "c1"|"c2"], ...]
usage: python3 scripts/gaze.py [t0 t1]
"""
import json, os, subprocess, sys
import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(ROOT, 'scripts', os.environ.get('EP002_CFG', 'sources.json'))))
SRC = os.environ.get('EP002_SRC', '/tmp/claude-0/-home-user-Mg/1696909f-e6cb-52b7-9a07-e6b6a363bb06/scratchpad/src')
STEP = 0.5
front = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
prof = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')


def frames(path, t0, t1, rotate_raw=False):
    """yield (t, gray 480p) every STEP seconds via one ffmpeg pipe"""
    w, h = 854, 480
    pre = ['-noautorotate'] if rotate_raw else []
    p = subprocess.Popen(['ffmpeg', '-v', 'quiet', *pre, '-ss', str(t0), '-i', path, '-t', str(t1 - t0), '-map', '0:v:0',
                          '-vf', f'fps={1 / STEP},scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    k = 0
    while True:
        buf = p.stdout.read(w * h)
        if len(buf) < w * h:
            break
        yield t0 + k * STEP, np.frombuffer(buf, np.uint8).reshape(h, w)
        k += 1


def frontal_score(g):
    _, _, lw = front.detectMultiScale3(g, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60), outputRejectLevels=True)
    fs = float(max(lw)) if len(lw) else 0.0
    pr = prof.detectMultiScale(g, 1.1, 4, minSize=(60, 60))
    pf = prof.detectMultiScale(cv2.flip(g, 1), 1.1, 4, minSize=(60, 60))
    return fs, int(len(pr) + len(pf))


if __name__ == '__main__':
    t0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    t1 = float(sys.argv[2]) if len(sys.argv) > 2 else cfg['cam1_dur'] + cfg['sync']['cam1']
    off = cfg['sync']['cam1']
    c1 = {round(t + off, 1): frontal_score(g) for t, g in frames(os.path.join(SRC, cfg['cam1_file']), max(0, t0 - off), max(0, t1 - off))}
    c2 = {}
    if cfg.get('c2_available', True):
        c2 = {round(t, 1): frontal_score(g) for t, g in frames(os.path.join(SRC, cfg['cam2_file']), t0, t1, rotate_raw=True)}
    out = []
    for t in sorted(set(c1) | set(c2)):
        f1, p1 = c1.get(t, (0.0, 0)); f2, p2 = c2.get(t, (0.0, 0))
        # looking at cam2 = cam2 sees a frontal face clearly better than cam1 does (or cam1 only sees a profile)
        look2 = (f2 > f1 + 1.0) or (f1 == 0.0 and p1 > 0)
        out.append([t, 'c2' if look2 else 'c1', round(f1, 2), round(f2, 2), p1])
    # smooth: require 2 consecutive samples to switch
    lab = [o[1] for o in out]
    for i in range(1, len(lab) - 1):
        if lab[i] != lab[i - 1] and lab[i] != lab[i + 1]:
            lab[i] = lab[i - 1]
    for o, l in zip(out, lab):
        o[1] = l
    json.dump(out, open(os.path.join(ROOT, 'work', 'gaze.json'), 'w'))
    print(sum(1 for o in out if o[1] == 'c2'), 'of', len(out), 'samples looking at cam2')
