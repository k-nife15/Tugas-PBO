# Kalender Meja Januari 2027 — 2 Varian Redesign

Redesign dari frame **`Kalender-Meja-Januari-2027`** (node `84:2`) di file Figma
[`PDF`](https://www.figma.com/design/QsOPwexICYv6i00y39KIce/PDF?node-id=0-1) —
versi flat, bukan yang *curved*.

| Varian | Karakter | File utama |
|---|---|---|
| **Playful & Rapi** | pastel, sticker miring, doodle, warna ceria | `kalender-januari-2027-playful.svg` |
| **Elegan · Islami · Business** | serif Marcellus, antique gold, panel mihrab, khatim 8 sudut, tabel garis rambut | `kalender-januari-2027-elegan.svg` |
| **Biru–Hijau–Emas · 3 Penanggalan** | 21,3 × 15,2 cm, slot foto promo, Masehi + Hijriah + Jawa per sel | `kalender-2027-biru-hijau-emas.svg` |

## Varian 3 — Biru–Hijau–Emas (ukuran cetak 21,3 × 15,2 cm)

Kanvas **2130 × 1520 px @ 10 px/mm = 21,3 × 15,2 cm** (254 dpi), landscape.

| Isi | Detail |
|---|---|
| **Slot foto promo** | bingkai emas ganda 750×454 px (≈ 7,5 × 4,5 cm) + kurung sudut + ribbon "PROGRAM UMROH 2027" + fade navy agar teks terbaca |
| **Kalender 3 lapis** | angka besar = **Masehi**; `H 22 Rajab` = **Hijriah**; `J 22 Rejeb · Pon` = **Jawa + pasaran** |
| **Kepala bulan** | "JANUARI" (Marcellus) + badge emas **2027** + `RAJAB – SYA'BAN 1448 H` · `REJEB – RUWAH 1960 DAL` + medali "01 BULAN" |
| **Palet** | navy `#0B2E4F`, biru `#12557F`, hijau `#0D6B4F`, emas `#B58A2B` / `#D4AF37`, kertas krem `#FAF7F0` |
| **Penghias (ramai tapi rapi)** | pita gradasi biru→hijau di tepi atas & kepala tiap kartu, bingkai ganda emas, khatim di 4 sudut, watermark khatim di belakang judul, garis emas + permata, chip hari berwarna, zebra baris, tint sel libur/puasa, penanda khatim/permata, legenda M–H–J, 3 kartu catatan beraksen, footer legal + kontak |

**Ganti / kosongkan foto:** taruh berkas di `assets/foto-promo.png`. Untuk versi
tanpa foto (slot kosong bergaris putus-putus + label "FOTO PROMOSI"), set
`PHOTO_PLACEHOLDER = True` di `generate_tiga_kalender.py` — nama berkas keluarannya
menjadi `kalender-2027-biru-hijau-emas-placeholder.*`.

**Catatan akurasi Jawa:** penomoran hari Jawa di sini = Hijriah (hisab), bulan Jawa
memakai padanan Sultan Agung (Rajab→Rejeb, Sya'ban→Ruwah), tahun Jawa = Hijriah + 512
(1448 H → 1960), dan nama tahun dari windu 8 tahunan (`1960 = Dal`). Kalender Jawa
Sultan Agung resmi bisa berselisih ±1 hari pada tahun-tahun tertentu; jika perlu
presisi rukyat, sesuaikan tabel di `generate_tiga_kalender.py`.


## Output (`dist/`)

| Pola nama | Keterangan |
|---|---|
| `*-playful.svg` / `*-elegan.svg` | **Master vektor**. Drag & drop ke Figma → jadi layer editable |
| `*@2x.png` | 1588×1118 — preview layar |
| `*@4x.png` | 3176×2236 — 384 dpi |
| `*-print.pdf` | Siap cetak (A5 210×148 mm untuk varian 1–2, 213×152 mm untuk varian 3) |
| `*-data.json` | Data 42 sel (tanggal, Hijriah, pasaran) untuk verifikasi |

Kanvas 794×559 px = **A5 landscape @96 dpi**.

## Cara regenerate

```bash
cd design
python3 -m pip install --user --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow
npm install                 # @resvg/resvg-js (renderer SVG, tanpa browser)
python3 generate.py                # playful        -> SVG + JSON
python3 generate_elegant.py        # elegan         -> SVG + JSON
python3 generate_tiga_kalender.py  # 3 penanggalan  -> SVG + JSON
node render.mjs                    # semua SVG -> PNG (1x/2x, +4x utk kanvas kecil)
python3 export_pdf.py              # PNG master -> PDF ukuran fisik asli
```

`common.py` adalah satu-satunya sumber untuk **data tanggal** (Hijriah + pasaran),
registry font, dan primitif SVG — supaya kedua varian tidak pernah berbeda data.

## Varian 2 — Elegan · Islami · Business

**Prinsipnya: kemewahan dari presisi, bukan dari hiasan.** Semua ornamen dibuat
dari geometri (bukan ilustrasi): khatim 8 sudut di 4 sudut bingkai, pattern khatim
sebagai watermark kertas, panel mihrab lancip di kartu promo, dan garis rambut emas
sebagai pemisah.

- **Tipografi** — Marcellus (serif Romawi) untuk kata, Lato 400/700/800 untuk teks
  kecil dan **semua angka**. Ini bukan pilihan estetis semata: Marcellus memakai
  *old-style figures*, sehingga "10" tampil seperti "IO" dan "2027" seperti "2O27" —
  tidak boleh untuk kalender. Karena itu angka dialihkan ke Lato (lining figures).
- **Warna** — kertas krem `#F7F3EA`, navy `#0F2540`, emerald `#0B5D45`,
  antique gold `#B08D3F`, garis `#E4DCC9`.
- **Tabel kalender** — bukan kartu-kartu, tapi tabel bergaris rambut 0,7 px dengan
  kolom 61,43 px dan baris 43 px; Ahad gold, Jum'at emerald, tanggal bulan lain abu.
- **Penanda** — libur: sel bertint emerald + angka emerald + permata emas;
  puasa sunnah: tint krem-emas; tanpa ikon kartun.
- Sudut pandang "business": bingkai ganda khas dokumen resmi, tracking lebar pada
  label kecil (2,4 px), dan blok legal OJK/LPS + kontak di kaki halaman.

## Varian 1 — Playful & Rapi

**Playful** — sticker harga & badge `01 BULAN` dimiringkan 4°, sparkle, blob pastel,
dot pattern, accent bar warna pada kartu info, doodle ka'bah → pesawat.
**Rapi** — grid 7×6 dengan kolom 57,71 px dan gap 5 px identik, radius seragam
(20 kartu / 11 sel / 999 pill), satu keluarga font (Poppins 400–800), dan semua
posisi teks dihitung dari metrik font — bukan tebakan.

### Design token
```
ink        #0B1B3F     paper      #FFFCF6     card     #FFFFFF
blue       #0052CC     blue-soft  #E8F1FF     line     #E7EEF9
emerald    #059669     emerald-soft #E6F8F1
gold       #FBBF24     gold-dark  #D97706     gold-soft #FFF6DE
rose       #E11D48     rose-soft  #FFEDF1
violet     #7C3AED     violet-soft #F3ECFF
```

### Pola warna tanggal (playful)
- **Ahad** → angka rose, header pill rose
- **Jum'at** → angka emerald, header pill emerald
- **Sabtu** → angka blue, header pill blue
- **Libur nasional** → sel penuh rose, angka putih + titik putih
- **Puasa sunnah** (22–24 Jan) → sel gold-soft, angka gold-dark + titik gold
- **Tanggal bulan lain** → sel abu terang, angka `#AEBACE`

## Catatan data (berlaku untuk kedua varian)

Tanggal Hijriah & pasaran dihitung ulang, bukan disalin. Hasil verifikasi:

1. **Pasaran & Hijriah Januari sudah benar** di desain lama (1 Jan = 22 Rajab 1448 H /
   Pon; 22 Jan = 13 Sya'ban 1448 H — konsisten dengan catatan Ayyamul Bidh 13–15 Sya'ban).
2. **Sel ekor Desember di desain lama salah** — tertulis `23 Wage … 27 Pon` untuk
   27–31 Des 2026. Yang benar: `17 Pon, 18 Wage, 19 Kliwon, 20 Legi, 21 Pahing`.
   Sudah diperbaiki di kedua varian.
3. **Isra' Mi'raj**: desain lama menulis **5 Jan**, padahal 27 Rajab 1448 H jatuh pada
   **6 Januari 2027** (kalender hisab; 27 Rajab 1447 H = 16 Jan 2026 + 354 hari).
   Kedua varian memakai 6 Jan — ubah `HOLIDAY_SET`/`HOLIDAYS` bila ingin tetap 5 Jan.
4. Typo yang diperbaiki: `Kelolaanya` → `Kelolaannya`, `Isra` → `Isra'`.
5. Label `Bush L` / `Bush T` pada versi curved tidak dipakai karena maknanya tidak jelas
   di file sumber — silakan beri definisi bila ingin ditampilkan.
6. Kedua varian tidak memakai skrip Arab: resvg di sini tidak melakukan shaping Arab
   dengan benar, jadi ornamen dibuat murni geometris agar tidak ada kaligrafi yang salah.

## Sumber aset

- Logo `assets/logo-brand.png` — hasil render node `84:4` (logo asli BPRS) dari file Figma.
- Font: Poppins, Marcellus, Lato — Google Fonts (OFL), ada di `assets/fonts/`.


## Output (`dist/`)

| File | Keterangan |
|---|---|
| `kalender-januari-2027-playful.svg` | **Master vektor**. Drag & drop ke Figma → jadi layer editable |
| `kalender-januari-2027-playful@2x.png` | 1588×1118 — preview layar |
| `kalender-januari-2027-playful@4x.png` | 3176×2236 — 384 dpi |
| `kalender-januari-2027-playful-A5.pdf` | Siap cetak, 210×148 mm (A5 landscape) |
| `kalender-januari-2027-data.json` | Data 42 sel (tanggal, Hijriah, pasaran) untuk verifikasi |

Kanvas 794×559 px = **A5 landscape @96 dpi**.

## Cara regenerate

```bash
cd design
python3 -m pip install --user --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow
npm install                 # @resvg/resvg-js (renderer SVG, tanpa browser)
python3 generate.py         # SVG + JSON
node render.mjs             # PNG 1x/2x/4x
python3 export_pdf.py       # PDF A5
```

## Keputusan desain

**Playful** — sticker harga & badge `01 BULAN` dimiringkan 4°, sparkle, blob pastel,
dot pattern di kertas, accent bar warna pada kartu info, doodle ka'bah → pesawat.
**Rapi** — kunci kerapiannya justru disiplin: grid 7×6 kolom dengan lebar kolom
57,71 px dan gap 5 px yang identik, radius seragam (20 kartu / 11 sel / 999 pill),
satu keluarga font (Poppins 400–800), dan semua posisi teks dihitung dari metrik
font — bukan tebakan.

### Design token
```
ink        #0B1B3F     paper      #FFFCF6     card     #FFFFFF
blue       #0052CC     blue-soft  #E8F1FF     line     #E7EEF9
emerald    #059669     emerald-soft #E6F8F1
gold       #FBBF24     gold-dark  #D97706     gold-soft #FFF6DE
rose       #E11D48     rose-soft  #FFEDF1
violet     #7C3AED     violet-soft #F3ECFF
radius  20 (kartu) · 11 (sel) · 12 (info) · 999 (pill)
font    Poppins 400/500/600/700/800
```

### Pola warna tanggal
- **Ahad** → angka rose, header pill rose
- **Jum'at** → angka emerald, header pill emerald
- **Sabtu** → angka blue, header pill blue
- **Libur nasional** → sel penuh rose, angka putih + titik putih
- **Puasa sunnah** (22–24 Jan) → sel gold-soft, angka gold-dark + titik gold
- **Tanggal bulan lain** → sel abu terang, angka `#AEBACE`

## Catatan data (penting)

Tanggal Hijriah & pasaran dihitung ulang, bukan disalin. Hasil verifikasi:

1. **Pasaran & Hijriah Januari sudah benar** di desain lama (1 Jan = 22 Rajab 1448 H /
   Pon; 22 Jan = 13 Sya'ban 1448 H — konsisten dengan catatan Ayyamul Bidh 13–15 Sya'ban).
2. **Sel ekor Desember di desain lama salah** — tertulis `23 Wage … 27 Pon` untuk
   27–31 Des 2026. Yang benar: `17 Pon, 18 Wage, 19 Kliwon, 20 Legi, 21 Pahing`.
   Sudah diperbaiki di versi ini.
3. **Isra' Mi'raj**: desain lama menulis **5 Jan**, padahal 27 Rajab 1448 H jatuh pada
   **6 Januari 2027** (kalender hisab; 27 Rajab 1447 H = 16 Jan 2026 + 354 hari).
   Versi ini memakai 6 Jan — ubah `HOLIDAYS` di `generate.py` bila ingin tetap 5 Jan.
4. Typo yang diperbaiki: `Kelolaanya` → `Kelolaannya`, `Isra` → `Isra'`,
   `do'a`/`nyata` diberi tanda baca konsisten.
5. Label `Bush L` / `Bush T` pada versi curved tidak dipakai karena maknanya tidak jelas
   di file sumber — silakan beri definisi bila ingin ditampilkan.

## Sumber aset

- Logo `assets/logo-brand.png` — hasil render node `84:4` (logo asli BPRS) dari file Figma.
- Font Poppins — Google Fonts (OFL), ada di `assets/fonts/`.
