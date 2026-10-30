#!/usr/bin/env python3
"""
Kalender Meja Januari 2027 - landscape 21,3 x 15,2 cm (BPRS Mitra Mentari Sejahtera).
Tiga sistem penanggalan per sel: MASEHI + HIJRIAH (angka & bulan Arab) + JAWA.

Kanvas 2130 x 1520 px @ 10 px/mm -> 21,3 x 15,2 cm (254 dpi).
Palet: biru - hijau - emas di atas kertas krem. Ornamen geometris Islam
(khatim), medali bulan, ribbon promo, bingkai foto ganda.

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
W, H = 2130, 1520                     # 10 px = 1 mm
M = 40
FRAME_OUT, FRAME_IN = 22, 28

# Kolom kiri (foto + promo) / kanan (kalender)
LX, LW = 40, 750
RX, RW = 820, 1270
TOP, BOT = 150, 1310
NOTES_Y, NOTES_H = 1330, 60
FOOT_RULE, FOOT_Y = 1412, 1442

# Palet biru - hijau - emas
PAPER = "#FAF7F0"
PANEL = "#FFFFFF"
NAVY = "#0B2E4F"
BLUE = "#12557F"
BLUE_SOFT = "#E8F1F8"
GREEN = "#0D6B4F"
GREEN_SOFT = "#E6F2EC"
GOLD = "#B58A2B"
GOLD_BRIGHT = "#D4AF37"
GOLD_SOFT = "#FBF3DE"
LINE = "#E6DFCE"
MUTED = "#7E8B99"
TAIL_TXT = "#B9C3CE"
TAIL_SUB = "#CBD4DD"

F_TITLE = "Marcellus"
F_BODY = "Lato"

PHOTO_FILE = "foto-promo.png"
PHOTO_PLACEHOLDER = False             # True -> slot foto kosong + label

# Konten
BRAND = "BANK MITRA SYARIAH"
BRAND_TAG = "Pilihan Amanah Keluarga"
HEAD_TAG = "KALENDER MEJA  \u00b7  2027"
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
RIBBON = "PROGRAM UMROH 2027"
H_MONTH_LINE = "RAJAB \u2013 SYA'BAN 1448 H"
J_MONTH_LINE = "REJEB \u2013 RUWAH 1960 DAL"
LEGEND = ("Angka besar = Masehi   \u00b7   H = Hijriah   \u00b7   "
          "J = Jawa (bulan + pasaran)")
OJK = ("PT BPRS Mitra Mentari Sejahtera  \u00b7  Berizin & Diawasi oleh OJK  "
       "\u00b7  Peserta Penjaminan LPS")
CONTACT = "0813-1349-9673   \u00b7   mitrasyariahbank.co.id   \u00b7   @mitrasyariahbank"

HOLIDAYS = [
    (BLUE, "1 Januari", "Tahun Baru 2027 Masehi"),
    (GREEN, "6 Januari", "Isra' Mi'raj Nabi Muhammad SAW 1448 H"),
    (GOLD, "22\u201324 Januari", "Puasa Sunnah Ayyamul Bidh (13\u201315 Sya'ban 1448 H)"),
]
HOLIDAY_SET = {"2027-01-01", "2027-01-06"}
PUASA_SET = {"2027-01-22", "2027-01-23", "2027-01-24"}

# ----------------------------------------------------------------------------
# KALENDER JAWA (Sultan Agung): bulan Jawa + nama tahun + pasaran
# ----------------------------------------------------------------------------
JAV_MONTHS = {
    "Muharram": "Sura", "Safar": "Sapar", "Rabiul Awal": "Mulud",
    "Rabiul Akhir": "Bakda Mulud", "Jumadil Awal": "Jumadilawal",
    "Jumadil Akhir": "Jumadilakir", "Rajab": "Rejeb", "Sya'ban": "Ruwah",
    "Ramadhan": "Pasa", "Syawal": "Sawal", "Dzulqadah": "Sela",
    "Dzulhijjah": "Besar",
}
# 1960 = Dal (mengikuti file sumber). Urutan windu 8 tahun.
JAV_YEARS = ["Dal", "Be", "Wawu", "Jimakir", "Alip", "Ehe", "Jimawal", "Je"]


def jav_year_name(year):
    return JAV_YEARS[year % 8]


for c in CELLS:
    c["jav_day"] = c["hijri_day"]           # penomoran sama dengan Hijriah
    c["jav_month"] = JAV_MONTHS[c["hijri_month"]]
    c["jav_year"] = c["hijri_year"] + 512   # 1448 H = 1960 Jawa
    c["jav_year_name"] = jav_year_name(c["jav_year"])


def fit(s, size, weight, max_w, family=F_BODY, min_size=10.0):
    """Perkecil ukuran font sampai teks muat di lebar tertentu."""
    while tw(s, size, weight, family=family) > max_w and size > min_size:
        size -= 0.5
    return size


def logo_uri():
    data = base64.b64encode((ASSETS / "logo-brand.png").read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def photo_uri():
    data = base64.b64encode((ASSETS / PHOTO_FILE).read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def defs():
    return f"""<defs>
  <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{NAVY}"/><stop offset="0.55" stop-color="{BLUE}"/>
    <stop offset="1" stop-color="{GREEN}"/>
  </linearGradient>
  <linearGradient id="blueGrad" x1="0" y1="0" x2="0.4" y2="1">
    <stop offset="0" stop-color="#1D7396"/><stop offset="0.55" stop-color="{BLUE}"/>
    <stop offset="1" stop-color="{NAVY}"/>
  </linearGradient>
  <linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#16906B"/><stop offset="1" stop-color="{GREEN}"/>
  </linearGradient>
  <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#E3C56B"/><stop offset="0.5" stop-color="{GOLD_BRIGHT}"/>
    <stop offset="1" stop-color="#A97F22"/>
  </linearGradient>
  <linearGradient id="photoFade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{NAVY}" stop-opacity="0.62"/>
    <stop offset="1" stop-color="{NAVY}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="goldRule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{GOLD}" stop-opacity="1"/>
    <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="khatim" width="120" height="120" patternUnits="userSpaceOnUse">
    <g fill="none" stroke="{GOLD}" stroke-width="1">
      {star8(60, 60, 30, stroke=GOLD, sw=1)}
      {star8(0, 0, 24, stroke=GOLD, sw=0.8)}
      {star8(120, 0, 24, stroke=GOLD, sw=0.8)}
      {star8(0, 120, 24, stroke=GOLD, sw=0.8)}
      {star8(120, 120, 24, stroke=GOLD, sw=0.8)}
    </g>
  </pattern>
  <filter id="soft" x="-25%" y="-25%" width="150%" height="160%">
    <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="{NAVY}"
                  flood-opacity="0.10"/>
  </filter>
  <clipPath id="photoClip">
    <rect x="{LX + 14}" y="{TOP + 14}" width="{LW - 28}" height="426" rx="6"/>
  </clipPath>
</defs>"""


# ----------------------------------------------------------------------------
# 1. LATAR, BINGKAI, KEPALA
# ----------------------------------------------------------------------------
def background():
    p = [rrect(0, 0, W, H, 0, PAPER)]
    p.append(f'<g opacity="0.055">{rrect(0, 0, W, H, 0, "url(#khatim)")}</g>')
    # pita gradasi biru-hijau di tepi atas
    p.append(rrect(0, 0, W, 10, 0, "url(#bgGrad)"))
    p.append(line(0, 10, W, 10, GOLD_BRIGHT, 1.6))
    # bingkai ganda
    p.append(rrect(FRAME_OUT, FRAME_OUT, W - 2 * FRAME_OUT, H - 2 * FRAME_OUT, 0,
                   "none", GOLD, 1.6))
    p.append(rrect(FRAME_IN, FRAME_IN, W - 2 * FRAME_IN, H - 2 * FRAME_IN, 0,
                   "none", GOLD_BRIGHT, 0.8))
    # ornamen besar: khatim biru & hijau sebagai hiasan latar
    p.append(star8(120, 1330, 250, stroke=BLUE, sw=2.5, opacity=0.055))
    p.append(star8(2020, 260, 230, stroke=GREEN, sw=2.5, opacity=0.055))
    p.append(star8(120, 1330, 165, stroke=GREEN, sw=1.6, opacity=0.05))
    p.append(star8(2020, 260, 150, stroke=BLUE, sw=1.6, opacity=0.045))
    for cx, cy in [(FRAME_IN + 22, FRAME_IN + 22), (W - FRAME_IN - 22, FRAME_IN + 22),
                   (FRAME_IN + 22, H - FRAME_IN - 22),
                   (W - FRAME_IN - 22, H - FRAME_IN - 22)]:
        p.append(star8(cx, cy, 10, stroke=GOLD, sw=1.1, opacity=0.8))
    return "".join(p)


def header():
    p = [f'<image x="{M}" y="62" width="267" height="50" '
         f'xlink:href="{logo_uri()}" preserveAspectRatio="xMinYMid meet"/>']
    p.append(text(W - M, 66, BRAND, 22, 800, NAVY, anchor="end", ls=7,
                  family=F_BODY))
    p.append(text(W - M, 96, BRAND_TAG, 18, 400, MUTED, anchor="end", ls=3,
                  family=F_BODY))
    p.append(text(W / 2, 108, HEAD_TAG, 17, 700, GOLD, anchor="middle", ls=7,
                  family=F_BODY))
    p.append(line(M, 126, W - M, 126, "url(#goldRule)", 1.6))
    p.append(rrect(W / 2 - 26, 120, 52, 12, 3, PAPER))
    p.append(diamond(W / 2, 126, 8, GOLD))
    return "".join(p)


# ----------------------------------------------------------------------------
# 2. SLOT FOTO PROMOSI
# ----------------------------------------------------------------------------
def photo_panel():
    ph = 454
    p = [rrect(LX, TOP, LW, ph, 10, PANEL, "url(#bgGrad)", 7,
               ' filter="url(#soft)"')]
    p.append(rrect(LX + 9, TOP + 9, LW - 18, ph - 18, 7, "none", GOLD, 2))
    p.append(rrect(LX + 13, TOP + 13, LW - 26, ph - 26, 6, "none", GOLD_BRIGHT, 0.8))

    if PHOTO_PLACEHOLDER:
        p.append(rrect(LX + 14, TOP + 14, LW - 28, ph - 28, 6, GOLD_SOFT,
                       GOLD_BRIGHT, 2, ' stroke-dasharray="14 10"'))
        p.append(text(LX + LW / 2, TOP + ph / 2 - 6, "FOTO PROMOSI", 34, 800, GOLD,
                      anchor="middle", ls=8, family=F_BODY))
        p.append(text(LX + LW / 2, TOP + ph / 2 + 34, "rasio 3:2 \u00b7 ganti berkas "
                      "assets/foto-promo.png", 18, 400, MUTED, anchor="middle",
                      family=F_BODY))
    else:
        p.append(f'<image x="{LX + 14}" y="{TOP + 14}" width="{LW - 28}" height="426" '
                 f'xlink:href="{photo_uri()}" preserveAspectRatio="xMidYMid slice" '
                 f'clip-path="url(#photoClip)"/>')
        # lapisan gradasi tipis agar ribbon terbaca
        p.append(f'<rect x="{LX + 14}" y="{TOP + 14}" width="{LW - 28}" height="170" '
                 f'fill="url(#photoFade)" clip-path="url(#photoClip)"/>')

    # kurung sudut emas
    for sx, sy, cx, cy in [(1, 1, LX + 26, TOP + 26), (-1, 1, LX + LW - 26, TOP + 26),
                           (1, -1, LX + 26, TOP + ph - 26),
                           (-1, -1, LX + LW - 26, TOP + ph - 26)]:
        p.append(f'<path d="M {cx} {cy + sy * 26} L {cx} {cy} L {cx + sx * 26} {cy}" '
                 f'fill="none" stroke="{GOLD}" stroke-width="3" opacity="0.85"/>')

    # ribbon promo
    rl = tw(RIBBON, 20, 800, 4.5, family=F_BODY) + 64
    rx, ry = LX + 74, TOP + 34
    p.append(rrect(rx, ry, rl, 52, 26, "url(#bgGrad)", GOLD_BRIGHT, 1.6))
    p.append(diamond(rx + 26, ry + 26, 6, GOLD_BRIGHT))
    p.append(text(rx + 42, ry + 34, RIBBON, 20, 800, "#FFFFFF", ls=4.5,
                  family=F_BODY))
    return "".join(p)


# ----------------------------------------------------------------------------
# 3. KARTU PROMO
# ----------------------------------------------------------------------------
def promo_panel():
    cy = 624
    p = [rrect(LX, cy, LW, BOT - cy, 10, PANEL, LINE, 1.4,
               ' filter="url(#soft)"')]
    p.append(rrect(LX, cy, LW, 8, 4, "url(#bgGrad)"))
    p.append(rrect(LX, cy + 10, 10, BOT - cy - 10, 0, "url(#greenGrad)"))
    p.append(star8(LX + 520, 760, 120, stroke=GREEN, sw=1.4, opacity=0.07))
    x = LX + 48

    p.append(text(x, 692, KICKER, 22, 800, GREEN, ls=7, family=F_BODY))
    p.append(text(x, 722, KICKER_SUB, 20, 400, MUTED, ls=1.6, family=F_BODY))

    p.append(text(x - 2, 790, HEADLINE[0], 64, 400, NAVY, family=F_TITLE))
    p.append(text(x - 2, 856, HEADLINE[1], 64, 400, NAVY, family=F_TITLE))

    p.append(line(x, 888, x + 74, 888, GOLD, 2.4))
    p.append(diamond(x + 92, 888, 7.5, GOLD))
    p.append(line(x + 110, 888, x + 184, 888, GOLD, 2.4))

    for i, ln in enumerate(BODY):
        p.append(text(x, 928 + i * 34, ln, 24, 400, MUTED, family=F_BODY))

    p.append(text(x, 1008, PRICE_LABEL, 18, 800, MUTED, ls=5, family=F_BODY))
    p.append(text(x - 2, 1072, PRICE_MAIN, 62, 700, GOLD, ls=1, family=F_BODY))
    pw = tw(PRICE_MAIN, 62, 700, 1, family=F_BODY)
    p.append(text(x + pw + 10, 1070, PRICE_SUB, 22, 400, MUTED, family=F_BODY))

    p.append(line(x, 1102, LX + LW - 48, 1102, LINE, 1.2))

    by = 1140
    for b in BENEFITS:
        p.append(diamond(x + 7, by - 8, 7, GOLD))
        p.append(text(x + 30, by, b, 24, 400, NAVY, family=F_BODY))
        by += 34

    p.append(line(x, 1256, LX + LW - 48, 1256, LINE, 1))
    p.append(text(x, 1288, FOOT, 20, 400, MUTED, ls=1, family=F_BODY))
    p.append(text(LX + LW - 48, 1288, "1448 H  \u00b7  1960", 20, 700, GOLD,
                  anchor="end", ls=2, family=F_BODY))
    return "".join(p)




# ----------------------------------------------------------------------------
# 4. PANEL KALENDER (3 penanggalan)
# ----------------------------------------------------------------------------
IX = RX + 44
IW = RW - 88                      # 1182
GRID_TOP = 468
GRID_BOT = 1240
ROW_H = (GRID_BOT - GRID_TOP) / 6  # 132
COL_W = IW / 7                     # 168.86


def calendar_panel():
    p = [rrect(RX, TOP, RW, BOT - TOP, 10, PANEL, LINE, 1.4,
               ' filter="url(#soft)"')]
    p.append(rrect(RX, TOP, RW, 8, 4, "url(#bgGrad)"))
    p.append(star8(IX + 470, 300, 150, stroke=GOLD, sw=1.4, opacity=0.075))

    # ---- judul
    p.append(text(IX - 4, 302, "JANUARI", 76, 400, NAVY, ls=6, family=F_TITLE))
    jw = tw("JANUARI", 76, 400, 6, family=F_TITLE)
    bw = tw("2027", 52, 800, 6, family=F_BODY) + 56
    bx, by = IX + jw + 42, 240
    p.append(f'<g transform="rotate(-2 {bx + bw / 2:.1f} {by + 39:.1f})">')
    p.append(rrect(bx, by, bw, 78, 12, "url(#goldGrad)", "#FFFFFF", 2))
    p.append(text(bx + bw / 2, by + 57, "2027", 52, 800, NAVY, anchor="middle",
                  ls=6, family=F_BODY))
    p.append("</g>")

    # ---- medali nomor bulan
    mgx, mgy, mgr = 1996, 252, 46
    p.append(f'<circle cx="{mgx}" cy="{mgy}" r="{mgr}" fill="url(#blueGrad)" '
             f'stroke="{GOLD}" stroke-width="2.8"/>')
    p.append(f'<circle cx="{mgx}" cy="{mgy}" r="{mgr - 8}" fill="none" '
             f'stroke="{GOLD_BRIGHT}" stroke-width="1.2"/>')
    p.append(text(mgx, mgy + 14, "01", 40, 800, "#FFFFFF", anchor="middle", ls=2,
                  family=F_BODY))
    p.append(text(mgx, mgy + 78, "BULAN", 15, 700, GOLD, anchor="middle", ls=4,
                  family=F_BODY))

    # ---- baris tiga penanggalan
    p.append(text(IX, 350, H_MONTH_LINE, 20, 700, GREEN, ls=4.5, family=F_BODY))
    hw = tw(H_MONTH_LINE, 20, 700, 4.5, family=F_BODY)
    p.append(diamond(IX + hw + 34, 344, 7, GOLD))
    p.append(text(IX + hw + 58, 350, J_MONTH_LINE, 20, 700, GOLD, ls=4.5,
                  family=F_BODY))
    ar_month, _ = ar_text(1928, 352,
                          f"{MONTHS_AR['Rajab']} \u2013 {MONTHS_AR[chr(83)+chr(121)+chr(97)+chr(39)+chr(98)+chr(97)+chr(110)]} \u0661\u0664\u0664\u0668 \u0647",
                          26, GOLD, anchor="end")
    p.append(ar_month)

    # ---- header hari
    for i, name in enumerate(WEEKDAYS):
        x = IX + i * COL_W
        if i == 0:
            bg, fg = GOLD_SOFT, GOLD
        elif i == 5:
            bg, fg = GREEN_SOFT, GREEN
        else:
            bg, fg = BLUE_SOFT, BLUE
        p.append(rrect(x + 5, 372, COL_W - 10, 84, 10, bg))
        p.append(text(x + COL_W / 2, 404, name.upper(), 19, 700, fg,
                      anchor="middle", ls=3, family=F_BODY))
        ar_day, _ = ar_text(x + COL_W / 2, 444, WEEKDAYS_AR[i], 32, fg,
                            anchor="middle")
        p.append(ar_day)

    # ---- zebra baris
    for r in range(6):
        if r % 2 == 1:
            p.append(rrect(IX, GRID_TOP + r * ROW_H, IW, ROW_H, 0, "#FCFAF3",
                           extra=' opacity="0.9"'))

    # ---- tint sel libur / puasa
    for c in CELLS:
        d = c["date"]
        tint = None
        if d in HOLIDAY_SET:
            tint = GREEN_SOFT
        elif d in PUASA_SET:
            tint = GOLD_SOFT
        if tint:
            x = IX + c["col"] * COL_W
            y = GRID_TOP + c["row"] * ROW_H
            p.append(rrect(x + 1, y + 1, COL_W - 2, ROW_H - 2, 0, tint))

    # ---- garis tabel
    for i in range(1, 7):
        x = IX + i * COL_W
        p.append(line(x, GRID_TOP, x, GRID_BOT, LINE, 1))
    for r in range(1, 6):
        y = GRID_TOP + r * ROW_H
        p.append(line(IX, y, IX + IW, y, LINE, 1))
    p.append(rrect(IX, GRID_TOP, IW, GRID_BOT - GRID_TOP, 0, "none", GOLD, 1.4))

    # ---- isi sel: Masehi + Hijriah + Jawa
    for c in CELLS:
        d = c["date"]
        cx = IX + COL_W * (c["col"] + 0.5)
        y = GRID_TOP + c["row"] * ROW_H
        if d in HOLIDAY_SET:
            num_c, h_c, j_c = GREEN, GREEN, "#5C8A78"
        elif d in PUASA_SET:
            num_c, h_c, j_c = GOLD, "#A8873F", GOLD
        elif not c["in_month"]:
            num_c, h_c, j_c = TAIL_TXT, TAIL_SUB, TAIL_SUB
        elif c["col"] == 0:
            num_c, h_c, j_c = GOLD, GREEN, GOLD
        elif c["col"] == 5:
            num_c, h_c, j_c = GREEN, GREEN, GOLD
        else:
            num_c, h_c, j_c = NAVY, GREEN, GOLD

        p.append(text(cx, y + 58, str(c["day"]), 40, 700, num_c, anchor="middle",
                      family=F_BODY))
        j_txt = f"J  {c['jav_day']} {c['jav_month']} \u00b7 {c['pasaran']}"
        j_fs = fit(j_txt, 17, 400, COL_W - 14, family=F_BODY, min_size=12)
        ar_s = f"{ar_digits(c['hijri_day'])} {MONTHS_AR[c['hijri_month']]}"
        h_size = 31
        while ar_width(ar_s, h_size) > COL_W - 16 and h_size > 20:
            h_size -= 1
        h_frag, _ = ar_text(cx, y + 94, ar_s, h_size, h_c, anchor="middle")
        p.append(h_frag)
        p.append(text(cx, y + 118, j_txt, j_fs, 400, j_c, anchor="middle", ls=0.2,
                      family=F_BODY))

        if d in HOLIDAY_SET:
            p.append(star8(cx + COL_W / 2 - 26, y + 22, 10, stroke=GOLD,
                           sw=1.4, opacity=0.9))
        elif d in PUASA_SET:
            p.append(diamond(cx + COL_W / 2 - 26, y + 22, 7, GOLD))

    # ---- legenda
    lx = IX
    for badge, color in [("M", NAVY), ("H", GREEN), ("J", GOLD)]:
        p.append(rrect(lx, 1252, 20, 20, 4, color))
        p.append(text(lx + 10, 1267, badge, 13, 800, "#FFFFFF", anchor="middle",
                      family=F_BODY))
        lx += 30
    p.append(text(lx + 6, 1268, "Hijriah 1448 H (angka Arab)  \u00b7  Jawa 1960 "
                  "Dal  \u00b7  pasaran Jawa", 17, 400, MUTED, family=F_BODY))


    return "".join(p)

# ----------------------------------------------------------------------------
# 5. CATATAN & KAKI
# ----------------------------------------------------------------------------
def notes_and_footer():
    p = []
    cw = (W - 2 * M - 2 * 20) / 3
    for i, (color, day, label) in enumerate(HOLIDAYS):
        x = M + i * (cw + 20)
        p.append(rrect(x, NOTES_Y, cw, NOTES_H, 8, PANEL, LINE, 1.2,
                       ' filter="url(#soft)"'))
        p.append(rrect(x, NOTES_Y, 10, NOTES_H, 4, color))
        p.append(star8(x + 48, NOTES_Y + NOTES_H / 2, 17, fill=color))
        p.append(star8(x + 48, NOTES_Y + NOTES_H / 2, 10, fill="#FFFFFF"))
        p.append(text(x + 78, NOTES_Y + 26, day, 21, 800, color, family=F_BODY))
        p.append(text(x + 78, NOTES_Y + 48, label, fit(label, 18, 400, cw - 46, family=F_BODY, min_size=14), 400, MUTED, family=F_BODY))

    p.append(line(M, FOOT_RULE, W - M, FOOT_RULE, "url(#goldRule)", 1.6))
    p.append(rrect(W / 2 - 26, FOOT_RULE - 6, 52, 12, 3, PAPER))
    p.append(diamond(W / 2, FOOT_RULE, 8, GOLD))
    p.append(text(M, FOOT_Y + 4, OJK, 17, 400, MUTED, family=F_BODY))
    p.append(text(W - M, FOOT_Y + 6, CONTACT, 18, 700, NAVY, anchor="end",
                  family=F_BODY))
    return "".join(p)


# ----------------------------------------------------------------------------
# 6. ASSEMBLY
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
    svg = build_svg()
    (DIST / f"{base}.svg").write_text(svg, encoding="utf-8")

    meta = {
        "title": "Kalender Meja Januari 2027 - 3 penanggalan",
        "variant": "biru-hijau-emas",
        "size_cm": [21.3, 15.2],
        "size_px": [W, H],
        "px_per_mm": 10,
        "dpi_effective": 254,
        "calendars": ["Masehi", "Hijriah 1448 H", "Jawa 1960 Dal (pasaran)"],
        "palette": {"navy": NAVY, "blue": BLUE, "green": GREEN, "gold": GOLD,
                    "gold_bright": GOLD_BRIGHT, "paper": PAPER},
        "fonts": {"display": "Marcellus", "body": "Lato"},
        "cells": CELLS,
    }
    (DIST / f"{base}-data.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SVG + JSON written:", base)


if __name__ == "__main__":
    main()
