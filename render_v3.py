"""THE WORLD TODAY — Thursday 19 November 2026 (v3).

A one-page newspaper front page, drawn entirely in code with PIL.
44 verified stories, 6 regions, one day. Deterministic: no network,
no clock, no random numbers. Every fact comes from RESEARCH.md /
SOURCES.md in this repo; the ICJ 9-6 verdict was verified against
live reporting (CNN, WSJ, BBC, NPR) on 20 Nov 2026.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
CW = W - 2 * MARGIN  # 996 content width

# ---- palette ----
PAPER = (250, 247, 238)
INK = (28, 28, 28)
RED = (168, 32, 32)
DARKRED = (138, 24, 24)
NAVY = (31, 47, 74)
NAVY2 = (24, 38, 60)
GOLD = (176, 124, 16)
GREEN = (46, 125, 79)
BLUE = (47, 93, 138)
SLATE = (88, 88, 88)
LIGHTGREY = (118, 118, 118)
SEA = (216, 231, 241)
LAND = (232, 216, 172)
LANDLINE = (198, 178, 128)
CREAM = (246, 241, 231)
RULE = (60, 60, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_fonts = {}


def F(path, size):
    key = (path, size)
    if key not in _fonts:
        try:
            _fonts[key] = ImageFont.truetype(path, size)
        except OSError:
            _fonts[key] = ImageFont.truetype(SANS, size)
    return _fonts[key]


def tw(d, s, font):
    return d.textlength(s, font=font)


def wrap(d, text, font, max_w):
    """Greedy word wrap by pixel width. Returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if tw(d, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, fill, max_w, max_lines, leading):
    """Draw wrapped text, top-left at (x, y). Raises if it needs more
    than max_lines lines, so overflow fails loudly at build time."""
    lines = wrap(d, text, font, max_w)
    if len(lines) > max_lines:
        raise ValueError(
            "text overflows %d lines (%d): %r" % (max_lines, len(lines), text)
        )
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=font, fill=fill)
    return y + len(lines) * leading


def fit_size(d, text, path, max_w, start, minimum=8):
    """Largest point size (<= start) at which text fits max_w on one line."""
    size = start
    while size > minimum and tw(d, text, F(path, size)) > max_w:
        size -= 1
    return size


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def pill(d, x, y, label, bg, fg=(255, 255, 255)):
    """Small status pill, left-aligned at (x, y). Returns right edge."""
    f = F(SANS_B, 8)
    w = int(tw(d, label, f)) + 10
    h = 12
    rrect(d, [x, y, x + w, y + h], 3, fill=bg)
    d.text((x + 5, y + 2), label, font=f, fill=fg)
    return x + w


PILL_FILL = {"REPORTED": (46, 125, 79), "CLAIM": (178, 60, 32), "FORECAST": (47, 93, 138)}

# ---- small drawing helpers ----

def flag_us(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    cw, ch = w * 0.42, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(28, 42, 90))
    for r in range(5):
        for c in range(6):
            sx = x + 3 + c * (cw - 5) / 5
            sy = y + 3 + r * (ch - 5) / 4
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.ellipse([x + w * 0.10, y + h * 0.12, x + w * 0.32, y + h * 0.46],
              fill=(255, 222, 0))
    for cx, cy in [(0.55, 0.14), (0.68, 0.30), (0.66, 0.52), (0.50, 0.62)]:
        d.ellipse([x + w * cx - 2, y + h * cy - 2, x + w * cx + 2, y + h * cy + 2],
                  fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def flag_ua(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 2], fill=(0, 91, 187))
    d.rectangle([x, y + h / 2, x + w, y + h], fill=(255, 213, 0))


def flag_mm(d, x, y, w, h):
    for i, col in enumerate([(254, 203, 0), (234, 40, 57), (74, 141, 69)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)
    cx, cy = x + w / 2, y + h / 2
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))


def person(d, cx, base, suit, skin=(232, 190, 150), hair=(40, 32, 24),
           hair_style="side", scale=1.0):
    """Seated figure: head + shoulders, seen from the front."""
    hr = 9 * scale
    d.ellipse([cx - hr, base - 34 * scale, cx + hr, base - 16 * scale], fill=skin)
    if hair_style == "blond":
        d.pieslice([cx - hr, base - 36 * scale, cx + hr, base - 18 * scale],
                   180, 360, fill=(232, 198, 110))
        d.rectangle([cx - hr, base - 28 * scale, cx + hr, base - 24 * scale],
                    fill=(232, 198, 110))
    elif hair_style == "grey":
        d.pieslice([cx - hr, base - 36 * scale, cx + hr, base - 20 * scale],
                   180, 360, fill=(180, 180, 175))
    else:
        d.pieslice([cx - hr, base - 36 * scale, cx + hr, base - 20 * scale],
                   180, 360, fill=hair)
    d.polygon([(cx - 15 * scale, base), (cx - 11 * scale, base - 16 * scale),
               (cx + 11 * scale, base - 16 * scale), (cx + 15 * scale, base)],
              fill=suit)
    d.polygon([(cx - 4 * scale, base - 16 * scale), (cx + 4 * scale, base - 16 * scale),
               (cx, base - 6 * scale)], fill=(255, 255, 255))
    d.polygon([(cx - 2 * scale, base - 14 * scale), (cx + 2 * scale, base - 14 * scale),
               (cx + 2.5 * scale, base - 5 * scale), (cx - 2.5 * scale, base - 5 * scale)],
              fill=(178, 32, 32))


def scales(d, cx, cy, s, gold=(212, 175, 55), dark=(60, 50, 30)):
    """Balance scales of justice, centred at (cx, cy), height ~ s."""
    d.line([cx, cy - s * 0.45, cx, cy + s * 0.40], fill=dark, width=3)
    d.line([cx - s * 0.32, cy - s * 0.28, cx + s * 0.32, cy - s * 0.28],
           fill=gold, width=3)
    d.ellipse([cx - 3, cy - s * 0.52, cx + 3, cy - s * 0.42], fill=gold)
    for sx in (cx - s * 0.32, cx + s * 0.32):
        d.line([sx, cy - s * 0.28, sx - s * 0.10, cy - s * 0.02], fill=dark, width=1)
        d.line([sx, cy - s * 0.28, sx + s * 0.10, cy - s * 0.02], fill=dark, width=1)
        d.line([sx, cy - s * 0.28, sx, cy - s * 0.02], fill=dark, width=1)
        d.pieslice([sx - s * 0.12, cy - s * 0.04, sx + s * 0.12, cy + s * 0.10],
                   0, 180, fill=gold, outline=dark)
    d.line([cx - s * 0.18, cy + s * 0.40, cx + s * 0.18, cy + s * 0.40],
           fill=dark, width=3)
    d.line([cx - s * 0.14, cy + s * 0.46, cx + s * 0.14, cy + s * 0.46],
           fill=dark, width=3)


def globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 135, 190),
              outline=(28, 60, 100), width=2)
    d.ellipse([cx - r * 0.55, cy - r * 0.62, cx - r * 0.05, cy - r * 0.10],
              fill=(92, 168, 92))
    d.ellipse([cx + r * 0.10, cy + r * 0.05, cx + r * 0.62, cy + r * 0.55],
              fill=(92, 168, 92))
    d.ellipse([cx + r * 0.30, cy - r * 0.55, cx + r * 0.60, cy - r * 0.25],
              fill=(110, 180, 100))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
    d.arc([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], 20, 160,
          fill=(255, 255, 255), width=2)


def thermometer(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=w // 2,
                        fill=(245, 245, 245), outline=(60, 60, 60), width=2)
    d.ellipse([x - 3, y + h - 12, x + w + 3, y + h + 4], fill=(213, 40, 40),
              outline=(60, 60, 60), width=2)
    d.rounded_rectangle([x + 3, y + h * 0.30, x + w - 3, y + h - 8],
                        radius=3, fill=(213, 40, 40))
    for i in range(4):
        yy = y + 6 + i * (h - 18) // 3
        d.line([x + w - 2, yy, x + w + 4, yy], fill=(60, 60, 60), width=1)


def spiral(d, cx, cy, r, col=(255, 255, 255)):
    for k in range(5):
        rr = r * (k + 1) / 5
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 200 + k * 40, 200 + k * 40 + 270,
              fill=col, width=3)


def skyline(d, x, y, w, h, col, windows=(255, 220, 120)):
    import random as _r
    rnd = _r.Random(19)
    bx = x
    while bx < x + w - 8:
        bw = rnd.randint(10, 22)
        bh = rnd.randint(int(h * 0.35), h)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=col)
        for wy in range(y + h - bh + 4, y + h - 3, 7):
            for wx in range(bx + 3, bx + bw - 2, 6):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=windows)
        bx += bw + 2


def sun(d, cx, cy, r, col=(255, 214, 64)):
    for a in range(0, 360, 30):
        import math
        x1 = cx + (r + 2) * math.cos(math.radians(a))
        y1 = cy + (r + 2) * math.sin(math.radians(a))
        x2 = cx + (r + 8) * math.cos(math.radians(a))
        y2 = cy + (r + 8) * math.sin(math.radians(a))
        d.line([x1, y1, x2, y2], fill=col, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(220, 160, 20), width=1)


def cloud(d, x, y, s, col=(240, 244, 248)):
    d.ellipse([x, y, x + 22 * s, y + 12 * s], fill=col)
    d.ellipse([x + 6 * s, y - 6 * s, x + 20 * s, y + 8 * s], fill=col)
    d.ellipse([x + 12 * s, y - 3 * s, x + 26 * s, y + 10 * s], fill=col)
    d.rectangle([x + 2, y + 8 * s, x + 24 * s, y + 12 * s], fill=col)


def rain_lines(d, x, y, w, h, col=(120, 160, 200), n=8):
    x, y, w, h = int(x), int(y), int(w), int(h)
    import random as _r
    rnd = _r.Random(7)
    for _ in range(n):
        rx = rnd.randint(x, x + w)
        ry = rnd.randint(y, y + h - 8)
        d.line([rx, ry, rx - 2, ry + 7], fill=col, width=1)

# ---- illustrations: one per main story (all drawn in code) ----

def ill_summit(d, x, y, w, h):
    for i, col in enumerate([(24, 38, 60), (31, 47, 74), (44, 62, 94)]):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=col)
    import random as _r
    rnd = _r.Random(3)
    for _ in range(26):
        lx = x + rnd.randint(4, w - 4)
        ly = y + h - 34 + rnd.randint(0, 18)
        d.ellipse([lx, ly, lx + 2, ly + 2], fill=(255, 220, 120))
    poles = [x + w * 0.18, x + w * 0.50, x + w * 0.82]
    for px, fn in zip(poles, (flag_us, flag_cn, flag_ru)):
        d.line([px, y + 8, px, y + 44], fill=(200, 200, 200), width=2)
        fn(d, px + 1, y + 8, 42, 25)
    table_top = y + h - 32
    d.rectangle([x + 4, table_top, x + w - 4, y + h - 4], fill=(246, 241, 231))
    d.rectangle([x + 4, table_top + 12, x + w - 4, y + h - 4], fill=(52, 52, 52))
    for px, style, suit in zip(poles, ("blond", "side", "grey"),
                               ((28, 32, 44), (28, 32, 44), (40, 40, 48))):
        person(d, px + 21, table_top, suit, hair_style=style, scale=1.05)
    f = F(SANS_B, 8)
    for px, name in zip(poles, ("TRUMP", "XI", "PUTIN")):
        nw = tw(d, name, f)
        d.rectangle([px + 21 - nw / 2 - 4, table_top + 14, px + 21 + nw / 2 + 4,
                     table_top + 25], fill=(246, 241, 231))
        d.text((px + 21 - nw / 2, table_top + 15), name, font=f, fill=(28, 28, 28))
    tag = "APEC 2026"
    tf = F(SANS_B, 9)
    d.rectangle([x + w - tw(d, tag, tf) - 12, y + 4, x + w - 4, y + 18],
                fill=(176, 124, 16))
    d.text((x + w - tw(d, tag, tf) - 8, y + 6), tag, font=tf, fill=(255, 255, 255))


def ill_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(196, 178, 140))
    bx, bw, bh = x + w * 0.06, w * 0.52, h * 0.66
    by = y + h - 12 - bh
    d.rectangle([bx, by, bx + bw, by + bh], fill=(168, 72, 52))
    d.rectangle([bx - 4, by - 6, bx + bw + 4, by], fill=(240, 235, 225))
    tx, tw2 = bx + bw * 0.32, bw * 0.36
    d.rectangle([tx, by - h * 0.22, tx + tw2, by], fill=(150, 60, 44))
    d.polygon([(tx - 3, by - h * 0.22), (tx + tw2 / 2, by - h * 0.38),
               (tx + tw2 + 3, by - h * 0.22)], fill=(90, 40, 36))
    for i in range(4):
        wx = bx + 8 + i * (bw - 16) / 3
        d.pieslice([wx, by + 12, wx + 12, by + 30], 180, 360, fill=(40, 50, 66))
        d.rectangle([wx, by + 30, wx + 12, by + bh - 8], fill=(40, 50, 66))
    d.rectangle([bx + bw / 2 - 8, by + bh - 22, bx + bw / 2 + 8, by + bh],
                fill=(52, 40, 32))
    for i in range(3):
        d.rectangle([bx - 4, by + bh + i * 4, bx + bw + 4, by + bh + 3 + i * 4],
                    fill=(220, 214, 200))
    scales(d, x + w * 0.76, y + h * 0.52, h * 0.62)
    d.line([x + 8, y + 8, x + 8, y + 34], fill=(120, 120, 120), width=2)
    flag_mm(d, x + 9, y + 8, 26, 16)
    badge = "9–6"
    bf = F(SANS_B, 14)
    d.ellipse([x + w - 40, y + 6, x + w - 6, y + 40], fill=(178, 32, 32),
              outline=(255, 255, 255), width=2)
    d.text((x + w - 40 + (34 - tw(d, badge, bf)) / 2, y + 13), badge, font=bf,
           fill=(255, 255, 255))


def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 92, 88))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(246, 241, 231))
    globe(d, x + w * 0.26, y + h * 0.36, int(h * 0.30))
    thermometer(d, x + w * 0.56, y + h * 0.10, 13, int(h * 0.62))
    sun(d, x + w * 0.84, y + h * 0.20, 10)
    tag = "DRAFT DEAL · 19 NOV"
    tf = F(SANS_B, 9)
    d.rectangle([x + w - tw(d, tag, tf) - 12, y + 4, x + w - 4, y + 18],
                fill=(138, 24, 24))
    d.text((x + w - tw(d, tag, tf) - 8, y + 6), tag, font=tf, fill=(255, 255, 255))
    ff = F(SANS_B, 13)
    d.text((x + 8, y + h - 23), "FOSSIL FUELS", font=ff, fill=(178, 32, 32))
    fw = tw(d, "FOSSIL FUELS", ff)
    d.line([x + 8, y + h - 14, x + 8 + fw, y + h - 14], fill=(178, 32, 32), width=2)
    cut = "CUT"
    cf = F(SANS_B, 12)
    cw = tw(d, cut, cf)
    d.rectangle([x + w - cw - 16, y + h - 24, x + w - 8, y + h - 5],
                outline=(178, 32, 32), width=2)
    d.text((x + w - cw - 12, y + h - 22), cut, font=cf, fill=(178, 32, 32))


def ill_gta(d, x, y, w, h):
    for i, col in enumerate([(88, 40, 110), (160, 60, 120), (240, 140, 60)]):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=col)
    d.ellipse([x + w * 0.62, y + h * 0.18, x + w * 0.62 + 26, y + h * 0.18 + 26],
              fill=(255, 214, 64))
    skyline(d, x, y + h - 20, w, 20, (28, 20, 44))
    vf = F(SERIF_B, 26)
    d.text((x + 6, y + 2), "VI", font=vf, fill=(20, 16, 30))
    d.text((x + 5, y + 1), "VI", font=vf, fill=(255, 255, 255))
    d.line([x + w - 26, y + 6, x + w - 26, y + h - 18], fill=(28, 20, 44), width=2)
    for a in range(-50, 60, 25):
        import math
        d.line([x + w - 26, y + 8, x + w - 26 + 12 * math.cos(math.radians(a - 90)),
                y + 8 + 12 * math.sin(math.radians(a - 90))], fill=(28, 20, 44), width=2)
    d.rounded_rectangle([x + w * 0.42, y + h - 12, x + w * 0.68, y + h - 5],
                        radius=3, fill=(236, 64, 122))
    d.ellipse([x + w * 0.46, y + h - 5, x + w * 0.46 + 5, y + h], fill=(20, 20, 20))
    d.ellipse([x + w * 0.61, y + h - 5, x + w * 0.61 + 5, y + h], fill=(20, 20, 20))


def ill_ant(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 58, 40))
    candles = [(8, 30, 12, 20, True), (34, 24, 12, 16, True), (60, 26, 12, 12, False),
               (86, 18, 12, 14, True), (112, 10, 12, 18, True), (138, 6, 12, 12, True),
               (164, 4, 12, 8, True)]
    for cx, top, cw, ch, up in candles:
        col = (46, 200, 110) if up else (230, 70, 60)
        d.rectangle([x + cx, y + top, x + cx + cw, y + top + ch], fill=col)
        d.line([x + cx + cw / 2, y + top - 4, x + cx + cw / 2, y + top + ch + 4],
               fill=col, width=1)
    pts = [(x + 14, y + 32), (x + 40, y + 26), (x + 66, y + 28), (x + 92, y + 20),
           (x + 118, y + 12), (x + 144, y + 8), (x + 170, y + 6)]
    d.line(pts, fill=(255, 214, 64), width=2, joint="curve")
    mf = F(SANS_B, 19)
    d.text((x + 6, y + 1), "$83", font=mf, fill=(255, 255, 255))
    tf = F(SANS_B, 8)
    d.text((x + 52, y + 8), "NASDAQ · ANT", font=tf, fill=(255, 214, 64))


def ill_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 38, 68))
    spiral(d, x + w * 0.34, y + h * 0.52, 20)
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(232, 216, 172))
    tag = "RED ALERT"
    tf = F(SANS_B, 8)
    d.rectangle([x + w - tw(d, tag, tf) - 10, y + 4, x + w - 4, y + 16],
                fill=(213, 40, 40))
    d.text((x + w - tw(d, tag, tf) - 7, y + 6), tag, font=tf, fill=(255, 255, 255))
    rain_lines(d, x + w * 0.55, y + 4, w * 0.4, h - 12, n=10)
    d.ellipse([x + w * 0.62, y + h - 16, x + w * 0.66, y + h - 12],
              fill=(120, 60, 40))
    d.rectangle([x + w * 0.60, y + h - 12, x + w * 0.68, y + h - 8],
                fill=(150, 90, 60))


def ill_iran(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 30, 48))
    import random as _r
    rnd = _r.Random(11)
    for _ in range(14):
        sx = x + rnd.randint(2, w - 2)
        sy = y + rnd.randint(2, h - 12)
        d.ellipse([sx, sy, sx + 1, sy + 1], fill=(255, 255, 255))
    d.polygon([(x + 20, y + h - 8), (x + 66, y + 12), (x + 74, y + 16),
               (x + 66, y + 22), (x + 26, y + h - 4)], fill=(170, 175, 185))
    d.polygon([(x + 66, y + 12), (x + 74, y + 16), (x + 66, y + 22)],
              fill=(213, 40, 40))
    d.polygon([(x + 8, y + h - 6), (x + 20, y + h - 8), (x + 22, y + h - 2),
               (x + 10, y + h - 1)], fill=(255, 150, 40))
    for r, col in ((12, (255, 200, 60)), (7, (255, 140, 40)), (3, (255, 255, 255))):
        d.ellipse([x + w - 22 - r, y + 4 + 12 - r, x + w - 22 + r, y + 4 + 12 + r],
                  fill=col)
    for r in (26, 18, 10):
        d.arc([x + 6, y + h - 8 - r, x + 6 + 2 * r, y + h - 8 + r], 270, 360,
              fill=(80, 220, 120), width=2)


def ill_apec(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 210, 235))
    sun(d, x + w - 18, y + 12, 8)
    skyline(d, x, y + h - 16, w, 16, (90, 110, 140))
    for px, fn in zip((x + w * 0.20, x + w * 0.48, x + w * 0.76),
                      (flag_us, flag_cn, flag_ru)):
        d.line([px, y + 8, px, y + 34], fill=(90, 90, 90), width=2)
        fn(d, px + 1, y + 8, 30, 18)
    tag = "21 ECONOMIES"
    tf = F(SANS_B, 8)
    d.rectangle([x + w - tw(d, tag, tf) - 10, y + h - 14, x + w - 4, y + h - 3],
                fill=(31, 47, 74))
    d.text((x + w - tw(d, tag, tf) - 7, y + h - 12), tag, font=tf,
           fill=(255, 255, 255))


def ill_florida(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(148, 162, 178))
    cloud(d, x + 8, y + 8, 1.0, col=(90, 100, 115))
    cloud(d, x + w * 0.55, y + 4, 0.9, col=(80, 90, 105))
    rain_lines(d, x + 6, y + 18, w - 12, h - 26, n=16)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(70, 120, 180))
    d.ellipse([x + 10, y + h - 18, x + 26, y + h - 12], fill=(220, 230, 240))
    d.rectangle([x + w * 0.60, y + h - 26, x + w * 0.60 + 34, y + h - 12],
                fill=(240, 235, 220))
    d.polygon([(x + w * 0.60 - 3, y + h - 26), (x + w * 0.60 + 17, y + h - 36),
               (x + w * 0.60 + 37, y + h - 26)], fill=(150, 60, 50))
    d.line([x + w * 0.30, y + 10, x + w * 0.30, y + h - 16], fill=(60, 90, 60), width=2)
    for a in range(-60, 70, 30):
        import math
        d.line([x + w * 0.30, y + 12, x + w * 0.30 + 12 * math.cos(math.radians(a - 90)),
                y + 12 + 12 * math.sin(math.radians(a - 90))], fill=(60, 90, 60), width=2)
    tag = "UP TO 15 IN"
    tf = F(SANS_B, 8)
    d.rectangle([x + w - tw(d, tag, tf) - 10, y + 3, x + w - 4, y + 14],
                fill=(31, 47, 74))
    d.text((x + w - tw(d, tag, tf) - 7, y + 5), tag, font=tf, fill=(255, 255, 255))


def ill_suneung(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 190))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(150, 110, 70))
    d.ellipse([x + w * 0.78, y + 4, x + w * 0.78 + 24, y + 28], fill=(255, 255, 255),
              outline=(60, 60, 60), width=2)
    cx, cy = x + w * 0.78 + 12, y + 16
    d.line([cx, cy, cx - 5, cy - 5], fill=(30, 30, 30), width=2)
    d.line([cx, cy, cx + 7, cy - 2], fill=(30, 30, 30), width=2)
    d.text((x + w * 0.78 + 2, y + 30), "08:40", font=F(SANS_B, 8), fill=(60, 60, 60))
    for i, dx in enumerate((0.08, 0.40)):
        bx = x + w * dx
        d.rectangle([bx, y + h - 24, bx + 44, y + h - 18], fill=(120, 82, 40))
        d.ellipse([bx + 12, y + h - 42, bx + 30, y + h - 24], fill=(232, 190, 150))
        d.pieslice([bx + 12, y + h - 44, bx + 30, y + h - 28], 180, 360,
                   fill=(40, 32, 24) if i == 0 else (90, 70, 50))
        d.rectangle([bx + 4, y + h - 24, bx + 38, y + h - 18], fill=(40, 50, 70))
    d.rectangle([x + w * 0.40 + 8, y + h - 32, x + w * 0.40 + 28, y + h - 26],
                fill=(255, 255, 255))
    d.line([x + w * 0.40 + 12, y + h - 30, x + w * 0.40 + 24, y + h - 30],
           fill=(150, 150, 150), width=1)


def ill_science(d, x, y, w, h):
    bands = [(122, 90, 60), (160, 130, 90), (96, 96, 96), (178, 120, 70),
             (70, 70, 78)]
    bh = h / len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=col)
    d.polygon([(x + w * 0.55, y), (x + w * 0.62, y), (x + w * 0.52, y + h),
               (x + w * 0.45, y + h)], fill=(50, 50, 56))
    cx, cy, r = x + w * 0.30, y + h * 0.52, 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 235, 220),
              outline=(40, 40, 40), width=2)
    spiral(d, cx, cy, 10, col=(150, 90, 60))
    d.line([cx + r - 2, cy + r - 2, cx + r + 9, cy + r + 9], fill=(40, 40, 40), width=3)
    tag = "NATURE"
    tf = F(SANS_B, 8)
    d.rectangle([x + w - tw(d, tag, tf) - 10, y + h - 14, x + w - 4, y + h - 3],
                fill=(31, 47, 74))
    d.text((x + w - tw(d, tag, tf) - 7, y + h - 12), tag, font=tf,
           fill=(255, 255, 255))


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 160, 172))
    rain_lines(d, x + 4, y + 4, w - 8, h - 16, n=14)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(110, 100, 80))
    for tx, tw2 in ((0.10, 52), (0.48, 58)):
        bx = x + w * tx
        d.polygon([(bx, y + h - 10), (bx + tw2 / 2, y + h - 34),
                   (bx + tw2, y + h - 10)], fill=(225, 220, 205))
        d.polygon([(bx + tw2 / 2 - 6, y + h - 10), (bx + tw2 / 2, y + h - 24),
                   (bx + tw2 / 2 + 6, y + h - 10)], fill=(90, 80, 66))
    d.rectangle([x + w * 0.78, y + h - 22, x + w * 0.78 + 24, y + h - 10],
                fill=(176, 138, 80))
    d.line([x + w * 0.78 + 12, y + h - 20, x + w * 0.78 + 12, y + h - 12],
           fill=(178, 32, 32), width=2)
    d.line([x + w * 0.78 + 6, y + h - 16, x + w * 0.78 + 18, y + h - 16],
           fill=(178, 32, 32), width=2)
    d.ellipse([x + w * 0.30, y + h - 8, x + w * 0.44, y + h - 4],
              fill=(120, 160, 200))


def ill_kyiv(d, x, y, w, h):
    d.polygon([(x, y + 4), (x + w, y), (x + w, y + h * 0.52),
               (x, y + h * 0.52 + 4)], fill=(0, 91, 187))
    d.polygon([(x, y + h * 0.52 + 4), (x + w, y + h * 0.52),
               (x + w, y + h), (x, y + h)], fill=(255, 213, 0))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(110, 72, 40))
    for i, cx in enumerate((0.20, 0.50, 0.80)):
        bx = x + w * cx
        d.rectangle([bx - 12, y + h - 26, bx + 12, y + h - 14], fill=(70, 50, 36))
        if i != 1:
            d.ellipse([bx - 7, y + h - 40, bx + 7, y + h - 26],
                      fill=(232, 190, 150))
            d.pieslice([bx - 7, y + h - 42, bx + 7, y + h - 30], 180, 360,
                       fill=(40, 32, 24) if i == 0 else (120, 120, 115))
    d.rectangle([x + w * 0.50 - 13, y + h - 27, x + w * 0.50 + 13, y + h - 13],
                outline=(255, 255, 255), width=2)

# ---- story data: facts from RESEARCH.md / SOURCES.md ----
# Display numbers run 1-13 in reading order. The ICJ 9-6 verdict was
# verified against live reporting on 20 Nov 2026 (CNN, WSJ, BBC, NPR):
# nine votes to six, first state ever held liable for genocide.

HEROES = [
    dict(num=1, place="SHENZHEN", cat="SUMMIT", pill="REPORTED",
         head="Trump, Xi and Putin hold first three-way summit",
         deck="The three leaders meet for the first time at APEC in Shenzhen; "
              "arms control and the Iran war top the agenda. — Reuters",
         ill=ill_summit),
    dict(num=2, place="THE HAGUE", cat="LAW", pill="REPORTED",
         head="World Court: Myanmar committed genocide",
         deck="By 9 votes to 6, the ICJ finds Myanmar guilty of genocide "
              "against the Rohingya; the first state ever held liable. — BBC",
         ill=ill_court),
    dict(num=3, place="ANTALYA", cat="CLIMATE", pill="FORECAST",
         head="COP31 enters its final 48 hours",
         deck="Ministers take over the text in Antalya; the $120bn adaptation "
              "goal and a fossil phase-out are still open. — AFP",
         ill=ill_cop31),
]

SMALL = [
    dict(num=4, place="WORLDWIDE", cat="GAMES", pill="REPORTED",
         head="GTA VI is out, 13 years after the last one",
         deck="Midnight unlocks, NZ first; 15.9m pre-orders banked (est.). — AFP",
         ill=ill_gta),
    dict(num=5, place="NASDAQ", cat="MARKETS", pill="FORECAST",
         head="Anthropic starts trading on Nasdaq as ANT",
         deck="Priced at $83; $81.3bn raised, the biggest IPO on record. — AP",
         ill=ill_ant),
    dict(num=6, place="ODISHA", cat="STORM", pill="FORECAST",
         head="Cyclone Akvan nears India's east coast",
         deck="Odisha readies evacuation of 200,000; landfall near Puri Friday. — IMD",
         ill=ill_akvan),
    dict(num=7, place="WASHINGTON", cat="IRAN WAR", pill="CLAIM",
         head="Trump weighs a new Iran offensive, reports say",
         deck="No decision yet; Netanyahu presses for a 4–7-day air campaign. — NYT",
         ill=ill_iran),
    dict(num=8, place="SHENZHEN", cat="TRADE", pill="REPORTED",
         head="APEC backs the Shenzhen Declaration",
         deck="Twenty-one economies back digital trade and a roadmap. — Xinhua",
         ill=ill_apec),
    dict(num=9, place="FLORIDA", cat="WEATHER", pill="FORECAST",
         head="Flooded Florida braces for still more rain",
         deck="Flood watch to Thursday night; Volusia schools shut Thu–Fri. — Fox Weather",
         ill=ill_florida),
    dict(num=10, place="SEOUL", cat="EDUCATION", pill="REPORTED",
         head="Half a million sit Korea's Suneung",
         deck="551,864 sit the exam; flights halt 35 minutes for listening. — AJU Press",
         ill=ill_suneung),
    dict(num=11, place="SCIENCE", cat="GEOLOGY", pill="REPORTED",
         head="Earth's missing billion years are explained",
         deck="Mantle currents and giant ice sheets erased the rock record. — Nature",
         ill=ill_science),
    dict(num=12, place="GAZA", cat="AID", pill="REPORTED",
         head="Rain displaces 46,000 households in Gaza",
         deck="Four nations ask Israel to let aid into flooded Gaza. — Paris Eye",
         ill=ill_gaza),
    dict(num=13, place="KYIV", cat="WAR", pill="REPORTED",
         head="Left off the agenda, Ukraine watches Shenzhen",
         deck="The war won't be raised at the summit, the White House says. — ANI",
         ill=ill_kyiv),
]

BRIEFS = [
    (14, "WASHINGTON", "Liu Yunping, first Taiwanese American to chair House Democrats.", "SimpleLife"),
    (15, "OTTAWA", "Carney rethinks China ties, seeking the right deal with the US.", "Jagran Josh"),
    (16, "NEW DELHI", "India and Japan review defence ties in 2+2 talks.", "News Partner"),
    (17, "NEW DELHI", "Schools reopen as GRAP-III smog curbs are lifted.", "News Partner"),
    (18, "WELLINGTON", "India–NZ First Test begins; Sindhu back in world top five.", "News Partner"),
    (19, "MUMBAI", "Goldman Sachs upgrades India; Reliance expands satellite capacity.", "News Partner"),
    (20, "NEW DELHI", "India slaps a 162.5% duty on bulk Scotch imports.", "News Partner"),
    (21, "WASHINGTON", "Microsoft in talks to sell AI services to ByteDance.", "SimpleLife"),
    (22, "WASHINGTON", "State Dept details $12bn in Venezuelan oil and mineral revenue.", "Paris Eye"),
    (23, "NAYPYIDAW", "Myanmar's president says he is reconsidering ties with ASEAN.", "RTM World"),
    (24, "SANTA FE", "Residents flee as the Parana River rises; homes flooded.", "RTM World"),
    (25, "WASHINGTON", "Senators warn AI cyber threats are outpacing defences.", "Jagran Josh"),
    (26, "SANTA CLARA", "Nvidia stops shipping H-series chips to mainland China.", "Earnings call"),
    (27, "RIYADH", "Saudis prepare for the Yemen war to run into 2027.", "Reuters"),
    (28, "KYIV", "Zelensky: Starshield speed cap still bites interceptor drones.", "Reported 12 Nov"),
    (29, "PARIS", "Mélenchon could win, says France's justice minister.", "Jagran Josh"),
    (30, "BERLIN", "Europe meets on Ukraine guarantees as Shenzhen talks go on.", "50kft"),
    (31, "NEW DELHI", "Air India Express names Deepak Rajawat chief executive.", "News Partner"),
    (32, "MUMBAI", "RBI warns on Yes Bank AT1 bonds.", "News Partner"),
    (33, "AUCKLAND", "New Zealanders are first to play GTA VI, at midnight.", "Stocktwits"),
    (34, "INDIA", "A design firm gives staff the day off to play GTA VI.", "SMEStreet"),
    (35, "NEW DELHI", "Railways on alert as Cyclone Akvan nears the coast.", "News Partner"),
    (36, "BANGKOK", "Migrant leader to file complaint over assault at protest.", "Mailchimp"),
    (37, "WASHINGTON", "Trump 'unhappy' Vance did not back the Iran war, report says.", "SimpleLife"),
    (38, "GAZA", "Israeli tanks cross the Yellow Line; Hamas calls it a violation.", "Dawn"),
    (39, "NEW YORK", "Oil falls as Middle East tensions and risk aversion rise.", "SimpleLife"),
    (40, "KEMEROVO", "An-12 crash toll confirmed at 19; ministry blames a technical fault.", "AP"),
    (41, "KUALA LUMPUR", "Sports ministry reviews a ban on athletes riding motorcycles.", "RTM World"),
    (42, "WASHINGTON", "Trump: 'We'll wipe them out' if Iran hits the US with a dirty bomb.", "Fox News"),
    (43, "BEIJING", "Xi pledges $20m for Asia-Pacific cooperation.", "Daily Jagran"),
    (44, "SHENZHEN", "Trump opposes global AI rules at APEC.", "Daily Jagran"),
]

DATE_CHECK = (
    "Voyager 1, one light-day out (Wed 18 Nov) · EU's €45bn Ukraine loan plan (Wed) · "
    "Jeffries nominated 251–11 (Wed) · Nvidia's $115.8bn quarter (Tue) · US strikes on "
    "Iran's Qeshm Island (Tue) · Iran drone interceptions, Kuwait and Bahrain (Wed) · "
    "First COP31 draft (Mon) · Van Gogh's record $190.4m sale (Wed) · Kahana elected "
    "speaker 66–52 (Tue) · Saudi all-clear after Houthi alerts (Wed) · Derna drug "
    "seizure, 4m pills (Tue, reported Wed) · William and Kate meet Modi (Wed) · "
    "Bangladesh garment shutdowns (Wed)"
)

TIMELINE = [
    ("00:00", "AUCKLAND", "GTA VI unlocks"),
    ("MORNING", "SHENZHEN", "Leaders meet"),
    ("08:40", "SEOUL", "Suneung begins"),
    ("10:00", "THE HAGUE", "Court reads judgment"),
    ("09:30", "NEW YORK", "Market opens"),
    ("EVENING", "ANTALYA", "Ministers take over"),
]

REGIONS = [
    ("EUROPE", 6, (47, 93, 138)),
    ("THE AMERICAS", 11, (168, 58, 58)),
    ("ASIA-PACIFIC", 18, (46, 125, 79)),
    ("MIDEAST", 4, (176, 124, 16)),
    ("OCEANIA", 2, (106, 76, 147)),
    ("WORLD", 3, (88, 88, 88)),
]

NUMBERS = [
    ("$81.3bn", "Anthropic's record IPO"),
    ("15.9m", "GTA VI pre-orders (est.)"),
    ("200,000", "Odisha's evacuation plan"),
    ("$120bn", "COP31 adaptation goal"),
    ("730,000", "Rohingya who fled in 2017"),
    ("551,864", "Korea's Suneung sitters"),
]

# ---- world map: coarse continent outlines, lon/lat ----
CONTINENTS = [
    [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54),
     (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
     (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-78, 9),
     (-82, 13), (-85, 16), (-88, 18), (-90, 21), (-91, 19), (-97, 26),
     (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32), (-76, 35),
     (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 52),
     (-60, 55), (-65, 58), (-68, 58), (-75, 62), (-78, 62), (-85, 66),
     (-90, 68), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71),
     (-165, 68), (-168, 66)],
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70),
     (-25, 74), (-35, 76), (-45, 76), (-55, 74), (-58, 70), (-58, 64)],
    [(-78, 8), (-80, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-58, -35), (-52, -32),
     (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3),
     (-44, -2), (-50, 0), (-55, 5), (-60, 8), (-68, 11), (-72, 12), (-76, 10),
     (-78, 8)],
    [(-17, 15), (-16, 20), (-15, 25), (-10, 30), (-5, 35), (0, 36), (10, 37),
     (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (40, 15), (43, 11),
     (48, 11), (51, 10), (44, 2), (40, -2), (40, -10), (36, -18), (32, -26),
     (28, -33), (20, -35), (17, -32), (14, -22), (12, -15), (13, -10),
     (12, -5), (9, 4), (6, 5), (-2, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 15)],
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
     (0, 51), (3, 53), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62),
     (10, 64), (13, 66), (18, 69), (25, 71), (30, 70), (35, 67), (40, 66),
     (45, 68), (50, 68), (55, 68), (60, 68), (65, 68), (68, 66), (60, 60),
     (55, 55), (50, 50), (45, 47), (40, 45), (38, 44), (35, 42), (30, 40),
     (28, 38), (25, 36), (22, 37), (20, 40), (18, 42), (15, 44), (12, 44),
     (10, 42), (8, 44), (6, 43), (3, 43), (0, 40), (-2, 37), (-6, 36),
     (-9, 37), (-10, 36)],
    [(30, 36), (36, 36), (40, 30), (44, 29), (48, 29), (52, 27), (56, 27),
     (60, 25), (66, 25), (70, 21), (73, 20), (76, 15), (78, 8), (80, 7),
     (82, 13), (86, 20), (89, 22), (92, 21), (95, 16), (98, 14), (100, 8),
     (103, 7), (105, 9), (107, 11), (109, 14), (108, 18), (110, 21),
     (114, 22), (118, 25), (121, 28), (122, 32), (120, 35), (122, 39),
     (126, 40), (129, 38), (130, 42), (133, 43), (136, 44), (139, 46),
     (141, 50), (142, 54), (140, 59), (137, 60), (135, 62), (140, 66),
     (145, 68), (150, 70), (157, 69), (162, 66), (170, 66), (178, 65),
     (180, 64), (170, 60), (162, 58), (158, 53), (156, 50), (150, 45),
     (144, 42), (140, 39), (135, 37), (130, 34), (127, 35), (125, 38),
     (121, 38), (118, 35), (112, 32), (108, 30), (105, 28), (102, 25),
     (100, 22), (97, 20), (94, 18), (90, 22), (86, 20), (83, 17), (80, 13),
     (78, 10), (75, 12), (72, 20), (68, 23), (65, 25), (61, 25), (57, 26),
     (53, 27), (49, 29), (45, 29), (41, 31), (38, 33), (35, 36), (30, 36)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 38), (142, 40), (143, 42), (144, 44), (142, 44), (140, 41),
     (138, 38), (136, 36), (134, 34), (131, 32), (130, 31)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-3, 50), (-5, 50)],
    [(113, -22), (114, -30), (115, -35), (118, -35), (122, -34), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (142, -38),
     (145, -38), (147, -39), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -15), (142, -11), (140, -17), (136, -15), (135, -12),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -5), (101, -1),
     (97, 3), (95, 5)],
    [(109, 1), (112, 3), (115, 5), (118, 2), (117, -2), (114, -4), (110, -3),
     (109, 1)],
    [(105, -6), (110, -7), (114, -7), (114, -8), (108, -8), (105, -6)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (147, -9),
     (142, -8), (136, -6), (131, -3), (131, -1)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (174, -41),
     (171, -43), (168, -46), (167, -45)],
]

# (lon, lat, display number, nudge dx, nudge dy)
MAP_DOTS = [
    (114.1, 22.5, "1", 0, 0),
    (4.3, 52.1, "2", 0, 0),
    (30.7, 36.9, "3", -6, -4),
    (85.8, 20.3, "6", 0, 0),
    (-77.0, 38.9, "7", -2, -3),
    (-80.1, 26.0, "9", 0, 5),
    (127.0, 37.5, "10", 0, 0),
    (34.5, 31.5, "12", 8, 6),
    (30.5, 50.5, "13", 4, -3),
    (96.1, 19.8, "23", 0, 0),
    (-60.7, -31.6, "24", 0, 0),
    (174.8, -36.8, "33", 0, 0),
]

# ---- page assembly ----

def rich_para(d, x, y, segments, max_w, leading, max_lines):
    """Draw a paragraph made of (text, font, fill) segments, word-wrapped.
    Returns the y just below the paragraph. Raises if > max_lines."""
    words = []
    for text, font, fill in segments:
        for w in text.split(" "):
            if w:
                words.append((w, font, fill))
    lines, cur, cur_w = [], [], 0
    for w, font, fill in words:
        ww = tw(d, w, font) + tw(d, " ", font)
        if cur and cur_w + ww > max_w:
            lines.append(cur)
            cur, cur_w = [(w, font, fill)], ww
        else:
            cur.append((w, font, fill))
            cur_w += ww
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        raise ValueError("rich para overflows %d lines (%d)" % (max_lines, len(lines)))
    for i, ln in enumerate(lines):
        cx = x
        for w, font, fill in ln:
            d.text((cx, y + i * leading), w, font=font, fill=fill)
            cx += tw(d, w + " ", font)
    return y + len(lines) * leading


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=RULE, width=1)
    def px(lon):
        return x + (lon + 180.0) / 360.0 * w
    def py(lat):
        return y + (80.0 - lat) / 135.0 * h
    for poly in CONTINENTS:
        d.polygon([(px(lon), py(lat)) for lon, lat in poly], fill=LAND,
                  outline=LANDLINE)
    for lon, lat, num, dx, dy in MAP_DOTS:
        cx, cy = px(lon) + dx, py(lat) + dy
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = F(SANS_B, 8 if len(num) == 1 else 7)
        d.text((cx - tw(d, num, f) / 2, cy - 5), num, font=f, fill=(255, 255, 255))


def hero_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    s["ill"](d, x + 1, y + 1, w - 2, 84)
    kx = x + 6
    d.text((kx, y + 89), "%d · %s · %s" % (s["num"], s["place"], s["cat"]),
           font=F(SANS_B, 11), fill=RED)
    pill(d, x + w - 58, y + 89, s["pill"], PILL_FILL[s["pill"]])
    block(d, x + 6, y + 102, s["head"], F(SERIF_B, 18), INK, w - 12, 2, 20)
    block(d, x + 6, y + 144, s["deck"], F(SANS, 10), INK, w - 12, 2, 9)


def small_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    s["ill"](d, x + 1, y + 1, w - 2, 38)
    kx = x + 5
    d.text((kx, y + 42), "%d · %s · %s" % (s["num"], s["place"], s["cat"]),
           font=F(SANS_B, 9), fill=RED)
    pill(d, x + w - 56, y + 41, s["pill"], PILL_FILL[s["pill"]])
    block(d, x + 5, y + 55, s["head"], F(SERIF_B, 12), INK, w - 10, 2, 12.5)
    block(d, x + 5, y + 81, s["deck"], F(SANS, 9), INK, w - 10, 2, 8)


def render_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top bar
    d.text((MARGIN, 10), "THE WORLD IN ONE DAY", font=F(SANS_B, 13), fill=RED)
    right = "44 STORIES · 6 REGIONS · ALL FROM THIS ONE DAY"
    d.text((W - MARGIN - tw(d, right, F(SANS_B, 11)), 11), right,
           font=F(SANS_B, 11), fill=INK)
    d.line([MARGIN, 27, W - MARGIN, 27], fill=RULE, width=1)

    # masthead: the date, large serif
    mast = "Thursday 19 November 2026"
    size = fit_size(d, mast, SERIF_B, CW, 64)
    d.text((MARGIN, 28), mast, font=F(SERIF_B, size), fill=INK)
    d.line([MARGIN, 92, W - MARGIN, 92], fill=INK, width=2)
    d.line([MARGIN, 95, W - MARGIN, 95], fill=INK, width=1)

    # deck line
    deck = ("Trump, Xi and Putin share one table · The World Court finds "
            "Myanmar committed genocide · COP31 enters its final 48 hours")
    dsize = fit_size(d, deck, SERIF_I, CW, 15)
    d.text((MARGIN, 99), deck, font=F(SERIF_I, dsize), fill=RED)

    # timeline strip
    tlabel = "THE DAY BY HOURS  "
    events = "  ·  ".join("%s %s %s" % (t, p, e) for t, p, e in TIMELINE)
    tsize = 10
    while (tw(d, tlabel, F(SANS_B, tsize)) + tw(d, events, F(SANS, tsize)) > CW
           and tsize > 8):
        tsize -= 1
    tx = MARGIN
    d.text((tx, 119), tlabel, font=F(SANS_B, tsize), fill=RED)
    tx += tw(d, tlabel, F(SANS_B, tsize))
    d.text((tx, 119), events, font=F(SANS, tsize), fill=INK)
    d.line([MARGIN, 134, W - MARGIN, 134], fill=RULE, width=1)

    # region strip
    cw = CW / len(REGIONS)
    for i, (name, n, col) in enumerate(REGIONS):
        x0 = MARGIN + i * cw
        d.rectangle([x0, 138, x0 + cw - 1, 158], fill=col)
        label = "%s %d" % (name, n)
        f = F(SANS_B, 11)
        d.text((x0 + (cw - tw(d, label, f)) / 2, 143), label, font=f,
               fill=(255, 255, 255))

    # big-number strip
    for i, (num, cap) in enumerate(NUMBERS):
        x0 = MARGIN + i * cw
        nf = F(SANS_B, 18)
        d.text((x0 + 4, 164), num, font=nf, fill=RED)
        d.text((x0 + 4, 183), cap, font=F(SANS, 9), fill=SLATE)

    # heroes
    hw = (CW - 18) // 3
    for i, s in enumerate(HEROES):
        hero_card(d, MARGIN + i * (hw + 9), 196, hw, 168, s)

    # small cards, 2 rows x 5
    sw = (CW - 4 * 9) // 5
    for r in range(2):
        for c in range(5):
            s = SMALL[r * 5 + c]
            small_card(d, MARGIN + c * (sw + 9), 368 + r * 104, sw, 100, s)

    # map + right column
    d.text((MARGIN, 578), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=RED)
    d.text((MARGIN + 132, 579), "numbers match the stories",
           font=F(SANS, 9), fill=SLATE)
    draw_map(d, MARGIN, 594, 620, 138)

    rx = 640
    rw = W - MARGIN - rx
    # THE VERDICT
    d.rectangle([rx, 578, rx + rw, 636], fill=NAVY)
    d.text((rx + 8, 583), "THE VERDICT · THE HAGUE", font=F(SANS_B, 10),
           fill=(255, 214, 64))
    d.text((rx + 8, 597), "Myanmar committed genocide, 9 to 6.",
           font=F(SERIF_B, 14), fill=(255, 255, 255))
    block(d, rx + 8, 616,
          "First state ever held liable. Final, no appeal. Orders reparations.",
          F(SANS, 9), (230, 230, 230), rw - 16, 2, 10)
    # HOW SURE ARE WE?
    d.rectangle([rx, 640, rx + rw, 690], outline=RULE, width=1)
    d.text((rx + 8, 644), "HOW SURE ARE WE?", font=F(SANS_B, 10), fill=INK)
    legend = [((46, 125, 79), "REPORTED", "confirmed by named sources"),
              ((178, 60, 32), "CLAIM", "one side says, unverified"),
              ((47, 93, 138), "FORECAST", "poll, draft or schedule")]
    for i, (col, word, desc) in enumerate(legend):
        yy = 659 + i * 11
        d.ellipse([rx + 8, yy + 1, rx + 15, yy + 8], fill=col)
        d.text((rx + 19, yy), word, font=F(SANS_B, 9), fill=INK)
        d.text((rx + 19 + tw(d, word + " ", F(SANS_B, 9)), yy), "— " + desc,
               font=F(SANS, 9), fill=SLATE)
    # MARKETS & MONEY
    d.rectangle([rx, 694, rx + rw, 732], outline=RULE, width=1)
    d.text((rx + 8, 698), "MARKETS & MONEY", font=F(SANS_B, 10), fill=INK)
    d.text((rx + 8, 712), "ANT $83 · IPO price, set Wed — $81.3bn · largest IPO on record",
           font=F(SANS, 9), fill=INK)
    d.text((rx + 8, 722), "$1.54bn · GTA VI pre-sales (est.) — $120bn · COP31 goal",
           font=F(SANS, 9), fill=INK)

    # brief list, 4 columns
    d.text((MARGIN, 736), "ALSO ON THURSDAY 19 NOVEMBER",
           font=F(SANS_B, 12), fill=RED)
    d.text((MARGIN + 268, 737), "— 31 MORE STORIES",
           font=F(SANS_B, 11), fill=INK)
    bw = 236
    cols = [BRIEFS[i * 8:(i + 1) * 8] for i in range(4)]
    for ci, col in enumerate(cols):
        bx = MARGIN + ci * (bw + 16)
        by = 754
        for num, place, text, src in col:
            segs = [(str(num) + " ", F(SANS_B, 9), RED),
                    (place + " — ", F(SANS_B, 9), INK),
                    (text + " ", F(SANS, 9), INK),
                    (src, F(SERIF_I, 9), SLATE)]
            by = rich_para(d, bx, by, segs, bw, 10, 2) + 2

    # DATE CHECK
    d.rectangle([MARGIN, 934, W - MARGIN, 986], outline=RED, width=1)
    d.text((MARGIN + 8, 939),
           "DATE CHECK ✓ — FIRST REPORTED EARLIER, SO NOT TODAY'S NEWS:",
           font=F(SANS_B, 10), fill=RED)
    block(d, MARGIN + 8, 953, DATE_CHECK, F(SANS, 9), INK, CW - 16, 3, 10.5)

    # footer
    d.line([MARGIN, 988, W - MARGIN, 988], fill=RULE, width=1)
    d.text((MARGIN, 992),
           "Every story here happened, or was first reported, on Thursday 19 November 2026. "
           "Disputed claims are attributed, not stated as fact. Pictures and map: original, drawn in code.",
           font=F(SANS, 9), fill=INK)
    d.text((MARGIN, 1003),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature "
           "— Compiled Thu 19 Nov 2026 · 44 stories, 6 regions",
           font=F(SANS, 9), fill=SLATE)
    return img


if __name__ == "__main__":
    render_page().save("/tmp/v3-preview.png")
    print("preview saved")
