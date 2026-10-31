# Credential Broker

Jalur permintaan kredensial untuk API pihak ketiga. **Permit.io bertindak sebagai
policy decision point (PDP) saja** — ia menjawab boleh/tidak. Rahasia aslinya
tinggal di vault dan **tidak pernah sampai ke klien**.

Runtime: **Vercel** (Node serverless, tanpa dependensi runtime).

> **Baru mulai di sini?** Baca [`SETUP.md`](SETUP.md) — langkah demi langkah,
> termasuk ke mana tiap jenis rahasia harus ditaruh dan cara membuktikan
> koneksi ke akun Permit benar-benar jalan.

```
klien (agent / service / app)
   │
   │  POST /api/broker   Authorization: Bearer <token identitas>
   │  { upstream, path, body, tenant, action }
   ▼
┌─────────────────────────── Vercel function ───────────────────────────┐
│ 1. identitas   → siapa pemanggilnya?        (401 kalau tidak sah)     │
│ 2. registry    → upstream apa? path boleh?  (404/403 kalau tidak)     │
│ 3. Permit PDP  → POST {pdp}/allowed         (403 kalau ditolak)       │
│ 4. vault       → ambil rahasia   ── hanya setelah langkah 3 allow     │
│ 5. upstream    → teruskan, tempelkan rahasia di header                │
│ 6. audit       → catat, allow maupun deny                             │
└───────────────────────────────────────────────────────────────────────┘
   │
   ▼  respons upstream diteruskan apa adanya (rahasia tidak ikut)
```

---

## Kenapa mode proxy, bukan sekadar membagikan kunci

Kunci API pihak ketiga (OpenAI, Stripe, Slack) berumur panjang dan berlaku penuh.
Membagikannya ke klien — walaupun lewat Permit — berarti satu kebocoran di sisi
klien langsung setara dengan kebocoran kunci produksi, dan Permit tidak bisa
menariknya kembali.

Karena itu default-nya **proxy**: klien tidak pernah memegang kunci. Ia meminta
*broker* yang memanggil API tujuan. Permit tetap satu-satunya penentu, dan
kuncinya tidak pernah meninggalkan server.

Mode `claim` (mengembalikan kunci mentah) tersedia, tetapi **mati per-upstream**
(`allowClaim`) dan sengaja tidak dinyalakan untuk apa pun di registry bawaan.
Nyalakan hanya kalau klien memang tidak mungkin memakai proxy — misalnya SDK
pihak ketiga yang berjalan di mesin lain dan menuntut kunci asli.

---

## Temuan penting: check TIDAK lewat `api.permit.io`

Dokumentasi Permit menyatakan jelas:

> "Permission checks don't go through this API. A check goes to the PDP, not to
> `api.permit.io`."

Kontrak yang dipakai broker ini (diverifikasi dari sumber SDK resmi
`permitio@2.7.7`, `build/index.js` → `Enforcer.checkWithExceptions`):

```
POST {PERMIT_PDP_URL}/allowed
Authorization: Bearer <PERMIT_API_KEY>
{ "user": {"key": "..."}, "action": "invoke",
  "resource": {"type":"...","key":"...","tenant":"default","attributes":{}},
  "context": {} }
→ 200 { "allow": true }
```

`PERMIT_PDP_URL` default ke `https://cloudpdp.api.permit.io` (Cloud PDP), sama
seperti perilaku SDK. Jadi host yang harus bisa dijangkau dari runtime adalah
**`cloudpdp.api.permit.io`**, bukan `api.permit.io`.

> Kalau nanti pindah ke PDP self-hosted (container OPA/OPAL di VPC sendiri),
> cukup ubah `PERMIT_PDP_URL`. Vercel tidak bisa menjalankan container PDP,
> jadi untuk Vercel pakai Cloud PDP.

---

## 1. Siapkan Permit

1. Buat project + environment di [app.permit.io](https://app.permit.io).
2. Definisikan resource sesuai registry di [`src/upstreams.js`](src/upstreams.js):

   | resourceType | resourceKey | action |
   |---|---|---|
   | `ai_provider` | `openai` | `invoke` |
   | `payment_provider` | `stripe` | `invoke` |
   | `messaging` | `slack` | `post_message` |

3. Beri role ke subjek (user/service) di tenant yang dipakai.
4. Salin **Environment API Key** → `PERMIT_API_KEY`.

Nama resource di Permit harus **persis** sama dengan `resourceType`/`resourceKey`
di registry. Kalau tidak cocok, semua permintaan akan ditolak — dan itu perilaku
yang benar (fail-closed), bukan bug.

---

## 2. Konfigurasi

```bash
cp .env.example .env
```

Variabel minimum:

| Variabel | Wajib | Keterangan |
|---|---|---|
| `PERMIT_API_KEY` | ya | Environment API key Permit |
| `PERMIT_PDP_URL` | tidak | default `https://cloudpdp.api.permit.io` |
| `BROKER_STATIC_TOKENS` | salah satu | JSON `{"token":"service:nama"}` |
| `SUPABASE_JWT_SECRET` | salah satu | untuk user login via Supabase |
| `VAULT_PROVIDER` | tidak | `env` (default) atau `supabase` |
| `AUDIT_PROVIDER` | tidak | `console` (default), `supabase`, `none` |
| `OPENAI_API_KEY` dll | ya (vault `env`) | rahasia asli per upstream |

Minimal satu metode identitas **harus** ada. Tanpa itu broker menolak start
dengan pesan yang menyebut nama variabel (tidak pernah nilainya).

---

## 3. Deploy ke Vercel

Karena proyek ini hidup di dalam repo studio, set **Root Directory** saat impor:

```
Root Directory : automation/credential-broker
Framework      : Other
Build Command  : (kosong)
```

Lalu isi Environment Variables di dashboard Vercel — **jangan** lewat file yang
di-commit. Setelah deploy, cek:

```bash
curl https://<project>.vercel.app/api/health
```

`ok: true` berarti konfigurasi terbaca. Endpoint ini tidak pernah menampilkan
nilai rahasia, hanya ada/tidak.

---

## 4. Memakai broker

### Mode proxy (default) — rahasia tidak pernah sampai ke klien

```bash
curl -X POST https://<project>.vercel.app/api/broker \
  -H "Authorization: Bearer $BROKER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "upstream": "openai",
    "path": "/v1/chat/completions",
    "method": "POST",
    "tenant": "default",
    "body": {
      "model": "gpt-4o-mini",
      "messages": [{"role": "user", "content": "halo"}]
    }
  }'
```

Balasannya adalah balasan OpenAI apa adanya. Kunci tidak muncul di mana pun.

### Mode claim — hanya kalau upstream mengizinkannya

```json
{ "upstream": "openai", "mode": "claim", "path": "/v1/models" }
```

```json
{
  "credential": "...",
  "credential_kind": "static_api_key",
  "expires_at": "2026-10-31T12:30:00.000Z",
  "request_id": "..."
}
```

> `expires_at` adalah **batas reveal**, bukan masa berlaku kunci. Kunci statis
> pihak ketiga tetap berlaku sampai dirotasi di sisi penyedia.

### Field permintaan

| Field | Wajib | Keterangan |
|---|---|---|
| `upstream` | ya | nama di registry |
| `path` | ya | harus diawali `/` dan cocok dengan `allowedPathPrefixes` |
| `method` | tidak | default `POST`; harus ada di `methods` upstream |
| `body` | tidak | JSON yang diteruskan ke upstream |
| `query` | tidak | objek; nilai non-skalar diabaikan |
| `headers` | tidak | disaring daftar putih; `authorization` selalu dibuang |
| `tenant` | tidak | default `default` |
| `action` | tidak | default dari registry |
| `attributes` | tidak | atribut ABAC untuk Permit |
| `context` | tidak | context ABAC untuk Permit |
| `mode` | tidak | `proxy` (default), `claim`, atau `probe` |

---

## 5. Kode respons

| Status | `error` | Arti |
|---|---|---|
| 200 | — | diizinkan; respons upstream diteruskan |
| 400 | `invalid_path`, `invalid_json`, `invalid_mode` | permintaan cacat |
| 401 | `missing_token`, `invalid_token`, `token_expired` | identitas tidak sah |
| 403 | `permit_denied` | policy Permit menolak |
| 403 | `claim_not_allowed` | mode claim tidak aktif untuk upstream ini |
| 403 | `path_not_allowed` | path di luar daftar izin |
| 404 | `unknown_upstream` | nama tidak ada di registry |
| 405 | `method_not_allowed` | metode HTTP tidak diizinkan |
| 413 | `body_too_large` | melebihi `MAX_BODY_BYTES` |
| 500 | `secret_not_found` | rahasia tidak ada di vault |
| 503 | `permit_unavailable` | PDP tidak terjangkau — **fail-closed**, tidak ada kredensial |
| 503 | `vault_unavailable` | vault tidak terjangkau |

**Fail-closed** adalah aturan keras: kalau PDP tidak bisa dihubungi, broker
menolak. Tidak ada jalur "kalau Permit down, anggap boleh".

---

## 6. Audit

`AUDIT_PROVIDER=supabase` menulis satu baris per permintaan ke tabel:

```sql
create table if not exists public.credential_audit (
  id           bigserial primary key,
  request_id   uuid        not null,
  at           timestamptz not null default now(),
  subject      text,
  upstream     text,
  mode         text,
  outcome      text,        -- allowed | denied | rejected | error
  status       integer,
  detail       text,
  duration_ms  integer
);

alter table public.credential_audit enable row level security;
-- Service role melewati RLS; tidak perlu policy untuk insert dari broker.
```

Isinya tidak pernah memuat rahasia. Kegagalan menulis audit tidak menggagalkan
permintaan yang sudah lolos policy, tetapi dicatat sebagai `audit_failure` di log.

Untuk vault lewat Supabase, siapkan RPC pembaca Supabase Vault:

```sql
create or replace function public.get_secret(secret_name text)
returns text
language sql
security definer
set search_path = vault, public
as $$
  select decrypted_secret from vault.decrypted_secrets where name = secret_name limit 1;
$$;

revoke all on function public.get_secret(text) from public, anon, authenticated;
```

---

## 7. Batas yang perlu diketahui

- **Bukan pengganti rotasi kunci.** Kalau kunci di vault bocor, Permit tidak
  menolong. Rotasi tetap tanggung jawabmu.
- **Registry hard-coded.** Menambah upstream = commit + deploy. Ini disengaja:
  base URL tidak boleh bisa ditentukan klien, kalau tidak broker jadi open proxy.
- **Streaming belum didukung.** Respons upstream dibaca utuh lalu diteruskan,
  jadi SSE/streaming token demi token tidak akan terasa real-time. Kalau butuh,
  tambahkan jalur pass-through untuk `content-type: text/event-stream`.
- **Batas ukuran respons.** Respons besar (mis. unduhan file) tidak cocok lewat
  jalur ini.
- **Budget waktu.** `maxDuration` 30 detik di `vercel.json`; panggilan upstream
  yang lebih lama akan terpotong.

---

## 8. Uji

```bash
npm test               # 56 unit + integrasi, fetch di-mock
node scripts/smoke.mjs # 13 pemeriksaan lewat HTTP sungguhan di loopback
```

Skrip bantu untuk menyiapkan dan memeriksa akun Permit asli:

```bash
node --env-file=.env scripts/verify.mjs         # uji koneksi + diagnosis per kode HTTP
node --env-file=.env scripts/seed-permit.mjs    # rencana resource/action/role (dry run)
node --env-file=.env scripts/seed-permit.mjs --apply
```

Keduanya berjalan tanpa internet dan tanpa kredensial asli: PDP dan upstream
ditiru server lokal. Yang diuji antara lain: rahasia hanya ditempelkan ke
upstream, `authorization` dari klien selalu dibuang, deny tidak pernah menyentuh
upstream, dan PDP mati menghasilkan 503 tanpa kredensial.

**Yang tidak bisa diuji dari sandbox:** panggilan nyata ke
`cloudpdp.api.permit.io`. Sandbox pengembangan hanya punya egress ke GitHub,
npm, dan PyPI. Uji pertama yang sesungguhnya adalah `/api/health` lalu satu
permintaan `mode: proxy` setelah deploy di Vercel.

---

## Peta berkas

```
api/broker.js        endpoint POST /api/broker (tipis, hanya merangkai)
api/health.js        GET /api/health — cek konfigurasi tanpa membocorkan rahasia
src/app.js           handler utama: urutan identitas → policy → vault → upstream → audit
src/permit.js        klien PDP Permit (POST /allowed)
src/identity.js      token statis + verifikasi JWT HS256 Supabase
src/upstreams.js     registry upstream + validasi path + penyaringan header
src/vault.js         pembacaan rahasia (env / Supabase Vault)
src/audit.js         pencatatan audit
src/http.js          helper HTTP kecil
SETUP.md             panduan setup: rahasia mana di mana, cara uji bertahap
scripts/smoke.mjs    uji end-to-end lewat socket sungguhan
scripts/verify.mjs   uji koneksi ke Permit + diagnosis kode HTTP
scripts/seed-permit.mjs  buat resource/action/role sesuai registry (dry run default)
test/                unit + integrasi (node:test, tanpa dependensi)
```
