/**
 * objects.ts — ukuran benda dihitung dari ZONA, bukan dikira-kira.
 *
 * Percobaan pertama gagal persis di sini: lebar benda ditulis manual (mis.
 * 880 px untuk kliping), sehingga tinggi aslinya (880 × 1,07 = 945 px)
 * melewati zona benda 726 px dan menabrak pita teks di bawah.
 *
 * Di sini setiap benda diberi RASIO (dari berkas PNG hasil potong) dan
 * pemanggil hanya menentukan TINGGI yang diinginkan; lebarnya dihitung.
 */
export const ASPECT_HW: Record<string, number> = {
  newspaper: 1.0735,
  fin: 1.823,
  'ballot-box': 1.2165,
  ballots: 1.2913,
  magnifier: 0.8558,
  'thread-knot': 1.1257,
};

/** lebar untuk tinggi tertentu (px pada skala kamera 1) */
export const wForH = (name: string, h: number) => h / (ASPECT_HW[name] ?? 1);

/** lebar maksimum supaya benda tidak menyentuh tepi bingkai (1080 − 2×56 margin) */
export const MAX_W = 968;

export const fitW = (name: string, h: number) => Math.min(wForH(name, h), MAX_W);
