import test from 'node:test';
import assert from 'node:assert/strict';

import { createPermitClient, PermitUnavailableError } from '../src/permit.js';
import { makeFetch } from './helpers.js';

const baseArgs = {
  subject: 'user:dana',
  action: 'invoke',
  resourceType: 'ai_provider',
  resourceKey: 'openai',
  tenant: 'default',
  attributes: { tier: 'pro' },
  context: {},
};

test('mengirim POST ke {pdp}/allowed dengan payload sesuai kontrak SDK', async () => {
  const fetchImpl = makeFetch([
    ['https://pdp.test/allowed', { body: { allow: true } }],
  ]);
  const permit = createPermitClient({
    pdpUrl: 'https://pdp.test/',
    apiKey: 'kunci',
    fetchImpl,
  });

  const result = await permit.check(baseArgs);

  assert.equal(result.allow, true);
  assert.equal(fetchImpl.calls[0].url, 'https://pdp.test/allowed');
  assert.equal(fetchImpl.calls[0].init.method, 'POST');
  assert.equal(fetchImpl.calls[0].headers.authorization, 'Bearer kunci');

  const sent = JSON.parse(fetchImpl.calls[0].init.body);
  assert.deepEqual(sent, {
    user: { key: 'user:dana' },
    action: 'invoke',
    resource: {
      type: 'ai_provider',
      key: 'openai',
      tenant: 'default',
      attributes: { tier: 'pro' },
    },
    context: {},
  });
});

test('allow:false → ditolak', async () => {
  const permit = createPermitClient({
    pdpUrl: 'https://pdp.test',
    apiKey: 'k',
    fetchImpl: makeFetch([['https://pdp.test/allowed', { body: { allow: false } }]]),
  });
  assert.equal((await permit.check(baseArgs)).allow, false);
});

test('bentuk OPA {result:{allow}} juga dikenali', async () => {
  const permit = createPermitClient({
    pdpUrl: 'https://pdp.test',
    apiKey: 'k',
    fetchImpl: makeFetch([['https://pdp.test/allowed', { body: { result: { allow: true } } }]]),
  });
  assert.equal((await permit.check(baseArgs)).allow, true);
});

test('jawaban tanpa field allow dianggap menolak', async () => {
  const permit = createPermitClient({
    pdpUrl: 'https://pdp.test',
    apiKey: 'k',
    fetchImpl: makeFetch([['https://pdp.test/allowed', { body: { aneh: true } }]]),
  });
  assert.equal((await permit.check(baseArgs)).allow, false);
});

test('HTTP 500 dari PDP → PermitUnavailableError', async () => {
  const permit = createPermitClient({
    pdpUrl: 'https://pdp.test',
    apiKey: 'k',
    fetchImpl: makeFetch([['https://pdp.test/allowed', { status: 500, body: {} }]]),
  });
  await assert.rejects(() => permit.check(baseArgs), PermitUnavailableError);
});

test('kegagalan jaringan → PermitUnavailableError', async () => {
  const permit = createPermitClient({
    pdpUrl: 'https://pdp.test',
    apiKey: 'k',
    fetchImpl: makeFetch([['https://pdp.test/allowed', { throws: 'ECONNREFUSED' }]]),
  });
  await assert.rejects(() => permit.check(baseArgs), PermitUnavailableError);
});

test('balasan bukan JSON → PermitUnavailableError', async () => {
  const permit = createPermitClient({
    pdpUrl: 'https://pdp.test',
    apiKey: 'k',
    fetchImpl: makeFetch([['https://pdp.test/allowed', { body: 'bukan json' }]]),
  });
  await assert.rejects(() => permit.check(baseArgs), PermitUnavailableError);
});
