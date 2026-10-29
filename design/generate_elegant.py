#!/usr/bin/env python3
"""
Varian 2: Kalender Meja Januari 2027 - arah ELEGAN - ISLAMI - BUSINESS.

Karakter: serif klasik (Marcellus), huruf kecil ber-tracking lebar (Lato),
palet navy/emerald/antique-gold di atas kertas krem, garis rambut emas,
ornamen geometri Islam (khatim 8 sudut) dan panel mihrab. Tanpa doodle kartun.

Output: dist/kalender-januari-2027-elegan.* (SVG master + PNG/PDF via pipeline
render yang sama).
"""
import base64
import json

from common import (ASSETS, CELLS, DIST, HIJRI_MONTHS, WEEKDAYS, arch, diamond,
                    line, rrect, star8, text, tw, wrap)

# ----------------------------------------------------------------------------
# KONFIGURASI
# ----------------------------------------------------------------------------
W, H = 794, 559
FRAME_OUT, FRAME_IN = 10, 14
M = 30
LEFT_X, LEFT_W = 30, 252
RIGHT_X, RIGHT_W = 298, 466
CARD_Y, CARD_H = 80, 384
PAD = 18

# Palet
PAPER = "#F7F3EA"
PANEL = "#FFFFFF"
INK = "#14263C"
NAVY = "#0F2540"
EMERALD = "#0B5D45"
EMERALD_SOFT = "#F1F7F3"
GOLD = "#B08D3F"
GOLD_LIGHT = "#D9C48A"
GOLD_SOFT = "#FBF4E2"
LINE = "#E4DCC9"
MUTED = "#7C8A99"
TAIL = "#B7C0CA"
TAIL_SOFT = "#CBD3DB"

F_TITLE = "Marcellus"
F_BODY = "Lato"

# Konten
BRAND_SUB = "Bank Mitra Syariah"
BRAND_TAG = "Pilihan Amanah Keluarga"
KICKER = "PROGRAM SIMIRA"
KICKER_SUB = "Simpanan Mitra Rencana"
HEADLINE = ["Tabungan", "Umroh Mitra"]
BODY = ["Hajilah tahun ini menjadi do'a,", "Umroh tahun depan menjadi nyata."]
PRICE_LABEL = "MULAI DARI"
PRICE_MAIN = "Rp40.000,-"
PRICE_SUB = "/ hari"
BENEFITS = ["Mudah Pendaftaran", "Transparan Kelolaannya",
            "Aman dan Amanah", "Menarik bagi hasilnya"]
FOOT = "Travel PPU & PIHK Terpercaya"
HIJRI_LINE = "RAJAB \u2013 SYA'BAN 1448 H    \u00b7    REJEB \u2013 RUWAH 1960 DAL"
OJK = ["PT BPRS Mitra Mentari Sejahtera  \u00b7  Berizin & Diawasi oleh OJK",
       "dan Merupakan Peserta Penjaminan (LPS)"]
CONTACT = "0813-1349-9673   \u00b7   mitrasyariahbank.co.id   \u00b7   @mitrasyariahbank"
ADDRESS = "Jl. Ayunda No. 23, Panorama, Bengkulu"

# Libur & puasa (sumber sama dengan varian playful: common.CELLS)
HOLIDAY_SET = {"2027-01-01", "2027-01-06"}
PUASA_SET = {"2027-01-22", "2027-01-23", "2027-01-24"}
NOTES = [
    ("1 Januari", "Tahun Baru 2027 Masehi"),
    ("6 Januari", "Isra' Mi'raj Nabi Muhammad SAW 1448 H"),
    ("22\u201324 Januari", "Puasa Sunnah Ayyamul Bidh (13\u201315 Sya'ban 1448 H)"),
]


def logo_uri():
    data = base64.b64encode((ASSETS / "logo-brand.png").read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def defs():
    return f"""<defs>
  <pattern id="khatim" width="58" height="58" patternUnits="userSpaceOnUse">
    <g stroke="{GOLD}" stroke-width="0.5" fill="none" opacity="0.5">
      {star8(29, 29, 15, stroke=GOLD, sw=0.5)}
      {star8(0, 0, 12, stroke=GOLD, sw=0.4)}
      {star8(58, 0, 12, stroke=GOLD, sw=0.4)}
      {star8(0, 58, 12, stroke=GOLD, sw=0.4)}
      {star8(58, 58, 12, stroke=GOLD, sw=0.4)}
    </g>
  </pattern>
  <linearGradient id="goldRule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{GOLD}" stop-opacity="1"/>
    <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </linearGradient>
</defs>"""


# ----------------------------------------------------------------------------
# 1. LATAR, BINGKAI, KEPALA
# ----------------------------------------------------------------------------
def background():
    p = [rrect(0, 0, W, H, 0, PAPER)]
    p.append(f'<g opacity="0.085">{rrect(0, 0, W, H, 0, "url(#khatim)")}</g>')
    # bingkai ganda (khas cetak formal)
    p.append(rrect(FRAME_OUT, FRAME_OUT, W - 2 * FRAME_OUT, H - 2 * FRAME_OUT, 0,
                   "none", GOLD, 0.9))
    p.append(rrect(FRAME_IN, FRAME_IN, W - 2 * FRAME_IN, H - 2 * FRAME_IN, 0,
                   "none", GOLD_LIGHT, 0.5))
    for cx, cy in [(FRAME_IN + 9, FRAME_IN + 9), (W - FRAME_IN - 9, FRAME_IN + 9),
                   (FRAME_IN + 9, H - FRAME_IN - 9),
                   (W - FRAME_IN - 9, H - FRAME_IN - 9)]:
        p.append(star8(cx, cy, 6.5, stroke=GOLD, sw=0.7, opacity=0.75))
    return "".join(p)


def header():
    p = [f'<image x="{M}" y="26" width="132" height="24.75" '
         f'xlink:href="{logo_uri()}" preserveAspectRatio="xMinYMid meet"/>']
    p.append(text(764, 35, BRAND_SUB.upper(), 7.6, 800, INK, anchor="end", ls=2.4,
                  family=F_BODY))
    p.append(text(764, 46, BRAND_TAG, 6.4, 400, MUTED, anchor="end", ls=1.2,
                  family=F_BODY))
    p.append(line(M, 64, 764, 64, "url(#goldRule)", 1))
    p.append(rrect(391, 60.5, 12, 7, 1, PAPER))
    p.append(diamond(397, 64, 3.4, GOLD))
    return "".join(p)


def left_panel():
    p = [rrect(LEFT_X, CARD_Y, LEFT_W, CARD_H, 2, PANEL, LINE, 0.9)]
    cx = LEFT_X + LEFT_W / 2
    # motif mihrab kecil
    ax, ay, aw, ah = cx - 28, 94, 56, 56
    sh = ay + ah * 0.80            # lengkung lancip (lancet) khas mihrab
    p.append(f'<path d="M {ax} {ay + ah} L {ax} {sh} Q {ax} {ay + 4} '
             f'{ax + aw / 2} {ay} Q {ax + aw} {ay + 4} {ax + aw} {sh} '
             f'L {ax + aw} {ay + ah} Z" fill="{GOLD_SOFT}" stroke="{GOLD}" '
             f'stroke-width="0.9"/>')
    p.append(diamond(cx, 92.5, 3.2, GOLD))
    p.append(star8(cx, 121, 7.5, stroke=GOLD, sw=0.8))
    p.append(diamond(cx, 121, 2.2, GOLD))

    x = LEFT_X + PAD
    p.append(text(x, 160, KICKER, 6.4, 800, EMERALD, ls=2.4, family=F_BODY))
    p.append(text(x, 172, KICKER_SUB, 6.2, 400, MUTED, ls=0.6, family=F_BODY))

    p.append(text(x - 0.5, 200, HEADLINE[0], 21, 400, NAVY, family=F_TITLE))
    p.append(text(x - 0.5, 226, HEADLINE[1], 21, 400, NAVY, family=F_TITLE))

    p.append(line(x, 238, x + 24, 238, GOLD, 0.9))
    p.append(diamond(x + 30, 238, 2.8, GOLD))
    p.append(line(x + 36, 238, x + 60, 238, GOLD, 0.9))

    for i, ln in enumerate(BODY):
        p.append(text(x, 256 + i * 11, ln, 7.4, 400, MUTED, family=F_BODY))

    p.append(text(x, 292, PRICE_LABEL, 5.6, 800, MUTED, ls=1.8, family=F_BODY))
    p.append(text(x - 1, 316, PRICE_MAIN, 19, 700, GOLD, ls=0.4, family=F_BODY))
    pw = tw(PRICE_MAIN, 19, 700, ls=0.4, family=F_BODY)
    p.append(text(x + pw + 4, 315, PRICE_SUB, 6.8, 400, MUTED, family=F_BODY))

    p.append(line(x, 328, LEFT_X + LEFT_W - PAD, 328, LINE, 0.8))

    by = 346
    for b in BENEFITS:
        p.append(diamond(x + 2.5, by - 2.6, 2.5, GOLD))
        p.append(text(x + 12, by, b, 7.6, 400, INK, family=F_BODY))
        by += 16

    p.append(text(x, 424, FOOT, 5.9, 400, MUTED, ls=0.4, family=F_BODY))
    p.append(line(x, 434, LEFT_X + LEFT_W - PAD, 434, LINE, 0.6, opacity=0.8))
    p.append(text(cx, 448, KICKER + "  \u00b7  " + KICKER_SUB.upper(), 5.4, 700,
                  GOLD, anchor="middle", ls=1.6, family=F_BODY, opacity=0.9))
    return "".join(p)




# ----------------------------------------------------------------------------
# 2. PANEL KALENDER
# ----------------------------------------------------------------------------
IX = RIGHT_X + PAD
IW = RIGHT_W - 2 * PAD
IY, IB = CARD_Y + PAD, CARD_Y + CARD_H - PAD       # 98 .. 446
GRID_TOP = 188
ROW_H = (IB - GRID_TOP) / 6                        # 43
COL_W = IW / 7


def calendar_panel():
    p = [rrect(RIGHT_X, CARD_Y, RIGHT_W, CARD_H, 2, PANEL, LINE, 0.9)]

    # ---- judul bulan (serif)
    p.append(text(IX - 1, 130, "JANUARI", 30, 400, NAVY, ls=2.4, family=F_TITLE))
    jw = tw("JANUARI", 30, 400, 2.4, family=F_TITLE)
    p.append(text(IX + jw + 9, 129, "2027", 28, 400, GOLD, ls=3.2, family=F_BODY))

    # ---- cincin nomor bulan
    rc = 16
    p.append(f'<circle cx="730" cy="114" r="{rc}" fill="none" stroke="{GOLD}" '
             f'stroke-width="0.9"/>')
    p.append(f'<circle cx="730" cy="114" r="{rc - 3.5}" fill="none" '
             f'stroke="{GOLD_LIGHT}" stroke-width="0.5"/>')
    p.append(text(730, 118, "01", 12, 700, NAVY, anchor="middle", ls=0.6,
                  family=F_BODY))
    p.append(text(730, 139, "BULAN", 4.4, 700, MUTED, anchor="middle", ls=1.4,
                  family=F_BODY))

    # ---- baris hijriah
    p.append(text(IX, 152, HIJRI_LINE, 6.8, 700, GOLD, ls=1.7, family=F_BODY))

    # ---- garis ganda
    p.append(line(IX, 163, RIGHT_X + RIGHT_W - PAD, 163, GOLD, 0.9))
    p.append(line(IX, 166, RIGHT_X + RIGHT_W - PAD, 166, GOLD_LIGHT, 0.6,
                  opacity=0.9))

    # ---- header hari
    for i, name in enumerate(WEEKDAYS):
        cx = IX + COL_W * (i + 0.5)
        color = GOLD if i == 0 else (EMERALD if i == 5 else MUTED)
        p.append(text(cx, 184, name.upper(), 6.4, 700, color, anchor="middle",
                      ls=1.5, family=F_BODY))
    p.append(line(IX, GRID_TOP, RIGHT_X + RIGHT_W - PAD, GRID_TOP, LINE, 0.7))

    # ---- tint sel khusus (sebelum garis tabel)
    for c in CELLS:
        d = c["date"]
        tint = None
        if d in HOLIDAY_SET:
            tint = EMERALD_SOFT
        elif d in PUASA_SET:
            tint = GOLD_SOFT
        if tint:
            x = IX + c["col"] * COL_W
            y = GRID_TOP + c["row"] * ROW_H
            p.append(rrect(x + 0.6, y + 0.6, COL_W - 1.2, ROW_H - 1.2, 0, tint))

    # ---- garis tabel
    for i in range(1, 7):
        x = IX + i * COL_W
        p.append(line(x, GRID_TOP, x, IB, LINE, 0.7))
    for r in range(1, 6):
        y = GRID_TOP + r * ROW_H
        p.append(line(IX, y, RIGHT_X + RIGHT_W - PAD, y, LINE, 0.7))
    # penutup tabel (kiri, kanan, bawah)
    p.append(line(IX, GRID_TOP, IX, IB, LINE, 0.7))
    p.append(line(RIGHT_X + RIGHT_W - PAD, GRID_TOP, RIGHT_X + RIGHT_W - PAD, IB,
                  LINE, 0.7))
    p.append(line(IX, IB, RIGHT_X + RIGHT_W - PAD, IB, LINE, 0.7))

    # ---- isi sel
    for c in CELLS:
        d = c["date"]
        cx = IX + COL_W * (c["col"] + 0.5)
        y = GRID_TOP + c["row"] * ROW_H
        if d in HOLIDAY_SET:
            num_c, sub_c = EMERALD, "#5F8A79"
        elif d in PUASA_SET:
            num_c, sub_c = GOLD, "#A98B4B"
        elif not c["in_month"]:
            num_c, sub_c = TAIL, TAIL_SOFT
        elif c["col"] == 0:
            num_c, sub_c = GOLD, MUTED
        elif c["col"] == 5:
            num_c, sub_c = EMERALD, MUTED
        else:
            num_c, sub_c = INK, MUTED

        p.append(text(cx, y + 23, str(c["day"]), 13.5, 700, num_c,
                      anchor="middle", family=F_BODY))
        p.append(text(cx, y + 34, f"{c['hijri_day']} {c['pasaran']}", 5.6, 400,
                      sub_c, anchor="middle", ls=0.5, family=F_BODY))
        if d in HOLIDAY_SET:
            p.append(diamond(cx + COL_W / 2 - 8, y + 10, 2.2, GOLD))
    return "".join(p)


# ----------------------------------------------------------------------------
# 3. CATATAN & KAKI
# ----------------------------------------------------------------------------
def notes_and_footer():
    p = [line(M, 478, 764, 478, "url(#goldRule)", 1)]
    p.append(diamond(397, 478, 3.4, GOLD))
    p.append(rrect(391, 474.5, 12, 7, 1, PAPER))

    # --- catatan hari libur (auto-fit lebar)
    widths, fs = [], 6.1
    for fs in (6.1, 5.8, 5.5, 5.2):
        widths = [tw(f"{a}  \u00b7  {b}", fs, 400, family=F_BODY) for a, b in NOTES]
        if sum(widths) + 2 * 24 + 3 * 9 <= 734:
            break
    x = M
    for (a, b), w in zip(NOTES, widths):
        p.append(diamond(x + 2.4, 493, 2.4, GOLD))
        aw = tw(a, fs, 800, family=F_BODY)
        p.append(text(x + 9, 495, a, fs, 800, INK, family=F_BODY))
        p.append(text(x + 9 + aw + 4, 495, "\u00b7  " + b, fs, 400, MUTED,
                      family=F_BODY))
        x += w + 24

    # --- kaki: legal + kontak
    p.append(line(M, 506, 764, 506, LINE, 0.6, opacity=0.9))
    p.append(text(M, 519, OJK[0] + "  " + OJK[1], 5.5, 400, MUTED, family=F_BODY))
    p.append(text(764, 519, CONTACT, 6.0, 700, INK, anchor="end", family=F_BODY))
    return "".join(p)


# ----------------------------------------------------------------------------
# 4. ASSEMBLY
# ----------------------------------------------------------------------------
def build_svg():
    body = "".join([background(), header(), left_panel(), calendar_panel(),
                    notes_and_footer()])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs()}{body}</svg>')


def main():
    svg = build_svg()
    (DIST / "kalender-januari-2027-elegan.svg").write_text(svg, encoding="utf-8")
    meta = {
        "title": "Kalender Meja Januari 2027 - BPRS Mitra Mentari Sejahtera",
        "variant": "elegan-islami-business",
        "month": "Januari 2027",
        "size_px": [W, H],
        "palette": {"paper": PAPER, "navy": NAVY, "emerald": EMERALD,
                    "gold": GOLD, "gold_light": GOLD_LIGHT, "line": LINE,
                    "muted": MUTED},
        "fonts": {"display": "Marcellus", "body": "Lato"},
        "cells": CELLS,
    }
    (DIST / "kalender-januari-2027-elegan-data.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SVG + JSON elegan written to", DIST)


if __name__ == "__main__":
    main()
