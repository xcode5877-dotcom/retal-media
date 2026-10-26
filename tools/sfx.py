"""Procedural SFX + light music bed, synced to a reel's motion cues. Output: stereo 48k WAV."""
import numpy as np, wave, sys, json

SR = 48000
rng = np.random.default_rng(7)

def env(n, a=0.005, r=0.2, shape=2.0):
    t = np.arange(n) / SR
    at = np.clip(t / a, 0, 1)
    rl = np.exp(-t / max(r, 1e-4) * shape)
    return at * rl

def lowpass(x, cutoff):
    # one-pole low-pass, cutoff may be an array (sweeps)
    y = np.zeros_like(x); c = np.broadcast_to(cutoff, x.shape)
    a = 1 - np.exp(-2 * np.pi * c / SR); acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc); y[i] = acc
    return y

def whoosh(dur=0.45, up=True, gain=0.5):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    cut = (300 + 5500 * (t if up else 1 - t) ** 1.5)
    x = lowpass(noise, cut)
    shape = np.sin(np.pi * t) ** 1.5
    return x / (np.abs(x).max() + 1e-9) * shape * gain

def impact(gain=0.9):
    n = int(SR * 0.6); t = np.arange(n) / SR
    f = 45 + 90 * np.exp(-t * 25)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    click = rng.standard_normal(n) * np.exp(-t * 120) * 0.4
    return (body + click) * gain

def tick(freq=1800, gain=0.35):
    n = int(SR * 0.12); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2.01 * t)) * np.exp(-t * 45) * gain

def ding(freq=1318.5, gain=0.3):
    n = int(SR * 0.9); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * freq * m * t) * np.exp(-t * d) for m, a, d in [(1, 1, 5), (2.0, .4, 8), (3.01, .2, 12)])
    return s * gain

def pop(gain=0.45):
    n = int(SR * 0.15); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 200
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35) * gain

def shimmer(dur=1.2, gain=0.22):
    n = int(SR * dur); t = np.arange(n) / SR; out = np.zeros(n)
    for k, f in enumerate([1568, 1976, 2349, 2637, 3136]):
        st = int(k * 0.06 * SR)
        tt = t[: n - st]
        out[st:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 4) * (0.6 ** k)
    return out * gain

def riser(dur=1.0, gain=0.3):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    x = lowpass(rng.standard_normal(n), 200 + 7000 * t ** 2)
    x = x / (np.abs(x).max() + 1e-9)
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * t ** 2) / SR) * 0.3
    return (x + tone) * t ** 2 * gain

def music_bed(total, bpm=100, gain=0.16):
    """Warm minimal bed: soft kick on beats, offbeat hat, sustained pad chords (Am - F - C - G)."""
    n = int(SR * total); out = np.zeros(n); beat = 60 / bpm
    t_all = np.arange(n) / SR
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 261.63, 329.63], [196.0, 246.94, 293.66]]
    bar = beat * 4
    for b in range(int(total / bar) + 1):
        st = int(b * bar * SR); en = min(n, int((b + 1) * bar * SR))
        if st >= n: break
        tt = (np.arange(en - st)) / SR
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2 * tt) for f in chords[b % 4])
        fade = np.minimum(1, np.minimum(tt / 0.25, (bar - tt) / 0.25))
        out[st:en] += pad * fade * 0.08
    for k in range(int(total / beat) + 1):
        st = int(k * beat * SR)
        if st >= n: break
        kk = impact(0.5)[: max(0, min(len(impact()), n - st))]
        out[st: st + len(kk)] += kk * 0.6
        hs = int((k + 0.5) * beat * SR)
        if hs < n:
            h = rng.standard_normal(int(SR * 0.05)) * np.exp(-np.arange(int(SR * 0.05)) / SR * 90) * 0.12
            out[hs: hs + len(h)] += h[: max(0, n - hs)]
    return out * gain

SOUNDS = {'whoosh_up': lambda: whoosh(0.45, True), 'whoosh_down': lambda: whoosh(0.5, False, 0.45),
          'impact': impact, 'tick': tick, 'ding': ding, 'pop': pop, 'shimmer': shimmer, 'riser': riser}

def build(cues, total, out, music=True):
    n = int(SR * total); mix = np.zeros(n)
    if music: mix += music_bed(total)
    for t0, name, g in cues:
        s = SOUNDS[name]() * g; st = int(t0 * SR)
        e = min(n, st + len(s)); mix[st:e] += s[: e - st]
    # gentle fade out + limiter
    fo = int(0.6 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
    peak = np.abs(mix).max(); mix = np.tanh(mix / peak * 1.3) * 0.89
    st = np.stack([mix, np.roll(mix, int(0.004 * SR)) * 0.96], 1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    build([tuple(c) for c in spec['cues']], spec['duration'], sys.argv[2], spec.get('music', True))
