# Karakter brand "SIMPUL" — keputusan bentuk dan alasannya

Dokumen ini mencatat **mengapa** karakternya berbentuk seperti ini. Kalau nanti
ada yang ingin mengubah bentuknya, perubahan itu harus bisa menjawab aturan di
sini — atau aturan di sini yang harus diubah lebih dulu, dengan alasan.

Lembar rujukan visual: [`img/character-sheet.png`](img/character-sheet.png)
Kode: `film/char/character.js` (bentuk) · `film/char/export_joints.py` (gerak)

---

## 1. Kenapa karakter ini ada

Kanal ini butuh satu wajah yang muncul di semua video, di semua tempat. Tanpa
itu, tiap video terasa dibuat oleh orang berbeda. Karakter ini bukan maskot
yang lucu — ia **alat baca**: ia menunjukkan ke mana mata harus melihat, dan
ia menyentuh diagram supaya angka tidak berdiri sendiri.

Karena itu syaratnya tiga, dan ketiganya mengikat:

1. **Terbaca pada ukuran kecil.** Di long-form ia 40% tinggi frame; di chart
   atau di dalam diagram ia bisa turun ke 30 px. Kalau siluetnya hilang di
   ukuran itu, ia gagal.
2. **Tidak bisa terbaca sebagai bicara.** Video ini faceless. Karakter yang
   punya mulut akan selalu terlihat lipsync palsu.
3. **Bisa dipindah ke tempat mana pun.** Satu set klip gerak, dipakai ulang di
   scene berbeda, tanpa perlu menggambar ulang.

---

## 2. Keputusan bentuk, satu per satu

| Elemen | Keputusan | Alasan |
|---|---|---|
| Kepala | **krem penuh, tanpa wajah** | satu-satunya bidang terang di badan gelap; inilah yang membuatnya masih terbaca pada 26 px |
| Mata | **satu lensa rose di dalam pita visor** | satu titik fokus, bukan dua; pita gelap di belakangnya memberi kontras supaya lensa tidak menyatu dengan kepala krem |
| Mulut | **tidak ada** | mustahil terbaca sebagai bicara → aman untuk faceless |
| Kerah | **kerah tegak + simpul kecil di tenggorokan** | mengacu langsung ke nama kanal; simpul adalah satu-satunya ornamen yang boleh ada di badan |
| Badan | **jas lonceng, hem depan pendek, belakang panjang** | siluet A-line; tabung lurus selalu terbaca sebagai piktogram tongkat |
| Ekor | **pita yang menyambung ke benang** | satu bentuk, bukan tempelan; ekor tertinggal saat bergerak, jadi satu still pun terbaca "sedang bergerak" |
| Ujung sepatu | **krem** | penanda kontak dengan tanah, terbaca tanpa perlu melihat bayangan |
| Tangan | **krem, tanpa jari** | sama seperti kepala: bidang terang untuk gerak; jari akan hilang di bawah 60 px dan hanya menambah derau |

**Yang sengaja tidak dipakai:** antena, tanduk, telinga hewan, sayap, jubah
bertudung, topi, kacamata bulat ganda, jakun, kancing, sabuk, logo di dada.
Semuanya menambah ciri tapi mengurangi keterbacaan pada ukuran kecil. Yang
dipilih adalah **tiga ciri besar** (kepala krem, pita visor, ekor-benang),
bukan dua belas ciri kecil.

---

## 3. Warna

| Peran | Warna | Dipakai di |
|---|---|---|
| ink | `#0A0E18` | latar, bayangan, casing simpul |
| slate | `#2B3650` | jas, lengan |
| krem | `#EFE7DC` | kepala, tangan, manset, ujung sepatu, sol |
| rose | `#D98E73` | lensa, simpul kerah, simpul yang diikat |

**Badan tidak pernah memakai sage atau lilac.** Keduanya aksen scene (vegetasi,
diagram, benang). Kalau badan diberi warna aksen, karakter berhenti terasa
seperti karakter dan mulai terasa seperti mainan — ini sudah dicoba dan
hasilnya buruk (lihat panel 05 di lembar identitas).

Varian resmi yang boleh dipakai, semuanya menurunkan rona dari palet yang sama:

- **slate** (dasar) — semua video
- **slate-rose** — topik yang lebih hangat (relasi, kerja, manusia)
- **lilac** — topik sistem (struktur, jaringan, aturan)

Varian lain di luar tiga ini harus dibuat dengan `mix()` dari palet, bukan
warna baru.

---

## 4. Aturan cahaya

Cahaya **selalu dari kanan-atas**. Semua gradien menyala di sisi itu
(`LIGHT = {x: 0.58, y: -0.81}` di `character.js`). Konsekuensinya: karakter
boleh dipindah ke scene mana pun tanpa diwarnai ulang — asal scene-nya juga
menaruh sumber cahaya di kanan-atas. Kalau sebuah scene butuh cahaya dari
kiri, yang diubah adalah scene-nya.

---

## 5. Gerak

Gerak **tidak digambar tangan**. `film/char/export_joints.py` memakai rig IK
Python (`cine.py`, `motion.py`) yang sudah divalidasi: **pijakan kaki 0,002 px**
terhadap permukaan tangga. Yang diekspor hanya **sendi**; bentuknya digambar
`character.js`. Karena itu bentuk boleh di-redesign total tanpa membuang data
gerak.

Klip yang tersedia:

| Klip | Durasi | Dipakai untuk |
|---|---|---|
| `walk` | 12 dtk | berjalan di tanah datar |
| `climb` | 12 dtk | menaiki 6 anak tangga |
| `idle` | 8 dtk | berdiri, napas + pandang menyapu |
| `tie` | 3,2 dtk | berdiri di puncak, mengikat benang |
| `reach` | 3 dtk | mengulur tangan ke diagram |

Aturan gerak:

- Kepala tidak boleh menoleh lebih dari 8° — di layar lebar ia terlihat gelisah.
- Lensa hanya bergeser maksimum **4 px** saat memandang. Lebih dari itu, mata
  terlihat melirik ketakutan.
- Ekor dan benang selalu tertinggal (lag), tidak pernah bergerak lebih dulu.
- Tidak ada blinks, tidak ada idle-acak: semua gerak berasal dari klip.

---

## 6. Cara memakai di scene baru

```html
<script type="module">
import { Character } from "../../char/character.js";
const J = await (await fetch("/assets/char-joints.json")).json();
const fig = new Character(document.getElementById("layer"));

// tiap frame — taruh grup di (originX, dy), lalu gambar klip pada waktu tt
fig.draw(J.clips.walk, tt, { ground: (an) => 940 });
</script>
```

`ground` wajib diberikan kalau permukaannya bukan bidang datar. Kalau tidak,
bayangan kontak akan salah dan kaki terlihat melayang walau datanya benar.

---

## 7. Yang belum ada (jujur)

- **Belum ada ekspresi.** Tidak bisa menunjukkan terkejut, ragu, atau tegas
  selain lewat gerak badan. Kalau nanti naskah butuh itu, solusinya bukan
  menggambar mulut, tapi menambah klip gerak (mundur satu langkah, berhenti,
  menoleh pelan).
- **Belum ada interaksi tangan dengan objek.** Benang sudah bisa diikat ke
  simpul, tapi tangan belum bisa memegang balok/grafik. Perlu satu klip lagi
  (`grip`) kalau scene butuh itu.
- **Belum ada versi 3/4 atau menghadap kiri.** Semua klip menghadap kanan.
  Scene yang butuh arah sebaliknya harus membalik grup (mirror) — dan itu
  membalik arah cahaya, jadi harus dipakai hati-hati.
