import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

RATE = 44100
CHANNELS = 2
BYTES_PER_FRAME = 4
FRAME_SAMPLES = 1152
FRAMES_PER_SECOND = RATE * BYTES_PER_FRAME
PEAK_THRESHOLDS = (0, 32, 104, 328)
MIN_REPEAT_FRAMES = 39


def runs(values):
    start = None
    for index, value in enumerate([*values, False]):
        if value and start is None:
            start = index
        elif not value and start is not None:
            yield [start, index]
            start = None


def fingerprint_window(buffer, fingerprints):
    samples = np.frombuffer(buffer, dtype="<i2").astype(np.int32)
    if np.abs(samples).max() > 328:
        fingerprints.append(hashlib.blake2b(buffer, digest_size=16).digest())
    else:
        fingerprints.append(None)


def repeated_runs(fingerprints):
    # Index the first and last frame of a minimum-length run. Then require
    # all intervening decoded frame fingerprints to match.
    prior = defaultdict(list)
    result = []
    end = len(fingerprints) - MIN_REPEAT_FRAMES + 1
    for index in range(end):
        block = fingerprints[index : index + MIN_REPEAT_FRAMES]
        if None in block:
            continue
        key = (block[0], block[-1])
        for previous in prior[key]:
            if index - previous < MIN_REPEAT_FRAMES:
                continue
            if fingerprints[previous : previous + MIN_REPEAT_FRAMES] != block:
                continue
            if previous > 0 and index > 0 and fingerprints[previous-1] is not None and fingerprints[previous-1] == fingerprints[index-1]:
                continue
            length = MIN_REPEAT_FRAMES
            while (index + length < len(fingerprints) and length < index - previous
                   and fingerprints[index+length] is not None
                   and fingerprints[index+length] == fingerprints[previous+length]):
                length += 1
            result.append([previous, index, length])
        prior[key].append(index)
    return result


def analyze(file, ffmpeg):
    command = [ffmpeg, "-v", "error", "-xerror", "-nostdin", "-i", str(file),
               "-map", "0:a:0", "-c:a", "pcm_s16le", "-f", "s16le", "-"]
    peaks = []
    fingerprints = []
    residue = b""
    size = 0
    partial = None
    width = FRAME_SAMPLES * BYTES_PER_FRAME
    with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
        while buffer := process.stdout.read(FRAMES_PER_SECOND):
            size += len(buffer)
            samples = np.frombuffer(buffer, dtype="<i2").reshape(-1, CHANNELS).astype(np.int32)
            peak = np.abs(samples).max(axis=0).tolist()
            if len(buffer) == FRAMES_PER_SECOND:
                peaks.append(peak)
            else:
                partial = {"frames": len(samples), "channel_peaks": peak}
            buf = residue + buffer
            stop = len(buf) - len(buf) % width
            for i in range(0, stop, width):
                fingerprint_window(buf[i:i+width], fingerprints)
            residue = buf[stop:]
        if process.wait():
            raise RuntimeError("Audio decode failed")
    if size % BYTES_PER_FRAME or not peaks:
        raise ValueError("Expected stereo s16le data")
    peak_array = np.array(peaks)
    simultaneous = peak_array.max(axis=1)
    quiet = {}
    for threshold in PEAK_THRESHOLDS:
        intervals = list(runs(simultaneous <= threshold))
        quiet[str(threshold)] = {
            "seconds": int((simultaneous <= threshold).sum()),
            "seconds_each_channel": (peak_array <= threshold).sum(axis=0).tolist(),
            "intervals_at_least_10_seconds": [r for r in intervals if r[1] - r[0] >= 10],
            "longest_seconds": max((r[1] - r[0] for r in intervals), default=0),
        }
    return dict(pcm_bytes=size, full_seconds=len(peaks), partial=partial,
                decoded_seconds=round(size / FRAMES_PER_SECOND, 6),
                quiet=quiet, channel_peaks=peak_array.max(axis=0).tolist(),
                tested_grid_frames=len(fingerprints),
                eligible_loud_frames=sum(p is not None for p in fingerprints),
                exact_repeat_runs_1152_sample_units=repeated_runs(fingerprints))


def self_test():
    assert list(runs([True, True, False, True, False, True])) == [[0, 2], [3, 4], [5, 6]]
    block = [i.to_bytes(16, "little") for i in range(50)]
    assert repeated_runs(block + [None] + block) == [[0, 51, 50]]
    assert repeated_runs(block + [None] + block[:-1][::-1]) == []
    fingerprints = []
    fingerprint_window(bytes(FRAME_SAMPLES * BYTES_PER_FRAME), fingerprints)
    loud = np.full(FRAME_SAMPLES * CHANNELS, 1000, dtype="<i2").tobytes()
    fingerprint_window(loud, fingerprints)
    assert fingerprints[0] is None and fingerprints[1] is not None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", nargs="+", type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    args = parser.parse_args()
    self_test()
    results = {p.name: analyze(p, args.ffmpeg) for p in args.audio}
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
