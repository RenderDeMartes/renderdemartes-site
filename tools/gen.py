# -*- coding: utf-8 -*-
"""Generates renderdemartes.com (2026 redesign): home + /academic/.

Home CV shows five studios only; everything else points at LinkedIn.
Studios with several shows render a gallery: one slide per show, dots to switch.
"""
import html, io, os, json

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
ROOT = _os.path.dirname(_HERE)   # site root is this folder's parent
LINKEDIN = "https://www.linkedin.com/in/esteban-rodriguez-488a68147/"

S = lambda title, img, yt=None: dict(title=title, img=img, yt=yt)

CREDITS = [
("2026", [
  dict(studio="Superneat", role="RIGGING TD · CONTRACT",
       meta="Feb 2026 — present · remote",
       body="Current gig. Rigging TD on a remote team, carrying the Mutant Tools workflow into a new pipeline.",
       tools=["MAYA","MUTANT TOOLS","PYTHON"],
       shows=[S("Rigging TD", "assets/img/work/superneat.png")]),

  dict(studio="The Coalition", role="CHARACTER RIGGER 3 · MICROSOFT",
       meta="Apr 2025 — Feb 2026 · Vancouver, hybrid",
       body="Body and prop rigs for AAA characters and skins in Unreal. Rod dynamics, Control Rig and Animation Blueprints, plus wrapping tools and Confluence docs so the next rigger does not start from zero.",
       tools=["MAYA","UNREAL","CONTROL RIG","PYTHON"],
       shows=[S("Gears of War: E-Day", "assets/img/still/gears-e-day.jpg", "12m0bw1W_tk")]),
]),

("2022", [
  dict(studio="Stellar Creative Lab", role="RIGGING SUPERVISOR · MARVEL · SONY",
       meta="Feb 2022 — Mar 2025 · Vancouver, remote",
       body="Ran the rigging department across five shows. Rebuilt the rigging system for What If…?, designed the pipeline from model intake to delivery, handled crowd rigs for 300+ assets, and built the save/load tooling the team lives in.",
       tools=["MAYA","PYTHON","MUTANT TOOLS","CROWDS"],
       shows=[S("Sausage Party: Foodtopia", "assets/img/still/foodtopia-s1.jpg", "JrmC2uJXsMM"),
              S("Sausage Party: Foodtopia — Season 2", "assets/img/still/foodtopia-s1.jpg"),
              S("Marvel Zombies", "assets/img/still/marvel-zombies.jpg", "twHYF506-9Y"),
              S("What If…? Season 2", "assets/img/still/what-if-s2.jpg", "TiEVqZ2Bc_c"),
              S("What If…? Season 3", "assets/img/still/what-if-s3.jpg", "umiKiW4En9g")]),
]),

("2021", [
  dict(studio="Scanline VFX", role="RIGGING DEVELOPER · CONTRACT",
       meta="May 2021 — Feb 2022 · Montreal, remote",
       body="In-house rigging tools across the slate — core asset classes, shape tools, crowd helpers. Converted custom nodes to vanilla Maya so external vendors could open the rigs. Git and PEP8, because other people have to read it.",
       tools=["MAYA","PYTHON","GIT"],
       shows=[S("The Batman", "assets/img/still/the-batman.jpg", "fWQrd6cwJ0A"),
              S("Andor", "assets/img/still/andor.jpg", "cKOegEuCcfw"),
              S("The Gray Man", "assets/img/still/gray-man.jpg", "BmllggGO4pM"),
              S("The Flash", "assets/img/still/the-flash.jpg", "r51cYVZWKdY"),
              S("Aquaman and the Lost Kingdom", "assets/img/still/aquaman-2.jpg", "FV3bqvOHRQo"),
              S("Slumberland", "assets/img/still/slumberland.jpg", "FBnkVJslRGo")]),
]),

("2020", [
  dict(studio="Bardel Entertainment", role="RIGGING ARTIST · CONTRACT",
       meta="May 2020 — May 2021 · Vancouver, remote",
       body="Body, facial and prop rigs on almost entirely custom productions. The scripts I wrote to survive the schedule became the team toolset and halved delivery times.",
       tools=["MAYA","PYTHON"],
       shows=[S("Diary of a Wimpy Kid", "assets/img/still/wimpy-kid.jpg", "a_DhEoPJHes"),
              S("Diary of a Wimpy Kid: Rodrick Rules", "assets/img/still/wimpy-rodrick.jpg", "lwKHUxX0YdU"),
              S("gen:LOCK Season 2", "assets/img/still/genlock-s2.jpg", "3FGAsgos8UE")]),
]),
]

STUDIES = [
 dict(year="2026 — NOW", title="Máster en Diseño Web Multidispositivo: UX/UI",
      school="ESDESIGN · Escuela Superior de Diseño de Barcelona",
      url="https://www.esdesignbarcelona.es/",
      note="Interface and experience design. The reason this site exists — riggers ship UIs every day and most of us never studied one.",
      accent="purple", chip="IN PROGRESS", live=True),
 dict(year="2026", title="Domina la IA con Gemini", school="Planeta Formación y Universidades",
      note="Applied AI for production work — where a model helps a pipeline and where it just makes noise.", accent="pink"),
 dict(year="2025", title="CS50x — Introduction to Computer Science", school="Harvard University · CS50",
      note="C, data structures, memory, SQL. Filled the gaps that self-taught Python leaves behind.", accent="cyan"),
 dict(year="2023", title="Google Project Management", school="Coursera · Google Career Certificates",
      note="Ran a rigging department before I had the vocabulary for it. This gave me the vocabulary.", accent="yellow"),
 dict(year="2020", title="Advanced Python for Artists", school="Alexander Richter",
      note="PEP8, structure, writing code another rigger can read a year later.", accent="green"),
 dict(year="2019 — 2020", title="Advanced 3D Character Rigging", school="Animum Creativity Advanced School",
      note="Mentors: Iker de los Mozos, Juan Carlos Lara, Ramiro Tell, Xenxo Álvarez. Where RdM Tools V2 came from.", accent="orange"),
 dict(year="2014 — 2019", title="BA, Digital Animation", school="Universidad LCI Veritas · Costa Rica",
      note="3D generalist degree. Teaching assistant for Maya production, rigging and geometry — the teaching stuck.", accent="pink"),
 dict(year="2014", title="Spain &amp; Costa Rica Diploma", school="Colegio Calasanz",
      note="Two curricula, two countries, one very confused timetable.", accent="muted"),
]


def plain(s):
    return html.escape(s.replace("&amp;", "&").replace("“", '"').replace("”", '"'), quote=True)


def slide(sh, i, active, prefix):
    cls = "media media--video" if sh["yt"] else "media"
    cls += " is-active" if active else ""
    yt = f' data-yt="{sh["yt"]}"' if sh["yt"] else ""
    sound = (
        '<button class="media__sound" type="button" aria-label="Play with sound">'
        '<span class="media__sound-ico" aria-hidden="true">►</span>'
        '<span class="media__sound-txt">SOUND</span></button>'
    ) if sh["yt"] else ""
    cap = sh["title"] + (" — trailer" if sh["yt"] else "")
    return (
        f'<figure class="{cls}"{yt} data-title="{plain(sh["title"])}" data-index="{i}">'
        f'<img class="media__poster" src="{prefix}{sh["img"]}" alt="{plain(sh["title"])}" loading="lazy" decoding="async">'
        f'{sound}<figcaption class="media__cap">{cap}</figcaption></figure>'
    )


def gallery(c, prefix=""):
    shows = c["shows"]
    slides = "".join(slide(sh, i, i == 0, prefix) for i, sh in enumerate(shows))
    if len(shows) == 1:
        return f'        <div class="gallery" data-gallery>{slides}</div>'
    dots = "".join(
        f'<button class="dot" type="button" role="tab" data-index="{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" '
        f'aria-label="{plain(sh["title"])}"></button>' for i, sh in enumerate(shows)
    )
    label = f'1 / {len(shows)} &nbsp; {shows[0]["title"].upper()}'
    return f"""        <div class="gallery" data-gallery>
          {slides}
          <div class="gallery__bar">
            <button class="gallery__arrow" type="button" data-prev aria-label="Previous show">&lsaquo;</button>
            <div class="dots" role="tablist" aria-label="Shows">{dots}</div>
            <button class="gallery__arrow" type="button" data-next aria-label="Next show">&rsaquo;</button>
            <p class="gallery__label" data-gallery-label>{label}</p>
          </div>
        </div>"""


def credit_block(c):
    chips = "".join(f'<li>{t}</li>' for t in c["tools"])
    titles = " · ".join(sh["title"] for sh in c["shows"])
    return f"""        <div class="credit">
          <p class="credit__role">{c['role']}</p>
          <h3 class="credit__studio">{c['studio']}</h3>
          <p class="credit__project">{titles}</p>
          <p class="credit__meta">{c['meta']}</p>
          <p class="credit__body">{c['body']}</p>
          <ul class="chips">{chips}</ul>
        </div>"""


FREELANCE_BAND = """      <aside class="band reveal">
        <div class="band__copy">
          <p class="band__kicker">ALSO FREELANCE · BLUETAPE RIGGING</p>
          <h3 class="band__title">A small rigging crew you can hire directly.</h3>
          <p class="band__note">Bluetape is a partner outfit — a tight crew of riggers I build and collaborate with. Body, facial, creature, crowds, props and the tooling around them. Every freelance enquiry goes through bluetaperigging.com.</p>
        </div>
        <a class="btn" href="https://bluetaperigging.com/" target="_blank" rel="noopener">HIRE BLUETAPE RIGGING <span aria-hidden="true">↗</span></a>
      </aside>"""


def head(title, desc, canonical, prefix="", og_image="assets/img/og.jpg"):
    ld = {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "Esteban Rodriguez",
      "url": "https://renderdemartes.com/",
      "jobTitle": "Technical Artist — Rigging & Python",
      "description": "Character rigger and rigging tools developer. Maya, Unreal, Unity. Creator of Mutant Tools.",
      "address": {"@type": "PostalAddress", "addressLocality": "Vancouver", "addressRegion": "BC", "addressCountry": "CA"},
      "sameAs": [LINKEDIN, "https://www.youtube.com/@renderdemartes6049", "https://mutanttools.com/"],
      "knowsAbout": ["Character rigging","Autodesk Maya","Unreal Engine","Python","Facial rigging","Pipeline tools"]
    }
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://renderdemartes.com/{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Esteban Rodriguez - technical artist, rigging and Python">
<meta property="og:site_name" content="Render de Martes">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}assets/img/favicon.ico" sizes="any">
<link rel="icon" href="{prefix}assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{prefix}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>"""


def nav(active, prefix=""):
    cv = f'<a href="{prefix}#cv" data-spy="cv"{" class=is-active" if active == "cv" else ""}>CV</a>' if prefix == "" \
        else f'<a href="{prefix or "/"}">CV</a>'
    ac_cls = ' class="is-active"' if active == "academic" else ""
    return f"""<a class="skip" href="#main">Skip to content</a>

<header class="nav">
  <a class="nav__mark" href="{prefix or '/'}">
    <img class="nav__logo" src="{prefix}assets/img/logo-mark.png" srcset="{prefix}assets/img/logo-mark@2x.png 2x" width="66" height="96" alt="" decoding="async">
    <span class="hide-sm">RENDER&nbsp;&nbsp;DE&nbsp;&nbsp;MARTES</span><span class="only-sm">RDM</span>
  </a>
  <nav class="nav__links" aria-label="Sections">
    {cv}
    <a href="/academic/"{ac_cls}>ACADEMIC</a>
    <a href="https://mutanttools.com/" target="_blank" rel="noopener"><span class="hide-sm">MUTANT </span>TOOLS <span aria-hidden="true">↗</span></a>
  </nav>
</header>"""


FOOT = """
  <a class="outbound" href="https://mutanttools.com/" target="_blank" rel="noopener">
    <span class="outbound__left">
      <span class="outbound__title">MUTANT TOOLS</span>
      <span class="outbound__note">Modular autorigger for Maya — body, face, quadrupeds, props.</span>
    </span>
    <span class="outbound__go">MUTANTTOOLS.COM <span aria-hidden="true">↗</span></span>
  </a>

<footer class="foot" id="contact">
  <div class="foot__contact">
    <p class="section__kicker">C O N T A C T</p>
    <h2 class="foot__title">Need a rigger?</h2>
    <p class="foot__lead">Freelance work goes through <a href="https://bluetaperigging.com/" target="_blank" rel="noopener">Bluetape Rigging</a>. For anything else, LinkedIn is the fastest way to reach me.</p>
    <p class="foot__btns">
      <a class="btn btn--cyan" href="__LINKEDIN__" target="_blank" rel="noopener">LINKEDIN PROFILE <span aria-hidden="true">↗</span></a>
      <a class="btn btn--ghost" href="https://bluetaperigging.com/" target="_blank" rel="noopener">BLUETAPE RIGGING <span aria-hidden="true">↗</span></a>
    </p>
  </div>
  <nav class="foot__services" aria-label="Services">
    <p class="foot__colhead">SERVICES</p>
    <a href="/hire-a-freelance-character-rigger/">HIRE A FREELANCE RIGGER</a>
    <a href="/maya-rigging-services/">MAYA RIGGING</a>
    <a href="/unreal-engine-character-rigging/">UNREAL RIGGING</a>
    <a href="/facial-rigging-services/">FACIAL RIGGING</a>
    <a href="/rigging-outsourcing-for-studios/">RIGGING FOR STUDIOS</a>
  </nav>
  <nav class="foot__links" aria-label="Elsewhere">
    <a href="__LINKEDIN__" target="_blank" rel="noopener">LINKEDIN ↗</a>
    <a href="https://www.youtube.com/@renderdemartes6049/videos" target="_blank" rel="noopener">YOUTUBE ↗</a>
    <a href="https://mutanttools.com/" target="_blank" rel="noopener">MUTANTTOOLS.COM ↗</a>
    <a href="/academic/">ACADEMIC</a>
    <a href="/creature-rigging/">WORKFLOWS</a>
  </nav>
  <p class="foot__fine">© 2026 Esteban Rodriguez · Costa Rica, working remotely worldwide · built with Claude — who has time to build a website while building rigs?</p>
</footer>

<script src="__PREFIX__assets/js/site.js" defer></script>
</body>
</html>
""".replace("__LINKEDIN__", LINKEDIN)


def build_home():
    rows = []
    for year, items in CREDITS:
        rows.append(f"""      <div class="yearline reveal">
        <span class="yearline__dash"></span><span class="yearline__num">{year}</span><span class="yearline__dash"></span>
      </div>""")
        for i, c in enumerate(items):
            flip = " row--flip" if i % 2 else ""
            rows.append(f"""      <article class="row{flip} reveal">
{gallery(c)}
{credit_block(c)}
      </article>""")
            if c["studio"] == "The Coalition":
                rows.append(FREELANCE_BAND)
    credits_html = "\n".join(rows)

    body = f"""
<main id="main">

  <section class="hero">
    <p class="hero__eyebrow">TECHNICAL ARTIST — RIGGING &amp; PYTHON</p>
    <h1 class="hero__h1">ESTEBAN<br>RODRIGUEZ</h1>
    <p class="hero__lead">I build rigs that animators actually like, and the tools that build the rigs. 600+ characters, 1000+ assets, Maya to Unreal — from Costa Rica to Vancouver, working remotely.</p>
    <p class="hero__status"><span class="dot-live"></span>AVAILABLE · REMOTE · OPEN TO RELOCATION WITH SPONSORSHIP</p>
    <ul class="stats">
      <li><b>08</b><span>YEARS RIGGING</span></li>
      <li><b>600+</b><span>CHARACTERS</span></li>
      <li><b>1000+</b><span>ASSETS</span></li>
      <li><b>30+</b><span>SHIPPED PROJECTS</span></li>
    </ul>
    <p class="hero__scroll" aria-hidden="true">SCROLL&nbsp;&nbsp;&nbsp;↓</p>
  </section>

  <section id="cv" class="section">
{credits_html}

      <div class="close reveal">
        <p class="section__kicker">T H E &nbsp; R E S T &nbsp; O F &nbsp; I T</p>
        <h2 class="close__title">Thirty more credits, back to 2018.</h2>
        <p class="close__lead">Fair Play Labs, Bluetape, Estudio Shout, Lasalapost, Relish, Martestudio, Artella and the rest — with dates, tools and references — live on LinkedIn.</p>
        <p><a class="btn btn--cyan" href="{LINKEDIN}" target="_blank" rel="noopener">SEE THE FULL CV ON LINKEDIN <span aria-hidden="true">↗</span></a></p>
      </div>
  </section>

</main>
"""
    doc = head(
        "Esteban Rodriguez — Rigger &amp; Rigging Tools Developer | Render de Martes",
        "Character rigger and tools developer. Gears of War: E-Day, Marvel&#39;s What If…?, The Batman, Andor. Creator of Mutant Tools for Maya.",
        "https://renderdemartes.com/",
    ) + "\n" + nav("cv") + body + FOOT.replace("__PREFIX__", "")
    write(os.path.join(ROOT, "index.html"), doc)


def build_academic():
    items = "\n".join(
        f"""      <li class="study reveal{' study--live' if s.get('live') else ''}" data-accent="{s['accent']}">
        <span class="study__year">{s['year']}</span>
        <span class="study__node" aria-hidden="true"></span>
        <div class="study__body">
          <h3 class="study__title">{s['title']}{f'<span class="tag">{s["chip"]}</span>' if s.get('chip') else ''}</h3>
          <p class="study__school">{f'<a href="{s["url"]}" target="_blank" rel="noopener">{s["school"]}</a>' if s.get('url') else s['school']}</p>
          <p class="study__note">{s['note']}</p>
        </div>
      </li>""" for s in STUDIES)

    body = f"""
<main id="main">
  <section class="section section--page">
    <header class="section__head reveal">
      <p class="section__kicker">0 2 &nbsp;/&nbsp; A C A D E M I C</p>
      <h1 class="section__title">Still learning, in public.</h1>
      <p class="section__lead">Newest first. Rigging got me in, code kept me here, design is what I am chewing on now.</p>
    </header>
    <ol class="timeline">
{items}
    </ol>
    <p class="back reveal"><a class="btn btn--ghost" href="/">← BACK TO THE CV</a></p>
  </section>
</main>
"""
    doc = head(
        "Academic — Esteban Rodriguez | Render de Martes",
        "Degrees, certificates and courses: UX/UI master at ESDESIGN, CS50x, Google Project Management, Animum advanced rigging, BA in Digital Animation.",
        "https://renderdemartes.com/academic/",
        prefix="/",
    ) + "\n" + nav("academic", prefix="/") + body + FOOT.replace("__PREFIX__", "/")
    write(os.path.join(ROOT, "academic", "index.html"), doc)


def write(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
    print("wrote", path)


if __name__ == "__main__":
    build_home()
    build_academic()
    studios = sum(len(v) for _, v in CREDITS)
    shows = sum(len(c["shows"]) for _, v in CREDITS for c in v)
    print(f"{studios} studios, {shows} shows, {len(STUDIES)} academic entries")
