"""Generiert die statische FWG-Oelde-Website: python3 tools_avatars.py && python3 build.py"""
import json, html
P = json.load(open("people.json", encoding="utf-8"))
NAV = [("index.html","Start"),("ueber-uns.html","Über uns"),("ratsmitglieder.html","Unser Team"),("programm.html","Programm"),("aktuelles.html","Aktuelles"),("termine.html","Termine")]

def layout(fn, title, body, desc):
    nav = "".join(f'<li><a href="{h}"{" aria-current=page" if h==fn else ""}>{t}</a></li>' for h,t in NAV)
    nav += f'<li><a class="cta" href="mitmachen.html"{" aria-current=page" if fn=="mitmachen.html" else ""}>Mitmachen</a></li>'
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} – FWG Oelde</title><meta name="description" content="{desc}">
<meta name="theme-color" content="#0f5c3a">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css"></head><body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="site-header"><div class="container nav">
<a class="brand" href="index.html" aria-label="FWG Oelde Startseite"><span class="logo">FWG</span><span>FWG Oelde<small>Freie Wählergemeinschaft</small></span></a>
<button class="burger" aria-label="Menü" aria-expanded="false"><span></span></button>
<ul class="menu">{nav}</ul></div></header>
<main id="main">{body}</main>
<footer><div class="container"><div class="cols">
<div><a class="brand" href="index.html" style="color:#fff"><span class="logo">FWG</span><span>FWG Oelde</span></a><p style="margin-top:1rem">Bürgernah, unabhängig, parteifrei – seit 1994 im Rat der Stadt Oelde.</p></div>
<div><h4>Entdecken</h4><a href="ueber-uns.html">Über uns</a><a href="ratsmitglieder.html">Unser Team</a><a href="programm.html">Programm</a></div>
<div><h4>Aktiv werden</h4><a href="aktuelles.html">Aktuelles</a><a href="termine.html">Termine</a><a href="mitmachen.html">Mitmachen</a><a href="kontakt.html">Kontakt</a></div>
<div><h4>Rechtliches</h4><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div>
</div><div class="bottom"><span>© 2026 FWG Oelde e. V. · Entwurf mit Platzhalter-Inhalten</span><span>Made with ♥ in Oelde</span></div></div></footer>
<script src="assets/js/main.js"></script></body></html>'''

def hero(eyebrow, h, p): return f'<div class="page-hero"><div class="container"><span class="eyebrow">{eyebrow}</span><h1>{h}</h1><p>{p}</p></div></div>'
def person(p): return f'<article class="person reveal"><div class="ph"><img src="assets/img/team/{p["id"]}.svg" alt="Platzhalter-Porträt von {p["name"]}"><span class="tag">{p["tag"]}</span></div><div class="info"><h3>{p["name"]}</h3><div class="role">{p["role"]}</div><p>{p["bio"]}</p></div></article>'
def band(t, s, href, label): return f'<section style="padding-top:0"><div class="container"><div class="band reveal"><div><h2>{t}</h2><p style="margin:.5rem 0 0">{s}</p></div><a class="btn btn-dark" href="{href}">{label} →</a></div></div></section>'
def card(i,t,d,l=None): return f'<div class="card reveal"><div class="icon">{i}</div><h3>{t}</h3><p>{d}</p>{f"<a class=more href={l}>Mehr erfahren →</a>" if l else ""}</div>'

pages = {}
# --- Start
pages["index.html"] = ("Start","Die Freie Wählergemeinschaft für Oelde: bürgernah, unabhängig und mit solider Finanzpolitik.", f'''
<div class="hero"><span class="blob b1"></span><span class="blob b2"></span><div class="container hero-grid">
<div><span class="eyebrow">Freie Wählergemeinschaft · Seit 1994</span>
<h1>Oelde. <em>Bürgernah</em> &amp; unabhängig.</h1>
<p>Wir sind Bürgerinnen und Bürger – keine Parteisoldaten. Für solide Finanzen, gute Schulen und eine lebenswerte Stadt, in der Politik wieder zuhört.</p>
<div class="actions"><a class="btn btn-primary" href="programm.html">Unser Programm →</a><a class="btn btn-ghost" href="ratsmitglieder.html">Das Team kennenlernen</a></div></div>
<div class="hero-stack"><img src="assets/img/team/keller.svg" alt="Platzhalter-Porträt Sabine Keller"><img src="assets/img/team/brinkmann.svg" alt="Platzhalter-Porträt Thomas Brinkmann"><img src="assets/img/team/wessels.svg" alt="Platzhalter-Porträt Anja Wessels"><div class="badge"><b>30+</b>Jahre im Rat</div></div>
</div></div>
<div class="container"><div class="stats">
<div class="stat"><b data-count="1994">0</b><span>aktiv seit</span></div><div class="stat"><b data-count="10">0</b><span>Engagierte im Team</span></div><div class="stat"><b data-count="6">0</b><span>Kernthemen</span></div><div class="stat"><b data-count="100" data-suffix="%">0</b><span>parteifrei &amp; lokal</span></div></div></div>
<section><div class="container"><div class="section-head reveal"><span class="eyebrow">Wofür wir stehen</span><h2>Politik, die bei den Menschen in Oelde ankommt.</h2><p class="lead">Unsere Schwerpunkte für Oelde, Stromberg, Lette und Sünninghausen.</p></div>
<div class="grid g3">
{card("💶","Solide Finanzen","Schuldenabbau fortsetzen, Gebühren und Steuern so niedrig wie möglich halten und kluge Beteiligungen wie die Stadtwerke Ostmünsterland sichern.","programm.html#finanzen")}
{card("🎒","Gute Schulen","Sanierung, Ausbau und Schulsozialarbeit – damit unsere Kinder die besten Voraussetzungen haben.","programm.html#schulen")}
{card("🌳","Klima &amp; Stadtgrün","Anpassung an Starkregen, Hitze und Trockenheit – zum Schutz von Gesundheit, Umwelt und Infrastruktur.","programm.html#klima")}
{card("🏙️","Lebendige Innenstadt","Handel, Gastronomie und Aufenthaltsqualität stärken – ein Zentrum, das man gerne besucht.","programm.html#innenstadt")}
{card("🤝","Ehrenamt &amp; Vereine","Vereine sind das Rückgrat unserer Stadt. Wir fördern, was Menschen verbindet.","programm.html#ehrenamt")}
{card("🚲","Mobilität &amp; Bauen","Sichere Wege für alle und bezahlbarer, zukunftsfähiger Wohnraum.","programm.html#mobilitaet")}
</div></div></section>
<section class="alt"><div class="container"><div class="split"><div class="reveal"><span class="eyebrow">Unser Team</span><h2>Gesichter, die Sie kennen.</h2><p class="lead">Unsere Ratsmitglieder und sachkundigen Bürger sind Nachbarn, Unternehmerinnen, Eltern, Vereinsmenschen – mitten aus Oelde.</p><a class="btn btn-dark" href="ratsmitglieder.html">Alle ansehen →</a></div>
<div class="grid" style="grid-template-columns:repeat(2,1fr)">{"".join(person(p) for p in P[:2])}</div></div></div></section>
<section><div class="container"><div class="section-head reveal"><span class="eyebrow">Aktuelles</span><h2>Was uns gerade bewegt.</h2></div><div class="grid g3">
<article class="card news reveal"><div class="thumb t1">🏢</div><span class="meta">12. September 2026</span><h3>FWG besucht lokale Betriebe</h3><p>Im Gespräch mit Unternehmen vor Ort: Was braucht der Standort Oelde?</p><a class="more" href="aktuelles.html">Weiterlesen →</a></article>
<article class="card news reveal"><div class="thumb t2">🗳️</div><span class="meta">28. August 2026</span><h3>Neuer Vorsitzender gewählt</h3><p>Bernhard Poppenberg führt die FWG Oelde in die nächste Phase.</p><a class="more" href="aktuelles.html">Weiterlesen →</a></article>
<article class="card news reveal"><div class="thumb t3">🌧️</div><span class="meta">3. August 2026</span><h3>Starkregenvorsorge im Fokus</h3><p>Warum wir Klimaanpassung jetzt konsequent anpacken wollen.</p><a class="more" href="aktuelles.html">Weiterlesen →</a></article></div></div></section>
{band("Oelde gestalten – gemeinsam.","Ob Mitglied, Unterstützer oder mit einer Idee: Wir freuen uns auf Sie.","mitmachen.html","Jetzt mitmachen")}''')

# --- Über uns
pages["ueber-uns.html"] = ("Über uns","Die FWG Oelde: Bürgerinitiative im Rat der Stadt seit 1994.", hero("Über uns","Eine Stimme für Oelde.","Die Freie Wählergemeinschaft Oelde e. V. ist ein Zusammenschluss engagierter Bürgerinnen und Bürger, die sich seit 1994 im Rat der Stadt für ihre Heimat einsetzen.")+f'''
<section><div class="container split"><div class="reveal prose"><span class="eyebrow">Unser Selbstverständnis</span><h2>Sachlich. Unabhängig. Nah dran.</h2>
<p>Wir sind an keine Bundes- oder Landespartei gebunden. Entscheidungen treffen wir nach einem Maßstab: Was nützt den Menschen in Oelde?</p>
<ul class="checks"><li>Kommunalpolitik ohne Parteibuch und Fraktionszwang</li><li>Sachkundige Bürger in den städtischen Ausschüssen</li><li>Transparente Entscheidungen und offene Ohren</li><li>Verantwortung für Finanzen kommender Generationen</li></ul></div>
<div class="panel reveal"><h3>Unsere Werte</h3><p>Ehrlichkeit, Pragmatismus und Heimatverbundenheit. Wir hören zu – bei Infoständen, Betriebsbesuchen und im persönlichen Gespräch.</p><p style="margin:0">„Wer vor Ort lebt, weiß am besten, was vor Ort gebraucht wird."</p></div></div></section>
<section class="alt"><div class="container"><div class="section-head reveal"><span class="eyebrow">Meilensteine</span><h2>Unsere Geschichte.</h2></div><div class="timeline">
<div class="item reveal"><b>1994</b><p>Gründung der FWG Oelde und Einzug in den Stadtrat.</p></div>
<div class="item reveal"><b>2000er</b><p>Engagement für Schulsanierungen und eine konsequente Haushaltskonsolidierung.</p></div>
<div class="item reveal"><b>Fast 17 Jahre</b><p>Friedhelm Hoberg prägt als Vorsitzender die Arbeit der Wählergemeinschaft.</p></div>
<div class="item reveal"><b>Heute</b><p>Bernhard Poppenberg übernimmt den Vorsitz – mit Fokus auf solide Finanzen, Schulen und Klimaanpassung.</p></div></div></div></section>
<section><div class="container"><div class="section-head reveal"><span class="eyebrow">Vorstand</span><h2>Wer die FWG führt.</h2></div><div class="team" style="max-width:300px">{person(P[0])}</div></div></section>
{band("Lernen Sie uns kennen.","Persönlich, am Infostand oder bei einer unserer Veranstaltungen.","termine.html","Zu den Terminen")}''')

# --- Team
pages["ratsmitglieder.html"] = ("Unser Team","Ratsmitglieder und sachkundige Bürger der FWG Oelde.", hero("Unser Team","Ihre Vertreter im Rat.","Ratsmitglieder und sachkundige Bürger der FWG – ansprechbar, engagiert und mitten in Oelde zu Hause.")+f'''
<section><div class="container"><div class="section-head reveal"><span class="eyebrow">Vorstand &amp; Fraktion</span><h2>Im Rat der Stadt Oelde</h2></div><div class="team">{"".join(person(p) for p in P if p["tag"] in ("Vorstand","Rat"))}</div>
<div class="section-head reveal" style="margin-top:4.5rem"><span class="eyebrow">Ausschüsse</span><h2>Sachkundige Bürger</h2><p class="lead">Unsere Expertinnen und Experten aus der Bürgerschaft arbeiten in den Fachausschüssen mit.</p></div><div class="team">{"".join(person(p) for p in P if p["tag"]=="Ausschuss")}</div>
<p class="note"><b>Hinweis:</b> Alle Porträts sind illustrierte Platzhalter. Namen, Funktionen und Kurzbeschreibungen (mit Ausnahme des Vorsitzenden) sind Beispieldaten und müssen durch die echten Angaben ersetzt werden.</p></div></section>''')

# --- Programm
topics=[("finanzen","💶 Solide Finanzen","Wir führen den erfolgreichen Weg des Schuldenabbaus fort. Gebühren und Abgaben halten wir so niedrig wie möglich. Vorteilhafte städtische Beteiligungen wie die Stadtwerke Ostmünsterland erhalten wir."),
("schulen","🎒 Schulen &amp; Bildung","Notwendige Sanierungen und bauliche Erweiterungen unserer Schulen treiben wir weiter voran. Die wichtige Schulsozialarbeit bauen wir aus."),
("klima","🌳 Klimaschutz &amp; Klimaanpassung","Starkregen, Hitze- und Trockenperioden sowie die Belastung unserer Wälder verlangen Vorsorge – für Gesundheit, Umwelt und Infrastruktur."),
("innenstadt","🏙️ Innenstadt &amp; Wirtschaft","Wir stärken Handel, Gastronomie und Gewerbe, schaffen Aufenthaltsqualität und unterstützen Gründerinnen und Gründer – etwa durch Angebote wie Coworking."),
("ehrenamt","🤝 Ehrenamt, Vereine &amp; Soziales","Vereine, Initiativen und Ehrenamtliche halten Oelde zusammen. Wir sichern ihre Förderung und schaffen Räume für Begegnung."),
("mobilitaet","🚲 Mobilität &amp; Wohnen","Sichere Rad- und Fußwege, gut erhaltene Straßen und bezahlbarer Wohnraum für alle Generationen.")]
pages["programm.html"] = ("Programm","Das Programm der FWG Oelde: Finanzen, Schulen, Klima, Innenstadt, Ehrenamt und Mobilität.", hero("Programm","Unsere Ziele für Oelde.","Klar, machbar und finanzierbar – das ist unser Anspruch an Kommunalpolitik.")+f'''
<section><div class="container" style="max-width:860px">{"".join(f'<details id="{i}" class="reveal"{" open" if n==0 else ""}><summary>{t}</summary><div><p>{d}</p></div></details>' for n,(i,t,d) in enumerate(topics))}
<p class="note">Die Beschreibungen fassen die Schwerpunkte des FWG-Wahlprogramms zusammen und sollten mit dem aktuellen Originaltext abgeglichen werden.</p></div></section>
{band("Ihre Idee fehlt?","Sagen Sie uns, was Oelde braucht – wir nehmen es mit in den Rat.","kontakt.html","Kontakt aufnehmen")}''')

# --- Aktuelles
posts=[("12. September 2026","🏢","t1","FWG besucht lokale Betriebe","Bei unseren Informationsbesuchen sprechen wir direkt mit Unternehmerinnen und Unternehmern über Standortfaktoren, Fachkräfte und Verwaltung."),
("28. August 2026","🗳️","t2","Neuer Vorsitzender gewählt","Nach fast 17 Jahren unter Friedhelm Hoberg wählt die FWG Bernhard Poppenberg zum neuen Vorsitzenden."),
("3. August 2026","🌧️","t3","Starkregenvorsorge im Fokus","Klimaanpassung ist Daseinsvorsorge: Wir wollen Risiken erkennen und Oelde robuster machen."),
("20. Juli 2026","💻","t1","Coworking in Oelde","Die FWG informiert sich über flexible Arbeitsplätze und neue Chancen für Selbstständige."),
("5. Juli 2026","⚡","t2","Besuch bei den Stadtwerken Ostmünsterland","Wir schauen hinter die Kulissen der kommunalen Energieversorgung."),
("14. Juni 2026","🐾","t3","Zu Gast im Einzelhandel","Ein Gespräch über Lage, Frequenz und Zukunft der Lindenstraße.")]
pages["aktuelles.html"] = ("Aktuelles","Neuigkeiten und Berichte der FWG Oelde.", hero("Aktuelles","Neuigkeiten aus Oelde.","Berichte, Besuche und Positionen der FWG.")+f'''
<section><div class="container"><div class="grid g3">{"".join(f'<article class="card news reveal"><div class="thumb {c}">{e}</div><span class="meta">{d}</span><h3>{t}</h3><p>{x}</p></article>' for d,e,c,t,x in posts)}</div><p class="note">Beispielhafte Beiträge – bitte durch echte Meldungen ersetzen.</p></div></section>''')

# --- Termine
ev=[("14","OKT","Offene Fraktionssitzung","Gäste willkommen · Vereinsheim Oelde · 19:30 Uhr"),("22","OKT","Bürgersprechstunde","Ratsmitglieder stehen Rede und Antwort · 17:00 Uhr"),("08","NOV","Infostand Wochenmarkt","Kommen Sie ins Gespräch · 9–12 Uhr"),("27","NOV","Mitgliederversammlung","FWG Oelde e. V. · 19:00 Uhr"),("12","DEZ","Jahresabschluss &amp; Glühwein","Gemütlicher Ausklang · 18:00 Uhr")]
pages["termine.html"] = ("Termine","Veranstaltungen und Sprechstunden der FWG Oelde.", hero("Termine","Treffen Sie uns.","Sprechstunden, Infostände und Versammlungen – sprechen Sie uns an.")+f'''
<section><div class="container" style="max-width:860px">{"".join(f'<div class="event reveal"><div class="date"><b>{d}</b><span>{m}</span></div><div><h3 style="margin:0">{t}</h3><span class="meta">{s}</span></div></div>' for d,m,t,s in ev)}<p class="note">Beispieltermine – bitte aktualisieren.</p></div></section>''')

# --- Mitmachen
pages["mitmachen.html"] = ("Mitmachen","Werden Sie Mitglied oder unterstützen Sie die FWG Oelde.", hero("Mitmachen","Gestalten Sie Oelde mit.","Sie brauchen kein Parteibuch – nur Lust, etwas zu bewegen.")+f'''
<section><div class="container split" style="align-items:start"><div class="reveal"><h2>Drei Wege zu uns</h2><div class="grid">
{card("🧑‍🤝‍🧑","Mitglied werden","Bringen Sie Ihre Ideen in Vorstand, Fraktion und Arbeitskreise ein.")}{card("🎤","Gast sein","Kommen Sie zu einer offenen Sitzung und lernen Sie uns kennen.")}{card("💡","Ideen teilen","Melden Sie Anliegen aus Ihrem Viertel – wir kümmern uns.")}</div></div>
<div class="card reveal"><h3>Interesse? Schreiben Sie uns.</h3><form data-demo><div class="row2"><label>Vorname<input required name="v"></label><label>Nachname<input required name="n"></label></div><label>E-Mail<input type="email" required></label><label>Ich möchte<select><option>Mitglied werden</option><option>Mehr Informationen</option><option>Als Gast teilnehmen</option></select></label><label>Nachricht<textarea rows="4"></textarea></label><button class="btn btn-primary" type="submit">Absenden</button><div class="success">Danke! (Demo-Formular – es werden keine Daten versendet.)</div></form></div></div></section>''')

# --- Kontakt
pages["kontakt.html"] = ("Kontakt","Kontakt zur FWG Oelde.", hero("Kontakt","Wir sind für Sie da.","Anregungen, Kritik oder Lob? Schreiben Sie uns.")+f'''
<section><div class="container split" style="align-items:start"><div class="reveal"><ul class="contact-list">
<li><div class="icon">📍</div><div><b>FWG Oelde e. V.</b><br>[Straße Nr.]<br>59302 Oelde</div></li>
<li><div class="icon">✉️</div><div><b>E-Mail</b><br>[info@beispiel.de]</div></li>
<li><div class="icon">📘</div><div><b>Facebook</b><br><a href="https://www.facebook.com/FWGOelde/">facebook.com/FWGOelde</a></div></li></ul>
<p class="note">Adresse und E-Mail sind Platzhalter und müssen ergänzt werden.</p></div>
<div class="card reveal"><form data-demo><label>Name<input required></label><label>E-Mail<input type="email" required></label><label>Nachricht<textarea rows="5" required></textarea></label><button class="btn btn-dark" type="submit">Senden</button><div class="success">Danke! (Demo-Formular)</div></form></div></div></section>''')

# --- Rechtliches
pages["impressum.html"] = ("Impressum","Impressum der FWG Oelde.", hero("Rechtliches","Impressum","")+'<section><div class="container prose"><h2>Angaben gemäß § 5 DDG</h2><p>FWG Oelde e. V.<br>[Straße Nr.]<br>59302 Oelde</p><h2>Vertreten durch</h2><p>Bernhard Poppenberg, Vorsitzender</p><h2>Kontakt</h2><p>E-Mail: [info@beispiel.de]</p><p class="note">Platzhalter – bitte rechtlich prüfen und vervollständigen.</p></div></section>')
pages["datenschutz.html"] = ("Datenschutz","Datenschutzerklärung der FWG Oelde.", hero("Rechtliches","Datenschutz","")+'<section><div class="container prose"><h2>Verantwortlicher</h2><p>FWG Oelde e. V., [Anschrift].</p><h2>Hosting &amp; Schriftarten</h2><p>Diese Seite lädt Schriftarten von Google Fonts. Für eine datenschutzfreundliche Variante sollten die Fonts lokal eingebunden werden.</p><h2>Kontaktformulare</h2><p>Die Formulare dieser Vorlage sind reine Demos und übertragen keine Daten.</p><p class="note">Platzhaltertext – vor Veröffentlichung rechtlich prüfen.</p></div></section>')

for fn,(t,d,b) in pages.items():
    open(fn,"w",encoding="utf-8").write(layout(fn,t,b,d))
open("assets/img/favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#0f5c3a"/><text x="32" y="41" font-family="Arial" font-weight="800" font-size="24" text-anchor="middle" fill="#f08a24">FWG</text></svg>')
print(len(pages),"Seiten")
