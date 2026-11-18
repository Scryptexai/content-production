# Hasil potong VO — run 44260594518

- status job: **failure**
- model: small
- commit: `a3fe860e8814a07ac7fc44d6f21e688a74e36921`
- waktu: 2026-11-18T07:41:11Z

## Log (ekor 60 baris)
```
  gdown gagal: download() got an unexpected keyword argument 'fuzzy'
  gdown tidak jalan, coba unduh langsung
  coba: https://drive.usercontent.google.com/download?id=1yzfE90efvYUJYMEu6iHof_do7aM8ZlLp&export=download&confirm=t
    HTTP 200 · audio/mpeg · Content-Length 7555666
    gagal: AttributeError: 'str' object has no attribute 'exists'
  coba: https://drive.google.com/uc?export=download&id=1yzfE90efvYUJYMEu6iHof_do7aM8ZlLp
    HTTP 200 · audio/mpeg · Content-Length 7555666
    gagal: AttributeError: 'str' object has no attribute 'exists'
  coba: https://drive.usercontent.google.com/download?id=1yzfE90efvYUJYMEu6iHof_do7aM8ZlLp&export=download
    HTTP 200 · audio/mpeg · Content-Length 7555666
    gagal: AttributeError: 'str' object has no attribute 'exists'
Traceback (most recent call last):
  File "/home/runner/work/content-production/content-production/ODDCHAPTER_BRAND/tools/fetch_vo.py", line 82, in <module>
    main()
  File "/home/runner/work/content-production/content-production/ODDCHAPTER_BRAND/tools/fetch_vo.py", line 77, in main
    if not direct(args.id, args.out):
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/content-production/content-production/ODDCHAPTER_BRAND/tools/fetch_vo.py", line 62, in direct
    target.unlink(missing_ok=True)
    ^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'unlink'
```
