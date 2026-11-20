"""THE WORLD TODAY — Thursday 19 November 2026 (v3).

Entry point for the make.fun program/v1 harness. Renders the front
page from code (see render_v3.py) and writes the PNG to
/output/entry.png, plus a copy next to this file for inspection.
Deterministic: no network, no clock, no randomness. The picture is
built from the verified facts in RESEARCH.md / SOURCES.md.
"""

import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render_v3


def main():
    image = render_v3.render_page()
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    data = buf.getvalue()
    # determinism self-check: render a second time in this process;
    # the bytes must be identical before anything is written.
    image2 = render_v3.render_page()
    buf2 = io.BytesIO()
    image2.save(buf2, format="PNG")
    assert buf2.getvalue() == data, "non-deterministic render"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)
    # Best-effort inspection copy next to this file: the grader runs
    # with a read-only repository, so a failed copy must never fail
    # the run.
    try:
        with open(os.path.join(HERE, "entry.png"), "wb") as fh:
            fh.write(data)
    except OSError:
        pass
    digest = hashlib.sha256(data).hexdigest()
    print("entry.png: %d bytes, sha256 %s" % (len(data), digest))
    print("size: %dx%d" % image.size)


if __name__ == "__main__":
    main()
