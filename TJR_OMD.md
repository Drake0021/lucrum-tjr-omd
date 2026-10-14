# TJR One Massive Doc (OMD) — TJR's day-trading model, written for Lucrum SPX

**Version:** 1.0 · **Compiled:** 2026-10-14 · **Subject:** TJR (YouTube @TJRTrades)
**Instrument target:** ES / MES (CME E-mini and Micro E-mini S&P 500 futures). NQ is used as a correlation and confirmation feed.

---

## 0. How to use this document (instructions to the trading agent)

**What this is.** This is the only source of truth for how Lucrum SPX replicates TJR's model. It was compiled from the full transcripts of every TJR Boot Camp video (Boot Camp 1, Days 1–55, and Boot Camp 2.0), plus 100+ hours of his other content from 2022 to October 2026. Section 20 lists every source, with coverage totals.

**Which version of TJR you are replicating.** TJR's model changed a lot between 2022 and 2026. He has said himself that the Boot Camp is "dated" [7a8tAGkVJac@01:41] and that his older strategy videos are "pretty dated" [TEp3a-7GUds@01:06]. This document makes his **2026 model (era E5) canonical**. Earlier versions are kept only so you understand the history (§14) and can tell old teaching apart from current rules.

The Boot Camp still supplies the foundational definitions he continues to use: swings, break of structure, liquidity, FVG and equilibrium.

**How to read it.**
1. **Definitions** (§2–§7) are binding. Every rule elsewhere uses those terms exactly as defined.
2. **The trading procedure** is §8 (the model in order) and §16 (state machine and pseudocode). If prose and pseudocode disagree, stop and flag it. Do not guess.
3. **Hard constraints** are §10–§13: risk, management, no-trade filters and psychology. They override any signal.
4. **Discretionary points** are listed in §18, the ambiguity register. Wherever TJR uses judgement, the register gives a **DEFAULT (not TJR-stated)**. Use the default unless your operator configures something else, and log every time a default decides a trade.
5. **Test cases** are in §19, worked examples drawn from his real trades. Use them to check your implementation before trading.

**Citations.** `[video_id@mm:ss]` means `https://www.youtube.com/watch?v=video_id` at that timestamp. Every rule carries at least one citation. Anything marked *(inferred)* was deduced by the compiler, not said by TJR.

**Configuration switches you must expose:**
- **`NEWS_MODE`**:
  - `STRICT` (recommended default; his long-standing rule) skips CPI, PPI, FOMC and NFP days, Fed-chair speech days and US bank holidays.
  - `CURRENT` (his 2025–2026 practice) is more permissive.
  - See §12.
- **`RISK_PER_TRADE`, `MAX_TRADES_PER_DAY`, `DAILY_LOSS_LIMIT`.** Defaults are in §10. Follow his *teaching*, never his live-stream behaviour (§10, §15).
- **`STOP_MODE`**: `INVALIDATION_1M` (the E5 canonical stop) or `SWEEP_EXTREME` (conservative). See §11.

**Honest limits of this document.**
- TJR describes his 2026 model as a discretionary toolbox, and has said he deliberately leaves some details out [yiuFUp0kFz8@6:03:43]. No document can reproduce his judgement perfectly. This one turns every rule he states into an explicit, testable rule and makes every judgement call visible in §18.
- The sources are auto-generated captions. Charts he drew on screen were inferred from his narration, not seen directly.
- The performance figures here are TJR's own unaudited claims. **Nothing in this document shows the model is profitable.** Backtest it and paper trade it on Lucrum SPX before risking capital.

### Contents
1. Philosophy and core principles · 2. Glossary (operational definitions) · 3. Market structure · 4. Liquidity · 5. Time · 6. PD arrays and imbalances · 7. SMT divergence and index selection · 8. The full model, in order · 9. Master confluence list, ranked · 10. Risk management · 11. Trade management and exits · 12. No-trade filters · 13. Psychology as hard constraints · 14. Model evolution timeline · 15. Why it works (TJR's claims) · 16. Decision procedure (state machine and pseudocode) · 17. Applying it to ES/MES · 18. Ambiguity register · 19. Worked examples (test cases) · 20. Source index

---

## 1. TJR's trading philosophy and core principles

Each principle is followed by its machine consequence.

| # | Principle (TJR) | Bot consequence | Cites |
|---|---|---|---|
| P1 | Trading = "predicting where price … is going to go with a high probability on a daily basis"; money is a side effect. | Optimise rule adherence and expectancy, not daily P&L. No "need to make money today" logic. | [yiuFUp0kFz8@20:26–21:32; 8PYgFVB0GHE@04:30–05:02] |
| P2 | A strategy is "less about telling you … what trade to take and more about … what trades not to take." Fewer trades = fewer losses. | Default state is FLAT. Every gate must pass; any missing gate means no trade. "No setup" is a valid outcome ("a drop in the probability bucket"). | [8PYgFVB0GHE@05:38; @56:04; @03:58; xRuMUvW3T7Q@29:40] |
| P3 | Liquidity is "the goat of confluences … it begins and it ends with liquidity." The market cannot move without filling orders. | Every trade starts at a swept **significant** draw on liquidity (DOL) and ends at an opposing DOL. No DOL to aim at means no trade. | [crMqxB_nHhk@04:32; Vulini8xbB0@01:07; FBX-gtFGWyU@14:56] |
| P4 | Three-step logic: "potential for orders to be filled, confirmation that orders are filled, and then a continuation of the current trend that is now being created." | Hard sequence: **Sweep → order-flow change (5m) → continuation retrace (5m FVG/EQ) → 1m trigger**. Steps cannot be skipped or reordered. | [Zzk864cVJek@11:40; joe_XTCn5Bs@03:22; X8Ag7BWd9dg@04:57–08:15; yiuFUp0kFz8@6:24:36] |
| P5 | A sweep is an **opportunity, not a certainty**. Never sell just because a high was taken, or buy because a low was taken. | A sweep alone never opens a position. | [crMqxB_nHhk@30:43; pKIo-aVic-c@05:00; Xdu6j2E1DEI@12:13] |
| P6 | Every confluence needs a *reason* (orders filled, trend continuation). He rejects support/resistance, chart patterns, indicators as signals, and ICT extras (power of three, OTE, CHoCH). | Use only the E5 confluence set: liquidity, BOS, IFVG, FVG, EQ, SMT, 79% extension close. Indicators only to *mark* levels (e.g., session H/L). | [yiuFUp0kFz8@14:53; @2:46:26; @38:49; TEp3a-7GUds@41:46; 9ar85Y6-5P4@22:11] |
| P7 | No single confluence is tradable in isolation; "these confluences are literally nothing without context." | Each detector only emits state. Only the sequencer decides. | [xX5LTSJ5wwM@09:27; wzq2AMsoJKY@14:20; n97MKj6wGFk@08:48] |
| P8 | "Higher time frames hold higher power." A lower-timeframe break against the higher timeframe is usually just a retrace of the higher timeframe. | Significant DOLs are 1H/4H/session/PD levels. 5m/15m swings are only for LTF manipulation (2B) and execution. | [Vulini8xbB0@29:18; Y1lqifylC4s@07:47; 9ar85Y6-5P4@04:24] |
| P9 | Wait for candle closes; decide only on candles that have formed. | All detectors run on bar close. | [bEkbNGUzQME@16:43; ironJFzNBic@11:16] |
| P10 | Never enter on a touch, and never enter on the first impulsive move. Wait for the retrace and its confirmation. | Limit orders resting in zones are forbidden. Entries are market-on-close of the trigger bar. | [8PYgFVB0GHE@25:44; TEp3a-7GUds@31:40; FBX-gtFGWyU@11:38] |
| P11 | The bias is a working hypothesis. "Let the market prove you wrong." Don't marry the bias. | Bias can be overridden intraday by a full opposite sequence (sweep + SMT + confirmation). Bias is re-evaluated at each key level. | [TEp3a-7GUds@39:03; yiuFUp0kFz8@6:27:56; 9ar85Y6-5P4@34:42; xxJyvmHROb4 title "I married my bias"] |
| P12 | Price action is king, above news. | News is a filter on *whether* to trade (Part on news), never a directional signal by itself. | [Xdu6j2E1DEI@10:33; w5sUCqFH3Lg@22:30] |
| P13 | Trade the NY open only. Manipulation comes first, then the move. Done by 10:30. | Time gates (see time section of the OMD): sweep/manipulation 09:30–09:50, entries 09:50–10:10 ("macro"), hard stop 10:30. | [L4xz2o23aPQ@03:22–05:02; yiuFUp0kFz8@4:31:51–4:33:36] |
| P14 | Profitability = strategy + risk management + psychology (= discipline: follow the plan). Losses "are required … part of the strategy." | Risk and discipline rules are hard constraints, not advice (see risk/psychology parts). A losing trade that met every rule is a "good loss". | [yiuFUp0kFz8@5:29:44; xRuMUvW3T7Q@31:21; TEp3a-7GUds@00:33] |
| P15 | The strategy is a toolbox, not a rigid checklist. He sometimes uses 1m instead of 5m and leaves room for discretion. | The bot must NOT copy his discretion. It uses the fixed default (5m confirmation/continuation, 1m trigger) and logs his discretionary variants as excluded. | [TEp3a-7GUds@01:41; @13:54; yiuFUp0kFz8@5:52:37–6:04:49] |

---

## 2. Glossary with operational definitions

Format per entry: **(a) Definition (TJR)** · **(b) Machine rule** · **(c) Edge cases / invalidation** · **(d) Use now (E5) vs before** · **(e) Cites**.

### 2.1 Candle, close, timeframe stack
- **(a)** Body = open→close; wick = traded but not closed there. Only formed candles count [bEkbNGUzQME@16:43; yiuFUp0kFz8@48:22–59:30]. Charts on New York time [yiuFUp0kFz8@44:27].
- **(b)** `bull(c) := close>open`, `bear(c) := close<open`. A level L is "closed beyond" upward iff `close > L` (strict). Timeframes used: 4H, 1H (context/DOL), 5m (confirmation + continuation), 1m (trigger) [FBX-gtFGWyU@00:32; 8PYgFVB0GHE@20:08–23:29].
- **(c)** Single-candle reads (doji, hammer) are context only, never a signal [bEkbNGUzQME@11:25; @14:25].
- **(d)** Unchanged E2→E5.
- **(e)** [bEkbNGUzQME@02:48; yiuFUp0kFz8@48:22; FBX-gtFGWyU@00:32]

### 2.2 Swing high / swing low (two-candle rule, doji handling)
- **(a)** "A high is a two candlestick pattern: a move up then a move down, a green candle then a red candle", priced at the higher wick of the two. A low is the mirror (down candle then up candle, lowest wick). "It's not a move down then a move down" [X37Vg1wyk7E@14:26; Vulini8xbB0@05:00–05:33; pKIo-aVic-c@11:00; PmhuPbY8ZHo@04:25].
- **(b)** On timeframe T, after dropping dojis from the sequence:
  - Swing high at the pair (i, j) where j is the next non-doji candle after i: `bull(i) AND bear(j)`. Price `SH = max(high_i, high_j)`. It is confirmed when candle j closes.
  - Swing low at (i, j): `bear(i) AND bull(j)`. Price `SL = min(low_i, low_j)`. Confirmed at j's close.
  - Doji: a candle "so minuscule … you can't even identify the color", open ≈ close, is **ignored** when sequencing. A doji between the up and down candle is "the middleman" and the pattern still holds [4LERkD7z_w4@10:12–10:48; aobHuNcI1QM@1:54:28; n97MKj6wGFk@06:36].
  - **DEFAULT (not TJR-stated):** doji iff `|close−open| ≤ 0.1 × (high−low)` or `|close−open| < 1 tick`. When a doji sits inside a swing pair, include its wick in the max/min (inferred: the level is the extreme actually traded).
- **(c)** Two same-colour candles never form a swing, even if a wick sticks out [SHJHpedYh6A@1:32:39; 4LERkD7z_w4@03:57; n97MKj6wGFk@19:44]. A swing on the 1m may not be a swing on the 5m; evaluate on the timeframe being read [n97MKj6wGFk@20:17; jeewXSLHt2g@06:47]. No symmetry and no "bigger high" lumping [PmhuPbY8ZHo@01:39–04:58]. A forming candle is never part of a swing.
- **(d)** Identical E2→E5. E3 (TT) added explicit doji skipping.
- **(e)** [PmhuPbY8ZHo@04:25; 4LERkD7z_w4@10:12; n97MKj6wGFk@06:36; yiuFUp0kFz8@1:05:11; Vulini8xbB0@05:00]

### 2.3 Trend / order flow / consolidation
- **(a)** Uptrend = higher highs + higher lows (bullish order flow). Downtrend = lower highs + lower lows (bearish). Third state = consolidation (sideways). "Order flow is literally just trends" [z0czA_OSq5M@01:07–02:54; jeewXSLHt2g@01:08; yiuFUp0kFz8@1:04:02].
- **(b)** `trend(T)` = direction of the last BOS on T (§2.5). Quick read: "if the most recent high has been closed above and the most recent low has not been closed below, it is an uptrend" [jeewXSLHt2g@13:57]. The current trend **persists until a close beyond its protective swing** (uptrend: the most recent swing low; downtrend: the most recent swing high) [9ar85Y6-5P4@04:24; ironJFzNBic@04:39].
- **(c)** A higher low inside a downtrend, or a wick to a lower low inside an uptrend, does not change the trend [jeewXSLHt2g@08:27; n97MKj6wGFk@14:00]. Consolidation: many internal breaks. The relevant event is the *breakout* (close beyond range high/low), "a form of a break of structure, but a little bit different" (not elaborated) [n97MKj6wGFk@03:52; jeewXSLHt2g@01:08]. **DEFAULT (not TJR-stated):** classify T as consolidation when ≥3 BOS events in alternating directions occur within the last 24 bars of T. Treat consolidation as no-trade on that TF.
- **(d)** E5: 4H/1H order flow gives context for bias. 5m order flow is the execution trend [ironJFzNBic@02:21; z0czA_OSq5M@12:25]. E2: the daily trend was the bias [sjuWqKDsQtI@01:43].
- **(e)** [z0czA_OSq5M@01:07; 9ar85Y6-5P4@04:24; jeewXSLHt2g@13:57; n97MKj6wGFk@01:04]

### 2.4 Prominent / significant swing
- **(a)** E2: the swings that "matter most", picked by eye ("relatively easy"): a high that starts a big trend, a double top, a swing that broke daily structure [KtC2SbemF6w@03:28–05:08]. BC2 required a BOS to break a **prominent** swing, not a minor internal one [5v4G4xJVKIQ@01:42–03:22]. E5 never uses "prominent". He uses **"significant" draws on liquidity**: 1H/4H highs and lows, session highs and lows, PDH/PDL [Vulini8xbB0@27:36–29:52; TEp3a-7GUds@24:54; 8PYgFVB0GHE@16:49]. For BOS he says simply the **most recent** swing [Zzk864cVJek@02:50; n97MKj6wGFk@14:35; TYbpk7WogHI@15:01].
- **(b)** E5 bot rule:
  1. **Significant swing (for sweeps / DOLs)** = any level in the DOL catalogue §4.1 (1H/4H swing H/L, session H/L, PDH/PDL, relative equal H/L, stacked trend H/L, data H/L, opening gaps). 5m/15m/1m swings are **never** significant [Vulini8xbB0@29:18].
  2. **Swing for the 5m confirmation BOS** = the most recent confirmed 5m swing on the opposite side. **DEFAULT (consistent with TJR, not a numeric rule):** for a bullish confirmation after a low sweep, use the most recent 5m swing high that formed *before* the sweep extreme ("the high that led into the lows being taken" [Xdu6j2E1DEI@14:58]); mirror for bearish.
- **(c)** No numeric threshold exists in any era. OPEN (ambiguity register).
- **(d)** E2 prominent filter → E5 replaced by (i) significance of the swept level and (ii) "most recent swing" for BOS.
- **(e)** [KtC2SbemF6w@03:28; 5v4G4xJVKIQ@03:22; Vulini8xbB0@29:18; Xdu6j2E1DEI@14:58; Zzk864cVJek@02:50]

### 2.5 Break of structure (BOS) = change in order flow = MSS
- **(a)** "BOS = change in order flow = change in trend = change in structure; all of those are literally the same exact thing" [jeewXSLHt2g@00:00–00:34]. Bearish BOS: in an uptrend, a candle **body closes below the most recent low**. Bullish BOS: in a downtrend, a body closes above the most recent high [yiuFUp0kFz8@2:35:49–2:36:23; 8PYgFVB0GHE@26:50–28:32].
- **(b)** State: `trend ∈ {up, down, none}`, `watch_low`, `watch_high`.
  - In `up`: on each newly confirmed swing low, set `watch_low := that low` (even if its wick is lower than the previous one) [jeewXSLHt2g@15:04; n97MKj6wGFk@14:00–15:09]. Fire **bearish BOS** at the first completed candle with `close < watch_low`. Then set `trend := down` and `watch_high :=` most recent confirmed swing high.
  - In `down`: mirror (`close > watch_high`).
  - A break *in* the trend direction (close above a high in an uptrend) is **not a BOS** ("not even a real thing"). It is continuation, and only updates swings [8PYgFVB0GHE@26:15; n97MKj6wGFk@11:06].
- **(c)** Wick through = not a BOS, "however far it goes", even three wicks in a row. Body **equal** to the level = not a BOS [Zzk864cVJek@04:29–08:20; jeewXSLHt2g@15:39; n97MKj6wGFk@21:59]. A wick through a level is usually a liquidity sweep [PmhuPbY8ZHo@12:21]. A huge news candle is judged by the same close logic [jeewXSLHt2g@12:53]. A BOS against the next-higher TF's trend is usually that TF's retrace [Y1lqifylC4s@07:47; 9ar85Y6-5P4@04:24]. A BOS is never an entry by itself [jeewXSLHt2g@11:46].
- **(d)** E5: a **confirmation confluence** (step 2 on 5m, trigger on 1m), interchangeable with IFVG; use whichever prints first [BdBxXKGWVjk@13:18; TEp3a-7GUds@27:45]. E2: BOS of a prominent swing, followed by a third confirmation. E1/BC1 early: enter on the BOS close (retired) [PyCPHiO2nj0@02:10].
- **(e)** [PmhuPbY8ZHo@07:47; Zzk864cVJek@06:07; jeewXSLHt2g@00:34; 8PYgFVB0GHE@26:50; yiuFUp0kFz8@2:38:03]

### 2.6 CHoCH (change of character): rejected
- **(a)** "I do not trade based off of change of character, I think it's kind of dumb" [aOldFdtKsVc@07:33]. He does not know ICT's CHoCH vs BOS distinction; he looks for "change of trend" [M6DQKMp-3Vo@41:57]. CHoCH appears once in E2 as a loose synonym of a LTF BOS [S1kY3Fw6JUQ@07:57]. The term is absent from the 2026 series [yiuFUp0kFz8 note: never mentioned].
- **(b)** Do **not** implement a separate CHoCH/internal-vs-external structure state. The first BOS against the trend *is* the change of order flow (§2.5).
- **(c)** Do not import ICT CHoCH/MSS semantics from other sources.
- **(d)** Rejected E1→E5.
- **(e)** [aOldFdtKsVc@07:33; M6DQKMp-3Vo@41:57; jeewXSLHt2g@00:00; Zzk864cVJek@01:42]

### 2.7 Change of order flow (confirmation confluence)
- **(a)** "How are orders filled? Through liquidity sweeps. How can we confirm that they're filled? Through inverse fair value gaps and break of structure" [9ar85Y6-5P4@22:11; X8Ag7BWd9dg@05:30]. Order flow is "disrespected" by a BOS, an IFVG, or a close beyond the 79% extension [z0czA_OSq5M@03:28–07:32].
- **(b)** `OF_change(dir, T)` fires on the first completed T-candle that produces any of: BOS(dir) §2.5; IFVG(dir) §2.18; 79%-extension close(dir) §2.23. Required on **5m** after the sweep (step 2) and on **1m** for the trigger (step 4). One is enough: "each one of these confluences signifies the same thing" [xRuMUvW3T7Q@02:14–03:18].
- **(c)** SMT is **not** an order-flow change in E5: "It doesn't tell me to take a trade … An SMT divergence means nothing until we get proper confirmations" [X8Ag7BWd9dg@10:59; @25:59]. (E4 listed SMT as one of four confirmations [8QDDxwUV1KM@11:00; xRuMUvW3T7Q@02:14]. History, recorded in the register.) "If no FVG in the leg to invert, wait for BOS" [TEp3a-7GUds@28:19].
- **(d)** E5 = {BOS, IFVG, 79%}. E2 = {BOS (prominent)}. E3 = BOS, with IFVG as an add-on.
- **(e)** [9ar85Y6-5P4@22:11; X8Ag7BWd9dg@05:30; z0czA_OSq5M@03:28; 8PYgFVB0GHE@20:08; tWYSAHQpywE@06:01]

### 2.8 Liquidity; buy-side (BSL) / sell-side (SSL)
- **(a)** "Resting orders" above highs and below lows. Above a high sit two sets of buy orders: breakout buyers and short-sellers' stops (= BSL). Below a low sit two sets of sell orders: breakdown sellers and longs' stops (= SSL). Market makers push price into these to fill size against them ("reverse psychology") [crMqxB_nHhk@11:15–23:19; Vulini8xbB0@07:14–15:31; AMlev-gYyHo@23:10].
- **(b)** BSL level = a swing-high price (§2.2) or catalogue level (§4.1) above current price. SSL = the same below. Every BSL/SSL object carries `{price, tf, type, created_ts, swept:bool, swept_ts, reacted:bool}`.
- **(c)** Liquidity is fractal (monthly → 1m), but only §4.1 levels are tradable sweeps [AMlev-gYyHo@14:38; Vulini8xbB0@29:18].
- **(d)** Unchanged in meaning E2→E5. E5 narrows which levels count.
- **(e)** [crMqxB_nHhk@09:34; Vulini8xbB0@07:14; rdz6vnXb8wE@02:12; AMlev-gYyHo@23:10]

### 2.9 Draw on liquidity (DOL) and DOL types
- **(a)** The liquidity price is drawn to: "Price moves towards draws on liquidity. That's the only way that price moves" [FBX-gtFGWyU@14:56]. Each DOL is both an **entry point** (sweep → reversal) and an **exit point** (target) [AGmAVyAuBE0@33:16; pKIo-aVic-c@21:18].
- **(b)** Types (full table with exact rules in §4.1): session H/L (Asia, London, NY pre-market), PDH/PDL, 1H/4H highs/lows, relative equal H/L, low-resistance (stacked trend) H/L, data (news-candle) H/L, NDOG/NWOG, market-open high/low and 30m lows (minor). He says "seven" types but lists five [AGmAVyAuBE0@00:45; yiuFUp0kFz8@1:47:06].
- **(c)** A DOL already traded through **without a reaction** is "pretty useless": remove it [TEp3a-7GUds@22:04; 8QDDxwUV1KM@09:23; xRuMUvW3T7Q@10:55]. Price "doesn't necessarily need to go all the way" to the farthest DOL [FBX-gtFGWyU@04:24].
- **(d)** E5 adds data H/L, NDOG/NWOG and low-/high-resistance to the E2 list (swings, sessions, pre-market, prior-week NY highs).
- **(e)** [AGmAVyAuBE0@00:45–51:55; Vulini8xbB0@27:36; FBX-gtFGWyU@03:18; 8PYgFVB0GHE@16:49]

### 2.10 Liquidity sweep (manipulation): reaction requirement, "2B"
- **(a)** Price pushes above a high or below a low, triggers the resting orders, then reverses [crMqxB_nHhk@22:10; Vulini8xbB0@01:07]. **Validity needs a reaction**: "If price comes down and takes out a low and keeps going down, is it a liquidity sweep? No. Because it's not reacting to it" [pKIo-aVic-c@16:26]. "Do we get a reaction? … If no reaction, liquidity has not been swept" [AMlev-gYyHo@24:50–25:58].
- **(b)** For a level L (BSL; mirror for SSL), on the 1m/5m feed:
  1. `trade_through`: some candle's `high > L` (wick or close both qualify for the take-out; no minimum depth stated) [UPA9LQW7phk@10:49; KtC2SbemF6w@13:02].
  2. `reaction`: TJR's words are "a strong candle against the run (a 'big' down candle off the highs)" [AMlev-gYyHo@26:35]. **DEFAULT (not TJR-stated):** reaction = within 6 × 5m bars after the trade-through, a 5m candle closes back below L **and** price does not reach the next BSL in the catalogue first.
  3. `valid_sweep(L) := trade_through ∧ reaction`. It becomes **actionable** only when the 5m order-flow change (§2.7) follows [pKIo-aVic-c@18:03].
  - **Step "2B"** (his checklist label, *not* the classic Sperandeo 2B pattern, inferred): IF the significant sweep (and its reaction) occurred **before 09:30** (pre-market from 08:30, London, or previous session), THEN after 09:30 also require a **5m manipulation**: a sweep of a 5m high (for shorts) or 5m low (for longs) that does **not** close-break the 5m trend set by the confirmation. IF the significant sweep happens at/after the open, skip 2B [xRuMUvW3T7Q@03:51–06:35; 8QDDxwUV1KM@16:03–19:25; 9ar85Y6-5P4@11:07–12:47].
- **(c)** Invalidation: price later trades/closes back beyond the swept extreme → sweep failed, idea dead (E2 stop logic [1FunNCUw_jM@01:41]; E5 order flow persists until a close beyond the protective high [9ar85Y6-5P4@04:24]). Near news, require a full take-out, not a tap [G7eq6U8e3yw@02:13]. Sweeps of 5m/15m levels do not start a trade (only 2B or continuation) [Vulini8xbB0@29:18; e_FV0Q14k8E@21:22]. A pre-market sweep "already reacting" = "the liquidity sweep for the day" [pKIo-aVic-c@18:36–19:08].
- **(d)** E5: step 1 of every trade. Pre-market sweeps count (with 2B). E2: sweep + BOS (+ third confirmation) inside a marked HTF zone; sweep "wick or close both acceptable".
- **(e)** [pKIo-aVic-c@16:26; AMlev-gYyHo@24:50; xRuMUvW3T7Q@03:51; 8QDDxwUV1KM@16:03; 8PYgFVB0GHE@17:55]

### 2.11 Manipulation
- **(a)** "Price pushes above a high or below a low", giving the market "the opportunity" to fill opposite orders and reverse. It is the same thing as a liquidity sweep [8PYgFVB0GHE@17:55–20:08; @35:50; Xdu6j2E1DEI@07:47]. "I am only trying to trade off of manipulation" [e_FV0Q14k8E@03:53]. New money at each session open manipulates the prior session's H/L [AGmAVyAuBE0@04:15].
- **(b)** `manipulation := valid_sweep` (§2.10). Time window for NY: **09:30–09:50** ("manipulation time frame"; sometimes 09:30–09:40) [L4xz2o23aPQ@03:22–05:02]. **HTF manipulation** = sweep of a §4.1 significant level. **LTF manipulation** = sweep of a 5m (lowest he goes) high/low, used only for 2B/continuation [9ar85Y6-5P4@11:07–12:47]. The "manipulation high/low" = the extreme of the sweep, used as a stop reference (stop rules live in the risk part).
- **(c)** "Ideally we don't take a trade within the first 10–15 minutes"; the first minutes are manipulation [9ar85Y6-5P4@18:52]. Manipulation can finish late (09:52) [L4xz2o23aPQ@08:56].
- **(d)** E5 term of choice. E2 called it "liquidity sweep / London fake-out / inducement".
- **(e)** [8PYgFVB0GHE@17:55; L4xz2o23aPQ@03:22; 9ar85Y6-5P4@11:07; e_FV0Q14k8E@03:53]

### 2.12 External vs internal liquidity (market cycle)
- **(a)** "Price is always either looking to take out external liquidity, which is … highs and lows, or fill imbalances, which is internal liquidity" [AGmAVyAuBE0@51:22; yiuFUp0kFz8@2:31:15]. Uptrend cycle: high (external) → retrace into FVG/EQ (internal) → new high → … [ironJFzNBic@24:51–25:58; yiuFUp0kFz8@5:23:30]. "Internal and external liquidity … is literally just order flow" [z0czA_OSq5M@18:05–19:48].
- **(b)** `external` = §4.1 swing/session/PD levels. `internal` = FVG/EQ/NDOG/NWOG/BPR of the current leg. HTF phase on T: `extending` if price has left the last internal zone toward an external target, `retracing` if price is in/approaching the leg's FVG/EQ. Bias logic uses this (bias part).
- **(c)** After a continuation zone reacts, expect the next external level to be taken. If the zone is inverted, the phase flips [ironJFzNBic@02:21; @08:30].
- **(d)** Explicit from E4 (Feb 2025) onward. E2 had "retracement vs extension" (trade only the extension) [Y1lqifylC4s@08:52].
- **(e)** [AGmAVyAuBE0@51:22; ironJFzNBic@24:51; z0czA_OSq5M@18:05; yiuFUp0kFz8@5:23:30]

### 2.13 Session highs/lows
- **(a)** The highest/lowest price of each session window. Each new session's money manipulates the previous session's high or low, then targets the opposite one. "It doesn't happen every single day" [AGmAVyAuBE0@04:15–14:04; yiuFUp0kFz8@1:51:36].
- **(b)** Windows (ET, E5): **Asia 18:00–03:00**, **London 03:00–08:30**, **NY pre-market 08:30–09:30**, NY session 09:30–17:00; 17:00–18:00 = "spread hour" [L4xz2o23aPQ@00:33–02:15; Vulini8xbB0@31:02–32:09; yiuFUp0kFz8@4:30:44]. Level = max(high) / min(low) of all bars with open time in the window. **DEFAULT (not TJR-stated):** use the extreme wick price as the level (E2 marked "body-to-wick zones" [OH--4nkbXlM@02:23]; E5 says only "highest point").
- **(c)** London "technically" runs to 11:00/11:30 NY; he ends it at 08:30 [L4xz2o23aPQ@01:09; Vulini8xbB0@31:02]. Contradiction: one E4 video gives pre-market from 08:00 [e_FV0Q14k8E@16:56]. Canonical = 08:30.
- **(d)** E5: core DOLs, both sweep levels and targets. E2: mostly for the forex strategy; for ES, pre-market lows as TP1.
- **(e)** [L4xz2o23aPQ@00:33; AGmAVyAuBE0@11:08; Vulini8xbB0@31:02; 8QDDxwUV1KM@03:54]

### 2.14 News-candle (data) high/low
- **(a)** "Data highs/lows": the high and low of the candle(s) printed at a high-impact (Forex Factory red folder) release, e.g., CPI/PPI/claims at 08:30, ISM at 10:00. Treated as a DOL [AGmAVyAuBE0@44:23–47:51; 2ZArg3kPPkE@00:00]. FOMC decision move high = "data highs" [7a8tAGkVJac@23:18]. "Advanced advanced", not used often [Vulini8xbB0@27:36].
- **(b)** On release time t_r: `data_high = high`, `data_low = low` of the candle opening at t_r. **DEFAULT (not TJR-stated):** use the **5m** candle opening at t_r. Store as type `DATA` and treat it like a session level.
- **(c)** His own examples were weak ("you're going to have to take my word for this") [yiuFUp0kFz8@2:25:08]. The candle timeframe is never stated.
- **(d)** New in E4–E5. Absent from E2.
- **(e)** [AGmAVyAuBE0@44:23; 2ZArg3kPPkE@00:00; 7a8tAGkVJac@23:18; Vulini8xbB0@27:36]

### 2.15 Opening gaps (NDOG / NWOG / new-candle gap)
- **(a)** **NDOG** = gap between the prior day's close (17:00 candle) and the new day's open (18:00). **NWOG** = gap between Friday's close and Sunday's open. Price "more often than not" seeks them out. Not required to fill, but treated as strong DOLs. **New candle opening gap** (close-to-next-open within session) = "pretty freaking useless" [PlsHO33j6B8@01:10–11:49; yiuFUp0kFz8@3:16:47–3:28:04].
- **(b)** `NDOG = [min(C_close, O_open), max(C_close, O_open)]`, where C = last bar before 17:00 and O = first bar at 18:00. NWOG: same with Friday's last bar and Sunday's first bar. Gap is "filled" when price trades through the far edge. Use as a **target** when price is away from it, or as a continuation **entry zone** inside it.
- **(c)** He doesn't trade Asia-session NDOG trades; NDOGs usually fill in Asia [PlsHO33j6B8@07:51]. An NWOG unfilled by Monday's NY open is "a very, very good target" [PlsHO33j6B8@10:43]. If an NWOG is filled, that changes context (he used NWOG fills as a reason for bias shifts [A3RNBK_7gcM; -RAJEWMl-F0]).
- **(d)** New in E4–E5 (NWOG named as a DOL in Oct 2026 bias video [FBX-gtFGWyU@17:09]). Absent from E2.
- **(e)** [PlsHO33j6B8@02:51; yiuFUp0kFz8@3:18:28; FBX-gtFGWyU@17:09; IVqY3b-KEbA (NDOG objective)]

### 2.16 Fair value gap (FVG) / imbalance
- **(a)** A three-candle pattern with an expansionary middle candle. Bullish FVG = gap between candle-1 **high** and candle-3 **low**. Bearish = candle-1 **low** to candle-3 **high**. Only wicks matter. Colours of candles 1 and 3 don't matter, only candle 2's direction does. Overlapping wicks = no FVG. "FVG = imbalance": a range lacking opposite orders [xX5LTSJ5wwM@02:15–11:17; xcDOMKaOIsk@01:39–07:15; S1kY3Fw6JUQ@05:09].
- **(b)** For consecutive completed candles c1, c2, c3 on T:
  - Bullish: `bull(c2) AND low(c3) > high(c1)` → zone `[high(c1), low(c3)]`.
  - Bearish: `bear(c2) AND high(c3) < low(c1)` → zone `[high(c3), low(c1)]`.
  - Equality (touching wicks) = no FVG (strict inequality; inferred from "overlap").
  - Object: `{dir, top, bottom, tf, leg_id, created_ts, state}`, with state ∈ {active, tapped, invalidated→IFVG, balanced/deleted}.
- **(c)** Size: "tiny FVGs are as valid as large ones" [xcDOMKaOIsk@08:56–11:16] (contradicts E3 BPR advice to prefer big displacement candles [TihRnXjqM5c@05:15]). Candle 3 with no wick still counts [xcDOMKaOIsk@12:25]. FVGs are **continuation** tools only, never reversal tools [S1kY3Fw6JUQ@02:53; xX5LTSJ5wwM@06:09]. Price has no obligation to fill them [xX5LTSJ5wwM@30:11].
- **(d)** E5: one of two continuation confluences (step 3 zone on 5m). E2: zone and third-confirmation option ("more of a confirmation rather than an entry" [qecF411R83s@15:54]).
- **(e)** [xX5LTSJ5wwM@02:15; xcDOMKaOIsk@01:39; yiuFUp0kFz8@2:46:26–2:57:03; S1kY3Fw6JUQ@05:09]

### 2.17 Stacked FVGs; FVG invalidation; FVG deletion
- **(a)** **Stacked** = two or more same-direction FVGs in one leg "without a different candlestick in between" (no opposite/retrace candle). They are "treated as one" imbalanced range, and all are valid [BdBxXKGWVjk@10:00–10:35; xX5LTSJ5wwM@18:07–20:24]. **Invalidation ("disrespected")** = a candle **close** beyond the far edge (bullish FVG: close below its bottom; bearish: close above its top). A wick through does not count [xX5LTSJ5wwM@15:47–17:30; rMkghkG-ZjE@01:08]. **Deletion**: once price retraces (into the stack or not) and then makes a new extreme beyond the leg's swing, all that leg's FVGs are spent. "Never extend old FVGs forward"; FVGs apply "only within the current trend" [xX5LTSJ5wwM@19:15–31:54; yiuFUp0kFz8@3:03:48–3:15:39].
- **(b)**
  - `stack_id`: assign consecutive same-direction FVGs to one stack until an opposite-colour candle prints. Stack range = union of member zones.
  - `invalidate(fvg)` when a completed candle closes beyond `bottom` (bull) / `top` (bear).
  - A close through an upper member of a bullish stack does **not** end the trend while a lower member holds and structure is not broken [xX5LTSJ5wwM@20:24; ironJFzNBic@14:41].
  - `delete(leg)` when price prints a new swing extreme beyond the leg's high (bull) / low (bear) after any retrace. Also delete every FVG price never retraced into before that new extreme. "Balanced price action" rule: after the retrace low and a push past the prior high, ignore all zones below that retrace low [xcDOMKaOIsk@32:18–35:01].
  - A later retrace into an old, deleted gap is a liquidity event, not an FVG reaction [xX5LTSJ5wwM@26:46].
- **(c)** A retrace resets the cycle: only FVGs of the new leg count for the stack rule [xcDOMKaOIsk@37:13]. Partial fills: E2 kept only the untouched remainder live [qecF411R83s@11:59]. **DEFAULT (not TJR-stated):** keep the original edges for invalidation and record `max_penetration` for analytics. The E5 FVG used as continuation can be "filled but invalidated" → no trade off it [8QDDxwUV1KM@33:58].
- **(d)** E5 makes these lifecycle rules explicit. E2 only had "trades fully through = dead" [qecF411R83s@09:09].
- **(e)** [BdBxXKGWVjk@10:00; xX5LTSJ5wwM@17:30; @24:54; xcDOMKaOIsk@32:18; yiuFUp0kFz8@3:00:24]

### 2.18 Inverse FVG (IFVG)
- **(a)** "A fair value gap that gets disrespected within the current trend that it's in". A with-trend FVG closed through = a change of order flow, "as a break of structure". Named by its **new** direction (bullish FVG inverted = bearish IFVG). It often prints before the BOS, so it gives an earlier entry and a tighter stop; he uses it "almost more than break of structure" [4sRDnVmLcMk@05:03–11:28; BdBxXKGWVjk@02:44–04:23; yiuFUp0kFz8@3:43:53–3:50:37].
- **(b)** `IFVG_bear` fires on the first completed candle (the next candle "or really any candle after") with `close < bottom` of the **outermost-holding** bullish FVG of the current with-trend stack (= the **lowest** gap of a bullish stack). `IFVG_bull`: `close > top` of the **highest** gap of a bearish stack [BdBxXKGWVjk@10:35–12:45; 4sRDnVmLcMk@15:27–18:17; xcDOMKaOIsk@28:58–31:47]. Close strictly beyond; a close inside the gap or a wick through = nothing [4sRDnVmLcMk@09:11; @20:40].
- **(c)** Context required: valid as confirmation only after a sweep of a significant DOL ("every single one of these examples … has been coming off of a liquidity sweep"). Don't flip trend just because some FVG failed [BdBxXKGWVjk@05:31–06:37; @13:50]. "IFVGs do not need to be filled at all"; no retest required [xcDOMKaOIsk@27:53]. If a BOS prints before any IFVG, use the BOS [BdBxXKGWVjk@13:18]. If there's no FVG in the leg, wait for BOS or the 79% close [TEp3a-7GUds@28:19; tWYSAHQpywE@06:01]. A continuation FVG that gets inverted makes the continuation "bunk" and signals the other way [X8Ag7BWd9dg@09:20].
- **(d)** E5: primary confirmation (5m) and trigger (1m); also a bias-flip tool on 1H/4H [ironJFzNBic@08:30]. E4 Feb 2025: "equal to break of structure" [xcDOMKaOIsk@23:28]. E3 May 2024: "a pretty made up concept", used only as a close-through trigger after bias+sweep+BOS [rMkghkG-ZjE@00:34; @08:03]. E2: absent.
- **(e)** [4sRDnVmLcMk@05:03; BdBxXKGWVjk@02:44; xcDOMKaOIsk@23:28; yiuFUp0kFz8@3:57:35; rMkghkG-ZjE@00:34]

### 2.19 Equilibrium (EQ), premium, discount
- **(a)** The 50% level of the **most recent** swing range, drawn with a Gann box (levels 0, 0.5, 1 only). Uptrend: most recent swing low → most recent swing high; below 50% = discount (buy zone). Downtrend: most recent swing high → most recent swing low; above 50% = premium (sell zone) [wzq2AMsoJKY@01:06–07:09; joe_XTCn5Bs@01:10–06:46; TYbpk7WogHI@11:06–13:20; -E7plUbSJUk@03:24].
- **(b)** Leg of the new 5m trend after confirmation (short case; mirror for long): `A` = most recent swing high (initially the manipulation high), `B` = lowest low since the order-flow change. B is **defined only after the first opposite (up) candle prints** [joe_XTCn5Bs@12:55–13:28; TEp3a-7GUds@30:00; wzq2AMsoJKY@06:04]. `EQ = (A+B)/2`. Premium = price ≥ EQ. Discount = price ≤ EQ. **Re-anchor** B whenever a new low forms before EQ is reached. Never anchor to an older swing when newer ones exist [wzq2AMsoJKY@06:38; yiuFUp0kFz8@4:04:20; -E7plUbSJUk@06:46]. `EQ_hit` = any wick touches or "pokes its head" beyond EQ, "even barely" [joe_XTCn5Bs@08:30–09:35].
- **(c)** EQ alone is "completely and utterly useless … without correct context" [joe_XTCn5Bs@08:30; yiuFUp0kFz8@4:08:16]. After EQ is hit, the entry still needs a LTF BOS/IFVG [wzq2AMsoJKY@08:51]. Invalidation of the EQ continuation: see §6.3 (ambiguity: "we close above equilibrium … that invalidates step number three" [xRuMUvW3T7Q@22:35]). He frequently says "discount" for a short zone (slip). The bot uses the standard meaning [wzq2AMsoJKY@16:32; Y1lqifylC4s@11:12].
- **(d)** E5: one of the two continuation confluences; it replaces OB and breaker ("when order blocks get filled, what else is typically getting filled? Equilibrium") [X8Ag7BWd9dg@14:18–14:50]. E2: zone filter; an EQ-only entry needed a close back beyond EQ plus a BOS [4FEty6xgOc0@04:25–04:59].
- **(e)** [wzq2AMsoJKY@01:06; joe_XTCn5Bs@08:30; yiuFUp0kFz8@3:59:50–4:13:16; TYbpk7WogHI@11:06; -E7plUbSJUk@06:46]

### 2.20 BPR / illiquid price range
- **(a)** E5 (TJR's own definition): "an imbalanced price range with a swift move up through it followed by a swift move back down through it (or vice versa)". The whole range is then treated as imbalanced. When price re-enters it, expect it to traverse "just as swiftly" to the other end. When price breaks the high/low bordering it, expect a "rapid fire" move through it [PlsHO33j6B8@12:24–16:26; yiuFUp0kFz8@3:28:04–3:38:12; rBdlDQgSjIc (illiquid price ranges)]. E3 (ICT-style): the overlap of a bullish FVG that was disrespected and a later opposing bearish FVG, shrunk to the overlap only [TihRnXjqM5c@03:00–09:30].
- **(b)** **DEFAULT (not TJR-stated) operationalization:** BPR zone = intersection of an FVG stack S1 (dir d) that was later invalidated, and the opposing FVG stack S2 (dir −d) created by the move that invalidated it. If S2 fully contains S1 or vice versa, use the smaller one [TihRnXjqM5c@14:36]. The E5 "illiquid range" = union(S1, S2), used **only as a target** (far edge) once price re-enters it or breaks its bordering swing.
- **(c)** "Not make or break" [TihRnXjqM5c@15:53]. Low priority; never a sweep level; never a standalone entry.
- **(d)** E3: tie-breaker between candidate FVGs. E5: target/continuation heuristic.
- **(e)** [PlsHO33j6B8@12:24; yiuFUp0kFz8@3:28:04; TihRnXjqM5c@03:00; @16:27]

### 2.21 Order block (OB): HISTORICAL, dropped in E5
- **(a)** E2: "All an order block is, is that move up that causes the liquidity sweep": the leg into the swept extreme just before the opposite BOS [qhuFg_OXdmE@03:10; RQSVIKddFHI@06:47]. TJR's drawing: the extreme candle from wick to start of body [12_F-mIUfL0@10:20]. E3 (TT): "the leg up that sweeps liquidity that causes the break of structure to the downside" (whole leg) [rBsbMoNwIw4@02:51–05:11]. Use needs a rejection, not a touch [uRXKBX1kzwc@06:58].
- **(b)** **Do not implement for trading.** For historical replay only: bearish OB = range of the up-leg from its origin swing low to the swept high, valid only if a bearish BOS follows immediately; bullish = mirror.
- **(c)** E2 "only one OB per trend" vs nested zones [qhuFg_OXdmE@09:13; IY9NJbaNyqA@11:47].
- **(d)** **E5: dropped.** "I no longer use order blocks. I no longer use breaker blocks" [wzq2AMsoJKY@17:05]; "Order blocks are completely useless … equilibrium" [X8Ag7BWd9dg@14:18–14:50]; removed "for the last 6 months" (≈ since Apr 2025) [8QDDxwUV1KM@06:05–07:09]. Contradiction: still listed in Sep 2025 [BMyeYQIj_vU] and as boilerplate in Oct 2025 [jeewXSLHt2g@17:18].
- **(e)** [qhuFg_OXdmE@03:10; rBsbMoNwIw4@02:51; 8QDDxwUV1KM@06:05; X8Ag7BWd9dg@14:18; wzq2AMsoJKY@17:05]

### 2.22 Breaker block: HISTORICAL, dropped in E5
- **(a)** E3 (TT Mar 2024): "a retracement followed by a break of structure opposite of the current trend". The broken retracement range now lacks orders, and a revisit with pressure gives continuation. Shortcut: "literally the opposite of an order block". Bullish breaker = the move up prior to the bullish BOS [YRU4hE19MVg@11:16–12:57; 4XeIodHUtUQ@02:48–05:09].
- **(b)** Not implemented. Which leg to box was vague even then [4XeIodHUtUQ@04:00–05:09].
- **(c)** —
- **(d)** E3–early E4 continuation confluence. **Dropped in E5** (see §2.21 cites).
- **(e)** [YRU4hE19MVg@11:16; 4XeIodHUtUQ@02:48; wzq2AMsoJKY@17:05; X8Ag7BWd9dg@14:50]

### 2.23 79% extension close
- **(a)** Draw a Fibonacci over the swing leg (like EQ). If price **closes** past the 0.79 level, the prior order flow is disrespected. It is a confirmation equal in status to BOS/IFVG, used when there is no gap to invert or the BOS level is too far for good R:R [KxBRLErkel0@24:32–25:05; z0czA_OSq5M@05:47–06:21; tWYSAHQpywE@06:01–06:34; IVqY3b-KEbA@51:13]. "Really just waited for that 79% extension closure … Didn't need to wait for a break of structure" [xxJyvmHROb4@20:24–20:57].
- **(b)** Long case (after a sell-side sweep): `H` = the most recent swing high of the leg into the sweep, `L` = the sweep low. `level = L + 0.79 × (H − L)`. Fire `EXT79_bull` on the first completed candle with `close > level`. Short case: `L` = swing low of the leg into the sweep, `H` = the sweep high, `level = H − 0.79 × (H − L)`, fire on `close < level` [tWYSAHQpywE@06:01 "fib from this high down to this low … right above those wicks"; 8QDDxwUV1KM@14:56 "from the low to the high of the sweep leg"]. Valid on 5m (step 2) and 1m (trigger).
- **(c)** Same context requirements as IFVG (only after a significant sweep). In Feb 2025 he "rarely" used it: "you guys can very well do without this" [z0czA_OSq5M@06:21]. Anchoring was never shown on screen in detail (OPEN). Note: mathematically this is a deep *retracement* of the prior leg; he calls it an "extension" (terminology only).
- **(d)** E4–E5 only. Not in E2 (E2 Fib = 0/0.5/1 only).
- **(e)** [tWYSAHQpywE@06:01; xxJyvmHROb4@20:57; KxBRLErkel0@24:32; 8QDDxwUV1KM@14:56; z0czA_OSq5M@05:47]

### 2.24 SMT divergence
- **(a)** Compare ES and NQ highs/lows at the **same points in time**. **Bearish SMT**: one index makes a high then a lower high while the other makes a high then a higher high. **Bullish SMT**: one makes a low then a higher low while the other makes a lower low. Bearish (bullish) for **both** indexes. It only matters "while actively sweeping draws on liquidity". Outside that, "these things will show up all the time and will be pretty much useless." He doesn't know what SMT stands for [7dTQA0t8SH0@00:00–07:18; yiuFUp0kFz8@4:13:52–4:21:12].
- **(b)** See §7.2 for the full detector (time-matched swings, significance gate, completion).
- **(c)** It is only a *potential* SMT until a change of order flow confirms it; the lagging index may simply take the level later [9ar85Y6-5P4@08:24–09:32]. A completed SMT (the holding index later takes the level too) becomes a sweep for the opposite move [rBdlDQgSjIc@02:50]. Doesn't apply to forex/commodities in E5 [yiuFUp0kFz8@4:13:52].
- **(d)** E5: bias strengthener + index selector, never an execution signal alone [X8Ag7BWd9dg@10:59–11:32]. E4: one of four 5m/1m confirmations, and the only continuation confluence under 2B [8QDDxwUV1KM@11:00; @21:06]. E3: a core confluence ("most of my trade setups are based off of this") [d5uOjnuzYhE]. E2: "I don't trade it and I don't even know what it is" [_6voYEdi5j4@05:00].
- **(e)** [7dTQA0t8SH0@05:00; yiuFUp0kFz8@4:18:57; X8Ag7BWd9dg@10:59; 3svETDwdFUU@04:31; _6voYEdi5j4@05:00]

### 2.25 Leading vs lagging index
- **(a)** **Leading** = the index that **failed** to make the new extreme (lower high in a bearish SMT, higher low in a bullish SMT); it is already showing the new trend and "is able to move a little bit quicker". **Lagging** = the one that made the new extreme (still continuing the old trend) [7dTQA0t8SH0@05:34; @07:18; yiuFUp0kFz8@4:24:09]. The terminology is consistent across eras; only the *choice* changed.
- **(b)** `leading(SMT) := index whose swing did NOT exceed its prior swing`. Determine on the **execution** timeframe [rBdlDQgSjIc@24:28–25:02].
- **(c)** See §7.3 for the selection rule, its exceptions and history.
- **(d)** E5 trades the leading index. Until ≈Jul 2025 he traded the lagging one: "we always take the leading index. Before I used to take the lagging index, but I changed that around … two and a half to three months ago" [5RWTzr1D994@56:46–57:20].
- **(e)** [7dTQA0t8SH0@05:34; 5RWTzr1D994@56:46; rBdlDQgSjIc@24:28; d5uOjnuzYhE@03:22; BOx7Lk8Xs3o@08:56]

### 2.26 Area of accumulation: HISTORICAL (E2–E3)
- **(a)** "Really just areas of consolidation prior to a big leg up (or down) … this is where orders were filled"; "consolidation, accumulation, order block — whatever" [M6DQKMp-3Vo; framework §2.14: Iu_v4kuFQhk@00:32; 7MBD3ow7I1g@01:43; -E7plUbSJUk@10:08]. It was the BC2 entry zone: after a change of trend, retrace into the accumulation that caused the breakout leg [ss-dZPMnjeY@01:43; @06:14].
- **(b)** Not implemented. Boundaries were never specified (box the chop range incl. sweep wick).
- **(c)** —
- **(d)** Absent from the E5 confluence list (only FVG and EQ are continuation zones) [joe_XTCn5Bs@00:34; TYbpk7WogHI@00:00; 18:22]. History only.
- **(e)** [M6DQKMp-3Vo; ss-dZPMnjeY@01:43; r-DdsJLUlBk@01:40; joe_XTCn5Bs@00:34]

### 2.27 Macro (time window)
- **(a)** "9:50–10:10 … that's called the macro … typically the ideal entry time", entry "for the overall hourly trend". "950 is when the macro starts … I rarely will ever take a trade before 950" [L4xz2o23aPQ@03:55–05:02; BOx7Lk8Xs3o@08:20; yiuFUp0kFz8@4:31:51–4:33:36]. SMTs "typically … happen within those macros, so from like 9:50 to 10:10" [d5uOjnuzYhE@08:58].
- **(b)** `MACRO := [09:50:00, 10:10:00)` ET. Preferred entry window inside the hard window (no entries before 09:50; none after 10:30). He sometimes takes 09:45 or 10:20 trades [L4xz2o23aPQ@08:56]. The bot uses the hard window from the time part of the OMD.
- **(c)** If 5m order flow at the start of the macro no longer supports the idea, the idea is "probably washed": "there's just not enough time" [-RAJEWMl-F0@09:23–10:30]. Only this NY-AM macro is used. Other ICT macro times are never mentioned (inferred from absence).
- **(d)** E3–E5 (Jul 2024 onward). E2 used "first ~90 minutes after the open".
- **(e)** [L4xz2o23aPQ@03:55; BOx7Lk8Xs3o@08:20; z0czA_OSq5M@13:00; yiuFUp0kFz8@4:31:51; -RAJEWMl-F0@09:23]

### 2.28 Reversal vs confirmation vs continuation confluences
- **(a)** E5 roles: **reversal/opportunity** = liquidity sweep ("potential for orders to be filled"). **Confirmation** = BOS or IFVG (also 79% close) ("confirmation that orders are filled"). **Continuation** = FVG or EQ ("continuation of the new trend") [4sRDnVmLcMk@00:35–04:31; wzq2AMsoJKY@07:42; joe_XTCn5Bs@00:34; X8Ag7BWd9dg@04:57–07:09].
- **(b)**

| Role | Members (E5) | Timeframe | Required? |
|---|---|---|---|
| Reversal (opportunity) | valid sweep of a significant DOL (§2.10) | 1H/4H/session level, detected on 1m/5m | yes, step 1 |
| LTF manipulation (2B) | sweep of a 5m H/L without a 5m trend break | 5m | only if the step-1 sweep was pre-09:30 |
| Confirmation | BOS, IFVG, 79% close | 5m (step 2), 1m (trigger) | yes, ≥1 |
| Continuation | FVG, EQ of the new 5m leg (SMT allowed only under 2B in E4) | 5m | yes, ≥1 |
| Strengthener / selector | SMT ES vs NQ | 5m (1m in practice) | no, but picks the index |

- **(c)** Naming is inconsistent: Oct 2026 calls the IFVG a "reversal" confluence [TYbpk7WogHI@07:45–09:26]; SMT is "kind of a blend of the confluences" [yiuFUp0kFz8@4:27:26]. Function is what matters: IFVG = order-flow change. A continuation confluence alone is never an entry: "this could just be a high time frame retrace" [X8Ag7BWd9dg@07:09; 4sRDnVmLcMk@03:23].
- **(d)** E5 framing is new (Jan 2026). E2 had "five building blocks" (sweep, BOS, OB, FVG, EQ) and a "third confirmation" [ESsy0uoFAz4@01:06; ss-dZPMnjeY@06:46].
- **(e)** [4sRDnVmLcMk@00:35; wzq2AMsoJKY@07:42; X8Ag7BWd9dg@04:57; xRuMUvW3T7Q@02:14; TYbpk7WogHI@07:45]

### 2.29 Daily bias
- **(a)** E5: "where price is going to go during … your specific time frame". He trades the first 60–90 min, so the bias is for that window only: "I don't necessarily have to be correct about what the bias is for the entire day" [FBX-gtFGWyU@00:00–01:06]. Inputs: (1) was a DOL swept recently (pre-market/at the open) and is price reacting away from it; (2) where the opposing DOLs are, how many, how close ("which cookies are closer and which has more cookies"); (3) HTF (4H/1H) order flow, and whether the HTF FVG/EQ price is in is respected or inverted; (4) price action must confirm (BOS toward the DOL, then continuation) [FBX-gtFGWyU@02:45–14:22; ironJFzNBic@02:21–08:30; yiuFUp0kFz8@6:10:28]. "No bias, no entry" [yiuFUp0kFz8@4:59:53]. "If we don't have an area that price wants to go towards … you should not be taking that trade at all" [FBX-gtFGWyU@14:56].
- **(b)** Full procedure is in the bias section of the OMD (outside Part A). Glossary-level rule: `bias ∈ {long, short, none}` for 09:30–~11:00. `none` → no trade. ES and NQ must agree on the 5m trend, else no trade [8PYgFVB0GHE@48:44–54:21].
- **(c)** A move that takes **no** DOL leaves the bias intact [FBX-gtFGWyU@07:12]. Bias can be overridden by a full opposite sequence (P11).
- **(d)** E2: daily bias = direction of the latest **daily** BOS, with daily+4H agreement [sjuWqKDsQtI@01:43; __fKQR5RR08@04:03]. E3 (TT 2024): 4H trend = bias [TBU7yfJzwrY]. E4 Jun 2025: previous-session profile + which HTF DOLs were manipulated [e_FV0Q14k8E@08:58–10:06]. E5: DOL/window bias plus 4H/1H order flow.
- **(e)** [FBX-gtFGWyU@00:00; ironJFzNBic@02:21; e_FV0Q14k8E@03:19; yiuFUp0kFz8@4:59:53; sjuWqKDsQtI@01:43]

### 2.30 Power of three (AMD): rejected
- **(a)** "I want you to forget about power three." Think only about where orders fill (sweeps), how fills are confirmed (IFVG/BOS), and continuation [9ar85Y6-5P4@22:11]. Dismissed for beginners: "you don't need to know that" [a5PLl1uM7CQ@07:09].
- **(b)** Do not model accumulation–manipulation–distribution of the daily candle. (The E4 session-profile logic [e_FV0Q14k8E] is liquidity-based and belongs to bias, not to PO3.)
- **(c)** —
- **(d)** Rejected E4–E5. Never adopted.
- **(e)** [9ar85Y6-5P4@22:11; a5PLl1uM7CQ@07:09]

### 2.31 High-resistance vs low-resistance liquidity
- **(a)** **Low-resistance** ("trend-line liquidity", "stacked highs and lows") = successive unswept higher lows of an uptrend (or lower highs of a downtrend). Price "actively" seeks it and runs through all of them once it reverses ("cookie jar") [AGmAVyAuBE0@24:56–29:21; Vulini8xbB0@39:27–42:12]. **High-resistance** = "the most recent … liquidity sweep that price is currently trading away from". Price is unlikely to return there soon [Vulini8xbB0@44:55–46:01; 9ar85Y6-5P4@12:13].
- **(b)** See §4.1 rows LR/HR. Rule: trade **toward** low-resistance and **away from** high-resistance. After highs are swept and price reverses, "lows must be taken first in order for us to even consider looking for longs again" [Vulini8xbB0@46:37–47:11].
- **(c)** A run of stacked lows already taken = sell-side used up, so look to buy [AGmAVyAuBE0@31:02].
- **(d)** E4–E5 concept.
- **(e)** [AGmAVyAuBE0@24:56; Vulini8xbB0@39:27; @44:55; 2ZArg3kPPkE@00:33]

### 2.32 Relative equal highs/lows (EQH/EQL)
- **(a)** Two highs (lows) at the exact same price or very nearly. Four sets of orders (two per swing). His example: lows "literally 50 cents apart" counted. "Pretty much the same thing as low resistance" [AGmAVyAuBE0@37:47–42:44; yiuFUp0kFz8@2:17:54–2:24:34].
- **(b)** Two confirmed swing highs (same TF, 5m or higher) with `|SH1 − SH2| ≤ tol` and no candle closed above max(SH1, SH2) between them. **DEFAULT (not TJR-stated):** `tol = 2 ticks (0.50 pt) on ES`; on NQ `tol = 2 ticks (0.50 pt)`. Level = max (EQH) / min (EQL).
- **(c)** "Easier to find on lower timeframes" [AGmAVyAuBE0@40:44]. An EQH/EQL cluster on 5m counts as a target. **DEFAULT:** as a sweep level only if it is on 1H/4H or coincides with a session/PD level.
- **(d)** E2 mentioned double tops as "prominent" [KtC2SbemF6w@03:28]. E5 names it a DOL type.
- **(e)** [AGmAVyAuBE0@37:47; yiuFUp0kFz8@2:17:54; KtC2SbemF6w@03:28]

---

## 3. Market structure

### 3.1 Timeframe roles (E5)
| TF | Role | Cites |
|---|---|---|
| 4H, 1H | Order-flow context for bias. Source of significant swing H/L (DOLs). HTF FVG/EQ respect vs inversion. | [FBX-gtFGWyU@00:32; ironJFzNBic@02:21; Vulini8xbB0@27:36] |
| 5m | Step 2 confirmation (BOS/IFVG/79%), 2B manipulation, step 3 continuation zone (FVG/EQ), ES–NQ alignment. | [8PYgFVB0GHE@20:08–22:23; @48:44] |
| 1m | Trigger: after the 5m retrace has broken 1m structure against the trade, enter on the 1m BOS/IFVG back in the trade direction. | [8PYgFVB0GHE@22:56–23:29; @31:17; xRuMUvW3T7Q@15:53] |
| 15m | Not used in the E5 default. E3/E4 sometimes executed on 15m sweeps/BOS; discretionary variant, excluded. | [60H1AumgjG8@10:12; L6TVpyi1eyE] |

### 3.2 Structure engine (per instrument × per TF, on bar close)
```
on_bar_close(tf, c):
  update_doji_filtered_sequence(c)
  if new swing high confirmed (bull i, bear j): push SH = max(high_i, high_j[, doji wicks])
  if new swing low  confirmed (bear i, bull j): push SL = min(low_i, low_j[, doji wicks])
  if trend == up:
      watch_low  = most recent confirmed SL          # updated on every new SL, even if lower by wick
      if c.close <  watch_low: emit BOS(bear); trend = down; watch_high = most recent confirmed SH
  elif trend == down:
      watch_high = most recent confirmed SH
      if c.close >  watch_high: emit BOS(bull); trend = up;  watch_low  = most recent confirmed SL
  else (init): trend = direction of first close beyond the most recent opposite swing
  # with-trend closes beyond the last high/low are NOT BOS; they only extend structure
```
Rules encoded: close strictly beyond; equality ≠ break; wicks ignored; only the most recent swing is monitored ("not monitoring a low that happened like seven lows ago") [n97MKj6wGFk@14:35; @18:36; Zzk864cVJek@04:29–08:55; jeewXSLHt2g@15:04–16:45].

### 3.3 Protective swing and order-flow persistence
- The current order flow on T stays valid until a close beyond its **protective swing**: the most recent swing low in an uptrend, the most recent swing high in a downtrend. "Anything below this high is still valid for bearish order flow" [9ar85Y6-5P4@04:24].
- A sweep against the trend does **not** flip order flow. It only creates the opportunity. Stay with the current order flow until a BOS/IFVG proves the change [9ar85Y6-5P4@03:21; @04:59; ironJFzNBic@04:39].

### 3.4 Multi-timeframe relationships
1. **LTF break against HTF = HTF retrace** (default reading): 1m BOS → 5m retrace; 5m → 15m; 15m → 1H; 1H → 4H [Y1lqifylC4s@07:47–08:20; S-scwzKRP-8@04:31; n97MKj6wGFk@07:42]. E5 example: a 15m BOS up while the hourly is bearish "is only a retrace". Look for 15m/5m bullish arrays to be disrespected to rejoin the hourly [9ar85Y6-5P4@04:24; @05:33].
2. **Exception = reversal at a significant sweep**: when the LTF break happens right after a valid sweep of a significant DOL (with SMT/IFVG), it is the start of the new trend (the trade). "Not every single time, because there's liquidity sweeps and change of market structure" [S-scwzKRP-8@05:05; BdBxXKGWVjk@06:05].
3. **5m retrace seen on 1m**: while the 5m retraces into its FVG/EQ, the 1m "more often than not" breaks structure against the trade. That is expected. The trigger is the 1m change back [xRuMUvW3T7Q@15:53–16:27; z0czA_OSq5M@15:17]. E5 canonical: the 1m counter-break is required first, and "the 5m retrace" may be detected as a 1m BOS against the new 5m trend even without an FVG/EQ tag [8PYgFVB0GHE@26:15; @35:50–36:22]. E4 (Feb 2025): if the 1m never flipped against, "we can take the trade regardless" [z0czA_OSq5M@15:52]. **Register this contradiction**; E5 rule wins.
4. **15m candle as 5m mini-trend**: a single counter 15m candle can be a mini BOS/trend on the 5m. A continuation short = 5m mini-uptrend, then a 5m BOS back down [Xdu6j2E1DEI@17:11–20:31].
5. **HTF holds higher power**: never trade a LTF idea straight into a nearby HTF draw in the opposite direction ("shorting when we were really close to a … high time frame draw on liquidity to the upside") [X8Ag7BWd9dg@20:00–20:32; z0czA_OSq5M@13:34].
6. **HTF confluence ≠ LTF trade**: don't take a short-term trade off a daily EQ; a daily reaction can take days [MiaTd3hh47I@04:58–07:48].

### 3.5 ES–NQ structural alignment (filter)
- "I do not like and I would highly recommend you guys don't take trades when the two indexes are not aligned." Aligned = both in a 5m uptrend or both in a 5m downtrend (by 5m BOS). Misaligned = "the market is indecisive". If still misaligned around 10:20, "call it a day" [8PYgFVB0GHE@48:44–54:21]. Also "if they tell two different things → no trade" (CANONICAL §2).
- Machine rule: `aligned := trend_5m(ES) == trend_5m(NQ) == trade_dir` evaluated at the trigger bar. If not aligned → no entry; keep watching until the cutoff.

### 3.6 Structural invalidation of a setup (summary)
| Event | Effect | Cites |
|---|---|---|
| 5m body close beyond the manipulation extreme (sweep high for shorts) | Idea dead; consider the opposite checklist (incl. 2B) | [xRuMUvW3T7Q@22:35–24:15; 9ar85Y6-5P4@04:24] |
| Continuation FVG inverted before a retrace candle | "Bunk" continuation; reassess the opposite direction | [X8Ag7BWd9dg@09:20] |
| Deep wick against the trade without a close breaking 5m structure | Not invalid; may "redo step two into step three" (fresh 5m BOS + new continuation zone) | [8QDDxwUV1KM@34:30–36:48] |
| 5m order flow reversed and held by the macro | Original idea "washed" | [-RAJEWMl-F0@09:23] |
| ES/NQ 5m misaligned | No entry | [8PYgFVB0GHE@48:44] |

---

## 4. Liquidity

### 4.1 DOL catalogue (mark before 09:30, on ES and NQ separately)

| Code | Level | Exact rule | Use | Cites |
|---|---|---|---|---|
| ASIA_H/L | Asia session high/low | max/min of bars 18:00–03:00 ET | sweep + target | [L4xz2o23aPQ@00:33; Vulini8xbB0@31:02] |
| LDN_H/L | London session high/low | max/min 03:00–08:30 ET | sweep + target ("NY frequently sweeps London's low or high") | [AGmAVyAuBE0@11:43; Vulini8xbB0@36:03] |
| PM_H/L | NY pre-market high/low | max/min 08:30–09:30 ET | sweep (with 2B) + target | [L4xz2o23aPQ@01:09; FBX-gtFGWyU@02:45; r-DdsJLUlBk@02:14] |
| PDH/PDL | Previous day high/low | max/min across all three sessions of the prior trading day (18:00→17:00, inferred) | sweep + extended target | [AGmAVyAuBE0@20:15; yiuFUp0kFz8@2:05:36] |
| H1_H/L | 1H swing highs/lows | §2.2 swings on 1H, unswept | sweep + target | [pKIo-aVic-c@15:20; 8PYgFVB0GHE@16:49] |
| H4_H/L | 4H swing highs/lows | §2.2 swings on 4H, unswept | sweep + extended target | [pKIo-aVic-c@15:20; Vulini8xbB0@28:45] |
| EQH/EQL | Relative equal H/L | §2.32 | target (sweep if HTF) | [AGmAVyAuBE0@37:47] |
| LR | Low-resistance (stacked trend) H/L | ≥2 consecutive unswept higher lows (uptrend) or lower highs (downtrend) on 5m+ (count: DEFAULT ≥2, not TJR-stated) | primary target ladder; sweep of the whole stack = entry context | [AGmAVyAuBE0@24:56; Vulini8xbB0@39:27] |
| HR | High-resistance | the most recent swept level price is trading away from | avoid trading back toward it | [Vulini8xbB0@44:55] |
| DATA_H/L | News-candle H/L | §2.14 | target / sweep level | [AGmAVyAuBE0@44:23; 2ZArg3kPPkE@00:00] |
| NDOG/NWOG | Opening gaps | §2.15 | target / entry inside | [PlsHO33j6B8@01:10; FBX-gtFGWyU@17:09] |
| OPEN_H/L, M30_L/H | Market-open high/low; 30m lows | minor, intraday | intermediate targets only | [FBX-gtFGWyU@12:45; xRuMUvW3T7Q@01:41] |
| M5_H/L | 5m swing H/L | §2.2 on 5m | **not significant**: only for 2B manipulation and TP1 | [Vulini8xbB0@29:18; 8QDDxwUV1KM@28:20] |

**Search procedure** [FBX-gtFGWyU@06:07–06:39; AMlev-gYyHo@22:35–23:45]: start on 4H; if few unswept levels near price, add 1H; then lower TFs for targets only. Mark levels made during pre-market too.

**Pruning** (before and during the session):
- Remove any level traded through **without a reaction** ("pretty useless") [TEp3a-7GUds@22:04; 8QDDxwUV1KM@09:23–09:55; xRuMUvW3T7Q@10:55].
- Remove levels "already taken out during pre-market" unless they produced a reaction, in which case that was "the liquidity sweep for the day" [AMlev-gYyHo@22:35; pKIo-aVic-c@18:36–19:08].
- A swept-and-reacted level becomes high-resistance (HR) [Vulini8xbB0@46:37].

### 4.2 Significance hierarchy (for step 1 sweeps)
1. **Significant (may start a trade):** session H/L (Asia, London, pre-market), PDH/PDL, 1H/4H swing H/L, plus EQH/EQL / LR / DATA when they are on 1H+ or coincide with the above [8PYgFVB0GHE@16:49; Vulini8xbB0@27:36–29:52; e_FV0Q14k8E@07:16; xRuMUvW3T7Q@01:08].
2. **LTF (cannot start a trade):** 5m/15m H/L, used for 2B manipulation and as near targets [e_FV0Q14k8E@21:22–23:38; 9ar85Y6-5P4@11:41].
3. Ties / several levels swept at once (e.g., "sweep takes all of them out") count as one sweep at the most extreme level [pKIo-aVic-c@16:58].
- **DEFAULT (not TJR-stated):** 1H/4H swing levels are eligible only if formed within the last 5 trading sessions and still unswept.

### 4.3 Sweep detection and validation (state machine per level)
```
UNSWEPT --(bar.high > L for BSL | bar.low < L for SSL)--> TRADED_THROUGH (record extreme, ts)
TRADED_THROUGH --(reaction: DEFAULT 5m close back on original side within 6×5m bars,
                  before next same-side DOL is taken)--> SWEPT_VALID
TRADED_THROUGH --(next same-side DOL taken first, or no reaction in window)--> RUN_THROUGH (prune; not a sweep)
SWEPT_VALID --(5m OF_change opposite to sweep)--> ACTIONABLE (step 2 done)
SWEPT_VALID/ACTIONABLE --(5m body close beyond the sweep extreme)--> FAILED (idea dead)
```
Notes: no minimum penetration is stated in any era (OPEN). TJR's own reaction cue is a "big" opposite candle [AMlev-gYyHo@26:35]; the DEFAULT window replaces that judgment. Sweep timing: pre-market/London sweeps are valid **if** reacted, and then require 2B after 09:30 [xRuMUvW3T7Q@03:51–06:00; X8Ag7BWd9dg@35:01]. No entries before 09:30 even if the whole reversal happened pre-market. After the open, look only for continuation [8PYgFVB0GHE@44:17–44:51].

### 4.4 Step 2B (NY-open LTF manipulation)
- Trigger condition: the step-1 sweep (and possibly its 5m confirmation) completed **before 09:30** [xRuMUvW3T7Q@03:51–05:28; 8QDDxwUV1KM@16:03].
- Requirement after 09:30: a sweep of a **5m** swing high (shorts) / low (longs) **in the counter-direction**, while the 5m trend set by the confirmation is **not** broken by a close (for shorts: no close above the relevant lower high) [8QDDxwUV1KM@16:03–17:44].
- Rationale: "when New York market opens, new money is coming into the market … there's almost always going to be some form of manipulation." "Every single time we get a pre-market sweep … we'll get big legs" that stop out early entries [xRuMUvW3T7Q@03:51; 8QDDxwUV1KM@16:03–19:25].
- E4 nuance: under 2B, price pushes beyond a 5m high, so no FVG/EQ retrace may exist, and SMT was allowed as the continuation confluence [8QDDxwUV1KM@19:25–22:46; xRuMUvW3T7Q@07:07]. E5 never restates this (OPEN; see §7.4).
- Precursor (E4 Jun 2025): previous-session profile 3 (manipulation + reversal) → NY continuation, which needs a 5m/15m sweep against the bias first [e_FV0Q14k8E@21:22–25:18].

### 4.5 Liquidity as targets (the ladder; detailed management lives in the trade-management part)
- Targets are the **opposing** DOLs ("we sweep out highs, we're looking for sells down to lows") [AGmAVyAuBE0@53:03]. Market makers exit their positions at opposing liquidity [Vulini8xbB0@42:47; ironJFzNBic@05:12].
- Ladder order (nearest first): 5m/30m/market-open H/L → session (London/Asia/pre-market) H/L → 1H H/L → 4H H/L / PDH/PDL / LR stack end / NWOG/BPR far edge [8PYgFVB0GHE@32:26; @45:59; xRuMUvW3T7Q@08:45; 8QDDxwUV1KM@26:07–28:20].
- TP1 ≈ 1:1 at the nearest DOL ("because it's a one to one right there"). Don't make a far HTF level the only target [8QDDxwUV1KM@28:20; 8PYgFVB0GHE@40:47; ironJFzNBic@20:58].
- No opposing DOL with acceptable distance → no trade [FBX-gtFGWyU@14:56].

### 4.6 Liquidity-side selection ("cookie monster")
- Favour the side with **more** DOLs that are **closer**. At the open, if price is very close to one cluster, "it would be stupid for us to want to target these highs before targeting these lows" [FBX-gtFGWyU@07:45–08:50]. Trade toward low-resistance and away from high-resistance [Vulini8xbB0@46:37]. **DEFAULT (not TJR-stated)** scoring: `score(side) = Σ_{unswept significant levels within 1.5×ATR(14,1H)} 1/distance`; prefer the higher score. Used in the bias module.

---

## 5. Time: sessions, the open, the macro, cut-offs (all times ET; also give CME exchange time = CT)

**Clock rules.**
- TJR sets his charts to New York time whatever his location, and every time he gives is ET [yiuFUp0kFz8@44:27].
- CME exchange time (CT) is always ET − 1 h, because both zones observe US daylight saving on the same dates. The bot keeps one clock in `America/New_York` and derives CT from it.
- Session boundaries are defined on the New York clock. TJR does not convert them for UK daylight-saving dates (inferred).
- All bars are time-stamped by their **open** time. A bar "closes" at open + bar length. Every rule that says "close" means the bar has completed.

### 5.1 Session map

| ET | CT | Name | What the bot does | Source |
|---|---|---|---|---|
| 17:00–18:00 | 16:00–17:00 | "Spread hour" / CME daily maintenance halt | No data. The **NDOG** (new day opening gap) forms between the 17:00 close and the 18:00 open. The **NWOG** forms between Friday 17:00 and Sunday 18:00. | [L4xz2o23aPQ@01:43] [yiuFUp0kFz8@3:16:47] |
| 18:00–03:00 | 17:00–02:00 | **Asia session** | Build the Asia high/low. Never trade it. | [L4xz2o23aPQ@00:33] [yiuFUp0kFz8@1:48:14] [065lMUrD_kg@10:47] |
| 02:00 | 01:00 | London pre-market | Information only. | [L4xz2o23aPQ@01:09] |
| 03:00–08:30 | 02:00–07:30 | **London session** (TJR ends it at the NY pre-market, although London "technically" trades until 11:30) | Build the London high/low. Never trade it. | [L4xz2o23aPQ@01:09] [yiuFUp0kFz8@4:29:38] |
| 08:30–09:30 | 07:30–08:30 | **NY pre-market**. Red-folder releases come at 08:30, and pre-market manipulation is "very typical" | Build the pre-market high/low and the news-candle ("data") high/low. **No entries**: "The answer is always going to be no." | [L4xz2o23aPQ@01:09] [8PYgFVB0GHE@44:17] [aobHuNcI1QM@8:23:26] |
| 09:30 | 08:30 | **Cash open** (NYSE). Start of RTH | Start the open-sequence watch (§8.3). | [L4xz2o23aPQ@03:22] |
| 09:30–09:50 | 08:30–08:50 | **Manipulation window** | Expect a sweep of an HTF or LTF draw on liquidity. Sweeps and 5m confirmations may complete here. **No entries before 09:50** (DEFAULT, see 5.2). | [L4xz2o23aPQ@03:22; @05:02] [yiuFUp0kFz8@4:31:51] [5RWTzr1D994@05:14] |
| 09:50–10:10 | 08:50–09:10 | **"The macro"**, the primary entry window ("typically the ideal entry time") | 1m triggers are taken. | [L4xz2o23aPQ@03:55] [yiuFUp0kFz8@4:31:51] [BOx7Lk8Xs3o@08:20] |
| 10:10–10:30 | 09:10–09:30 | Late window | 1m triggers are still allowed. If ES and NQ are still misaligned on the 5m at 10:20, the day is over. | [8PYgFVB0GHE@53:13] [rBdlDQgSjIc@36:30] ("10:05 still a good time") |
| **10:30** | **09:30** | **Entry cut-off** | No new entries after 10:30:00 ET. "If I can't find a trade by 10:30, I'm done for the day." | [L4xz2o23aPQ@05:02] [yiuFUp0kFz8@4:33:36] [8PYgFVB0GHE@53:13] |
| 10:30–12:00 | 09:30–11:00 | Management only | An open position is managed to TP/SL. Hard flatten at **12:00 ET** (DEFAULT, not TJR-stated; he managed a runner to 11:11 and then closed it as "not worth the extra time" [3SygD-YgZuQ@1:38:48]). | see §8.10 |
| 13:00–16:00 | 12:00–15:00 | NY PM session | **Not traded in E5**: "Me personally, I don't trade this." The E3 PM model is historical (5.4). The FOMC exception exists only under NEWS_MODE=CURRENT and is disabled by default (§16). | [L4xz2o23aPQ@03:55] [yiuFUp0kFz8@4:32:29] |
| 16:00 | 15:00 | Cash close | End of RTH. | — |

### 5.2 Window rules (machine form)

- `ENTRY_EARLIEST = 09:50:00 ET` (DEFAULT). TJR sometimes enters at ~09:45 ("manipulation 9:30–9:40 with an entry at 9:45" [L4xz2o23aPQ@05:02]; entries at ~9:45–9:48 [_zzxRMbyE44; xxJyvmHROb4]). He also calls 9:41–9:43 "too early" [xxJyvmHROb4@12:24; @15:04] and says "It's 9:40 … still a decent amount of time until I'm willing to look for a trade" [YfS5yBQgubI@14:03]. In the Trading Transformation he said "Never really try and look to execute before 950" [aobHuNcI1QM@8:22:53]. Optional `ENTRY_EARLIEST_AGGRESSIVE = 09:45`; it is off by default.
- `ENTRY_LATEST = 10:30:00 ET` [L4xz2o23aPQ@05:02]. A trigger bar that closes at 10:30:00 is allowed. Anything later is not.
- `ALIGN_DEADLINE = 10:20 ET`: if the ES and NQ 5m trends still disagree at this time, the day ends [8PYgFVB0GHE@53:13].
- **The windows are soft for TJR and hard for the bot.** "This doesn't have to be point-blank period" [L4xz2o23aPQ@09:30]. Manipulation sometimes finishes at 9:52 [L4xz2o23aPQ@08:56]. Sweeps may therefore complete up to the entry cut-off. Only entries are fenced.
- **9:50 time-location test** (bias aid): "if we're still hanging up here at this high-time-frame manipulation point at around 9:50 with all of these draws on liquidity to the downside … bearish; versus if price dumps down and we take out these draws … bullish" [5RWTzr1D994@05:14–06:22]. In §8.2 this is how the open's manipulation is resolved.
- **Bias horizon** = his trading window, the first 60–90 min after the open. He is not forecasting the daily candle [FBX-gtFGWyU@00:00–01:06].
- **Pre-market and London events** are used for levels, bias and the 2B flag (§8.3), never for entries [8PYgFVB0GHE@44:17] [X8Ag7BWd9dg@35:01].

### 5.3 Calendar / day-level time rules

- **US bank holidays: no trading**. The day after a holiday that also has a Powell speech is skipped too [xxJyvmHROb4@00:00] [1FunNCUw_jM@12:24]. E2 adds a 50% de-risk on the day before a holiday [1FunNCUw_jM@09:36] (STRICT only).
- **Scheduled news times that matter**: 08:30 (CPI, PPI, NFP, claims, GDP), 10:00 (ISM, PCE, JOLTS and similar), 14:00 (FOMC decision), 14:30 (FOMC press conference) [yiuFUp0kFz8@2:25:08] [7a8tAGkVJac@08:48]. Day handling is set by `NEWS_MODE` (§16.3).
- **Early-close days** (for example the day after Thanksgiving, Christmas Eve): not addressed by TJR. DEFAULT: treat as a holiday (no trade).
- **Skip-next-day after a red day**: he did this in practice [rBdlDQgSjIc@1:03:28]. It is optional, `SKIP_AFTER_LOSS_DAY = false` DEFAULT.

### 5.4 Evolution (historical, do not implement)

| Era | Window rule | Source |
|---|---|---|
| E2 | "Murder it for the first hour and a half then leave": entries until about 11:00 ET, and an open trade may run past it | [065lMUrD_kg@10:12–11:18] |
| E3 | AM macro 9:50–10:10, "never execute before 950", because the 1H/4H candles close at 10:00. **PM model**: kill zone 13:50–14:10 / prime time 13:30–15:00, with 15m = bias, 5m = DOL, 1m = execution and a single TP | [aobHuNcI1QM@8:22:53–8:27:56] [i3FU-9OUU90@04:43–07:01] |
| E4 | Same AM window. Off the charts by about 10:30. FOMC traded only after 14:00/14:30 | [BOx7Lk8Xs3o@08:20; @20:12] [7a8tAGkVJac@12:41] |
| E5 | 09:30–09:50 manipulation, 09:50–10:10 macro, done at 10:30, no PM | [L4xz2o23aPQ@03:22–05:02] [yiuFUp0kFz8@4:31:51–4:33:36] |

---

## 6. PD arrays / imbalances (FVG, IFVG, EQ, BPR; OB/breaker as historical)

"PD array" = his collective term for the premium/discount tools (E2: EQ, FVG, OB [z9p7OThLkr4@19:38]; E5 usage: "bullish PD arrays … FVG/EQ" [9ar85Y6-5P4@01:05–01:38]). **E5 active set: FVG, EQ** (continuation) and **IFVG** (order-flow change, i.e. an FVG used the other way). Secondary targets: NDOG/NWOG, BPR/illiquid range. **Inactive (historical): OB, breaker, area of accumulation.**

### 6.1 Respect vs disrespect (the single principle)
- In a downtrend, look only for **bearish** arrays to be **respected** (price enters, then continues down) and for **bullish** arrays to be **disrespected** (closed through = IFVG). A bullish FVG in a downtrend is used "only in the opposite direction" [9ar85Y6-5P4@01:05–01:38; @10:03]. Mirror for uptrends.
- Respected = price trades into the zone and the next confirmation (5m close in the trade direction, or a 1m BOS/IFVG back in the trade direction) occurs before a close beyond the far edge [yiuFUp0kFz8@6:21:47–6:24:01; BdBxXKGWVjk@06:37].
- Disrespected = body close beyond the far edge (§2.17).
- HTF version (bias): the 4H/1H FVG/EQ price is in. Respected → target the external DOL in the trend direction; inverted → bias flips to the opposite DOLs. A respected 4H FVG is confirmed by a 1H BOS in the trend direction out of it [ironJFzNBic@02:21; @08:30; @19:52].

### 6.2 FVG lifecycle (5m execution leg)
```
create (3-candle rule, §2.16) -> ACTIVE
ACTIVE --price trades into [bottom, top]--> TAPPED (never an entry by itself)
TAPPED/ACTIVE --body close beyond far edge--> INVALIDATED (emit IFVG(opposite) if it is the
               outermost-holding gap of a with-trend stack AND sweep context exists)
any --new swing extreme beyond the leg's high (bull)/low (bear)--> BALANCED -> delete leg's FVGs
any --new opposite BOS--> drop all old-direction continuation FVGs ("I no longer give a [care] about this FVG")
```
Cites: [xX5LTSJ5wwM@15:47–31:54; yiuFUp0kFz8@2:59:16–3:15:39; ironJFzNBic@28:18; xcDOMKaOIsk@40:27].

Selection when several 5m continuation FVGs exist in the new leg:
- Any member of a stack is a valid continuation zone. Only inversion needs the whole stack [BdBxXKGWVjk@12:45].
- In an LTF uptrend with stacked gaps, "prefer the gap under equilibrium (discount) for longs" [ironJFzNBic@14:41–15:15].
- Prefer the **first retracement** after the sweep + BOS; the second is still good; the third is weaker; late in the trend, don't enter [xcDOMKaOIsk@15:09–16:46].
- **DEFAULT (not TJR-stated):** if both an FVG and EQ exist, the zone = union of {FVGs of the new leg, the EQ line}. The first one touched arms the 1m trigger.

### 6.3 Equilibrium (continuation) — exact procedure
1. After the 5m order-flow change (step 2), wait for the first 5m candle opposite to the new trend. That fixes the leg extreme B (low for shorts) [joe_XTCn5Bs@12:55; TEp3a-7GUds@30:00].
2. A = most recent swing on the other end (the manipulation high for a fresh reversal; a newer lower high if one formed) [wzq2AMsoJKY@06:38–07:09].
3. EQ = (A+B)/2. Shorts need price ≥ EQ (premium); longs ≤ EQ (discount). A touch or a "poke" counts as filled [joe_XTCn5Bs@08:30–09:35].
4. If a new extreme forms before EQ is hit → re-anchor B [-E7plUbSJUk@06:46; yiuFUp0kFz8@4:04:20].
5. If EQ is not reached but an FVG of the leg is, the FVG serves (either continuation confluence) [joe_XTCn5Bs@09:02].
6. Then drop to 1m for the trigger (§3.4 item 3) [wzq2AMsoJKY@08:51].
7. **Invalidation of the EQ step — AMBIGUOUS.** Literal words: "It's going higher and we close above equilibrium … that invalidates step number three", followed by "we closed above these highs" [xRuMUvW3T7Q@22:35–23:42 (transcript)]. Read literally, a close beyond EQ *into* premium would kill a short, which contradicts "sell in premium" [wzq2AMsoJKY@03:52]. **DEFAULT (not TJR-stated):** step 3 is invalid when a 5m body closes beyond A (the leg's origin/manipulation extreme), i.e. the new 5m structure breaks. A deep wick without that close is tolerated [8QDDxwUV1KM@34:30–36:48]. Log both readings for backtest.

### 6.4 IFVG — detection details
- Candidate gaps: FVGs of the **current with-trend leg** (the trend being reversed), on the same TF as the check (5m for step 2, 1m for the trigger) [4sRDnVmLcMk@05:03].
- Fire on the first close beyond the outermost-holding gap of that leg's stack (§2.18). For a bullish stack, the "last fair value gap that is holding up the trend" is the bottom one [4sRDnVmLcMk@15:27–18:17].
- Must follow a valid significant sweep (step 1) for step-2 use; on the 1m it must occur after price has entered the 5m continuation zone and the 1m has flipped against the trade [8PYgFVB0GHE@31:17; xRuMUvW3T7Q@15:53].
- Same candle may be both IFVG and BOS [8PYgFVB0GHE@40:14]. A BOS candle can invert one gap and create a new opposite FVG ("two in one") [rMkghkG-ZjE@10:52].
- Cross-index use: the confirming index's IFVG ("NQ also invalidated its gap") is used as supporting evidence [5RWTzr1D994@30:39; rBdlDQgSjIc@36:30–37:02] (§7.5).

### 6.5 79% extension close — usage priority
- Use when no FVG exists to invert **and** the BOS level is far (poor R:R) [IVqY3b-KEbA@51:13; tWYSAHQpywE@06:01]. Formula in §2.23. **DEFAULT (not TJR-stated):** priority order for the confirmation event = first of {IFVG, BOS, EXT79} to print on a closed bar. All three are equal in status per [xRuMUvW3T7Q@02:14].

### 6.6 BPR / illiquid range and opening gaps (targets)
- BPR: §2.20 DEFAULT. Use only as a target (far edge) or as context that price will traverse quickly after breaking the bordering H/L [PlsHO33j6B8@15:16–20:23]. E3 use as an FVG tie-breaker is optional [TihRnXjqM5c@16:27].
- NDOG/NWOG: §2.15. Target when price is away. A Monday-NY unfilled NWOG is a high-value target [PlsHO33j6B8@10:43].
- New-candle opening gaps: ignore [PlsHO33j6B8@11:49].

### 6.7 Historical PD arrays (do NOT trade; keep for replay/evolution log)
| Array | Era active | Definition then | Status | Cites |
|---|---|---|---|---|
| Order block | E1–E4 (to ~Apr 2025) | leg (or extreme candle wick→body) into the swept extreme before the opposite BOS; needs rejection | dropped: "completely useless", EQ fills anyway | [qhuFg_OXdmE@03:10; 12_F-mIUfL0@10:20; rBsbMoNwIw4@02:51; X8Ag7BWd9dg@14:18; 8QDDxwUV1KM@06:05] |
| Breaker block | E3–E4 | broken retracement range; move up before a bullish BOS | dropped with OB | [YRU4hE19MVg@11:16; 4XeIodHUtUQ@02:48; wzq2AMsoJKY@17:05] |
| Area of accumulation | E2–E3 | consolidation before a big leg; BC2 core entry zone | absent from the E5 list | [M6DQKMp-3Vo; ss-dZPMnjeY@01:43; joe_XTCn5Bs@00:34] |
| EQ-only entry with close back beyond EQ | E2 | EQ + reaction close + new BOS | replaced by EQ → 1m BOS/IFVG | [4FEty6xgOc0@04:25; wzq2AMsoJKY@08:51] |
| Displacement-candle CE (50%) | E5 (student Q) | retrace to 50% of a displacement candle | muddled "yes"; stated preference "literally just two forms … FVG or EQ" → not implemented | [9ar85Y6-5P4@14:27–16:08] |

---

## 7. SMT divergence and index selection

### 7.1 Why the bot needs NQ
NQ is required for: (1) SMT at the sweep (bias strength + index choice) [yiuFUp0kFz8@4:24:42]; (2) the 5m alignment filter [8PYgFVB0GHE@48:44]; (3) cross-index confirmation ("NASDAQ has confirmed") [4KzkQEM28tc@02:55–03:28]. The bot **executes only ES/MES**. When TJR would pick NQ, the bot either skips or trades ES under the rules below (§7.6).

### 7.2 SMT detector
```
inputs: 5m bars ES, NQ (same timestamps); significant level set per index (§4.2)
bearish SMT at time t2 (a candidate):
  swing highs H1 at t1 and H2 at t2 on BOTH indexes, at matching timestamps
     (DEFAULT tolerance: same bar or ±1 bar on the TF, not TJR-stated)  [rBdlDQgSjIc@22:42; d5uOjnuzYhE@08:26; 8QDDxwUV1KM@13:50]
  index X: H2 > H1 (higher high) AND index Y: H2 <= H1 (lower/equal high)
  AND X's H2 (or the pair) is sweeping a significant DOL on X           [7dTQA0t8SH0@05:00; @15:03; yiuFUp0kFz8@4:18:24]
bullish SMT: mirror with lows (only lows for bullish, only highs for bearish) [3svETDwdFUU@09:04]
status:
  POTENTIAL  -> until a change of order flow (BOS/IFVG/79%) in the SMT direction   [9ar85Y6-5P4@08:24–09:32; @33:03]
  CONFIRMED  -> after that change
  COMPLETED/VOID -> the holding index Y later also takes the level: SMT is used up and
                    becomes a sweep for the opposite move                          [rBdlDQgSjIc@02:50]
```
- Timeframe: 5m (and 15m) for SMT. HTF SMT (1H/4H) for bias. E3 said not 1m ("1 minute SMT pretty freaking weak") [BOx7Lk8Xs3o@03:55; 3svETDwdFUU@10:09; d5uOjnuzYhE@08:26], but E4 live trades used a 1m SMT as an early trigger [rBdlDQgSjIc@24:28] and even a 30-second SMT [IVqY3b-KEbA]. **E5/bot: 5m SMT counts; 1m SMT is logged only, never a trigger** (consistent with "doesn't tell me to execute" [X8Ag7BWd9dg@10:59]).
- Equal highs on the holding index: **DEFAULT (not TJR-stated)**: treat `H2 == H1` on Y as "failed to exceed" (holding). Note E4 example: "ES had relative equal highs at the London high" vs NQ swept [iVOjRDrjFM4].
- A London SMT that already completed before the open is invalid for NY [5RWTzr1D994 summary].

### 7.3 Role of SMT in the E5 sequence
| Use | E5 rule | Cites |
|---|---|---|
| Bias | Strengthens bias at the sweep. A HTF SMT is a bias input. SMT + LTF confirmation can override the pre-market bias. | [X8Ag7BWd9dg@10:59; TEp3a-7GUds@25:28; @38:31; yiuFUp0kFz8@4:24:42] |
| Confirmation | **Not** sufficient: "A bearish SMT alone is not enough — I want to see a change in order flow." | [TEp3a-7GUds@29:27; X8Ag7BWd9dg@25:59] |
| Confluence weight | Without SMT, demand more (e.g., wait for the FVG fill) | [X8Ag7BWd9dg@11:32] |
| Index selection | Picks the index to execute (§7.4) | [X8Ag7BWd9dg@11:32; TEp3a-7GUds@30:35] |
| Context | Valid only at a significant DOL sweep; elsewhere "useless" | [7dTQA0t8SH0@04:26] |
| Hot time | typically forms 9:50–10:10 | [d5uOjnuzYhE@08:58] |
| Trade exit (E4 practice) | partials keyed to the other index's levels; close if an opposing SMT forms | [rBdlDQgSjIc@27:52–35:24] |

History: E2 not used [_6voYEdi5j4@05:00] → E3 core ("nothing without bias", only SMT in line with bias) [d5uOjnuzYhE@06:41; 3svETDwdFUU@09:37] → E4 one of four confirmations and the only continuation under 2B [8QDDxwUV1KM@11:00; @21:06; xRuMUvW3T7Q@07:07] → E5 strengthener/selector.

### 7.4 Index selection rule (E5) and its evolution
1. **Default: execute on the LEADING index** = the one that **failed** to make the new extreme (lower high for shorts, higher low for longs) [yiuFUp0kFz8@4:24:09–4:27:26; 7dTQA0t8SH0@10:41–14:31; TEp3a-7GUds@30:35; 2ZArg3kPPkE@11:41; 8QDDxwUV1KM@23:20–24:25]. Reason: the leader "was able to fill probably more orders", expands faster and further, and is closer to the targets [7dTQA0t8SH0@05:34; @14:31; 8QDDxwUV1KM@23:52].
2. **Determine leader on the execution timeframe** (5m/1m), not the HTF. Picking the HTF leader when the other index led on the LTF was "the wrong index" [rBdlDQgSjIc@24:28–25:02; @35:24].
3. **Confirmation from the opposed index**: when the indexes disagree, require the index most opposed to the trade to confirm too (e.g., ES completes every step, then "all I would be looking for would be NASDAQ breaking structure to the downside"; "wait for ES to flip bullish before I … look for a trade on NASDAQ") [4KzkQEM28tc@02:55–03:28; rBdlDQgSjIc@37:02]. Combined with the 5m alignment filter (§3.5).
4. **History (do not use):** E3–mid-E4 he executed on the **lagging** index (the one that made the new extreme: "go to the lagging index") [d5uOjnuzYhE@03:22; @10:37; BOx7Lk8Xs3o@04:29; @09:31; 3svETDwdFUU@19:49]. Switched ≈Jul 2025 [5RWTzr1D994@56:46–57:20].
5. **Observed exceptions in E5/E4 practice** (register; bot behaviour in §7.6):
   - No SMT, only one index swept: "As long as one of the indexes is doing it for us, that's all we need." He traded **NQ, the index that DID sweep**, because ES had no manipulation [8PYgFVB0GHE@37:25–43:04].
   - Proximity: chose the index closer to its HTF draw [MiaTd3hh47I@02:20; kH-rbepWkNE@05:31].
   - No SMT reasoning: trade whichever index sets up first [FBX-gtFGWyU@06:07].
   - Hindsight conflicts: "I probably should have longed on ES rather than NASDAQ" [3SygD-YgZuQ@25:01; @35:18].
   - With-strength choice on a continuation leg [J1vPj1m6crQ@42:25].

### 7.5 Cross-index evidence the bot should compute every bar (5m and 1m)
`trend_5m(ES)`, `trend_5m(NQ)`; per index: last sweep status of each significant level; active SMT objects; the IFVG/BOS events of each index. Partial-close hooks on the other index's levels (E4 practice, optional) [rBdlDQgSjIc@27:52].

### 7.6 Bot policy (ES/MES-only execution)
| Situation | Bot action |
|---|---|
| Valid SMT, ES is leading (failed to make the extreme) | Trade ES (canonical). |
| Valid SMT, NQ is leading | **DEFAULT (not TJR-stated):** no trade (TJR would trade NQ). Optional config `ALLOW_LAGGING_ES=false`. If enabled, require ES to complete its own sweep → 5m OF change → continuation → 1m trigger, and log as non-canonical. |
| No SMT; both indexes swept the same significant level | Allowed (SMT is not required), but requires the extra confluence: the continuation must be an FVG fill, not EQ alone [X8Ag7BWd9dg@11:32] (DEFAULT reading). |
| No SMT; only NQ swept, ES did not | **DEFAULT:** no ES trade unless ES itself has a valid sweep of its own significant level (TJR traded NQ here [8PYgFVB0GHE@37:25]). |
| ES and NQ 5m trends disagree at the trigger | No trade [8PYgFVB0GHE@48:44]. |
| Opposite SMT forms while in a trade | Flag for management (exit logic lives in the management part) [rBdlDQgSjIc@33:39–35:24]. |

## 8. The full model, in order

The model is the E5 sequence "**opportunity → confirmation → continuation → LTF trigger → exit at liquidity**". In his words: "We look for potential for orders to be filled, confirmation that orders are filled, and then a continuation of the current trend that is now being created" [yiuFUp0kFz8@2:45:16]. The same sequence appears in [TEp3a-7GUds@10:36], [X8Ag7BWd9dg@04:21–08:15], [8PYgFVB0GHE@16:49–23:29] and [FBX-gtFGWyU@10:32].

TJR calls it a discretionary "toolbox" and says he deliberately leaves pieces out [yiuFUp0kFz8@5:52:03; @6:03:43]. The bot therefore uses the fixed defaults below.

**Timeframes.** 4H/1H give context and bias. 5m gives the sweep read, confirmation and continuation. 1m gives the trigger [yiuFUp0kFz8@6:10:28; @6:22:20] [FBX-gtFGWyU@00:32].

**Feeds.** Every step is evaluated on **both ES and NQ**. Only ES/MES is executed (§17).

### 8.1 Pre-open prep (finish by 09:25 ET)

| | |
|---|---|
| **Conditions** | **(a) Day filter:** apply `NEWS_MODE` and holidays (§16.3). If the day is blocked, the day ends with NO_TRADE. **(b) Mark DOLs separately on ES and on NQ:** Asia H/L (18:00–03:00); London H/L (03:00–08:30); NY pre-market H/L (08:30–09:30); PDH/PDL (prior Globex day 18:00→17:00, "all three sessions" [yiuFUp0kFz8@2:05:36]); unswept 1H and 4H swing highs/lows; relative equal highs/lows; stacked "low-resistance" trend highs/lows; news-candle (data) H/L; NWOG/NDOG if unfilled [yiuFUp0kFz8@1:47:06–2:32:58] [8PYgFVB0GHE@16:49] [TEp3a-7GUds@19:19–22:39]. **(c) Delete used levels:** any level price has already traded through with no reaction ("pretty useless") [TEp3a-7GUds@22:04] [yiuFUp0kFz8@6:09:19]. **(d) HTF order flow on 4H and 1H:** trend by the last BOS/IFVG; whether price is extending to external liquidity or retracing into a 4H/1H FVG/EQ; whether that zone is respected or inverted [ironJFzNBic@02:21; @08:30; @26:31] [yiuFUp0kFz8@6:06:34–6:11:01]. **(e) HTF SMT state:** is there an open SMT, and has it been completed? A completed SMT is void [5RWTzr1D994@01:13] [YfS5yBQgubI@01:11] [rBdlDQgSjIc@02:50]. **(f) 2B flag:** set `HTF_SWEPT_PREOPEN = true` if a significant DOL was swept and reacted between the previous 16:00 and 09:30 [xRuMUvW3T7Q@03:51–06:35] [8QDDxwUV1KM@16:03]. |
| **Timeframe** | 4H, 1H (context). 5m and 1m for session and pre-market levels. |
| **Not significant** | 5m, 15m and 1m swings are **not** significant sweep levels (CANONICAL). They may still be TP1 targets and 2B manipulation levels. |
| **Invalidates prep** | A data gap in either feed, or a missing calendar → NO_TRADE (DEFAULT). |
| **If it fails** | No DOL on either side within reach (top-down search 4H → 1H → LTF finds nothing) → "If we don't have an area that price wants to go towards, then you should not be taking that trade at all" → NO_TRADE [FBX-gtFGWyU@06:07; @14:56]. |

**DEFAULT parameters (not TJR-stated).**
- Equal-level tolerance: ES 0.50 pt (2 ticks), because "50 cents apart … close enough" [yiuFUp0kFz8@2:22:52]. NQ 2.00 pt (scaled DEFAULT).
- Stacked/low-resistance levels: ≥3 consecutive unswept with-trend swing lows (or highs) on 5m–1H.
- 1H/4H swing: TJR's two-candle high/low definition [yiuFUp0kFz8@1:05:11].
- Lookback for 1H/4H swings: 10 trading days (DEFAULT).

### 8.2 Bias (for the 09:30–11:00 window)

| | |
|---|---|
| **Conditions** | Bias is DOL-driven and answers four questions [FBX-gtFGWyU@02:45–14:22]. **Q1.** Was a significant DOL swept recently (London, pre-market or at the open) with price reacting away from it? If yes, the bias is away from it [FBX-gtFGWyU@02:45]. **Q2.** Where are the opposing DOLs, and how many? Prefer the side with **more and closer** unswept DOLs, the "cookie monster" rule [FBX-gtFGWyU@07:45–08:50]. **Q3.** HTF context: a 4H/1H trend respecting its FVG/EQ means the bias follows the trend toward the external DOL. An HTF FVG that is inverted (IFVG) or an HTF BOS against the trend flips the bias [ironJFzNBic@02:21; @08:30; @19:52] [yiuFUp0kFz8@5:01:33]. **Q4.** Price action must confirm with a 5m BOS toward the DOL and then continuation (that is, steps 8.4–8.5) [FBX-gtFGWyU@13:50–14:22]. |
| **Output** | `bias ∈ {LONG, SHORT, NONE}` plus a list of target DOLs. DEFAULT combination order: Q1 if present, else Q3; Q2 breaks ties; if all are empty or in conflict, NONE. HTF SMT: a 4H/1H SMT at a significant DOL adds to the bias in its direction. It is multi-day context, "doesn't even have to play out today" [YfS5yBQgubI@02:52] [7dTQA0t8SH0@11:13]. |
| **Timeframe** | 4H/1H for context. Session levels. 5m at the open. |
| **Invalidates bias** | (i) A sweep of a significant DOL **in the bias direction** followed by an SMT and a 5m BOS/IFVG against it. "We can let the market prove us wrong and we can still make money" [TEp3a-7GUds@39:03] [yiuFUp0kFz8@6:27:56]. (ii) A 1H BOS against the bias [ironJFzNBic@28:18]. (iii) At about 09:50, price is still parked at the HTF manipulation point with draws on the other side [5RWTzr1D994@05:14]. A move that takes **no** DOL leaves the bias intact; it is read as a retrace [FBX-gtFGWyU@07:12]. |
| **If it fails** | Bias NONE at 09:30 is not a stop. Wait for the open's sweep to define direction (Q1). If the bias is still NONE at `ENTRY_LATEST` → NO_TRADE. A trade **against** the pre-open bias is allowed only when it comes from a sweep of a significant DOL **with an SMT at that sweep** plus the full 8.4–8.6 sequence (DEFAULT, built from [TEp3a-7GUds@24:54–39:03] and "without SMT … I'd want more confluence" [X8Ag7BWd9dg@11:32]). |
| **Historical** | E2: daily-structure bias. E3: 4H trend = bias, with the 1H choosing the execution TF (agree → 5m/1m, disagree → 15m/5m) [OvmbAxG15YE@24:14]. E2: news-direction bias. None of these are used in E5. |

### 8.3 Sweep (the opportunity)

| | |
|---|---|
| **Conditions** | On ES **or** NQ ("As long as one of the indexes is doing it for us, that's all we need" [8PYgFVB0GHE@38:00]), price trades beyond a significant DOL from 8.1 **and reacts**, meaning it moves back away from the level [FBX-gtFGWyU@02:45] [yiuFUp0kFz8@1:40:54]. DEFAULT test: ≥1 tick beyond the level (TJR counted a ~4-tick ES overshoot as a sweep [eEg0_zc8Hxg@45:12]), then a 5m candle **closes back on the original side** of the level, inside the 5m candles before step 8.4 completes. The sweep extreme is the most extreme price printed before the 8.4 confirmation candle closes. |
| **Timing** | Sweep at or after 09:30: proceed to 8.4. Sweep before 09:30 (London or pre-market), shown as `HTF_SWEPT_PREOPEN`: **2B applies**. After 09:30, also require a **5m manipulation**, a sweep of a 5m high (for shorts) or 5m low (for longs) in the original direction **without** a 5m body close that reverses the confirmed 5m trend [xRuMUvW3T7Q@03:51–06:35] [8QDDxwUV1KM@16:03–19:25]. "Even though we already had the sweep … I want a New York [manipulation] because new money's in the market now" [YfS5yBQgubI@09:41]. E5 restates it: if the sweep and reversal happened pre-market, "after the open only look for the continuation step" [8PYgFVB0GHE@44:17]. |
| **Priority** | When an HTF (1H/4H/session) sweep and a 5m-only sweep point opposite ways, the HTF sweep wins: "Higher time frame is always going to hold higher power" [5RWTzr1D994@28:21]. |
| **Timeframe** | Level from 8.1. Detection on 1m/5m. |
| **Invalidates** | (a) Price trades through and keeps going: 5m bodies close beyond the level and no 8.4 confirmation forms before price reaches the next DOL. That is a breakout, not a sweep, and the level is consumed. (b) Only a 5m/1m level was taken (not significant), except as the 2B manipulation. (c) An SMT is "completed" when the leading index also takes its level; that SMT is void [5RWTzr1D994@01:13]. |
| **If it fails** | Return to WATCH_SWEEP for the next significant DOL. Each level can be swept once. |

### 8.4 5m confirmation (order-flow change)

| | |
|---|---|
| **Conditions** | After the sweep, on 5m, **one** of the following in the reversal direction. **(1) BOS:** a candle **body close strictly beyond** the most recent opposite 5m swing, i.e. the swing that bounds the leg into the sweep. A wick or an equal close does not count [yiuFUp0kFz8@2:35:49–2:41:57] [8PYgFVB0GHE@26:50]. **(2) IFVG:** a body close beyond the far edge of the **outermost** with-trend 5m FVG of the stack in the leg into the sweep, i.e. the gap "holding up the trend". Closing through an inner gap "doesn't mean anything" [yiuFUp0kFz8@3:43:53; @3:51:19–3:57:35] [3SygD-YgZuQ@02:54–04:39]. Preferred, because it usually comes before the BOS [yiuFUp0kFz8@3:50:04]. "If no FVG in the leg to invert, wait for BOS" [TEp3a-7GUds@28:19]. **(3) 79% extension close** (E4–E5 alternative when no gap exists): a Fibonacci is drawn on the leg into the sweep (for a long: last swing high → sweep low). A candle **closing beyond the 0.79 level** confirms [tWYSAHQpywE@06:01] [xxJyvmHROb4@20:57] [8QDDxwUV1KM@14:56]. The anchoring is (inferred). |
| **Required alongside** | **(A) ES/NQ 5m alignment:** both indexes must be in the new 5m trend, each having printed a 5m BOS or IFVG in the trade direction since the sweep. "I do not like and I would highly recommend you guys don't take trades when the two indexes are not aligned" [8PYgFVB0GHE@48:44–51:33]. This also enforces "confirmation must come from the index most opposed to the trade": for shorts, wait for the more bullish index to break down [3SygD-YgZuQ@04:39–06:56; @13:50–14:24] [YfS5yBQgubI@24:07]. **(B) SMT check** at the swept level on 5m (8.4.1). |
| **Timeframe** | 5m. |
| **Do NOT** | Enter on the confirmation candle: "that's going to cause you guys to get a horrible entry" [8PYgFVB0GHE@25:44] [X8Ag7BWd9dg@06:36]. |
| **Invalidates** | Price makes a new extreme beyond the sweep extreme **and** a 5m body closes beyond it. The reversal has failed; return to 8.3 (the level counts as traded through). |
| **If it fails** | No confirmation → keep waiting until `ENTRY_LATEST`. Misaligned → wait; if still misaligned at 10:20 → DONE [8PYgFVB0GHE@53:13]. |
| **Historical** | E4 (Sep–Nov 2025) listed **SMT itself** as a fourth 5m confirmation option [xRuMUvW3T7Q@02:14] [BMyeYQIj_vU@09:25]. In E5 SMT "doesn't tell me to take a trade" [X8Ag7BWd9dg@10:59]. Not used as a confirmation. |

**8.4.1 SMT and index choice.**
- **Definition.** At the same swing time (DEFAULT: extremes within ±2 bars on 5m), one index makes a new extreme beyond the swept level and the other does **not** (lower high vs higher high, or higher low vs lower low) [7dTQA0t8SH0@05:00–07:18]. It counts only at a significant DOL; "outside of that … pretty much useless" [7dTQA0t8SH0@05:00].
- **Leading index** = the one that failed to make the new extreme. E5 trades it ("we always take the leading index. Before I used to take the lagging index" [5RWTzr1D994@56:46]; [7dTQA0t8SH0@13:25] [yiuFUp0kFz8@4:24:09]).
- The leader is judged on the **execution** timeframe [rBdlDQgSjIc@24:28].
- No SMT (both swept, or only one index has the level) → no index preference.
- Bot application: §17.4.

### 8.5 5m continuation (the retrace)

| | |
|---|---|
| **Conditions** | After 8.4, price retraces against the new leg **into a 5m continuation confluence of the new leg**. Either **(a)** a 5m FVG formed in the new leg's displacement, or **(b)** 5m **EQ**, the 50% of the most recent swing (for a short, Gann box from the new leg's high to its most recent low; the low exists only once an opposite candle has printed). Shorts need price at ≥50% (premium); longs need ≤50% (discount) [yiuFUp0kFz8@3:59:50–4:06:35] [TEp3a-7GUds@30:00–31:08] [TYbpk7WogHI@12:13]. When EQ isn't reached, the FVG may be the zone respected, and the reverse is also true [yiuFUp0kFz8@4:08:16]. In a stack, a deeper gap below EQ counts even if an upper gap was closed through [ironJFzNBic@14:41]. **AND** on 1m, the retrace has broken 1m structure **against** the new trend (a 1m counter-BOS) [8PYgFVB0GHE@26:15; @35:50] [TEp3a-7GUds@33:55]. |
| **2B case** | When 2B applied, the 5m manipulation leg (pushing beyond a 5m high/low) has no FVG/EQ retrace. Then a **5m SMT** at that 5m sweep is the continuation confluence [8QDDxwUV1KM@21:06–22:46] [xRuMUvW3T7Q@07:07]. |
| **Mode switch** | `CONT_MODE = STRICT` (DEFAULT): FVG/EQ touch **and** a 1m counter-BOS. `CONT_MODE = SIMPLE` (E5 operationalisation [8PYgFVB0GHE@21:50–22:23; @26:15]): a 1m counter-BOS alone. |
| **Timeframe** | Zone on 5m. Counter-BOS on 1m. |
| **Never** | Enter on the touch. "If we just press sell right when equilibrium gets pushed into, then why do we even draw equilibrium in the first place?" [TEp3a-7GUds@31:40] [yiuFUp0kFz8@6:21:12]. |
| **Invalidates** | (a) A 5m body close through the **outermost** FVG of the new leg (that gap is inverted). The continuation is "bunk", and the opposite direction should be reassessed [X8Ag7BWd9dg@09:20]. (b) Price trades beyond the sweep extreme. (c) Order blocks and breaker blocks are **not** valid zones in E5: "Order blocks are completely useless … what else is typically getting filled? Equilibrium" [X8Ag7BWd9dg@14:18–14:50]. |
| **If it fails** | No retrace (an impulsive one-way move): no entry. "Massive amounts of candles … no sort of entry confluence" [FBX-gtFGWyU@09:24] [8PYgFVB0GHE@51:33]. The bot may wait for a fresh 5m swing in the same direction and its own retrace, i.e. redo 8.4 → 8.5 inside the window [8QDDxwUV1KM@30:00–40:44]. After invalidation (a), a new setup the other way still needs its own significant sweep (it may be one that already happened) plus 8.4–8.6. |

### 8.6 1m trigger

| | |
|---|---|
| **Conditions** | With 8.5 satisfied, wait on the **1m** for an order-flow shift back in the trade direction. Either **1m BOS** (a body close beyond the 1m swing created by the retrace, e.g. for a short, a close below the last 1m higher low of the retrace) or **1m IFVG** (a body close through the outermost 1m with-retrace FVG) [8PYgFVB0GHE@22:56–23:29; @31:17] [yiuFUp0kFz8@6:22:20–6:24:01] [TEp3a-7GUds@33:55] [X8Ag7BWd9dg@07:42–08:15]. The 1m 79% close is an accepted alternative [rBdlDQgSjIc@35:24] [tWYSAHQpywE@06:34]. |
| **Alternative (slower)** | Wait for the next **5m candle to close** in the trade direction out of the zone [yiuFUp0kFz8@6:21:47]. Not the bot default, because TJR prefers the 1m: "TP1 was being hit about when a 5m-close trader would be entering" [yiuFUp0kFz8@6:05:23–6:29:35]. |
| **Not a trigger** | A 1m SMT alone. He did this once [rBdlDQgSjIc@24:28], but in E5 it is excluded [X8Ag7BWd9dg@10:59]. |
| **Timeframe** | 1m on the execution index (ES). The other index's 1m shift is supporting evidence [5RWTzr1D994@30:39] [YfS5yBQgubI@24:07]. |
| **Invalidates** | The trigger bar closes after `ENTRY_LATEST`. Price trades beyond the sweep extreme. The 8.5 invalidation fires first. |
| **If it fails** | Keep waiting for the next trigger within the window. A new 1m counter-BOS just re-arms the trigger, so there is no limit on re-arms before the cut-off (DEFAULT). |

### 8.7 Entry

| | |
|---|---|
| **Conditions** | Enter at the **close** of the 1m trigger bar: market or marketable limit at the next bar's open, the same second [8PYgFVB0GHE@31:17]. Pre-entry checks: within the time window; trades and risk budget available (§8.11); stop computable (8.8); `R(TP1) ≥ 1.0` (8.9); size ≥ 1 MES (§17.3). |
| **If a check fails** | Skip this trigger. If the failure is structural (no stop, TP1 < 1R), return to WAIT_RETRACE for a deeper retrace or a new leg. |

### 8.8 Stop

| | |
|---|---|
| **Rule (E5)** | Beyond the invalidation: the **1m retrace swing** (the "second high" for shorts, "second low" for longs, the extreme created by the 1m counter-move) [8PYgFVB0GHE@35:13; @40:14; @45:26] [TEp3a-7GUds@35:03] [FBX-gtFGWyU@12:45; @18:14] ("under the low or the second low") [xRuMUvW3T7Q@10:22]. |
| **Conservative alternative** | `STOP_MODE = SWEEP`: beyond the sweep extreme. This was the E2–E4 default ("I almost always put my stop loss above the liquidity sweep" [1FunNCUw_jM@01:08]). |
| **Buffer** | DEFAULT 2 ticks (0.50 pt) beyond the swing on ES. E2 quoted about 0.5 pt [1FunNCUw_jM@05:44]. |
| **Size guide** | His 2026 ES stops were about **16, 28 and 34–35 ticks (4–9 pts)** [hBnD6T1M4w8@11:45]. E2 gave ES ~4–7 pts [KSiWKfPOlh4@08:33]. **Never a fixed-points stop** [1FunNCUw_jM@10:43]. |
| **Wide stop** | If the stop is "drastically larger than usual", cut size in half [hBnD6T1M4w8@13:59]. DEFAULT: wide = stop > 2× the median of the bot's last 20 ES stops (cold start: > 10 pts). DEFAULT hard max 16 pts → skip. |
| **No structural stop** | No clean invalidation → **no trade**. He lost a trade with an arbitrary stop and named that as the cause [C5zIaZzbbgM@36:55; @49:17]. Never trade without a stop. His no-stop trades [_zzxRMbyE44@32:43] are explicitly NOT to be copied. |

### 8.9 Targets (DOL ladder)

- **Ladder** (in the trade direction, nearest first): 5m swing H/L and the market-open high/low → pre-market H/L → London H/L → Asia H/L → 1H H/L → PDH/PDL → 4H H/L, 4H FVG, NWOG/NDOG, BPR far side → daily H/L [8PYgFVB0GHE@32:26; @40:47; @45:59] [yiuFUp0kFz8@6:24:36; @6:29:35] [FBX-gtFGWyU@12:45–13:18] [YfS5yBQgubI@30:42–37:49].
- **TP1** ≈ 1:1 at the nearest liquidity: "intermediate highs/lows for an approximate 1:1 TP1 rather than waiting 10 years" [8PYgFVB0GHE@40:47]. "Don't set a far HTF high as the one and only take profit" [ironJFzNBic@20:58]. Rule: **if R(TP1) < 1.0 → skip the trade** (CANONICAL; [5v4G4xJVKIQ@08:52]).
  - DEFAULT refinement: a 5m-only swing below 1.0R is stepped over to the next ladder level.
  - A significant (session / 1H / 4H / PD) level below 1.0R → skip, because it sits in the path.
- **TP2 / TP3 / runner**: the next ladder levels. Usually 3–4 TPs [yiuFUp0kFz8@6:30:42] [5RWTzr1D994@57:54].
- **Stretch target**: daily H/L and 4H draws, only for the runner [8PYgFVB0GHE@45:59].
- **Not targets**: 1m levels [FjSiLFrg5fo@09:06]. Fib extensions appeared once as a projection tool [3SygD-YgZuQ@26:09] and are historical/optional, not used.

### 8.10 Management

- **At TP1**: close **50%** and move the stop to **break-even** [8PYgFVB0GHE@45:59] [5RWTzr1D994@56:13] [xRuMUvW3T7Q@18:07] [tWYSAHQpywE@30:45]. DEFAULT BE = entry + 1 tick in favour ("slightly in profit" [tWYSAHQpywE@30:45]).
- **At TP2**: close 50% of the remainder. The runner (25%) goes to TP3/stretch. This comes from BC2 [ss-dZPMnjeY@05:06]. E5 only says "partials along the way" [8PYgFVB0GHE@35:13].
- **Hold through normal noise.** A 1m BOS against the trade inside a valid 5m extension is normal. Do not exit on it [3SygD-YgZuQ@34:05–34:39].
- **Early exit, before or after TP1.** Close everything if (a) a **5m body close inverts the continuation FVG** (the trade's own 5m FVG becomes an IFVG against it), **or** (b) an opposing SMT forms at a DOL together with a 1m IFVG against the trade on both indexes [3SygD-YgZuQ@16:54–18:16; @23:10] [rBdlDQgSjIc@33:39–35:24]. Runner only: also exit on a 1m BOS against the trade at an HTF DOL [ss-dZPMnjeY@05:06].
- **Do not flip** into the opposite direction on the same signal. His live flip [3SygD-YgZuQ@17:44] is NOT copied. Any new trade needs the full sequence and the daily budget.
- **Time stop**: flatten everything at 12:00 ET (DEFAULT).

### 8.11 End of day

| Condition | Action | Source |
|---|---|---|
| No entry by 10:30 ET | DONE (NO_TRADE) | [L4xz2o23aPQ@05:02] |
| ES/NQ misaligned at 10:20 | DONE | [8PYgFVB0GHE@53:13] |
| Trade closed as a **win** (any TP hit) | DONE: "one win → done" | CANONICAL [rBdlDQgSjIc@58:05; @48:44] [5RWTzr1D994@1:01:24] |
| Trade closed as a **loss** with full-budget risk | DONE | [XcA0GiWZp7M@03:56] |
| Trade 1 was taken at half budget (`SPLIT_BUDGET`) and lost | One more trade allowed at the remaining half, with the full sequence | [5v4G4xJVKIQ@08:18] [065lMUrD_kg@07:59] |
| DOLs on both sides taken, or full TP hit (the day's bias is done) | DONE: "I wouldn't try and chase that today. The majority of the move is done" | [3SygD-YgZuQ@1:21:48] |
| Third trade | **Never** | [rBdlDQgSjIc@58:05; @1:02:21] |
| Always | Journal the trade or no-trade with all gate values | [yiuFUp0kFz8@34:21] |

---

## 9. Master confluence list, in order and ranked

**Roles:**
- **reversal** = opportunity (the sweep)
- **confirmation** = order flow has changed
- **continuation** = retrace zone / trigger in the new trend
- **target** = exit liquidity
- **filter/context** = gates or bias inputs

TJR's own E5 ranking of "the only confluences that I use" is (1) liquidity, (2) IFVG, (3) FVG, (4) EQ, (5) BOS [TYbpk7WogHI@00:00–18:22]. SMT and time are listed separately as blending tools [yiuFUp0kFz8@4:27:26; @4:31:51].

| # | Confluence | Role | Status (bot) | TJR's weight (stated) | Era | Citations |
|---|---|---|---|---|---|---|
| 1 | Liquidity sweep of a significant DOL (session H/L, PDH/PDL, 1H/4H H/L, EQH/EQL, stacked lows/highs, data H/L) | reversal (+ target) | **REQUIRED** | #1, "the goat of confluences", "by far my favorite" | E1–E5 | [TYbpk7WogHI@00:33] [yiuFUp0kFz8@1:15:14] [8PYgFVB0GHE@16:49] |
| 2 | Inverse FVG (5m confirmation; 1m trigger) | confirmation / trigger | **REQUIRED** (one of #2, #5, #6) | #2; "almost every single day almost more than BOS" | E4–E5 (skeptical in E3) | [TYbpk7WogHI@07:45] [yiuFUp0kFz8@3:50:04] |
| 3 | FVG (5m, new leg) | continuation | **REQUIRED** (one of #3, #4) | #3 | E1–E5 | [TYbpk7WogHI@03:19] [yiuFUp0kFz8@2:51:31] |
| 4 | Equilibrium 50% (Gann box, most recent swing; premium/discount) | continuation | **REQUIRED** (one of #3, #4) | #4; "useless without context" | E2–E5 | [TYbpk7WogHI@11:06] [yiuFUp0kFz8@4:08:16] |
| 5 | Break of structure (body close) | confirmation / trigger | **REQUIRED** (one of #2, #5, #6) | #5 | E1–E5 | [TYbpk7WogHI@15:01] [yiuFUp0kFz8@2:35:49] |
| 6 | 79% extension close | confirmation / trigger (when no gap) | OPTIONAL alternative to #2/#5 | used "when there's no gap to invert" | E4–E5 | [tWYSAHQpywE@06:01] [xxJyvmHROb4@20:57] [8QDDxwUV1KM@14:56] |
| 7 | 1m counter-BOS, then 1m BOS/IFVG back (LTF trigger) | trigger | **REQUIRED** | "the last step in my strategy" | E3–E5 | [X8Ag7BWd9dg@08:15] [8PYgFVB0GHE@22:56] |
| 8 | ES/NQ 5m trend alignment, with confirmation from the most-opposed index | filter | **REQUIRED** | "highly recommend you don't take trades when … not aligned" | E5 | [8PYgFVB0GHE@48:44] [3SygD-YgZuQ@05:14] |
| 9 | Time window (no entries before 09:50 / after 10:30; manipulation 09:30–09:50) | filter | **REQUIRED** | core "time theory" | E3–E5 | [L4xz2o23aPQ@03:22–05:02] |
| 10 | Daily bias / DOL on the target side ("an area price wants to go to") | context / target | **REQUIRED** | "without daily bias … why are we entering" | E1–E5 | [FBX-gtFGWyU@14:56] [yiuFUp0kFz8@4:59:53] |
| 11 | DOL ladder giving TP1 ≥ 1R | target | **REQUIRED** | "minimum one to one" | E2–E5 | [8PYgFVB0GHE@40:47] [FjSiLFrg5fo@06:15] |
| 12 | Structural stop available | risk | **REQUIRED** | his stated cause of a loss | E5 | [C5zIaZzbbgM@49:17] |
| 13 | News/holiday day filter (`NEWS_MODE`) | filter | **REQUIRED** | see §16.3 | E1–E5 (changed) | [w5sUCqFH3Lg@06:49] [7a8tAGkVJac@01:41] |
| 14 | 2B: 5m manipulation after the open when the HTF sweep was pre-open | reversal (LTF) | **REQUIRED when triggered** | "every single time we get a pre-market sweep … big legs" | E4–E5 | [8QDDxwUV1KM@16:03] [xRuMUvW3T7Q@03:51] [8PYgFVB0GHE@44:17] |
| 15 | SMT divergence (ES vs NQ) at the swept DOL | context + index selector (+ continuation in 2B) | OPTIONAL (strong); required for counter-bias trades (DEFAULT) | "strengthens our bias … determines what index"; never a trigger | E3–E5 (rejected in E2) | [X8Ag7BWd9dg@10:59] [7dTQA0t8SH0@05:00] [5RWTzr1D994@56:46] |
| 16 | HTF (4H/1H) order flow: respect vs inversion of the HTF FVG/EQ | context | OPTIONAL (bias input) | main bias tool in the Jan 2026 lesson | E3–E5 | [ironJFzNBic@02:21; @08:30] |
| 17 | HTF sweep outranks LTF sweep | context | OPTIONAL (tie-break) | "Higher time frame is always going to hold higher power" | E4–E5 | [5RWTzr1D994@28:21] |
| 18 | More/closer DOLs on the target side ("cookies") | context | OPTIONAL | bias step 3 | E5 | [FBX-gtFGWyU@07:45] |
| 19 | Relative equal highs/lows | reversal / target | OPTIONAL (subtype of #1) | "four times the orders" | E1–E5 | [yiuFUp0kFz8@2:17:54] |
| 20 | Stacked "low-resistance" lows/highs | reversal / target | OPTIONAL (subtype of #1) | "cookie monster" | E4–E5 | [yiuFUp0kFz8@2:09:34] [YfS5yBQgubI@05:42] |
| 21 | News-candle (data) H/L | reversal / target | OPTIONAL | admits weak examples | E4–E5 | [yiuFUp0kFz8@2:25:08] [2ZArg3kPPkE@00:00] |
| 22 | NWOG / NDOG | target (occasional entry) | OPTIONAL | NWOG "very very good target"; NDOG rarely | E4–E5 | [yiuFUp0kFz8@3:16:47–3:26:58] [FBX-gtFGWyU@17:09] |
| 23 | BPR / illiquid price range | target / POI | OPTIONAL | "swift move down → same flush up" | E4–E5 | [yiuFUp0kFz8@3:28:04] [rBdlDQgSjIc@03:59] [YfS5yBQgubI@35:39] |
| 24 | 9:50 time-location test | context | OPTIONAL | | E4 | [5RWTzr1D994@05:14] |
| 25 | Negative: entry too close to an opposing HTF DOL / "already at EQ" / fading a fresh ATH break | filter (penalty) | OPTIONAL (penalty) | | E5 | [X8Ag7BWd9dg@20:00] [3SygD-YgZuQ@15:34; @01:42] |
| 26 | New candle opening gap | — | REJECTED | "pretty freaking useless" | E5 | [yiuFUp0kFz8@3:20:42] |
| 27 | Order block | continuation | **HISTORICAL** (dropped) | "completely useless" in E5; BC1 first choice | E1–E4 | [X8Ag7BWd9dg@14:18] [8QDDxwUV1KM@06:05] |
| 28 | Breaker block | continuation | **HISTORICAL** | "completely useless" | E3–E4 | [X8Ag7BWd9dg@14:50] |
| 29 | Area of accumulation / "third confirmation" | continuation | **HISTORICAL** (BC2) | | E2 | framework §4.E |
| 30 | Daily-structure bias; news-direction bias | context | **HISTORICAL** | | E2 | framework §3, §8 |
| 31 | 4H/1H agreement selects 5m vs 15m execution | context | **HISTORICAL** | | E3 | [OvmbAxG15YE@24:14] |
| 32 | Trading the lagging index (the one that swept) | index selector | **HISTORICAL** (changed about Jul 2025) | | E3–E4 | [BOx7Lk8Xs3o@08:20] [5RWTzr1D994@56:46] |
| 33 | Fib extension targets | target | HISTORICAL/rare | one live use | E5 (once) | [3SygD-YgZuQ@26:09] |
| 34 | Support/resistance, chart patterns, indicators as signals | — | REJECTED | "don't use" | all | [yiuFUp0kFz8@2:46:58; @39:21] [TEp3a-7GUds@42:19] |

### 9.1 Checklist rubric

**REQUIRED gates (all must pass; any FAIL → no entry).**

| Gate | Test |
|---|---|
| G1 Day | `day_allowed(NEWS_MODE)` and not a holiday |
| G2 Bias/DOL | at least one unswept DOL on the target side; the trade direction equals the bias, **or** the counter-bias condition holds (sweep of a significant DOL + SMT at it) |
| G3 Sweep | significant DOL swept + reaction (8.3); if `HTF_SWEPT_PREOPEN`, a 2B 5m manipulation after 09:30 |
| G4 Confirmation | 5m BOS, 5m IFVG or 5m 79% close in the trade direction after the sweep |
| G5 Alignment | ES and NQ 5m trends both equal the trade direction |
| G6 Continuation | `CONT_MODE` satisfied (5m FVG/EQ touched + 1m counter-BOS; 2B: 5m SMT) |
| G7 Trigger | 1m BOS, 1m IFVG or 1m 79% close back in the trade direction, on a closed bar |
| G8 Time | 09:50 ≤ trigger close ≤ 10:30 ET |
| G9 Stop | structural stop exists, and stop_pts ≤ `STOP_MAX_PTS` |
| G10 RR | R(TP1) ≥ 1.0 per 8.9 |
| G11 Budget | trades_today < allowed (8.11) and risk budget left |
| G12 Index | §17.4 policy permits ES |

**OPTIONAL score (all weights DEFAULT, not TJR-stated).** Range −3 … +7.

| Item | Points |
|---|---|
| SMT at the swept DOL with ES as leading index | +2 |
| SMT with NQ leading | +0 (see §17.4) |
| Swept level is 1H/4H/PDH/PDL (vs session-only) | +1 |
| Bias agrees with 4H/1H order flow | +1 |
| Target side has ≥3 unswept DOLs, nearest ≤ 2R | +1 |
| Both FVG and EQ coincide at the retrace | +1 |
| Confirmation was an IFVG (earlier and tighter) | +1 |
| Opposing significant DOL within 1× stop beyond the stop | −1 |
| Entry with price "already at EQ" of the larger range / fading a fresh ATH break | −1 |
| Trigger in 10:20–10:30 | −1 |

**Use of the score.**
- **score ≥ 3**: full size (×1.0).
- **1 ≤ score ≤ 2**: ×0.5. This follows the E2 "iffy technicals → half" idea [7MBD3ow7I1g@07:52].
- **score ≤ 0**: skip (DEFAULT).

**Size multipliers multiply together, with a floor of ×0.25** (TJR used 0.25% around Powell [G7eq6U8e3yw@01:41]).
- High-impact news day traded under CURRENT: ×0.5 [hBnD6T1M4w8@14:33].
- Wide stop: ×0.5 [hBnD6T1M4w8@13:59].
- ES-fallback when the canonical index is NQ: ×0.5 (DEFAULT, §17.4).
- The day before a holiday, STRICT only: ×0.5 [1FunNCUw_jM@09:36].
- **Never above ×1.0.** His 2× "confident" tier is for proven traders only, and his live oversizing is NOT copied [KSiWKfPOlh4@14:10] [xxJyvmHROb4@37:29].

---

## 10. Risk management and position sizing

**Binding principle.** The bot follows TJR's **teaching** on risk, not his live behaviour (CANONICAL §11). In his 2025–26 streams he often risks far more than he teaches: ≈$40k typical risk per trade [C5zIaZzbbgM@51:01], "full-ported" funded accounts, and trades taken with no stop. §13.2 lists these behaviours. None of them is copied.

Era key: E1 pre-bootcamp 2022–mid 2023 · E2 Boot Camp 1/2.0 (Jun–Oct 2023) · E3 Sep 2023–2024 · E4 2025 · E5 2026 (canonical).

### 10.1 Per-trade risk: what TJR says, by era

| Era | Stated rule | Cites |
|---|---|---|
| E1 | "Risk one percent ... and only take like one trade a day" | [T-Bo-9GDi3s@44:54] |
| E2 | Base risk is **1%** ("my normal risk is just one percent"). 1–3% is the cap; >3% is "immediately doing something wrong". **Set lot size**: size the position so the *minimum* typical stop (ES ≈4 pt) equals 1%. BC2 variant: compute the contracts that give 1% at the actual stop, then apply the tier factor | [KSiWKfPOlh4@08:33–14:44; RkMBoqbeUq8@10:41; CZRs2NuLQIw@05:36; 7MBD3ow7I1g@06:10–06:43] |
| E3 | 1% per trade is the reference. "Risk management is more than 1% per trade": study your win rate and RR | [6GNy02w2WIo@02:11; MNA9gtZCVqM@07:44] |
| E4 | 1–3% per trade for high-win-rate / low-RR traders like him; 0.25–1% for high-RR / low-win-rate traders; never 10%. The stop is a fixed $ amount and the TP varies. "Profitable traders are not risking 5% in a day." Size so you survive three losing days in a row or a losing month | [SHJHpedYh6A@4:09:32–4:15:17; NZqRbc_9u_I@23:16; -zyDnjozaMM@15:20–15:55] |
| E5 | He **moved away from 1% of balance to a fixed contract count per instrument**, chosen so the *largest* typical stop is tolerable. The "sweet spot" is 1–3%, and he accepts 3–4% on wide-stop trades. His ES stops are quoted at ~16, 28 and 34–35 ticks (≈4–8.75 pt) | [hBnD6T1M4w8@10:39–13:25; yiuFUp0kFz8@5:39:52–5:43:12] |

**Bot rule.** `RISK_PER_TRADE_PCT = 1.0`, sized from the actual stop distance (E2 method). The E5 fixed-contract method is **not** the default. With a fixed size, risk floats up to 3–4% when the stop is wide, which breaks the bot's hard cap. A fixed-contract mode is provided only as an option, and when it is on the 3% cap still applies (the trade is halved, then skipped).

Position size formula (from his method; the contract specs are market facts, not TJR):
`contracts = floor( equity × RISK_PER_TRADE_PCT/100 × tier_multiplier / (stop_pts × point_value) )`
- Point values: ES $50/pt and MES $5/pt; tick = 0.25 pt ($12.50 ES, $1.25 MES).
- Example (inferred): 1% of $100k = $1,000. A 4-pt stop gives 5 ES or 50 MES; an 8-pt stop gives 2 ES or 25 MES.
- The size must split into partials. He notes "with the 10 you're able to split it" [L6TVpyi1eyE@20:33]. DEFAULT (not TJR-stated): if ES contracts < 4, use MES so the 50/25/25 ladder (§11.3) can be executed. If MES contracts < 1 after tiers, there is **no trade**.

### 10.2 Daily budget and trade count

| Item | TJR statement | Cites | Bot default |
|---|---|---|---|
| Trades per day | E1–E2: one trade, win or lose, then done; max 1–2; beginners exactly one. E4: "only one or two trades a day ... usually only one setup 9:50–10:30". E4/E5: "taking multiple trades every day is not okay at all"; "I really only see one trade per day" | [z9p7OThLkr4@05:01; 4moWbfm6smw@04:24; 065lMUrD_kg@09:05; SHJHpedYh6A@4:30:02; VTwmHVAX29o@18:37; -mJ8mww-Flw@49:45] | `MAX_TRADES_PER_DAY = 2` as a hard ceiling. The effective default is **1** (the second trade exists only in re-entry mode, §11.6) |
| Daily budget | Two trades: de-risk each so the total equals one trade's risk. BC2: expecting 2 trades → ~50% of the daily budget each; worst case is 100% of the budget. E4: aggressive entry at "half of what I'm willing to risk for the day", the other half held for confirmation or re-entry. E4: leaving budget for a re-entry is "smart thinking" | [065lMUrD_kg@07:59–08:32; 5v4G4xJVKIQ@08:18–10:03; ss-dZPMnjeY@08:59–10:06; KxBRLErkel0@03:55–04:28; iVOjRDrjFM4@12:26] | `DAILY_RISK_BUDGET_PCT = 1.0`. With `REENTRY_MODE=OFF` the single trade uses 1.0%. With `REENTRY_MODE=ON` each trade uses 0.5% |
| Daily max loss | A pre-designated $/day in the written plan ("I am risking $100 a day while taking one trade"). No risk set means no trade | [065lMUrD_kg@09:05; @18:36] | `DAILY_MAX_LOSS = DAILY_RISK_BUDGET` (1%). When it is hit, the bot is flat and done |
| Two losses | "Allotted daily risk across two trades; after two losses, stop." "After two losses, most people should be done for the day" | [MiaTd3hh47I@28:34; @59:24; gKOQbcg0r1M@40:18] | Hard stop after 2 losses (already implied by the budget) |
| Per-day cap | Never >3% per day; never full-port | [CZRs2NuLQIw@05:36; KSiWKfPOlh4@01:07; aobHuNcI1QM@7:52:50] | `MAX_DAILY_RISK_PCT_HARD = 3.0`. Config validation refuses anything higher |
| Weekly / drawdown | No weekly loss limit is stated. A losing streak means 2–3 losing *weeks*, and the strategy is not changed for that | [PyCPHiO2nj0@08:16; 8PYgFVB0GHE@13:25–16:14] | DEFAULT (not TJR-stated): halt live trading and return to paper if peak-to-trough drawdown ≥ 6% (≈ six full-risk losses), pending review |
| Red flag | "A 10% day means you did something wrong" | [TwakmPZJGJA@04:58] | Alert if daily P&L magnitude > 3% (inferred) |

### 10.3 Sizing tiers (multipliers applied to `RISK_PER_TRADE_PCT`)

Tiers are set **pre-session**. They are never changed intraday in response to P&L [z9p7OThLkr4@04:29; 4moWbfm6smw@05:29]. When several tiers apply, multiply them, then apply the 0.25× floor (DEFAULT).

| Tier | Multiplier | Trigger (TJR) | Cites | Bot |
|---|---|---|---|---|
| NORMAL | 1.0 | All conditions met | — | default |
| HIGH-IMPACT NEWS DAY (traded) | 0.5 | "Cut contract size in half on news days" (e.g. PPI); de-risk 50% on high-impact news days | [hBnD6T1M4w8@13:59–14:33; yiuFUp0kFz8@5:43:46; KSiWKfPOlh4@13:04; 7MBD3ow7I1g@04:29] | ON whenever NEWS_MODE allows trading a red-folder day (§12.2) |
| LESSER / PRE-OPEN NEWS | 0.75 | Claims/PCE an hour before the open | [7MBD3ow7I1g@04:29–05:05] | ON for the items marked "0.75" in §12.2 |
| PRE/POST BANK HOLIDAY | 0.5 | De-risk the day before a holiday; the day after is slow | [1FunNCUw_jM@09:36; KSiWKfPOlh4@13:04; YGSXw_B-UgM@05:46] | ON |
| WIDE STOP | 0.5 | "If the stop-loss is very drastically larger than usual, cut the contract size in half" | [hBnD6T1M4w8@13:59] | DEFAULT threshold: stop > 9 ES pts (just above his largest quoted typical stop of 34–35 ticks, inferred). Under %-risk sizing the contract count already shrinks, so this extra halving is deliberately conservative |
| LOW CONFLUENCE / "iffy" | 0.5 | 0.5% instead of 1% on iffy technicals; "only an SMT going for us ... I'm definitely going to derisk"; primary draws already taken → "second-hand trade" | [7MBD3ow7I1g@07:52; g27VsJS3a58@44:08; mV3YFmtnRdo@38:29] | The bot does **not** take iffy trades: a full checklist is required. The tier is kept only for an optional "B-grade" research mode, OFF |
| BAD PRICE ACTION / RANGE | 0.5 | "If I do take a trade today I'll definitely de-risk" | [BUZrKRaYa3A@03:27; dy9jckID-pY@01:07] | Superseded by the chop filter (§12.5 F14): no trade |
| CONFIDENT | 2.0 | No news + favourite setup + all biases aligned. **Students must never use it until proven profitable** | [KSiWKfPOlh4@14:10–14:44; RkMBoqbeUq8@11:14; 7MBD3ow7I1g@05:38] | **OFF** (locked). It may be unlocked only after ≥6 months live under §10.5 criteria. Even then, the 3%/day cap holds |
| COUNTER-BIAS | ~0.1 | "Don't take this trade" is the better choice | [-rYGugTIsbU@12:53; @15:41] | Not traded |

### 10.4 Risk config table (recommended bot defaults vs TJR, by era)

| Parameter | E1 | E2 (Boot Camp) | E3 | E4 (2025) | E5 (2026, canonical teaching) | **Bot default** |
|---|---|---|---|---|---|---|
| `RISK_PER_TRADE_PCT` | 1 [T-Bo-9GDi3s@44:54] | 1 (cap 3) [KSiWKfPOlh4@14:44] | 1 [6GNy02w2WIo@02:11] | 1–3 [SHJHpedYh6A@4:13:35] | fixed contracts ≈1–3%, 3–4% on wide stops [hBnD6T1M4w8@12:52] | **1.0** |
| `SIZING_METHOD` | % | set-lot (min stop = 1%) or calculated | % | fixed $ stop | fixed contracts per instrument | **% of equity from actual stop** |
| `DAILY_RISK_BUDGET_PCT` | 1 | 1 (1–3 refined) [RkMBoqbeUq8@10:41] | — | 1–3 [SHJHpedYh6A@4:30:02] | not stated | **1.0** |
| `MAX_TRADES_PER_DAY` | 1 | 1 (max 2) | 1 ("I take one trade a day") [339amTioakE@11:03] | 1–2 | 1 ("one trade per day") [-mJ8mww-Flw@49:45] | **2 ceiling / 1 effective** |
| `STOP_AFTER_WIN` | yes | yes [4moWbfm6smw@03:16] | — | yes [SHJHpedYh6A@4:49:02] | yes [kH-rbepWkNE@32:49; ZioWcbxSuIw@10:50] | **true** |
| `STOP_AFTER_LOSS` | yes [I0fLlm5s0yg] | BC1 yes / BC2 re-entry within budget | — | beginner guide yes [SHJHpedYh6A@4:45:10]; live: re-entry [iVOjRDrjFM4@11:52] | re-entry seen live; "after two losses be done" [gKOQbcg0r1M@40:18] | **true** (`REENTRY_MODE=OFF`) |
| `NEWS_MULT` | — | 0.5 / 0.75 | de-risk [PIoJUvpG4uc@02:21] | — | 0.5 [hBnD6T1M4w8@14:33] | **0.5 / 0.75** |
| `WIDE_STOP_MULT` | — | — | — | — | 0.5 [hBnD6T1M4w8@13:59] | **0.5 (>9 pt, DEFAULT)** |
| `CONFIDENT_MULT` | — | 2.0 (not for students) | — | — | not mentioned | **disabled** |
| `MAX_DAILY_RISK_PCT_HARD` | — | 3 | — | "not 5% in a day" | accepts 3–4%/trade | **3.0** |
| `MIN_TP1_R` | — | 1.0 [5v4G4xJVKIQ@08:52] | — | 1.0 [SHJHpedYh6A@4:11:17] | ≈1:1 TP1 [8PYgFVB0GHE@40:47] | **1.0** |
| `INSTRUMENT` | SPX CFD / FX | ES + FX | ES/NQ futures | ES/NQ | ES/NQ only | **ES or MES; NQ as data feed only** |

### 10.5 Demo → live progression

| Era | TJR rule | Cites |
|---|---|---|
| E2 | Demo, one trade/day at 1%, for **≥3 months profitable with >10% gain**. Then a small live account (~$100 at 1%), then funded or own capital you can afford to lose, then payouts into live. If you blow up, go back to demo. Keep identical risk when going live | [TwakmPZJGJA@06:40–13:23; 4moWbfm6smw@12:12] |
| E4 | **Three consecutive green months** on demo (e.g. +10%, +5%, +7%); any losing month resets the count. No prop challenges until profitable on demo. Reassess size only after ~6 months of consistency and +30–40% account growth; drop back if emotions appear | [NZqRbc_9u_I@16:35–18:51; a5PLl1uM7CQ@17:28–18:34; VTwmHVAX29o@05:30–07:10] |
| E4–E5 | "You are not going to be profitable within your first 3 months"; return to demo rather than keep losing. Learn on demo first; backtest and journal | [cXlVBiwIlbI@07:09; @09:22; yiuFUp0kFz8@26:31; 5:48:11] |

**Bot progression** (TJR's criteria applied to a machine; the stage gates are DEFAULT where marked):
1. **Backtest** on ES and NQ 1m data with no look-ahead. HTF candles must be closed at decision time: bar replay leaks HTF information [NPG_BZ_83fo@04:30], and a 4H candle is not known until it closes [OvmbAxG15YE]. DEFAULT gate: ≥ 100 signal days and positive expectancy after fees and slippage.
2. **Paper / forward test** live-time at 1% notional for **≥ 3 consecutive green calendar months**; any red month resets the count (TJR E4 rule).
3. **Live, minimum size**: MES at 1%, same rules as paper (TJR: identical risk demo→live).
4. **Scale size** (the equity % stays 1%; the account grows) only after ≥ 6 months of live consistency and ≥ +30% growth (TJR E4). The CONFIDENT tier stays off unless separately validated.
5. **Regression**: if the §10.2 drawdown halt fires, go back to paper (TJR: "if you blow up, go back to demo").

### 10.6 Prop-firm profile: SEPARATE, NOT FOR BOT

Recorded only so the model is understood. **The bot must not use any row in this table.** These numbers are account-gaming tactics tied to evaluation rules, which TJR himself calls "a little bit reckless" [akkPDEAm1jw@02:12].

| Stage | TJR rule | Cites |
|---|---|---|
| Evaluation, one-day-pass accounts | Risk the **entire max loss limit** on one trade at 1:2 R (only when "my strategy presents itself") | [akkPDEAm1jw@23:56–25:41] |
| Evaluation, consistency-rule accounts | Risk the full MLL at 1:1 R per day, one trade per day | [akkPDEAm1jw@26:47–27:58] |
| Evaluation (2025 / 2026 tutorial) | "Common practice": risk near maximum on evals, scale down once funded. Futures prop: either risk "way less" or ~1% accepting resets | [yiuFUp0kFz8@5:44:20–5:47:39; hBnD6T1M4w8@17:19; tT3lUnwayb0@37:21] |
| Funded | Risk **1/4 to 1/8 of the MLL** per trade; scale down to farm minimum winning days; on consistency-rule accounts, consider closing a big winner early | [akkPDEAm1jw@31:20–34:47; tT3lUnwayb0@34:36] |
| Funded, A+ only | No "partial-risk" B-trades on funded accounts | [tT3lUnwayb0@24:27] |
| Contract cap | "10 contracts is plenty" | [52nxvJKM57U@07:58] |
| Live behaviour | "Full-porting" funded accounts to pass in one day ("if it loses it loses") | [-mJ8mww-Flw@20:33; vIjIitndRXQ@10:15; 4KzkQEM28tc] |

If the bot is ever run on a prop account (DEFAULT, not TJR-stated): keep the §10 rules unchanged. Treat the firm's MLL, DLL, contract cap and consistency rule as **additional** hard limits. Never apply the evaluation sizing.

---

## 11. Trade management and exits

### 11.1 Stop placement tiers

| Tier | Placement | Era | Cites | Status |
|---|---|---|---|---|
| **S1: retrace swing ("second high/low")** | Beyond the swing made by the 1m/5m retrace, i.e. the high (for shorts) that the 1m counter-BOS created before the entry trigger | E4–E5 | [8PYgFVB0GHE@35:13; @40:14; @45:26; TEp3a-7GUds@35:03; 8QDDxwUV1KM@27:47] | **CANONICAL (bot default)** |
| S2: sweep / manipulation extreme | Beyond the swept extreme (the invalidation point); "I almost always put my stop above the liquidity sweep". 2026: stop "above the high, out of potential manipulation" | E2–E4 (also used in E5) | [1FunNCUw_jM@01:08; ss-dZPMnjeY@05:06; L5eRg5BZOOY] | Conservative alternative (`STOP_MODE=SWEEP_EXTREME`) |
| S3: zone stop | Beyond the entry FVG/OB/IFVG/EQ zone or the BOS-origin low | E2–E4 | [SHJHpedYh6A@3:50:46; tT3lUnwayb0@33:28; aobHuNcI1QM@6:15:35] | Historical, not used |

- **Buffer:** ≈0.5 pt beyond the level on ES [1FunNCUw_jM@05:44–06:50]. Bot: 0.5 pt (2 ticks).
- **Never a fixed number of points** [1FunNCUw_jM@10:43; ss-dZPMnjeY@02:50]. Typical E2 ES stop is 4–7 pt [KSiWKfPOlh4@08:33]; E5 stops are 16–35 ticks [hBnD6T1M4w8@11:45].
- **Minimum stop:** DEFAULT (not TJR-stated) 2 ES pts. If S1 is closer than that, use S2 provided TP1 still yields ≥1:1; otherwise skip.
- **Set the stop before entry.** It is a working order from the fill [SHJHpedYh6A@4:31:44; @4:40:41]. Stopless trading is a documented violation (§13.2).
- **No structural stop → no trade.** This covers both "no identifiable swing" and "invalidation too far for TP1 ≥ 1:1" [SHJHpedYh6A@4:11:17–4:11:51].

### 11.2 Take-profit ladder (targets = draws on liquidity in trade direction)

| Rung | Target | Cites |
|---|---|---|
| TP1 | Nearest liquidity giving **≈1:1**: 5m high/low, relative equal highs/lows, hourly H/L, or the nearest session H/L. Prefer an intermediate level for ≈1:1 over waiting "10 freaking years" | [8PYgFVB0GHE@40:47; 8QDDxwUV1KM@28:20; iVOjRDrjFM4@1:18:11; IVqY3b-KEbA@16:58] |
| TP2 | London / Asia / pre-market session H/L, hourly H/L, news-candle ("data") H/L | [8PYgFVB0GHE@32:26; @35:13; TEp3a-7GUds@35:03; 2ZArg3kPPkE@39:16] |
| TP3 (runner) | 4H H/L, 4H FVG, PDH/PDL; daily lows/highs as extended targets | [8PYgFVB0GHE@45:59; yiuFUp0kFz8@6:24:36] |

- **Skip if TP1 < 1:1** [5v4G4xJVKIQ@08:52; SHJHpedYh6A@4:11:17]. "It's a horrible RR" means no trade, even when the pattern is technically valid [_zzxRMbyE44@25:38].
- **Timeframe:** E2 used the execution TF and one above [FjSiLFrg5fo@04:35]. The E4 tutorial said "I don't really like taking profits on the 15-minute or 5-minute", preferring 4H/1H [aobHuNcI1QM@6:16:10]. E5 uses hourly/session for TP1 and 4H/daily for extended targets [8PYgFVB0GHE@40:47; @45:59]. **The bot uses the E5 ladder.**
- Skip a rung that has already been traded through. A rung closer than TP1 merges into TP1.
- If the next draw is a cluster of stacked "low-resistance" levels, target the far end of the stack [KxBRLErkel0@16:48; @17:54].
- **Never extend a TP out of greed** [CZRs2NuLQIw@06:42; _H9Gk8U7_VU@06:57; SHJHpedYh6A@4:45:41].

### 11.3 Partial sizes

| Era | Rule | Cites |
|---|---|---|
| E2 (canonical BC2) | 50% at TP1; 50% of the remainder at TP2; let TP3 run | [Iu_v4kuFQhk@01:39; ss-dZPMnjeY@05:06; IY9NJbaNyqA@03:59] |
| E4 | Half at TP1 + BE, then ladder [IVqY3b-KEbA@16:58; tWYSAHQpywE@30:45; A3RNBK_7gcM@54:33]. Tutorial: half / half of the remainder / rest [aobHuNcI1QM@6:12:44]. Variant: 25% at TP1 [-RAJEWMl-F0]. Single-target full exit at the first draw [vSduJn-l52A] | as listed |
| E5 | "Partials along the way", unquantified [8PYgFVB0GHE@35:13; @42:28]. "The majority of my position off" at the first 5m/15m highs [3SygD-YgZuQ@26:09]. Tells viewers to take partials and move to BE [kaPlPoXGXKw@21:15; c5f6hLzchyM@1:20:28] | as listed |

**Bot default: 50% / 25% / 25%.** With only two valid rungs, use 50/50. With one rung, close 100% at TP1. Round contract splits down at TP1 and up at the runner (DEFAULT).

### 11.4 Breakeven rule and the "seek and destroy" caveat

- **Default:** when TP1 fills, move the stop to the entry price [8PYgFVB0GHE@45:59–46:32; 2ZArg3kPPkE@36:31; iVOjRDrjFM4@1:18:58 ("before it gets vicious"); BMyeYQIj_vU@24:59; ss-dZPMnjeY@07:53].
- **Offset:** not stated. He once set BE "slightly in profit" [tWYSAHQpywE@30:45]. Fees make BE exits show as small losses [8PYgFVB0GHE@00:00–03:24]. DEFAULT (not TJR-stated): entry ± 1 tick in the trade's favour.
- **Other BE triggers he used:** after TP2 [WlnpOPPnBQw@08:04]; after the 5m lows / London lows are taken [rBdlDQgSjIc@33:39; _zzxRMbyE44@29:56]. These are not canonical.
- **Seek-and-destroy caveat (E3, Sep 2024):** after the open move, price often returns at ~10:15–11:00 ET to take the early entries and BE stops "to the tick", and only then completes the HTF move. His advice was "don't get too greedy with your take profits ... reward yourself for being right", and "maybe sometimes not even move our stop loss to break even" [p5CKu0FNbyg@00:32–01:04; @36:06; @38:20]. In E5 he once held without BE because "a 5m extension may produce a 1m BOS down to BE" [3SygD-YgZuQ@34:05–34:39].
  - **Bot:** keep BE at TP1, because the 50% TP1 partial already banks the 1R exposure. Expose `BE_MODE = AT_TP1 | AT_TP2 | OFF` and **backtest all three**. The seek-and-destroy re-entry window (10:20–11:00) is *not* traded (E3 only; E5 is done by 10:30).

### 11.5 Runner exits and exits other than TP/SL

| Exit | Rule | Cites | Bot |
|---|---|---|---|
| Hold rule | Don't close on floating P&L; exits only by TP/SL/defined rules. Don't exit on a drawdown smaller than 50% of the stop distance | [z9p7OThLkr4@03:21; OH--4nkbXlM@08:25–10:04; mV3YFmtnRdo@1:12:14; J1vPj1m6crQ@05:13–06:53] | enforced |
| **Opposing IFVG + SMT (early full exit)** | "If we inverse this gap right here, I'm fully just going to close this", after an opposing SMT. "I won't even wait for the stop to get hit." On FOMC: a 5m SMT + IFVG against → close all. Close fully if the idea weakens (the other index holds while yours moves = emerging opposing SMT) | [3SygD-YgZuQ@16:54–18:16; @23:10; 7a8tAGkVJac@18:46–19:58; rBdlDQgSjIc@33:39–35:24] | **Before TP1:** close 100% when a 5m IFVG closes against the position AND an opposing ES/NQ SMT exists at that swing. **After TP1:** same rule for the remainder. Do not reverse into the opposite trade unless it is a new full setup within the time window and budget (it counts as trade 2) |
| Runner on 1m BOS against | Closed the runner on a 1m BOS against the position *at HTF liquidity* [ss-dZPMnjeY@05:06–05:40]. Counter-rule: "don't wait for a BOS against you; a 1m BOS can be a fake-out", take profit into levels [6zXKK3Wrusg@11:00–11:34] | as listed | Runner only: exit on a 1m BOS against **only if** price has tagged a marked DOL within the last 5 bars (DEFAULT). Otherwise hold to TP/BE |
| Stagnation / time | Closed everything after ~1h45 of chop when a gap inverted [3SygD-YgZuQ@1:38:48]. Time exit ~2 pm ET after 2–2.5 h stagnation [-rYGugTIsbU@17:19]. At 10:30 he leaves an open trade on with its stop/TP [g27VsJS3a58@1:06:26]. An open trade may run past the entry cutoff [065lMUrD_kg@10:12–11:18] | as listed | 10:30 cutoff applies to **entries only**. DEFAULT hard flat for any remainder at 14:00 ET (from -rYGugTIsbU). Never hold overnight or over a weekend [Y1lqifylC4s@12:55] |
| Final TP cap | "I won't hold any longer past these data highs" | [2ZArg3kPPkE@39:16] | TP3 is final; no trailing beyond it |

### 11.6 Stop/TP integrity, adding and re-entry

- **Never move the stop away from price, never widen it, never move or extend a TP** once set. The only permitted stop move is toward BE/profit by §11.4 [SHJHpedYh6A@4:31:44; aobHuNcI1QM@6:10:28; _H9Gk8U7_VU@06:57; 88tyzO9CxGA@29:05].
- **Never add to a position** on dips ("that's how you lose all your bread") [c5f6hLzchyM@1:48:10–1:49:19]. The E4 "aggressive half + confirmation half" split entry [J1vPj1m6crQ@26:45; KxBRLErkel0@03:55] is not used: the bot enters once on the 1m trigger.
- **Re-entry** (`REENTRY_MODE`, default **OFF**):
  - E4 beginner rule: after a loss, "my idea is gone", done for the day [SHJHpedYh6A@4:45:10–4:50:07].
  - E4–E5 live practice: re-enter the **same idea** if it is not invalidated (the swept extreme holds and the 5m order flow is intact) and budget remains [iVOjRDrjFM4@11:52–12:26; tWYSAHQpywE@19:09–20:27; 2ZArg3kPPkE@21:25–23:56; WlnpOPPnBQw@06:22–06:57]. If a deep counter-wick does not close through, "redo step two into step three" with a fresh 5m BOS and continuation [8QDDxwUV1KM@34:30–36:48].
  - When ON, all of these must hold: (a) trade 1 hit its stop; (b) the S2 level (the sweep extreme) was **not** taken; (c) a complete new 5m confirmation → retrace → 1m trigger sequence forms; (d) it is before 10:30 ET; (e) risk = the remaining 0.5% budget, **never larger**. His heavier re-entry "to recover" [2ZArg3kPPkE@38:23] is a violation.
  - After 2 losses, done.

### 11.7 Done-for-the-day rules (any one ends new entries)

1. A win, defined as TP1 hit (including a TP1 partial followed by a BE runner): "take your money and leave" [SHJHpedYh6A@4:49:02; kH-rbepWkNE@32:49; ZioWcbxSuIw@10:50; 5RWTzr1D994@1:01:24; OJXkE2h2mz4@31:27].
2. A loss with `REENTRY_MODE=OFF`, or a second loss [SHJHpedYh6A@4:45:10; MiaTd3hh47I@59:24].
3. A missed or hesitated valid setup: "go home, you're done" [SHJHpedYh6A@4:53:32]. Bot analogue: an order not filled or a trigger missed for a technical reason → no chasing.
4. The full TP was hit, or the bias is completed: "our bias has been completed for the day" [xcDOMKaOIsk@16:13–16:46].
5. DOLs on **both** sides have been taken: "stand down once both sides' objectives are taken" [LLWBdwtpbiI@30:47].
6. The invalidation level was taken: "can't come above these highs or else it's toast" → done [xxJyvmHROb4@29:17; @36:55].
7. The clock: no entry after 10:30 ET; ES/NQ still misaligned at ~10:20 → done [8PYgFVB0GHE@53:13].
8. The daily budget is used (§10.2).

---

## 12. No-trade filters

Default state = **no trade**; the market must supply every condition [339amTioakE@04:26; 8PYgFVB0GHE@05:38 ("your strategy is ... more about telling you what trades not to take")]. Evaluate the filters in this order. Any FAIL means no new entry.

### 12.1 Time

| ID | Filter | Cites |
|---|---|---|
| F1 | No entries before **09:50 ET**. 09:30–09:50 is manipulation; ≤09:45 is "too early" | [yiuFUp0kFz8@4:31:51–4:33:36; SHJHpedYh6A@3:35:38; tT3lUnwayb0@27:18–28:59; 2ZArg3kPPkE@13:54; xxJyvmHROb4@12:24; @15:04; g27VsJS3a58@30:23] |
| F2 | Entry window 09:50–10:30 (primary 09:50–10:10 "macro"). **No new entry after 10:30** | [8PYgFVB0GHE@53:13; SHJHpedYh6A@3:45:39; L4xz2o23aPQ] |
| F3 | No pre-market entries, even if sweep + reversal completed pre-market ("the answer is always going to be no"); after the open, look only for the continuation step (2B) | [8PYgFVB0GHE@44:17–44:51; 8QDDxwUV1KM@16:03–19:25] |
| F4 | No PM session (E3 had a PM model; historical). No Asia/London trading on ES | [yiuFUp0kFz8@4:31:51; p5CKu0FNbyg@38:20; sjuWqKDsQtI@14:48] |
| F5 | Late sweeps: a sweep/confirmation that completes so late that the 1m trigger would fall after 10:30 → no trade. A sweep+BOS ~3 h after the open is "too late" | [OvmbAxG15YE@22:31; 8PYgFVB0GHE@54:21–55:30] |

### 12.2 News: `NEWS_MODE` switch

He said in Oct 2025: "the boot camp is dated ... there's some days that I'm actually willing to trade on now that previously in the boot camp I said not to trade on" [7a8tAGkVJac@01:41]. **Default `NEWS_MODE = STRICT`.** CURRENT reflects E4–E5 practice, much of it from live streams. Use it only after it has been separately backtested.

Times are ET. "Wait" = no entry until the release has printed and its 5m candle has closed, then the normal 09:50+ rules apply. "×0.5" and "×0.75" are §10.3 tiers.

| Event | STRICT (E1–E3 teaching; default) | CURRENT (E4–E5 practice) | Cites |
|---|---|---|---|
| **CPI** (08:30) | No trade all day | MIXED. Skipped in 2025 ("CPI news data tomorrow, I won't be trading") but traded and "full-ported" in 2026. Bot under CURRENT: trade after the open ×0.5 only if CPI is released pre-market and the reaction gate passes | STRICT [w5sUCqFH3Lg@06:49; qhuFg_OXdmE@11:24; S-scwzKRP-8@02:19]; skip [xE6m4UvuT5s@01:40; e_FV0Q14k8E; 2ZArg3kPPkE@02:19]; traded [ironJFzNBic@01:44; 4KzkQEM28tc; _zzxRMbyE44@02:45; @12:17] |
| **PPI** (08:30) | No trade | Trade after the open, ×0.5 | STRICT [w5sUCqFH3Lg@06:49; 4FEty6xgOc0@01:08]; CURRENT [2ZArg3kPPkE@1:00:08; BMyeYQIj_vU@22:15; gKOQbcg0r1M@32:23–33:32; hBnD6T1M4w8@14:33; vIjIitndRXQ] |
| **FOMC day** (14:00 decision, 14:30 presser) | No trade all day | **Never the FOMC-day open.** He trades only after the 14:00 decision / 14:30 presser, which falls outside the bot's 09:50–10:30 window. Bot: **no trade on FOMC day in either mode** | STRICT [w5sUCqFH3Lg@06:49; ch9Hjb7jF40@00:00]; CURRENT [7a8tAGkVJac@12:41–14:21; gKOQbcg0r1M@32:23; g27VsJS3a58@01:12]; FOMC-day loss [IVqY3b-KEbA] |
| FOMC minutes (14:00) | No trade (part of a no-trade stack) | Not discussed. Bot: trade AM ×1.0 (inferred: release is after the window) | [Uk8RiSde97w@00:32–01:42] |
| Day before FOMC | Not stated | Traded [A3RNBK_7gcM@01:07; g27VsJS3a58], but called "super ugly" / sideways [yiuFUp0kFz8@4:36:26; g27VsJS3a58@37:33]. DEFAULT: STRICT ×0.5, CURRENT ×1.0, chop filter applies | as listed |
| **NFP** (08:30 Fri) | No trade | **No trade** (unchanged) | [w5sUCqFH3Lg@06:49; IY9NJbaNyqA@02:17; IVqY3b-KEbA@53:31; MiaTd3hh47I@34:35] |
| Day before NFP | De-risk ("last trading day of the week, I'm going to be de-risking") | "Tentative"; suggests avoiding. DEFAULT: ×0.5 in both modes | [dy9jckID-pY@00:33–01:07; MiaTd3hh47I@58:46; QRoLG0QRiNM@43:52] |
| **Fed chair (Powell / successor) speech or testimony** | No trade that day | If it lands in the window (e.g. 10:00 hearing): finish a trade before it, or no trade until it is clearly not moving price. Bot: STRICT no trade; CURRENT no entry from 30 min before until 15 min after the start (DEFAULT), ×0.5 | STRICT [4moWbfm6smw@16:19–18:31; sjuWqKDsQtI@04:01; K8DwhtmvAW8@06:52]; 0.25% "reps" around Powell [G7eq6U8e3yw@01:41]; CURRENT [L5eRg5BZOOY; xxJyvmHROb4@00:00] |
| Other FOMC-member speeches | Not a concern | Not a concern | [4FEty6xgOc0@01:08; UvNYFPOQIfA; X6-mKG2s4Q4@03:50] |
| **10:00 ET red-folder releases** (ISM PMI, JOLTS, consumer sentiment, new home sales, PCE when at 10:00) | No entry before the release; then wait 15–30 min (≈ no trade before ~10:30, so effectively no trade in the bot window) | Wait until it is out, then trade (entry ~10:01 after a 10:00 PCE). Bot: no entry 09:50–10:05 (DEFAULT), then trade ×0.75 until 10:30 | STRICT [w5sUCqFH3Lg@08:31–09:07; IY9NJbaNyqA@01:09; PIoJUvpG4uc@02:21]; CURRENT [X6-mKG2s4Q4@02:40; J1vPj1m6crQ@23:30–24:40; QRoLG0QRiNM@43:52; G_N6bj11A9U] |
| **Unemployment claims** (08:30 Thu) | Tradeable after the open ×0.75. Be selective if the pre-market move is huge | Trade normally ("not too worried") | [7MBD3ow7I1g@04:29; QRvZgj3k8pk@03:27; X6-mKG2s4Q4@03:50; xE6m4UvuT5s@01:40] |
| **GDP** (08:30) | Trade after the open, de-risked ("high-risk day") ×0.5 | Traded after the 08:30 print. Bot ×0.75 | [1qIZmrvs9ao@04:36–05:09; 7MBD3ow7I1g; J1vPj1m6crQ] |
| **PCE / core PCE** (08:30) | ×0.75 (lesser news an hour before the open) | Traded after the release | [7MBD3ow7I1g@04:29–05:05; I0fLlm5s0yg; J1vPj1m6crQ] |
| **ISM** (10:00) | See 10:00 row. On NFP Friday it compounds → no trade | Wait for the release, then trade | [IY9NJbaNyqA@02:17; X6-mKG2s4Q4@02:40; G_N6bj11A9U] |
| **JOLTS** (10:00) | A stack (JOLTS + ISM + FOMC minutes + member) = no trade. JOLTS alone: unclear | Traded a JOLTS day (the day before FOMC) at reduced size | [Uk8RiSde97w@00:32–01:42; g27VsJS3a58@01:12; @44:08] |
| Other red/orange USD folders (any time) | Never before the release; wait 15–30 min after | Same | [w5sUCqFH3Lg@04:02–05:41; __fKQR5RR08@09:12] |
| Yellow folders, Philly Fed, Empire | Ignore | Ignore (traded an Empire day) | [w5sUCqFH3Lg@01:42; QRvZgj3k8pk@03:27; xxJyvmHROb4] |
| **US bank holiday** | No trade | No trade | [1FunNCUw_jM@12:24; Z-9HuHf5egU@13:43; 065lMUrD_kg@19:41; xxJyvmHROb4@00:00] |
| Day before a bank holiday | ×0.5 | ×0.5 | [1FunNCUw_jM@09:36; KSiWKfPOlh4@13:04] |
| **Day after a bank holiday** | Expected slow ("no money put in") → ×0.5 | Skipped (post-holiday + Powell + volatile weekend). Bot: ×0.5; no trade if combined with a Fed-chair event | [YGSXw_B-UgM@05:46; xxJyvmHROb4@00:00–00:33] |
| **Government shutdown** (releases cancelled or delayed) | DEFAULT: no trade during a shutdown week | He "avoided trading during the government shutdown" (Oct 2025), yet traded 15 Oct 2025 during it (−$152k). Bot: no trade in either mode | [8QDDxwUV1KM@00:00–00:32; xxJyvmHROb4] |
| News-heavy week | "Look for a reason not to trade" | — | [w5sUCqFH3Lg@09:07; 7Q3nalPsSpk@13:30] |
| Day-before-CPI chop | Expect chop; not ruled out | A 21-tick range before CPI → no trade | [Da6MH3H81TM@02:14; aobHuNcI1QM@5:46:13] |

**Reaction gate (all modes):** if a release drastically moves the market (huge wicks, outsized 5m candle), stop for the day. A muted reaction allows trading at the tier size [w5sUCqFH3Lg@06:16; @08:31]. TJR says to write your own numeric cutoff; "5 points in a 5-minute candle" was only an example [065lMUrD_kg@12:26–13:00]. DEFAULT (not TJR-stated): a release 5m candle range ≥ 3× the median 5m range of the prior 5 sessions' 08:30–10:30 window → done for the day.
**Release-time rule:** a setup forming *during* a release candle is never tradable [S-scwzKRP-8@11:35; G7eq6U8e3yw@02:50].
**Calendar:** load the US economic calendar (ForexFactory red/orange USD) each morning and build the weekly plan [w5sUCqFH3Lg@24:09; QRvZgj3k8pk@01:50]. If the calendar is unavailable → no trade (DEFAULT).

### 12.3 Structure, levels and the two indexes

| ID | Filter (no trade if...) | Cites |
|---|---|---|
| F6 | **ES and NQ disagree on 5m trend** (by 5m BOS) at the decision time: "the market is indecisive". Wait; if still misaligned ~10:20, done | [8PYgFVB0GHE@48:44–54:21; _zzxRMbyE44@20:47–21:37] |
| F7 | **No significant DOL swept** (session/1H/4H/PDH-PDL/data H-L) on ES or NQ; 5m/15m/1m levels don't count. A sweep without a reaction is not a sweep | [8QDDxwUV1KM@10:27; TEp3a-7GUds@22:04; 5RWTzr1D994@28:21] |
| F8 | The level was already traded through earlier (e.g. an Asia high taken by London) → "pretty useless" | [TEp3a-7GUds@22:04; 8QDDxwUV1KM@09:23] |
| F9 | No 5m confirmation (BOS body close / IFVG / 79% close); SMT alone is never a trigger | [TEp3a-7GUds@29:27; xxJyvmHROb4@23:00] |
| F10 | Touch-only entry: price touched the FVG/EQ with no 1m trigger. A single-candle or IFVG-only entry without the retrace sequence | [yiuFUp0kFz8@6:21:12; g27VsJS3a58@17:46–20:54] |
| F11 | **No structural stop**, or TP1 at the nearest valid DOL < **1:1** | [SHJHpedYh6A@4:11:17; 5v4G4xJVKIQ@08:52; _zzxRMbyE44@25:38] |
| F12 | No opposing DOL to target (no draw in the trade direction); entry too close to the opposing liquidity | [9sD9kTia4V4@09:46; IVqY3b-KEbA@02:54–04:01] |
| F13 | **Already-completed bias:** the day's draw was already reached, the full TP is already hit, or the SMT has already completed. "Don't long after draws were already taken"; "it's too late to enter" after the TPs are hit; "the majority of the move is done" | [xcDOMKaOIsk@16:13; KxBRLErkel0@26:11; g27VsJS3a58@38:47; _zzxRMbyE44@44:20; 3SygD-YgZuQ@1:21:48; -mJ8mww-Flw@40:19; 5RWTzr1D994@01:13] |

### 12.4 Bias and timeframe conflicts

| ID | Filter | Cites |
|---|---|---|
| F14a | 4H/1H order flow conflict with no sweep resolving it: no bias, so no trade ("without daily bias ... why are we entering?") | [yiuFUp0kFz8@4:59:53; framework §3.2] |
| F14b | Trading against the current bias is forbidden. **But** in E5 a significant-DOL sweep + SMT + 5m confirmation *updates* the bias ("let the market prove us wrong") [TEp3a-7GUds@39:03; yiuFUp0kFz8@6:27:56]. Bot: the bias state machine may flip only via that full sequence. Never trade a direction the state machine does not hold | [uGi6EeKnWSk@02:20; C5zIaZzbbgM@1:05:41] |
| F14c | "Don't marry the bias": after the invalidation is taken, do not re-assert the old bias | [9ar85Y6-5P4@18:52; xxJyvmHROb4@36:55–38:39] |

### 12.5 Regime: chop, range, tiny range

| ID | Filter | Cites |
|---|---|---|
| F15 | Chop / sideways: no 5m BOS, overlapping candles, a sideways 4H → no trade. Example: a day moving "only 21 ticks" (5.25 pt). Consolidation is "when I lose the most" | [OvmbAxG15YE@26:01–27:44; aobHuNcI1QM@5:44:29–5:46:13; 075G84Tx5OQ@00:00; ssPMxVk6B9Y; rBdlDQgSjIc@00:33] |
| F15-bot | DEFAULT (not TJR-stated; thresholds inferred): no trade if (a) the 09:30–09:50 ES range is < 5.25 pt (his 21-tick example), or (b) no 5m BOS/IFVG has printed on either index by 10:20, or (c) the 1H chart has made no new BOS in the last 8 hours of trading. Backtest and tune | — |
| F16 | Pre-open sideways or poor price action → be willing to have a no-trade day | [rBdlDQgSjIc@00:33; @02:16; ssPMxVk6B9Y@02:15–02:50] |

### 12.6 Operational

| ID | Filter | Cites |
|---|---|---|
| F17 | Risk not set or config invalid → no trade ("no risk set → no trade") | [065lMUrD_kg@18:36] |
| F18 | Daily budget used / done-for-day state (§11.7) | — |
| F19 | Bot analogue of "don't trade sick/emotional/travelling": data-feed gaps, clock skew, broker disconnect, or missing NQ feed → no trade | [VTwmHVAX29o@10:57–13:08; g27VsJS3a58@49:37] (analogy, inferred) |
| F20 | Wrong chart timeframe (he once read a 3m as a 5m): the bot asserts its bar intervals | [g27VsJS3a58@49:03–50:09] |

---

## 13. Psychology rules rewritten as hard bot constraints

TJR: "psychology is literally just discipline ... to stick to your strategy ... and stick to your risk management plan" [hBnD6T1M4w8@01:39; yiuFUp0kFz8@5:31:24]. For a bot, every psychological rule becomes an invariant.

### 13.1 Constraint table

| # | TJR's rule | Bot constraint | Cites |
|---|---|---|---|
| H1 | Only trade when every plan item appears; abandoning the edge = "flipping a coin" | Order submission requires all checklist booleans to be TRUE; no override path exists | [-zyDnjozaMM@07:43–08:16; @14:48; 065lMUrD_kg@19:41] |
| H2 | Come expecting not to trade; zero-trade days and weeks are fine | The default daily state is NO_TRADE. No minimum-trade quota or "activity" metric exists | [339amTioakE@04:26; VTwmHVAX29o@18:37; 8PYgFVB0GHE@57:49] |
| H3 | Take every valid setup; skipping after a loss forfeits the edge | If all filters pass and budget remains, the bot **must** take the signal. A recent loss/drawdown never suppresses a valid signal (except via §10/§11.7 rules) | [88tyzO9CxGA@16:14–17:20; @32:22] |
| H4 | Manage risk identically every trade | Size is computed only from §10 formula + pre-session tiers; no discretionary multiplier | [88tyzO9CxGA@32:22] |
| H5 | Don't increase risk after a win / during a win streak ($10k→$112k→0 story; "dumb to increase risk during a winning streak"; raising risk end-March cost him) | `RISK_PER_TRADE_PCT` is read-only intraday. Changes require an offline config change and are rate-limited to one per review period (≥ 6 months, §10.5) | [VTwmHVAX29o@03:49–04:56; ssPMxVk6B9Y@06:15; 8PYgFVB0GHE@00:35; SHJHpedYh6A@4:32:48] |
| H6 | No revenge trade; no upsizing after a loss | After a loss: either done (default) or the re-entry ≤ the remaining budget (§11.6). The re-entry size is never > the original | [EMSTUOAtCo0@07:18; C5zIaZzbbgM@52:16; 2ZArg3kPPkE@38:23 (violation)] |
| H7 | No FOMO / chasing; "the trade you missed is here tomorrow" | No entry when F5/F13 fire; no market-order "catch-up" after a missed trigger; a missed trigger means done | [a5PLl1uM7CQ@36:36; g27VsJS3a58@26:54; SHJHpedYh6A@4:53:32] |
| H8 | Never a third, thesis-less trade ("there was not a thought behind that position") | Every order must carry a complete signal record (sweep id, confirmation id, trigger id, stop, TPs). Orders without one are rejected; there is a hard cap of 2 | [rBdlDQgSjIc@58:05; @1:02:21–1:02:55] |
| H9 | Accept the max loss before entry; always set a stop; never full-port | The bracket (stop + TP1) is sent atomically with the entry. Naked entries are impossible. Risk ≤ caps | [88tyzO9CxGA@07:19–08:27; aobHuNcI1QM@7:52:50; SHJHpedYh6A@4:40:41] |
| H10 | Never move stops/TPs, don't hold losers to "be right" | Stop modifications are allowed only toward profit by §11.4 rules; TP prices are immutable | [88tyzO9CxGA@29:05–30:12; aobHuNcI1QM@6:10:28] |
| H11 | Don't close early on floating P&L | Exits are only TP/SL/§11.5 rules | [z9p7OThLkr4@03:21; mV3YFmtnRdo@1:12:14] |
| H12 | Never trade against the bias; don't marry it | §12.4 F14b/F14c state machine | [uGi6EeKnWSk@02:20; 9ar85Y6-5P4@18:52] |
| H13 | One win → done; don't search for more | §11.7 rule 1 | [4moWbfm6smw@03:16; SHJHpedYh6A@4:49:02] |
| H14 | Journal every trade *and* no-trade (direction, risk, confluences HTF→LTF, plan followed Y/N, post-trade recap) | Write a structured log row per session: all marked DOLs, the filter that blocked (if any), each checklist boolean with timestamps, fills, exits, R, and slippage | [CZRs2NuLQIw@02:15–08:19; VTwmHVAX29o@19:11–20:50; SHJHpedYh6A@4:16:25–4:23:47] |
| H15 | A "good loss" (all rules met) is acceptable; a rule-breaking win is still an error | The log classifies each trade as RULES_MET / RULE_BREACH. Any RULE_BREACH, win or lose, halts the bot pending review | [oJq8egtzCto@05:17; 7Q3nalPsSpk@10:09] |
| H16 | Judge on months/years, in %; don't change strategy after 1–2 losing weeks; a strategy needs months | Parameter changes are allowed only after ≥ 2–3 losing weeks *and* journal evidence, via an offline backtest. Never intraday | [PyCPHiO2nj0@01:02; @08:16; 8PYgFVB0GHE@13:25–16:14; aobHuNcI1QM@4:51:02] |
| H17 | Don't trade from fundamentals / macro opinion | No news-sentiment input changes direction; news only gates time and size | [UPA9LQW7phk@04:02; IY9NJbaNyqA@10:39] |
| H18 | One instrument; don't add indicators/confluences | ES/MES only (NQ = data). The confluence set is frozen to the canonical model | [065lMUrD_kg@13:35; LG_IbfjbaOo@16:49–18:32; _zzxRMbyE44@04:25] |
| H19 | Wins and losses are randomly distributed; think in probabilities | Evaluate only over ≥ 100-trade samples; no per-day "tilt" logic | [88tyzO9CxGA@33:29–35:08; SHJHpedYh6A@4:54:38] |
| H20 | Don't trade when off / sick / traveling | System-health gate (F19) | [VTwmHVAX29o@10:57; g27VsJS3a58@49:37] |
| H21 | Don't copy-trade others; don't trade on chat pressure | The bot takes no external signal inputs (no social or stream feeds) | [MiaTd3hh47I@44:06; kH-rbepWkNE@10:40] |
| H22 | Don't set daily $ goals | No profit target per day beyond the TP ladder; no "make back" logic | [SHJHpedYh6A@4:46:49–4:49:34] |

Human-only items with no bot equivalent: affirmations, goal setting, meditation, cortisol and anger management, sleep [oQSL21VryP4@04:35; 9ar85Y6-5P4@39:08–40:47; C5zIaZzbbgM@13:23].

### 13.2 Documented gaps between TJR's teaching and his live behaviour (NOT to be copied)

| Behaviour seen live | Contradicts teaching | Cites |
|---|---|---|
| **Extra impulsive trades:** two extra trades turned +$8k into −$52.7k; the third had "no thought behind it" | 1–2 trades max; win → done | [rBdlDQgSjIc@58:05; @1:02:21–1:02:55] |
| **Three attempts after big losses:** first-ever pre-market trade, stopped, re-entered, stopped (≈ −$100k); a third attempt off stream because his "risk tolerance" allows it | No pre-market entries; done after 2 losses | [gKOQbcg0r1M@32:23; @40:18] |
| **Upsized re-entry "to recover"** | Never upsize after a loss | [2ZArg3kPPkE@38:23; c5f6hLzchyM@1:17:21] |
| **4× risk:** doubled size *and* doubled stop on a bias he "married" (−$152k) | Fixed risk; don't marry bias | [xxJyvmHROb4@37:29] |
| **No-stop trades:** trading without a stop because the lows felt "overly guaranteed"; his student blew 10 funded accounts full-porting CPI with no stop | Always set a stop; never full-port, especially on news | [_zzxRMbyE44@32:43–33:16; X8Ag7BWd9dg@26:32–27:03; aobHuNcI1QM@7:52:50] |
| **Prop full-ports** (whole MLL on one trade, CPI/PPI/FOMC "full port") | ≤1–3%; de-risk on news | [-mJ8mww-Flw@20:33; vIjIitndRXQ@10:15; 7a8tAGkVJac@00:33; akkPDEAm1jw@23:56] |
| **Huge absolute risk** (~$40k per trade typical; a −$135k single trade) | Survive 3 losing days / a losing month | [C5zIaZzbbgM@51:01; 88tyzO9CxGA@17:20; QRoLG0QRiNM@42:10] |
| **Raised risk at end of March 2026** ("could have been a lot more had I not upped the risk") | Keep risk constant | [8PYgFVB0GHE@00:35] |
| **Trading against plan or timing:** trade at ~10:40 ET past his 10:30 cutoff; FOMC PM-session trade despite "no PM"; entries "very early" before both indexes confirmed; trading FOMC day itself (loss) | Time windows; ES/NQ alignment | [L5eRg5BZOOY; 7a8tAGkVJac; OJXkE2h2mz4@08:35; IVqY3b-KEbA] |
| **Joking "force a trade today ... no matter what"** | Default no-trade | [c5f6hLzchyM@32:52] |
| **Trading while emotionally triggered** (rage at chat, "cortisol blocker") | Don't trade when emotionally compromised | [C5zIaZzbbgM@13:23–14:41; L5eRg5BZOOY] |

---

## 14. Model evolution timeline

**Why this section exists.** TJR's model changed a lot between 2022 and 2026. Older videos often contradict newer ones, and he says himself that the old material is out of date. A bot that learns from mixed-era examples will pick up rules he has since dropped. **Use this table to label any TJR statement with its era. Then follow the E5 column, unless CANONICAL.md says otherwise.**

**Era key** (from CANONICAL.md):

| Era | Period | Main sources |
|---|---|---|
| E1 | Pre-Boot Camp, Sep 2022 – May 2023 | YouTube strategy videos (go3cEFGN-1c … Z9iXb9mBWgc) |
| E2 | Boot Camp 1 (May–Jul 2023) and Boot Camp 2.0 (Aug–Sep 2023) | kb/framework_v1.md |
| E3 | Sep 2023 – 2024 | Sep 2023 strategy video M6DQKMp-3Vo; Jan–Feb 2024 daily-bias videos; Trading Transformation (TT) Feb–Jul 2024; Jul–Nov 2024 strategy videos |
| E4 | 2025 | Live-trading recaps; the Mar 2025 5-hour guide SHJHpedYh6A; the Sep 2025 9-hour guide aobHuNcI1QM (much of it is older TT footage, so treat it as E3/E4 mixed); the Oct–Nov 2025 "cheat sheet" videos 8QDDxwUV1KM and xRuMUvW3T7Q |
| **E5 (canonical)** | 2026 | Path to Profitability (P2P) series, Jan 2026; 2026 tutorial yiuFUp0kFz8; updated strategy 8PYgFVB0GHE (Jun 2026); 2026 live streams; Oct 2026 bias and confluence videos |

### 14.1 Component-by-era table

| Component | E1 (2022 – May 2023) | E2 (BC1 + BC2.0, May–Sep 2023) | E3 (Sep 2023 – 2024) | E4 (2025) | **E5 (2026, canonical)** |
|---|---|---|---|---|---|
| **Bias source & timeframe** | Not consistent across videos:<br>• HTF liquidity used "for a bias" only [XxJAkUfbs0k@14:42]<br>• daily bias holds until the daily low is *closed* below [aOldFdtKsVc@30:45]<br>• a pre-market 15m BOS sets the day [T-Bo-9GDi3s@08:21]<br>• 1H structure is the day's bias and the 4H is ignored [ogK04pUS2GM@01:13] | Daily market structure is the intraday bias. Weekly/4H/1H agreement raises quality; the daily overrides the weekly [4FEty6xgOc0@09:20]. An HTF building block (OB/FVG/EQ) must be hit before the LTF sweep counts [__fKQR5RR08@21:32]. News bias is secondary [w5sUCqFH3Lg@15:17]. | **4H trend = bias**, and he "stays away from the daily". The 1H picks the execution TF [67vLAkcdPu4; OvmbAxG15YE; aobHuNcI1QM@5:01:42]. "Never really looking at the daily" [Qk-mHUlSJGU@08:28]. Counter-4H trades are allowed toward 4H EQ after an extension + sweep [Qk-mHUlSJGU@03:55]. "Do we need a daily bias? For me not necessarily" [BOx7Lk8Xs3o@03:23]. | No HTF-trend gate. Direction comes from **which key level is swept + 5m confirmation** [SHJHpedYh6A@3:34:32; BMyeYQIj_vU@05:34; xRuMUvW3T7Q@01:41]. Session-profile bias: London manipulation leads to NY continuation or reversal [e_FV0Q14k8E@21:55]. | 4H/1H order flow and respect or inversion of the HTF FVG/EQ that price is in [ironJFzNBic@08:30; yiuFUp0kFz8@6:10:28]. The 60–90-min window bias comes from swept vs. remaining DOLs on each side [FBX-gtFGWyU@02:12]. A sweep + SMT + 5m confirmation **overrides** the pre-market bias [TEp3a-7GUds@39:03]. ES and NQ must agree on the 5m trend [8PYgFVB0GHE@48:44]. |
| **Execution timeframes** | NY-open sweep → **1m** BOS [XxJAkUfbs0k@24:23; ogK04pUS2GM@02:19]. A **5m** BOS is wanted for a "more prominent" sweep [0R3TEHZgwxA@18:05]. Forex uses 30m boxes → 5m BOS [Z9iXb9mBWgc@13:19]. | HTF block (1H/15m) → 5m BOS → 1m BOS or 5m reaction candle (framework §4.E). | 4H/1H aligned → 5m execution with a 1m trigger. Opposed → 15m execution with a 5m trigger [yp1HQ7gbgYU@11:56; TBU7yfJzwrY@07:47]. 15m sweeps with 1m entries [60H1AumgjG8@10:12]. PM stack is 15m/5m/1m [i3FU-9OUU90@05:53]. | Standard flow: 5m order-flow shift → 5m continuation → 1m trigger [A3RNBK_7gcM@20:50; KxBRLErkel0@18:27]. An "aggressive" pure-1m variant exists [KxBRLErkel0@23:28]. | 4H/1H bias; **5m** confirmation and continuation; **1m** trigger [yiuFUp0kFz8@6:10:28; @6:22:20]. The 5m is the lowest TF for manipulation [9ar85Y6-5P4@12:13]. A 3m chart is "wrong timeframe" [g27VsJS3a58@41:48]. |
| **Confirmation types** | BOS = body close beyond the wick of the latest swing [aOldFdtKsVc@16:39]. Entry on the BOS close is allowed [XxJAkUfbs0k@38:47]. No SMT, no IFVG. | BOS must break a **prominent** swing [5v4G4xJVKIQ@03:22], then a third confirmation (reaction at FVG/EQ/OB) [ss-dZPMnjeY@06:46]. SMT: "I don't trade it and I don't even know what it is" [_6voYEdi5j4@05:00]. IFVG absent. | IFVG: skeptical in Jan 2024 [FdMf33jbUyM@05:12] → taught May 2024 [rMkghkG-ZjE@05:15] → "BOS-equivalent" by Jun–Jul 2024 [qswlc-I-DuA@06:02; v3c6A-Vs1Oc]. SMT introduced May 2024 [3svETDwdFUU@21:38] and "used every single day" by Jul 2024 [d5uOjnuzYhE@03:22]; on the 5m/15m, never the 1m [3svETDwdFUU@10:09]. | 5m BOS / IFVG / 5m SMT / **79% extension close** [xRuMUvW3T7Q@01:41; 8QDDxwUV1KM]. 79% first appears as a disrespect gauge [z0czA_OSq5M] and becomes a trigger [J1vPj1m6crQ; tWYSAHQpywE@06:01; xxJyvmHROb4@20:57]. A 1m SMT is used as an early trigger [rBdlDQgSjIc@24:28]. | **BOS or IFVG**; the IFVG is used "almost more than BOS" [4sRDnVmLcMk@11:28; yiuFUp0kFz8@3:50:04]. For stacked gaps, the close must clear the outermost gap [BdBxXKGWVjk@10:35]. SMT = bias strengthener + index picker, **never an entry** [X8Ag7BWd9dg@10:59]. SMT only counts after an order-flow change [9ar85Y6-5P4@08:59]. 79% close = alternative when no gap exists (C4). |
| **Continuation zones** | FVG, with a limit at its 50% [YMqC2ZvwCJg@17:54]. OB = candle before the expansion [AUUZ9Vk6p5E@10:13]. EQ + BOS [lyXKaPy-1SU@16:18]. Says he dislikes OBs [0R3TEHZgwxA]. | OB is the first choice; FVG; EQ (needs a close back beyond 0.5). Area of accumulation = OB [5v4G4xJVKIQ@06:06]. A reaction is required. | OB / FVG / **breaker** (new) / EQ [4XeIodHUtUQ; 67vLAkcdPu4@18:45]. BPR added [TihRnXjqM5c]. OB = only the leg that swept liquidity [rBsbMoNwIw4]. | OB/breaker still listed in Feb–Sep 2025 [-RAJEWMl-F0; BMyeYQIj_vU@10:33]. EQ is the "last resort" [SHJHpedYh6A@3:01:48]. Then: "removed ... for the last 6 months" [8QDDxwUV1KM@06:05]. | **FVG or EQ only.** "I no longer use order blocks. I no longer use breaker blocks" [wzq2AMsoJKY@17:05]. "Completely useless" [X8Ag7BWd9dg@14:50]. A 1m counter-BOS by itself can mark the retrace [8PYgFVB0GHE@26:15]. |
| **SMT index choice** | n/a (not used) | n/a (rejected) | Proto-SMT, Jan–Feb 2024: prefers the index that swept [BUZrKRaYa3A@06:21] or the cleaner trend [X6-mKG2s4Q4]. Jul 2024: trade the index that **made** the new extreme, which he calls "lagging" [d5uOjnuzYhE@03:22; BOx7Lk8Xs3o@09:31; Ias0HhHUqj4@02:16]. | Early 2025 still trades the index that made the extreme [SHJHpedYh6A@3:15:43], but practice is mixed (ES that failed [WlnpOPPnBQw; A3RNBK_7gcM; tT3lUnwayb0]). **Switch about Jul 2025:** "we always take the leading index. Before I used to take the lagging index" [5RWTzr1D994@56:46]. Pick the leader on the **execution** TF [rBdlDQgSjIc@24:28]. | Trade the index that **failed** to make the new extreme [7dTQA0t8SH0@10:41]. Confirmation must come from the index most opposed to the trade [3SygD-YgZuQ@05:14]. Exceptions:<br>• traded the sweeping NQ: "as long as one of the indexes is doing it for us" [8PYgFVB0GHE@37:25]<br>• chose the index nearer its target [kH-rbepWkNE@05:31]<br>• whichever index sets up first [FBX-gtFGWyU@06:07] |
| **Time windows (ET)** | NY open; sweeps usually within ~30 min [ogK04pUS2GM]. Forex: first 2 h of a session [Z9iXb9mBWgc@23:35]. PM and post-FOMC trades happen [0R3TEHZgwxA]. | Only at/after the 09:30 open [qecF411R83s@02:50]. "First hour and a half ... or else I'm done" (about 11:00) [065lMUrD_kg@10:47]. Avoid late session [9sD9kTia4V4@11:26]. | 09:50–10:10 "macro" + PM 13:50–14:10 [r-7-gWZsnZc@09:21]. PM model 13:30–15:00 [i3FU-9OUU90]. "10:30 territory ... off the charts" [BOx7Lk8Xs3o@20:12]. Sep 2024: "I just don't trade PM session"; optional 10:20–11:00 "seek and destroy" window [p5CKu0FNbyg@05:34; @38:20]. | Entries 09:50–10:30 only, none 09:30–09:50 [SHJHpedYh6A@3:35:38]. "At least 10 minutes into market open" [tWYSAHQpywE@06:01]. A pre-09:50 entry failed [2ZArg3kPPkE]. PM only for FOMC [egQLtQLmauk; 7a8tAGkVJac]. | 09:30–09:50 manipulation; 09:50–10:10 macro; done by 10:30; no PM [L4xz2o23aPQ@03:22; @05:02; @03:55]. "I usually wait until 9:50"; 09:45 is "too early" [0RBTSUGKA0w@1:09:23]. Practice exceptions at 09:36–09:48 [OJXkE2h2mz4; -mJ8mww-Flw; 3SygD-YgZuQ] and 10:40 [L5eRg5BZOOY; QRoLG0QRiNM]. |
| **News rules** | "Never trade CPI, FOMC, or NFP days"; trade other red-folder days if the reaction is muted [w1tC9OUdkGs@02:44]. Adds PPI and Powell days [ogK04pUS2GM@13:03]. Yet traded *after* the FOMC release in Nov 2022 [0R3TEHZgwxA@11:52]. Wait for 10:00 releases [0R3TEHZgwxA@08:27]. | Never CPI/PPI/FOMC/NFP [w5sUCqFH3Lg@06:49]. Other high-impact days: trade at 50% size after the open [7MBD3ow7I1g@04:29; 1FunNCUw_jM]. | "A single red folder = no trade" (Oct 2023) [6GNy02w2WIo]. Practice in Jan–Feb 2024: no CPI/PPI/FOMC/NFP [FdMf33jbUyM@04:02; hA9I8KsMC_U; dy9jckID-pY]; claims/ISM traded after the release [X6-mKG2s4Q4]; Powell days off [ox3p5Um1TqY@01:14]. | CPI avoided (Jun 2025) [e_FV0Q14k8E]. PPI traded, CPI skipped (Sep 2025) [2ZArg3kPPkE@02:19]. FOMC traded at/after 14:00 [egQLtQLmauk@03:26; 7a8tAGkVJac]. "The boot camp is dated ... some days I'm now willing to trade" [7a8tAGkVJac@01:41]. Waits for 10:00 releases [J1vPj1m6crQ@24:40]. | PPI traded [vIjIitndRXQ; gKOQbcg0r1M@26:32]. CPI traded with full size [ironJFzNBic@01:44; 4KzkQEM28tc; _zzxRMbyE44]. No NFP day [MiaTd3hh47I@34:35]. FOMC: no trade at the open [gKOQbcg0r1M@26:32]. Halve size on news days [hBnD6T1M4w8@13:59]. A 10:00 Fed-chair hearing means trade only if done before the Q&A [L5eRg5BZOOY]. → **NEWS_MODE switch (C12).** |
| **Risk sizing** | 0.5% in FOMC week [0R3TEHZgwxA]. "One trade a day, keep my risk low" [HDxpo-Vj3JA@30:14]. | 1–3% per trade or per day [RkMBoqbeUq8@03:26; @10:41]. Daily budget split 50/50 or 25/75 across ideas [5v4G4xJVKIQ@10:03]. Half size on news/holiday [1FunNCUw_jM@05:09]. | "More than risk 1% per trade" (1% baseline) [MNA9gtZCVqM@08:20]. "Never full port on news" [aobHuNcI1QM@7:52:50]. | 1% baseline, 2–3% for himself [a5PLl1uM7CQ]. Fixed risk amount, resized about every 6 months [VTwmHVAX29o@05:30]. 1–2 trades max; done after any win or loss [SHJHpedYh6A@4:30:02]. Live risk of $13K–$40K per trade; 2× stop with 2× size produced −$152K [xxJyvmHROb4@37:29]. | **Fixed contract count**; 1–3% "sweet spot"; accepts 3–4% on wide stops; halve size on news days or for unusually wide stops [hBnD6T1M4w8@10:03; @12:52; @13:59; yiuFUp0kFz8@5:39:52]. Prop accounts: risk as a fraction of max loss limit (MLL) [akkPDEAm1jw]. His "full-port" live behaviour is **not** to be copied (C11). |
| **TP / management** | TP1 → 50% off + BE; TP2 → 25%; runner [0R3TEHZgwxA@04:31; T-Bo-9GDi3s@14:26]. TPs at prior liquidity [XxJAkUfbs0k@31:58]. | TP1 ≈1:1 on the execution TF+1, "not 4H levels" [FjSiLFrg5fo@04:35]. 50% + BE [7MBD3ow7I1g@02:16]. "Don't wait for a BOS against you to exit" [6zXKK3Wrusg@11:00]. | TPs mainly at 4H/1H levels [_H9Gk8U7_VU] vs. matching-TF TPs [60H1AumgjG8]. TP1 <1:1 is OK [7zAy8xbzoNo]. BE at TP1 "maybe sometimes not" [p5CKu0FNbyg@00:32]. PM uses a single TP [i3FU-9OUU90]. | 25% at TP1 [-RAJEWMl-F0@03:50]. TP1 ≈1:1 at the nearest draw; BE with partials [8QDDxwUV1KM; xRuMUvW3T7Q; IVqY3b-KEbA]. "Don't trail" [WlnpOPPnBQw@04:42]. | TP1 ≈1:1 at hourly/session draws; extended TPs at 4H/daily [8PYgFVB0GHE@40:47]. BE after TP1 [8PYgFVB0GHE@45:59]. Scale out by halves [kaPlPoXGXKw]. Exit the runner on a 1m BOS against [kaPlPoXGXKw@1:07:40] or an opposing IFVG+SMT [3SygD-YgZuQ@16:54]. Stand down when "most of the objectives are taken" [LLWBdwtpbiI@30:47]. |
| **Stop placement** | Beyond the sweep + 4 pips (his own 2.5) [0R3TEHZgwxA@03:25]. Above the entry FVG [go3cEFGN-1c@15:43]. Beyond the sweep [XxJAkUfbs0k@31:58]. | Beyond the sweep + ~0.5 pt on ES [1FunNCUw_jM@01:08; @06:18]. "Under the invalidation point", not fixed points [ss-dZPMnjeY@05:06]. | Three tiers: beyond the sweep (best) → beyond the whole confluence → beyond the swing inside the confluence [-Ei4GP5mp60; aobHuNcI1QM@5:58:02]. | Beyond the zone / IFVG / swing extreme, "not so tight" [SHJHpedYh6A@3:50:46]. Tight above the candle [vSduJn-l52A]. Under the 1m lows that formed the BOS [tT3lUnwayb0]. | Beyond the **1m retrace swing ("second high/low")** [8PYgFVB0GHE@35:13; @40:14]. "Should have had our stop underneath this one-minute low" [c5f6hLzchyM@51:46]. No structural stop location → loss [C5zIaZzbbgM@39:56]. ES stops of 16/28/34 ticks [hBnD6T1M4w8@11:45]. |

### 14.2 Key turning points (narrative, chronological)

1. **2022 – early 2023 (E1): sweep → BOS is the core from the start.** His first strategy videos already have the skeleton that survives into 2026:
   - "one, liquidity sweep; two, break of structure; three, fair value gap entry" [YMqC2ZvwCJg@16:45];
   - "look for a liquidity sweep, look for a break of structure and honestly that's all you need" [XxJAkUfbs0k@38:47].
   - Entries in this era are loose: on the BOS close, or a limit at the FVG 50% [YMqC2ZvwCJg@17:54].
   - He trades several times a day [aOldFdtKsVc] and sometimes trades the PM session [0R3TEHZgwxA].
   - Even so, the news ban on CPI/FOMC/NFP is already present [w1tC9OUdkGs@02:44].

2. **Jul 2023 (BC1 day 41) → BC2.0 (Aug–Sep 2023): third confirmation, prominent swings, invalidation stops.**
   - After losses he stops entering on a bare LTF sweep + BOS [PyCPHiO2nj0@02:10].
   - BC2.0 requires a "third confirmation" (a reaction at OB/FVG/EQ) after the BOS [ss-dZPMnjeY@06:46].
   - The BOS must break a "prominent" high or low [5v4G4xJVKIQ@03:22].
   - The stop moves from "fixed points" to "under the invalidation point" [ss-dZPMnjeY@05:06].
   - This is the origin of C5 (continuation) and C8 (structural stop).

3. **Jan 2024: instrument switch to ES/NQ futures.**
   - He leaves forex because offshore brokers lost MetaQuotes licences and says he will "mainly just focus on S&P, NASDAQ" [YGSXw_B-UgM@01:08].
   - By late 2024: "at this point in time I am only trading the S&P 500 and NASDAQ" [AMlev-gYyHo@21:27].
   - From here on, **every forex-only rule is out of scope** for the bot. That includes entries on the BOS close with no third confluence (framework §11.4).

4. **Feb–Apr 2024 (Trading Transformation): the old course is disowned and the model is systemized.**
   - On the Boot Camp: "I don't even really want to mention the boot camp anymore" [HlllJ9YH3Qw@05:15]; "I didn't give you guys a systemized strategy" [QI1ihQiH-F8@11:51].
   - The bias moves from the daily to the **4H** [67vLAkcdPu4].
   - The HTF point of interest becomes a **sweep of 1H/4H highs/lows**, "not on the 15-minute, not on the 5-minute" [aobHuNcI1QM@5:09:27].
   - Breaker blocks join the continuation list [4XeIodHUtUQ].

5. **May–Jul 2024: IFVG, SMT and the time windows arrive.**
   - The IFVG is taught [rMkghkG-ZjE] and then called equivalent to a BOS [qswlc-I-DuA@06:02].
   - SMT reverses the BC1 "I don't trade it": "most of my trade setups are based off of this" [d5uOjnuzYhE@03:22].
   - The 09:50–10:10 "macro" window is defined, along with a PM window [r-7-gWZsnZc@09:21].
   - At this stage he executes on the index that **made** the new extreme and calls it "lagging" [d5uOjnuzYhE@05:02; BOx7Lk8Xs3o@09:31].

6. **Mar–Jun 2025: the 2026 skeleton is in place, but OBs are still in use.**
   - The 5-hour guide teaches: sweep of a key level → 5m BOS/IFVG/SMT → FVG/EQ/OB/breaker → 1m BOS/IFVG trigger → TPs at the draws.
   - It has **no HTF trend gate** and allows entries only from 09:50 to 10:30 [SHJHpedYh6A@3:34:32; @3:35:38].
   - The 79% extension close appears [J1vPj1m6crQ; KxBRLErkel0].
   - Bias becomes session/liquidity-profile based [e_FV0Q14k8E@21:55].

7. **About Apr–Jul 2025: OBs/breakers are dropped and the SMT index rule flips.**
   - In Oct 2025 he says he made his P&L "without using order blocks and breaker blocks for the last 6 months" [8QDDxwUV1KM@06:05].
   - On 7 Oct 2025: "we always take the leading index. Before I used to take the lagging index, but I changed that around ... two and a half to three months ago" [5RWTzr1D994@56:46]. That dates the change to about Jul 2025.
   - The terminology is inconsistent: in 2024 "lagging" meant the index that swept; in 2025–26 "leading" means the index that failed to make the new extreme [rBdlDQgSjIc@03:23]. **The bot should key on the behaviour (which index failed to make the extreme), not on the word.**

8. **Sep–Nov 2025: news rules loosen, and he says the Boot Camp is dated.**
   - He trades PPI after the open [2ZArg3kPPkE@02:19; BMyeYQIj_vU@22:15] and FOMC at/after the 14:00 release [egQLtQLmauk; 7a8tAGkVJac].
   - His statement: "the boot camp is dated, okay? I do not trade the same way ... My strategy is different. My confluences ... are different ... There's some days that I'm actually willing to trade on now that previously in the boot camp I said not to trade on" [7a8tAGkVJac@01:41].
   - The cheat-sheet videos add the **2B rule** (an extra 5m sweep after 09:30 when the HTF sweep was pre-market) and formalize the 79% close [xRuMUvW3T7Q@01:41; 8QDDxwUV1KM].

9. **Jan 2026 (P2P): the canonical teaching.**
   - "Those other strategy videos are pretty dated ... my strategy has changed since then" [TEp3a-7GUds@01:06; repeated at yiuFUp0kFz8@5:52:03].
   - The fixed time template is stated: 09:30–09:50 manipulation, 09:50–10:10 entries, done by 10:30, no PM [L4xz2o23aPQ@03:22; @03:55].
   - Risk moves from "1% of balance" to a **fixed contract count**, with half size on news days or very wide stops [hBnD6T1M4w8@10:03; @13:59].
   - On OBs: "I no longer use order blocks. I no longer use breaker blocks" [wzq2AMsoJKY@17:05].
   - He also says plainly that the published model is an approximation of his discretion: "my strategies changed ... ideation/toolbox" [yiuFUp0kFz8@6:03:43].

10. **Jun 2026: the updated strategy video (8PYgFVB0GHE) is the latest complete statement.** It adds three operational details:
    - (a) the 5m retrace can be detected purely as a **1m BOS against** the new 5m trend, with entry on the next 1m BOS back [8PYgFVB0GHE@26:15];
    - (b) **ES/NQ 5m alignment** is required, and a disagreement means no trade [8PYgFVB0GHE@48:44];
    - (c) the stop goes beyond the "second high/low" (the retrace swing) [8PYgFVB0GHE@35:13].
    - It also shows him trading the index that *did* sweep on 28 May 2026 [8PYgFVB0GHE@37:25]. This is an unresolved exception (see §18, A-12).

11. **Oct 2026: further simplification for beginners.**
    - Bias is defined for the first 60–90 minutes only, from swept vs. remaining DOLs [FBX-gtFGWyU@02:12].
    - "First hour to hour 30 minutes of price action" [FBX-gtFGWyU@00:00].
    - IFVG is his "#2 confluence"; OBs are absent from "the only confluences that I use" [TYbpk7WogHI@00:00; @07:45].
    - Nothing in Oct 2026 contradicts CANONICAL.md.

**Rule for the bot (binding):** when two eras conflict, use E5 (CANONICAL.md). Use E4 only to fill gaps E5 does not cover, and never use E1–E3 to override E5. Statements from 2025–2026 live streams that contradict his own *teaching* go in the register (§18) as practice, not as rules. Examples are trading without a stop, full-porting, third trades and pre-market trades.

## 15. Why it works: TJR's stated reasoning (HIS CLAIMS, not proven edge)

Everything in this section is **TJR's explanation and self-report**. None of it is independently verified. The microstructure story is a narrative common to "smart money concepts" and has not been demonstrated in these sources. The bot must not assume an edge exists: it must be **backtested without look-ahead, then paper-traded (≥3 consecutive green months, §10.5)** before any live capital.

### 15.1 His causal claims

| Claim (his words, paraphrased) | Cites |
|---|---|
| **Market makers need liquidity to fill size.** Institutions/"the algorithm" cannot fill large sells inside an uptrend without moving price against themselves. Above highs sit breakout buys and short-stops, so pushing above a high lets them sell into that liquidity at the best price, and price reverses | [Lxnu7InGhGE@03:21–03:56; AMlev-gYyHo@05:37–08:23; GJbC6nO3oHQ@18:12; Vulini8xbB0@12:47–15:31; 8QDDxwUV1KM@02:48–03:22] |
| **Sweeps are the "opportunity", not a certainty.** A sweep gives the *potential* for orders to be filled. A BOS/IFVG afterwards is the evidence that they were filled ("orders filled → change in order flow → continuation → target other draws") | [8PYgFVB0GHE@17:55–20:08; TEp3a-7GUds@10:36; ESsy0uoFAz4@01:38] |
| **Opposing liquidity is the exit.** Market makers who sold at the high must buy back where others are selling, below lows, so the opposite DOLs are targets | [KtC2SbemF6w@08:28–10:12; FBX-gtFGWyU@03:51–04:24; Vulini8xbB0@42:47–44:22] |
| **Order flow / imbalance.** FVGs are imbalances price tends to rebalance, giving continuation entries. An IFVG or BOS close against the flow means the flow changed | [xcDOMKaOIsk@03:20–04:26; z0czA_OSq5M] |
| **Higher timeframes hold higher power.** "I would much rather put my faith in a high time frame hourly sweep ... Higher time frame is always going to hold higher power." HTF levels define bias and targets; 1m levels don't | [5RWTzr1D994@28:21; FjSiLFrg5fo@09:06; BOx7Lk8Xs3o@03:55] |
| **Time / manipulation.** "Institutional money comes into the market every single day at market open", so 09:30–09:50 is manipulation and entries come after it. New money at each session open manipulates the prior session's H/L. 08:30 is pre-market manipulation. A pre-market sweep is followed by a 5m manipulation after the open (2B) | [BMyeYQIj_vU@07:45; L4xz2o23aPQ@01:09–03:22; 8QDDxwUV1KM@16:03–19:25; yiuFUp0kFz8@4:31:51] |
| **SMT.** ES/NQ divergence at a level shows one index "failing", signalling a trend change "before even being able to see a BOS or IFVG" | [7dTQA0t8SH0@05:00–07:18] |
| **Edge = probability, and the strategy is mainly a filter.** "Higher probability of being right than wrong, and when we win we make more than when we lose." Example math: 70% at 1:1.5 is net positive. "Your strategy is ... more about telling you what trades *not* to take" | [88tyzO9CxGA@05:00–05:35; @22:55–23:27; EMSTUOAtCo0@01:06–02:15; 8PYgFVB0GHE@05:38; @56:04–56:41] |

### 15.2 His self-reported results (unaudited)

| Period | Claim | Cite |
|---|---|---|
| Jan 1–Jun 1 2026 | $874,782 gross on a live account; **64.29% daily win rate; average R:R ≈ 1:1.33**; average win ≈ $22k vs average loss ≈ $16k; Jan ≈ $41k, Feb ≈ $148k, Mar ≈ $293k, Apr ≈ $230k, May ≈ $34k; "no red month". He says BE trades show as small losses with fees, so the true win rate is higher | [8PYgFVB0GHE@00:00–03:24] |
| 2025–26 months | Sep +$491k, Nov +$475k, Jan +$41k, Feb +$148k, Mar +$293k, Apr MTD +$214k; one losing month −$26k; no December trading | [L5eRg5BZOOY@14:49; QRoLG0QRiNM@22:53] |
| Apr–Oct 2025 | "$1,047,984 in 6 months" (title) | [8QDDxwUV1KM] |
| Aug 2025 | $156,943 for the month | [BMyeYQIj_vU@00:00–00:37] |
| May 2025 | $291,456 for the month; "every trade posted" | [KxBRLErkel0@00:00–00:34] |
| 2026 | "No red month this year, all trades live on stream" | [88tyzO9CxGA@27:57–28:33] |

Arithmetic on his own figures (inferred, not a claim): 0.6429 × 1.33 − 0.3571 × 1 ≈ **+0.50 R per trading day before costs**. This number is only as good as the unaudited inputs.

**Caveats the bot's operators must accept:**
- The stats are self-reported from his journal (Tradezella screenshots) and are **not audited**. One 2026 stream is titled "I GOT EXPOSED FOR FAKING TRADES" [L5eRg5BZOOY]; the content is a rant about the allegation and settles nothing.
- His results come from discretionary trading at much larger and more variable risk than the bot will use (§13.2). Win rate and R depend on discretion the OMD can only approximate; he says he deliberately leaves pieces out [yiuFUp0kFz8@5:52:37–6:04:49].
- The live P&L includes NQ trades, FOMC/CPI full-ports and prop-account gaming that the bot excludes. So **his numbers are not an estimate of the bot's performance.**
- Losing stretches are real: −$122k in one week [MiaTd3hh47I]; a 3-day losing streak [C5zIaZzbbgM]; May 2026 weeks of −$10k and −$70k [8PYgFVB0GHE@13:25].
- **Requirement:** a walk-forward backtest on ES/NQ 1m data (no look-ahead, real fees and slippage), then ≥ 3 consecutive green months of paper trading, then minimum-size live. Any claimed edge is treated as a hypothesis until those stages pass.

## 16. Decision procedure

### 16.1 Configuration (all DEFAULT unless cited)

```
NEWS_MODE            = STRICT        # STRICT | CURRENT  (§16.3)
CONT_MODE            = STRICT        # STRICT (FVG/EQ + 1m counter-BOS) | SIMPLE (1m counter-BOS only) [8PYgFVB0GHE@26:15]
STOP_MODE            = RETRACE       # RETRACE (E5, 1m retrace swing) | SWEEP (E2–E4, sweep extreme)
ES_ONLY_POLICY       = HALF_IF_VALID # HALF_IF_VALID | SKIP   (§17.4, flagged)
ENTRY_EARLIEST       = 09:50 ET      # optional 09:45
ENTRY_LATEST         = 10:30 ET      # [L4xz2o23aPQ@05:02]
ALIGN_DEADLINE       = 10:20 ET      # [8PYgFVB0GHE@53:13]
FLATTEN_AT           = 12:00 ET
RISK_PCT             = 1.0%          # teaching default; 1–3% band [yiuFUp0kFz8@5:39:52]
SPLIT_BUDGET         = false         # true → trade 1 at 0.5×, trade 2 allowed at the remaining 0.5×
MIN_R_TP1            = 1.0
STOP_BUFFER_TICKS    = 2
STOP_MAX_PTS         = 16 (ES)       # skip above; ×0.5 above WIDE_STOP
WIDE_STOP            = 2 × median(last 20 stops) else 10 pts
EQ_TOL               = ES 0.50 pt, NQ 2.00 pt
SMT_SYNC_BARS        = 2
SWEEP_MIN_TICKS      = 1
```

### 16.2 State machine

| State | Entered when | Leaves to | On |
|---|---|---|---|
| **S0 PRE_OPEN** | session start (≥08:30 ET; levels built continuously since 18:00) | S1 | 09:25 |
| **S1 DAY_FILTER** | 09:25 | S2 if `day_allowed`; else **DONE(NO_TRADE: news/holiday)** | — |
| **S2 PREP** | | S3 if any DOL on ≥1 side; else **DONE(NO_TRADE: no DOL)** | levels, bias, 2B flag computed |
| **S3 WATCH_SWEEP** | 09:30 | S4 on a significant sweep+reaction (ES or NQ). Pre-open sweep with `HTF_SWEPT_PREOPEN` → S3b. Time > 10:30 → **DONE(NO_TRADE: no setup)** | |
| **S3b WAIT_2B** | 2B required | S5 when a 5m manipulation (5m H/L swept in the trade direction, 5m trend intact) → continuation via 5m SMT; or back to S4 if the 5m trend breaks the other way; > 10:30 → DONE | [8QDDxwUV1KM@16:03] |
| **S4 WAIT_CONFIRM** | sweep exists | S4a on a 5m BOS/IFVG/79% close in the reversal direction (on ≥1 index). Sweep extreme exceeded + 5m close beyond it → S3 (level consumed) | |
| **S4a WAIT_ALIGN** | confirmation exists | S5 when both indexes are in the new 5m trend (with the most-opposed index confirmed). ≥ 10:20 still misaligned → **DONE(NO_TRADE: misaligned)** | [8PYgFVB0GHE@48:44–53:13] |
| **S5 WAIT_RETRACE** | aligned | S6 when the 5m FVG/EQ is touched (STRICT) or immediately (SIMPLE). Invalidation (5m close through the outermost new-leg FVG, or sweep extreme exceeded) → S3. No retrace and a new 5m swing forms → re-anchor EQ/FVG and stay in S5 | [X8Ag7BWd9dg@09:20] |
| **S6 WAIT_COUNTER_1M** | in zone | S7 on a 1m BOS against the trade. Invalidation → S3 | [8PYgFVB0GHE@26:15] |
| **S7 WAIT_TRIGGER** | counter-BOS done | S8 on a 1m BOS/IFVG/79% close back in the trade direction **and** all gates pass. A gate fails for a non-structural reason (e.g. time < 09:50) → stay. TP1 < 1R or no stop → S5. Time > 10:30 → **DONE(NO_TRADE: late)**. Invalidation → S3 | |
| **S8 IN_TRADE_PRE_TP1** | filled | S9 at TP1 (50% off, stop → BE). Stop hit → S10(loss). Early-exit rule → S10(scratch/loss). 12:00 → S10 | |
| **S9 IN_TRADE_POST_TP1** | TP1 done | partial at TP2; runner to TP3/stretch; BE stop / early-exit / 12:00 → S10(win) | |
| **S10 POST_TRADE** | flat | **DONE(win)** if any TP hit. **DONE(loss)** unless `SPLIT_BUDGET` and trades_today = 1 and budget left → S3 (only if time ≤ 10:30). Never a third trade | CANONICAL |
| **DONE** | terminal | journal, cancel all orders, flat | |

### 16.3 NEWS_MODE table

| Event (US, red folder) | STRICT (E1–E3 teaching; **default**) | CURRENT (E5 practice) |
|---|---|---|
| CPI day | no trade [w5sUCqFH3Lg@06:49] | **mixed**: skipped in Sep 2025 [2ZArg3kPPkE@02:19], "full-ported" in 2026 [4KzkQEM28tc] [_zzxRMbyE44@02:45]. DEFAULT: trade after the open at ×0.5 (flag) |
| PPI day | no trade | trade after the open at ×0.5 [2ZArg3kPPkE@02:19] [hBnD6T1M4w8@14:33] |
| FOMC day | no trade | no AM trade. A PM trade at/after 14:00/14:30 is TJR practice [7a8tAGkVJac@12:41], but `FOMC_PM_ENABLED=false` (no E5 PM rule-set) → effectively no trade |
| NFP day | no trade | no trade [0R3TEHZgwxA@43:30] |
| Fed-chair speech day | no trade [4moWbfm6smw@16:19] | no trade if the speech is before 12:00 ET (DEFAULT); else normal |
| US bank holiday | no trade | no trade [xxJyvmHROb4@00:00] |
| Day after a holiday + Powell | no trade | no trade [xxJyvmHROb4@00:00] |
| Day before a holiday | ×0.5 [1FunNCUw_jM@09:36] | normal (not stated) |
| Other red folder at 08:30 | trade after the open (release + ≥15–30 min has passed) at ×0.5 | trade, ×1.0 (not stated; DEFAULT) |
| Red folder at 10:00 | no entries before release + 30 min → effectively no trade (window ends 10:30) [w5sUCqFH3Lg@04:02] [IY9NJbaNyqA@01:09] | wait until it is out: entries allowed from 10:15 (DEFAULT +15 min) to 10:30 |
| 08:30 release spikes the market | STRICT reaction gate: if the 08:30 5m candle range > 2.5× its 20-day median → no trade (DEFAULT number; TJR asks for a self-set numeric cutoff [065lMUrD_kg@12:26]) | not applied |

### 16.4 Pseudocode (one trading day)

Concepts used, all defined in the glossary (§2–7): swing high/low (two-candle), BOS (body close), FVG, FVG stack (outermost gap), IFVG, EQ (50% Gann box, premium/discount), 79% extension close, DOL (types in §8.1), sweep + reaction, SMT (bullish/bearish, completed), leading index, 2B manipulation, session H/L, PDH/PDL, NWOG/NDOG, NEWS_MODE, entry window.

```
procedure RUN_DAY(date):
  # ---------- S0/S1: day filter ----------
  cal  ← economic_calendar(date)          # times ET, impact, event type
  if is_us_bank_holiday(date) or is_early_close(date): return DONE("holiday")
  (allowed, news_mult, earliest_override) ← NEWS_FILTER(cal, NEWS_MODE)
  if not allowed: return DONE("news")
  earliest ← max(ENTRY_EARLIEST, earliest_override)      # e.g. 10:15 for a 10:00 release in CURRENT

  # ---------- S2: prep (both feeds) ----------
  for X in {ES, NQ}:
     L[X] ← DOLS(X)                        # Asia, London, pre-market, PDH/PDL, 1H/4H swings,
                                           # EQH/EQL (EQ_TOL), stacked, data H/L, NWOG/NDOG
     L[X] ← remove_traded_through(L[X])    # "useless" levels
     HTF[X] ← htf_order_flow(X, {4H,1H})   # trend, respect/invert of HTF FVG/EQ
  smt_htf ← smt_state(ES, NQ, {4H,1H}); if smt_htf.completed: smt_htf ← NONE
  preopen ← significant_sweep_with_reaction(ES or NQ, window=[prev 16:00, 09:30))
  HTF_SWEPT_PREOPEN ← preopen ≠ NONE
  bias ← BIAS(preopen, HTF, L, smt_htf)    # §8.2 order: Q1 > Q3, Q2 tie-break → LONG/SHORT/NONE
  if no DOL above and none below on ES: return DONE("no DOL")
  trades ← 0 ; budget ← 1.0

  loop each closed 1m bar t from 09:30 to FLATTEN_AT:
    # ---------- S3: sweep ----------
    if state = WATCH_SWEEP:
       if t > ENTRY_LATEST: return DONE("no setup")
       s ← newest significant sweep+reaction on ES or NQ at t ≥ 09:30   # 8.3; HTF beats LTF
       if HTF_SWEPT_PREOPEN and s = NONE: s ← preopen ; need2B ← true
       if s ≠ NONE:
          dir ← opposite(s.side)            # swept high → SHORT, swept low → LONG
          counter_bias ← (bias ≠ NONE and dir ≠ bias)
          smt ← SMT_AT(s.level, ES, NQ, tf=5m, sync=SMT_SYNC_BARS)  # discard if completed
          if counter_bias and smt = NONE: continue          # G2 DEFAULT
          state ← WAIT_CONFIRM

    # ---------- S4: 5m confirmation ----------
    if state = WAIT_CONFIRM and 5m bar closed:
       if beyond(s.extreme_updated, dir) and 5m body closed beyond s.level against dir:
            consume(s); state ← WATCH_SWEEP; continue
       conf ← first of {IFVG_5m(outermost gap of leg), BOS_5m(swing bounding leg), EXT79_5m(leg)} in dir
       if conf: state ← WAIT_ALIGN

    # ---------- S4a: alignment ----------
    if state = WAIT_ALIGN:
       if trend_5m(ES) = dir and trend_5m(NQ) = dir:      # most-opposed index has confirmed too
           if need2B: state ← WAIT_2B else state ← WAIT_RETRACE
       elif t ≥ ALIGN_DEADLINE: return DONE("misaligned")

    # ---------- S3b: 2B ----------
    if state = WAIT_2B and t ≥ 09:30:
       m ← sweep of a 5m swing in direction opposite(dir) with trend_5m(ES,NQ) still = dir
       if m and SMT_AT(m.level, ES, NQ, 5m): zone ← m ; state ← WAIT_COUNTER_1M   # SMT = continuation
       elif m: zone ← m ; state ← WAIT_RETRACE
       if trend_5m flips against dir on either index: state ← WATCH_SWEEP

    # ---------- S5: continuation ----------
    if state = WAIT_RETRACE:
       leg ← current 5m leg in dir (after confirmation)
       Z ← {FVG_5m(leg) unbalanced} ∪ {EQ_5m(leg) premium/discount side}
       if invalid(leg): state ← WATCH_SWEEP; continue  # outermost-FVG IFVG against dir, or s.extreme broken
       if CONT_MODE = SIMPLE or price_touched(Z): state ← WAIT_COUNTER_1M

    # ---------- S6/S7: 1m ----------
    if state = WAIT_COUNTER_1M and BOS_1m(against dir): state ← WAIT_TRIGGER
    if state = WAIT_TRIGGER:
       if invalid(leg): state ← WATCH_SWEEP; continue
       if t > ENTRY_LATEST: return DONE("late")
       trig ← BOS_1m(dir) or IFVG_1m(dir) or EXT79_1m(dir)   # on ES; NQ shift = supportive
       if trig and t ≥ earliest:
          sym ← INDEX_POLICY(smt, dir)                      # §17.4 → ES, or NONE
          if sym = NONE: return DONE("canonical index NQ, policy SKIP")
          stop ← STOP(STOP_MODE, dir) ± STOP_BUFFER_TICKS   # 8.8; NONE → back to WAIT_RETRACE
          if stop = NONE or stop_pts > STOP_MAX_PTS: state ← WAIT_RETRACE; continue
          T ← LADDER(dir, L[ES])                            # 8.9
          if R(T[1]) < MIN_R_TP1: state ← WAIT_RETRACE; continue
          score ← OPTIONAL_SCORE(...)                       # §9.1
          if score ≤ 0: continue
          mult ← news_mult × (0.5 if stop_pts > WIDE_STOP) × (0.5 if score ≤ 2)
                 × (0.5 if sym is ES-fallback) ; mult ← max(mult, 0.25)
          mult ← mult × (0.5 if SPLIT_BUDGET and trades = 0 else 1) ; mult ← min(mult, budget)
          qty ← SIZE(equity × RISK_PCT × mult, stop_pts)    # §17.3; 0 → skip
          if qty = 0: return DONE("size < 1 MES")
          ENTER(sym, dir, qty, stop, T) ; trades += 1 ; budget −= mult ; state ← IN_TRADE

    # ---------- S8/S9: management ----------
    if state = IN_TRADE:
       if hit(T[1]) first time: close 50%; stop ← entry + 1 tick (favourable)
       if hit(T[2]): close 50% of the rest ; if hit(T[3]) or stretch: close all
       if 5m body close inverts the trade's continuation FVG
          or (opposing SMT at a DOL and IFVG_1m against dir on ES and NQ): close all
       if runner only and BOS_1m(against dir) at an HTF DOL: close all
       if t ≥ FLATTEN_AT: close all
       if flat:
          if any TP hit: return DONE("win")
          if SPLIT_BUDGET and trades = 1 and budget > 0 and t ≤ ENTRY_LATEST:
               state ← WATCH_SWEEP ; continue                # full sequence again
          return DONE("loss/scratch")
  return DONE("time")

procedure NEWS_FILTER(cal, mode):  # returns (allowed, size_mult, earliest_override)
  per §16.3 table; multiple events → most restrictive row wins

procedure INDEX_POLICY(smt, dir):  # §17.4
  if smt = NONE: return ES
  lead ← index that FAILED to make the new extreme (on 5m)
  if lead = ES: return ES
  if ES_ONLY_POLICY = SKIP: return NONE
  return ES (flag fallback, ×0.5) only if ES itself passed G3–G7 on its own chart, else NONE
```

**Every no-trade exit**, logged with a reason code:
- holiday / early close
- news (by mode)
- 08:30 reaction gate (STRICT)
- data or calendar missing
- no DOL
- counter-bias trade without SMT
- no sweep by 10:30
- sweep consumed (trade-through) and no other
- misaligned at 10:20
- no retrace (impulsive)
- continuation invalidated
- no structural stop / stop too wide
- TP1 < 1R
- score ≤ 0
- canonical index NQ under SKIP
- size < 1 MES
- trigger after 10:30
- budget exhausted / win already / loss already / third trade

---

## 17. Applying it to ES/MES (Lucrum SPX)

### 17.1 Contract specifications (CME facts, not TJR; verify at deployment)

| | ES (E-mini S&P 500) | MES (Micro E-mini) | NQ (feed only) |
|---|---|---|---|
| Multiplier | $50 × index | $5 × index | $20 × index |
| Tick | 0.25 pt = **$12.50** | 0.25 pt = **$1.25** | 0.25 pt = $5.00 |
| $/pt | **$50** | **$5** | $20 |
| Contract months | H, M, U, Z (quarterly) | same | same |
| Roll | DEFAULT: roll to the next quarter on the Thursday 8 days before the third-Friday expiry (volume roll); recompute all levels on the continuous back-adjusted series, or on the front contract per day (DEFAULT: front contract; take session levels only from the contract actually traded) | | |

### 17.2 Session hours

- **Globex (ETH + RTH)**: Sun–Fri 18:00–17:00 ET (17:00–16:00 CT), with a daily halt 17:00–18:00 ET (16:00–17:00 CT).
- **Bot RTH** = equity cash session **09:30–16:00 ET (08:30–15:00 CT)**. ES keeps trading until 17:00 ET.
- **ETH** = all Globex time outside RTH. Asia, London and pre-market levels come from ETH. "S&P = NY session only" for trading [sjuWqKDsQtI@14:48].
- **Session H/L computation**: max(high) and min(low) of 1m bars whose open time t satisfies:
  - Asia: 18:00 ≤ t < 03:00 (spanning midnight)
  - London: 03:00 ≤ t < 08:30
  - Pre-market: 08:30 ≤ t < 09:30
  - Prior day (PDH/PDL): previous 18:00 ≤ t < 17:00
- The NDOG is [close of the 16:59 bar, open of the 18:00 bar]. The NWOG is [Fri 16:59 close, Sun 18:00 open].
- 1H/4H bars are anchored to the 18:00 ET Globex open (4H closes at 22:00, 02:00, 06:00, 10:00, 14:00). This is DEFAULT and matches the TradingView futures default (inferred); TJR notes that 1H/4H closes at 10:00 cause movement [aobHuNcI1QM@8:24:34].

### 17.3 Sizing

```
risk$      = equity × RISK_PCT × mult          # RISK_PCT 1% default; TJR teaches 1–3% [yiuFUp0kFz8@5:39:52]
contracts  = floor(risk$ / (stop_pts × $/pt))  # ES $/pt = 50; MES = 5
if contracts_ES ≥ 1: trade ES (optionally top up with MES: floor((risk$ − n_ES·stop·50)/(stop·5)))
elif contracts_MES ≥ 1: trade MES
else: skip
```

- **Partials** need a quantity that splits 50/25/25. With fewer than 4 ES lots, size in MES so the split is possible. If the position is a single lot, a partial is impossible: exit everything at TP1 (DEFAULT).
- **Example**: $100,000 × 1% = $1,000 risk with a 6-pt stop gives ES = floor(1000/300) = 3 (risk $900), or MES = floor(1000/30) = 33.
- **TJR's live 2026 practice** is a **fixed contract count** chosen so the largest typical stop is acceptable, with 3–4% accepted on wide stops [yiuFUp0kFz8@5:39:52–5:43:12] [hBnD6T1M4w8@11:45–12:52]. The bot uses the risk-based formula above (CANONICAL #11). Dollar risks in his streams (about $30–40K per trade [C5zIaZzbbgM@51:01] [2ZArg3kPPkE@22:00]) are not scaled into the bot.

### 17.4 Translating his NQ examples / SMT index rule

- **Never** convert NQ point distances to ES. Re-run every rule on the ES chart. TJR's NQ stops and targets do not transfer; only the sequence does.
- Many of his E5 trades are on NQ ([8PYgFVB0GHE] 28 and 27 May; [3SygD-YgZuQ]; [YfS5yBQgubI]; [rBdlDQgSjIc]). As test cases, they become "did ES satisfy G1–G12 at the same time?"
- **Canonical rule**: trade the **leading** index, the one that **failed** to make the new extreme at the swept DOL, judged on the execution TF [5RWTzr1D994@56:46] [7dTQA0t8SH0@13:25] [rBdlDQgSjIc@24:28].
- **Implication for an ES-only bot:**

| Case at the swept DOL | Canonical pick | Bot action |
|---|---|---|
| NQ makes the new extreme, ES fails (ES leads) | ES | Trade ES. This is the textbook case [TEp3a-7GUds@30:35] [yiuFUp0kFz8@4:24:09] [5RWTzr1D994@29:58] |
| ES makes the new extreme, NQ fails (NQ leads) | NQ | **DEFAULT `HALF_IF_VALID`** (not TJR-stated, flagged): trade ES at ×0.5 only if ES itself passed sweep → 5m confirmation → alignment → continuation → 1m trigger on its own chart, with an ES structural stop and ES TP1 ≥ 1R. Alternative `SKIP`. Rationale: E3–early-E4 TJR traded exactly this "lagging/swept" index [BOx7Lk8Xs3o@08:20]; it often still worked but with less expansion ("we got the worst index on this trade" [tWYSAHQpywE@44:45]; "NQ shorts did worse" [5RWTzr1D994@56:46]; "should have longed ES rather than NASDAQ" [3SygD-YgZuQ@25:01]). |
| Both make the extreme, or no divergence | none | Trade ES if ES passes all gates. When both set up, he takes "the one that happened first" [FBX-gtFGWyU@06:07] |
| Only NQ reaches a DOL, ES has no corresponding level | — | Valid opportunity ("one index is enough" [8PYgFVB0GHE@38:00]). ES leads by definition, so trade ES |

### 17.5 Required data feeds

| Feed | Use |
|---|---|
| ES and NQ front-month OHLCV bars at **1m, 5m, 15m, 1H, 4H, 1D**, full Globex history ≥ 15 trading days, ET time-stamps (bar open), with real-time closed-bar events | levels, swings, FVG/IFVG/BOS, SMT, alignment (15m for context and the E3 PM model only) |
| Session H/L engine (Asia/London/pre-market/PD/NDOG/NWOG; EQH/EQL; stacked levels; consumed-level tracking per index) | §8.1 |
| Economic calendar: US red-folder events with **exact ET time**, impact, and type (CPI, PPI, FOMC decision/press conference, NFP, Fed chair speech, ISM, PCE, claims, GDP…) | NEWS_MODE |
| US exchange holiday and early-close calendar (CME + NYSE) | day filter |
| Account equity, open orders and fills | sizing, budget |

### 17.6 Order types

| Purpose | Order |
|---|---|
| Entry | Market (or marketable limit, ≤2 ticks through) sent at the 1m trigger-bar close. No resting limit orders at FVG/EQ, because "never enter on the touch" |
| Stop loss | Server-side **stop-market**, placed with the entry as an OCO bracket |
| TPs | Resting **limit** orders at the ladder levels: TP1 50%, TP2 25%, TP3 25%. Place 1 tick before the level (DEFAULT) so a tag of the exact level fills |
| BE move | Modify the stop to entry + 1 tick when TP1 fills |
| Early exit / flatten | Cancel the bracket, then market close |
| Forbidden | Pre-market orders; orders outside 09:50–10:30 for entry; adding to losers; trades without a stop |

## 18. Ambiguity register

**What this is.** A list of every item where TJR is unclear, contradicts himself, or decides by eye. For each one the register sets a deterministic bot default. Each default is a **parameter**: the bot must expose it in config and record it in the trade journal, so that backtests can re-tune it.

**How to read the columns.**
- **Evidence count** = the number of distinct videos cited in the "what TJR says" column for that item. It is a measure of how much material exists, not how strong it is. The E5 sources outweigh the rest.
- **Era tags:** E1–E5 as defined in §14.

| ID | Item | What TJR says (by era, cited) | Evidence | **RECOMMENDED BOT DEFAULT** | Rationale | Risk if wrong |
|---|---|---|---|---|---|---|
| A-01 | **"Prominent / significant" swing, for the sweep (DOL)** | No numeric definition in any era.<br>• E1: "most recent, most prominent high and low before the NYSE open" [XxJAkUfbs0k@24:23]<br>• E2: "prominent" = the high/low before a big extension [5v4G4xJVKIQ@03:22; M6DQKMp-3Vo]<br>• E3: only 1H/4H highs/lows, "not on the 15-minute, not on the 5-minute" [aobHuNcI1QM@5:09:27; 67vLAkcdPu4@15:43]<br>• E4: session H/L, 1H/4H swings, PDH/PDL, 1H/4H FVGs; drop levels already taken [SHJHpedYh6A@3:38:24]<br>• E5: significant = 1H/4H or session extremes; stacked/equal levels add weight; "5m sweeps are too weak" [Vulini8xbB0@28:45] | 8 | **Significant DOL** = one of:<br>• Asia (18:00–03:00), London (03:00–08:30) or NY pre-market (08:30–09:30) high/low<br>• PDH/PDL<br>• a 1H or 4H swing high/low (2-candle swing on that TF, wick price)<br>• relative equal highs/lows (within 2 ticks on ES, inferred) on 15m or higher<br>• the 08:30 news-candle H/L<br><br>Keep a level only if it is **untouched since it formed**. Drop it if price has closed beyond it. 5m/15m swings are **never** significant DOLs; they are allowed only as the 2B sweep (A-19). | This matches C1 and his explicit E5 list. Using levels fixed by the session clock or by the TF makes the rule deterministic. | Too strict means missed trades on days he would call a 15m sweep significant (E1/E3 accepted 15m). Too loose means fake sweeps; he says 5m sweeps "too weak". |
| A-02 | **Swing used for the 5m BOS** | E2 requires a *prominent* swing [5v4G4xJVKIQ@03:22]. Every later era just says "most recent swing" [Zzk864cVJek@02:50; nR9Iikd6V2s; n97MKj6wGFk; TYbpk7WogHI]. Doji/indecision swings don't count [4LERkD7z_w4; kH-rbepWkNE@31:39]. A close exactly equal to the level is not a BOS [nR9Iikd6V2s; C5zIaZzbbgM@53:00]. | 7 | Use the **most recent confirmed 5m swing in the leg that ran into the sweep**, where a swing is the 2-candle rule and doji candles are skipped. A BOS needs a **body close strictly beyond** that swing's wick price, by at least 1 tick. Only the *first* opposite close counts as the BOS; later closes in the same direction are continuation [n97MKj6wGFk]. | This matches C4 and every E3–E5 definition. "Bounds the leg into the sweep" filters the tiny internal swings that E2 tried to filter with "prominent". | If he really means a bigger swing, the bot will confirm too early on small internal breaks. Backtest a variant that uses the swing of the last 5m leg of at least N points. |
| A-03 | **Sweep validity / depth** | Trade-through is needed; "barely miss it" is not a sweep [OvmbAxG15YE@19:07]; equal highs touched ≠ swept [Da6MH3H81TM]. It must react: "a run without a reaction = not swept" [AMlev-gYyHo@25:24; pKIo-aVic-c@16:26]. A high exceeded by about $1 counted as a potential sweep [eEg0_zc8Hxg@45:12]. Wick or close are both acceptable (E2) [UPA9LQW7phk@10:49]. | 6 | Swept = price trades **≥1 tick beyond** the level. Then, within 3 bars of 5m (15 min, inferred), price **closes back inside** the level, or a 5m confirmation (A-02/A-21) fires before the price runs **more than 2× the ES 5m ATR(14)** beyond it (inferred). Otherwise mark the level "taken, no reaction" and move to the next DOL. | Encodes "trade through AND react" from C3. The numbers are inferred placeholders. | Depth thresholds are guesses. A deep sweep that later reverses would be missed, so tune on data. |
| A-04 | **Stop placement** | • E1: beyond the sweep + buffer [0R3TEHZgwxA@03:25]; or above the entry FVG [go3cEFGN-1c@15:43]<br>• E2: beyond the sweep + ~0.5 pt [1FunNCUw_jM@06:18]; "under the invalidation point" [ss-dZPMnjeY@05:06]<br>• E3: three tiers, sweep → confluence → inner swing [-Ei4GP5mp60; aobHuNcI1QM@5:58:02]<br>• E4: zone/IFVG/swing extreme, "not so tight" [SHJHpedYh6A@3:50:46]; tight above the candle [vSduJn-l52A]<br>• E5: beyond the "second high/low" (the 1m retrace swing) [8PYgFVB0GHE@35:13]; under the 1m low after a too-tight stop lost [c5f6hLzchyM@51:46]; no clean spot → loss [C5zIaZzbbgM@39:56] | 11 | `STOP_MODE = RETRACE_SWING` (E5): stop = 1 tick beyond the extreme of the 1m retrace swing that the 1m trigger broke, + **0.5 pt ES buffer** [1FunNCUw_jM@06:18].<br>`STOP_MODE = SWEEP_EXTREME` (conservative alternative): 1 tick beyond the sweep extreme + 0.5 pt.<br>**No trade** if neither swing exists (C8). | This is C8 exactly. The 0.5 pt buffer is the only numeric buffer he ever stated for ES. | RETRACE_SWING gives tighter stops and higher RR, but more wick-outs (he lost to a tight stop on 22 Jan 2026). Backtest both modes. |
| A-05 | **Stop size in points** | Rarely stated:<br>• E2: ES ~4–7 pt (framework §6); the 7Q3n stop was missed by 2.7 pt<br>• E5: ES stops of 16, 28, 34–35 ticks (4–8.75 pt) [hBnD6T1M4w8@11:45]; a student's NQ 200-tick (50 pt) stop [9ar85Y6-5P4@33:37]<br>• Fixed size means a wide stop gives lower R:R [hBnD6T1M4w8@12:52] | 3 | No fixed stop. Use the structural stop (A-04). **Skip** if stop > **12 pt ES** (inferred cap ≈1.4× his largest cited 34–35-tick stop). Use **half size** if stop > 9 pt (C11 "unusually wide"). Skip if stop < 2 pt (inferred; noise). | Keeps the bot inside the stop range he actually shows. | The caps are inferred. Too low a cap drops valid high-volatility days; tune it. |
| A-06 | **TP timeframe / ladder** | • E2: TP1 on execution TF+1, "not 4H levels" [FjSiLFrg5fo@04:35]<br>• E3: mainly 4H/1H [_H9Gk8U7_VU] vs. matching TF [60H1AumgjG8]<br>• E4: TP1 ≈1:1 at the nearest draw (hourly lows) [8QDDxwUV1KM]<br>• E5: TP1 ≈1:1 at hourly/session draws; extended at 4H/daily [8PYgFVB0GHE@40:47]; 5m highs as TP1 [YfS5yBQgubI@35:05; 3SygD-YgZuQ] | 7 | Build the ladder from **unswept DOLs in the trade direction**, ordered by distance:<br>(1) nearest 5m swing / session / 1H level giving ≥1:1;<br>(2) next session H/L (London/Asia/pre-market);<br>(3) 1H H/L;<br>(4) 4H H/L, 4H FVG edge, PDH/PDL.<br>Use at most 4 TPs. | This is C9. | Using 4H levels as TP1 would cut the win rate; using only 5m levels would cut RR. |
| A-07 | **Minimum RR for TP1** | "Skip if TP1 < ~1:1" (C9). TP1 below 1:1 is acceptable [7zAy8xbzoNo; zAWKsS6kw4Y]. He skipped a 1:0.7 trade [5v4G4xJVKIQ@07:44]. Skipping bad-RR setups is explicit in E5 [_zzxRMbyE44]. | 4 | Require **TP1 R ≥ 1.0** after the buffer. If the nearest DOL gives < 1.0R, use the next DOL as TP1. If that DOL is beyond 3R, skip the trade (inferred). | Follows C9. | Some of his winners had TP1 at about 0.8R (25% at 1:0.8 [-RAJEWMl-F0@03:50]); this rule loses those. |
| A-08 | **Breakeven timing** | • E1/E2: BE at TP1 [T-Bo-9GDi3s@14:26; 7MBD3ow7I1g@02:16]<br>• E3: "maybe sometimes not even move our stop loss to break even" [p5CKu0FNbyg@00:32]<br>• E4: BE after TP2 once [WlnpOPPnBQw]; usually at TP1 [IVqY3b-KEbA; xRuMUvW3T7Q]<br>• E5: BE after TP1 [8PYgFVB0GHE@45:59]; "should have moved BE at London lows" [-mJ8mww-Flw@18:45]; BE when a named draw is taken [_zzxRMbyE44] | 8 | Move the stop to **entry + 1 tick (covers costs)** when **TP1 fills** (50% partial). Do not move it earlier. | Majority view in E5 and C9. | BE is hit "to the tick" before continuation [p5CKu0FNbyg]. Backtest a "BE after TP2" variant. |
| A-09 | **Partial sizes / runner exit** | 50% at TP1 [8PYgFVB0GHE; kaPlPoXGXKw]; 25% at TP1 once [-RAJEWMl-F0]; halves at each later level [kaPlPoXGXKw]. Runner exit:<br>• E2: "don't wait for a BOS against you" [6zXKK3Wrusg@11:00]<br>• E5: 1m BOS against exits the runner [kaPlPoXGXKw@1:07:40]; opposing IFVG + SMT [3SygD-YgZuQ@16:54]<br>• He stated an IFVG exit and then ignored it [b_ksEb6cJ50] | 6 | 50% at TP1. Then 50% of the remainder at each later TP. Close the remainder at the last TP. Exit the runner early only after TP1, and only when a **1m BOS + 1m IFVG against** the trade print together, or a 5m close through the continuation FVG/EQ. Hard time exit for any runner: **12:00 ET** (inferred; he held to 11:11 [3SygD-YgZuQ] and past noon once). | Follows C9. Requiring two signals avoids the 1m fake-outs he warned about in E2. | A late exit gives back profit; an early exit truncates 1:5+ runners. |
| A-10 | **News handling** | • E1–E3: never CPI/PPI/FOMC/NFP/Powell days [w1tC9OUdkGs@02:44; ogK04pUS2GM@13:03; w5sUCqFH3Lg@06:49; FdMf33jbUyM@04:02]<br>• E4: PPI after the open OK, CPI skipped [2ZArg3kPPkE@02:19]; FOMC traded at/after 14:00 [egQLtQLmauk; 7a8tAGkVJac]; "the boot camp is dated" [7a8tAGkVJac@01:41]<br>• E5: CPI "full-ported" [ironJFzNBic@01:44; 4KzkQEM28tc; _zzxRMbyE44]; PPI traded [vIjIitndRXQ]; no NFP [MiaTd3hh47I@34:35]; no FOMC at the open [gKOQbcg0r1M@26:32]; halve size on news [hBnD6T1M4w8@13:59] | 14 | `NEWS_MODE = STRICT` (**default**, C12): no entries on CPI, PPI, FOMC, NFP, Fed-chair testimony/speech days, or US bank holidays. On other red-folder days: wait until 15 min after the release, then trade at 50% size.<br>`NEWS_MODE = CURRENT` (E5 practice): CPI/PPI at 08:30 → trade after 09:30 at **50% size**; FOMC day → no morning trade, PM only after the 14:30 presser (only if `PM_FOMC=on`, default off); NFP day → no trade; Fed-chair at 10:00 → trade only if fully in by 09:55, otherwise none. | His teaching is strict; his 2026 practice is looser and was profitable on several CPI days. STRICT costs fewer trades and has smaller tail risk. | STRICT skips about 4–6 days a month that E5 practice trades profitably. CURRENT exposes the bot to news spikes, which already caused −$24K [iVOjRDrjFM4] and wick-outs. |
| A-11 | **10:00 ET releases** | Wait until it is out [0R3TEHZgwxA@08:27; ox3p5Um1TqY@05:46; J1vPj1m6crQ@24:40; c5f6hLzchyM]. He traded through a minor 10:00 release: "not really worried about the red folder news" [kH-rbepWkNE@07:43]. | 5 | For a high-impact 10:00 release (ISM, JOLTS, consumer confidence, new home sales): **no entry 09:55–10:01**. Allow entries 10:01–10:30 if the setup forms after the release. Positions opened before 09:55 are held with their stop. | Matches his consistent "wait for release". | Losing the 09:50–10:00 core window on those days. |
| A-12 | **SMT index edge cases** | • E3: trade the index that **made** the extreme [d5uOjnuzYhE@03:22]<br>• Switch about Jul 2025 to the one that **failed** [5RWTzr1D994@56:46]; leader on the execution TF [rBdlDQgSjIc@24:28]<br>• Confirmation from the most-opposed index [3SygD-YgZuQ@05:14]<br>• Exceptions: traded the sweeping NQ [8PYgFVB0GHE@37:25]; nearer-to-target [kH-rbepWkNE@05:31]; first to set up [FBX-gtFGWyU@06:07]<br>• "We got the worst index" [tWYSAHQpywE@44:45] | 10 | (1) If exactly one index sweeps the DOL, the other is the **leader** (it failed to make the extreme). (2) If **both** sweep, there is no SMT; use the one that prints the 5m confirmation **first**. (3) If neither sweeps but one is within 2 ticks, treat it as unswept. (4) Determine leader/lagger on the **5m** for setups and the **1m** for triggers. (5) Always require **both** indices to show 5m confirmation in the trade direction before entry (C2 alignment). | Codifies C10 plus his 2026 rule to listen to the opposed index. | When the lagging index runs further (as on 25 Aug 2025), the bot underperforms; that is acceptable. |
| A-13 | **Trading only ES/MES when NQ is the canonical (leading) index** | The bot can trade only ES/MES (CANONICAL). When ES swept and NQ held, the rule says trade NQ. He did trade the sweeping index once and won [8PYgFVB0GHE@37:25]. Picking the wrong index cost money [rBdlDQgSjIc@35:24; 5RWTzr1D994@56:46 "NQ shorts did worse"]. | 4 | `ES_WHEN_NQ_LEADS = HALF`: allow the ES trade only if **ES itself** completes every step (its own 5m confirmation, its own 5m FVG/EQ retrace, its own 1m trigger) at **50% risk**, with ES's own DOLs as TPs. Alternative `SKIP`. When ES is the leader, trade at full size. | Keeps the edge where it is strongest. He says the sweeping index tends to give a worse trade, but still a valid one. | HALF means more trades with lower expectancy; SKIP means fewer trades. Decide by backtest. |
| A-14 | **Bias when ES and NQ disagree** | "If they tell two different things → no trade" (C2). He stood aside on a 2026-06-01 divergence [8PYgFVB0GHE@48:44]. "Don't trade while the indexes disagree" [_zzxRMbyE44]. He fought a divergence and lost [MiaTd3hh47I]. In E3 the leans could differ by index [hA9I8KsMC_U]. | 5 | **No trade** while the last confirmed 5m BOS/IFVG direction differs between ES and NQ. Re-check at every 5m close until 10:20. At 10:20, if still misaligned → done for the day. | C2 and an explicit E5 example. | Some days with a clean ES-only move are lost. |
| A-15 | **Time-window edge 09:45–09:50** | • "I usually wait until 9:50"; 9:45 "too early" [0RBTSUGKA0w@1:09:23]<br>• "ideally ... not within first 10–15 minutes" [9ar85Y6-5P4@18:52]<br>• ≥10 min [tWYSAHQpywE@06:01]<br>• E4 rule "no entries 9:30–9:50 even if the setup completes" [SHJHpedYh6A@3:35:38]<br>• Practice: entries at 09:36–09:48 that won [OJXkE2h2mz4; -mJ8mww-Flw; kH-rbepWkNE; 3SygD-YgZuQ] and a 09:46 entry that lost [2ZArg3kPPkE]<br>• The 09:52 manipulation-leg example [L4xz2o23aPQ] | 9 | **No 1m trigger accepted before 09:50:00 ET.** Sweep, confirmation and continuation may form from 09:30. A trigger that formed 09:45–09:50 is **not** chased; the bot waits for the next 1m trigger at or after 09:50 inside the same continuation zone. | His stated rule; the early entries are self-labelled exceptions. | Missing the occasional fast 09:40 move. |
| A-16 | **After 10:30** | • E2: about 11:00 cutoff [065lMUrD_kg@10:47]<br>• E3: off the charts by 10:30 [BOx7Lk8Xs3o@20:12]; 10:20–11:00 seek-and-destroy [p5CKu0FNbyg@38:20]<br>• E5: done by 10:30 [L4xz2o23aPQ@05:02; 8PYgFVB0GHE@53:13]; "first hour to hour 30" [FBX-gtFGWyU@00:00]<br>• Practice: 10:32 entry lost [0RBTSUGKA0w]; 10:40 entries won [L5eRg5BZOOY; QRoLG0QRiNM], the latter labelled "way later than I would typically" | 8 | **Last trigger at 10:30:00 ET.** No new entries after that. Open positions are managed to TP/stop/runner rules (A-09). | C7. | Losing some late winners; that is acceptable. |
| A-17 | **Daily trade/loss limits** | • Teaching: one trade/day [z9p7OThLkr4@05:01]; 1–2 [065lMUrD_kg@07:59]; done after any win or loss [SHJHpedYh6A@4:45:10; @4:49:02]; the third trade was the mistake [SHJHpedYh6A@4:49:02]<br>• Practice: 3 trades / −$100K [gKOQbcg0r1M]; −$41K then re-entry [c5f6hLzchyM] | 9 | **Max 2 entries/day** (the second must be a re-entry, A-18). **Stop for the day** after: (a) any trade closes in profit (TP1 hit counts as a win day), (b) a second loss, (c) the daily risk budget (1R default) is used up, or (d) DOLs on both sides are taken. Never a third trade. | C11 teaching over practice. | Some profitable re-entries are forgone. |
| A-18 | **Re-entry** | • E2: re-enter if the bias is not invalidated and budget remains [ss-dZPMnjeY@04:32]<br>• E4–E5: re-entries after a loss on the same idea, while the swept extreme holds [2ZArg3kPPkE; tWYSAHQpywE; WlnpOPPnBQw; iVOjRDrjFM4]<br>• An opposite-direction re-entry lost [MiaTd3hh47I]<br>• Done after a loss [SHJHpedYh6A@4:45:10] | 7 | One re-entry allowed only if all hold: (1) first trade lost; (2) **same direction**; (3) the original sweep extreme has not been closed beyond; (4) a **fresh** 1m trigger after a new 1m counter-move inside the time window; (5) the remaining budget is ≥ 0.5R; size = the remaining budget. Never re-enter in the opposite direction on the same day. | BC2 rule, E4–E5 practice and C11's cap. | Re-entries carry the bias error twice. |
| A-19 | **2B rule** | When the HTF sweep (step 1) happened before 09:30 (London or pre-market), also require a **5m sweep after the open** in the trade direction [xRuMUvW3T7Q@03:51–05:28; 8QDDxwUV1KM]. Skip 2B if the sweep is at or after the open [xRuMUvW3T7Q@06:00]. A 5m SMT may serve as the continuation only after 2B [xRuMUvW3T7Q@07:07]. In 2026 he trades reactively off a pre-market sweep [pKIo-aVic-c@19:08] and says a London/pre-market hourly sweep can be the day's sweep [LLWBdwtpbiI@00:33]. | 4 | **On** (C3): pre-open HTF sweep → require a post-09:30 sweep of a 5m swing high/low in the manipulation direction **before** the 5m confirmation counts. | Explicitly canonical; ignoring 2B was shown to lose [8QDDxwUV1KM@09:55]. | On days when price leaves straight from the open with no 5m manipulation, the bot misses the trade. |
| A-20 | **79% extension close** | Fib from swing high → swing low (for longs); a candle **close** beyond 0.79 [tWYSAHQpywE@06:01; xxJyvmHROb4@20:57]. Used when there is no gap to invert. Its TF varies: 1m [xxJyvmHROb4], 5m [8QDDxwUV1KM]. The −$152K trade used the 79% close alone, with no EQ retrace [xxJyvmHROb4]. Not mentioned in the P2P/Oct 2026 lists. | 6 | Allowed as **5m confirmation (C4)** only when the impulse leg has no with-trend FVG. Anchor = the extreme of the leg into the sweep → the sweep extreme, i.e. the swing high and low that bound the reversal leg (inferred). Valid with a **body close** beyond the 0.79 level. Never use it as a 1m trigger without the 5m continuation step. | Keeps it as an alternative, not a shortcut. | Wrong anchoring changes the signals. Log every signal and evaluate separately. |
| A-21 | **IFVG details** | Close through the gap (body) is required; a close at the edge ≠ inversion [MzJK2-NDOhk@02:14]. For stacked gaps, the close must be beyond the outermost gap [BdBxXKGWVjk@10:35; 4sRDnVmLcMk@15:27]. Won't take an IFVG alone for longs [g27VsJS3a58@18:21]. | 4 | IFVG = 5m/1m **body close ≥1 tick beyond the far edge** of the outermost with-trend FVG of the current stack. An FVG = 3-candle wick-to-wick gap ≥ 1 tick. | Matches C4 and his definitions. | Little risk. |
| A-22 | **EQ "filled"** | "Poking its head" beyond 50% counts [joe_XTCn5Bs@08:30]. E2 required a close back beyond EQ [4FEty6xgOc0@04:25]. EQ is confirmed with a LTF BOS or IFVG [wzq2AMsoJKY@08:51]. A close beyond EQ against the trade invalidates it [xRuMUvW3T7Q@22:35]. | 4 | Filled = any 5m wick reaching the 0.5 of the latest 5m impulse leg (Gann box, re-anchored on new extremes). Invalid = a 5m **close** beyond the 0.5 *and* beyond the protected swing. Entry needs the 1m trigger regardless. | Follows C5 and C6. | Little risk; the trigger gates it. |
| A-23 | **Chop / bad price action** | No numeric rule. Sideways 4H, no execution-TF BOS, about a 21-tick day range = no trade [OvmbAxG15YE@26:01; aobHuNcI1QM@5:44:29]. "Piano keys" chop → done [8PYgFVB0GHE@54:21]. No strong bias, price above the session highs → no trade [ssPMxVk6B9Y@02:15]. A week of bad price action [WlnpOPPnBQw@08:04]. | 6 | **Chop filter (inferred):** no trade if any of:<br>(a) ES/NQ 5m misaligned (A-14);<br>(b) ≥ 3 alternating 5m BOS flips between 09:30 and the candidate trigger;<br>(c) range from the overnight high to the low < 40% of its 20-day median;<br>(d) no significant DOL swept by 10:20. | Encodes his qualitative examples. | The thresholds are inferred; risk of over-filtering. |
| A-24 | **PM session** | • E1: PM trades [0R3TEHZgwxA]<br>• E3: PM model 13:30–15:00 / 13:50–14:10 [i3FU-9OUU90; r-7-gWZsnZc@11:06]<br>• Sep 2024: "I just don't trade PM session" [p5CKu0FNbyg@05:34]<br>• E5: no PM [L4xz2o23aPQ@03:55]; except FOMC afternoons [7a8tAGkVJac; egQLtQLmauk]; a 10:45 "PM-style" late trade [QRoLG0QRiNM] | 7 | **No PM trading.** `PM_FOMC` defaults to off. | C7. | Missing FOMC-day moves, which were his largest trades. Kept off for tail-risk reasons. |
| A-25 | **Pre-market trades** | His first pre-market trade lost twice [gKOQbcg0r1M]. Pre-market manipulation is allowed, entries only after the open [8PYgFVB0GHE@44:17]. E2 had an evening ES trade [Iu_v4kuFQhk]. | 3 | **No entries before 09:30** (C7). | Explicit. | Little risk. |
| A-26 | **Counter-HTF trades** | • E2: never against the daily [4FEty6xgOc0@09:54]<br>• E3: counter-4H toward 4H EQ allowed [Qk-mHUlSJGU@03:55]<br>• E5: sweep + SMT + 5m BOS overrides the bullish pre-open bias [TEp3a-7GUds@39:03]; shorted against the 4H with room to the 4H gap [-mJ8mww-Flw]; "should have went long" [0RBTSUGKA0w@1:36:18] | 6 | Allowed only if the full chain (C3–C6) completes **and** TP1 is a DOL that sits *before* the nearest opposing HTF (1H/4H) FVG/EQ. Use 50% size when the trade is against the 4H order flow (inferred). | Respects his 2026 "the market proved me wrong" while limiting tail risk. | Too permissive: more losing reversals. Too strict: misses his best 2026 trade. |
| A-27 | **HTF candle-close gating** | He waited for the 10:00 4H close to confirm a 4H inversion [kaPlPoXGXKw@13:30]. The hourly close decides the bias flip [MiaTd3hh47I@08:59]. The bias is fixed from candles closed before 09:30 [OvmbAxG15YE@03:36]. | 3 | Pre-open bias uses only candles closed before 09:30. A 1H/4H close at 10:00 that **inverts** the HTF FVG against the open position's direction → tighten to BE if not yet at TP1 (inferred). It never creates a new entry by itself. | Safe middle ground. | Rarely triggers. |
| A-28 | **Session clocks** | London ends at 08:00 [CPPREA-6ubY] vs 08:30 [AGmAVyAuBE0; Vulini8xbB0]. Pre-market starts at 08:00 [e_FV0Q14k8E] vs 08:30 [8QDDxwUV1KM]. NY session ends at 17:00 vs 18:00 [yiuFUp0kFz8@2:05:03; @4:30:11]. | 5 | Asia 18:00–03:00; London 03:00–08:30; pre-market 08:30–09:30; RTH open 09:30 ET (C1). | E5 statements. | Little risk. |
| A-29 | **Risk per trade** | • E2: 1–3% per trade or per day [RkMBoqbeUq8]<br>• E4: 1% baseline [a5PLl1uM7CQ]<br>• E5: fixed contracts, 1–3%, accepts 3–4% [hBnD6T1M4w8@12:52]<br>• Live practice: $16K–$40K+ per trade; $152K and $135K losses [xxJyvmHROb4; 88tyzO9CxGA@17:20] | 6 | **1.0% of equity per trade** (risk-based sizing in MES; ES only when ≥ 1 ES contract fits). The daily cap is 1R in total across ≤2 entries. Use 50% size for news days, wide stops (A-05), counter-4H trades (A-26) and ES_WHEN_NQ_LEADS (A-13). | C11 teaching. | Sizing by % rather than fixed contracts deviates from E5 literal practice, but gives a bounded drawdown. |
| A-30 | **Entry on 1m SMT alone, or on the 5m close without a 1m trigger** | 1m SMT as the trigger [rBdlDQgSjIc@24:28; BMyeYQIj_vU@14:25]. A 5m close in the FVG without a 1m trigger lost [0RBTSUGKA0w@1:25:14]. Entering at market on the 5m BOS without a retrace lost [gKOQbcg0r1M@01:41]. SMT never an entry [X8Ag7BWd9dg@10:59]. | 5 | **Trigger = 1m BOS or 1m IFVG close only (C6).** A 1m SMT is logged as context, never a trigger. | C6; his own losses. | Some earlier entries are lost. |
| A-31 | **Order execution / fills** | "Horrible fill" destroyed the RR [MiaTd3hh47I@20:46]. "Lost way more than I was supposed to" [gKOQbcg0r1M@21:58]. A platform failure meant no stop [iVOjRDrjFM4@30:45]. No stop on CPI day [_zzxRMbyE44]. | 4 | Enter with a **marketable limit** at the trigger close ± 2 ticks. If not filled within 1 bar, cancel. Place a **server-side stop at the same time** as entry. If the stop can't be confirmed, flatten immediately. | Engineering safeguard. | Some fills are missed. |
| A-32 | **Holidays / half-days / Fridays / days around news** | No trading on bank holidays [T-Bo-9GDi3s@48:48; Z-9HuHf5egU; xxJyvmHROb4]. The day after is slow [YGSXw_B-UgM@05:46]. Avoid the day before NFP [MiaTd3hh47I@58:46]. Fridays are not avoided [0RBTSUGKA0w]. | 5 | No trading on US bank holidays or CME early-close days (inferred: half-days). Normal rules apply on Fridays and on the day before NFP; `PRE_NFP_SKIP` defaults to off. | Explicit except half-days. | Little risk. |
| A-33 | **Bias invalidation: wick vs close** | "We have to close above this high" [9ar85Y6-5P4@04:24]. A wick is not a BOS [C5zIaZzbbgM@53:00]. | 3 | Invalidation (of both bias and setup) needs a **body close** beyond the protected level; wicks are ignored. The stop is still a hard price stop. | Consistent across eras. | Little risk. |


### 18.x Cross-check list from the section writers

The items below were raised while drafting §5–§17. Most are resolved in the register above; any not listed there should be treated as OPEN, with the default stated here.

```
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
```

## 19. Worked examples

**What these are.** Annotated TJR trades and no-trade days, taken from the notes. Each one is a regression test: a correct bot that replays the day should reach the same decision, or should *differ for the stated reason*. That reason matters most when TJR broke his own rules.

**Conventions.**
- **Times** are ET. "(inferred)" marks a value the note derived from stream timestamps or context rather than one he stated.
- **"not stated"** means the source does not give the value. **No prices are invented.** Where a note gives no level prices, the levels are named only.
- **Outcome** is in R when he stated an R:R, otherwise in his stated $ figure. Dollar figures are his live-account P&L, often at very large size. Use them only as a sign: win, loss or breakeven.
- **"Expected bot action"** says what the bot should do under CANONICAL.md and §18 defaults. Where that differs from what TJR did, the deviation *is* the test.
- **Rule codes** C1–C13 refer to CANONICAL.md; A-xx refers to the register in §18.

### 19.0 Index

| ID | Date | Era | Inst. | Dir | Type | Outcome | Main rules tested |
|---|---|---|---|---|---|---|---|
| EX-01 | 2026-01-16 | E5 | ES | Short | Live | Win (TP1–TP3) | C2 override, C4 BOS-no-gap, C5 EQ, C6, C10 |
| EX-02 | 2026-05-29 (inferred) | E5 | ES | Short | Live | Win | Four-step template, C6 |
| EX-03 | 2026-05-28 | E5 | NQ | Long | Live | Win | A-12/A-13 exception |
| EX-04 | 2026-05-27 | E5 | NQ | Short | Live | Win (TP1, rest BE) | A-25, C5 continuation-only |
| EX-05 | 2026-06-01 | E5 | ES/NQ | — | No trade | No trade | A-14, A-16, A-23 |
| EX-06 | ~2026-10-06/07 (inferred) | E5 | ES | Short | Live | Win (2 TPs, rest BE) | C2 DOL-count bias |
| EX-07 | ~2026-10-06/07 (inferred) | E5 | NQ | Long | Hypothetical | Would win | C2, C5, C6 IFVG |
| EX-08 | ~2026-04-06 (inferred) | E5 | NQ | Long | Live | +$60,630 | A-12, A-15 |
| EX-09 | ~2026-04-07 (inferred) | E5 | ES | Short | Live | Win (~$103K day) | A-15 early entry |
| EX-10 | ~2026-04-16 (inferred) | E5 | NQ | Short | Live | +$48,332 | A-08, A-15 |
| EX-11 | 2026-04-17 | E5 | NQ | Short | Live | −$44,000 (cut early) | A-26, A-09 |
| EX-12 | 2026-04-17 | E5 | NQ | Long | Live | Win; day +$75,210 | A-12, A-09, A-16 |
| EX-13 | 2026-05-12 (CPI) | E5 | ES | Short | Live | +$19,620 day | A-10, A-31 |
| EX-14 | 2026-05-11 | E5 | ES/NQ | — | No trade | No trade | C3 "too fast" |
| EX-15 | ~2026-04-27 (inferred) | E5 | ES | Long | Live | −$20,160 | A-04, C3 |
| EX-16 | 2026-04-21 | E5 | ES (inferred) | Short | Live | Win (+$88,300 title) | A-16, A-10 |
| EX-17 | ~2026-03-27 (inferred) | E5 | NQ | Short | Missed / no trade | No trade | C13, A-15 |
| EX-18 | 2026-01-08 (inferred) | E5 | ES | Short | Live | −$44,850 | A-14, A-31 |
| EX-19 | 2026-01-08 (inferred) | E5 | ES | Long | Live | Loss; day −$93,000 | A-18, A-17 |
| EX-20 | 2026-01-22 | E5 | ES | Long | Live | −$41,290 | A-04, A-11 |
| EX-21 | 2026-01-22 | E5 | NQ | Long | Live | Partial win | A-18, A-12 |
| EX-22 | 2026-01-27 | E5 | NQ | Long | Live | Two losses (−$36,920; second not stated), then an off-stream win | A-25, C5, A-17 |
| EX-23 | 2026-01-21 | E5 | ES/NQ | Long | Live | +$88,322 | A-27, A-09 |
| EX-24 | 2026-01-14 (PPI) | E5 | NQ | Short | Live | +$67,680 | A-10, A-15 |
| EX-25 | ~2026-01-07 (inferred) | E5 | ES | Long | Live | +$42,510 | A-15 |
| EX-26 | 2026, a Friday (inferred) | E5 | NQ | Short | Live | −$52,660 | A-16, A-30, A-26 |
| EX-27 | same day as EX-26 | E5 | ES/NQ | Long | No trade (missed) | No trade | C6 1m counter-BOS |
| EX-28 | ~2026-03-09/10 (inferred) | E5 | NQ | Long | Live (student + TJR) | Win | C5 retrace patience |
| EX-29 | 2026-01-06 (inferred) | E5 | NQ (inferred) | Short | Live (late) | TP1, rest BE | A-16, A-30 |
| EX-30 | ~2026-01-09 (inferred) | E5 | ES | Long | Teaching replay | TP hit | C3–C6 with FVG under EQ |
| EX-31 | 2025-10-07 (inferred) | E4 | ES | Short | Live | +$45,180 (~1:2) | C10 leading index |
| EX-32 | 2025-10-08 (inferred) | E4 | NQ | Long | Live | +$35,827 | C10, cross-index trigger |
| EX-33 | 2025-10-09 (inferred) | E4 | NQ | Short | Live | +$8,280 | A-12 (execution-TF leader) |
| EX-34 | 2025-10-09 (inferred) | E4 | NQ | Long ×2 | Live | Two losses; day −$52,660 | A-17, A-18 |
| EX-35 | 2025-10-15 (inferred) | E4 | NQ | Short | Live | −$152,060 | A-20, A-29, C5 |
| EX-36 | 2025-10-07 | E4 | ES | Short | Backtest | 1:7.36 | A-19 (2B at the open) |
| EX-37 | 2025-10-17 | E4 | ES/NQ | Short→Long | Backtest + live | ES no-trade, ES loss, NQ +1.39R | A-19, A-22 |
| EX-38 | 2025-10-02 (inferred) | E4 | ES | Short | Backtest | 1:3.63 max, ~1:2 realized | A-19 2B |
| EX-39 | 2025-10-01 (inferred) | E4 | ES | Long | Backtest | ~1:3 realized | C5 re-anchoring |
| EX-40 | 2025-09-10 (PPI, inferred) | E4 | ES | Long ×2 | Live | −$41,620, then BE; day −$1,953 | A-15, A-18 |
| EX-41 | 2025-08-25 (inferred) | E4 | ES | Long ×2 | Live | −$20,000, then partial; day −$4,100 | A-15, A-20 |
| EX-42 | 2025-09-09 (inferred) | E4 | NQ (inferred) | Short | Live | Win (all TPs) | C5 EQ, C6 |
| EX-43 | ~2025-05-09/12 (inferred) | E4 | ES | Long | Live | Win (TPs at 1:2.29 / 1:3.48 / 1:5.68) | C10, C7 |
| EX-44 | 2025-05-21 | E4 | ES | Short ×2 | Live | −$24,000, then re-entry; day −$3,650 realized | A-31, A-18 |
| EX-45 | ~2025-03-17 (inferred) | E4 | ES | Short ×2 | Live | −$19K, then re-entry; day ≈+$4K | A-08 (no trailing) |
| EX-46 | 2025-03-04 (inferred) | E4 | NQ | Short | Live | +$25,000 (TP1 1:1.7) | E4 lagging-index rule |
| EX-47 | 2025-05-22 | E4 | ES/NQ | — | No trade | No trade | A-23 |
| EX-48 | 2025-12-09 | E4 | NQ | Short | Live | Loss (title −$14,646, inferred) | Execution TF = 5m |
| EX-49 | 2024-06-06 | E3 | ES | Short | Live | +$6,000 | E3 "made-the-extreme" index |
| EX-50 | 2023-07-03 | E2 | ES | Long | Live | Loss (wick-out) | A-04 buffer |
| EX-51 | 2023-07-14 | E2 | ES | Long | Live | ≈ −$9.5K | A-01 (unmarked LTF sweep) |
| EX-52 | 2023-09-05 | E2 | ES | Long ×2 | Live | Loss (fixed 5 pt), then a re-entry win | A-04, A-18 |
| EX-53 | 2023-08-30 | E2 | ES | Long | Live | TP1 + TP2, rest BE | A-10 half size |
| EX-54 | ~2023-08-24 (inferred) | E2 | ES | Short | Live | ≈ −$13K | C5 third confirmation |
| EX-55 | ~2023-07-19 | E2 | ES | — | No trade | No trade | A-16 |
| EX-56 | 2023-09-12 | E2 | ES | Long | Live | Loss (stop missed by 2.7 pt) | A-04, A-05 |

**Counts by era:** E5 30 · E4 18 · E3 1 · E2 7 · total 56.

**Counts by outcome.** Each block is classified by its first, rule-relevant trade:
- **Win: 30.** Five of these are hypothetical, backtest or teaching cases: EX-07, EX-30, EX-36, EX-38 and EX-39.
- **Loss: 20.** This includes EX-37, classified by its ES backtest loss. The multi-trade blocks EX-22, EX-40, EX-41, EX-44, EX-45 and EX-52 start with a loss and contain a later re-entry.
- **No trade or missed: 6** (EX-05, EX-14, EX-17, EX-27, EX-47, EX-55). EX-37 also contains a no-trade sub-case.

---

### E5 (2026, canonical)

**EX-01 | E5 | ES | SHORT | WIN**
- **date:** Fri 16 Jan 2026 (stated [TEp3a-7GUds@16:25]). The same trade is re-presented as "literally yesterday on Friday" in yiuFUp0kFz8 (inferred). hBnD6T1M4w8 gives the same day's ES winner with a ~16-tick stop at 1:4.81 (inferred to be this trade).
- **pre-open DOLs & bias:**
  - Marked: PDH, PDL, Asia low, London high and low, hourly highs. The Asia high was already run with no reaction, so it was ignored.
  - Bias **bullish**: 4H bullish; ES inverted its top 4H gap and broke structure up; both indices respected the 4H gap/EQ. Draws above were the London high, hourly highs and PDH.
  - On the 1H, price had swept lows before the open.
- **sweep:** at 09:30 NQ pushed above the London session high while ES stayed below its own. That is a bearish SMT. He stayed bullish but waited.
- **5m confirmation:** a big 5m down candle broke 5m structure on **both** ES and NQ. The up-leg had no FVG to invert, so the BOS was the confirmation.
- **continuation zone:** 5m EQ (Gann box from the recent high to the recent low). Price retraced into premium; no 5m FVG formed.
- **1m trigger & entry time:** the 1m retrace built bullish structure into EQ, then a **1m IFVG down** (a bullish 1m FVG inverted). He entered on that close, before the next 5m close. Time: not stated, shortly after the open (inferred).
- **stop:** above the highs (the retrace/sweep high; exact level not stated). About 16 ticks if hBnD6T1M4w8 is the same trade (inferred).
- **targets & management:** London session low → Asia session low → hourly lows. TP1, TP2 and TP3 all hit. Partial sizes not stated.
- **outcome:** win, "significant amount of money". Possibly 1:4.81 (inferred).
- **TJR's lesson:** "bias was bullish but the market proved me wrong; follow the sequence". The 1m entry hit TP1 at about the time a 5m-close trader would have been entering.
- **tests:** C2 (a sweep + SMT + 5m confirmation overrides the pre-open bias); C4 (BOS when there is no gap); C5 (EQ only); C6 (1m IFVG); C10 (ES = the index that failed to make the new high).
- **expected bot action:** short ES after 09:50 (A-15). If the IFVG printed before 09:50, wait for the next 1m trigger inside EQ.
- **citation:** [TEp3a-7GUds@16:25–40:08]; [yiuFUp0kFz8@6:05:23–6:29:35]; [hBnD6T1M4w8@11:45].

**EX-02 | E5 | ES | SHORT | WIN**
- **date:** Fri 29 May 2026 (inferred from "Friday's price action").
- **pre-open DOLs & bias:** London session highs on ES and NQ. Bias: not stated.
- **sweep:** at the 09:30 open price ripped above the **London session highs** on both indices.
- **5m confirmation:** a 5m bullish FVG was inverted to the downside (bearish IFVG) on both ES and NQ.
- **continuation zone:** the 5m retrace was identified by a 1m BOS up; no FVG/EQ tag was needed [8PYgFVB0GHE@26:15].
- **1m trigger & entry time:** a 1m BOS back down → short ES ("I took this on the S&P 500"). Time: not stated.
- **stop:** above the second high, i.e. the retrace high (inferred).
- **targets & management:** session lows and hourly lows. The NQ version had partials and about 1:3.4 R:R.
- **outcome:** win. ES R:R was "pretty bad" because of the big BOS candle; exact R not stated.
- **TJR's lesson:** a textbook four-step trade.
- **tests:** C3–C6 template; A-04 RETRACE_SWING stop; A-07 (check TP1 ≥ 1R; a big BOS candle can fail it).
- **citation:** [8PYgFVB0GHE@24:04–35:13].

**EX-03 | E5 | NQ | LONG | WIN**
- **date:** Thu 28 May 2026.
- **pre-open DOLs & bias:** lows below the open on both indices. Bias: not stated.
- **sweep:** at the open price swept the lows on **NQ only**; ES did not take its lows. "As long as one of the indexes is doing it for us, that's all we need."
- **5m confirmation:** a 5m IFVG up (top gap inverted).
- **continuation zone:** a 5m FVG fill plus a 1m BOS down (the retrace).
- **1m trigger & entry time:** a tiny bullish 1m gap inverted and a 1m BOS up on the same candle → long NQ. Time: not stated.
- **stop:** under the second low.
- **targets & management:** intermediate highs (~1:1), more highs, then a big gap. He took profit at three levels. The far highs were taken the next day.
- **outcome:** win; amount "doesn't remember". ES later broke 5m structure up and filled its gap.
- **TJR's lesson:** none beyond the template.
- **tests:** **A-12 / A-13 exception.** He traded the index that *made* the sweep, which goes against C10.
- **expected bot action:** with the defaults (`ES_WHEN_NQ_LEADS=HALF`), the bot trades ES only if ES itself completes the chain. ES did not sweep, so ES is the leader here; check whether ES produced its own 5m confirmation in time.
- **citation:** [8PYgFVB0GHE@37:25–43:04].

**EX-04 | E5 | NQ | SHORT | WIN (TP1, rest BE)**
- **date:** Wed 27 May 2026.
- **pre-open DOLs & bias:** the manipulation of the highs and the reversal both happened **in pre-market**.
- **sweep:** pre-market (highs). No entry in pre-market. After the open he looked only for continuation.
- **5m confirmation:** formed in pre-market (inferred from "reversal in pre-market").
- **continuation zone:** after the open, a 1m BOS up (the retrace).
- **1m trigger & entry time:** a 1m BOS down → short NQ, after the open. Exact time: not stated.
- **stop:** above the high.
- **targets & management:** first TP at a significant (hourly/4H) low; extended TPs at the daily low and lower lows. TP1 hit, stop to BE, rest stopped at BE.
- **outcome:** win day; R not stated.
- **TJR's lesson:** pre-market manipulation means no pre-market entry; trade continuation after the open.
- **tests:** A-25 (no pre-market entries); A-19 (2B: the bot needs a post-open 5m sweep before step 2 counts); A-08 BE at TP1.
- **expected bot action:** with 2B on, the bot enters only if a 5m swing high was swept after 09:30. The source does not say whether one was (not stated). A no-trade is an acceptable result here.
- **citation:** [8PYgFVB0GHE@44:17–46:32].

**EX-05 | E5 | ES/NQ | — | NO TRADE**
- **date:** Mon 1 Jun 2026.
- **pre-open DOLs & bias:** not stated.
- **sweep:** at the open, manipulation to the downside.
- **5m confirmation:** NQ broke 5m structure **up**, but ES did **not** (still bearish on the 5m) → misaligned → no trade.
  - 09:50: NQ broke 5m down and aligned with ES, but dumped straight down with no 5m retrace and no 1m counter-BOS.
  - 10:07: a 1m BOS up, but no 1m BOS back down followed.
  - NQ then broke 5m back up.
- **1m trigger & entry time:** none qualifying.
- **management:** 10:20 still misaligned → "call it a day". An 11:05 setup (IFVG + 1m BOS up, about 1:1) worked, but he would not sit through the chop ("piano keys").
- **outcome:** no trade.
- **TJR's lesson:** don't trade when ES and NQ disagree on the 5m. The step sequence prevents the loss that a bare sweep + 5m BOS would have taken.
- **tests:** A-14 (misalignment), C6 (needs a retrace), A-16 (done by 10:30; ignore 11:05), A-23 chop.
- **citation:** [8PYgFVB0GHE@48:11–57:16].

**EX-06 | E5 | ES | SHORT | WIN (2 TPs, rest BE)**
- **date:** ~6–7 Oct 2026 (inferred; the day of recording).
- **pre-open DOLs & bias:** pre-market swept a **high** (upside DOL taken) and price reacted down. Four downside DOLs were close to price within the first 5 minutes of the open: several 5m lows and the London session lows. Bias: bearish for the window.
- **sweep:** pre-market high.
- **5m confirmation:** BOS to the downside after the sweep.
- **continuation zone:** retrace into a bearish FVG.
- **1m trigger & entry time:** continuation down from the FVG. Trigger details and time: not stated.
- **stop:** not stated (inferred above the FVG or the swept high).
- **targets & management:** 5m lows, then London session lows. Two TPs hit, rest stopped at BE.
- **outcome:** win. Price later traded higher because "these draws ... was literally all price needed".
- **TJR's lesson:** a sweep plus nearby opposing DOLs sets the bias for the window.
- **tests:** C2 (bias from which side has more and closer unswept DOLs), A-19 (pre-market sweep → 2B required), C9 stand-down after the DOLs are taken.
- **citation:** [FBX-gtFGWyU@02:12–04:57; @08:17].

**EX-07 | E5 | NQ | LONG | HYPOTHETICAL (would win)**
- **date:** same recording as EX-06 (~Oct 2026, inferred). He says he also took a NQ long to these highs that day, but gives no details.
- **pre-open DOLs & bias:** no DOL swept in pre-market. The 4H/1H had little nearby. The LTF had stacked highs just above the open and only one low below, plus two 4H highs further up → bullish (more and closer DOLs above).
- **sweep:** none. NQ dumped at the open without taking a downside DOL, so the bias stayed valid.
- **5m confirmation:** four up-candles formed structure.
- **continuation zone:** retrace into EQ of the up-leg, with a bullish reaction.
- **1m trigger & entry time:** inversion (close above) of a bearish FVG that had been respected twice. Time: not stated.
- **stop:** under the retrace lows.
- **targets & management:** market-open high (~1:1.5), next high (~1:1.7), then the 4H highs.
- **outcome:** three upside DOLs taken, with some drawdown first.
- **TJR's lesson:** the side with more and closer DOLs wins. Wait for the retrace + IFVG.
- **tests:** C2 DOL-count bias; C3 (**no sweep → does the canonical chain allow it?** CANONICAL C3 requires a sweep, so the bot should **not** take this. It is a negative test of C3 strictness).
- **citation:** [FBX-gtFGWyU@05:33–13:18].

**EX-08 | E5 | NQ | LONG | WIN +$60,630**
- **date:** ~6 Apr 2026 (inferred from upload).
- **pre-open DOLs & bias:** 1H bullish. A potential bearish 4H SMT (NQ took the 4H highs, ES did not) was noted but overridden by current structure. Draws: London highs, hourly highs, ES London highs.
- **sweep:** 5m lows swept after the open's 5m BOS up (manipulation).
- **5m confirmation:** the 5m stayed bullish. He skipped a 09:41 BOS as too early and because ES's swing was a doji.
- **continuation zone:** retrace that swept the 5m lows.
- **1m trigger & entry time:** a bearish 1m FVG inverted on NQ, **then on ES** (ES was the more bearish index). He entered after the ES inversion, on the **09:45/09:46** candle.
- **stop:** not stated (below the sweep low, inferred).
- **targets & management:** London highs (half off, +$20K, stop to BE) → hourly highs → ES London highs (closed everything).
- **outcome:** +$60,630.
- **TJR's lesson:** waiting for ES saved him from an earlier fake. He chose NQ as "closer to these London highs".
- **tests:** A-12 (confirmation from the most opposed index; index chosen by proximity to target); A-15 (09:46 entry → the bot waits until 09:50 for a trigger); A-08.
- **citation:** [kH-rbepWkNE@05:31; @06:35–08:16; @15:23; @23:59; @27:45–31:39].

**EX-09 | E5 | ES | SHORT | WIN (+$44K at partial; ~$103K day per title)**
- **date:** ~7 Apr 2026 (inferred from upload).
- **pre-open DOLs & bias:** 4H BOS down on ES and NQ; price filling a bearish 1H FVG; draw = London lows.
- **sweep:** 4H highs swept, with a bearish SMT.
- **5m confirmation:** ES 5m BOS down + gap inversion (IFVG). NQ had not yet confirmed ("still bullish").
- **continuation zone:** not stated; the entry was on the IFVG.
- **1m trigger & entry time:** ~**09:36–09:38** (inferred). He called it "very early ... not typical".
- **stop:** above the highs, later moved near the retrace EQ (exact level not stated).
- **targets & management:** half off at London lows, stop to BE; remainder closed at a lower low.
- **outcome:** win.
- **TJR's lesson:** the early entry worked, but he flagged the risk. He wished he had held lower.
- **tests:** A-15 (bot: **no trade before 09:50**; if no later trigger appears, the expected bot result is no trade); A-12 (NQ not yet confirming → the bot's both-index alignment fails at entry time).
- **citation:** [OJXkE2h2mz4@02:08–34:33].

**EX-10 | E5 | NQ | SHORT | WIN +$48,332**
- **date:** ~16 Apr 2026 (inferred from upload).
- **pre-open DOLs & bias:** 4H bullish; 1H bearish after a sweep of the hourly highs; bearish SMT in the London session. Draws: Asia lows, hourly lows, 4H FVG.
- **sweep:** hourly highs / ES highs.
- **5m confirmation:** not explicit; a 1m gap fill plus a bearish candle close on NQ and ES.
- **continuation zone:** 1m gap.
- **1m trigger & entry time:** ≈**09:36** (inferred). "Early ass trades. I know." He re-entered "the exact same" after a 1m sweep.
- **stop:** above the high (not quantified). Funded accounts had essentially no stop and were auto-stopped.
- **targets & management:** Asia lows + hourly lows (partials +$23,440, stop to BE) → middle of the 4H FVG → bottom of the FVG (final).
- **outcome:** +$48,332.50 for the day.
- **TJR's lesson:** "You entered too soon. Yeah, potentially." BE should have been at the London lows.
- **tests:** A-15, A-08, A-26 (counter-4H short with room into the 4H gap), C11 (no-stop funded accounts are not to be copied).
- **citation:** [-mJ8mww-Flw@15:16; @18:45; @19:59; @20:33–21:42; @25:31; @32:25–35:24; @47:07].

**EX-11 | E5 | NQ | SHORT | LOSS −$44,000 (cut early)**
- **date:** Fri 17 Apr 2026.
- **pre-open DOLs & bias:** ES at a fresh ATH (bullish); London expansion up. He preferred longs. Few draws below; price already at EQ.
- **sweep:** not stated.
- **5m confirmation:** ES (the more bullish index) broke 5m structure down after NQ had already broken down.
- **continuation zone:** none; he entered on the confirmation.
- **1m trigger & entry time:** NQ short ~**09:48** (inferred from "it is 9:43").
- **stop:** above the highs (buy stop).
- **targets & management:** lows below. Closed early when a bullish SMT formed and a gap inverted up.
- **outcome:** −$44,000.
- **TJR's lesson:** cutting early prevented a bigger loss. He dislikes shorting right after ATHs.
- **tests:** C5 (no retrace → the bot does not enter); A-26 (counter-HTF); A-15 (pre-09:50); A-09 (the opposing-signal exit gave a smaller loss).
- **citation:** [3SygD-YgZuQ@10:22; @14:24–17:44].

**EX-12 | E5 | NQ | LONG | WIN (day +$75,210)**
- **date:** Fri 17 Apr 2026 (same day as EX-11).
- **pre-open DOLs & bias:** as in EX-11. NQ ATH as the final draw.
- **sweep:** the lows. ES made a lower low while NQ made a higher low → bullish SMT.
- **5m confirmation:** gap inversion up, then a 5m BOS up later (~09:59).
- **continuation zone:** not stated.
- **1m trigger & entry time:** ~**09:50** entry.
- **stop:** below the lows. Moved to BE at ~10:24.
- **targets & management:** NQ 5m highs (partials ~10:40) → final at the NQ ATH (sell limit). He held through a 1m BOS down, a 5m gap fill and a sweep of 1m lows. Closed everything ~11:11.
- **outcome:** day net +$75,210.
- **TJR's lesson:** hold valid 5m-extension retraces; exit when the trade drags and an opposing gap inverts.
- **tests:**
  - A-12: execute on NQ, the index that failed to make the new low; confirmation from ES, the more bearish index.
  - A-18: an opposite-direction trade after a loss, which the **bot forbids**. The expected bot action is no trade, because this is the second idea and in the opposite direction.
  - A-09 runner logic.
- **citation:** [3SygD-YgZuQ@05:14; @17:44; @51:56; @1:06:55; @1:08:06; @1:38:48].

**EX-13 | E5 | ES | SHORT | WIN (+$19,620 day) — CPI day**
- **date:** Tue 12 May 2026 (CPI).
- **pre-open DOLs & bias:** ES 4H bearish, 1H bullish; NQ 1H bearish. Draws: relative equal lows, pre-market lows, London lows, hourly lows.
- **sweep:** pre-market took the highs. NQ took the London highs and ES did not → SMT. ES is the index that failed.
- **5m confirmation:** 5m bearish structure.
- **continuation zone:** price filled the 5m bearish gap.
- **1m trigger & entry time:** bullish 1m confluences were disrespected, and a spike into a tiny bearish gap filled. Entry ~**09:45–09:55** (inferred).
- **stop:** **none initially.** It was placed mid-trade ("6,000 and I have five on ... 7,000"; ambiguous).
- **targets & management:** London lows taken → stop to BE + partial; full TP on the eval account; partial at the hourly lows; rest stopped at BE.
- **outcome:** +$19,620 for the day.
- **TJR's lesson:** "I got a little bit overconfident" by not placing a stop.
- **tests:** A-10 (NEWS_MODE: STRICT → no trade; CURRENT → trade at 50% after 09:50); A-31 (stop must be placed with the entry); C10.
- **citation:** [_zzxRMbyE44@27:39–52:05].

**EX-14 | E5 | ES/NQ | — | NO TRADE**
- **date:** Mon 11 May 2026.
- **what happened:** "it moved too fast for me". No details on DOLs, sweep or confirmation (not stated).
- **outcome:** no trade. It was his only trade-free day of that week up to then.
- **tests:** C5/C6 (no retrace → no entry); the bot must accept no-trade days.
- **citation:** [_zzxRMbyE44@52:05].

**EX-15 | E5 | ES | LONG | LOSS −$20,160**
- **date:** ~27 Apr 2026 (inferred; a Monday).
- **pre-open DOLs & bias:** bullish toward the ES and NQ equal highs (London-session high).
- **sweep:** **no explicit sweep before entry.** The ES gap had already been inversed; "both the indexes are bearish".
- **5m confirmation:** none valid. He described a 5m FVG retrace as not ideal ("would want a better fair value gap fill").
- **continuation zone:** a bullish gap he called "no man's land".
- **1m trigger & entry time:** market long ~**10:05** (inferred): "I just need to hammer this regardless".
- **stop:** "a healthy amount down" below the bullish gap; "there was just no good spot to put my stop".
- **targets & management:** TP1 at the ES equal highs (poor RR), extended targets higher. Stopped out before TP1. NQ had inversed its bullish gap and swept triple equal lows.
- **outcome:** −$20,160 at "half of what I typically risk". The equal highs were taken later.
- **TJR's lesson:** no good stop location; the idea was still valid.
- **tests:** C3 (no sweep → no trade); A-04 (no structural stop → no trade); A-14 (both indices bearish vs. long bias); A-07 (poor RR to TP1).
- **expected bot action:** no trade.
- **citation:** [C5zIaZzbbgM@23:30; @32:18; @36:55–49:51; @1:09:27].

**EX-16 | E5 | ES (inferred) | SHORT | WIN (title +$88,300)**
- **date:** Tue 21 Apr 2026 (Fed-chair confirmation hearing at 10:00).
- **pre-open DOLs & bias:**
  - Pre-open he leaned long after NQ swept all the lows at the open.
  - HTF: an unconfirmed 1H bearish SMT at the highs; a 1H IFVG on ES.
  - News plan: trade only if a trade could be done before the Q&A.
- **sweep:** NQ swept the London/Asia/hourly lows at the open. Later the 5m lows / "potential bullish SMTs" were swept.
- **5m confirmation:** ES 5m BOS down; ES respecting the 5m bearish FVG.
- **continuation zone:** ES 5m bearish FVG.
- **1m trigger & entry time:** NQ 1m BOS down ("that break was like OD weak"). Short at market ~**10:40** (inferred).
- **stop:** above the high that could be manipulated.
- **targets & management:** TP1 → stop to BE (realized $21,360 + $24K floating) → TP2 → TP3 → about $70K banked, $13K running to max TP.
- **outcome:** win (title +$88,300).
- **TJR's lesson:** none stated. He broke his own news plan by trading during the Q&A.
- **tests:** A-16 (**after 10:30 → the bot does not enter**); A-10 (Fed-chair day: STRICT → no trade).
- **expected bot action:** no trade.
- **citation:** [L5eRg5BZOOY@09:48–11:31; @1:01:51; @1:05:10; @1:21:09–1:21:43; @1:32:13–1:41:21].

**EX-17 | E5 | NQ | SHORT | MISSED → NO TRADE**
- **date:** ~27 Mar 2026 (inferred from upload).
- **pre-open DOLs & bias:** stacked lows below; ES/NQ cross-check.
- **sweep:** a sweep of highs, with a bearish SMT vs. ES. NQ failed to take the London highs.
- **5m confirmation:** not stated.
- **1m trigger & entry time:** a short "off this candle" ~09:58–10:00 (inferred). He was distracted helping a student and missed it.
- **targets & management:** would have reached partials.
- **outcome:** no trade.
- **TJR's lesson:** 09:37 is "a little bit early"; 09:56 is "pretty good" timing. Stand down when "most of the objectives are taken".
- **tests:** A-15; C9 stand-down; A-01 (a London/pre-market hourly sweep can be the day's sweep [LLWBdwtpbiI@00:33]).
- **expected bot action:** take the short if the 1m trigger printed at or after 09:50 and both indices were aligned.
- **citation:** [LLWBdwtpbiI@00:33–01:08; @27:20–28:33; @30:47; @31:21].

**EX-18 | E5 | ES | SHORT | LOSS −$44,850**
- **date:** 8 Jan 2026 (inferred). The day before he lost $99K; NFP was the next day.
- **pre-open DOLs & bias:** 4H bearish; bearish SMT at the highs with NQ leading lower. **But ES showed a bullish SMT and held 1m bullish structure.**
- **sweep:** the highs (with SMT).
- **5m confirmation:** not explicit.
- **continuation zone:** a "fluid" range.
- **1m trigger & entry time:** ES inverted a 1m gap through the range. Entry ≈**10:00** (inferred). It was a "very low risk" setup but got a "horrible fill" lower than planned.
- **stop:** above the range (inferred; not quantified).
- **targets & management:** TP1 was planned at the end of the range but was lost to the fill, so it was reset to further lows.
- **outcome:** stopped ≈10:05; −$44,850 (−$46.9K with costs).
- **TJR's lesson:** he "didn't even want to be risking that much"; the fill destroyed the RR.
- **tests:** A-14 (ES and NQ disagreeing → the bot does not trade); A-31 (fill-quality guard); A-07 (re-check RR after the fill).
- **expected bot action:** no trade.
- **citation:** [MiaTd3hh47I@15:11; @20:46–26:38].

**EX-19 | E5 | ES | LONG (opposite-direction re-entry) | LOSS (day −$93,000)**
- **date:** 8 Jan 2026 (same day as EX-18).
- **pre-open DOLs & bias:** idea = a breakaway gap up to the relative equal highs + Asia highs.
- **sweep:** not stated before entry.
- **5m confirmation:** price "ripped through this gap and then retested this order block and then made a bullish confirmation".
- **1m trigger & entry time:** ≈**10:08–10:11** (inferred).
- **stop:** "right underneath that one minute low".
- **targets & management:** equal highs, then Asia highs. He sat through −$18K to −$40K of drawdown.
- **outcome:** stopped ≈10:37. Day −$93,000 (title −$97,421); week −$122K. Price **then** swept the low and ripped to the highs: "We were the market's liquidity".
- **TJR's lesson:** refused to chase afterwards. Two trades, two losses, done.
- **tests:** A-18 (no opposite-direction re-entry); A-17 (second loss → done); C5 (OB retest = E5-dropped zone); A-04.
- **expected bot action:** no trade.
- **citation:** [MiaTd3hh47I@29:21–32:09; @48:32; @51:36–58:46; @59:24–1:02:51].

**EX-20 | E5 | ES | LONG | LOSS −$41,290**
- **date:** Thu 22 Jan 2026. News at 10:00 "didn't do much".
- **pre-open DOLs & bias:** 4H bullish on both indices; the 1H broke down (~10:10). NQ took the London lows, ES took the hourly lows, then ES took the London lows.
- **sweep:** London lows.
- **5m confirmation:** price was above the 5m highs, in a retrace into the 15m gap / 15m EQ.
- **continuation zone:** 15m FVG / 15m EQ, which is not on the 5m (inferred deviation).
- **1m trigger & entry time:** 1m BOS up ("I went long" after breaking the highs) ~**10:22** (inferred).
- **stop:** tight, **not** under the 1m low.
- **targets & management:** TP1 at the highs right there. Stopped out; price then went his way.
- **outcome:** −$41,290 live, plus ~$2.5K funded drawdown.
- **TJR's lesson:** "we probably should have had our stop underneath this one minute low ... it was just such a low time frame trade".
- **tests:** A-04 (RETRACE_SWING stop); A-11 (10:00 news → entries allowed after 10:01); A-16 (10:22 is inside the window).
- **expected bot action:** a structural stop under the 1m low. The trade survives if the low held (not stated).
- **citation:** [c5f6hLzchyM@17:39–35:46; @40:17; @51:46–54:11; @1:12:45].

**EX-21 | E5 | NQ | LONG | WIN (partial; day roughly −$11K realized + $14–15K floating; title +$14,300)**
- **date:** Thu 22 Jan 2026 (same day as EX-20).
- **pre-open DOLs & bias:** same as EX-20. ES ripping and inverting its gap.
- **sweep:** as in EX-20.
- **5m confirmation:** ES gap inversion.
- **continuation zone:** a 1m gap respected.
- **1m trigger & entry time:** the long was taken "off of this gap getting inversed", ~**10:28** (inferred).
- **stop:** under the 1m low area (inferred).
- **targets & management:** TP1 at the 5m highs + 15m EQ (~10:34; half closed live, stop to BE) → 15m FVG → hourly highs → relative equal highs. Trimmed 1/5, then more. Runner held. Final exit keyed to ES taking its highs. RR ~1:2 floating, 1:3 at the final highs.
- **outcome:** partial win. The final close was not shown.
- **TJR's lesson:** right bias; the first stop was too tight.
- **tests:**
  - A-18 (same-direction re-entry after a loss: allowed if the sweep extreme holds and budget remains; size = remaining budget).
  - A-12: he planned ES but traded NQ ("NASDAQ gave a better opportunity"), and ES then rallied harder.
- **citation:** [c5f6hLzchyM@04:33; @56:48–1:04:24; @1:40:14–1:42:05; @2:06:13–2:08:28].

**EX-22 | E5 | NQ | LONG ×3 | LOSS, LOSS, then OFF-STREAM WIN**
- **date:** Tue 27 Jan 2026.
- **pre-open DOLs & bias:** bullish; draws at the hourly REH and 4H highs.
- **sweep:** ES swept the hourly lows; NQ held the London lows → bullish SMT.
- **5m confirmation:** 5m IFVG + 5m BOS up on NQ; 1m BOS on ES.
- **continuation zone:** **none.** He entered at market after the 5m BOS, without waiting for the retrace.
- **1m trigger & entry time:** **pre-market ~09:00–09:05** (inferred): "first time I've taken any pre-market trade".
- **stop:** not stated.
- **targets & management:** hourly/4H highs.
- **outcome:**
  - Trade 1 stopped ~09:15: −$36,920 live.
  - Re-entry ~09:16 on his phone stopped again ("lost way more than I was supposed to"); day at −$100,240.
  - Off stream, after the open, an inverse of the 5m gap gave a win of about $150K on the trade and ~+$50K on the day.
- **TJR's lesson:** should have waited for a 5m EQ/FVG respect; pre-market is slow; "the idea was there ... the execution was just" bad.
- **tests:** A-25 (no pre-market entry); C5 (retrace required); A-17 (no third trade); A-31.
- **expected bot action:** no trade before 09:30. After the open, take one trade if the 5m gap inversion + retrace + 1m trigger occurred in the window.
- **citation:** [gKOQbcg0r1M@00:00–01:41; @11:22; @20:14–24:23; @34:42–38:03].

**EX-23 | E5 | ES/NQ (not explicit) | LONG | WIN +$88,322**
- **date:** Wed 21 Jan 2026.
- **pre-open DOLs & bias:** bullish: a 4H gap inversion; ES holding stronger than NQ; "NASDAQ took out these 4-hour highs". Draws: first highs, hourly gap, PDH, 4H highs, relative equal highs.
- **sweep:** 15m FVG filled; 5m lows swept.
- **5m confirmation:** 5m gap disrespect / IFVG; a clean break above the highs on ES/NQ. He waited for the **10:00 4H close** to confirm the 4H inversion.
- **continuation zone:** a retest after the break.
- **1m trigger & entry time:** long after the retest, ~**09:50** (inferred).
- **stop:** not stated.
- **targets & management:** half at TP1 (+$23,415, stop to BE) → half of the rest at the fill of the hourly gap (+$42,639) → half at the next level (+$57,885) → full close at the final highs. Runner exit rule: 1m BOS against.
- **outcome:** +$88,322 live, plus ~$20K funded (+$4K × 5; funded risk ~$2K each for ~$4.1K, ≈1:2).
- **TJR's lesson:** "I told you guys exactly what was going to happen ... if we inverse this 4-hour gap".
- **tests:** A-27 (HTF close gating); A-09 (halves; runner exit on a 1m BOS against); C9.
- **citation:** [kaPlPoXGXKw@12:21; @13:30–33:37; @59:57–1:00:33; @1:07:40; @1:13:59–1:14:32].

**EX-24 | E5 | NQ | SHORT | WIN +$67,680 — PPI day**
- **date:** Wed 14 Jan 2026 (PPI).
- **pre-open DOLs & bias:** price ran into an hourly FVG/EQ. Draws: stacked lows.
- **sweep:** data highs / highs above the open (inferred). ES swept both highs; NQ failed the second → bearish SMT.
- **5m confirmation:** not explicit.
- **continuation zone:** hourly FVG/EQ (HTF POI).
- **1m trigger & entry time:** a 1m FVG inversion on NQ ("barely inversed"); ES had not yet inverted. Entry ≈**09:40** (inferred).
- **stop:** not stated ("full ported").
- **targets & management:** TP1 at the stacked lows (half off, stop to BE) → TP2 (half of the rest) → TP3 ≈09:57 → full close. He held through the 10:00 tariff/Supreme Court news at BE.
- **outcome:** +$67,680.32.
- **TJR's lesson:** take profit at HTF draws. For the year: "My win rate's there. The risk-to-reward is not there." He was down $64K YTD.
- **tests:**
  - A-10 (STRICT → no trade; CURRENT → allowed at 50%).
  - A-15: 09:40 → the bot waits until 09:50, by which point the TPs were mostly done, so the expected bot result is a probable no-trade.
  - A-12: ES not yet confirmed → alignment fails.
- **citation:** [vIjIitndRXQ@07:00; @11:59; @16:16–17:28; @20:00; @22:56; @30:29–34:01].

**EX-25 | E5 | ES | LONG | WIN +$42,510**
- **date:** ~7 Jan 2026 (inferred from upload).
- **pre-open DOLs & bias:** long to take the triple equal highs above.
- **sweep:** 5m lows, including the triple equal lows.
- **5m confirmation:** bullish closes above candle bodies on the 1m with NQ ripping. He missed the first leg.
- **continuation zone:** retrace into a 1m gap.
- **1m trigger & entry time:** within the first minutes of the open (inferred): "the earliest trade that I've ever taken".
- **stop:** set, not described.
- **targets & management:** TP1 at the (quadruple) equal highs → half off, stop to BE; TP2 at the next high → full close.
- **outcome:** +$42,510 ($38,500 also quoted). Done for the day after the win.
- **TJR's lesson:** "I said I want these highs to be the target, and I want us to sweep out these five-minute lows first."
- **tests:** A-15 (the bot must not enter before 09:50); A-17 (one win → done).
- **citation:** [ZioWcbxSuIw@02:17; @04:04–13:09].

**EX-26 | E5 | NQ (inferred) | SHORT | LOSS −$52,660**
- **date:** a Friday in the first week of a month, 2026 (inferred; upload date unknown).
- **pre-open DOLs & bias:** ATH, with 1H/4H bullish; "longs were the play". Price was "so overextended", so he wanted a short to the stacked 5m lows.
- **sweep:** not a significant DOL (stacked 5m lows were the *target*).
- **5m confirmation:** a bearish 5m close in the 5m FVG on both indices ("ES close bearish too").
- **continuation zone:** 5m FVG ("full-fledged retrace into this gap").
- **1m trigger & entry time:** **none.** He shorted at market on the 5m close ~**10:32** ("It's 10:30" plus ~2.5 min).
- **stop:** placed; location not stated.
- **targets & management:** stacked lows / a big gap; 50% + BE planned once ES took the first lows.
- **outcome:** ES took the first 5m lows but NQ lagged. Price swept the highs and respected the bullish gap. Stopped: −$52,660.
- **TJR's lesson:** "just entered a little bit too early"; "Stupid trade. Should have went long."
- **tests:** A-16 (after 10:30 → no trade); A-30 (a 1m trigger is required); A-26 (counter-HTF).
- **expected bot action:** no trade.
- **citation:** [0RBTSUGKA0w@1:09:23–1:11:08; @1:24:08; @1:25:14–1:25:51; @1:33:45; @1:36:18].

**EX-27 | E5 | ES/NQ | LONG | MISSED → NO TRADE**
- **date:** same day as EX-26.
- **pre-open DOLs & bias:** long (ATH, 1H/4H bullish).
- **sweep:** the open swept the lows, then price ripped.
- **5m confirmation:** implied by the rip (not stated).
- **continuation zone:** a mini retrace.
- **1m trigger & entry time:** **none.** "We had this mini retrace here, but we never broke structure to the downside on the one minute". A student took a 09:45 1m-BOS long, which TJR said was too early for him.
- **outcome:** no trade. "I usually wait until 9:50."
- **tests:** C6 (the 1m retrace must break 1m structure against the new trend before the trigger); A-15.
- **citation:** [0RBTSUGKA0w@43:27; @1:09:23].

**EX-28 | E5 | NQ | LONG | WIN**
- **date:** ~9–10 Mar 2026 (inferred). This is Tim's trade; TJR says "you could have been in the same exact trade as me". TJR's day was $139K per the title.
- **pre-open DOLs & bias:** ES swept HTF lows with NQ holding → bullish SMT.
- **sweep:** HTF lows on ES. (The open also swept a high and gave a 5m BOS down; that bearish gap was then inverted.)
- **5m confirmation:** the 5m FVG was inverted up.
- **continuation zone:** retrace to EQ.
- **1m trigger & entry time:** 1m IFVG long. Time not stated; a 09:35 bearish FVG short was skipped.
- **stop:** below the retrace (not quantified).
- **targets & management:** highs/draws; Tim's limit at $6K.
- **outcome:** win (Tim ~+$6K).
- **TJR's lesson:** waiting for the pullback "genuinely saved my life"; entering right on the 5m inversion would have been FOMO. An earlier short off the first SMT was a "bad trade" with no extension out of the continuation confluence.
- **tests:** C5 (wait for the retrace); C10 (NQ held = the leader); A-30.
- **citation:** [X8Ag7BWd9dg@00:00–02:12; @08:47–10:26; @25:59; @32:39].

**EX-29 | E5 | NQ (inferred) | SHORT | TP1 HIT, REST BE (~$25K)**
- **date:** 6 Jan 2026 (inferred). This was the day after a $99K loss.
- **pre-open DOLs & bias:** a big smooth imbalance up from the open; stacked 5m lows below; equal lows / hourly equal lows as the draw.
- **sweep:** none of significance. At ~09:39 a bearish 5m SMT (ES leading at the highs) was **passed**: "I want a higher time frame trade".
- **5m confirmation:** smooth displacement down through the imbalance (no formal BOS/IFVG cited).
- **continuation zone:** not stated.
- **1m trigger & entry time:** ≈**10:40–10:45** (inferred).
- **stop:** not stated; risk ≈ $40K.
- **targets & management:** stop to BE after the first lows; partials at the next high (+$26,540); final TP at the equal lows (not reached; rest at BE).
- **outcome:** ~+$25K.
- **TJR's lesson:** late-session trades are a downside, "way later than I would typically be trading"; patience after the loss.
- **tests:** A-16 (bot: no entry after 10:30); A-30 (an SMT alone is not an entry); C3 (stacked 5m lows are targets, not the sweep).
- **expected bot action:** no trade.
- **citation:** [QRoLG0QRiNM@07:10; @08:24; @10:58; @34:35–43:52].

**EX-30 | E5 | ES | LONG | TP HIT (teaching replay)**
- **date:** Fri 9 Jan 2026 (inferred).
- **pre-open DOLs & bias:** 4H/1H uptrend; target = hourly highs. No NY manipulation at first; equal lows below.
- **sweep:** equal lows swept on the 1H and the 5m.
- **5m confirmation:** 5m BOS up.
- **continuation zone:** the retrace closed below the upper FVG (trend still valid because lower gaps remained) and tapped a deeper FVG under EQ (discount) plus EQ.
- **1m trigger & entry time:** long; trigger and time not stated.
- **stop:** not stated.
- **targets & management:** take profit at the hourly highs, which was hit.
- **outcome:** TP hit (R not stated).
- **TJR's lesson:** be patient when NY hasn't manipulated yet.
- **tests:** C5 (a stacked-FVG continuation: closing through the top gap does not invalidate while deeper gaps exist; prefer an FVG under EQ); A-22.
- **citation:** [ironJFzNBic@09:35–16:55]; [yiuFUp0kFz8@5:08:20–5:15:38].

### E4 (2025)

**EX-31 | E4 | ES | SHORT | WIN +$45,180 (~1:2)**
- **date:** 7 Oct 2025 (inferred). A "no news" day.
- **pre-open DOLs & bias:** an hourly sweep above the PDH in pre-market; draws below.
- **sweep:** 5m manipulation. NQ took the 5m highs while ES made a lower high → 5m bearish SMT. This doubles as 2B (pre-market HTF sweep plus a post-open 5m sweep).
- **5m confirmation:** SMT plus order flow (details at [28:55–29:58]).
- **continuation zone:** not stated.
- **1m trigger & entry time:** 1m IFVG on ES; NQ also invalidated its gap. Entry ≈**10:00–10:02** (inferred; "9:53" stated shortly before).
- **stop:** not quantified.
- **targets & management:** TP1 after a long stall (≈10:27) → +$16,140, stop to BE; further TPs at the lows ($25,820 total), then the final TP.
- **outcome:** +$45,180, "1 to 2 return ratio".
- **TJR's lesson:** "That's why we always take the leading index. Before I used to take the lagging index" (the NQ shorts did worse).
- **tests:** C10 (the switch statement); A-19 2B; A-08.
- **citation:** [5RWTzr1D994@28:55–31:21; @56:13–57:20; @59:57–1:01:24].

**EX-32 | E4 | NQ | LONG | WIN +$35,827**
- **date:** 8 Oct 2025 (inferred).
- **pre-open DOLs & bias:** multi-day bullish SMT. NQ had already swept its lows; ES had stacked low-resistance lows.
- **sweep:** ES swept its stacked/equal lows; NQ held → 5m bullish SMT.
- **5m confirmation:** SMT plus structure.
- **continuation zone:** 5m retrace into EQ.
- **1m trigger & entry time:** an ES 1m BOS up + gap inversion → long **NQ** ≈**09:58** (inferred). At 09:47 he said "still a decent amount of time until I'm willing to look for a trade".
- **stop:** not specified; later moved to BE.
- **targets & management:** TP1 at the 5m highs (+$15,690, stop to BE, ≈10:03) → TP2 partial (total +$28,586, ≈10:10) → runners toward the PDH; full close ≈10:36.
- **outcome:** +$35,827.30.
- **TJR's lesson:** be patient for the 5m retrace. Confirm on the index that could still sweep.
- **tests:** C10 (trade the leader NQ; take the trigger from the opposed index ES); A-13 (**the bot trades ES/MES only; ES was the sweeping index**, so `ES_WHEN_NQ_LEADS=HALF` applies → ES long at 50% only if ES completes its own chain).
- **citation:** [YfS5yBQgubI@15:13–19:18; @23:23–31:38; @35:05; @43:23; @1:07:31].

**EX-33 | E4 | NQ | SHORT | WIN +$8,280 (wrong index)**
- **date:** 9 Oct 2025 (inferred).
- **pre-open DOLs & bias:** a bullish SMT completed (ES took the highs), used as a sweep; better draws below.
- **sweep:** highs made at 09:39.
- **5m confirmation:** 5m bearish SMT, then a NQ BOS down.
- **continuation zone:** 5m retrace into EQ.
- **1m trigger & entry time:** a **1m bearish SMT**, entered before an IFVG/BOS, ≈**09:45** (inferred).
- **stop:** above the highs.
- **targets & management:** partial when ES took the 5m lows → BE → full close.
- **outcome:** +$8,280.
- **TJR's lesson:** "ES was the leading index on the lower time frame ... we really should have taken the trade on ES."
- **tests:** A-12 (leader on the **execution** TF); A-30 (1m SMT is not a trigger); A-15.
- **citation:** [rBdlDQgSjIc@03:23; @21:11–25:49; @33:39–35:24].

**EX-34 | E4 | NQ | LONG ×2 | LOSS, LOSS (day −$52,660)**
- **date:** 9 Oct 2025 (inferred; same day as EX-33).
- **Trade 2:**
  - HTF bullish SMT at the lows (NQ held above the lows ES took).
  - Trigger: ES inverted its top gap; he wanted a 1m close above the 79% extension.
  - Entry ≈**10:07** (inferred). Stop below the lows (inferred). Targets: "this high, this high, and this high".
  - Stopped ≈10:21; day −$25,140 after it.
- **Trade 3:**
  - An impulsive NQ long ≈**10:24** (inferred): "There was not a thought behind that position."
  - Stopped ≈10:30; day −$52,660.
- **TJR's lesson:** "I really only should have lost like under 20k today and I ended up just giving the market 50k."
- **tests:** A-17 (the bot is already done after EX-33's win → **no trade 2, no trade 3**); A-18 (no opposite-direction re-entry).
- **citation:** [rBdlDQgSjIc@35:57–38:34; @52:51; @58:05; @1:01:46; @1:02:55].

**EX-35 | E4 | NQ | SHORT | LOSS −$152,060**
- **date:** 15 Oct 2025 (inferred). The day after a bank holiday; Powell the next day.
- **pre-open DOLs & bias:** weekly BOS down, retrace into an FVG, HTF bearish SMT. Draws: stacked lows (Asia, PDL, trend-line lows).
- **sweep:** ES took the 5m highs; NQ stayed below → 5m SMT.
- **5m confirmation:** **none.** No BOS and no EQ retrace.
- **continuation zone:** none.
- **1m trigger & entry time:** a 1m candle closing below the 79% extension ("Didn't need to wait for a break of structure"), ≈**09:48** (inferred).
- **stop:** above the highs, at **2× normal stop size**, with 2× normal size → ~4× normal risk.
- **targets & management:** stacked lows; never reached.
- **outcome:** stopped ≈09:54; −$152,060. A bullish SMT at the lows had been ignored ("married my bias").
- **TJR's lesson:** "Should have waited for my confluences."
- **tests:** A-20 (79% close is only a 5m confirmation, never a stand-alone 1m trigger); C5 (no retrace → no trade); A-29 / A-05 (wide stop → half size or skip); A-15.
- **expected bot action:** no trade.
- **citation:** [xxJyvmHROb4@15:04–25:26; @36:55–37:29].

**EX-36 | E4 | ES | SHORT | BACKTEST WIN 1:7.36**
- **date:** Tue 7 Oct 2025 (stated as a random-day backtest).
- **pre-open DOLs & bias:**
  - Marked: PDH, London low, PDL, 30m lows.
  - The Asia high and London high were taken pre-market and disregarded.
  - PDH swept in pre-market, with no 5m confirmation before the open.
- **sweep:** after the open, NQ swept a 5m high while ES made a lower high → bearish SMT. This is step 2 and 2B together.
- **5m confirmation:** the 5m SMT.
- **continuation zone:** ES retraced into 5m EQ; a 5m FVG was also filled.
- **1m trigger & entry time:** the first 1m confirmation was a **1m IFVG down** → short ES. Time: not stated.
- **stop:** above the retrace highs.
- **targets & management:** London lows (TP1, then BE + partials) → 30m lows → PDL. All hit.
- **outcome:** 1:7.36.
- **TJR's lesson:** the strategy works on a random day.
- **tests:** A-19; C10 (ES failed to make the new high); A-04 RETRACE_SWING; A-06 ladder.
- **citation:** [xRuMUvW3T7Q@11:30–18:07].

**EX-37 | E4 | ES & NQ | SHORT (no trade) → LONG (ES backtest LOSS; NQ live WIN)**
- **date:** Fri 17 Oct 2025.
- **pre-open DOLs & bias:** London swept the 4H lows with a 5m BOS up (a bullish idea pre-open, so 2B is required).
- **(a) Short attempt:**
  - At the open price swept the London session highs and made a 5m BOS down.
  - No bearish FVG, so he waited on EQ.
  - Price **closed above EQ** → short invalidated → no trade (~09:50).
- **(b) ES long:**
  - The open's dip was a 5m manipulation of the lows (2B), then a 5m BOS up and a 5m EQ hit (no FVG).
  - On the 1m he waited for a close above a high: failed twice, then succeeded on the third.
  - Long; stop under the lows; target the 5m highs.
  - **"On the S&P 500, you would have got stopped out."**
- **(c) NQ live:** the same sequence, with a 5m FVG fill on NQ, then a 1m entry inside it. Full profit at one target (he left for the airport): **1:1.39**.
- **TJR's lesson:** following the strategy exactly can still lose on ES. That is probability.
- **tests:** A-22 (a close beyond EQ invalidates the side, then re-check the other side); A-19; the **bot expectation is an ES LOSS** on (b), which is a valid losing test case.
- **citation:** [xRuMUvW3T7Q@20:22–26:58].

**EX-38 | E4 | ES | SHORT | BACKTEST WIN (1:3.63 max; ~1:2.x with partials)**
- **date:** Thu 2 Oct 2025 (inferred: "today", not traded).
- **pre-open DOLs & bias:** London session highs swept right as pre-market opened (08:30).
- **sweep:** pre-market (so 2B is needed). All four 5m confirmations were present pre-market: BOS, IFVG (lowest of the stacked gaps inverted), SMT (ES high at 09:00 and lower high at 09:15 vs. a NQ higher high at 09:15), and a 79% close.
- **without 2B:** a short at the 5m FVG fill with the stop above the highs, targeting the Asia lows, "would have been stopped out".
- **with 2B:**
  - After the open NQ swept the 5m highs (10:05 → a 10:25 higher high) while ES made a lower high (09:50 → 10:25). That bearish SMT is the continuation confluence; ES = the leading index.
  - The 5m trend stayed intact.
- **1m trigger & entry time:** 1m BOS down ≈**10:25–10:30**.
- **stop:** above the highs.
- **targets & management:** hourly lows (≈1:1 TP1) → stacked draws → Asia session lows. TP1–TP3 hit; TP4 missed; rest at BE.
- **outcome:** 1:3.63 max; about 1:2.x with partials.
- **TJR's lesson:** 2B prevents the pre-market-confirmation loss.
- **tests:** A-19; A-16 (the entry at 10:25–10:30 sits at the window edge; the bot accepts a trigger only if it is ≤ 10:30:00).
- **citation:** [8QDDxwUV1KM@09:55–28:54].

**EX-39 | E4 | ES | LONG | BACKTEST WIN (~1:3 realized; 1:24.27 if held)**
- **date:** Wed 1 Oct 2025 (inferred).
- **pre-open DOLs & bias:** no pre-market sweep → no 2B.
- **sweep:** at the open, HTF/London-type lows swept (seen on the 1m).
- **5m confirmation:** BOS up; SMT (ES higher low vs. NQ lower low → trade ES); 79% close. No IFVG.
- **continuation zone:** the first 5m FVG was filled but invalidated. A deep wick came down to equal the lows without closing above EQ ("spooked"). The patient route: a fresh 5m BOS up → 5m EQ (low to the new high) → entry.
- **1m trigger & entry time:** a 1m IFVG (aggressive) or a 1m BOS / 79% close (patient). Time: not stated.
- **stop:** under the low.
- **targets & management:** 5m highs → Asia session highs → PDH. All TPs hit.
- **outcome:** ~1:3 with partials; 1:24.27 if held to the last TP.
- **tests:** C5 (re-anchor EQ after an invalidated FVG); A-22; C10.
- **citation:** [8QDDxwUV1KM@30:00–40:44].

**EX-40 | E4 | ES | LONG ×2 | LOSS −$41,620, then BE re-entry (day −$1,953) — PPI day**
- **date:** 10 Sep 2025 (inferred; PPI). He skipped CPI the next day.
- **pre-open DOLs & bias:** originally a bearish lean. PPI 08:30 data highs and lows marked as draws.
- **sweep:** NQ swept the PPI data lows while ES held → bullish SMT.
- **5m confirmation:** not explicit before trade 1.
- **continuation zone:** not stated.
- **Trade 1:**
  - Trigger: a 1m bullish SMT and bullish closes on both indices. Entry ≈**09:46** (inferred).
  - Stop: below the lows.
  - Stopped ≈09:51: −$41,620 ("way more risk than I wanted ... I thought it was going to be like $30,000").
- **Trade 2 (re-entry):**
  - ≈**09:54** (inferred), after NQ inverted its gap and printed a 1m BOS up; ES was still above the lows.
  - TP1 ≈10:06 → stop to BE. Final targets at the data highs / relative equal highs.
  - Remainder stopped at BE.
- **outcome:** day −$1,953 after fees.
- **TJR's lesson:** directional bias right all week; entries too early (before 09:50).
- **tests:** A-15 (bot: trade 1 is not allowed before 09:50); A-18 (re-entry rule); A-30 (a 1m SMT is not a trigger); A-10 (PPI: STRICT → no trade).
- **citation:** [2ZArg3kPPkE@02:19; @09:10–27:51; @36:31–39:16; @1:00:08].

**EX-41 | E4 | ES | LONG ×2 | LOSS −$20,000, then partial (day −$4,100)**
- **date:** 25 Aug 2025 (inferred; post-Jackson Hole).
- **pre-open DOLs & bias:** bullish; pre-market sweep of the London lows with a bullish SMT.
- **sweep:** NQ swept the 5m lows; ES held (SMT). This is 2B.
- **5m confirmation:** not explicit.
- **continuation zone:** retrace into the gap/EQ held.
- **Trade 1:**
  - Trigger: bullish candle closes. Entry ≈**09:41** (inferred).
  - Stop: below the lows. Two 1m bearish SMTs were a warning.
  - Stopped ≈09:46: −$20,000.
- **Trade 2:**
  - ≈**09:49** (inferred), on NQ closing above the highs.
  - TP1 half at nearby highs ≈10:00, then BE; rest stopped ≈10:13.
- **outcome:** day −$4,100.
- **TJR's lesson:** "we got the worst index on this trade" (NQ ran; ES lagged). "Ideally, we wait at least like 10 minutes into market open."
- **tests:** A-15; A-20 (the 79% close is defined here: fib from the swing high to the low, used when there is no gap); A-12.
- **citation:** [tWYSAHQpywE@03:21–18:26; @19:49–31:29; @44:13–44:45].

**EX-42 | E4 | NQ (inferred) | SHORT | WIN (all TPs)**
- **date:** Tue 9 Sep 2025 (inferred: "yesterday"; live trade re-shown in replay).
- **pre-open DOLs & bias:** 1H highs (two), 1H lows, Asia session low, London session high.
- **sweep:** at the open NQ swept a key-level high; ES did not → bearish 5m SMT (the confirmation).
- **5m confirmation:** the SMT.
- **continuation zone:** no FVG/OB/breaker existed, so EQ from the high to the new low. A 5m retrace candle pushed into and above EQ.
- **1m trigger & entry time:** the retrace broke 1m structure up, then a **1m SMT** (ES lower high vs. NQ higher high) triggered the short. A 1m BOS came slightly later as the alternative trigger. Time: not stated.
- **stop:** above the sweep high (or the retrace highs).
- **targets & management:** pre-market lows → Asia session lows. "We hit all of our take profits."
- **outcome:** win.
- **tests:** C5 EQ-only continuation; C6 (bot trigger = the later 1m BOS, not the 1m SMT, per A-30); C10. Note the index oddity: he executed on NQ, which made the higher high (pre-switch-like). Bot: ES failed → trade ES.
- **citation:** [BMyeYQIj_vU@14:25–20:34].

**EX-43 | E4 | ES | LONG | WIN (TP1 1:2.29, TP2 1:3.48, TP3 1:5.68)**
- **date:** ~12 May 2025 or the prior trading day (inferred).
- **pre-open DOLs & bias:** 4H low draw below on both indices; hourly highs plus London/Asia session highs above.
- **sweep:**
  - First 5m candle swept the 5m low-resistance highs (manipulation; not traded).
  - NQ then dumped and swept its 4H low; ES did **not** (higher low) → HTF SMT, ES = the leading index.
- **5m confirmation:** a 1m BOS up on both, plus a 1m SMT (this is a 1m-execution variant).
- **continuation zone:** a 1m FVG filled by a wick, then an up-candle close.
- **1m trigger & entry time:** long ES, after **09:50**. Exact time not stated.
- **stop:** under the 1m lows that formed the BOS (below the FVG).
- **targets & management:** TP1 hourly high **1:2.29** → TP2 next hourly high **1:3.48** → London session high **1:5.68**.
- **outcome:** win.
- **TJR's lesson:** A+ = HTF level + SMT + BOS + continuation.
- **tests:** C10 (ES failed to make the new low → trade ES, the canonical case for an ES bot); C7 (after 09:50); A-06 ladder.
- **citation:** [tT3lUnwayb0@25:04–37:21].

**EX-44 | E4 | ES | SHORT ×2 | LOSS −$24,000, then re-entry (realized −$3,650)**
- **date:** Wed 21 May 2025.
- **pre-open DOLs & bias:** HTF bearish (low-resistance lows). **NQ bullish on all order flow.**
- **sweep:** London session highs.
- **5m confirmation:** ES 5m BOS down, then the gap filled.
- **continuation zone:** 5m gap.
- **Trade 1:**
  - Entry "right here on ES" ≈**10:00** (inferred).
  - Stop placed on one position only; two positions had no stop (platform failure).
  - A no-news 10:00 spike → −$24,000.
- **Trade 2:**
  - ≈**10:11** (inferred), after an ES 5m close; NQ closed below the 79% level and broke 1m structure.
  - TP1 at four equal lows (≈10:48) → partials + BE; runner toward the hourly/London lows.
- **outcome:** realized −$3,650; ~+$7K floating at the end.
- **TJR's lesson:** execution/platform risk.
- **tests:** A-14 (NQ bullish on all order flow vs. an ES short → **misaligned → bot no trade**); A-31 (stop placed with the entry); A-18.
- **citation:** [iVOjRDrjFM4@30:45–34:02; @39:54–43:50; @1:18:11–1:23:23].

**EX-45 | E4 | ES | SHORT ×2 | LOSS −$19K, then re-entry (day ≈+$4K)**
- **date:** Mon 17 Mar 2025 (inferred).
- **pre-open DOLs & bias:** draws at the London highs + CPI data highs. NQ took them; ES did not → 5m SMT ("ES lagging" in his E4 wording; ES = the index that failed).
- **sweep:** London/data highs on NQ.
- **5m confirmation:** 5m SMT.
- **continuation zone:** none stated.
- **Trade 1:**
  - Trigger: a 1m breaker, after "the macro opened". Stop above the highs; TP1 at EQ.
  - At ~2R (equal lows formed) he moved the stop down *under* the highs → stopped: ~−$19K.
- **Trade 2:**
  - Re-entry on a BOS down; stop above the highs.
  - Partial at the equal lows / EQ → TP2 → final at the hourly lows; runner stopped at BE.
- **outcome:** day ≈+$4,000.
- **TJR's lesson:** don't trail stops. The emotional move came from adjusting to a bigger size.
- **tests:** A-08/A-09 (no discretionary trailing before TP1); C5 (a 1m breaker is not a valid E5 zone); A-18.
- **citation:** [WlnpOPPnBQw@04:42–08:04].

**EX-46 | E4 | NQ | SHORT | WIN (~$25,000; TP1 1:1.7)**
- **date:** Tue 4 Mar 2025 (inferred).
- **pre-open DOLs & bias:**
  - Hourly downtrend; the S&P was in a 5m downtrend into the open.
  - Levels: Asia and London H/L, a 1H high, a 1H FVG. No useful 4H level.
- **sweep:** at 09:30 the London low was swept, but no confirmation followed, so no trade. Price then pushed up into the **1H FVG**. At 09:35 ES made a lower high while NQ made a higher high → bearish SMT. He traded **NQ, "the lagging index"**, which made the higher high (pre-Jul-2025 rule).
- **5m confirmation:** SMT. The 5m was still bearish, so the up-move also counted as an EQ fill.
- **continuation zone:** EQ; price went above the 5m OB and breaker (acceptable "because it's an SMT setup").
- **1m trigger & entry time:** a 1m BOS + IFVG before 09:50 was **not** taken ("not 950 yet"). At 09:50 the 1m was back in an uptrend. A **1m bearish IFVG closed right at 09:50** → short.
- **stop:** just above the IFVG or above the highs.
- **targets & management:** TP1 at the key level below, **1:1.7**; further TPs at the 4H lows; "hits every single one of them".
- **outcome:** "made $25,000".
- **TJR's lesson:** don't enter before 09:50.
- **tests:**
  - A-15 (perfect positive example).
  - C10 under E5: the bot trades **ES**, the index that failed to make the new high, and checks whether ES produced its own 1m trigger. This tests the era switch.
- **citation:** [SHJHpedYh6A@3:18:29–3:20:12; @3:42:15–3:53:09].

**EX-47 | E4 | ES/NQ | — | NO TRADE (chop)**
- **date:** Thu 22 May 2025 (unemployment claims day).
- **pre-open DOLs & bias:** no strong bias; price above the Asia/London highs.
- **why no trade:** a short would be "catching a rising knife". "Zero trades taken."
- **outcome:** no trade.
- **tests:** A-23 (chop/no-bias filter); A-01 (no significant DOL swept in the right direction).
- **citation:** [ssPMxVk6B9Y@02:15–02:50; @07:21].

**EX-48 | E4 | NQ | SHORT | LOSS (title −$14,646, inferred)**
- **date:** Tue 9 Dec 2025 (the day before FOMC).
- **pre-open DOLs & bias:** HTF lows as low-resistance draws.
- **missed long earlier:** an HTF PDL sweep (NQ), bullish SMT, 5m BOS up on ES. He wanted a 1m BOS down + 5m gap fill + 1m BOS up; it never came. Price rallied to the hourly highs. Correct no-trade by C6.
- **sweep:** ES took the highs/Asia highs; NQ failed → bearish SMT.
- **5m confirmation:** a "5m BOS" that was actually on the **3m chart**.
- **continuation zone:** EQ filled; 5m lows taken.
- **1m trigger & entry time:** ES 1m IFVG → short NQ ≈**10:08** (inferred). He de-risked: ≈$13K risk.
- **stop:** above the highs.
- **targets & management:** TP1 at a marked line (not specified). Unresolved on stream at 10:30.
- **outcome:** loss (inferred from the title).
- **TJR's lesson:** "13K on pretty much a coin flip"; wrong timeframe; don't trade sick.
- **tests:** execution TF = 5m only (no 3m); C6 (the missed long is a correct no-trade).
- **citation:** [g27VsJS3a58@18:21; @27:40; @38:10–51:16; @1:06:26–1:07:00].

### E3 (Sep 2023 – 2024)

**EX-49 | E3 | ES | SHORT | WIN +$6,000**
- **date:** Thu 6 Jun 2024.
- **pre-open DOLs & bias:** bearish. "Overbought" after Wednesday's rally; daily highs swept; range EQ below.
- **sweep:** 1H highs swept right at the open. SMT: **ES higher high vs. NQ lower high**. He traded **ES**, the index that *made* the extreme (E3 rule).
- **5m confirmation:** a 1m bullish FVG invalidated (IFVG); 1m execution.
- **continuation zone:** a bearish 1m FVG filled "perfectly", plus a reaction.
- **1m trigger & entry time:** short, minutes after 09:30. Exact time not stated.
- **stop:** above the high.
- **targets & management:** TP1 at the 15m lows (1:2; one contract closed); final at the HTF lows (NQ had already taken its equivalent lows), hit "over time".
- **outcome:** +$6,000 in under an hour.
- **TJR's lesson:** a full confluence stack: bias + sweep + SMT + IFVG + FVG.
- **tests:**
  - Era contrast for C10: under E5 the bot would trade **NQ**, the index that failed. Since the bot only trades ES, `ES_WHEN_NQ_LEADS=HALF` applies.
  - A-15: a pre-09:50 entry → the bot waits.
- **citation:** [Ias0HhHUqj4@00:00–04:31].

### E2 (Boot Camp 1 & 2.0, 2023)

**EX-50 | E2 | ES | LONG | LOSS (wicked out)**
- **date:** Mon 3 Jul 2023 (high-impact news; bank holiday the next day).
- **pre-open DOLs & bias:** daily bullish.
- **sweep:** a 5m liquidity sweep (lows).
- **5m confirmation:** none; a 1m BOS up only.
- **continuation zone:** none (BC1 model 1).
- **1m trigger & entry time:** entered on the close of the 1m BOS candle. Time: not stated.
- **stop:** under the 5m sweep low with a buffer ("four below").
- **targets & management:** not reached.
- **outcome:** stopped by a wick. Price then moved higher, and a 5m BOS up formed afterwards. Size: 100 lots = half his normal 200 because of news and the holiday.
- **TJR's lesson:** the stop was at invalidation, and being wicked out while the bias plays out is acceptable: "maybe we should have covered ourselves by putting price lower".
- **tests:**
  - A-01: a 5m sweep is not a significant DOL → **bot no trade**.
  - C5: no continuation step.
  - A-04: the 0.5-pt buffer.
  - A-10: half size on news / the eve of a holiday.
- **citation:** [1FunNCUw_jM@05:09–12:58].

**EX-51 | E2 | ES | LONG | LOSS ≈ −$9.5K**
- **date:** Fri 14 Jul 2023 (after a 10:00 news release).
- **pre-open DOLs & bias:** weekly, daily, 4H, 1H and 15m all bullish. A 1H OB and accumulation were marked, plus an FVG and a 15m low below.
- **sweep:** an **unmarked** lower-timeframe sweep.
- **5m confirmation:** BOS up.
- **continuation zone:** EQ; a strong rejection candle closed back out of EQ = entry.
- **1m trigger & entry time:** the close of the rejection candle. Time: after 10:00 (not stated exactly).
- **stop:** just below the wick.
- **targets & management:** near TP1 but never hit.
- **outcome:** reversed and stopped out, ≈ −$9.5K. Price later swept under the stops, came into the marked 1H OB, filled the FVG and rallied.
- **TJR's lesson:** wait for your marked HTF building blocks; the LTF sweep entry was the error.
- **tests:** A-01 (only significant DOLs count as the sweep → **bot no trade** at the first sweep; possible trade later at the 1H-level sweep, if it falls inside the window).
- **citation:** [__fKQR5RR08@18:44–28:10].

**EX-52 | E2 | ES | LONG ×2 | LOSS (fixed 5-pt stop), then RE-ENTRY WIN**
- **date:** Tue 5 Sep 2023.
- **pre-open DOLs & bias:** a downtrend broke → bullish. An area of accumulation was tapped in pre-market and again at the open.
- **Trade 1:**
  - Entry immediately at the FVG fill with **no reaction**.
  - **Fixed 5-point stop**, using 50% of the daily risk → stopped: "jumped the gun".
- **Trade 2:**
  - The sweep low held (bias intact). BOS up, FVG filled, reaction (three confluences).
  - Stop under the invalidation point.
  - TP1 50% → TP2 50% of the rest → rest closed on a 1m BOS down.
- **outcome:** profit for the day.
- **TJR's lesson:** the stop must sit at invalidation, not a fixed size; wait for the reaction.
- **tests:** A-04 (structural stop, never a fixed one); C6 (a trigger is required, not a touch); A-18 re-entry conditions.
- **citation:** [ss-dZPMnjeY@01:43–05:40; @10:06].

**EX-53 | E2 | ES | LONG | WIN (TP1 + TP2, rest BE) — news day, half size**
- **date:** Wed 30 Aug 2023 (GDP + employment data; NFP week).
- **pre-open DOLs & bias:** bullish: the news was bullish and the 1H broke structure up in pre-market.
- **sweep:** not emphasized (not stated).
- **5m confirmation:** price drew into the 5m accumulation.
- **continuation zone:** 5m accumulation (≈ OB, an E2 zone).
- **1m trigger & entry time:** 1m BOS up. Time: not stated.
- **stop:** under the low.
- **targets & management:** TP1 1:1 (50% off, BE) → TP2 at the hourly liquidity range that caused the big drop; rest at BE.
- **outcome:** TP1 + TP2. Half normal size.
- **TJR's lesson:** reduce risk on news days.
- **tests:** A-10 (other high-impact news → 50% size after the release); C3 (no stated significant sweep → under E5 the bot needs a sweep; likely no trade).
- **citation:** [7MBD3ow7I1g@01:43–04:29].

**EX-54 | E2 | ES | SHORT | LOSS ≈ −$13K**
- **date:** ~24 Aug 2023 (inferred; PMI day).
- **pre-open DOLs & bias:** daily, 4H and 1H bearish. He wanted a sweep of the hourly highs.
- **sweep:** **none.** Price pushed into the 15m/1H OB + FVG without sweeping the hourly highs.
- **5m confirmation:** none; a 1m BOS down only.
- **continuation zone:** none (no third confluence).
- **1m trigger & entry time:** a 50% position on the 1m BOS candle at the NY open. Time: not stated.
- **stop:** above (inferred: beyond the hourly structure).
- **targets & management:** hourly low, 4H low, 4H OB, daily lows.
- **outcome:** price ripped up; ≈ −$13K.
- **TJR's lesson:** wait for the third confluence.
- **tests:** C3 (no sweep), C4/C5 (no 5m confirmation, no retrace) → **bot no trade**.
- **citation:** [o_SdawM3DIE@04:52–07:44].

**EX-55 | E2 | ES | — | NO TRADE (late setup)**
- **date:** ~19 Jul 2023.
- **pre-open DOLs & bias:** everything bullish; monthly high as the draw. He wanted an OB pullback.
- **what happened:** price ripped with no pullback entry. A setup appeared late in NY and he skipped it as too late.
- **outcome:** no trade.
- **tests:** A-16 (no late entries); C5 (no retrace → no trade).
- **citation:** [9sD9kTia4V4@02:49–04:28; @10:52–11:26].

**EX-56 | E2 | ES | LONG | LOSS (stop missed by 2.7 pt)**
- **date:** Tue 12 Sep 2023.
- **pre-open DOLs & bias:** the daily broke its downtrend → bullish.
- **sweep:** lows swept.
- **5m confirmation:** BOS up.
- **continuation zone:** the FVG filled too deep; then a new high and a second 1m BOS.
- **1m trigger & entry time:** close of the second 1m BOS. Time: not stated.
- **stop:** under the low. **Stopped by 2.7 points.**
- **targets & management:** not reached.
- **outcome:** loss. Price then filled the 15m accumulation and rallied through his targets.
- **TJR's lesson:** right bias, execution off; not upset.
- **tests:** A-04 (RETRACE_SWING vs. SWEEP_EXTREME: would the sweep-extreme stop have survived? Not stated); A-05 (stop size).
- **citation:** [7Q3nalPsSpk@00:35–04:34].

---

**How to use these cases in testing.**

1. **Replay ES and NQ 1m data for each dated case.** Where the date is marked "(inferred)", first confirm the date by matching the described sequence. Check, for example, that NQ swept the London high at 09:30 while ES did not.
2. **Assert the expected bot action, not TJR's.** The expected action follows from CANONICAL.md and §18. The cases where he broke his own rules are intentional negative tests: EX-09, EX-11, EX-15, EX-16, EX-18, EX-19, EX-22, EX-24, EX-26, EX-29, EX-34, EX-35, EX-40, EX-44, EX-50, EX-51 and EX-54.
3. **Report how often the bot matches.** Report the match rate separately for E5 and E4 cases. Never tune the defaults on E2/E3 cases.

## 20. Source index

Coverage: 260 videos processed from full transcripts — Boot Camp + Boot Camp 2.0: 69 videos / 22.1 h (only Day 48 Pt.1 has no audio; its re-upload Pt.2 is included); other TJR content: 191 videos / 114.1 h. Total 136.2 h.

| # | video_id | upload date | min | type | substance | title |
|---|---|---|---|---|---|---|
| 1 | [Xq6-oO2n6-U](https://www.youtube.com/watch?v=Xq6-oO2n6-U) | 20230526 | 55 | psychology | low | Boot Camp Day 1: Take Action |
| 2 | [bEkbNGUzQME](https://www.youtube.com/watch?v=bEkbNGUzQME) | 20230527 | 23 | lesson | medium | Boot Camp Day 2: Candlesticks |
| 3 | [w2CWF0WtLmQ](https://www.youtube.com/watch?v=w2CWF0WtLmQ) | 20230528 | 33 | psychology | low | Boot Camp Day 3: Discipline |
| 4 | [viuGHEuv0nw](https://www.youtube.com/watch?v=viuGHEuv0nw) | 20230529 | 28 | lesson | high | Boot Camp Day 4: Trends |
| 5 | [N7so8LEHmLA](https://www.youtube.com/watch?v=N7so8LEHmLA) | 20230530 | 23 | psychology | low | Boot Camp Day 5: Goal Setting |
| 6 | [PmhuPbY8ZHo](https://www.youtube.com/watch?v=PmhuPbY8ZHo) | 20230531 | 30 | lesson | high | Boot Camp Day 6: Break of Structure |
| 7 | [_6voYEdi5j4](https://www.youtube.com/watch?v=_6voYEdi5j4) | 20230601 | 18 | psychology | low | Boot Camp Day 7: Individuality |
| 8 | [Lxnu7InGhGE](https://www.youtube.com/watch?v=Lxnu7InGhGE) | 20230602 | 11 | lesson | high | Boot Camp Day 8: Liquidity Pt 1 |
| 9 | [-ga9oK2bClQ](https://www.youtube.com/watch?v=-ga9oK2bClQ) | 20230603 | 7 | psychology | low | Boot Camp Day 9: Check In |
| 10 | [rdz6vnXb8wE](https://www.youtube.com/watch?v=rdz6vnXb8wE) | 20230604 | 16 | lesson | high | Boot Camp Day 10: Liquidity Pt. 2 |
| 11 | [_jLR3XcB5eQ](https://www.youtube.com/watch?v=_jLR3XcB5eQ) | 20230605 | 17 | psychology | low | Boot Camp Day 11: How to take a Loss |
| 12 | [KtC2SbemF6w](https://www.youtube.com/watch?v=KtC2SbemF6w) | 20230606 | 20 | lesson | high | Boot Camp Day 12: Liquidity Pt  3 |
| 13 | [RkMBoqbeUq8](https://www.youtube.com/watch?v=RkMBoqbeUq8) | 20230607 | 16 | psychology | medium | Boot Camp Day 13: Risk Management |
| 14 | [d0AxLACYaqU](https://www.youtube.com/watch?v=d0AxLACYaqU) | 20230608 | 10 | lesson | medium | Boot Camp Day 14: Fair Value Gaps Pt. 1 |
| 15 | [T4xVS7iV5d8](https://www.youtube.com/watch?v=T4xVS7iV5d8) | 20230609 | 18 | psychology | low | Boot Camp Day 15: Identifying problems |
| 16 | [339amTioakE](https://www.youtube.com/watch?v=339amTioakE) | 20230611 | 14 | psychology | low | Boot Camp Day 17: Patience |
| 17 | [S1kY3Fw6JUQ](https://www.youtube.com/watch?v=S1kY3Fw6JUQ) | 20230611 | 12 | lesson | high | Boot Camp Day 16: FVG Pt. 2 |
| 18 | [w5sUCqFH3Lg](https://www.youtube.com/watch?v=w5sUCqFH3Lg) | 20230613 | 24 | lesson | high | Boot Camp Day 19: How to Read News Data |
| 19 | [qhuFg_OXdmE](https://www.youtube.com/watch?v=qhuFg_OXdmE) | 20230614 | 12 | lesson | medium | Boot Camp Day 20: Order Blocks |
| 20 | [z9p7OThLkr4](https://www.youtube.com/watch?v=z9p7OThLkr4) | 20230616 | 60 | psychology | low | Boot Camp Day 21: How to Take a Win & Life Lessons |
| 21 | [RQSVIKddFHI](https://www.youtube.com/watch?v=RQSVIKddFHI) | 20230617 | 25 | lesson | high | Boot Camp Day 22: Order Blocks pt.2 |
| 22 | [ERbhCL9KW_g](https://www.youtube.com/watch?v=ERbhCL9KW_g) | 20230618 | 15 | mixed | low | Boot Camp Day 23: Check In/ Be my boy |
| 23 | [12_F-mIUfL0](https://www.youtube.com/watch?v=12_F-mIUfL0) | 20230620 | 27 | lesson | high | Boot Camp Day 24: Order Blocks pt.3 |
| 24 | [4moWbfm6smw](https://www.youtube.com/watch?v=4moWbfm6smw) | 20230621 | 18 | psychology | medium | Boot Camp Day 25: Over Confidence |
| 25 | [j1pVK897oZQ](https://www.youtube.com/watch?v=j1pVK897oZQ) | 20230622 | 18 | lesson | medium | Boot Camp Day 26: Equilibrium |
| 26 | [-E7plUbSJUk](https://www.youtube.com/watch?v=-E7plUbSJUk) | 20230623 | 21 | lesson | high | Boot Camp Day 28: Equilibrium pt.2 |
| 27 | [TwakmPZJGJA](https://www.youtube.com/watch?v=TwakmPZJGJA) | 20230623 | 32 | psychology | medium | Boot Camp Day 27: Fear |
| 28 | [065lMUrD_kg](https://www.youtube.com/watch?v=065lMUrD_kg) | 20230624 | 23 | lesson | high | Boot Camp Day 29: Trading Plan |
| 29 | [ESsy0uoFAz4](https://www.youtube.com/watch?v=ESsy0uoFAz4) | 20230625 | 9 | lesson | high | Boot Camp Day 30: Execution |
| 30 | [isetVuqlSLo](https://www.youtube.com/watch?v=isetVuqlSLo) | 20230625 | 19 | psychology | low | Boot Camp Day 31: Hard Work |
| 31 | [K8DwhtmvAW8](https://www.youtube.com/watch?v=K8DwhtmvAW8) | 20230628 | 24 | lesson | medium | Boot Camp Day 33: Execution pt.3 |
| 32 | [SLhIA7vW9x8](https://www.youtube.com/watch?v=SLhIA7vW9x8) | 20230628 | 23 | lesson | medium | Boot Camp Day 32: Execution pt.2 |
| 33 | [sjuWqKDsQtI](https://www.youtube.com/watch?v=sjuWqKDsQtI) | 20230629 | 20 | lesson | high | Boot Camp Day 34: Daily Bias |
| 34 | [UPA9LQW7phk](https://www.youtube.com/watch?v=UPA9LQW7phk) | 20230630 | 15 | mixed | high | Boot Camp Day 35: Daily Bias pt. 2 |
| 35 | [Y1lqifylC4s](https://www.youtube.com/watch?v=Y1lqifylC4s) | 20230701 | 22 | lesson | high | Boot Camp Day 36: Daily Bias pt. 3 |
| 36 | [FjSiLFrg5fo](https://www.youtube.com/watch?v=FjSiLFrg5fo) | 20230702 | 11 | lesson | high | Boot Camp Day 37: Taking Profits |
| 37 | [1FunNCUw_jM](https://www.youtube.com/watch?v=1FunNCUw_jM) | 20230703 | 13 | mixed | high | Boot Camp Day 38: Stop Losses |
| 38 | [KSiWKfPOlh4](https://www.youtube.com/watch?v=KSiWKfPOlh4) | 20230704 | 15 | lesson | high | Boot Camp Day 39: Calculating Lot Size |
| 39 | [O_4yHzZO0u0](https://www.youtube.com/watch?v=O_4yHzZO0u0) | 20230705 | 9 | mixed | low | Boot Camp Day 40: Help me help you |
| 40 | [PyCPHiO2nj0](https://www.youtube.com/watch?v=PyCPHiO2nj0) | 20230706 | 12 | psychology | medium | Boot Camp Day 41: Learn from Losses |
| 41 | [NPG_BZ_83fo](https://www.youtube.com/watch?v=NPG_BZ_83fo) | 20230707 | 10 | lesson | medium | Boot Camp Day 42: How to Backtest |
| 42 | [9SUJfAo6Sl8](https://www.youtube.com/watch?v=9SUJfAo6Sl8) | 20230709 | 10 | lesson | medium | Boot Camp Day 43: Weekly Analysis |
| 43 | [LG_IbfjbaOo](https://www.youtube.com/watch?v=LG_IbfjbaOo) | 20230710 | 22 | psychology | low | Boot Camp Day 45: Over Complicating |
| 44 | [uGi6EeKnWSk](https://www.youtube.com/watch?v=uGi6EeKnWSk) | 20230710 | 26 | mixed | medium | Boot Camp Day 44: Try not to Trade |
| 45 | [CZRs2NuLQIw](https://www.youtube.com/watch?v=CZRs2NuLQIw) | 20230711 | 12 | lesson | medium | Boot Camp Day 46: Journaling Trades |
| 46 | [__fKQR5RR08](https://www.youtube.com/watch?v=__fKQR5RR08) | 20230714 | 30 | mixed | high | Boot Camp Day 49: Daily Bias/Backtesting + $9k Loss SPX Trade Recap |
| 47 | [QRvZgj3k8pk](https://www.youtube.com/watch?v=QRvZgj3k8pk) | 20230715 | 10 | lesson | medium | Boot Camp Day 50: Weekly Analysis |
| 48 | [-rYGugTIsbU](https://www.youtube.com/watch?v=-rYGugTIsbU) | 20230717 | 20 | mixed | medium | Boot Camp Day 52: Daily Bias + Break Even Trading Recap |
| 49 | [XcA0GiWZp7M](https://www.youtube.com/watch?v=XcA0GiWZp7M) | 20230717 | 24 | psychology | low | Boot Camp Day 51: Sunday Motivation |
| 50 | [Oi_mK1Lt-iQ](https://www.youtube.com/watch?v=Oi_mK1Lt-iQ) | 20230719 | 10 | mixed | medium | Boot Camp Day 53: Daily Bias + $19k Profit GBPJPY Recap |
| 51 | [9sD9kTia4V4](https://www.youtube.com/watch?v=9sD9kTia4V4) | 20230720 | 16 | mixed | medium | Boot Camp Day 54: Daily Bias + No Trades Today |
| 52 | [IFgysr8gDjc](https://www.youtube.com/watch?v=IFgysr8gDjc) | 20230725 | 21 | psychology | low | Boot Camp Day 55: THE END |
| 53 | [OH--4nkbXlM](https://www.youtube.com/watch?v=OH--4nkbXlM) | 20230824 | 19 | mixed | medium | Boot Camp 2.0 Day 2: How to handle emotions |
| 54 | [o_SdawM3DIE](https://www.youtube.com/watch?v=o_SdawM3DIE) | 20230824 | 40 | mixed | medium | Boot Camp 2.0 |
| 55 | [G7eq6U8e3yw](https://www.youtube.com/watch?v=G7eq6U8e3yw) | 20230825 | 18 | mixed | medium | Boot Camp 2.0 Day 3: Risk |
| 56 | [4aYaeI2Av2I](https://www.youtube.com/watch?v=4aYaeI2Av2I) | 20230826 | 22 | mixed | low | Boot Camp 2.0 Day 4: Best Forex Broker |
| 57 | [IY9NJbaNyqA](https://www.youtube.com/watch?v=IY9NJbaNyqA) | 20230828 | 19 | mixed | high | Boot Camp 2.0 Day 5: How to find Trade Bias |
| 58 | [Iu_v4kuFQhk](https://www.youtube.com/watch?v=Iu_v4kuFQhk) | 20230828 | 3 | recap | medium | Boot Camp 2.0 Day 5.5: Second Trade |
| 59 | [oJq8egtzCto](https://www.youtube.com/watch?v=oJq8egtzCto) | 20230829 | 10 | recap | medium | Boot Camp 2.0 Day 6: Best Loss to Take |
| 60 | [7MBD3ow7I1g](https://www.youtube.com/watch?v=7MBD3ow7I1g) | 20230830 | 8 | mixed | high | Boot Camp 2.0 Day 7: Risk Management and Probabilities |
| 61 | [ss-dZPMnjeY](https://www.youtube.com/watch?v=ss-dZPMnjeY) | 20230905 | 14 | mixed | high | Boot Camp 2.0 Day 9: Leveraging Risk |
| 62 | [r-DdsJLUlBk](https://www.youtube.com/watch?v=r-DdsJLUlBk) | 20230907 | 10 | recap | medium | Boot Camp 2.0 Day 10: Trade Recaps |
| 63 | [6zXKK3Wrusg](https://www.youtube.com/watch?v=6zXKK3Wrusg) | 20230908 | 14 | mixed | high | Boot Camp 2.0 Day 11: Where to Take Profit |
| 64 | [SV37R6j5f4M](https://www.youtube.com/watch?v=SV37R6j5f4M) | 20230911 | 11 | recap | medium | Boot Camp 2.0 Day 12: Red Day |
| 65 | [7Q3nalPsSpk](https://www.youtube.com/watch?v=7Q3nalPsSpk) | 20230912 | 14 | mixed | high | Boot Camp 2.0 Day 13: I Made $ on a Bad Trade |
| 66 | [5v4G4xJVKIQ](https://www.youtube.com/watch?v=5v4G4xJVKIQ) | ?   # missing in transcript front matter; content implies ~20230831 (inferred: "GJ loss two days ago" = Day 6, 20230829) | 16 | mixed | high | Boot Camp 2.0 Day 8: How to split positions |
| 67 | [S-scwzKRP-8](https://www.youtube.com/watch?v=S-scwzKRP-8) | unknown   # front matter "?"; content is CPI day, most likely 20230712 (inferred) | 17 | lesson | high | Boot Camp Day 47: Back Testing CPI |
| 68 | [4FEty6xgOc0](https://www.youtube.com/watch?v=4FEty6xgOc0) | unknown   # front matter "?"; content is PPI day, most likely 20230713 (inferred) | 15 | lesson | high | Boot Camp Day 48 Pt. 2 (with audio): Live Daily Bias Analysis on PPI |
| 69 | [qecF411R83s](https://www.youtube.com/watch?v=qecF411R83s) | unknown   # transcript front matter has "?"; sits between 20230611 and the Day 19 upload | 17 | lesson | high | Boot Camp Day 18: FVG Pt. 3 |
| 70 | [ox3p5Um1TqY](https://www.youtube.com/watch?v=ox3p5Um1TqY) | "? (recorded Monday 2024-07-08 at 8:41 am ET, per his own statement)" | 11 | lesson | medium | Live Example: How to Find Daily Bias |
| 71 | [go3cEFGN-1c](https://www.youtube.com/watch?v=go3cEFGN-1c) | 20220927 | 20 | mixed | medium | S&P500 Weekly analysis + How to enter a Trade |
| 72 | [XxJAkUfbs0k](https://www.youtube.com/watch?v=XxJAkUfbs0k) | 20221003 | 41 | mixed | medium | How to Spot Liquidity Sweeps in the Market |
| 73 | [YMqC2ZvwCJg](https://www.youtube.com/watch?v=YMqC2ZvwCJg) | 20221012 | 31 | mixed | medium | How to Spot Fair Value Gaps in the Market |
| 74 | [0R3TEHZgwxA](https://www.youtube.com/watch?v=0R3TEHZgwxA) | 20221105 | 56 | mixed | medium | How to Day Trade FOMC |
| 75 | [aOldFdtKsVc](https://www.youtube.com/watch?v=aOldFdtKsVc) | 20221109 | 41 | mixed | medium | How to Spot a Break of Structure in the Market |
| 76 | [lyXKaPy-1SU](https://www.youtube.com/watch?v=lyXKaPy-1SU) | 20221111 | 36 | mixed | medium | How to spot Equilibrium in the Market |
| 77 | [8IyR7pAvamE](https://www.youtube.com/watch?v=8IyR7pAvamE) | 20221124 | 30 | lesson | medium | How to Invest Correctly Using Price Action |
| 78 | [AUUZ9Vk6p5E](https://www.youtube.com/watch?v=AUUZ9Vk6p5E) | 20221212 | 40 | mixed | high | How to Spot Order Blocks in the Market |
| 79 | [w1tC9OUdkGs](https://www.youtube.com/watch?v=w1tC9OUdkGs) | 20221216 | 21 | mixed | medium | How to Read News Data and Apply it to the Market |
| 80 | [T-Bo-9GDi3s](https://www.youtube.com/watch?v=T-Bo-9GDi3s) | 20230116 | 55 | mixed | high | My Trading Strategy |
| 81 | [ogK04pUS2GM](https://www.youtube.com/watch?v=ogK04pUS2GM) | 20230126 | 16 | lesson | high | How to find Daily Bias in Trading |
| 82 | [_4-gzk18pQw](https://www.youtube.com/watch?v=_4-gzk18pQw) | 20230218 | 12 | lesson | medium | My Forex Strategy Explained |
| 83 | [HDxpo-Vj3JA](https://www.youtube.com/watch?v=HDxpo-Vj3JA) | 20230320 | 31 | lesson | high | The Strategy That Turned Me Profitable |
| 84 | [I0fLlm5s0yg](https://www.youtube.com/watch?v=I0fLlm5s0yg) | 20230331 | 22 | mixed | medium | Live Trading with Discord (How to take a Loss) |
| 85 | [Z9iXb9mBWgc](https://www.youtube.com/watch?v=Z9iXb9mBWgc) | 20230516 | 39 | lesson | high | My Forex Strategy Explained |
| 86 | [EAe5PUcZ99M](https://www.youtube.com/watch?v=EAe5PUcZ99M) | 20230812 | 10 | psychology | low | How to Start Trading With $100 |
| 87 | [0PRUVOrVVdg](https://www.youtube.com/watch?v=0PRUVOrVVdg) | 20230819 | 10 | psychology | medium | Is This the End for Smart Money Concepts? |
| 88 | [M6DQKMp-3Vo](https://www.youtube.com/watch?v=M6DQKMp-3Vo) | 20230905 | 53 | lesson | high | My "New" Day Trading Strategy Revealed |
| 89 | [6GNy02w2WIo](https://www.youtube.com/watch?v=6GNy02w2WIo) | 20231017 | 16 | psychology | medium | How to Trade with Millions of Dollars |
| 90 | [JNsC3HRfVhA](https://www.youtube.com/watch?v=JNsC3HRfVhA) | 20231123 | 20 | mixed | low | Banned Funded Account Strategy: How To Pass A Funded Account Every Time Pt. 1 |
| 91 | [YYuUgMjjec0](https://www.youtube.com/watch?v=YYuUgMjjec0) | 20231125 | 36 | mixed | low | Banned Funded Account Strategy: How To Pass A Funded Account Every Time Pt. 2 |
| 92 | [7zAy8xbzoNo](https://www.youtube.com/watch?v=7zAy8xbzoNo) | 20231127 | 21 | lesson | medium | How To Create Your Own Profitable Day Trading Strategy Pt.1 |
| 93 | [aKN0juZOCss](https://www.youtube.com/watch?v=aKN0juZOCss) | 20231128 | 4 | mixed | low | Banned Funded Account Strategy: How To Pass A Funded Account Every Time Pt. 3 |
| 94 | [zAWKsS6kw4Y](https://www.youtube.com/watch?v=zAWKsS6kw4Y) | 20231129 | 23 | lesson | medium | How To Create Your Own Profitable Day Trading Strategy Pt.2 |
| 95 | [q9stGbAb-_E](https://www.youtube.com/watch?v=q9stGbAb-_E) | 20231218 | 24 | mixed | low | Weekly Analysis |
| 96 | [YGSXw_B-UgM](https://www.youtube.com/watch?v=YGSXw_B-UgM) | 20240102 | 18 | mixed | medium | 01/02/2024 Daily Bias |
| 97 | [Uk8RiSde97w](https://www.youtube.com/watch?v=Uk8RiSde97w) | 20240103 | 12 | lesson | medium | 01/03/2024 Daily Bias |
| 98 | [vaz9BgwSoOE](https://www.youtube.com/watch?v=vaz9BgwSoOE) | 20240104 | 9 | lesson | medium | 01/04/2024 Daily Bias |
| 99 | [UvNYFPOQIfA](https://www.youtube.com/watch?v=UvNYFPOQIfA) | 20240105 | 8 | lesson | medium | 01/05/2024 Daily Bias |
| 100 | [BoLUAk7Z3C8](https://www.youtube.com/watch?v=BoLUAk7Z3C8) | 20240108 | 5 | lesson | medium | 01/08/2024 Daily Bias |
| 101 | [Da6MH3H81TM](https://www.youtube.com/watch?v=Da6MH3H81TM) | 20240110 | 6 | lesson | medium | 01/10/2024 Daily Bias |
| 102 | [jS6VORUrXfU](https://www.youtube.com/watch?v=jS6VORUrXfU) | 20240111 | 10 | lesson | medium | 01/11/2024 Daily Bias |
| 103 | [FdMf33jbUyM](https://www.youtube.com/watch?v=FdMf33jbUyM) | 20240112 | 25 | lesson | medium | 01/12/2024 Daily Bias |
| 104 | [Z-9HuHf5egU](https://www.youtube.com/watch?v=Z-9HuHf5egU) | 20240115 | 15 | lesson | medium | 01/15/2024 Daily Bias |
| 105 | [075G84Tx5OQ](https://www.youtube.com/watch?v=075G84Tx5OQ) | 20240116 | 5 | lesson | medium | 01/16/2024 Daily Bias |
| 106 | [Wev11XJtIiY](https://www.youtube.com/watch?v=Wev11XJtIiY) | 20240118 | 9 | lesson | medium | 01/18/2024 Daily Bias |
| 107 | [PIoJUvpG4uc](https://www.youtube.com/watch?v=PIoJUvpG4uc) | 20240119 | 5 | lesson | medium | 01/19/2024 Daily Bias |
| 108 | [bUzog1XUGKE](https://www.youtube.com/watch?v=bUzog1XUGKE) | 20240122 | 9 | lesson | medium | 01/22/2024 Daily Bias |
| 109 | [DcQ_tGB9D9E](https://www.youtube.com/watch?v=DcQ_tGB9D9E) | 20240123 | 6 | lesson | medium | 01/23/2024 Daily Bias |
| 110 | [THCqAkntnow](https://www.youtube.com/watch?v=THCqAkntnow) | 20240124 | 9 | lesson | medium | 01/24/2024 Daily Bias |
| 111 | [1qIZmrvs9ao](https://www.youtube.com/watch?v=1qIZmrvs9ao) | 20240125   # transcript header shows "?"; date inferred from title | 8 | lesson | medium | 01/25/2024 Daily Bias |
| 112 | [BUZrKRaYa3A](https://www.youtube.com/watch?v=BUZrKRaYa3A) | 20240129 | 8 | lesson | medium | 01/29/2024 Daily Bias |
| 113 | [hA9I8KsMC_U](https://www.youtube.com/watch?v=hA9I8KsMC_U) | 20240130 | 10 | lesson | high | 01/30/2024 Daily Bias |
| 114 | [ch9Hjb7jF40](https://www.youtube.com/watch?v=ch9Hjb7jF40) | 20240131 | 9 | lesson | medium | 01/31/2024 Daily Bias |
| 115 | [dy9jckID-pY](https://www.youtube.com/watch?v=dy9jckID-pY) | 20240201 | 6 | lesson | medium | 02/01/2024 Daily Bias |
| 116 | [X6-mKG2s4Q4](https://www.youtube.com/watch?v=X6-mKG2s4Q4) | 20240205 | 22 | recap | low | LIve Daily Bias 02/05/2024 |
| 117 | [G_N6bj11A9U](https://www.youtube.com/watch?v=G_N6bj11A9U) | 20240206 | 27 | recap | medium | LIve Daily Bias |
| 118 | [HlllJ9YH3Qw](https://www.youtube.com/watch?v=HlllJ9YH3Qw) | 20240207 | 72 | psychology | low | Trading Transformation Day 1: My Purpose |
| 119 | [TAHameI2DX8](https://www.youtube.com/watch?v=TAHameI2DX8) | 20240207 | 32 | recap | low | LIve Daily Bias |
| 120 | [X37Vg1wyk7E](https://www.youtube.com/watch?v=X37Vg1wyk7E) | 20240209 | 28 | psychology | low | Trading Transformation Day 3: How to be good at trading |
| 121 | [zZYmGcg9I_4](https://www.youtube.com/watch?v=zZYmGcg9I_4) | 20240209 | 23 | psychology | low | Trading Transformation Day 2: How to Learn a Skill (to trade) |
| 122 | [HsBtpgqQdZo](https://www.youtube.com/watch?v=HsBtpgqQdZo) | 20240211 | 21 | lesson | low | Trading Transformation Day 4: Candlesticks and Timeframes |
| 123 | [4LERkD7z_w4](https://www.youtube.com/watch?v=4LERkD7z_w4) | 20240213 | 13 | lesson | medium | Trading Transformation Day 6: Highs, Lows, and Trends |
| 124 | [wDH8IqakaQo](https://www.youtube.com/watch?v=wDH8IqakaQo) | 20240213 | 28 | psychology | low | Trading Transformation Day 5: Signals |
| 125 | [2Yjg-gqj33A](https://www.youtube.com/watch?v=2Yjg-gqj33A) | 20240214 | 30 | psychology | low | Trading Transformation Day 7: Trading Mindset Shift |
| 126 | [nR9Iikd6V2s](https://www.youtube.com/watch?v=nR9Iikd6V2s) | 20240219 | 13 | lesson | medium | Trading Transformation Day 8: Break of Structure |
| 127 | [vGxfICLK5QQ](https://www.youtube.com/watch?v=vGxfICLK5QQ) | 20240219 | 12 | psychology | low | Trading Transformation Day 9: Time |
| 128 | [5MJbi51w8tk](https://www.youtube.com/watch?v=5MJbi51w8tk) | 20240220 | 12 | lesson | low | Trading Transformation Day 10: Liquidity pt. 1 |
| 129 | [GJbC6nO3oHQ](https://www.youtube.com/watch?v=GJbC6nO3oHQ) | 20240224 | 19 | lesson | medium | Trading Transformation Day 11: Liquidity pt. 2 |
| 130 | [MSfIS6cv28A](https://www.youtube.com/watch?v=MSfIS6cv28A) | 20240226 | 8 | psychology | low | Trading Transformation Day 12: How to turn profitable |
| 131 | [rBsbMoNwIw4](https://www.youtube.com/watch?v=rBsbMoNwIw4) | 20240227 | 14 | lesson | medium | Trading Transformation Day 15: Order Blocks pt. 2 |
| 132 | [uRXKBX1kzwc](https://www.youtube.com/watch?v=uRXKBX1kzwc) | 20240227 | 8 | lesson | low | Trading Transformation Day 14: Order Blocks pt. 1 |
| 133 | [QI1ihQiH-F8](https://www.youtube.com/watch?v=QI1ihQiH-F8) | 20240301 | 13 | mixed | medium | Trading Transformation Day 16: How to Build a Strategy |
| 134 | [prRGeD527pE](https://www.youtube.com/watch?v=prRGeD527pE) | 20240302 | 9 | lesson | medium | Trading Transformation Day 17: Fair Value Gaps + Imbalances pt.1 |
| 135 | [h5uagl2C1IE](https://www.youtube.com/watch?v=h5uagl2C1IE) | 20240304 | 16 | lesson | medium | Trading Transformation Day 18: Fair Value Gaps + Imbalances pt.2 |
| 136 | [fl9ofZ4Rtb0](https://www.youtube.com/watch?v=fl9ofZ4Rtb0) | 20240307 | 9 | lesson | low | Trading Transformation Day 19: Equilibrium pt.1 |
| 137 | [vrGMaYeMJCg](https://www.youtube.com/watch?v=vrGMaYeMJCg) | 20240308 | 13 | lesson | medium | Trading Transformation Day 20: Equilibrium pt.2 |
| 138 | [YRU4hE19MVg](https://www.youtube.com/watch?v=YRU4hE19MVg) | 20240312 | 15 | lesson | medium | Trading Transformation Day 21: Breaker Blocks pt. 1 |
| 139 | [4XeIodHUtUQ](https://www.youtube.com/watch?v=4XeIodHUtUQ) | 20240314 | 12 | lesson | medium | Trading Transformation Day 22: Breaker Blocks pt. 2 |
| 140 | [67vLAkcdPu4](https://www.youtube.com/watch?v=67vLAkcdPu4) | 20240316 | 25 | lesson | high | Trading Transformation Day 23: Strategy Creation pt.1 |
| 141 | [OvmbAxG15YE](https://www.youtube.com/watch?v=OvmbAxG15YE) | 20240317 | 30 | lesson | high | Trading Transformation Day 24: Strategy Creation pt.2 |
| 142 | [TBU7yfJzwrY](https://www.youtube.com/watch?v=TBU7yfJzwrY) | 20240323 | 12 | lesson | medium | Trading Transformation Day 25: Strategy Creation pt.3 |
| 143 | [-Ei4GP5mp60](https://www.youtube.com/watch?v=-Ei4GP5mp60) | 20240324 | 16 | lesson | medium | Trading Transformation Day 26: Stop Losses |
| 144 | [_H9Gk8U7_VU](https://www.youtube.com/watch?v=_H9Gk8U7_VU) | 20240402 | 14 | lesson | high | Trading Transformation Day 27: Take Profits |
| 145 | [zELK1pm8pF8](https://www.youtube.com/watch?v=zELK1pm8pF8) | 20240403 | 14 | lesson | high | Trading Transformation Day 28: Strategy Creation pt.4 |
| 146 | [yp1HQ7gbgYU](https://www.youtube.com/watch?v=yp1HQ7gbgYU) | 20240414 | 17 | lesson | high | Trading Transformation Day 29: Strategy Creation pt.5 |
| 147 | [MNA9gtZCVqM](https://www.youtube.com/watch?v=MNA9gtZCVqM) | 20240415 | 27 | psychology | low | Trading Transformation Day 30: How to Turn Profitable with Information |
| 148 | [3boJd1-Dupk](https://www.youtube.com/watch?v=3boJd1-Dupk) | 20240417 | 15 | lesson | medium | Trading Transformation Day 31: Forex Strategy Creation pt.1 |
| 149 | [spBeqjQViq0](https://www.youtube.com/watch?v=spBeqjQViq0) | 20240425 | 43 | lesson | medium | Trading Transformation Day 32: Forex Strategy Explained |
| 150 | [rMkghkG-ZjE](https://www.youtube.com/watch?v=rMkghkG-ZjE) | 20240506 | 23 | lesson | high | Trading Transformation Day 33: Inverse FVGs |
| 151 | [i3FU-9OUU90](https://www.youtube.com/watch?v=i3FU-9OUU90) | 20240512 | 24 | lesson | high | Trading Transformation Day 34: How to Trade Pm Session |
| 152 | [r-7-gWZsnZc](https://www.youtube.com/watch?v=r-7-gWZsnZc) | 20240514 | 22 | lesson | medium | Trading Transformation Day 35: Best Time to Trade |
| 153 | [60H1AumgjG8](https://www.youtube.com/watch?v=60H1AumgjG8) | 20240517 | 14 | lesson | medium | Trading Transformation Day 36: How to Trade on Multiple Timeframes |
| 154 | [3svETDwdFUU](https://www.youtube.com/watch?v=3svETDwdFUU) | 20240522 | 22 | lesson | high | Trading Transformation Day 37: SMT Divergence |
| 155 | [qswlc-I-DuA](https://www.youtube.com/watch?v=qswlc-I-DuA) | 20240620 | 15 | lesson | medium | The Only Fair Value Gap Video You Need. |
| 156 | [Ias0HhHUqj4](https://www.youtube.com/watch?v=Ias0HhHUqj4) | 20240704 | 6 | recap | high | This Boring ICT Strategy Made Me $6,000 In Under An Hour |
| 157 | [BOx7Lk8Xs3o](https://www.youtube.com/watch?v=BOx7Lk8Xs3o) | 20240712 | 26 | lesson | high | Copy This Day Trading Strategy To Turn Profitable |
| 158 | [Qk-mHUlSJGU](https://www.youtube.com/watch?v=Qk-mHUlSJGU) | 20240717 | 17 | lesson | high | How to Find Daily Bias (Updated 2026) |
| 159 | [v3c6A-Vs1Oc](https://www.youtube.com/watch?v=v3c6A-Vs1Oc) | 20240722 | 18 | lesson | high | This Trading Confluence will Instantly Increase Your Win Rate |
| 160 | [TihRnXjqM5c](https://www.youtube.com/watch?v=TihRnXjqM5c) | 20240728 | 18 | lesson | medium | Trading Transformation Day 38: BPR |
| 161 | [d5uOjnuzYhE](https://www.youtube.com/watch?v=d5uOjnuzYhE) | 20240729 | 16 | lesson | high | DO NOT Trade Without This Confluence (SMT Divergence) |
| 162 | [0RT_nPp1w3M](https://www.youtube.com/watch?v=0RT_nPp1w3M) | 20240801 | 15 | psychology | low | 16 Minutes of The Best Trading Advice |
| 163 | [xgaep2fI6-Q](https://www.youtube.com/watch?v=xgaep2fI6-Q) | 20240809 | 7 | psychology | low | How To Start Day Trading With Only $100 |
| 164 | [z1STKCnivbM](https://www.youtube.com/watch?v=z1STKCnivbM) | 20240829 | 17 | lesson | low | The ONLY Candlestick Video You’ll EVER Need (Step By Step Guide) |
| 165 | [p5CKu0FNbyg](https://www.youtube.com/watch?v=p5CKu0FNbyg) | 20240903 | 39 | lesson | high | My Day Trading Strategy Explained (Step By Step) |
| 166 | [L13OfAXg8ck](https://www.youtube.com/watch?v=L13OfAXg8ck) | 20241014 | 30 | lesson | low | How To Start Day Trading In 2026 (Step by Step) |
| 167 | [AMlev-gYyHo](https://www.youtube.com/watch?v=AMlev-gYyHo) | 20241104 | 35 | lesson | high | Liquidity Sweeps Explained |
| 168 | [n97MKj6wGFk](https://www.youtube.com/watch?v=n97MKj6wGFk) | 20241119 | 23 | lesson | high | Break of Structure Explained |
| 169 | [oQSL21VryP4](https://www.youtube.com/watch?v=oQSL21VryP4) | 20250101 | 28 | psychology | low | Brutally Honest Advice To My Younger Broke Self |
| 170 | [xE6m4UvuT5s](https://www.youtube.com/watch?v=xE6m4UvuT5s) | 20250116 | 12 | recap | high | Live Day Trading Making $21,415 (I FULLPORTED MY ACCOUNT FOR THIS) |
| 171 | [xcDOMKaOIsk](https://www.youtube.com/watch?v=xcDOMKaOIsk) | 20250203 | 47 | lesson | high | Fair Value Gaps Explained |
| 172 | [-RAJEWMl-F0](https://www.youtube.com/watch?v=-RAJEWMl-F0) | 20250204 | 11 | recap | high | Live Day Trading Making $16,320 (HOW TO GET SNIPER ENTRIES) |
| 173 | [NZqRbc_9u_I](https://www.youtube.com/watch?v=NZqRbc_9u_I) | 20250212 | 30 | psychology | low | How To Start Day Trading With $0 |
| 174 | [z0czA_OSq5M](https://www.youtube.com/watch?v=z0czA_OSq5M) | 20250220 | 32 | lesson | high | Order Flow Explained |
| 175 | [vSduJn-l52A](https://www.youtube.com/watch?v=vSduJn-l52A) | 20250303 | 12 | recap | medium | Live Day Trading Making $15,474 (HOW TO PASS A FUNDED ACCOUNT) |
| 176 | [SHJHpedYh6A](https://www.youtube.com/watch?v=SHJHpedYh6A) | 20250307 | 315 | lesson | high | Beginners Guide To Start Day Trading In 2026 (5 hours) |
| 177 | [a5PLl1uM7CQ](https://www.youtube.com/watch?v=a5PLl1uM7CQ) | 20250318 | 49 | mixed | medium | Day Trading For Beginners: The Complete Starter Guide 2025 |
| 178 | [WlnpOPPnBQw](https://www.youtube.com/watch?v=WlnpOPPnBQw) | 20250320 | 11 | recap | high | Live Day Trading Making $4,735 (HOW TO SCALP TRADE) |
| 179 | [CPPREA-6ubY](https://www.youtube.com/watch?v=CPPREA-6ubY) | 20250414 | 28 | lesson | medium | This Simple Strategy Made Me My First $100k |
| 180 | [J1vPj1m6crQ](https://www.youtube.com/watch?v=J1vPj1m6crQ) | 20250430 | 56 | live_trading | high | Live Day Trading Making $31,085 (HOW TO FIND AGGRESSIVE ENTRIES) |
| 181 | [A3RNBK_7gcM](https://www.youtube.com/watch?v=A3RNBK_7gcM) | 20250506 | 62 | live_trading | high | Live Day Trading Making $78,795 (MY SCALPING STRATEGY EXPLAINED) |
| 182 | [tT3lUnwayb0](https://www.youtube.com/watch?v=tT3lUnwayb0) | 20250512 | 48 | mixed | medium | Beginners Guide To Get Funded In 2026 |
| 183 | [iVOjRDrjFM4](https://www.youtube.com/watch?v=iVOjRDrjFM4) | 20250521 | 83 | live_trading | medium | Live Day Trading Losing $3,650 (HOW TO KEEP LOSSES SMALL) |
| 184 | [mV3YFmtnRdo](https://www.youtube.com/watch?v=mV3YFmtnRdo) | 20250521 | 98 | live_trading | medium | Live Day Trading Making $18,541 (HOW TO MAKE WINS BIGGER THAN LOSSES) |
| 185 | [ssPMxVk6B9Y](https://www.youtube.com/watch?v=ssPMxVk6B9Y) | 20250522 | 8 | mixed | low | Live Day Trading Making $0 (HOW TO TRADE CHOPPY PRICE ACTION) |
| 186 | [KxBRLErkel0](https://www.youtube.com/watch?v=KxBRLErkel0) | 20250526 | 35 | lesson | high | The Science Based Trading Strategy That Made Me $291,456 This Month |
| 187 | [e_FV0Q14k8E](https://www.youtube.com/watch?v=e_FV0Q14k8E) | 20250630 | 27 | lesson | high | How To Find Daily Bias (Step By Step) |
| 188 | [VTwmHVAX29o](https://www.youtube.com/watch?v=VTwmHVAX29o) | 20250723 | 26 | psychology | low | 7 Trading Rules That Changed My Life |
| 189 | [IVqY3b-KEbA](https://www.youtube.com/watch?v=IVqY3b-KEbA) | 20250731 | 53 | live_trading | high | Live Day Trading Making $40,030 (HOW TO WIN LOW TIMEFRAME TRADES) |
| 190 | [tWYSAHQpywE](https://www.youtube.com/watch?v=tWYSAHQpywE) | 20250825 | 47 | live_trading | medium | Live Day Trading Losing $4,100 (HOW TO MITIGATE LOSSES) |
| 191 | [cXlVBiwIlbI](https://www.youtube.com/watch?v=cXlVBiwIlbI) | 20250904 | 19 | psychology | low | Brutally Honest Advice To My Younger Unprofitable Self |
| 192 | [2ZArg3kPPkE](https://www.youtube.com/watch?v=2ZArg3kPPkE) | 20250911 | 61 | live_trading | medium | Live Day Trading Losing $1,953 (1 WIN & 1 LOSS BREAKEVEN DAY PPI NEWS DATA) |
| 193 | [BMyeYQIj_vU](https://www.youtube.com/watch?v=BMyeYQIj_vU) | 20250917 | 33 | lesson | high | The Stupid Simple Strategy That Makes Me $156,943/Month (Backtested Results) |
| 194 | [egQLtQLmauk](https://www.youtube.com/watch?v=egQLtQLmauk) | 20250917   # inferred: catalog date missing; catalog neighbours ~2025-09-17 and the Sep-2025 FOMC 25bp cut fits the content | 14 | recap | medium | How I Made $427,390 In One Day Trading FOMC! |
| 195 | [aobHuNcI1QM](https://www.youtube.com/watch?v=aobHuNcI1QM) | 20250925 | 543 | mixed | high | How To Start Day Trading As A Beginner In 2026 (9 hours) |
| 196 | [jeewXSLHt2g](https://www.youtube.com/watch?v=jeewXSLHt2g) | 20251001 | 17 | lesson | medium | The ONLY Break Of Structure Video You’ll Ever Need |
| 197 | [8QDDxwUV1KM](https://www.youtube.com/watch?v=8QDDxwUV1KM) | 20251006 | 51 | lesson | high | How I Made $1,047,984 In 6 Months Of Day Trading (Strategy Revealed) |
| 198 | [5RWTzr1D994](https://www.youtube.com/watch?v=5RWTzr1D994) | 20251007 | 61 | live_trading | high | Live Day Trading Making $45,180 (HOW TO HIT FULL TAKE PROFITS) |
| 199 | [YfS5yBQgubI](https://www.youtube.com/watch?v=YfS5yBQgubI) | 20251008 | 68 | live_trading | high | Live Day Trading Making $35,827 (HOW TO TAKE CONTINUATION TRADES) |
| 200 | [rBdlDQgSjIc](https://www.youtube.com/watch?v=rBdlDQgSjIc) | 20251009 | 63 | live_trading | high | Live Day Trading Losing $52,660 (MADE DUMB MISTAKES) |
| 201 | [xxJyvmHROb4](https://www.youtube.com/watch?v=xxJyvmHROb4) | 20251015 | 40 | live_trading | medium | Live Day Trading Losing $152,060 (I MARRIED MY BIAS) |
| 202 | [7a8tAGkVJac](https://www.youtube.com/watch?v=7a8tAGkVJac) | 20251030 | 26 | recap | high | Live Day Trading Making $401,280 (I FULLPORTED FOMC) |
| 203 | [xRuMUvW3T7Q](https://www.youtube.com/watch?v=xRuMUvW3T7Q) | 20251104 | 33 | lesson | high | This Data-Backed Strategy Works Everyday (Stupid Simple And Proven) |
| 204 | [-zyDnjozaMM](https://www.youtube.com/watch?v=-zyDnjozaMM) | 20251126 | 28 | psychology | low | 6 Years of Brutally Honest Trading Lessons For 2026 |
| 205 | [pKIo-aVic-c](https://www.youtube.com/watch?v=pKIo-aVic-c) | 20251203 | 24 | lesson | medium | Liquidity Is The Easiest Way To Become Profitable FAST |
| 206 | [g27VsJS3a58](https://www.youtube.com/watch?v=g27VsJS3a58) | 20251209 | 69 | live_trading | medium | Live Day Trading Losing $14,646 (I TOOK A TRADE OFF THE WRONG TIMEFRAME) |
| 207 | [3GZgBBMzC_E](https://www.youtube.com/watch?v=3GZgBBMzC_E) | 20260101 | 39 | psychology | low | Path to Profitability: One Day or Day One |
| 208 | [R62RnJrKH3Q](https://www.youtube.com/watch?v=R62RnJrKH3Q) | 20260102 | 22 | psychology | low | Path to Profitability: What is Trading |
| 209 | [8qwEmE1DwYw](https://www.youtube.com/watch?v=8qwEmE1DwYw) | 20260103 | 41 | lesson | medium | Path to Profitability: How to Read a Candlestick Chart |
| 210 | [crMqxB_nHhk](https://www.youtube.com/watch?v=crMqxB_nHhk) | 20260104 | 35 | lesson | high | Path to Profitability: Liquidity Explained |
| 211 | [AGmAVyAuBE0](https://www.youtube.com/watch?v=AGmAVyAuBE0) | 20260105 | 53 | lesson | high | Advanced Liquidity Concepts (Path to Profitability) |
| 212 | [QRoLG0QRiNM](https://www.youtube.com/watch?v=QRoLG0QRiNM) | 20260106 | 44 | live_trading | medium | Live Day Trading Making $25,400 (HOW TO TAKE PM SESSION TRADES) |
| 213 | [Zzk864cVJek](https://www.youtube.com/watch?v=Zzk864cVJek) | 20260106 | 12 | lesson | high | Path to Profitability: Break of Structure Explained |
| 214 | [ZioWcbxSuIw](https://www.youtube.com/watch?v=ZioWcbxSuIw) | 20260107 | 13 | live_trading | medium | Live Day Trading Making $42,510 (HOW TO SCALP ON THE 1 MINUTE) |
| 215 | [xX5LTSJ5wwM](https://www.youtube.com/watch?v=xX5LTSJ5wwM) | 20260107 | 33 | lesson | high | Path to Profitability: Fair Value Gaps Explained |
| 216 | [MiaTd3hh47I](https://www.youtube.com/watch?v=MiaTd3hh47I) | 20260108 | 63 | live_trading | medium | Live Day Trading Losing $97,421 (I AM DOWN 122K THIS WEEK) |
| 217 | [PlsHO33j6B8](https://www.youtube.com/watch?v=PlsHO33j6B8) | 20260108 | 23 | lesson | medium | Path to Profitability: Advanced Imbalance Concepts |
| 218 | [4sRDnVmLcMk](https://www.youtube.com/watch?v=4sRDnVmLcMk) | 20260109 | 22 | lesson | high | Path to Profitability: Inverse Fair Value Gaps Explained |
| 219 | [joe_XTCn5Bs](https://www.youtube.com/watch?v=joe_XTCn5Bs) | 20260110 | 14 | lesson | high | Path to Profitability: Equilibrium Explained |
| 220 | [7dTQA0t8SH0](https://www.youtube.com/watch?v=7dTQA0t8SH0) | 20260111 | 16 | lesson | high | Path to Profitability: SMT Divergence Explained |
| 221 | [L4xz2o23aPQ](https://www.youtube.com/watch?v=L4xz2o23aPQ) | 20260112 | 11 | lesson | high | Path to Profitability: Time Theory Explained |
| 222 | [52nxvJKM57U](https://www.youtube.com/watch?v=52nxvJKM57U) | 20260113 | 19 | lesson | low | Path to Profitability: Funded Accounts Explained |
| 223 | [ironJFzNBic](https://www.youtube.com/watch?v=ironJFzNBic) | 20260114 | 30 | lesson | high | Path to Profitability: How To Find Daily Bias |
| 224 | [vIjIitndRXQ](https://www.youtube.com/watch?v=vIjIitndRXQ) | 20260114 | 34 | live_trading | medium | Live Day Trading Making $67,680 (I FULLPORTED NEWS) |
| 225 | [hBnD6T1M4w8](https://www.youtube.com/watch?v=hBnD6T1M4w8) | 20260116 | 18 | psychology | medium | Path to Profitability: Risk Management & Psychology |
| 226 | [TEp3a-7GUds](https://www.youtube.com/watch?v=TEp3a-7GUds) | 20260117 | 43 | mixed | high | Path to Profitability: TJR's Strategy Explained |
| 227 | [kaPlPoXGXKw](https://www.youtube.com/watch?v=kaPlPoXGXKw) | 20260121 | 75 | live_trading | low | Live Day Trading Making $88,322 (HOW TO TAKE CONTINUATION TRADES) |
| 228 | [c5f6hLzchyM](https://www.youtube.com/watch?v=c5f6hLzchyM) | 20260122 | 129 | live_trading | medium | Live Day Trading Making $14,300 (MADE ALL MY MONEY BACK) |
| 229 | [gKOQbcg0r1M](https://www.youtube.com/watch?v=gKOQbcg0r1M) | 20260127 | 42 | live_trading | medium | Live Day Trading Making $49,930 (I MADE BACK ALL MY LOSSES) |
| 230 | [wzq2AMsoJKY](https://www.youtube.com/watch?v=wzq2AMsoJKY) | 20260203 | 18 | lesson | high | The ONLY Equilibrium Video You’ll Ever Need |
| 231 | [9ar85Y6-5P4](https://www.youtube.com/watch?v=9ar85Y6-5P4) | 20260302 | 41 | mixed | medium | Live Day Trading Losing $6,000 (HE BLEW 3 ACCOUNTS) |
| 232 | [BdBxXKGWVjk](https://www.youtube.com/watch?v=BdBxXKGWVjk) | 20260302 | 15 | lesson | high | This Simple Concept Made Me +$1,000,000 (Full Breakdown) |
| 233 | [X8Ag7BWd9dg](https://www.youtube.com/watch?v=X8Ag7BWd9dg) | 20260310 | 38 | mixed | high | Live Day Trading Making $139,000 (UP $624K THIS MONTH) |
| 234 | [4KzkQEM28tc](https://www.youtube.com/watch?v=4KzkQEM28tc) | 20260312 | 25 | live_trading | medium | Live Day Trading - FULL PORTING CPI |
| 235 | [3qqRo-Qo280](https://www.youtube.com/watch?v=3qqRo-Qo280) | 20260319 | 22 | live_trading | low | Live Day Trading (SMOKED BY THE CHARTS) |
| 236 | [L6TVpyi1eyE](https://www.youtube.com/watch?v=L6TVpyi1eyE) | 20260321 | 34 | live_trading | low | Live Day Trading $75,390 (BACK IN THE GREEN) |
| 237 | [LLWBdwtpbiI](https://www.youtube.com/watch?v=LLWBdwtpbiI) | 20260327 | 31 | live_trading | high | Live Day Trading Making $0 (NO TRADES TAKEN) |
| 238 | [kH-rbepWkNE](https://www.youtube.com/watch?v=kH-rbepWkNE) | 20260406 | 42 | live_trading | high | How I Pulled $60,630 From One Setup |
| 239 | [OJXkE2h2mz4](https://www.youtube.com/watch?v=OJXkE2h2mz4) | 20260407 | 43 | live_trading | medium | The Only Setup That Mattered Today ($103K) |
| 240 | [-mJ8mww-Flw](https://www.youtube.com/watch?v=-mJ8mww-Flw) | 20260416 | 50 | live_trading | medium | How I Turned One Setup Into $48,305 Live on Stream |
| 241 | [3SygD-YgZuQ](https://www.youtube.com/watch?v=3SygD-YgZuQ) | 20260417 | 100 | live_trading | high | $75,210 in One Day Trading Live (Full Breakdown) |
| 242 | [L5eRg5BZOOY](https://www.youtube.com/watch?v=L5eRg5BZOOY) | 20260421 | 108 | live_trading | medium | Live Day Trading Making $88,300 (I GOT EXPOSED FOR FAKING TRADES) |
| 243 | [C5zIaZzbbgM](https://www.youtube.com/watch?v=C5zIaZzbbgM) | 20260427 | 73 | live_trading | low | Live Day Trading Losing $20,160 (3 DAY LOSSING STREAK) |
| 244 | [b_ksEb6cJ50](https://www.youtube.com/watch?v=b_ksEb6cJ50) | 20260507 | 74 | live_trading | low | Live Day Trading Making $16,770 (PROVING EVERYONE WRONG) |
| 245 | [yiuFUp0kFz8](https://www.youtube.com/watch?v=yiuFUp0kFz8) | 20260507 | 400 | lesson | high | How To Start Day Trading In 2026 [Full Tutorial] |
| 246 | [_zzxRMbyE44](https://www.youtube.com/watch?v=_zzxRMbyE44) | 20260512 | 52 | live_trading | medium | Live Day Trading Making $19,620(I FULLPORTED CPI) |
| 247 | [8PYgFVB0GHE](https://www.youtube.com/watch?v=8PYgFVB0GHE) | 20260605 | 58 | mixed | high | My UPDATED Day Trading Strategy (2026) |
| 248 | [eEg0_zc8Hxg](https://www.youtube.com/watch?v=eEg0_zc8Hxg) | 20260706 | 55 | lesson | low | How To Use TradingView For BEGINNERS In 2026 (Full Guide) |
| 249 | [88tyzO9CxGA](https://www.youtube.com/watch?v=88tyzO9CxGA) | 20260713 | 37 | psychology | low | 9 Years of Trading Psychology in 37 Minutes |
| 250 | [Vulini8xbB0](https://www.youtube.com/watch?v=Vulini8xbB0) | 20260721 | 49 | lesson | high | The ONLY Liquidity Guide You’ll Ever Need |
| 251 | [akkPDEAm1jw](https://www.youtube.com/watch?v=akkPDEAm1jw) | 20260727 | 35 | lesson | medium | Beginners Guide To Pass A Prop Firm In 2026 |
| 252 | [EMSTUOAtCo0](https://www.youtube.com/watch?v=EMSTUOAtCo0) | 20260807 | 10 | psychology | low | 7 Years of Trading Advice in 10 Minutes |
| 253 | [VhRZ5-JjlTQ](https://www.youtube.com/watch?v=VhRZ5-JjlTQ) | 20260818 | 31 | lesson | low | How To Start Day Trading With Only $100 |
| 254 | [Xdu6j2E1DEI](https://www.youtube.com/watch?v=Xdu6j2E1DEI) | 20261002 | 22 | lesson | medium | Once You Learn Price Action, Trading Becomes Embarrassingly Simple |
| 255 | [FBX-gtFGWyU](https://www.youtube.com/watch?v=FBX-gtFGWyU) | 20261007 | 19 | mixed | high | How To Find Daily Bias (Step By Step) |
| 256 | [TYbpk7WogHI](https://www.youtube.com/watch?v=TYbpk7WogHI) | 20261012 | 18 | lesson | high | Learn Every Trading Confluence In 18 Minutes |
| 257 | [_Fkofoggjv4](https://www.youtube.com/watch?v=_Fkofoggjv4) | unknown   # not in catalog/dates.tsv; catalog order places it ~Jun 2025 (inferred, between 20250526 and later 2025 uploads) | 49 | lesson | high | The ONLY Liquidity Sweeps Video You’ll Ever Need |
| 258 | [vlnNPFu4rEQ](https://www.youtube.com/watch?v=vlnNPFu4rEQ) | unknown   # not in metadata; "6 years of trading" suggests ~late 2025 (inferred, cf. -zyDnjozaMM 20251126) | 14 | psychology | low | 6 Rules I've Learned From 6 Years of Trading |
| 259 | [0RBTSUGKA0w](https://www.youtube.com/watch?v=0RBTSUGKA0w) | unknown (2026, inferred; a Friday in the first week of a month) | 101 | live_trading | medium | Live Day Trading Losing $52,660 (MY STUDENTS ARE BETTER THAN ME) |
| 260 | [MzJK2-NDOhk](https://www.youtube.com/watch?v=MzJK2-NDOhk) | unknown (inferred ~late March 2025: "nearing the end of the first quarter" [06:48]) | 7 | recap | medium | Live Day Trading Making $7,370 (HOW TO FIND DAILY BIAS) |

