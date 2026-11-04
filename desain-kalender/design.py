"""CSS + builder halaman kalender (ukuran final 213 x 152 mm landscape)."""

from __future__ import annotations

import assets as A
import kalender_data as K

W, H = 213.0, 152.0   # mm, ukuran jadi (trim)
BAND = 15.0           # ruang ring / jilid spiral di sisi atas
FOOT = 9.0

CSS = """
@page { size: @@PWPT@@pt @@PHPT@@pt; margin: 0 }
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;padding:0;background:#fff;font-family:'Noto Sans',Arial,sans-serif;color:#0D1B2A}
.page{position:relative;width:@@PW@@mm;height:@@PH@@mm;overflow:hidden;background:#fff;
      page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}
.frame{position:absolute;left:@@PAD@@mm;top:@@PAD@@mm;width:@@W@@mm;height:@@H@@mm}
.pat{pointer-events:none}

/* ---------- band ring (area jilid spiral) ---------- */
.band{position:absolute;left:-@@PAD@@mm;right:-@@PAD@@mm;top:-@@PAD@@mm;
      height:calc(@@BAND@@mm + @@PAD@@mm);overflow:hidden;
      background:linear-gradient(100deg,#061C38 0%,#0A2E5C 38%,#0C4A5E 68%,#0B6E5F 100%)}
.band:after{content:'';position:absolute;left:0;right:0;bottom:0;height:.55mm;
      background:linear-gradient(90deg,rgba(198,161,91,0),#C6A15B 20%,#F3E2B4 50%,#C6A15B 80%,rgba(198,161,91,0))}
.band .bandlbl{position:absolute;left:7mm;bottom:1.9mm;font-size:3.4pt;letter-spacing:.6mm;
      color:rgba(255,255,255,.55);font-weight:700}
.band .bandyr{position:absolute;right:7mm;bottom:1.4mm;font-size:6.6pt;letter-spacing:.5mm;
      font-weight:700;color:#E7CE93}

/* ---------- tipografi umum ---------- */
.wordmark{display:flex;align-items:center;gap:2mm}
.wm-txt{line-height:1}
.wm-top{font-size:3.5pt;letter-spacing:.42mm;font-weight:700}
.wm-name{font-size:11pt;font-weight:700;letter-spacing:-.15mm;margin-top:.35mm}
.wm-sub{font-size:3.3pt;letter-spacing:.28mm;margin-top:.45mm;font-weight:600}
.eyebrow{font-size:4.4pt;font-weight:700;letter-spacing:1.1mm;text-transform:uppercase}
.sec{display:flex;align-items:center;gap:1.6mm;font-size:4.3pt;font-weight:700;
     letter-spacing:.55mm;text-transform:uppercase;color:#8E6F2E}
.sec:after{content:'';flex:1;height:.2mm;
     background:linear-gradient(90deg,#E7CE93,rgba(231,206,147,0))}
.rule{height:.35mm;background:linear-gradient(90deg,#C6A15B,#F3E2B4 30%,rgba(198,161,91,0))}
.ico{display:block}

/* ---------- header bulan ---------- */
.hijri{position:absolute;right:7mm;top:16.4mm;text-align:right;line-height:1.15}
.hijri .h1{font-size:7.2pt;font-weight:700;letter-spacing:.35mm;color:#0A2A52}
.hijri .h2{font-size:4.2pt;letter-spacing:.3mm;color:#6C8093;font-weight:600;margin-top:.5mm}
.hijri .h3{font-family:'Noto Naskh Arabic';font-size:10.5pt;color:#A9822F;margin-top:.6mm}

.mrow{position:absolute;left:7mm;top:32.6mm;height:18mm;display:flex;align-items:center;gap:3.2mm}
.chip{width:13.6mm;height:13.6mm;border-radius:2.6mm;flex:0 0 auto;
      background:linear-gradient(150deg,#12507F,#0A2A52);border:.35mm solid rgba(198,161,91,.6);
      display:flex;align-items:center;justify-content:center;color:#E7CE93;
      font-size:13.5pt;font-weight:700;letter-spacing:.3mm;
      box-shadow:0 .5mm 1.4mm rgba(10,42,82,.25)}
.mname{line-height:1}
.mname .n{font-size:23pt;font-weight:700;letter-spacing:1mm;color:#0A2A52}
.mname .y{font-size:11pt;font-weight:700;letter-spacing:.4mm;color:#C6A15B;margin-left:1.6mm}
.mname .ar{font-family:'Noto Naskh Arabic';font-size:9pt;color:#8E6F2E;margin-top:.9mm;letter-spacing:.2mm}

/* ---------- header hari ---------- */
.wk{position:absolute;left:7mm;top:52.6mm;width:168mm;display:grid;
    grid-template-columns:repeat(7,1fr);gap:1.4mm}
.wk span{height:5.6mm;display:flex;align-items:center;justify-content:center;
    font-size:4.5pt;font-weight:700;letter-spacing:.32mm;color:#fff;border-radius:1.2mm;
    background:linear-gradient(180deg,#12507F,#0A2A52)}
.wk .sun{background:linear-gradient(180deg,#A13647,#7C2534)}
.wk .sat{background:linear-gradient(180deg,#12886F,#0B6E5F)}

/* ---------- grid tanggal ---------- */
.grid{position:absolute;left:7mm;top:59.4mm;width:168mm;height:59.6mm;display:grid;
      grid-template-columns:repeat(7,1fr);grid-template-rows:repeat(5,1fr);gap:1.4mm}
.cell{position:relative;border-radius:1.5mm;background:#fff;border:.22mm solid #DCE6EE;
      overflow:hidden}
.cell .d{position:absolute;left:1.8mm;top:1.1mm;font-size:14.6pt;font-weight:700;line-height:1;color:#0A2A52}
.cell .h{position:absolute;right:1.6mm;top:1.6mm;font-family:'Noto Sans Arabic';font-size:6.6pt;
      color:#12886F;font-weight:600}
.cell .p{position:absolute;left:1.8mm;bottom:1mm;font-size:3.9pt;font-weight:700;letter-spacing:.28mm;
      text-transform:uppercase;color:#93A3B3}
.cell.sun{background:#FFF8F7;border-color:#F3D6D1}
.cell.sun .d{color:#B23A48}
.cell.hol{background:linear-gradient(160deg,#FFF4F2,#FFE7E3);border-color:#EEBDB4}
.cell.hol .d{color:#B23A48}
.cell.hol:before{content:'';position:absolute;left:0;top:0;bottom:0;width:.85mm;background:#B23A48}
.cell.fri .p{color:#A9822F}
.cell.out{background:transparent;border:.22mm dashed #E6ECF2}
.cell.out .d{color:#C6D1DC;font-weight:600}
.cell.out .h{opacity:.3}
.cell.bidh:after{content:'';position:absolute;right:1.8mm;bottom:1.4mm;width:1.25mm;height:1.25mm;
      border-radius:50%;background:#C6A15B}
.cell .tag{position:absolute;right:1.3mm;bottom:1.05mm;font-size:3.2pt;font-weight:700;
      letter-spacing:.14mm;color:#8E6F2E;background:#FBF3DF;border:.15mm solid #E7CE93;
      border-radius:.7mm;padding:.2mm .65mm}

/* ---------- catatan bawah ---------- */
.notes{position:absolute;left:7mm;top:121mm;width:168mm}
.note{display:flex;gap:1.3mm;align-items:flex-start;font-size:4.15pt;color:#3A4E62;
      line-height:1.35;margin-top:1.05mm}
.note .b{font-weight:700;color:#B23A48;flex:0 0 auto}
.note .i{color:#12886F;font-weight:700;flex:0 0 auto}
.note .g{font-weight:600;color:#8E6F2E;flex:0 0 auto}
.catat{margin-top:1.7mm;font-size:4pt;color:#6C8093;display:flex;align-items:baseline;gap:1.4mm}
.catat .ln{flex:1;border-bottom:.2mm dotted #C6D1DC;height:2.4mm}

/* ---------- rail kanan: kalender mini + QR ---------- */
.rail{position:absolute;left:178.4mm;top:59.4mm;width:27.6mm}
.mini{border:.22mm solid #DCE6EE;border-radius:1.5mm;padding:1.1mm .9mm .9mm;background:#fff}
.mini.m2{margin-top:2mm}
.mini .mt{font-size:3.9pt;font-weight:700;letter-spacing:.22mm;text-align:center;color:#0A2A52;
     margin-bottom:.55mm}
.mini table{width:100%;border-collapse:collapse;table-layout:fixed}
.mini th{font-size:3.1pt;font-weight:700;color:#A9822F;text-align:center;padding:0 0 .3mm}
.mini td{font-size:3.4pt;text-align:center;color:#4A5C6E;padding:.1mm 0}
.mini td.su{color:#B23A48}
.mini td.e{color:#CBD5DF}
.qr{margin-top:2mm;border:.22mm solid #DCE6EE;border-radius:1.5mm;padding:1.2mm 1mm 1mm;
    background:linear-gradient(160deg,#FFFFFF,#F6FAF8);text-align:center}
.qr .qt{font-size:3.7pt;font-weight:700;letter-spacing:.35mm;color:#0B6E5F;margin-bottom:.9mm}
.qr svg{display:block;margin:0 auto;background:#fff}
.qr .qu{font-size:3.1pt;color:#6C8093;margin-top:.8mm;letter-spacing:-.02mm}

/* ---------- footer legal ---------- */
.foot{position:absolute;left:-@@PAD@@mm;right:-@@PAD@@mm;bottom:-@@PAD@@mm;
      height:calc(@@FOOT@@mm + @@PAD@@mm);overflow:hidden;
      background:linear-gradient(90deg,#071F3A,#0A2E5C 48%,#0B6E5F);color:#fff;
      display:flex;align-items:center;justify-content:space-between;
      padding:0 7mm;gap:4mm}
.foot:before{content:'';position:absolute;left:0;right:0;top:0;height:.35mm;
      background:linear-gradient(90deg,rgba(198,161,91,0),#C6A15B 22%,#F3E2B4 50%,#C6A15B 78%,rgba(198,161,91,0))}
.foot .fc{font-size:3.5pt;line-height:1.5;opacity:.92;max-width:96mm}
.foot .fr{display:flex;align-items:center;gap:3.2mm;font-size:3.5pt;line-height:1.5}
.foot .fr .k{display:flex;align-items:center;gap:.9mm}
.foot .fr svg{width:2.6mm;height:2.6mm;opacity:.95}
.foot b{color:#F3E2B4;font-weight:700}

/* ---------- halaman depan ---------- */
.cover{background:radial-gradient(circle at 78% 22%,#12507F 0%,#0A2E5C 38%,#08213C 68%,#061C38 100%)}
.cover .halo{position:absolute;right:-18mm;top:-6mm;width:120mm;height:120mm;border-radius:50%;
      background:radial-gradient(circle,rgba(18,136,111,.55),rgba(18,136,111,0) 62%)}
.cover .cv-in{position:absolute;left:0;right:0;top:@@BAND@@mm;bottom:0}
.cover .cv-frame{position:absolute;left:5mm;top:19mm;right:5mm;bottom:5mm;
      border:.25mm solid rgba(198,161,91,.34);border-radius:1mm}
.cover .cv-frame:before,.cover .cv-frame:after{content:'';position:absolute;width:6mm;height:6mm;
      border:.45mm solid rgba(231,206,147,.75)}
.cover .cv-frame:before{left:-1mm;top:-1mm;border-right:0;border-bottom:0}
.cover .cv-frame:after{right:-1mm;bottom:-1mm;border-left:0;border-top:0}
.cover .brand{position:absolute;left:14mm;top:13mm}
.cover .eyeb{position:absolute;left:14mm;top:40mm;display:flex;align-items:center;gap:2mm}
.cover .eyeb .ln{width:9mm;height:.3mm;background:linear-gradient(90deg,rgba(231,206,147,0),#E7CE93)}
.cover .yr{position:absolute;left:14mm;top:58mm;display:block;overflow:visible}
.cover .yrsub{position:absolute;left:14.5mm;top:76mm;font-size:6.4pt;font-weight:700;letter-spacing:1.5mm;
      color:rgba(255,255,255,.82)}
.cover .yrsub span{color:#E7CE93}
.cover .crule{position:absolute;left:14mm;top:83mm;width:34mm;height:.35mm;
      background:linear-gradient(90deg,#C6A15B,rgba(198,161,91,0))}
.cover .tag{position:absolute;left:14mm;top:87mm;font-size:7.6pt;font-weight:600;letter-spacing:.35mm;
      color:#EAF5F1}
.cover .co{position:absolute;left:14mm;top:96mm;font-size:5pt;line-height:1.7;color:rgba(255,255,255,.72);
      letter-spacing:.2mm}
.cover .co b{color:#F3E2B4;font-weight:700;font-size:6pt;letter-spacing:.4mm}
.cover .cvcap{position:absolute;left:14mm;bottom:18mm;font-size:3.9pt;font-weight:700;
      letter-spacing:.55mm;color:rgba(231,206,147,.78)}
.cover .medal{position:absolute;right:7mm;top:15.5mm}
.cover .badge{position:absolute;left:14mm;bottom:9mm;display:flex;align-items:center;gap:2mm;
      border:.25mm solid rgba(198,161,91,.45);border-radius:1.2mm;padding:1.4mm 2.2mm;
      font-size:4.2pt;letter-spacing:.4mm;color:rgba(255,255,255,.8);font-weight:600}
.cover .badge i{width:1.6mm;height:1.6mm;background:#12886F;border-radius:50%;display:block}

/* ---------- halaman belakang ---------- */
.back{background:linear-gradient(165deg,#FFFFFF 0%,#F8FBF9 52%,#EDF5F1 100%)}
.back .bkin{position:absolute;left:0;right:0;top:@@BAND@@mm;bottom:0;overflow:hidden}
.back .bkin .glow{position:absolute;left:-30mm;bottom:-40mm;width:120mm;height:120mm;border-radius:50%;
      background:radial-gradient(circle,rgba(18,136,111,.10),rgba(18,136,111,0) 65%)}
.back .brand{position:absolute;left:9mm;top:5.5mm}
.back .eyeb{position:absolute;left:9mm;top:21mm;display:flex;align-items:center;gap:1.8mm;
      color:#A9822F;font-size:4.1pt;font-weight:700;letter-spacing:1mm}
.back .eyeb .ln{width:7mm;height:.3mm;background:linear-gradient(90deg,#C6A15B,rgba(198,161,91,0))}
.back .h1{position:absolute;left:9mm;top:25mm;font-size:17.5pt;font-weight:700;line-height:1.02;
      letter-spacing:.1mm;color:#0A2A52}
.back .h1 em{font-style:normal;color:#0B6E5F}
.back .h1 .gold{color:#C6A15B}
.back .sub{position:absolute;left:9mm;top:43mm;width:96mm;font-size:5pt;line-height:1.45;color:#3A4E62}
.back .qlab{position:absolute;left:9mm;top:61mm;font-size:4.3pt;font-weight:700;letter-spacing:.3mm;color:#0B6E5F}
.back .feats{position:absolute;left:9mm;top:66.5mm;width:99mm;display:grid;
      grid-template-columns:1fr 1fr;gap:3.1mm 4mm}
.back .feat{display:flex;align-items:center;gap:1.5mm;font-size:4.15pt;color:#22415C;line-height:1.2}
.back .feat .b{width:3.2mm;height:3.2mm;border-radius:50%;flex:0 0 auto;color:#fff;
      background:linear-gradient(150deg,#17A085,#0B6E5F);display:flex;align-items:center;
      justify-content:center}
.back .feat .b svg{width:2.1mm;height:2.1mm}
.back .cta{position:absolute;left:9mm;bottom:11mm;display:flex;align-items:center;gap:3.4mm}
.back .price{border:.35mm solid #C6A15B;border-radius:2mm;padding:1.4mm 3mm 1.6mm;
      background:linear-gradient(160deg,#FFFFFF,#FDF8EC);box-shadow:0 .4mm 1.2mm rgba(198,161,91,.18)}
.back .price .l{font-size:3.5pt;font-weight:700;letter-spacing:.35mm;color:#A9822F}
.back .price .v{font-size:12pt;font-weight:700;color:#0B6E5F;line-height:1.05;margin-top:.3mm}
.back .price .s{font-size:3.2pt;color:#6C8093}
.back .wa{display:flex;align-items:center;gap:1.8mm;padding:2mm 3.2mm;border-radius:2mm;color:#fff;
      background:linear-gradient(150deg,#17A085,#0B6E5F)}
.back .wa .t{font-size:3.4pt;letter-spacing:.3mm;opacity:.9}
.back .wa .n{font-size:6pt;font-weight:700;letter-spacing:.2mm}
.back .art{position:absolute;right:7mm;top:8mm}
.back .ribbon{position:absolute;right:14mm;top:15mm;transform:rotate(-6deg);
      background:linear-gradient(135deg,#0B6E5F,#12886F);color:#fff;border-radius:1.4mm;
      padding:1.5mm 3mm;text-align:center;box-shadow:0 .5mm 1.4mm rgba(6,28,56,.3);
      border:.3mm solid rgba(243,226,180,.5)}
.back .ribbon .a{font-size:3.3pt;letter-spacing:.3mm;opacity:.9}
.back .ribbon .b{font-size:4.6pt;font-weight:700;letter-spacing:.2mm;color:#F3E2B4}
"""

CSS2 = """
.back .quote{position:absolute;left:9mm;top:91mm;width:98mm;border-left:.9mm solid #C6A15B;
      padding:1.6mm 0 1.6mm 3mm;background:linear-gradient(90deg,rgba(198,161,91,.10),rgba(198,161,91,0))}
.back .quote .q{font-size:5pt;font-style:italic;color:#0A2A52;line-height:1.4}
.back .quote .a{font-size:3.6pt;letter-spacing:.35mm;color:#A9822F;font-weight:700;margin-top:1mm}
.back .langkah{position:absolute;left:9mm;top:99mm;display:flex;gap:2.4mm}
"""


CSS3 = """
/* ---------- grid 6 baris (bulan dengan 6 pekan) ---------- */
.grid.g6{grid-template-rows:repeat(6,1fr)}
.grid.g6 .cell .d{font-size:13pt}
.grid.g6 .cell .h{font-size:6.1pt;top:1.25mm}
.grid.g6 .cell .p{font-size:3.65pt;bottom:.85mm}
.grid.g6 .cell .tag{font-size:3pt;bottom:.9mm}
.src{margin-top:1.6mm;font-size:3.1pt;color:#A4B3C1;letter-spacing:.02mm}
/* ---------- blok catatan 2 kolom ---------- */
.notes{position:absolute;left:7mm;top:120.4mm;width:168mm;height:21mm}
.notes .nA,.notes .nB{position:absolute;top:0}
.notes .nA{left:0;width:98mm}
.notes .nB{left:101mm;width:67mm}
.notes .sec{margin-bottom:1.5mm}
.notes .nA .note,.notes .nB .note{margin-top:1.15mm}
.notes .nl{position:absolute;left:0;top:11.7mm;width:98mm;display:flex;gap:2.6mm;flex-wrap:wrap}
.notes .ncat{position:absolute;left:0;right:0;top:15.4mm;display:flex;align-items:baseline;gap:1.4mm;
      font-size:4pt;color:#6C8093}
.notes .ncat .ln{flex:1;border-bottom:.2mm dotted #C6D1DC;height:2.2mm}
.notes .nsrc{position:absolute;left:0;right:0;top:18.8mm;font-size:3.1pt;color:#A4B3C1}
.legend{display:flex;gap:2.6mm;flex-wrap:wrap}
.legend .it{display:flex;align-items:center;gap:1mm;font-size:3.5pt;color:#6C8093}
.legend .sw{width:2.2mm;height:2.2mm;border-radius:.5mm;flex:0 0 auto}
.cell.blank{background:none;border:0}
.note b{color:#B23A48;font-weight:700;flex:0 0 auto}
.note span{flex:1}
.back .simira{position:absolute;left:9mm;top:104mm;display:flex;align-items:center;gap:1.4mm;
      font-size:3.6pt;color:#0B6E5F;font-weight:700;letter-spacing:.25mm}
.back .simira span{border:.2mm solid #9FD8C8;background:#F0FAF6;border-radius:1mm;padding:.7mm 1.6mm}
"""


def build_css(pad: float) -> str:
    pw, ph = W + 2 * pad, H + 2 * pad
    css = CSS + CSS2 + CSS3
    for k, v in {
        "@@W@@": f"{W:g}", "@@H@@": f"{H:g}",
        "@@PW@@": f"{pw:g}", "@@PH@@": f"{ph:g}",
        "@@PWPT@@": f"{pw / 25.4 * 72:.3f}", "@@PHPT@@": f"{ph / 25.4 * 72:.3f}",
        "@@PAD@@": f"{pad:g}", "@@BAND@@": f"{BAND:g}", "@@FOOT@@": f"{FOOT:g}",
    }.items():
        css = css.replace(k, v)
    return css


def page(inner: str, cls: str = "") -> str:
    return f'<section class="page {cls}"><div class="frame">{inner}</div></section>'


def band(prefix: str = "b") -> str:
    return f'<div class="band">{A.pattern(prefix + "band", "#F3E2B4", 0.10, 44)}</div>'


def foot() -> str:
    return f"""<div class="foot">
  <div class="fc">PT BPR Mitra Mentari Sejahtera &mdash; Berizin &amp; Diawasi oleh Otoritas Jasa Keuangan (OJK)
     dan merupakan Peserta Penjaminan (LPS).</div>
  <div class="fr">
    <div class="k">{A.icon('pin', 2.6)}<span>Jl. Ir. Juanda No. 21 Tonatan, Ponorogo</span></div>
    <div class="k">{A.icon('phone', 2.6)}<span>(0352) 3576 800</span></div>
    <div class="k">{A.icon('globe', 2.6)}<span><b>www.mitrasyariahbank.com</b></span></div>
  </div>
</div>"""

BULAN_ID = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
            "Agustus", "September", "Oktober", "November", "Desember"]
LIBUR_TEKS = {
    (2027, 1, 1): "Libur Tahun Baru 2027 Masehi",
    (2027, 1, 5): "Libur Isra Mi'raj Nabi Muhammad SAW 1448 H",
}


# --------------------------------------------------------------------------- #
# Halaman 1 - sampul depan
# --------------------------------------------------------------------------- #
def page_cover() -> str:
    inner = f"""
  <div class="halo"></div>
  {A.pattern('cv', '#F3E2B4', 0.06, 52)}
  <div class="cv-frame"></div>
  <div class="brand">{A.wordmark('cvm', 12.4, dark=True)}</div>
  <div class="eyeb"><div class="ln"></div>
    <div class="eyebrow" style="color:rgba(255,255,255,.66)">Kalender Meja &middot; Edisi 2027</div></div>
  <svg class="yr" style="width:38mm;height:15.6mm" viewBox="0 0 150 62">
    <defs><linearGradient id="yrcv" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FBF1D2"/><stop offset=".45" stop-color="#E7CE93"/>
      <stop offset=".78" stop-color="#C6A15B"/><stop offset="1" stop-color="#9A7A34"/>
    </linearGradient></defs>
    <text x="0" y="58" font-family="Noto Sans" font-weight="700" font-size="62"
          letter-spacing="-2" fill="url(#yrcv)">2027</text>
  </svg>
  <div class="yrsub"><span>1448 &ndash; 1449</span> &nbsp;HIJRIYAH</div>
  <div class="crule"></div>
  <div class="tag">Amanah &middot; Transparan &middot; Terjangkau</div>
  <div class="co"><b>BPR SYARIAH MITRA MENTARI SEJAHTERA</b><br>
      Ponorogo &middot; Jawa Timur &nbsp;|&nbsp; www.mitrasyariahbank.com</div>
  <div class="cvcap">12 Lembar Bulan &nbsp;&middot;&nbsp; Kalender Masehi &amp; Hijriah &nbsp;&middot;&nbsp; Pasaran Jawa</div>
  <div class="badge"><i></i>Berizin &amp; diawasi OJK &nbsp;&middot;&nbsp; Peserta Penjaminan LPS</div>
  {A.medallion('cv', 84)}
"""
    inner += band('cvb')
    return page(inner, "cover")


def _cell(item, col: int) -> str:
    d, bulan_ini = item
    if d is None:
        return '<div class="cell blank"></div>'
    hy, hm, hd = K.hijriah(d)
    cls = ["cell"]
    if not bulan_ini:
        cls.append("out")
    if col == 0:
        cls.append("sun")
    if col == 5:
        cls.append("fri")
    if bulan_ini and (d.year, d.month, d.day) in LIBUR_TEKS:
        cls.append("hol")
    if bulan_ini and d.month == 1 and d.day in K.PUASA_BIDH_JAN:
        cls.append("bidh")
    tag = ""
    if bulan_ini and hd == 1:
        tag = f'<span class="tag">1 {K.HIJRI_ID[hm].upper()}</span>'
    return (f'<div class="{" ".join(cls)}"><span class="d">{d.day}</span>'
            f'<span class="h">{K.angka_arab(hd)}</span>'
            f'<span class="p">{K.pasaran(d)}</span>{tag}</div>')


def _mini(judul: str, tahun: int, bulan: int) -> str:
    rows = K.matriks_bulan(tahun, bulan)
    head = "".join(f"<th>{h}</th>" for h in ["Ah", "Sn", "Sl", "Rb", "Km", "Jm", "Sb"])
    body = ""
    for row in rows:
        tds = ""
        for i, (d, bulan_ini) in enumerate(row):
            if d is None or not bulan_ini:
                tds += '<td class="e"></td>'
            else:
                cls = ' class="su"' if i == 0 else ""
                tds += f"<td{cls}>{d.day}</td>"
        body += f"<tr>{tds}</tr>"
    return (f'<div class="mini"><div class="mt">{judul}</div>'
            f'<table><tr>{head}</tr>{body}</table></div>')


def _qr_card(size: float = 16.6) -> str:
    from qr_code import encode, to_svg_path
    path, _ = to_svg_path(encode("https://www.mitrasyariahbank.com"), size, quiet=2)
    return f"""<div class="qr">
  <div class="qt">SCAN ME</div>
  <svg style="width:{size}mm;height:{size}mm" viewBox="0 0 {size} {size}">
    <path d="{path}" fill="#0A2A52"/></svg>
  <div class="qu">mitrasyariahbank.com</div>
</div>"""

# --------------------------------------------------------------------------- #
# Halaman 2 - lembar tanggal bulanan (Januari 2027)
# --------------------------------------------------------------------------- #
def _notes_blok() -> str:
    from datetime import date as D
    libur = ""
    for (y, m, d) in sorted(LIBUR_TEKS):
        libur += (f'<div class="note"><b>{K.weton(D(y, m, d)).upper()}, {d} '
                  f'{BULAN_ID[m].upper()} {y}</b>'
                  f'<span>&mdash; {LIBUR_TEKS[(y, m, d)]}</span></div>')
    return f"""<div class="notes">
  <div class="nA"><div class="sec">Keterangan Hari Besar</div>{libur}</div>
  <div class="nB"><div class="sec">Catatan Penting</div>
    <div class="note"><b>Puasa Ayyamul Bidh</b><span>21, 22, 23 Januari 2027 (13&ndash;15 Sya'ban 1448 H)</span></div>
    <div class="note"><b>Awal Sya'ban 1448 H</b><span>Sabtu, 9 Januari 2027</span></div>
  </div>
  <div class="nl"><div class="legend">
    <div class="it"><span class="sw" style="background:#F7CFC8;border:.15mm solid #E7B4AB"></span>Libur / hari Ahad</div>
    <div class="it"><span class="sw" style="background:#C6A15B;border-radius:50%"></span>Puasa sunnah</div>
    <div class="it"><span class="sw" style="background:#FBF3DF;border:.15mm solid #E7CE93"></span>Awal bulan Hijriah</div>
  </div></div>
  <div class="ncat"><span>Catatan</span><span class="ln"></span></div>
  <div class="nsrc">Penanggalan Hijriah mengacu Kalender Islam Kemenag RI &amp; Umm al-Qura &middot;
    pasaran Jawa memakai siklus 5 hari.</div>
</div>"""


def page_month(tahun: int = 2027, bulan: int = 1) -> str:
    import calendar as _cal
    from datetime import date as D

    rows = K.matriks_bulan(tahun, bulan)
    nrow = len(rows)
    sel = "".join(_cell(d, i) for row in rows for i, d in enumerate(row))
    akhir = D(tahun, bulan, _cal.monthrange(tahun, bulan)[1])
    hy1, hm1, _ = K.hijriah(D(tahun, bulan, 1))
    hy2, hm2, _ = K.hijriah(akhir)
    if hm1 == hm2:
        span_id = f"{K.HIJRI_ID[hm1].upper()} {hy2} H"
        span_ar = f"{K.HIJRI_AR[hm1]} {K.angka_arab(hy2)} هـ"
    else:
        span_id = f"{K.HIJRI_ID[hm1].upper()} &ndash; {K.HIJRI_ID[hm2].upper()} {hy2} H"
        span_ar = f"{K.HIJRI_AR[hm1]} &ndash; {K.HIJRI_AR[hm2]} {K.angka_arab(hy2)} هـ"
    tgl1 = D(tahun, bulan, 1)
    g6 = ' g6' if nrow >= 6 else ''

    inner = f"""
  {band('mo')}
  <div class="brand" style="position:absolute;left:7mm;top:16.2mm">{A.wordmark('mob', 10.6)}</div>
  <div class="hijri">
    <div class="h1">{span_id}</div>
    <div class="h2">1 {BULAN_ID[bulan].upper()} {tahun} = {K.hijriah_teks(tgl1)}</div>
    <div class="h3">{span_ar}</div>
  </div>
  <div class="mrow">
    <div class="chip">{bulan:02d}</div>
    <div class="mname"><span class="n">{BULAN_ID[bulan].upper()}</span><span class="y">{tahun}</span>
      <div class="ar">{K.HIJRI_AR[hm1]} &nbsp;&middot;&nbsp; {K.HIJRI_ID[hm1]} {hy1} H</div></div>
  </div>
  <div class="wk"><span class="sun">AHAD</span><span>SENIN</span><span>SELASA</span><span>RABU</span>
    <span>KAMIS</span><span>JUM'AT</span><span class="sat">SABTU</span></div>
  <div class="grid{g6}">{sel}</div>
  {_notes_blok()}
  <div class="rail">{_mini('DESEMBER 2026', 2026, 12)}{_mini('FEBRUARI 2027', 2027, 2)}{_qr_card()}</div>
  {foot()}
"""
    return page(inner, "month")

# --------------------------------------------------------------------------- #
# Halaman 3 - sampul belakang (promo produk)
# --------------------------------------------------------------------------- #
def page_back() -> str:
    feats = [
        "Mudah pendaftarannya",
        "Transparan pengelolaan",
        "Aman dananya",
        "Menarik bagi hasilnya",
        "Bebas biaya administrasi",
        "Travel PP IuH &amp; PIHK terpercaya",
    ]
    feat_html = "".join(
        f'<div class="feat"><span class="b">{A.icon("check", 2.1, 2.6)}</span><span>{f}</span></div>'
        for f in feats
    )
    inner = f"""
  {band('bk')}
  <div class="bkin">
    <div class="glow"></div>
    {A.pattern('bk', '#0B6E5F', 0.018, 64)}
    <div class="brand">{A.wordmark('bkb', 10.6)}</div>
    <div class="eyeb"><div class="ln"></div>Produk Unggulan</div>
    <div class="h1">Tabungan <em>Umroh</em><br>Mitra</div>
    <div class="sub">Rencanakan perjalanan ibadah Anda sejak dini. Menabung bertahap
      dengan akad syariah, ringan, dan aman bersama Bank Mitra.</div>
    <div class="qlab">Kenapa menabung Umroh di Bank Mitra?</div>
    <div class="feats">{feat_html}</div>
    <div class="quote">
      <div class="q">&ldquo;Haji tahun ini menjadi do&rsquo;a, Umroh tahun depan jadi nyata.&rdquo;</div>
      <div class="a">MITRA SYARIAH &middot; AMANAH, TRANSPARAN, TERJANGKAU</div>
    </div>
    <div class="simira"><span>SiMIRA</span> Simpanan Mitra Rencana &mdash; setor kapan saja</div>
    <div class="cta">
      <div class="price"><div class="l">MULAI</div><div class="v">Rp40.000</div>
        <div class="s">ribuan per-setor</div></div>
      <div class="wa">{A.icon('phone', 5.2, 1.7)}
        <div><div class="t">HUBUNGI KAMI &middot; WA RESMI</div>
          <div class="n">0813-1349-9873</div></div></div>
    </div>
    <div class="art">{A.kaaba_scene('bk', 84, 101)}
      <div class="ribbon"><div class="a">RENCANAKAN</div><div class="b">DARI SEKARANG</div></div>
    </div>
  </div>
  {foot()}
"""
    return page(inner, "back")


def build_html(pad: float = 0.0) -> str:
    pages = page_cover() + page_month() + page_back()
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<title>Kalender Meja 2027 - BPR Syariah Mitra Mentari Sejahtera</title>
<style>{build_css(pad)}</style></head>
<body>{pages}</body></html>"""


if __name__ == "__main__":
    print("page_cover:", len(page_cover()))
    print("page_month:", len(page_month()))
    print("page_back :", len(page_back()))
