"""Полный конвейер обработки WAV."""

import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.io import wavfile

from app_paths import ffmpeg_available
from audio_effects import (
    apply_compressor,
    apply_eq,
    apply_limiter,
    apply_micro_pan,
    apply_noise,
    apply_reverb,
    apply_stereo_width,
    butter_lowpass,
    from_float32,
    mp3_roundtrip,
    normalize_peak,
    pitch_shift_cents,
    resample_chain,
    tempo_resample,
    to_float32,
    trim_silence,
)
from i18n import t
from presets import ProcessingConfig, get_preset_config


def process_audio(
    input_path: str,
    output_path: str,
    config: ProcessingConfig | None = None,
) -> str:
    cfg = config or ProcessingConfig()
    sample_rate, raw = wavfile.read(input_path)
    original_dtype = raw.dtype
    data = to_float32(raw)
    steps: list[str] = []

    if cfg.trim_silence:
        data = trim_silence(
            data, cfg.silence_threshold_ratio, cfg.trim_padding
        )
        steps.append(t("step.trim"))

    if cfg.enable_tempo_resample and abs(cfg.speed_factor - 1.0) > 1e-6:
        data = tempo_resample(data, cfg.speed_factor)
        steps.append(t("step.tempo", factor=cfg.speed_factor))

    if cfg.enable_pitch and abs(cfg.pitch_cents) > 0.01:
        data = pitch_shift_cents(data, cfg.pitch_cents)
        steps.append(t("step.pitch", cents=cfg.pitch_cents))

    if cfg.enable_resample_chain:
        data, sample_rate = resample_chain(data, sample_rate, cfg.resample_via_hz)
        steps.append(t("step.resample", hz=cfg.resample_via_hz))

    if cfg.enable_eq:
        data = apply_eq(
            data,
            sample_rate,
            low_shelf_db=cfg.eq_low_shelf_db,
            low_hz=cfg.eq_low_hz,
            mid_db=cfg.eq_mid_db,
            mid_hz=cfg.eq_mid_hz,
            mid_q=cfg.eq_mid_q,
            high_shelf_db=cfg.eq_high_shelf_db,
            high_hz=cfg.eq_high_hz,
        )
        steps.append(t("step.eq"))

    filter_fs = int(sample_rate * cfg.speed_factor)
    if cfg.enable_lowpass:
        data = butter_lowpass(
            data, cfg.cutoff_freq, filter_fs, order=cfg.filter_order
        )
        steps.append(t("step.lowpass", freq=cfg.cutoff_freq))

    if cfg.enable_compressor:
        data = apply_compressor(
            data,
            sample_rate,
            cfg.comp_threshold_db,
            cfg.comp_ratio,
            cfg.comp_attack_ms,
            cfg.comp_release_ms,
        )
        steps.append(t("step.compress"))

    if cfg.enable_limiter:
        data = apply_limiter(
            data, sample_rate, cfg.limiter_ceiling_db, cfg.limiter_release_ms
        )
        steps.append(t("step.limiter"))

    if cfg.enable_reverb:
        data = apply_reverb(
            data, sample_rate, cfg.reverb_mix, cfg.reverb_decay_ms
        )
        steps.append(t("step.reverb"))

    if cfg.enable_stereo_width:
        data = apply_stereo_width(data, cfg.stereo_width)
        steps.append(t("step.stereo"))

    if cfg.enable_micro_pan:
        data = apply_micro_pan(data, cfg.pan_offset)
        steps.append(t("step.pan"))

    if cfg.enable_noise:
        data = apply_noise(data, cfg.noise_dbfs)
        steps.append(t("step.noise"))

    if cfg.enable_mp3_roundtrip:
        data, ok = mp3_roundtrip(data, sample_rate, cfg.mp3_bitrate_kbps)
        if ok:
            steps.append(t("step.mp3", bitrate=cfg.mp3_bitrate_kbps))
        else:
            steps.append(t("step.mp3_skip"))

    if cfg.normalize_output:
        data = normalize_peak(data, cfg.target_peak_dbfs)
        steps.append(t("step.normalize"))

    out_pcm = from_float32(data, original_dtype)
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    wavfile.write(output_path, sample_rate, out_pcm)
    return "; ".join(steps) if steps else t("step.saved")


# обратная совместимость
def bypass_ai_detector(input_path: str, output_path: str, **kwargs) -> str:
    cfg = ProcessingConfig.from_dict(kwargs) if kwargs else get_preset_config("light")
    return process_audio(input_path, output_path, cfg)


def process_batch(
    source_paths: list[str],
    output_folder: str,
    *,
    output_prefix: str = "cleaned_",
    config: ProcessingConfig | None = None,
    on_progress=None,
    parallel: bool = False,
    max_workers: int = 4,
    **kwargs,
) -> list[tuple[str, bool, str]]:
    if config is None:
        config = ProcessingConfig.from_dict(kwargs) if kwargs else get_preset_config("recommended")

    os.makedirs(output_folder, exist_ok=True)
    wav_files = [p for p in source_paths if Path(p).suffix.lower() == ".wav"]
    total = len(wav_files)
    if total == 0:
        return []

    workers = max(1, min(max_workers, total))

    def _process_one(in_file: str) -> tuple[str, bool, str]:
        name = os.path.basename(in_file)
        out_file = os.path.join(output_folder, f"{output_prefix}{name}")
        try:
            detail = process_audio(in_file, out_file, config)
            msg = t("step.done", detail=detail)
            return name, True, msg
        except Exception as exc:
            return name, False, t("step.error", msg=str(exc))

    results: list[tuple[str, bool, str] | None] = [None] * total
    file_index = {f: i for i, f in enumerate(wav_files)}

    if not parallel or workers == 1:
        for i, in_file in enumerate(wav_files, start=1):
            name, ok, msg = _process_one(in_file)
            results[i - 1] = (name, ok, msg)
            if on_progress:
                on_progress(i, total, name, msg)
        return [r for r in results if r is not None]

    lock = threading.Lock()
    done_count = 0

    def _run_and_report(in_file: str) -> None:
        nonlocal done_count
        name, ok, msg = _process_one(in_file)
        idx = file_index[in_file]
        results[idx] = (name, ok, msg)
        with lock:
            done_count += 1
            cur = done_count
        if on_progress:
            on_progress(cur, total, name, msg)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_run_and_report, f) for f in wav_files]
        for fut in as_completed(futures):
            fut.result()

    return [r for r in results if r is not None]


def collect_wav_files(path: str) -> list[str]:
    p = Path(path)
    if p.is_file() and p.suffix.lower() == ".wav":
        return [str(p.resolve())]
    if p.is_dir():
        return sorted(str(f.resolve()) for f in p.glob("*.wav"))
    return []
