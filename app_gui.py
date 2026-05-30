"""Графический интерфейс WAV Masker с пресетами."""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app_paths import ffmpeg_available, ffmpeg_missing_details, ffmpeg_status_message
from audio_processor import collect_wav_files, process_batch
from ffmpeg_ui import show_ffmpeg_missing_dialog, warn_ffmpeg_if_mp3_enabled
from i18n import load_saved_language, preset_desc, preset_label, set_language, t
from presets import PRESET_ORDER, ProcessingConfig, get_preset_config
from project_meta import AUTHOR, FORK_NOTICE, UPSTREAM_NAME, UPSTREAM_REPOSITORY
from risk_slider import RiskScale
from scroll_text import bind_mousewheel, make_scrollable_text
from setting_hints import SETTING_HINTS, danger_color, format_hint, get_preset_hint, scale_danger, setting_title
from tooltips import ToolTip, attach_hint

_PROCESS_BTN = {
    "bg": "#28a745",
    "fg": "white",
    "activebackground": "#218838",
    "activeforeground": "white",
}

UI_SECTIONS = [
    ("section.basic", [
        ("trim_silence", "check", "setting.trim_silence"),
        ("enable_tempo_resample", "check", "setting.enable_tempo"),
        ("speed_factor", "scale", "setting.speed_factor", 1.0, 1.02, "{:.4f}"),
        ("enable_lowpass", "check", "setting.enable_lowpass"),
        ("cutoff_freq", "scale", "setting.cutoff_freq", 14000, 19000, "{:.0f}"),
        ("filter_order", "scale", "setting.filter_order", 2, 10, "{:.0f}"),
    ]),
    ("section.pitch", [
        ("enable_pitch", "check", "setting.enable_pitch"),
        ("pitch_cents", "scale", "setting.pitch_cents", 0, 80, "{:.0f}"),
        ("enable_resample_chain", "check", "setting.resample_chain"),
        ("resample_via_hz", "scale", "setting.resample_hz", 44100, 96000, "{:.0f}"),
    ]),
    ("section.eq", [
        ("enable_eq", "check", "setting.enable_eq"),
        ("eq_low_shelf_db", "scale", "setting.eq_low", -3, 3, "{:.1f}"),
        ("eq_mid_db", "scale", "setting.eq_mid", -4, 2, "{:.1f}"),
        ("eq_high_shelf_db", "scale", "setting.eq_high", -4, 2, "{:.1f}"),
    ]),
    ("section.dynamics", [
        ("enable_compressor", "check", "setting.enable_comp"),
        ("comp_threshold_db", "scale", "setting.comp_thresh", -30, -8, "{:.0f}"),
        ("comp_ratio", "scale", "setting.comp_ratio", 1.5, 5, "{:.1f}"),
        ("enable_limiter", "check", "setting.enable_limiter"),
        ("limiter_ceiling_db", "scale", "setting.limiter_ceil", -3, 0, "{:.1f}"),
    ]),
    ("section.space", [
        ("enable_reverb", "check", "setting.enable_reverb"),
        ("reverb_mix", "scale", "setting.reverb_mix", 0, 0.2, "{:.2f}"),
        ("enable_stereo_width", "check", "setting.enable_stereo"),
        ("stereo_width", "scale", "setting.stereo_width", 1.0, 1.3, "{:.2f}"),
        ("enable_micro_pan", "check", "setting.enable_pan"),
        ("pan_offset", "scale", "setting.pan_offset", 0, 0.12, "{:.2f}"),
    ]),
    ("section.export", [
        ("enable_noise", "check", "setting.enable_noise"),
        ("noise_dbfs", "scale", "setting.noise_dbfs", -60, -45, "{:.0f}"),
        ("enable_mp3_roundtrip", "check", "setting.enable_mp3"),
        ("mp3_bitrate_kbps", "scale", "setting.mp3_bitrate", 128, 320, "{:.0f}"),
        ("normalize_output", "check", "setting.normalize"),
        ("target_peak_dbfs", "scale", "setting.target_peak", -3, 0, "{:.1f}"),
    ]),
]

INTEGER_SCALES = frozenset({"filter_order", "resample_via_hz", "mp3_bitrate_kbps"})

# Дочерние настройки → родительский переключатель
SETTING_PARENT: dict[str, str] = {
    "speed_factor": "enable_tempo_resample",
    "cutoff_freq": "enable_lowpass",
    "filter_order": "enable_lowpass",
    "pitch_cents": "enable_pitch",
    "resample_via_hz": "enable_resample_chain",
    "eq_low_shelf_db": "enable_eq",
    "eq_mid_db": "enable_eq",
    "eq_high_shelf_db": "enable_eq",
    "comp_threshold_db": "enable_compressor",
    "comp_ratio": "enable_compressor",
    "limiter_ceiling_db": "enable_limiter",
    "reverb_mix": "enable_reverb",
    "stereo_width": "enable_stereo_width",
    "pan_offset": "enable_micro_pan",
    "noise_dbfs": "enable_noise",
    "mp3_bitrate_kbps": "enable_mp3_roundtrip",
    "target_peak_dbfs": "normalize_output",
}

CHILDREN_BY_PARENT: dict[str, list[str]] = {}
for _child, _parent in SETTING_PARENT.items():
    CHILDREN_BY_PARENT.setdefault(_parent, []).append(_child)


class ScrollableFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        self.inner = ttk.Frame(canvas)
        self.inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        self._win = canvas.create_window((0, 0), window=self.inner, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(self._win, width=e.width))

        def _wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _wheel, add="+")
        self.canvas = canvas


class AudioMaskerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        load_saved_language()
        self.title(t("app.title"))
        self.minsize(760, 640)
        self.geometry("820x720")

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value=os.path.join(os.getcwd(), "masked_tracks"))
        self.output_prefix = tk.StringVar(value="cleaned_")
        self.preset_key = tk.StringVar(value="recommended")
        self.preset_desc = tk.StringVar()
        self.lang_var = tk.StringVar(value=load_saved_language())
        self.parallel_var = tk.BooleanVar(value=True)

        self._cfg: dict[str, tk.Variable] = {}
        self._applying_preset = False
        self._processing = False
        self._hint_tooltips: list[tuple[ToolTip, str | None]] = []
        self._static_hint_getters: dict[int, object] = {}
        self._section_frames: dict[str, ttk.LabelFrame] = {}
        self._field_labels: dict[str, ttk.Label] = {}
        self._value_labels: dict[str, ttk.Label] = {}
        self._checkbuttons: dict[str, ttk.Checkbutton] = {}
        self._io_labels: dict[str, ttk.Label] = {}
        self._buttons: dict[str, ttk.Button] = {}
        self._setting_rows: dict[str, ttk.Frame] = {}
        self._max_workers = max(2, min(8, (os.cpu_count() or 4)))

        self._init_config_vars()
        self._build_ui()
        self._apply_preset("recommended")
        self._v("enable_mp3_roundtrip").trace_add("write", self._on_mp3_option_changed)

        if ffmpeg_available():
            status = ffmpeg_status_message()
            if status:
                self._log_line(status)
        else:
            self._log_ffmpeg_missing()
            self.after(500, lambda: show_ffmpeg_missing_dialog(self))

    def _init_config_vars(self):
        c = ProcessingConfig()
        d = c.to_kwargs()
        for key, val in d.items():
            if isinstance(val, bool):
                self._cfg[key] = tk.BooleanVar(value=val)
            elif isinstance(val, int):
                self._cfg[key] = tk.IntVar(value=val)
            else:
                self._cfg[key] = tk.DoubleVar(value=float(val))

    def _v(self, name: str) -> tk.Variable:
        return self._cfg[name]

    def _register_hint(self, widget: tk.Misc, hint_key: str) -> ToolTip:
        tip = attach_hint(widget, format_hint(hint_key))
        self._hint_tooltips.append((tip, hint_key))
        return tip

    def _register_static_hint(self, widget: tk.Misc, getter) -> ToolTip:
        tip = attach_hint(widget, getter())
        self._hint_tooltips.append((tip, None))
        self._static_hint_getters[id(tip)] = getter
        return tip

    def _refresh_hints(self):
        for tip, key in self._hint_tooltips:
            if key is None:
                getter = self._static_hint_getters.get(id(tip))
                if getter:
                    tip.set_text(getter())
            else:
                tip.set_text(format_hint(key))

    def _build_menu(self):
        self._menubar = tk.Menu(self)
        lang_menu = tk.Menu(self._menubar, tearoff=0)
        lang_menu.add_radiobutton(
            label=t("menu.lang.ru"),
            variable=self.lang_var,
            value="ru",
            command=lambda: self._set_language("ru"),
        )
        lang_menu.add_radiobutton(
            label=t("menu.lang.en"),
            variable=self.lang_var,
            value="en",
            command=lambda: self._set_language("en"),
        )
        self._menubar.add_cascade(label=t("menu.language"), menu=lang_menu)

        help_menu = tk.Menu(self._menubar, tearoff=0)
        help_menu.add_command(label=t("menu.hints"), command=self._show_hints_guide)
        help_menu.add_command(label=t("menu.about"), command=self._show_about)
        self._menubar.add_cascade(label=t("menu.help"), menu=help_menu)
        self.config(menu=self._menubar)

    def _set_language(self, code: str):
        set_language(code)
        self.lang_var.set(code)
        self._retranslate()

    def _retranslate(self):
        self.title(t("app.title"))
        self._build_menu()

        self._io_frame.configure(text=t("files.title"))
        self._config_frame.configure(text=t("config.title"))
        self._log_frame.configure(text=t("log.title"))

        self._io_labels["source"].configure(text=t("files.source"))
        self._io_labels["output"].configure(text=t("files.output"))
        self._io_labels["prefix"].configure(text=t("files.prefix"))
        self._buttons["file"].configure(text=t("btn.file"))
        self._buttons["folder"].configure(text=t("btn.folder"))
        self.process_btn.configure(text=t("btn.process"))
        self.parallel_cb.configure(text=t("setting.parallel"))
        self._credit_label.configure(text=t("about.credit"))

        for section_key, frame in self._section_frames.items():
            frame.configure(text=t(section_key))

        for cfg_key, cb in self._checkbuttons.items():
            i18n_key = self._check_i18n.get(cfg_key)
            if i18n_key:
                cb.configure(text=t(i18n_key))

        for cfg_key, lbl in self._field_labels.items():
            i18n_key = self._field_i18n.get(cfg_key)
            if i18n_key:
                lbl.configure(text=t(i18n_key))

        labels = [preset_label(k) for k in PRESET_ORDER]
        current = self.preset_key.get()
        self.preset_combo.configure(values=labels)
        if current in PRESET_ORDER:
            self.preset_combo.current(PRESET_ORDER.index(current))
        self.preset_desc.set(preset_desc(current))

        if not self._processing:
            self.status_label.configure(text=t("status.ready"))

        self._refresh_hints()

    def _show_hints_guide(self):
        win = tk.Toplevel(self)
        win.title(t("hints.title"))
        win.geometry("560x480")
        win.minsize(400, 320)
        win.transient(self)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)

        outer = ttk.Frame(win, padding=8)
        outer.grid(row=0, column=0, sticky="nsew")
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)

        text_frame, text, _scroll = make_scrollable_text(
            outer,
            padx=10,
            pady=10,
            font=("Segoe UI", 10),
        )
        text_frame.grid(row=0, column=0, sticky="nsew")

        sections = [(t("hints.presets"), get_preset_hint())]
        for key in SETTING_HINTS:
            sections.append((setting_title(key), format_hint(key)))
        for title, body in sections:
            text.insert(tk.END, f"{title}\n", "h")
            text.insert(tk.END, body + "\n\n")
        text.tag_configure("h", font=("Segoe UI", 10, "bold"))
        text.configure(state=tk.DISABLED)

    def _show_about(self):
        messagebox.showinfo(
            t("about.title"),
            f"{UPSTREAM_NAME}\n\n"
            f"{t('about.author')}: {AUTHOR}\n"
            f"{t('about.credit')}\n\n"
            f"{t('about.repo')}:\n{UPSTREAM_REPOSITORY}\n\n"
            f"{FORK_NOTICE}",
            parent=self,
        )

    def _build_ui(self):
        self._build_menu()
        self._check_i18n: dict[str, str] = {}
        self._field_i18n: dict[str, str] = {}
        pad = {"padx": 10, "pady": 4}
        root = ttk.Frame(self, padding=10)
        root.pack(fill=tk.BOTH, expand=True)

        self._io_frame = ttk.LabelFrame(root, text=t("files.title"), padding=8)
        self._io_frame.pack(fill=tk.X, **pad)
        io = self._io_frame
        self._io_labels["source"] = ttk.Label(io, text=t("files.source"))
        self._io_labels["source"].grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(io, textvariable=self.input_path).grid(row=1, column=0, sticky=tk.EW)
        bf = ttk.Frame(io)
        bf.grid(row=1, column=1, padx=6)
        self._buttons["file"] = ttk.Button(bf, text=t("btn.file"), command=self._pick_file, width=6)
        self._buttons["file"].pack(side=tk.LEFT, padx=2)
        self._buttons["folder"] = ttk.Button(
            bf, text=t("btn.folder"), command=self._pick_folder, width=6
        )
        self._buttons["folder"].pack(side=tk.LEFT)
        self._io_labels["output"] = ttk.Label(io, text=t("files.output"))
        self._io_labels["output"].grid(row=2, column=0, sticky=tk.W, pady=(6, 0))
        ttk.Entry(io, textvariable=self.output_path).grid(row=3, column=0, sticky=tk.EW)
        ttk.Button(io, text="…", width=3, command=self._pick_out).grid(row=3, column=1)
        self._io_labels["prefix"] = ttk.Label(io, text=t("files.prefix"))
        self._io_labels["prefix"].grid(row=4, column=0, sticky=tk.W, pady=(6, 0))
        ttk.Entry(io, textvariable=self.output_prefix, width=16).grid(row=4, column=0, sticky=tk.W, pady=2)
        io.columnconfigure(0, weight=1)

        self._config_frame = ttk.LabelFrame(root, text=t("config.title"), padding=8)
        self._config_frame.pack(fill=tk.X, **pad)
        pf = self._config_frame
        self.preset_combo = ttk.Combobox(
            pf,
            values=[preset_label(k) for k in PRESET_ORDER],
            state="readonly",
            width=28,
        )
        self.preset_combo.pack(side=tk.LEFT)
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_selected)
        preset_hint_lbl = ttk.Label(pf, text=" ⓘ", cursor="question_arrow")
        preset_hint_lbl.pack(side=tk.LEFT, padx=(2, 0))
        self._register_static_hint(preset_hint_lbl, get_preset_hint)
        ttk.Label(pf, textvariable=self.preset_desc, foreground="#444").pack(
            side=tk.LEFT, padx=12
        )

        scroll = ScrollableFrame(root)
        scroll.pack(fill=tk.BOTH, expand=True, **pad)
        inner = scroll.inner

        for section_key, fields in UI_SECTIONS:
            self._section(inner, section_key, fields)

        self._refresh_setting_states()

        actions = ttk.Frame(root)
        actions.pack(fill=tk.X, **pad)
        self.parallel_cb = ttk.Checkbutton(
            actions,
            text=t("setting.parallel"),
            variable=self.parallel_var,
        )
        self.parallel_cb.pack(side=tk.LEFT, padx=(0, 10))
        self.process_btn = tk.Button(
            actions,
            text=t("btn.process"),
            command=self._start,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            **_PROCESS_BTN,
        )
        self.process_btn.pack(side=tk.LEFT)
        self.progress = ttk.Progressbar(actions, mode="determinate")
        self.progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.status_label = ttk.Label(actions, text=t("status.ready"))
        self.status_label.pack(side=tk.RIGHT)

        self._log_frame = ttk.LabelFrame(root, text=t("log.title"), padding=4)
        self._log_frame.pack(fill=tk.BOTH, expand=True, **pad)
        log_inner = ttk.Frame(self._log_frame)
        log_inner.pack(fill=tk.BOTH, expand=True)
        log_inner.columnconfigure(0, weight=1)
        log_inner.rowconfigure(0, weight=1)
        self.log = tk.Text(log_inner, height=8, wrap=tk.WORD, state=tk.DISABLED)
        log_sb = ttk.Scrollbar(log_inner, command=self.log.yview)
        self.log.configure(yscrollcommand=log_sb.set)
        self.log.grid(row=0, column=0, sticky="nsew")
        log_sb.grid(row=0, column=1, sticky="ns")
        bind_mousewheel(self.log, self.log)
        bind_mousewheel(log_inner, self.log)

        self._credit_label = ttk.Label(
            root,
            text=t("about.credit"),
            foreground="#888",
            font=("Segoe UI", 8),
        )
        self._credit_label.pack(anchor=tk.E, pady=(2, 0))

    def _hint_icon(self, parent, key: str) -> ttk.Label:
        lbl = ttk.Label(parent, text="ⓘ", cursor="question_arrow", foreground="#0066aa", width=2)
        if key in SETTING_HINTS:
            self._register_hint(lbl, key)
        return lbl

    def _scale_row(self, frame, row: int, key: str, i18n_key: str, lo, hi, fmt: str):
        row_frame = ttk.Frame(frame)
        row_frame.grid(row=row, column=0, columnspan=4, sticky=tk.EW, pady=1)
        row_frame.columnconfigure(1, weight=1)
        self._setting_rows[key] = row_frame

        name_lbl = ttk.Label(row_frame, text=t(i18n_key), width=22)
        name_lbl.grid(row=0, column=0, sticky=tk.W)
        self._field_labels[key] = name_lbl
        self._field_i18n[key] = i18n_key
        val_lbl = ttk.Label(row_frame, width=7)
        val_lbl.grid(row=0, column=2)
        self._value_labels[key] = val_lbl

        scale_wrap = ttk.Frame(row_frame)
        scale_wrap.grid(row=0, column=1, sticky=tk.EW, padx=6)
        scale_wrap.columnconfigure(0, weight=1)
        var = self._v(key)

        def _upd_val(*_, k=key, f=fmt, l=val_lbl):
            raw = var.get()
            if k in INTEGER_SCALES:
                rounded = int(round(float(raw)))
                if rounded != raw:
                    var.set(rounded)
                    return
                raw = rounded
            l.configure(text=f.format(raw))
            d = scale_danger(k, raw, lo, hi)
            l.configure(foreground=danger_color(d))

        RiskScale(
            scale_wrap,
            variable=var,
            hint_key=key,
            lo=lo,
            hi=hi,
            on_change=_upd_val,
        ).pack(fill=tk.X)
        self._hint_icon(row_frame, key).grid(row=0, column=3, padx=(4, 0))
        var.trace_add("write", _upd_val)
        _upd_val()

    def _refresh_parent_children(self, parent_key: str) -> None:
        active = bool(self._v(parent_key).get())
        for child in CHILDREN_BY_PARENT.get(parent_key, []):
            row = self._setting_rows.get(child)
            if row is None:
                continue
            if active:
                row.grid()
            else:
                row.grid_remove()

    def _refresh_setting_states(self) -> None:
        for parent_key in CHILDREN_BY_PARENT:
            self._refresh_parent_children(parent_key)

    def _on_parent_toggle(self, parent_key: str) -> None:
        if self._applying_preset:
            return
        self._refresh_parent_children(parent_key)

    def _section(self, parent, section_key: str, fields: list):
        frame = ttk.LabelFrame(parent, text=t(section_key), padding=6)
        frame.pack(fill=tk.X, pady=4, padx=2)
        self._section_frames[section_key] = frame
        for i, spec in enumerate(fields):
            key = spec[0]
            kind = spec[1]
            i18n_key = spec[2]
            if kind == "check":
                row = ttk.Frame(frame)
                row.grid(row=i, column=0, columnspan=4, sticky=tk.EW, pady=1)
                cb = ttk.Checkbutton(row, text=t(i18n_key), variable=self._v(key))
                cb.pack(side=tk.LEFT)
                self._checkbuttons[key] = cb
                self._check_i18n[key] = i18n_key
                self._hint_icon(row, key).pack(side=tk.LEFT, padx=(6, 0))
                if key in CHILDREN_BY_PARENT:
                    self._v(key).trace_add(
                        "write",
                        lambda *_a, p=key: self._on_parent_toggle(p),
                    )
            elif kind == "scale":
                lo, hi, fmt = spec[3], spec[4], spec[5]
                self._scale_row(frame, i, key, i18n_key, lo, hi, fmt)
        frame.columnconfigure(1, weight=1)

    def _log_ffmpeg_missing(self):
        info = ffmpeg_missing_details()
        self._log_line(f"⚠ {t('log.ffmpeg_missing')}")
        self._log_line(t("log.ffmpeg_local", anchor=info["anchor"]))
        self._log_line(t("log.ffmpeg_folder", folder=info["folder"]))
        self._log_line(t("log.ffmpeg_path"))
        self._log_line(t("log.ffmpeg_download", url=info["url_primary"]))

    def _on_mp3_option_changed(self, *_args):
        if (
            not self._applying_preset
            and self._v("enable_mp3_roundtrip").get()
            and not ffmpeg_available()
        ):
            self.after(100, lambda: show_ffmpeg_missing_dialog(self))

    def _apply_preset(self, key: str):
        self._applying_preset = True
        cfg = get_preset_config(key)
        d = cfg.to_kwargs()
        for name, var in self._cfg.items():
            if name in d:
                val = d[name]
                if isinstance(var, tk.BooleanVar):
                    var.set(bool(val))
                elif isinstance(var, tk.IntVar):
                    var.set(int(val))
                else:
                    var.set(float(val))
        self.preset_key.set(key)
        if key in PRESET_ORDER:
            self.preset_combo.current(PRESET_ORDER.index(key))
        self.preset_desc.set(preset_desc(key))
        self._applying_preset = False
        self._refresh_setting_states()

    def _on_preset_selected(self, _event=None):
        idx = self.preset_combo.current()
        if idx < 0:
            return
        key = PRESET_ORDER[idx]
        if key != "custom":
            self._apply_preset(key)
        else:
            self.preset_key.set("custom")
            self.preset_desc.set(preset_desc("custom"))

    def _config_from_ui(self) -> ProcessingConfig:
        data = {}
        for name, var in self._cfg.items():
            data[name] = var.get()
        return ProcessingConfig.from_dict(data)

    def _log_line(self, text: str):
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _pick_file(self):
        p = filedialog.askopenfilename(filetypes=[("WAV", "*.wav")])
        if p:
            self.input_path.set(p)

    def _pick_folder(self):
        p = filedialog.askdirectory()
        if p:
            self.input_path.set(p)

    def _pick_out(self):
        p = filedialog.askdirectory()
        if p:
            self.output_path.set(p)

    def _start(self):
        src = self.input_path.get().strip()
        out = self.output_path.get().strip()
        if not src or not os.path.exists(src):
            messagebox.showwarning(t("dlg.warn"), t("dlg.no_source"))
            return
        if not out:
            messagebox.showwarning(t("dlg.warn"), t("dlg.no_output"))
            return
        files = collect_wav_files(src)
        if not files:
            messagebox.showinfo(t("dlg.no_files"), t("dlg.no_wav"))
            return

        config = self._config_from_ui()
        if not warn_ffmpeg_if_mp3_enabled(self, config.enable_mp3_roundtrip):
            return
        self._processing = True
        self.process_btn.configure(state=tk.DISABLED)
        self.progress["maximum"] = len(files)
        self.progress["value"] = 0
        preset_name = preset_label(self.preset_key.get())
        parallel = self.parallel_var.get()
        workers = self._max_workers if parallel else 1
        self._log_line(t("log.start", preset=preset_name))
        if parallel and len(files) > 1:
            self._log_line(t("log.parallel", n=workers))
        self.status_label.configure(text=t("status.processing"))

        def worker():
            def on_progress(cur, tot, name, msg):
                self.after(0, lambda: self._on_progress(cur, tot, name, msg))

            results = process_batch(
                files,
                out,
                output_prefix=self.output_prefix.get(),
                config=config,
                on_progress=on_progress,
                parallel=parallel,
                max_workers=workers,
            )
            self.after(0, lambda: self._done(results, out))

        threading.Thread(target=worker, daemon=True).start()

    def _on_progress(self, cur, tot, name, msg):
        self.progress["value"] = cur
        self.status_label.configure(text=f"{cur}/{tot}")
        self._log_line(f"[{cur}/{tot}] {name} — {msg}")

    def _done(self, results, out):
        ok = sum(1 for _, s, _ in results if s)
        fail = len(results) - ok
        self._processing = False
        self.process_btn.configure(state=tk.NORMAL)
        self.status_label.configure(text=t("status.ok", ok=ok, fail=fail))
        self._log_line(t("log.finish", path=out))
        if fail:
            messagebox.showwarning(t("dlg.done"), t("dlg.ok_fail", ok=ok, fail=fail))
        else:
            messagebox.showinfo(t("dlg.done"), t("dlg.ok_done", ok=ok, path=out))


def main():
    if sys.platform == "win32":
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    AudioMaskerApp().mainloop()


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    main()
