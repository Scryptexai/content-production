# Hasil potong VO — run 44315522833

- status job: **success**
- model: small
- commit: `d87b291153927a9fac8ec3f698b56dfb505a166b`
- waktu: 2026-11-18T13:52:07Z

## Laporan potong
```
seg  mulai   akhir   durasi  kata   wpm
--------------------------------------------
  1    0.00   23.59   23.59    56  142.4
  2   23.59   46.02   22.42    63  168.6
  3   46.02  109.04   63.03   162  154.2
  4  109.04  191.40   82.35   199  145.0
  5  191.40  262.92   71.52   188  157.7
  6  262.92  316.84   53.92   124  138.0
  7  316.84  375.42   58.58   144  147.5
  8  375.42  416.70   41.28   104  151.1
  9  416.70  471.17   54.47   137  150.9

median 150.9 wpm · total 471.17 dtk · audio 471.17 dtk
BATAS MENCURIGAKAN: tidak ada
```
## Berkas
```
total 44M
-rw-r--r-- 1 runner runner 2.2M Nov 18 13:52 VO_01.wav
-rw-r--r-- 1 runner runner 2.1M Nov 18 13:52 VO_02.wav
-rw-r--r-- 1 runner runner 5.8M Nov 18 13:52 VO_03.wav
-rw-r--r-- 1 runner runner 7.6M Nov 18 13:52 VO_04.wav
-rw-r--r-- 1 runner runner 6.6M Nov 18 13:52 VO_05.wav
-rw-r--r-- 1 runner runner 5.0M Nov 18 13:52 VO_06.wav
-rw-r--r-- 1 runner runner 5.4M Nov 18 13:52 VO_07.wav
-rw-r--r-- 1 runner runner 3.8M Nov 18 13:52 VO_08.wav
-rw-r--r-- 1 runner runner 5.0M Nov 18 13:52 VO_09.wav
-rw-r--r-- 1 runner runner 1.2K Nov 18 13:52 boundaries.json
-rw-r--r-- 1 runner runner  542 Nov 18 13:52 report.txt
-rw-r--r-- 1 runner runner  97K Nov 18 13:52 words.json
```
## Log (ekor 60 baris)
```
Downloading...
From: https://drive.google.com/uc?id=1yzfE90efvYUJYMEu6iHof_do7aM8ZlLp
To: /home/runner/work/content-production/content-production/vo.mp3
  0%|          | 0.00/7.56M [00:00<?, ?B/s] 62%|██████▏   | 4.72M/7.56M [00:00<00:00, 15.8MB/s]100%|██████████| 7.56M/7.56M [00:00<00:00, 24.4MB/s]
  gdown: vo.mp3 (7555666 byte)
-rw------- 1 runner runner 7.3M Nov 18 04:33 vo.mp3
duration=471.170563
bit_rate=128287
ASR: model=small bahasa=id
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
ASR: 942 kata, durasi audio 471.17 dtk
batas ASR   snap    jeda dipakai
       24.05   23.59   23.38-23.80 (0.42s)
       45.77   46.02   45.49-46.54 (1.04s)
      108.25  109.05   108.88-109.21 (0.33s)
      191.45  191.40   191.16-191.64 (0.48s)
      263.07  262.92   262.78-263.07 (0.29s)
      317.03  316.84   316.59-317.09 (0.50s)
      375.53  375.42   375.21-375.63 (0.42s)
      416.85  416.70   416.55-416.86 (0.31s)
batas final (menimpa snap): 23.59, 46.02, 109.04, 191.40, 262.92, 316.84, 375.42, 416.70
words.json: 1185 kata (6 kata beda segmen naskah/waktu)
seg  mulai   akhir   durasi  kata   wpm
--------------------------------------------
  1    0.00   23.59   23.59    56  142.4
  2   23.59   46.02   22.42    63  168.6
  3   46.02  109.04   63.03   162  154.2
  4  109.04  191.40   82.35   199  145.0
  5  191.40  262.92   71.52   188  157.7
  6  262.92  316.84   53.92   124  138.0
  7  316.84  375.42   58.58   144  147.5
  8  375.42  416.70   41.28   104  151.1
  9  416.70  471.17   54.47   137  150.9

median 150.9 wpm · total 471.17 dtk · audio 471.17 dtk
BATAS MENCURIGAKAN: tidak ada
OK: sembilan segmen dipotong, semua laju dalam ±30% median
```
