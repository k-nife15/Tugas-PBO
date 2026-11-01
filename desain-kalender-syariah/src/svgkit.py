"""
svgkit.py — Helper kecil untuk menyusun SVG artwork (bukan library umum,
sengaja minimal agar SVG keluaran mudah dibuka di Illustrator / Inkscape).
"""
from __future__ import annotations

import math
from tokens import *


def f(v: float) -> str:
    """Format angka pendek & deterministik (2 desimal max)."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --- <defs> -------------------------------------------------------------
def _stops(stops):
    out = ""
    for st in stops:
        o, c = st[0], st[1]
        a = st[2] if len(st) > 2 else None
        out += f'<stop offset="{f(o)}" stop-color="{c}"'
        if a is not None:
            out += f' stop-opacity="{f(a)}"'
        out += "/>"
    return out


def grad_linear(gid, stops, x1=0, y1=0, x2=1, y2=1, units="objectBoundingBox"):
    s = _stops(stops)
    return (
        f'<linearGradient id="{gid}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
        f'gradientUnits="{units}">{s}</linearGradient>'
    )


def grad_radial(gid, stops, cx=0.5, cy=0.5, r=0.5, units="objectBoundingBox"):
    return (
        f'<radialGradient id="{gid}" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" '
        f'gradientUnits="{units}">{_stops(stops)}</radialGradient>'
    )


def foil_gradient(gid, angle="h"):
    """Simulasi Gold Foil: gelap -> terang -> sedang -> terang (metalik)."""
    stops = [
        (0.00, GOLD_DEEP), (0.20, GOLD_MID), (0.34, GOLD_PALE),
        (0.50, GOLD), (0.66, GOLD_LIGHT), (0.82, GOLD_MID), (1.00, GOLD_DEEP),
    ]
    if angle == "h":
        return grad_linear(gid, stops, 0, 0, 1, 0)
    if angle == "v":
        return grad_linear(gid, stops, 0, 0, 0, 1)
    return grad_linear(gid, stops, 0, 0, 1, 1)


# --- Elemen dasar -------------------------------------------------------
def text(x, y, s, size, family=SANS, fill="#000", weight=None, tracking=None,
         anchor="start", opacity=None, extra=""):
    """Teks dengan posisi dalam mm & ukuran dalam pt (dikonversi ke mm)."""
    size_mm = size * 25.4 / 72.0
    a = [
        f'x="{f(x)}"', f'y="{f(y)}"',
        f'font-family="{family}"', f'font-size="{f(size_mm)}"',
        f'fill="{fill}"',
    ]
    if weight:
        a.append(f'font-weight="{weight}"')
    if tracking is not None:
        a.append(f'letter-spacing="{f(tracking * size_mm)}"')
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        a.append(f'opacity="{f(opacity)}"')
    if extra:
        a.append(extra)
    return f"<text {' '.join(a)}>{esc(s)}</text>"


def rect(x, y, w, h, fill="none", stroke=None, sw=0.2, rx=0, opacity=None,
         extra="", dash=None):
    a = [f'x="{f(x)}"', f'y="{f(y)}"', f'width="{f(w)}"', f'height="{f(h)}"']
    if rx:
        a.append(f'rx="{f(rx)}"')
    a.append(f'fill="{fill}"')
    if stroke:
        a.append(f'stroke="{stroke}" stroke-width="{f(sw)}"')
    if dash:
        a.append(f'stroke-dasharray="{dash}"')
    if opacity is not None:
        a.append(f'opacity="{f(opacity)}"')
    if extra:
        a.append(extra)
    return f"<rect {' '.join(a)}/>"


def line(x1, y1, x2, y2, stroke=GOLD, sw=0.25, dash=None, opacity=None, cap="butt"):
    a = [f'x1="{f(x1)}"', f'y1="{f(y1)}"', f'x2="{f(x2)}"', f'y2="{f(y2)}"',
         f'stroke="{stroke}"', f'stroke-width="{f(sw)}"', f'stroke-linecap="{cap}"']
    if dash:
        a.append(f'stroke-dasharray="{dash}"')
    if opacity is not None:
        a.append(f'opacity="{f(opacity)}"')
    return f"<line {' '.join(a)}/>"


def circle(cx, cy, r, fill="none", stroke=None, sw=0.25, opacity=None, dash=None):
    a = [f'cx="{f(cx)}"', f'cy="{f(cy)}"', f'r="{f(r)}"', f'fill="{fill}"']
    if stroke:
        a.append(f'stroke="{stroke}" stroke-width="{f(sw)}"')
    if dash:
        a.append(f'stroke-dasharray="{dash}"')
    if opacity is not None:
        a.append(f'opacity="{f(opacity)}"')
    return f"<circle {' '.join(a)}/>"


def path(d, fill="none", stroke=None, sw=0.25, opacity=None, dash=None,
         cap="round", join="round"):
    a = [f'd="{d}"', f'fill="{fill}"']
    if stroke:
        a.append(f'stroke="{stroke}" stroke-width="{f(sw)}"')
        a.append(f'stroke-linecap="{cap}" stroke-linejoin="{join}"')
    if dash:
        a.append(f'stroke-dasharray="{dash}"')
    if opacity is not None:
        a.append(f'opacity="{f(opacity)}"')
    return f"<path {' '.join(a)}/>"


def group(content, transform=None, opacity=None, clip=None):
    a = []
    if transform:
        a.append(f'transform="{transform}"')
    if opacity is not None:
        a.append(f'opacity="{f(opacity)}"')
    if clip:
        a.append(f'clip-path="url(#{clip})"')
    return f"<g {' '.join(a)}>{content}</g>"


def rot(deg, cx, cy):
    return f"rotate({f(deg)} {f(cx)} {f(cy)})"


def svg_doc(width, height, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(width)}mm" '
        f'height="{f(height)}mm" viewBox="0 0 {f(width)} {f(height)}">'
        f"{body}</svg>"
    )
