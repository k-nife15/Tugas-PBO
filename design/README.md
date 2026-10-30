# Kalender Meja Januari 2027 — Corporate Elegant (21,3 × 15,2 cm)

Kalender meja **BPRS Mitra Mentari Sejahtera**, landscape, **dasar putih bersih**,
dengan tiga sistem penanggalan dalam setiap sel (**Masehi · Hijriah · Jawa**),
slot foto promosi, dan aksen **biru – hijau — emas** yang dipakai terkendali.

Konsep: **corporate elegant** — rapi, tegas, dan lapang. Struktur dibentuk oleh
blok warna, garis rambut, dan label small-caps (bukan ornamen ramai).

Desain ini diturunkan dari frame `Kalender-Meja-Januari-2027` (node `84:2`) di file
Figma [`PDF`](https://www.figma.com/design/QsOPwexICYv6i00y39KIce/PDF?node-id=0-1),
lalu digambar ulang penuh (bukan sekadar skala dari desain lama).

## Output (`dist/`)

| File | Isi |
|---|---|
| `kalender-2027-biru-hijau-emas.svg` | **Master vektor** 2130×1520 — drag & drop ke Figma jadi layer editable (kecuali teks Arab, lihat catatan) |
| `kalender-2027-biru-hijau-emas@2x.png` | 4260×3040 px (508 dpi) — preview / percetakan digital |
| `kalender-2027-biru-hijau-emas-print.pdf` | **213 × 152 mm**, 508 dpi — siap cetak |
| `kalender-2027-biru-hijau-emas-data.json` | Data 42 sel: Masehi, Hijriah, Jawa, pasaran, nama tahun Jawa |

## Spesifikasi

| Aspek | Nilai |
|---|---|
| Ukuran jadi | **21,3 × 15,2 cm** (landscape) |
| Kanvas | 2130 × 1520 px @ **10 px/mm** (254 dpi) |
| Font | Marcellus (judul), Lato (teks & angka), Noto Naskh Arabic (teks Arab) |
| Warna | dasar **putih `#FFFFFF`**; navy `#0B2E4F`, biru `#12557F`, hijau `#0D6B4F`, emas `#B58A2B` / `#D4AF37`, garis rambut `#E3E7EE` |
| Slot foto | 7,5 × 4,5 cm — bingkai gradasi biru→hijau + garis emas ganda, kurung sudut, ribbon "PROGRAM UMROH 2027" |
| Kalender | angka besar = Masehi · **٢٢ رجب** = Hijriah · `J 22 Rejeb · Pon` = Jawa + pasaran |
| Nama hari | dwibahasa: `AHAD` + **الأحد** … `SABTU` + **السبت** |
| Struktur | blok judul navy + garis emas, pita tiga warna biru–hijau–emas di kepala halaman, tabel bergaris rambut, kepala tabel biru muda, baris zebra |
| Ornamen (arabesque) | bingkai halaman + **arabesque sudut** (busur ganda, khatim, curl, daun), **medali khatim** di tengah atas foto, pita khatim pada strip foto & dasar blok navy, **pembatas vertikal bermedali** di antara kolom, pembatas flourish di kaki halaman, permata pada kartu catatan, watermark khatim di blok navy |

## Cara regenerate

```bash
cd design
python3 -m pip install --user --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow uharfbuzz fonttools
npm install                     # @resvg/resvg-js (renderer SVG, tanpa browser)
python3 generate.py             # SVG + JSON
node render.mjs                 # PNG 1x & 2x
python3 export_pdf.py           # PDF 213 × 152 mm
```

| Berkas | Peran |
|---|---|
| `generate.py` | seluruh komposisi desain (satu sumber kebenaran untuk layout) |
| `common.py` | primitif SVG, registry font, dan **perhitungan Hijriah + pasaran Jawa** |
| `arabic.py` | shaper Arab: HarfBuzz → outline glyph → `<path>` SVG |
| `render.mjs` | resvg: SVG → PNG |
| `export_pdf.py` | PNG → PDF dengan ukuran fisik asli |

## Teks Arab (penting)

Renderer `resvg` tidak melakukan shaping kompleks, jadi teks Arab **tidak** bisa
dirender sebagai `<text>`. Semua teks Arab di sini di-shape dengan **HarfBuzz**
(`uharfbuzz`) lalu dikonversi menjadi `<path>`:

- Huruf tersambung sesuai kaidah (initial/median/final), harakat menempel benar.
- **Angka Arab-Indik tetap LTR** di dalam kalimat RTL → `٢٢ رجب`, bukan `رجب ٢٢`.
- Konsekuensi: di Figma, teks Arab menjadi vektor (tidak bisa diketik ulang).
  Bila butuh yang editable, ketik langsung di Figma (Figma punya shaper Arab sendiri).

## Ganti / kosongkan foto

- Ganti foto: timpa `assets/foto-promo.png` (rasio mendekati 1,7 : 1), lalu regenerate.
- Slot kosong: set `PHOTO_PLACEHOLDER = True` di `generate.py` → keluaran bernama
  `kalender-2027-biru-hijau-emas-placeholder.*` (kotak garis putus-putus + label).

## Data & akurasi

Tanggal dihitung, bukan disalin:

1. **Hijriah** — algoritma tabular (Kuwaiti), teruji: `2026-01-16 → 1447-07-27`
   (Isra' Mi'raj 1447 H) dan `2027-01-01 → 1448-07-22`.
2. **Jawa** — penomoran hari = Hijriah (hisab), nama bulan padanan Sultan Agung
   (Rajab→Rejeb, Sya'ban→Ruwah), tahun Jawa = Hijriah + 512 (1448 H → **1960**),
   nama tahun dari windu 8 tahunan (**1960 = Dal**). Kalender Jawa Sultan Agung
   resmi bisa berselisih ±1 hari; sesuaikan bila perlu presisi rukyat.
3. **Pasaran** — daur 5 hari dengan acuan baku 17 Agustus 1945 = Jumat Legi.
4. **Koreksi terhadap desain lama**: sel ekor Desember yang salah (`23 Wage … 27 Pon`)
   diperbaiki menjadi `17 Pon, 18 Wage, 19 Kliwon, 20 Legi, 21 Pahing`; Isra' Mi'raj
   dipakai **6 Januari 2027** (27 Rajab 1448 H), bukan 5 Januari. Typo
   `Kelolaanya` → `Kelolaannya`, `Isra` → `Isra'`.
5. Label `Bush L` / `Bush T` dari versi *curved* tidak dipakai karena maknanya tidak
   jelas di file sumber.

## Riwayat

Eksplorasi awal (varian "playful" dan "elegan–islami–business" pada kanvas A5 794×559)
sudah **dihapus** dari repo agar tidak membingungkan. Bila suatu saat diperlukan,
masih bisa diambil dari riwayat git: commit `ab55481` (playful) dan `ac3dec3` (elegan).
