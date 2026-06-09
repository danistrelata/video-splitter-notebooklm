#!/usr/bin/env python3
"""Split a video file into fixed-length segments (default: 30 minutes)."""

import argparse
import math
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_ffmpeg() -> str:
    if shutil.which("ffmpeg"):
        return "ffmpeg"

    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass

    print(
        "ffmpeg is required but was not found.\n"
        "Install it on PATH, or run: pip install imageio-ffmpeg\n"
        "  winget install Gyan.FFmpeg\n"
        "  choco install ffmpeg",
        file=sys.stderr,
    )
    sys.exit(1)


def get_duration_seconds(video_path: Path, ffmpeg: str) -> float:
    if shutil.which("ffprobe"):
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(video_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return float(result.stdout.strip())

    result = subprocess.run(
        [ffmpeg, "-i", str(video_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    import re

    match = re.search(
        r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)",
        result.stderr,
    )
    if not match:
        raise RuntimeError("Could not determine video duration.")
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"


def split_video(
    input_path: Path,
    segment_minutes: int = 30,
    output_dir: Path | None = None,
) -> list[Path]:
    ffmpeg = resolve_ffmpeg()

    input_path = input_path.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    segment_seconds = segment_minutes * 60
    total_duration = get_duration_seconds(input_path, ffmpeg)
    num_segments = max(1, math.ceil(total_duration / segment_seconds))

    if output_dir is None:
        output_dir = input_path.parent / f"{input_path.stem}_parts"
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    suffix = input_path.suffix or ".mp4"
    created: list[Path] = []

    print(f"Input: {input_path.name}")
    print(f"Duration: {format_timestamp(total_duration)}")
    print(f"Splitting into {num_segments} part(s) of {segment_minutes} minutes\n")

    for index in range(num_segments):
        start = index * segment_seconds
        output_file = output_dir / f"{input_path.stem}_part{index + 1:03d}{suffix}"

        cmd = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-ss",
            str(start),
            "-i",
            str(input_path),
            "-t",
            str(segment_seconds),
            "-c",
            "copy",
            "-avoid_negative_ts",
            "make_zero",
            str(output_file),
        ]

        print(f"[{index + 1}/{num_segments}] {output_file.name}")
        subprocess.run(cmd, check=True)
        created.append(output_file)

    return created


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split a video into segments of a fixed length (default: 30 minutes)."
    )
    parser.add_argument("input", type=Path, help="Path to the input video file")
    parser.add_argument(
        "-m",
        "--minutes",
        type=int,
        default=30,
        help="Length of each segment in minutes (default: 30)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Directory for output files (default: <input_name>_parts next to input)",
    )
    args = parser.parse_args()

    if args.minutes <= 0:
        parser.error("Segment length must be greater than 0 minutes.")

    try:
        created = split_video(args.input, args.minutes, args.output_dir)
    except subprocess.CalledProcessError as exc:
        print(f"ffmpeg failed with exit code {exc.returncode}", file=sys.stderr)
        sys.exit(exc.returncode or 1)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    print(f"\nDone. Created {len(created)} file(s) in {created[0].parent}")


if __name__ == "__main__":
    main()
