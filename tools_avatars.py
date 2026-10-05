"""Erzeugt illustrierte Platzhalter-Porträts (SVG) für Ratsmitglieder."""
import json
PEOPLE = json.load(open("people.json", encoding="utf-8"))
BG = [("#1f6f4a","#8fd3a8"),("#e8833a","#ffd1a3"),("#2b5d8a","#a9cdee"),("#7a4aa0","#d9c3ee"),("#c2485b","#f6b9c4"),("#2f8f8f","#a6e3e0")]
for i,p in enumerate(PEOPLE):
    skin,hair,cloth,style,glass,beard = p["look"]
    b1,b2 = BG[i % len(BG)]
    hairs = {
     "short": f'<path d="M62 92c-2-34 20-52 48-52s50 18 48 52c-8-18-24-26-48-26s-40 8-48 26z" fill="{hair}"/>',
     "long": f'<path d="M58 100c-6-44 18-64 52-64s58 20 52 64l6 70h-26l-4-60H82l-4 60H52z" fill="{hair}"/>',
     "bob": f'<path d="M60 108c-8-46 14-68 50-68s58 22 50 68l-2 24h-18V92H80v40H62z" fill="{hair}"/>',
     "bald": f'<path d="M66 84c4-14 20-22 44-22s40 8 44 22c-10-8-26-12-44-12s-34 4-44 12z" fill="{hair}" opacity=".35"/>',
     "curly": f'<g fill="{hair}"><circle cx="72" cy="78" r="20"/><circle cx="96" cy="62" r="22"/><circle cx="124" cy="62" r="22"/><circle cx="148" cy="78" r="20"/><circle cx="110" cy="56" r="22"/></g>',
    }[style]
    back = hairs if style in ("long","bob") else ""
    front = "" if style in ("long","bob") else hairs
    if style in ("long","bob"):
        front = f'<path d="M72 92c6-18 22-26 38-26s32 8 38 26c-10-8-22-10-38-10s-28 2-38 10z" fill="{hair}"/>'
    gl = '<g fill="none" stroke="#2a2a2a" stroke-width="3"><circle cx="92" cy="106" r="13"/><circle cx="128" cy="106" r="13"/><path d="M105 106h10"/></g>' if glass else ""
    bd = f'<path d="M80 124c2 34 20 46 30 46s28-12 30-46c-8 12-18 16-30 16s-22-4-30-16z" fill="{hair}"/>' if beard else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 260" role="img" aria-label="Platzhalter-Porträt {p["name"]}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{b1}"/><stop offset="1" stop-color="{b2}"/></linearGradient></defs>
<rect width="220" height="260" fill="url(#g)"/>
<circle cx="170" cy="50" r="60" fill="#fff" opacity=".12"/><circle cx="30" cy="230" r="70" fill="#fff" opacity=".10"/>
{back}
<path d="M20 260c4-52 42-72 90-72s86 20 90 72z" fill="{cloth}"/>
<path d="M92 188l18 28 18-28z" fill="#fff" opacity=".9"/>
<rect x="95" y="150" width="30" height="42" rx="12" fill="{skin}"/>
<ellipse cx="110" cy="112" rx="42" ry="50" fill="{skin}"/>
<ellipse cx="68" cy="116" rx="7" ry="11" fill="{skin}"/><ellipse cx="152" cy="116" rx="7" ry="11" fill="{skin}"/>
{front}{bd}
<ellipse cx="92" cy="106" rx="4" ry="5" fill="#2a2a2a"/><ellipse cx="128" cy="106" rx="4" ry="5" fill="#2a2a2a"/>
<path d="M84 94q8-6 16 0M120 94q8-6 16 0" stroke="#2a2a2a" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>
{gl}
<path d="M110 112v14q-5 3-9 1" stroke="#00000030" stroke-width="3" fill="none" stroke-linecap="round"/>
<path d="M96 138q14 12 28 0" stroke="#7a2e2e" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>'''
    open(f"assets/img/team/{p['id']}.svg","w",encoding="utf-8").write(svg)
print(len(PEOPLE),"Porträts")
