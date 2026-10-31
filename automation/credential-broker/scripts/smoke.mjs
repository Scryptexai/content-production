/**
 * Smoke test end-to-end lewat HTTP sungguhan (loopback), tanpa internet.
 *
 * Yang diuji:
 *   - handler Vercel dipasang di server Node asli
 *   - body dibaca dari stream (bukan req.body yang sudah diparsing)
 *   - panggilan PDP + upstream benar-benar terjadi lewat socket
 *
 * Jalankan: node scripts/smoke.mjs
 */

import http from 'node:http';
import { createApp } from '../src/app.js';

const SECRET = 'smoke-secret-123';

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function baseConfig(pdpUrl) {
  return {
    permitApiKey: 'permit_smoke',
    permitPdpUrl: pdpUrl,
    staticTokens: { 'tok-smoke': 'service:smoke' },
    supabaseJwtSecret: null,
    vaultProvider: 'env',
    vaultRpc: 'get_secret',
    auditProvider: 'console',
    auditTable: 'credential_audit',
    supabaseUrl: null,
    supabaseServiceKey: null,
    requestTimeoutMs: 5000,
    maxBodyBytes: 1_000_000,
    claimTtlSeconds: 300,
  };
}

function registry(baseUrl) {
  return {
    echo: {
      name: 'echo',
      resourceType: 'third_party_api',
      resourceKey: 'echo',
      action: 'invoke',
      baseUrl,
      secretName: 'SMOKE_API_KEY',
      auth: (secret) => ({ authorization: `Bearer ${secret}` }),
      allowedPathPrefixes: ['/v1/'],
      methods: ['GET', 'POST'],
      forwardHeaders: ['content-type'],
      allowClaim: false,
    },
  };
}

/** Server tiruan: berperan sebagai PDP DAN sebagai upstream. */
function makeMockServer() {
  return http.createServer((req, res) => {
    let raw = '';
    req.on('data', (c) => (raw += c));
    req.on('end', () => {
      res.setHeader('content-type', 'application/json');

      if (req.url === '/allowed') {
        const body = JSON.parse(raw || '{}');
        // Izinkan hanya subjek tertentu — meniru policy nyata.
        const allow = body.user?.key === 'service:smoke' && body.action === 'invoke';
        res.end(JSON.stringify({ allow }));
        return;
      }

      if (req.url?.startsWith('/v1/echo')) {
        // Sengaja TIDAK memantulkan header authorization mentah: kalau dipantulkan,
        // respons akan memuat rahasia karena ulah mock, bukan karena broker bocor.
        res.end(
          JSON.stringify({
            upstream_saw_correct_secret: req.headers.authorization === `Bearer ${SECRET}`,
            upstream_saw_client_secret: req.headers.authorization === 'Bearer rahasia-klien',
            upstream_saw_body: JSON.parse(raw || '{}'),
            path: req.url,
          }),
        );
        return;
      }

      res.statusCode = 404;
      res.end(JSON.stringify({ error: 'not found' }));
    });
  });
}

function post(port, payload, token) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(payload);
    const req = http.request(
      {
        host: '127.0.0.1',
        port,
        path: '/api/broker',
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'content-length': Buffer.byteLength(data),
          ...(token ? { authorization: `Bearer ${token}` } : {}),
        },
      },
      (res) => {
        let raw = '';
        res.on('data', (c) => (raw += c));
        res.on('end', () => {
          let parsed = null;
          try {
            parsed = JSON.parse(raw);
          } catch {
            parsed = raw;
          }
          resolve({ status: res.statusCode, body: parsed });
        });
      },
    );
    req.on('error', reject);
    req.end(data);
  });
}

const checks = [];
function check(name, condition, extra = '') {
  checks.push({ name, ok: Boolean(condition), extra });
  console.log(`${condition ? '✅' : '❌'} ${name}${extra ? ` — ${extra}` : ''}`);
}

async function main() {
  process.env.SMOKE_API_KEY = SECRET;

  const mock = makeMockServer();
  const mockPort = await listen(mock);
  const mockBase = `http://127.0.0.1:${mockPort}`;

  const app = createApp({
    config: baseConfig(mockBase),
    registry: registry(mockBase),
    logger: { log() {}, error: () => {} },
  });

  const broker = http.createServer((req, res) => app(req, res));
  const brokerPort = await listen(broker);

  // 1. Jalur bahagia
  const ok = await post(
    brokerPort,
    { upstream: 'echo', path: '/v1/echo', body: { pesan: 'halo' } },
    'tok-smoke',
  );
  check('allow → 200', ok.status === 200, `status ${ok.status}`);
  check('rahasia asli ditempelkan oleh broker', ok.body?.upstream_saw_correct_secret === true);
  check('body klien diteruskan utuh', ok.body?.upstream_saw_body?.pesan === 'halo');
  check('rahasia tidak kembali ke klien', !JSON.stringify(ok.body).includes(SECRET));

  // 1b. Klien mencoba menyelundupkan authorization sendiri → harus dibuang
  const smuggle = await post(
    brokerPort,
    {
      upstream: 'echo',
      path: '/v1/echo',
      headers: { authorization: 'Bearer rahasia-klien' },
    },
    'tok-smoke',
  );
  check('authorization klien dibuang', smuggle.body?.upstream_saw_client_secret === false);
  check('broker tetap memakai rahasia asli', smuggle.body?.upstream_saw_correct_secret === true);

  // 2. Tanpa token
  const noAuth = await post(brokerPort, { upstream: 'echo', path: '/v1/echo' }, null);
  check('tanpa token → 401', noAuth.status === 401, `status ${noAuth.status}`);

  // 3. Token asing
  const badAuth = await post(brokerPort, { upstream: 'echo', path: '/v1/echo' }, 'tok-palsu');
  check('token asing → 401', badAuth.status === 401, `status ${badAuth.status}`);

  // 4. Aksi yang tidak diizinkan policy → deny
  const denied = await post(
    brokerPort,
    { upstream: 'echo', path: '/v1/echo', action: 'hapus_semua' },
    'tok-smoke',
  );
  check('policy menolak → 403', denied.status === 403, `status ${denied.status}`);
  check('kode = permit_denied', denied.body?.code === 'permit_denied');

  // 5. Path traversal
  const traversal = await post(
    brokerPort,
    { upstream: 'echo', path: '/v1/../admin' },
    'tok-smoke',
  );
  check('path traversal ditolak', traversal.status === 400 || traversal.status === 403, `status ${traversal.status}`);

  // 6. PDP dimatikan → fail-closed
  const deadBroker = http.createServer(
    (req, res) =>
      createApp({
        config: baseConfig('http://127.0.0.1:1'), // port tertutup
        registry: registry(mockBase),
        logger: { log() {}, error: () => {} },
      })(req, res),
  );
  const deadPort = await listen(deadBroker);
  const dead = await post(deadPort, { upstream: 'echo', path: '/v1/echo' }, 'tok-smoke');
  check('PDP mati → 503 fail-closed', dead.status === 503, `status ${dead.status}`);
  check('kode = permit_unavailable', dead.body?.error === 'permit_unavailable');

  mock.close();
  broker.close();
  deadBroker.close();

  const failed = checks.filter((c) => !c.ok);
  console.log(`\n${checks.length - failed.length}/${checks.length} lulus`);
  if (failed.length > 0) process.exitCode = 1;
}

main().catch((err) => {
  console.error('smoke gagal:', err);
  process.exitCode = 1;
});
