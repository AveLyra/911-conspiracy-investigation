#!/usr/bin/env python3
"""Plot a time-domain peak envelope and spectrogram for a source-audio window.

This is a screening/visualization tool, not a blast classifier. It decodes only the
requested interval with ffmpeg, averages channels to mono, and preserves the source
file unchanged.
"""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile


def marker(value: str) -> tuple[float, str]:
    try:
        time_text, label = value.split("=", 1)
        return float(time_text), label
    except ValueError as exc:
        raise argparse.ArgumentTypeError("marker must be TIME=LABEL") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--start", type=float, required=True)
    parser.add_argument("--end", type=float, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--marker", action="append", type=marker, default=[])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.end <= args.start:
        raise SystemExit("--end must be greater than --start")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="audio-window-") as temp_dir:
        wav_path = Path(temp_dir) / "window.wav"
        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-ss",
                str(args.start),
                "-i",
                str(args.input),
                "-t",
                str(args.end - args.start),
                "-ac",
                "1",
                "-ar",
                "44100",
                "-c:a",
                "pcm_f32le",
                str(wav_path),
            ],
            check=True,
        )
        sample_rate, samples = wavfile.read(wav_path)

    samples = np.asarray(samples, dtype=np.float64)
    block = max(1, round(sample_rate * 0.002))
    usable = len(samples) - (len(samples) % block)
    peak = np.max(np.abs(samples[:usable].reshape(-1, block)), axis=1)
    peak_dbfs = 20 * np.log10(np.maximum(peak, 1e-8))
    peak_time = args.start + (np.arange(len(peak)) + 0.5) * block / sample_rate

    frequency, spec_time, magnitude = signal.spectrogram(
        samples,
        fs=sample_rate,
        window="hann",
        nperseg=2048,
        noverlap=1792,
        scaling="spectrum",
        mode="magnitude",
    )
    spec_time = spec_time + args.start
    spec_db = 20 * np.log10(np.maximum(magnitude, 1e-8))

    fig, (ax_peak, ax_spec) = plt.subplots(
        2,
        1,
        figsize=(18, 9),
        sharex=True,
        gridspec_kw={"height_ratios": [1, 2]},
        constrained_layout=True,
    )
    ax_peak.plot(peak_time, peak_dbfs, linewidth=0.8)
    ax_peak.set_ylim(-80, 1)
    ax_peak.set_ylabel("2 ms peak (dBFS)")
    ax_peak.grid(alpha=0.25)
    ax_peak.set_title(args.title)

    image = ax_spec.pcolormesh(
        spec_time,
        frequency,
        spec_db,
        shading="auto",
        cmap="magma",
        vmin=-100,
        vmax=-15,
    )
    ax_spec.set_ylim(0, 8000)
    ax_spec.set_ylabel("frequency (Hz)")
    ax_spec.set_xlabel("source-video time (s)")
    colorbar = fig.colorbar(image, ax=ax_spec)
    colorbar.set_label("spectral magnitude (dB re full scale)")

    for event_time, label in args.marker:
        for axis in (ax_peak, ax_spec):
            axis.axvline(event_time, color="#00c8d7", linewidth=1.0, alpha=0.9)
        ax_peak.annotate(
            label,
            xy=(event_time, 0),
            xytext=(3, -4),
            textcoords="offset points",
            rotation=90,
            va="top",
            ha="left",
            fontsize=8,
            color="#006a73",
        )

    fig.savefig(args.output, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
