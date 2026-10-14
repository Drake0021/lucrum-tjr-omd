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
