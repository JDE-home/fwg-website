import test from 'node:test';
import assert from 'node:assert/strict';
import middleware, { config } from '../middleware.js';
import { POST } from '../api/login.js';
import { COOKIE, makeToken } from '../auth.js';

const PW = 'ein-langes-test-passwort';
const login = (body) => POST(new Request('https://example.test/api/login', { method: 'POST', body: typeof body === 'string' ? body : JSON.stringify(body) }));
const visit = (path, cookie) => middleware(new Request('https://example.test' + path, { headers: cookie ? { cookie } : {} }));
const matchesProtected = (path) => new RegExp('^' + config.matcher[0] + '$').test(path);

test('Login: richtiges Passwort setzt ein sicheres Cookie', async () => {
  process.env.SITE_PASSWORD = PW;
  const r = await login({ password: PW });
  assert.equal(r.status, 200);
  const c = r.headers.get('set-cookie');
  assert.ok(c.startsWith(`${COOKIE}=${await makeToken(PW)}`));
  for (const flag of ['HttpOnly', 'Secure', 'SameSite=Lax', 'Path=/', 'Max-Age=604800']) assert.ok(c.includes(flag), flag);
  assert.equal(r.headers.get('cache-control'), 'no-store');
});

test('Login: falsches Passwort wird abgelehnt, ohne Cookie', async () => {
  process.env.SITE_PASSWORD = PW;
  const r = await login({ password: 'falsch' });
  assert.equal(r.status, 401);
  assert.equal(r.headers.get('set-cookie'), null);
});

test('Login: kaputte Anfrage und fehlende Konfiguration', async () => {
  process.env.SITE_PASSWORD = PW;
  assert.equal((await login('kein json')).status, 400);
  assert.equal((await login({})).status, 401);
  delete process.env.SITE_PASSWORD;
  assert.equal((await login({ password: PW })).status, 503);
});

test('Middleware: ohne Cookie Weiterleitung zur Login-Seite, mit Rücksprungadresse', async () => {
  process.env.SITE_PASSWORD = PW;
  const r = await visit('/programm.html');
  assert.equal(r.status, 302);
  const loc = new URL(r.headers.get('location'));
  assert.equal(loc.pathname, '/login.html');
  assert.equal(loc.searchParams.get('next'), '/programm.html');
  const home = new URL((await visit('/')).headers.get('location'));
  assert.equal(home.pathname, '/login.html');
  assert.equal(home.searchParams.get('next'), null);
});

test('Middleware: gültiges Cookie lässt durch, falsches nicht', async () => {
  process.env.SITE_PASSWORD = PW;
  const good = await visit('/programm.html', `foo=1; ${COOKIE}=${await makeToken(PW)}`);
  assert.equal(good.status, 200);
  assert.equal(good.headers.get('x-middleware-next'), '1');
  assert.equal((await visit('/programm.html', `${COOKIE}=abc`)).status, 302);
  assert.equal((await visit('/programm.html', `${COOKIE}=${await makeToken('anderes')}`)).status, 302);
});

test('Middleware: ohne SITE_PASSWORD bleibt alles gesperrt, auch mit Cookie', async () => {
  delete process.env.SITE_PASSWORD;
  assert.equal((await visit('/', `${COOKIE}=${await makeToken(PW)}`)).status, 302);
});

test('Matcher: Seiten sind geschützt, Login, Rechtstexte und Assets bleiben offen', () => {
  for (const p of ['/', '/programm.html', '/kandidaten-2025.html', '/api/contact.php']) assert.ok(matchesProtected(p), p);
  for (const p of ['/login.html', '/api/login', '/impressum.html', '/datenschutz.html', '/assets/css/style.css', '/assets/img/logo.jpg']) assert.ok(!matchesProtected(p), p);
});
