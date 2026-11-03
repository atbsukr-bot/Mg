"""Original score for ep002 (no third-party audio): three cues composed and synthesised in code.
  calm.wav     - piano melody in D minor over string pad (story narration, ~2:08 loop)
  tension.wav  - same motif, lower, with pulse + ticking clock (investigation, ~1:44 loop)
  finale.wav   - slow, sparse piano + swell (ending, ~1:20)
  sfx/*.wav    - ring (old rotary phone), tick, dial, static, heartbeat, boom, whoosh
Run from montage/ep002: python3 scripts/make_music.py
"""
import os, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(2)
os.makedirs('public/music', exist_ok=True)
os.makedirs('public/sfx', exist_ok=True)


def save(path, x, peak=0.89):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    x = x / (np.abs(x).max() + 1e-9) * peak
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def hz(n):  # MIDI note -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def reverb(x, secs=2.8, mix=0.32, seed=0):
    r = np.random.default_rng(seed)
    n = int(secs * SR); t = np.arange(n) / SR
    out = []
    for ch in range(2):
        ir = r.standard_normal(n) * np.exp(-t * 6.9 / secs)
        ir[:int(0.012 * SR)] = 0
        L = 1 << int(np.ceil(np.log2(len(x) + n)))
        wet = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[:len(x)]
        wet /= np.abs(wet).max() + 1e-9
        out.append((1 - mix) * x / (np.abs(x).max() + 1e-9) + mix * wet)
    return np.stack(out, 1)


def piano(f, dur, vel=0.8):
    n = int((dur + 2.5) * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for k, a in enumerate([1, .55, .32, .18, .1, .06, .035], 1):
        inh = f * k * (1 + 0.0004 * k * k)
        s += a * np.sin(2 * np.pi * inh * t) * np.exp(-t * (1.1 + 0.9 * k))
    hammer = rng.standard_normal(n) * np.exp(-t * 180) * 0.15
    env = np.minimum(1, t / 0.004)
    rel = np.where(t > dur, np.exp(-(t - dur) * 5), 1)
    return (s + hammer) * env * rel * vel


def strings(f, dur, vel=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for d in (-0.15, 0, 0.17):  # detuned ensemble
        ff = f * 2 ** (d / 12) * (1 + 0.003 * np.sin(2 * np.pi * 5.2 * t + d * 9))
        ph = 2 * np.pi * np.cumsum(ff) / SR
        s += np.sin(ph) + 0.45 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph) + 0.12 * np.sin(4 * ph)
    k = 60; s = np.convolve(s, np.ones(k) / k, 'same')
    a = np.minimum(1, t / 1.6) * np.minimum(1, (dur - t) / 1.8)
    return s * np.clip(a, 0, 1) * vel


def mix_in(buf, x, at):
    i = int(at * SR); j = min(len(buf), i + len(x))
    if i < len(buf):
        buf[i:j] += x[:j - i]


# --- harmony / melody (D minor). chords as MIDI roots+triads, 4 beats each
BPM = 60; B = 60 / BPM
PROG = [[50, 53, 57], [46, 50, 53], [43, 46, 50], [45, 49, 52]]   # Dm  Bb  Gm  A
PROG2 = [[50, 53, 57], [48, 52, 55], [46, 50, 53], [45, 49, 52]]  # Dm  C   Bb  A
MOTIF = [(74, 1), (72, 0.5), (70, 0.5), (69, 2),                  # A  "theme of the call"
         (69, 1), (70, 0.5), (72, 0.5), (74, 1), (77, 1),
         (76, 1.5), (74, 0.5), (73, 2),
         (74, 3), (None, 1)]
MOTIF_B = [(77, 1), (76, 0.5), (74, 0.5), (72, 2),
           (70, 1), (69, 1), (67, 1), (65, 1),
           (64, 1.5), (65, 0.5), (67, 1), (69, 1),
           (69, 3), (None, 1)]


def melody_line(buf, motif, at, transpose=0, vel=0.55):
    t = at
    for n, d in motif:
        if n is not None:
            mix_in(buf, piano(hz(n + transpose), d * B * 0.95, vel), t)
        t += d * B
    return t


def chords(buf, prog, at, bars, octave=0, vel=0.18, arp=True):
    t = at
    for i in range(bars):
        ch = prog[i % len(prog)]
        mix_in(buf, strings(hz(ch[0] - 12 + octave), 4 * B, vel * 1.2), t)
        for n in ch:
            mix_in(buf, strings(hz(n + octave), 4 * B, vel), t)
        if arp:  # soft left-hand broken chord
            for k, n in enumerate([ch[0] - 12, ch[1], ch[2], ch[1]]):
                mix_in(buf, piano(hz(n + octave), B * 0.9, 0.22), t + k * B)
        t += 4 * B
    return t


def cue_calm():
    bars = 32; L = bars * 4 * B + 4
    buf = np.zeros(int(L * SR))
    chords(buf, PROG, 0, 8)
    chords(buf, PROG2, 8 * 4 * B, 8)
    chords(buf, PROG, 16 * 4 * B, 8)
    chords(buf, PROG2, 24 * 4 * B, 8)
    for s in (4, 12, 20, 28):  # melody enters after an intro, phrase every 8 bars (2 phrases)
        e = melody_line(buf, MOTIF, s * 4 * B)
        melody_line(buf, MOTIF_B, e, vel=0.5)
    return reverb(buf, 3.2, 0.35, 1)


def cue_tension():
    bars = 26; L = bars * 4 * B + 4
    buf = np.zeros(int(L * SR))
    chords(buf, [[c - 2 for c in ch] for ch in PROG], 0, bars, vel=0.16, arp=False)
    # heartbeat-like low pulse on every beat + clock tick on off-beats
    for k in range(bars * 4):
        t = np.arange(int(0.35 * SR)) / SR
        mix_in(buf, np.sin(2 * np.pi * 46 * t) * np.exp(-t * 14) * 0.5, k * B)
        tt = np.arange(int(0.04 * SR)) / SR
        mix_in(buf, np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt * 140) * 0.12, k * B + B / 2)
    for s in (2, 10, 18):
        melody_line(buf, MOTIF, s * 4 * B, transpose=-14, vel=0.5)
    # rising swell into each section end
    for s in (8, 16, 24):
        n = int(6 * SR); t = np.arange(n) / SR
        sw = strings(hz(62), 6, 0.3) * (t / 6) ** 2
        mix_in(buf, sw, s * 4 * B - 6)
    return reverb(buf, 2.4, 0.3, 2)


def cue_finale():
    bars = 18; L = bars * 4 * B + 6
    buf = np.zeros(int(L * SR))
    chords(buf, PROG2, 0, bars, vel=0.14, arp=False)
    t = 4 * 4 * B
    for n, d in MOTIF[:7]:
        if n:
            mix_in(buf, piano(hz(n), d * B * 1.5 * 0.95, 0.5), t)
        t += d * B * 1.5
    melody_line(buf, MOTIF_B, 11 * 4 * B, vel=0.42)
    return reverb(buf, 4.0, 0.42, 3)


# --- sound effects
def tt(d):
    return np.arange(int(SR * d)) / SR


def sfx():
    x = tt(4.0)  # old rotary phone bell: fast clapper on two bells, 2 rings
    bell = (np.sin(2 * np.pi * 1180 * x) + 0.6 * np.sin(2 * np.pi * 1530 * x) + 0.3 * np.sin(2 * np.pi * 2950 * x))
    clap = 0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 22 * x))
    gate = ((x % 2.0) < 1.1).astype(float)
    save('public/sfx/ring.wav', reverb(bell * clap * gate * np.minimum(1, x / 0.01), 1.0, 0.18, 4))
    x = tt(0.06); save('public/sfx/tick.wav', np.sin(2 * np.pi * 2300 * x) * np.exp(-x * 120) + 0.4 * rng.standard_normal(len(x)) * np.exp(-x * 400))
    x = tt(1.4)  # rotary dial return: ratchet clicks slowing down
    d = np.zeros(len(x)); tc = 0.0; k = 0
    while tc < 1.3:
        c = tt(0.012); mix_in(d, np.sin(2 * np.pi * 1800 * c) * np.exp(-c * 300), tc); tc += 0.055 + 0.004 * k; k += 1
    save('public/sfx/dial.wav', d)
    x = tt(1.0); n = rng.standard_normal(len(x)); n = n - np.convolve(n, np.ones(6) / 6, 'same')
    save('public/sfx/static.wav', n * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 11 * x))) * np.minimum(1, (1 - x) / 0.3))
    x = tt(3.0); hb = np.zeros(len(x))
    for b0 in np.arange(0, 3, 0.9):
        for dd, a in ((0, 1), (0.26, 0.7)):
            k_ = tt(0.25); mix_in(hb, a * np.sin(2 * np.pi * 50 * k_) * np.exp(-k_ * 16), b0 + dd)
    save('public/sfx/heartbeat.wav', hb)
    x = tt(3.0); save('public/sfx/boom.wav', reverb(np.sin(2 * np.pi * (40 + 30 * np.exp(-x * 6)) * x) * np.exp(-x * 1.6), 2.0, 0.3, 5))
    x = tt(0.9); n = rng.standard_normal(len(x)); w = np.convolve(n, np.ones(25) / 25, 'same')
    save('public/sfx/whoosh.wav', w * np.sin(np.pi * x / 0.9) ** 3)
    x = tt(2.5)  # dial tone cut + line dead beep
    save('public/sfx/deadline.wav', (np.sin(2 * np.pi * 950 * x) * ((x % 0.6) < 0.3)) * 0.6)


if __name__ == '__main__':
    import sys
    if 'sfx' in sys.argv:
        sfx(); raise SystemExit
    save('public/music/calm.wav', cue_calm())
    save('public/music/tension.wav', cue_tension())
    save('public/music/finale.wav', cue_finale())
    sfx()
    print('music + sfx ok')
