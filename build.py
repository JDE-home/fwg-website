"""Generiert die statische FWG-Oelde-Website: python3 tools_avatars.py && python3 build.py"""
import json
P = {p["id"]: p for p in json.load(open("people.json", encoding="utf-8"))}
NAV = [("index.html","Start"),("ueber-uns.html","Über uns"),("ratsmitglieder.html","Unser Team"),("programm.html","Programm"),("aktuelles.html","Aktuelles"),("termine.html","Termine")]
MOTTO = "Gemeinschaft fördern. Bürgernähe leben. Zukunft gestalten."

def layout(fn, title, body, desc):
    nav = "".join(f'<li><a href="{h}"{" aria-current=page" if h==fn else ""}>{t}</a></li>' for h,t in NAV)
    nav += f'<li><a class="cta" href="mitmachen.html"{" aria-current=page" if fn=="mitmachen.html" else ""}>Mitmachen</a></li>'
    logo = '<span class="logo"><img src="assets/img/logo.jpg" alt=""></span>'
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} – FWG Oelde</title><meta name="description" content="{desc}">
<meta name="theme-color" content="#29488b">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css"></head><body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="site-header"><div class="container nav">
<a class="brand" href="index.html" aria-label="FWG Oelde Startseite">{logo}<span>FWG Oelde<small>Bürgernah in Oelde</small></span></a>
<button class="burger" aria-label="Menü" aria-expanded="false"><span></span></button>
<ul class="menu">{nav}</ul></div></header>
<main id="main">{body}</main>
<footer><div class="container"><div class="cols">
<div><a class="brand" href="index.html" style="color:#fff">{logo}<span>FWG Oelde</span></a><p style="margin-top:1rem">Unabhängig, überparteilich, bürgernah – seit 1994 im Rat der Stadt Oelde.</p></div>
<div><h4>Entdecken</h4><a href="ueber-uns.html">Über uns</a><a href="ratsmitglieder.html">Unser Team</a><a href="programm.html">Programm</a></div>
<div><h4>Aktiv werden</h4><a href="aktuelles.html">Aktuelles</a><a href="termine.html">Termine</a><a href="mitmachen.html">Mitmachen &amp; Spenden</a><a href="kontakt.html">Kontakt</a></div>
<div><h4>Rechtliches</h4><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div>
</div><div class="bottom"><span>© 2026 FWG Oelde e. V. · Entwurf – Porträts sind Platzhalter</span><span>lokal engagiert</span></div></div></footer>
<script src="assets/js/main.js"></script></body></html>'''

def hero(eyebrow, h, p): return f'<div class="page-hero"><div class="container"><span class="eyebrow">{eyebrow}</span><h1>{h}</h1><p>{p}</p></div></div>'
def contact_line(p):
    c = []
    if p.get("phone"): c.append(f'<a href="tel:{p["phone"].replace(" ","").replace("/","")}">📞 {p["phone"]}</a>')
    if p.get("email"): c.append(f'<a href="mailto:{p["email"]}">✉️ {p["email"]}</a>')
    return f'<div class="contact-line">{"".join(c)}</div>' if c else ""
def person(p): return f'<article class="person reveal"><div class="ph"><img src="assets/img/team/{p["id"]}.svg" alt="Platzhalter-Porträt von {p["name"]}"><span class="tag">{p["tag"]}</span></div><div class="info"><h3>{p["name"]}</h3><div class="role">{p["role"]}</div><p>{p["bio"]}</p>{contact_line(p)}</div></article>'
def band(t, s, href, label): return f'<section style="padding-top:0"><div class="container"><div class="band reveal"><div><h2>{t}</h2><p style="margin:.5rem 0 0">{s}</p></div><a class="btn btn-dark" href="{href}">{label} →</a></div></div></section>'
def card(i,t,d,l=None): return f'<div class="card reveal"><div class="icon">{i}</div><h3>{t}</h3><p>{d}</p>{f"<a class=more href={l}>Mehr erfahren →</a>" if l else ""}</div>'
def ul(items): return '<ul class="checks">'+"".join(f"<li>{i}</li>" for i in items)+"</ul>"

topics=[("gemeinschaft","🤝","Gemeinschaft &amp; Bürgernähe","Ehrenamt, Kultur und Beteiligung stärken – transparent und nah an den Menschen.",
 ["Ehrenamt und Seniorenarbeit fördern","Kultur für Jung und Alt","Transparente Entscheidungen und Bürgerbeteiligung","Digitale Services und Live-Übertragung von Rats- und Ausschusssitzungen","Bürgersprechstunden der Bürgermeisterin bzw. des Bürgermeisters","Jugendparlament"]),
("finanzen","💶","Solide Finanzen","Schuldenabbau und sparsamer Mitteleinsatz – für kommende Generationen.",
 ["Schuldenabbau und sparsamer Mitteleinsatz","Investitionen nur mit Kosten-Nutzen-Bewertung","Keine Prestigeprojekte – „Trinkwasserspender statt künstlicher Wasserläufe“","Sach- und Personalkosten kritisch prüfen"]),
("bildung","🎒","Bildung","Wohnortnahe Kitas und starke Schulen in allen Ortsteilen.",
 ["Wohnortnahe Kitaplätze","Erhalt und Ausbau der Schulen","Mehr Schulsozialarbeit","Unterstützung der VHS"]),
("wirtschaft","🏭","Wirtschaftsstandort","Aktive Wirtschaftsförderung für Handel, Handwerk und Gewerbe.",
 ["Aktive Wirtschaftsförderung und Citymanagement","Leerstände reduzieren","Maßvolle Entwicklung von Wohn- und Gewerbeflächen, auch für Kleingewerbe und Handwerk","Niedriger Gewerbesteuersatz"]),
("klima","🌳","Klimaschutz","Nachvollziehbare Maßnahmen gegen Hochwasser und Hitze.",
 ["Hochwasser- und Hitzeschutz","Radwege ausbauen und instand halten","Mehr Fahrradstellplätze in der Innenstadt","Erhalt der Hochbeete in der Fußgängerzone"]),
("ortsteile","🏘️","Ortsteile","Lette, Stromberg und Sünninghausen sind mehr als Randlagen.",
 ["Kitas und Schulen erhalten","Bauplätze bereitstellen","Straßen, Rad- und Wirtschaftswege sowie Sportanlagen erhalten"]),
("stadt","🏙️","Lebenswerte Stadt","Bezahlbar, barrierefrei und mit guter Infrastruktur.",
 ["Bezahlbarer und barrierefreier Wohnraum","Sanierung der Geiststraße","Barrierefreiheit in der Innenstadt","Wiederaufbau der Gläsernen Küche im Park","Gutes Freizeit- und Sportstättenangebot"])]


def contact_form(kind, submit_cls="btn-primary"):
    """Echtes Formular -> api/contact.php (siehe assets/js/main.js)."""
    if kind == "mitmachen":
        top = '<div class="row2"><label>Vorname<input required name="vorname" autocomplete="given-name" maxlength="60"></label><label>Nachname<input required name="nachname" autocomplete="family-name" maxlength="60"></label></div>'
        mid = '<label>E-Mail<input type="email" required name="email" autocomplete="email" maxlength="200"></label><label>Ich möchte<select name="topic"><option>Mitglied werden</option><option>Mehr Informationen</option><option>Spenden</option><option>Sonstiges</option></select></label><label>Nachricht (optional)<textarea rows="4" name="message" maxlength="5000"></textarea></label>'
    else:
        top = '<div class="row2"><label>Name<input required name="name" autocomplete="name" maxlength="120"></label><label>Telefon (optional)<input type="tel" name="phone" autocomplete="tel" maxlength="50"></label></div>'
        mid = '<label>E-Mail<input type="email" required name="email" autocomplete="email" maxlength="200"></label><label>Nachricht<textarea rows="5" required minlength="5" name="message" maxlength="5000"></textarea></label>'
    return f'''<form data-contact action="api/contact.php" method="post" novalidate>
<input type="hidden" name="form" value="{kind}"><input type="hidden" name="ts" value="">
<div class="hp" aria-hidden="true"><label>Bitte leer lassen<input name="website" tabindex="-1" autocomplete="off"></label></div>
{top}{mid}
<label class="check"><input type="checkbox" name="privacy" value="1" required><span>Ich habe die <a href="datenschutz.html" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen und bin einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage verwendet werden.</span></label>
<button class="btn {submit_cls}" type="submit">Absenden</button>
<div class="form-status" role="status" aria-live="polite"></div></form>'''

VORSTAND = [dict(P[i], tag="Vorstand", role=r, bio=b) for i,r,b in [
 ("poppenberg","1. Vorsitzender","Seit 2026 einstimmig gewählt, Nachfolger von Friedhelm Hoberg. Ratsmitglied mit Schwerpunkt Umwelt, Energie und Mobilität."),
 ("hakenholt","Stellv. Vorsitzender","Beisitzer, jetzt stellvertretender Vorsitzender. Sachkundiger Bürger aus Lette."),
 ("fertich","Kassierer","Verwaltet die Vereinsfinanzen. Sachkundiger Bürger für Schule, Kultur und Sport."),
 ("soldat","Schriftführer","Führt das Protokoll des Vereins.")]]
pages = {}
# ---------- Start
home_cards = "".join(card(i,t,d,f"programm.html#{k}") for k,i,t,d,_ in [topics[1],topics[2],topics[3],topics[6],topics[5],topics[0]])
news = [("Juli 2026","🗳️","t2","Jahreshauptversammlung in Lette","Bernhard Poppenberg wird einstimmig zum neuen Vorsitzenden gewählt – Friedhelm Hoberg gibt nach knapp 17 Jahren ab."),
("2026","🎤","t1","Haushaltsrede 2026","Fraktionsvorsitzender Thorsten Retzlaff bezieht für die FWG Stellung zum städtischen Haushalt."),
("November 2026","📊","t3","Haushaltsberatungen","Unser Bericht über die Beratungen folgt im November.")]
pages["index.html"] = ("Start","Die Freie Wählergemeinschaft Oelde: unabhängig, überparteilich und bürgernah – seit 1994 im Stadtrat.", f'''
<div class="hero"><span class="blob b1"></span><span class="blob b2"></span><div class="container hero-grid">
<div><span class="eyebrow">Freie Wählergemeinschaft · seit 1994</span>
<h1><em>Bürgernah</em> in Oelde.</h1>
<p>Unabhängig, überparteilich und ohne Fraktionszwang: Wir sind Bürgerinnen und Bürger, die Oelde, Lette, Stromberg und Sünninghausen mit Sachverstand und Herz mitgestalten.</p>
<div class="actions"><a class="btn btn-primary" href="programm.html">Unser Programm →</a><a class="btn btn-ghost" href="ratsmitglieder.html">Das Team kennenlernen</a></div><span class="motto">{MOTTO}</span></div>
<div class="hero-stack"><img src="assets/img/team/retzlaff.svg" alt="Platzhalter-Porträt Thorsten Retzlaff"><img src="assets/img/team/steuer.svg" alt="Platzhalter-Porträt Manuela Steuer"><img src="assets/img/team/knop.svg" alt="Platzhalter-Porträt Felix Knop"><div class="badge"><b>30+</b>Jahre im Rat</div></div>
</div></div>
<div class="container"><div class="stats">
<div class="stat"><b>1994</b><span>gegründet</span></div><div class="stat"><b data-count="5">0</b><span>Sitze im Stadtrat</span></div><div class="stat"><b data-count="4">0</b><span>Stadtteile im Blick</span></div><div class="stat"><b>0</b><span>Fraktionszwang</span></div></div></div>
<section><div class="container"><div class="section-head reveal"><span class="eyebrow">Wofür wir stehen</span><h2>Politik, die bei den Menschen ankommt.</h2><p class="lead">Die Schwerpunkte aus unserem Wahlprogramm 2025.</p></div>
<div class="grid g3">{home_cards}</div></div></section>
<section class="alt"><div class="container"><blockquote class="quote reveal">Oelde hat kein Einnahmenproblem, sondern ein Ausgabenproblem. Darum setzen wir Prioritäten statt „Wünsch dir was“.</blockquote></div></section>
<section><div class="container"><div class="split"><div class="reveal"><span class="eyebrow">Unser Team</span><h2>Gesichter, die Sie kennen.</h2><p class="lead">Fünf Ratsmitglieder und viele sachkundige Bürgerinnen und Bürger aus allen Ortsteilen – Nachbarn, Unternehmer, Eltern, Vereinsmenschen.</p><a class="btn btn-dark" href="ratsmitglieder.html">Alle ansehen →</a></div>
<div class="grid" style="grid-template-columns:repeat(2,1fr)">{person(P["retzlaff"])}{person(P["knop"])}</div></div></div></section>
<section class="alt"><div class="container"><div class="section-head reveal"><span class="eyebrow">Aktuelles</span><h2>Was uns gerade bewegt.</h2></div><div class="grid g3">
{"".join(f'<article class="card news reveal"><div class="thumb {c}">{e}</div><span class="meta">{d}</span><h3>{t}</h3><p>{x}</p><a class="more" href="aktuelles.html">Alle Beiträge →</a></article>' for d,e,c,t,x in news)}</div></div></section>
{band("Oelde gestalten – gemeinsam.","Mitglied werden, mitreden, unterstützen: Wir freuen uns auf Sie.","mitmachen.html","Jetzt mitmachen")}''')

# ---------- Über uns
tl=[("09.02.1994","Gründung der FWG Oelde. Ziel: eine absolute Mehrheit einer Partei im Stadtrat verhindern."),
("2005","Die heutige Vereinssatzung wird beschlossen."),
("2011–2013","Die Zahl der Mitglieder verdreifacht sich."),
("2009","Karl-Friedrich Knop, Gründungsmitglied der FWG, wird zum Bürgermeister der Stadt Oelde gewählt und 2014 im Amt bestätigt – bis 2020."),
("2017","Klausurtagung „FWG 2020“: Finanzen, Schule, Familie und Soziales, Bauvorhaben und Wohnungsbau im Fokus."),
("2019","25 Jahre FWG Oelde."),
("2024","30 Jahre FWG: Feier und Mitgliederehrung im Heimathaus Lette."),
("2025","Kommunalwahl: Die FWG behält ihre 5 Sitze im auf 50 Mitglieder gewachsenen Rat."),
("2026","Bernhard Poppenberg wird einstimmig zum Vorsitzenden gewählt – Nachfolger von Friedhelm Hoberg nach knapp 17 Jahren.")]
pages["ueber-uns.html"] = ("Über uns","Die FWG Oelde: unabhängige Wählergemeinschaft im Rat der Stadt seit 1994.", hero("Über uns","Lokal engagiert. Unabhängig. Überparteilich.","Die Freie Wählergemeinschaft Oelde e. V. ist nur in Oelde und im Kreis Warendorf aktiv – ohne „Mutterpartei“, ohne Fraktionszwang.")+f'''
<section><div class="container split"><div class="reveal prose"><span class="eyebrow">Unser Selbstverständnis</span><h2>Sachlich. Bürgernah. Unabhängig.</h2>
<p>Unsere Entscheidungen richten sich allein nach dem Wohl der Menschen in Oelde und den Ortsteilen Lette, Stromberg und Sünninghausen.</p>
{ul(["Kommunalpolitik ohne Bundes- oder Landespartei im Rücken","Kein Fraktionszwang","Sachkundige Bürger arbeiten in den städtischen Ausschüssen mit","Typische Politikfelder: Finanzen, Schule, Familie und Soziales, Senioren, Bauvorhaben, Wohnungsbau"])}</div>
<div class="panel reveal"><h3>Gründungsmitglied &amp; Altbürgermeister</h3><img src="assets/img/team/knopkf.svg" alt="Platzhalter-Porträt Karl-Friedrich Knop" style="width:150px;border-radius:22px;margin:0 0 1rem;border:4px solid rgba(255,255,255,.8)"><p><b>Karl-Friedrich Knop</b> gehört zu den Gründern der FWG Oelde und war von 2009 bis 2020 Bürgermeister der Stadt Oelde.</p></div></div></section>
<section class="alt"><div class="container"><div class="section-head reveal"><span class="eyebrow">Meilensteine</span><h2>Unsere Geschichte.</h2></div><div class="timeline">{"".join(f'<div class="item reveal"><b>{y}</b><p>{t}</p></div>' for y,t in tl)}</div></div></section>
<section><div class="container"><div class="section-head reveal"><span class="eyebrow">Vorstand</span><h2>Wer den Verein führt.</h2><p class="lead">Der engere Vorstand der FWG Oelde e. V. – gewählt auf der Mitgliederversammlung 2026 in Lette.</p></div>
<div class="team">{"".join(person(v) for v in VORSTAND)}</div>
<div class="card reveal" style="margin-top:1.6rem"><h3>Weitere Vorstandsmitglieder (Beisitzer)</h3><ul class="mini-list"><li>Hubert Bleß</li><li>Harald Herklotz</li><li>Friedhelm Hoberg</li><li>Ludger Lücke</li><li>Thomas Populoh</li><li>Thorsten Retzlaff</li><li>Manuela Steuer</li></ul></div>
<div class="grid g2" style="margin-top:1.4rem">{card("📜","Satzung in Kürze","Eingetragener Verein (VR 70744). Zweck ist die Teilnahme an Kommunal- und Kreistagswahlen mit eigenen Wahlvorschlägen. Mitglied wird, wer mindestens 16 Jahre alt ist und das Grundgesetz anerkennt. Der Vorstand wird für zwei Jahre ehrenamtlich gewählt.")}{card("🏛️","Auch im Kreistag","Dorothea Nienkemper ist Fraktionsvorsitzende der FWG im Kreistag Warendorf.")}</div></div></section>
{band("Lernen Sie uns kennen.","Persönlich, am Infostand oder bei einem unserer Formate.","termine.html","Treffen &amp; Formate")}''')

# ---------- Team
frak=[P[k] for k in ("retzlaff","knop","populoh","poppenberg","steuer")]
sk=[("Soziales, Familien, Senioren · Finanzen · Wirtschaftsförderung",["bless","fibbe","hoberg","aschulz"]),("Umwelt, Energie, Mobilität &amp; Verkehr · Forum",["rdesel","hakenholt","kemper","schestak","specken"]),("Schule, Kultur, Sport · Wirtschaftsförderung",["fertich","haensel","pickenaecker","sumkoetter"])]
pages["ratsmitglieder.html"] = ("Unser Team","Ratsmitglieder und sachkundige Bürger der FWG Oelde.", hero("Unser Team","Ihre Vertreter im Rat.","Fünf Ratsmitglieder und engagierte sachkundige Bürgerinnen und Bürger aus allen Ortsteilen.")+f'''
<section><div class="container"><div class="section-head reveal"><span class="eyebrow">Fraktion</span><h2>Im Rat der Stadt Oelde</h2><p class="lead">Die FWG stellt seit der Kommunalwahl 2025 weiterhin fünf der 50 Ratsmitglieder.</p></div><div class="team">{"".join(person(p) for p in frak)}</div>
<div class="section-head reveal" style="margin-top:4.5rem"><span class="eyebrow">Ausschüsse</span><h2>Sachkundige Bürgerinnen und Bürger</h2><p class="lead">Sie bringen Fachwissen aus Beruf, Verein und Ortsteil in die städtischen Ausschüsse ein.</p></div>
{"".join(f'<h3 class="reveal" style="margin:2rem 0 1rem;color:var(--orange-d)">{t}</h3><div class="team">{"".join(person(P[i]) for i in ids)}</div>' for t,ids in sk)}
<p class="note"><b>Hinweis:</b> Alle Porträts sind illustrierte Platzhalter und zeigen nicht das tatsächliche Aussehen. Sie werden durch echte Fotos ersetzt.</p></div></section>''')

# ---------- Programm
fin=[("2015","Ablehnung","no","Streit um die Grundsteuererhöhung; Haushalt von CDU und SPD beschlossen."),
("2016","Zustimmung „ohne gutes Gefühl“","mid","Defizit 2015 von über 5 Mio. € trotz Haushaltssperre."),
("2019","Zustimmung","ok","Oelde „auf gutem Weg“, Warnung vor einer Schuldenverdopplung auf 67 Mio. €."),
("2020","Zustimmung","ok","Investitionen von rund 35 Mio. €, vor allem in Schulen; Ablehnung der AUREA-Erweiterung."),
("2023","Zustimmung","ok","Priorisierung und Transparenz; Wohnungsbau-Antrag mit SPD und Grünen; PV-Mittel von 100.000 auf 300.000 €."),
("2024","Ablehnung","no","Multifunktionshalle von 19,13 auf 22,8 Mio. € gestiegen, Wasserspiel im Kreisverkehr, zu optimistische Gewerbesteuerprognose."),
("2025","Zustimmung unter starken Vorbehalten","mid","Defizit von 12,36 Mio. €; Schulden steigen bis 2027 auf 73,73 Mio. €. „Planung muss dem Budget folgen.“")]
pages["programm.html"] = ("Programm","Das Wahlprogramm 2025 der FWG Oelde: Gemeinschaft, Finanzen, Bildung, Wirtschaft, Klima, Ortsteile.", hero("Programm 2025",MOTTO,"Unser Wahlprogramm zur Kommunalwahl vom 14. September 2025 – klar, machbar und finanzierbar.")+f'''
<section><div class="container" style="max-width:860px">{"".join(f'<details id="{k}" class="reveal"{" open" if n==0 else ""}><summary><span>{i} {t}</span></summary><div><p>{d}</p>{ul(items)}</div></details>' for n,(k,i,t,d,items) in enumerate(topics))}</div></section>
<section class="alt" id="haushalt"><div class="container"><div class="section-head reveal"><span class="eyebrow">Haushalt im Fokus</span><h2>Wie die FWG zum Haushalt stimmt.</h2><p class="lead">Unsere Linie: generationengerechtes Kostenbewusstsein, Schuldenabbau, Transparenz. Zustimmen, wenn es trägt – ablehnen, wenn nicht.</p></div>
<div class="table-wrap reveal"><table class="fin"><thead><tr><th>Jahr</th><th>Votum</th><th>Begründung</th></tr></thead><tbody>{"".join(f'<tr><td><b>{y}</b></td><td><span class="pill {c}">{v}</span></td><td>{t}</td></tr>' for y,v,c,t in fin)}</tbody></table></div></div></section>
{band("Ihre Idee fehlt?","Sagen Sie uns, was Oelde braucht – wir nehmen es mit in den Rat.","kontakt.html","Kontakt aufnehmen")}''')

# ---------- Aktuelles
posts=[("November 2026","📊","t3","Bericht: Haushaltsberatungen","Wir berichten über die Haushaltsberatungen im Rat – der Bericht folgt im November.","Folgt"),
("2026","🎤","t1","Haushaltsrede von Thorsten Retzlaff","Der Fraktionsvorsitzende der FWG bezieht Stellung zum Haushalt 2026. Die Rede im Wortlaut wird hier veröffentlicht. Hintergrund: Die Rücklagen der Stadt sind fast aufgebraucht, für 2026 ist keine Neuverschuldung geplant, der erwartete Fehlbetrag soll aus den Rücklagen gedeckt werden.","Rede"),
("Juli 2026","🗳️","t2","Jahreshauptversammlung in Lette","Bei der ordentlichen Mitgliederversammlung im Sportlerheim Lette wählte die FWG Bernhard Poppenberg einstimmig zum neuen 1. Vorsitzenden. Er folgt auf Friedhelm Hoberg, der nach knapp 17 Jahren an der Spitze nicht erneut antrat. Neuer stellvertretender Vorsitzender ist Achim Hakenholt, Kassierer Alexander Fertich, Schriftführer Wolf-Rüdiger Soldat.","Bericht")]
pages["aktuelles.html"] = ("Aktuelles","Neuigkeiten, Besuche und Positionen der FWG Oelde.", hero("Aktuelles 2026","Neuigkeiten aus Oelde.","Berichte und Positionen der FWG aus dem laufenden Jahr.")+f'''
<section><div class="container"><div class="grid g3">{"".join(f'<article class="card news reveal"><div class="thumb {c}">{e}</div><span class="meta">{d} · <b>{k}</b></span><h3>{t}</h3><p>{x}</p></article>' for d,e,c,t,x,k in posts)}</div></div></section>''')

# ---------- Termine
fm=[("🗣️","Bürgersprechstunden","Ratsmitglieder vor Ort in den Ortsteilen – sprechen Sie uns an."),("🛒","Infostand Wochenmarkt","Kommen Sie ins Gespräch, wir hören zu."),("📊","Haushaltsberatungen","Im November berät der Rat den Haushalt – wir berichten."),("🏢","Betriebsbesuche","Wir informieren uns vor Ort bei Unternehmen und Einrichtungen."),("📋","Mitgliederversammlung","Mindestens einmal im Jahr, Einladung mit zwei Wochen Frist."),("💶","Veranstaltung zu den Stadtfinanzen","Eine öffentliche Veranstaltung ist für den Herbst geplant.")]
pages["termine.html"] = ("Termine","Formate und Veranstaltungen der FWG Oelde.", hero("Termine","Treffen Sie uns.","Aktuell sind keine festen Termine veröffentlicht. So finden Sie den Kontakt zu uns:")+f'''
<section><div class="container"><div class="grid g3">{"".join(card(i,t,d) for i,t,d in fm)}</div><p class="note">Konkrete Termine werden hier ergänzt, sobald sie feststehen. Fragen Sie gern über das <a href="kontakt.html">Kontaktformular</a> nach.</p></div></section>
{band("Nichts verpassen.","Schreiben Sie uns, wir halten Sie auf dem Laufenden.","kontakt.html","Kontakt")}''')

# ---------- Mitmachen
pages["mitmachen.html"] = ("Mitmachen","Mitglied werden oder die FWG Oelde unterstützen.", hero("Mitmachen","Gestalten Sie Oelde mit.","Sie brauchen kein Parteibuch – nur Lust, etwas zu bewegen.")+f'''
<section><div class="container split" style="align-items:start"><div class="reveal"><h2>Mitglied werden</h2><p>Mitglied der FWG kann werden, wer mindestens 16 Jahre alt ist und das Grundgesetz anerkennt. Über die Aufnahme entscheidet der Vorstand, ein Austritt ist jederzeit schriftlich möglich.</p>
<div class="grid">{card("🧑‍🤝‍🧑","Mitreden","Bringen Sie Ihre Ideen in Vorstand, Fraktion und Gesprächsrunden ein.")}{card("❤️","Spenden","Unterstützen Sie unsere Arbeit: Sparkasse Münsterland Ost, <b>IBAN DE29 4005 0150 0042 6378 27</b>, BIC WELADED1MST. Für eine Zuwendungsbestätigung geben Sie bitte Ihre Anschrift im Verwendungszweck an.")}</div></div>
<div class="card reveal"><h3>Interesse? Schreiben Sie uns.</h3>{contact_form("mitmachen")}</div></div></section>''')

# ---------- Kontakt
pages["kontakt.html"] = ("Kontakt","Kontakt zur FWG Oelde.", hero("Kontakt","Wir sind für Sie da.","Anregungen, Kritik oder Lob? Schreiben Sie uns.")+f'''
<section><div class="container split" style="align-items:start"><div class="reveal"><ul class="contact-list">
<li><div class="icon">📍</div><div><b>FWG Oelde e. V.</b><br>59302 Oelde<br><small>[Postanschrift ergänzen]</small></div></li>
<li><div class="icon">✉️</div><div><b>E-Mail</b><br><a href="mailto:info@fwg-oelde.de">info@fwg-oelde.de</a></div></li>
<li><div class="icon">📘</div><div><b>Facebook</b><br><a href="https://www.facebook.com/FWGOelde/">facebook.com/FWGOelde</a></div></li></ul></div>
<div class="card reveal">{contact_form("kontakt","btn-dark")}</div></div></section>''')

pages["impressum.html"] = ("Impressum","Impressum der FWG Oelde.", hero("Rechtliches","Impressum","")+'<section><div class="container prose"><h2>Angaben gemäß § 5 DDG</h2><p>FWG Oelde e. V.<br>[Anschrift]<br>59302 Oelde</p><p>Vereinsregister: VR 70744, Registergericht: [ergänzen]</p><h2>Vertreten durch</h2><p>Bernhard Poppenberg, Vorsitzender</p><h2>Kontakt</h2><p>E-Mail: info@fwg-oelde.de</p><p class="note">Entwurf – bitte rechtlich prüfen und vervollständigen.</p></div></section>')
pages["datenschutz.html"] = ("Datenschutz","Datenschutzerklärung der FWG Oelde.", hero("Rechtliches","Datenschutz","")+'<section><div class="container prose"><h2>Verantwortlicher</h2><p>FWG Oelde e. V., [Anschrift], E-Mail: info@fwg-oelde.de</p><h2>Kontaktformulare</h2><p>Wenn Sie uns über das Kontakt- oder Mitmachen-Formular schreiben, verarbeiten wir Ihren Namen, Ihre E-Mail-Adresse, optional Ihre Telefonnummer und Ihre Nachricht, um Ihre Anfrage zu beantworten (Art. 6 Abs. 1 lit. a und b DSGVO). Die Daten werden per E-Mail an uns übermittelt und nicht auf dem Webserver gespeichert. Wir löschen sie, sobald die Anfrage erledigt ist und keine gesetzlichen Aufbewahrungspflichten bestehen. Zum Schutz vor Missbrauch wird kurzzeitig eine gekürzte Prüfsumme Ihrer IP-Adresse zur Mengenbegrenzung zwischengespeichert.</p><h2>Schriftarten</h2><p>Diese Seite lädt Schriftarten von Google Fonts. Für eine datenschutzfreundliche Variante sollten die Fonts lokal eingebunden werden.</p><h2>Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit und Widerspruch sowie auf Beschwerde bei einer Aufsichtsbehörde.</p><p class="note">Entwurf – vor Veröffentlichung rechtlich prüfen.</p></div></section>')

for fn,(t,d,b) in pages.items():
    open(fn,"w",encoding="utf-8").write(layout(fn,t,b,d))
open("assets/img/favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#29488b"/><text x="32" y="41" font-family="Arial" font-weight="800" font-size="24" text-anchor="middle" fill="#fff">FWG</text><rect x="12" y="48" width="40" height="4" rx="2" fill="#ff984f"/></svg>')
print(len(pages),"Seiten")
