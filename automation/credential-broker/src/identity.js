/**
 * Identitas pemanggil. Dua metode:
 *  1. BROKER_STATIC_TOKENS — {"tok_abc": "service:reporting"} untuk service internal.
 *  2. JWT HS256 bertanda tangan Supabase (SUPABASE_JWT_SECRET) — untuk user login.
 *
 * Tanpa identitas yang sah, broker tidak tahu "siapa" yang harus diperiksa Permit,
 * jadi permintaan ditolak sebelum apa pun terjadi.
 */

import { createHmac, timingSafeEqual } from 'node:crypto';
import { HttpError } from './http.js';

function bearerToken(req) {
  const raw = req.headers?.authorization ?? req.headers?.Authorization;
  if (typeof raw !== 'string') return null;
  const match = /^Bearer\s+(.+)$/i.exec(raw.trim());
  return match ? match[1].trim() : null;
}

function safeEqual(a, b) {
  const bufA = Buffer.from(a, 'utf8');
  const bufB = Buffer.from(b, 'utf8');
  if (bufA.length !== bufB.length) return false;
  return timingSafeEqual(bufA, bufB);
}

function decodeBase64Url(segment) {
  return Buffer.from(segment.replace(/-/g, '+').replace(/_/g, '/'), 'base64');
}

/**
 * Verifikasi JWT HS256 tanpa dependensi.
 * @returns {object} payload
 */
export function verifyJwtHS256(token, secret) {
  const parts = token.split('.');
  if (parts.length !== 3) throw new HttpError(401, 'invalid_token', 'Format token bukan JWT');
  const [headerB64, payloadB64, signatureB64] = parts;

  const expected = createHmac('sha256', secret)
    .update(`${headerB64}.${payloadB64}`)
    .digest();
  const given = decodeBase64Url(signatureB64);

  if (given.length !== expected.length || !timingSafeEqual(given, expected)) {
    throw new HttpError(401, 'invalid_token', 'Tanda tangan token tidak sah');
  }

  let payload;
  try {
    payload = JSON.parse(decodeBase64Url(payloadB64).toString('utf8'));
  } catch {
    throw new HttpError(401, 'invalid_token', 'Payload token bukan JSON');
  }

  const now = Math.floor(Date.now() / 1000);
  if (typeof payload.exp === 'number' && now >= payload.exp) {
    throw new HttpError(401, 'token_expired', 'Token sudah kedaluwarsa');
  }
  if (typeof payload.nbf === 'number' && now < payload.nbf) {
    throw new HttpError(401, 'invalid_token', 'Token belum berlaku');
  }

  return payload;
}

/**
 * @returns {Promise<{subject: string, method: string}>}
 * @throws {HttpError} 401
 */
export async function authenticate(req, config) {
  const token = bearerToken(req);
  if (!token) {
    throw new HttpError(401, 'missing_token', 'Header Authorization: Bearer <token> wajib ada');
  }

  // 1. Token statis untuk service internal.
  for (const [knownToken, subject] of Object.entries(config.staticTokens ?? {})) {
    if (typeof subject !== 'string' || !subject) continue;
    if (safeEqual(token, knownToken)) {
      return { subject, method: 'static_token' };
    }
  }

  // 2. JWT Supabase.
  if (config.supabaseJwtSecret) {
    const payload = verifyJwtHS256(token, config.supabaseJwtSecret);
    const subject = typeof payload.sub === 'string' ? payload.sub : null;
    if (!subject) {
      throw new HttpError(401, 'invalid_token', 'Token tidak punya klaim "sub"');
    }
    return { subject, method: 'supabase_jwt' };
  }

  throw new HttpError(401, 'invalid_token', 'Token tidak dikenal');
}
