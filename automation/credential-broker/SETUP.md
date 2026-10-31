# SETUP — dari nol sampai terbukti tersambung

Dokumen ini menjawab satu kebingungan yang paling sering muncul:
**rahasia mana ditaruh di mana, dan bagaimana membuktikan koneksinya jalan.**

---

## 0. Tiga jenis rahasia yang berbeda — jangan dicampur

Ini sumber utama kesalahpahaman. Ada **tiga** hal berbeda yang semuanya disebut
"API key", dan tidak satu pun boleh ditaruh di tempat yang sama.

| # | Rahasia | Dari mana | Disimpan di mana | Untuk apa |
|---|---|---|---|---|
| 1 | **Permit API key** | Dashboard Permit → Settings → API Keys | Environment variable **di server/klien yang memanggil** (`PERMIT_API_KEY`) | Membuktikan ke PDP bahwa permintaan datang dari environment-mu |
| 2 | **API key pihak ketiga** (OpenAI, Stripe, Slack) | Dashboard masing-masing penyedia | **Vault-mu** — env var Vercel atau Supabase Vault | Rahasia asli yang ditempelkan broker ke upstream |
| 3 | **Token pemanggil broker** | Kamu buat sendiri (acak) | Env var (`BROKER_STATIC_TOKENS` / `SUPABASE_JWT_SECRET`) | Mengenali *siapa* yang meminta, supaya bisa diperiksa Permit |

> ### Permit TIDAK menyimpan API key pihak ketigamu.
>
> Permit menyimpan **policy**: siapa boleh melakukan apa terhadap resource apa.
> Permit tidak pernah menerima, menyimpan, atau meneruskan kunci OpenAI/Stripe-mu.
> Kalau kamu menaruh kunci asli di Permit, ia tidak akan dipakai di mana pun.
>
> Alurnya selalu: Permit menjawab "boleh" → **baru** broker mengambil kunci dari
> vault-mu sendiri.

Dan yang **tidak** boleh ada di mana pun: kunci di dalam repo Git. Aturan repo
(`README.md` poin 5) sudah menegaskan itu, dan `.gitignore` sudah menolak `.env`.

---

## 1. Menyambungkan ke akun Permit

"Setup belum terhubung ke akun Permit" hampir selalu berarti salah satu dari dua
hal: environment variable belum diisi, **atau** nama resource di Permit belum ada.

### 1a. Ambil API key dan ID

Di [app.permit.io](https://app.permit.io):

1. Pilih project, lalu environment (mis. `Development`).
2. **Settings → API Keys** → salin **Environment API Key**.
3. Catat juga **Project ID** dan **Environment ID** (dipakai untuk seeding, bukan runtime).

Simpan ke `.env` lokal:

```bash
PERMIT_API_KEY=permit_xxxxxxxxxxxxxxxx
PERMIT_PDP_URL=https://cloudpdp.api.permit.io
PERMIT_PROJECT_ID=xxxxxxxxxxxx
PERMIT_ENV_ID=xxxxxxxxxxxx
```

### 1b. Buat resource + action + role

Broker hanya tahu **nama**: `ai_provider`/`openai`, dst (lihat
`src/upstreams.js`). Kalau nama itu belum ada di Permit, setiap check dijawab
DENY — bukan karena broker rusak, tapi karena policy-nya belum punya objeknya.

Skrip ini membuatnya, meniru registry broker:

```bash
# lihat rencananya dulu — tidak mengubah apa pun
node --env-file=.env scripts/seed-permit.mjs

# terapkan
node --env-file=.env scripts/seed-permit.mjs --apply
```

> Skrip ini memanggil `api.permit.io` (REST API untuk mengelola schema).
> Itu **berbeda** dari PDP yang dipakai broker saat melayani permintaan.
> Mengelola policy → `api.permit.io`. Memutuskan akses → `cloudpdp.api.permit.io`.
> Broker hanya butuh yang kedua.

### 1c. Assign role — bagian yang tidak bisa diotomatiskan

Buat/assign role `credential_user` ke **subjek yang benar-benar memakai broker**:
user tertentu, atau service account. Di dashboard: **Directory → Users → pilih user
→ Roles → assign**, pada tenant yang sesuai.

Selama role belum di-assign, check akan tetap DENY. Itu perilaku yang benar.

---

## 2. Menaruh rahasia pihak ketiga

### Pilihan A — env var Vercel (paling sederhana)

Set di dashboard Vercel: **Settings → Environment Variables**.

```
VAULT_PROVIDER = env
OPENAI_API_KEY = sk-...
STRIPE_SECRET_KEY = sk_live_...
SLACK_BOT_TOKEN = xoxb-...
```

Nama variabel harus sama dengan `secretName` di `src/upstreams.js`. Env var Vercel
terenkripsi saat disimpan dan tidak muncul lagi di UI.

### Pilihan B — Supabase Vault (untuk rotasi tanpa redeploy)

```
VAULT_PROVIDER          = supabase
SUPABASE_URL            = https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY = ...
VAULT_RPC               = get_secret
```

Dengan RPC pembaca di Supabase (SQL lengkap ada di `README.md` §6). Keunggulan:
mengganti kunci tidak perlu deploy ulang, karena broker hanya menyimpan *nama*
rahasia.

---

## 3. Membuat token pemanggil broker

Ini rahasia yang **kamu** buat. Contoh:

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64url'))"
```

Lalu:

```
BROKER_STATIC_TOKENS={"<token-tadi>":"service:reporting"}
```

Kalau pemanggilnya user yang login lewat Supabase, cukup isi
`SUPABASE_JWT_SECRET` (Settings → API → JWT Secret) dan broker akan memverifikasi
JWT user secara lokal, tanpa round-trip.

---

## 4. Menguji — empat tahap, dari yang paling murah

### Tahap 1 — plumbing, tanpa internet, tanpa kredensial

```bash
npm test          # 56 test, fetch di-mock
node scripts/smoke.mjs   # 13 pemeriksaan lewat HTTP sungguhan di loopback
```

Lulus di sini berarti logika broker benar: rahasia hanya ditempelkan ke upstream,
`authorization` dari klien selalu dibuang, deny tidak menyentuh upstream, PDP mati
→ 503 tanpa kredensial.

### Tahap 2 — benar-benar tersambung ke akun Permit-mu?

Jalankan **di mesinmu sendiri**, bukan di sandbox:

```bash
node --env-file=.env scripts/verify.mjs
```

Skrip ini mengirim satu check per upstream dan menerjemahkan setiap kemungkinan
jawaban:

| Gejala | Artinya | Perbaikan |
|---|---|---|
| `401` | API key ditolak | Salah salin, atau key milik environment lain |
| `403` | Key tidak punya cakupan | Cocokkan project/environment |
| `404` | `PERMIT_PDP_URL` salah | Harus `https://cloudpdp.api.permit.io`, tanpa `/allowed` |
| `ENOTFOUND` / timeout | Jaringan memblokir | Coba dari mesin lain, atau lewat Vercel |
| `→ DENY` | **Sudah tersambung**, policy menolak | Wajar untuk subjek uji; assign role |

Baris terakhir itu yang paling penting: **DENY berarti koneksi berhasil.** Yang
menolak adalah policy, bukan jaringan. Banyak orang salah membaca ini sebagai
"belum tersambung".

### Tahap 3 — konfigurasi di Vercel

Setelah deploy:

```bash
curl https://<project>.vercel.app/api/health
```

```json
{ "ok": true, "pdp": "https://cloudpdp.api.permit.io",
  "identity": { "static_tokens": 1, "supabase_jwt": false },
  "vault_provider": "env", "audit_provider": "console",
  "upstreams": ["openai","slack","stripe"], "claim_enabled_for": [] }
```

`ok: true` = variabel terbaca di Vercel. Endpoint ini tidak pernah menampilkan
nilai rahasia, hanya ada/tidak.

### Tahap 4 — jalur penuh, dari Vercel

```bash
# probe: jalankan policy check saja, tanpa menyentuh vault/upstream
node scripts/verify.mjs --remote https://<project>.vercel.app --token <BROKER_TOKEN>
```

`mode: "probe"` mengembalikan keputusan policy tanpa pernah mengambil rahasia —
jadi aman dipakai kapan saja untuk memastikan rantai
`klien → broker → Permit` utuh.

Baru setelah itu uji jalur sungguhan:

```bash
curl -X POST https://<project>.vercel.app/api/broker \
  -H "Authorization: Bearer <BROKER_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"upstream":"openai","path":"/v1/models","method":"GET"}'
```

---

## 5. Kalau masih gagal

| Gejala | Sebab paling mungkin |
|---|---|
| `/api/health` → `config_error` | Pesannya menyebut nama variabel yang kosong — isi di Vercel, lalu redeploy |
| `403 permit_denied` padahal role sudah di-assign | Nama resource/action di Permit beda dengan `src/upstreams.js`; cek huruf besar-kecil |
| `500 secret_not_found` | Nama env var tidak sama dengan `secretName` upstream |
| `503 permit_unavailable` | PDP tidak terjangkau dari runtime — cek `PERMIT_PDP_URL` |
| `401` dari broker | Token pemanggil salah; ini beda dari Permit API key |
| Semua DENY setelah seeding | Role belum di-assign ke subjek yang dipakai |

Prinsip yang berlaku di seluruh sistem ini: **kalau ada yang tidak pasti, tolak.**
Tidak ada jalur "kalau ragu, izinkan".
