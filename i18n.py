"""Локализация интерфейса (ru / en)."""

from __future__ import annotations

import json
from pathlib import Path

from app_paths import get_app_root

_LANG = "ru"

_STRINGS: dict[str, dict[str, str]] = {
    "ru": {
        "app.title": "WAV Masker Pro — обработка WAV",
        "menu.language": "Язык",
        "menu.lang.ru": "Русский",
        "menu.lang.en": "English",
        "menu.help": "Справка",
        "menu.hints": "Справка по настройкам",
        "menu.about": "О программе",
        "hints.title": "Подсказки к настройкам",
        "hints.presets": "Пресеты",
        "about.title": "О программе",
        "about.author": "Автор",
        "about.credit": "Сделано в Ноябрьске — там всегда зима",
        "about.repo": "Репозиторий",
        "about.fork": "Форки должны содержать ссылку на оригинал",
        "files.title": "Файлы",
        "files.source": "Источник (.wav / папка):",
        "files.output": "Результат:",
        "files.prefix": "Префикс:",
        "btn.file": "Файл",
        "btn.folder": "Папка",
        "config.title": "Конфигурация",
        "log.title": "Журнал",
        "btn.process": "Обработать",
        "setting.parallel": "Параллельная обработка файлов",
        "log.parallel": "Потоков: {n}",
        "status.ready": "Готово",
        "status.processing": "Обработка…",
        "section.basic": "Базовая обработка",
        "section.pitch": "Высота и ресэмплинг",
        "section.eq": "EQ",
        "section.dynamics": "Динамика",
        "section.space": "Пространство",
        "section.export": "Экспорт и финал",
        "setting.trim_silence": "Обрезать тишину",
        "setting.enable_tempo": "Изменить темп (ресэмпл)",
        "setting.speed_factor": "Коэфф. скорости",
        "setting.enable_lowpass": "НЧ-фильтр (срез верхов)",
        "setting.cutoff_freq": "Срез, Гц",
        "setting.filter_order": "Порядок фильтра",
        "setting.enable_pitch": "Сдвиг высоты (pitch)",
        "setting.pitch_cents": "Сдвиг, cent",
        "setting.resample_chain": "Цепочка 44.1→48→44.1",
        "setting.resample_hz": "Промежуточная частота",
        "setting.enable_eq": "Включить EQ",
        "setting.eq_low": "Низы, dB",
        "setting.eq_mid": "Середина, dB",
        "setting.eq_high": "Верха, dB",
        "setting.enable_comp": "Компрессор",
        "setting.comp_thresh": "Порог, dB",
        "setting.comp_ratio": "Ratio",
        "setting.enable_limiter": "Лимитер",
        "setting.limiter_ceil": "Потолок, dB",
        "setting.enable_reverb": "Лёгкий reverb",
        "setting.reverb_mix": "Mix reverb",
        "setting.enable_stereo": "Стерео-ширина",
        "setting.stereo_width": "Ширина",
        "setting.enable_pan": "Микросдвиг панорамы",
        "setting.pan_offset": "Сдвиг L/R",
        "setting.enable_noise": "Фоновый дизер/шум",
        "setting.noise_dbfs": "Уровень шума, dBFS",
        "setting.enable_mp3": "Проход WAV→MP3→WAV (ffmpeg рядом с exe или в PATH)",
        "setting.mp3_bitrate": "Битрейт MP3",
        "setting.normalize": "Нормализация пика",
        "setting.target_peak": "Целевой пик, dBFS",
        "preset.recommended.label": "★ Рекомендуемая",
        "preset.recommended.desc": "Баланс обработки и качества звука",
        "preset.light.label": "Лёгкая",
        "preset.light.desc": "Минимум обработки, почти без окраски",
        "preset.aggressive.label": "Агрессивная",
        "preset.aggressive.desc": "Сильнее меняет звук, возможны артефакты",
        "preset.maximum.label": "Максимальная",
        "preset.maximum.desc": "Все этапы на усиленных настройках",
        "preset.custom.label": "Своя (ручная)",
        "preset.custom.desc": "Параметры задаёте вручную",
        "dlg.warn": "Внимание",
        "dlg.no_source": "Укажите файл или папку с .wav",
        "dlg.no_output": "Укажите папку для результатов",
        "dlg.no_files": "Нет файлов",
        "dlg.no_wav": "Не найдено .wav",
        "dlg.done": "Готово",
        "dlg.ok_fail": "Успешно: {ok}, ошибок: {fail}",
        "dlg.ok_done": "Обработано: {ok}\n{path}",
        "log.ffmpeg_missing": "ffmpeg не найден — этап MP3 будет пропущен",
        "log.ffmpeg_local": "  Вариант 1: ffmpeg.exe рядом с {anchor}",
        "log.ffmpeg_folder": "  Папка: {folder}",
        "log.ffmpeg_path": "  Вариант 2: ffmpeg в системном PATH",
        "log.ffmpeg_download": "  Скачать: {url}",
        "log.start": "--- Старт ({preset}) ---",
        "log.finish": "--- Готово: {path} ---",
        "status.ok": "OK: {ok}, ошибок: {fail}",
        "ffmpeg.title": "ffmpeg не найден",
        "ffmpeg.header": "ffmpeg.exe не найден",
        "ffmpeg.download_hdr": "Скачать для Windows:",
        "ffmpeg.path_hint": "Рекомендуемый путь (рядом с {anchor}):",
        "ffmpeg.btn.gyan": "Скачать — gyan.dev",
        "ffmpeg.btn.github": "Скачать — GitHub",
        "ffmpeg.btn.close": "Закрыть",
        "ffmpeg.skip_mp3": "Этап MP3 будет пропущен.\n\nПродолжить обработку без MP3?",
        "ffmpeg.status_local": "ffmpeg: {name} (рядом с {anchor})",
        "ffmpeg.status_path": "ffmpeg: системный PATH ({path})",
        "hint.header_effect": "Как меняет звук",
        "hint.header_quality": "Качество",
        "risk.safe": "Низкий риск для качества",
        "risk.moderate": "Средний риск — слушайте результат",
        "risk.risky": "Высокий риск — только если нужен сильный эффект",
        "hints.preset_body": (
            "Готовый набор настроек.\n\n"
            "★ Рекомендуемая — баланс маскировки и качества.\n"
            "Лёгкая — минимум окраски.\n"
            "Агрессивная / Максимальная — сильнее меняет звук, выше риск артефактов."
        ),
        "ffmpeg.body": (
            "Для этапа «WAV → MP3 → WAV» нужен ffmpeg.\n\n"
            "Где ищет программа:\n"
            "1) {ffmpeg_name} рядом с {anchor}:\n   {folder}\n"
            "2) ffmpeg или ffmpeg.exe в системном PATH\n\n"
            "Как установить локально:\n"
            "• Скачайте {direct_hint}\n"
            "• Скопируйте {ffmpeg_name} в папку выше\n"
            "• Или добавьте ffmpeg в PATH Windows\n"
            "• Перезапустите программу\n\n"
            "Без ffmpeg остальная обработка работает;\n"
            "шаг MP3 будет пропущен."
        ),
        "ffmpeg.direct_hint": "ffmpeg-release-essentials.zip → папка bin → ffmpeg.exe",
        "ffmpeg.download_urls": "• {url_primary}\n• {url_alt}",
        "step.trim": "обрезка тишины",
        "step.tempo": "темп ×{factor:.4f}",
        "step.pitch": "pitch {cents:+.0f} cent",
        "step.resample": "ресэмпл {hz} Гц",
        "step.eq": "EQ",
        "step.lowpass": "НЧ {freq:.0f} Гц",
        "step.compress": "компрессия",
        "step.limiter": "лимитер",
        "step.reverb": "reverb",
        "step.stereo": "стерео-ширина",
        "step.pan": "микропан",
        "step.noise": "дизер/шум",
        "step.mp3": "MP3 {bitrate}k",
        "step.mp3_skip": "MP3 пропущен (нет ffmpeg)",
        "step.normalize": "нормализация",
        "step.saved": "сохранено",
        "step.done": "Готово: {detail}",
        "step.error": "Ошибка: {msg}",
    },
    "en": {
        "app.title": "WAV Masker Pro — WAV processing",
        "menu.language": "Language",
        "menu.lang.ru": "Русский",
        "menu.lang.en": "English",
        "menu.help": "Help",
        "menu.hints": "Settings guide",
        "menu.about": "About",
        "hints.title": "Settings guide",
        "hints.presets": "Presets",
        "about.title": "About",
        "about.author": "Author",
        "about.credit": "Made in Noyabrsk — always winter",
        "about.repo": "Repository",
        "about.fork": "Forks must link to the original repository",
        "files.title": "Files",
        "files.source": "Source (.wav / folder):",
        "files.output": "Output:",
        "files.prefix": "Prefix:",
        "btn.file": "File",
        "btn.folder": "Folder",
        "config.title": "Configuration",
        "log.title": "Log",
        "btn.process": "Process",
        "setting.parallel": "Parallel file processing",
        "log.parallel": "Workers: {n}",
        "status.ready": "Ready",
        "status.processing": "Processing…",
        "section.basic": "Basic processing",
        "section.pitch": "Pitch & resampling",
        "section.eq": "EQ",
        "section.dynamics": "Dynamics",
        "section.space": "Space",
        "section.export": "Export & final",
        "setting.trim_silence": "Trim silence",
        "setting.enable_tempo": "Change tempo (resample)",
        "setting.speed_factor": "Speed factor",
        "setting.enable_lowpass": "Low-pass filter",
        "setting.cutoff_freq": "Cutoff, Hz",
        "setting.filter_order": "Filter order",
        "setting.enable_pitch": "Pitch shift",
        "setting.pitch_cents": "Shift, cents",
        "setting.resample_chain": "Chain 44.1→48→44.1",
        "setting.resample_hz": "Intermediate rate",
        "setting.enable_eq": "Enable EQ",
        "setting.eq_low": "Low, dB",
        "setting.eq_mid": "Mid, dB",
        "setting.eq_high": "High, dB",
        "setting.enable_comp": "Compressor",
        "setting.comp_thresh": "Threshold, dB",
        "setting.comp_ratio": "Ratio",
        "setting.enable_limiter": "Limiter",
        "setting.limiter_ceil": "Ceiling, dB",
        "setting.enable_reverb": "Light reverb",
        "setting.reverb_mix": "Reverb mix",
        "setting.enable_stereo": "Stereo width",
        "setting.stereo_width": "Width",
        "setting.enable_pan": "Micro pan",
        "setting.pan_offset": "L/R shift",
        "setting.enable_noise": "Background dither/noise",
        "setting.noise_dbfs": "Noise level, dBFS",
        "setting.enable_mp3": "WAV→MP3→WAV pass (ffmpeg next to exe or in PATH)",
        "setting.mp3_bitrate": "MP3 bitrate",
        "setting.normalize": "Peak normalize",
        "setting.target_peak": "Target peak, dBFS",
        "preset.recommended.label": "★ Recommended",
        "preset.recommended.desc": "Balance of processing and sound quality",
        "preset.light.label": "Light",
        "preset.light.desc": "Minimal processing, little coloration",
        "preset.aggressive.label": "Aggressive",
        "preset.aggressive.desc": "Stronger changes, possible artifacts",
        "preset.maximum.label": "Maximum",
        "preset.maximum.desc": "All stages at boosted settings",
        "preset.custom.label": "Custom (manual)",
        "preset.custom.desc": "Adjust all parameters manually",
        "dlg.warn": "Warning",
        "dlg.no_source": "Select a .wav file or folder",
        "dlg.no_output": "Select output folder",
        "dlg.no_files": "No files",
        "dlg.no_wav": "No .wav files found",
        "dlg.done": "Done",
        "dlg.ok_fail": "OK: {ok}, errors: {fail}",
        "dlg.ok_done": "Processed: {ok}\n{path}",
        "log.ffmpeg_missing": "ffmpeg not found — MP3 step will be skipped",
        "log.ffmpeg_local": "  Option 1: ffmpeg.exe next to {anchor}",
        "log.ffmpeg_folder": "  Folder: {folder}",
        "log.ffmpeg_path": "  Option 2: ffmpeg in system PATH",
        "log.ffmpeg_download": "  Download: {url}",
        "log.start": "--- Start ({preset}) ---",
        "log.finish": "--- Done: {path} ---",
        "status.ok": "OK: {ok}, errors: {fail}",
        "ffmpeg.title": "ffmpeg not found",
        "ffmpeg.header": "ffmpeg.exe not found",
        "ffmpeg.download_hdr": "Download for Windows:",
        "ffmpeg.path_hint": "Recommended path (next to {anchor}):",
        "ffmpeg.btn.gyan": "Download — gyan.dev",
        "ffmpeg.btn.github": "Download — GitHub",
        "ffmpeg.btn.close": "Close",
        "ffmpeg.skip_mp3": "MP3 step will be skipped.\n\nContinue without MP3?",
        "ffmpeg.status_local": "ffmpeg: {name} (next to {anchor})",
        "ffmpeg.status_path": "ffmpeg: system PATH ({path})",
        "hint.header_effect": "How it changes sound",
        "hint.header_quality": "Quality",
        "risk.safe": "Low risk to quality",
        "risk.moderate": "Moderate risk — listen to the result",
        "risk.risky": "High risk — use only if you need a strong effect",
        "hints.preset_body": (
            "A ready-made settings bundle.\n\n"
            "★ Recommended — balance of masking and quality.\n"
            "Light — minimal coloration.\n"
            "Aggressive / Maximum — stronger changes, higher artifact risk."
        ),
        "ffmpeg.body": (
            "The WAV→MP3→WAV step requires ffmpeg.\n\n"
            "Search order:\n"
            "1) {ffmpeg_name} next to {anchor}:\n   {folder}\n"
            "2) ffmpeg or ffmpeg.exe in system PATH\n\n"
            "Local install:\n"
            "• Download {direct_hint}\n"
            "• Copy {ffmpeg_name} to the folder above\n"
            "• Or add ffmpeg to Windows PATH\n"
            "• Restart the app\n\n"
            "Without ffmpeg other processing still works;\n"
            "the MP3 step will be skipped."
        ),
        "ffmpeg.direct_hint": "ffmpeg-release-essentials.zip → bin folder → ffmpeg.exe",
        "ffmpeg.download_urls": "• {url_primary}\n• {url_alt}",
        "step.trim": "trim silence",
        "step.tempo": "tempo ×{factor:.4f}",
        "step.pitch": "pitch {cents:+.0f} cent",
        "step.resample": "resample {hz} Hz",
        "step.eq": "EQ",
        "step.lowpass": "LP {freq:.0f} Hz",
        "step.compress": "compression",
        "step.limiter": "limiter",
        "step.reverb": "reverb",
        "step.stereo": "stereo width",
        "step.pan": "micro pan",
        "step.noise": "dither/noise",
        "step.mp3": "MP3 {bitrate}k",
        "step.mp3_skip": "MP3 skipped (no ffmpeg)",
        "step.normalize": "normalize",
        "step.saved": "saved",
        "step.done": "Done: {detail}",
        "step.error": "Error: {msg}",
    },
}


def get_language() -> str:
    return _LANG


def set_language(code: str) -> None:
    global _LANG
    if code in _STRINGS:
        _LANG = code
        _save_language(code)


def t(key: str, **kwargs) -> str:
    lang = _LANG if _LANG in _STRINGS else "ru"
    text = _STRINGS[lang].get(key) or _STRINGS["ru"].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text


def preset_label(key: str) -> str:
    return t(f"preset.{key}.label")


def preset_desc(key: str) -> str:
    return t(f"preset.{key}.desc")


def _config_path() -> Path:
    return get_app_root() / "language.json"


def load_saved_language() -> str:
    try:
        data = json.loads(_config_path().read_text(encoding="utf-8"))
        code = data.get("lang", "ru")
        if code in _STRINGS:
            global _LANG
            _LANG = code
            return code
    except (OSError, json.JSONDecodeError, KeyError):
        pass
    return "ru"


def _save_language(code: str) -> None:
    try:
        _config_path().write_text(
            json.dumps({"lang": code}, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError:
        pass
