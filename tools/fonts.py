# -*- coding: utf-8 -*-
"""Self-host the two webfonts: no Google round trip, no third-party cookie surface.

Both families are variable fonts, so one latin file per family covers every
weight the site uses. The CSS declares a weight *range* per face; declaring
per-weight faces (and latin-ext) points at files that do not exist and 404s.
File names are fixed because optimize.py preloads them by name.
"""
import io, os, re, urllib.request

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
SITE = _os.path.dirname(_HERE)   # site root is this folder's parent
FONT_DIR = os.path.join(SITE, "assets", "fonts")
CSS_URL = ("https://fonts.googleapis.com/css2?"
           "family=Space+Grotesk:wght@300..700&family=JetBrains+Mono:wght@100..800&display=swap")
# a modern UA so Google serves woff2 + the latin subsets
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
KEEP = ("latin",)
# file name per family — must match the preloads in optimize.py
NAMES = {"Space Grotesk": "space-grotesk-700-latin.woff2",
         "JetBrains Mono": "jetbrains-mono-400-latin.woff2"}


def get(url, headers=UA):
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60).read()


def main():
    os.makedirs(FONT_DIR, exist_ok=True)
    css = get(CSS_URL).decode("utf-8")

    blocks = re.findall(r"/\*\s*([\w\-\[\]]+)\s*\*/\s*@font-face\s*{(.*?)}", css, re.S)
    out, seen = [], set()
    for subset, block in blocks:
        if subset not in KEEP:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        weight = re.search(r"font-weight:\s*(\d+(?:\s+\d+)?)", block).group(1)
        style = re.search(r"font-style:\s*(\w+)", block).group(1)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)

        name = NAMES[fam]
        path = os.path.join(FONT_DIR, name)
        if name not in seen:
            with open(path, "wb") as f:
                f.write(get(url))
            seen.add(name)
            print(f"  {os.path.getsize(path):>7,} B  {name}")

        out.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
            "src:url('../fonts/%s') format('woff2')}" % (fam, style, weight, name))

    face_css = "/* self-hosted webfonts — no third-party request */\n" + "\n".join(out) + "\n"
    with io.open(os.path.join(SITE, "assets", "css", "fonts.css"), "w", encoding="utf-8", newline="\n") as f:
        f.write(face_css)
    total = sum(os.path.getsize(os.path.join(FONT_DIR, n)) for n in seen)
    print(f"\n{len(seen)} font files, {total/1024:.0f} KB total")


if __name__ == "__main__":
    main()
