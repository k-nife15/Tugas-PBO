"""build.py — Render semua artwork ke SVG, PNG preview, dan PDF cetak."""
from __future__ import annotations

import os
import sys

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
PREVIEW = os.path.join(ROOT, "preview")
sys.path.insert(0, HERE)

import front_cover  # noqa: E402
import back_cover   # noqa: E402
import spec_sheet   # noqa: E402

# 96 dpi * 4 = 384 dpi preview (cukup tajam, file tetap ringan)
SCALE = 4.0


def emit(name: str, svg: str, dpi_scale: float = SCALE) -> None:
    svg_path = os.path.join(ASSETS, f"{name}.svg")
    png_path = os.path.join(PREVIEW, f"{name}.png")
    pdf_path = os.path.join(PREVIEW, f"{name}.pdf")
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=png_path,
                     scale=dpi_scale)
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=pdf_path)
    print(f"  ✓ {name}: svg + png({dpi_scale:g}x) + pdf")


def main() -> None:
    os.makedirs(ASSETS, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    print("Render artwork kalender …")
    emit("01-cover-depan", front_cover.build())
    emit("02-cover-belakang", back_cover.build())
    emit("03-panduan-teknis", spec_sheet.build(), 3.0)
    print("Selesai.")


if __name__ == "__main__":
    main()
