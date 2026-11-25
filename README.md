# FWG Oelde – Website-Entwurf

Statische, responsive Website (HTML/CSS/JS, keine Build-Abhängigkeiten im Betrieb).

- Seiten: Start, Über uns, Unser Team, Programm, Aktuelles, Termine, Mitmachen, Kontakt, Impressum, Datenschutz
- Neu generieren: `python3 tools_avatars.py && python3 build.py` (Inhalte in `build.py`, Personen in `people.json`)
- Vorschau: `python3 -m http.server` und `index.html` öffnen

**Hinweis:** Porträts sind illustrierte Platzhalter. Namen/Funktionen (außer Vorsitzender B. Poppenberg), Termine, News, Adresse und Kontaktdaten sind Beispieldaten. Inhalte stammen sinngemäß aus öffentlichen Suchergebnissen zur FWG-Website (diese war aus der Entwicklungsumgebung nicht direkt abrufbar) und sind vor Veröffentlichung abzugleichen.

## Kontaktformular

Die Formulare auf `kontakt.html` und `mitmachen.html` senden per `fetch` an `api/contact.php`, das die Nachricht per `mail()` an die Adresse in `api/config.php` verschickt (Voraussetzung: Hosting mit PHP ≥ 8.1 und funktionierendem Mailversand).

- Vor dem Livegang `api/config.php` prüfen: Empfänger (`to`) und Absender (`from`, muss zur Domain des Hostings passen, damit Mails nicht als Spam landen).
- Schutz: Honeypot-Feld, Mindestzeit, Rate-Limit pro IP (nur gehasht im Temp-Verzeichnis), Herkunftsprüfung, Schutz vor Header-Injection, Datenschutz-Checkbox. Es werden keine Nachrichten gespeichert.
- Lokal testen: `php -S 127.0.0.1:8001` im Projektordner (für echten Mailversand muss `sendmail_path` konfiguriert sein).
- Datenschutzerklärung und Impressum sind Entwürfe und müssen rechtlich geprüft werden.

## Passwortschutz (Vercel)

Der Schutz arbeitet mit einer Login-Seite und einem Cookie, wie bei Finanzkonzepte Desel:

- `login.html` ist die Anmeldeseite, sie schickt das Passwort an `api/login.js`.
- `api/login.js` prüft das Passwort und setzt bei Erfolg das Cookie `fwg_auth` (7 Tage, `HttpOnly`, `Secure`, `SameSite=Lax`).
- `middleware.js` leitet alle Seiten ohne gültiges Cookie auf `/login.html` um. Öffentlich bleiben Login, Impressum, Datenschutz und `assets/`.
- `auth.js` enthält die gemeinsame Token-Logik. Das Passwort steht nie im Code.

**Einrichten:**
1. In Vercel: **Project → Settings → Environment Variables** → `SITE_PASSWORD` mit dem gewünschten Passwort anlegen (Production und Preview).
2. **Neu deployen** (Variablen gelten erst für neue Deployments).
3. Beim Aufruf erscheint die Login-Seite. Wird das Passwort geändert, müssen sich alle erneut anmelden.

Ist `SITE_PASSWORD` nicht gesetzt, bleibt die Seite gesperrt. Lokal testen: `npm install`, `npm test` (Tests für Login und Middleware), `npx vercel dev`.

`vercel.json` setzt die Region Frankfurt und den Header `X-Robots-Tag: noindex`. `.vercelignore` schließt Build-Werkzeuge, Rohdaten, Tests und das PHP-Formular vom Deployment aus.

**Passwortschutz abschalten (Livegang):** `middleware.js`, `auth.js`, `api/login.js` und `login.html` löschen, den Header `X-Robots-Tag` in `vercel.json` entfernen und in `build.py` den Absatz „Passwortgeschützter Bereich“ der Datenschutzerklärung streichen (danach `python3 build.py`). Nur die Variable zu löschen reicht nicht, ohne `SITE_PASSWORD` bleibt die Seite gesperrt, solange `middleware.js` existiert.

## Kandidatenübersicht 2025 (versteckte Seite)

`kandidaten-2025.html` erscheint **nicht** in Navigation oder Footer und ist per `noindex` von Suchmaschinen ausgenommen. Erreichbar ist sie nur über die Karte „Wer hinter dem Programm steht“ am Ende des Abschnitts „Programm 2025“ auf `programm.html`.

Die Inhalte kommen aus `candidates.json` (Stand 14.11.2026, Kernaussagen gekürzt, Themen von uns zugeordnet): Wahlbezirk, Name, Kernaussage, Themen, `gewaehlt` (true/false) und optional `photo` (Pfad zu einem Bild; aktuell noch leer). Einträge ohne Kernaussage werden mit einem Hinweis angezeigt. Nach dem Ändern `python3 build.py` ausführen.
