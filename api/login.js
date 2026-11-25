import { COOKIE, MAX_AGE, makeToken, safeEqual } from '../auth.js';

export async function POST(request) {
  const expected = process.env.SITE_PASSWORD;
  if (!expected) return Response.json({ error: 'not_configured' }, { status: 503 });

  let given = '';
  try {
    given = String((await request.json()).password ?? '');
  } catch {
    return Response.json({ error: 'bad_request' }, { status: 400 });
  }

  // Vergleich über Hashes, damit die Länge nichts verrät.
  // Ein leeres Passwort ist nie gültig (Web-Crypto erlaubt keinen leeren HMAC-Schlüssel).
  const ok = given !== '' && safeEqual(await makeToken(given), await makeToken(expected));
  if (!ok) {
    await new Promise((r) => setTimeout(r, 800)); // bremst Durchprobieren
    return Response.json({ error: 'wrong_password' }, { status: 401 });
  }

  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
      'Set-Cookie': `${COOKIE}=${await makeToken(expected)}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
    },
  });
}
