"""Draw the front page for Wednesday 25 November 2026.

Grid layout: the page is a 12-column grid (36 px margins, 16 px
gutters). Stories are plain data — kicker, headline, body, and an
optional graphic — and a small Typesetter wraps and draws text into
grid cells. A horizontal bar chart carries the market falls.
Everything is drawn with Pillow; no network, no randomness, no
clock — the same input always produces the same PNG bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (163, 18, 18)
BLUE = (26, 58, 107)
GREY = (90, 86, 76)
FAINT = (210, 205, 190)
BAND = (20, 20, 20)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = FONT_DIR + "/DejaVuSerif.ttf"
SERIF_B = FONT_DIR + "/DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "/DejaVuSans.ttf"
SANS_B = FONT_DIR + "/DejaVuSans-Bold.ttf"

MARGIN = 36
CONTENT = W - 2 * MARGIN          # 952
GUTTER = 16
COLS = 12
UNIT = (CONTENT + GUTTER) / COLS  # 80.666...


def col_x(c):
    """Left edge of grid column c (0-based)."""
    return MARGIN + c * UNIT


def span_w(n):
    """Width of n grid columns."""
    return n * UNIT - GUTTER


def load(path, size):
    return ImageFont.truetype(path, size)


class Typesetter:
    """Wraps and draws text for one draw context."""

    def __init__(self, draw):
        self.d = draw

    def wrap(self, text, fnt, width):
        lines, cur = [], ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if self.d.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def block(self, text, fnt, x, y, width, leading, fill=INK,
              align="left"):
        """Draw a wrapped paragraph; return the y below its last line."""
        for line in self.wrap(text, fnt, width):
            lx = x
            if align == "center":
                lx = x + (width - self.d.textlength(line, font=fnt)) / 2
            self.d.text((lx, y), line, font=fnt, fill=fill)
            y += leading
        return y

    def headline(self, text, fnt, x, y, width, leading, max_lines=2):
        """Headline in at most max_lines; shrink the font until it fits."""
        size = fnt.size
        lines = self.wrap(text, fnt, width)
        while len(lines) > max_lines and size > 14:
            size -= 2
            fnt = ImageFont.truetype(fnt.path, size)
            lines = self.wrap(text, fnt, width)
        for line in lines[:max_lines]:
            self.d.text((x, y), line, font=fnt, fill=INK)
            y += leading
        return y


def rule(d, y, width=2, x0=MARGIN, x1=W - MARGIN):
    d.line([(x0, y), (x1, y)], fill=INK, width=width)


def divider(d, x, y0, y1):
    d.line([(x, y0), (x, y1)], fill=GREY, width=1)


def kicker(ts, text, x, y, width, size=20):
    return ts.block(text, load(SANS_B, size), x, y, width, size + 4,
                    fill=RED)


def falls_chart(d, ts, x, y, w):
    """Horizontal bars for Wednesday's market falls, in percent."""
    rows = [
        ("KOSPI", -6.1), ("TAIPEI", -4.9), ("NIKKEI", -2.6),
        ("SHANGHAI", -1.7), ("HANG SENG", -0.7), ("NASDAQ FUT.", -2.4),
    ]
    ts.block("WEDNESDAY'S FALLS, %", load(SANS_B, 16), x, y, w, 20)
    top = y + 26
    bar_x = x + 118
    bar_w = w - 118 - 52
    for i, (name, val) in enumerate(rows):
        ry = top + i * 36
        ts.block(name, load(SANS, 15), x, ry, 112, 19)
        d.rectangle([bar_x, ry + 2, bar_x + bar_w * abs(val) / 6.5,
                     ry + 16], fill=RED)
        ts.block(f"{val:.1f}%", load(SANS_B, 15), x + w - 48, ry, 48,
                 19, fill=RED, align="right")


def masthead(ts):
    ts.block("THE WORLD", load(SERIF_B, 96), MARGIN, 26, CONTENT, 100,
             align="center")
    ts.block("WEDNESDAY, 25 NOVEMBER 2026  ·  ONE DAY, ONE PAGE",
             load(SANS, 19), MARGIN, 138, CONTENT, 24, fill=GREY,
             align="center")
    rule(ts.d, 168, width=3)


def lead(ts):
    tx, tw = col_x(0), span_w(8)
    cx, cw = col_x(8), span_w(4)
    kicker(ts, "MARKETS", tx, 184, tw)
    ts.headline("AI rout deepens as Asia plunges",
                load(SERIF_B, 52), tx, 212, tw, 58)
    ts.block("Chip stocks lead a second day of losses as the AI rally "
             "unwinds: Seoul falls 6.1%, Taipei 4.9% and Tokyo 2.6%, "
             "while Nasdaq futures slide and Nvidia drops 5% before "
             "the US open.",
             load(SERIF, 22), tx, 338, tw, 29)
    falls_chart(ts.d, ts, cx, 188, cw)
    ts.block("TOKYO  ·  SEOUL  ·  TAIPEI", load(SANS, 16), cx, 440, cw,
             20, fill=GREY, align="center")
    rule(ts.d, 470, width=2)


def duo(ts):
    lx, lw = col_x(0), span_w(6)
    rx, rw = col_x(6), span_w(6)
    kicker(ts, "TECHNOLOGY", lx, 486, lw, size=18)
    ts.headline("Huawei convicted in US trade-secrets case",
                load(SERIF_B, 30), lx, 510, lw, 35)
    ts.block("A New York jury finds the Chinese firm guilty of "
             "conspiring to steal trade secrets, acquitting it of "
             "racketeering; Beijing accuses Washington of "
             "obstructing Chinese firms.",
             load(SERIF, 20), lx, 590, lw, 25)
    divider(ts.d, col_x(6) - GUTTER / 2, 486, 726)
    kicker(ts, "SPACE", rx, 486, rw, size=18)
    ts.headline("China carries Pakistan's first astronaut into orbit",
                load(SERIF_B, 30), rx, 510, rw, 35)
    ts.block("A Pakistani astronaut rides to the Tiangong station as "
             "China launches its first foreign crew member — a "
             "milestone for its space programme.",
             load(SERIF, 20), rx, 590, rw, 25)
    rule(ts.d, 732, width=2)


def trio(ts):
    stories = [
        ("RESCUE",
         "Colombia frees all hostages in supermarket siege",
         "Security forces storm a Cartagena supermarket, freeing "
         "every hostage and killing one captor."),
        ("LABOUR",
         "Bangladesh raises garment wage 36%",
         "Entry-level garment pay rises to 17,000 taka a month "
         "after weeks of violent protests."),
        ("DISASTER",
         "Miners trapped as flood hits Indonesian gold mine",
         "Rescuers search for dozens of workers after heavy rain "
         "floods a gold mine in West Java."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        x = col_x(4 * i)
        w = span_w(4)
        kicker(ts, kick, x, 748, w, size=17)
        ts.headline(head, load(SERIF_B, 26), x, 770, w, 28)
        ts.block(body, load(SERIF, 18), x, 836, w, 22)
        if i:
            divider(ts.d, x - GUTTER / 2, 748, 928)
    rule(ts.d, 940, width=2)


def ticker(ts):
    d = ts.d
    d.rectangle([MARGIN, 950, W - MARGIN, 1014], fill=BAND)
    lines = [
        "UKRAINE NEEDS €115BN AID FOR 2027  •  "
        "US READIES TARIFFS ON 16 PARTNERS  •  "
        "EUROZONE INFLATION 4.0%",
        "NORTH KOREA EXPELS SWISS DIPLOMAT  •  "
        "SAUDI STRIKES HODEIDAH PORT  •  "
        "ANTHROPIC BELOW IPO PRICE",
    ]
    size = 13
    fnt = load(SANS_B, size)
    while max(d.textlength(t, font=fnt) for t in lines) > 940 and size > 8:
        size -= 1
        fnt = ImageFont.truetype(SANS_B, size)
    d.text((512, 968), lines[0], font=fnt, fill=PAPER, anchor="ma")
    d.text((512, 992), lines[1], font=fnt, fill=PAPER, anchor="ma")


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    ts = Typesetter(d)
    masthead(ts)
    lead(ts)
    duo(ts)
    trio(ts)
    ticker(ts)
    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import sys
    render(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
