# drive-requests

Titik masuk untuk mengambil berkas milik pemilik dari Google Drive ke sesi kerja.

Sandbox kerja hanya bisa menghubungi github.com (lihat `SKILLS/00_RULEBOOK.md`
§13); `drive.google.com` tidak terjangkau dari sini. Workflow `drive-fetch.yml`
berjalan di runner GitHub — yang punya internet penuh — setiap kali ada berkas
JSON baru di folder ini.

```json
{ "file_id": "1dD1nKT97...", "name": "VO-EP09.mp3" }
```

Hasilnya di-commit ke branch `drive/inbox`, bukan ke branch kerja:

```bash
git fetch origin +refs/heads/drive/inbox:refs/remotes/origin/drive/inbox
git show origin/drive/inbox:drive-inbox/VO-EP09.mp3 > /tmp/VO-EP09.mp3
```

Berkas Drive harus bisa dibaca "siapa saja yang punya tautan" selama job
berjalan; cabut izinnya setelah berkas diambil.
