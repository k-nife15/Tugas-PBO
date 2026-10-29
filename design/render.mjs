// Render SVG master -> PNG (1x/2x/4x) memakai resvg (pure render, tanpa browser)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DIST = path.join(__dirname, 'dist');
const SVG = path.join(DIST, 'kalender-januari-2027-playful.svg');
const FONTS = path.join(__dirname, 'assets', 'fonts');

const fontFiles = fs.readdirSync(FONTS)
  .filter((f) => f.endsWith('.ttf'))
  .map((f) => path.join(FONTS, f));

const svg = fs.readFileSync(SVG);
for (const scale of [1, 2, 4]) {
  const resvg = new Resvg(svg, {
    fitTo: { mode: 'zoom', value: scale },
    background: '#FFFCF6',
    font: { fontFiles, loadSystemFonts: false, defaultFontFamily: 'Poppins' },
  });
  const png = resvg.render();
  const name = scale === 1 ? 'kalender-januari-2027-playful.png'
                           : `kalender-januari-2027-playful@${scale}x.png`;
  fs.writeFileSync(path.join(DIST, name), png.asPng());
  console.log(`${name} -> ${png.width}x${png.height}`);
}
