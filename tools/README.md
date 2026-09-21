# Site generators

renderdemartes.com is static HTML with no build step and no framework — but the
pages are *generated*, and this is where the generators live. Editing the HTML by
hand is fine; just know a regeneration will overwrite it.

`tools/` is deliberately **not** in `.cpanel.yml`, so nothing here deploys.

## Regenerating the site

Order matters. `optimize.py` runs **last**.

```bash
cd tools
python gen.py        # / and /academic/
python seo.py        # the five SEO landing pages
python tut.py        # the six workflow pages
python optimize.py   # images, minify, cache-bust  <- always last
```

### Why optimize.py must run last

It does three things the others depend on not having happened yet:

1. Recompresses images, caps them at 1600px and writes WebP siblings, then
   rewrites every `<img>` to the WebP and adds width/height.
2. Minifies `assets/css/site.css`, `assets/css/fonts.css` and `assets/js/site.js`
   **in place**.
3. Stamps a content hash onto every CSS/JS URL (`site.css?v=6976c4eb`).

Step 3 is not cosmetic. `.htaccess` serves assets with `immutable, max-age=1y`,
so a deploy that does not change those URLs never reaches anyone who has already
visited the site. **Skip it and your change is invisible to returning visitors.**

### Do not run optimize.py twice

It minifies the on-disk asset files in place. The readable sources live here as
`src_site.css` and `src_site.js` — edit those, copy them over the minified ones,
then run `optimize.py`. Running it on already-minified files is not fatal but it
is not idempotent either.

## Files

| File | What it does |
|---|---|
| `gen.py` | Builds `/` (the CV) and `/academic/`. Holds `CREDITS` and `STUDIES` — the actual content. |
| `seo.py` | The five SEO landing pages. |
| `tut.py` | The six workflow pages, from `tutorials.json`. |
| `optimize.py` | The post-build pass. Run last. |
| `posters.py` | First-frame posters for the heavy GIFs. |
| `gif2mp4.py` | Transcodes GIFs to H.264 (37 clips, 67 MB → 14 MB). |
| `fonts.py` | Downloads and subsets the self-hosted woff2 faces. |
| `src_site.css`, `src_site.js` | The readable sources. The deployed copies are minified. |
| `tutorials.json` | Extracted workflow-page content. |

### One-off migration scripts

These ran once during the WordPress migration and are kept for reference. They
point at backup folders on the Desktop, not at this repo:

| File | |
|---|---|
| `backup_wp.py` | Pulled renderdemartes.com's media library through the WP REST API |
| `backup_mutant.py` | The same for mutanttools.com |
| `extract_tutorials.py` | Turned the archived WordPress tutorial pages into `tutorials.json` |
| `build_mutant.py` | Built the first static mutanttools.com from its WordPress mirror |

## Deploying

See [UPLOAD.md](../UPLOAD.md). Short version: push, then in cPanel use **Update
from Remote** followed by **Deploy HEAD Commit** — there is no push-to-deploy
hook, because shell access is disabled on the account.

## Gotchas

- **`.htaccess` redirects must stay host-scoped `RewriteRule`s.** A parent
  `.htaccess` applies to subdirectories too, and mutanttools.com lives inside
  `public_html/`. A bare `RedirectMatch` here takes that site down. It has
  happened once.
- **`assets/img/og.jpg` must stay a jpg.** `optimize.py` lists it in
  `KEEP_ORIGINAL` because several link scrapers refuse WebP.
- **`google693ef86f823ca3aa.html`** at the root is the Search Console
  verification token. Deleting it un-verifies the property.
