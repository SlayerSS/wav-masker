"""Подсказки к настройкам: влияние на звук и риск для качества."""

from __future__ import annotations

from i18n import get_language, t
from setting_hints_en import HINTS_EN

# risk: safe | moderate | risky
HINTS_RU: dict[str, dict[str, str]] = {
    "trim_silence": {
        "effect": "Убирает тишину в начале и конце. Трек становится короче, без «пустых» хвостов.",
        "quality": "Низкий риск. Может срезать очень тихие атаки (фейд-ин), если порог слишком высокий.",
        "risk": "safe",
    },
    "enable_tempo_resample": {
        "effect": "Чуть ускоряет или замедляет трек (меняется длительность). Меняется «сетка» сэмплов.",
        "quality": "Средний риск. Заметно при значениях выше ~1.5%. На 1% обычно почти не слышно.",
        "risk": "moderate",
    },
    "speed_factor": {
        "effect": "Сила изменения темпа. 1.008 ~ +0.8% быстрее — чуть выше тон и короче трек.",
        "quality": "До 1.01 — низкий риск. Выше 1.015 — возможны артефакты и ощущение «ускоренной» записи.",
        "risk": "moderate",
    },
    "enable_lowpass": {
        "effect": "Срезает верхние частоты (яркость, «воздух», шипение). Звук мягче и темнее.",
        "quality": "Средний риск. Срез ниже 15 кГц заметен на тарелках и «с» в вокале.",
        "risk": "moderate",
    },
    "cutoff_freq": {
        "effect": "Частота среза НЧ-фильтра. Ниже — меньше верхов, больше «телефонного» оттенка.",
        "quality": "16–17 кГц — умеренно. Ниже 14 кГц — высокий риск потери детализации.",
        "risk": "moderate",
    },
    "filter_order": {
        "effect": "Крутизна фильтра. Выше порядок — резче срез верхов, сильнее фазовые сдвиги.",
        "quality": "5–7 обычно достаточно. 9–10 — выше риск «звона» и неестественности на верхах.",
        "risk": "moderate",
    },
    "enable_pitch": {
        "effect": "Сдвигает высоту тона без смены длины (центы). Меняет тембр голоса и инструментов.",
        "quality": "До 30 cent — низкий риск. 50+ — средний (легкий «хор»). Сильный сдвиг — артефакты.",
        "risk": "moderate",
    },
    "pitch_cents": {
        "effect": "Величина сдвига в центах (100 cent = полутон). Плюс — выше, минус — ниже.",
        "quality": "20–40 cent — обычно безопасно. Больше 50 — возможен «пластиковый» вокал.",
        "risk": "moderate",
    },
    "enable_resample_chain": {
        "effect": "Пересчёт 44.1→48→44.1 кГц. Слегка размывает микродетали и меняет цифровой отпечаток.",
        "quality": "Низкий–средний риск. На слух почти незаметно, но не для аудиофильского мастера.",
        "risk": "moderate",
    },
    "resample_via_hz": {
        "effect": "Промежуточная частота в цепочке. 48 кГц — стандарт; 96 — мягче, но дольше обработка.",
        "quality": "Низкий риск при 48 кГц. Экстремальные значения мало влияют при короткой цепочке.",
        "risk": "safe",
    },
    "enable_eq": {
        "effect": "Тональная коррекция: низы, середина, верха. Меняет баланс и «характер» микса.",
        "quality": "±1 dB — низкий риск. Сильные срезы (−2 dB и более) — средний, меняется окраска.",
        "risk": "moderate",
    },
    "eq_low_shelf_db": {
        "effect": "Усиление или ослабление баса и низа. Плюс — плотнее, минус — суше.",
        "quality": "До ±1 dB — безопасно. +2 dB и выше — риск перегруза на колонках.",
        "risk": "moderate",
    },
    "eq_mid_db": {
        "effect": "Середина (вокал, гитары). Минус — дальше/мягче, плюс — ближе и чётче.",
        "quality": "Умеренные значения безопасны. Сильный минус — «полый» звук.",
        "risk": "moderate",
    },
    "eq_high_shelf_db": {
        "effect": "Верха: яркость и чёткость. Минус — теплее, плюс — жёстче и «цифровее».",
        "quality": "Сильный минус вместе с НЧ-фильтром — высокий риск «тусклого» трека.",
        "risk": "moderate",
    },
    "enable_compressor": {
        "effect": "Сжимает динамику: тихое громче, пики ограничены. Трек кажется плотнее и громче.",
        "quality": "Ratio 2–3 — умеренно. Высокий ratio и низкий порог — «пампинг», усталость слуха.",
        "risk": "moderate",
    },
    "comp_threshold_db": {
        "effect": "С какого уровня начинается сжатие. Ниже порог (ближе к 0) — сжимается больше сигнала.",
        "quality": "−18…−22 dB — типично для мастера. Ниже −14 — высокий риск пересжатия.",
        "risk": "moderate",
    },
    "comp_ratio": {
        "effect": "Сила сжатия. 2:1 — мягко, 4:1 и выше — агрессивно, меньше перепадов.",
        "quality": "До 3 — средний риск. Выше 4 — заметное «кирпичное» звучание.",
        "risk": "moderate",
    },
    "enable_limiter": {
        "effect": "Ограничивает максимальную громкость, убирает пики. Защита от клиппинга.",
        "quality": "Потолок −0.5…−1 dB — низкий риск. 0 dB и перегон — искажения.",
        "risk": "safe",
    },
    "limiter_ceiling_db": {
        "effect": "Максимальный уровень после лимитера. Ближе к 0 — громче, но опаснее для клиппинга.",
        "quality": "−0.3…−1 dB — безопасно для стриминга. 0 dB — высокий риск искажений на пиках.",
        "risk": "moderate",
    },
    "enable_reverb": {
        "effect": "Добавляет лёгкое эхо/комнату. Звук «дальше» и объёмнее.",
        "quality": "Малый mix (до 0.08) — низкий риск. Выше 0.12 — заметная «ванна», мутность.",
        "risk": "moderate",
    },
    "reverb_mix": {
        "effect": "Доля обработанного (мокрого) сигнала. 0 — выкл, 0.1 — лёгкая комната.",
        "quality": "До 0.08 — обычно безопасно. 0.15+ — средний/высокий риск размытости.",
        "risk": "moderate",
    },
    "enable_stereo_width": {
        "effect": "Расширяет стереобазу (стороны шире, центр тоньше). Больше «объёма» в наушниках.",
        "quality": "1.05–1.15 — умеренно. 1.25+ — фазовые проблемы в моно, «пустой» центр.",
        "risk": "moderate",
    },
    "stereo_width": {
        "effect": "Степень расширения. 1.0 — без изменений, выше — шире панорама.",
        "quality": "До 1.12 — низкий–средний риск. Выше 1.2 — проверьте трек в моно.",
        "risk": "moderate",
    },
    "enable_micro_pan": {
        "effect": "Слегка сдвигает баланс L/R. Меняет стерео-картину без сильного расширения.",
        "quality": "Малый сдвиг — низкий риск. Большой — странная панорама в наушниках.",
        "risk": "safe",
    },
    "pan_offset": {
        "effect": "Величина сдвига панорамы между каналами.",
        "quality": "До 0.05 — безопасно. Выше 0.08 — средний риск дисбаланса.",
        "risk": "moderate",
    },
    "enable_noise": {
        "effect": "Добавляет очень тихий шум/дизер. Меняет «цифровую чистоту» сигнала.",
        "quality": "−53 dBFS и тише — почти неслышно. −48 и громче — средний риск шипа в тишине.",
        "risk": "moderate",
    },
    "noise_dbfs": {
        "effect": "Громкость фонового шума. Чем ближе к 0, тем заметнее.",
        "quality": "−54…−56 — низкий риск. Выше −50 — может слышаться между фразами.",
        "risk": "moderate",
    },
    "enable_mp3_roundtrip": {
        "effect": "Кодирует в MP3 и обратно в WAV. Теряются мелкие детали, появляется «цифровая» окраска.",
        "quality": "320 kbps — средний риск. 256 и ниже — высокий риск артефактов и потери верхов.",
        "risk": "risky",
    },
    "mp3_bitrate_kbps": {
        "effect": "Качество MP3 в промежуточном этапе. Выше — лучше сохраняются детали.",
        "quality": "320 — приемлемо для маскировки. 128 — высокий риск для музыки.",
        "risk": "moderate",
    },
    "normalize_output": {
        "effect": "Поднимает общую громкость до целевого пика. Трек звучит громче и ровнее по уровню.",
        "quality": "Низкий риск, если не было перегруза раньше. Усиливает уже существующие артефакты.",
        "risk": "safe",
    },
    "target_peak_dbfs": {
        "effect": "Целевая громкость пика. −0.3 dB — почти максимум, −1 dB — запас для кодеков.",
        "quality": "−0.3…−1 dB — безопасно. 0 dB — риск клиппинга при конвертации.",
        "risk": "safe",
    },
}

SETTING_HINTS = HINTS_RU

SETTING_I18N: dict[str, str] = {
    "trim_silence": "setting.trim_silence",
    "enable_tempo_resample": "setting.enable_tempo",
    "speed_factor": "setting.speed_factor",
    "enable_lowpass": "setting.enable_lowpass",
    "cutoff_freq": "setting.cutoff_freq",
    "filter_order": "setting.filter_order",
    "enable_pitch": "setting.enable_pitch",
    "pitch_cents": "setting.pitch_cents",
    "enable_resample_chain": "setting.resample_chain",
    "resample_via_hz": "setting.resample_hz",
    "enable_eq": "setting.enable_eq",
    "eq_low_shelf_db": "setting.eq_low",
    "eq_mid_db": "setting.eq_mid",
    "eq_high_shelf_db": "setting.eq_high",
    "enable_compressor": "setting.enable_comp",
    "comp_threshold_db": "setting.comp_thresh",
    "comp_ratio": "setting.comp_ratio",
    "enable_limiter": "setting.enable_limiter",
    "limiter_ceiling_db": "setting.limiter_ceil",
    "enable_reverb": "setting.enable_reverb",
    "reverb_mix": "setting.reverb_mix",
    "enable_stereo_width": "setting.enable_stereo",
    "stereo_width": "setting.stereo_width",
    "enable_micro_pan": "setting.enable_pan",
    "pan_offset": "setting.pan_offset",
    "enable_noise": "setting.enable_noise",
    "noise_dbfs": "setting.noise_dbfs",
    "enable_mp3_roundtrip": "setting.enable_mp3",
    "mp3_bitrate_kbps": "setting.mp3_bitrate",
    "normalize_output": "setting.normalize",
    "target_peak_dbfs": "setting.target_peak",
}


def _hints_for_lang() -> dict[str, dict[str, str]]:
    return HINTS_EN if get_language() == "en" else HINTS_RU


def get_preset_hint() -> str:
    return t("hints.preset_body")


def setting_title(key: str) -> str:
    i18n_key = SETTING_I18N.get(key)
    return t(i18n_key) if i18n_key else key


def format_hint(key: str) -> str:
    h = _hints_for_lang()[key]
    risk_key = h.get("risk", "moderate")
    risk = t(f"risk.{risk_key}")
    return (
        f"{t('hint.header_effect')}:\n{h['effect']}\n\n"
        f"{t('hint.header_quality')}:\n{h['quality']}\n\n({risk})"
    )


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _interp_zones(v: float, points: list[tuple[float, float]]) -> float:
    """Линейная интерполяция danger по точкам (значение, риск 0..1)."""
    if not points:
        return 0.0
    if v <= points[0][0]:
        return points[0][1]
    if v >= points[-1][0]:
        return points[-1][1]
    for i in range(len(points) - 1):
        v0, d0 = points[i]
        v1, d1 = points[i + 1]
        if v0 <= v <= v1:
            if v1 == v0:
                return d1
            t_ = (v - v0) / (v1 - v0)
            return d0 + t_ * (d1 - d0)
    return points[-1][1]


# Пороги согласованы с текстами подсказок (quality).
_SCALE_ZONES: dict[str, list[tuple[float, float]]] = {
    "speed_factor": [(1.0, 0.0), (1.01, 0.25), (1.015, 0.7), (1.02, 1.0)],
    "cutoff_freq": [(14000, 1.0), (15000, 0.8), (16000, 0.55), (17000, 0.3), (19000, 0.0)],
    "filter_order": [(2, 0.35), (5, 0.0), (7, 0.0), (8, 0.35), (9, 0.7), (10, 1.0)],
    "pitch_cents": [(0, 0.0), (30, 0.2), (50, 0.6), (80, 1.0)],
    "resample_via_hz": [(44100, 0.15), (48000, 0.0), (96000, 0.2)],
    "comp_threshold_db": [(-30, 0.0), (-22, 0.1), (-18, 0.35), (-14, 0.65), (-8, 1.0)],
    "comp_ratio": [(1.5, 0.0), (2.5, 0.25), (3.0, 0.5), (4.0, 0.85), (5.0, 1.0)],
    "limiter_ceiling_db": [(-3, 0.0), (-1.0, 0.0), (-0.5, 0.1), (-0.3, 0.2), (-0.1, 0.75), (0, 1.0)],
    "target_peak_dbfs": [(-3, 0.0), (-1.0, 0.0), (-0.5, 0.1), (-0.3, 0.2), (-0.1, 0.75), (0, 1.0)],
    "reverb_mix": [(0, 0.0), (0.08, 0.25), (0.12, 0.6), (0.15, 0.8), (0.2, 1.0)],
    "stereo_width": [(1.0, 0.0), (1.05, 0.2), (1.12, 0.45), (1.2, 0.75), (1.3, 1.0)],
    "pan_offset": [(0, 0.0), (0.05, 0.25), (0.08, 0.6), (0.12, 1.0)],
    "noise_dbfs": [(-60, 0.0), (-56, 0.15), (-54, 0.25), (-50, 0.6), (-45, 1.0)],
    "mp3_bitrate_kbps": [(128, 1.0), (192, 0.75), (256, 0.5), (320, 0.25)],
}


def _eq_danger(v: float, lo: float, hi: float) -> float:
    """±1 dB безопасно, ±2 dB умеренно, дальше — выше риск."""
    a = abs(v)
    if a <= 1.0:
        return _clamp01(a * 0.15)
    if a <= 2.0:
        return _clamp01(0.15 + (a - 1.0) * 0.45)
    cap = max(abs(lo), abs(hi), 2.01)
    return _clamp01(0.6 + (a - 2.0) / (cap - 2.0) * 0.4)


def scale_danger(key: str, value: float, lo: float, hi: float) -> float:
    """0 = безопасно, 1 = высокий риск искажений для текущего значения ползунка."""
    v = float(value)
    if key in _SCALE_ZONES:
        return _clamp01(_interp_zones(v, _SCALE_ZONES[key]))
    if key in ("eq_low_shelf_db", "eq_mid_db", "eq_high_shelf_db"):
        return _eq_danger(v, lo, hi)
    return 0.0


def danger_color(danger: float) -> str:
    """Зелёный → жёлтый → красный."""
    d = _clamp01(danger)
    if d <= 0.5:
        t_ = d * 2
        r = int(39 + (243 - 39) * t_)
        g = int(174 + (156 - 174) * t_)
        b = int(96 + (18 - 96) * t_)
    else:
        t_ = (d - 0.5) * 2
        r = int(243 + (192 - 243) * t_)
        g = int(156 + (57 - 156) * t_)
        b = int(18 + (43 - 18) * t_)
    return f"#{r:02x}{g:02x}{b:02x}"
