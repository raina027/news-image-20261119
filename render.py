#!/usr/bin/env python3
"""Render THE WORLD TODAY — front page for 19 November 2026 (1024x1024).

Build-time script. The graded program is main.py, which only copies the
baked entry.png to /output/entry.png (deterministic, no network).
All 44 stories were verified against live reporting on 19 Nov 2026
(see RESEARCH.md and SOURCES.md). Date hygiene: anything first reported
on an earlier day is NOT presented as 19 Nov news — it goes in the
DATE CHECK box. The ICJ Rohingya outcome is NOT stated (the judgment is
read at 16:00 WIB, after this page was built); only the reading itself
is the news. GTA VI pre-order figures are Sensor Tower ESTIMATES —
Take-Two has disclosed no official numbers.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26                      # margin
CW = W - 2 * M              # 972 content width
PAPER = (253, 252, 246)
INK = (17, 17, 17)
GREY = (90, 90, 84)
RED = (178, 24, 24)
RULE = (17, 17, 17)
SEA_DARK = (16, 32, 62)
LAND = (206, 190, 148)
LAND_EDGE = (140, 125, 90)


def font(name, size):
    cands = {
        "serif_b": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
        "serif": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
        "serif_i": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"],
        "sans_b": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
        "sans": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    }
    for p in cands[name]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ content
DECK_LINE = ("Three leaders meet in Shenzhen. GTA VI unlocks worldwide after "
             "thirteen years. Anthropic starts trading in the biggest IPO on record.")

REGIONS = [
    ("EUROPE", 6, (46, 90, 140)),
    ("THE AMERICAS", 11, (178, 24, 24)),
    ("ASIA-PACIFIC", 18, (30, 120, 90)),
    ("MIDEAST", 4, (200, 130, 30)),
    ("OCEANIA", 2, (90, 60, 140)),
    ("WORLD", 3, (90, 90, 84)),
]

NUMBERS = [
    ("$81.3bn", "raised by Anthropic, a record IPO"),
    ("15.9m", "GTA VI pre-orders banked already"),
    ("200,000", "Odisha's planned evacuation"),
    ("$120bn", "adaptation finance still unresolved"),
    ("730,000", "Rohingya who fled in 2017"),
    ("551,864", "students sitting Korea's Suneung"),
]

HEROES = [
    {"kicker": "1  •  SHENZHEN — SUMMIT",
     "head": "Trump, Xi and Putin hold first three-way summit",
     "deck": ("The three nuclear powers meet at APEC in Shenzhen; arms control "
              "and the Iran war top the agenda."),
     "ill": "trilateral"},
    {"kicker": "2  •  WORLDWIDE — GAMES",
     "head": "GTA VI arrives after a 13-year wait",
     "deck": ("Unlocks at midnight, New Zealand first; an estimated 15.9m "
              "pre-orders banked, worth about $1.54bn."),
     "ill": "gta"},
    {"kicker": "3  •  NASDAQ — MARKETS",
     "head": "Anthropic debuts in the biggest IPO on record",
     "deck": ("Priced at $83 a share, $81.3bn raised; first trade today values "
              "the AI maker at about $1.5tn."),
     "ill": "ipo"},
]

CARDS = [
    {"kicker": "4  •  THE HAGUE — LAW",
     "head": "World Court rules on Myanmar's Rohingya case",
     "deck": ("Judgment read at 10:00; Gambia's case over the 2017 campaign "
              "that drove 730,000 to flee."),
     "ill": "court"},
    {"kicker": "5  •  ANTALYA — CLIMATE",
     "head": "COP31 enters its final 48 hours",
     "deck": ("Ministers take over the text; the $120bn fund and a fossil "
              "'phase out' still open."),
     "ill": "cop"},
    {"kicker": "6  •  ODISHA — STORM",
     "head": "Akvan bears down as 200,000 flee the coast",
     "deck": ("Landfall due Friday, Narsapur–Puri; latest bulletin cuts gusts "
              "to 110 km/h."),
     "ill": "cyclone"},
    {"kicker": "7  •  WASHINGTON — IRAN WAR",
     "head": "Trump weighs a new Iran offensive, reports say",
     "deck": ("NYT: Netanyahu wants a 4–7-day air campaign; Iran calls the "
              "claims baseless."),
     "ill": "iran"},
    {"kicker": "8  •  SHENZHEN — TRADE",
     "head": "APEC backs the Shenzhen Declaration",
     "deck": ("Twenty-one economies back digital trade and a community roadmap; "
              "Putin backs the draft."),
     "ill": "apec"},
    {"kicker": "9  •  FLORIDA — WEATHER",
     "head": "Flooded Florida braces for still more rain",
     "deck": ("Hollywood saw 15 inches overnight; Volusia schools shut Thu–Fri "
              "as more rain looms."),
     "ill": "florida"},
    {"kicker": "10  •  SEOUL — EDUCATION",
     "head": "Half a million sit Korea's Suneung",
     "deck": ("551,864 students; flights halted 35 minutes, the market opens an "
              "hour late."),
     "ill": "suneung"},
    {"kicker": "11  •  SCIENCE — GEOLOGY",
     "head": "Earth's missing billion years are explained",
     "deck": ("Nature study blames mantle currents and ancient ice sheets for "
              "the Great Unconformity."),
     "ill": "geology"},
    {"kicker": "12  •  GAZA — AID",
     "head": "Rain displaces 46,000 households in Gaza",
     "deck": ("40,000 shelters damaged; four nations demand aid access; "
              "150,000 tents wait."),
     "ill": "gaza"},
    {"kicker": "13  •  KYIV — WAR",
     "head": "Left off the agenda, Ukraine watches Shenzhen",
     "deck": ("The war will not be raised at the summit, the White House says; "
              "Kyiv fears a carve-up."),
     "ill": "ukraine"},
]

BRIEFS = [
    (14, "WASHINGTON", "Liu Yunping is the first Taiwanese American to chair the House Democratic Caucus."),
    (15, "OTTAWA", "Carney rethinks China ties, seeking the right deal with the US."),
    (16, "NEW DELHI", "India and Japan review defence ties in 2+2 talks."),
    (17, "NEW DELHI", "Schools reopen as GRAP-III smog curbs are lifted."),
    (18, "WELLINGTON", "India vs New Zealand First Test begins; Sindhu back in badminton's world top five."),
    (19, "MUMBAI", "Goldman Sachs upgrades India to overweight; Reliance expands satellite capacity."),
    (20, "NEW DELHI", "India slaps a 162.5% duty on bulk Scotch imports."),
    (21, "WASHINGTON", "Microsoft in talks to sell AI services to ByteDance; House panel seeks a briefing."),
    (22, "WASHINGTON", "State Dept details $12bn in Venezuelan oil and mineral revenue."),
    (23, "NAYPYIDAW", "Myanmar's president says he is reconsidering ties with ASEAN."),
    (24, "SANTA FE", "Residents flee as the Parana River rises; homes flooded."),
    (25, "WASHINGTON", "Senators warn AI cyber threats are outpacing defences."),
    (26, "SANTA CLARA", "Nvidia stops shipping H-series chips to mainland China."),
    (27, "RIYADH", "Saudis prepare for the Yemen war to run into 2027; coalition chief replaced."),
    (28, "KYIV", "Zelensky: Starshield speed cap still bites interceptor drones."),
    (29, "PARIS", "Mélenchon could win, says France's justice minister."),
    (30, "BERLIN", "Europe meets on Ukraine guarantees as Shenzhen talks go on."),
    (31, "NEW DELHI", "Air India Express names Deepak Rajawat chief executive."),
    (32, "MUMBAI", "RBI warns on Yes Bank AT1 bonds."),
    (33, "AUCKLAND", "New Zealanders are first to play GTA VI, at midnight."),
    (34, "INDIA", "A design firm gives staff the day off to play GTA VI."),
    (35, "NEW DELHI", "Railways on alert as Cyclone Akvan nears the coast."),
    (36, "BANGKOK", "Migrant leader to file complaint over assault at protest."),
    (37, "WASHINGTON", "Trump 'unhappy' Vance did not back the Iran war, report says; Rubio praised in private."),
    (38, "GAZA", "Israeli tanks cross the Yellow Line. IDF: targeted op against a tunnel; Hamas calls it a flagrant violation; 3 killed in strikes."),
    (39, "NEW YORK", "Oil falls as Middle East tensions and risk aversion rise."),
    (40, "KEMEROVO", "Russian An-12 crash toll confirmed at 19; ministry blames a technical fault."),
    (41, "KUALA LUMPUR", "Sports ministry reviews a ban on athletes riding motorcycles."),
    (42, "WASHINGTON", "Trump: 'We'll wipe them out' if Iran hits the US with a dirty bomb."),
    (43, "BEIJING", "Xi pledges $20m for Asia-Pacific cooperation."),
    (44, "SHENZHEN", "Trump opposes global AI rules at APEC."),
]

DATE_CHECK = ("Voyager 1, one light-day (Wed)  •  EU €45bn Ukraine loan (Wed)  •  "
              "Jeffries nominated 251–11 (Wed)  •  Nvidia $115.8bn quarter (Tue)  •  "
              "US strikes on Qeshm Island (Tue)  •  Iran drone interceptions, "
              "Kuwait/Bahrain (Wed)  •  First COP31 draft (Mon)  •  Van Gogh "
              "$190.4m sale (Wed)  •  Kahana elected speaker 66–52 (Tue)  •  Saudi "
              "all-clear (Wed)  •  Derna seizure, 4m pills (Tue)  •  William and "
              "Kate meet Modi (Wed)  •  Bangladesh garment shutdowns (Wed)")

# (label, story no., lon, lat) — dots on the map
DOTS = [
    ("SHENZHEN", 1, 114.1, 22.5), ("KYIV", 13, 30.5, 50.5),
    ("THE HAGUE", 4, 4.3, 52.1), ("ANTALYA", 5, 30.7, 36.9),
    ("ODISHA", 6, 85.8, 20.3), ("WASHINGTON", 7, -77.0, 38.9),
    ("FLORIDA", 9, -80.1, 26.0), ("SEOUL", 10, 127.0, 37.5),
    ("GAZA", 12, 34.5, 31.5), ("NAYPYIDAW", 23, 96.1, 19.8),
    ("SANTA FE", 24, -60.7, -31.6), ("AUCKLAND", 33, 174.8, -36.8),
]

# coarse continent polygons (lon, lat) — same shapes as the 18 Nov edition
NA = [(-168, 65), (-158, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54),
      (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
      (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-79, 9),
      (-81, 13), (-86, 15), (-90, 21), (-97, 26), (-93, 30), (-89, 30),
      (-84, 30), (-81, 26), (-80, 32), (-76, 35), (-74, 40), (-70, 42),
      (-68, 45), (-65, 44), (-60, 47), (-55, 52), (-60, 55), (-65, 58),
      (-68, 58), (-72, 62), (-78, 62), (-82, 66), (-88, 66), (-95, 69),
      (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68), (-168, 66)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70),
             (-20, 74), (-25, 76), (-35, 77), (-50, 76), (-58, 74), (-60, 70)]
SA = [(-79, 9), (-77, 7), (-77, 4), (-80, -3), (-81, -6), (-79, -9),
      (-76, -13), (-72, -18), (-70, -22), (-70, -28), (-72, -33), (-73, -38),
      (-73, -44), (-71, -50), (-68, -52), (-66, -55), (-68, -54), (-65, -48),
      (-64, -42), (-61, -37), (-57, -34), (-52, -32), (-48, -28), (-44, -23),
      (-40, -20), (-38, -15), (-35, -9), (-35, -6), (-38, -4), (-42, -2),
      (-46, 0), (-50, 1), (-53, 4), (-57, 6), (-61, 9), (-65, 11),
      (-70, 12), (-75, 11), (-77, 10)]
AFRICA = [(-17, 15), (-16, 21), (-14, 27), (-9, 31), (-5, 35), (0, 36),
          (9, 37), (11, 34), (15, 32), (20, 32), (25, 32), (30, 31),
          (32, 31), (34, 27), (35, 22), (37, 18), (39, 15), (43, 12),
          (48, 11), (51, 12), (49, 7), (45, 2), (41, -2), (40, -8),
          (40, -14), (38, -18), (35, -23), (33, -26), (30, -29), (27, -33),
          (22, -35), (19, -34), (17, -32), (15, -27), (13, -20), (12, -15),
          (13, -10), (12, -6), (9, -1), (9, 4), (5, 5), (0, 6), (-5, 5),
          (-8, 5), (-12, 8), (-15, 11)]
EURASIA = [(-9, 37), (-9, 43), (-4, 44), (-2, 47), (-4, 48), (-1, 49),
           (1, 51), (3, 53), (7, 55), (8, 57), (10, 59), (6, 60), (5, 62),
           (12, 65), (18, 69), (25, 71), (30, 70), (35, 68), (40, 67),
           (44, 68), (48, 69), (52, 69), (56, 69), (60, 69), (65, 70),
           (70, 72), (75, 73), (80, 73), (85, 74), (90, 75), (95, 76),
           (100, 77), (105, 77), (110, 76), (115, 74), (120, 73), (125, 72),
           (130, 72), (135, 72), (140, 72), (145, 72), (150, 71), (155, 70),
           (160, 69), (165, 67), (170, 66), (178, 65), (178, 62), (170, 60),
           (164, 60), (160, 56), (157, 52), (150, 59), (146, 59), (142, 54),
           (141, 50), (140, 45), (138, 40), (135, 34), (132, 33), (130, 31),
           (127, 32), (124, 30), (121, 28), (119, 25), (116, 23), (112, 22),
           (109, 20), (108, 18), (106, 10), (104, 9), (101, 7), (99, 10),
           (97, 15), (94, 17), (92, 21), (89, 22), (87, 21), (84, 19),
           (81, 16), (80, 13), (77, 8), (75, 11), (73, 16), (70, 20),
           (68, 22), (66, 25), (62, 25), (58, 26), (56, 27), (53, 26),
           (51, 28), (49, 30), (48, 29), (50, 26), (52, 25), (55, 24),
           (57, 22), (59, 22), (58, 20), (55, 17), (52, 15), (48, 14),
           (45, 12), (43, 12), (42, 15), (40, 20), (38, 24), (36, 28),
           (35, 29), (34, 31), (33, 31), (30, 36), (27, 37), (23, 36),
           (21, 38), (19, 40), (18, 40), (16, 38), (15, 40), (12, 44),
           (10, 44), (8, 44), (6, 43), (3, 43), (0, 38), (-1, 37),
           (-4, 36), (-6, 36), (-9, 37)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-4, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 37), (139, 38), (140, 40),
         (141, 42), (142, 44), (144, 44), (145, 42), (142, 40), (140, 36),
         (138, 35), (136, 33), (133, 34), (131, 32)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -6),
           (100, -2), (97, 2)]
BORNEO = [(109, 1), (112, 3), (116, 6), (118, 2), (117, -2), (114, -3), (110, -3)]
JAVA = [(105, -6), (110, -7), (114, -8), (114, -7), (108, -6)]
NEWGUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (147, -9),
             (142, -8), (137, -6), (132, -4)]
AUSTRALIA = [(114, -22), (114, -30), (115, -34), (119, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
             (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
             (118, -20)]
NZ = [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
      (175, -41), (172, -43), (168, -46)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24),
              (45, -25), (43, -21), (44, -17)]
PHILIPPINES = [(120, 18), (122, 17), (122, 14), (121, 11), (123, 10), (121, 13)]
LAND_POLYS = [NA, GREENLAND, SA, AFRICA, EURASIA, UK, JAPAN, SUMATRA, BORNEO,
              JAVA, NEWGUINEA, AUSTRALIA, NZ, MADAGASCAR, PHILIPPINES]


# ---------------------------------------------------------------- illustrations
# Original drawings built from PIL primitives only (no photos, no stock).
def _skyline(dd, x0, y0, w, h, color, seed_heights, lit=True):
    """Row of dark buildings with lit windows."""
    n = len(seed_heights)
    bw = w / n
    for i, hh in enumerate(seed_heights):
        bx = x0 + i * bw
        bh = h * hh
        dd.rectangle([bx, y0 + h - bh, bx + bw - 1, y0 + h], fill=color)
        if lit:
            for wy in range(int(y0 + h - bh + 3), int(y0 + h - 2), 5):
                for wx in range(int(bx + 2), int(bx + bw - 2), 5):
                    if (int(wx) * 7 + int(wy) * 13) % 11 < 4:
                        dd.rectangle([wx, wy, wx + 1, wy + 1],
                                     fill=(255, 214, 120))


def ill_trilateral(w, h):
    im = Image.new("RGB", (w, h), (16, 32, 62))
    dd = ImageDraw.Draw(im)
    _skyline(dd, 0, h - 26, w, 26, (8, 18, 40), [0.5, 0.9, 0.65, 1.0, 0.75, 0.9, 0.55, 1.0, 0.7])
    # three flag poles, left to right: US, China, Russia
    flags = [("us", w * 0.16), ("cn", w * 0.5), ("ru", w * 0.84)]
    for kind, cx in flags:
        dd.line([(cx, 4), (cx, h - 26)], fill=(200, 200, 190), width=2)
        fw, fh = w * 0.13, h * 0.34
        fx, fy = cx + 2, 5
        if kind == "us":
            for i in range(7):
                dd.rectangle([fx, fy + i * fh / 7, fx + fw, fy + (i + 1) * fh / 7],
                             fill=(178, 24, 24) if i % 2 == 0 else (245, 245, 240))
            dd.rectangle([fx, fy, fx + fw * 0.45, fy + fh * 0.55], fill=(30, 50, 110))
            for sx in range(3):
                for sy in range(3):
                    dd.ellipse([fx + 2 + sx * fw * 0.13, fy + 2 + sy * fh * 0.15,
                                fx + 4 + sx * fw * 0.13, fy + 4 + sy * fh * 0.15],
                               fill=(255, 255, 255))
        elif kind == "cn":
            dd.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 32, 32))
            dd.ellipse([fx + 2, fy + 2, fx + 7, fy + 7], fill=(255, 220, 60))
            for sx, sy in [(0.55, 0.15), (0.7, 0.3), (0.7, 0.55), (0.55, 0.7)]:
                dd.ellipse([fx + fw * sx, fy + fh * sy, fx + fw * sx + 3, fy + fh * sy + 3],
                           fill=(255, 220, 60))
        else:
            for i, c in enumerate([(245, 245, 240), (30, 80, 180), (178, 24, 24)]):
                dd.rectangle([fx, fy + i * fh / 3, fx + fw, fy + (i + 1) * fh / 3], fill=c)
    return im


def ill_gta(w, h):
    im = Image.new("RGB", (w, h), (120, 40, 110))
    dd = ImageDraw.Draw(im)
    # sunset bands
    bands = [(150, 60, 130), (200, 90, 90), (240, 140, 70), (250, 190, 110)]
    for i, c in enumerate(bands):
        dd.rectangle([0, i * h / 4, w, (i + 1) * h / 4], fill=c)
    dd.ellipse([w * 0.62, h * 0.08, w * 0.78, h * 0.08 + w * 0.16],
               fill=(255, 236, 180))
    # palm silhouettes
    for px, ph, lean in [(w * 0.12, h * 0.55, -1), (w * 0.30, h * 0.42, 1),
                         (w * 0.88, h * 0.5, -1)]:
        top = (px + lean * 6, h - ph)
        dd.line([(px, h), top], fill=(40, 10, 50), width=3)
        for a in range(-2, 3):
            dd.arc([top[0] - 16, top[1] - 8, top[0] + 16, top[1] + 10],
                   start=200 + a * 28, end=250 + a * 28, fill=(40, 10, 50), width=2)
    _skyline(dd, 0, h - 18, w, 18, (40, 10, 50),
             [0.5, 0.8, 0.6, 1.0, 0.7, 0.9, 0.6, 1.0, 0.75], lit=False)
    return im


def ill_ipo(w, h):
    im = Image.new("RGB", (w, h), (10, 48, 28))
    dd = ImageDraw.Draw(im)
    # candlesticks rising left to right
    xs = [w * f for f in (0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.90)]
    base = h * 0.82
    tops = [h * f for f in (0.62, 0.58, 0.50, 0.52, 0.40, 0.34, 0.20)]
    for x, t in zip(xs, tops):
        up = (x * 3) % 2 < 1
        c = (60, 200, 110) if up else (220, 70, 60)
        dd.line([(x, t - 4), (x, base)], fill=c, width=1)
        dd.rectangle([x - 4, t, x + 4, base - (base - t) * 0.35], fill=c)
    # rising trend line with arrow
    pts = [(xs[i], tops[i] - 6) for i in range(len(xs))]
    dd.line(pts, fill=(255, 255, 255), width=2)
    dd.polygon([(xs[-1] - 6, tops[-1] - 10), (xs[-1] + 6, tops[-1] - 2),
                (xs[-1] - 2, tops[-1] - 12)], fill=(255, 255, 255))
    return im


def ill_court(w, h):
    im = Image.new("RGB", (w, h), (232, 226, 210))
    dd = ImageDraw.Draw(im)
    dd.polygon([(w * 0.08, h * 0.34), (w * 0.5, h * 0.06), (w * 0.92, h * 0.34)],
               fill=(190, 182, 160))
    for i in range(4):
        cx = w * (0.18 + i * 0.21)
        dd.rectangle([cx - 5, h * 0.34, cx + 5, h * 0.82], fill=(245, 242, 232),
                     outline=(150, 142, 120))
    dd.rectangle([0, h * 0.82, w, h * 0.88], fill=(170, 162, 140))
    dd.rectangle([0, h * 0.88, w, h], fill=(150, 142, 120))
    return im


def ill_cop(w, h):
    im = Image.new("RGB", (w, h), (150, 200, 235))
    dd = ImageDraw.Draw(im)
    dd.ellipse([w * 0.68, h * 0.08, w * 0.68 + w * 0.18, h * 0.08 + w * 0.18],
               fill=(255, 170, 40))
    dd.ellipse([0, h * 0.55, w * 0.7, h * 1.5], fill=(60, 140, 80))
    dd.ellipse([w * 0.45, h * 0.68, w * 1.15, h * 1.6], fill=(40, 110, 60))
    return im


def ill_cyclone(w, h):
    im = Image.new("RGB", (w, h), (40, 55, 80))
    dd = ImageDraw.Draw(im)
    cx, cy = w * 0.5, h * 0.52
    for i, r in enumerate(range(4, int(w * 0.42), 5)):
        dd.arc([cx - r, cy - r * 0.75, cx + r, cy + r * 0.75],
               start=20 + i * 55, end=300 + i * 55, fill=(220, 225, 235), width=2)
    dd.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 220, 60))
    dd.rectangle([0, h - 4, w, h], fill=(178, 24, 24))
    return im


def ill_iran(w, h):
    im = Image.new("RGB", (w, h), (12, 20, 44))
    dd = ImageDraw.Draw(im)
    for sx, sy in [(0.1, 0.2), (0.3, 0.1), (0.55, 0.25), (0.8, 0.12), (0.9, 0.35)]:
        dd.ellipse([w * sx, h * sy, w * sx + 2, h * sy + 2], fill=(255, 255, 255))
    # dashed trajectory arc
    for t in range(0, 11):
        a = t / 10
        x = w * (0.08 + a * 0.55)
        y = h * (0.75 - a * 0.45)
        dd.ellipse([x, y, x + 2, y + 2], fill=(255, 200, 80))
    # missile
    dd.polygon([(w * 0.62, h * 0.22), (w * 0.74, h * 0.30), (w * 0.66, h * 0.36),
                (w * 0.58, h * 0.30)], fill=(200, 200, 200))
    dd.polygon([(w * 0.58, h * 0.30), (w * 0.52, h * 0.40), (w * 0.60, h * 0.36)],
               fill=(255, 140, 40))
    return im


def ill_apec(w, h):
    im = Image.new("RGB", (w, h), (120, 180, 225))
    dd = ImageDraw.Draw(im)
    dd.ellipse([w * 0.42, h * 0.10, w * 0.42 + w * 0.16, h * 0.10 + w * 0.16],
               fill=(255, 220, 120))
    _skyline(dd, 0, h - 20, w, 20, (30, 60, 110),
             [0.5, 0.9, 0.65, 1.0, 0.75, 0.9, 0.55, 1.0, 0.7], lit=False)
    return im


def ill_florida(w, h):
    im = Image.new("RGB", (w, h), (120, 140, 165))
    dd = ImageDraw.Draw(im)
    dd.ellipse([w * 0.10, h * 0.08, w * 0.38, h * 0.34], fill=(90, 105, 130))
    dd.ellipse([w * 0.55, h * 0.05, w * 0.85, h * 0.30], fill=(100, 115, 140))
    for x in range(4, w, 12):
        dd.line([(x, h * 0.36), (x - 3, h * 0.58)], fill=(210, 225, 240), width=1)
    dd.rectangle([0, h * 0.60, w, h], fill=(40, 90, 140))
    for x in range(8, w, 22):
        dd.line([(x, h * 0.72), (x + 10, h * 0.72)], fill=(180, 210, 235), width=1)
        dd.line([(x + 4, h * 0.86), (x + 14, h * 0.86)], fill=(180, 210, 235), width=1)
    return im


def ill_suneung(w, h):
    im = Image.new("RGB", (w, h), (245, 238, 220))
    dd = ImageDraw.Draw(im)
    dd.rectangle([w * 0.08, h * 0.14, w * 0.62, h * 0.86], fill=(255, 255, 255),
                 outline=(180, 175, 160))
    for i in range(5):
        dd.line([(w * 0.13, h * (0.28 + i * 0.13)), (w * 0.57, h * (0.28 + i * 0.13))],
                fill=(200, 195, 180), width=1)
    # pencil diagonal
    dd.polygon([(w * 0.62, h * 0.78), (w * 0.92, h * 0.30), (w * 0.96, h * 0.34),
                (w * 0.66, h * 0.82)], fill=(255, 200, 60))
    dd.polygon([(w * 0.92, h * 0.30), (w * 0.97, h * 0.24), (w * 0.96, h * 0.34)],
               fill=(240, 220, 200))
    # clock
    cx, cy, r = w * 0.80, h * 0.72, w * 0.10
    dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
               outline=(60, 60, 60))
    dd.line([(cx, cy), (cx, cy - r * 0.6)], fill=(178, 24, 24), width=1)
    dd.line([(cx, cy), (cx + r * 0.5, cy + r * 0.3)], fill=(17, 17, 17), width=1)
    return im


def ill_geology(w, h):
    im = Image.new("RGB", (w, h), (210, 180, 140))
    dd = ImageDraw.Draw(im)
    bands = [(190, 150, 110), (160, 110, 70), (140, 90, 55), (200, 170, 120),
             (120, 80, 50), (170, 130, 90)]
    for i, c in enumerate(bands):
        dd.rectangle([0, i * h / 6, w, (i + 1) * h / 6], fill=c)
    # fault line
    dd.line([(w * 0.62, 0), (w * 0.58, h)], fill=(60, 40, 25), width=2)
    return im


def ill_gaza(w, h):
    im = Image.new("RGB", (w, h), (130, 135, 140))
    dd = ImageDraw.Draw(im)
    for x in range(4, w, 12):
        dd.line([(x, 2), (x - 3, h * 0.45)], fill=(210, 215, 220), width=1)
    for tx, tw, c in [(0.16, 0.30, (120, 110, 85)), (0.55, 0.34, (100, 95, 80))]:
        dd.polygon([(w * tx, h * 0.92), (w * (tx + tw / 2), h * 0.45),
                    (w * (tx + tw), h * 0.92)], fill=c)
    return im


def ill_ukraine(w, h):
    im = Image.new("RGB", (w, h), (40, 110, 200))
    dd = ImageDraw.Draw(im)
    dd.rectangle([0, h * 0.5, w, h], fill=(255, 210, 60))
    # golden dome silhouette
    bx = w * 0.5
    dd.rectangle([bx - 14, h * 0.42, bx + 14, h], fill=(30, 30, 40))
    dd.ellipse([bx - 10, h * 0.22, bx + 10, h * 0.48], fill=(255, 190, 60))
    dd.line([(bx, h * 0.10), (bx, h * 0.22)], fill=(255, 190, 60), width=2)
    dd.line([(bx - 4, h * 0.14), (bx + 4, h * 0.14)], fill=(255, 190, 60), width=2)
    return im


ILL = {"trilateral": ill_trilateral, "gta": ill_gta, "ipo": ill_ipo,
       "court": ill_court, "cop": ill_cop, "cyclone": ill_cyclone,
       "iran": ill_iran, "apec": ill_apec, "florida": ill_florida,
       "suneung": ill_suneung, "geology": ill_geology, "gaza": ill_gaza,
       "ukraine": ill_ukraine}


# ------------------------------------------------------------------ render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = M

    # ---- top bar
    f_top = font("sans_b", 12)
    d.text((M, y), "THURSDAY, 19 NOVEMBER 2026", font=f_top, fill=INK)
    r = "No. 323  •  44 STORIES  •  6 REGIONS"
    d.text((W - M - d.textlength(r, font=f_top), y), r, font=f_top, fill=INK)
    y += 18
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 6

    # ---- masthead
    f_mast = font("serif_b", 58)
    name = "THE WORLD TODAY"
    d.text(((W - d.textlength(name, font=f_mast)) / 2, y), name,
           font=f_mast, fill=INK)
    y += 68
    f_tag = font("sans", 11)
    tag = "T H E   D A Y ' S   W O R L D   N E W S   —   I N   O N E   P A G E"
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, y), tag, font=f_tag, fill=GREY)
    y += 16
    d.line([(M, y), (W - M, y)], fill=RULE, width=3)
    y += 3
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 7

    # ---- red italic deck line
    f_deck0 = font("serif_i", 13)
    for ln in wrap(d, DECK_LINE, f_deck0, CW):
        d.text((M, y), ln, font=f_deck0, fill=RED)
        y += 17
    y += 3
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6

    # ---- region strip
    seg_w = CW // len(REGIONS)
    f_reg = font("sans_b", 10)
    for i, (label, cnt, color) in enumerate(REGIONS):
        x0 = M + i * seg_w
        x1 = M + (i + 1) * seg_w if i < len(REGIONS) - 1 else W - M
        d.rectangle([x0, y, x1, y + 18], fill=color)
        t = f"{label} {cnt}"
        d.text((x0 + (x1 - x0 - d.textlength(t, font=f_reg)) / 2, y + 4),
               t, font=f_reg, fill=(255, 255, 255))
    y += 18 + 6

    # ---- numbers strip
    col_w = CW // len(NUMBERS)
    f_n = font("serif_b", 16)
    f_nt = font("sans", 8)
    ny = y
    for i, (num, txt) in enumerate(NUMBERS):
        x = M + i * col_w
        d.text((x, ny), num, font=f_n, fill=RED)
        yy = ny + 19
        for ln in wrap(d, txt, f_nt, col_w - 8)[:2]:
            d.text((x, yy), ln, font=f_nt, fill=INK)
            yy += 10
    y = ny + 38
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 7

    # ---- heroes (3 columns, illustrated)
    hcol = (CW - 2 * 14) // 3
    f_hk = font("sans_b", 9)
    f_hh = font("serif_b", 18)
    f_hd = font("serif", 11)
    hero_top = y
    hero_bottom = hero_top
    ILL_H = 46
    for i, s in enumerate(HEROES):
        x = M + i * (hcol + 14)
        yy = hero_top
        img.paste(ILL[s["ill"]](hcol, ILL_H), (x, yy))
        yy += ILL_H + 4
        d.text((x, yy), s["kicker"], font=f_hk, fill=RED)
        yy += 13
        for ln in wrap(d, s["head"], f_hh, hcol)[:2]:
            d.text((x, yy), ln, font=f_hh, fill=INK)
            yy += 20
        yy += 1
        for ln in wrap(d, s["deck"], f_hd, hcol)[:2]:
            d.text((x, yy), ln, font=f_hd, fill=(40, 40, 38))
            yy += 13
        hero_bottom = max(hero_bottom, yy)
        if i < 2:
            d.line([(x + hcol + 7, hero_top), (x + hcol + 7, yy)],
                   fill=(200, 200, 190), width=1)
    y = hero_bottom + 5
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 7

    # ---- small cards: 2 rows x 5 columns, illustrated
    ccol = (CW - 4 * 12) // 5
    f_ck = font("sans_b", 8)
    f_ch = font("sans_b", 10)
    f_cd = font("sans", 9)
    ILL_C = 32
    card_top = y
    for row in range(2):
        yy = card_top + row * 93
        for col in range(5):
            s = CARDS[row * 5 + col]
            x = M + col * (ccol + 12)
            y2 = yy
            img.paste(ILL[s["ill"]](ccol, ILL_C), (x, y2))
            y2 += ILL_C + 3
            d.text((x, y2), s["kicker"], font=f_ck, fill=RED)
            y2 += 11
            for ln in wrap(d, s["head"], f_ch, ccol)[:2]:
                d.text((x, y2), ln, font=f_ch, fill=INK)
                y2 += 12
            for ln in wrap(d, s["deck"], f_cd, ccol)[:2]:
                d.text((x, y2), ln, font=f_cd, fill=GREY)
                y2 += 10
        if row == 0:
            d.line([(M, yy + 89), (W - M, yy + 89)], fill=(220, 220, 210), width=1)
    y = card_top + 2 * 93
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 7

    # ---- map (left) + briefs (right)
    map_w = 430
    brief_x = M + map_w + 14
    brief_w = W - M - brief_x
    f_sec = font("sans_b", 10)
    d.text((M, y), "THE DAY ON THE MAP — 12 PLACES THAT MADE THE NEWS",
           font=f_sec, fill=INK)
    d.text((brief_x, y), "THE REST OF THE DAY — IN BRIEF",
           font=f_sec, fill=INK)
    y += 15
    band_top = y
    map_h = 340
    d.rectangle([M, band_top, M + map_w, band_top + map_h],
                fill=SEA_DARK, outline=(150, 150, 140), width=1)
    lon0, lon1, lat0, lat1 = -170, 190, 78, -58

    def proj(lon, lat):
        return (M + (lon - lon0) / (lon1 - lon0) * map_w,
                band_top + (lat0 - lat) / (lat0 - lat1) * map_h)

    for poly in LAND_POLYS:
        d.polygon([proj(lo, la) for lo, la in poly],
                  fill=LAND, outline=LAND_EDGE)
    f_lab = font("sans_b", 8)
    f_num = font("sans_b", 8)
    OFF = {"SHENZHEN": (8, -14), "KYIV": (-32, -13), "THE HAGUE": (0, 10),
           "ANTALYA": (10, -14), "ODISHA": (-40, 10), "WASHINGTON": (-52, -13),
           "FLORIDA": (-34, 10), "SEOUL": (8, -13), "GAZA": (10, 10),
           "NAYPYIDAW": (8, 10), "SANTA FE": (-30, 10), "AUCKLAND": (-42, 10)}
    for name_, no, lon, lat in DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        ns = str(no)
        d.text((px - d.textlength(ns, font=f_num) / 2, py - 6), ns,
               font=f_num, fill=(255, 255, 255))
        dx, dy = OFF.get(name_, (0, -13))
        lx = min(max(px + dx, M + 2),
                 M + map_w - d.textlength(name_, font=f_lab) - 2)
        d.text((lx, py + dy), name_, font=f_lab, fill=(255, 255, 255))
    # briefs: 2 columns, number in bold red, city in bold ink, rest regular
    bcol = (brief_w - 12) // 2
    f_b = font("sans", 8)
    f_bb = font("sans_b", 8)
    f_bn = font("sans_b", 8)
    col1 = BRIEFS[:16]
    col2 = BRIEFS[16:]
    brief_bottom = band_top
    for ci, col in enumerate((col1, col2)):
        bx = brief_x + ci * (bcol + 12)
        yy = band_top
        for no, city, txt in col:
            num_s = f"{no} "
            city_s = f"{city} — "
            w_num = d.textlength(num_s, font=f_bn)
            w_city = d.textlength(city_s, font=f_bb)
            # first line of txt fits the space after the bold prefix
            words = txt.split()
            first, rest = "", list(words)
            while rest:
                t = (first + " " + rest[0]).strip()
                if d.textlength(t, font=f_b) <= bcol - w_num - w_city:
                    first = t
                    rest.pop(0)
                else:
                    break
            d.text((bx, yy), num_s, font=f_bn, fill=RED)
            d.text((bx + w_num, yy), city_s, font=f_bb, fill=INK)
            d.text((bx + w_num + w_city, yy), first, font=f_b, fill=INK)
            yy += 10
            for ln in wrap(d, " ".join(rest), f_b, bcol)[:1]:
                d.text((bx, yy), ln, font=f_b, fill=INK)
                yy += 10
            yy += 0
        brief_bottom = max(brief_bottom, yy)
    y = max(band_top + map_h, brief_bottom) + 6
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 7

    # ---- DATE CHECK
    f_dc = font("sans_b", 10)
    d.text((M, y), "DATE CHECK — FIRST REPORTED EARLIER, NOT TODAY'S NEWS",
           font=f_dc, fill=RED)
    y += 14
    f_dct = font("sans", 9)
    for ln in wrap(d, DATE_CHECK, f_dct, CW):
        d.text((M, y), ln, font=f_dct, fill=GREY)
        y += 12
    y += 3
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6

    # ---- footer
    f_f = font("sans", 9)
    f1 = ("Every story here happened, or was first reported, on Thursday 19 November 2026. "
          "Disputed claims are attributed, not stated as fact.")
    for ln in wrap(d, f1, f_f, CW):
        d.text((M, y), ln, font=f_f, fill=INK)
        y += 12
    f2 = ("Pre-order figures are Sensor Tower estimates.  Sources: Reuters • AP • AFP • BBC • "
          "The Hindu • ANI • Xinhua • IMD • Nature • Compiled Thu 19 Nov 2026  •  44 stories, 6 regions")
    for ln in wrap(d, f2, f_f, CW):
        d.text((M, y), ln, font=f_f, fill=GREY)
        y += 12
    print("content bottom y =", y, "of", H)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")
