#!/usr/bin/env node
/**
 * zernio (runner lokal) — jembatan semi-otomatis antara kalender draf di repo
 * dan akun Zernio. Pola & endpoint mengikuti mcp/zernio di repo zyvro-labs
 * (REST base https://zernio.com/api/v1, Bearer API key).
 *
 *   node automation/zernio/runner/zernio.mjs accounts
 *   node automation/zernio/runner/zernio.mjs connect
 *   node automation/zernio/runner/zernio.mjs push --dry-run
 *   node automation/zernio/runner/zernio.mjs push --day 1
 *   node automation/zernio/runner/zernio.mjs status
 *   node automation/zernio/runner/zernio.mjs sync
 *
 * Flag push:
 *   --dry-run        cetak payload, tidak mengirim apa pun
 *   --day N          hanya hari ke-N (1..7)
 *   --platform P     hanya youtube|tiktok|instagram
 *   --limit N        batas jumlah draf
 *   --yes            setujui semua tanpa prompt (hanya untuk uji, tidak untuk produksi)
 *
 * Rahasia: automation/zernio/.env (gitignored). Tidak ada token di repo.
 * Tidak ada autoPublish: setiap draf harus disetujui manusia.
 */
import {existsSync, readFileSync, writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createInterface} from 'node:readline';

const HERE = dirname(fileURLToPath(import.meta.url));
const ZDIR = join(HERE, '..');
const REPO = join(ZDIR, '..', '..');
const CALENDAR = join(ZDIR, 'content', 'calendar.json');
const CHANNELS = join(ZDIR, 'content', 'channels.json');
const MAPPING = join(ZDIR, '.zernio-mapping.json');
const ENV_FILE = join(ZDIR, '.env');
const API = 'https://zernio.com/api/v1';

function loadEnv() {
  const env = {...process.env};
  if (existsSync(ENV_FILE)) {
    for (const line of readFileSync(ENV_FILE, 'utf8').split('\n')) {
      const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
      if (m && !(m[1] in env)) env[m[1]] = m[2].replace(/^["']|["']$/g, '');
    }
  }
  return env;
}
const ENV = loadEnv();
const ARGS = process.argv.slice(2);
const cmd = ARGS[0];
const has = (f) => ARGS.includes(`--${f}`);
const opt = (f) => {
  const i = ARGS.indexOf(`--${f}`);
  return i >= 0 ? ARGS[i + 1] : undefined;
};

const readJson = (p, fb) => {
  try {
    return JSON.parse(readFileSync(p, 'utf8'));
  } catch {
    return fb;
  }
};

async function api(path, init = {}) {
  if (!ENV.ZERNIO_API_KEY) throw new Error('ZERNIO_API_KEY kosong — isi automation/zernio/.env');
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${ENV.ZERNIO_API_KEY}`,
      'Content-Type': 'application/json',
      ...(init.headers ?? {}),
    },
  });
  const text = await res.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = {raw: text};
  }
  if (!res.ok) throw new Error(`${init.method ?? 'GET'} ${path} → ${res.status}: ${text.slice(0, 400)}`);
  return body;
}

const profileId = () => {
  const p = ENV.ZERNIO_PROFILE_ID;
  if (!p) throw new Error('ZERNIO_PROFILE_ID kosong — lihat docs/03-publishing-zernio.md §2');
  return p;
};

function channelPlatform(channelId) {
  const channels = readJson(CHANNELS, []);
  const ch = channels.find((c) => c.id === channelId);
  if (!ch) throw new Error(`channel tidak dikenal: ${channelId}`);
  return ch.platform;
}

function accountFor(channelId) {
  const map = readJson(MAPPING, {});
  const id = map[channelId] ?? ENV[`ZERNIO_CHANNEL_${channelId.toUpperCase().replace(/-/g, '_')}`];
  if (!id) {
    throw new Error(
      `account id untuk ${channelId} belum ada. Jalankan "accounts" lalu "connect", ` +
        `atau isi ZERNIO_CHANNEL_${channelId.toUpperCase().replace(/-/g, '_')} di .env`,
    );
  }
  return id;
}

/* ------------------------------------------------------------------ media */
const mediaCache = new Map();

async function uploadMedia(file) {
  if (mediaCache.has(file)) return mediaCache.get(file);
  const abs = join(REPO, file.replace(/^\//, ''));
  if (!existsSync(abs)) throw new Error(`media tidak ada: ${abs}`);
  const bytes = readFileSync(abs);
  const name = abs.split('/').pop();
  const presign = await api('/media/presign', {
    method: 'POST',
    body: JSON.stringify({
      fileName: name,
      contentType: name.endsWith('.mp4') ? 'video/mp4' : 'image/jpeg',
      size: bytes.length,
    }),
  });
  const d = presign.data ?? presign;
  const uploadUrl = d.uploadUrl ?? d.upload_url;
  const publicUrl = d.publicUrl ?? d.public_url;
  if (!uploadUrl || !publicUrl) throw new Error(`presign tidak lengkap: ${JSON.stringify(presign).slice(0, 300)}`);
  const put = await fetch(uploadUrl, {
    method: 'PUT',
    headers: {'Content-Type': name.endsWith('.mp4') ? 'video/mp4' : 'image/jpeg'},
    body: bytes,
  });
  if (!put.ok) throw new Error(`upload media gagal ${put.status}`);
  mediaCache.set(file, publicUrl);
  return publicUrl;
}

async function mediaItemsFor(draft, dry) {
  if (dry) {
    return [{type: 'video', url: `${ENV.SITE_BASE_URL ?? '(presign)'}${draft.media.video}`}];
  }
  const video = await uploadMedia(draft.media.video);
  return [{type: 'video', url: video}];
}

/* ------------------------------------------------------------------ payload */
async function payloadFor(draft, dry) {
  const platform = channelPlatform(draft.channelId);
  const payload = {
    content: draft.body,
    scheduledFor: draft.publishAt,
    publishNow: false,
    isDraft: false,
    timezone: 'UTC',
    profileId: profileId(),
    platforms: [{platform, accountId: accountFor(draft.channelId)}],
    mediaItems: await mediaItemsFor(draft, dry),
    visibility: 'public',
  };
  if (platform === 'youtube' && ENV.ZERNIO_SEND_TITLE !== '0') payload.title = draft.title;
  return payload;
}

/* ------------------------------------------------------------------ commands */
async function cmdAccounts() {
  const {accounts = []} = await api(`/accounts?profileId=${profileId()}`);
  console.log(`[zernio] profil ${profileId()} — ${accounts.length} akun terhubung\n`);
  for (const a of accounts) {
    console.log(`  ${String(a.platform).padEnd(10)} ${a._id}  ${a.username ?? a.displayName ?? ''}${a.isActive === false ? ' (nonaktif)' : ''}`);
  }
  const channels = readJson(CHANNELS, []);
  const map = {};
  for (const ch of channels) {
    const candidate = accounts.find((a) => a.platform === ch.platform);
    if (candidate) {
      map[ch.id] = candidate._id;
      console.log(`  map ${ch.id.padEnd(22)} → ${candidate._id}`);
    } else {
      console.log(`  map ${ch.id.padEnd(22)} → (belum terhubung)`);
    }
  }
  if (Object.keys(map).length) {
    writeFileSync(MAPPING, JSON.stringify(map, null, 2));
    console.log('\nPemetaan disimpan di .zernio-mapping.json (gitignored).');
  }
}

async function cmdConnect() {
  const channels = readJson(CHANNELS, []);
  for (const ch of channels) {
    try {
      const r = await api(`/connect/${ch.platform}?profileId=${profileId()}`);
      const url = (r.data ?? r).url ?? (r.data ?? r).authUrl;
      console.log(`${ch.id.padEnd(22)} ${url ?? '(tidak ada url)'}`);
    } catch (e) {
      console.log(`${ch.id.padEnd(22)} gagal: ${e.message}`);
    }
  }
  console.log('\nBuka url di browser mesin ini, setujui akun, lalu ulangi "accounts".');
}

async function cmdPush() {
  const dry = has('dry-run');
  const day = opt('day') ? Number(opt('day')) : undefined;
  const platform = opt('platform');
  const limit = opt('limit') ? Number(opt('limit')) : undefined;
  const yes = has('yes');
  if (yes && !dry) throw new Error('--yes hanya diizinkan bersama --dry-run (tidak ada autoPublish)');

  const cal = readJson(CALENDAR, {drafts: []});
  let drafts = cal.drafts.filter((d) => d.status === 'DRAFT' || d.status === 'NEEDS_REVIEW');
  if (day) drafts = drafts.filter((d) => dayOf(d) === day);
  if (platform) drafts = drafts.filter((d) => d.platform === platform);
  drafts.sort((a, b) => a.publishAt.localeCompare(b.publishAt));
  if (limit) drafts = drafts.slice(0, limit);

  if (!drafts.length) return console.log('tidak ada draf yang cocok.');

  const rl = createInterface({input: process.stdin, output: process.stdout});
  const ask = (q) => new Promise((r) => rl.question(q, r));
  let sent = 0;
  let skipped = 0;

  for (const d of drafts) {
    const payload = await payloadFor(d, dry);
    console.log('\n─────────────────────────────────────────────');
    console.log(`${d.publishAtWib} WIB · ${d.channelId} · ${d.contentId}`);
    console.log(`judul : ${d.title}`);
    console.log(`durasi: ${d.durationSec}s`);
    console.log(`teks  : ${d.body.replace(/\n+/g, ' ⏎ ').slice(0, 220)}…`);
    if (dry) {
      console.log('PAYLOAD:');
      console.log(JSON.stringify(payload, null, 2));
      skipped++;
      continue;
    }
    const ok = yes ? 'y' : await ask('kirim ke Zernio? (y/N) ');
    if (ok.trim().toLowerCase() !== 'y') {
      skipped++;
      continue;
    }
    const created = await api('/posts', {method: 'POST', body: JSON.stringify(payload)});
    const postId = (created.data ?? created)._id ?? (created.data ?? created).id;
    d.status = 'SCHEDULED';
    d.zernioPostId = postId;
    d.reviewNote = `Disetujui lewat runner lokal; Zernio post ${postId}`;
    writeFileSync(CALENDAR, JSON.stringify(cal, null, 2));
    sent++;
    console.log(`  ✓ terjadwal (${postId})`);
  }
  rl.close();
  console.log(`\nselesai: ${sent} dijadwalkan, ${skipped} dilewati${dry ? ' (dry-run)' : ''}.`);
}

function dayOf(d) {
  const start = new Date(`${readJson(CALENDAR, {meta: {}}).meta.startDate}T00:00:00+07:00`);
  const t = new Date(`${d.publishAtWib.replace(' ', 'T')}:00+07:00`);
  return Math.floor((t - start) / 86400000) + 1;
}

async function cmdStatus() {
  const {posts = []} = await api(`/posts?status=scheduled&profileId=${profileId()}`);
  console.log(`[zernio] ${posts.length} post terjadwal\n`);
  for (const p of posts) {
    console.log(`  ${p.scheduledFor}  ${(p.platforms ?? []).map((x) => x.platform).join('+').padEnd(10)} ${String(p.content ?? '').slice(0, 70).replace(/\n/g, ' ')}`);
  }
}

async function cmdSync() {
  const {posts = []} = await api(`/posts?profileId=${profileId()}`);
  const byId = new Map(posts.map((p) => [String(p._id ?? p.id), p]));
  const cal = readJson(CALENDAR, {drafts: []});
  let changed = 0;
  for (const d of cal.drafts) {
    if (!d.zernioPostId) continue;
    const p = byId.get(String(d.zernioPostId));
    if (!p) continue;
    const st = String(p.status ?? '').toUpperCase();
    if (st === 'PUBLISHED' && d.status !== 'PUBLISHED') {
      d.status = 'PUBLISHED';
      changed++;
    }
    if (st === 'FAILED' && d.status !== 'FAILED') {
      d.status = 'FAILED';
      d.reviewNote = 'Zernio melaporkan FAILED — periksa dashboard';
      changed++;
    }
  }
  writeFileSync(CALENDAR, JSON.stringify(cal, null, 2));
  console.log(`sync selesai, ${changed} draf diperbarui.`);
}

const table = {accounts: cmdAccounts, connect: cmdConnect, push: cmdPush, status: cmdStatus, sync: cmdSync};
if (!table[cmd]) {
  console.log('perintah: accounts | connect | push [--dry-run --day N --platform P --limit N] | status | sync');
  process.exit(1);
}
table[cmd]().catch((e) => {
  console.error(`\n✗ ${e.message}`);
  process.exit(1);
});
