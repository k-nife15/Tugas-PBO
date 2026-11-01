"""
back_cover.py — Cover belakang kalender meja (trim 213 x 152 mm + bleed 3 mm).

Konsep: ruang lapang & bersih di atas kertas Soft Beige, pesan komitmen
pelayanan syariah di tengah, kisi rapi 4 kolom di bawah (call center, media
sosial, QR mobile banking, legalitas OJK/LPS), serta ornamen garis emas
senada di sudut bawah.
"""
from __future__ import annotations

import math

from tokens import *
from svgkit import (f, svg_doc, grad_linear, grad_radial, foil_gradient, text,
                    rect, line, circle, path, group, rot)
import patterns as P

COL_X = [15.0, 61.5, 108.0, 154.5]      # 4 kolom kisi, lebar 46,5 mm
COL_W = 46.5
GRID_TOP = 103.0
GRID_LINE_BOTTOM = 133.0


def _defs():
    d = [
        grad_linear("paper", [(0, "#FBF6EA"), (0.55, BEIGE), (1, BEIGE_DEEP)],
                    0, 0, 1, 1),
        grad_radial("warm", [(0, "#FFFFFF", 0.65), (1, "#FFFFFF", 0.0)]),
        foil_gradient("foil_v", "v"),
    ]
    return "<defs>" + "".join(d) + "</defs>"


def _background():
    out = [rect(0, 0, DOC_W, DOC_H, fill="url(#paper)")]
    # cahaya krem lembut dari kanan-atas (lapang)
    out.append(rect(X(80), Y(-40), 160, 130, fill="url(#warm)"))
    return "".join(out)


def _top_bar():
    body = [
        line(X(0), Y(15), X(TRIM_W), Y(15), stroke=GOLD, sw=0.25, opacity=0.45),
        # logo mono emerald
        rect(X(15), Y(18), 10, 10, fill="none", stroke=EMERALD, sw=0.35, rx=2.4),
        path(P.star8(X(20), Y(23), 3.4, 1.9), stroke=EMERALD, sw=0.38),
        P.circle(X(20), Y(23), 0.8, fill=EMERALD, opacity=0.9),
        text(X(28.5), Y(22.4), BRAND_LINE_1, 4.6, SANS_MED, INK_SOFT,
             tracking=0.22),
        text(X(28.5), Y(27.2), BRAND_LINE_2, 6.0, SANS, EMERALD,
             weight="bold", tracking=0.14),
    ]
    return "".join(body)



def _message():
    body = []
    # kicker
    body.append(text(X(15), Y(48.0), BACK_KICKER, 4.8, SANS_MED, GOLD_DEEP,
                     tracking=0.28))
    body.append(line(X(15), Y(51.6), X(38), Y(51.6), stroke=GOLD, sw=0.4))
    # headline serif + sans
    body.append(text(X(15), Y(62.0), BACK_HEAD_SERIF, 20.0, SERIF_SEMI,
                     EMERALD_DEEP))
    body.append(text(X(15), Y(71.4), BACK_HEAD_SANS, 11.0, SANS_LIGHT,
                     EMERALD_MID, tracking=0.045))
    # paragraf komitmen
    y = 82.0
    for ln in BACK_BODY:
        body.append(text(X(15), Y(y), ln, 6.8, SANS, INK_SOFT, opacity=0.88,
                         tracking=0.005))
        y += 5.4
    return "".join(body)


def _medallion():
    """Medali garis emas di kanan (penyeimbang, senada motif cover depan)."""
    cx, cy = X(172), Y(62)
    body = [
        P.circle(cx, cy, 24.5, stroke=GOLD, sw=0.32, opacity=0.55),
        P.circle(cx, cy, 22.6, stroke=GOLD, sw=0.18, opacity=0.35),
        path(P.arc(cx, cy, 27.5, math.radians(-150), math.radians(-30)),
             stroke=GOLD, sw=0.3, opacity=0.30, dash="1.4 2.2"),
        group(path(P.star8(cx, cy, 17.5, 9.6), stroke=GOLD, sw=0.32),
              opacity=0.55),
        group(P.rosette(cx, cy, 13.0, 4.8, petals=8, sw=0.24, opacity=0.35),
              opacity=0.9),
        P.circle(cx, cy, 1.3, fill=GOLD, opacity=0.7),
    ]
    return "".join(body)


def _grid():
    body = []
    # garis atas + garis pemisah kolom
    body.append(line(X(15), Y(GRID_TOP), X(201), Y(GRID_TOP), stroke=GOLD,
                     sw=0.35, opacity=0.55))
    for i in range(1, 4):
        x = X(COL_X[i] - 2.5)
        body.append(line(x, Y(GRID_TOP + 3), x, Y(GRID_LINE_BOTTOM),
                         stroke=GOLD, sw=0.24, opacity=0.32))

    # --- kolom 1: call center ---
    x = X(COL_X[0])
    body.append(text(x, Y(110.0), "CALL CENTER", 4.2, SANS_SEMI, GOLD_DEEP,
                     tracking=0.24))
    body.append(text(x, Y(119.4), "14040", 12.5, SANS, EMERALD_DEEP,
                     weight="bold", tracking=0.02))
    body.append(text(x, Y(125.4), "(021) 5050 1404", 4.8, SANS_MED, INK_SOFT,
                     opacity=0.8))
    body.append(text(x, Y(130.4), "Setiap hari 08.00–20.00 WIB", 3.9, SANS,
                     INK_SOFT, opacity=0.65))

    # --- kolom 2: media sosial ---
    x = X(COL_X[1])
    body.append(text(x, Y(110.0), "MEDIA SOSIAL", 4.2, SANS_SEMI, GOLD_DEEP,
                     tracking=0.24))
    for i, g in enumerate(["IG", "f", "X", "▶"]):
        body.append(P.icon_badge(x + 4.6 + i * 11.4, Y(117.6), 4.2, g,
                                 stroke=EMERALD_MID, sw=0.3))
    body.append(text(x, Y(125.4), "@namabanksyariah", 4.6, SANS_MED, INK_SOFT,
                     opacity=0.8))
    body.append(text(x, Y(130.4), "Senin–Jumat 09.00–17.00", 3.9, SANS,
                     INK_SOFT, opacity=0.65))

    # --- kolom 3: QR mobile banking ---
    x = X(COL_X[2])
    body.append(text(x, Y(110.0), "MOBILE BANKING", 4.2, SANS_SEMI, GOLD_DEEP,
                     tracking=0.24))
    body.append(P.qr_placeholder(x, Y(112.6), 21.0, modules=25, seed=11))
    body.append(text(x + 22.8, Y(120.0), "Pindai untuk", 4.4, SANS_MED,
                     INK_SOFT, opacity=0.85))
    body.append(text(x + 22.8, Y(124.4), "unduh aplikasi", 4.4, SANS_MED,
                     INK_SOFT, opacity=0.85))
    body.append(text(x + 22.8, Y(128.8), "mobile banking", 4.4, SANS_MED,
                     INK_SOFT, opacity=0.85))

    # --- kolom 4: legalitas ---
    x = X(COL_X[3])
    body.append(text(x, Y(110.0), "LEGALITAS", 4.2, SANS_SEMI, GOLD_DEEP,
                     tracking=0.24))
    body.append(P.legal_badge(x, Y(113.0), 21.0, 9.6, "OJK", "OTORITAS JASA KEUANGAN",
                              stroke=EMERALD, color=EMERALD_DEEP))
    body.append(P.legal_badge(x + 24.0, Y(113.0), 21.0, 9.6, "LPS",
                              "LEMBAGA PENJAMIN SIMPANAN",
                              stroke=EMERALD, color=EMERALD_DEEP))
    body.append(text(x, Y(126.6), "Terdaftar & diawasi OJK.", 3.9, SANS,
                     INK_SOFT, opacity=0.75))
    body.append(text(x, Y(130.6), "Simpanan dijamin LPS s.d. Rp2 miliar.", 3.9,
                     SANS, INK_SOFT, opacity=0.75))
    return "".join(body)


def _ornament():
    """Pola garis emas senada di sudut bawah kiri (dibatasi pita y >= 132 mm)."""
    cx, cy = X(6), Y(153)
    body = []
    # busur konsentris
    for i, rr in enumerate([9.5, 15.5, 21.5, 27.5]):
        body.append(path(P.arc(cx, cy, rr, math.radians(-42), math.radians(0)),
                         stroke=GOLD, sw=0.28 if i % 2 == 0 else 0.18,
                         opacity=0.55 if i % 2 == 0 else 0.38))
    # jari-jari + titik simpul (bersih, tidak “scribble”)
    for ang in (-12.0, -24.0, -36.0):
        a = math.radians(ang)
        x0, y0 = cx + 7.0 * math.cos(a), cy + 7.0 * math.sin(a)
        x1, y1 = cx + 24.5 * math.cos(a), cy + 24.5 * math.sin(a)
        body.append(path(f"M {f(x0)} {f(y0)} L {f(x1)} {f(y1)}",
                         stroke=GOLD, sw=0.24, opacity=0.45))
        body.append(circle(x1, y1, 0.65, fill=GOLD, opacity=0.6))
    # deret belah ketupat kecil di busur terluar (aksen playful)
    for k in range(5):
        a = math.radians(-8 - k * 9.5)
        px, py = cx + 27.5 * math.cos(a), cy + 27.5 * math.sin(a)
        body.append(path(f"M {f(px)} {f(py)} l 1.05 1.05 l -1.05 1.05 "
                         f"l -1.05 -1.05 Z", fill=GOLD, opacity=0.5))
    return "".join(body)


def _accents():
    return P.dot_grid(X(166), Y(20), 4, 3, 3.0, r=0.4, fill=GOLD,
                      opacity=0.35)


def _footer():
    return text(X(201), Y(138.4), COPYRIGHT, 4.0, SANS, INK_SOFT,
                tracking=0.02, anchor="end", opacity=0.55)


def build() -> str:
    body = (_defs() + _background() + _ornament() + _message() + _medallion()
            + _grid() + _top_bar() + _accents() + _footer())
    return svg_doc(DOC_W, DOC_H, body)


if __name__ == "__main__":
    print(build()[:300])

