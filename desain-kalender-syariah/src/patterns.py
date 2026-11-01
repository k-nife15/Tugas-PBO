"""
patterns.py — Generator motif geometri Islami modern & arabesque abstrak.
Semua fungsi mengembalikan potongan SVG (string) dengan satuan mm.
"""
from __future__ import annotations

import math

from svgkit import f, path, circle, group, rot, line
from tokens import GOLD, GOLD_LIGHT, MINT


def _pt(cx, cy, r, ang):
    return cx + r * math.cos(ang), cy + r * math.sin(ang)


def _poly(pts, close=True):
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts)
    return d + (" Z" if close else "")


# --- 1. Octagram girih (bintang 8) --------------------------------------
def girih_octagram(cx, cy, r, stroke=GOLD, sw=0.25, opacity=0.55,
                   spokes=True, rings=(0.62, 0.30)):
    """Dua persegi bertumpuk (rotasi 45°) + oktagon dalam = girih 8-fold."""
    parts = []
    for off in (0.0, math.pi / 4):
        pts = [_pt(cx, cy, r, off + i * math.pi / 2) for i in range(4)]
        parts.append(path(_poly(pts), stroke=stroke, sw=sw))
    for rr in rings:
        pts = [_pt(cx, cy, r * rr, i * math.pi / 4 + math.pi / 8) for i in range(8)]
        parts.append(path(_poly(pts), stroke=stroke, sw=sw * 0.8))
    if spokes:
        for i in range(8):
            ang = i * math.pi / 4
            x1, y1 = _pt(cx, cy, r * 0.30, ang)
            x2, y2 = _pt(cx, cy, r, ang)
            parts.append(line(x1, y1, x2, y2, stroke=stroke, sw=sw * 0.6))
    return group("".join(parts), opacity=opacity)


def star8(cx, cy, r_out, r_in=None, rot_off=math.pi / 8):
    """Bintang 8 bersudut bersih (untuk logo/monogram kecil)."""
    r_in = r_in if r_in is not None else r_out * 0.56
    pts = []
    for i in range(16):
        rr = r_out if i % 2 == 0 else r_in
        pts.append(_pt(cx, cy, rr, rot_off + i * math.pi / 8))
    return _poly(pts)


# --- 2. Rosette arabesque (kelopak) ------------------------------------
def rosette(cx, cy, r_out, r_in, petals=16, stroke=GOLD, sw=0.25,
            opacity=0.6, spread=0.62):
    """Rosette kelopak abstrak; spread mengatur lebar pangkal kelopak."""
    d_all = []
    for k in range(petals):
        a = k * 2 * math.pi / petals
        d = spread * math.pi / petals
        x0, y0 = _pt(cx, cy, r_in, a - d)
        x1, y1 = _pt(cx, cy, r_in, a + d)
        tx, ty = _pt(cx, cy, r_out, a)
        c1x, c1y = _pt(cx, cy, r_out * 0.78, a - d * 1.45)
        c2x, c2y = _pt(cx, cy, r_out * 0.78, a + d * 1.45)
        d_all.append(
            f"M {f(x0)} {f(y0)} Q {f(c1x)} {f(c1y)} {f(tx)} {f(ty)} "
            f"Q {f(c2x)} {f(c2y)} {f(x1)} {f(y1)}"
        )
    parts = [path(" ".join(d_all), stroke=stroke, sw=sw)]
    parts.append(circle(cx, cy, r_in * 0.98, stroke=stroke, sw=sw * 0.7))
    parts.append(circle(cx, cy, r_in * 0.42, stroke=stroke, sw=sw * 0.7))
    return group("".join(parts), opacity=opacity)


# --- 3. Spiral, daun, busur -------------------------------------------
def spiral(cx, cy, r0, r1, turns=1.1, a0=0.0, steps=44, cw=1):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        a = a0 + cw * turns * 2 * math.pi * t
        pts.append(_pt(cx, cy, r, a))
    return _poly(pts, close=False)


def leaf(cx, cy, length, ang, width_ratio=0.46):
    """Daun arabesque: dua kuadratic simetris berujung runcing."""
    tx, ty = _pt(cx, cy, length, ang)
    w = length * width_ratio
    c1x, c1y = _pt(cx, cy, length * 0.5, ang - w / length)
    c2x, c2y = _pt(cx, cy, length * 0.5, ang + w / length)
    return (f"M {f(cx)} {f(cy)} Q {f(c1x)} {f(c1y)} {f(tx)} {f(ty)} "
            f"Q {f(c2x)} {f(c2y)} {f(cx)} {f(cy)} Z")


def arc(cx, cy, r, a0, a1, steps=40):
    pts = []
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        pts.append(_pt(cx, cy, r, a))
    return "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts)


def _cubic(p0, p1, p2, p3, t):
    """Titik + sudut tangen pada kurva bezier kubik."""
    mt = 1 - t
    x = (mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0]
         + t**3 * p3[0])
    y = (mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1]
         + t**3 * p3[1])
    dx = (3 * mt**2 * (p1[0] - p0[0]) + 6 * mt * t * (p2[0] - p1[0])
          + 3 * t**2 * (p3[0] - p2[0]))
    dy = (3 * mt**2 * (p1[1] - p0[1]) + 6 * mt * t * (p2[1] - p1[1])
          + 3 * t**2 * (p3[1] - p2[1]))
    return (x, y), math.atan2(dy, dx)


# --- 4. Komposisi sulur utama (organic flow) ---------------------------
def tendril_flow(x, y, scale=1.0, stroke=GOLD, sw=0.3, opacity=0.4,
                 rotate=0.0, leaves=(0.30, 0.58, 0.82)):
    """Sulur-S: kurva utama + daun yang menempel persis di kurva + spiral ujung."""
    s = scale
    p0 = (x, y)
    p1 = (x + 15 * s, y - 13 * s)
    p2 = (x + 31 * s, y + 5 * s)
    p3 = (x + 27 * s, y - 13 * s)
    p4 = (x + 23 * s, y - 29 * s)
    p5 = (x + 41 * s, y - 27 * s)
    p6 = (x + 45 * s, y - 41 * s)
    d = (f"M {f(p0[0])} {f(p0[1])} "
         f"C {f(p1[0])} {f(p1[1])} {f(p2[0])} {f(p2[1])} {f(p3[0])} {f(p3[1])} "
         f"C {f(p4[0])} {f(p4[1])} {f(p5[0])} {f(p5[1])} {f(p6[0])} {f(p6[1])}")
    body = [path(d, stroke=stroke, sw=sw)]
    # daun menempel pada kurva (tangen mengikuti arah sulur)
    for i, t in enumerate(leaves):
        if t <= 0.5:
            pt, ang = _cubic(p0, p1, p2, p3, t / 0.5)
        else:
            pt, ang = _cubic(p3, p4, p5, p6, (t - 0.5) / 0.5)
        side = 1 if i % 2 == 0 else -1
        ln = 6.6 * s * (1 - 0.10 * i)
        la = ang + side * 1.05
        body.append(path(leaf(pt[0], pt[1], ln, la), stroke=stroke,
                         sw=sw * 0.72, fill="none"))
        ex, ey = _pt(pt[0], pt[1], ln * 0.86, la)
        body.append(path(f"M {f(pt[0])} {f(pt[1])} L {f(ex)} {f(ey)}",
                         stroke=stroke, sw=sw * 0.45))
    # spiral kecil di ujung sulur
    body.append(path(spiral(p6[0], p6[1], 0.5 * s, 5.4 * s, 1.2, -0.5),
                     stroke=stroke, sw=sw * 0.9))
    return group("".join(body), transform=(rot(rotate, x, y) if rotate else None),
                 opacity=opacity)



# --- 5. Ornamen sudut (untuk cover belakang) ---------------------------
def corner_arabesque(cx, cy, size=52.0, stroke=GOLD, sw=0.3, opacity=0.55,
                     a0=-math.pi / 2, a1=0.0):
    """Kipas garis emas berlapis keluar dari satu sudut."""
    body = []
    for i, rr in enumerate([0.34, 0.48, 0.62, 0.76, 0.90, 1.0]):
        body.append(path(arc(cx, cy, size * rr, a0, a1),
                         stroke=stroke, sw=sw * (1.0 if i % 2 == 0 else 0.65)))
    for k, ang in enumerate([-0.16, -0.42, -0.72, -1.02, -1.30]):
        rr = size * (0.62 + 0.09 * (k % 3))
        x0, y0 = _pt(cx, cy, size * 0.18, ang)
        x1, y1 = _pt(cx, cy, rr, ang)
        body.append(path(f"M {f(x0)} {f(y0)} L {f(x1)} {f(y1)}",
                         stroke=stroke, sw=sw * 0.8))
        body.append(path(spiral(x1, y1, 0.4, size * 0.075, 1.1, ang, cw=-1),
                         stroke=stroke, sw=sw * 0.85))
        body.append(path(leaf(x1, y1, size * 0.10, ang + 0.9),
                         stroke=stroke, sw=sw * 0.7))
    for k in range(5):
        ang = a1 - 0.2 - k * 0.28
        px, py = _pt(cx, cy, size * 0.90, ang)
        body.append(circle(px, py, 0.55, fill=stroke))
    return group("".join(body), opacity=opacity)


# --- 6. Micropattern titik (tekstur playful) ---------------------------
def dot_grid(x0, y0, cols, rows, gap, r=0.4, fill=GOLD, opacity=0.3):
    parts = []
    for i in range(cols):
        for j in range(rows):
            parts.append(circle(x0 + i * gap, y0 + j * gap, r, fill=fill))
    return group("".join(parts), opacity=opacity)


# --- 7. Panel glassmorphism -------------------------------------------
def glass_panel(x, y, w, h, rx, fill="#ffffff", fill_op=0.07, stroke=GOLD,
                sw=0.3, stroke_op=0.85, angle=0.0):
    """Kartu kaca: fill transparan + garis emas + kilau atas (tanpa filter)."""
    cx, cy = x + w / 2, y + h / 2
    parts = [
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" '
        f'fill="{fill}" fill-opacity="{f(fill_op)}" stroke="none"/>',
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" '
        f'fill="none" stroke="{stroke}" stroke-width="{f(sw)}" '
        f'stroke-opacity="{f(stroke_op)}"/>',
        f'<rect x="{f(x + 0.9)}" y="{f(y + 0.9)}" width="{f(w - 1.8)}" '
        f'height="{f(h * 0.34)}" rx="{f(max(rx - 0.9, 0.4))}" fill="url(#shine)" '
        f'stroke="none"/>',
    ]
    return group("".join(parts), transform=(rot(angle, cx, cy) if angle else None))


# --- 8. <defs> pendukung ---------------------------------------------
def shine_def(gid="shine"):
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="#ffffff" stop-opacity="0"/>'
        f"</linearGradient>"
    )


def glow_def(gid="glow_mint", color=None):
    c = color or MINT
    return (
        f'<radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{c}" stop-opacity="0.32"/>'
        f'<stop offset="0.55" stop-color="{c}" stop-opacity="0.11"/>'
        f'<stop offset="1" stop-color="{c}" stop-opacity="0"/>'
        f"</radialGradient>"
    )

