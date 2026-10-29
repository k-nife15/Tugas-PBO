#!/usr/bin/env python3
"""Ekspor PDF siap cetak dari PNG 4x.

Kanvas desain 794x559 px = A5 landscape pada 96 dpi (210 x 148 mm).
Pada 4x (3176x2236 px) ekuivalen 384 dpi -> cetak tajam tanpa upscaling.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
SRC = DIST / "kalender-januari-2027-playful@4x.png"
OUT = DIST / "kalender-januari-2027-playful-A5.pdf"

DPI = 384.0
img = Image.open(SRC).convert("RGB")
img.save(OUT, "PDF", resolution=DPI)
print(f"{OUT.name} -> {img.width}x{img.height}px @{DPI:.0f}dpi "
      f"({img.width / DPI * 25.4:.0f}x{img.height / DPI * 25.4:.0f} mm)")
