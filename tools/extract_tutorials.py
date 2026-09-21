# -*- coding: utf-8 -*-
"""Pull the workflow/tutorial content out of the archived WordPress pages.

Reads the local mirror, walks the Elementor widgets in document order and emits
an ordered block list per page, then copies the full-size images out of the
media backup into the new site.
"""
import html, io, json, os, re, shutil
from html.parser import HTMLParser

MIRROR = r"C:\Users\rodri\Desktop\WebsitesDesign\_backup\renderdemartes.com"
MEDIA = r"C:\Users\rodri\Desktop\RdM WordPress Backup\files\wp-content\uploads"
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
SITE = _os.path.dirname(_HERE)   # site root is this folder's parent
OUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tutorials.json")

SLUGS = ["the-king", "creature-rigging", "face-rig-study", "how-to-rig-a-car",
         "prop-rig", "rig-with-mocap-packs", "qt-designer-basics"]

SKIP_TEXT = re.compile(
    r"^(table of contents|copy|download|previous|next|menu|search|skip to content)$", re.I)


VOID = {"img", "br", "hr", "input", "meta", "link", "source", "track", "area", "base", "col", "embed", "param", "wbr"}
SUPPRESS_CLASS = re.compile(r"elementor-nav-menu|table-of-content|ekit-|site-header|site-footer|breadcrumb", re.I)


class Blocks(HTMLParser):
    """Walks the archived markup in document order, skipping page chrome.

    Suppression is depth-tracked: when a chrome element opens we remember the
    depth it opened at, and stop suppressing once we climb back above it. The
    previous version only ever un-suppressed on </nav>, so a chrome <div>
    silenced the whole page.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.buf = []
        self.capture = None
        self.depth = 0
        self.mutes = []      # depths at which a chrome element opened
        self.in_code = 0

    @property
    def muted(self):
        return bool(self.mutes)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        void = tag in VOID
        if not void:
            self.depth += 1
        if tag in ("nav", "header", "footer", "form", "script", "style", "aside") or SUPPRESS_CLASS.search(cls):
            if not void:
                self.mutes.append(self.depth)
            return
        if self.muted:
            return

        if tag == "img":
            src = a.get("src") or a.get("data-src") or ""
            if "/uploads/" in src:
                self.blocks.append({"t": "img", "src": src, "alt": (a.get("alt") or "").strip()})
        elif tag in ("h1", "h2", "h3", "h4"):
            self.capture, self.buf = "h" + tag[1], []
        elif tag == "p":
            self.capture, self.buf = "p", []
        elif tag == "li":
            self.capture, self.buf = "li", []
        elif tag in ("pre", "code"):
            self.in_code += 1
            if self.in_code == 1:
                self.capture, self.buf = "code", []

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.capture and not self.muted:
            if tag in ("pre", "code"):
                self.in_code = max(0, self.in_code - 1)
                if self.in_code == 0 and self.capture == "code":
                    self.flush("code")
            elif (tag.startswith("h") and self.capture.startswith("h")) or                  (tag == "p" and self.capture == "p") or (tag == "li" and self.capture == "li"):
                self.flush(self.capture)
        self.depth = max(0, self.depth - 1)
        while self.mutes and self.mutes[-1] > self.depth:
            self.mutes.pop()

    def handle_data(self, data):
        if self.capture and not self.muted:
            self.buf.append(data)

    def flush(self, kind):
        raw = "".join(self.buf)
        if kind == "code":
            # keep the line breaks — this is a code tutorial, not prose
            lines = [ln.rstrip() for ln in raw.replace("\r\n", "\n").split("\n")]
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            text = "\n".join(lines)
        else:
            text = re.sub(r"\s+", " ", raw).strip()
        self.buf, self.capture = [], None
        if not text or SKIP_TEXT.match(text):
            return
        self.blocks.append({"t": kind, "text": text})


def original_of(src):
    """Strip WordPress size suffixes and return the best local file for a src."""
    rel = src.split("/uploads/")[-1]
    parts = rel.split("/")
    name = parts[-1]
    stem, ext = os.path.splitext(name)
    stem = re.sub(r"-\d+x\d+$", "", stem)
    candidates = [os.path.join(MEDIA, *parts[:-1], stem + ext),
                  os.path.join(MEDIA, *parts)]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def main():
    pages = {}
    copied, missing = 0, []
    for slug in SLUGS:
        path = os.path.join(MIRROR, slug, "index.html")
        if not os.path.exists(path):
            print("missing mirror:", slug)
            continue
        raw = io.open(path, encoding="utf-8", errors="ignore").read()
        # body only, and drop obvious chrome
        body = raw.split("<body", 1)[-1]
        b = Blocks()
        b.feed(body)

        blocks, seen_img, seen_txt = [], set(), set()
        for bl in b.blocks:
            if bl["t"] == "img":
                key = bl["src"].split("/uploads/")[-1]
                key = re.sub(r"-\d+x\d+(\.\w+)$", r"\1", key)
                if key in seen_img:
                    continue
                seen_img.add(key)
                srcfile = original_of(bl["src"])
                if not srcfile:
                    missing.append(bl["src"])
                    continue
                dest_rel = f"assets/img/tut/{slug}/{os.path.basename(srcfile)}"
                dest = os.path.join(SITE, *dest_rel.split("/"))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                if not os.path.exists(dest):
                    shutil.copy2(srcfile, dest)
                    copied += 1
                blocks.append({"t": "img", "src": dest_rel, "alt": bl["alt"],
                               "bytes": os.path.getsize(dest)})
            else:
                t = bl["text"]
                if len(t) < 3:
                    continue
                if bl["t"] in ("p", "li"):
                    if t in seen_txt:
                        continue
                    seen_txt.add(t)
                blocks.append(bl)
        pages[slug] = blocks
        kinds = {}
        for bl in blocks:
            kinds[bl["t"]] = kinds.get(bl["t"], 0) + 1
        print(f"{slug:24} {kinds}")

    with io.open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=1)
    print(f"\ncopied {copied} images; {len(missing)} missing")
    for m in missing[:10]:
        print("  missing:", m)


if __name__ == "__main__":
    main()
