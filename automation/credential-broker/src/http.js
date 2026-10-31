/**
 * Helper HTTP kecil: error bertipe, pengiriman JSON, pembacaan body.
 * Tanpa dependensi luar — Vercel Node runtime sudah menyediakan semuanya.
 */

export class HttpError extends Error {
  /**
   * @param {number} status
   * @param {string} code
   * @param {string} message
   */
  constructor(status, code, message) {
    super(message);
    this.name = 'HttpError';
    this.status = status;
    this.code = code;
  }
}

export function sendJson(res, status, body) {
  // 204/304 tidak boleh punya body.
  if (status === 204 || status === 304) {
    res.statusCode = status;
    res.end();
    return;
  }
  const payload = JSON.stringify(body ?? null);
  res.statusCode = status;
  res.setHeader('content-type', 'application/json; charset=utf-8');
  res.setHeader('cache-control', 'no-store');
  res.setHeader('x-content-type-options', 'nosniff');
  res.end(payload);
}

/**
 * Baca body sebagai JSON.
 * Vercel Node runtime kadang sudah mem-parse body ke req.body; kalau belum,
 * kita baca stream-nya sendiri dengan batas ukuran.
 */
export async function readJsonBody(req, limitBytes = 1_000_000) {
  let raw;

  if (req.body !== undefined && req.body !== null) {
    if (Buffer.isBuffer(req.body)) {
      raw = req.body.toString('utf8');
    } else if (typeof req.body === 'string') {
      raw = req.body;
    } else {
      return req.body; // sudah objek hasil parse
    }
  } else {
    const chunks = [];
    let size = 0;
    for await (const chunk of req) {
      size += chunk.length;
      if (size > limitBytes) {
        throw new HttpError(413, 'body_too_large', `Body melebihi batas ${limitBytes} byte`);
      }
      chunks.push(chunk);
    }
    raw = Buffer.concat(chunks).toString('utf8');
  }

  if (raw.trim() === '') return {};

  try {
    const parsed = JSON.parse(raw);
    if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
      throw new Error('bukan objek');
    }
    return parsed;
  } catch {
    throw new HttpError(400, 'invalid_json', 'Body harus berupa objek JSON');
  }
}

export function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}
