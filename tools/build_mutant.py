# -*- coding: utf-8 -*-
"""Turn the mutanttools.com WordPress pages into a static site, same design.

Astra's stylesheet is what carries the layout, so it stays (pulled local along
with the Spectra block extensions and the menu script). What goes: the REST /
oEmbed / feed plumbing, React, SureForms, AOS, and the 800 KB block-editor
bundle. The contact form becomes a mailto button.
"""
import io, os, re

MIRROR = r"C:\Users\rodri\Desktop\MutantTools WordPress Backup\pages"
OUT = r"C:\Users\rodri\Desktop\MutantTools Site"

PAGES = {
    "index.html": ("", "Mutant Tools — Production-Ready Rigging Tools for Maya",
                   "Modular autorigger and rigging framework for Maya: blocks, guides, build, save/load. Body, face, quadrupeds, props. Built for production pipelines."),
    "rigger/.html": ("rigger", "For Riggers — Mutant Tools",
                     "Mutant Tools for riggers: modular blocks, guide placement, rebuilds that keep controllers and skins, and a workflow built for real deadlines."),
    "developer/.html": ("developer", "For Developers — Mutant Tools",
                        "Extend Mutant Tools: the Python API, custom blocks, and hooks for studio pipelines."),
    "learn/.html": ("learn", "Learn — Mutant Tools",
                    "Tutorials, block-based workflows and production examples for rigging in Maya with Mutant Tools."),
    "free-assets/.html": ("free-assets", "Free Assets — Mutant Tools",
                          "Free rigs, tools and assets from Mutant Tools for riggers and animators."),
    "contact/.html": ("contact", "Contact — Mutant Tools",
                      "Get in touch about Mutant Tools, studio services, custom rigging and pipeline development."),
}

MAIL_BTN = (
    '<div class="wp-block-buttons is-content-justification-center is-layout-flex">'
    '<div class="wp-block-button">'
    '<button class="wp-block-button__link wp-element-button" type="button" '
    'data-mail data-u="info" data-d="renderdemartes.com" data-s="Mutant Tools">'
    'EMAIL ME</button></div></div>'
)

JS = """/* Mutant Tools - static. Spam-safe mail button, plus a menu fallback. */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    var m = e.target.closest ? e.target.closest('[data-mail]') : null;
    if (!m) return;
    var addr = m.getAttribute('data-u') + String.fromCharCode(64) + m.getAttribute('data-d');
    var s = m.getAttribute('data-s');
    window.location.href = 'mailto:' + addr + (s ? '?subject=' + encodeURIComponent(s) : '');
  });
})();
"""

KEEP_CSS = ("astra/assets/css/minified/main.min.css",
            "astra/assets/css/minified/menu-animation.min.css",
            "spectra-v3/build/styles/extensions/")
KEEP_JS = ("astra/assets/js/minified/frontend.min.js",
           "astra/assets/js/minified/flexibility.min.js")

UPLOADS = re.compile(r"""https://mutanttools\.com/wp-content/uploads/\d{4}/\d{2}/([^"'\s\)]+?)(\?[^"'\s\)]*)?(?=["'\s\)])""")
WPCONTENT = re.compile(r"""https://mutanttools\.com/wp-content/([^"'\s\)]+?)(\?[^"'\s\)]*)?(?=["'\s\)])""")
SCRIPTS = re.compile(r"<script\b[^>]*>.*?</script>|<script\b[^>]*/>", re.S)
SHEETS = re.compile(r"""<link\b[^>]*rel=['"]stylesheet['"][^>]*>""")


def clean(html, slug, title, desc):
    h = html

    # assets local — uploads first, then everything else under wp-content
    h = UPLOADS.sub(lambda m: "/assets/img/" + m.group(1), h)
    h = WPCONTENT.sub(lambda m: "/assets/vendor/" + m.group(1), h)

    # scripts: keep Astra's menu script and the inline config it reads
    def script_filter(m):
        tag = m.group(0)
        src = re.search(r"""src\s*=\s*['"]([^'"]+)['"]""", tag)
        if src:
            return tag if any(k in src.group(1) for k in KEEP_JS) else ""
        return tag if re.search(r"\bastra\s*=|var\s+astra", tag) else ""
    h = SCRIPTS.sub(script_filter, h)

    # stylesheets: theme + block extensions stay, form/animation CSS goes
    def css_filter(m):
        tag = m.group(0)
        href = re.search(r"""href\s*=\s*['"]([^'"]+)['"]""", tag)
        if not href:
            return tag
        u = href.group(1)
        if u.startswith("/assets/css/") or any(k in u for k in KEEP_CSS):
            return tag
        return "" if "/assets/vendor/" in u else tag
    h = SHEETS.sub(css_filter, h)

    # WordPress plumbing
    h = re.sub(r"""<link[^>]+rel=['"](?:EditURI|wlwmanifest|alternate|shortlink|pingback|profile|dns-prefetch)['"][^>]*>""", "", h)
    h = re.sub(r"<link[^>]+(?:api\.w\.org|wp-json|xmlrpc|oembed)[^>]*>", "", h)
    h = re.sub(r"""<meta[^>]+name=['"]generator['"][^>]*>""", "", h)

    # Montserrat self-hosted
    h = re.sub(r"<link[^>]+fonts\.googleapis\.com[^>]*>",
               '<link rel="stylesheet" href="/assets/css/fonts.css">', h)

    # internal links
    h = h.replace("https://mutanttools.com/", "/")

    # SureForms -> mailto
    if "<form" in h:
        h = re.sub(r"<form.*?</form>", MAIL_BTN, h, flags=re.S)

    canonical = "https://mutanttools.com/" + (slug + "/" if slug else "")
    head_add = "\n".join([
        '<meta name="description" content="%s">' % desc,
        '<link rel="canonical" href="%s">' % canonical,
        '<link rel="icon" href="/assets/img/LogoWhite03-74x74.png" sizes="any">',
        '<link rel="apple-touch-icon" href="/assets/img/LogoWhite03-300x300.png">',
        '<meta property="og:title" content="%s">' % title,
        '<meta property="og:description" content="%s">' % desc,
        '<meta property="og:image" content="https://mutanttools.com/assets/img/santa_render.png">',
        '<meta name="twitter:card" content="summary_large_image">',
    ])
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>\n%s" % (title, head_add), h, flags=re.S)
    h = h.replace("</body>", '<script src="/assets/js/site.js" defer></script>\n</body>')
    h = re.sub(r"\n{3,}", "\n\n", h)
    return h


CONTACT_BLOCK = """
<div style="padding:7rem 20px 8rem;text-align:center">
  <h1 style="font-size:clamp(2.2rem,6vw,3.4rem);color:#fff;margin:0 0 1.2rem;letter-spacing:-.02em">Contact</h1>
  <p style="max-width:620px;margin:0 auto 2.5rem;color:#c9ccd2;font-size:1.05rem;line-height:1.7">
    Questions about Mutant Tools, studio services, custom rigging or pipeline
    development &mdash; the fastest way to reach me is email.
  </p>
  <button type="button" data-mail data-u="info" data-d="renderdemartes.com" data-s="Mutant Tools"
    style="display:inline-block;background:#f0561d;color:#fff;border:0;border-radius:999px;
           padding:16px 34px;font-size:.95rem;font-weight:700;letter-spacing:.06em;cursor:pointer">
    EMAIL ME
  </button>
</div>
"""


def graft_contact_header():
    """The contact page uses Astra's page-builder template, which ships no
    header or footer. Borrow both from /rigger/ so the page stops looking
    like an orphan."""
    src = io.open(os.path.join(OUT, "rigger", "index.html"), encoding="utf-8").read()
    body = src.split("<body", 1)[1]
    hi, hj = body.find("<header"), body.find("</header>") + len("</header>")
    header = body[hi:hj] if hi != -1 else ""
    fi, fj = body.find("<footer"), body.find("</footer>") + len("</footer>")
    footer = body[fi:fj] if fi != -1 else ""

    path = os.path.join(OUT, "contact", "index.html")
    h = io.open(path, encoding="utf-8").read()
    marker = '<div id="content" class="site-content">'
    if marker in h and header:
        h = h.replace(marker, header + "\n" + marker, 1)
    # replace the lone button with a real contact block
    h = h.replace(MAIL_BTN, CONTACT_BLOCK, 1)
    if footer:
        h = h.replace("</body>", footer + "\n</body>", 1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(h)
    print("  contact: header+footer grafted, %d KB" % (len(h) / 1024))


def main():
    os.makedirs(os.path.join(OUT, "assets", "js"), exist_ok=True)
    io.open(os.path.join(OUT, "assets", "js", "site.js"), "w", encoding="utf-8", newline="\n").write(JS)

    before = after = 0
    for src, (slug, title, desc) in PAGES.items():
        raw = io.open(os.path.join(MIRROR, src), encoding="utf-8").read()
        out = clean(raw, slug, title, desc)
        before += len(raw)
        after += len(out)
        dest = os.path.join(OUT, "index.html") if not slug else os.path.join(OUT, slug, "index.html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        io.open(dest, "w", encoding="utf-8", newline="\n").write(out)
        print("  %-13s %6.1f KB -> %6.1f KB   css:%d  js:%d" % (
            slug or "/", len(raw) / 1024, len(out) / 1024,
            len(SHEETS.findall(out)), len(re.findall(r"<script", out))))

    graft_contact_header()

    io.open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(
        "User-agent: *\nAllow: /\n\nSitemap: https://mutanttools.com/sitemap.xml\n")
    urls = ["https://mutanttools.com/"] + [
        "https://mutanttools.com/%s/" % s for s in ("rigger", "developer", "learn", "free-assets", "contact")]
    urls.append("https://mutanttools.com/docs/_build/html/index.html")
    rows = "\n".join("  <url><loc>%s</loc><changefreq>monthly</changefreq></url>" % u for u in urls)
    io.open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n")

    print("\ntotal html %.0f KB -> %.0f KB" % (before / 1024, after / 1024))


if __name__ == "__main__":
    main()
