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
import month_page   # noqa: E402

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


def pair_preview(name: str, items: list[tuple[str, str]]) -> None:
    """Gabungkan dua halaman jadi satu lembar presentasi."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

    imgs = [(Image.open(os.path.join(PREVIEW, f"{n}.png")), lab)
            for n, lab in items]
    gap, pad, cap = 150, 170, 190
    W = pad * 2 + sum(i.width for i, _ in imgs) + gap * (len(imgs) - 1)
    H = pad * 2 + max(i.height for i, _ in imgs) + cap
    sheet = Image.new("RGB", (W, H), "#EDEAE3")
    draw = ImageDraw.Draw(sheet)

    def font(size):
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        return ImageFont.truetype(path, size) if os.path.exists(path) \
            else ImageFont.load_default()

    x = pad
    for img, label in imgs:
        y = pad
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
        x += img.width + gap

    out = os.path.join(PREVIEW, f"{name}.png")
    sheet.resize((W // 2, H // 2), Image.LANCZOS).save(out, optimize=True)
    print(f"  ✔ {name}.png")


def main() -> None:
    os.makedirs(ASSETS, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    print("Render artwork kalender …")
    emit("01-cover-depan", front_cover.build())
    emit("02-cover-belakang", back_cover.build())
    emit("03-panduan-teknis", spec_sheet.build(), 3.0)
    emit("04-januari-depan", month_page.build_front())
    emit("05-januari-belakang", month_page.build_back())
    pair_preview("00-pasangan-cover",
                 [("01-cover-depan", "COVER DEPAN"),
                  ("02-cover-belakang", "COVER BELAKANG")])
    pair_preview("06-pasangan-januari",
                 [("04-januari-depan", "JANUARI 2027 — SISI DEPAN"),
                  ("05-januari-belakang", "JANUARI 2027 — SISI BELAKANG")])
    print("Selesai.")


if __name__ == "__main__":
    main()

