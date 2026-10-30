#!/usr/bin/env python3
"""
Kalender Meja Januari 2027 - 21,3 x 15,2 cm - CORPORATE ELEGANT.
Dasar putih bersih, struktur tegas (blok navy, garis rambut, label small-caps),
aksen biru - hijau - emas. Tiga penanggalan per sel:
MASEHI (angka besar) + HIJRIAH (angka & bulan Arab) + JAWA (pasaran).

Kanvas 2130 x 1520 px @ 10 px/mm -> 213 x 152 mm (254 dpi).

Output: dist/kalender-2027-biru-hijau-emas.*
"""
import base64
import json

from arabic import MONTHS_AR, WEEKDAYS_AR, ar_digits, ar_text, ar_width
from common import (ASSETS, CELLS, DIST, WEEKDAYS, diamond, line, rrect, star8,
                    text, tw, wrap)

# ----------------------------------------------------------------------------
# KONFIGURASI
# ----------------------------------------------------------------------------
W, H = 2130, 1520
M = 56

LX, LW = 56, 744             # kolom kiri (foto + promo)
RX, RW = 840, 1234           # kolom kanan (kalender)
TOP, BOT = 200, 1330
PHOTO_H = 430
PROMO_Y = 648

CARD_PAD = 56
IX = RX + CARD_PAD            # 896
IW = RW - 2 * CARD_PAD        # 1122
HEAD_H = 196                  # blok navy judul
GRID_TOP, GRID_BOT = 540, 1240
ROW_H = (GRID_BOT - GRID_TOP) / 6      # 116.7
COL_W = IW / 7                         # 160.3

# Palet corporate: putih + navy / biru / hijau / emas
WHITE = "#FFFFFF"
NAVY = "#0B2E4F"
BLUE = "#12557F"
BLUE_SOFT = "#F1F6FA"
GREEN = "#0D6B4F"
GREEN_SOFT = "#EEF6F1"
GOLD = "#B58A2B"
GOLD_BRIGHT = "#D4AF37"
GOLD_SOFT = "#FBF5E6"
HAIR = "#E3E7EE"
MUTED = "#7C8894"
TAIL = "#BFC8D2"

F_TITLE = "Marcellus"
F_BODY = "Lato"

PHOTO_FILE = "foto-promo.png"
PHOTO_PLACEHOLDER = False            # True -> slot foto kosong + label

# Konten
BRAND = "BANK MITRA SYARIAH"
BRAND_TAG = "Pilihan Amanah Keluarga"
HEAD_TAG = "KALENDER MEJA  \u00b7  2027"
EYEBROW = "PROGRAM SIMIRA"
EYEBROW_SUB = "Simpanan Mitra Rencana"
HEADLINE = ["Tabungan", "Umroh Mitra"]
BODY = ["Hajilah tahun ini menjadi do'a,",
        "Umroh tahun depan menjadi nyata."]
PRICE_LABEL = "MULAI DARI"
PRICE_MAIN = "Rp40.000,-"
PRICE_SUB = "/ hari"
BENEFITS = ["Mudah Pendaftaran", "Transparan Kelolaannya",
            "Aman dan Amanah", "Menarik bagi hasilnya"]
FOOT = "Travel PPU & PIHK Terpercaya"
CAPTION = "PROGRAM UMROH 2027"
H_MONTH_LINE = "RAJAB \u2013 SYA'BAN 1448 H"
J_MONTH_LINE = "REJEB \u2013 RUWAH 1960 DAL"
OJK = ("PT BPRS Mitra Mentari Sejahtera   \u00b7   Berizin & Diawasi oleh OJK   "
       "\u00b7   Peserta Penjaminan LPS")
CONTACT = "0813-1349-9673   \u00b7   mitrasyariahbank.co.id   \u00b7   @mitrasyariahbank"

HOLIDAYS = [
    (BLUE, "1 Januari", "Tahun Baru 2027 Masehi"),
    (GREEN, "6 Januari", "Isra' Mi'raj Nabi Muhammad SAW 1448 H"),
    (GOLD, "22\u201324 Januari", "Puasa Sunnah Ayyamul Bidh (13\u201315 Sya'ban 1448 H)"),
]
HOLIDAY_SET = {"2027-01-01", "2027-01-06"}
PUASA_SET = {"2027-01-22", "2027-01-23", "2027-01-24"}

JAV_MONTHS = {
    "Muharram": "Sura", "Safar": "Sapar", "Rabiul Awal": "Mulud",
    "Rabiul Akhir": "Bakda Mulud", "Jumadil Awal": "Jumadilawal",
    "Jumadil Akhir": "Jumadilakir", "Rajab": "Rejeb", "Sya'ban": "Ruwah",
    "Ramadhan": "Pasa", "Syawal": "Sawal", "Dzulqadah": "Sela",
    "Dzulhijjah": "Besar",
}
JAV_YEARS = ["Dal", "Be", "Wawu", "Jimakir", "Alip", "Ehe", "Jimawal", "Je"]

for c in CELLS:
    c["jav_day"] = c["hijri_day"]
    c["jav_month"] = JAV_MONTHS[c["hijri_month"]]
    c["jav_year"] = c["hijri_year"] + 512
    c["jav_year_name"] = JAV_YEARS[c["jav_year"] % 8]


def fit(s, size, weight, max_w, family=F_BODY, min_size=10.0):
    while tw(s, size, weight, family=family) > max_w and size > min_size:
        size -= 0.5
    return size


def logo_uri():
    data = base64.b64encode((ASSETS / "logo-brand.png").read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def photo_uri():
    data = base64.b64encode((ASSETS / PHOTO_FILE).read_bytes()).decode()
    return f"data:image/png;base64,{data}"


# ----------------------------------------------------------------------------
# 1. LATAR & KEPALA
# ----------------------------------------------------------------------------
def defs():
    return f"""<defs>
  <linearGradient id="navyGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{NAVY}"/><stop offset="0.62" stop-color="#12456F"/>
    <stop offset="1" stop-color="{BLUE}"/>
  </linearGradient>
  <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#E3C56B"/><stop offset="0.5" stop-color="{GOLD_BRIGHT}"/>
    <stop offset="1" stop-color="#A97F22"/>
  </linearGradient>
  <linearGradient id="photoFade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{NAVY}" stop-opacity="0.55"/>
    <stop offset="1" stop-color="{NAVY}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="photoClip">
    <rect x="{LX}" y="{TOP}" width="{LW}" height="{PHOTO_H}"/>
  </clipPath>
</defs>"""


def background():
    p = [rrect(0, 0, W, H, 0, WHITE)]
    # (latar dibiarkan bersih: corporate elegant)
    # tanda sudut (crop-mark style)
    for sx, sy, cx, cy in [(1, 1, 22, 22), (-1, 1, W - 22, 22),
                           (1, -1, 22, H - 22), (-1, -1, W - 22, H - 22)]:
        p.append(f'<path d="M {cx} {cy + sy * 34} L {cx} {cy} L {cx + sx * 34} {cy}" '
                 f'fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0.75"/>')
    return "".join(p)


def header():
    p = [f'<image x="{M}" y="80" width="252" height="47.3" '
         f'xlink:href="{logo_uri()}" preserveAspectRatio="xMinYMid meet"/>']
    p.append(text(W - M, 112, BRAND, 22, 800, NAVY, anchor="end", ls=7,
                  family=F_BODY))
    p.append(text(W - M, 142, BRAND_TAG, 17, 400, MUTED, anchor="end", ls=2.4,
                  family=F_BODY))
    p.append(text(W / 2 + 40, 124, HEAD_TAG, 16, 700, GOLD, anchor="middle",
                  ls=7, family=F_BODY))

    # pita tiga warna: biru - hijau - emas (struktur corporate)
    y, hh = 176, 9
    span = W - 2 * M
    w1, w2 = int(span * 0.46), int(span * 0.32)
    p.append(rrect(M, y, w1, hh, 0, BLUE))
    p.append(rrect(M + w1, y, w2, hh, 0, GREEN))
    p.append(rrect(M + w1 + w2, y, span - w1 - w2, hh, 0, "url(#goldGrad)"))
    p.append(line(M, y + hh + 6, W - M, y + hh + 6, HAIR, 1.4))
    return "".join(p)


# ----------------------------------------------------------------------------
# 2. SLOT FOTO + BLOK PROMO
# ----------------------------------------------------------------------------
def photo_panel():
    p = []
    if PHOTO_PLACEHOLDER:
        p.append(rrect(LX, TOP, LW, PHOTO_H, 0, BLUE_SOFT))
        p.append(rrect(LX + 18, TOP + 18, LW - 36, PHOTO_H - 36, 0, "none",
                       GOLD_BRIGHT, 2, ' stroke-dasharray="16 10"'))
        p.append(text(LX + LW / 2, TOP + PHOTO_H / 2 - 8, "FOTO PROMOSI", 40, 800,
                      GOLD, anchor="middle", ls=9, family=F_BODY))
        p.append(text(LX + LW / 2, TOP + PHOTO_H / 2 + 34, "rasio 16:9  \u00b7  "
                      "ganti assets/foto-promo.png", 19, 400, MUTED,
                      anchor="middle", family=F_BODY))
    else:
        p.append(f'<image x="{LX}" y="{TOP}" width="{LW}" height="{PHOTO_H}" '
                 f'xlink:href="{photo_uri()}" preserveAspectRatio="xMidYMid slice" '
                 f'clip-path="url(#photoClip)"/>')
        p.append(f'<rect x="{LX}" y="{TOP}" width="{LW}" height="150" '
                 f'fill="url(#photoFade)" clip-path="url(#photoClip)"/>')

    # bingkai tipis emas + kurung sudut
    p.append(rrect(LX, TOP, LW, PHOTO_H, 0, "none", GOLD, 2.4))
    for sx, sy, cx, cy in [(1, 1, LX + 16, TOP + 16), (-1, 1, LX + LW - 16, TOP + 16),
                           (1, -1, LX + 16, TOP + PHOTO_H - 16),
                           (-1, -1, LX + LW - 16, TOP + PHOTO_H - 16)]:
        p.append(f'<path d="M {cx} {cy + sy * 22} L {cx} {cy} L {cx + sx * 22} {cy}" '
                 f'fill="none" stroke="{GOLD_BRIGHT}" stroke-width="3" '
                 f'opacity="0.9"/>')

    # strip judul promo (blok navy)
    cy = TOP + PHOTO_H - 60
    p.append(f'<rect x="{LX}" y="{cy}" width="{LW}" height="60" fill="{NAVY}" '
             f'opacity="0.94"/>')
    p.append(rrect(LX, cy, LW, 3, 0, "url(#goldGrad)"))
    p.append(diamond(LX + 34, cy + 33, 7.5, GOLD_BRIGHT))
    p.append(text(LX + 56, cy + 40, CAPTION, 21, 800, WHITE, ls=6, family=F_BODY))
    p.append(text(LX + LW - 28, cy + 39, "1448 H  \u00b7  1960 Dal", 17, 400,
                  GOLD_SOFT, anchor="end", ls=1.6, family=F_BODY))
    return "".join(p)


def promo_panel():
    p = []
    # eyebrow dengan garis hijau
    p.append(rrect(LX, 686, 46, 4, 0, GREEN))
    p.append(text(LX + 64, 700, EYEBROW, 18, 800, GREEN, ls=7, family=F_BODY))
    p.append(text(LX + 64 + tw(EYEBROW, 18, 800, 7, family=F_BODY) + 16, 699,
                  "\u00b7  " + EYEBROW_SUB, 17, 400, MUTED, family=F_BODY))

    # judul serif
    p.append(text(LX - 2, 772, HEADLINE[0], 62, 400, NAVY, family=F_TITLE))
    p.append(text(LX - 2, 838, HEADLINE[1], 62, 400, NAVY, family=F_TITLE))
    p.append(line(LX, 872, LX + LW, 872, HAIR, 1.4))

    for i, ln in enumerate(BODY):
        p.append(text(LX, 912 + i * 32, ln, 22, 400, MUTED, family=F_BODY))

    # harga
    p.append(text(LX, 1002, PRICE_LABEL, 15, 800, MUTED, ls=6, family=F_BODY))
    p.append(text(LX - 2, 1066, PRICE_MAIN, 58, 700, GOLD, ls=1, family=F_BODY))
    pw = tw(PRICE_MAIN, 58, 700, 1, family=F_BODY)
    p.append(text(LX + pw + 10, 1064, PRICE_SUB, 21, 400, MUTED, family=F_BODY))

    # benefit 2 x 2 (gaya lembar spesifikasi)
    for i, b in enumerate(BENEFITS):
        col, row = i % 2, i // 2
        x = LX + col * 372
        y = 1130 + row * 76
        p.append(text(x, y, f"0{i + 1}", 15, 800, GOLD, ls=1, family=F_BODY))
        p.append(text(x + 34, y, b, 21, 400, NAVY, family=F_BODY))
        p.append(line(x, y + 22, x + 332, y + 22, HAIR, 1))

    p.append(line(LX, 1298, LX + LW, 1298, HAIR, 1.4))
    p.append(text(LX, 1326, FOOT, 17, 400, MUTED, ls=1, family=F_BODY))
    p.append(text(LX + LW, 1326, "PROGRAM SIMIRA", 15, 800, GREEN, anchor="end",
                  ls=5, family=F_BODY))
    return "".join(p)

    p.append(line(M, y + hh + 6, W - M, y + hh + 6, HAIR, 1.4))
    return "".join(p)




# ----------------------------------------------------------------------------
# 3. PANEL KALENDER (3 penanggalan)
# ----------------------------------------------------------------------------
def calendar_panel():
    p = [rrect(RX, TOP, RW, BOT - TOP, 0, WHITE, HAIR, 1.6)]

    # ---- blok judul navy
    p.append(f'<rect x="{RX}" y="{TOP}" width="{RW}" height="{HEAD_H}" '
             f'fill="url(#navyGrad)"/>')
    # watermark khatim halus di dalam blok navy
    p.append(star8(RX + RW - 250, TOP + HEAD_H / 2, 150, stroke="#FFFFFF",
                   sw=1.6, opacity=0.07))
    p.append(star8(RX + RW - 250, TOP + HEAD_H / 2, 96, stroke=GOLD_BRIGHT,
                   sw=1.2, opacity=0.10))
    p.append(rrect(RX, TOP + HEAD_H - 4, RW, 4, 0, "url(#goldGrad)"))
    p.append(text(RX + CARD_PAD - 4, TOP + 132, "JANUARI", 78, 400, WHITE, ls=6,
                  family=F_TITLE))
    jw = tw("JANUARI", 78, 400, 6, family=F_TITLE)
    p.append(line(RX + CARD_PAD + jw + 24, TOP + 72, RX + CARD_PAD + jw + 24,
                  TOP + 136, GOLD_BRIGHT, 2))
    p.append(text(RX + CARD_PAD + jw + 52, TOP + 128, "2027", 54, 800, GOLD_BRIGHT,
                  ls=5, family=F_BODY))

    # nomor bulan (kanan)
    p.append(text(RX + RW - CARD_PAD, TOP + 118, "01", 62, 800, WHITE,
                  anchor="end", ls=2, family=F_BODY))
    p.append(text(RX + RW - CARD_PAD, TOP + 154, "BULAN", 14, 700, GOLD_BRIGHT,
                  anchor="end", ls=5, family=F_BODY))

    # ---- baris tiga penanggalan
    my = 442
    p.append(text(IX, my, H_MONTH_LINE, 20, 700, GREEN, ls=5, family=F_BODY))
    hw = tw(H_MONTH_LINE, 20, 700, 5, family=F_BODY)
    p.append(diamond(IX + hw + 34, my - 7, 6.5, GOLD))
    p.append(text(IX + hw + 56, my, J_MONTH_LINE, 20, 700, GOLD, ls=5,
                  family=F_BODY))
    ar_m = (MONTHS_AR["Rajab"] + " \u2013 " + MONTHS_AR["Sya'ban"] +
            " \u0661\u0664\u0664\u0668 \u0647")
    frag, _ = ar_text(RX + RW - CARD_PAD, my + 2, ar_m, 26, GOLD, anchor="end")
    p.append(frag)

    # ---- header hari (dwibahasa)
    p.append(f'<rect x="{IX}" y="460" width="{IW}" height="70" fill="{BLUE_SOFT}"/>')
    for i, name in enumerate(WEEKDAYS):
        x = IX + i * COL_W
        fg = GOLD if i == 0 else (GREEN if i == 5 else NAVY)
        p.append(text(x + COL_W / 2, 494, name.upper(), 16, 700, fg,
                      anchor="middle", ls=3, family=F_BODY))
        frag, _ = ar_text(x + COL_W / 2, 528, WEEKDAYS_AR[i], 27, fg,
                          anchor="middle")
        p.append(frag)
        if i:
            p.append(line(x, 460, x, 530, WHITE, 2))

    # ---- zebra + tint khusus
    for r in range(6):
        if r % 2 == 1:
            p.append(rrect(IX, GRID_TOP + r * ROW_H, IW, ROW_H, 0, "#FBFCFD"))
    for c in CELLS:
        d = c["date"]
        tint = GREEN_SOFT if d in HOLIDAY_SET else (GOLD_SOFT if d in PUASA_SET else None)
        if tint:
            p.append(rrect(IX + c["col"] * COL_W, GRID_TOP + c["row"] * ROW_H,
                           COL_W, ROW_H, 0, tint))

    # ---- garis tabel
    for i in range(1, 7):
        p.append(line(IX + i * COL_W, GRID_TOP, IX + i * COL_W, GRID_BOT, HAIR, 1))
    for r in range(1, 6):
        p.append(line(IX, GRID_TOP + r * ROW_H, IX + IW, GRID_TOP + r * ROW_H,
                      HAIR, 1))
    p.append(line(IX, GRID_TOP, IX + IW, GRID_TOP, GOLD, 1.6))

    # ---- isi sel
    for c in CELLS:
        d = c["date"]
        cx = IX + COL_W * (c["col"] + 0.5)
        y = GRID_TOP + c["row"] * ROW_H
        if d in HOLIDAY_SET:
            num_c, h_c, j_c = GREEN, GREEN, "#5C8A78"
        elif d in PUASA_SET:
            num_c, h_c, j_c = GOLD, "#A8873F", GOLD
        elif not c["in_month"]:
            num_c, h_c, j_c = TAIL, TAIL, TAIL
        elif c["col"] == 0:
            num_c, h_c, j_c = GOLD, GREEN, GOLD
        elif c["col"] == 5:
            num_c, h_c, j_c = GREEN, GREEN, GOLD
        else:
            num_c, h_c, j_c = NAVY, GREEN, GOLD

        p.append(text(cx, y + 50, str(c["day"]), 38, 700, num_c, anchor="middle",
                      family=F_BODY))
        ar_s = f"{ar_digits(c['hijri_day'])} {MONTHS_AR[c['hijri_month']]}"
        hs = 28
        while ar_width(ar_s, hs) > COL_W - 14 and hs > 18:
            hs -= 1
        frag, _ = ar_text(cx, y + 86, ar_s, hs, h_c, anchor="middle")
        p.append(frag)
        j_txt = f"J {c['jav_day']} {c['jav_month']} \u00b7 {c['pasaran']}"
        p.append(text(cx, y + 108, j_txt,
                      fit(j_txt, 16, 400, COL_W - 12, family=F_BODY, min_size=11),
                      400, j_c, anchor="middle", ls=0.2, family=F_BODY))

        if d in HOLIDAY_SET:
            p.append(diamond(cx + COL_W / 2 - 16, y + 16, 6, GOLD))
        elif d in PUASA_SET:
            p.append(diamond(cx + COL_W / 2 - 16, y + 16, 5, GOLD))

    # ---- legenda
    lx = IX
    for badge, color in [("M", NAVY), ("H", GREEN), ("J", GOLD)]:
        p.append(rrect(lx, 1264, 18, 18, 2, color))
        p.append(text(lx + 9, 1278, badge, 12, 800, WHITE, anchor="middle",
                      family=F_BODY))
        lx += 26
    p.append(text(lx + 8, 1279,
                  "Masehi  \u00b7  Hijriah 1448 H (angka Arab)  \u00b7  "
                  "Jawa 1960 Dal + pasaran", 16, 400, MUTED, family=F_BODY))
    return "".join(p)


# ----------------------------------------------------------------------------
# 4. CATATAN & KAKI
# ----------------------------------------------------------------------------
def notes_and_footer():
    p = []
    ny, nh = 1352, 68
    cw = (W - 2 * M - 2 * 24) / 3
    for i, (color, day, label) in enumerate(HOLIDAYS):
        x = M + i * (cw + 24)
        p.append(rrect(x, ny, cw, nh, 0, WHITE, HAIR, 1.4))
        p.append(rrect(x, ny, cw, 4, 0, color))
        p.append(text(x + 26, ny + 31, day, 21, 800, color, family=F_BODY))
        p.append(text(x + 26, ny + 56, label,
                      fit(label, 18, 400, cw - 52, family=F_BODY, min_size=14),
                      400, MUTED, family=F_BODY))

    p.append(line(M, 1450, W - M, 1450, HAIR, 1.4))
    p.append(text(M, 1484, OJK, 16, 400, MUTED, family=F_BODY))
    p.append(text(W - M, 1484, CONTACT, 17, 700, NAVY, anchor="end",
                  family=F_BODY))
    return "".join(p)


# ----------------------------------------------------------------------------
# 5. ASSEMBLY
# ----------------------------------------------------------------------------
def build_svg():
    body = "".join([background(), header(), photo_panel(), promo_panel(),
                    calendar_panel(), notes_and_footer()])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs()}{body}</svg>')


def main():
    suffix = "-placeholder" if PHOTO_PLACEHOLDER else ""
    base = f"kalender-2027-biru-hijau-emas{suffix}"
    (DIST / f"{base}.svg").write_text(build_svg(), encoding="utf-8")
    meta = {
        "title": "Kalender Meja Januari 2027 - corporate elegant",
        "variant": "corporate-elegant",
        "size_cm": [21.3, 15.2],
        "size_px": [W, H],
        "px_per_mm": 10,
        "calendars": ["Masehi", "Hijriah 1448 H (Arab)", "Jawa 1960 Dal"],
        "palette": {"white": WHITE, "navy": NAVY, "blue": BLUE, "green": GREEN,
                    "gold": GOLD, "gold_bright": GOLD_BRIGHT, "hairline": HAIR},
        "fonts": {"display": "Marcellus", "body": "Lato",
                  "arabic": "Noto Naskh Arabic"},
        "cells": CELLS,
    }
    (DIST / f"{base}-data.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SVG + JSON written:", base)


if __name__ == "__main__":
    main()
