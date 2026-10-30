/**
 * theme.ts — satu-satunya sumber warna, huruf, dan ukuran di film ini.
 *
 * Aturan yang dipegang (dari references/aesthetic-rules.md + direction film ini):
 *  - satu look per film: panggung gelap tungsten (bukan biru-neon, bukan putih SaaS)
 *  - aksen rose hanya untuk angka/penekanan, ≤5% permukaan
 *  - tipografi: serif untuk pernyataan, mono untuk label/sumber, sans untuk badan
 *  - semua huruf dibundel lokal (public/../node_modules @fontsource) — mesin ini
 *    tidak punya font sistem sama sekali
 */
import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';
import '@fontsource/instrument-serif/400.css';
import '@fontsource/instrument-serif/400-italic.css';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/500.css';

export const FONT = {
  serif: '"Instrument Serif", "Times New Roman", Georgia, serif',
  sans: 'Inter, "Helvetica Neue", Arial, sans-serif',
  mono: '"JetBrains Mono", ui-monospace, Menlo, monospace',
};

export const C = {
  ink: '#05070F',
  ink2: '#0A0E1A',
  ink3: '#111726',
  slate: '#2B3650',
  slate2: '#3E4A66',
  cream: '#EFE7DC',
  cream2: '#CFC5B6',
  muted: '#8A93A3',
  muted2: '#6B7488',
  rose: '#D98E73',
  roseLit: '#F2B79C',
  roseDeep: '#9E5C45',
  sage: '#8FA98B',
  lilac: '#A79BC8',
  tungsten: '#FFD2A0',
  cool: '#8AA0CE',
};

/** hex → "r,g,b" untuk rgba() */
export const rgb = (hex: string) => {
  const h = hex.replace('#', '');
  const n = parseInt(h.length === 3 ? h.split('').map((c) => c + c).join('') : h.slice(0, 6), 16);
  return `${(n >> 16) & 255},${(n >> 8) & 255},${n & 255}`;
};
export const alpha = (hex: string, a: number) => `rgba(${rgb(hex)},${a})`;

/**
 * Skala tipografi 1080×1920. Nilai di sini diuji pada bingkai vertikal:
 * badan ≥ 44 px supaya masih terbaca saat ditonton di layar telepon,
 * label/sumber ≥ 22 px, angka utama boleh 150–230 px.
 */
export const TYPE = {
  mega: 230,
  display: 150,
  h1: 104,
  h2: 78,
  h3: 56,
  body: 46,
  bodySm: 38,
  label: 26,
  source: 22,
} as const;

/** jarak antar huruf: judul besar dirapatkan, label kecil direnggangkan */
export const tracking = (size: number, caps = false) => {
  const base = size >= 120 ? -0.03 : size >= 72 ? -0.02 : size >= 44 ? -0.012 : size >= 26 ? 0 : 0.02;
  return `${(base + (caps ? 0.16 : 0)).toFixed(3)}em`;
};
