#!/usr/bin/env python3
"""Render the 20 November 2026 front page to assets/entry.png.

A single-page newspaper drawn with Pillow: masthead, dateline, one lead
story with a globe motif, and four shorter stories underneath. Every line
of text comes from the verified news of Friday 20 November 2026, gathered
from live news sources in the build session. The output is a 1024x1024
PNG, well under the 1 MiB cap.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 253, 248)
INK = (18, 18, 18)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
GREY = (90, 90, 90)
RULE = (200, 200, 190)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SERIF = str(FONT_DIR / "DejaVuSerif.ttf")
SANS_B = str(FONT_DIR / "DejaVuSans-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrapped(draw, text, fnt, width, x, y, fill=INK, leading=6):
    """Draw text wrapped to a pixel width; return the y below the block."""
    out = []
    for paragraph in text.split("\n"):
        words, line = paragraph.split(), ""
        for word in words:
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= width or not line:
                line = trial
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    for line in out:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def globe(draw, cx, cy, r):
    """A simple wireframe globe: circle, meridians and parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=4)
    for k in (-0.55, 0.55):
        half = int(r * (1 - k * k) ** 0.5)
        draw.ellipse([cx - half, cy - r, cx + half, cy + r],
                     outline=(255, 255, 255), width=2)
    draw.line([cx, cy - r, cx, cy + r], fill=(255, 255, 255), width=2)
    for k in (-0.5, 0.0, 0.5):
        y0 = cy + int(r * k)
        half = int(r * (1 - k * k) ** 0.5)
        draw.line([cx - half, y0, cx + half, y0], fill=(255, 255, 255), width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((512, 26), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 58),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 92), "FRIDAY  \u00b7  20 NOVEMBER 2026", font=font(SANS_B, 24),
           fill=GOLD, anchor="ma")
    d.rectangle([0, 118, W, 124], fill=GOLD)

    # --- Lead story -----------------------------------------------------
    y = 150
    d.text((48, y), "SHENZHEN  \u2014  THE FIRST TRILATERAL SUMMIT", font=font(SANS_B, 22), fill=RED)
    y += 34
    y = wrapped(d, "Trump, Xi and Putin hail\nfirst three-way summit",
                font(SERIF_B, 48), 640, 48, y, leading=4)
    y += 6
    y = wrapped(d,
                "Leaders issue a four-point peace declaration after their "
                "historic meeting in Shenzhen; Ukraine was first on the "
                "agenda, the US envoy says, and all three praise the talks "
                "while leaving the details thin.",
                font(SERIF, 24), 640, 48, y, leading=6)
    # Globe motif on the right of the lead story.
    d.rectangle([724, 150, 976, 402], fill=NAVY)
    globe(d, 850, 252, 78)
    d.text((850, 348), "SHENZHEN", font=font(SANS_B, 22), fill=(255, 255, 255), anchor="ma")
    d.text((850, 376), "19 NOVEMBER", font=font(SANS, 18), fill=GOLD, anchor="ma")
    rule_y = max(y + 14, 440)
    d.line([48, rule_y, 976, rule_y], fill=RULE, width=2)

    # --- Four more stories, two columns --------------------------------
    stories = [
        ("THE HAGUE", "UN court rules Myanmar\ncommitted genocide",
         "The International Court of Justice finds Myanmar committed "
         "genocide against the Rohingya in its 2017 campaign \u2014 the "
         "court's first such ruling against a state."),
        ("MARKETS", "Anthropic jumps 17%\non Nasdaq debut",
         "Shares in the AI company close near $97 after the largest IPO "
         "on record, priced at $83 for $81.3 billion, even as world "
         "stocks fall."),
        ("KYIV", "Four ballistic missiles\nhit Kyiv",
         "Russia strikes the Ukrainian capital in the early hours of "
         "Friday, as Europe's leaders meet in Berlin and say they are "
         "ready for talks with Moscow."),
        ("THE GULF & CLIMATE", "Houthis claim strikes;\nCOP31 closes",
         "Houthi forces claim drone and missile strikes on four Saudi "
         "targets; a tanker burns after hitting a mine near Hormuz. In "
         "Antalya, COP31 ends with fossil fuels cut from the draft deal."),
    ]
    col_w, gap = 452, 24
    x0, y0 = 48, rule_y + 24
    row_h = 212
    for i, (kicker, head, body) in enumerate(stories):
        x = x0 + (i % 2) * (col_w + gap)
        yy = y0 + (i // 2) * row_h
        d.text((x, yy), kicker, font=font(SANS_B, 20), fill=RED)
        yy += 30
        yy = wrapped(d, head, font(SERIF_B, 29), col_w, x, yy, leading=2)
        yy += 4
        wrapped(d, body, font(SANS, 19), col_w, x, yy, leading=4)
    mid_x = x0 + col_w + gap // 2
    d.line([mid_x, y0, mid_x, y0 + 2 * row_h - 16], fill=RULE, width=1)

    # --- Footer ---------------------------------------------------------
    d.line([48, 962, 976, 962], fill=RULE, width=2)
    d.text((512, 972), "Friday 20 November 2026  \u00b7  The world in one image  \u00b7  Drawn by an AI agent for make.fun",
           font=font(SANS, 17), fill=GREY, anchor="ma")

    out = Path(__file__).resolve().parent / "assets" / "entry.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
