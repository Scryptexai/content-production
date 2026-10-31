import test from 'node:test';
import assert from 'node:assert/strict';

import { createApp } from '../src/app.js';
import { makeConfig, makeRegistry, makeFetch, makeReq, makeRes } from './helpers.js';

const PDP_ALLOW = ['https://pdp.test/allowed', { body: { allow: true } }];
const PDP_DENY = ['https://pdp.test/allowed', { body: { allow: false } }];
const PDP_DOWN = ['https://pdp.test/allowed', { status: 502, body: {} }];
const UPSTREAM_OK = ['https://dummy.test/v1/echo', { body: { ok: true, via: 'upstream' } }];

const goodAuth = { authorization: 'Bearer tok-good' };

process.env.DUMMY_API_KEY = 'rahasia-asli-dummy';

function build({ routes, config = {}, registryOverrides = {}, logger } = {}) {
  const fetchImpl = makeFetch(routes);
  const auditEvents = [];
  const app = createApp({
    config: makeConfig({ auditProvider: 'none', ...config }),
    registry: makeRegistry(registryOverrides),
    fetchImpl,
    logger: logger ?? { log() {}, error() {} },
  });
  return { app, fetchImpl, auditEvents };
}

test('allow → meneruskan ke upstream dengan rahasia ditempelkan', async () => {
  const { app, fetchImpl } = build({ routes: [PDP_ALLOW, UPSTREAM_OK] });

  const res = makeRes();
  await app(
    makeReq({
      headers: goodAuth,
      body: { upstream: 'dummy', path: '/v1/echo', body: { hello: 'dunia' } },
    }),
    res,
  );

  assert.equal(res.statusCode, 200);
  assert.deepEqual(res.json, { ok: true, via: 'upstream' });

  const upstreamCall = fetchImpl.callsTo('https://dummy.test')[0];
  assert.equal(upstreamCall.headers.authorization, 'Bearer rahasia-asli-dummy');
  assert.deepEqual(JSON.parse(upstreamCall.init.body), { hello: 'dunia' });

  // Rahasia tidak boleh muncul di body respons.
  assert.ok(!res.body.includes('rahasia-asli-dummy'));
});

test('allow → authorization dari klien tidak ikut diteruskan', async () => {
  const { app, fetchImpl } = build({ routes: [PDP_ALLOW, UPSTREAM_OK] });

  await app(
    makeReq({
      headers: { authorization: 'Bearer tok-good', 'content-type': 'application/json' },
      body: {
        upstream: 'dummy',
        path: '/v1/echo',
        headers: { authorization: 'Bearer klien-jahat', 'content-type': 'application/json' },
      },
    }),
    makeRes(),
  );

  const upstreamCall = fetchImpl.callsTo('https://dummy.test')[0];
  assert.equal(upstreamCall.headers.authorization, 'Bearer rahasia-asli-dummy');
});

test('deny → 403 dan upstream TIDAK pernah dipanggil', async () => {
  const { app, fetchImpl } = build({ routes: [PDP_DENY, UPSTREAM_OK] });

  const res = makeRes();
  await app(makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo' } }), res);

  assert.equal(res.statusCode, 403);
  assert.equal(res.json.code, 'permit_denied');
  assert.equal(fetchImpl.callsTo('https://dummy.test').length, 0, 'upstream tidak boleh dihubungi');
});

test('PDP mati → 503 fail-closed, upstream tidak dihubungi', async () => {
  const { app, fetchImpl } = build({ routes: [PDP_DOWN, UPSTREAM_OK] });

  const res = makeRes();
  await app(makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo' } }), res);

  assert.equal(res.statusCode, 503);
  assert.equal(res.json.error, 'permit_unavailable');
  assert.equal(fetchImpl.callsTo('https://dummy.test').length, 0);
});

test('tanpa token → 401, PDP tidak dihubungi', async () => {
  const { app, fetchImpl } = build({ routes: [PDP_ALLOW, UPSTREAM_OK] });

  const res = makeRes();
  await app(makeReq({ body: { upstream: 'dummy', path: '/v1/echo' } }), res);

  assert.equal(res.statusCode, 401);
  assert.equal(fetchImpl.callsTo('https://pdp.test').length, 0);
});

test('upstream tak terdaftar → 404', async () => {
  const { app } = build({ routes: [PDP_ALLOW] });

  const res = makeRes();
  await app(makeReq({ headers: goodAuth, body: { upstream: 'entah', path: '/v1/x' } }), res);

  assert.equal(res.statusCode, 404);
  assert.equal(res.json.error, 'unknown_upstream');
});

test('path traversal → 400/403 sebelum upstream', async () => {
  const { app, fetchImpl } = build({ routes: [PDP_ALLOW, UPSTREAM_OK] });

  const res = makeRes();
  await app(
    makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/../../admin' } }),
    res,
  );

  assert.ok([400, 403].includes(res.statusCode));
  assert.equal(fetchImpl.callsTo('https://dummy.test').length, 0);
});

test('path di luar daftar izin → 403 path_not_allowed', async () => {
  const { app } = build({ routes: [PDP_ALLOW] });

  const res = makeRes();
  await app(makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/admin/rahasia' } }), res);

  assert.equal(res.statusCode, 403);
  assert.equal(res.json.error, 'path_not_allowed');
});

test('metode di luar daftar izin → 405', async () => {
  const { app } = build({ routes: [PDP_ALLOW] });

  const res = makeRes();
  await app(
    makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo', method: 'PUT' } }),
    res,
  );

  assert.equal(res.statusCode, 405);
});

test('mode claim ditolak kalau upstream tidak mengizinkannya', async () => {
  const { app, fetchImpl } = build({ routes: [PDP_ALLOW] });

  const res = makeRes();
  await app(
    makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo', mode: 'claim' } }),
    res,
  );

  assert.equal(res.statusCode, 403);
  assert.equal(res.json.code, 'claim_not_allowed');
  assert.ok(!res.body.includes('rahasia-asli-dummy'));
  assert.equal(fetchImpl.callsTo('https://dummy.test').length, 0);
});

test('mode claim yang diizinkan → mengembalikan kunci + expires_at', async () => {
  const { app } = build({
    routes: [PDP_ALLOW],
    registryOverrides: { allowClaim: true },
  });

  const res = makeRes();
  await app(
    makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo', mode: 'claim' } }),
    res,
  );

  assert.equal(res.statusCode, 200);
  assert.equal(res.json.credential, 'rahasia-asli-dummy');
  assert.equal(res.json.credential_kind, 'static_api_key');
  assert.ok(Date.parse(res.json.expires_at) > Date.now());
});

test('mode tidak dikenal → 400', async () => {
  const { app } = build({ routes: [PDP_ALLOW] });

  const res = makeRes();
  await app(
    makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo', mode: 'sihir' } }),
    res,
  );

  assert.equal(res.statusCode, 400);
  assert.equal(res.json.error, 'invalid_mode');
});

test('metode selain POST → 405', async () => {
  const { app } = build({ routes: [PDP_ALLOW] });

  const res = makeRes();
  await app(makeReq({ method: 'GET' }), res);

  assert.equal(res.statusCode, 405);
  assert.equal(res.headers.allow, 'POST');
});

test('rahasia tidak ada di vault → 500 secret_not_found, pesan tidak membocorkan nama env', async () => {
  delete process.env.DUMMY_API_KEY;
  const { app } = build({ routes: [PDP_ALLOW] });

  const res = makeRes();
  await app(makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo' } }), res);

  process.env.DUMMY_API_KEY = 'rahasia-asli-dummy';

  assert.equal(res.statusCode, 500);
  assert.equal(res.json.error, 'secret_not_found');
});

test('audit dicatat untuk keputusan allow maupun deny', async () => {
  const logged = [];
  const logger = { log: (line) => logged.push(JSON.parse(line)), error() {} };

  for (const route of [PDP_ALLOW, PDP_DENY]) {
    const { app } = build({
      routes: [route, UPSTREAM_OK],
      config: { auditProvider: 'console' },
      logger,
    });
    await app(makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo' } }), makeRes());
  }

  assert.equal(logged.length, 2);
  assert.equal(logged[0].audit.outcome, 'allowed');
  assert.equal(logged[1].audit.outcome, 'denied');
  assert.equal(logged[0].audit.subject, 'service:reporting');
  assert.equal(logged[0].audit.upstream, 'dummy');
  assert.ok(logged[0].audit.request_id);
});

test('audit tidak pernah memuat rahasia', async () => {
  const logged = [];
  const logger = { log: (line) => logged.push(line), error() {} };
  const { app } = build({
    routes: [PDP_ALLOW, UPSTREAM_OK],
    config: { auditProvider: 'console' },
    logger,
  });

  await app(makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo' } }), makeRes());

  assert.ok(!logged.join('\n').includes('rahasia-asli-dummy'));
});

test('kegagalan audit tidak menggagalkan permintaan yang sudah allow', async () => {
  const fetchImpl = makeFetch([
    PDP_ALLOW,
    UPSTREAM_OK,
    ['https://audit.test', { status: 500, body: {} }],
  ]);
  const app = createApp({
    config: makeConfig({
      auditProvider: 'supabase',
      supabaseUrl: 'https://audit.test',
      supabaseServiceKey: 'kunci-service',
    }),
    registry: makeRegistry(),
    fetchImpl,
    logger: { log() {}, error() {} },
  });

  const res = makeRes();
  await app(makeReq({ headers: goodAuth, body: { upstream: 'dummy', path: '/v1/echo' } }), res);

  assert.equal(res.statusCode, 200);
});
