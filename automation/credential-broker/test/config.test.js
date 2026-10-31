import test from 'node:test';
import assert from 'node:assert/strict';

import { loadConfig, ConfigError } from '../src/config.js';

test('konfigurasi minimal valid', () => {
  const config = loadConfig({
    PERMIT_API_KEY: 'permit_k',
    BROKER_STATIC_TOKENS: '{"tok":"service:a"}',
  });

  assert.equal(config.permitApiKey, 'permit_k');
  assert.equal(config.permitPdpUrl, 'https://cloudpdp.api.permit.io');
  assert.equal(config.vaultProvider, 'env');
  assert.equal(config.auditProvider, 'console');
  assert.deepEqual(config.staticTokens, { tok: 'service:a' });
});

test('tanpa PERMIT_API_KEY → gagal dan menyebut nama variabel', () => {
  assert.throws(
    () => loadConfig({ BROKER_STATIC_TOKENS: '{"a":"b"}' }),
    (err) => err instanceof ConfigError && /PERMIT_API_KEY/.test(err.message),
  );
});

test('tanpa metode identitas apa pun → gagal', () => {
  assert.throws(
    () => loadConfig({ PERMIT_API_KEY: 'x' }),
    (err) => err instanceof ConfigError && /BROKER_STATIC_TOKENS|SUPABASE_JWT_SECRET/.test(err.message),
  );
});

test('BROKER_STATIC_TOKENS bukan JSON → gagal, pesan tidak memuat isi token', () => {
  try {
    loadConfig({ PERMIT_API_KEY: 'x', BROKER_STATIC_TOKENS: 'bukan-json-rahasia' });
    assert.fail('harus melempar');
  } catch (err) {
    assert.ok(err instanceof ConfigError);
    assert.ok(!err.message.includes('bukan-json-rahasia'));
  }
});

test('VAULT_PROVIDER tidak dikenal → gagal', () => {
  assert.throws(
    () => loadConfig({ PERMIT_API_KEY: 'x', BROKER_STATIC_TOKENS: '{"a":"b"}', VAULT_PROVIDER: 'ajaib' }),
    ConfigError,
  );
});

test('vault supabase tanpa kredensial supabase → gagal', () => {
  assert.throws(
    () =>
      loadConfig({
        PERMIT_API_KEY: 'x',
        BROKER_STATIC_TOKENS: '{"a":"b"}',
        VAULT_PROVIDER: 'supabase',
      }),
    (err) => err instanceof ConfigError && /SUPABASE_URL/.test(err.message),
  );
});

test('angka tak valid jatuh ke default', () => {
  const config = loadConfig({
    PERMIT_API_KEY: 'x',
    BROKER_STATIC_TOKENS: '{"a":"b"}',
    REQUEST_TIMEOUT_MS: 'xyz',
  });
  assert.equal(config.requestTimeoutMs, 15000);
});

test('trailing slash pada PDP dibuang', () => {
  const config = loadConfig({
    PERMIT_API_KEY: 'x',
    BROKER_STATIC_TOKENS: '{"a":"b"}',
    PERMIT_PDP_URL: 'https://pdp.test///',
  });
  assert.equal(config.permitPdpUrl, 'https://pdp.test');
});
