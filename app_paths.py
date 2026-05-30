"""Пути приложения (корень, локальный ffmpeg)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

FFMPEG_NAME = "ffmpeg.exe"

# Страницы загрузки для Windows
FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/"
FFMPEG_DOWNLOAD_ALT_URL = "https://github.com/BtbN/FFmpeg-Builds/releases"
FFMPEG_DIRECT_HINT = "ffmpeg-release-essentials.zip → папка bin → ffmpeg.exe"


def get_app_root() -> Path:
    """Корень приложения: папка с exe (сборка) или папка проекта (скрипт)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def local_ffmpeg_path() -> Path:
    return get_app_root() / FFMPEG_NAME


def ffmpeg_local_anchor_name() -> str:
    """Имя файла-ориентира в папке приложения."""
    if getattr(sys, "frozen", False):
        return "WAV Masker.exe"
    return "app_gui.py"


def ffmpeg_missing_details() -> dict[str, str]:
    """Тексты для диалога «ffmpeg не найден»."""
    from i18n import t

    folder = str(get_app_root())
    anchor = ffmpeg_local_anchor_name()
    return {
        "title": t("ffmpeg.title"),
        "folder": folder,
        "target_file": str(local_ffmpeg_path()),
        "anchor": anchor,
        "body": t(
            "ffmpeg.body",
            ffmpeg_name=FFMPEG_NAME,
            anchor=anchor,
            folder=folder,
            direct_hint=t("ffmpeg.direct_hint"),
        ),
        "url_primary": FFMPEG_DOWNLOAD_URL,
        "url_alt": FFMPEG_DOWNLOAD_ALT_URL,
    }


def find_ffmpeg() -> str | None:
    """
    Ищет ffmpeg: сначала ffmpeg.exe в корне приложения,
    затем в PATH системы.
    """
    local = local_ffmpeg_path()
    if local.is_file():
        return str(local)
    return shutil.which("ffmpeg")


def ffmpeg_available() -> bool:
    return find_ffmpeg() is not None


def ffmpeg_status_message() -> str | None:
    """Краткая строка для журнала; None если ffmpeg найден."""
    from i18n import t

    exe = find_ffmpeg()
    if exe:
        local = local_ffmpeg_path()
        if Path(exe).resolve() == local.resolve():
            anchor = ffmpeg_local_anchor_name()
            return t("ffmpeg.status_local", name=local.name, anchor=anchor)
        return t("ffmpeg.status_path", path=exe)
    return None
