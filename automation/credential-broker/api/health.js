import { loadConfig } from '../src/config.js';
import { UPSTREAM_NAMES, claimEnabledNames } from '../src/upstreams.js';

/**
 * GET /api/health — dipakai untuk memastikan konfigurasi terbaca.
 * Tidak pernah mengembalikan nilai rahasia, hanya status ada/tidak.
 */
export default async function handler(req, res) {
  res.setHeader('cache-control', 'no-store');
  res.setHeader('content-type', 'application/json; charset=utf-8');

  try {
    const config = loadConfig(process.env);
    res.statusCode = 200;
    res.end(
      JSON.stringify({
        ok: true,
        pdp: config.permitPdpUrl,
        identity: {
          static_tokens: Object.keys(config.staticTokens).length,
          supabase_jwt: Boolean(config.supabaseJwtSecret),
        },
        vault_provider: config.vaultProvider,
        audit_provider: config.auditProvider,
        upstreams: UPSTREAM_NAMES,
        claim_enabled_for: claimEnabledNames(),
      }),
    );
  } catch (err) {
    res.statusCode = 503;
    res.end(JSON.stringify({ ok: false, error: 'config_error', message: err?.message ?? '' }));
  }
}
