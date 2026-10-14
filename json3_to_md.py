"""Convert a YouTube json3 caption file into a timestamped Markdown transcript.

Usage: python3 json3_to_md.py <in.json3> <out.md> <video_id> <title> <upload_date> <duration_s>
Groups words into ~30-second paragraphs, each prefixed with [mm:ss] / [h:mm:ss].
"""
import json
import sys


def ts(ms):
    s = int(ms // 1000)
    h, m, s = s // 3600, (s % 3600) // 60, s % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main():
    src, dst, vid, title, date, dur = sys.argv[1:7]
    data = json.load(open(src, encoding="utf-8"))
    paras, cur, cur_start = [], [], None
    for ev in data.get("events", []):
        segs = ev.get("segs")
        if not segs:
            continue
        start = ev.get("tStartMs", 0)
        text = "".join(s.get("utf8", "") for s in segs).replace("\n", " ").strip()
        if not text:
            continue
        if cur_start is None:
            cur_start = start
        cur.append(text)
        if start - cur_start >= 30000:
            paras.append((cur_start, " ".join(cur)))
            cur, cur_start = [], None
    if cur:
        paras.append((cur_start or 0, " ".join(cur)))
    words = sum(len(p[1].split()) for p in paras)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(f"---\nvideo_id: {vid}\ntitle: {title}\nupload_date: {date}\n"
                f"duration_s: {dur}\nurl: https://www.youtube.com/watch?v={vid}\n"
                f"words: {words}\n---\n\n")
        for start, text in paras:
            f.write(f"[{ts(start)}] {' '.join(text.split())}\n\n")
    print(f"{vid}: {words} words")


if __name__ == "__main__":
    main()
