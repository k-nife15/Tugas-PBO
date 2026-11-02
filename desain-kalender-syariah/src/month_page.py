"""
month_page.py — Halaman bulanan kalender (Januari 2027 sebagai contoh).

Sisi A (depan)  : grid kalender 7 kolom × 5–6 baris + tanggal Hijriyah
Sisi B (belakang): halaman catatan & rencana bulanan
Keduanya 213 × 152 mm + bleed 3 mm, zona jilid 15 mm, safe area 12 mm.
"""
from __future__ import annotations

import math

from tokens import *
from svgkit import (f, svg_doc, grad_linear, grad_radial, foil_gradient, text,
                    rect, line, circle, path, group, rot)
import patterns as P
import calendar_data as C

# --- geometri grid kalender ---------------------------------------------
GX0, GW = 68.0, 19.0            # kolom mulai x = 68 mm, lebar 19 mm
GCOLS = 7
GT0 = 30.5                      # garis atas grid
GT1 = 132.5                     # garis bawah grid
DOW_BASELINE = 27.2

LEFT_X = 15.0
LEFT_W = 47.0                   # kolom identitas bulan (15 → 62)
DIV_X = 64.0                    # garis emas pemisah

YEAR = 2027
MONTH = 1
HOLIDAYS = C.HOLIDAYS_2027_01


def _defs(paper=("#FDFBF4", "#F6EFE0")):
    return "<defs>" + "".join([
        grad_linear("mp_paper", [(0, paper[0]), (1, paper[1])], 0, 0, 1, 1),
        grad_radial("mp_warm", [(0, "#FFFFFF", 0.55), (1, "#FFFFFF", 0.0)]),
        foil_gradient("foil", "d"),
    ]) + "</defs>"


def _brandmark(x, y, size=9.0, color=EMERALD, scale_text=1.0):
    """Logo mono + wordmark dua baris (dipakai semua halaman dalam)."""
    body = [
        rect(x, y, size, size, fill="none", stroke=color, sw=0.32,
             rx=size * 0.24),
        path(P.star8(x + size / 2, y + size / 2, size * 0.34, size * 0.19),
             stroke=color, sw=0.36),
        P.circle(x + size / 2, y + size / 2, size * 0.08, fill=color,
                 opacity=0.9),
        text(x + size + 3.6, y + size * 0.42, BRAND_LINE_1, 4.4 * scale_text,
             SANS_MED, INK_SOFT, tracking=0.22),
        text(x + size + 3.6, y + size * 0.94, BRAND_LINE_2, 5.8 * scale_text,
             SANS, color, weight="bold", tracking=0.14),
    ]
    return "".join(body)


def _top_rule():
    return line(X(0), Y(15), X(TRIM_W), Y(15), stroke=GOLD, sw=0.25,
                opacity=0.40)


# ======================================================================
# SISI A — GRID BULAN
# ======================================================================
def _identity_column():
    """Kolom kiri: logo, nama bulan, tahun, rentang Hijriyah, angka bulan."""
    body = [
        _brandmark(X(LEFT_X), Y(17.5)),
        line(X(DIV_X), Y(18), X(DIV_X), Y(140), stroke=GOLD, sw=0.25,
             opacity=0.45),
        text(X(LEFT_X), Y(41.0), "BULAN 01 / 12", 3.9, SANS_MED, GOLD_DEEP,
             tracking=0.24),
        text(X(LEFT_X), Y(52.0), C.GREG_MONTHS[MONTH - 1].upper(), 24.0,
             SERIF_SEMI, EMERALD_DEEP),
        text(X(LEFT_X), Y(58.6), str(YEAR), 10.0, SANS_SEMI, GOLD_DEEP,
             tracking=0.26),
        text(X(LEFT_X), Y(64.0), C.hijri_span(YEAR, MONTH), 4.0, SANS,
             EMERALD_MID, tracking=0.10, opacity=0.85),
        # angka bulan besar (aksen emas)
        text(X(LEFT_X), Y(88.0), f"{MONTH:02d}", 50.0, SERIF, "url(#foil)",
             weight="bold"),
    ]
    return "".join(body)


def _message_card():
    """Kartu pesan bulan — pengingat syariah, bukan kutipan ayat."""
    x, y, w, h = X(LEFT_X), Y(94), LEFT_W - 1, 34
    body = [
        rect(x, y, w, h, fill=MINT, extra='fill-opacity="0.10"', stroke=GOLD,
             sw=0.30, rx=2.6),
        rect(x + 1.1, y + 1.1, w - 2.2, h - 2.2, fill="none",
             stroke=GOLD_LIGHT, sw=0.16, opacity=0.55, rx=1.8),
        text(x + 3.2, y + 5.6, "PESAN BULAN INI", 3.5, SANS_SEMI, GOLD_DEEP,
             tracking=0.20),
        text(x + 3.2, y + 12.0, "Bulan baru, niat baru.", 8.2, SERIF_SEMI,
             EMERALD_DEEP),
        text(x + 3.2, y + 17.4, "Kelola rezeki dengan", 7.4, SERIF,
             EMERALD_MID),
        text(x + 3.2, y + 22.8, "amanah dan transparan.", 7.4, SERIF,
             EMERALD_MID),
        path(P.star8(x + w - 5.2, y + h - 5.0, 2.4, 1.35), stroke=GOLD,
             sw=0.24, opacity=0.8),
    ]
    return "".join(body)


def _dow_header():
    body = []
    for i, name in enumerate(C.DAY_SHORT):
        weekend = i >= 5
        body.append(text(X(GX0 + i * GW + GW / 2), Y(DOW_BASELINE), name, 4.0,
                         SANS_SEMI, GOLD_DEEP if weekend else EMERALD,
                         tracking=0.20, anchor="middle",
                         opacity=1.0 if weekend else 0.85))
    body.append(line(X(GX0), Y(DOW_BASELINE + 1.8), X(GX0 + GCOLS * GW),
                     Y(DOW_BASELINE + 1.8), stroke=GOLD, sw=0.3, opacity=0.55))
    return "".join(body)


def _grid():
    weeks = C.month_grid(YEAR, MONTH)
    used = [w for w in weeks if any(d.month == MONTH for d in w)]
    n_rows = len(used)
    rh = (GT1 - GT0) / n_rows
    body = []

    # 1. tint kolom akhir pekan (Sabtu–Ahad)
    for i in (5, 6):
        body.append(rect(X(GX0 + i * GW), Y(GT0), GW, GT1 - GT0, fill=MINT,
                         extra='fill-opacity="0.12"'))

    # 2. garis grid
    for r in range(n_rows + 1):
        yy = Y(GT0 + r * rh)
        body.append(line(X(GX0), yy, X(GX0 + GCOLS * GW), yy, stroke=EMERALD,
                         sw=0.22, opacity=0.30 if r in (0, n_rows) else 0.16))
    for c in range(GCOLS + 1):
        xx = X(GX0 + c * GW)
        body.append(line(xx, Y(GT0), xx, Y(GT1), stroke=EMERALD, sw=0.22,
                         opacity=0.30 if c in (0, GCOLS) else 0.16))

    # 3. isi sel
    for r, wk in enumerate(used):
        for c, d in enumerate(wk):
            cx, cy = X(GX0 + c * GW), Y(GT0 + r * rh)
            base = cy + 8.4
            if d.month != MONTH:                      # tanggal bulan tetangga
                body.append(text(cx + 2.8, base, str(d.day), 8.6, SANS,
                                 EMERALD, weight="bold", opacity=0.20))
                continue
            holiday = HOLIDAYS.get(d.day)
            if holiday:
                body.append(rect(cx, cy, GW, rh, fill=GOLD,
                                 extra='fill-opacity="0.12"'))
                body.append(circle(cx + GW - 3.2, cy + 3.6, 0.85, fill=GOLD,
                                   opacity=0.95))
            body.append(text(cx + 2.8, base, str(d.day), 9.4, SANS,
                             EMERALD_DEEP, weight="bold"))
            _, _, hd = C.hijri_of(d)
            body.append(text(cx + GW - 2.6, base, str(hd), 3.8, SANS_MED,
                             GOLD_DEEP, anchor="end", opacity=0.9))
            if holiday:
                body.append(text(cx + 2.8, cy + 13.8, holiday, 3.2, SANS_MED,
                                 GOLD_DEEP, tracking=0.04))
    return "".join(body)


def _legend():
    y = 139.2
    body = [
        rect(X(LEFT_X), Y(y) - 1.5, 3.0, 3.0, fill=GOLD,
             extra='fill-opacity="0.45"'),
        text(X(LEFT_X + 4.4), Y(y), "Hari besar", 3.6, SANS, INK_SOFT,
             opacity=0.8),
        rect(X(LEFT_X + 22), Y(y) - 1.5, 3.0, 3.0, fill=MINT,
             extra='fill-opacity="0.5"'),
        text(X(LEFT_X + 26.4), Y(y), "Akhir pekan", 3.6, SANS, INK_SOFT,
             opacity=0.8),
        text(X(201), Y(y), "Angka kecil = tanggal Hijriyah (perkiraan hisab; "
             "verifikasi takwim Kemenag)", 3.5, SANS, INK_SOFT, anchor="end",
             opacity=0.55),
    ]
    return "".join(body)


def build_front() -> str:
    body = (
        _defs()
        + rect(0, 0, DOC_W, DOC_H, fill="url(#mp_paper)")
        + rect(X(60), Y(-30), 150, 110, fill="url(#mp_warm)")
        + _top_rule()
        + _identity_column()
        + _message_card()
        + _dow_header()
        + _grid()
        + _legend()
    )
    return svg_doc(DOC_W, DOC_H, body)


# ======================================================================
# SISI B — HALAMAN CATATAN & RENCANA
# ======================================================================
def _dotted(x1, x2, y, opacity=0.22):
    return line(X(x1), Y(y), X(x2), Y(y), stroke=EMERALD_MID, sw=0.20,
                dash="0.9 1.5", opacity=opacity)


def _plan_rows():
    """Daftar rencana bulan dengan kotak centang (kiri)."""
    body = [
        text(X(15), Y(70.0), "RENCANA BULAN INI", 4.2, SANS_SEMI, GOLD_DEEP,
             tracking=0.22),
        line(X(15), Y(72.6), X(34), Y(72.6), stroke=GOLD, sw=0.35, opacity=0.8),
    ]
    y = 78.4
    for _ in range(6):
        body.append(rect(X(15), Y(y) - 1.3, 2.6, 2.6, fill="none",
                         stroke=EMERALD, sw=0.24, rx=0.5, opacity=0.55))
        body.append(_dotted(19.6, 98.0, y + 1.3))
        y += 4.6
    return "".join(body)


def _note_lines():
    """Garis catatan bebas (kanan)."""
    body = [
        text(X(106), Y(70.0), "CATATAN", 4.2, SANS_SEMI, GOLD_DEEP,
             tracking=0.22),
        line(X(106), Y(72.6), X(122), Y(72.6), stroke=GOLD, sw=0.35,
             opacity=0.8),
    ]
    y = 78.4
    for _ in range(6):
        body.append(_dotted(106.0, 201.0, y + 1.3))
        y += 4.6
    return "".join(body)


def _quote_card():
    x, y, w, h = X(15), Y(108), 186, 23
    body = [
        rect(x, y, w, h, fill=MINT, extra='fill-opacity="0.10"', stroke=GOLD,
             sw=0.30, rx=2.6),
        rect(x + 1.1, y + 1.1, w - 2.2, h - 2.2, fill="none",
             stroke=GOLD_LIGHT, sw=0.16, opacity=0.5, rx=1.8),
        path(P.star8(x + 10.5, y + h / 2, 4.6, 2.6), stroke=GOLD, sw=0.26,
             opacity=0.85),
        P.circle(x + 10.5, y + h / 2, 0.7, fill=GOLD, opacity=0.85),
        text(x + 20.0, y + 10.6, "Setiap amanah yang dijaga adalah",
             10.5, SERIF_SEMI, EMERALD_DEEP),
        text(x + 20.0, y + 17.2, "keberkahan yang tumbuh bersama nasabah.",
             10.5, SERIF_SEMI, EMERALD_DEEP),
    ]
    return "".join(body)


def _watermark():
    """Motif samar di belakang kolom catatan (tidak mengganggu tulisan)."""
    cx, cy = X(170), Y(40)
    return "".join([
        group(P.girih_octagram(cx, cy, 21, sw=0.28, opacity=1.0,
                               spokes=False, rings=(0.56,)), opacity=0.09),
        group(P.rosette(cx, cy, 20.2, 7.0, petals=16, sw=0.26, opacity=1.0),
              opacity=0.08),
    ])


def build_back() -> str:
    body = (
        _defs(("#FDFBF4", "#F7F0E1"))
        + rect(0, 0, DOC_W, DOC_H, fill="url(#mp_paper)")
        + rect(X(40), Y(-30), 170, 120, fill="url(#mp_warm)")
        + _top_rule()
        + _brandmark(X(15), Y(17.5))
        + text(X(15), Y(41.0), "HALAMAN CATATAN", 3.9, SANS_MED, GOLD_DEEP,
               tracking=0.24)
        + text(X(15), Y(51.0), f"{C.GREG_MONTHS[MONTH - 1]} {YEAR}", 19.0,
               SERIF_SEMI, EMERALD_DEEP)
        + text(X(15), Y(56.4), C.hijri_span(YEAR, MONTH), 4.0, SANS,
               EMERALD_MID, tracking=0.10, opacity=0.85)
        + _watermark()
        + line(X(102), Y(68), X(102), Y(103), stroke=GOLD, sw=0.25,
               opacity=0.40)
        + _plan_rows()
        + _note_lines()
        + _quote_card()
        + text(X(201), Y(137.6), f"{MONTH:02d}", 5.4, SANS_SEMI, GOLD_DEEP,
               tracking=0.18, anchor="end", opacity=0.8)
        + text(X(15), Y(137.6), "Nama Bank Syariah  ·  Kalender Meja 2027",
               3.7, SANS, INK_SOFT, tracking=0.06, opacity=0.5)
    )
    return svg_doc(DOC_W, DOC_H, body)


if __name__ == "__main__":
    print(build_front()[:200])
    print(build_back()[:200])
