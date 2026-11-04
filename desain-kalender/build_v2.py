"""Build output desain v2 'Editorial Mihrab': PDF + preview PNG."""

from __future__ import annotations

import pathlib
import re
import subprocess

import design_v2 as D

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "output" / "v2"
OUT.mkdir(parents=True, exist_ok=True)
PX = 96 / 25.4


def _chrome(*args: str) -> None:
    cmd = ["chromium", "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
           "--force-color-profile=srgb", "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=8000", *args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-600:])


def html(name: str, body: str, extra_css: str = "", pad: float = 0.0) -> pathlib.Path:
    p = OUT / name
    p.write_text("<!DOCTYPE html><html lang='id'><head><meta charset='utf-8'>"
                 f"<style>{D.build_css(pad)}{extra_css}</style></head><body>{body}</body></html>",
                 encoding="utf-8")
    return p


def pdf(src: pathlib.Path, dst: pathlib.Path):
    _chrome("--no-pdf-header-footer", f"--print-to-pdf={dst}", f"file://{src}")
    raw = dst.read_bytes()
    box = [float(x) for x in re.search(rb"MediaBox\s*\[([^\]]*)\]", raw).group(1).split()]
    n = len(re.findall(rb"/Type\s*/Page[^s]", raw))
    return box[2] / 72 * 25.4, box[3] / 72 * 25.4, n


def png(src: pathlib.Path, dst: pathlib.Path):
    w, h = round(D.W * PX), round(D.H * PX)
    _chrome("--force-device-scale-factor=2", f"--window-size={w},{h}",
            f"--screenshot={dst}", f"file://{src}")


GUIDE = """
.gd{position:absolute;inset:0;pointer-events:none;z-index:99}
.gd .safe{position:absolute;left:5mm;right:5mm;top:18mm;bottom:5mm;border:.3mm dashed rgba(214,0,90,.8)}
.gd .ring{position:absolute;left:0;right:0;top:14mm;border-top:.3mm dashed rgba(0,110,200,.85)}
.gd .hole{position:absolute;width:6mm;height:6mm;border-radius:50%;top:6.5mm;
  border:.35mm solid rgba(214,0,90,.95);background:rgba(214,0,90,.10)}
.gd .lab{position:absolute;font:700 2mm/1.5 'Noto Sans';color:#B00050;background:rgba(255,255,255,.94);
  padding:.6mm 1.4mm;border-radius:.7mm;border:.15mm solid rgba(214,0,90,.5)}
"""


def guides() -> str:
    m, n = 25.0, 6
    pitch = (D.W - 2 * m) / (n - 1)
    holes = "".join(f'<div class="hole" style="left:{m + i * pitch - 3:.2f}mm"></div>' for i in range(n))
    return (f'<div class="gd"><div class="ring"></div><div class="safe"></div>{holes}'
            f'<div class="lab" style="left:12mm;top:1.2mm">AREA RING 14 mm &mdash; bebas teks</div>'
            f'<div class="lab" style="left:12mm;top:15.2mm">AREA AMAN ISI 5 mm</div>'
            f'<div class="lab" style="right:12mm;bottom:1.4mm">TRIM 213 &times; 152 mm &nbsp;|&nbsp;'
            f'6 ring &Oslash;6 mm &nbsp;|&nbsp; pitch {pitch:.1f} mm</div></div>')


def main() -> None:
    for pad, suf in ((0.0, "trim"), (3.0, "bleed3mm")):
        p = html(f"kalender-2027-v2-{suf}.html", D.build_html(pad), pad=pad)
        w, h, n = pdf(p, OUT / f"kalender-2027-v2-{suf}.pdf")
        print(f"PDF {suf:9s}: {w:.2f} x {h:.2f} mm, {n} halaman")

    for nama, fn in (("1-sampul-depan", D.page_cover), ("2-januari-2027", D.page_month),
                     ("3-sampul-belakang", D.page_back)):
        png(html(f"_p-{nama}.html", fn()), OUT / f"preview-v2-{nama}.png")
        print("PNG", f"preview-v2-{nama}.png")

    png(html("_p-guide.html", D.page_month() + guides(), GUIDE), OUT / "preview-v2-panduan-ring.png")
    print("PNG  preview-v2-panduan-ring.png")


if __name__ == "__main__":
    main()
