#!/usr/bin/env python3
"""THE WORLD TODAY — 19 November 2026 edition (program/v1).

Writes the baked front page to /output/entry.png. Deterministic:
no network, no clock, no randomness — two runs produce byte-identical
output. The image itself is drawn at build time by render.py (PIL);
this program only copies it, exactly like the 18 Nov entry that was
accepted by make.fun.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    if not os.path.exists(SRC):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
