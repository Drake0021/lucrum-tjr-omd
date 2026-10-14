Gaps flagged by writer B (must appear in §18 ambiguity register):
1. SMT index exceptions: traded NQ that DID sweep [8PYgFVB0GHE@37:25–43:04]; "wrong index" = HTF leader vs exec-TF leader [rBdlDQgSjIc@24:28]; "should have longed ES" [3SygD-YgZuQ@25:01]; Oct 2026 "took the one that set up first", no SMT [FBX-gtFGWyU@06:07].
2. SMT as confirmation in Sep–Nov 2025 [xRuMUvW3T7Q@02:14; BMyeYQIj_vU@09:25] vs 2026 "doesn't tell me to take a trade" [X8Ag7BWd9dg@10:59]. Default: never a confirmation.
3. Continuation step: 1m counter-break may substitute for 5m FVG/EQ retrace [8PYgFVB0GHE@26:15] (switch) vs default requiring both.
4. 2B rule explicit in E4 only; implied in E5 [8PYgFVB0GHE@44:17].
5. 79% extension anchoring only from tWYSAHQpywE@06:01 (inferred).
6. No numbers from TJR for: sweep reaction test, significant swing, equal-level tolerance ("50 cents" [yiuFUp0kFz8@2:22:52]; ~4 ticks counted as sweep [eEg0_zc8Hxg@45:12]), SMT time sync, min/max stop (2026 ES 16–35 ticks [hBnD6T1M4w8@11:45]).
7. TP1 < 1:1 skip is Boot Camp [5v4G4xJVKIQ@08:52]; E5 took a "pretty bad" R trade (29 May 2026). 50/25/25 split is BC2.0; E5 says only "partials".
8. Early exit on opposing IFVG+SMT (E5 [3SygD-YgZuQ@16:54; @23:10]) vs BC2.0 "take profit into levels" [6zXKK3Wrusg@11:00].
9. Holding after 10:30: managed to 11:11 [3SygD-YgZuQ@1:38:48]; 12:00 ET flatten is DEFAULT.
10. Entry edges: entries at 9:45 [L4xz2o23aPQ@05:02; _zzxRMbyE44] vs 9:41–9:43 "too early" [xxJyvmHROb4@12:24]. Default 09:50.
11. News: CPI skipped Sep 2025 [2ZArg3kPPkE@02:19] vs full-ported 2026; FOMC afternoon only [7a8tAGkVJac], no E5 PM rules; 08:30 spike cutoff example only (5 pt/5 min [065lMUrD_kg@12:26]).
12. Risk: 2026 practice fixed contracts, $30–40K risk/trade [C5zIaZzbbgM@51:01] vs 1% teaching; flip/re-entry after loss [3SygD-YgZuQ; rBdlDQgSjIc].
13. Counter-bias trades "let the market prove us wrong" [TEp3a-7GUds@39:03]; require SMT (DEFAULT from X8Ag7BWd9dg@11:32).
14. Session edges: London cut 08:30 vs runs to 11:30; NY end 17:00 vs 18:00 [yiuFUp0kFz8@2:05:03 vs @4:30:11]; day boundary 18:00 ET (inferred).
15. Announces seven DOL types, covers five [yiuFUp0kFz8@1:47:06].
16. ES/MES contract facts are CME facts — verify at deployment; single-lot → all out at TP1.
17. ES-only bot when canonical index is NQ: DEFAULT trade ES half size only if ES passes all steps; alternative SKIP.
Also: "one win → done" cite rBdlDQgSjIc@58:05 actually reads "there was not a thought behind that position" — re-check; may better support "never a third impulsive trade".

Gaps flagged by writer C (also for §18):
- "one win → done" correct cites: SHJHpedYh6A@4:49:02, kH-rbepWkNE@32:49, ZioWcbxSuIw@10:50, 5RWTzr1D994@1:01:24 (NOT rBdlDQgSjIc@58:05, which = no-thought third trade).
- 2026 fixed-contract sizing (risk floats 1–4%) [hBnD6T1M4w8@10:39–13:25] vs 1% equity; bot uses 1% equity sized from stop, cap 3%.
- Max-2-trades vs stop-after-loss → effectively 1 trade/day; REENTRY_MODE optional (0.5%+0.5%).
- BE timing varies: TP1 / TP2 [WlnpOPPnBQw] / after London or 5m lows [_zzxRMbyE44; rBdlDQgSjIc] / none (seek & destroy [p5CKu0FNbyg]); BE offset unstated (DEFAULT 1 tick).
- Partial %: 50/25/25 from 2023–25; 25% at TP1 once [-RAJEWMl-F0]; E5 unstated.
- Runner exit on 1m BOS against: yes [ss-dZPMnjeY@05:06] vs no [6zXKK3Wrusg@11:00]; DEFAULT only after a DOL tagged.
- News unclear: JOLTS-only, day before FOMC/NFP/CPI, government shutdown (avoided yet traded 15 Oct 2025). FOMC trades only after 2 PM → bot never trades FOMC day.
- Invented DEFAULT thresholds: chop, reaction gate, wide stop >9 pt, min stop 2 pt, runner flat 14:00 ET, 6% drawdown halt, MES switch <4 ES contracts, B-grade mode, rule-breach halt.
- Bias override resolved as state machine flipped only by sweep+SMT+5m confirmation.
- Stats credibility: "I GOT EXPOSED FOR FAKING TRADES" stream [L5eRg5BZOOY]; "no red month" vs −$26k month [L5eRg5BZOOY@14:49; 7a8tAGkVJac@25:37].
- Demo→live: ≥3 months profitable & >10% (per month or total?) [TwakmPZJGJA] vs 3 consecutive green months [NZqRbc_9u_I].
