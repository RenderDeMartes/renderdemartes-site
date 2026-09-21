# Upload to cPanel

No build step, no npm, no framework. Upload the **contents** of this folder into `public_html/`.

```
index.html      academic/index.html     404.html
robots.txt      sitemap.xml             .htaccess      assets/
```

In cPanel File Manager: Settings → **Show hidden files**, or `.htaccess` will not appear and the
HTTPS redirect, the old-URL redirects, gzip and cache headers will all be missing.

Do **not** upload `UPLOAD.md` or `.claude/` — both are working files.

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
| `/the-king/` · `/creature-rigging/` · `/face-rig-study/` | Workflow write-ups, original URLs kept |
| `/how-to-rig-a-car/` · `/prop-rig/` · `/rig-with-mocap-packs/` · `/qt-designer-basics/` | Workflow write-ups |

The five landing pages are **deliberately not in the menu**. They exist to be found in search, they
cross-link to each other so they are not orphans, and each closes with a contact call to action.
All five are in `sitemap.xml` — submit that in Google Search Console after upload, or nothing gets
crawled for weeks.

The CV shows **Superneat, The Coalition, Stellar Creative Lab, Scanline VFX and Bardel**, plus
Bluetape Rigging as the freelance band. Everything older points at LinkedIn instead of living here.

A studio with several shows gets dots under the media — click, or focus a dot and use the arrow
keys. Only the visible slide ever mounts a player.

## Trailers

Each trailer streams **muted, looping, no controls**, mounted only while its row is on screen and
removed when it scrolls away, so the page never keeps more than two or three players alive. The
still underneath is the poster. **SOUND** swaps in a normal player with audio and controls.

Videos are `youtube-nocookie.com`, so no YouTube cookie is set until someone plays one.

Superneat (NDA) and Foodtopia Season 2 (no public footage) show a still only.

## Contact — and the spam question

There is no form and no PHP. Two buttons: **LinkedIn profile**, and **Email me**, which builds
`info@renderdemartes.com` in the browser from two `data-` attributes at click time. The address
never appears in the HTML, so scrapers reading the page find nothing to harvest; hovering shows it
in the tooltip so a human knows where the click goes.

**This needs `info@renderdemartes.com` to exist** — create it in cPanel → Email Accounts, or forward
it to your Gmail.

## The WordPress backup

Before anything is deleted, the full media library is saved at `C:\Users\rodri\Desktop\RdM WordPress Backup` — **310 files, 135 MB**, pulled through the WordPress REST API rather than by crawling links, so files nobody linked to came down too. `media-manifest.csv` lists every item with its original URL, date, type and local path.

Two of them are not pictures and would otherwise have been lost: **`mutantbot.zip` (7.6 MB)** and `ui_tutorial.zip`.

## Workflow pages

The seven tutorials are rebuilt in the new design at their original URLs, so the links and rankings they already have keep working. Text and images were extracted from the archive automatically.

They carry about 94 MB of GIFs. Anything over 1.5 MB ships as a **first-frame poster with a click-to-play button** — the page shows a badge (`GIF · 13.8 MB · CLICK TO PLAY`) and only fetches the animation when someone asks for it. Smaller GIFs load inline, lazily.

## Old URLs

`/blog/`, `/hire/`, `/workflows/`, `/contact/` and `/cv/` no longer exist here — `.htaccess` sends them to `/`
with a 301 so inbound links survive. The tutorial URLs are **no longer redirected**, because those pages exist again.

## Local preview

```bash
python -m http.server 8791
```

Then open http://localhost:8791.

## Regenerating

Both pages come from `gen.py` (session scratchpad) so the ledger stays consistent. Editing the HTML
by hand is fine too — it is plain static markup.

## Still open

- Confirm the UX/UI master's official name and start date.
- Old tutorial pages are redirected, not ported. Port them later if you want that traffic back.
