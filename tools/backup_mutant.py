# -*- coding: utf-8 -*-
"""Back up mutanttools.com before its WordPress install is removed.

Media comes from the REST API (catches unlinked library items); pages and every
asset they reference are mirrored so the current look can be rebuilt exactly.
"""
import csv, io, json, os, re, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

SITE = "https://mutanttools.com"
OUT = r"C:\Users\rodri\Desktop\MutantTools WordPress Backup"
UA = {"User-Agent": "Mozilla/5.0 (backup before migration)"}
PAGES = ["/", "/rigger/", "/developer/", "/learn/", "/free-assets/", "/contact/", "/hello-world/"]


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()


def save(rel, data):
    path = os.path.join(OUT, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)

    # 1. media library
    media, page = [], 1
    while True:
        try:
            batch = json.loads(get(f"{SITE}/wp-json/wp/v2/media?per_page=100&page={page}").decode())
        except Exception:
            break
        if not batch:
            break
        media.extend(batch)
        page += 1
        if page > 10:
            break
    print(f"media library: {len(media)} items")

    def fetch_media(it):
        src = it.get("source_url")
        if not src:
            return None
        rel = "files/" + urllib.parse.urlparse(src).path.lstrip("/")
        try:
            p = save(rel, get(src))
            return (it["id"], it.get("mime_type"), src, rel, os.path.getsize(p))
        except Exception as e:
            return (it["id"], it.get("mime_type"), src, rel, f"FAIL {e}")

    rows = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(fetch_media, media):
            if r:
                rows.append(r)
                print(f"  {r[4] if isinstance(r[4],int) else r[4]}  {r[3]}")

    # 2. pages + their assets
    assets, saved_pages = set(), []
    for p in PAGES:
        try:
            html = get(SITE + p).decode("utf-8", "ignore")
        except Exception as e:
            print(f"  page FAIL {p}: {e}")
            continue
        rel = "pages" + (p if p != "/" else "/index") + ".html"
        rel = rel.replace("//", "/").rstrip("/")
        if not rel.endswith(".html"):
            rel += "/index.html"
        save(rel, html.encode("utf-8"))
        saved_pages.append((p, rel, len(html)))
        for m in re.findall(r'(?:src|href)="([^"]+)"', html):
            if m.startswith("//"):
                m = "https:" + m
            if m.startswith("/"):
                m = SITE + m
            if m.startswith(SITE) and re.search(r"\.(css|js|jpe?g|png|gif|webp|svg|woff2?|ttf|mp4|zip|ico)(\?|$)", m, re.I):
                assets.add(m.split("?")[0])
    print(f"pages mirrored: {len(saved_pages)}")

    def fetch_asset(u):
        rel = "assets/" + urllib.parse.urlparse(u).path.lstrip("/")
        try:
            save(rel, get(u))
            return rel
        except Exception:
            return None

    ok = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(fetch_asset, sorted(assets)):
            if r:
                ok += 1
    print(f"theme assets: {ok}/{len(assets)}")

    with io.open(os.path.join(OUT, "manifest.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["kind", "id", "mime", "source", "local", "bytes"])
        for r in rows:
            w.writerow(["media", r[0], r[1], r[2], r[3], r[4]])
        for p, rel, n in saved_pages:
            w.writerow(["page", "", "text/html", SITE + p, rel, n])

    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _, fs in os.walk(OUT) for f in fs)
    print(f"\nbackup total: {total/1048576:.1f} MB at {OUT}")


if __name__ == "__main__":
    main()
