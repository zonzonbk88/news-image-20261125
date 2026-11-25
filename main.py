#!/usr/bin/env python3
"""Copy the news-summary image into the harness output directory.

The image itself (entry.png) is the deliverable; this script just places
it where the make.fun harness expects it and verifies the copy, so a
truncated or corrupted write is caught here rather than at judging time.
"""

import os
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

# The image lives next to this script; the harness tells us where to
# put it through $MAKEFUN_OUTPUT_DIR, with a conventional fallback.
SOURCE = Path(__file__).resolve().parent / "entry.png"


def output_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(out_dir) / "entry.png"


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: {SOURCE} not found", file=sys.stderr)
        return 1

    dest = output_path()
    if dest.resolve() == SOURCE.resolve():
        print(f"error: source and destination are the same file ({dest})",
              file=sys.stderr)
        return 1
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Read the bytes once, write them, then re-read the destination to
    # confirm what actually landed on disk.
    data = SOURCE.read_bytes()
    dest.write_bytes(data)

    written = dest.read_bytes()
    if written[: len(PNG_MAGIC)] != PNG_MAGIC:
        print(f"error: {dest} does not start with PNG magic bytes",
              file=sys.stderr)
        return 1
    if len(written) != len(data):
        print(f"error: size mismatch ({len(written)} != {len(data)})",
              file=sys.stderr)
        return 1

    print(f"copied {SOURCE.name} -> {dest} "
          f"({len(data)} bytes written, {len(written)} bytes verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
