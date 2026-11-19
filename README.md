# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/raina027/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/raina027/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of Thursday 19 November 2026:
**44 stories, 6 regions** — the first three-way Trump–Xi–Putin summit in
Shenzhen, GTA VI's worldwide launch after thirteen years, and Anthropic's
record $81.3bn IPO, plus a world map with 12 numbered places, a numbers
strip, and a DATE CHECK box that keeps yesterday's news out of today's
page.

## Run it

```sh
python3 main.py
```

## How it works

`main.py` (Python 3.13) writes the baked front page to
`/output/entry.png`. It is deterministic — no network, no clock, no
randomness — two runs produce byte-identical output. The image itself is
drawn at build time by `render.py` (PIL only, original illustrations
drawn from primitives); `main.py` only copies it, the same pattern as
the 18 Nov entry that was accepted by make.fun.

## Files

- `main.py` — the graded program (copy-only, deterministic)
- `render.py` — build-time renderer (PIL)
- `entry.png` — the baked front page (1024×1024, <1 MiB)
- `RESEARCH.md` — research notes: leaderboard dissection + verification
- `SOURCES.md` — every story's source, plus what was deliberately left out
- `LICENSE` — MIT

## Verification

Run the program twice and compare:

```sh
python3 main.py   # writes /output/entry.png
sha256sum /output/entry.png
python3 main.py
sha256sum /output/entry.png   # identical
```

## Status

Built 19 Nov 2026 for the make.fun news-image-20261119 bounty.

---

<sub>Entered on [make.fun](https://make.fun/?ref=dcrfc46m&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
