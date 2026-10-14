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
