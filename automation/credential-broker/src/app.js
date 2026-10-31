/**
 * Handler utama broker.
 *
 * Alur satu permintaan:
 *
 *   klien ──POST /api/broker──▶ 1. identitas (siapa?)
 *                              2. registry (upstream apa? path boleh?)
 *                              3. Permit PDP /allowed (boleh atau tidak?)
 *                              4. vault (ambil rahasia) ── hanya kalau allow
 *                              5. teruskan ke upstream, kembalikan hasilnya
 *                              6. audit (selalu)
 *
 * Mode:
 *   "proxy" (default) — rahasia TIDAK pernah sampai ke klien; broker yang menempelkan.
 *   "claim"           — mengembalikan kunci mentah; harus diaktifkan per-upstream
 *                       (allowClaim) karena kunci pihak ketiga umumnya berumur panjang.
 */

import { randomUUID } from 'node:crypto';
import { authenticate } from './identity.js';
import { createPermitClient, PermitUnavailableError } from './permit.js';
import { createVault, SecretNotFoundError, VaultUnavailableError } from './vault.js';
import { createAudit } from './audit.js';
import { resolveUpstream, buildUpstreamUrl, pickForwardHeaders } from './upstreams.js';
import { HttpError, sendJson, readJsonBody, isPlainObject } from './http.js';

const BODYLESS_METHODS = new Set(['GET', 'HEAD', 'DELETE', 'OPTIONS']);

export function createApp({
  config,
  registry,
  fetchImpl = globalThis.fetch,
  logger = console,
}) {
  const permit = createPermitClient({
    pdpUrl: config.permitPdpUrl,
    apiKey: config.permitApiKey,
    timeoutMs: config.requestTimeoutMs,
    fetchImpl,
  });
  const vault = createVault({ config, fetchImpl });
  const audit = createAudit({ config, fetchImpl, logger });

  return async function handler(req, res) {
    const requestId = randomUUID();
    const startedAt = Date.now();

    let subject = null;
    let upstreamName = null;
    let mode = null;
    let outcome = 'error';
    let detail = null;
    let finished = false;

    const finish = async (status, payload) => {
      if (finished) return;
      finished = true;
      await audit.record({
        request_id: requestId,
        at: new Date().toISOString(),
        subject,
        upstream: upstreamName,
        mode,
        outcome,
        status,
        detail,
        duration_ms: Date.now() - startedAt,
      });
      sendJson(res, status, payload);
    };

    if (req.method !== 'POST') {
      res.setHeader('allow', 'POST');
      outcome = 'rejected';
      detail = 'method';
      await finish(405, { error: 'method_not_allowed', request_id: requestId });
      return;
    }

    try {
      // 1. Identitas
      const identity = await authenticate(req, config);
      subject = identity.subject;

      const body = await readJsonBody(req, config.maxBodyBytes);

      // 2. Upstream + path
      upstreamName = typeof body.upstream === 'string' ? body.upstream : null;
      const upstream = resolveUpstream(upstreamName, registry);

      mode = body.mode === undefined ? 'proxy' : body.mode;
      if (mode !== 'proxy' && mode !== 'claim' && mode !== 'probe') {
        throw new HttpError(
          400,
          'invalid_mode',
          "Field \"mode\" harus 'proxy', 'claim', atau 'probe'",
        );
      }

      const tenant = typeof body.tenant === 'string' && body.tenant ? body.tenant : 'default';
      const action =
        typeof body.action === 'string' && body.action ? body.action : upstream.action;
      const attributes = isPlainObject(body.attributes) ? body.attributes : {};
      const context = isPlainObject(body.context) ? body.context : {};

      // 3. Keputusan policy — satu-satunya pintu.
      const decision = await permit.check({
        subject,
        action,
        resourceType: upstream.resourceType,
        resourceKey: upstream.resourceKey,
        tenant,
        attributes,
        context,
      });

      // 3b. Mode probe — hanya melaporkan keputusan policy.
      // Tidak menyentuh vault dan tidak memanggil upstream, jadi aman dipakai
      // untuk mendiagnosis koneksi ke Permit tanpa membocorkan rahasia apa pun.
      if (mode === 'probe') {
        outcome = decision.allow ? 'allowed' : 'denied';
        detail = 'probe';
        await finish(200, {
          allow: decision.allow,
          pdp: config.permitPdpUrl,
          subject,
          action,
          resource: {
            type: upstream.resourceType,
            key: upstream.resourceKey,
            tenant,
          },
          request_id: requestId,
        });
        return;
      }

      if (!decision.allow) {
        outcome = 'denied';
        detail = 'permit';
        await finish(403, {
          error: 'forbidden',
          code: 'permit_denied',
          message: 'Policy Permit menolak permintaan ini',
          request_id: requestId,
        });
        return;
      }

      // 4a. Mode claim — kunci mentah.
      if (mode === 'claim') {
        if (!upstream.allowClaim) {
          outcome = 'denied';
          detail = 'claim_not_allowed';
          await finish(403, {
            error: 'forbidden',
            code: 'claim_not_allowed',
            message:
              `Upstream "${upstream.name}" tidak mengizinkan mode claim. ` +
              'Pakai mode proxy (default) agar kunci tidak pernah meninggalkan server.',
            request_id: requestId,
          });
          return;
        }

        const secret = await vault.getSecret(upstream.secretName);
        outcome = 'allowed';
        detail = 'claim';
        await finish(200, {
          credential: secret,
          credential_kind: 'static_api_key',
          upstream: upstream.name,
          // Untuk kunci statis ini BATAS REVEAL, bukan masa berlaku kunci.
          expires_at: new Date(Date.now() + config.claimTtlSeconds * 1000).toISOString(),
          request_id: requestId,
        });
        return;
      }

      // 4b. Mode proxy.
      const method = (typeof body.method === 'string' ? body.method : 'POST').toUpperCase();
      if (!upstream.methods.includes(method)) {
        throw new HttpError(
          405,
          'method_not_allowed',
          `Metode ${method} tidak diizinkan untuk "${upstream.name}" (${upstream.methods.join(', ')})`,
        );
      }

      const targetUrl = buildUpstreamUrl(upstream, body.path, body.query);
      const secret = await vault.getSecret(upstream.secretName);

      const headers = {
        ...upstream.auth(secret),
        ...pickForwardHeaders(upstream, body.headers),
      };
      if (headers['content-type'] === undefined && !BODYLESS_METHODS.has(method)) {
        headers['content-type'] = 'application/json';
      }

      const upstreamRes = await fetchImpl(targetUrl, {
        method,
        headers,
        body: BODYLESS_METHODS.has(method) ? undefined : JSON.stringify(body.body ?? {}),
        signal: AbortSignal.timeout(config.requestTimeoutMs),
        redirect: 'manual',
      });

      const text = await upstreamRes.text();
      let data;
      try {
        data = text === '' ? null : JSON.parse(text);
      } catch {
        data = text;
      }

      outcome = 'allowed';
      detail = 'proxy';
      res.setHeader('x-request-id', requestId);
      await finish(upstreamRes.status, data ?? {});
      return;
    } catch (err) {
      if (err instanceof HttpError) {
        outcome = err.status === 401 || err.status === 403 ? 'rejected' : 'error';
        detail = err.code;
        await finish(err.status, {
          error: err.code,
          message: err.message,
          request_id: requestId,
        });
        return;
      }

      if (err instanceof PermitUnavailableError) {
        // Fail-closed: kalau PDP tidak bisa dihubungi, JANGAN beri kredensial.
        outcome = 'error';
        detail = 'permit_unavailable';
        logger.error(JSON.stringify({ request_id: requestId, permit_error: err.message }));
        await finish(503, {
          error: 'permit_unavailable',
          message: 'PDP Permit tidak bisa dihubungi. Permintaan ditolak (fail-closed).',
          request_id: requestId,
        });
        return;
      }

      if (err instanceof SecretNotFoundError) {
        outcome = 'error';
        detail = 'secret_not_found';
        logger.error(JSON.stringify({ request_id: requestId, secret_error: err.message }));
        await finish(500, {
          error: 'secret_not_found',
          message: 'Rahasia tidak ada di vault. Periksa konfigurasi vault.',
          request_id: requestId,
        });
        return;
      }

      if (err instanceof VaultUnavailableError) {
        outcome = 'error';
        detail = 'vault_unavailable';
        logger.error(JSON.stringify({ request_id: requestId, vault_error: err.message }));
        await finish(503, {
          error: 'vault_unavailable',
          message: 'Vault tidak bisa dihubungi.',
          request_id: requestId,
        });
        return;
      }

      // Jangan bocorkan detail internal ke klien; catat di server.
      outcome = 'error';
      detail = 'internal';
      logger.error(
        JSON.stringify({
          request_id: requestId,
          internal_error: err?.name ?? 'Error',
          message: err?.message ?? '',
        }),
      );
      await finish(500, { error: 'internal_error', request_id: requestId });
    }
  };
}
