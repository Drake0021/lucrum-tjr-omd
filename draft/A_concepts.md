# OMD Part A: Concepts (Sections 1, 2, 3, 4, 6, 7)

Conventions used in this part
- Citations: `[video_id@mm:ss]` (or `h:mm:ss` for long videos); several in one bracket are separated by `;`. A range `@a–b` cites a span.
- Eras (binding, from CANONICAL): **E1** pre-Boot Camp (2022–mid 2023) · **E2** Boot Camp 1 & 2.0 (Jun–Oct 2023) · **E3** Sep 2023–2024 (Sep 2023 strategy video, Jan 2024 daily-bias videos, Trading Transformation "TT") · **E4** 2025 · **E5** 2026 = **CANONICAL**. Where eras disagree, E5 is the rule; older behaviour is recorded as history.
- `(inferred)` = our inference, not TJR's words. `DEFAULT (not TJR-stated)` = a bot parameter we chose because TJR is vague; every one of these must be listed in the ambiguity register and be configurable.
- Times are New York (ET). Instruments: the bot trades **ES/MES**; **NQ** is a required correlation feed (SMT, alignment, confirmation).
- "Close" always means the candle **body close** of a **completed** candle on the stated timeframe. Wicks never confirm anything. A close **equal** to a level is not beyond it.
- Tick size ES/MES = 0.25 pt (exchange spec, not TJR).

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
