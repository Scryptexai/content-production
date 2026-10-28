// Menanam woff2 sebagai data URI di src/film/fontData.ts.
// Alasan: saat render panjang, permintaan font ke static server bisa menggantung
// dan memicu "delayRender() was called but not cleared". Data URI tidak pernah
// menyentuh jaringan, jadi font selalu siap sebelum frame pertama.
import {readdirSync, readFileSync, writeFileSync} from 'node:fs';
import {join} from 'node:path';

const dir = 'public/fonts';
const files = readdirSync(dir).filter((f) => f.endsWith('.woff2')).sort();
const entries = files.map((f) => {
  const b64 = readFileSync(join(dir, f)).toString('base64');
  return `  '${f}': 'data:font/woff2;base64,${b64}',`;
});
writeFileSync(
  'src/film/fontData.ts',
  `// Dibuat oleh scripts/embed-fonts.mjs — jangan diedit manual.\nexport const FONT_DATA: Record<string, string> = {\n${entries.join('\n')}\n};\n`,
);
console.log(`${files.length} font ditanam (${(files.reduce((a, f) => a + readFileSync(join(dir, f)).length, 0) / 1024).toFixed(0)} KB)`);
