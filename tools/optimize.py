# -*- coding: utf-8 -*-
"""Post-build optimisation pass. Run LAST, after gen/seo/tut have written the HTML.

- recompresses JPEG/PNG, caps them at 1600px, writes WebP siblings
- rewrites every <img>/srcset to the WebP and adds width/height (no layout shift)
- swaps the Google Fonts <link> for the self-hosted faces + preloads
- minifies CSS and JS
"""
import io, os, re, shutil
from PIL import Image

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
SITE = _os.path.dirname(_HERE)   # site root is this folder's parent
IMG = os.path.join(SITE, "assets", "img")
MAXW = 1600
KEEP_ORIGINAL = {                      # referenced by crawlers/OS, must stay as-is
    "assets/img/og.jpg",                  # og:image - WhatsApp/Facebook need jpg
    "assets/img/still/gears-e-day.jpg",
    "assets/img/favicon-32.png",
    "assets/img/apple-touch-icon.png",
    "assets/img/favicon-512.png",
    "assets/img/favicon.png",
}
SIZES = {}                              # rel path -> (w, h)


def rel(path):
    return os.path.relpath(path, SITE).replace("\\", "/")


def optimise_rasters():
    saved_before = saved_after = 0
    made = 0
    for root, _, files in os.walk(IMG):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in (".jpg", ".jpeg", ".png"):
                continue
            path = os.path.join(root, f)
            r = rel(path)
            before = os.path.getsize(path)
            saved_before += before

            im = Image.open(path)
            im.load()
            if im.width > MAXW:
                im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)

            has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)

            # rewrite the original in place, smaller
            if ext == ".png" and not has_alpha:
                im.convert("RGB").save(path, "PNG", optimize=True)
            elif ext == ".png":
                im.convert("RGBA").save(path, "PNG", optimize=True)
            else:
                im.convert("RGB").save(path, "JPEG", quality=80, optimize=True, progressive=True)

            # webp sibling
            webp = os.path.splitext(path)[0] + ".webp"
            (im if has_alpha else im.convert("RGB")).save(webp, "WEBP", quality=80, method=6)
            made += 1
            SIZES[rel(webp)] = (im.width, im.height)
            SIZES[r] = (im.width, im.height)
            saved_after += os.path.getsize(path)

    print(f"rasters: {saved_before/1048576:.1f} MB -> {saved_after/1048576:.1f} MB, {made} webp written")


def drop_superseded():
    """Delete originals that nothing references any more (WebP replaced them)."""
    freed = 0
    for root, _, files in os.walk(IMG):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in (".jpg", ".jpeg", ".png"):
                continue
            path = os.path.join(root, f)
            r = rel(path)
            if r in KEEP_ORIGINAL:
                continue
            if os.path.exists(os.path.splitext(path)[0] + ".webp"):
                freed += os.path.getsize(path)
                os.remove(path)
    print(f"removed superseded originals: {freed/1048576:.1f} MB freed")


IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
ATTR = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')


def rewrite_html():
    pages = 0
    for root, _, files in os.walk(SITE):
        if os.sep + "assets" in root or os.sep + ".claude" in root:
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(root, f)
            s = io.open(path, encoding="utf-8").read()
            orig = s

            # 1. fonts: self-hosted + preload the two faces the first screen needs
            s = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\s*', "", s)
            def font_link(m):
                prefix = m.group(1)
                return (f'<link rel="preload" href="{prefix}assets/fonts/space-grotesk-700-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
                        f'<link rel="preload" href="{prefix}assets/fonts/jetbrains-mono-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
                        f'<link rel="stylesheet" href="{prefix}assets/css/fonts.css">')
            s = re.sub(r'<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">',
                       lambda m: font_link(re.search(r'href="([^"]*)assets/css/site\.css"', s)), s)

            # 2. images -> webp, plus width/height
            def fix_img(m):
                tag = m.group(0)
                attrs = dict(ATTR.findall(tag))
                src = attrs.get("src", "")
                key = src.lstrip("/")
                webp_key = os.path.splitext(key)[0] + ".webp"
                if key and os.path.exists(os.path.join(SITE, *webp_key.split("/"))) and key not in KEEP_ORIGINAL:
                    new_src = ("/" if src.startswith("/") else "") + webp_key
                    tag = tag.replace(f'src="{src}"', f'src="{new_src}"')
                    if "srcset" in attrs:
                        ss = attrs["srcset"]
                        new_ss = re.sub(r"(\S+)\.(png|jpe?g)(\s+\d+x)",
                                        lambda mm: mm.group(1) + ".webp" + mm.group(3), ss)
                        tag = tag.replace(f'srcset="{ss}"', f'srcset="{new_ss}"')
                    key = webp_key
                dims = SIZES.get(key)
                if dims and "width=" not in tag:
                    tag = tag.replace("<img", f'<img width="{dims[0]}" height="{dims[1]}"', 1)
                return tag
            s = IMG_TAG.sub(fix_img, s)

            # 3. click-to-play gif buttons point at a src too
            s = re.sub(r'data-gif="([^"]+)"', lambda m: f'data-gif="{m.group(1)}"', s)

            if s != orig:
                io.open(path, "w", encoding="utf-8", newline="\n").write(s)
                pages += 1
    print(f"rewrote {pages} html files")


def minify_css(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"\s+", " ", src)
    src = re.sub(r"\s*([{}:;,>~])\s*", r"\1", src)
    src = src.replace(";}", "}")
    return src.strip()


def minify_js(src):
    out = []
    for line in src.split("\n"):
        stripped = line.strip()
        if stripped.startswith("//") and "://" not in stripped:
            continue
        out.append(stripped)
    js = "\n".join(l for l in out if l)
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    return js


def minify_assets():
    for name, fn in (("css/site.css", minify_css), ("css/fonts.css", minify_css), ("js/site.js", minify_js)):
        path = os.path.join(SITE, "assets", *name.split("/"))
        src = io.open(path, encoding="utf-8").read()
        backup = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src_" + os.path.basename(name))
        if not os.path.exists(backup):
            shutil.copy2(path, backup)      # keep the readable source in the scratchpad
        out = fn(src)
        io.open(path, "w", encoding="utf-8", newline="\n").write(out)
        print(f"  {name}: {len(src)/1024:.1f} KB -> {len(out)/1024:.1f} KB")


def version_assets():
    """Cache-bust CSS/JS.

    .htaccess serves assets with `immutable, max-age=1y`, so a redeploy alone
    never reaches a returning visitor. HTML is no-cache, so stamping a content
    hash onto the asset URLs is what actually ships a change.
    """
    import hashlib
    stamps = {}
    for name in ("css/site.css", "css/fonts.css", "js/site.js"):
        path = os.path.join(SITE, "assets", *name.split("/"))
        if os.path.exists(path):
            stamps[name] = hashlib.md5(io.open(path, "rb").read()).hexdigest()[:8]

    touched = 0
    for root, _, files in os.walk(SITE):
        if os.sep + ".git" in root or os.sep + ".claude" in root:
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(root, f)
            s = io.open(path, encoding="utf-8").read()
            orig = s
            for name, h in stamps.items():
                s = re.sub(r'(assets/' + name.replace("/", r"/") + r')(\?v=[a-f0-9]+)?',
                           lambda m, h=h: m.group(1) + "?v=" + h, s)
            if s != orig:
                io.open(path, "w", encoding="utf-8", newline="\n").write(s)
                touched += 1
    print("versioned assets on %d pages: %s" % (touched, ", ".join("%s=%s" % kv for kv in stamps.items())))


def main():
    optimise_rasters()
    rewrite_html()
    drop_superseded()
    print("minifying:")
    minify_assets()
    version_assets()
    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _, fs in os.walk(SITE) for f in fs
                if ".claude" not in r)
    print(f"\nsite total: {total/1048576:.1f} MB")


if __name__ == "__main__":
    main()
