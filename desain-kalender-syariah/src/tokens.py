"""
tokens.py — Design tokens (warna, tipografi, grid) untuk kalender meja
Bank Syariah. Semua satuan geometri dalam milimeter (mm) mengikuti
ukuran jadi 213 x 152 mm (landscape) + bleed 3 mm.
"""

# --- Geometri cetak -----------------------------------------------------
TRIM_W, TRIM_H = 213.0, 152.0          # ukuran jadi (landscape)
BLEED = 3.0                            # bleed tiap sisi
DOC_W = TRIM_W + 2 * BLEED             # 219 mm
DOC_H = TRIM_H + 2 * BLEED             # 158 mm

SAFE_TOP = 15.0      # zona jilid Wire-O (1,5 cm) — wajib kosong
SAFE_SIDE = 12.0     # margin aman kiri/kanan
SAFE_BOTTOM = 12.0   # margin aman bawah

WIRE_PITCH = 3       # 3:1 pitch (3 lubang per inci) -> pitch 8,467 mm
WIRE_HOLES = 24      # jumlah lubang untuk panjang 213 mm


def X(mm: float) -> float:
    """Konversi mm (relatif trim kiri) -> koordinat dokumen."""
    return BLEED + mm


def Y(mm: float) -> float:
    """Konversi mm (relatif trim atas) -> koordinat dokumen."""
    return BLEED + mm


# --- Palet warna --------------------------------------------------------
# Dominan: Deep Emerald Green (utama) / Navy Blue (alternatif)
EMERALD_DEEP = "#062B22"
EMERALD = "#0E5241"
EMERALD_MID = "#12684F"
EMERALD_SOFT = "#1B7A5E"
NAVY_DEEP = "#061A2E"
NAVY = "#0B2440"

# Aksen mewah
GOLD = "#C9A227"          # base foil
GOLD_DEEP = "#8C6A1E"     # shadow foil
GOLD_MID = "#DDB44A"
GOLD_LIGHT = "#F0DCA8"    # highlight foil
GOLD_PALE = "#F8EFD6"

# Sentuhan playful & ramah
MINT = "#A8E0CD"
MINT_SOFT = "#CDEEE1"
MINT_GLOW = "#7FD0B4"
BEIGE = "#F5EDDD"
BEIGE_DEEP = "#E8DBC1"
BEIGE_WARM = "#EFE2C8"

INK = "#0E1F1A"           # teks di latar terang
INK_SOFT = "#25443B"

# --- Tipografi ----------------------------------------------------------
SERIF = "Playfair Display"
SERIF_SEMI = "Playfair Display SemiBold"
SERIF_MED = "Playfair Display Medium"
SERIF_BLACK = "Playfair Display Black"
SANS = "Montserrat"
SANS_LIGHT = "Montserrat Light"
SANS_MED = "Montserrat Medium"
SANS_SEMI = "Montserrat SemiBold"

# --- Copy (placeholder yang mudah diganti klien) ------------------------
BRAND_LINE_1 = "NAMA BANK"
BRAND_LINE_2 = "SYARIAH"
KICKER = "KALENDER MEJA  ·  EDISI 2027"
THEME_SERIF = "Tumbuh Berkah,"
THEME_SANS = "Melangkah Bersama"
YEAR = "2027"

BACK_KICKER = "KOMITMEN PELAYANAN SYARIAH"
BACK_HEAD_SERIF = "Amanah dalam Melayani,"
BACK_HEAD_SANS = "Tumbuh Bersama Anda"
BACK_BODY = [
    "Kami hadir dengan prinsip syariah yang rahmatan lil ‘alamin: transparan",
    "dalam setiap akad, adil dalam setiap nisbah, dan tumbuh bersama nasabah.",
    "Setiap produk dijalankan sesuai fatwa DSN-MUI serta diawasi OJK,",
    "sehingga berkahnya terasa nyata bagi keluarga dan usaha Anda.",
]
COPYRIGHT = "© 2027 Nama Bank Syariah  ·  Seluruh hak cipta dilindungi"
