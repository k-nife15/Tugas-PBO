"""
Data penanggalan kalender meja BPR Syariah Mitra Mentari Sejahtera 2027.

Acuan Hijriah: Umm al-Qura / Kemenag RI (SKB 3 Menteri)
  - 1 Rajab  1448 H = 10 Desember 2026
  - 1 Sya'ban 1448 H =  9 Januari 2027   (Rajab 30 hari)
  - 27 Rajab 1448 H =  5 Januari 2027    -> Isra Mi'raj
Pasaran Jawa memakai siklus 5 hari kontinu terhadap Julian Day,
di-anchor pada 17 Agustus 1945 = Jum'at Legi.
"""

from __future__ import annotations

import datetime as _dt

HARI_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Ahad"]

HIJRI_ID = [
    "", "Muharram", "Safar", "Rabiul Awal", "Rabiul Akhir", "Jumadil Awal",
    "Jumadil Akhir", "Rajab", "Sya'ban", "Ramadhan", "Syawal", "Dzulqa'dah",
    "Dzulhijjah",
]

HIJRI_AR = [
    "", "مُحَرَّم", "صَفَر", "رَبِيع الأَوَّل", "رَبِيع الآخِر", "جُمَادَى الأُولَى",
    "جُمَادَى الآخِرَة", "رَجَب", "شَعْبَان", "رَمَضَان", "شَوَّال", "ذُو القَعْدَة",
    "ذُو الحِجَّة",
]

HARI_AR = [
    "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد",
]

PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]

_JD_HIJRI_EPOCH = 1948440  # 1 Muharram 1 H (kalender tabular)


def gregorian_to_jd(y: int, m: int, d: int) -> int:
    """Julian Day Number dari tanggal Gregorian."""
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


_JD_LEGI_ANCHOR = gregorian_to_jd(1945, 8, 17)  # 17 Agustus 1945 = Legi


def pasaran(tanggal: _dt.date) -> str:
    jd = gregorian_to_jd(tanggal.year, tanggal.month, tanggal.day)
    return PASARAN[(jd - _JD_LEGI_ANCHOR) % 5]


def weton(tanggal: _dt.date) -> str:
    return f"{HARI_ID[tanggal.weekday()]} {pasaran(tanggal)}"


AWAL_BULAN = {
    (1448, 7): _dt.date(2026, 12, 10),
    (1448, 8): _dt.date(2027, 1, 9),
}

PANJANG_BULAN = {(1448, 7): 30, (1448, 8): 30}


def _panjang_bulan(hy: int, hm: int) -> int:
    return PANJANG_BULAN.get((hy, hm), 30 if hm % 2 == 1 else 29)


def _hijri_tabular(tanggal: _dt.date):
    jd = gregorian_to_jd(tanggal.year, tanggal.month, tanggal.day)
    l = jd - _JD_HIJRI_EPOCH + 1
    hy = int((30 * l + 10646) / 10631)
    while True:
        awal = _JD_HIJRI_EPOCH + (hy - 1) * 354 + (3 + 11 * hy) // 30
        akhir = _JD_HIJRI_EPOCH + hy * 354 + (3 + 11 * (hy + 1)) // 30
        if awal <= jd < akhir:
            break
        hy += 1 if jd >= akhir else -1
    sisa = jd - awal + 1
    hm = 1
    while True:
        pb = _panjang_bulan(hy, hm)
        if sisa <= pb:
            return hy, hm, sisa
        sisa -= pb
        hm += 1


def hijriah(tanggal: _dt.date):
    """(tahun, bulan, hari) Hijriah untuk tanggal Gregorian."""
    for (hy, hm) in sorted(AWAL_BULAN, reverse=True):
        awal = AWAL_BULAN[(hy, hm)]
        if tanggal >= awal:
            selisih = (tanggal - awal).days
            while True:
                pb = _panjang_bulan(hy, hm)
                if selisih < pb:
                    break
                selisih -= pb
                hm += 1
                if hm > 12:
                    hm, hy = 1, hy + 1
                if (hy, hm) in AWAL_BULAN:
                    selisih = (tanggal - AWAL_BULAN[(hy, hm)]).days
            return hy, hm, selisih + 1
    return _hijri_tabular(tanggal)


def hijriah_teks(tanggal: _dt.date) -> str:
    hy, hm, hd = hijriah(tanggal)
    return f"{hd} {HIJRI_ID[hm]} {hy} H"


def angka_arab(n: int) -> str:
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


# --- Hari libur / hari besar (mengikuti kalender sumber) -------------------
LIBUR_NASIONAL = {
    (2027, 1, 1): "LIBUR TAHUN BARU 2027 MASEHI",
    (2027, 1, 5): "LIBUR ISRA MIRAJ NABI MUHAMMAD SAW 1448 H",
}

CATATAN_TANGGAL = [
    "Awal bulan Sya'ban 1448 H jatuh pada Sabtu, 9 Januari 2027.",
    "Puasa Sunnah Ayyamul Bidh: 21 - 23 Januari 2027 (13 - 15 Sya'ban 1448 H).",
]

PUASA_BIDH_JAN = [21, 22, 23]


def matriks_bulan(tahun: int, bulan: int, isi_awal: bool = True, isi_akhir: bool = False):
    """Matriks 5/6 baris x 7 kolom (kolom 0 = Ahad).

    Mengembalikan list baris berisi tuple (tanggal, apakah_bulan_ini).
    Tanggal awal (sisa bulan sebelumnya) ikut ditampilkan seperti kalender
    dinding/meja pada umumnya; sel kosong di akhir bernilai (None, False).
    """
    pertama = _dt.date(tahun, bulan, 1)
    kolom_awal = (pertama.weekday() + 1) % 7
    berikut = _dt.date(tahun + (bulan == 12), bulan % 12 + 1, 1)
    jml = (berikut - pertama).days
    sel = []
    if isi_awal:
        for i in range(kolom_awal):
            sel.append((pertama - _dt.timedelta(days=kolom_awal - i), False))
    else:
        sel += [(None, False)] * kolom_awal
    sel += [(pertama + _dt.timedelta(days=i), True) for i in range(jml)]
    if isi_akhir:
        n = 0
        while len(sel) % 7:
            n += 1
            sel.append((berikut + _dt.timedelta(days=n - 1), False))
    while len(sel) % 7:
        sel.append((None, False))
    return [sel[i:i + 7] for i in range(0, len(sel), 7)]


if __name__ == "__main__":
    for tgl in [
        _dt.date(2026, 12, 10), _dt.date(2027, 1, 1), _dt.date(2027, 1, 5),
        _dt.date(2027, 1, 9), _dt.date(2027, 1, 31), _dt.date(2027, 2, 1),
    ]:
        print(tgl, "|", hijriah_teks(tgl), "|", weton(tgl))
