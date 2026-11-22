#!/usr/bin/env python3
"""Pokémon Prismfall — Audio Mastering, OGG Conversion & mkxp-z Loop-Tagging Tool.

Normalizes any BGM/BGS/SE/ME track to consistent EBU R128 loudness (two-pass loudnorm),
converts .mp3/.wav/.flac/.ogg -> 44.1 kHz Ogg Vorbis (q=6), and writes exact
LOOPSTART / LOOPLENGTH Vorbis comments in samples for seamless mkxp-z looping.

Requirements: ffmpeg, ffprobe, vorbiscomment (vorbis-tools).

Examples:
  # Audit loudness & loop tags across a directory
  python3 master_track.py --audit audio/dedrum_tectonic

  # Master a BGM track to -14 LUFS with loop points in seconds (loop from 12.4s to 128.8s)
  python3 master_track.py in.mp3 "Audio/BGM/Battle - Voss.ogg" --lufs -14 --loop-start 12.4 --loop-end 128.8

  # Master a full-file seamless BGS loop at -18 LUFS (LOOPSTART=0, LOOPLENGTH=total_samples)
  python3 master_track.py raw_wind.wav "Audio/BGS/Wind - Isenmar.ogg" --lufs -18 --full-loop

  # Master a one-shot SE at -12 LUFS (no loop tags)
  python3 master_track.py raw_boom.wav "Audio/SE/Beam break.ogg" --lufs -12
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AUDIO_EXTS = {".ogg", ".mp3", ".wav", ".flac", ".m4a", ".opus"}


def require_tools(*names: str) -> None:
    missing = [n for n in names if shutil.which(n) is None]
    if missing:
        sys.exit(f"Missing required CLI tools: {', '.join(missing)}")


def probe_track(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_name,sample_rate,channels,duration_ts,duration:format=duration:stream_tags=LOOPSTART,LOOPLENGTH:format_tags=LOOPSTART,LOOPLENGTH",
        "-of", "json", str(path),
    ]
    data = json.loads(subprocess.check_output(cmd, text=True))
    stream = (data.get("streams") or [{}])[0]
    fmt = data.get("format") or {}
    tags = {}
    tags.update({k.upper(): v for k, v in (fmt.get("tags") or {}).items()})
    tags.update({k.upper(): v for k, v in (stream.get("tags") or {}).items()})
    sr = int(stream.get("sample_rate") or 44100)
    dur = float(stream.get("duration") or fmt.get("duration") or 0.0)
    samples = int(stream.get("duration_ts") or round(dur * sr))
    return {
        "codec": stream.get("codec_name", "?"),
        "sample_rate": sr,
        "channels": int(stream.get("channels") or 2),
        "duration": dur,
        "samples": samples,
        "loopstart": tags.get("LOOPSTART"),
        "looplength": tags.get("LOOPLENGTH"),
    }


def measure_loudness(path: Path, target_i: float = -14.0, target_tp: float = -1.5, target_lra: float = 11.0) -> dict:
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-af", f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:print_format=json",
        "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    matches = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", proc.stderr, re.S)
    if not matches:
        raise RuntimeError(f"Could not parse loudnorm stats for {path}")
    return json.loads(matches[-1])


def count_pcm_samples(path: Path) -> int:
    """Count exact decoded PCM samples per channel via ffprobe/ffmpeg."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate,duration", "-of", "json", str(path),
    ]
    info = json.loads(subprocess.check_output(cmd, text=True))["streams"][0]
    # Exact sample count by decoding raw s16le mono/stereo byte length
    ch_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=channels", "-of", "default=nw=1:nk=1", str(path),
    ]
    channels = int(subprocess.check_output(ch_cmd, text=True).strip() or "2")
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-fflags", "+genpts", "-i", str(path), "-f", "s16le", "-acodec", "pcm_s16le", "-"],
    )
    return len(raw) // (2 * channels)


def write_loop_tags(ogg_path: Path, loop_start: int, loop_length: int) -> None:
    # Preserve non-loop tags, replace LOOPSTART & LOOPLENGTH cleanly
    existing = subprocess.run(
        ["vorbiscomment", "-l", str(ogg_path)], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    kept = [
        line for line in existing
        if not line.upper().startswith(("LOOPSTART=", "LOOPLENGTH=")) and "=" in line
    ]
    kept.append(f"LOOPSTART={loop_start}")
    kept.append(f"LOOPLENGTH={loop_length}")
    subprocess.run(
        ["vorbiscomment", "-w", "-R", str(ogg_path)],
        input="\n".join(kept) + "\n",
        text=True,
        check=True,
    )


def audit_directory(target: Path) -> None:
    files = sorted(p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS)
    if not files:
        print(f"No audio files found under {target}")
        return
    print(f"{'FILE':<44} {'FMT':<7} {'SR':>6} {'DUR':>6} {'LUFS':>7} {'TP':>6} {'LOOPSTART':>10} {'LOOPLENGTH':>10}")
    print("-" * 104)
    lufs_vals = []
    tagged = 0
    for f in files:
        info = probe_track(f)
        stats = measure_loudness(f)
        in_i = stats.get("input_i", "?")
        in_tp = stats.get("input_tp", "?")
        try:
            lufs_vals.append(float(in_i))
        except ValueError:
            pass
        ls = info["loopstart"] or "-"
        ll = info["looplength"] or "-"
        if info["loopstart"] is not None:
            tagged += 1
        rel = str(f.relative_to(target))
        if len(rel) > 43:
            rel = "…" + rel[-42:]
        print(f"{rel:<44} {info['codec']:<7} {info['sample_rate']:>6} {info['duration']:>5.1f}s {str(in_i):>7} {str(in_tp):>6} {ls:>10} {ll:>10}")
    print("-" * 104)
    if lufs_vals:
        spread = max(lufs_vals) - min(lufs_vals)
        print(f"Total: {len(files)} files | Loop-tagged: {tagged}/{len(files)} | Loudness range: {min(lufs_vals):.1f} to {max(lufs_vals):.1f} LUFS (spread {spread:.1f} dB)")


def master_file(
    src: Path,
    dst: Path,
    target_lufs: float,
    target_tp: float,
    sample_rate: int,
    quality: float,
    full_loop: bool,
    loop_start_sec: float | None,
    loop_end_sec: float | None,
    loop_start_samples: int | None,
    loop_length_samples: int | None,
) -> None:
    stats = measure_loudness(src, target_i=target_lufs, target_tp=target_tp)
    af = (
        f"loudnorm=I={target_lufs}:TP={target_tp}:LRA=11:"
        f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true"
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp_out = Path(td) / "mastered.ogg"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", str(src),
            "-af", af, "-ar", str(sample_rate),
            "-c:a", "libvorbis", "-q:a", str(quality),
            str(tmp_out),
        ], check=True)

        total_samples = count_pcm_samples(tmp_out)
        ls: int | None = None
        ll: int | None = None

        if full_loop:
            ls = 0
            ll = total_samples
        elif loop_start_samples is not None:
            ls = max(0, min(loop_start_samples, total_samples - 1))
            ll = loop_length_samples if loop_length_samples is not None else (total_samples - ls)
        elif loop_start_sec is not None:
            ls = max(0, min(round(loop_start_sec * sample_rate), total_samples - 1))
            if loop_end_sec is not None:
                le = max(ls + 1, min(round(loop_end_sec * sample_rate), total_samples))
                ll = le - ls
            else:
                ll = total_samples - ls

        if ls is not None and ll is not None:
            write_loop_tags(tmp_out, ls, ll)

        shutil.copyfile(tmp_out, dst)

    after = measure_loudness(dst, target_i=target_lufs, target_tp=target_tp)
    info = probe_track(dst)
    print(
        f"[OK] {src.name} -> {dst} | {stats['input_i']} -> {after['input_i']} LUFS (TP {after['input_tp']} dB) | "
        f"{info['sample_rate']} Hz, {total_samples} samples | "
        f"LOOPSTART={info['loopstart'] or '-'} LOOPLENGTH={info['looplength'] or '-'}"
    )


def main() -> None:
    require_tools("ffmpeg", "ffprobe", "vorbiscomment")
    ap = argparse.ArgumentParser(description="Prismfall audio mastering, OGG conversion & mkxp-z loop tagger.")
    ap.add_argument("--audit", type=Path, help="Audit loudness and loop tags for all audio files in a directory.")
    ap.add_argument("input", nargs="?", type=Path, help="Source audio file (.mp3/.wav/.flac/.ogg)")
    ap.add_argument("output", nargs="?", type=Path, help="Destination .ogg file")
    ap.add_argument("--lufs", type=float, default=-14.0, help="Target integrated loudness in LUFS (default: -14.0 BGM, -18.0 BGS, -12.0 SE)")
    ap.add_argument("--tp", type=float, default=-1.5, help="Target true peak dBTP (default: -1.5)")
    ap.add_argument("--sr", type=int, default=44100, help="Output sample rate in Hz (default: 44100)")
    ap.add_argument("--quality", type=float, default=6.0, help="libvorbis VBR quality 0..10 (default: 6.0 ~192kbps)")
    ap.add_argument("--full-loop", action="store_true", help="Tag entire file as seamless loop (LOOPSTART=0, LOOPLENGTH=total_samples)")
    ap.add_argument("--loop-start", type=float, help="Loop start time in seconds")
    ap.add_argument("--loop-end", type=float, help="Optional loop end time in seconds (defaults to end of file)")
    ap.add_argument("--loop-start-samples", type=int, help="Exact LOOPSTART in samples")
    ap.add_argument("--loop-length-samples", type=int, help="Exact LOOPLENGTH in samples")
    args = ap.parse_args()

    if args.audit:
        audit_directory(args.audit)
        return
    if not args.input or not args.output:
        ap.error("Provide either --audit <dir> OR <input> <output>.")
    master_file(
        args.input, args.output,
        target_lufs=args.lufs, target_tp=args.tp, sample_rate=args.sr, quality=args.quality,
        full_loop=args.full_loop,
        loop_start_sec=args.loop_start, loop_end_sec=args.loop_end,
        loop_start_samples=args.loop_start_samples, loop_length_samples=args.loop_length_samples,
    )


if __name__ == "__main__":
    main()
