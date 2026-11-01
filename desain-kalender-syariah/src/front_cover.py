"""
front_cover.py — Cover depan kalender meja (trim 213 x 152 mm + bleed 3 mm).

Konsep "Lensa Tumbuh":
  logo di kiri-atas, fokus visual berupa lensa kaca (glassmorphism) berisi
  geometri Islami 8-fold + rosette arabesque bergaris emas di tengah,
  sulur tumbuh dari tepi lensa, lalu judul tema serif+sans di kiri-bawah
  berdampingan dengan angka tahun beraksen gold foil.
"""
from __future__ import annotations

import math

from tokens import *
from svgkit import (f, svg_doc, grad_linear, grad_radial, foil_gradient, text,
                    rect, line, circle, path, group, rot)
import patterns as P

CX, CY = 108.0, 57.0          # pusat lensa (mm dari trim kiri/atas)
R_LENS = 38.0


def _defs():
    d = [
        grad_linear("bg", [(0, EMERALD_MID), (0.45, EMERALD), (1, EMERALD_DEEP)],
                    0, 0, 1, 1),
        grad_radial("vignette", [(0, "#000000", 0.0), (0.62, "#000000", 0.0),
                                 (1, "#000000", 0.42)]),
        grad_linear("glassref", [(0, "#ffffff", 0.10), (0.55, "#ffffff", 0.02),
                                 (1, "#ffffff", 0.0)], 0, 0, 0.85, 1),
        P.glow_def("glow_mint"),
        foil_gradient("foil", "d"),
    ]
    return "<defs>" + "".join(d) + "</defs>"


def _background():
    out = [rect(0, 0, DOC_W, DOC_H, fill="url(#bg)")]
    # glow mint hangat kanan-atas (nuansa ramah)
    out.append(rect(X(118), Y(-30), 130, 96, fill="url(#glow_mint)"))
    # cahaya lembut di belakang lensa (depth)
    out.append(rect(X(CX - 78), Y(CY - 64), 156, 128, fill="url(#glow_mint)",
                    extra='opacity="0.75"'))
    out.append(rect(0, 0, DOC_W, DOC_H, fill="url(#vignette)"))
    return "".join(out)



def _glass_card(x, y, w, h, rx, angle, fill="#ffffff", op=0.08,
                border_op=0.9, sw=0.32):
    """Kartu kaca bergaris emas: fill transparan + refleksi + garis ganda."""
    cxc, cyc = x + w / 2, y + h / 2
    parts = [
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" '
        f'rx="{f(rx)}" fill="{fill}" fill-opacity="{f(op)}"/>',
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" '
        f'rx="{f(rx)}" fill="url(#glassref)"/>',
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" '
        f'rx="{f(rx)}" fill="none" stroke="{GOLD}" stroke-width="{f(sw)}" '
        f'stroke-opacity="{f(border_op)}"/>',
        f'<rect x="{f(x + 1.1)}" y="{f(y + 1.1)}" width="{f(w - 2.2)}" '
        f'height="{f(h - 2.2)}" rx="{f(max(rx - 1, 0.4))}" fill="none" '
        f'stroke="{GOLD_LIGHT}" stroke-width="0.18" stroke-opacity="0.5"/>',
    ]
    return group("".join(parts), transform=rot(angle, cxc, cyc))


def _glass_disc(cx, cy, r, op=0.045):
    """Lensa kaca: cakram transparan + kilau + busur highlight."""
    parts = [
        (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#ffffff" '
         f'fill-opacity="{f(op)}"/>'),
        (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" '
         f'fill="url(#glassref)"/>'),
        path(P.arc(cx, cy, r * 0.985, math.radians(-148), math.radians(-42)),
             stroke="#ffffff", sw=0.45, opacity=0.16),
    ]
    return "".join(parts)


def _centerpiece():
    body = []
    cxc, cyc = X(CX), Y(CY)

    # 1. orbit emas putus-putus (rasa "melangkah" & lapang)
    body.append(path(P.arc(cxc, cyc, 46, math.radians(-168), math.radians(-14)),
                     stroke=GOLD, sw=0.30, opacity=0.26, dash="1.6 2.2"))
    body.append(path(P.arc(cxc, cyc, 46, math.radians(162), math.radians(96)),
                     stroke=GOLD, sw=0.30, opacity=0.14, dash="1.6 2.2"))

    # 2. lensa kaca sebagai dudukan motif
    body.append(_glass_disc(cxc, cyc, R_LENS))
    body.append(P.circle(cxc, cyc, R_LENS, stroke=GOLD, sw=0.34, opacity=0.75))
    body.append(P.circle(cxc, cyc, R_LENS - 1.4, stroke=GOLD_LIGHT, sw=0.16,
                         opacity=0.5))

    # 3. fokus visual: girih 8-fold + rosette arabesque bertumpuk
    body.append(P.girih_octagram(cxc, cyc, 30, sw=0.28, opacity=0.52,
                                 spokes=False, rings=(0.56,)))
    body.append(P.rosette(cxc, cyc, 29, 10.2, petals=16, sw=0.24, opacity=0.44))
    body.append(P.rosette(cxc, cyc, 9.8, 4.2, petals=8, sw=0.26, opacity=0.55,
                          spread=1.05))
    body.append(P.circle(cxc, cyc, 1.4, fill=GOLD_PALE, opacity=0.9))
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        body.append(P.circle(cxc + 30 * math.cos(a), cyc + 30 * math.sin(a),
                             0.7, fill=GOLD_LIGHT, opacity=0.75))

    # 4. badge kaca kecil di tepi lensa (aksen playful)
    body.append(_glass_card(X(CX + 30), Y(CY - 34), 11, 11, 1.9, 16,
                            fill=MINT, op=0.10, border_op=0.7, sw=0.26))
    body.append(_glass_card(X(CX - 47), Y(CY + 14), 9, 9, 1.7, -16,
                            fill=BEIGE, op=0.14, border_op=0.6, sw=0.24))

    # 5. sulur arabesque tumbuh dari tepi lensa (metafora "tumbuh")
    body.append(P.tendril_flow(X(CX + 20), Y(CY + 30), scale=0.82, sw=0.26,
                               opacity=0.42, rotate=-14))

    # 6. percikan titik emas (playful)
    body.append(P.dot_grid(X(CX - 64), Y(CY - 6), 3, 3, 2.6, r=0.36, fill=GOLD,
                           opacity=0.22))
    return "".join(body)


def _logo():
    x, y = X(15), Y(17)
    body = []
    body.append(rect(x, y, 12, 12, fill="#ffffff",
                     extra='fill-opacity="0.08"', stroke=GOLD, sw=0.35, rx=2.8))
    body.append(path(P.star8(x + 6.2, y + 6.2, 4.1, 2.3), stroke=GOLD_LIGHT,
                     sw=0.4))
    body.append(P.circle(x + 6.2, y + 6.2, 0.9, fill=GOLD_LIGHT, opacity=0.95))
    tx = x + 16.0
    body.append(text(tx, y + 4.6, BRAND_LINE_1, 5.2, SANS_MED, GOLD_PALE,
                     tracking=0.22))
    body.append(text(tx, y + 10.2, BRAND_LINE_2, 6.8, SANS, GOLD,
                     weight="bold", tracking=0.14))
    body.append(line(tx, y + 12.0, tx + 27, y + 12.0, stroke=GOLD, sw=0.25,
                     opacity=0.5))
    return "".join(body)


def _title_block():
    body = []
    # kicker + rule emas + belah ketupat
    body.append(line(X(15), Y(98.5), X(52), Y(98.5), stroke=GOLD, sw=0.5))
    body.append(path(f"M {f(X(55))} {f(Y(98.5))} l 1.9 1.9 l -1.9 1.9 "
                     f"l -1.9 -1.9 Z", fill=GOLD, opacity=0.95))
    body.append(text(X(15), Y(104.8), KICKER, 5.0, SANS_MED, MINT_SOFT,
                     tracking=0.26))

    # judul tema: serif elegan + sans bersih
    body.append(text(X(15), Y(118.0), THEME_SERIF, 23.5, SERIF_SEMI, GOLD_PALE))
    body.append(text(X(15), Y(128.6), THEME_SANS, 13.2, SANS, MINT_SOFT,
                     tracking=0.05))

    # angka tahun beraksen gold foil, berdampingan (rata kanan)
    body.append(line(X(157), Y(106.0), X(157), Y(131.0), stroke=GOLD, sw=0.3,
                     opacity=0.45))
    body.append(text(X(201), Y(126.4), YEAR, 44.0, SERIF, "url(#foil)",
                     weight="bold", anchor="end"))
    body.append(text(X(201), Y(134.2), "1448–1449 HIJRIYAH", 4.6, SANS_MED,
                     GOLD, tracking=0.22, anchor="end", opacity=0.75))
    return "".join(body)


def _accents():
    body = []
    # hairline batas zona jilid Wire-O (15 mm)
    body.append(line(X(0), Y(15), X(TRIM_W), Y(15), stroke=GOLD, sw=0.25,
                     opacity=0.28))
    # tekstur titik playful kanan-atas
    body.append(P.dot_grid(X(180), Y(20), 4, 4, 3.0, r=0.42, fill=GOLD,
                           opacity=0.28))
    return "".join(body)


def build() -> str:
    body = (_defs() + _background() + _accents() + _centerpiece() + _logo()
            + _title_block())
    return svg_doc(DOC_W, DOC_H, body)


if __name__ == "__main__":
    print(build()[:300])

