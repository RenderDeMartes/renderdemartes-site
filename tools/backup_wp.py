# -*- coding: utf-8 -*-
"""Pull every media item off the live WordPress install before it is deleted.

Uses the REST API rather than crawling links, so files that are in the media
library but not referenced by any page still come down.
"""
import csv, json, os, sys, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

SITE = "https://renderdemartes.com"
OUT = r"C:\Users\rodri\Desktop\RdM WordPress Backup"
UA = {"User-Agent": "Mozilla/5.0 (backup before migration)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def list_media():
    items, page = [], 1
    while True:
        url = f"{SITE}/wp-json/wp/v2/media?per_page=100&page={page}"
        try:
            batch = json.loads(get(url).decode("utf-8"))
        except Exception as e:
            print("list error", page, e)
            break
        if not batch:
            break
        items.extend(batch)
        print(f"  page {page}: {len(batch)} items")
        page += 1
        if page > 20:
            break
    return items


def local_path(src):
    p = urllib.parse.urlparse(src).path.lstrip("/")
    return os.path.join(OUT, "files", *p.split("/"))


def fetch(item):
    src = item.get("source_url")
    if not src:
        return (item.get("id"), None, 0, "no source_url")
    dest = local_path(src)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return (item["id"], dest, os.path.getsize(dest), "cached")
    try:
        data = get(src)
        with open(dest, "wb") as f:
            f.write(data)
        return (item["id"], dest, len(data), "ok")
    except Exception as e:
        return (item["id"], dest, 0, f"FAIL {e}")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("listing media library...")
    items = list_media()
    print(f"{len(items)} media items")

    results = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, res in enumerate(ex.map(fetch, items), 1):
            results.append(res)
            if i % 40 == 0:
                print(f"  {i}/{len(items)}")

    by_id = {it["id"]: it for it in items}
    with open(os.path.join(OUT, "media-manifest.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "date", "title", "mime", "source_url", "local_file", "bytes", "status"])
        for mid, dest, size, status in results:
            it = by_id.get(mid, {})
            w.writerow([mid, it.get("date", ""),
                        (it.get("title", {}) or {}).get("rendered", ""),
                        it.get("mime_type", ""), it.get("source_url", ""),
                        os.path.relpath(dest, OUT) if dest else "", size, status])

    ok = sum(1 for r in results if r[3] in ("ok", "cached"))
    fail = [r for r in results if r[3].startswith("FAIL")]
    total = sum(r[2] for r in results)
    print(f"\ndownloaded {ok}/{len(results)} files, {total/1048576:.1f} MB")
    mimes = {}
    for mid, dest, size, status in results:
        m = by_id.get(mid, {}).get("mime_type", "?")
        mimes[m] = mimes.get(m, 0) + 1
    for m, n in sorted(mimes.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {m}")
    if fail:
        print("\nFAILURES:")
        for r in fail[:20]:
            print(" ", r)


if __name__ == "__main__":
    main()
