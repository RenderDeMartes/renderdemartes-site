# -*- coding: utf-8 -*-
"""First-frame posters for heavy GIFs, so a workflow page does not pull 39 MB on load."""
import io, json, os
from PIL import Image

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
SITE = _os.path.dirname(_HERE)   # site root is this folder's parent
TUT = os.path.join(SITE, "assets", "img", "tut")
THRESHOLD = 1_500_000          # gifs above this get click-to-play
MAXW = 1200

out = {}
for root, _, files in os.walk(TUT):
    for f in files:
        if not f.lower().endswith(".gif"):
            continue
        path = os.path.join(root, f)
        size = os.path.getsize(path)
        rel = os.path.relpath(path, SITE).replace("\\", "/")
        if size < THRESHOLD:
            continue
        im = Image.open(path)
        im.seek(0)
        frame = im.convert("RGB")
        w, h = frame.size
        if w > MAXW:
            frame = frame.resize((MAXW, round(h * MAXW / w)), Image.LANCZOS)
        poster = os.path.splitext(path)[0] + ".poster.jpg"
        frame.save(poster, "JPEG", quality=82, optimize=True)
        out[rel] = {
            "poster": os.path.relpath(poster, SITE).replace("\\", "/"),
            "bytes": size,
            "w": w, "h": h,
        }
        print(f"{size/1048576:6.1f} MB  {rel}")

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "posters.json"),
             "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print(f"\n{len(out)} posters written")
