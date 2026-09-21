# -*- coding: utf-8 -*-
"""Rebuilds the workflow (tutorial) pages in the 2026 design.

Content comes from tutorials.json (extracted from the WordPress archive);
heavy GIFs render as click-to-play posters so a page does not pull 39 MB.
"""
import html, io, json, os, re, textwrap
from gen import head, nav, FOOT, write, LINKEDIN, ROOT

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCKS = json.load(io.open(os.path.join(HERE, "tutorials.json"), encoding="utf-8"))
POSTERS = json.load(io.open(os.path.join(HERE, "posters.json"), encoding="utf-8"))
VIDEOS = json.load(io.open(os.path.join(HERE, "videos.json"), encoding="utf-8"))

META = {
 "the-king": dict(
   title="The King — a Maya rig taken into Unreal Engine",
   seo="The King — Maya to Unreal Rigging Case Study | Render de Martes",
   desc="Case study: a ZBrush sculpt rigged with Mutant Tools, skinned in ngSkinTools, tested with HumanIK mocap and imported into Unreal Engine with dynamics.",
   lede="A full case study — a ZBrush sculpt taken through Mutant Tools, skinned, tested with mocap, and imported into Unreal with dynamics.",
   chips=["MAYA","MUTANT TOOLS","NGSKINTOOLS","UNREAL","HUMANIK"]),
 "creature-rigging": dict(
   title="Creature rigging — quadrupeds, wings and split-geo skinning",
   seo="Creature Rigging in Maya — Quadruped &amp; Wing Setup | Render de Martes",
   desc="Quadruped rigging in Maya: template guides block by block, wing feather systems, and the split/merge skinning technique that keeps quadruped weights sane.",
   lede="The quadruped template block by block, a wing system with scapulars, secondaries and primaries, and the split-geo skinning technique that keeps weights editable.",
   chips=["MAYA","MUTANT TOOLS","NGSKINTOOLS","QUADRUPED"]),
 "face-rig-study": dict(
   title="Face rig study — a layered facial system",
   seo="Facial Rigging Study — Layered Face Rig in Maya | Render de Martes",
   desc="How a layered facial rig is built: skull locals, eyelids on the real eye pivot, orbicularis wires, lips around the teeth, brows, cheeks and correctives.",
   lede="The face rigged in layers — skull locals, eyelids, orbicularis, lips, brows, cheeks — each its own system, combined at the end so a note on the mouth never means rebuilding the eyes.",
   chips=["MAYA","MUTANT TOOLS","NGSKINTOOLS","SHAPES"]),
 "how-to-rig-a-car": dict(
   title="How to rig a car",
   seo="How to Rig a Car in Maya — Chassis, Wheels, Doors | Render de Martes",
   desc="Rigging a car in Maya block by block: COG placement, chassis, trunks, doors, mirrors, wheels with auto-roll and the cluster trick for fast guide placement.",
   lede="A simple but complete vehicle rig an animator will actually enjoy: chassis, trunks, doors, mirrors and wheels that roll on their own.",
   chips=["MAYA","MUTANT TOOLS","VEHICLE"]),
 "prop-rig": dict(
   title="Simple prop rig",
   seo="Simple Prop Rig in Maya — Base, COG, Bind, Squash | Render de Martes",
   desc="The short one: a prop rig in Maya from template to bind joint, plus a squash and stretch block for the bounce.",
   lede="The short one. Template, global and mover controls, a bind joint, a cleanup pass for the animation department, and a squash block for the bounce.",
   chips=["MAYA","MUTANT TOOLS","PROPS"]),
 "rig-with-mocap-packs": dict(
   title="Rig with mocap packs",
   seo="Game-Ready Rigging with Mocap Packs — HumanIK &amp; Mixamo | Render de Martes",
   desc="Build a game-ready rig in Maya and drive it with mocap: single joint chain skinning, HumanIK custom mapping, Mixamo retargeting, and fixing feet and hands after the bake.",
   lede="A game-ready rig, then mocap on top of it: single-chain skinning, HumanIK custom mapping, retargeting from Mixamo, and the cleanup every capture needs afterwards.",
   chips=["MAYA","HUMANIK","MIXAMO","GAME READY"]),
 "qt-designer-basics": dict(
   title="Qt Designer basics for Maya tools",
   seo="Qt Designer for Maya — Build a Python Tool UI | Render de Martes",
   desc="Build a Maya tool UI with Qt Designer and PySide: widget setup, loading the .ui in Maya, wiring buttons to Python commands, and keeping the window docked and sane.",
   lede="Build a Maya tool UI that does not look like 2004: a widget in Qt Designer, loaded into Maya with PySide, wired to Python commands you can actually maintain.",
   chips=["QT DESIGNER","PYSIDE","PYTHON","MAYA"]),
}

ORDER = ["creature-rigging", "face-rig-study", "how-to-rig-a-car",
         "prop-rig", "rig-with-mocap-packs", "qt-designer-basics"]

CARD_NOTE = {
 "the-king": "Mutant Tools rig, dynamics and mocap, taken into Unreal",
 "creature-rigging": "Quadruped template, wings, split-geo skinning",
 "face-rig-study": "Layered facial systems, region by region",
 "how-to-rig-a-car": "Chassis, wheels, doors, a drivable rig",
 "prop-rig": "Base, COG, bind, squash and stretch",
 "rig-with-mocap-packs": "Game-ready rig plus HumanIK retargeting",
 "qt-designer-basics": "A Maya tool UI in Qt Designer and PySide",
}


def esc(t):
    return html.escape(t, quote=False)


def media(bl):
    # pages live at /<slug>/, so asset paths must be root-relative
    key = bl["src"].lstrip("/")
    src = "/" + key
    alt = esc(bl.get("alt") or "")
    cap = f'<figcaption>{alt}</figcaption>' if alt else ''

    v = VIDEOS.get(key)
    if v:   # former GIF, now H.264 — plays muted on loop while it is on screen
        return (
            f'<figure class="wf-media wf-media--video">'
            f'<video class="wf-video" poster="/{v["poster"]}" width="{v["w"]}" height="{v["h"]}" '
            f'muted loop playsinline preload="none" data-autoplay aria-label="{alt or "Rigging clip"}">'
            f'<source src="/{v["mp4"]}" type="video/mp4"></video>'
            f'{cap}</figure>')

    return (f'<figure class="wf-media">'
            f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async">'
            f'{cap}</figure>')


def render(slug):
    blocks = BLOCKS[slug]
    meta = META[slug]
    out, n = [], 0
    skipped_first_head = False
    for bl in blocks:
        t = bl["t"]
        if t == "img":
            out.append(media(bl))
        elif t in ("h1", "h2"):
            text = esc(bl["text"])
            if not skipped_first_head:
                skipped_first_head = True          # page title already says it
                continue
            n += 1
            out.append(f'<h2 class="wf-h2"><span class="wf-h2__n">{n:02d}</span>{text}</h2>')
        elif t == "h3":
            out.append(f'<h3 class="wf-h3">{esc(bl["text"])}</h3>')
        elif t == "h4":
            out.append(f'<h4 class="wf-h4">{esc(bl["text"])}</h4>')
        elif t == "p":
            out.append(f'<p class="wf-p">{esc(bl["text"])}</p>')
        elif t == "li":
            out.append(f'<p class="wf-li">{esc(bl["text"])}</p>')
        elif t == "code":
            code = textwrap.dedent(bl["text"].expandtabs(4)).strip()
            out.append(f'<pre class="wf-code"><code>{esc(code)}</code></pre>')
    return "\n      ".join(out)


def cards(slug):
    others = [s for s in ORDER if s != slug][:3]
    return "".join(
        f'<a class="wf-card" href="/{s}/"><span class="wf-card__title">{META[s]["title"].split("—")[0].strip()}</span>'
        f'<span class="wf-card__note">{CARD_NOTE[s]}</span><span class="wf-card__go">OPEN →</span></a>'
        for s in others)


def build(slug):
    meta = META[slug]
    i = ORDER.index(slug) + 1
    canonical = f"https://renderdemartes.com/{slug}/"
    ld = {
      "@context": "https://schema.org", "@type": "HowTo",
      "name": meta["title"], "description": meta["desc"].replace("&amp;", "&"),
      "url": canonical,
      "author": {"@type": "Person", "name": "Esteban Rodriguez", "url": "https://renderdemartes.com/"},
      "step": [{"@type": "HowToStep", "name": re.sub("<[^>]+>", "", s)}
               for s in re.findall(r'<h2 class="wf-h2">(.*?)</h2>', render(slug))][:12],
    }
    body = f"""
<main id="main">
  <article class="wf">
    <header class="wf__head">
      <p class="section__kicker">W O R K F L O W &nbsp; · &nbsp; {i:02d} &nbsp; O F &nbsp; {len(ORDER):02d}</p>
      <h1 class="wf__h1">{meta['title']}</h1>
      <p class="wf__lede">{meta['lede']}</p>
      <ul class="chips">{''.join(f'<li>{c}</li>' for c in meta['chips'])}</ul>
    </header>

    <div class="wf__body">
      {render(slug)}
    </div>

    <section class="found found--wf">
      <p class="found__kicker">B U I L T &nbsp; T H I S &nbsp; W A Y &nbsp; F O R &nbsp; Y O U ?</p>
      <h2 class="found__title">I do this on shows, not just on my own time.</h2>
      <p class="found__note">Every workflow on this site is the one I use in production. If you want it applied to your characters instead of read about, that is the job.</p>
      <p class="found__row">
        <a class="btn" href="https://bluetaperigging.com/" target="_blank" rel="noopener">HIRE BLUETAPE RIGGING <span aria-hidden="true">↗</span></a>
        <a class="btn btn--ghost" href="/hire-a-freelance-character-rigger/">RIGGING SERVICES →</a>
      </p>
    </section>

    <nav class="wf-more" aria-label="More workflows">
      <p class="section__kicker">M O R E &nbsp; W O R K F L O W S</p>
      <div class="wf-more__grid">{cards(slug)}</div>
    </nav>
  </article>
</main>
"""
    doc = head(meta["seo"], meta["desc"], canonical, prefix="/").replace(
        "</head>", f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n</head>')
    doc += "\n" + nav("", prefix="/") + body + FOOT.replace("__PREFIX__", "/")
    write(os.path.join(ROOT, slug, "index.html"), doc)


def sitemap():
    from seo import PAGES as SEO_PAGES
    urls = [("https://renderdemartes.com/", "1.0"),
            ("https://renderdemartes.com/academic/", "0.8")]
    urls += [(f'https://renderdemartes.com/{p["slug"]}/', "0.8") for p in SEO_PAGES]
    urls += [(f"https://renderdemartes.com/{s}/", "0.7") for s in ORDER]
    rows = "\n".join(f'  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{p}</priority></url>'
                     for u, p in urls)
    write(os.path.join(ROOT, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '\n</urlset>\n')


if __name__ == "__main__":
    for s in ORDER:
        build(s)
    sitemap()
    print(f"{len(ORDER)} workflow pages + sitemap")
