#!/usr/bin/env python3
"""Primitif desain + data kalender yang dipakai bersama oleh semua varian.

Berisi: registry font, pengukuran teks (Pillow), helper SVG (rect/pill/text/star/
ornamen Islam) dan perhitungan tanggal Hijriah + pasaran Jawa.
"""
import datetime as dt
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# FONT
# ----------------------------------------------------------------------------
FONT_FILES = {
    "Poppins": {
        400: "Poppins-Regular.ttf",
        500: "Poppins-Medium.ttf",
        600: "Poppins-SemiBold.ttf",
        700: "Poppins-Bold.ttf",
        800: "Poppins-ExtraBold.ttf",
    },
    "Marcellus": {400: "Marcellus-Regular.ttf"},
    "Lato": {
        400: "Lato-Regular.ttf",
        500: "Lato-Regular.ttf",
        700: "Lato-Bold.ttf",
        800: "Lato-Black.ttf",
    },
}

_cache = {}


def font(size, weight=400, family="Poppins"):
    files = FONT_FILES[family]
    weight = min(files, key=lambda w: abs(w - weight))
    key = (family, size, weight)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(str(ASSETS / "fonts" / files[weight]), size)
    return _cache[key]


def tw(text, size, weight=400, ls=0.0, family="Poppins", safety=None):
    """Lebar teks (px). `safety` mengkompensasi pembulatan advance glyph oleh
    renderer pada ukuran kecil (terukur: teks 7px bisa ~10-14% lebih lebar)."""
    base = font(size, weight, family).getlength(text) + ls * max(len(text) - 1, 0)
    if safety is None:
        safety = 1.14 if size < 8 else (1.07 if size < 10 else 1.02)
    return base * safety


def wrap(text, size, weight, max_w, family="Poppins"):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if tw(trial, size, weight, family=family) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines



# ----------------------------------------------------------------------------
# SVG PRIMITIF
# ----------------------------------------------------------------------------
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=8, weight=400, fill="#000", anchor="start", ls=0.0,
         opacity=1.0, extra="", family="Poppins"):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    o = f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{a}{l}{o}{extra}>{esc(s)}</text>')


def rrect(x, y, w, h, r, fill, stroke=None, sw=1, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{r}" fill="{fill}"{s}{extra}/>')


def pill(x, y, h, label, size, bg, fg, weight=600, padx=10, ls=0.0, r=None,
         stroke=None, sw=1, family="Poppins"):
    w = tw(label, size, weight, ls, family=family) + padx * 2
    r = h / 2 if r is None else r
    svg = (rrect(x, y, w, h, r, bg, stroke, sw)
           + text(x + w / 2, y + h / 2 + size * 0.36, label, size, weight, fg,
                  anchor="middle", ls=ls, family=family))
    return svg, w


def line(x1, y1, x2, y2, color, sw=1, dash=None, cap="butt", opacity=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    c = f' stroke-linecap="{cap}"' if cap != "butt" else ""
    o = f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{sw}"{d}{c}{o}/>')


def star(cx, cy, r, fill, opacity=1.0):
    """Bintang 4 sudut (sparkle) - elemen playful."""
    d = r * 0.28
    pts = (f"{cx:.2f},{cy - r:.2f} {cx + d:.2f},{cy - d:.2f} {cx + r:.2f},{cy:.2f} "
           f"{cx + d:.2f},{cy + d:.2f} {cx:.2f},{cy + r:.2f} {cx - d:.2f},{cy + d:.2f} "
           f"{cx - r:.2f},{cy:.2f} {cx - d:.2f},{cy - d:.2f}")
    return f'<polygon points="{pts}" fill="{fill}" opacity="{opacity}"/>'


def star8(cx, cy, r, fill="none", stroke=None, sw=1, inner=0.42, opacity=1.0):
    """Bintang 8 sudut (khatim) - ornamen geometri Islam."""
    import math
    pts = []
    for i in range(16):
        rad = r if i % 2 == 0 else r * inner
        ang = math.pi / 8 * i - math.pi / 2
        pts.append(f"{cx + rad * math.cos(ang):.2f},{cy + rad * math.sin(ang):.2f}")
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}"{s} '
            f'opacity="{opacity}"/>')


def arch(x, y, w, h, fill, stroke=None, sw=1, apex=0.42, extra=""):
    """Panel mihrab: lengkung runcing khas arsitektur Islam."""
    ay = y + h * apex
    d = (f"M {x:.2f} {y + h:.2f} L {x:.2f} {ay:.2f} "
         f"Q {x:.2f} {y + h * apex * 0.22:.2f} {x + w / 2:.2f} {y:.2f} "
         f"Q {x + w:.2f} {y + h * apex * 0.22:.2f} {x + w:.2f} {ay:.2f} "
         f"L {x + w:.2f} {y + h:.2f} Z")
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{s}{extra}/>'


def diamond(cx, cy, r, fill):
    return (f'<polygon points="{cx:.2f},{cy - r:.2f} {cx + r:.2f},{cy:.2f} '
            f'{cx:.2f},{cy + r:.2f} {cx - r:.2f},{cy:.2f}" fill="{fill}"/>')



# ----------------------------------------------------------------------------
# DATA KALENDER
# ----------------------------------------------------------------------------
PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
PASARAN_REF = dt.date(1945, 8, 17)          # Jumat Legi (referensi baku)
HIJRI_MONTHS = ["Muharram", "Safar", "Rabiul Awal", "Rabiul Akhir",
                "Jumadil Awal", "Jumadil Akhir", "Rajab", "Sya'ban",
                "Ramadhan", "Syawal", "Dzulqadah", "Dzulhijjah"]
WEEKDAYS = ["Ahad", "Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu"]


def jdn(y, m, d):
    a = (14 - m) // 12
    y2, m2 = y + 4800 - a, m + 12 * a - 3
    return (d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4
            - y2 // 100 + y2 // 400 - 32045)


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
    start = dt.date(2026, 12, 27)           # Ahad
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
