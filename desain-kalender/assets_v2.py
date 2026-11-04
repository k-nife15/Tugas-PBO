"""Aset vektor untuk arah desain v2 'Editorial Mihrab' (garis tipis / line-art)."""

from __future__ import annotations

PAPER = "#FBF9F4"
INK = "#10202E"
TEAL = "#0C4F45"
TEAL_L = "#12796A"
GOLD = "#B99154"
GOLD_L = "#D8BE8A"
SAND = "#EFE7D7"
RED = "#A6432F"


def logo(prefix: str, size_mm: float = 10, dark: bool = False) -> str:
    """Logo garis: cincin + bulan sabit emas + bintang."""
    ring = GOLD_L if dark else TEAL
    return f"""<svg class="mkl" style="width:{size_mm}mm;height:{size_mm}mm" viewBox="0 0 100 100">
  <defs><mask id="lm{prefix}"><rect width="100" height="100" fill="#fff"/>
    <circle cx="61" cy="43" r="21" fill="#000"/></mask></defs>
  <circle cx="50" cy="50" r="46.5" fill="none" stroke="{ring}" stroke-width="2.6"/>
  <circle cx="45" cy="48" r="25" fill="{GOLD}" mask="url(#lm{prefix})"/>
  <path d="M67 60l2.4 6 6 2.4-6 2.4-2.4 6-2.4-6-6-2.4 6-2.4z" fill="{GOLD}"/>
</svg>"""


def wordmark(prefix: str, size_mm: float = 10, dark: bool = False) -> str:
    ink = PAPER if dark else INK
    mut = "rgba(255,255,255,.62)" if dark else "rgba(16,32,46,.55)"
    return f"""<div class="wm2">
  {logo(prefix, size_mm, dark)}
  <div class="wm2t">
    <div class="wm2a" style="color:{mut}">BPR SYARIAH</div>
    <div class="wm2b" style="color:{ink}">mitra syariah</div>
    <div class="wm2c" style="color:{mut}">Mitra Mentari Sejahtera</div>
  </div>
</div>"""


def arch(prefix: str, w_mm: float, h_mm: float, rosette: bool = True, label: str = "") -> str:
    """Lengkung mihrab garis emas + rosetta bintang 8."""
    ros = ""
    if rosette:
        ros = f"""<g stroke="{GOLD}" stroke-width=".7" fill="none" opacity=".85">
      <circle cx="50" cy="86" r="20"/>
      <path d="M50 62 L67 86 L50 110 L33 86 Z"/>
      <path d="M50 62 L67 86 L50 110 L33 86 Z" transform="rotate(45 50 86)"/>
      <circle cx="50" cy="86" r="4.4"/>
    </g>"""
    return f"""<svg class="arch" style="width:{w_mm}mm;height:{h_mm}mm" viewBox="0 0 100 160">
  <g fill="none" stroke="{GOLD}" stroke-width=".9">
    <path d="M12 158V66c0-21 17-38 38-38s38 17 38 38v92"/>
    <path d="M19 158V67c0-17 14-31 31-31s31 14 31 31v91" opacity=".55"/>
    <path d="M4 158h92" opacity=".8"/>
  </g>
  <circle cx="50" cy="22" r="2.2" fill="{GOLD}"/>
  {ros}
  <text x="50" y="144" text-anchor="middle" fill="{GOLD}" font-family="Noto Naskh Arabic"
        font-size="12" opacity=".9">{label}</text>
</svg>"""


def kaaba_line(prefix: str, w_mm: float, h_mm: float) -> str:
    """Ka'bah line-art sederhana di dalam lengkung mihrab."""
    dots = "".join(f'<circle cx="{x}" cy="102.8" r=".8"/>' for x in (38, 44, 51, 58, 64))
    return f"""<svg class="kab" style="width:{w_mm}mm;height:{h_mm}mm" viewBox="0 0 100 160">
  <g fill="none" stroke="{GOLD}" stroke-width=".9">
    <path d="M10 158V64c0-22 18-40 40-40s40 18 40 40v94"/>
    <path d="M18 158V65c0-17 14-31 32-31s32 14 32 31v93" opacity=".4"/>
    <path d="M12 136h76" opacity=".45"/>
  </g>
  <g fill="none" stroke="{GOLD_L}" stroke-width="1">
    <path d="M33 92h34v32H33z"/>
    <path d="M33 92l6-6h34l-6 6"/>
    <path d="M67 92l6-6v32l-6 6"/>
    <path d="M33 100h34"/>
    <path d="M39 94h34" opacity=".55"/>
  </g>
  <g fill="{GOLD}">{dots}</g>
  <g stroke="{GOLD}" stroke-width=".85" fill="none" opacity=".85">
    <path d="M55 104h9M55 104v21M64 104v21"/>
  </g>
  <path d="M29 124h48" stroke="{GOLD}" stroke-width="1" opacity=".8"/>
  <text x="50" y="150" text-anchor="middle" fill="{GOLD}" font-family="Noto Naskh Arabic"
        font-size="10.5" opacity=".85">١٤٤٨ هـ</text>
</svg>"""


def sparkle(size_mm: float = 3.2, color: str = GOLD) -> str:
    return (f'<svg style="width:{size_mm}mm;height:{size_mm}mm" viewBox="0 0 20 20">'
            f'<path d="M10 1l1.6 6.6L18 10l-6.4 2.4L10 19 8.4 12.4 2 10l6.4-2.4z" fill="{color}"/>'
            '</svg>')
