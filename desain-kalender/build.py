"""Build semua output kalender: HTML, PDF siap cetak, dan preview PNG.

Pemakaian:  python3 build.py
"""

from __future__ import annotations

import pathlib
import re
import subprocess

import design as D

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)
DPI_MM = 96 / 25.4  # px per mm pada 96 dpi


def _chromium(*args: str) -> None:
    cmd = ["chromium", "--headless", "--no-sandbox", "--disable-gpu",
           "--hide-scrollbars", "--force-color-profile=srgb",
           "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000", *args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"chromium gagal: {r.stderr[-800:]}")


def html_file(name: str, html: str) -> pathlib.Path:
    p = OUT / name
    p.write_text(html, encoding="utf-8")
    return p


def to_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path) -> tuple[float, float, int]:
    _chromium("--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
              f"file://{html_path}")
    raw = pdf_path.read_bytes()
    box = re.search(rb"MediaBox\s*\[([^\]]*)\]", raw)
    nums = [float(x) for x in box.group(1).split()]
    w_mm, h_mm = nums[2] / 72 * 25.4, nums[3] / 72 * 25.4
    pages = len(re.findall(rb"/Type\s*/Page[^s]", raw))
    return w_mm, h_mm, pages


def to_png(html_path: pathlib.Path, png_path: pathlib.Path, scale: int = 2) -> None:
    w = round(D.W * DPI_MM)
    h = round(D.H * DPI_MM)
    _chromium(f"--force-device-scale-factor={scale}", f"--window-size={w},{h}",
              f"--screenshot={png_path}", f"file://{html_path}")


GUIDE_CSS = """
.guide{position:absolute;inset:0;pointer-events:none;z-index:99}
.guide .safe{position:absolute;left:6mm;right:6mm;top:18mm;bottom:6mm;
  border:.3mm dashed rgba(255,0,120,.85)}
.guide .ringline{position:absolute;left:0;right:0;top:15mm;border-top:.3mm dashed rgba(0,120,255,.9)}
.guide .hole{position:absolute;width:6mm;height:6mm;border-radius:50%;top:6.5mm;
  border:.35mm solid rgba(255,0,120,.95);background:rgba(255,0,120,.10)}
.guide .lab{position:absolute;font:700 2.1mm/1.5 'Noto Sans';color:#C2185B;letter-spacing:.1mm;background:rgba(255,255,255,.93);padding:.6mm 1.4mm;border-radius:.8mm;border:.15mm solid rgba(255,0,120,.55)}
"""


def guide_overlay(n_holes: int = 6, pitch: float | None = None) -> str:
    margin = 25.0
    if pitch is None:
        pitch = (D.W - 2 * margin) / (n_holes - 1)
    holes = "".join(
        f'<div class="hole" style="left:{margin + i * pitch - 3:.2f}mm"></div>'
        for i in range(n_holes)
    )
    labels = ""
    return f"""<div class="guide">
  <div class="ringline"></div><div class="safe"></div>{holes}{labels}
  <div class="lab" style="left:6mm;top:16.4mm">AREA AMAN ISI &mdash; 6 mm dari tepi potong</div>

  <div class="lab" style="right:6mm;bottom:1.5mm">TRIM 213 &times; 152 mm &nbsp;|&nbsp; 6 ring &Oslash;6 mm &nbsp;|&nbsp; pitch {pitch:.1f} mm</div>
  <div class="lab" style="left:6mm;top:1.2mm">AREA JILID / RING &mdash; 15 mm (bebas teks)</div>
</div>"""


def main() -> None:
    # 1) HTML + PDF versi final (trim) & versi bleed 3 mm
    for pad, suf in ((0.0, "trim"), (3.0, "bleed3mm")):
        html = D.build_html(pad)
        hp = html_file(f"kalender-mitra-syariah-2027-{suf}.html", html)
        w, h, n = to_pdf(hp, OUT / f"kalender-mitra-syariah-2027-{suf}.pdf")
        print(f"PDF {suf:9s}: {w:.2f} x {h:.2f} mm, {n} halaman")

    # 2) preview PNG per halaman
    pages = [("1-halaman-depan", D.page_cover, "cover"),
             ("2-januari-2027", D.page_month, "month"),
             ("3-halaman-belakang", D.page_back, "back")]
    for nama, fn, cls in pages:
        body = fn()
        html = ("<!DOCTYPE html><html lang='id'><head><meta charset='utf-8'>"
                f"<style>{D.build_css(0)}</style></head><body>{body}</body></html>")
        hp = html_file(f"_preview-{nama}.html", html)
        to_png(hp, OUT / f"preview-{nama}.png")
        print("PNG preview:", f"preview-{nama}.png")

    # 3) halaman panduan cetak (posisi ring + area aman)
    html = ("<!DOCTYPE html><html lang='id'><head><meta charset='utf-8'>"
            f"<style>{D.build_css(0)}{GUIDE_CSS}</style></head>"
            f"<body>{D.page_month()}{guide_overlay(6)}</body></html>")
    hp = html_file("_panduan.html", html)
    to_png(hp, OUT / "preview-panduan-cetak-ring.png")
    print("PNG preview: preview-panduan-cetak-ring.png")


if __name__ == "__main__":
    main()
