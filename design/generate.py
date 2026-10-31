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
import math

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
# 0. ORNAMEN (arabesque geometris: busur, khatim, permata, daun)
# ----------------------------------------------------------------------------
def arc(cx, cy, r, sx, sy, color, sw=1.4, opacity=0.9):
    """Busur seperempat lingkaran yang menghadap titik sudut (cx, cy)."""
    sweep = 0 if sx * sy > 0 else 1
    return (f'<path d="M {cx + sx * r:.2f} {cy:.2f} A {r} {r} 0 0 {sweep} '
            f'{cx:.2f} {cy + sy * r:.2f}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" opacity="{opacity}"/>')


def leaf(x, y, scale, angle, color, opacity=0.45):
    """Daun kecil (lens) untuk hiasan arabesque."""
    return (f'<g transform="translate({x:.2f} {y:.2f}) rotate({angle}) '
            f'scale({scale})">'
            f'<path d="M0 0 C 5 -4.6 13 -4.6 18 0 C 13 4.6 5 4.6 0 0 Z" '
            f'fill="{color}" opacity="{opacity}"/></g>')


def arabesque_corner(cx, cy, size, sx, sy, color=GOLD, sw=1.4, opacity=0.9,
                     leaves=True):
    """Ornamen sudut: dua busur sejajar + khatim + curl + daun."""
    r = size
    off, curl = r * 0.19, r * 0.085
    p = [arc(cx, cy, r, sx, sy, color, sw, opacity),
         arc(cx, cy, r - off, sx, sy, color, sw * 0.7, opacity * 0.65)]
    # curl di ujung busur
    p.append(f'<circle cx="{cx + sx * r:.2f}" cy="{cy:.2f}" r="{curl:.2f}" '
             f'fill="none" stroke="{color}" stroke-width="{sw * 0.8}" '
             f'opacity="{opacity}"/>')
    p.append(f'<circle cx="{cx:.2f}" cy="{cy + sy * r:.2f}" r="{curl:.2f}" '
             f'fill="none" stroke="{color}" stroke-width="{sw * 0.8}" '
             f'opacity="{opacity}"/>')
    # khatim kecil di titik terdekat sudut
    k = r - r * 0.7071
    p.append(star8(cx + sx * k, cy + sy * k, max(4.0, size * 0.15), stroke=color,
                   sw=sw * 0.85, opacity=opacity))
    if leaves and size > 44:
        ccx, ccy = cx + sx * r, cy + sy * r
        for deg in (196, 232, 268):
            th = math.radians(deg)
            px, py = ccx + r * math.cos(th), ccy + r * math.sin(th)
            if (px - cx) * sx < r * 0.2 or (py - cy) * sy < r * 0.2:
                continue
            p.append(leaf(px, py, size / 60, deg + 90, color, 0.4))
    return "".join(p)


def flourish(cx, y, half, color=GOLD, sw=1.3):
    """Pembatas horizontal: garis + dua curl + permata tengah."""
    p = [line(cx - half, y, cx - 30, y, color, sw, opacity=0.75),
         line(cx + 30, y, cx + half, y, color, sw, opacity=0.75),
         diamond(cx, y, 8, color)]
    for s in (-1, 1):
        p.append(f'<path d="M {cx + s * 30:.2f} {y:.2f} c {s * 9} 0 {s * 11} -7 '
                 f'{s * 4} -10 c {-s * 6} -2 {-s * 8} 4 {-s * 3} 6" fill="none" '
                 f'stroke="{color}" stroke-width="{sw}" opacity="0.8"/>')
    return "".join(p)


def pattern_band(x, y, w, color, step=36, r=7.5, opacity=0.45, sw=1.1):
    """Deret khatim kecil sebagai pita hias."""
    n = int(w // step)
    return "".join(star8(x + i * step, y, r, stroke=color, sw=sw, opacity=opacity)
                   for i in range(n + 1))


def vertical_ornament(x, y1, y2, color=GOLD):
    """Pembatas vertikal antar kolom: garis + permata + medali khatim."""
    p = [line(x, y1 + 12, x, y2 - 12, color, 1.1, opacity=0.5)]
    for yy in (y1, y2):
        p.append(diamond(x, yy, 7, color))
        p.append(diamond(x, yy + (14 if yy == y1 else -14), 3.5, color))
    mid = (y1 + y2) / 2
    p.append(star8(x, mid, 15, stroke=color, sw=1.1, opacity=0.85))
    p.append(star8(x, mid, 7, fill=color, opacity=0.5))
    for f in (0.25, 0.75):
        p.append(star8(x, y1 + (y2 - y1) * f, 10, stroke=color, sw=0.9,
                       opacity=0.6))
    return "".join(p)


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
    # bingkai ganda tipis (elegant, bukan kaku)
    p.append(rrect(14, 14, W - 28, H - 28, 0, "none", GOLD, 1.6,
                   ' opacity="0.85"'))
    p.append(rrect(21, 21, W - 42, H - 42, 0, "none", BLUE, 0.8,
                   ' opacity="0.4"'))
    # arabesque di 4 sudut bingkai
    for sx, sy, cx, cy in [(1, 1, 14, 14), (-1, 1, W - 14, 14),
                           (1, -1, 14, H - 14), (-1, -1, W - 14, H - 14)]:
        p.append(arabesque_corner(cx, cy, 48, sx, sy, GOLD, 1.5, 0.8))
    # permata di tengah tiap sisi bingkai
    for gx, gy in [(W / 2, 14), (W / 2, H - 14), (14, H / 2), (W - 14, H / 2)]:
        p.append(diamond(gx, gy, 9, GOLD))
        p.append(diamond(gx, gy, 4, WHITE))
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
    p.append(diamond(M - 12, y + hh / 2, 8, GOLD))
    p.append(diamond(W - M + 12, y + hh / 2, 8, GOLD))
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

    # arabesque kecil di 4 sudut dalam foto
    for sx, sy, cx, cy in [(1, 1, LX, TOP), (-1, 1, LX + LW, TOP),
                           (1, -1, LX, TOP + PHOTO_H),
                           (-1, -1, LX + LW, TOP + PHOTO_H)]:
        p.append(arabesque_corner(cx, cy, 46, sx, sy, GOLD_BRIGHT, 1.4, 0.62))
    # medali khatim di tengah sisi atas (memecah garis bingkai)
    mx, my = LX + LW / 2, TOP
    p.append(f'<circle cx="{mx}" cy="{my}" r="26" fill="{WHITE}" '
             f'stroke="{GOLD}" stroke-width="1.6"/>')
    p.append(star8(mx, my, 17, stroke=GOLD, sw=1.3, opacity=0.95))
    p.append(diamond(mx, my, 5.5, GOLD))

    # strip judul promo (blok navy)
    cy = TOP + PHOTO_H - 60
    p.append(f'<rect x="{LX}" y="{cy}" width="{LW}" height="60" fill="{NAVY}" '
             f'opacity="0.94"/>')
    p.append(rrect(LX, cy, LW, 3, 0, "url(#goldGrad)"))
    p.append(diamond(LX + 34, cy + 33, 7.5, GOLD_BRIGHT))
    p.append(text(LX + 56, cy + 40, CAPTION, 21, 800, WHITE, ls=6, family=F_BODY))
    p.append(text(LX + LW - 28, cy + 39, "1448 H  \u00b7  1960 Dal", 17, 400,
                  GOLD_SOFT, anchor="end", ls=1.6, family=F_BODY))
    p.append(pattern_band(LX + 20, cy + 50, LW - 40, GOLD_BRIGHT, 46, 4.6, 0.3, 0.8))
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
    # pita khatim halus di dasar blok navy
    p.append(pattern_band(RX + 44, TOP + HEAD_H - 26, RW - 88, GOLD_BRIGHT,
                          40, 6.5, 0.22, 1.0))
    # arabesque emas di dua sudut atas blok navy
    for sx, cx in [(1, RX), (-1, RX + RW)]:
        p.append(arabesque_corner(cx, TOP, 42, sx, 1, GOLD_BRIGHT, 1.3, 0.42))
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
    p.append(line(IX, GRID_BOT, IX + IW, GRID_BOT, GOLD, 1.6))
    # arabesque di sudut bawah kartu
    for sx, cx in [(1, RX), (-1, RX + RW)]:
        p.append(arabesque_corner(cx, BOT, 44, sx, -1, GOLD, 1.35, 0.6))

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
        p.append(diamond(x + 13, ny + 17, 5, color))
        p.append(diamond(x + cw - 13, ny + 17, 5, color))
        p.append(text(x + 26, ny + 31, day, 21, 800, color, family=F_BODY))
        p.append(text(x + 26, ny + 56, label,
                      fit(label, 18, 400, cw - 52, family=F_BODY, min_size=14),
                      400, MUTED, family=F_BODY))

    p.append(line(M, 1450, W / 2 - 150, 1450, HAIR, 1.4))
    p.append(line(W / 2 + 150, 1450, W - M, 1450, HAIR, 1.4))
    p.append(flourish(W / 2, 1450, 140, GOLD, 1.3))
    p.append(text(M, 1484, OJK, 16, 400, MUTED, family=F_BODY))
    p.append(text(W - M, 1484, CONTACT, 17, 700, NAVY, anchor="end",
                  family=F_BODY))
    return "".join(p)


# ----------------------------------------------------------------------------
# 5. ASSEMBLY
# ----------------------------------------------------------------------------
def build_svg():
    gutter = vertical_ornament((LX + LW + RX) / 2, TOP, BOT)
    body = "".join([background(), header(), photo_panel(), promo_panel(),
                    calendar_panel(), notes_and_footer(), gutter])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs()}{body}</svg>')


def main():
    suffix = "-placeholder" if PHOTO_PLACEHOLDER else ""
    base = f"kalender-2027-biru-hijau-emas{suffix}"
    (DIST / f"{base}.svg").write_text(build_svg(), encoding="utf-8")
    (DIST / f"{base}-belakang.svg").write_text(build_back(), encoding="utf-8")
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





# ----------------------------------------------------------------------------
# 6. HALAMAN BELAKANG — PROFIL & PRODUK
# ----------------------------------------------------------------------------
# Draf konten: mohon dikoreksi/diresmikan oleh pihak bank sebelum cetak.
PROFILE_PARAS = [
    ("BPRS Mitra Mentari Sejahtera adalah lembaga keuangan mikro syariah yang "
     "berizin dan diawasi oleh OJK, hadir melayani masyarakat Bengkulu dengan "
     "prinsip syariah yang amanah dan transparan."),
    ("Kami tumbuh bersama nasabah: membuka akses permodalan usaha, mendorong "
     "semangat menabung, dan menemani langkah spiritual umat melalui layanan "
     "perjalanan ibadah."),
    ("Sebagai bagian dari ekosistem Bank Mitra Syariah, kami berkomitmen "
     "menghadirkan layanan yang halal, adil, dan bermanfaat bagi banyak orang."),
]
VALUES = [
    ("Amanah", "Menyampaikan apa adanya, tanpa kelebihan dan kekurangan.", BLUE),
    ("Transparan", "Terbuka dalam setiap muamalah dan pengelolaan dana.", GREEN),
    ("Terjangkau", "Layanan keuangan syariah yang dekat dengan masyarakat.", GOLD),
]
PRODUCTS = [
    ("SIMIRA",
     "Simpanan Mitra Rencana — tabungan berencana harian mulai Rp40.000,-/hari "
     "sebagai persiapan dana umroh."),
    ("Tabungan Umroh Mitra",
     "Program tabungan ibadah: Haji tahun ini menjadi do'a, Umroh tahun depan "
     "jadi nyata."),
    ("Pembiayaan Mikro",
     "Pembiayaan usaha dengan akad syariah bagi pelaku UMKM dan masyarakat "
     "sekitar."),
    ("Layanan Lainnya",
     "Produk dan layanan syariah lainnya \u2014 silakan berkonsultasi dengan "
     "petugas kami."),
]
ADDRESS = "Kantor Kami  \u2014  Jl. Ayunda No. 23, Panorama, Bengkulu"
CONTACT_LINE = ("0813-1349-9673   \u00b7   mitrasyariahbank.co.id   \u00b7   "
                "@mitrasyariahbank")

BX, BW = 56, 944           # kolom kiri (profil)
PX, PW = 1044, 1030        # kolom kanan (produk)
DIV_X = 1022               # pembatas vertikal
BTOP, BBOT = 220, 1300
BAR_Y, BAR_H = 1330, 96


def eyebrow(x, y, label, color):
    return (rrect(x, y - 16, 46, 4, 0, color) +
            text(x + 62, y, label, 18, 800, color, ls=7, family=F_BODY))


def back_page():
    p = []
    p.append(star8(300, 1150, 240, stroke=BLUE, sw=2, opacity=0.04))
    p.append(star8(1800, 420, 240, stroke=GREEN, sw=2, opacity=0.04))

    # ---- kolom kiri: profil
    p.append(eyebrow(BX, 272, "TENTANG KAMI", GREEN))
    p.append(text(BX - 2, 334, "Bank Mitra Mentari Sejahtera", 42, 400, NAVY,
                  family=F_TITLE))
    p.append(line(BX, 364, BX + BW, 364, HAIR, 1.4))
    y = 408
    for para in PROFILE_PARAS:
        for ln in wrap(para, 21, 400, BW - 16, family=F_BODY):
            p.append(text(BX, y, ln, 21, 400, "#41505E", family=F_BODY))
            y += 33
        y += 12

    p.append(eyebrow(BX, 800, "NILAI KAMI", GREEN))
    vy = 858
    for name, desc, color in VALUES:
        p.append(star8(BX + 22, vy - 9, 24, fill=color))
        p.append(star8(BX + 22, vy - 9, 11, fill=WHITE))
        p.append(text(BX + 64, vy, name, 24, 800, NAVY, family=F_BODY))
        p.append(text(BX + 64, vy + 30, desc, 17, 400, MUTED, family=F_BODY))
        vy += 74

    # blok tagline navy
    p.append(f'<rect x="{BX}" y="1136" width="{BW}" height="164" '
             f'fill="url(#navyGrad)"/>')
    p.append(rrect(BX, 1136, BW, 4, 0, "url(#goldGrad)"))
    p.append(pattern_band(BX + 40, 1156, BW - 80, GOLD_BRIGHT, 40, 6, 0.25, 1.0))
    p.append(text(BX + BW / 2, 1232, "Pilihan Amanah Keluarga", 44, 400, WHITE,
                  anchor="middle", family=F_TITLE))
    p.append(diamond(BX + BW / 2, 1262, 7, GOLD_BRIGHT))
    p.append(text(BX + BW / 2, 1286, "BANK MITRA SYARIAH  \u00b7  BENGKULU", 15,
                  700, GOLD_SOFT, anchor="middle", ls=6, family=F_BODY))
    return "".join(p)


def back_products():
    p = []
    p.append(eyebrow(PX, 272, "PRODUK & LAYANAN", BLUE))
    ry = 330
    for i, (name, desc) in enumerate(PRODUCTS):
        p.append(text(PX, ry + 14, f"0{i + 1}", 22, 800, GOLD, ls=1,
                      family=F_BODY))
        p.append(text(PX + 66, ry + 16, name, 34, 400, NAVY, family=F_TITLE))
        for j, ln in enumerate(wrap(desc, 18, 400, PW - 120, family=F_BODY)[:2]):
            p.append(text(PX + 66, ry + 58 + j * 30, ln, 18, 400, MUTED,
                          family=F_BODY))
        p.append(star8(PX + PW - 14, ry + 22, 13, stroke=GOLD, sw=1.2,
                       opacity=0.7))
        p.append(line(PX, ry + 170, PX + PW, ry + 170, HAIR, 1.2))
        ry += 230
    p.append(text(PX, ry + 8, "Layanan lainnya dapat ditanyakan langsung ke "
                  "kantor kami \u2014 dengan akad syariah yang transparan.", 18,
                  400, MUTED, family=F_BODY))
    return "".join(p)


def back_footer_bar():
    p = [f'<rect x="{M}" y="{BAR_Y}" width="{W - 2 * M}" height="{BAR_H}" '
         f'fill="url(#navyGrad)"/>']
    p.append(rrect(M, BAR_Y, W - 2 * M, 4, 0, "url(#goldGrad)"))
    p.append(pattern_band(M + 30, BAR_Y + 22, W - 2 * M - 60, GOLD_BRIGHT, 44,
                          5.5, 0.22, 0.9))
    p.append(diamond(M + 26, BAR_Y + BAR_H / 2, 7, GOLD_BRIGHT))
    p.append(diamond(W - M - 26, BAR_Y + BAR_H / 2, 7, GOLD_BRIGHT))
    p.append(text(M + 40, BAR_Y + 44, ADDRESS, 19, 400, WHITE, family=F_BODY))
    p.append(text(M + 40, BAR_Y + 74, CONTACT_LINE, 16, 400, GOLD_SOFT,
                  family=F_BODY))
    p.append(text(W - M - 40, BAR_Y + 44, "PT BPRS Mitra Mentari Sejahtera", 19,
                  800, WHITE, anchor="end", family=F_BODY))
    p.append(text(W - M - 40, BAR_Y + 74, "Berizin & Diawasi oleh OJK  \u00b7  "
                  "Peserta Penjaminan LPS", 14, 400, GOLD_SOFT, anchor="end",
                  family=F_BODY))
    # kaki halaman (ritme sama dengan depan)
    p.append(line(M, 1450, W / 2 - 150, 1450, HAIR, 1.4))
    p.append(line(W / 2 + 150, 1450, W - M, 1450, HAIR, 1.4))
    p.append(flourish(W / 2, 1450, 140, GOLD, 1.3))
    p.append(text(M, 1484, OJK, 16, 400, MUTED, family=F_BODY))
    p.append(text(W - M, 1484, HEAD_TAG, 16, 700, GOLD, anchor="end", ls=4,
                  family=F_BODY))
    return "".join(p)


def build_back():
    body = "".join([background(), header(), back_page(), back_products(),
                    vertical_ornament(DIV_X, BTOP, BBOT), back_footer_bar()])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs()}{body}</svg>')


    # blok tagline navy
    p.append(f'<rect x="{BX}" y="1136" width="{BW}" height="164" '
             f'fill="url(#navyGrad)"/>')
    p.append(rrect(BX, 1136, BW, 4, 0, "url(#goldGrad)"))
    p.append(pattern_band(BX + 40, 1156, BW - 80, GOLD_BRIGHT, 40, 6, 0.25, 1.0))
    p.append(text(BX + BW / 2, 1232, "Pilihan Amanah Keluarga", 44, 400, WHITE,
                  anchor="middle", family=F_TITLE))
    p.append(diamond(BX + BW / 2, 1262, 7, GOLD_BRIGHT))
    p.append(text(BX + BW / 2, 1286, "BANK MITRA SYARIAH  \u00b7  BENGKULU", 15,
                  700, GOLD_SOFT, anchor="middle", ls=6, family=F_BODY))
    return "".join(p)


if __name__ == "__main__":
    main()
