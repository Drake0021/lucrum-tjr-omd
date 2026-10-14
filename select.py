"""Pick the transcript set from catalog/catalog.csv -> catalog/selection.csv."""
import csv, re
rows = list(csv.DictReader(open("catalog/catalog.csv", encoding="utf-8")))
for r in rows:
    r["tier"] = int(r["tier"]); r["rank"] = int(r["rank"]); r["duration_s"] = int(r["duration_s"])
RESCUE = re.compile(r"live trade|recap|breakdown|q ?& ?a|qna|when not to trade|win rate|knowledge|"
                    r"start day trading|learn how to day trade|teaching my friend|taught a beginner|"
                    r"market review|trading skill|blueprint|trade$|in one trade|myths|losing week", re.I)
TEACH = re.compile(r"how to|continuation|scalp|pm session|full take|wrong timeframe|married my bias|"
                   r"dumb mistakes|setup|full breakdown|exposed|smoked|students|fullport|cpi|fomc|news", re.I)
sel = []
for r in rows:
    if r["duration_s"] <= 0:
        continue
    if r["tier"] in (0, 1, 2, 4):
        sel.append((r, "auto"))
    elif r["tier"] == 9 and r["category"] == "other" and RESCUE.search(r["title"]):
        sel.append((r, "rescued"))
live = sorted([r for r in rows if r["tier"] == 3 and r["duration_s"] > 0], key=lambda r: r["rank"])
budget = 35 * 3600
picked = [r for r in live if TEACH.search(r["title"])]
rest = [r for r in live if r not in picked]
chosen, tot = [], 0
for r in picked + rest[::4] + rest[1::4]:
    if tot >= budget:
        break
    if r["duration_s"] > 3 * 3600:
        continue
    chosen.append(r); tot += r["duration_s"]
sel += [(r, "live_sample") for r in chosen]
seen, out = set(), []
for r, why in sel:
    if r["id"] in seen:
        continue
    seen.add(r["id"]); r = dict(r); r["why"] = why; out.append(r)
with open("catalog/selection.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
b = sum(r["duration_s"] for r in out if r["tier"] == 0) / 3600
o = sum(r["duration_s"] for r in out if r["tier"] != 0) / 3600
print(f"selected {len(out)} videos: bootcamp {b:.1f} h, other {o:.1f} h, total {b+o:.1f} h")
