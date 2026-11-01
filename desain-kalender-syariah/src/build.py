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

SCALE = 4.0      # ~384 dpi untuk preview PNG


def emit(name: str, svg: str, dpi_scale: float = SCALE) -> None:
    svg_path = os.path.join(ASSETS, f"{name}.svg")
    png_path = os.path.join(PREVIEW, f"{name}.png")
    pdf_path = os.path.join(PREVIEW, f"{name}.pdf")
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=png_path,
                     scale=dpi_scale)
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=pdf_path)
    print(f"  ✔ {name}: svg + png({dpi_scale:g}x) + pdf")


def pair_preview() -> None:
    """Gabungkan cover depan & belakang jadi satu lembar presentasi."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

    front = Image.open(os.path.join(PREVIEW, "01-cover-depan.png"))
    back = Image.open(os.path.join(PREVIEW, "02-cover-belakang.png"))
    gap, pad, cap = 150, 170, 190
    W = pad * 2 + front.width * 2 + gap
    H = pad * 2 + front.height + cap
    sheet = Image.new("RGB", (W, H), "#EDEAE3")
    draw = ImageDraw.Draw(sheet)

    def font(size):
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        return ImageFont.truetype(path, size) if os.path.exists(path) \
            else ImageFont.load_default()

    for i, (img, label) in enumerate(
            ((front, "COVER DEPAN"), (back, "COVER BELAKANG"))):
        x = pad + i * (front.width + gap)
        y = pad
        # bayangan lembut di bawah artwork
        shadow = Image.new("RGBA", (img.width + 80, img.height + 80),
                           (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rectangle(
            [40, 52, 40 + img.width, 52 + img.height], fill=(20, 30, 26, 90))
        shadow = shadow.filter(ImageFilter.GaussianBlur(28))
        sheet.paste(Image.new("RGB", shadow.size, "#2A2A28"), (x - 40, y - 40),
                    shadow.split()[3])
        sheet.paste(img, (x, y))
        f = font(54)
        tw = draw.textlength(label, font=f)
        draw.text((x + (img.width - tw) / 2, y + img.height + 56), label,
                  font=f, fill="#0E5241")

    out = os.path.join(PREVIEW, "00-pasangan-cover.png")
    sheet.resize((W // 2, H // 2), Image.LANCZOS).save(out, optimize=True)
    print("  ✔ 00-pasangan-cover.png")


def main() -> None:
    os.makedirs(ASSETS, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    print("Render artwork kalender …")
    emit("01-cover-depan", front_cover.build())
    emit("02-cover-belakang", back_cover.build())
    emit("03-panduan-teknis", spec_sheet.build(), 3.0)
    pair_preview()
    print("Selesai.")


if __name__ == "__main__":
    main()

