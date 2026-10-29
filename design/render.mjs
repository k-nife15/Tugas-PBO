// Render semua SVG master di dist/ -> PNG (1x/2x/4x) memakai resvg (tanpa browser)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DIST = path.join(__dirname, 'dist');
const FONTS = path.join(__dirname, 'assets', 'fonts');

const fontFiles = fs.readdirSync(FONTS)
  .filter((f) => f.endsWith('.ttf'))
  .map((f) => path.join(FONTS, f));

const svgs = fs.readdirSync(DIST).filter((f) => f.endsWith('.svg'));
if (!svgs.length) {
  console.error('Tidak ada SVG di dist/. Jalankan generate.py / generate_elegant.py dulu.');
  process.exit(1);
}

for (const file of svgs) {
  const base = file.replace(/\.svg$/, '');
  const svg = fs.readFileSync(path.join(DIST, file));
  for (const scale of [1, 2, 4]) {
    const resvg = new Resvg(svg, {
      fitTo: { mode: 'zoom', value: scale },
      background: '#FFFFFF',
      font: { fontFiles, loadSystemFonts: false, defaultFontFamily: 'Poppins' },
    });
    const png = resvg.render();
    const name = scale === 1 ? `${base}.png` : `${base}@${scale}x.png`;
    fs.writeFileSync(path.join(DIST, name), png.asPng());
    console.log(`${name} -> ${png.width}x${png.height}`);
  }
}
