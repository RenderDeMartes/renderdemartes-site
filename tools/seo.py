# -*- coding: utf-8 -*-
"""SEO landing pages for renderdemartes.com.

Not linked from the nav — they exist to be found in search, and they cross-link
to each other so they are not orphans. Each one is written for a different query
and shares no copy with the others.
"""
import io, os, json
from gen import head, nav, FOOT, write, LINKEDIN, ROOT

MAIL_BTN = ('<a class="btn" href="%s" target="_blank" rel="noopener">'
            'HIRE BLUETAPE RIGGING <span aria-hidden="true">↗</span></a>') % 'https://bluetaperigging.com/'

PAGES = [
dict(
  slug="hire-a-freelance-character-rigger",
  title="Hire a Freelance Character Rigger — Maya &amp; Unreal | Render de Martes",
  desc="Freelance character rigger for film, series and games. Body, facial, creature and prop rigs in Maya and Unreal. Credits on Gears of War: E-Day, Marvel&#39;s What If…?, The Batman.",
  kicker="F R E E L A N C E &nbsp; S E R V I C E",
  h1="Hire a freelance<br>character rigger.",
  lede="Maya and Unreal rigs for film, series and games — body, facial, creature, props and the pipeline tooling around them. Eight years, 600+ characters, 1000+ assets, and credits on Gears of War: E-Day, Marvel’s What If…? and The Batman.",
  intro=[
    "Most rigging problems are not rigging problems. They are a model that fights the deformation, a naming convention nobody wrote down, or a rig built for a turntable and handed to an animator with a deadline. I have been on all three sides of that — artist, developer, and the supervisor who has to explain the delay — so the first thing I do on a job is find which one you have.",
    "What you get back is a rig an animator can pick up without a tutorial, documentation short enough that someone reads it, and tooling that makes the second character cheaper than the first.",
  ],
  cols=[
    ("BODY RIGS", "FK/IK with space switching, twist chains, bendy limbs, foot rolls that behave on uneven ground — built so nobody has to open the outliner to animate."),
    ("FACIAL RIGS", "Joint, blendshape or hybrid, chosen by where the rig has to run rather than by fashion, and adapted to the joint budget your engine actually allows."),
    ("PIPELINE TOOLS", "Python and PySide: autorig blocks, save and load of controllers and skins, batch fixes across an asset library, validation that runs before publish instead of after."),
  ],
  steps=[
    ("01", "Model in", "You send the model, the reference and the engine target. I flag topology that will fight the deformation before anything is built — cheaper now than after skinning."),
    ("02", "Blocks and guides", "Guides placed with Mutant Tools, my own modular autorigger, so a change to the skeleton is a rebuild rather than a restart. Controllers and skins survive it."),
    ("03", "Skin and shapes", "ngSkinTools layers, correctives where they earn their weight, tested against real animation or mocap instead of a T-pose and a prayer."),
    ("04", "Handoff", "Rig, picker, short docs and a screen recording of how it is meant to be used. Fixes stay free for the run of the show."),
  ],
  faq=[
    ("What does a character rig cost?",
     "It scales with the deformation, not the character count. A game-ready biped on an existing template is days; a hero facial rig with correctives is weeks. Send the model and the shot list and you get a fixed number for the job, not an hourly rate card."),
    ("Can you match our in-house naming and pipeline?",
     "Yes, and that is most of the job. I have shipped into Maya, Unreal and Unity pipelines at four studios, each with its own conventions, and written the conversion tooling for the times two of them disagreed."),
    ("Do you take a whole show, or single assets?",
     "Both. A single hero character, a crowd batch of 300, or supervising a department for a season — all three have happened, the last one for three years at Stellar Creative Lab."),
    ("Who owns the rig and the tools?",
     "You own every rig and every tool written for your production. Mutant Tools stays mine; everything it builds is yours, with no runtime dependency on it."),
    ("How fast can you start?",
     "Usually within a week, sometimes the same day for a fix or a test. I am in Costa Rica and work remotely across North American and European hours."),
  ],
  related_note="Looking for something more specific?",
),

dict(
  slug="maya-rigging-services",
  title="Maya Rigging Services — Autorig, Skinning, Tools | Render de Martes",
  desc="Maya character rigging: modular autorig, ngSkinTools skinning, SHAPES correctives, Python and PySide tooling. Freelance rigger with film, series and AAA game credits.",
  kicker="M A Y A &nbsp; R I G G I N G",
  h1="Maya rigging,<br>from guides to handoff.",
  lede="Everything here is built in Maya, with Python that follows PEP8 and a scene you can hand to another rigger without an apology. Autorig, skinning, correctives, publish validation, and the tools to repeat it across a library.",
  intro=[
    "Maya rewards riggers who keep their scenes boring. No stray constraints, no duplicate shape nodes, no script node that only works on the machine it was written on. The rigs I deliver are built from modular blocks, so the skeleton can change in week six without the skinning going in the bin.",
    "That modularity is not a pitch — it is a product. <a href="https://mutanttools.com/maya-auto-rigger/" target="_blank" rel="noopener">Mutant Tools</a> is the autorigger I wrote, free and open source, and it is the same one your show would be built with.",
  ],
  cols=[
    ("AUTORIG BLOCKS", "Biped, quadruped, wings, props, vehicles. Place guides, hit build, paint skins. Rebuild after a model change without losing controllers or weights."),
    ("SKINNING", "ngSkinTools layers with the split-and-merge technique for quadrupeds, SHAPES for correctives, and an influence budget that respects wherever the asset has to run."),
    ("SCENE HYGIENE", "Referencing that survives a publish, namespaces that do not collide, outliner cleanup, and validation that catches the broken thing before the animator does."),
  ],
  steps=[
    ("01", "Template", "Pick the closest block template — human, quadruped, prop, vehicle — or build a new one. The template is data, so it is reusable across the whole asset list."),
    ("02", "Guides", "Place the guides. Zombinator wraps a base mesh onto your topology and gets placement to roughly 90% before anyone touches a joint by hand."),
    ("03", "Build and skin", "Build, paint hard first, then layer and smooth. Corrective shapes only where the deformation actually breaks."),
    ("04", "Package", "Publish-ready file, picker UI, and the Python entry point if your pipeline needs to build the rig on a farm instead of a workstation."),
  ],
  faq=[
    ("Which Maya versions do you support?",
     "2020 through the current release. Tools are written against vanilla Maya nodes wherever possible, so a vendor without your plugin set can still open the rig — I did exactly that conversion work at Scanline VFX."),
    ("Do you use mGear, Advanced Skeleton or your own system?",
     "All three, depending on what the studio already runs. I have shipped mGear work at Fair Play Labs and my own Mutant Tools everywhere else. The right answer is whichever one your team can maintain after I leave."),
    ("Can you fix or finish someone else’s rig?",
     "Often, yes. Send the file — I will tell you honestly whether repairing it costs less than rebuilding it, and I have been wrong in both directions often enough to check first."),
    ("Do you write tools as well as rigs?",
     "That is half the work. Save/load of rig components, crowd helpers, shape libraries, batch fixes, Qt UIs that artists actually use — most of it started as a script to get my own week back."),
  ],
  related_note="Other things I get asked for:",
),

dict(
  slug="unreal-engine-character-rigging",
  title="Unreal Engine Character Rigging — Control Rig &amp; Game-Ready Skinning | Render de Martes",
  desc="Game-ready character rigging for Unreal Engine: joint budgets, twist chains, Control Rig, IK Retargeter, Animation Blueprints and rod dynamics. AAA credits including Gears of War: E-Day.",
  kicker="U N R E A L &nbsp; E N G I N E",
  h1="Rigs that survive<br>the engine.",
  lede="Maya-to-Unreal character work with the constraints in mind from the first joint: influence limits, LODs, twist chains that do not collapse, Control Rig setups animators can actually pose, and dynamics that behave at runtime.",
  intro=[
    "A film rig fails in the engine for boring reasons. Too many influences per vertex. A skeleton hierarchy the retargeter cannot read. Dynamics that look perfect at 24fps and explode when the player sprints. Game rigging is the discipline of deciding what to give up, and where.",
    "Most recently that was Gears of War: E-Day at The Coalition — body and prop rigs for AAA characters and skins, rod dynamics, Control Rig and Animation Blueprints, plus the wrapping tools and Confluence docs so the next rigger did not start from zero.",
  ],
  cols=[
    ("GAME-READY SKINNING", "Single bind hierarchy, influence caps that match the engine setting rather than the wishlist, LOD-aware weighting, and twist joints that keep the forearm readable."),
    ("CONTROL RIG", "In-engine rigs for animators and cinematics: pose-friendly controls, IK setups, and forward solves that do not fight the imported skeleton."),
    ("DYNAMICS &amp; BLUEPRINTS", "Rod dynamics for hair, cloth, straps and antennae; Animation Blueprint hookups; the parts where the rig stops being a Maya problem."),
  ],
  steps=[
    ("01", "Target first", "Engine version, skeleton standard, influence limit, LOD plan. Everything downstream is decided here, and getting it in writing saves the reskin."),
    ("02", "Maya build", "Rig built on a game preset — one clean joint chain for the engine, the animation rig layered above it, never the other way around."),
    ("03", "Export and verify", "FBX out, skeleton in, retargeting checked against real locomotion, not an idle. Dynamics tuned at the frame rate the game actually runs."),
    ("04", "In-engine polish", "Control Rig, Anim BP wiring, and documentation in whatever your team reads — Confluence, Notion, or a video if nobody reads anything."),
  ],
  faq=[
    ("Can you work to the Epic skeleton, or a custom one?",
     "Either. Epic’s skeleton buys you the Marketplace and the retargeter; a custom one buys you anatomy. If you are early enough to choose, that is a conversation worth twenty minutes before anyone rigs anything."),
    ("What influence limit do you build to?",
     "Whatever your project sets — commonly four or eight. The limit is not the hard part; keeping the silhouette readable at the limit is, and that is what the layered skinning workflow is for."),
    ("Do you handle Unity as well?",
     "Yes. Game-ready rigs at Fair Play Labs shipped to Unity for Nicktoons and SpeedRunners 2, so the same constraints apply with different button names."),
    ("Can you rig for mocap and cleanup?",
     "Yes — HumanIK setups, retargeting from Mixamo or Rokoko for tests, and rigs that keep an FK fallback so an animator can fix what the capture got wrong."),
  ],
  related_note="Related services:",
),

dict(
  slug="facial-rigging-services",
  title="Facial Rigging Services — Joint, Blendshape and Hybrid Face Rigs | Render de Martes",
  desc="Facial rigging for film, series and games: layered joint systems, blendshape correctives, phoneme sets and engine-budget face rigs that still deform in close-up.",
  kicker="F A C I A L &nbsp; R I G G I N G",
  h1="Faces that hold up<br>in close-up.",
  lede="Layered facial rigs — skull locals, orbiculars, lips, brows, cheeks — built as independent systems that combine, so a note on the mouth does not mean rebuilding the eyes.",
  intro=[
    "A face rig is not one rig. It is a stack of small systems sharing a skull, and the quality of the result comes from how honestly each layer respects anatomy: where a muscle starts, where it ends, what it drags with it, and the fact that the skull underneath does not move.",
    "Built that way, the face survives revision. The lower and upper skull stay local to each other, every region hangs off the right parent, and the animator gets controls that behave like the muscles they are named after.",
  ],
  cols=[
    ("LAYERED SYSTEMS", "Skull locals, eyelids rotating on the real eye pivot, an orbicularis wire that moves lid skin without dragging the brow, lips that rotate around the teeth."),
    ("SHAPES &amp; CORRECTIVES", "SHAPES-driven correctives where joints alone go flat, sculpted on the pose that breaks rather than on a checklist of 52."),
    ("PHONEMES &amp; EXPRESSIONS", "Phoneme sets and expression libraries saved as data, so the same face can be re-used across a season without re-sculpting."),
  ],
  steps=[
    ("01", "Read the face", "Topology check on the lips, lids and nasolabial loops. A face with the wrong edge flow costs more in correctives than it saves in modelling time."),
    ("02", "Guides by region", "Each region placed separately — eyes, lids, orbiculars, lips, commissures, brows, cheeks, jaw — with pivots where the anatomy says, not where the mesh centre is."),
    ("03", "Build and paint", "Build, then paint each region against its own local geometry, so weights stay editable region by region instead of as one impossible blob."),
    ("04", "Test with acting", "Tested on real dialogue and extreme poses. If the smile only works at 100% it does not work."),
  ],
  faq=[
    ("Joints or blendshapes?",
     "Joints for anything that has to run in an engine or be re-used at scale, blendshapes for correctives and hero close-ups, and a hybrid on most shows. The deciding factor is where the face runs and who has to animate it."),
    ("Can a film-quality face rig work in a game engine?",
     "A version of it can. The workflow I use adapts facial rigs to an engine joint budget while keeping the deformation — that was the Fair Play Labs brief exactly, human and animal faces at game weight."),
    ("Do you support ARKit or FACS-style blendshape sets?",
     "Yes, when the pipeline needs them for capture. They are a delivery format, not a rigging philosophy — the underlying rig still has to deform properly before anything maps onto it."),
    ("How long does a hero face take?",
     "Typically two to four weeks including correctives and revisions, faster on a second character that shares topology, because then the guide placement is mostly automated."),
  ],
  related_note="Related services:",
),

dict(
  slug="rigging-outsourcing-for-studios",
  title="Rigging Outsourcing for Studios — Overflow, Crowds &amp; Supervision | Render de Martes",
  desc="Outsourced rigging for animation and game studios: overflow capacity, crowd batches, department supervision and pipeline tooling, with a small crew of riggers behind it.",
  kicker="F O R &nbsp; S T U D I O S",
  h1="Rigging capacity,<br>without the headcount.",
  lede="A small crew of riggers for overflow, crowd batches and whole-department work — with someone who has run a rigging department for three years deciding how the work is split.",
  intro=[
    "Studios rarely need one rigger. They need six weeks of four riggers, starting the week after next, on a show that has already changed twice. That is the shape of the problem I work on with Bluetape — a partner outfit and a tight crew of riggers I build and collaborate with, so the capacity is real rather than a promise from one freelancer with a calendar.",
    "The supervision side is not theoretical either: at Stellar Creative Lab I ran the rigging department across five Marvel and Sony shows, 1000+ assets, 600+ characters, including a full rebuild of the rigging system mid-production.",
  ],
  cols=[
    ("OVERFLOW", "A batch of characters, props or crowds delivered to your conventions and your publish process, so the work lands in the pipeline rather than next to it."),
    ("CROWDS AT SCALE", "Crowd rigs handled at 300+ assets, with the batch tooling and validation that makes that number survivable."),
    ("SUPERVISION", "Department structure, review cadence, and the unglamorous part: deciding what gets rebuilt and what ships as-is."),
  ],
  steps=[
    ("01", "Scope and conventions", "Asset list, deadlines, naming, publish path, review tooling. We adapt to yours — every studio I have worked in was convinced theirs was the strange one."),
    ("02", "Pilot asset", "One asset, built and reviewed end to end, before anyone scales. It catches the mismatch that would otherwise repeat 300 times."),
    ("03", "Batch delivery", "Work split across the crew with a single point of contact, weekly builds, and a status you can forward to production without editing it."),
    ("04", "Wrap", "Tools, docs and the rebuilt templates stay with you, so next season starts from where this one ended."),
  ],
  faq=[
    ("How big is the crew?",
     "Small on purpose — riggers I have worked with and would hire again, scaled per project. You get a named team, not a body-shop roster."),
    ("Can you work under NDA?",
     "Yes, routinely. Most of the game work is under NDA, which is why parts of this site show a still and no trailer."),
    ("Can you supervise our in-house team instead of replacing it?",
     "Yes, and it is often the better buy. Building the templates and the review structure so your own riggers move faster outlasts any batch of delivered assets."),
    ("What time zones do you cover?",
     "Costa Rica as a base, with a history of shipping to Vancouver, Montreal and European teams. Overlap with both North America and Europe is workable in the same day."),
  ],
  related_note="Related services:",
),
]


def cta_block(subject):
    return f"""      <section class="found">
        <p class="found__kicker">S O &nbsp; T H E &nbsp; S E O &nbsp; W O R K E D</p>
        <h2 class="found__title">You searched, you landed here. That was the whole plan.</h2>
        <p class="found__note">This page was written and built with AI, by a rigger, in an afternoon between rigs — which is roughly the point: I use the tools that shorten the boring part, on websites and on pipelines. If that instinct is useful on your show, or you are about to post a rigging job, skip the posting and email me.</p>
        <p class="found__row">
          {MAIL_BTN.format(subject=subject)}
          <span class="found__aside">or send me the job post — I will tell you straight if I am the wrong rigger for it.</span>
        </p>
      </section>"""


def related(current):
    others = [p for p in PAGES if p["slug"] != current["slug"]]
    links = "".join(
        f'<a href="/{p["slug"]}/">{p["slug"].replace("-", " ").upper()} →</a>'
        for p in others)
    return f"""      <nav class="related" aria-label="Related services">
        <p class="related__note">{current["related_note"]}</p>
        <div class="related__links">{links}</div>
      </nav>"""


def build(p):
    canonical = f'https://renderdemartes.com/{p["slug"]}/'
    cols = "".join(
        f'<div class="col"><h3 class="col__title">{t}</h3><p class="col__note">{n}</p></div>'
        for t, n in p["cols"])
    steps = "".join(
        f'<li class="step"><span class="step__n">{n}</span><div class="step__body">'
        f'<h3 class="step__title">{t}</h3><p class="step__note">{d}</p></div></li>'
        for n, t, d in p["steps"])
    intro = "".join(f'<p>{par}</p>' for par in p["intro"])
    faq = "".join(
        f'<div class="q"><h3 class="q__q">{q}</h3><p class="q__a">{a}</p></div>'
        for q, a in p["faq"])

    ld = [
      {"@context": "https://schema.org", "@type": "Service",
       "name": p["title"].split("—")[0].strip().replace("&amp;", "&"),
       "serviceType": "Character rigging",
       "provider": {"@type": "Person", "name": "Esteban Rodriguez", "url": "https://renderdemartes.com/",
                    "sameAs": [LINKEDIN]},
       "areaServed": "Worldwide",
       "url": canonical,
       "description": p["desc"].replace("&#39;", "'").replace("&amp;", "&")},
      {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q.replace("&amp;", "&"),
                       "acceptedAnswer": {"@type": "Answer", "text": a.replace("&amp;", "&")}}
                      for q, a in p["faq"]]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList",
       "itemListElement": [
         {"@type": "ListItem", "position": 1, "name": "Render de Martes", "item": "https://renderdemartes.com/"},
         {"@type": "ListItem", "position": 2, "name": p["slug"].replace("-", " ").title(), "item": canonical}]},
    ]

    body = f"""
<main id="main">
  <article class="seo">
    <header class="seo__head">
      <p class="section__kicker">{p['kicker']}</p>
      <h1 class="seo__h1">{p['h1']}</h1>
      <p class="seo__lede">{p['lede']}</p>
      <p class="seo__cta">
        {MAIL_BTN.format(subject=p['slug'].replace('-', ' ').title())}
        <a class="btn btn--ghost" href="{LINKEDIN}" target="_blank" rel="noopener">LINKEDIN <span aria-hidden="true">↗</span></a>
      </p>
    </header>

    <div class="prose">{intro}</div>

    <div class="cols">{cols}</div>

    <section class="steps-wrap">
      <p class="section__kicker">H O W &nbsp; I T &nbsp; W O R K S</p>
      <ol class="steps">{steps}</ol>
    </section>

    <section class="proof" aria-label="Selected credits">
      <div><b>GEARS OF WAR: E-DAY</b><span>The Coalition · Microsoft</span></div>
      <div><b>WHAT IF…? S2 · S3</b><span>Marvel · Stellar Creative Lab</span></div>
      <div><b>THE BATMAN · ANDOR</b><span>Scanline VFX</span></div>
      <div><b>WIMPY KID · GEN:LOCK</b><span>Bardel Entertainment</span></div>
    </section>

    <section class="faq">
      <p class="section__kicker">F A Q</p>
      {faq}
    </section>

{cta_block(p['slug'].replace('-', ' ').title())}

{related(p)}
  </article>
</main>
"""
    scripts = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    doc = head(p["title"], p["desc"], canonical, prefix="/").replace("</head>", scripts + "\n</head>")
    doc += "\n" + nav("", prefix="/") + body + FOOT.replace("__PREFIX__", "/")
    write(os.path.join(ROOT, p["slug"], "index.html"), doc)


def sitemap():
    urls = ["https://renderdemartes.com/", "https://renderdemartes.com/academic/"] + \
           [f'https://renderdemartes.com/{p["slug"]}/' for p in PAGES]
    rows = "\n".join(
        f'  <url><loc>{u}</loc><changefreq>monthly</changefreq>'
        f'<priority>{"1.0" if u.endswith("com/") else "0.8"}</priority></url>' for u in urls)
    write(os.path.join(ROOT, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '\n</urlset>\n')


if __name__ == "__main__":
    for p in PAGES:
        build(p)
    sitemap()
    print(f"{len(PAGES)} SEO pages + sitemap")
