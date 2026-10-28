import {FONT_DATA} from './fontData';

/**
 * Font ditanam sebagai data URI (lihat scripts/embed-fonts.mjs): tidak ada
 * permintaan jaringan saat render, jadi tidak mungkin menggantung.
 *
 * Catatan penting: jangan pakai `loadFont()` dari `@remotion/fonts` di sini.
 * Saat render dengan dua tab, `font.load()` di tab kedua kadang tidak pernah
 * resolve sehingga `delayRender` menggantung 28 detik dan render gagal di
 * tengah (kejadian nyata: frame 395 dan 405). Gate di bawah selalu melepas
 * handle — lewat `finally` maupun timeout pengaman.
 */
const face = (family: string, file: string, weight: string, style = 'normal') =>
  `@font-face{font-family:'${family}';src:url(${FONT_DATA[file]}) format('woff2');font-weight:${weight};font-style:${style};font-display:block;}`;

export const FONT_CSS = [
  face('DMSerif', 'DMSerif-Regular.woff2', '400'),
  face('DMSerif', 'DMSerif-Italic.woff2', '400', 'italic'),
  face('Inter', 'Inter-400.woff2', '400'),
  face('Inter', 'Inter-600.woff2', '600'),
  face('Inter', 'Inter-800.woff2', '800'),
  face('PlexMono', 'PlexMono-500.woff2', '500'),
  face('PlexMono', 'PlexMono-600.woff2', '600'),
].join('\n');

export const FONT_SPECS = [
  '400 40px DMSerif',
  'italic 400 40px DMSerif',
  '400 40px Inter',
  '600 40px Inter',
  '800 40px Inter',
  '500 40px PlexMono',
  '600 40px PlexMono',
];
