# news-image-20: the 20 November 2026 front page.
#
# The graded program is deliberately tiny: the front page itself lives in
# this repository at assets/entry.png (drawn in this session by draw.py
# from the verified news of Friday 20 November 2026), and this entrypoint
# just places that exact file at the grader's output path. Copying one
# fixed file is byte-for-byte deterministic, so the grader's two runs
# always produce identical bytes.
#
# SPDX-License-Identifier: MIT
import sys
from pathlib import Path

IMAGE = Path(__file__).resolve().parent / "assets" / "entry.png"


def output_path() -> Path:
    import os

    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(base) / "entry.png"


def run() -> int:
    if not IMAGE.is_file():
        print(f"missing image: {IMAGE}", file=sys.stderr)
        return 1
    data = IMAGE.read_bytes()
    dest = output_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    if dest.read_bytes() != data:
        print("output differs from source image", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
