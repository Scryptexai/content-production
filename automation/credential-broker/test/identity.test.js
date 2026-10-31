import test from 'node:test';
import assert from 'node:assert/strict';

import { authenticate, verifyJwtHS256 } from '../src/identity.js';
import { HttpError } from '../src/http.js';
import { makeConfig, makeReq, signJwt } from './helpers.js';

const SECRET = 'rahasia-jwt-test-yang-cukup-panjang';

test('token statis yang cocok → subject dari peta', async () => {
  const config = makeConfig();
  const req = makeReq({ headers: { authorization: 'Bearer tok-good' } });
  const identity = await authenticate(req, config);
  assert.deepEqual(identity, { subject: 'service:reporting', method: 'static_token' });
});

test('tanpa header → 401 missing_token', async () => {
  await assert.rejects(
    () => authenticate(makeReq(), makeConfig()),
    (err) => err instanceof HttpError && err.code === 'missing_token',
  );
});

test('skema selain Bearer → 401', async () => {
  const req = makeReq({ headers: { authorization: 'Basic abc' } });
  await assert.rejects(() => authenticate(req, makeConfig()), HttpError);
});

test('token asal-asalan → 401', async () => {
  const req = makeReq({ headers: { authorization: 'Bearer tok-palsu' } });
  await assert.rejects(
    () => authenticate(req, makeConfig()),
    (err) => err instanceof HttpError && err.status === 401,
  );
});

test('JWT sah → subject dari klaim sub', async () => {
  const token = signJwt({ sub: 'user:dana', exp: Math.floor(Date.now() / 1000) + 60 }, SECRET);
  const config = makeConfig({ staticTokens: {}, supabaseJwtSecret: SECRET });
  const identity = await authenticate(makeReq({ headers: { authorization: `Bearer ${token}` } }), config);
  assert.deepEqual(identity, { subject: 'user:dana', method: 'supabase_jwt' });
});

test('JWT kedaluwarsa → 401 token_expired', async () => {
  const token = signJwt({ sub: 'user:dana', exp: Math.floor(Date.now() / 1000) - 10 }, SECRET);
  const config = makeConfig({ staticTokens: {}, supabaseJwtSecret: SECRET });
  await assert.rejects(
    () => authenticate(makeReq({ headers: { authorization: `Bearer ${token}` } }), config),
    (err) => err instanceof HttpError && err.code === 'token_expired',
  );
});

test('JWT tanda tangan salah → 401', async () => {
  const token = signJwt({ sub: 'user:dana' }, 'kunci-yang-salah');
  const config = makeConfig({ staticTokens: {}, supabaseJwtSecret: SECRET });
  await assert.rejects(
    () => authenticate(makeReq({ headers: { authorization: `Bearer ${token}` } }), config),
    (err) => err instanceof HttpError && err.status === 401,
  );
});

test('alg:none tidak bisa dipakai menembus verifikasi', async () => {
  // Header alg none, tanda tangan kosong → tetap harus gagal.
  const header = Buffer.from(JSON.stringify({ alg: 'none', typ: 'JWT' })).toString('base64url');
  const payload = Buffer.from(JSON.stringify({ sub: 'user:penyusup' })).toString('base64url');
  const token = `${header}.${payload}.`;

  assert.throws(() => verifyJwtHS256(token, SECRET), HttpError);
});

test('JWT tanpa klaim sub → 401', async () => {
  const token = signJwt({ email: 'x@y.z' }, SECRET);
  const config = makeConfig({ staticTokens: {}, supabaseJwtSecret: SECRET });
  await assert.rejects(
    () => authenticate(makeReq({ headers: { authorization: `Bearer ${token}` } }), config),
    (err) => err instanceof HttpError && err.status === 401,
  );
});

test('token statis dicocokkan mendahului JWT', async () => {
  const config = makeConfig({ supabaseJwtSecret: SECRET });
  const identity = await authenticate(
    makeReq({ headers: { authorization: 'Bearer tok-good' } }),
    config,
  );
  assert.equal(identity.method, 'static_token');
});
