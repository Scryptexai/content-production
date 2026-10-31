import test from 'node:test';
import assert from 'node:assert/strict';

import {
  resolveUpstream,
  assertSafePath,
  buildUpstreamUrl,
  pickForwardHeaders,
  UPSTREAM_NAMES,
  claimEnabledNames,
} from '../src/upstreams.js';
import { HttpError } from '../src/http.js';
import { makeRegistry } from './helpers.js';

test('registry produksi tidak mengizinkan claim secara default', () => {
  assert.deepEqual([...UPSTREAM_NAMES].sort(), ['openai', 'slack', 'stripe'].sort());
  assert.deepEqual(claimEnabledNames(), []);
});

test('registry produksi di-freeze', () => {
  const upstream = resolveUpstream('openai');
  assert.throws(() => {
    'use strict';
    upstream.baseUrl = 'https://evil.test';
  }, TypeError);
});

test('upstream tak dikenal → 404', () => {
  assert.throws(() => resolveUpstream('tidakada'), (err) => err instanceof HttpError && err.status === 404);
});

test('upstream kosong → 400', () => {
  assert.throws(() => resolveUpstream(''), (err) => err instanceof HttpError && err.status === 400);
});

test('upstream bernama properti prototipe tidak lolos', () => {
  assert.throws(
    () => resolveUpstream('constructor'),
    (err) => err instanceof HttpError && err.status === 404,
  );
});

test('path traversal ditolak', () => {
  for (const bad of ['/v1/../../etc/passwd', '/v1/a\\b', 'v1/models', '//evil.test/v1']) {
    assert.throws(() => assertSafePath(bad), HttpError, `harus menolak: ${bad}`);
  }
});

test('path dengan karakter kontrol ditolak', () => {
  assert.throws(() => assertSafePath('/v1/a\u0000b'), HttpError);
});

test('path di luar prefix izin ditolak', () => {
  const upstream = resolveUpstream('openai');
  assert.throws(
    () => buildUpstreamUrl(upstream, '/admin/secret', undefined),
    (err) => err instanceof HttpError && err.code === 'path_not_allowed',
  );
});

test('URL dibangun dari origin registry, bukan dari klien', () => {
  const upstream = resolveUpstream('openai');
  const url = buildUpstreamUrl(upstream, '/v1/models', { limit: 5 });
  assert.equal(url, 'https://api.openai.com/v1/models?limit=5');
});

test('query non-skalar diabaikan', () => {
  const upstream = resolveUpstream('openai');
  const url = buildUpstreamUrl(upstream, '/v1/models', { a: 1, b: { nested: true }, c: 'x' });
  assert.equal(url, 'https://api.openai.com/v1/models?a=1&c=x');
});

test('header klien difilter daftar putih dan authorization dibuang', () => {
  const registry = makeRegistry({ forwardHeaders: ['content-type', 'authorization'] });
  const upstream = registry.dummy;

  const out = pickForwardHeaders(upstream, {
    'content-type': 'application/json',
    authorization: 'Bearer token-palsu-dari-klien',
    'x-jahat': 'nilai',
  });

  assert.deepEqual(out, { 'content-type': 'application/json' });
});
