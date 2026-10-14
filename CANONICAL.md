# Canonical decisions (binding for all OMD writers)

These were settled during extraction (≈250 videos read). Write the OMD to match them. Where
notes disagree, the OMD presents THIS as the default and records the alternatives in the
evolution log / ambiguity register with citations. Verify and cite each from notes/.

## Eras
E1 pre-bootcamp (2022–mid 2023) · E2 Boot Camp 1 & 2.0 (Jun–Oct 2023) · E3 Sep 2023–2024
(Sep 2023 strategy video, Jan 2024 daily-bias videos, Trading Transformation 2024) · E4 2025 ·
E5 2026 (Path to Profitability Jan 2026, 2026 tutorial yiuFUp0kFz8 May 2026, Jun 2026
strategy walkthrough 8PYgFVB0GHE, Oct 2026 confluence/bias videos, 2026 live streams) =
CANONICAL.

## Canonical model (E5)
Instruments: ES and NQ only (bot trades ES/MES; NQ needed as SMT/confirmation feed).
1. Pre-open: mark draws on liquidity (DOL): Asia (18:00–03:00 ET), London (03:00–08:30 ET),
   NY pre-market (08:30–09:30) highs/lows, previous-day high/low, 1H and 4H highs/lows,
   relative equal highs/lows, stacked "low-resistance" trend highs/lows, news-candle H/L.
   Drop levels already traded through. 5m/15m/1m levels are NOT significant sweeps.
2. Bias (for the first 60–90 min after open): from which significant DOL was swept (pre-market,
   London or at the open) and price reacting away from it, plus prior-session profile, plus
   which side has more/closer unswept DOL; HTF (4H/1H) order flow as context. ES and NQ must
   agree on 5m trend; if they "tell two different things" → no trade.
3. Sweep (opportunity) of a significant DOL — must trade through AND react (no reaction = not
   swept). If the HTF sweep happened pre-market/London, also wait for a 5m sweep after 09:30 ("2B").
4. Confirmation of order-flow change on 5m: BOS (candle BODY close strictly beyond most recent
   swing; wick/equal close ≠ BOS) OR IFVG (body close through the outermost with-trend FVG of a
   stack). SMT (ES vs NQ divergence at the swept level) strengthens bias & picks the index; it is
   never a trigger alone. 79% extension close (fib swing high→low; candle close beyond 0.79) = valid alternative
   confirmation/trigger when there is no gap to invert (E4–E5; tWYSAHQpywE@06:01, xxJyvmHROb4@20:57).
5. Continuation: retrace into a 5m FVG or EQ (50% of most recent swing leg, Gann box) of the new
   leg. Never enter on the touch. Order blocks and breaker blocks are DROPPED in E5 ("completely
   useless") — document as historical only.
6. Trigger: on 1m, the retrace must first break 1m structure against the new trend, then enter on
   the CLOSE of a 1m BOS or 1m IFVG back in the trade direction.
7. Time: no entries 09:30–09:50 (manipulation; ≤09:45 "too early"); primary window 09:50–10:10
   ("macro"), done by 10:30 ET if not in. No pre-market trades. No PM session in E5 (E3 had a PM
   model — historical).
8. Stop: beyond the invalidation — the 1m retrace swing / manipulation high-low (E5); the sweep
   extreme is the conservative alternative (E2–E4 default). No structural stop → no trade.
9. Targets: DOL ladder in trade direction — TP1 ≈1:1 at nearest liquidity (5m/session/hourly),
   then London/Asia/pre-market H/L, hourly H/L, 4H H/L / 4H FVG / PDH-PDL. Skip if TP1 < ~1:1.
   Take ~50% at TP1 and move stop to breakeven; scale the rest at later DOLs. Runner may be
   exited on 1m structure break / opposing IFVG+SMT. Done for the day when DOLs on both sides
   are taken or full TP hit.
10. SMT index choice (changed ~Jul 2025: "we always take the leading index. Before I used to take
    the lagging index" [5RWTzr1D994@56:46]; his "leading" = the one that failed to make the new
    extreme; pick on the EXECUTION timeframe [rBdlDQgSjIc@24:28]): trade the index that FAILED to make the new extreme (stronger for longs /
    weaker for shorts); confirmation must come from the index most opposed to the trade. E3–early
    E4 he traded the index that DID sweep — record as evolution. Exception seen: picks the index
    closer to its target.
11. Risk (bot rules, from his TEACHING, not his live behaviour): 1 trade/day typical, max 2;
    fixed risk per trade (1% default; he teaches 1–3%), daily budget split if 2 ideas; one win → done
    for the day [rBdlDQgSjIc@58:05]; stop after a loss or once the day's bias is completed; never a
    third impulsive trade. Half size on high-impact news days /
    unusually wide stops. His live streams show violations (3 trades, re-entries after big losses,
    no-stop prop "full ports") — document as NOT to be copied.
12. News (he said Sep/Oct 2025 "the boot camp is dated... some days I'm now willing to trade" [7a8tAGkVJac@01:41]): provide a NEWS_MODE switch. STRICT (E1–E3 teaching, recommended default): no trading on
    CPI, PPI, FOMC (day), NFP, Fed-chair speech days, US bank holidays; for other red-folder news
    wait until released (+15–30 min); 10:00 ET news → no trade before release. CURRENT (E5 practice):
    PPI after the open is traded; FOMC traded only at/after the 2 PM release (never FOMC morning);
    still no NFP day, no bank holidays; CPI is MIXED (skipped in late 2025 [2ZArg3kPPkE@02:19] but
    "full-ported" CPI in 2026 [4KzkQEM28tc; _zzxRMbyE44]); 10:00 releases → wait until out. Cite both.
13. Psychology → hard constraints: process over outcome; journal every trade/no-trade; never
    trade against bias; no revenge/FOMO; a "good loss" = all rules met.

## Known unresolved (put in ambiguity register with defaults)
- "Prominent/significant" swing has no numeric definition (he picks by eye) → propose a default
  (e.g., 1H/4H/session-level swings only; for 5m BOS use swings that bound the leg into the sweep).
- Exact stop size in points: rarely stated (E2: ES ~4–7 pt; one E5 student 200 NQ ticks).
- TP timeframe conflicts across eras.
- News handling changed across eras.
- Daily trade/loss limits in his practice vs teaching.
