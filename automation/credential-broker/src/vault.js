/**
 * Vault: tempat rahasia asli disimpan.
 *
 *  - provider "env"      → process.env, nama rahasia dipetakan ke env var.
 *                           Paling sederhana: env var Vercel terenkripsi saat disimpan.
 *  - provider "supabase" → RPC Postgres, membaca dari Supabase Vault (pgsodium).
 *                           Untuk rahasia yang perlu dirotasi tanpa redeploy.
 *
 * Rahasia tidak pernah di-log dan tidak pernah ikut ke pesan error.
 */

export class SecretNotFoundError extends Error {
  constructor(name) {
    super(`Rahasia "${name}" tidak ditemukan di vault`);
    this.name = 'SecretNotFoundError';
  }
}

export class VaultUnavailableError extends Error {
  constructor(message, cause) {
    super(message);
    this.name = 'VaultUnavailableError';
    this.cause = cause;
  }
}

export function createVault({ config, fetchImpl = globalThis.fetch }) {
  const cache = new Map();
  const CACHE_TTL_MS = 30_000;

  async function readEnv(name) {
    const value = process.env[name];
    if (typeof value !== 'string' || value === '') throw new SecretNotFoundError(name);
    return value;
  }

  async function readSupabase(name) {
    const url = `${config.supabaseUrl}/rest/v1/rpc/${encodeURIComponent(config.vaultRpc)}`;
    let response;
    try {
      response = await fetchImpl(url, {
        method: 'POST',
        headers: {
          apikey: config.supabaseServiceKey,
          authorization: `Bearer ${config.supabaseServiceKey}`,
          'content-type': 'application/json',
        },
        body: JSON.stringify({ secret_name: name }),
        signal: AbortSignal.timeout(config.requestTimeoutMs),
      });
    } catch (err) {
      throw new VaultUnavailableError('Tidak bisa menghubungi Supabase Vault', err);
    }

    if (response.status === 404) throw new SecretNotFoundError(name);
    if (!response.ok) {
      throw new VaultUnavailableError(`Supabase Vault membalas HTTP ${response.status}`);
    }

    const data = await response.json().catch(() => null);
    // RPC bisa mengembalikan string langsung, atau baris objek.
    const value =
      typeof data === 'string'
        ? data
        : typeof data?.secret === 'string'
          ? data.secret
          : typeof data?.decrypted_secret === 'string'
            ? data.decrypted_secret
            : Array.isArray(data) && typeof data[0]?.secret === 'string'
              ? data[0].secret
              : null;

    if (!value) throw new SecretNotFoundError(name);
    return value;
  }

  return {
    async getSecret(name) {
      const cached = cache.get(name);
      if (cached && cached.expiresAt > Date.now()) return cached.value;

      const value =
        config.vaultProvider === 'supabase' ? await readSupabase(name) : await readEnv(name);

      cache.set(name, { value, expiresAt: Date.now() + CACHE_TTL_MS });
      return value;
    },
  };
}
