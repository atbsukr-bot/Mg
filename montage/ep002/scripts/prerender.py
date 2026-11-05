"""Speed-up helper: pre-render the camera pieces of an EDL from the END backwards, in parallel with a running build.
build.py caches pieces by key, so the main build picks these up instead of rendering them itself.
Each piece is written to a temp file and renamed, so the main build never sees a half-written file.
usage: python3 scripts/prerender.py edl_A.json [workers]"""
import multiprocessing as mp
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402

calls = []


class Stop(Exception):
    pass


def collect():
    real_piece, real_run = B.piece, B.run

    def rec(*a, **kw):
        calls.append((a, kw))
        return os.path.join(B.WORK, f'_dummy_{len(calls)}.mp4')

    def stop(cmd, **kw):
        raise Stop()
    B.piece, B.broll, B.insert, B.run = rec, (lambda *a: 'b_x.mp4'), (lambda *a: 'i_x.mp4'), stop
    try:
        B.build(os.path.join(B.ROOT, 'scripts', sys.argv[1]), os.devnull)
    except Stop:
        pass
    B.piece, B.run = real_piece, real_run


def safe_run(cmd, **kw):
    out = cmd[-1]
    tmp = out[:-4] + '.tmp.mp4'
    B.subprocess.run(cmd[:-1] + [tmp], check=True, **kw)
    os.replace(tmp, out)


def work(c):
    B.run = safe_run
    a, kw = c
    B.piece(*a, **kw)


if __name__ == '__main__':
    collect()
    todo = list(reversed(calls))
    print('pieces', len(todo), flush=True)
    with mp.Pool(int(sys.argv[2]) if len(sys.argv) > 2 else 2) as p:
        for k, _ in enumerate(p.imap(work, todo)):
            if k % 25 == 0:
                print('done', k, flush=True)
    print('prerender finished', flush=True)
