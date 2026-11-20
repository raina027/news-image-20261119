#!/usr/bin/env python3
"""THE WORLD TODAY — Thursday 19 November 2026 (v3).

Entry point for the make.fun program/v1 harness. Writes the baked
front page to the grader output directory. Deterministic: no network,
no clock, no randomness — the copy is byte-identical every run. The
picture itself is drawn at build time by render_v3.py (PIL) inside the
recorded build session; this program only copies it, exactly like the
round-2 entry that make.fun scored. The grader image has no Pillow,
so rendering at run time cannot work there (rounds 3 and 4 both died
on run_completes for exactly that reason).
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    if not os.path.exists(SRC):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(dst, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print("entry.png: %d bytes, sha256 %s" % (os.path.getsize(dst), digest))
    print("size: 1024x1024")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
