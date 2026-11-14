# Jadwal 15 Nov 2026 — dikerjakan ulang dengan VO internal

Pemilik (16 Nov): *"vo nya jangan pakai elevenlabs lagi tapi pakai vo internal kamu yg kamu
gunakan pada ep06-07."* Semua jadwal lama dibatalkan, lalu dibuat ulang satu per satu.

| jam WIB | episode | VO | durasi | post Zernio | status |
|---|---|---|---|---|---|
| 07.30 | EP08 | **internal (voice-04)** | 42,2 s | `6af8ebde26409c28f9b3285f` | **scheduled** |
| 12.30 | EP09 | sedang direkam ulang | — | lama `6af8a02b…` **dibatalkan** | menunggu |
| 18.30 | EP10 | sedang direkam ulang | — | lama `6af8a2cd…` **dibatalkan** | menunggu |

Post lama yang dibatalkan (HTTP 200 dari `DELETE /v1/posts/<id>`):

- `6af89b196abb0bb79a196d29` — EP08 VO ElevenLabs (07.30)
- `6af8a02b588bc489d6d82eb5` — EP09 VO ElevenLabs (12.30)
- `6af8a2cdc3753df892a8fc08` — EP10 VO ElevenLabs (18.30)

## Bunyi VO

| | EP06 | EP07 | voice-04 (sekarang) |
|---|---|---|---|
| f0 median | 102,2 Hz | 101,4 Hz | 116,8 Hz |
| tilt (dada vs kepala) | 12,9 dB | 12,1 dB | 12,2 dB |

Karakter gelapnya sama; nada dasarnya ~2,5 semiton lebih tinggi. Tidak saya geser
dengan pitch-shift karena pergeseran sebesar itu mengubah formant dan terdengar
seperti orang lain yang meniru.

## Aturan produksi yang berubah

1. Narasi dibuat di sesi agen (`generate_speech`), bukan API ElevenLabs.
2. Batas alat: **10 klip per giliran** — satu episode (9–10 segmen) selesai dalam satu giliran.
3. Efek suara tetap dari `fx/*.mp3`; `eleven_audio.py --only place` hanya menempel, tidak memanggil API.
4. Sisanya tidak berubah: target 35–45 dtk, VO mulai 0,15 dtk, bed −38 LUFS, semua segmen disamakan RMS.

## Angka EP08 v5

42,2 s · narasi −17,5 dBFS vs jeda −35,1 dBFS (**selisih 17,6 dB**) · −14,0 LUFS · TP −1,7 dBTP ·
VO mulai 0,15 dtk · `voice_consistency` LULUS 9/9 segmen.
