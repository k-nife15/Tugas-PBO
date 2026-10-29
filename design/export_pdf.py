#!/usr/bin/env python3
"""Ekspor PDF siap cetak dari semua PNG 4x di dist/.

Kanvas desain 794x559 px = A5 landscape pada 96 dpi (210 x 148 mm).
Pada 4x (3176x2236 px) ekuivalen 384 dpi -> cetak tajam tanpa upscaling.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
DPI = 384.0

for src in sorted(DIST.glob("*@4x.png")):
    img = Image.open(src).convert("RGB")
    out = DIST / (src.name.replace("@4x.png", "-A5.pdf"))
    img.save(out, "PDF", resolution=DPI)
    print(f"{out.name} <- {src.name} | {img.width}x{img.height}px @{DPI:.0f}dpi "
          f"({img.width / DPI * 25.4:.0f}x{img.height / DPI * 25.4:.0f} mm)")
