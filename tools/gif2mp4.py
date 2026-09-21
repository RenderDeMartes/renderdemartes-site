# -*- coding: utf-8 -*-
"""Transcode the workflow GIFs to MP4 + WebM. A 13.8 MB GIF becomes ~400 KB of H.264."""
import io, json, os, subprocess
import imageio_ffmpeg
from PIL import Image

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
SITE = _os.path.dirname(_HERE)   # site root is this folder's parent
TUT = os.path.join(SITE, "assets", "img", "tut")
HERE = os.path.dirname(os.path.abspath(__file__))
MAXW = 1100


def run(args):
    return subprocess.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error"] + args,
                          capture_output=True, text=True)


def main():
    out = {}
    gif_bytes = vid_bytes = 0
    gifs = []
    for root, _, files in os.walk(TUT):
        for f in files:
            if f.lower().endswith(".gif"):
                gifs.append(os.path.join(root, f))
    gifs.sort()

    for i, path in enumerate(gifs, 1):
        rel = os.path.relpath(path, SITE).replace("\\", "/")
        size = os.path.getsize(path)
        gif_bytes += size
        base = os.path.splitext(path)[0]

        with Image.open(path) as im:
            w, h = im.size
            frames = getattr(im, "n_frames", 1)
        scale = f"scale={MAXW}:-2:flags=lanczos" if w > MAXW else "scale=trunc(iw/2)*2:trunc(ih/2)*2"

        mp4 = base + ".mp4"
        r = run(["-i", path, "-movflags", "+faststart", "-pix_fmt", "yuv420p",
                 "-vf", scale, "-c:v", "libx264", "-crf", "27", "-preset", "slow", "-an", mp4])
        if r.returncode != 0 or not os.path.exists(mp4):
            print(f"  FAIL {rel}: {r.stderr.strip()[:120]}")
            continue

        # poster: first frame, webp
        poster = base + ".poster.webp"
        if not os.path.exists(poster):
            with Image.open(path) as im:
                im.seek(0)
                fr = im.convert("RGB")
                if fr.width > MAXW:
                    fr = fr.resize((MAXW, round(fr.height * MAXW / fr.width)), Image.LANCZOS)
                fr.save(poster, "WEBP", quality=80, method=6)

        vsize = os.path.getsize(mp4)
        vid_bytes += vsize
        with Image.open(poster) as pim:
            pw, ph = pim.size
        out[rel] = {"mp4": os.path.relpath(mp4, SITE).replace("\\", "/"),
                    "poster": os.path.relpath(poster, SITE).replace("\\", "/"),
                    "w": pw, "h": ph, "frames": frames,
                    "gif_bytes": size, "mp4_bytes": vsize}
        print(f"  [{i:2d}/{len(gifs)}] {size/1048576:6.2f} -> {vsize/1048576:5.2f} MB  {os.path.basename(path)}")
        os.remove(path)

    # drop the old jpg posters, the webp ones replace them
    for root, _, files in os.walk(TUT):
        for f in list(files):
            if f.endswith(".poster.jpg") or f.endswith(".poster.webp") and False:
                os.remove(os.path.join(root, f))

    with io.open(os.path.join(HERE, "videos.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"\n{len(out)} clips: {gif_bytes/1048576:.1f} MB of GIF -> {vid_bytes/1048576:.1f} MB of MP4")


if __name__ == "__main__":
    main()
