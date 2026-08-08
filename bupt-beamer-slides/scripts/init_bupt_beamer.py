#!/usr/bin/env python3
"""Create a BUPT Beamer slide project from the bundled template."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "template"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Directory to create or populate.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing template files in the target directory.",
    )
    args = parser.parse_args()

    target = args.target.resolve()
    if not TEMPLATE_DIR.is_dir():
        raise SystemExit(f"template directory not found: {TEMPLATE_DIR}")

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

    print(f"created BUPT Beamer project at {target}")
    print(f"entry: {target / 'slide.tex'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
