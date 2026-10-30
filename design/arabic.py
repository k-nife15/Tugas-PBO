#!/usr/bin/env python3
"""
Shaper teks Arab -> path SVG (vektor).

Kenapa perlu: renderer resvg TIDAK melakukan shaping kompleks (tanpa HarfBuzz),
sehingga teks Arab akan tampil terpisah-pisah dan urutannya salah. Modul ini
memakai HarfBuzz (uharfbuzz) untuk shaping + fontTools untuk mengambil outline
glyph, lalu menghasilkan satu `<path>` yang tipis dan tajam di semua ukuran.
"""
from functools import lru_cache

import re

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from common import ASSETS

FONT_DIR = ASSETS / "fonts"

# Nama hari & bulan dalam bahasa Arab
WEEKDAYS_AR = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة",
               "السبت"]
MONTHS_AR = {
    "Muharram": "محرم", "Safar": "صفر", "Rabiul Awal": "ربيع الأول",
    "Rabiul Akhir": "ربيع الآخر", "Jumadil Awal": "جمادى الأولى",
    "Jumadil Akhir": "جمادى الآخرة", "Rajab": "رجب", "Sya'ban": "شعبان",
    "Ramadhan": "رمضان", "Syawal": "شوال", "Dzulqadah": "ذو القعدة",
    "Dzulhijjah": "ذو الحجة",
}
_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

# run: angka Latin/Arab-Indik (LTR) | kata Arab (RTL) | spasi
_RUN_RE = re.compile(r"([0-9\u0660-\u0669]+)|(\s+)|([^\s0-9\u0660-\u0669]+)")


def ar_digits(n):
    """Ubah angka Latin -> angka Arab-Indik (٢٢)."""
    return str(n).translate(_DIGITS)


@lru_cache(maxsize=8)
def _font(font_file):
    path = str(FONT_DIR / font_file)
    tt = TTFont(path)
    face = hb.Face(hb.Blob.from_file_path(path))
    return tt, hb.Font(face), tt["head"].unitsPerEm, tt.getGlyphSet()


@lru_cache(maxsize=8192)
def _shape_run(text, size, font_file, direction):
    """Shape satu run; kembalikan (path_d, lebar). Urutan visual siap digambar."""
    tt, hb_font, upem, glyphset = _font(font_file)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = direction
    buf.script = "Arab"
    buf.language = "ar"
    hb.shape(hb_font, buf)

    scale = size / upem
    order = tt.getGlyphOrder()
    x = 0.0
    parts = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(glyphset)
        tpen = TransformPen(
            pen, (scale, 0, 0, -scale,
                  x + pos.x_offset * scale, -pos.y_offset * scale))
        glyphset[order[info.codepoint]].draw(tpen)
        cmd = pen.getCommands()
        if cmd:
            parts.append(cmd)
        x += pos.x_advance * scale
    return " ".join(parts), x


def shape(text, size, font_file="NotoNaskhArabic[wght].ttf"):
    """Shape satu baris campuran (angka + Arab) dengan urutan visual RTL.

    Kembalikan (path_d, lebar_px). Baseline path di y=0, arah y ke bawah.
    """
    runs = []
    for m in _RUN_RE.finditer(text):
        if m.group(1):
            runs.append((m.group(1), "ltr"))     # angka tetap LTR
        elif m.group(2):
            runs.append((" ", "ltr"))
        else:
            runs.append((m.group(3), "rtl"))
    shaped = [(t, *_shape_run(t, size, font_file, d)) for t, d in runs]
    total = sum(w for _, _, w in shaped)

    # Susun dari kanan ke kiri (bidi sederhana untuk teks berbasis Arab)
    cursor = total
    parts = []
    for _, d, w in shaped:
        cursor -= w
        if d:
            parts.append(f'<g transform="translate({cursor:.2f} 0)"><path d="{d}"/></g>')
    return "".join(parts), total


def ar_text(x, y, text, size, fill, anchor="start",
            font_file="NotoNaskhArabic[wght].ttf", opacity=1.0):
    """Teks Arab sebagai path SVG. `y` = baseline."""
    frag, w = shape(text, size, font_file)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    o = f' opacity="{opacity}"' if opacity != 1 else ""
    # fill diwariskan ke path di dalam grup
    return (f'<g transform="translate({x:.2f} {y:.2f})" fill="{fill}"{o}>'
            f'{frag}</g>'), w


def ar_width(text, size, font_file="NotoNaskhArabic[wght].ttf"):
    return shape(text, size, font_file)[1]
