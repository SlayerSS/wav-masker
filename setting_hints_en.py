"""English setting hints (effect, quality, risk)."""

HINTS_EN: dict[str, dict[str, str]] = {
    "trim_silence": {
        "effect": "Removes silence at the start and end. Track gets shorter without empty tails.",
        "quality": "Low risk. May cut very quiet attacks (fade-in) if the threshold is too high.",
        "risk": "safe",
    },
    "enable_tempo_resample": {
        "effect": "Slightly speeds up or slows the track (duration changes). Sample grid shifts.",
        "quality": "Moderate risk. Noticeable above ~1.5%. At 1% usually almost inaudible.",
        "risk": "moderate",
    },
    "speed_factor": {
        "effect": "Tempo change strength. 1.008 ~ +0.8% faster — slightly higher pitch and shorter track.",
        "quality": "Up to 1.01 — low risk. Above 1.015 — possible artifacts and a “sped up” feel.",
        "risk": "moderate",
    },
    "enable_lowpass": {
        "effect": "Cuts high frequencies (brightness, air, hiss). Sound becomes softer and darker.",
        "quality": "Moderate risk. Cut below 15 kHz is audible on cymbals and vocal “s”.",
        "risk": "moderate",
    },
    "cutoff_freq": {
        "effect": "Low-pass cutoff frequency. Lower — fewer highs, more “telephone” color.",
        "quality": "16–17 kHz — moderate. Below 14 kHz — high risk of lost detail.",
        "risk": "moderate",
    },
    "filter_order": {
        "effect": "Filter steepness. Higher order — sharper high cut, stronger phase shift.",
        "quality": "5–7 is usually enough. 9–10 — higher risk of ringing and unnatural highs.",
        "risk": "moderate",
    },
    "enable_pitch": {
        "effect": "Shifts pitch without changing length (cents). Changes vocal and instrument timbre.",
        "quality": "Up to 30 cents — low risk. 50+ — moderate (slight chorus). Strong shift — artifacts.",
        "risk": "moderate",
    },
    "pitch_cents": {
        "effect": "Shift amount in cents (100 cents = semitone). Plus — higher, minus — lower.",
        "quality": "20–40 cents — usually safe. Above 50 — possible “plastic” vocal.",
        "risk": "moderate",
    },
    "enable_resample_chain": {
        "effect": "Recalculates 44.1→48→44.1 kHz. Slightly blurs micro-detail and changes digital fingerprint.",
        "quality": "Low–moderate risk. Almost inaudible, but not for audiophile mastering.",
        "risk": "moderate",
    },
    "resample_via_hz": {
        "effect": "Intermediate rate in the chain. 48 kHz — standard; 96 — softer but slower processing.",
        "quality": "Low risk at 48 kHz. Extreme values matter little with a short chain.",
        "risk": "safe",
    },
    "enable_eq": {
        "effect": "Tonal correction: lows, mids, highs. Changes balance and mix character.",
        "quality": "±1 dB — low risk. Strong cuts (−2 dB and more) — moderate color change.",
        "risk": "moderate",
    },
    "eq_low_shelf_db": {
        "effect": "Boost or cut bass and low end. Plus — fuller, minus — drier.",
        "quality": "Up to ±1 dB — safe. +2 dB and above — risk of overload on speakers.",
        "risk": "moderate",
    },
    "eq_mid_db": {
        "effect": "Mids (vocals, guitars). Minus — farther/softer, plus — closer and clearer.",
        "quality": "Moderate values are safe. Strong minus — hollow sound.",
        "risk": "moderate",
    },
    "eq_high_shelf_db": {
        "effect": "Highs: brightness and clarity. Minus — warmer, plus — harsher and more digital.",
        "quality": "Strong minus with low-pass — high risk of a dull track.",
        "risk": "moderate",
    },
    "enable_compressor": {
        "effect": "Compresses dynamics: quiet parts louder, peaks limited. Track feels denser and louder.",
        "quality": "Ratio 2–3 — moderate. High ratio and low threshold — pumping, ear fatigue.",
        "risk": "moderate",
    },
    "comp_threshold_db": {
        "effect": "Level where compression starts. Lower threshold (closer to 0) — more signal compressed.",
        "quality": "−18…−22 dB — typical for mastering. Below −14 — high risk of over-compression.",
        "risk": "moderate",
    },
    "comp_ratio": {
        "effect": "Compression strength. 2:1 — gentle, 4:1 and above — aggressive, less dynamics.",
        "quality": "Up to 3 — moderate risk. Above 4 — noticeable “brick wall” sound.",
        "risk": "moderate",
    },
    "enable_limiter": {
        "effect": "Caps maximum loudness, removes peaks. Clipping protection.",
        "quality": "Ceiling −0.5…−1 dB — low risk. 0 dB and drive — distortion.",
        "risk": "safe",
    },
    "limiter_ceiling_db": {
        "effect": "Maximum level after limiter. Closer to 0 — louder but riskier for clipping.",
        "quality": "−0.3…−1 dB — safe for streaming. 0 dB — high peak-clipping risk.",
        "risk": "moderate",
    },
    "enable_reverb": {
        "effect": "Adds light echo/room. Sound feels farther and more spacious.",
        "quality": "Small mix (up to 0.08) — low risk. Above 0.12 — noticeable bath, muddiness.",
        "risk": "moderate",
    },
    "reverb_mix": {
        "effect": "Wet signal amount. 0 — off, 0.1 — light room.",
        "quality": "Up to 0.08 — usually safe. 0.15+ — moderate/high blur risk.",
        "risk": "moderate",
    },
    "enable_stereo_width": {
        "effect": "Widens stereo (sides wider, center thinner). More “space” in headphones.",
        "quality": "1.05–1.15 — moderate. 1.25+ — phase issues in mono, empty center.",
        "risk": "moderate",
    },
    "stereo_width": {
        "effect": "Width amount. 1.0 — unchanged, higher — wider panorama.",
        "quality": "Up to 1.12 — low–moderate risk. Above 1.2 — check track in mono.",
        "risk": "moderate",
    },
    "enable_micro_pan": {
        "effect": "Slightly shifts L/R balance. Changes stereo image without strong widening.",
        "quality": "Small shift — low risk. Large — odd panning in headphones.",
        "risk": "safe",
    },
    "pan_offset": {
        "effect": "Pan shift amount between channels.",
        "quality": "Up to 0.05 — safe. Above 0.08 — moderate balance risk.",
        "risk": "moderate",
    },
    "enable_noise": {
        "effect": "Adds very quiet noise/dither. Changes digital “cleanliness” of the signal.",
        "quality": "−53 dBFS and quieter — almost inaudible. −48 and louder — moderate hiss risk in silence.",
        "risk": "moderate",
    },
    "noise_dbfs": {
        "effect": "Background noise level. Closer to 0 — more audible.",
        "quality": "−54…−56 — low risk. Above −50 — may be heard between phrases.",
        "risk": "moderate",
    },
    "enable_mp3_roundtrip": {
        "effect": "Encodes to MP3 and back to WAV. Loses fine detail, adds digital coloration.",
        "quality": "320 kbps — moderate risk. 256 and below — high artifact and treble loss risk.",
        "risk": "risky",
    },
    "mp3_bitrate_kbps": {
        "effect": "MP3 quality in the intermediate step. Higher — better detail retention.",
        "quality": "320 — acceptable for masking. 128 — high risk for music.",
        "risk": "moderate",
    },
    "normalize_output": {
        "effect": "Raises overall loudness to target peak. Track sounds louder and more even in level.",
        "quality": "Low risk if no prior clipping. Amplifies existing artifacts.",
        "risk": "safe",
    },
    "target_peak_dbfs": {
        "effect": "Target peak loudness. −0.3 dB — near max, −1 dB — headroom for codecs.",
        "quality": "−0.3…−1 dB — safe. 0 dB — clipping risk on conversion.",
        "risk": "safe",
    },
}
