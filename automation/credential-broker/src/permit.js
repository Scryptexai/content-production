/**
 * Klien PDP Permit.io.
 *
 * Kontrak yang dipakai (diverifikasi dari sumber SDK resmi `permitio@2.7.7`,
 * `build/index.js` → Enforcer.checkWithExceptions):
 *
 *   POST {pdp}/allowed
 *   Authorization: Bearer <PERMIT_API_KEY>
 *   { "user": {...}, "action": "...", "resource": {"type","key","tenant","attributes"}, "context": {} }
 *   → 200 { "allow": true }
 *
 * Catatan penting: permission check TIDAK lewat api.permit.io. Docs Permit:
 * "Permission checks don't go through this API. A check goes to the PDP."
 * PDP cloud default: https://cloudpdp.api.permit.io
 */

export class PermitUnavailableError extends Error {
  constructor(message, cause) {
    super(message);
    this.name = 'PermitUnavailableError';
    this.cause = cause;
  }
}

export function createPermitClient({ pdpUrl, apiKey, timeoutMs = 15_000, fetchImpl = globalThis.fetch }) {
  const endpoint = `${String(pdpUrl).replace(/\/+$/, '')}/allowed`;

  return {
    endpoint,

    /**
     * @param {{subject: string, action: string, resourceType: string,
     *          resourceKey: string, tenant: string,
     *          attributes?: object, context?: object}} input
     * @returns {Promise<{allow: boolean}>}
     */
    async check({ subject, action, resourceType, resourceKey, tenant, attributes, context }) {
      const body = {
        user: { key: subject },
        action,
        resource: {
          type: resourceType,
          key: resourceKey,
          tenant,
          attributes: attributes ?? {},
        },
        context: context ?? {},
      };

      let response;
      try {
        response = await fetchImpl(endpoint, {
          method: 'POST',
          headers: {
            authorization: `Bearer ${apiKey}`,
            'content-type': 'application/json',
            accept: 'application/json',
          },
          body: JSON.stringify(body),
          signal: AbortSignal.timeout(timeoutMs),
        });
      } catch (err) {
        throw new PermitUnavailableError('Tidak bisa menghubungi PDP Permit', err);
      }

      if (!response.ok) {
        throw new PermitUnavailableError(`PDP Permit membalas HTTP ${response.status}`);
      }

      let data;
      try {
        data = await response.json();
      } catch (err) {
        throw new PermitUnavailableError('Balasan PDP bukan JSON', err);
      }

      // SDK menerima dua bentuk: {allow} untuk PDP, {result:{allow}} untuk OPA.
      const allow = 'allow' in data ? data.allow : data?.result?.allow;
      return { allow: allow === true };
    },
  };
}
