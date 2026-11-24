#!/usr/bin/env python3
"""Build the 23 November 2026 world-news infographic (1024x1024 PNG).

Programmatic drawing with Pillow only: no AI image generation, no network,
no randomness, no clock. The output is fully deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rrect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- icons
def icon_globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 200, 340, fill=color, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 20, 160, fill=color, width=3)


def icon_target(d, cx, cy, r, color):
    for rr, w in ((r, 4), (r * 0.62, 4), (r * 0.26, 0)):
        if w:
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=color, width=w)
        else:
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color)
    d.line([cx - r - 4, cy, cx + r + 4, cy], fill=color, width=3)
    d.line([cx, cy - r - 4, cx, cy + r + 4], fill=color, width=3)


def icon_chip(d, cx, cy, s, color):
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=color)
    d.rectangle([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45, cy + s * 0.45],
                outline="white", width=3)
    for i in (-1, 0, 1):
        d.line([cx + i * s * 0.55, cy - s - 8, cx + i * s * 0.55, cy - s], fill=color, width=4)
        d.line([cx + i * s * 0.55, cy + s, cx + i * s * 0.55, cy + s + 8], fill=color, width=4)
        d.line([cx - s - 8, cy + i * s * 0.55, cx - s, cy + i * s * 0.55], fill=color, width=4)
        d.line([cx + s, cy + i * s * 0.55, cx + s + 8, cy + i * s * 0.55], fill=color, width=4)


def icon_ballot(d, cx, cy, color):
    d.rectangle([cx - 22, cy - 8, cx + 22, cy + 20], outline=color, width=4)
    d.line([cx - 24, cy - 8, cx + 24, cy - 8], fill=color, width=4)
    d.line([cx - 12, cy + 4, cx - 3, cy + 13, cx + 14, cy - 10], fill=color, width=5)


def icon_plane(d, cx, cy, color):
    # Simple paper-plane silhouette.
    d.polygon([(cx - 26, cy + 4), (cx + 26, cy - 14), (cx + 8, cy + 6),
               (cx + 2, cy + 18), (cx - 2, cy + 6)], fill=color)


def icon_flags(d, cx, cy, color):
    d.line([cx - 16, cy - 20, cx - 16, cy + 20], fill=color, width=3)
    d.line([cx + 14, cy - 20, cx + 14, cy + 20], fill=color, width=3)
    d.polygon([(cx - 16, cy - 20), (cx + 2, cy - 20), (cx + 2, cy - 6),
               (cx - 16, cy - 6)], fill=color)
    d.polygon([(cx + 14, cy - 20), (cx + 30, cy - 20), (cx + 30, cy - 6),
               (cx + 14, cy - 6)], outline=color, width=3)


ICONS = {
    "globe": icon_globe, "target": icon_target, "chip": icon_chip,
    "ballot": icon_ballot, "plane": icon_plane, "flags": icon_flags,
}

CARDS = [
    dict(tag="CLIMATE", color=(14, 124, 107), icon="globe",
         headline="Climate summit ends in failure",
         body="COP31 in Turkey collapsed after 49 hours of overtime. "
              "No deal on fossil fuels.",
         pill="1st collapse since 2009"),
    dict(tag="WAR", color=(192, 57, 43), icon="target",
         headline="Ukraine war spreads to Libya",
         body="Kyiv says its drones sank a Russian warship off Libya. "
              "Strikes near Kyiv killed at least 15.",
         pill="15 killed near Kyiv"),
    dict(tag="TECH", color=(30, 142, 62), icon="chip",
         headline="Nvidia brings back its CEO",
         body="Jensen Huang is CEO again after the board changed its "
              "mind. Nvidia shares jumped about 30%.",
         pill="Shares +30%"),
    dict(tag="POLITICS", color=(26, 95, 180), icon="ballot",
         headline="Democrats win big in the House",
         body="Flipping a North Carolina seat gave Democrats 258 House seats, the largest since 1992.",
         pill="258 seats"),
    dict(tag="TRAVEL", color=(108, 63, 181), icon="plane",
         headline="Delta glitch delays 2,000 flights",
         body="A computer failure hit Delta on Thanksgiving Eve. "
              "Crews did the math by hand.",
         pill="~2,000 flights delayed"),
    dict(tag="DIPLOMACY", color=(211, 84, 0), icon="flags",
         headline="Nepal PM's first visit to India",
         body="Balendra Shah met PM Modi in New Delhi. A big new "
              "package of deals was agreed.",
         pill="19 outcomes agreed"),
]

FOOTER = [
    ("S. Korea minister quits", "Resigned over AI cheating fears at the big college exam."),
    ("Factory fire in Indonesia", "A candy factory fire in Banten killed 24 people."),
    ("Houthis hit Saudi refinery", "Yemen's Houthis claim an attack on the Rabigh refinery."),
]

NAVY = (11, 31, 58)
NAVY2 = (16, 45, 84)
GOLD = (212, 175, 55)
BG = (233, 236, 240)
INK = (24, 32, 44)
MUTED = (90, 100, 114)


def draw_card(d, x, y, w, h, card):
    rrect(d, [x, y, x + w, y + h], 14, fill=(255, 255, 255),
          outline=(205, 212, 220), width=1)
    # coloured top bar (clipped look: rounded top via small rect + cover)
    d.rounded_rectangle([x, y, x + w, y + 10], radius=7, fill=card["color"])
    d.rectangle([x, y + 5, x + w, y + 10], fill=card["color"])
    pad = 22
    ix, iy = x + pad + 28, y + 40
    # icon badge
    d.ellipse([ix - 30, iy - 30, ix + 30, iy + 30], fill=card["color"] + (255,))
    # icons draw in white inside badge: temporarily use white
    white = (255, 255, 255)
    name = card["icon"]
    if name == "globe":
        icon_globe(d, ix, iy, 17, white)
    elif name == "target":
        icon_target(d, ix, iy, 16, white)
    elif name == "chip":
        icon_chip(d, ix, iy, 15, white)
    elif name == "ballot":
        icon_ballot(d, ix, iy, white)
    elif name == "plane":
        icon_plane(d, ix, iy, white)
    elif name == "flags":
        icon_flags(d, ix, iy, white)
    # tag next to icon
    f_tag = font(BOLD, 19)
    d.text((x + pad + 68, y + 26), card["tag"], font=f_tag, fill=card["color"])
    # headline
    f_head = font(BOLD, 27)
    lines = wrap(d, card["headline"], f_head, w - 2 * pad)
    ty = y + 82
    for ln in lines[:2]:
        d.text((x + pad, ty), ln, font=f_head, fill=INK)
        ty += 33
    # body
    f_body = font(REG, 19)
    blines = wrap(d, card["body"], f_body, w - 2 * pad)
    by = ty + 6
    for ln in blines[:2]:
        d.text((x + pad, by), ln, font=f_body, fill=(52, 63, 79))
        by += 25
    # data pill
    f_pill = font(BOLD, 18)
    pill = card["pill"]
    pw = d.textlength(pill, font=f_pill) + 28
    py = y + h - 42
    rrect(d, [x + pad, py, x + pad + pw, py + 30], 15, fill=(238, 242, 246))
    d.text((x + pad + 14, py + 5), pill, font=f_pill, fill=card["color"])


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.rectangle([0, 0, W, 6], fill=GOLD)
    d.rectangle([0, 152, W, 158], fill=GOLD)
    # thin gold corner accents
    d.text((32, 22), "WORLD NEWS", font=font(BOLD, 54), fill=(255, 255, 255))
    d.text((32, 92), "MONDAY, 23 NOVEMBER 2026", font=font(BOLD, 30), fill=GOLD)
    f_sub = font(REG, 24)
    sub = "THE DAY IN ONE PAGE"
    sw = d.textlength(sub, font=f_sub)
    d.text((W - 32 - sw, 30), sub, font=f_sub, fill=(176, 190, 208))
    d.text((W - 32 - d.textlength("6 STORIES  •  3 MORE BELOW", font=font(BOLD, 18)),
            96), "6 STORIES  •  3 MORE BELOW", font=font(BOLD, 18), fill=(176, 190, 208))

    # ---- 2x3 grid ----
    margin, gutter = 24, 18
    cw = (W - 2 * margin - gutter) // 2
    ch = 216
    top = 178
    for i, card in enumerate(CARDS):
        row, col = divmod(i, 2)
        x = margin + col * (cw + gutter)
        y = top + row * (ch + gutter)
        draw_card(d, x, y, cw, ch, card)

    # ---- footer ----
    fy = top + 3 * ch + 2 * gutter + 16  # 876
    fh = H - fy - 20  # ~128
    rrect(d, [margin, fy, W - margin, fy + fh], 14, fill=NAVY2)
    d.text((margin + 22, fy + 14), "ALSO TODAY", font=font(BOLD, 20), fill=GOLD)
    col_w = (W - 2 * margin - 44) // 3
    f_t = font(BOLD, 19)
    f_b = font(REG, 17)
    for i, (title, body) in enumerate(FOOTER):
        x0 = margin + 22 + i * col_w
        d.ellipse([x0, fy + 52, x0 + 12, fy + 64], fill=GOLD)
        d.text((x0 + 20, fy + 46), title, font=f_t, fill=(255, 255, 255))
        for j, ln in enumerate(wrap(d, body, f_b, col_w - 24)[:2]):
            d.text((x0, fy + 76 + j * 22), ln, font=f_b, fill=(196, 208, 224))

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
