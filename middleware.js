// Passwortschutz für die gesamte Website (Vercel Routing Middleware).
// Das Passwort wird in Vercel als Umgebungsvariable SITE_PASSWORD hinterlegt
// (Project → Settings → Environment Variables). Der Benutzername ist beliebig.
// Ist die Variable nicht gesetzt, bleibt die Seite gesperrt (fail closed).

const REALM = 'FWG Oelde (Entwurf)';

export const config = { matcher: '/:path*' };

async function digest(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return new Uint8Array(buf);
}

// Vergleich in konstanter Zeit über feste Hash-Längen
async function safeEqual(a, b) {
  const [x, y] = await Promise.all([digest(a), digest(b)]);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

function denied(status, body) {
  return new Response(body, {
    status,
    headers: {
      'WWW-Authenticate': `Basic realm="${REALM}", charset="UTF-8"`,
      'Cache-Control': 'no-store',
      'Content-Type': 'text/plain; charset=utf-8',
      'X-Robots-Tag': 'noindex, nofollow',
    },
  });
}

export default async function middleware(request) {
  const expected = process.env.SITE_PASSWORD;
  if (!expected) {
    return new Response('Passwortschutz ist nicht konfiguriert (SITE_PASSWORD fehlt).', {
      status: 503,
      headers: { 'Cache-Control': 'no-store', 'Content-Type': 'text/plain; charset=utf-8' },
    });
  }

  const header = request.headers.get('authorization') || '';
  const [scheme, encoded] = header.split(' ');
  if (scheme && scheme.toLowerCase() === 'basic' && encoded) {
    try {
      const bytes = Uint8Array.from(atob(encoded), (c) => c.charCodeAt(0));
      const decoded = new TextDecoder().decode(bytes);
      const password = decoded.slice(decoded.indexOf(':') + 1);
      if (decoded.includes(':') && (await safeEqual(password, expected))) {
        // Anfrage durchlassen (entspricht next() aus @vercel/edge)
        return new Response(null, { headers: { 'x-middleware-next': '1' } });
      }
    } catch {
      /* ungültiger Header → unten abgelehnt */
    }
  }
  return denied(401, 'Bitte Passwort eingeben.');
}
