"""Aset visual vektor (SVG) untuk desain kalender.

Semua fungsi mengembalikan string SVG siap-tempel (inline). Prefix id dipakai
agar id gradient/pattern antar halaman tidak saling bentrok.
"""

from __future__ import annotations

NAVY = "#0A2A52"
NAVY_D = "#061C38"
BLUE = "#1A6BB0"
TEAL = "#0B6E5F"
GREEN = "#12886F"
GOLD = "#C6A15B"
GOLD_L = "#E7CE93"


# --------------------------------------------------------------------------- #
# Logo & wordmark
# --------------------------------------------------------------------------- #
def logo_mark(prefix: str, size_mm: float, on_dark: bool = False) -> str:
    """Simbol bank: lingkaran gradasi + bulan sabit putih + bintang emas."""
    ring = "rgba(255,255,255,.38)" if on_dark else "rgba(255,255,255,.55)"
    return f"""<svg class="mark" style="width:{size_mm}mm;height:{size_mm}mm" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="mk{prefix}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{GREEN}"/><stop offset=".55" stop-color="{TEAL}"/>
      <stop offset="1" stop-color="{BLUE}"/>
    </linearGradient>
    <linearGradient id="mg{prefix}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GOLD_L}"/><stop offset="1" stop-color="{GOLD}"/>
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="49" fill="url(#mk{prefix})"/>
  <circle cx="50" cy="50" r="43" fill="none" stroke="{ring}" stroke-width="1.6"/>
  <mask id="lm{prefix}"><rect width="100" height="100" fill="#fff"/>
    <circle cx="66" cy="50" r="27" fill="#000"/></mask>
  <circle cx="46" cy="50" r="29" fill="#fff" mask="url(#lm{prefix})"/>
  <path d="M71 39l3.6 9 9 3.6-9 3.6-3.6 9-3.6-9-9-3.6 9-3.6z"
        fill="url(#mg{prefix})"/>
</svg>"""


def wordmark(prefix: str, size_mm: float = 11, dark: bool = False) -> str:
    """Logo lengkap: simbol + teks 'mitra syariah'."""
    c_mitra = GOLD_L if dark else GREEN
    c_syariah = "#FFFFFF" if dark else NAVY
    c_top = "rgba(255,255,255,.62)" if dark else "#6C8093"
    return f"""<div class="wordmark" style="--mk:{size_mm}mm">
  {logo_mark(prefix, size_mm, on_dark=dark)}
  <div class="wm-txt">
    <div class="wm-top" style="color:{c_top}">BPR SYARIAH</div>
    <div class="wm-name"><span style="color:{c_mitra}">mitra</span><span style="color:{c_syariah}"> syariah</span></div>
    <div class="wm-sub" style="color:{c_top}">Mitra Mentari Sejahtera</div>
  </div>
</div>"""


# --------------------------------------------------------------------------- #
# Pola geometri Islami (tessellation bintang 8)
# --------------------------------------------------------------------------- #
def pattern(prefix: str, color: str = "#FFFFFF", opacity: float = 0.14,
            unit: int = 46) -> str:
    """Overlay pola garis bintang-delapan (khatam) di atas latar."""
    u = unit
    h = u / 2
    return f"""<svg class="pat"
     style="position:absolute;inset:0;width:100%;height:100%;display:block">
  <defs>
    <pattern id="pt{prefix}" width="{u}" height="{u}" patternUnits="userSpaceOnUse">
      <g fill="none" stroke="{color}" stroke-width="0.9" opacity="{opacity}">
        <path d="M{h} 4 L{u-4} {h} L{h} {u-4} L4 {h} Z"/>
        <path d="M{h} 4 L{u-4} {h} L{h} {u-4} L4 {h} Z" transform="rotate(45 {h} {h})"/>
        <circle cx="{h}" cy="{h}" r="2.2"/>
        <circle cx="0" cy="0" r="2.2"/><circle cx="{u}" cy="0" r="2.2"/>
        <circle cx="0" cy="{u}" r="2.2"/><circle cx="{u}" cy="{u}" r="2.2"/>
      </g>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#pt{prefix})"/>
</svg>"""


# --------------------------------------------------------------------------- #
# Ikon kecil (stroke memakai currentColor)
# --------------------------------------------------------------------------- #
def icon(name: str, size_mm: float = 3.0, sw: float = 1.6) -> str:
    paths = {
        "check": '<path d="M4 12.5l5 5L20 6.5"/>',
        "phone": '<path d="M6 3h3l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2A2 2 0 0 1 6 3z"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14 0 18M12 3c-3 3.5-3 14 0 18"/>',
        "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
        "plane": '<path d="M2 13.5l20-8-8 20-3-8-9-4z"/>',
        "star": '<path d="M12 2.5l2.9 6.2 6.6.9-4.8 4.7 1.2 6.7-5.9-3.2-5.9 3.2 1.2-6.7L2.5 9.6l6.6-.9z"/>',
        "wallet": '<rect x="3" y="6" width="18" height="13" rx="2.5"/><path d="M3 10h18M16.5 14.5h2"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 7.7-8 9-4.5-1.3-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-4.5"/>',
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M7.5 14h3v3h-3z"/>',
        "scissors": '<circle cx="6" cy="6" r="2.6"/><circle cx="6" cy="18" r="2.6"/><path d="M8 8l12 10M8 16L20 6"/>',
    }
    return (f'<svg class="ico" style="width:{size_mm}mm;height:{size_mm}mm" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round">{paths[name]}</svg>')


# --------------------------------------------------------------------------- #
# Medali (halaman depan)
# --------------------------------------------------------------------------- #
def medallion(prefix: str, size_mm: float = 88) -> str:
    """Medali emas: cincin ganda + bintang 8 + bulan sabit + tahun Hijriah."""
    return f"""<svg class="medal" style="width:{size_mm}mm;height:{size_mm}mm" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="md{prefix}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F7EAC8"/><stop offset=".42" stop-color="{GOLD_L}"/>
      <stop offset="1" stop-color="#9C7B32"/>
    </linearGradient>
    <radialGradient id="mg2{prefix}" cx=".46" cy=".38" r=".68">
      <stop offset="0" stop-color="#1C8C74" stop-opacity=".95"/>
      <stop offset=".62" stop-color="#0C4E63" stop-opacity=".95"/>
      <stop offset="1" stop-color="#061E38" stop-opacity=".97"/>
    </radialGradient>
    <mask id="cr{prefix}">
      <rect width="200" height="200" fill="#fff"/>
      <circle cx="116" cy="96" r="37" fill="#000"/>
    </mask>
  </defs>
  <circle cx="100" cy="100" r="97" fill="url(#mg2{prefix})"/>
  <circle cx="100" cy="100" r="97" fill="none" stroke="url(#md{prefix})" stroke-width="1.7"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="url(#md{prefix})" stroke-width=".7" opacity=".8"/>
  <g stroke="url(#md{prefix})" fill="none" opacity=".38">
    <path d="M100 26 L174 100 L100 174 L26 100 Z" stroke-width=".6"/>
    <path d="M100 26 L174 100 L100 174 L26 100 Z" stroke-width=".6" transform="rotate(45 100 100)"/>
    <circle cx="100" cy="100" r="70" stroke-width=".5"/>
  </g>
  <circle cx="98" cy="96" r="41" fill="url(#md{prefix})" mask="url(#cr{prefix})"/>
  <path d="M133 58l3.4 8.6 8.6 3.4-8.6 3.4-3.4 8.6-3.4-8.6-8.6-3.4 8.6-3.4z"
        fill="url(#md{prefix})"/>
  <rect x="57" y="144" width="86" height="25" rx="12.5" fill="#04182C" opacity=".62"
        stroke="url(#md{prefix})" stroke-width=".7"/>
  <text x="100" y="162.5" text-anchor="middle" fill="url(#md{prefix})"
        font-family="Noto Sans Arabic" font-size="15">١٤٤٨ هـ</text>
</svg>"""


# --------------------------------------------------------------------------- #
# Ilustrasi halaman belakang: langit malam, masjid, Ka'bah, pesawat
# --------------------------------------------------------------------------- #
def kaaba_scene(prefix: str, w_mm: float, h_mm: float) -> str:
    """Panorama malam: langit, bulan, masjid, Ka'bah, dan pesawat."""
    return f"""<svg class="scene" style="width:{w_mm}mm;height:{h_mm}mm" viewBox="0 0 172 208">
  <defs>
    <linearGradient id="sky{prefix}" x1="0" y1="0" x2=".12" y2="1">
      <stop offset="0" stop-color="#04182F"/><stop offset=".38" stop-color="#0A3B5C"/>
      <stop offset=".72" stop-color="#0B635F"/><stop offset="1" stop-color="#12886F"/>
    </linearGradient>
    <radialGradient id="glow{prefix}" cx=".76" cy=".18" r=".46">
      <stop offset="0" stop-color="{GOLD_L}" stop-opacity=".20"/>
      <stop offset="1" stop-color="{GOLD_L}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="floor{prefix}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F1EBDC"/><stop offset=".55" stop-color="#E2D9C3"/>
      <stop offset="1" stop-color="#CFC4A9"/>
    </linearGradient>
    <linearGradient id="gld{prefix}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8E6F2E"/><stop offset=".45" stop-color="{GOLD_L}"/>
      <stop offset="1" stop-color="#8E6F2E"/>
    </linearGradient>
    <radialGradient id="kb{prefix}" cx=".5" cy=".55" r=".5">
      <stop offset="0" stop-color="{GOLD_L}" stop-opacity=".34"/>
      <stop offset="1" stop-color="{GOLD_L}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="shd{prefix}" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#0A2033" stop-opacity=".34"/>
      <stop offset="1" stop-color="#0A2033" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="lgt{prefix}" cx=".5" cy=".42" r=".55">
      <stop offset="0" stop-color="#FFFDF4" stop-opacity=".85"/>
      <stop offset="1" stop-color="#FFFDF4" stop-opacity="0"/>
    </radialGradient>
    <mask id="moon{prefix}">
      <rect width="172" height="208" fill="#fff"/>
      <circle cx="55" cy="34" r="13" fill="#000"/>
    </mask>
    <clipPath id="clip{prefix}"><rect x="0" y="0" width="172" height="208" rx="7"/></clipPath>
  </defs>
  <g clip-path="url(#clip{prefix})">
    <rect width="172" height="208" fill="url(#sky{prefix})"/>
    <rect width="172" height="208" fill="url(#glow{prefix})"/>
    <g fill="#fff" opacity=".72">
      <circle cx="22" cy="26" r="1.1"/><circle cx="44" cy="14" r=".8"/>
      <circle cx="72" cy="30" r=".7"/><circle cx="104" cy="18" r="1"/>
      <circle cx="128" cy="44" r=".8"/><circle cx="16" cy="56" r=".7"/>
      <circle cx="90" cy="52" r=".6"/><circle cx="38" cy="74" r=".6"/>
      <circle cx="150" cy="30" r=".9"/><circle cx="62" cy="94" r=".5"/>
      <circle cx="120" cy="86" r=".6"/>
    </g>
    <circle cx="46" cy="36" r="15" fill="url(#gld{prefix})" mask="url(#moon{prefix})"/>
    <path d="M12 148C48 128 84 104 112 76" fill="none" stroke="{GOLD_L}"
          stroke-width="1.2" stroke-dasharray="5 4" opacity=".6"/>
    <g transform="translate(112 76) rotate(56) scale(.9)" fill="{GOLD_L}" opacity=".95">
      <path d="M0-10l2.6 7.8L10 1.4v2L2.6 1.6V7l2.8 1.8v1.6L0 9l-5.4 1.4v-1.6L-2.6 7V1.6L-10 3.4v-2l7.4-3.8z"/>
    </g>
    <!-- siluet masjid -->
    <g fill="#062B45">
      <rect x="0" y="126" width="172" height="30"/>
      <path d="M56 126a30 30 0 0 1 60 0z"/>
      <path d="M18 126a16 16 0 0 1 32 0z"/>
      <path d="M122 126a16 16 0 0 1 32 0z"/>
      <rect x="10" y="92" width="8" height="34"/>
      <path d="M10 92a4 4 0 0 1 8 0z"/>
      <rect x="154" y="100" width="8" height="26"/>
      <path d="M154 100a4 4 0 0 1 8 0z"/>
    </g>
    <g stroke="url(#gld{prefix})" fill="none" stroke-width=".8" opacity=".5">
      <path d="M56 126a30 30 0 0 1 60 0"/><path d="M18 126a16 16 0 0 1 32 0"/>
      <path d="M122 126a16 16 0 0 1 32 0"/>
    </g>
    <!-- lantai marmer -->
    <rect x="0" y="156" width="172" height="52" fill="url(#floor{prefix})"/>
    <rect x="0" y="156" width="172" height="52" fill="url(#lgt{prefix})" opacity=".55"/>
    <g stroke="#B3A78C" opacity=".28" stroke-width=".5">
      <path d="M0 172h172M0 190h172"/>
    </g>
    <ellipse cx="86" cy="150" rx="58" ry="40" fill="url(#kb{prefix})"/>
    <ellipse cx="86" cy="172" rx="30" ry="6.5" fill="url(#shd{prefix})"/>
    <!-- ka'bah -->
    <g>
      <rect x="66" y="122" width="40" height="48" fill="#0B1016"/>
      <rect x="66" y="122" width="40" height="48" fill="none" stroke="#2A343E" stroke-width=".8"/>
      <rect x="66" y="130" width="40" height="5.6" fill="url(#gld{prefix})"/>
      <g fill="#0B1016" opacity=".35">
        <circle cx="74" cy="132.8" r=".65"/><circle cx="80" cy="132.8" r=".65"/>
        <circle cx="92" cy="132.8" r=".65"/><circle cx="98" cy="132.8" r=".65"/>
      </g>
      <rect x="81" y="135.6" width="7" height="34.4" fill="url(#gld{prefix})" opacity=".9"/>
      <path d="M66 122h40l-4-4H70z" fill="#1B242E"/>
    </g>
    <g fill="#fff" opacity=".08">
      <ellipse cx="24" cy="196" rx="30" ry="7"/><ellipse cx="150" cy="192" rx="26" ry="6"/>
    </g>
  </g>
  <rect x=".8" y=".8" width="170.4" height="206.4" rx="7" fill="none"
        stroke="url(#gld{prefix})" stroke-width="1.5"/>
</svg>"""
