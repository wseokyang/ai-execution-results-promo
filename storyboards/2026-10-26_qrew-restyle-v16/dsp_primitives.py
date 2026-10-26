"""Mathematical instrument primitives adapted from user-owned QREW DSP; no source score events."""

import numpy as np

SR=48000

RNG=np.random.default_rng(261016)

def axis(duration):
    return np.arange(round(duration * SR), dtype=np.float64) / SR

def hz(midi):
    return 440 * 2 ** ((midi - 69) / 12)

def fade(signal, attack=0.003, release=0.03):
    result = signal.copy()
    a, r = (min(len(result), round(attack * SR)), min(len(result), round(release * SR)))
    if a:
        result[:a] *= np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    if r:
        result[-r:] *= np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return result

def noise(duration, lower=200, upper=3400):
    raw = RNG.standard_normal(round(duration * SR))
    f = np.fft.rfftfreq(len(raw), 1 / SR)
    filt = f ** 2 / (f ** 2 + lower ** 2) / np.sqrt(1 + (f / upper) ** 8)
    sig = np.fft.irfft(np.fft.rfft(raw) * filt, n=len(raw))
    return sig / max(float(np.std(sig)), 1e-09)

def kick(duration=0.22):
    t = axis(duration)
    freq = 48 + 102 * np.exp(-t / 0.019)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    body = np.sin(phase) * np.exp(-t / 0.064)
    knock = 0.09 * noise(duration, 1200, 3000) * np.exp(-t / 0.005)
    return fade(body + knock, 0.001, 0.018)

def snare(duration=0.18, ghost=False):
    t = axis(duration)
    pitch = 172 + 52 * np.exp(-t / 0.013)
    body = 0.26 * np.sin(2 * np.pi * np.cumsum(pitch) / SR) * np.exp(-t / 0.025)
    wires = 0.31 * noise(duration, 1500, 6800) * np.exp(-t / (0.033 if ghost else 0.047))
    return fade(body + wires, 0.0013, 0.028)

def hat(duration=0.07, opened=False):
    t = axis(duration)
    decay = 0.072 if opened else 0.015
    metallic = sum((np.sin(2 * np.pi * f * t) for f in [6120, 7033, 8917])) / 3
    sig = (0.7 * noise(duration, 5000, 10000) + 0.15 * metallic) * np.exp(-t / decay)
    return fade(sig, 0.001, 0.012)

def rim(duration=0.08):
    t = axis(duration)
    sig = 0.4 * np.sin(2 * np.pi * 835 * t) + 0.27 * np.sin(2 * np.pi * 1721 * t)
    sig *= np.exp(-t / 0.009)
    sig += 0.15 * noise(duration, 2000, 5000) * np.exp(-t / 0.004)
    return fade(sig, 0.0007, 0.01)

def conga(midi, duration=0.16):
    t = axis(duration)
    f = hz(midi)
    phase = 2 * np.pi * (f * t + 0.9 * (1 - np.exp(-t / 0.007)))
    sig = (np.sin(phase) + 0.23 * np.sin(phase * 1.503)) * np.exp(-t / 0.048)
    sig += 0.035 * noise(duration, 800, 3000) * np.exp(-t / 0.003)
    return fade(sig, 0.0008, 0.018)

def funk_bass(midi, duration=0.21, pop=False, slide=0):
    t, f = (axis(duration), hz(midi))
    freq = f * (1 + 0.06 * np.exp(-t / 0.006))
    if slide:
        freq *= 2 ** (slide / 12 * np.exp(-t / 0.018))
    phase = 2 * np.pi * np.cumsum(freq) / SR
    sig = np.zeros_like(t)
    for p in range(1, 12):
        sig += np.sin(phase * p + 0.04 * p) / p ** 1.45 * np.exp(-t / (0.19 / p ** 0.48))
    sig += (0.11 if pop else 0.055) * noise(duration, 1400, 6200) * np.exp(-t / 0.0045)
    sig = np.tanh(sig * 1.35) / 1.35
    return fade(sig, 0.0012, 0.029)

def clav(midi, duration=0.16):
    t, f = (axis(duration), hz(midi))
    phase = 2 * np.pi * f * t
    sig = sum((np.sin(p * phase + 0.1 * p) / p ** 1.2 * np.exp(-t / (0.075 / np.sqrt(p))) for p in range(1, 14)))
    sig += 0.12 * np.sin(2 * np.pi * f * 1.002 * t) * np.exp(-t / 0.06)
    return fade(np.tanh(sig) * 0.85, 0.001, 0.035)

def electric_key(midi, duration=0.7):
    t, f = (axis(duration), hz(midi))
    phase = 2 * np.pi * f * t
    sig = np.sin(phase + 0.95 * np.sin(phase * 2) * np.exp(-t / 0.14))
    sig *= np.exp(-t / 0.28)
    sig += 0.16 * np.sin(phase * 3.002) * np.exp(-t / 0.081)
    return fade(sig, 0.008, 0.2)

def brass_stab(notes, duration=0.18):
    t = axis(duration)
    sig = np.zeros_like(t)
    for midi in notes:
        phase = 2 * np.pi * hz(midi) * t
        for p in range(1, 9):
            sig += np.sin(p * phase) / p ** 1.52 * np.exp(-t * p / 0.25)
    return fade(np.tanh(sig / len(notes)), 0.012, 0.05)

def strings(midi, duration, bright=False):
    """A small additive, detuned string ensemble with slow bow movement."""
    t, f = (axis(duration), hz(midi))
    sig = np.zeros_like(t)
    for detune in [-0.0034, -0.0011, 0.0018, 0.0041]:
        phase_offset = RNG.uniform(0, 2 * np.pi)
        phase = 2 * np.pi * f * (1 + detune) * t + 0.018 * np.sin(2 * np.pi * 5.15 * t + phase_offset)
        for harmonic in range(1, 16 if bright else 11):
            formant = 0.6 + 0.4 * np.exp(-((harmonic * f - 900) / 750) ** 2)
            sig += np.sin(phase * harmonic + phase_offset) * formant / harmonic ** 1.65
    sig /= 5.3
    bow = 0.79 + 0.12 * np.sin(2 * np.pi * 0.39 * t) + 0.055 * np.sin(2 * np.pi * 4.1 * t)
    sig *= bow
    return fade(sig, 0.2, min(0.37, duration * 0.25))

def low_blast(midi, duration=2.35):
    """Bowed low brass-like resonant pressure, without sampled instruments."""
    t, f = (axis(duration), hz(midi))
    phase = 2 * np.pi * f * t + 0.032 * np.sin(2 * np.pi * 3.8 * t)
    sig = np.zeros_like(t)
    for harmonic in range(1, 14):
        sig += np.sin(phase * harmonic) / harmonic ** 1.25
    sig = np.tanh(sig * 1.05) * (0.68 + 0.32 * np.exp(-t / 0.7))
    return fade(sig, 0.09, 0.72)

def kettle(midi=36, duration=0.85):
    t, f = (axis(duration), hz(midi))
    pitch = f * (1 + 0.36 * np.exp(-t / 0.023))
    phase = 2 * np.pi * np.cumsum(pitch) / SR
    sig = 0.8 * np.sin(phase) * np.exp(-t / 0.27)
    sig += 0.35 * np.sin(phase * 1.51) * np.exp(-t / 0.15)
    sig += 0.14 * noise(duration, 90, 2700) * np.exp(-t / 0.039)
    return fade(sig, 0.001, 0.25)

def pluck(midi, duration=0.55):
    t, f = (axis(duration), hz(midi))
    sig = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.1)
    sig += 0.27 * np.sin(2 * np.pi * f * 2.008 * t) * np.exp(-t / 0.032)
    sig += 0.07 * np.sin(2 * np.pi * f * 3.015 * t) * np.exp(-t / 0.02)
    return fade(sig, 0.0015, 0.18)

def chime(midi, duration=0.75):
    t, f = (axis(duration), hz(midi))
    sig = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.34)
    sig += 0.18 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.13)
    sig += 0.075 * np.sin(2 * np.pi * f * 3 * t) * np.exp(-t / 0.07)
    return fade(sig, 0.003, 0.24)

def submarine(midi, duration):
    """Slow, beating, slightly metallic pressure rather than bowed strings."""
    t, f = (axis(duration), hz(midi))
    phase = 2 * np.pi * f * t + 0.19 * np.sin(2 * np.pi * 0.37 * t)
    sig = 0.62 * np.sin(phase) + 0.22 * np.sin(phase * 1.0027 + 0.7)
    sig += 0.18 * np.sin(2 * phase + 0.18 * np.sin(2 * np.pi * 3.1 * t))
    sig += 0.055 * np.sin(3 * phase) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.43 * t))
    sig *= 0.62 + 0.3 * np.sin(np.pi * np.minimum(t / duration, 1)) ** 0.7
    return fade(sig, 0.17, 0.34)

def suspended_tone(midi, duration):
    t, f = (axis(duration), hz(midi))
    phase = 2 * np.pi * f * t + 0.065 * np.sin(2 * np.pi * 0.53 * t)
    sig = np.sin(phase) + 0.3 * np.sin(phase * 2.001) + 0.12 * np.sin(phase * 3.002)
    sig *= 0.56 + 0.44 * np.sin(np.pi * t / duration) ** 2
    return fade(sig, 0.28, 0.45)

def depth_pulse(duration=0.68):
    t = axis(duration)
    phase = 2 * np.pi * (40 * t + 48 * 0.026 * (1 - np.exp(-t / 0.026)))
    sig = 0.84 * np.sin(phase) * np.exp(-t / 0.16)
    sig += 0.15 * np.sin(2 * phase) * np.exp(-t / 0.075)
    sig += 0.025 * noise(duration, 90, 650) * np.exp(-t / 0.026)
    return fade(sig, 0.009, 0.22)
