"""Classify the TJR catalog and build the selection + coverage ledger.

Reads catalog/*.tsv (id, duration_s, title) and writes catalog/catalog.csv with
columns: id, rank (1 = newest upload), duration_s, title, playlists, category, tier.
Tiers: 0 = bootcamp (mandatory), 1 = core courses, 2 = strategy/education,
3 = live trading / recaps, 4 = psychology/risk, 9 = excluded (lifestyle/vlog/other).
"""
import csv
import glob
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog")


def read(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3 and p[0]:
                rows.append((p[0], int(float(p[1])) if p[1] not in ("NA", "") else 0, p[2]))
    return rows


videos = read(os.path.join(D, "videos.tsv")) + read(os.path.join(D, "streams.tsv"))
rank = {v[0]: i + 1 for i, v in enumerate(videos)}
info = {v[0]: v for v in videos}
pls = {}
for f in glob.glob(os.path.join(D, "pl_*.tsv")) + [os.path.join(D, "bootcamp.tsv")]:
    name = os.path.basename(f)[3:-4] if os.path.basename(f).startswith("pl_") else "Boot_Camp_user_link"
    for vid, dur, title in read(f):
        pls.setdefault(vid, set()).add(name)
        info.setdefault(vid, (vid, dur, title))
        rank.setdefault(vid, 9999)

LIFESTYLE = re.compile(r"weekend|day in the life|\bpov\b|vlog|lamborghini|rolls royce|bugatti|hellcat|"
                       r"\bvegas\b|miami|dubai|paris|ibiza|tropez|italy|greece|egypt|saudi|coachella|"
                       r"barths|puerto rico|nyc|los angeles|\bbet\b|bought|spent|giving away|"
                       r"music video|trailer|island|tattoo|lazy river|interview|christmas|memecoin|"
                       r"\blarp|swapped lives|week in|24 hours|48 hours|hours in|realistic day|regular day|"
                       r"compete|unboxing|car\b|house tour|mansion|watch collection", re.I)
STRATEGY = re.compile(r"explained|guide|strategy|concept|break of structure|\bbos\b|liquidity|fair value|"
                      r"\bfvg|ifvg|order block|equilibrium|\bsmt\b|bias|confluence|tutorial|price action|"
                      r"backtest|setup|entry|entries|market structure|time theory|session|imbalance|"
                      r"\bbpr\b|candlestick|timeframe|how to (trade|scalp|find|use|read|start)|full breakdown|"
                      r"model|killzone|news|cpi|fomc|nfp|continuation|take profit|stop loss|"
                      r"indicator|tradingview|analysis|framework|checklist|rules|lessons|advice", re.I)
LIVE = re.compile(r"live day trading|trade recap|market recap|index analysis|live trading|stream|"
                  r"setup .*\$|\$.* from one|one setup|in one day", re.I)
PSYCH = re.compile(r"psychology|mindset|discipline|emotion|risk|loss|losing streak|patience|fear|"
                   r"over ?confidence|funded|prop firm|payout|journal|habits|mistake", re.I)

out = []
for vid, (_, dur, title) in info.items():
    p = pls.get(vid, set())
    if p & {"Boot_Camp", "Boot_Camp_2.0", "Boot_Camp_user_link"}:
        cat, tier = "bootcamp", 0
    elif p & {"Path_To_Profitability", "Trading_Transformation"} or re.search(
            r"how to start day trading.*(full tutorial|9 hours)", title, re.I):
        cat, tier = "core_course", 1
    elif "Vlogs" in p or "Day_in_the_Life" in p or (LIFESTYLE.search(title) and not LIVE.search(title)):
        cat, tier = "lifestyle", 9
    elif LIVE.search(title) or "Trade_Recaps" in p:
        cat, tier = "live_or_recap", 3
    elif STRATEGY.search(title):
        cat, tier = "strategy_education", 2
    elif PSYCH.search(title):
        cat, tier = "psychology_risk", 4
    else:
        cat, tier = "other", 9
    out.append(dict(id=vid, rank=rank.get(vid, 9999), duration_s=dur, title=title,
                    playlists=";".join(sorted(p)), category=cat, tier=tier))

out.sort(key=lambda r: (r["tier"], r["rank"]))
with open(os.path.join(D, "catalog.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)

from collections import defaultdict
agg = defaultdict(lambda: [0, 0])
for r in out:
    agg[(r["tier"], r["category"])][0] += 1
    agg[(r["tier"], r["category"])][1] += r["duration_s"]
for k in sorted(agg):
    print(f"tier {k[0]} {k[1]:20s} {agg[k][0]:4d} videos {agg[k][1] / 3600:6.1f} h")
