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
