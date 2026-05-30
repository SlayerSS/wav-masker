"""Текстовое поле с полосой прокрутки и колёсиком мыши."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def bind_mousewheel(widget: tk.Misc, scroll_target: tk.Text) -> None:
    def _wheel(event):
        scroll_target.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    widget.bind("<MouseWheel>", _wheel, add="+")


def make_scrollable_text(
    parent: tk.Misc,
    *,
    readonly: bool = False,
    **text_kwargs,
) -> tuple[ttk.Frame, tk.Text, ttk.Scrollbar]:
    """Контейнер с Text + Scrollbar (grid)."""
    frame = ttk.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    text = tk.Text(frame, wrap=tk.WORD, **text_kwargs)
    scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    text.grid(row=0, column=0, sticky="nsew")
    scroll.grid(row=0, column=1, sticky="ns")

    bind_mousewheel(text, text)
    bind_mousewheel(frame, text)

    if readonly:
        text.bind("<Key>", lambda _e: "break")

    return frame, text, scroll


def set_readonly_text(text: tk.Text, content: str) -> None:
    text.configure(state=tk.NORMAL)
    text.delete("1.0", tk.END)
    text.insert(tk.END, content)
    text.configure(state=tk.DISABLED)
    text.see("1.0")
