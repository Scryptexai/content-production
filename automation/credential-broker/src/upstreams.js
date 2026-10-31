/**
 * Registry upstream — SATU-SATUNYA sumber kebenaran tentang API mana yang boleh
 * dijangkau broker. Sengaja hard-coded dan di-freeze: klien tidak bisa menentukan
 * base URL sendiri (kalau bisa, broker jadi open proxy / celah SSRF).
 *
 * Menambah upstream = menambah entri di sini + commit + deploy.
 */

import { HttpError } from './http.js';

/**
 * @typedef {object} Upstream
 * @property {string}   name
 * @property {string}   resourceType  tipe resource di Permit
 * @property {string}   resourceKey   key resource di Permit
 * @property {string}   action        aksi default yang diperiksa ke Permit
 * @property {string}   baseUrl       origin upstream (hard-coded)
 * @property {string}   secretName    nama rahasia di vault
 * @property {(secret: string) => Record<string,string>} auth
 * @property {string[]} allowedPathPrefixes  prefix path yang diizinkan
 * @property {string[]} methods       metode HTTP yang diizinkan
 * @property {string[]} forwardHeaders  header klien yang boleh diteruskan
 * @property {boolean}  allowClaim    izinkan mode "claim" (mengembalikan kunci mentah)
 */

const REGISTRY = {
  openai: {
    name: 'openai',
    resourceType: 'ai_provider',
    resourceKey: 'openai',
    action: 'invoke',
    baseUrl: 'https://api.openai.com',
    secretName: 'OPENAI_API_KEY',
    auth: (secret) => ({ authorization: `Bearer ${secret}` }),
    allowedPathPrefixes: ['/v1/'],
    methods: ['GET', 'POST', 'DELETE'],
    forwardHeaders: ['content-type', 'accept', 'openai-organization', 'openai-beta'],
    allowClaim: false,
  },

  stripe: {
    name: 'stripe',
    resourceType: 'payment_provider',
    resourceKey: 'stripe',
    action: 'invoke',
    baseUrl: 'https://api.stripe.com',
    secretName: 'STRIPE_SECRET_KEY',
    auth: (secret) => ({ authorization: `Bearer ${secret}` }),
    allowedPathPrefixes: ['/v1/'],
    methods: ['GET', 'POST', 'DELETE'],
    forwardHeaders: ['content-type', 'accept', 'idempotency-key'],
    allowClaim: false,
  },

  slack: {
    name: 'slack',
    resourceType: 'messaging',
    resourceKey: 'slack',
    action: 'post_message',
    baseUrl: 'https://slack.com',
    secretName: 'SLACK_BOT_TOKEN',
    auth: (secret) => ({ authorization: `Bearer ${secret}` }),
    allowedPathPrefixes: ['/api/'],
    methods: ['POST'],
    forwardHeaders: ['content-type', 'accept'],
    allowClaim: false,
  },
};

for (const upstream of Object.values(REGISTRY)) {
  Object.freeze(upstream.allowedPathPrefixes);
  Object.freeze(upstream.methods);
  Object.freeze(upstream.forwardHeaders);
  Object.freeze(upstream);
}
Object.freeze(REGISTRY);

export const UPSTREAM_NAMES = Object.freeze(Object.keys(REGISTRY));

/** Nama upstream yang mengizinkan mode claim (pengembalian kunci mentah). */
export function claimEnabledNames() {
  return UPSTREAM_NAMES.filter((name) => REGISTRY[name].allowClaim === true);
}

/**
 * @param {string|null} name
 * @param {object} [registry]
 * @returns {Upstream}
 */
export function resolveUpstream(name, registry = REGISTRY) {
  if (typeof name !== 'string' || !name) {
    throw new HttpError(400, 'missing_upstream', 'Field "upstream" wajib diisi');
  }
  if (!Object.prototype.hasOwnProperty.call(registry, name)) {
    throw new HttpError(
      404,
      'unknown_upstream',
      `Upstream "${name}" tidak terdaftar. Tersedia: ${Object.keys(registry).join(', ')}`,
    );
  }
  return registry[name];
}

/** Tolak path yang bisa dipakai keluar dari origin upstream. */
export function assertSafePath(rawPath) {
  if (typeof rawPath !== 'string' || rawPath === '') {
    throw new HttpError(400, 'invalid_path', 'Field "path" wajib berupa string, mis. "/v1/models"');
  }
  if (!rawPath.startsWith('/')) {
    throw new HttpError(400, 'invalid_path', 'Path harus diawali "/"');
  }
  if (rawPath.startsWith('//')) {
    throw new HttpError(400, 'invalid_path', 'Path tidak boleh diawali "//"');
  }
  if (rawPath.includes('..') || rawPath.includes('\\')) {
    throw new HttpError(400, 'invalid_path', 'Path tidak boleh mengandung ".." atau "\\"');
  }
  // eslint-disable-next-line no-control-regex
  if (/[\u0000-\u001f\u007f]/.test(rawPath)) {
    throw new HttpError(400, 'invalid_path', 'Path mengandung karakter kontrol');
  }
}

/**
 * Bangun URL tujuan. Origin selalu dari registry, tidak pernah dari klien.
 * @returns {string}
 */
export function buildUpstreamUrl(upstream, rawPath, query) {
  assertSafePath(rawPath);

  const allowed = upstream.allowedPathPrefixes.some((prefix) => rawPath.startsWith(prefix));
  if (!allowed) {
    throw new HttpError(
      403,
      'path_not_allowed',
      `Path "${rawPath}" di luar daftar izin (${upstream.allowedPathPrefixes.join(', ')})`,
    );
  }

  const url = new URL(upstream.baseUrl);
  url.pathname = rawPath;

  if (query !== undefined && query !== null) {
    if (typeof query !== 'object' || Array.isArray(query)) {
      throw new HttpError(400, 'invalid_query', 'Field "query" harus objek');
    }
    for (const [key, value] of Object.entries(query)) {
      if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
        url.searchParams.set(key, String(value));
      }
    }
  }

  return url.toString();
}

/** Hanya header yang masuk daftar putih yang diteruskan; `authorization` klien dibuang. */
export function pickForwardHeaders(upstream, clientHeaders) {
  const out = {};
  if (!clientHeaders || typeof clientHeaders !== 'object' || Array.isArray(clientHeaders)) {
    return out;
  }
  for (const key of upstream.forwardHeaders) {
    if (key.toLowerCase() === 'authorization') continue;
    const raw = clientHeaders[key] ?? clientHeaders[key.toLowerCase()];
    if (typeof raw === 'string' && raw.length <= 4096) out[key] = raw;
  }
  return out;
}
