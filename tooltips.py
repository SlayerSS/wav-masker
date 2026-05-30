"""Всплывающие подсказки для tkinter."""

from __future__ import annotations

import tkinter as tk


class ToolTip:
    def __init__(self, widget: tk.Misc, text: str, *, wraplength: int = 380):
        self.widget = widget
        self.text = text
        self.wraplength = wraplength
        self._tip: tk.Toplevel | None = None
        widget.bind("<Enter>", self._show, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _show(self, _event=None):
        if self._tip or not self.text.strip():
            return
        x = self.widget.winfo_rootx() + 24
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        tw.wm_geometry(f"+{x}+{y}")
        frame = tk.Frame(tw, background="#fffef5", relief=tk.SOLID, borderwidth=1)
        frame.pack()
        tk.Label(
            frame,
            text=self.text,
            justify=tk.LEFT,
            background="#fffef5",
            foreground="#222",
            wraplength=self.wraplength,
            padx=10,
            pady=8,
            font=("Segoe UI", 9),
        ).pack()

    def _hide(self, _event=None):
        if self._tip:
            self._tip.destroy()
            self._tip = None

    def set_text(self, text: str) -> None:
        self.text = text
        self._hide()


def attach_hint(widget: tk.Misc, text: str) -> ToolTip:
    return ToolTip(widget, text)
