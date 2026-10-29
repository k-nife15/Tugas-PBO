#!/usr/bin/env python3
"""
Generator desain: Kalender Meja Januari 2027 - BPRS Mitra Mentari Sejahtera
Gaya: playful + rapi (grid disiplin, aksen warna ceria, sticker/badge miring halus).

Output:
  dist/kalender-januari-2027-playful.svg   -> master vektor (bisa di-import ke Figma)
  dist/kalender-januari-2027-playful@2x.png
  dist/kalender-januari-2027-playful@4x.png
  dist/kalender-januari-2027-playful.pdf   -> raster 4x, 300 dpi siap cetak
  dist/kalender-januari-2027-data.json     -> data tanggal (mudah diverifikasi)

Semua angka layout dihitung dari font metrics (Pillow), bukan tebakan.
"""
import datetime as dt
import base64
import json
import os
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# 1. KONFIGURASI
# ----------------------------------------------------------------------------
W, H = 794, 559
M = 22                      # margin luar
LEFT_X, LEFT_W = 22, 272
RIGHT_X, RIGHT_W = 306, 466
CARD_Y, CARD_H = 92, 372
NOTES_Y, NOTES_H = 472, 38
FOOTER_Y = 520

PAD = 16                    # padding dalam kartu
INNER_L = LEFT_X + PAD      # 38
INNER_R = LEFT_X + LEFT_W - PAD   # 278
RIN_X = RIGHT_X + PAD       # 322
RIN_W = RIGHT_W - 2 * PAD   # 434

# Palet: brand BPRS + aksen playful
INK = "#0B1B3F"
SLATE = "#5B6B85"
MUTED = "#93A1B8"
LINE = "#E7EEF9"
PAPER = "#FFFCF6"
CARD = "#FFFFFF"
BLUE = "#0052CC"
BLUE_SOFT = "#E8F1FF"
EMERALD = "#059669"
EMERALD_SOFT = "#E6F8F1"
GOLD = "#FBBF24"
GOLD_DARK = "#D97706"
GOLD_SOFT = "#FFF6DE"
ROSE = "#E11D48"
ROSE_SOFT = "#FFEDF1"
VIOLET = "#7C3AED"
VIOLET_SOFT = "#F3ECFF"
CELL_BG = "#FBFDFF"
CELL_LINE = "#EDF2FA"
TAIL_BG = "#F4F7FC"
TAIL_TXT = "#AEBACE"

# Konten
BRAND_PILL = "Bank Mitra Syariah  \u00b7  Pilihan Amanah Keluarga"
HEAD_TAG = "Kalender Meja  \u00b7  Edisi Januari 2027"
HIJRI_LINE = "RAJAB \u2013 SYA'BAN 1448 H   \u00b7   REJEB \u2013 RUWAH 1960 Dal"
PROMO_KICKER = "PROGRAM SIMIRA"
PROMO_KICKER_SUB = "Simpanan Mitra Rencana"
PROMO_TITLE = ["TABUNGAN", "UMROH MITRA"]
PROMO_SUB = ["Hajilah tahun ini jadi do'a,", "Umroh tahun depan jadi nyata."]
PRICE_MAIN = "Mulai Rp40.000,-"
PRICE_SUB = "/ hari"
BENEFITS = [
    ("Mudah Pendaftaran", EMERALD),
    ("Transparan Kelolaannya", BLUE),
    ("Aman dan Amanah", VIOLET),
    ("Menarik bagi hasilnya", GOLD_DARK),
]
PROMO_FOOT = ["Travel PPU & PIHK Terpercaya", "Amanah \u00b7 Transparan \u00b7 Terjangkau"]
OIJD = "PT BPRS Mitra Mentari Sejahtera  \u00b7  Berizin & Diawasi OJK  \u00b7  Peserta Penjaminan LPS"
CONTACTS = [("tel", "0813-1349-9673"), ("web", "mitrasyariahbank.co.id"), ("ig", "@mitrasyariahbank")]

# Catatan: Isra Mi'raj = 27 Rajab 1448 H = 6 Januari 2027 (hasil kalender hisab).
# Ubah ke 5 jika mengikuti versi desain lama.
HOLIDAYS = [
    (ROSE, "1 Jan", "Tahun Baru 2027 Masehi"),
    (VIOLET, "6 Jan", "Isra' Mi'raj Nabi Muhammad SAW 1448 H"),
    (GOLD_DARK, "22\u201324 Jan", "Puasa Sunnah Ayyamul Bidh (13\u201315 Sya'ban 1448 H)"),
]

WEEKDAYS = ["Ahad", "Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu"]

# ----------------------------------------------------------------------------
# 2. FONT & TEKS
# ----------------------------------------------------------------------------
FONT_FILES = {
    400: "Poppins-Regular.ttf",
    500: "Poppins-Medium.ttf",
    600: "Poppins-SemiBold.ttf",
    700: "Poppins-Bold.ttf",
    800: "Poppins-ExtraBold.ttf",
}
_cache = {}


def font(size, weight=400):
    key = (size, weight)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(str(ASSETS / "fonts" / FONT_FILES[weight]), size)
    return _cache[key]


def tw(text, size, weight=400, ls=0.0, safety=None):
    """Lebar teks (px). `safety` mengkompensasi pembulatan advance glyph oleh
    renderer pada ukuran kecil (terukur: teks 7px bisa ~10-14% lebih lebar)."""
    base = font(size, weight).getlength(text) + ls * max(len(text) - 1, 0)
    if safety is None:
        safety = 1.14 if size < 8 else (1.07 if size < 10 else 1.02)
    return base * safety


def wrap(text, size, weight, max_w):
    """Word-wrap sederhana berbasis lebar terukur."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if tw(trial, size, weight) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size=8, weight=400, fill=INK, anchor="start", ls=0.0,
         opacity=1.0, extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    o = f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="Poppins" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{a}{l}{o}{extra}>{esc(s)}</text>')


def rrect(x, y, w, h, r, fill, stroke=None, sw=1, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{r}" fill="{fill}"{s}{extra}/>')


def pill(x, y, h, label, size, bg, fg, weight=600, padx=10, ls=0.0, r=None,
         stroke=None, sw=1):
    """Pill auto-width; mengembalikan (svg, lebar)."""
    w = tw(label, size, weight, ls) + padx * 2
    r = h / 2 if r is None else r
    svg = (rrect(x, y, w, h, r, bg, stroke, sw)
           + text(x + w / 2, y + h / 2 + size * 0.36, label, size, weight, fg,
                  anchor="middle", ls=ls))
    return svg, w


def star(cx, cy, r, fill, opacity=1.0):
    """Bintang 4 sudut (sparkle) - elemen playful."""
    d = r * 0.28
    pts = (f"{cx:.2f},{cy - r:.2f} {cx + d:.2f},{cy - d:.2f} {cx + r:.2f},{cy:.2f} "
           f"{cx + d:.2f},{cy + d:.2f} {cx:.2f},{cy + r:.2f} {cx - d:.2f},{cy + d:.2f} "
           f"{cx - r:.2f},{cy:.2f} {cx - d:.2f},{cy - d:.2f}")
    return f'<polygon points="{pts}" fill="{fill}" opacity="{opacity}"/>'


# ----------------------------------------------------------------------------
# 3. DATA KALENDER (Gregorian -> Hijriah + pasaran Jawa)
# ----------------------------------------------------------------------------
PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
PASARAN_REF = dt.date(1945, 8, 17)          # Jumat Legi (referensi baku)
HIJRI_MONTHS = ["Muharram", "Safar", "Rabiul Awal", "Rabiul Akhir",
                "Jumadil Awal", "Jumadil Akhir", "Rajab", "Sya'ban",
                "Ramadhan", "Syawal", "Dzulqadah", "Dzulhijjah"]


def jdn(y, m, d):
    a = (14 - m) // 12
    y2, m2 = y + 4800 - a, m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045


def hijri(y, m, d):
    """Konversi tabular (Kuwaiti algorithm). Teruji: 2026-01-16 -> 1447-07-27."""
    j = jdn(y, m, d)
    l = j - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    jj = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - jj) // 15) * ((17719 * jj) // 50) - (jj // 16) * ((15238 * jj) // 43) + 29
    mo = (24 * l) // 709
    da = l - (709 * mo) // 24
    yr = 30 * n + jj - 30
    return yr, mo, da


def build_cells():
    """42 sel: 27 Des 2026 .. 6 Feb 2027 (6 baris x 7 kolom)."""
    cells = []
    start = dt.date(2026, 12, 27)            # Ahad
    for i in range(42):
        day = start + dt.timedelta(days=i)
        hy, hm, hd = hijri(day.year, day.month, day.day)
        cells.append({
            "date": day.isoformat(),
            "day": day.day,
            "col": i % 7,
            "row": i // 7,
            "in_month": day.month == 1,
            "weekday": WEEKDAYS[(day.weekday() + 1) % 7],
            "pasaran": PASARAN[(day - PASARAN_REF).days % 5],
            "hijri_day": hd,
            "hijri_month": HIJRI_MONTHS[hm - 1],
            "hijri_year": hy,
        })
    return cells



CELLS = build_cells()


# ----------------------------------------------------------------------------
# 4. BAGIAN-BAGIAN DESAIN
# ----------------------------------------------------------------------------
def logo_uri():
    data = base64.b64encode((ASSETS / "logo-brand.png").read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def defs():
    return f"""<defs>
  <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FFD965"/><stop offset="0.55" stop-color="#FBBF24"/>
    <stop offset="1" stop-color="#F59E0B"/>
  </linearGradient>
  <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#0052CC"/><stop offset="1" stop-color="#059669"/>
  </linearGradient>
  <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
    <circle cx="1.2" cy="1.2" r="0.9" fill="#E6D9BF" opacity="0.55"/>
  </pattern>
  <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#0B1B3F" flood-opacity="0.09"/>
  </filter>
  <filter id="chipShadow" x="-30%" y="-30%" width="160%" height="180%">
    <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#8A5A00" flood-opacity="0.28"/>
  </filter>
</defs>"""


def background():
    p = [rrect(0, 0, W, H, 0, PAPER)]
    p.append(rrect(0, 0, W, H, 0, "url(#dots)"))
    # blob lembut di area header (playful, tapi tetap tenang)
    p.append(f'<circle cx="756" cy="4" r="72" fill="{GOLD_SOFT}" opacity="0.75"/>')
    p.append(f'<circle cx="828" cy="66" r="58" fill="{EMERALD_SOFT}" opacity="0.85"/>')
    p.append(f'<circle cx="438" cy="10" r="30" fill="{BLUE_SOFT}" opacity="0.9"/>')
    return "".join(p)


def header():
    p = []
    # logo brand asli (dari file Figma)
    p.append(f'<image x="22" y="26" width="150" height="28.13" '
             f'xlink:href="{logo_uri()}" preserveAspectRatio="xMinYMid meet"/>')
    # tag edisi + sparkle
    p.append(star(190, 36, 5.2, GOLD_DARK, 0.95))
    p.append(text(199, 40, HEAD_TAG, 8.6, 600, SLATE, ls=0.2))
    # pill brand kanan
    svg, w = pill(0, 28, 24, BRAND_PILL, 8, BLUE_SOFT, BLUE, weight=600, padx=11,
                  stroke=BLUE, sw=0.8)
    x = 772 - w
    p.append(f'<g transform="translate({x:.2f},0)">')
    p.append(rrect(0, 28, w, 24, 12, BLUE_SOFT, BLUE, 0.8))
    p.append(f'<circle cx="12" cy="40" r="3.2" fill="{GOLD}"/>')
    p.append(text(21, 43, BRAND_PILL, 8, 600, BLUE, ls=0.1))
    p.append("</g>")
    return "".join(p)


def left_card():
    p = [rrect(LEFT_X, CARD_Y, LEFT_W, CARD_H, 20, CARD, LINE, 1,
               ' filter="url(#cardShadow)"')]
    # aksen sudut: garis lengkung putus-putus
    p.append(f'<path d="M {LEFT_X + LEFT_W - 46} {CARD_Y} q 40 26 12 62" fill="none" '
             f'stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="1 6" '
             f'stroke-linecap="round" opacity="0.75"/>')
    p.append(star(LEFT_X + LEFT_W - 26, CARD_Y + 22, 4.6, GOLD, 0.9))

    # kicker
    y = CARD_Y + 18
    kv, kw = pill(INNER_L, y, 19, PROMO_KICKER, 6.8, EMERALD_SOFT, EMERALD,
                  weight=700, padx=9, ls=0.7)
    p.append(kv)
    p.append(text(INNER_L + kw + 7, y + 12.4, PROMO_KICKER_SUB, 6.6, 500, MUTED))

    # judul
    p.append(text(INNER_L, 174, PROMO_TITLE[0], 20, 800, INK, ls=0.2))
    p.append(rrect(INNER_L - 3, 184, tw("UMROH", 20, 800) + 8, 13, 5, GOLD_SOFT))
    p.append(text(INNER_L, 198, PROMO_TITLE[1], 20, 800, INK, ls=0.2))

    # sub copy
    p.append(text(INNER_L, 220, PROMO_SUB[0], 8, 400, SLATE))
    p.append(text(INNER_L, 231, PROMO_SUB[1], 8, 400, SLATE))

    # sticker harga (miring halus)
    main_w = tw(PRICE_MAIN, 12.5, 800)
    sub_w = tw(PRICE_SUB, 7.5, 600) + 3
    sw_ = main_w + sub_w + 26
    sh = 34
    sy = 244
    cx, cy = INNER_L + sw_ / 2, sy + sh / 2
    p.append(f'<g transform="rotate(-2.4 {cx:.2f} {cy:.2f})">')
    p.append(rrect(INNER_L, sy, sw_, sh, 11, "url(#goldGrad)", "#FFFFFF", 2,
                   ' filter="url(#chipShadow)"'))
    p.append(text(INNER_L + 13, sy + sh / 2 + 4.6, PRICE_MAIN, 12.5, 800, "#3D2600"))
    p.append(text(INNER_L + 13 + main_w + 3, sy + sh / 2 + 3.4, PRICE_SUB, 7.5, 600,
                  "#5A3B00"))
    p.append("</g>")

    # benefit list
    by = 302
    for label, color in BENEFITS:
        p.append(f'<circle cx="{INNER_L + 7}" cy="{by - 3.4}" r="7" fill="{color}"/>')
        p.append(f'<path d="M {INNER_L + 4.1} {by - 3.5} l 2.1 2.1 l 3.7 -3.9" fill="none" '
                 f'stroke="#FFFFFF" stroke-width="1.7" stroke-linecap="round" '
                 f'stroke-linejoin="round"/>')
        p.append(text(INNER_L + 20, by, label, 8.4, 600, "#2E3D57"))
        by += 21.5

    # divider putus-putus
    p.append(f'<line x1="{INNER_L}" y1="382" x2="{INNER_R}" y2="382" stroke="{LINE}" '
             f'stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round"/>')

    # doodle: ka'bah -> jalur terbang -> pesawat (playful, tema umroh)
    kx, ky, ks = INNER_L + 6, 390, 26
    p.append(rrect(kx, ky, ks, ks, 4, "#111827"))
    p.append(rrect(kx, ky + 9, ks, 5, 0, GOLD))
    p.append(rrect(kx, ky + 9, ks, 1.2, 0, "#FFFFFF", extra=' opacity="0.55"'))
    p.append(f'<path d="M {kx + ks + 8} {ky + 18} q 52 -26 104 -6" fill="none" '
             f'stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="1 5" '
             f'stroke-linecap="round" opacity="0.6"/>')
    px, py = kx + ks + 112, ky + 12
    p.append(f'<g transform="translate({px} {py}) rotate(-18)">'
             f'<path d="M0 0 L16 5 L4.5 9.5 L3.5 15 L0 8 Z" fill="{BLUE}" opacity="0.92"/>'
             f'</g>')
    p.append(star(INNER_R - 10, ky + 4, 5.2, GOLD, 0.95))
    p.append(star(kx + 20, ky - 6, 3.4, GOLD_DARK, 0.7))

    # footnote
    p.append(text(INNER_L, 444, "Travel PPU & PIHK Terpercaya  \u00b7  Amanah  \u00b7  "
                  "Transparan  \u00b7  Terjangkau", 6.5, 500, MUTED))
    return "".join(p)


HOLIDAY_SET = {"2027-01-01", "2027-01-06"}
PUASA_SET = {"2027-01-22", "2027-01-23", "2027-01-24"}
ROWH, ROWGAP, COLGAP = 39, 5, 5
COLW = (RIN_W - 6 * COLGAP) / 7
GRID_Y = 186


def right_card():
    p = [rrect(RIGHT_X, CARD_Y, RIGHT_W, CARD_H, 20, CARD, LINE, 1,
               ' filter="url(#cardShadow)"')]

    # ---- judul bulan
    p.append(text(RIN_X, 132, "JANUARI", 25, 800, INK, ls=0.3))
    jw = tw("JANUARI", 25, 800, 0.3)
    p.append(text(RIN_X + jw + 8, 132, "2027", 25, 800, GOLD_DARK, ls=0.3))

    # ---- sticker 01 BULAN (miring, playful)
    bx, by_, bw, bh = 718, 104, 38, 36
    ccx, ccy = bx + bw / 2, by_ + bh / 2
    p.append(f'<g transform="rotate(4.5 {ccx:.2f} {ccy:.2f})">')
    p.append(rrect(bx, by_, bw, bh, 11, VIOLET_SOFT, VIOLET, 1.1))
    p.append(text(ccx, by_ + 21.5, "01", 16, 800, VIOLET, anchor="middle"))
    p.append(text(ccx, by_ + 31, "BULAN", 5.6, 700, VIOLET, anchor="middle", ls=1))
    p.append("</g>")

    # ---- subjudul hijriah
    p.append(text(RIN_X, 150, HIJRI_LINE, 8.2, 500, SLATE, ls=0.15))

    # ---- header hari
    hy, hh = 160, 20
    for i, name in enumerate(WEEKDAYS):
        x = RIN_X + i * (COLW + COLGAP)
        if i == 0:
            bg, fg = ROSE_SOFT, ROSE
        elif i == 5:
            bg, fg = EMERALD_SOFT, EMERALD
        elif i == 6:
            bg, fg = BLUE_SOFT, BLUE
        else:
            bg, fg = "#F5F8FD", SLATE
        p.append(rrect(x, hy, COLW, hh, 8, bg))
        p.append(text(x + COLW / 2, hy + hh / 2 + 2.7, name, 7.4, 600, fg,
                      anchor="middle"))

    # ---- grid tanggal
    for c in CELLS:
        x = RIN_X + c["col"] * (COLW + COLGAP)
        y = GRID_Y + c["row"] * (ROWH + ROWGAP)
        d = c["date"]
        is_holiday = d in HOLIDAY_SET
        is_puasa = d in PUASA_SET
        tail = not c["in_month"]

        if is_holiday:
            bg, stroke, num_c, sub_c = ROSE, None, "#FFFFFF", "rgba(255,255,255,0.88)"
        elif is_puasa:
            bg, stroke, num_c, sub_c = GOLD_SOFT, "#FFE3A6", GOLD_DARK, "#9A6A12"
        elif tail:
            bg, stroke, num_c, sub_c = TAIL_BG, None, TAIL_TXT, "#C2CCDC"
        else:
            bg, stroke = CELL_BG, CELL_LINE
            num_c = {0: ROSE, 5: EMERALD, 6: BLUE}.get(c["col"], INK)
            sub_c = MUTED

        p.append(rrect(x, y, COLW, ROWH, 11, bg, stroke, 1))
        p.append(text(x + COLW / 2, y + 22, str(c["day"]), 15.5, 800, num_c,
                      anchor="middle"))
        p.append(text(x + COLW / 2, y + 33, f"{c['hijri_day']} {c['pasaran']}",
                      6.1, 500, sub_c, anchor="middle", ls=0.1))

        if is_holiday:
            p.append(f'<circle cx="{x + COLW - 9}" cy="{y + 9}" r="2.4" fill="#FFFFFF" '
                     f'opacity="0.9"/>')
        elif is_puasa:
            p.append(f'<circle cx="{x + COLW - 9}" cy="{y + 9}" r="2.4" fill="{GOLD_DARK}" '
                     f'opacity="0.85"/>')
    return "".join(p)


def notes_strip():
    """3 kartu info hari libur (aman dari tabrakan teks, lebih playful)."""
    cw = (W - 2 * M - 2 * 12) / 3
    y, h = 470, 40
    p = []
    for i, (color, day, label) in enumerate(HOLIDAYS):
        x = M + i * (cw + 12)
        p.append(rrect(x, y, cw, h, 12, CARD, LINE, 1,
                       ' filter="url(#cardShadow)"'))
        p.append(rrect(x + 10, y + 11, 3.2, h - 22, 1.6, color))
        p.append(text(x + 20, y + 16.5, day, 7.6, 800, color))
        lines = wrap(label, 6.6, 500, cw - 32)[:2]
        for j, ln in enumerate(lines):
            p.append(text(x + 20, y + 26.5 + j * 9, ln, 6.6, 500, SLATE))
    return "".join(p)


ICON_COLORS = {"tel": EMERALD, "web": BLUE, "ig": ROSE}
ICON_LABEL = {"tel": "WA", "web": "WEB", "ig": "IG"}


def footer():
    p = []
    p.append(text(M, 526,
                  "PT BPRS Mitra Mentari Sejahtera  \u00b7  Berizin & Diawasi oleh OJK",
                  6.5, 500, MUTED))
    p.append(text(M, 537, "dan Merupakan Peserta Penjaminan (LPS)", 6.5, 500, MUTED))

    chips = []
    for kind, label in CONTACTS:
        chips.append((kind, label, 18 + tw(label, 6.8, 600)))
    total = sum(c[2] for c in chips) + 12 * (len(chips) - 1)
    x = 772 - total
    cy = 527
    for kind, label, w in chips:
        p.append(rrect(x, cy - 9, 13, 13, 4.5, ICON_COLORS[kind]))
        p.append(text(x + 6.5, cy - 1.4, ICON_LABEL[kind], 4.7, 700, "#FFFFFF",
                      anchor="middle", ls=0.2))
        p.append(text(x + 18, cy + 0.6, label, 6.8, 600, SLATE))
        x += w + 12
    return "".join(p)




# ----------------------------------------------------------------------------
# 5. ASSEMBLY
# ----------------------------------------------------------------------------
def build_svg():
    body = "".join([background(), header(), left_card(), right_card(),
                    notes_strip(), footer()])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs()}{body}</svg>')


def main():
    svg = build_svg()
    (DIST / "kalender-januari-2027-playful.svg").write_text(svg, encoding="utf-8")
    data = {
        "title": "Kalender Meja Januari 2027 - BPRS Mitra Mentari Sejahtera",
        "month": "Januari 2027",
        "hijri": "Rajab - Sya'ban 1448 H / Rejeb - Ruwah 1960 Dal",
        "size_px": [W, H],
        "palette": {"blue": BLUE, "emerald": EMERALD, "gold": GOLD,
                    "gold_dark": GOLD_DARK, "rose": ROSE, "violet": VIOLET,
                    "ink": INK, "slate": SLATE},
        "holidays": [{"date": d, "label": l} for _, d, l in HOLIDAYS],
        "cells": CELLS,
    }
    (DIST / "kalender-januari-2027-data.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SVG + JSON written to", DIST)


if __name__ == "__main__":
    main()
