# Kalender Meja 2027 — Versi 2 “Editorial Mihrab”

Eksperimen desain ulang oleh saya (bukan meniru file asli). Format penanggalan
tetap sama: **Masehi + Hijriah + pasaran Jawa**, ukuran **landscape 213 × 152 mm**,
tetap menyisakan **ruang ring** di sisi atas.

## 1. Arah desain yang saya pilih

Referensi rasa: *annual report* bank / majalah bisnis, bukan kalender promo.

| Keputusan | Alasan |
|---|---|
| Kertas **krem `#FBF9F4`**, bukan putih | terasa seperti kertas cetak mahal, mata tidak silau |
| **Serif (Noto Serif)** untuk angka & nama bulan | memberi wibawa korporat; angka jadi “bintang” halaman |
| **Tabel hairline** (garis 0,15 mm), bukan kartu berwarna | struktur rapi seperti laporan keuangan, tidak berisik |
| Aksen **emas `#B99154`** tipis + **hijau tua `#0C4F45`** | dua warna bank syariah, emas dipakai sangat hemat |
| Panel hijau tua + **lengkung mihrab garis emas** | identitas “syariah” tanpa perlu ornamen ramai |
| Ruang kosong dibiarkan | kesan premium; tidak semua bidang harus diisi |

Perbedaan paling mencolok dengan versi 1: tabel tanggal bergaya tipografi
(angka serif besar + pasaran kecil), rel kiri berisi identitas bulan, dan warna
merah hanya muncul sebagai aksen tipis (bukan blok).

## 2. Spesifikasi cetak

| Item | Nilai |
|---|---|
| Ukuran jadi | **213 × 152 mm** (landscape) |
| Bleed | 3 mm (file terpisah 219 × 158 mm) |
| Ruang ring | **14 mm** di sisi atas, tanpa teks |
| Lubang ring | **6 ring Ø 6 mm**, pitch **32,6 mm**, pusat 9,5 mm dari tepi atas |
| Area aman | 5 mm dari tepi potong |
| Palet | Krem `#FBF9F4` · Tinta `#10202E` · Hijau `#0C4F45` · Emas `#B99154` · Merah aksen `#A6432F` |
| Font | Noto Serif (display), Noto Sans (teks kecil), Noto Naskh/Sans Arabic |
| Semua grafis | vektor (SVG) + QR vektor |

## 3. Isi per halaman

**Sampul depan** — krem + panel hijau tua di kanan. Wordmark, label “Kalender Meja”,
angka **2027** serif 62 pt, **1448–1449 Hijriah**, tagline miring serif, identitas
bank, baris informasi (12 lembar · Masehi & Hijriah · Pasaran Jawa), dan badge OJK/LPS.
Di panel: lengkung mihrab + rosetta bintang-8 + **١٤٤٨ هـ**.

**Lembar Januari 2027** — rel kiri: `BULAN 01/12`, **Januari** (serif 24 pt), 2027,
nama bulan Arab, rentang Hijriah, konversi `1 Januari 2027 = 23 Rajab 1448 H`,
pasaran, legenda, dan QR. Kanan: tabel 7 kolom × 6 baris — angka Masehi serif,
**angka Hijriah Arab-Indik** (emas) di kanan atas, **pasaran** di kiri bawah,
tanggal libur berwarna merah + titik, puasa Ayyamul Bidh ditandai titik emas,
awal Sya’ban diberi label, tanggal bulan lain diredupkan.

**Sampul belakang** — promo **Tabungan Umroh Mitra** (6 keunggulan dengan garis
emas, kutipan serif miring), harga **Rp40.000**, WA **0813-1349-9873**, SiMIRA.
Panel kanan: **Ka’bah line-art** di dalam mihrab.

## 4. Data penanggalan (sama & tervalidasi)

- Acuan: Umm al-Qura / Kemenag RI — 1 Rajab 1448 = 10 Des 2026, 1 Sya’ban = 9 Jan 2027
- 1 Jan 2027 = **23 Rajab 1448 H · Jum’at Pon** · 5 Jan = 27 Rajab (Isra Mi’raj)
- Semua angka dihitung dari kode (`kalender_data.py`), bukan diketik manual
- QR: dibuat & diuji sendiri (`qr_code.py`, self-test Reed-Solomon lulus)

## 5. File

```
output/v2/
├─ kalender-2027-v2-bleed3mm.pdf   ← kirim ke percetakan
├─ kalender-2027-v2-trim.pdf       ← 213 × 152 mm (preview)
├─ preview-v2-1-sampul-depan.png
├─ preview-v2-2-januari-2027.png
├─ preview-v2-3-sampul-belakang.png
└─ preview-v2-panduan-ring.png     ← posisi ring & area aman
```

Build ulang: `python3 build_v2.py` (kode: `design_v2.py`, `assets_v2.py`).
Bulan lain: `design_v2.page_month(2027, 2)`.

## 6. Catatan

Logo bank, foto, dan ilustrasi masih **rekonstruksi vektor** (aset resmi belum
ada) — ganti sebelum cetak. Data alamat/telepon/WA mengikuti kalender sumber.
