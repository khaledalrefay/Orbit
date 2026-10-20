"""Build Himma's logo SVGs (mark, lockups, icon sources) from the approved geometry.

Mark: "Orbit dot" (A1) with all approved refinements: ring gradient that turns with the
circle (bright at the dot, fading behind it), dot at 60 degrees, dot 1.5x the ring
width, a separate small-size version, and a soft glow behind the ring on dark icons.

Usage: python3 brand/tools/build_logo.py   (writes into brand/logo and brand/icons/src)
Needs: fonttools, uharfbuzz (for the wordmark, set in Rubik).
"""
import io
import math
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "fonts" / "Rubik[wght].ttf"
LOGO = ROOT / "logo"
SRC = ROOT / "icons" / "src"

NAVY = "#14213D"
WHITE = "#FFFFFF"
APRICOT = "#F2A65A"
ON_DARK = {"bg": NAVY, "near": "#7FD8BE", "far": "#6CB4E8", "solid": "#7FD8BE", "ink": "#EEF3FF", "muted": "#A9B6D6"}
ON_LIGHT = {"bg": WHITE, "near": "#2A8CA6", "far": "#3D4FA3", "solid": "#2A8CA6", "ink": NAVY, "muted": "#5A6785"}

# Geometry in a 100 x 100 box
R = 27.0
ANGLE = -60.0


def pt(deg, r):
    a = math.radians(deg)
    return 50 + r * math.cos(a), 50 + r * math.sin(a)


def mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(pa, pb))


def mark(colors, *, small=False, mono=None, uid="m"):
    """SVG elements of the mark. The gap around the dot is a mask, so it stays transparent."""
    sw = 14.0 if small else 11.0
    dr = 10.5 if small else sw * 0.75
    cut = 5.5 if small else 3.5
    dx, dy = pt(ANGLE, R)
    out = [
        f'<defs><mask id="{uid}-gap" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="100">'
        f'<rect width="100" height="100" fill="#fff"/><circle cx="{dx:.2f}" cy="{dy:.2f}" r="{dr + cut:.2f}" fill="#000"/></mask></defs>',
        f'<g mask="url(#{uid}-gap)">',
    ]
    if mono or small:
        col = mono or colors["solid"]
        out.append(f'<circle cx="50" cy="50" r="{R}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
    else:
        # Opaque short arcs, coloured from the dot backwards; the fade is mixed into the colour so overlaps leave no seams
        n = 180
        for i in range(n):
            t = i / n
            a0 = ANGLE - t * 360 + 0.6
            a1 = ANGLE - (i + 1) / n * 360 - 0.6
            x0, y0 = pt(a0, R)
            x1, y1 = pt(a1, R)
            col = mix(mix(colors["near"], colors["far"], min(1.0, t * 1.15)), colors["bg"], 0.32 * t)
            out.append(f'<path d="M{x0:.2f} {y0:.2f}A{R} {R} 0 0 0 {x1:.2f} {y1:.2f}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
    out.append("</g>")
    out.append(f'<circle cx="{dx:.2f}" cy="{dy:.2f}" r="{dr:.2f}" fill="{mono or APRICOT}"/>')
    return "".join(out)


def glow(uid):
    return (f'<defs><radialGradient id="{uid}-glow" cx=".5" cy=".5" r=".5">'
            f'<stop offset="0" stop-color="#6CB4E8" stop-opacity=".22"/><stop offset=".55" stop-color="#6CB4E8" stop-opacity=".07"/>'
            f'<stop offset="1" stop-color="#6CB4E8" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="100" height="100" fill="url(#{uid}-glow)"/>')


def svg(body, vb="0 0 100 100", w=None, h=None):
    size = f' width="{w}" height="{h}"' if w else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{size}>{body}</svg>\n'


def scaled(body, s):
    """Scale a 100-box drawing about its centre."""
    o = (1 - s) * 50
    return f'<g transform="translate({o:.3f} {o:.3f}) scale({s})">{body}</g>'


# ---------- Wordmark (Rubik, shaped with HarfBuzz) ----------

def rubik(weight):
    f = instancer.instantiateVariableFont(TTFont(str(FONT)), {"wght": weight})
    buf = io.BytesIO()
    f.save(buf)
    return f, buf.getvalue()


def shape(text, weight, *, rtl, tracking=0):
    """Return (svg path d in font units, y-up flipped to y-down, bbox) for a run of text."""
    font, data = rubik(weight)
    face = hb.Face(data)
    hbf = hb.Font(face)
    b = hb.Buffer()
    b.add_str(text)
    b.guess_segment_properties()
    if rtl:
        b.direction = "rtl"
    hb.shape(hbf, b, {})
    gs = font.getGlyphSet()
    order = font.getGlyphOrder()
    x = 0
    parts, xmin, ymin, xmax, ymax = [], 1e9, 1e9, -1e9, -1e9
    for info, pos in zip(b.glyph_infos, b.glyph_positions):
        name = order[info.codepoint]
        ox, oy = x + pos.x_offset, pos.y_offset
        pen = SVGPathPen(gs)
        gs[name].draw(pen)
        d = pen.getCommands()
        if d:
            parts.append(f'<path transform="translate({ox} {-oy}) scale(1 -1)" d="{d}"/>')
            bp = BoundsPen(gs)
            gs[name].draw(bp)
            if bp.bounds:
                bx0, by0, bx1, by1 = bp.bounds
                xmin, xmax = min(xmin, ox + bx0), max(xmax, ox + bx1)
                ymin, ymax = min(ymin, -(oy + by1)), max(ymax, -(oy + by0))
        x += pos.x_advance + tracking
    return "".join(parts), (xmin, ymin, xmax, ymax)


def lockup(colors, *, stacked=False, mono=None, uid="l"):
    ink = mono or colors["ink"]
    muted = mono or colors["muted"]
    ar, (ax0, ay0, ax1, ay1) = shape("هِمّة", 700, rtl=True)
    en, (ex0, ey0, ex1, ey1) = shape("HIMMA", 500, rtl=False, tracking=140)
    ah = ay1 - ay0                      # height of the Arabic word, diacritics included
    S = ah / 0.65 * 0.95                # mark box: ring outer diameter ~ word height
    en_scale = 0.34
    gap = S * 0.12                      # space between mark and word
    line = ah * 0.12                    # space between Arabic and Latin lines
    ar_w, en_w = ax1 - ax0, (ex1 - ex0) * en_scale
    m = mark(colors, mono=mono, uid=uid)
    if not stacked:
        # RTL lockup: mark on the right, words on the left, Latin right-aligned under the Arabic
        words_w = max(ar_w, en_w)
        tx_ar = -ax0 + (words_w - ar_w)
        tx_en = words_w - en_w - ex0 * en_scale
        en_top = ay1 - ay0 + line
        words_h = en_top + (ey1 - ey0) * en_scale
        mx = words_w + gap
        my = words_h / 2 - S / 2
        body = (f'<g fill="{ink}" transform="translate({tx_ar:.1f} {-ay0:.1f})">{ar}</g>'
                f'<g fill="{muted}" transform="translate({tx_en:.1f} {en_top - ey0 * en_scale:.1f}) scale({en_scale})">{en}</g>'
                f'<g transform="translate({mx:.1f} {my:.1f}) scale({S / 100:.4f})">{m}</g>')
        W, H = mx + S, max(words_h, S)
        pad = S * 0.06
        return svg(body, f"{-pad:.1f} {min(0, my) - pad:.1f} {W + 2 * pad:.1f} {H + 2 * pad:.1f}")
    # Stacked: mark centred on top, Arabic then Latin centred below
    W = max(S, ar_w, en_w)
    body = (f'<g transform="translate({(W - S) / 2:.1f} 0) scale({S / 100:.4f})">{m}</g>'
            f'<g fill="{ink}" transform="translate({(W - ar_w) / 2 - ax0:.1f} {S * 0.92 - ay0:.1f})">{ar}</g>')
    en_top = S * 0.92 + ah + line
    body += f'<g fill="{muted}" transform="translate({(W - en_w) / 2 - ex0 * en_scale:.1f} {en_top - ey0 * en_scale:.1f}) scale({en_scale})">{en}</g>'
    H = en_top + (ey1 - ey0) * en_scale
    pad = S * 0.06
    return svg(body, f"{-pad:.1f} {-pad:.1f} {W + 2 * pad:.1f} {H + 2 * pad:.1f}")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT.parent))


def main():
    # Mark, on transparent background
    write(LOGO / "mark-on-dark.svg", svg(mark(ON_DARK, uid="md")))
    write(LOGO / "mark-on-light.svg", svg(mark(ON_LIGHT, uid="ml")))
    write(LOGO / "mark-small-on-dark.svg", svg(mark(ON_DARK, small=True, uid="sd")))
    write(LOGO / "mark-small-on-light.svg", svg(mark(ON_LIGHT, small=True, uid="sl")))
    write(LOGO / "mark-mono-black.svg", svg(mark(ON_LIGHT, mono="#000000", uid="mb")))
    write(LOGO / "mark-mono-white.svg", svg(mark(ON_DARK, mono="#FFFFFF", uid="mw")))
    # Lockups
    write(LOGO / "lockup-horizontal-on-light.svg", lockup(ON_LIGHT, uid="hl"))
    write(LOGO / "lockup-horizontal-on-dark.svg", lockup(ON_DARK, uid="hd"))
    write(LOGO / "lockup-stacked-on-light.svg", lockup(ON_LIGHT, stacked=True, uid="vl"))
    write(LOGO / "lockup-stacked-on-dark.svg", lockup(ON_DARK, stacked=True, uid="vd"))
    write(LOGO / "lockup-horizontal-mono-black.svg", lockup(ON_LIGHT, mono="#000000", uid="hb"))

    # Icon sources (rendered to PNG by render_icons.mjs)
    bg = f'<rect width="100" height="100" fill="{NAVY}"/>'
    # iOS: full square (the system applies the mask); mark at 64% of the canvas
    write(SRC / "ios.svg", svg(bg + glow("i") + scaled(mark(ON_DARK, uid="i"), 0.64)))
    # iOS dark appearance: no background, the system draws its own dark backdrop
    write(SRC / "ios-dark.svg", svg(scaled(mark(ON_DARK, uid="idk"), 0.64)))
    # iOS tinted: grayscale on transparent, the system applies the tint
    write(SRC / "ios-tinted.svg", svg(scaled(mark(ON_DARK, mono="#FFFFFF", uid="it").replace(f'fill="#FFFFFF"/>', 'fill="#B8B8B8"/>'), 0.64)))
    # Android legacy launcher (square and round), mark at 64%
    write(SRC / "android-legacy.svg", svg(f'<rect width="100" height="100" rx="18" fill="{NAVY}"/>' + glow("al") + scaled(mark(ON_DARK, uid="al"), 0.64)))
    write(SRC / "android-legacy-round.svg", svg(f'<circle cx="50" cy="50" r="50" fill="{NAVY}"/>' + glow("ar") + scaled(mark(ON_DARK, uid="ar"), 0.6)))
    # Android adaptive (108dp canvas, 66dp safe circle): mark scaled to stay inside the safe zone
    write(SRC / "android-foreground.svg", svg(glow("af") + scaled(mark(ON_DARK, uid="af"), 0.62)))
    write(SRC / "android-monochrome.svg", svg(scaled(mark(ON_DARK, mono="#FFFFFF", uid="am"), 0.62)))
    # Android notification icon: white silhouette, small-size version
    write(SRC / "android-notification.svg", svg(scaled(mark(ON_DARK, small=True, mono="#FFFFFF", uid="an"), 0.9)))
    # Play Store 512: full square, Play applies its own mask
    write(SRC / "play-store.svg", svg(bg + glow("ps") + scaled(mark(ON_DARK, uid="ps"), 0.66)))


if __name__ == "__main__":
    main()
