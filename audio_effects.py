"""Отдельные аудио-эффекты (float32, -1..1)."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, iirpeak, lfilter, resample, resample_poly

from app_paths import find_ffmpeg, ffmpeg_available


def to_float32(data: np.ndarray) -> np.ndarray:
    if np.issubdtype(data.dtype, np.floating):
        out = data.astype(np.float32)
    elif data.dtype == np.int16:
        out = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        out = data.astype(np.float32) / 2147483648.0
    elif data.dtype == np.uint8:
        out = (data.astype(np.float32) - 128) / 128.0
    else:
        out = data.astype(np.float32)
    return np.clip(out, -1.0, 1.0)


def from_float32(data: np.ndarray, dtype) -> np.ndarray:
    data = np.clip(data, -1.0, 1.0)
    if dtype == np.int16:
        return (data * 32767.0).astype(np.int16)
    if dtype == np.int32:
        return (data * 2147483647.0).astype(np.int32)
    if dtype == np.uint8:
        return ((data + 1.0) * 127.5).astype(np.uint8)
    if np.issubdtype(dtype, np.floating):
        return data.astype(dtype)
    return (data * 32767.0).astype(np.int16)


def ensure_stereo(data: np.ndarray) -> np.ndarray:
    if data.ndim == 1:
        return np.column_stack([data, data])
    return data


def to_mono_shape(data: np.ndarray) -> np.ndarray:
    if data.ndim == 1:
        return data
    return data


def apply_channel(data: np.ndarray, fn) -> np.ndarray:
    if data.ndim == 1:
        return fn(data)
    out = np.zeros_like(data, dtype=np.float32)
    for ch in range(data.shape[1]):
        out[:, ch] = fn(data[:, ch])
    return out


def butter_lowpass(data: np.ndarray, cutoff: float, fs: int, order: int = 5) -> np.ndarray:
    nyq = 0.5 * fs
    wn = min(cutoff / nyq, 0.99)
    b, a = butter(order, wn, btype="low", analog=False)
    return apply_channel(data, lambda x: lfilter(b, a, x))


def pitch_shift_cents(data: np.ndarray, cents: float) -> np.ndarray:
    if abs(cents) < 0.01:
        return data
    factor = 2 ** (cents / 1200.0)
    n = data.shape[0]

    def _one(x: np.ndarray) -> np.ndarray:
        n2 = max(8, int(n / factor))
        y = resample(x, n2)
        return resample(y, n).astype(np.float32)

    return apply_channel(data, _one)


def tempo_resample(data: np.ndarray, speed_factor: float) -> np.ndarray:
    if abs(speed_factor - 1.0) < 1e-6:
        return data
    n_out = max(8, int(data.shape[0] / speed_factor))
    if data.ndim == 1:
        return resample(data, n_out).astype(np.float32)
    out = np.zeros((n_out, data.shape[1]), dtype=np.float32)
    for ch in range(data.shape[1]):
        out[:, ch] = resample(data[:, ch], n_out)
    return out


def resample_chain(data: np.ndarray, sr: int, via_hz: int = 48000) -> tuple[np.ndarray, int]:
    if sr == via_hz:
        return data, sr
    down_len = len(data)

    def _ch(x: np.ndarray) -> np.ndarray:
        up = resample_poly(x, via_hz, sr)
        down = resample_poly(up, sr, via_hz)
        if len(down) > down_len:
            down = down[:down_len]
        elif len(down) < down_len:
            down = np.pad(down, (0, down_len - len(down)))
        return down.astype(np.float32)

    if data.ndim == 1:
        return _ch(data), sr
    return np.column_stack([_ch(data[:, c]) for c in range(data.shape[1])]), sr


def apply_eq(
    data: np.ndarray,
    fs: int,
    *,
    low_shelf_db: float = 0.0,
    low_hz: float = 120.0,
    mid_db: float = 0.0,
    mid_hz: float = 3200.0,
    mid_q: float = 0.9,
    high_shelf_db: float = 0.0,
    high_hz: float = 9000.0,
) -> np.ndarray:
    out = data.copy()

    def filt(x):
        y = x.copy()
        if abs(low_shelf_db) >= 0.05:
            w0 = min(low_hz / (fs * 0.5), 0.95)
            b, a = butter(2, w0, btype="low")
            low = lfilter(b, a, y)
            y = y + low * (10 ** (low_shelf_db / 20.0) - 1.0)
        if abs(mid_db) >= 0.05:
            w0 = min(mid_hz / (fs * 0.5), 0.95)
            b, a = iirpeak(w0, mid_q)
            band = lfilter(b, a, y)
            y = y + band * (10 ** (mid_db / 20.0) - 1.0)
        if abs(high_shelf_db) >= 0.05:
            w0 = min(high_hz / (fs * 0.5), 0.95)
            b, a = butter(2, w0, btype="high")
            high = lfilter(b, a, y)
            y = y + high * (10 ** (high_shelf_db / 20.0) - 1.0)
        return y

    return apply_channel(out, filt)


def apply_compressor(
    data: np.ndarray,
    fs: int,
    threshold_db: float = -20.0,
    ratio: float = 2.0,
    attack_ms: float = 12.0,
    release_ms: float = 120.0,
) -> np.ndarray:
    thresh = 10 ** (threshold_db / 20.0)
    attack = max(1, int(fs * attack_ms / 1000.0))
    release = max(1, int(fs * release_ms / 1000.0))
    atk_coef = np.exp(-1.0 / attack)
    rel_coef = np.exp(-1.0 / release)

    def _one(x: np.ndarray) -> np.ndarray:
        env = 0.0
        out = np.zeros_like(x)
        for i, s in enumerate(x):
            level = abs(s)
            coef = atk_coef if level > env else rel_coef
            env = coef * env + (1 - coef) * level
            if env < 1e-8:
                out[i] = s
                continue
            if env <= thresh:
                out[i] = s
            else:
                over_db = 20 * np.log10(env / thresh)
                gain_db = over_db - over_db / ratio
                gain = 10 ** (-gain_db / 20.0)
                out[i] = s * gain
        return out

    return apply_channel(data, _one)


def apply_limiter(
    data: np.ndarray,
    fs: int,
    ceiling_db: float = -0.5,
    release_ms: float = 50.0,
) -> np.ndarray:
    ceiling = 10 ** (ceiling_db / 20.0)
    release = max(1, int(fs * release_ms / 1000.0))
    rel_coef = np.exp(-1.0 / release)

    def _one(x: np.ndarray) -> np.ndarray:
        gain = 1.0
        out = np.zeros_like(x)
        for i, s in enumerate(x):
            peak = abs(s) * gain
            if peak > ceiling:
                target_gain = ceiling / (abs(s) + 1e-12)
                gain = min(gain, target_gain)
            else:
                gain = gain * rel_coef + (1 - rel_coef) * 1.0
                gain = min(gain, 1.0)
            out[i] = s * gain
        return np.clip(out, -ceiling, ceiling)

    return apply_channel(data, _one)


def apply_reverb(data: np.ndarray, fs: int, mix: float = 0.06, decay_ms: float = 40.0) -> np.ndarray:
    mix = float(np.clip(mix, 0.0, 0.35))
    ir_len = max(32, int(fs * decay_ms / 1000.0))
    t = np.linspace(0, 1, ir_len)
    ir = np.exp(-6 * t) * np.random.randn(ir_len).astype(np.float32) * 0.02
    ir[0] = 1.0

    def _one(x: np.ndarray) -> np.ndarray:
        wet = np.convolve(x, ir, mode="full")[: len(x)]
        return (1 - mix) * x + mix * wet

    return apply_channel(data, _one)


def apply_stereo_width(data: np.ndarray, width: float = 1.1) -> np.ndarray:
    if data.ndim == 1:
        return data
    L = data[:, 0].copy()
    R = data[:, 1].copy()
    mid = (L + R) * 0.5
    side = (L - R) * 0.5 * width
    out = np.column_stack([mid + side, mid - side])
    return out.astype(np.float32)


def apply_micro_pan(data: np.ndarray, offset: float = 0.03) -> np.ndarray:
    if data.ndim == 1:
        return data
    offset = float(np.clip(offset, 0.0, 0.25))
    L_gain = 1.0 - offset
    R_gain = 1.0 + offset
    out = data.copy()
    out[:, 0] *= L_gain
    out[:, 1] *= R_gain
    mx = np.max(np.abs(out)) + 1e-9
    if mx > 1.0:
        out /= mx
    return out


def apply_noise(data: np.ndarray, noise_dbfs: float = -54.0) -> np.ndarray:
    amp = 10 ** (noise_dbfs / 20.0)
    rng = np.random.default_rng()
    noise = rng.normal(0, amp, data.shape).astype(np.float32)
    return np.clip(data + noise, -1.0, 1.0)


def normalize_peak(data: np.ndarray, target_dbfs: float = -0.3) -> np.ndarray:
    peak = np.max(np.abs(data))
    if peak < 1e-9:
        return data
    target = 10 ** (target_dbfs / 20.0)
    return (data * (target / peak)).astype(np.float32)


def mp3_roundtrip(data: np.ndarray, sr: int, bitrate_kbps: int = 320) -> tuple[np.ndarray, bool]:
    """WAV -> MP3 -> WAV через ffmpeg. Возвращает (audio, success)."""
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        return data, False

    with tempfile.TemporaryDirectory() as tmp:
        wav_in = Path(tmp) / "in.wav"
        mp3 = Path(tmp) / "mid.mp3"
        wav_out = Path(tmp) / "out.wav"
        wavfile.write(str(wav_in), sr, from_float32(data, np.int16))
        br = f"{bitrate_kbps}k"
        cmd1 = [
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(wav_in), "-b:a", br, str(mp3),
        ]
        cmd2 = [
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(mp3), str(wav_out),
        ]
        try:
            subprocess.run(cmd1, check=True, capture_output=True)
            subprocess.run(cmd2, check=True, capture_output=True)
            _, out = wavfile.read(str(wav_out))
            out = to_float32(out)
            # выровнять длину
            if len(out) > len(data):
                out = out[: len(data)]
            elif len(out) < len(data):
                if out.ndim == 1:
                    out = np.pad(out, (0, len(data) - len(out)))
                else:
                    pad = len(data) - len(out)
                    out = np.vstack([out, np.zeros((pad, out.shape[1]), dtype=np.float32)])
            return out.astype(np.float32), True
        except (subprocess.CalledProcessError, OSError):
            return data, False


def trim_silence(
    data: np.ndarray,
    threshold_ratio: float = 0.005,
    padding: int = 1000,
) -> np.ndarray:
    if data.ndim > 1:
        amplitude = np.max(np.abs(data), axis=1)
    else:
        amplitude = np.abs(data)
    peak = np.max(amplitude)
    if peak <= 0:
        return data
    threshold = threshold_ratio * peak
    idx = np.where(amplitude > threshold)[0]
    if len(idx) == 0:
        return data
    start = max(0, idx[0] - padding)
    end = min(len(data), idx[-1] + padding)
    return data[start:end]
