/**
 * Audit log. Setiap permintaan kredensial — diizinkan maupun ditolak — dicatat.
 *
 * Kegagalan audit TIDAK boleh menggagalkan permintaan yang sudah lolos policy,
 * tetapi harus berisik di log supaya ketahuan.
 *
 * Tidak ada rahasia yang masuk ke sini. Hanya identitas, upstream, keputusan.
 */

export function createAudit({ config, fetchImpl = globalThis.fetch, logger = console }) {
  async function toSupabase(event) {
    const response = await fetchImpl(`${config.supabaseUrl}/rest/v1/${config.auditTable}`, {
      method: 'POST',
      headers: {
        apikey: config.supabaseServiceKey,
        authorization: `Bearer ${config.supabaseServiceKey}`,
        'content-type': 'application/json',
        prefer: 'return=minimal',
      },
      body: JSON.stringify(event),
      signal: AbortSignal.timeout(config.requestTimeoutMs),
    });
    if (!response.ok) {
      throw new Error(`audit insert HTTP ${response.status}`);
    }
  }

  return {
    /** @param {object} event */
    async record(event) {
      if (config.auditProvider === 'none') return;
      try {
        if (config.auditProvider === 'supabase') {
          await toSupabase(event);
        } else {
          logger.log(JSON.stringify({ audit: event }));
        }
      } catch (err) {
        logger.error(
          JSON.stringify({
            audit_failure: true,
            request_id: event?.request_id,
            error: err?.message ?? 'unknown',
          }),
        );
      }
    },
  };
}
