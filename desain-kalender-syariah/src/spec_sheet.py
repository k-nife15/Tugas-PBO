"""
spec_sheet.py — Lembar panduan teknis: bleed, trim, safe area, zona jilid
Wire-O, grid, dimensi, palet warna CMYK, dan catatan produksi.
Kanvas 280x245 mm (artwork 219x158 mm diletakkan di dalamnya).
"""
from __future__ import annotations

import math

from tokens import *
from svgkit import (f, svg_doc, grad_linear, grad_radial, text, rect, line,
                    circle, path, group, rot)

CANVAS_W, CANVAS_H = 280.0, 292.0
OFF_X, OFF_Y = 30.0, 40.0
INK_LINE = "#2B2B2B"
GREY = "#6B6B66"
BLEED_FILL = "#F1E1E1"
BAND_FILL = EMERALD

N_HOLES = 23
PITCH = 25.4 / 3.0          # 3:1 pitch -> 8,467 mm


def PX(mm):
    return OFF_X + BLEED + mm


def PY(mm):
    return OFF_Y + BLEED + mm


def _dim_h(x1, x2, y, label, size=4.2):
    body = [
        line(x1, y, x2, y, stroke=INK_LINE, sw=0.25),
        line(x1, y - 1.2, x1, y + 1.2, stroke=INK_LINE, sw=0.25),
        line(x2, y - 1.2, x2, y + 1.2, stroke=INK_LINE, sw=0.25),
        text((x1 + x2) / 2, y - 1.4, label, size, SANS_MED, INK_LINE,
             tracking=0.08, anchor="middle"),
    ]
    return "".join(body)


def _dim_v(y1, y2, x, label, size=4.2, side="right"):
    body = [
        line(x, y1, x, y2, stroke=INK_LINE, sw=0.25),
        line(x - 1.2, y1, x + 1.2, y1, stroke=INK_LINE, sw=0.25),
        line(x - 1.2, y2, x + 1.2, y2, stroke=INK_LINE, sw=0.25),
        text(x + (2.2 if side == "right" else -2.2), (y1 + y2) / 2 + 1.4,
             label, size, SANS_MED, INK_LINE, tracking=0.08,
             anchor="start" if side == "right" else "end"),
    ]
    return "".join(body)


def _crop_marks():
    """Tanda potong (crop marks) di keempat sudut trim."""
    body = []
    x0, y0 = PX(0), PY(0)
    x1, y1 = PX(TRIM_W), PY(TRIM_H)
    L = 5.0
    for (x, y, sx, sy) in ((x0, y0, -1, -1), (x1, y0, 1, -1),
                           (x0, y1, -1, 1), (x1, y1, 1, 1)):
        body.append(line(x + sx * 3.0, y, x + sx * (3.0 + L), y,
                         stroke=INK_LINE, sw=0.2))
        body.append(line(x, y + sy * 3.0, x, y + sy * (3.0 + L),
                         stroke=INK_LINE, sw=0.2))
    return "".join(body)


def _artboard():
    """Bleed, trim, safe area, zona jilid, lubang wire-o, grid kolom."""
    body = []
    # area bleed (di luar trim)
    body.append(rect(PX(-BLEED), PY(-BLEED), DOC_W, DOC_H, fill=BLEED_FILL))
    body.append(rect(PX(0), PY(0), TRIM_W, TRIM_H, fill="#FFFFFF",
                     stroke=INK_LINE, sw=0.35))
    # grid 12 kolom di dalam safe area
    gutter, x = 4.0, 15.0
    colw = (TRIM_W - 15 - 12 - 11 * gutter) / 12.0
    for i in range(13):
        body.append(line(PX(x), PY(16), PX(x), PY(TRIM_H - 12), stroke="#8FB3A6",
                         sw=0.18, opacity=0.55, dash="1 1.4"))
        x += colw + gutter
    # zona jilid 15 mm
    body.append(rect(PX(0), PY(0), TRIM_W, 15, fill=BAND_FILL,
                     extra='fill-opacity="0.10"'))
    body.append(line(PX(0), PY(15), PX(TRIM_W), PY(15), stroke=EMERALD,
                     sw=0.35, dash="2 1.2"))
    body.append(text(PX(TRIM_W / 2), PY(9.4), "ZONA JILID WIRE-O  ·  15 mm  "
                     "·  WAJIB KOSONG DARI ELEMEN PENTING", 4.6, SANS_SEMI,
                     EMERALD, tracking=0.16, anchor="middle"))
    # lubang punch 3:1 pitch
    first = (TRIM_W - (N_HOLES - 1) * PITCH) / 2.0
    for i in range(N_HOLES):
        cx = PX(first + i * PITCH)
        body.append(circle(cx, PY(4.8), 2.4, fill="#FFFFFF", stroke=INK_LINE,
                           sw=0.22))
    body.append(line(PX(first), PY(4.8), PX(first + (N_HOLES - 1) * PITCH),
                     PY(4.8), stroke=INK_LINE, sw=0.15, dash="1 1.2"))
    # safe area
    body.append(rect(PX(15), PY(15), TRIM_W - 15 - 12, TRIM_H - 15 - 12,
                     stroke=GOLD, sw=0.3, dash="1.6 1.2"))
    body.append(text(PX(15.8), PY(TRIM_H - 13.2), "SAFE AREA 12 mm",
                     3.8, SANS_MED, GOLD_DEEP, tracking=0.12))
    return "".join(body)


def _dimensions():
    body = []
    # horizontal: trim & total
    body.append(_dim_h(PX(0), PX(TRIM_W), PY(-BLEED) - 3.4,
                       "213 mm  (lebar jadi)"))
    body.append(_dim_h(PX(-BLEED), PX(TRIM_W + BLEED), PY(-BLEED) - 9.6,
                       "219 mm termasuk bleed 3 mm"))
    # vertikal: trim & total
    body.append(_dim_v(PY(0), PY(TRIM_H), PX(TRIM_W + BLEED) + 8,
                       "152 mm"))
    body.append(_dim_v(PY(-BLEED), PY(TRIM_H + BLEED),
                       PX(TRIM_W + BLEED) + 17, "158 mm"))
    # zona jilid
    body.append(_dim_v(PY(0), PY(15), PX(0) - 7, "15 mm", side="left"))
    # margin bawah
    body.append(_dim_v(PY(TRIM_H - 12), PY(TRIM_H), PX(0) - 7, "12 mm",
                       side="left"))
    # pitch lubang (catatan diletakkan di bawah artboard)
    body.append(text(PX(0), PY(TRIM_H) + 8.0,
                     "23 lubang  ·  3:1 pitch (8,47 mm)  ·  Ø lubang 4,5–4,8 mm"
                     "  ·  jarak as lubang dari tepi atas 4,8 mm  ·  buku tebal "
                     "± 12 mm → wire Ø 9,5 mm", 4.0, SANS, GREY,
                     tracking=0.06))
    return "".join(body)


PALETTE = [
    ("Deep Emerald", EMERALD, "C85 M40 Y68 K38", "PANTONE 3435 C"),
    ("Emerald Mid", EMERALD_MID, "C82 M32 Y68 K18", "PANTONE 3415 C"),
    ("Navy Blue", NAVY, "C100 M88 Y45 K42", "PANTONE 289 C"),
    ("Warm Gold", GOLD, "C22 M33 Y100 K6", "PANTONE 1245 C / Foil 871"),
    ("Mint", MINT, "C36 M0 Y23 K0", "PANTONE 573 C"),
    ("Soft Beige", BEIGE, "C4 M6 Y14 K0", "PANTONE 7527 C"),
]


def _palette(y):
    body = [text(PX(0), y, "PALET WARNA  (CMYK coated / Pantone pendekatan)",
                 4.4, SANS_SEMI, INK_LINE, tracking=0.14)]
    x = PX(0)
    for name, hexv, cmyk, pms in PALETTE:
        body.append(rect(x, y + 3.2, 14, 14, fill=hexv, stroke="#D8D2C4",
                         sw=0.25, rx=1.4))
        body.append(text(x, y + 21.4, name, 3.9, SANS_SEMI, INK_LINE))
        body.append(text(x, y + 25.0, hexv.upper(), 3.6, SANS, GREY,
                         tracking=0.04))
        body.append(text(x, y + 28.4, cmyk, 3.4, SANS, GREY, tracking=0.02))
        body.append(text(x, y + 31.6, pms, 3.4, SANS, GREY, tracking=0.02))
        x += 31.0
    return "".join(body)


NOTES = [
    "1.  Ukuran jadi 213 × 152 mm (landscape). File kerja + bleed 3 mm = 219 × 158 mm.",
    "2.  Amankan zona jilid 15 mm di sisi atas: tanpa teks, logo, atau QR.",
    "3.  Resolusi gambar 300 dpi; teks minimal 4 pt; garis emas minimal 0,25 pt (hairline).",
    "4.  Warna final CMYK + 1 spot (Pantone 871 C untuk foil). Minta proof cetak (hard proof).",
    "5.  QR & logo OJK/LPS wajib diganti aset resmi sebelum naik cetak (konten di sini placeholder).",
]


def _notes(y):
    body = [text(PX(0), y, "CATATAN PRODUKSI", 4.4, SANS_SEMI, INK_LINE,
                 tracking=0.14)]
    yy = y + 5.0
    for n in NOTES:
        body.append(text(PX(0), yy, n, 3.9, SANS, "#3C3C38", tracking=0.01))
        yy += 4.4
    return "".join(body)


def build() -> str:
    body = (
        rect(0, 0, CANVAS_W, CANVAS_H, fill="#FBFAF5")
        + text(OFF_X, 14.0, "PANDUAN TEKNIS CETAK  —  KALENDER MEJA BANK SYARIAH",
               6.6, SERIF_SEMI, EMERALD_DEEP)
        + text(OFF_X, 19.4, "Skala 1:1  ·  satuan milimeter  ·  artwork 219 × 158 mm "
               "(termasuk bleed)", 4.2, SANS, GREY, tracking=0.1)
        + _artboard() + _crop_marks() + _dimensions()
        + _palette(PY(TRIM_H) + 22)
        + _notes(PY(TRIM_H) + 64)
    )
    return svg_doc(CANVAS_W, CANVAS_H, body)


if __name__ == "__main__":
    print(build()[:300])
