#!/usr/bin/env python3
"""Create a Chinese math book LaTeX project from the bundled template.

Also generates a placeholder cover.png (solid-color) so the template
compiles out of the box. Replace cover.png with a real cover later.
"""

from __future__ import annotations

import argparse
import shutil
import struct
import zlib
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "template"

# Cover placeholder color (matches template's "main" color #3D445F)
COVER_RGB = (0x3D, 0x44, 0x5F)
COVER_SIZE = (800, 1200)  # width, height (px), roughly A4 portrait ratio


def _make_png(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    """Build a minimal solid-color PNG using only the standard library."""
    r, g, b = rgb
    # One row: filter byte 0 (None) + width pixels of RGB
    row = b"\x00" + bytes((r, g, b)) * width
    raw = row * height

    def chunk(tag: bytes, data: bytes) -> bytes:
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Directory to create or populate.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing template files in the target directory.",
    )
    parser.add_argument(
        "--skip-cover",
        action="store_true",
        help="Do not generate a placeholder cover.png.",
    )
    args = parser.parse_args()

    if not TEMPLATE_DIR.is_dir():
        raise SystemExit(f"template directory not found: {TEMPLATE_DIR}")

    target = args.target.resolve()
    target.mkdir(parents=True, exist_ok=True)

    for src in TEMPLATE_DIR.iterdir():
        dst = target / src.name
        if dst.exists():
            if not args.force:
                raise SystemExit(f"target already exists: {dst}; rerun with --force to overwrite")
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    if not args.skip_cover:
        cover = target / "cover.png"
        if not cover.exists() or args.force:
            cover.write_bytes(_make_png(*COVER_SIZE, COVER_RGB))
            print(f"generated placeholder cover: {cover}")

    print(f"created Chinese math book LaTeX project at {target}")
    print(f"entry: {target / 'main.tex'}")
    print("compile: cd <target> && xelatex main.tex && xelatex main.tex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
