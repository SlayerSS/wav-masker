"""Диалог предупреждения об отсутствии ffmpeg."""

from __future__ import annotations

import webbrowser

import tkinter as tk
from tkinter import messagebox, ttk

from app_paths import (
    FFMPEG_DOWNLOAD_ALT_URL,
    FFMPEG_DOWNLOAD_URL,
    ffmpeg_available,
    ffmpeg_missing_details,
)
from i18n import t
from scroll_text import make_scrollable_text, set_readonly_text


def show_ffmpeg_missing_dialog(parent: tk.Misc) -> None:
    """Показывает окно с инструкцией и кнопками скачивания."""
    if ffmpeg_available():
        return

    info = ffmpeg_missing_details()
    win = tk.Toplevel(parent)
    win.title(info["title"])
    win.transient(parent)
    win.grab_set()
    win.resizable(True, True)
    win.minsize(480, 360)
    win.columnconfigure(0, weight=1)
    win.rowconfigure(0, weight=1)

    frame = ttk.Frame(win, padding=16)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    ttk.Label(
        frame,
        text=f"⚠ {t('ffmpeg.header')}",
        font=("Segoe UI", 11, "bold"),
    ).grid(row=0, column=0, sticky=tk.W)

    body = (
        info["body"]
        + f"\n\n{t('ffmpeg.download_hdr')}\n"
        + t(
            "ffmpeg.download_urls",
            url_primary=FFMPEG_DOWNLOAD_URL,
            url_alt=FFMPEG_DOWNLOAD_ALT_URL,
        )
    )
    text_frame, text, _scroll = make_scrollable_text(
        frame,
        height=12,
        relief=tk.FLAT,
        padx=4,
        pady=4,
        font=("Segoe UI", 10),
    )
    text_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 8))
    set_readonly_text(text, body)

    ttk.Label(
        frame,
        text=t("ffmpeg.path_hint", anchor=info.get("anchor", "app_gui.py")),
        font=("Segoe UI", 9, "bold"),
    ).grid(row=2, column=0, sticky=tk.W)
    path_var = tk.StringVar(value=info["target_file"])
    path_entry = ttk.Entry(frame, textvariable=path_var, state="readonly")
    path_entry.grid(row=3, column=0, sticky=tk.EW, pady=(2, 10))

    btn_row = ttk.Frame(frame)
    btn_row.grid(row=4, column=0, sticky=tk.EW)

    def open_url(url: str) -> None:
        webbrowser.open(url)

    ttk.Button(
        btn_row,
        text=t("ffmpeg.btn.gyan"),
        command=lambda: open_url(info["url_primary"]),
    ).pack(side=tk.LEFT, padx=(0, 6))
    ttk.Button(
        btn_row,
        text=t("ffmpeg.btn.github"),
        command=lambda: open_url(info["url_alt"]),
    ).pack(side=tk.LEFT, padx=(0, 6))
    ttk.Button(btn_row, text=t("ffmpeg.btn.close"), command=win.destroy).pack(side=tk.RIGHT)

    win.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() - win.winfo_width()) // 2
    y = parent.winfo_rooty() + (parent.winfo_height() - win.winfo_height()) // 2
    win.geometry(f"+{max(0, x)}+{max(0, y)}")

    win.wait_window()


def warn_ffmpeg_if_mp3_enabled(parent: tk.Misc, mp3_enabled: bool) -> bool:
    """
    Если включён MP3, но ffmpeg нет — показывает диалог.
    Возвращает True, если можно продолжать обработку.
    """
    if not mp3_enabled or ffmpeg_available():
        return True

    show_ffmpeg_missing_dialog(parent)
    info = ffmpeg_missing_details()
    return messagebox.askyesno(
        info["title"],
        t("ffmpeg.skip_mp3"),
        parent=parent,
        icon=messagebox.WARNING,
    )
