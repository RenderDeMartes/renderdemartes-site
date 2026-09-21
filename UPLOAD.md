# Deploying renderdemartes.com

No build step, no npm, no framework — plain static files.

## The normal way: cPanel Git

The site lives at **github.com/RenderDeMartes/renderdemartes-site** and cPanel pulls from it.
Shell access is off on the account, so **there is no push-to-deploy hook**. A push on its own
changes nothing live. Three steps, every time:

1. `git push origin master`
2. cPanel → **Git™ Version Control** → `renderdemartes-site` → *Pull or Deploy* → **Update from Remote**
3. Same tab → **Deploy HEAD Commit**

Step 3 runs `.cpanel.yml`, which copies the tracked files into `/home/renderdem/public_html/`.
Check the result with `curl https://renderdemartes.com/` rather than the browser — the browser is
the one thing guaranteed to show you a cached copy.

`mutanttools.com` works the same way from `mutanttools-site`, deploying into
`public_html/mutanttools.com/`. Its `.cpanel.yml` is scoped to that subfolder on purpose: a
deploy path of bare `public_html/` there would bury this site.

**Assets are served `immutable, max-age=1y`.** Redeploying a changed `site.css` does not reach
anyone who has already visited. `optimize.py` handles this by stamping a content hash onto every
CSS/JS URL (`site.css?v=6976c4eb`) — run it before committing or the deploy is invisible.

## The fallback: File Manager

Upload the **contents** of this folder into `public_html/`. In File Manager, turn on
Settings → **Show hidden files** first, or `.htaccess` never arrives and the HTTPS redirect,
the old-URL redirects, gzip and the cache headers all silently vanish.

Do not upload `UPLOAD.md`, `.git/` or `.claude/` — working files.

## Pages

| URL | What |
|---|---|
| `/` | Hero, CV (five studios), freelance band, LinkedIn call to action, contact |
| `/academic/` | Degrees, certificates, courses — newest first |
| `/hire-a-freelance-character-rigger/` | SEO landing — general hiring |
| `/maya-rigging-services/` | SEO landing — Maya work |
| `/unreal-engine-character-rigging/` | SEO landing — game/engine work |
| `/facial-rigging-services/` | SEO landing — faces |
| `/rigging-outsourcing-for-studios/` | SEO landing — studios and crews |
| `/creature-rigging/` · `/face-rig-study/` · `/how-to-rig-a-car/` | Workflow write-ups, original URLs kept |
| `/prop-rig/` · `/rig-with-mocap-packs/` · `/qt-designer-basics/` | Workflow write-ups |
| `/downloads/` | `mutantbot.zip`, `ui_tutorial.zip` — the old upload URLs 301 here |

The five landing pages are **deliberately not in the menu**. They exist to be found in search, they
cross-link to each other so they are not orphans, and each closes with a contact call to action.
All five are in `sitemap.xml`, submitted in Google Search Console on 2026-09-21 (13 URLs, status
*Correcto*).

The CV shows **Superneat, The Coalition, Stellar Creative Lab, Scanline VFX and Bardel**, plus
Bluetape Rigging as the freelance band. Everything older points at LinkedIn instead of living here.

## Galleries

A studio with several shows gets a bar under the media: **arrows, dots, and the show's name**.
On a phone you swipe. Keyboard works too — focus a dot and use the arrow keys. Only the visible
slide ever mounts a player.

## Trailers

Each trailer streams **muted, looping, no controls**, mounted only while its row is on screen and
removed when it scrolls away, so the page never keeps more than two or three players alive. The
still underneath is the poster. **SOUND** swaps in a normal player with audio and controls.

Videos are `youtube-nocookie.com`, so no YouTube cookie is set until someone plays one.

Superneat (NDA) and Foodtopia Season 2 (no public footage) show a still only.

## Contact and freelance

No form, no PHP, no email address in the HTML — nothing for a scraper to harvest.

- Every **freelance** button goes to `bluetaperigging.com`.
- Every **contact** button goes to the LinkedIn profile.

## Sharing

`assets/img/og.jpg` is the cartoon share card (1200×630) used by WhatsApp, Facebook, LinkedIn and
Twitter. If a platform still shows an old image, its cache is stale, not the tags — force a rescrape
in the Facebook Sharing Debugger and LinkedIn Post Inspector.

Keep that file a **jpg**. `optimize.py` lists it in `KEEP_ORIGINAL` because several scrapers refuse
WebP.

## Old URLs

`/blog/`, `/hire/`, `/workflows/`, `/contact/`, `/cv/` and everything under `/wp-content/uploads/`
301 to `/`. The workflow URLs are **not** redirected — those pages exist again.

The redirect rules are host-scoped `RewriteRule`s, not `Redirect`/`RedirectMatch`. This matters:
a parent `.htaccess` applies to subdirectories too, and `mutanttools.com` lives inside
`public_html/`. A bare `RedirectMatch` here hijacks that site. It has happened once.

## Workflow pages

Six tutorials rebuilt in the new design at their original URLs, so existing links and rankings keep
working. Text and images were extracted from the WordPress archive automatically.

They carry about 94 MB of GIFs. Anything over 1.5 MB ships as a **first-frame poster with a
click-to-play button** — the page shows a badge (`GIF · 13.8 MB · CLICK TO PLAY`) and only fetches
the animation when someone asks for it. Smaller GIFs load inline, lazily.

## The WordPress backup

The full media library is saved at `C:\Users\rodri\Desktop\RdM WordPress Backup` — **310 files,
135 MB**, pulled through the WordPress REST API rather than by crawling links, so files nobody
linked to came down too. `media-manifest.csv` lists every item with its original URL, date, type
and local path. Mutant Tools has its own backup at `C:\Users\rodri\Desktop\MutantTools WordPress
Backup` (30.7 MB).

## Local preview

```bash
python -m http.server 8791
```

Then open http://localhost:8791.

## Regenerating

`gen.py` builds `/` and `/academic/`, `seo.py` the five landing pages, `tut.py` the six workflow
pages (session scratchpad). `optimize.py` runs **last** — it rewrites images to WebP, minifies, and
stamps the cache-busting hashes. Editing the HTML by hand is fine too; it is plain static markup.

## Search Console

URL-prefix property `https://renderdemartes.com/`, verified 2026-09-21 by the HTML file
`google693ef86f823ca3aa.html` at the site root. **Do not delete that file** — Google rechecks it
periodically and drops the property if it disappears. It is listed in `.cpanel.yml`, so every
deploy re-copies it. `mutanttools.com` is a second property using the same per-account token.

## Still open

- Confirm the UX/UI master's official name and start date (`/academic/` currently says
  "Master in UX/UI Design, ESDESIGN, 2026 — now").
