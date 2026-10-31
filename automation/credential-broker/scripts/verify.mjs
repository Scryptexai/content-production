#!/usr/bin/env node
/**
 * Uji koneksi ke akun Permit-mu — dan jelaskan penyebab kalau gagal.
 *
 * Semua kode HTTP diterjemahkan jadi diagnosis yang bisa ditindaklanjuti,
 * karena inilah bagian yang paling sering membingungkan saat pertama menyiapkan.
 *
 * ── Uji langsung ke Permit (dari mesinmu) ────────────────────────────
 *   node --env-file=.env scripts/verify.mjs
 *
 * ── Uji lewat broker yang sudah deploy (mode probe, tanpa rahasia) ───
 *   node scripts/verify.mjs --remote https://proyek.vercel.app --token <BROKER_TOKEN>
 */

import { UPSTREAM_NAMES } from '../src/upstreams.js';

const args = process.argv.slice(2);

function arg(name) {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
}

const REMOTE = arg('--remote');
const TOKEN = arg('--token');

const OK = '✅';
const NO = '❌';
const WARN = '⚠️';

function line(symbol, title, detail) {
  console.log(`${symbol} ${title}`);
  if (detail) {
    for (const d of String(detail).split('\n')) console.log(`     ${d}`);
  }
}

/** Terjemahkan status HTTP Permit jadi diagnosis. */
function diagnoseHttp(status) {
  if (status === 401) {
    return [
      'API key ditolak Permit (401).',
      'Periksa: apakah PERMIT_API_KEY disalin utuh, dan apakah ia milik',
      'environment yang sama dengan yang ada di dashboard?',
      'API key terikat ke satu project+environment — key project lain akan ditolak.',
    ].join('\n');
  }
  if (status === 403) {
    return [
      'Ditolak (403).',
      'Biasanya berarti key tidak punya cakupan untuk project/environment ini,',
      'atau PDP URL menunjuk environment yang berbeda.',
    ].join('\n');
  }
  if (status === 404) {
    return [
      '404 dari host PDP.',
      'PERMIT_PDP_URL kemungkinan salah. Nilai yang benar untuk Cloud PDP:',
      'https://cloudpdp.api.permit.io   (tanpa /allowed di belakangnya)',
    ].join('\n');
  }
  return `Permintaan gagal dengan HTTP ${status}. Cek log PDP / status layanan Permit.`;
}

async function checkLocal() {
  const apiKey = process.env.PERMIT_API_KEY;
  const pdpUrl = (process.env.PERMIT_PDP_URL || 'https://cloudpdp.api.permit.io').replace(/\/+$/, '');

  console.log('─ Uji langsung ke Permit ─────────────────────────────\n');

  if (!apiKey) {
    line(NO, 'PERMIT_API_KEY belum diisi', 'Ambil dari dashboard Permit → Settings → API Keys.');
    console.log('\nJalankan dengan: node --env-file=.env scripts/verify.mjs');
    process.exitCode = 1;
    return;
  }

  line(OK, 'PERMIT_API_KEY terbaca', `panjang ${apiKey.length} karakter`);
  line(OK, 'PDP yang dituju', pdpUrl);

  console.log('\nMenghubungi PDP…\n');

  let anyAllow = false;
  let anySuccess = false;

  for (const name of UPSTREAM_NAMES) {
    const { resolveUpstream } = await import('../src/upstreams.js');
    const upstream = resolveUpstream(name);

    const body = {
      user: { key: 'probe:verify' },
      action: upstream.action,
      resource: {
        type: upstream.resourceType,
        key: upstream.resourceKey,
        tenant: 'default',
        attributes: {},
      },
      context: {},
    };

    try {
      const res = await fetch(`${pdpUrl}/allowed`, {
        method: 'POST',
        headers: {
          authorization: `Bearer ${apiKey}`,
          'content-type': 'application/json',
        },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(10_000),
      });

      if (!res.ok) {
        line(NO, `${upstream.resourceKey}:${upstream.action}`, diagnoseHttp(res.status));
        continue;
      }

      anySuccess = true;
      const data = await res.json();
      const allow = data?.allow === true || data?.result?.allow === true;

      if (allow) {
        anyAllow = true;
        line(OK, `${upstream.resourceKey}:${upstream.action} → ALLOW`);
      } else {
        line(
          WARN,
          `${upstream.resourceKey}:${upstream.action} → DENY`,
          [
            'Koneksi ke akun Permit BERHASIL. Yang menolak adalah policy-nya.',
            'Artinya: resource/action ini belum ada di Permit, atau subjek',
            '"probe:verify" belum punya role yang mengizinkannya.',
            'Itu normal untuk subjek uji — yang penting balasannya sampai.',
          ].join('\n'),
        );
      }
    } catch (err) {
      line(
        NO,
        `${upstream.resourceKey}:${upstream.action} → tidak terjangkau`,
        [
          `Penyebab: ${err?.message ?? err}`,
          'Kalau pesan menyebut DNS/ENOTFOUND: host PDP tidak bisa di-resolve.',
          'Kalau ECONNREFUSED/timeout: jaringan atau firewall memblokir.',
          'Ingat: sandbox pengembangan hanya bisa GitHub/npm/PyPI —',
          'jalankan skrip ini di mesin sendiri atau di Vercel.',
        ].join('\n'),
      );
    }
  }

  console.log('\n─────────────────────────────────────────────────────');
  if (anyAllow) {
    console.log(`${OK} Terhubung ke akun Permit, dan minimal satu action diizinkan.`);
    console.log('   Broker siap dipakai untuk resource tersebut.');
  } else if (anySuccess) {
    console.log(`${OK} Terhubung ke akun Permit.`);
    console.log(`${WARN} Semua action DENY untuk subjek uji — wajar.`);
    console.log('   Langkah berikutnya: buat resource/action/role di Permit,');
    console.log('   lalu uji dengan subjek yang benar-benar punya role.');
  } else {
    console.log(`${NO} Belum berhasil terhubung. Perbaiki temuan di atas dulu.`);
    process.exitCode = 1;
  }
}

async function checkRemote(baseUrl, token) {
  console.log('─ Uji lewat broker yang sudah deploy ────────────────\n');

  if (!token) {
    line(NO, 'Token broker belum diberikan', 'Tambahkan --token <BROKER_TOKEN>.');
    process.exitCode = 1;
    return;
  }

  const base = baseUrl.replace(/\/+$/, '');

  // 1. Health
  try {
    const res = await fetch(`${base}/api/health`, { signal: AbortSignal.timeout(10_000) });
    const body = await res.json();
    if (body.ok) {
      line(OK, 'Konfigurasi broker terbaca', `PDP: ${body.pdp}`);
      line(
        OK,
        'Channel identitas',
        `token statis: ${body.identity.static_tokens}, supabase JWT: ${body.identity.supabase_jwt}`,
      );
    } else {
      line(NO, 'Konfigurasi broker bermasalah', body.message || JSON.stringify(body));
      process.exitCode = 1;
      return;
    }
  } catch (err) {
    line(NO, 'Tidak bisa menjangkau /api/health', err?.message ?? String(err));
    process.exitCode = 1;
    return;
  }

  // 2. Probe policy lewat broker
  console.log('');
  for (const name of UPSTREAM_NAMES) {
    try {
      const res = await fetch(`${base}/api/broker`, {
        method: 'POST',
        headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json' },
        body: JSON.stringify({ upstream: name, mode: 'probe' }),
        signal: AbortSignal.timeout(15_000),
      });
      const body = await res.json();

      if (res.status === 401) {
        line(NO, `${name}: token broker ditolak`, 'Periksa BROKER_STATIC_TOKENS / JWT.');
        process.exitCode = 1;
        return;
      }
      if (res.status === 403) {
        line(OK, `${name} → DENY`, 'Broker hidup dan Permit menjawab (policy menolak).');
      } else if (res.status === 200) {
        line(
          body.allow ? OK : WARN,
          `${name} → ${body.allow ? 'ALLOW' : 'DENY'}`,
          `subject: ${body.subject}`,
        );
      } else {
        line(NO, `${name}: HTTP ${res.status}`, body?.message || JSON.stringify(body));
      }
    } catch (err) {
      line(NO, `${name}: gagal`, err?.message ?? String(err));
      process.exitCode = 1;
    }
  }

  console.log('\n─────────────────────────────────────────────────────');
  console.log('DENY di sini berarti jalur sudah tersambung penuh:');
  console.log('klien → broker → Permit → jawaban. Yang tersisa hanya policy.');
}

if (REMOTE) {
  await checkRemote(REMOTE, TOKEN);
} else {
  await checkLocal();
}
