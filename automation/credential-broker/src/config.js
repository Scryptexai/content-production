/**
 * Konfigurasi broker. Semua dari environment variable Vercel.
 * Gagal cepat (fail fast) saat start: pesan menyebut NAMA variabel, tidak pernah nilainya.
 */

export class ConfigError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ConfigError';
  }
}

const DEFAULTS = {
  // Dokumentasi Permit: tanpa PERMIT_PDP_URL, SDK memakai Cloud PDP.
  permitPdpUrl: 'https://cloudpdp.api.permit.io',
  vaultProvider: 'env',
  auditProvider: 'console',
  auditTable: 'credential_audit',
  requestTimeoutMs: 15_000,
  maxBodyBytes: 1_048_576,
  claimTtlSeconds: 300,
};

function str(env, key) {
  const v = env[key];
  return typeof v === 'string' ? v.trim() : '';
}

function int(env, key, fallback) {
  const raw = str(env, key);
  if (!raw) return fallback;
  const n = Number.parseInt(raw, 10);
  return Number.isFinite(n) && n > 0 ? n : fallback;
}

/** @returns {object} objek konfigurasi biasa (tanpa class) agar mudah diuji */
export function loadConfig(env = process.env) {
  const problems = [];

  const permitApiKey = str(env, 'PERMIT_API_KEY');
  if (!permitApiKey) problems.push('PERMIT_API_KEY');

  // --- identitas pemanggil: minimal satu metode ---
  let staticTokens = {};
  const rawTokens = str(env, 'BROKER_STATIC_TOKENS');
  if (rawTokens) {
    try {
      const parsed = JSON.parse(rawTokens);
      if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
        problems.push('BROKER_STATIC_TOKENS (harus objek JSON: {"token": "subject"})');
      } else {
        staticTokens = parsed;
      }
    } catch {
      problems.push('BROKER_STATIC_TOKENS (bukan JSON valid)');
    }
  }
  const supabaseJwtSecret = str(env, 'SUPABASE_JWT_SECRET') || null;
  if (Object.keys(staticTokens).length === 0 && !supabaseJwtSecret) {
    problems.push('BROKER_STATIC_TOKENS atau SUPABASE_JWT_SECRET (minimal satu harus diisi)');
  }

  // --- vault ---
  const vaultProvider = str(env, 'VAULT_PROVIDER') || DEFAULTS.vaultProvider;
  if (vaultProvider !== 'env' && vaultProvider !== 'supabase') {
    problems.push("VAULT_PROVIDER (harus 'env' atau 'supabase')");
  }

  // --- audit ---
  const auditProvider = str(env, 'AUDIT_PROVIDER') || DEFAULTS.auditProvider;
  if (!['console', 'supabase', 'none'].includes(auditProvider)) {
    problems.push("AUDIT_PROVIDER (harus 'console', 'supabase', atau 'none')");
  }

  // --- supabase (dipakai vault dan/atau audit) ---
  const supabaseUrl = str(env, 'SUPABASE_URL').replace(/\/+$/, '') || null;
  const supabaseServiceKey = str(env, 'SUPABASE_SERVICE_ROLE_KEY') || null;
  const needsSupabase = vaultProvider === 'supabase' || auditProvider === 'supabase';
  if (needsSupabase) {
    if (!supabaseUrl) problems.push('SUPABASE_URL');
    if (!supabaseServiceKey) problems.push('SUPABASE_SERVICE_ROLE_KEY');
  }

  if (problems.length > 0) {
    throw new ConfigError(`Konfigurasi belum lengkap / tidak valid: ${problems.join(', ')}`);
  }

  return {
    permitApiKey,
    permitPdpUrl: (str(env, 'PERMIT_PDP_URL') || DEFAULTS.permitPdpUrl).replace(/\/+$/, ''),
    staticTokens,
    supabaseJwtSecret,
    vaultProvider,
    vaultRpc: str(env, 'VAULT_RPC') || 'get_secret',
    auditProvider,
    auditTable: str(env, 'AUDIT_TABLE') || DEFAULTS.auditTable,
    supabaseUrl,
    supabaseServiceKey,
    requestTimeoutMs: int(env, 'REQUEST_TIMEOUT_MS', DEFAULTS.requestTimeoutMs),
    maxBodyBytes: int(env, 'MAX_BODY_BYTES', DEFAULTS.maxBodyBytes),
    claimTtlSeconds: int(env, 'CLAIM_TTL_SECONDS', DEFAULTS.claimTtlSeconds),
  };
}
