"""Готовые конфигурации обработки."""

from dataclasses import asdict, dataclass, fields
from typing import Any


@dataclass
class ProcessingConfig:
    # Базовые
    speed_factor: float = 1.008
    cutoff_freq: float = 16500.0
    filter_order: int = 6
    trim_silence: bool = True
    trim_padding: int = 1000
    silence_threshold_ratio: float = 0.005
    enable_lowpass: bool = True

    # Высота / время
    enable_pitch: bool = False
    pitch_cents: float = 0.0
    enable_tempo_resample: bool = False  # реальное изменение длины через ресэмпл

    # Ресэмплинг
    enable_resample_chain: bool = False
    resample_via_hz: int = 48000

    # EQ
    enable_eq: bool = False
    eq_low_shelf_db: float = 0.0
    eq_low_hz: float = 120.0
    eq_mid_db: float = 0.0
    eq_mid_hz: float = 3200.0
    eq_mid_q: float = 0.9
    eq_high_shelf_db: float = 0.0
    eq_high_hz: float = 9000.0

    # Динамика
    enable_compressor: bool = False
    comp_threshold_db: float = -20.0
    comp_ratio: float = 2.0
    comp_attack_ms: float = 12.0
    comp_release_ms: float = 120.0
    enable_limiter: bool = False
    limiter_ceiling_db: float = -0.5
    limiter_release_ms: float = 50.0

    # Пространство
    enable_reverb: bool = False
    reverb_mix: float = 0.06
    reverb_decay_ms: float = 40.0
    enable_stereo_width: bool = False
    stereo_width: float = 1.1
    enable_micro_pan: bool = False
    pan_offset: float = 0.03  # 0..1 сдвиг баланса L/R

    # Шум / экспорт
    enable_noise: bool = False
    noise_dbfs: float = -54.0
    enable_mp3_roundtrip: bool = False
    mp3_bitrate_kbps: int = 320

    # Финал
    normalize_output: bool = True
    target_peak_dbfs: float = -0.3

    def to_kwargs(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProcessingConfig":
        valid = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in valid})


def _p(**kwargs) -> dict[str, Any]:
    base = ProcessingConfig().to_kwargs()
    base.update(kwargs)
    return base


PRESETS: dict[str, dict[str, Any]] = {
    "recommended": {
        "label": "★ Рекомендуемая",
        "description": "Баланс маскировки и качества звука",
        "config": _p(
            speed_factor=1.008,
            cutoff_freq=16500,
            filter_order=6,
            trim_silence=True,
            enable_lowpass=True,
            enable_pitch=True,
            pitch_cents=28,
            enable_tempo_resample=True,
            enable_resample_chain=True,
            resample_via_hz=48000,
            enable_eq=True,
            eq_low_shelf_db=0.4,
            eq_mid_db=-0.9,
            eq_high_shelf_db=-1.3,
            enable_compressor=True,
            comp_threshold_db=-18,
            comp_ratio=2.3,
            enable_limiter=True,
            enable_reverb=True,
            reverb_mix=0.07,
            reverb_decay_ms=38,
            enable_stereo_width=True,
            stereo_width=1.12,
            enable_noise=True,
            noise_dbfs=-53,
            enable_mp3_roundtrip=True,
            mp3_bitrate_kbps=320,
            normalize_output=True,
            target_peak_dbfs=-0.3,
        ),
    },
    "light": {
        "label": "Лёгкая",
        "description": "Минимум обработки, почти без окраски",
        "config": _p(
            speed_factor=1.005,
            cutoff_freq=17000,
            filter_order=5,
            trim_silence=True,
            enable_lowpass=True,
            enable_pitch=True,
            pitch_cents=15,
            enable_tempo_resample=False,
            enable_resample_chain=False,
            enable_eq=False,
            enable_compressor=False,
            enable_limiter=True,
            limiter_ceiling_db=-1.0,
            enable_reverb=False,
            enable_stereo_width=False,
            enable_noise=False,
            enable_mp3_roundtrip=False,
            normalize_output=True,
        ),
    },
    "aggressive": {
        "label": "Агрессивная",
        "description": "Сильнее меняет отпечаток, возможны артефакты",
        "config": _p(
            speed_factor=1.012,
            cutoff_freq=15800,
            filter_order=7,
            trim_silence=True,
            enable_lowpass=True,
            enable_pitch=True,
            pitch_cents=45,
            enable_tempo_resample=True,
            enable_resample_chain=True,
            enable_eq=True,
            eq_low_shelf_db=0.8,
            eq_mid_db=-1.5,
            eq_high_shelf_db=-2.0,
            enable_compressor=True,
            comp_threshold_db=-16,
            comp_ratio=3.0,
            enable_limiter=True,
            enable_reverb=True,
            reverb_mix=0.1,
            enable_stereo_width=True,
            stereo_width=1.18,
            enable_micro_pan=True,
            pan_offset=0.05,
            enable_noise=True,
            noise_dbfs=-50,
            enable_mp3_roundtrip=True,
            mp3_bitrate_kbps=256,
            normalize_output=True,
        ),
    },
    "maximum": {
        "label": "Максимальная",
        "description": "Все этапы на усиленных настройках",
        "config": _p(
            speed_factor=1.015,
            cutoff_freq=15500,
            filter_order=8,
            trim_silence=True,
            enable_lowpass=True,
            enable_pitch=True,
            pitch_cents=55,
            enable_tempo_resample=True,
            enable_resample_chain=True,
            resample_via_hz=48000,
            enable_eq=True,
            eq_low_shelf_db=1.0,
            eq_mid_db=-2.0,
            eq_high_shelf_db=-2.5,
            enable_compressor=True,
            comp_threshold_db=-14,
            comp_ratio=3.5,
            enable_limiter=True,
            limiter_ceiling_db=-0.8,
            enable_reverb=True,
            reverb_mix=0.12,
            reverb_decay_ms=55,
            enable_stereo_width=True,
            stereo_width=1.22,
            enable_micro_pan=True,
            pan_offset=0.07,
            enable_noise=True,
            noise_dbfs=-48,
            enable_mp3_roundtrip=True,
            mp3_bitrate_kbps=256,
            normalize_output=True,
            target_peak_dbfs=-0.5,
        ),
    },
    "custom": {
        "label": "Своя (ручная)",
        "description": "Параметры задаёте вручную",
        "config": _p(),
    },
}

PRESET_ORDER = ["recommended", "light", "aggressive", "maximum", "custom"]


def get_preset_config(key: str) -> ProcessingConfig:
    if key not in PRESETS:
        key = "recommended"
    return ProcessingConfig.from_dict(PRESETS[key]["config"])
