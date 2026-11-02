"""
calendar_data.py — Data kalender untuk halaman bulanan (tanpa dependensi luar).

Gregorian memakai modul `calendar` bawaan Python; tanggal Hijriyah dihitung
dengan kalender Islam tabular (hisab 'urfi). Hasilnya PERKIRAAN dan wajib
diverifikasi dengan Kemenag/takwim resmi sebelum naik cetak.
"""
from __future__ import annotations

import calendar
import datetime as dt

HIJRI_MONTHS = [
    "Muharram", "Safar", "Rabiul Awal", "Rabiul Akhir", "Jumadil Awal",
    "Jumadil Akhir", "Rajab", "Sya'ban", "Ramadan", "Syawal", "Zulkaidah",
    "Zulhijah",
]

# Nama hari: Senin–Ahad (grid dimulai Senin)
DAY_NAMES = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Ahad"]
DAY_SHORT = ["SEN", "SEL", "RAB", "KAM", "JUM", "SAB", "AHD"]

GREG_MONTHS = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
               "Agustus", "September", "Oktober", "November", "Desember"]


def gregorian_to_jd(y: int, m: int, d: int) -> float:
    """Julian Day Number untuk tanggal Gregorian (algoritma Meeus)."""
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    return (int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5)


def jd_to_islamic(jd: float) -> tuple[int, int, int]:
    """Kalender Islam tabular (Kuwaiti algorithm)."""
    jd = int(jd) + 1
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = (((10985 - l) // 5316) * ((50 * l) // 17719)
         + (l // 5670) * ((43 * l) // 15238))
    l = (l - ((30 - j) // 15) * ((17719 * j) // 50)
         - (j // 16) * ((15238 * j) // 43) + 29)
    month = (24 * l) // 709
    day = l - (709 * month) // 24
    year = 30 * n + j - 30
    return year, month, day


def hijri_of(d: dt.date) -> tuple[int, int, int]:
    return jd_to_islamic(gregorian_to_jd(d.year, d.month, d.day))


def month_weeks(year: int, month: int) -> list[list[dt.date | None]]:
    """Matriks 6 baris × 7 kolom (Senin–Ahad).

    Sel di luar bulan diisi `None` supaya grid tetap 6 baris di semua bulan
    (ritme halaman konsisten) dan tanggal asing tidak tercetak.
    """
    cal = calendar.Calendar(firstweekday=0)      # 0 = Senin
    weeks: list[list[dt.date | None]] = []
    for wk in cal.monthdatescalendar(year, month):
        row = [d if d.month == month else None for d in wk]
        weeks.append(row)
    while len(weeks) < 6:
        weeks.append([None] * 7)
    return weeks


def month_grid(year: int, month: int) -> list[list[dt.date]]:
    """Matriks 7 kolom (Senin–Ahad) berisi tanggal asli, termasuk tanggal
    bulan sebelum/sesudahnya (dipakai untuk mengisi sel kosong secara halus)."""
    cal = calendar.Calendar(firstweekday=0)
    weeks = [list(wk) for wk in cal.monthdatescalendar(year, month)]
    while len(weeks) < 6:
        last = weeks[-1][-1]
        weeks.append([last + dt.timedelta(days=i) for i in range(1, 8)])
    return weeks


def hijri_span(year: int, month: int) -> str:
    """Label rentang Hijriyah sebuah bulan Gregorian, mis. 'Rajab – Sya'ban 1448 H'."""
    first = dt.date(year, month, 1)
    last = dt.date(year, month, calendar.monthrange(year, month)[1])
    y1, m1, _ = hijri_of(first)
    y2, m2, _ = hijri_of(last)
    if (y1, m1) == (y2, m2):
        return f"{HIJRI_MONTHS[m1 - 1]} {y1} H"
    if y1 == y2:
        return f"{HIJRI_MONTHS[m1 - 1]} – {HIJRI_MONTHS[m2 - 1]} {y1} H"
    return f"{HIJRI_MONTHS[m1 - 1]} {y1} – {HIJRI_MONTHS[m2 - 1]} {y2} H"


def weekday_name(d: dt.date) -> str:
    return DAY_NAMES[d.weekday()]


# Hari besar yang ditandai pada halaman Januari 2027.
# Tanggal keagamaan sengaja TIDAK dicetak otomatis (butuh keputusan Kemenag);
# tambahkan manual setelah disetujui.
HOLIDAYS_2027_01 = {
    1: "Tahun Baru 2027",
}
