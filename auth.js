// Gemeinsame Hilfsfunktionen für Middleware und Login (Web-Crypto, läuft in Edge und Node).
export const COOKIE = 'fwg_auth';
export const MAX_AGE = 60 * 60 * 24 * 7; // 7 Tage

const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');

// Token = HMAC-SHA256 über eine feste Zeichenfolge, Schlüssel ist das Passwort.
// Wird das Passwort in Vercel geändert, werden alle bestehenden Anmeldungen ungültig.
export async function makeToken(password) {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return hex(await crypto.subtle.sign('HMAC', key, new TextEncoder().encode('fwg-oelde-auth-v1')));
}

// Zeitkonstanter Vergleich
export function safeEqual(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}
