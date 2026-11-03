import sys, json, wave, numpy as np
sys.path.insert(0, '/home/claude/retal/sfx'); import sfx
spec = json.load(open(sys.argv[1])); total = spec['duration']; SR = sfx.SR
n = int(SR * total); mix = sfx.music_bed(total, bpm=spec.get('bpm', 120), gain=0.2)
for t0, name, g in spec['cues']:
    s = sfx.SOUNDS[name]() * g; st = int(t0 * SR); e = min(n, st + len(s)); mix[st:e] += s[:e - st]
fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
mix = np.tanh(mix / np.abs(mix).max() * 1.4) * 0.9
st = np.stack([mix, np.roll(mix, int(0.004 * SR)) * 0.96], 1)
with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
