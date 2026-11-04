"""Arah desain v2 — 'Editorial Mihrab' (krem, serif, garis emas, tabel hairline)."""

from __future__ import annotations

import assets_v2 as A2
import kalender_data as K

W, H = 213.0, 152.0
BAND = 14.0
FOOT = 9.0

BULAN_ID = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
            "Agustus", "September", "Oktober", "November", "Desember"]
LIBUR_TEKS = {
    (2027, 1, 1): "Libur Tahun Baru 2027 Masehi",
    (2027, 1, 5): "Libur Isra Mi'raj Nabi Muhammad SAW 1448 H",
}

CSS = """
@page{size:@@PWPT@@pt @@PHPT@@pt;margin:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;padding:0;background:#fff;font-family:'Noto Sans',sans-serif;color:#10202E}
.page{position:relative;width:@@PW@@mm;height:@@PH@@mm;overflow:hidden;background:#FBF9F4;
      page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}
.frame{position:absolute;left:@@PAD@@mm;top:@@PAD@@mm;width:@@W@@mm;height:@@H@@mm}
.pat{pointer-events:none}

/* ---------- pita ring ---------- */
.band{position:absolute;left:-@@PAD@@mm;right:-@@PAD@@mm;top:-@@PAD@@mm;
      height:calc(@@BAND@@mm + @@PAD@@mm);background:#FBF9F4;overflow:hidden}
.band:after{content:'';position:absolute;left:0;right:0;bottom:0;height:.3mm;
      background:linear-gradient(90deg,rgba(185,145,84,0),#B99154 28%,#D8BE8A 50%,#B99154 72%,rgba(185,145,84,0))}

/* ---------- wordmark ---------- */
.wm2{display:flex;align-items:center;gap:2.4mm}
.wm2t{line-height:1.05}
.wm2a{font-size:3.3pt;letter-spacing:.48mm;font-weight:700}
.wm2b{font-size:11pt;font-weight:700;letter-spacing:-.1mm;margin-top:.4mm}
.wm2c{font-size:3.2pt;letter-spacing:.3mm;margin-top:.5mm;font-weight:600}
.lbl{font-size:3.9pt;font-weight:700;letter-spacing:.85mm;text-transform:uppercase;color:#B99154}
.lbl2{font-size:4pt;font-weight:700;letter-spacing:.7mm;text-transform:uppercase;color:#10202E}
.rule{height:.2mm;background:rgba(185,145,84,.55)}

/* ---------- header bulan ---------- */
.hd{position:absolute;left:12mm;right:12mm;top:17.5mm}
.hd .hr{position:absolute;right:0;top:0;text-align:right}
.hd .hr .a{font-size:5.6pt;font-weight:700;letter-spacing:.45mm;color:#10202E}
.hd .hr .b{font-size:3.7pt;letter-spacing:.3mm;color:rgba(16,32,46,.55);margin-top:.9mm}
.hd .hr .c{font-family:'Noto Naskh Arabic';font-size:9pt;color:#B99154;margin-top:.7mm}

/* ---------- rail kiri ---------- */
.rail{position:absolute;left:12mm;top:33mm;width:43mm;height:93.4mm}
.rail .vln{position:absolute;right:-3mm;top:-1mm;bottom:-1mm;width:.15mm;background:#E3DBCA}
.rail .hidx{font-size:4pt;font-weight:700;letter-spacing:.6mm;color:rgba(16,32,46,.45)}
.rail .mname{font-family:'Noto Serif';font-weight:700;font-size:24pt;line-height:1;color:#10202E;
      margin-top:1.6mm;letter-spacing:-.2mm}
.rail .myear{font-size:8.5pt;font-weight:700;letter-spacing:1.4mm;color:#B99154;margin-top:2.2mm}
.rail .mrule{width:22mm;height:.2mm;background:#B99154;margin:3.2mm 0 2.6mm}
.rail .mar{font-family:'Noto Naskh Arabic';font-size:13pt;color:#0C4F45;line-height:1.4}
.rail .mhij{font-size:4pt;letter-spacing:.35mm;color:rgba(16,32,46,.6);margin-top:1.4mm;line-height:1.5}
.rail .mhij b{color:#10202E;font-weight:700}
.rail .rgt{position:absolute;left:0;right:3mm;top:38mm;display:flex;flex-direction:column;gap:1.5mm}
.rail .gi{display:flex;align-items:center;gap:1.3mm;font-size:3.5pt;color:rgba(16,32,46,.62)}
.rail .gs{width:2mm;height:2mm;flex:0 0 auto}

/* ---------- tabel tanggal ---------- */
.tbl{position:absolute;left:64mm;top:33mm;width:137mm;height:93.4mm;display:grid;
      grid-template-columns:repeat(7,1fr)}
.tc{position:relative;border-right:.15mm solid #E4DCCB;border-bottom:.15mm solid #E4DCCB;
      padding:1.3mm 1.5mm}
.tc.lc{border-right:0}
.th{display:flex;align-items:center;justify-content:center;height:6.6mm;
      border-bottom:.45mm solid #10202E;font-size:3.9pt;font-weight:700;letter-spacing:.42mm;
      color:rgba(16,32,46,.78)}
.th.red{color:#A6432F}
.th.grn{color:#0C4F45}
.tc .d{font-family:'Noto Serif';font-weight:700;font-size:16.5pt;line-height:1;color:#10202E;
      display:block;margin-top:.5mm}
.tc .h{position:absolute;right:1.4mm;top:1.2mm;font-family:'Noto Sans Arabic';font-size:5.7pt;
      color:#B99154}
.tc .p{position:absolute;left:1.5mm;bottom:1.1mm;font-size:3.4pt;font-weight:700;letter-spacing:.3mm;
      text-transform:uppercase;color:rgba(16,32,46,.4)}
.tc.sun{background:rgba(239,231,215,.6)}
.tc.sat{background:rgba(18,121,106,.05)}
.tc.fri .p{color:#8C6D33}
.tc.hol .d{color:#A6432F}
.tc.hol:after{content:'';position:absolute;right:1.5mm;bottom:1.4mm;width:1.1mm;height:1.1mm;
      border-radius:50%;background:#A6432F}
.tc.bidh:before{content:'';position:absolute;right:1.5mm;bottom:1.4mm;width:1.1mm;height:1.1mm;
      border-radius:50%;background:#B99154}
.tc.out .d{color:rgba(16,32,46,.2)}
.tc.out .h{color:rgba(185,145,84,.45)}
.tc.out .p{color:rgba(16,32,46,.18)}
.tc .tg{position:absolute;left:1.5mm;top:8.2mm;font-size:3pt;font-weight:700;letter-spacing:.16mm;
      color:#8C6D33}

/* ---------- catatan ---------- */
.nt{position:absolute;left:12mm;right:12mm;top:130.4mm;display:flex;gap:9mm}
.nt .col{flex:1}
.nt .nh{font-size:3.5pt;font-weight:700;letter-spacing:.7mm;text-transform:uppercase;
      color:#B99154;margin-bottom:1.5mm}
.nt .ni{display:flex;gap:1.8mm;font-size:3.6pt;line-height:1.5;color:rgba(16,32,46,.72);margin-bottom:.6mm}
.nt .ni b{color:#A6432F;font-weight:700;flex:0 0 auto}
.nt .ni i{color:#B99154;font-style:normal;font-weight:700;flex:0 0 auto}
.nt .src{font-size:2.9pt;color:rgba(16,32,46,.33);margin-top:1.4mm}

/* ---------- footer ---------- */
.ft{position:absolute;left:-@@PAD@@mm;right:-@@PAD@@mm;bottom:-@@PAD@@mm;
      height:calc(@@FOOT@@mm + @@PAD@@mm);background:#0C4F45;display:flex;align-items:center;
      justify-content:space-between;padding:0 12mm;gap:6mm;color:rgba(255,255,255,.66);
      font-size:3.25pt}
.ft .fl{max-width:108mm;line-height:1.5}
.ft .fr{display:flex;align-items:center;gap:3.4mm;line-height:1.5}
.ft b{color:#D8BE8A;font-weight:700}
.ft .sep{width:.15mm;height:2.6mm;background:rgba(255,255,255,.22)}

/* ---------- sampul depan ---------- */
.cv{background:#FBF9F4}
.cv .panel{position:absolute;right:-@@PAD@@mm;top:-@@PAD@@mm;bottom:-@@PAD@@mm;width:82mm;
      background:linear-gradient(165deg,#11604F 0%,#0C4F45 45%,#08362D 100%);overflow:hidden}
.cv .panel .arch2{position:absolute;left:50%;margin-left:-26mm;top:23mm}
.cv .panel .cap{position:absolute;left:0;right:0;bottom:11mm;text-align:center;font-size:3.1pt;
      letter-spacing:.95mm;color:rgba(216,190,138,.72);font-weight:700}
.cv .wm{position:absolute;left:12mm;top:25mm}
.cv .eb{position:absolute;left:12mm;top:47mm;display:flex;align-items:center;gap:2.2mm}
.cv .eb .ln{width:8mm;height:.2mm;background:#B99154}
.cv .yr{position:absolute;left:11.2mm;top:51mm;font-family:'Noto Serif';font-weight:700;
      font-size:62pt;line-height:.9;letter-spacing:-1.2mm;color:#10202E}
.cv .hij{position:absolute;left:12mm;top:81mm;font-size:5.2pt;font-weight:700;letter-spacing:1.7mm;
      color:#B99154}
.cv .hij span{color:rgba(16,32,46,.5)}
.cv .cr{position:absolute;left:12mm;top:87.5mm;width:36mm;height:.2mm;background:rgba(185,145,84,.65)}
.cv .tg{position:absolute;left:12mm;top:91mm;font-family:'Noto Serif';font-style:italic;font-size:7.6pt;
      color:#0C4F45}
.cv .co{position:absolute;left:12mm;top:101mm;font-size:3.8pt;letter-spacing:.3mm;
      color:rgba(16,32,46,.6);line-height:1.75}
.cv .co b{display:block;font-size:4.7pt;letter-spacing:.45mm;color:#10202E;font-weight:700;margin-bottom:.9mm}
.cv .col2{position:absolute;left:12mm;bottom:13mm;display:flex;align-items:center;gap:2mm;
      font-size:3.3pt;letter-spacing:.45mm;color:rgba(16,32,46,.45)}
.cv .col2 i{width:1.3mm;height:1.3mm;border-radius:50%;background:#B99154;display:block;flex:0 0 auto}

/* ---------- sampul belakang ---------- */
.bk{background:#FBF9F4}
.bk .panel{position:absolute;right:-@@PAD@@mm;top:-@@PAD@@mm;bottom:-@@PAD@@mm;width:82mm;
      background:linear-gradient(165deg,#11604F 0%,#0C4F45 50%,#08362D 100%);overflow:hidden}
.bk .panel .kab2{position:absolute;left:50%;margin-left:-26mm;top:25mm}
.bk .wm{position:absolute;left:12mm;top:24mm}
.bk .eb{position:absolute;left:12mm;top:45mm;font-size:3.8pt;font-weight:700;letter-spacing:.85mm;
      color:#B99154;text-transform:uppercase}
.bk .h1{position:absolute;left:12mm;top:49.5mm;font-family:'Noto Serif';font-weight:700;font-size:18.5pt;
      line-height:1.1;color:#10202E;letter-spacing:-.2mm}
.bk .h1 em{font-style:italic;color:#0C4F45}
.bk .sub{position:absolute;left:12mm;top:71.5mm;width:70mm;font-size:4.5pt;line-height:1.6;
      color:rgba(16,32,46,.7)}
.bk .ql{position:absolute;left:12mm;top:82mm;font-size:3.7pt;font-weight:700;letter-spacing:.55mm;
      color:#0C4F45}
.bk .fgr{position:absolute;left:12mm;top:86mm;width:78mm;display:grid;
      grid-template-columns:1fr 1fr;gap:2.8mm 5mm}
.bk .fi{display:flex;align-items:flex-start;gap:1.7mm;font-size:3.85pt;line-height:1.35;
      color:rgba(16,32,46,.8)}
.bk .fi i{width:3mm;height:.25mm;background:#B99154;margin-top:1.1mm;flex:0 0 auto}
.bk .q{position:absolute;left:12mm;top:108mm;width:74mm;border-left:.5mm solid #B99154;
      padding-left:3mm;font-family:'Noto Serif';font-style:italic;font-size:5.4pt;line-height:1.5;
      color:#0C4F45}
.bk .cta{position:absolute;left:12mm;bottom:13mm;display:flex;align-items:center;gap:4mm}
.bk .pr{border:.25mm solid #B99154;padding:1.8mm 3mm}
.bk .pr .l{font-size:3.1pt;letter-spacing:.5mm;color:#8C6D33;font-weight:700}
.bk .pr .v{font-family:'Noto Serif';font-weight:700;font-size:11pt;color:#0C4F45;
      line-height:1.1;margin-top:.4mm}
.bk .wa{display:flex;align-items:center;gap:2mm;background:#0C4F45;color:#fff;padding:2.3mm 3.4mm}
.bk .wa .t{font-size:3pt;letter-spacing:.4mm;opacity:.78}
.bk .wa .n{font-size:5.4pt;font-weight:700;letter-spacing:.2mm;margin-top:.6mm}
.bk .sml{position:absolute;left:12mm;bottom:8mm;font-size:3.1pt;letter-spacing:.35mm;
      color:rgba(16,32,46,.38)}
"""

CSS3 = """
.rail .rgt2{display:flex;flex-direction:column;gap:1.7mm;margin-top:5.4mm}
.rail .rqr{position:absolute;left:0;bottom:0;width:31mm}
.rail .rqr .qt{font-size:3.2pt;font-weight:700;letter-spacing:.62mm;color:#B99154;
      text-transform:uppercase;margin-bottom:1.3mm}
.rail .rqr .qu{font-size:3pt;color:rgba(16,32,46,.42);margin-top:1.1mm;letter-spacing:.1mm}
.nt .cat{margin-top:1.6mm;display:flex;align-items:baseline;gap:1.6mm;font-size:3.5pt;
      color:rgba(16,32,46,.45)}
.nt .cat .ln{flex:1;border-bottom:.18mm dotted rgba(16,32,46,.25);height:2.1mm}
"""


def build_css(pad: float) -> str:
    pw, ph = W + 2 * pad, H + 2 * pad
    css = CSS + CSS3 + CSS4
    for k, v in {
        "@@W@@": f"{W:g}", "@@H@@": f"{H:g}", "@@PW@@": f"{pw:g}", "@@PH@@": f"{ph:g}",
        "@@PWPT@@": f"{pw / 25.4 * 72:.3f}", "@@PHPT@@": f"{ph / 25.4 * 72:.3f}",
        "@@PAD@@": f"{pad:g}", "@@BAND@@": f"{BAND:g}", "@@FOOT@@": f"{FOOT:g}",
    }.items():
        css = css.replace(k, v)
    return css


def page(inner: str, cls: str = "") -> str:
    return f'<section class="page {cls}"><div class="frame">{inner}</div></section>'


def band() -> str:
    return '<div class="band"></div>'


def foot() -> str:
    return """<div class="ft">
  <div class="fl">PT BPR Mitra Mentari Sejahtera &mdash; berizin &amp; diawasi OJK,
     peserta penjaminan LPS. Kalender ini dicetak dalam 2 penanggalan: Masehi dan Hijriah.</div>
  <div class="fr"><span>Jl. Ir. Juanda No. 21 Tonatan, Ponorogo</span><span class="sep"></span>
    <span>(0352) 3576 800</span><span class="sep"></span>
    <span><b>www.mitrasyariahbank.com</b></span></div>
</div>"""


def qr_block(size: float = 17.0) -> str:
    from qr_code import encode, to_svg_path
    path, _ = to_svg_path(encode("https://www.mitrasyariahbank.com"), size, quiet=2)
    return (f'<div class="rqr"><div class="qt">Scan me</div>'
            f'<svg style="display:block;width:{size}mm;height:{size}mm" viewBox="0 0 {size} {size}">'
            f'<path d="{path}" fill="#0C4F45"/></svg>'
            f'<div class="qu">mitrasyariahbank.com</div></div>')


def _legend() -> str:
    items = [("#A6432F", "Libur nasional &amp; hari Ahad"),
             ("#B99154", "Puasa Ayyamul Bidh"),
             ("#0C4F45", "Awal bulan Hijriah")]
    out = ""
    for warna, teks in items:
        out += (f'<div class="gi"><span class="gs" style="background:{warna};'
                f'{"border-radius:50%" if warna != "#0C4F45" else "border:.2mm solid #0C4F45;background:none"}">'
                f'</span><span>{teks}</span></div>')
    return out

CSS4 = """
.hd .hl{position:absolute;left:0;top:0}
.src2{position:absolute;left:12mm;right:12mm;top:140.9mm;font-size:2.9pt;
      color:rgba(16,32,46,.34);letter-spacing:.05mm}
.cv .panel:before,.bk .panel:before{content:'';position:absolute;left:0;top:0;bottom:0;
      width:.2mm;background:rgba(216,190,138,.45)}
.bk .panel .cap{position:absolute;left:0;right:0;bottom:11mm;text-align:center;font-size:3.1pt;
      letter-spacing:.95mm;color:rgba(216,190,138,.72);font-weight:700}
.cv .col3{position:absolute;left:12mm;bottom:23.5mm;font-size:3.4pt;letter-spacing:.62mm;
      color:rgba(16,32,46,.4);text-transform:uppercase}
.bk .sml{bottom:28.4mm}
"""


def _tc(item, col: int) -> str:
    d, bulan_ini = item
    lc = " lc" if col == 6 else ""
    if d is None:
        return f'<div class="tc{lc}"></div>'
    hy, hm, hd = K.hijriah(d)
    cls = ["tc"]
    if col == 6:
        cls.append("lc")
    if not bulan_ini:
        cls.append("out")
    if col == 0:
        cls.append("sun")
    if col == 6:
        cls.append("sat")
    if col == 5:
        cls.append("fri")
    if bulan_ini and (d.year, d.month, d.day) in LIBUR_TEKS:
        cls.append("hol")
    if bulan_ini and d.month == 1 and d.day in K.PUASA_BIDH_JAN:
        cls.append("bidh")
    tag = ""
    if bulan_ini and hd == 1:
        tag = f'<span class="tg">1 {K.HIJRI_ID[hm].upper()}</span>'
    return (f'<div class="{" ".join(cls)}"><span class="d">{d.day}</span>'
            f'<span class="h">{K.angka_arab(hd)}</span>'
            f'<span class="p">{K.pasaran(d)}</span>{tag}</div>')


def _tabel(tahun: int, bulan: int) -> str:
    rows = K.matriks_bulan(tahun, bulan, isi_akhir=True)
    head = "".join(
        f'<div class="th{" red" if i == 0 else (" grn" if i == 6 else "")}">{h}</div>'
        for i, h in enumerate(["Ahad", "Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu"]))
    body = "".join(_tc(item, col) for row in rows for col, item in enumerate(row))
    return (f'<div class="tbl" style="grid-template-rows:6.6mm repeat({len(rows)},1fr)">'
            f'{head}{body}</div>')


def _notes() -> str:
    from datetime import date as D
    l1 = ""
    for (y, m, d) in sorted(LIBUR_TEKS):
        l1 += (f'<div class="ni"><b>{K.weton(D(y, m, d)).upper()}, {d} {BULAN_ID[m].upper()}</b>'
               f'<span>&mdash; {LIBUR_TEKS[(y, m, d)]}</span></div>')
    return f"""<div class="nt">
  <div class="col"><div class="nh">Keterangan hari besar</div>{l1}</div>
  <div class="col"><div class="nh">Catatan penting</div>
    <div class="ni"><i>13&ndash;15 Sya'ban</i><span>Puasa sunnah Ayyamul Bidh &mdash; 21, 22, 23 Januari 2027</span></div>
    <div class="ni"><i>1 Sya'ban 1448</i><span>Awal bulan Sya'ban &mdash; Sabtu, 9 Januari 2027</span></div>
    <div class="cat"><span>Catatan</span><span class="ln"></span></div>
  </div>
</div>
<div class="src2">Penanggalan Hijriah mengikuti Kalender Islam Kemenag RI &amp; Umm al-Qura &middot;
  pasaran Jawa memakai siklus 5 hari.</div>"""


def _rail(tahun: int, bulan: int) -> str:
    import calendar as _cal
    from datetime import date as D
    tgl1 = D(tahun, bulan, 1)
    akhir = D(tahun, bulan, _cal.monthrange(tahun, bulan)[1])
    hy1, hm1, _ = K.hijriah(tgl1)
    hy2, hm2, _ = K.hijriah(akhir)
    if hm1 == hm2:
        span = f"{K.HIJRI_ID[hm1]} {hy2} H"
        ar = K.HIJRI_AR[hm1]
    else:
        span = f"{K.HIJRI_ID[hm1]} – {K.HIJRI_ID[hm2]} {hy2} H"
        ar = f"{K.HIJRI_AR[hm1]} &middot; {K.HIJRI_AR[hm2]}"
    return f"""<div class="rail">
  <div class="vln"></div>
  <div class="hidx">BULAN {bulan:02d} &nbsp;/&nbsp; 12</div>
  <div class="mname">{BULAN_ID[bulan]}</div>
  <div class="myear">{tahun}</div>
  <div class="mrule"></div>
  <div class="mar">{ar}</div>
  <div class="mhij"><b>{span.upper()}</b><br>
    {tgl1.day} {BULAN_ID[bulan]} {tahun}<br>= {K.hijriah_teks(tgl1)}<br>{K.weton(tgl1)}</div>
  <div class="rgt2">{_legend()}</div>
  {qr_block()}
</div>"""


def page_month(tahun: int = 2027, bulan: int = 1) -> str:
    import calendar as _cal
    from datetime import date as D
    tgl1 = D(tahun, bulan, 1)
    akhir = D(tahun, bulan, _cal.monthrange(tahun, bulan)[1])
    hy1, hm1, _ = K.hijriah(tgl1)
    hy2, hm2, _ = K.hijriah(akhir)
    if hm1 == hm2:
        span = f"{K.HIJRI_ID[hm1].upper()} {hy2} H"
        span_ar = f"{K.HIJRI_AR[hm1]} {K.angka_arab(hy2)} هـ"
    else:
        span = f"{K.HIJRI_ID[hm1].upper()} – {K.HIJRI_ID[hm2].upper()} {hy2} H"
        span_ar = f"{K.HIJRI_AR[hm1]} – {K.HIJRI_AR[hm2]} {K.angka_arab(hy2)} هـ"
    inner = f"""
  {band()}
  <div class="hd">
    <div class="hl">{A2.wordmark('mo', 8.8)}</div>
    <div class="hr">
      <div class="a">{span}</div>
      <div class="b">{tgl1.day} {BULAN_ID[bulan].upper()} {tahun} = {K.hijriah_teks(tgl1).upper()} &nbsp;&middot;&nbsp; {K.weton(tgl1).upper()}</div>
      <div class="c">{span_ar}</div>
    </div>
  </div>
  {_rail(tahun, bulan)}
  {_tabel(tahun, bulan)}
  {_notes()}
  {foot()}
"""
    return page(inner, "mn")


def page_cover() -> str:
    inner = f"""
  {band()}
  <div class="panel">
    <div class="arch2">{A2.arch('cv', 52, 106, label='١٤٤٨ هـ')}</div>
    <div class="cap">KALENDER MEJA &nbsp;&middot;&nbsp; EDISI 2027 &nbsp;&middot;&nbsp; EKONOMI SYARIAH</div>
  </div>
  <div class="wm">{A2.wordmark('cvm', 11)}</div>
  <div class="eb"><div class="ln"></div><div class="lbl">Kalender meja</div></div>
  <div class="yr">2027</div>
  <div class="hij">1448 &ndash; 1449 <span>HIJRIYAH</span></div>
  <div class="cr"></div>
  <div class="tg">Amanah, transparan, terjangkau.</div>
  <div class="co"><b>BPR SYARIAH MITRA MENTARI SEJAHTERA</b>
     Ponorogo &middot; Jawa Timur &nbsp;|&nbsp; www.mitrasyariahbank.com</div>
  <div class="col3">12 lembar bulan &nbsp;&middot;&nbsp; Masehi &amp; Hijriah &nbsp;&middot;&nbsp; Pasaran Jawa</div>
  <div class="col2"><i></i>Berizin &amp; diawasi OJK &nbsp;&middot;&nbsp; Peserta Penjaminan LPS</div>
"""
    return page(inner, "cv")


def page_back() -> str:
    feats = [
        "Mudah pendaftarannya",
        "Transparan pengelolaan",
        "Aman dananya",
        "Menarik bagi hasilnya",
        "Bebas biaya administrasi",
        "Travel PP IuH &amp; PIHK terpercaya",
    ]
    fgr = "".join(f'<div class="fi"><i></i><span>{f}</span></div>' for f in feats)
    inner = f"""
  {band()}
  <div class="panel"><div class="kab2">{A2.kaaba_line('bk', 52, 106)}</div>
    <div class="cap">AMANAH &nbsp;&middot;&nbsp; TRANSPARAN &nbsp;&middot;&nbsp; TERJANGKAU</div></div>
  <div class="wm">{A2.wordmark('bkm', 10)}</div>
  <div class="eb">Produk unggulan</div>
  <div class="h1">Tabungan <em>Umroh</em><br>Mitra</div>
  <div class="sub">Rencanakan perjalanan ibadah Anda sejak dini. Menabung bertahap dengan
    akad syariah &mdash; ringan, aman, dan tanpa biaya administrasi.</div>
  <div class="ql">Kenapa menabung Umroh di Bank Mitra?</div>
  <div class="fgr">{fgr}</div>
  <div class="q">&ldquo;Haji tahun ini menjadi do&rsquo;a,<br>Umroh tahun depan jadi nyata.&rdquo;</div>
  <div class="sml">SiMIRA &nbsp;&middot;&nbsp; Simpanan Mitra Rencana &nbsp;&middot;&nbsp; setor kapan saja</div>
  <div class="cta">
    <div class="pr"><div class="l">MULAI DARI</div><div class="v">Rp40.000</div></div>
    <div class="wa"><div><div class="t">HUBUNGI KAMI &middot; WA RESMI</div>
      <div class="n">0813-1349-9873</div></div></div>
  </div>
  {foot()}
"""
    return page(inner, "bk")


def build_html(pad: float = 0.0) -> str:
    pages = page_cover() + page_month() + page_back()
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<title>Kalender Meja 2027 v2 - Editorial Mihrab</title>
<style>{build_css(pad)}</style></head>
<body>{pages}</body></html>"""


if __name__ == "__main__":
    print("cover", len(page_cover()), "| month", len(page_month()), "| back", len(page_back()))
