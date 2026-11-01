"""Probe: cek dukungan cairosvg terhadap fitur yang akan dipakai di artwork."""
import cairosvg

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="120mm" height="60mm" viewBox="0 0 120 60">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0E5241"/><stop offset="1" stop-color="#062B22"/>
  </linearGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#B8862B"/><stop offset="0.35" stop-color="#F4DFA0"/>
    <stop offset="0.6" stop-color="#C9A227"/><stop offset="1" stop-color="#F0DCA8"/>
  </linearGradient>
  <clipPath id="cp"><rect x="10" y="30" width="100" height="24" rx="4"/></clipPath>
</defs>
<rect width="120" height="60" fill="url(#g)"/>
<g clip-path="url(#cp)"><rect x="0" y="0" width="120" height="60" fill="#ffffff" opacity="0.08"/></g>
<text x="10" y="14" font-family="Playfair Display" font-size="9" fill="#F2E8D5">Playfair Regular Tumbuh</text>
<text x="10" y="24" font-family="Playfair Display" font-weight="bold" font-size="9" fill="#F2E8D5">Playfair Bold Tumbuh</text>
<text x="10" y="34" font-family="Playfair Display SemiBold" font-size="9" fill="url(#gold)">Playfair SemiBold Gold 2027</text>
<text x="10" y="44" font-family="Montserrat" font-size="6" letter-spacing="1.2" fill="#DCEFE7">MONTSERRAT TRACKING 1.2</text>
<text x="10" y="52" font-family="Montserrat" font-weight="bold" font-size="6" fill="#DCEFE7">Montserrat Bold</text>
<text x="10" y="58" font-family="Montserrat Light" font-size="6" fill="#A8E0CD">Montserrat Light 300</text>
<circle cx="100" cy="20" r="10" fill="none" stroke="url(#gold)" stroke-width="0.4" stroke-dasharray="1.5 1"/>
</svg>"""

cairosvg.svg2png(bytestring=SVG.encode(), write_to="/tmp/probe.png", scale=6)
cairosvg.svg2pdf(bytestring=SVG.encode(), write_to="/tmp/probe.pdf")
print("rendered ok")
