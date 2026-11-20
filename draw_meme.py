#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: a Vice City sunset with make.fun's ghost.

The joke: after 13 years of waiting for GTA 6, launch day is finally here
and the player has called in sick to play it in Vice City -- and got paid
to meme about it on make.fun. The ghost is make.fun's mascot from its
press kit (https://make.fun/press/mark-1024.png), pasted in large so it
stays recognisable when the picture is shrunk to 480 by 480.

Usage: python3 draw_meme.py <ghost-png>  (writes meme.png, 1024x1024)
The finished meme.png is what gets posted on X; the repository's main.ts
only hands in the post's URL (POST.json).
"""

import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sunset():
    """Vertical gradient: orange dusk at the top to purple night below."""
    img = Image.new("RGB", (W, H))
    top, mid, bot = (255, 138, 61), (232, 72, 110), (74, 32, 110)
    px = img.load()
    for y in range(H):
        t = y / H
        c = lerp(top, mid, min(t * 2, 1)) if t < 0.5 else lerp(mid, bot, (t - 0.5) * 2)
        for x in range(W):
            px[x, y] = c
    return img


def sun(d):
    """A big synthwave sun rising behind the ghost."""
    d.ellipse([342, 190, 682, 530], fill=(255, 214, 120))
    for i, y in enumerate(range(430, 530, 14)):
        d.rectangle([342, y, 682, y + 5 + i], fill=(232, 72, 110))


def skyline(d):
    """Dark Vice City towers with lit windows along the bottom."""
    import random
    rnd = random.Random(20)
    x = 0
    while x < W:
        bw = rnd.randint(70, 130)
        top = rnd.randint(690, 830)
        d.rectangle([x, top, x + bw, H], fill=(38, 16, 62))
        for wy in range(top + 18, H - 14, 34):
            for wx in range(x + 12, x + bw - 12, 30):
                if rnd.random() < 0.4:
                    d.rectangle([wx, wy, wx + 12, wy + 16], fill=(255, 214, 120))
        x += bw + rnd.randint(4, 18)


def palm(d, x, y, s):
    """One palm silhouette: curved trunk and drooping fronds."""
    d.line([(x, y), (x + 14 * s, y - 150 * s)], fill=(30, 12, 50), width=int(10 * s))
    cx, cy = x + 14 * s, y - 150 * s
    for ang in (-70, -40, -12, 16, 44, 72):
        import math
        r = math.radians(ang)
        ex, ey = cx + int(95 * s * math.cos(r)), cy + int(55 * s * math.sin(r)) - 20 * s
        d.arc([cx - 95 * s, cy - 60 * s, cx + 95 * s, cy + 40 * s],
              start=ang - 28, end=ang + 28, fill=(30, 12, 50), width=int(7 * s))


def outline_text(d, xy, text, fnt, fill=(255, 255, 255), stroke=(20, 10, 40)):
    d.text(xy, text, font=fnt, fill=fill, anchor="ma",
           stroke_width=7, stroke_fill=stroke)

def main():
    ghost_path = sys.argv[1] if len(sys.argv) > 1 else "ghost-mark.png"
    img = sunset()
    d = ImageDraw.Draw(img)
    sun(d)
    skyline(d)
    palm(d, 60, 1024, 1.0)
    palm(d, 920, 1024, 0.85)

    # The joke, top and bottom, in big outlined type.
    outline_text(d, (512, 44), "13 YEARS WAITING", ImageFont.truetype(SANS_B, 82))
    outline_text(d, (512, 132), "FOR GTA 6", ImageFont.truetype(SANS_B, 82))

    # make.fun's ghost, large in the middle, over the sunset.
    ghost = Image.open(ghost_path).convert("RGBA").resize((430, 430), Image.LANCZOS)
    img.paste(ghost, (297, 330), ghost)
    d = ImageDraw.Draw(img)

    outline_text(d, (512, 782), "CALLED IN SICK FOR LAUNCH DAY",
                 ImageFont.truetype(SANS_B, 52))
    outline_text(d, (512, 846), "AND GOT PAID TO MEME ABOUT IT",
                 ImageFont.truetype(SANS_B, 44))
    outline_text(d, (512, 928), "make.fun", ImageFont.truetype(SANS_B, 46),
                 fill=(255, 214, 120))

    img.save("meme.png", optimize=True)
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
