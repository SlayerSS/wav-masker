"""Ползунок с градиентом риска искажения звука."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from setting_hints import danger_color, scale_danger


class RiskScale(ttk.Frame):
    """Горизонтальный ползунок с цветной шкалой опасности."""

    _BAR_H = 10

    def __init__(
        self,
        parent,
        *,
        variable: tk.Variable,
        hint_key: str,
        lo: float,
        hi: float,
        on_change=None,
    ):
        super().__init__(parent)
        self._key = hint_key
        self._lo = float(lo)
        self._hi = float(hi)
        self._var = variable
        self._on_change = on_change
        self._gradient_id: int | None = None
        self._marker_id: int | None = None

        self._bar = tk.Canvas(
            self,
            height=self._BAR_H,
            highlightthickness=0,
            bd=0,
            bg="#f0f0f0",
        )
        self._bar.pack(fill=tk.X, pady=(0, 2))
        self._bar.bind("<Configure>", self._redraw_bar)

        self.scale = ttk.Scale(
            self,
            from_=lo,
            to=hi,
            variable=variable,
            orient=tk.HORIZONTAL,
            command=self._on_scale_drag,
        )
        self.scale.pack(fill=tk.X)

        self._var.trace_add("write", self._on_var_change)
        self.after_idle(self._redraw_bar)

    def _on_scale_drag(self, _val):
        self._update_marker()
        if self._on_change:
            self._on_change()

    def _on_var_change(self, *_args):
        self._update_marker()
        if self._on_change:
            self._on_change()

    def _redraw_bar(self, _event=None):
        w = max(self._bar.winfo_width(), 2)
        h = self._BAR_H
        self._bar.delete("all")
        steps = min(w, 120)
        for i in range(steps):
            x0 = int(i * w / steps)
            x1 = int((i + 1) * w / steps) + 1
            val = self._lo + (self._hi - self._lo) * (i + 0.5) / steps
            d = scale_danger(self._key, val, self._lo, self._hi)
            self._bar.create_rectangle(x0, 0, x1, h, fill=danger_color(d), outline="")
        self._bar.create_rectangle(0, 0, w, h, outline="#bbb")
        self._update_marker()

    def _update_marker(self):
        w = max(self._bar.winfo_width(), 2)
        try:
            val = float(self._var.get())
        except (tk.TclError, ValueError):
            return
        frac = 0.0 if self._hi == self._lo else (val - self._lo) / (self._hi - self._lo)
        frac = max(0.0, min(1.0, frac))
        x = int(frac * w)
        if self._marker_id is not None:
            self._bar.delete(self._marker_id)
        self._marker_id = self._bar.create_line(
            x, 0, x, self._BAR_H, fill="#222", width=2
        )

    def danger(self) -> float:
        try:
            return scale_danger(self._key, float(self._var.get()), self._lo, self._hi)
        except (tk.TclError, ValueError):
            return 0.0
