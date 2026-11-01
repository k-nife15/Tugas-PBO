# 03 · Spesifikasi Teknis Cetak

## 3.1 Dimensi

| Item | Nilai | Catatan |
|---|---|---|
| Ukuran jadi (trim) | **213 × 152 mm** landscape | panjang 21,3 cm × lebar 15,2 cm |
| Area aman konten | atas **15 mm**, kiri/kanan/bawah **12 mm** | 15 mm atas = zona jilid Wire-O |
| Bleed | **3 mm** tiap sisi | total berkas 219 × 158 mm |
| Margin optis judul | 15 mm dari tepi kiri | sejajar logo, memberi "dinding" kiri |
| Toleransi potong | ± 0,5 mm | komposisi dibuat tahan geser 1 mm |

## 3.2 Jilid Wire-O (twin loop) — sisi atas

| Parameter | Nilai rekomendasi |
|---|---|
| Pitch | **3:1** (3 lubang per inci) → jarak antar lubang **8,47 mm** |
| Jumlah lubang | **23** lubang sepanjang 213 mm (lubang pertama 13,35 mm dari tepi kiri) |
| Diameter lubang | **4,5–4,8 mm** (untuk wire Ø 3/8" / 9,5 mm) |
| Jarak as lubang dari tepi atas | **4,8 mm** |
| Diameter wire | **9,5 mm (3/8")** untuk tebal buku ± 8–12 mm |
| Material wire | *nylon coated* — hitam matte (netral) atau gold (senada foil) |
| Orientasi | **di sisi panjang atas** (landscape, gantung ke bawah) |

Safety margin 15 mm dipilih karena: 4,8 mm (as lubang) + 4,8 mm (radius
lengkung wire di dalam blok) + ± 5 mm ruang bernapas visual = 14,6 mm → dibulatkan 15 mm.
Tidak ada teks, logo, QR, atau garis penting di dalam pita ini.

Opsi penopang meja:

1. **Easel back** — *greyboard* 1,5 mm direkatkan di belakang cover belakang,
   dilipat menjadi kaki segitiga. Paling umum, paling murah.
2. **A-frame / tent** — dua panel kaku dengan wire di puncak, membentuk "Λ".
   Lebih premium, memakan ruang meja lebih besar.

Rekomendasi untuk brand korporat: **easel back** dengan tinggi bukaan 55–60°.

## 3.3 Material

| Bagian | Bahan | Gramatur | Alasan |
|---|---|---|---|
| Cover depan & belakang | Ivory/matte art card (mis. Concorde Ivory, Sirio Color, Matte Art Card) | **300–350 gsm** | menerima foil & spot UV dengan baik, tidak melengkung |
| Isi (12 halaman bulanan) | Art paper / matte | **150 gsm** | tidak terlalu berat untuk wire 9,5 mm, mudah dibuka |
| Penopang (easel back) | Greyboard | **1,5 mm** | kaku, tidak melengkung di iklim lembap |
| Halaman catatan (opsional) | Uncoated | 120 gsm | nyaman ditulisi |

Tebal blok total (cover 2 × 0,4 + isi 14 × 0,15 + board 1,5) ≈ **4,5–5 mm** →
wire Ø 9,5 mm masih aman (memberi ruang buka yang lega).

## 3.4 Grid & modul

- **Grid dasar**: 12 kolom, lebar kolom 11,83 mm, gutter 4 mm, pada area aman
  186 mm.
- **Baseline**: kelipatan 2,7 mm (setengah dari leading body 5,4 mm).
- **Kisi informasi (cover belakang)**: 4 kolom × 46,5 mm, garis pemisah
  0,24 pt mulai 3 mm di bawah garis atas kisi.
- **Kisi tanggal (halaman dalam)**: 7 kolom × 26,4 mm, 6 baris × 20 mm.

## 3.5 Persiapan berkas (pre-press checklist)

1. **Mode warna**: CMYK untuk semua elemen proses. Warna RGB di artwork ini
   (`#0E5241` dsb.) sudah disertai padanan CMYK di `01-konsep-visual.md`.
2. **Spot channel**: buat dua *spot color* terpisah —
   `FOIL_GOLD` (100% tint) dan `SPOT_UV` (100% tint). Semua elemen foil/UV
   diletakkan di layer sendiri, di atas artwork, dengan nama channel tersebut.
3. **Overprint**: set *overprint fill* pada elemen foil agar warna di bawahnya
   tidak "knock-out" (menghindari garis putih akibat meleset register).
4. **Rich black** untuk bidang gelap besar: C60 M50 Y40 K100 (total ink ≤ 300%).
   Jangan memakai 100K saja untuk emerald gelap — akan terlihat kehijauan kusam.
5. **Ketebalan garis minimum**: 0,25 pt (0,09 mm) untuk proses cetak;
   0,18 pt hanya boleh untuk foil/spot.
6. **Teks**: minimal 4 pt; semua teks di-*outline* pada file final
   (simpan juga versi ber-font untuk revisi).
7. **Resolusi gambar/efek**: 300 dpi pada ukuran final; hindari raster untuk
   garis emas (gunakan vektor agar tidak bergerigi saat foil).
8. **Format kirim**: PDF/X-4 + file AI/PDF berlapis (layer: `ARTWORK`,
   `FOIL_GOLD`, `SPOT_UV`, `DIELINE`).
9. **Helah (dieline)**: sertakan dieline punch Wire-O 23 lubang, posisi as
   4,8 mm dari tepi atas.
10. **Proof**: minta *hard proof* (bukan soft proof) untuk mengecek emerald
    gelap, gradasi foil, dan hasil *soft-touch* + spot UV.

## 3.6 Toleransi register antar-finishing

| Pasangan | Toleransi aman | Cara mengamankan |
|---|---|---|
| Foil ↔ cetak emerald | ± 0,2 mm | foil dibuat 1–2% *choke* (garis foil sedikit lebih tebal dari garis cetak) |
| Spot UV ↔ artwork | ± 0,3 mm | UV diletakkan di dalam bidang, jangan menyentuh tepi tajam |
| Potong ↔ artwork | ± 0,5 mm | jaga elemen penting ≥ 3 mm dari trim |
| Punch Wire-O ↔ artwork | ± 0,5 mm | pita 15 mm kosong sudah memberi ruang lebih |

## 3.7 Urutan produksi

1. Proof digital & persetujuan copy legal (OJK/LPS, nomor call center).
2. Cetak CMYK 4 warna cover (depan-belakang) + isi.
3. Laminasi *soft-touch matte* dua sisi cover (lihat `04-finishing-produksi.md`).
4. Hot foil stamping (Gold) pada area bertanda.
5. Spot UV glossy pada motif geometri & logo.
6. Emboss/deboss logo (opsional, 1 die).
7. Potong (guillotine/die-cut), sudut 0 mm siku atau radius 4 mm (opsional).
8. Punch 23 lubang + jilid Wire-O.
9. Rekat easel back, lipat, QC, *shrink wrap* + sleeve.

## 3.8 QC sebelum kirim

- [ ] Cek 15 mm pita jilid benar-benar kosong di **semua** halaman.
- [ ] Cek QR dapat dipindai dari jarak 20 cm (uji 3 ponsel berbeda).
- [ ] Cek teks 3,9–4 pt masih terbaca (bukan "blob") setelah laminasi.
- [ ] Cek foil tidak pecah di area garis hairline lengkung.
- [ ] Cek warna emerald konsisten antara cover depan & belakang (satu *run*).
- [ ] Cek wire tidak menggores cover depan saat dibuka-tutup 20×.
- [ ] Cek logo OJK/LPS utuh, tidak terpotong, dan kalimat penjaminan sesuai.
