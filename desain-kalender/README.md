# Kalender Meja 2027 — BPR Syariah Mitra Mentari Sejahtera

Redesain kalender (format **landscape**) dengan gaya korporat bank syariah:
palet **biru – hijau – emas**, ornamen geometri Islami, penanggalan **Masehi +
Hijriah + pasaran Jawa**, dan **ruang ring jilid spiral di sisi atas**.

## 1. Spesifikasi cetak

| Item | Nilai |
|---|---|
| Ukuran jadi (trim) | **213 × 152 mm** (p 21,3 cm × l 15,2 cm), landscape |
| Bleed | 3 mm (file terpisah, total 219 × 158 mm) |
| Area ring / jilid | **15 mm** di sisi atas, bebas teks & elemen penting |
| Lubang ring | **6 ring, Ø 6 mm**, pitch **32,6 mm**, pusat lubang 9,5 mm dari tepi atas |
| Area aman isi | 6 mm dari tepi potong (atas 18 mm karena area ring) |
| Jumlah halaman | 3 halaman: sampul depan — lembar Januari 2027 — sampul belakang |
| Warna | CMYK-safe: Navy `#0A2A52` `#061C38`, Hijau `#0B6E5F` `#12886F`, Emas `#C6A15B` `#E7CE93`, Krem `#FBF7EF` |
| Font | Noto Sans (teks), Noto Sans Arabic / Noto Naskh Arabic (Hijriah) |
| Resolusi elemen | semua artwork vektor (SVG) + QR vektor → aman dicetak berapa pun DPI |

**File yang dikirim ke percetakan:** `kalender-mitra-syariah-2027-bleed3mm.pdf`
(sudah ada bleed 3 mm, cetak 100% / *actual size*, jangan *fit to page*).
`…-trim.pdf` dipakai untuk preview/digital (ukuran persis 213 × 152 mm).

## 2. Isi desain per halaman

**Halaman 1 — Sampul depan**
- Latar gradasi navy → hijau dengan pola *khatam* (bintang 8) 6%.
- Logo + wordmark “mitra syariah” / “BPR Syariah Mitra Mentari Sejahtera”.
- Angka tahun **2027** (gradasi emas) + **1448–1449 HIJRIAH**.
- Medali emas: bulan sabit, bintang, dan cartouche tahun Hijriah **١٤٤٨ هـ**.
- Tagline *Amanah · Transparan · Terjangkau* + badge OJK/LPS.

**Halaman 2 — Januari 2027** (format penanggalan mengikuti kalender asli)
- Header: logo, rentang Hijriah **RAJAB – SYA’BAN 1448 H** (Arab + Latin),
  dan keterangan `1 Januari 2027 = 23 Rajab 1448 H`.
- Blok bulan: chip **01**, judul **JANUARI 2027**, subjudul Arab.
- Grid 7 kolom (Ahad–Sabtu) × 6 baris; isi tiap sel:
  - angka Masehi (besar),
  - **angka Hijriah Arab-Indik** (mis. ٢٣) di kanan atas,
  - **pasaran Jawa** (Legi/Pahing/Pon/Wage/Kliwon) di kiri bawah,
  - penanda: Ahad & libur nasional (merah), puasa Ayyamul Bidh (titik emas),
    awal bulan Hijriah (tag “1 SYA’BAN”), tanggal bulan lalu (redup/putus-putus).
- Kolom kanan: mini kalender **Desember 2026** & **Februari 2027**, dan kartu **SCAN ME** (QR asli, mengarah ke `https://www.mitrasyariahbank.com`).
- Catatan: 2 libur nasional, ayyamul bidh, awal Sya’ban, legenda warna, kolom “Catatan”, sumber penanggalan.
- Footer legal OJK/LPS + alamat, telepon, website.

**Halaman 3 — Sampul belakang**
- Promo **Tabungan Umroh Mitra**: headline, 6 keunggulan bercentang, kutipan,
  chip **SiMIRA**, harga **Rp40.000**, dan tombol WA **0813-1349-9873**.
- Ilustrasi vektor panorama malam: masjid + Ka’bah + pesawat + bulan sabit.
- Footer legal OJK/LPS.

## 3. Sumber & validasi penanggalan

- Hijriah: **Umm al-Qura / Kemenag RI (SKB 3 Menteri)**
  - 1 Rajab 1448 H = 10 Des 2026 · 1 Sya’ban 1448 H = 9 Jan 2027
  - 1 Januari 2027 = **23 Rajab 1448 H** · 5 Januari 2027 = **27 Rajab** (Isra Mi’raj)
- Pasaran Jawa: siklus 5 hari kontinu (anchor 17 Agustus 1945 = Jum’at Legi)
  → 1 Januari 2027 = **Jum’at Pon** (sama dengan kalender sumber).
- Semua baris tanggal otomatis dari kode (`kalender_data.py`), bukan diketik manual,
  sehingga tidak ada salah hitung saat isi diubah.

## 4. Cara pakai / ubah

```bash
cd desain-kalender
python3 build.py        # menghasilkan ulang PDF + PNG di folder output/
```

- **Ganti bulan lain:** `design.page_month(2027, 2)` dst. (grid, jumlah baris,
  angka Hijriah, pasaran, dan mini kalender ikut menyesuaikan otomatis).
- **Ganti logo asli:** ganti fungsi `assets.logo_mark()` dengan file
  `logo.svg`/PNG resmi bank (taruh di `assets/`, lalu `<img>` di `wordmark()`).
- **Ganti gambar promo** (foto keluarga/Ka’bah asli): ganti `assets.kaaba_scene()`
  dengan `<img>` foto, rasio 84 × 101 mm, sudut membulat 7 mm.
- **Ganti QR:** `design._qr_card()` — cukup ubah URL di dalamnya, QR dibuat ulang.
- **Ubah warna:** konstanta warna di bagian atas `design.py` (CSS) dan `assets.py`.

## 5. Struktur file

```
desain-kalender/
├─ kalender_data.py   # Hijriah (Kemenag/Umm al-Qura), pasaran Jawa, hari libur
├─ qr_code.py         # encoder QR murni Python (ISO/IEC 18004, self-test)
├─ assets.py          # logo, pola geometri, medali, ilustrasi, ikon (SVG)
├─ design.py          # CSS + builder 3 halaman (mm presisi)
├─ build.py           # render PDF (Chromium) + preview PNG + halaman panduan
├─ README.md
└─ output/
   ├─ kalender-mitra-syariah-2027-trim.pdf      (213 × 152 mm)
   ├─ kalender-mitra-syariah-2027-bleed3mm.pdf  (219 × 158 mm) — untuk cetak
   ├─ preview-1-halaman-depan.png
   ├─ preview-2-januari-2027.png
   ├─ preview-3-halaman-belakang.png
   └─ preview-panduan-cetak-ring.png            (posisi ring & area aman)
```

## 6. Catatan aset

Logo, foto keluarga, dan foto Ka’bah pada desain ini **dibuat ulang sebagai
vektor** karena file asli belum tersedia — silakan ditukar dengan aset resmi
bank sebelum cetak. Alamat, telepon, website, dan nomor WA mengikuti data pada
kalender sumber.
