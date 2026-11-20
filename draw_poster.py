#!/usr/bin/env python3
"""Draw the news poster for Friday 20 November 2026.

Renders a 1024x1024 newspaper-style front page with one lead story, two
mid stories and three further stories, all first reported on 20 November
2026, using only Pillow and the DejaVu fonts shipped with the system.

Run:
    python3 draw_poster.py            # writes entry.png beside this file
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (18, 22, 30)
NAVY = (13, 32, 56)
NAVY2 = (22, 48, 80)
GOLD = (198, 145, 48)
GOLD_LT = (233, 196, 106)
RULE = (150, 140, 118)
GREY = (84, 90, 100)
RED = (178, 34, 34)
TEAL = (14, 116, 110)
SKY = (37, 99, 180)
ORANGE = (196, 92, 20)
VIOLET = (98, 62, 160)
GREEN = (34, 120, 70)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def para(d, x, y, text, fnt, max_w, fill, leading):
    """Draw wrapped paragraph, return y after last line."""
    for ln in wrap(d, text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, color):
    f = font(FB, 15)
    d.text((x, y), text, font=f, fill=color)
    return y + 22


def stars(d, cx, cy, r, n, color):
    import math
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=color)


def flag_usa(d, x, y, w, h):
    for i in range(13):
        col = (178, 34, 52) if i % 2 == 0 else (240, 240, 240)
        d.rectangle([x, y + i * h / 13, x + w, y + (i + 1) * h / 13], fill=col)
    d.rectangle([x, y, x + w * 0.4, y + h * 7 / 13], fill=(30, 48, 110))
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 6 + c * 13, y + 5 + r * 11,
                       x + 10 + c * 13, y + 9 + r * 11], fill=(255, 255, 255))


def flag_chn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.text((x + 6, y + 2), "\u2605", font=font(FB, 26), fill=(255, 222, 89))
    d.text((x + 34, y + 4), "\u2605", font=font(FB, 13), fill=(255, 222, 89))
    d.text((x + 46, y + 16), "\u2605", font=font(FB, 13), fill=(255, 222, 89))
    d.text((x + 34, y + 30), "\u2605", font=font(FB, 13), fill=(255, 222, 89))
    d.text((x + 18, y + 34), "\u2605", font=font(FB, 13), fill=(255, 222, 89))


def flag_rus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def scales(d, cx, cy, s, color):
    """Simple scales-of-justice icon centred at (cx, cy), size s."""
    d.line([(cx, cy - s), (cx, cy + s)], fill=color, width=4)
    d.line([(cx - s, cy - s + 6), (cx + s, cy - s + 6)], fill=color, width=4)
    for sx in (-1, 1):
        bx = cx + sx * s
        d.line([(bx, cy - s + 6), (bx, cy + 2)], fill=color, width=3)
        d.polygon([(bx - s * 0.45, cy + 2), (bx + s * 0.45, cy + 2),
                   (bx, cy + s * 0.7)], fill=color)
    d.ellipse([cx - 6, cy + s - 4, cx + 6, cy + s + 4], fill=color)


def cyclone(d, cx, cy, r, color):
    import math
    for k in range(3):
        pts = []
        for t in range(0, 200):
            a = t / 200 * 3.4 * math.pi + k * 2.1
            rr = r * (1 - t / 260)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.85))
        d.line(pts, fill=color, width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=color)


def probe(d, cx, cy, color):
    """Voyager-like probe: dish, body, boom, RTG fins."""
    d.ellipse([cx - 34, cy - 30, cx + 34, cy + 6], outline=color, width=4)
    d.line([(cx - 34, cy - 12), (cx, cy + 2)], fill=color, width=3)
    d.line([(cx + 34, cy - 12), (cx, cy + 2)], fill=color, width=3)
    d.rectangle([cx - 10, cy - 2, cx + 10, cy + 16], fill=color)
    d.line([(cx + 10, cy + 8), (cx + 52, cy + 26)], fill=color, width=3)
    for i in range(3):
        d.line([(cx + 30 + i * 7, cy + 16 + i * 3),
                (cx + 30 + i * 7, cy + 30 + i * 3)], fill=color, width=3)
    d.line([(cx - 10, cy + 8), (cx - 52, cy + 30)], fill=color, width=3)


def asteroid(d, cx, cy, r, color):
    pts = [(cx - r, cy - 6), (cx - r * 0.5, cy - r), (cx + r * 0.4, cy - r * 0.8),
           (cx + r, cy - 6), (cx + r * 0.7, cy + r * 0.6), (cx - r * 0.3, cy + r),
           (cx - r * 0.9, cy + r * 0.4)]
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.4, cy - r * 0.3, cx - r * 0.1, cy], fill=(90, 80, 70))
    d.ellipse([cx + r * 0.2, cy + r * 0.2, cx + r * 0.45, cy + r * 0.45],
              fill=(90, 80, 70))


def controller(d, cx, cy, color):
    d.rounded_rectangle([cx - 46, cy - 22, cx + 46, cy + 26], radius=18,
                        fill=color)
    d.line([(cx - 30, cy - 4), (cx - 30, cy + 12)], fill=PAPER, width=5)
    d.line([(cx - 38, cy + 4), (cx - 22, cy + 4)], fill=PAPER, width=5)
    for bx, by in ((26, -6), (36, 4), (26, 12), (16, 4)):
        d.ellipse([cx + bx - 4, cy + by - 4, cx + bx + 4, cy + by + 4],
                  fill=PAPER)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # ---- Masthead ----
    d.rectangle([10, 10, W - 11, 118], fill=NAVY)
    d.text((512, 26), "THE WORLD IN ONE DAY", font=font(SB, 52),
           fill=(255, 255, 255), anchor="ma")
    d.line([(40, 92), (984, 92)], fill=GOLD, width=2)
    d.text((512, 98), "FRIDAY  \u2022  20 NOVEMBER 2026  \u2022  THE DAY'S NEWS IN A SINGLE IMAGE",
           font=font(FB, 16), fill=GOLD_LT, anchor="ma")

    # ---- Lead story: the three-way summit ----
    ly, lh = 132, 300
    d.rectangle([22, ly, 1002, ly + lh], outline=NAVY2, width=2)
    d.rectangle([22, ly, 1002, ly + lh], fill=(255, 255, 255))
    # Left: text.
    tx, tw = 44, 520
    y = ly + 16
    y = kicker(d, tx, y, "THE BIG MEETING  \u2014  SHENZHEN, CHINA", RED)
    y = para(d, tx, y + 4, "TRUMP, XI AND PUTIN",
             font(SB, 38), tw, INK, 42)
    y = para(d, tx, y, "SIT DOWN TOGETHER",
             font(SB, 38), tw, INK, 42)
    y = para(d, tx, y + 8,
             "First-ever three-way summit at the APEC meeting \u2014 "
             "nuclear risks, energy and the wars on the table.",
             font(FR, 19), tw, GREY, 25)
    y = para(d, tx, y + 6,
             "Trump: no rush on Iran \u2014 the war decision waits until "
             "2027.",
             font(FB, 18), tw, NAVY2, 24)
    # Right: three flags, captions, and a small globe.
    gx0, gy0, gx1, gy1 = 600, ly + 16, 984, ly + lh - 16
    fw, fh = 104, 64
    flag_usa(d, 622, gy0 + 8, fw, fh)
    flag_chn(d, 740, gy0 + 8, fw, fh)
    flag_rus(d, 858, gy0 + 8, fw, fh)
    for fx in (622, 740, 858):
        d.rectangle([fx, gy0 + 8, fx + fw, gy0 + 8 + fh], outline=INK, width=1)
    d.text((803, gy0 + 88), "USA  \u2022  CHINA  \u2022  RUSSIA",
           font=font(FB, 15), fill=NAVY2, anchor="ma")
    d.text((803, gy0 + 112), "One table. Three nuclear powers.",
           font=font(FR, 15), fill=GREY, anchor="ma")
    # Small globe: blue disc with meridian and latitude lines.
    gcx, gcy, gr = 803, gy0 + 196, 44
    d.ellipse([gcx - gr, gcy - gr, gcx + gr, gcy + gr], fill=(176, 216, 240),
              outline=SKY, width=2)
    d.ellipse([gcx - gr * 0.45, gcy - gr, gcx + gr * 0.45, gcy + gr],
              outline=SKY, width=2)
    d.line([(gcx - gr, gcy), (gcx + gr, gcy)], fill=SKY, width=2)
    d.arc([gcx - gr, gcy - gr // 2, gcx + gr, gcy + gr // 2], 0, 360,
          fill=SKY, width=2)

    # ---- Row 2: two half-width stories ----
    ry, rh = 448, 218
    # ICJ verdict.
    d.rectangle([22, ry, 500, ry + rh], outline=NAVY2, width=2)
    d.rectangle([22, ry, 500, ry + rh], fill=(255, 255, 255))
    y = ry + 14
    y = kicker(d, 42, y, "THE VERDICT  \u2014  THE HAGUE", TEAL)
    y = para(d, 42, y + 2, "World court: Myanmar",
             font(SB, 27), 300, INK, 31)
    y = para(d, 42, y, "committed genocide",
             font(SB, 27), 300, INK, 31)
    para(d, 42, y + 6,
         "ICJ rules 9\u20136: the 2017 crackdown on the Rohingya was "
         "genocide \u2014 a first for the court.",
         font(FR, 16), 300, GREY, 21)
    scales(d, 420, ry + 108, 42, TEAL)
    # Cyclone Akvan.
    d.rectangle([524, ry, 1002, ry + rh], outline=NAVY2, width=2)
    d.rectangle([524, ry, 1002, ry + rh], fill=(255, 255, 255))
    y = ry + 14
    y = kicker(d, 544, y, "THE STORM  \u2014  INDIA", ORANGE)
    y = para(d, 544, y + 2, "Cyclone Akvan:",
             font(SB, 27), 300, INK, 31)
    y = para(d, 544, y, "300,000 evacuated",
             font(SB, 27), 300, INK, 31)
    para(d, 544, y + 6,
         "Severe storm bears down on Odisha; 423 rescue teams deployed "
         "as heavy rain begins on the east coast.",
         font(FR, 16), 300, GREY, 21)
    cyclone(d, 920, ry + 112, 52, ORANGE)

    # ---- Row 3: three stories ----
    ty, th = 682, 212
    cols = [(22, 348), (360, 686), (698, 1002)]
    stories = [
        ("SPACE", SKY, "Voyager 1 passes a light-day from Earth",
         "NASA confirms the probe\u2019s milestone, 48 years after launch \u2014 "
         "the farthest human-made object ever.", "probe"),
        ("CULTURE", VIOLET, "GTA VI outsells The Odyssey",
         "Sales pass $1.8 billion \u2014 the biggest entertainment launch "
         "in history, days after release.", "controller"),
        ("SCIENCE", GREEN, "Hayabusa2 gives up its asteroid landing",
         "Engine trouble forces Japan\u2019s probe to change course; "
         "the touchdown is off.", "asteroid"),
    ]
    for (x0, x1), (tag, col, head, body, icon) in zip(cols, stories):
        d.rectangle([x0, ty, x1, ty + th], outline=NAVY2, width=2)
        d.rectangle([x0, ty, x1, ty + th], fill=(255, 255, 255))
        y = ty + 12
        y = kicker(d, x0 + 18, y, tag, col)
        y = para(d, x0 + 18, y + 2, head, font(SB, 21), x1 - x0 - 36,
                 INK, 25)
        para(d, x0 + 18, y + 4, body, font(FR, 14), x1 - x0 - 36, GREY, 19)
        cx = (x0 + x1) // 2
        if icon == "probe":
            probe(d, cx, ty + th - 34, SKY)
            stars(d, x0 + 40, ty + th - 40, 16, 5, GOLD)
            stars(d, x1 - 40, ty + th - 56, 12, 4, GOLD)
        elif icon == "controller":
            controller(d, cx, ty + th - 36, VIOLET)
        else:
            asteroid(d, cx, ty + th - 30, 26, (120, 108, 92))
            stars(d, x0 + 44, ty + th - 44, 12, 4, GOLD)

    # ---- Footer ticker ----
    fy = 910
    d.rectangle([22, fy, 1002, 988], fill=NAVY)
    d.text((512, fy + 12), "ALSO TODAY", font=font(FB, 15), fill=GOLD_LT,
           anchor="ma")
    para(d, 44, fy + 36,
         "Europe ready for talks with Russia on ending the Ukraine war  \u2022  "
         "India v New Zealand: Nicholls 113* in Wellington  \u2022  Anthropic "
         "valued at $1.5 trillion  \u2022  World Children\u2019s Day",
         font(FR, 15), 936, (230, 235, 240), 20)

    d.text((512, 996), "All stories first reported Friday 20 November 2026  \u2022  "
           "Drawn from the day\u2019s news, no photographs",
           font=font(FR, 13), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    draw()
