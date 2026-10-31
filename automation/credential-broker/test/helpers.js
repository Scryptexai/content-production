/** Helper bersama untuk test. */

import { createHmac } from 'node:crypto';

/** Bangun objek config mirip hasil loadConfig(), tanpa menyentuh env. */
export function makeConfig(overrides = {}) {
  return {
    permitApiKey: 'permit_test_key',
    permitPdpUrl: 'https://pdp.test',
    staticTokens: { 'tok-good': 'service:reporting' },
    supabaseJwtSecret: null,
    vaultProvider: 'env',
    vaultRpc: 'get_secret',
    auditProvider: 'none',
    auditTable: 'credential_audit',
    supabaseUrl: null,
    supabaseServiceKey: null,
    requestTimeoutMs: 5000,
    maxBodyBytes: 1_000_000,
    claimTtlSeconds: 300,
    ...overrides,
  };
}

/** Registry uji — base URL `dummy.test`, bukan internet. */
export function makeRegistry(overrides = {}) {
  const base = {
    name: 'dummy',
    resourceType: 'third_party_api',
    resourceKey: 'dummy',
    action: 'invoke',
    baseUrl: 'https://dummy.test',
    secretName: 'DUMMY_API_KEY',
    auth: (secret) => ({ authorization: `Bearer ${secret}` }),
    allowedPathPrefixes: ['/v1/'],
    methods: ['GET', 'POST'],
    forwardHeaders: ['content-type', 'accept'],
    allowClaim: false,
  };
  return { dummy: { ...base, ...overrides } };
}

/** Req palsu yang cukup untuk handler. */
export function makeReq({ method = 'POST', headers = {}, body = {} } = {}) {
  return { method, headers, body };
}

/** Res palsu yang merekam apa yang dikirim. */
export function makeRes() {
  const res = {
    statusCode: 200,
    headers: {},
    body: undefined,
    ended: false,
    setHeader(key, value) {
      this.headers[key.toLowerCase()] = value;
    },
    end(payload) {
      this.body = payload;
      this.ended = true;
    },
    get json() {
      return this.body === undefined || this.body === '' ? null : JSON.parse(this.body);
    },
  };
  return res;
}

/**
 * fetch palsu: rute dicocokkan berdasarkan prefix URL atau RegExp.
 * Merekam setiap panggilan di `fn.calls`.
 */
export function makeFetch(routes) {
  const calls = [];
  const fn = async (url, init = {}) => {
    const href = typeof url === 'string' ? url : url.toString();
    calls.push({ url: href, init, headers: init.headers ?? {} });

    for (const [matcher, responder] of routes) {
      const match = typeof matcher === 'string' ? href.startsWith(matcher) : matcher.test(href);
      if (match) {
        const result = typeof responder === 'function' ? responder({ url: href, init }) : responder;

        // Izinkan test meniru kegagalan jaringan.
        if (result && result.throws) throw new Error(result.throws);

        const payload = typeof result.body === 'string' ? result.body : JSON.stringify(result.body ?? {});
        return new Response(payload, {
          status: result.status ?? 200,
          headers: { 'content-type': 'application/json' },
        });
      }
    }
    throw new Error(`fetch tak terduga: ${href}`);
  };
  fn.calls = calls;
  fn.callsTo = (prefix) => calls.filter((c) => c.url.startsWith(prefix));
  return fn;
}

/** Buat JWT HS256 untuk test. */
export function signJwt(payload, secret, header = { alg: 'HS256', typ: 'JWT' }) {
  const enc = (obj) => Buffer.from(JSON.stringify(obj)).toString('base64url');
  const head = enc(header);
  const body = enc(payload);
  const sig = createHmac('sha256', secret).update(`${head}.${body}`).digest('base64url');
  return `${head}.${body}.${sig}`;
}
