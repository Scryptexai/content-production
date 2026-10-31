#!/usr/bin/env node
/**
 * Buat resource + action + role di akun Permit-mu, sesuai registry broker.
 *
 * Ini yang membuat "setup terhubung ke akun Permit": broker hanya tahu NAMA
 * resource (ai_provider/openai, dsb). Kalau nama itu belum ada di project
 * Permit-mu, setiap check akan dijawab DENY — bukan karena broker rusak,
 * tapi karena policy-nya memang belum punya objeknya.
 *
 * PERHATIAN: skrip ini memanggil api.permit.io (REST API untuk mengelola schema).
 * Itu berbeda dari PDP yang dipakai broker saat melayani permintaan.
 *   - mengelola policy  → https://api.permit.io
 *   - memutuskan akses  → https://cloudpdp.api.permit.io   (PERMIT_PDP_URL)
 *
 * Default DRY RUN — tidak mengubah apa pun. Tambahkan --apply untuk menulis.
 *
 *   node --env-file=.env scripts/seed-permit.mjs
 *   node --env-file=.env scripts/seed-permit.mjs --apply
 *
 * Butuh: PERMIT_API_KEY, PERMIT_PROJECT_ID, PERMIT_ENV_ID
 * Keduanya terlihat di dashboard Permit (Settings → Project / Environment).
 */

import { UPSTREAM_NAMES, resolveUpstream } from '../src/upstreams.js';

const APPLY = process.argv.includes('--apply');
const API = 'https://api.permit.io';

const apiKey = process.env.PERMIT_API_KEY;
const projectId = process.env.PERMIT_PROJECT_ID;
const envId = process.env.PERMIT_ENV_ID;

const ROLE_KEY = process.env.SEED_ROLE_KEY || 'credential_user';

function fail(msg) {
  console.error(`❌ ${msg}`);
  process.exitCode = 1;
}

if (!apiKey) fail('PERMIT_API_KEY belum diisi.');
if (!projectId) fail('PERMIT_PROJECT_ID belum diisi.');
if (!envId) fail('PERMIT_ENV_ID belum diisi.');
if (process.exitCode === 1) {
  console.error('\nLihat SETUP.md bagian "Menyambungkan ke akun Permit".');
  process.exit();
}

async function call(method, path, body) {
  const res = await fetch(`${API}${path}`, {
    method,
    headers: {
      authorization: `Bearer ${apiKey}`,
      'content-type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
    signal: AbortSignal.timeout(15_000),
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }
  return { status: res.status, ok: res.ok, data };
}

function summarize(res) {
  if (res.ok) return 'ok';
  if (res.status === 409) return 'sudah ada';
  if (res.status === 422) return `tidak valid (422): ${JSON.stringify(res.data?.detail ?? res.data)}`;
  return `HTTP ${res.status}: ${JSON.stringify(res.data?.detail ?? res.data)}`;
}

async function main() {
  console.log(`\nProject: ${projectId}   Environment: ${envId}`);
  console.log(APPLY ? 'Mode: APPLY (menulis ke akun Permit)\n' : 'Mode: DRY RUN (tidak mengubah apa pun)\n');

  const schema = `/v2/schema/${encodeURIComponent(projectId)}/${encodeURIComponent(envId)}`;
  const permissions = [];

  // 1. Resource + action
  for (const name of UPSTREAM_NAMES) {
    const upstream = resolveUpstream(name);
    const resourceKey = upstream.resourceKey;
    const permission = `${resourceKey}:${upstream.action}`;
    permissions.push(permission);

    console.log(`Resource  ${resourceKey}`);
    console.log(`  type    : ${upstream.resourceType}`);
    console.log(`  action  : ${upstream.action}`);
    console.log(`  izin    : ${permission}`);

    if (!APPLY) {
      console.log('  → akan dibuat / dipastikan ada\n');
      continue;
    }

    const payload = {
      key: resourceKey,
      name: resourceKey,
      actions: { [upstream.action]: { name: upstream.action } },
    };

    const created = await call('POST', `${schema}/resources`, payload);
    if (created.ok) {
      console.log('  → dibuat\n');
      continue;
    }
    if (created.status === 409) {
      // Sudah ada: pastikan action-nya juga ada.
      const patched = await call('PATCH', `${schema}/resources/${encodeURIComponent(resourceKey)}`, {
        actions: { [upstream.action]: { name: upstream.action } },
      });
      console.log(`  → sudah ada, action disinkronkan (${summarize(patched)})\n`);
      continue;
    }
    console.log(`  → GAGAL: ${summarize(created)}\n`);
    process.exitCode = 1;
  }

  // 2. Role yang mengizinkan semua action di atas
  console.log(`Role      ${ROLE_KEY}`);
  console.log(`  izin    : ${permissions.join(', ')}`);

  if (!APPLY) {
    console.log('  → akan dibuat / dipastikan ada\n');
  } else {
    const rolePayload = { key: ROLE_KEY, name: ROLE_KEY, permissions };
    const created = await call('POST', `${schema}/roles`, rolePayload);

    if (created.ok) {
      console.log('  → dibuat\n');
    } else if (created.status === 409) {
      const patched = await call('PATCH', `${schema}/roles/${encodeURIComponent(ROLE_KEY)}`, {
        permissions,
      });
      console.log(`  → sudah ada, izin disinkronkan (${summarize(patched)})\n`);
    } else {
      console.log(`  → GAGAL: ${summarize(created)}\n`);
      process.exitCode = 1;
    }
  }

  console.log('─────────────────────────────────────────────────────');
  if (!APPLY) {
    console.log('Ini baru rencana. Jalankan ulang dengan --apply untuk menerapkan:');
    console.log('  node --env-file=.env scripts/seed-permit.mjs --apply');
  } else {
    console.log('Schema siap. Langkah terakhir yang TIDAK bisa diotomatiskan:');
    console.log(`  1. Di dashboard Permit, assign role "${ROLE_KEY}" ke subjek yang memakai broker`);
    console.log('     (user atau service account), di tenant yang sesuai.');
    console.log('  2. Uji: node --env-file=.env scripts/verify.mjs');
    console.log('\nSelama role belum di-assign, check akan tetap DENY — itu benar.');
  }
}

await main();
