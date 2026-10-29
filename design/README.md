# Kalender Meja Januari 2027 — Redesign "Playful & Rapi"

Redesign dari frame **`Kalender-Meja-Januari-2027`** (node `84:2`) di file Figma
[`PDF`](https://www.figma.com/design/QsOPwexICYv6i00y39KIce/PDF?node-id=0-1) —
versi flat, bukan yang *curved*.

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
