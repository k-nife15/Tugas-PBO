#!/usr/bin/env python3
"""Ekspor PDF siap cetak dari PNG master (4x untuk kanvas kecil, 2x untuk kanvas besar).

Ukuran fisik diturunkan dari kanvas desain:
  kalender-2027-*  ->  2130 px = 213 mm (21,3 x 15,2 cm)
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

# prefix nama file -> (lebar kanvas px, lebar fisik mm)
SIZES = {
    "kalender-2027": (2130, 213.0),
}


def size_of(name):
    for prefix, spec in SIZES.items():
        if name.startswith(prefix):
            return spec
    return None


def main():
    for base_svg in sorted(DIST.glob("*.svg")):
        base = base_svg.stem
        spec = size_of(base)
        if not spec:
            continue
        canvas_px, mm = spec
        src = next((DIST / f"{base}{sfx}.png" for sfx in ("@4x", "@2x")
                    if (DIST / f"{base}{sfx}.png").exists()), None)
        if not src:
            print("skip (no PNG):", base)
            continue
        img = Image.open(src).convert("RGB")
        dpi = img.width / mm * 25.4
        out = DIST / f"{base}-print.pdf"
        img.save(out, "PDF", resolution=dpi)
        print(f"{out.name} <- {src.name} | {img.width}x{img.height}px "
              f"@{dpi:.0f}dpi ({mm:.0f}x{img.height / dpi * 25.4:.0f} mm)")

    # --- gabungan 2 halaman (depan + belakang) untuk percetakan bolak-balik
    front = DIST / "kalender-2027-biru-hijau-emas@2x.png"
    back = DIST / "kalender-2027-biru-hijau-emas-belakang@2x.png"
    if front.exists() and back.exists():
        pages = [Image.open(p).convert("RGB") for p in (front, back)]
        dpi = pages[0].width / 213.0 * 25.4
        out = DIST / "kalender-2027-cetak-2halaman.pdf"
        pages[0].save(out, "PDF", resolution=dpi, save_all=True,
                      append_images=pages[1:])
        print(f"{out.name} <- 2 halaman (depan + belakang) @{dpi:.0f}dpi")


if __name__ == "__main__":
    main()
