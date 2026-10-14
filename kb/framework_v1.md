# TJR Day-Trading Model: Base Framework v1 (Boot Camp 1 + Boot Camp 2.0)

Purpose: the backbone of the OMD (master document) that teaches an ES/MES futures bot to replicate TJR (@TJRTrades). Built only from the structured notes in `notes/<video_id>.md` for the 69 Boot Camp videos that have notes. (Day 48 part 1, `OQIs8I2jMgs`, has no audio and no notes; Day 48 Pt. 2, `4FEty6xgOc0`, covers it.)

Conventions
- Citations: `[video_id@mm:ss]`. Several citations in one bracket are separated by `;`. A range like `@05:05–06:44` cites a span of the notes.
- "BC1" = Boot Camp Days 1–55 (May 26 – Jul 25, 2023). "BC2" = Boot Camp 2.0 Days 1–13 (Aug 24 – Sep 12, 2023). Where they differ, **BC2 supersedes BC1**.
- `(inferred)` = my inference, not TJR's statement. `(vague)` = TJR left it unspecified. Text marked "OPEN" also appears in §12.
- Instruments in the source: ES/SPX/"S&P" (traded as a CFD on MT4/MT5 in this period, sized in "lots"), GU = GBPUSD, GJ = GBPJPY, gold = XAUUSD, EU = EURUSD. For the bot, rules stated on forex pairs are evidence of the general model unless they are flagged as **Forex strategy** (a separate session-level playbook, §4.F).
- Times are New York (ET) unless stated. The NYSE cash open is 9:30 ET (he shows it as 14:30 on a UTC chart [OH--4nkbXlM@02:23]).

## Source key (course order → video_id)

| # | Day | video_id | Topic | | # | Day | video_id | Topic |
|---|---|---|---|---|---|---|---|---|
| 1 | BC1 D1 | Xq6-oO2n6-U | Take action | | 36 | D36 | Y1lqifylC4s | Daily bias 3 |
| 2 | D2 | bEkbNGUzQME | Candlesticks | | 37 | D37 | FjSiLFrg5fo | Taking profits |
| 3 | D3 | w2CWF0WtLmQ | Discipline | | 38 | D38 | 1FunNCUw_jM | Stop losses |
| 4 | D4 | viuGHEuv0nw | Trends | | 39 | D39 | KSiWKfPOlh4 | Lot size |
| 5 | D5 | N7so8LEHmLA | Goal setting | | 40 | D40 | O_4yHzZO0u0 | Check-in |
| 6 | D6 | PmhuPbY8ZHo | Break of structure | | 41 | D41 | PyCPHiO2nj0 | Learn from losses |
| 7 | D7 | _6voYEdi5j4 | Individuality | | 42 | D42 | NPG_BZ_83fo | Backtesting |
| 8 | D8 | Lxnu7InGhGE | Liquidity 1 | | 43 | D43 | 9SUJfAo6Sl8 | Weekly analysis |
| 9 | D9 | -ga9oK2bClQ | Check-in | | 44 | D44 | uGi6EeKnWSk | Try not to trade |
| 10 | D10 | rdz6vnXb8wE | Liquidity 2 | | 45 | D45 | LG_IbfjbaOo | Over-complicating |
| 11 | D11 | _jLR3XcB5eQ | Taking a loss | | 46 | D46 | CZRs2NuLQIw | Journaling |
| 12 | D12 | KtC2SbemF6w | Liquidity 3 | | 47 | D47 | S-scwzKRP-8 | Backtesting CPI |
| 13 | D13 | RkMBoqbeUq8 | Risk management | | 49 | D48 pt2 | 4FEty6xgOc0 | Live bias on PPI |
| 14 | D14 | d0AxLACYaqU | FVG 1 | | 50 | D49 | __fKQR5RR08 | Bias + $9k loss |
| 15 | D15 | T4xVS7iV5d8 | Identifying problems | | 51 | D50 | QRvZgj3k8pk | Weekly analysis |
| 16 | D16 | S1kY3Fw6JUQ | FVG 2 | | 52 | D51 | XcA0GiWZp7M | Sunday motivation |
| 17 | D17 | 339amTioakE | Patience | | 53 | D52 | -rYGugTIsbU | Bias + BE recap |
| 18 | D18 | qecF411R83s | FVG 3 | | 54 | D53 | Oi_mK1Lt-iQ | Bias + GJ recap |
| 19 | D19 | w5sUCqFH3Lg | News data | | 55 | D54 | 9sD9kTia4V4 | Bias, no trades |
| 20 | D20 | qhuFg_OXdmE | Order blocks 1 | | 56 | D55 | IFgysr8gDjc | The end |
| 21 | D21 | z9p7OThLkr4 | Taking a win | | 57 | BC2 D1 | o_SdawM3DIE | BC2 launch |
| 22 | D22 | RQSVIKddFHI | Order blocks 2 | | 58 | BC2 D2 | OH--4nkbXlM | Emotions |
| 23 | D23 | ERbhCL9KW_g | Check-in | | 59 | BC2 D3 | G7eq6U8e3yw | Risk |
| 24 | D24 | 12_F-mIUfL0 | Order blocks 3 | | 60 | BC2 D4 | 4aYaeI2Av2I | Broker |
| 25 | D25 | 4moWbfm6smw | Overconfidence | | 61 | BC2 D5 | IY9NJbaNyqA | Trade bias |
| 26 | D26 | j1pVK897oZQ | Equilibrium 1 | | 62 | BC2 D5.5 | Iu_v4kuFQhk | Second trade |
| 27 | D27 | TwakmPZJGJA | Fear | | 63 | BC2 D6 | oJq8egtzCto | Best loss |
| 28 | D28 | -E7plUbSJUk | Equilibrium 2 | | 64 | BC2 D7 | 7MBD3ow7I1g | Risk & probabilities |
| 29 | D29 | 065lMUrD_kg | Trading plan | | 65 | BC2 D8 | 5v4G4xJVKIQ | Splitting positions |
| 30 | D30 | ESsy0uoFAz4 | Execution 1 | | 66 | BC2 D9 | ss-dZPMnjeY | Leveraging risk |
| 31 | D31 | isetVuqlSLo | Hard work | | 67 | BC2 D10 | r-DdsJLUlBk | Trade recaps |
| 32 | D32 | SLhIA7vW9x8 | Execution 2 | | 68 | BC2 D11 | 6zXKK3Wrusg | Where to take profit |
| 33 | D33 | K8DwhtmvAW8 | Execution 3 | | 69 | BC2 D12 | SV37R6j5f4M | Red day |
| 34 | D34 | sjuWqKDsQtI | Daily bias 1 | | 70 | BC2 D13 | 7Q3nalPsSpk | Made $ on a bad trade |
| 35 | D35 | UPA9LQW7phk | Daily bias 2 | | | | | |

---

## 1. Overview

**The model in one paragraph.** TJR trades with the higher-timeframe trend, defined purely by candle-close market structure. "Higher time frames hold higher power" [viuGHEuv0nw@08:19; Y1lqifylC4s@07:47; uGi6EeKnWSk@12:00]. He sets a top-down bias: the monthly and weekly give context, the **daily market structure is the intraday bias**, and the 4H and 1H must at least not contradict it [sjuWqKDsQtI@01:43; __fKQR5RR08@04:03; 4FEty6xgOc0@08:47]. He marks the higher-timeframe "building blocks" a with-trend trade would come from: liquidity, order blocks / areas of accumulation, fair value gaps and equilibrium (premium/discount). Then he waits for price to retrace into one of them during the New York session [sjuWqKDsQtI@12:06; r-DdsJLUlBk@01:40; 9sD9kTia4V4@03:56]. Inside that zone he drops to the 5m/1m. There he needs a **liquidity sweep**, then a **break of structure / change of trend** (a candle body closing beyond a prominent swing), then a **third confirmation**: a retrace into the new 5m FVG, equilibrium or order block that produces a reaction, or a 1m BOS [ss-dZPMnjeY@06:46; SV37R6j5f4M@05:36; 5v4G4xJVKIQ@03:22]. The stop goes beyond the invalidation point, which is the swept extreme plus a buffer [1FunNCUw_jM@01:08; ss-dZPMnjeY@05:06]. The first take-profit is about 1:1 at the nearest draw on liquidity: close 50% there and move the stop to breakeven. Later targets sit at higher-timeframe building blocks [7MBD3ow7I1g@02:16; Iu_v4kuFQhk@01:39; 6zXKK3Wrusg@05:25]. Risk is about 1% normal, sized down by news and confidence. The daily risk budget is split across at most about 2 ideas. He trades within the first ~90 minutes after the 9:30 ET open and skips CPI, PPI, FOMC and NFP days [065lMUrD_kg@10:47; w5sUCqFH3Lg@06:49; 7MBD3ow7I1g@04:29; 5v4G4xJVKIQ@10:03]. He sums up the philosophy as "take a trade off of high time frame bias in line with low time frame confirmation" [__fKQR5RR08@11:59].

**Canonical order of operations (as of BC2.0, Sep 2023).** Steps are tagged with the latest source that supports them.

0. **Weekly prep (Sunday).** Read the economic calendar for the week. Classify each day as trade normally, wait for the release, de-risk, or no trade [9SUJfAo6Sl8@00:00–02:07; QRvZgj3k8pk@01:50; IY9NJbaNyqA@01:09–02:17]. Do top-down analysis monthly → weekly → daily → 4H and mark the draws [9SUJfAo6Sl8@08:14].
1. **Morning gate.** Check ForexFactory before trading [w5sUCqFH3Lg@24:09]. Apply the news rules (§8) and set the day's risk tier (§6) before anything else [065lMUrD_kg@18:36; 7MBD3ow7I1g@04:29–07:52]. No trade on US bank holidays [1FunNCUw_jM@12:24; 065lMUrD_kg@19:41].
2. **Big-picture bias.** Use the monthly, weekly and daily trend plus any HTF sweep ("trades within monthly, weekly, daily sentiment") [IY9NJbaNyqA@08:26; @14:34].
3. **Daily bias = latest daily BOS direction.** Require at least daily + 4H agreement, ideally the 1H as well. Any conflict means no trade, or waiting for the lower timeframes to re-align (§3) [__fKQR5RR08@04:03–05:11; 4FEty6xgOc0@10:27; -rYGugTIsbU@05:34].
4. **Mark HTF POIs in the bias direction.** These are 1H/4H/daily order blocks / areas of accumulation, FVGs, equilibrium (premium for shorts, discount for longs), plus liquidity: hourly highs/lows, session highs/lows, pre-market highs/lows [sjuWqKDsQtI@12:41; __fKQR5RR08@02:19; o_SdawM3DIE@04:52]. On S&P, 1H blocks work better than 15m blocks [__fKQR5RR08@02:19].
5. **Wait for the NY open (9:30 ET).** No entries in pre-market. Pre-market price can still set structure and bias [qecF411R83s@02:50; 7MBD3ow7I1g@01:43; RQSVIKddFHI@12:35].
6. **Price taps the marked HTF building block.** Don't settle for an unmarked LTF sweep [__fKQR5RR08@22:05; r-DdsJLUlBk@01:40].
7. **LTF sequence (5m/1m):** liquidity sweep → change of trend / BOS that closes beyond a **prominent** swing → mark the area of accumulation (the leg that caused the breakout) and its FVG/EQ/OB [5v4G4xJVKIQ@03:22; ss-dZPMnjeY@01:43; 6zXKK3Wrusg@02:02–03:07].
8. **Third confirmation:** price retraces into that 5m FVG/EQ/OB and reacts. The trigger is a reaction candle close or a 1m BOS. If the reaction is weak, wait for a new high and a second 1m BOS [ss-dZPMnjeY@06:46; SV37R6j5f4M@05:36; 7Q3nalPsSpk@01:09].
9. **Enter** on the close of the trigger candle (1m BOS close or 5m reaction candle) [Iu_v4kuFQhk@01:06; 7MBD3ow7I1g@02:16; 5v4G4xJVKIQ@04:29].
10. **Stop** goes beyond the invalidation point (the sweep extreme) plus a buffer, never a fixed number of points [1FunNCUw_jM@01:08; @05:44; ss-dZPMnjeY@05:06].
11. **Targets.** TP1 is about 1:1 at the first draw on liquidity (one timeframe above execution): close 50% and move the stop to BE. TP2–TP5 sit at HTF building blocks. Never place targets at Fibonacci or random levels [7MBD3ow7I1g@02:16; FjSiLFrg5fo@03:29; 6zXKK3Wrusg@03:07–07:06].
12. **Re-entry.** Allowed only if the bias is not invalidated (the sweep extreme holds), daily risk budget remains, and a fresh full sequence forms [ss-dZPMnjeY@03:25–05:06; SV37R6j5f4M@02:48].
13. **Post-session.** Journal the trade or no-trade, and review bias vs. execution [CZRs2NuLQIw@02:15; 4FEty6xgOc0@13:47].

---

## 2. Glossary (operational definitions)

Format for each entry: **Definition** (TJR) · **Rule** (machine-checkable; `(inferred)` where I formalize) · **Edge cases / invalidation** · **Use** · **Cites** · **Evolution**.

### 2.1 Candle, timeframe, closed-candle rule
- **Definition.** Timeframe = the time it takes one candle to close [bEkbNGUzQME@02:48]. Body = open→close. Wick = traded but not closed there [bEkbNGUzQME@05:05–06:13].
- **Rule.** All structure decisions use **closed candles only**: "We can only make bias and decision on candles that have formed, not candles that are forming" [bEkbNGUzQME@16:43]. Evaluate only at bar close on the timeframe being read [PmhuPbY8ZHo@20:35].
- **Edge cases.** Single-candle reads (doji, hammer, long rejection wick, strong close) are minor context only. They never override structure and are never a standalone trade reason [bEkbNGUzQME@11:25; @14:25]. Multi-candle patterns (W, head & shoulders) are not used [bEkbNGUzQME@07:21–09:07].
- **Use.** A doji or indecision candle while waiting for a BOS [qecF411R83s@13:06]. Large wicks at highs or lows suggest liquidity was taken [bEkbNGUzQME@09:44].
- **Cites.** [bEkbNGUzQME@02:48; @16:43; @20:35]

### 2.2 Swing high / swing low ("high", "low")
- **Definition.** "A high is a move up then a move down; a low is a move down then a move up" [PmhuPbY8ZHo@01:39].
- **Rule.** Minimum two candles. Swing high: a bullish candle followed by a bearish candle. Its price = max(high of candle 1, high of candle 2) [PmhuPbY8ZHo@04:25]. Swing low: a bearish candle followed by a bullish candle. Its price = min(low of the two) [PmhuPbY8ZHo@02:15; @04:58]. A swing exists only once the second candle has closed. A forming candle or its wick is not yet a high, and if the next candle is down the high moves there [PmhuPbY8ZHo@20:35–21:08].
- **Edge cases.** Don't lump several candles into a "bigger" high, and don't require symmetry [PmhuPbY8ZHo@01:39–04:58]. A lower-timeframe zoom can settle which wick is the true extreme [PmhuPbY8ZHo@05:33–06:04]. Only the **most recent** swing is relevant for BOS; forget older ones [PmhuPbY8ZHo@17:44].
- **Use.** The basis of trend, BOS, liquidity and stops.
- **Evolution.** BC2 adds the "prominent" filter for which swings count as structure (§2.5).

### 2.3 Trend / consolidation
- **Definition.** Uptrend = higher highs and higher lows. Downtrend = lower highs and lower lows. Consolidation = price static with alternating highs and lows, no BOS, no follow-through [viuGHEuv0nw@02:11–03:16; @12:14–13:22; PmhuPbY8ZHo@19:27].
- **Rule (inferred formalization).** Trend state on timeframe T = the direction of the last BOS on T (§2.4). Consolidation = no new BOS over N bars while swings alternate (N is unstated; OPEN).
- **Edge cases.** In a trend the impulse legs are larger than the retracements ("the moves higher are always smaller than the moves lower" in a downtrend) [viuGHEuv0nw@20:34]. "The extension is always way larger than the retracement" [UPA9LQW7phk@02:53]. Retracements chop; extensions are clean [IY9NJbaNyqA@14:34; __fKQR5RR08@15:20].
- **Use.** Trade with the trend. Never trade the retracement, only the extension [Y1lqifylC4s@08:52; 4FEty6xgOc0@09:54]. Trending markets are the highest-probability markets, and chop is a no-trade condition [uGi6EeKnWSk@06:28; @04:39]. A line chart may be used to read weekly direction [viuGHEuv0nw@18:24; sjuWqKDsQtI@11:32].

### 2.4 Break of structure (BOS)
- **Definition.** "A shift in the trend" [PmhuPbY8ZHo@01:07]. BOS confirms that orders were filled and structure shifted [ESsy0uoFAz4@01:38].
- **Rule.** Bullish BOS: a candle **body closes above** the most recent swing high's wick ("the candle body has to be above the wick of the high") [PmhuPbY8ZHo@07:47]. Bearish BOS: a candle body closes below the most recent swing low [PmhuPbY8ZHo@11:46]. "It is not a break of structure unless the candle closes above a high or below a low" [PmhuPbY8ZHo@12:57]. Checklist: identify trend → in an uptrend watch the most recent low → in a downtrend watch the most recent high → a close beyond it is the BOS [PmhuPbY8ZHo@14:07–17:44]. Wait for the candle close [bEkbNGUzQME@16:43].
- **Edge cases / invalidation.**
  - A wick through a level without a close is **not** a BOS. It is usually a liquidity sweep [PmhuPbY8ZHo@12:21–13:33; @23:22].
  - A BOS against the next-higher timeframe's trend is usually a retracement of that higher timeframe: 1m BOS → 5m retrace; 5m → 15m; 15m → 1H; 1H → 4H; 4H → daily; daily → weekly [Y1lqifylC4s@07:47–08:20; S-scwzKRP-8@04:31–05:37; uGi6EeKnWSk@12:00]. "Not every single time, because there's liquidity sweeps and change of market structure" [S-scwzKRP-8@05:05].
  - BC2: the break must be of a **prominent** high or low. A 5m BOS of a minor internal high is insufficient [5v4G4xJVKIQ@01:42–03:57].
  - BC2: "big extension up" on the 4H was accepted as a BOS [IY9NJbaNyqA@05:05]. This is looser wording; treat it as a close beyond the prior swing (inferred).
  - A weak BOS "wasn't enough" (forex) [OH--4nkbXlM@01:49]. A breakout should show "very obvious volume" [7Q3nalPsSpk@07:19].
- **Use.** (a) Sets trend and bias on every timeframe. (b) Is the confirmation after a sweep. (c) Is the LTF entry trigger.
- **Evolution.** BC1: entering on the BOS itself is entry model 1 [ESsy0uoFAz4@03:18]. From Day 41 a bare sweep+BOS is no longer an entry [PyCPHiO2nj0@02:10–03:18]. BC2 requires a BOS of a prominent swing plus a third confirmation (§4).

### 2.5 Prominent high / prominent low
- **Definition.** The liquidity that matters most. What counts as prominent depends on the timeframe; he says it is "relatively easy" to see by eye and gives no exact rule. Examples: a high that starts a big trend, a double top, a high or low that broke structure on the daily, the most recent swing points before a BOS [KtC2SbemF6w@03:28–05:08]. BC2: a significant swing whose break counts as real structure confirmation, as opposed to a minor internal high [5v4G4xJVKIQ@01:42; @02:49–03:22]. Breaking "a series of prominent highs" is the BC2 trigger [6zXKK3Wrusg@01:27].
- **Rule (inferred, OPEN).** Candidate operationalization: a swing high on timeframe T is prominent if it is (i) the origin of a leg that later produced a BOS on T, or (ii) an equal-high/double-top cluster, or (iii) a swing that produced a BOS itself. TJR gives no numeric threshold.
- **Use.** Which swings count for BOS confirmation (BC2), which liquidity to target, and the "next unreacted prominent high" as a target [KtC2SbemF6w@12:28].
- **Evolution.** BC1 uses it for liquidity (Day 12). BC2 makes it a filter on BOS validity (Day 8, Day 11).

### 2.6 Market structure shift (MSS) / change of character (CHoCH) / change of trend
- **Definition.** He uses MSS interchangeably with BOS ("break of structure / market structure shift") [PmhuPbY8ZHo@06:39; Lxnu7InGhGE@06:43]. "CHoCH" appears only once, as an alternative LTF confirmation alongside BOS and MSS [S1kY3Fw6JUQ@07:57]. In BC2 he says **"change of trend"**: price breaks out of a downtrend (or uptrend) and the first opposite BOS forms [ss-dZPMnjeY@01:43; oJq8egtzCto@03:38; r-DdsJLUlBk@01:40].
- **Rule.** Same candle-close logic as BOS (§2.4). The first BOS against the prevailing LTF trend = change of trend (inferred). The model journal entry lists "market structure shift, then a break of structure on the LTF → enter" [z9p7OThLkr4@19:38]. That suggests MSS = the first break and BOS = the confirming break (inferred, vague).
- **Evolution.** BC2 frames the whole model as "accumulation → distribution → change of trend" [oJq8egtzCto@03:38–04:11].

### 2.7 Liquidity; buy-side / sell-side liquidity
- **Definition.** "Resting orders": stop orders plus buy/sell limit orders clustered at price points [Lxnu7InGhGE@02:13]. Concretely these are **highs and lows** [KtC2SbemF6w@02:53]. Above highs (in uptrends) sit breakout buy-stops and shorts' stop losses = buy-side liquidity. Below lows sit sell-stops and longs' stops = sell-side liquidity [rdz6vnXb8wE@02:12–06:38]. "Sell-side liquidity" appears in [9SUJfAo6Sl8@03:15] (term use partly inferred). Liquidity is "a magnet for price" [KtC2SbemF6w@05:41]. "The market is unable to move in the direction it wants without taking out liquidity" [rdz6vnXb8wE@11:08].
- **Rule.** Mark swing highs and lows, prominent ones first (§2.5), on the timeframe in use. Also mark session highs and lows (§2.10), pre-market highs and lows [r-DdsJLUlBk@02:14], the prior week's NY highs [-rYGugTIsbU@07:11] and HTF (monthly/weekly/daily) highs and lows.
- **Edge cases.** Not every high or low will be used to fill orders, so wait for confluence [KtC2SbemF6w@19:15]. Never buy at a low or sell at a high just because it was reached [KtC2SbemF6w@06:16]. In BC2 Day 11 he loosely says liquidity is "just a higher low within the market" (likely a misstatement) [6zXKK3Wrusg@11:00].
- **Use.** Two uses [KtC2SbemF6w@06:49–10:12]: (1) the place to wait for a sweep and then confirmation; (2) the target, i.e. opposing liquidity.
- **Cites.** [Lxnu7InGhGE@02:13; rdz6vnXb8wE@04:56; KtC2SbemF6w@02:53; @05:41]

### 2.8 Liquidity sweep (a.k.a. "London fake-out", "inducement")
- **Definition.** A prominent high or low is taken out and price then reverses: "uptrend, sweep of the highs, collapse" [rdz6vnXb8wE@07:10]. It "shows the potential for orders to get filled; we don't know whether it's confirmed yet" [ESsy0uoFAz4@01:06]. He calls it "the inducement" [j1pVK897oZQ@09:10]. His original discovery was the GJ London-open fake-out [Xq6-oO2n6-U@37:05; _6voYEdi5j4@06:40].
- **Rule.** Sweep of a high: some bar's high trades above the marked high. Either a wick or a close beyond counts ("wicked below lows ... or a close below them — both acceptable", vague) [UPA9LQW7phk@10:49]. A barely-wicked high counts [KtC2SbemF6w@13:02]. A sweep may be visible only on a lower timeframe [KtC2SbemF6w@14:11]. **Confirmation** is required: a BOS in the opposite direction [Lxnu7InGhGE@08:24; rdz6vnXb8wE@09:57].
- **Edge cases / invalidation.**
  - No BOS after the sweep means "hands off" [Lxnu7InGhGE@08:24; SLhIA7vW9x8@04:36].
  - If price later trades back beyond the swept extreme, the sweep was not valid. That is why the stop goes there [1FunNCUw_jM@01:41–02:15].
  - Near news, require the high to be **taken out**, not merely tapped [G7eq6U8e3yw@02:13].
  - A sweep against the HTF picture is low probability [__fKQR5RR08@11:25].
  - An unmarked LTF sweep is not a substitute for the marked HTF block being hit [__fKQR5RR08@21:32–22:40].
  - GU: "maybe wait for the NY lows to be fully taken out" [OH--4nkbXlM@06:14].
- **Use.** Core of the model: "the most valuable and the most essential thing" [-ga9oK2bClQ@02:46]. Defines the order block (the leg that swept). Defines the stop (invalidation). Defines bias invalidation for re-entries [ss-dZPMnjeY@04:32; SV37R6j5f4M@03:55].
- **Evolution.** BC1: sweep + BOS = complete entry (model 1). From Day 41: necessary but not sufficient. BC2: the sweep extreme = bias invalidation for the day's idea.

### 2.9 Draw on liquidity (DOL)
- **Definition.** The liquidity price is drawn to. Market makers who sell at highs must exit at lows, so a short targets the prior lows and a long targets the prior highs [KtC2SbemF6w@08:28–10:12].
- **Rule.** The next unswept prominent opposing high or low in the trade direction. If no building blocks sit in between, expect price to run all the way to it [QRvZgj3k8pk@03:59]. In a downtrend the next draw is "just the most recent low", then the 50% level, then further liquidity, then the OB [Y1lqifylC4s@14:02–14:36].
- **Use.** Targets (§5) and bias context (S&P draw = monthly highs) [-rYGugTIsbU@00:00; 9sD9kTia4V4@02:49].

### 2.10 Session highs/lows (Asia, London, NY, pre-market)
- **Definition.** The high and low of the Asian session, the London session and the prior New York session, plus pre-market highs and lows. All are treated as liquidity [S-scwzKRP-8@07:36; -rYGugTIsbU@07:11; OH--4nkbXlM@01:15; r-DdsJLUlBk@02:14].
- **Rule.** Mark them as zones **from the candle body ("base") to the wick** [OH--4nkbXlM@02:23]. The exact session clock times are not stated (OPEN).
- **Use.** Primarily the **Forex strategy** (§4.F): sweep a session high or low → 5m BOS. For ES: TP1 at pre-market lows [r-DdsJLUlBk@02:14]. The prior NY session highs/lows are TP1 in the gold trade [OH--4nkbXlM@02:23]. A 30-minute high or OB is required for the forex short [9sD9kTia4V4@14:45].

### 2.11 Fair value gap (FVG) / imbalance / liquidity void
- **Definition.** "A price range where there are no contradicting orders" [d0AxLACYaqU@02:13]. He treats FVG, imbalance and liquidity void as the same thing [d0AxLACYaqU@01:40].
- **Rule.** Three-candle pattern; candle 2 is the large displacement candle [S1kY3Fw6JUQ@04:01]. **Bullish FVG** = [high of candle 1, low of candle 3], valid only if low(C3) > high(C1) [S1kY3Fw6JUQ@05:09]. **Bearish FVG** = [high of candle 3, low of candle 1], valid only if high(C3) < low(C1) [S1kY3Fw6JUQ@06:49]. If the wicks of C1 and C3 overlap, it is not an FVG [S1kY3Fw6JUQ@04:36; @09:37–10:49]. **Refinement:** if a later wick has already traded into part of the gap, only the untouched remainder is the live FVG [qecF411R83s@11:59–12:33].
- **Edge cases / invalidation.** If price trades fully through the gap ("all the way up through this, past it"), it is dead [qecF411R83s@09:09]. An FVG that is "disrespected" (no reaction) is ignored, so use the next level [RQSVIKddFHI@11:27; @17:03]. A deep fill without a close back out is a weak reaction [7Q3nalPsSpk@01:09]. FVGs are **not reversal tools**; use only FVGs in the bias direction after a BOS [S1kY3Fw6JUQ@02:53; @03:29; @05:42].
- **Use.** A retracement and continuation entry zone. The "patient entry" when the sweep+BOS entry gives poor RR [qecF411R83s@05:10]. "More of a confirmation rather than an entry" [qecF411R83s@15:54]. Also a target (its start, 50% or end) [qecF411R83s@10:20; RQSVIKddFHI@13:44]. Never enter merely because it was touched: wait for a reaction candle or a LTF BOS/CHoCH [S1kY3Fw6JUQ@07:57; ss-dZPMnjeY@02:50].
- **Evolution.** BC1 Day 14: "I don't use fair value gaps for entries necessarily" [d0AxLACYaqU@03:54]. By Day 30 an FVG fill is entry model 3 [ESsy0uoFAz4@04:25]. BC2: one of the three "third confirmation" options [ss-dZPMnjeY@06:46]. ES preference: no "small FVG plays" when an HTF OB is wanted [9sD9kTia4V4@03:56].

### 2.12 Inverse FVG (IFVG)
- **Not present** in any Boot Camp notes (0 hits). Do not add to the model from this material. Flag for the later-video pass (§12).

### 2.13 Order block (OB)
- **Definition (BC1).** "All an order block is, is that move up that causes the liquidity sweep" [qhuFg_OXdmE@03:10]: the leg into the swept extreme, immediately before the BOS in the other direction [RQSVIKddFHI@01:05; @22:23; 12_F-mIUfL0@06:58]. It is the price range where orders were filled on the sweep, so price returns to fill more [qhuFg_OXdmE@04:16–05:53]. "It's the whole up move prior to the move down" [RQSVIKddFHI@06:47]. "Order block" and "accumulation area" are interchangeable [qhuFg_OXdmE@10:52].
- **Rule (drawing).**
  - Beginner: box the **entire leg** that swept liquidity before the BOS [12_F-mIUfL0@10:20; @25:42].
  - TJR's own: box the extreme candle **from its wick to the start of its body**. The "base of the body" is the usual reaction point [12_F-mIUfL0@10:20–11:27].
  - Bearish OB = last up-leg/candle that made the high before a bearish BOS. Bullish OB = last down-leg that made the low before a bullish BOS (inferred formalization of [RQSVIKddFHI@01:05]).
- **Edge cases / invalidation.**
  - Best when it includes a liquidity sweep: "if you see a liquidity sweep and then a leg higher you should assume there's an order block there" [12_F-mIUfL0@09:47; @23:20].
  - "Only one order block within every trend" [qhuFg_OXdmE@09:13]. Later contradicted by nested accumulations (§11).
  - OBs don't always get hit; if price never retraces into it, there is no trade [RQSVIKddFHI@18:48; SLhIA7vW9x8@12:07].
  - Reactions weaken late in the session [LG_IbfjbaOo@06:20].
  - An OB tap + 1m BOS without a secondary OB/FVG is "not necessarily high confluence" [__fKQR5RR08@26:30].
  - A tap is "not enough in itself" [12_F-mIUfL0@19:58].
- **Use.** First-choice retracement entry in BC1 ("first option every single time") [qhuFg_OXdmE@06:28]. Also a TP level [12_F-mIUfL0@13:39] and a stop reference [RQSVIKddFHI@20:42]. The HTF OB is the POI where LTF execution happens [RQSVIKddFHI@13:09].
- **Evolution.** In BC2 "order block" is used loosely as "just an area where orders were filled prior" [5v4G4xJVKIQ@06:06]. It is the "leg up before the extension down" [o_SdawM3DIE@04:52] and the "leg down that caused the leg up" [6zXKK3Wrusg@01:27], and it is largely merged with **area of accumulation** (§2.14).

### 2.14 Area of accumulation ("accumulation", "where orders were filled")
- **Definition.** A consolidation or chop range just before a strong extension leg; "where orders were filled" before the leg. Price draws back into it before continuing [Iu_v4kuFQhk@00:32; 7MBD3ow7I1g@01:43–02:16; oJq8egtzCto@03:05]. A consolidation can be considered an OB [-E7plUbSJUk@10:08]. A range containing multiple OBs, FVGs and lows can be treated as one area, "accumulation central" [__fKQR5RR08@02:52]. A nested smaller-timeframe accumulation inside a larger one is a high-confluence POI [IY9NJbaNyqA@11:47–12:21].
- **Rule (inferred formalization, OPEN).** After a change of trend / BOS on timeframe T, the area of accumulation = the price range of the opposite-direction leg or chop that **immediately preceded and caused** the breakout leg ("the leg down that filled the orders for the leg up") [ss-dZPMnjeY@01:43; @06:14; SV37R6j5f4M@04:27]. Boundaries: from the extreme of that leg to the start of the breakout leg (inferred). Apply fractally: after a 5m BOS, find the accumulation that caused that 5m BOS, wait for the revisit, then look for a 1m BOS [ss-dZPMnjeY@07:21; 6zXKK3Wrusg@04:50].
- **Edge cases.** A first touch may fail and sweep nearby lows; keep waiting for the retest after the sweep [Iu_v4kuFQhk@00:32–01:06]. A leg with too little movement is no longer a valid leg [SV37R6j5f4M@07:49]. Do not enter **inside** a consolidation; wait for the breakout with volume and then the retest [o_SdawM3DIE@20:09; 7Q3nalPsSpk@07:19].
- **Use.** The BC2 core entry zone and a final TP (an HTF accumulation) [ss-dZPMnjeY@07:53]. TP2 = the accumulation before the prior drop [Iu_v4kuFQhk@01:39].
- **Evolution.** Mentioned in BC1 as a target [qecF411R83s@11:27]. It is the central concept of BC2 ("areas of accumulation after our high time frame building blocks get hit") [r-DdsJLUlBk@01:40]. A dedicated strategy video was promised but is not in this set (OPEN).

### 2.15 Equilibrium (EQ), premium, discount
- **Definition.** The 50% level of a swing range, "where big money is likely to buy again" [j1pVK897oZQ@05:16; @06:24]. Uptrend: measure swing low → swing high; below 0.5 = discount (buy zone). Downtrend: measure swing high → swing low; above 0.5 = premium (sell zone) [j1pVK897oZQ@06:57–08:03; -E7plUbSJUk@01:45–02:51].
- **Rule.** Tool = Gann box or Fibonacci with only the 0, 0.5 and 1 levels [-E7plUbSJUk@03:24–04:30]. Anchor at the latest swing low → latest swing high (uptrend), or the reverse. **Re-anchor** whenever a new extreme forms before 0.5 is reached [-E7plUbSJUk@06:46; @18:02]. In execution, EQ = 50% of the BOS leg, drawn when the first retracement candle prints [K8DwhtmvAW8@15:00; @19:49]. Longs need price ≤ 0.5 (discount); shorts need price ≥ 0.5 (premium). This is "the bare minimum that I look for for retracements" [Y1lqifylC4s@11:12].
- **Edge cases.**
  - Never enter purely off EQ [j1pVK897oZQ@08:35; -E7plUbSJUk@02:51].
  - **EQ-only entry** requires a candle **close back beyond** the EQ line (above it for longs), ideally with a new BOS. A single reaction candle is enough only inside an OB or FVG [4FEty6xgOc0@04:25–04:59].
  - Terminology slips: he often says "discount" for a bearish premium zone [Y1lqifylC4s@11:12; UPA9LQW7phk@08:33]. The bot must use the standard meaning (inferred).
  - Fib 0.5/~0.62 levels work "because it's equilibrium" [-E7plUbSJUk@07:19]. Fib is **not** used for TPs [6zXKK3Wrusg@05:59].
- **Use.** Zone filter. EQ + FVG = "the perfect tools to combine" [j1pVK897oZQ@09:43]. EQ overlapping an FVG/OB = "high confluence trade" [K8DwhtmvAW8@15:00]. Also a target (the 50% of a daily OB) [o_SdawM3DIE@12:55].
- **Evolution.** See §11 (EQ + BOS sufficiency).

### 2.16 Building blocks / PD array / POI / high-confluence zone
- **Definition.** The five building blocks: liquidity sweep, break of structure, order block, fair value gap, equilibrium [ESsy0uoFAz4@01:06]. Day 45 lists four (sweep, BOS, OB, FVG) [LG_IbfjbaOo@17:24]. "Simple concepts plugged into an execution order" [_6voYEdi5j4@04:27]. The "PD array" phrase appears in his model journal entry (EQ, FVG, OB) [z9p7OThLkr4@19:38]. A **high-confluence price zone** is an HTF area where blocks overlap, such as a 4H FVG + OB, or FVG + EQ + OB [UPA9LQW7phk@07:29; QRvZgj3k8pk@05:10].
- **Rule.** A zone = the union or overlap of ≥1 HTF building block in the bias direction. Overlap of ≥2 = high confluence (inferred from usage). If nothing marked is hit, there is no trade [4FEty6xgOc0@12:07–13:14; S-scwzKRP-8@14:35].
- **Use.** Entry locations (HTF), entry confirmation (LTF) and targets.

### 2.17 Retracement vs. extension
- **Definition.** Extension = the with-trend leg on the higher timeframe. Retracement = the counter-leg. "Would you rather take the retracement or the extension ... I'm taking the extension every single day" [Y1lqifylC4s@08:52].
- **Rule.** A trade direction must equal the extension direction of the bias timeframe. Mark every building block a retrace could reach, then act on the reaction that starts the next extension [__fKQR5RR08@15:20–17:36]. "We never want to trade retraces unless it's on like the weekly time frame" [4FEty6xgOc0@09:54].

### 2.18 Daily bias (and weekly/monthly context)
- **Definition.** "Where price wants to go for the day" [sjuWqKDsQtI@00:02], taken from the **daily current market structure**: the direction of the latest daily BOS [sjuWqKDsQtI@01:43; UPA9LQW7phk@04:02]. See §3 for the full procedure.
- **Evolution.** BC2 widens the lens to monthly + weekly + daily "big picture" sentiment [IY9NJbaNyqA@08:26; @14:34] and adds news direction as a bias input [7MBD3ow7I1g@01:43; r-DdsJLUlBk@05:34] (see §11).

### 2.19 Third confirmation / third confluence
- **Definition (BC2).** After (1) price taps the area/POI and (2) a BOS forms, wait for (3) a reaction off a 5m FVG, 5m equilibrium or 5m OB [ss-dZPMnjeY@06:46]. In BC2 D1 the three are: POI tag, FVG or OB, rejection off it [o_SdawM3DIE@07:09].
- **Rule.** Price retraces into the post-BOS 5m FVG/EQ/OB, then a reaction appears: a candle closing in the trade direction, or a 1m BOS. For an EQ-only reaction, the candle must close back beyond EQ (§2.15). If the reaction is weak (filled too deep, no close back above), wait for a new high and a second 1m BOS [7Q3nalPsSpk@01:09–01:44].
- **Edge cases.** Skipping it is "the mistake" [SV37R6j5f4M@05:36; o_SdawM3DIE@07:09]. Not required in the **Forex strategy** [OH--4nkbXlM@02:23].

### 2.20 Reaction (confirmation candle)
- **Definition.** A candle in the trade direction after price enters a zone [S1kY3Fw6JUQ@07:57]. Waiting 1–2 extra candles is permitted [339amTioakE@08:21; oJq8egtzCto@04:44].
- **Rule (inferred).** Long: a bullish candle (close > open) that closes inside or above the zone after trading into it. For EQ-only zones the close must be above 0.5 [4FEty6xgOc0@04:59]. The 5m "reaction candle" close is used as an entry trigger [ss-dZPMnjeY@06:14–08:26; 7Q3nalPsSpk@07:19].
- **Edge case.** In BC1 Day 26 he says an OB can be entered "instantly when that price point gets hit" [j1pVK897oZQ@14:13] (see §11).

### 2.21 Invalidation point
- **Definition.** "Our stop loss always has a purpose; our stop loss is essentially our invalidation area" [1FunNCUw_jM@02:15]. It is the swept extreme. BC2: the bias stays valid as long as the sweep low is not taken out [ss-dZPMnjeY@04:32]. An example invalidation is the London session low sweep being swept again [5v4G4xJVKIQ@01:42].
- **Rule.** Long idea: invalidated if price trades below the sweep low. Short idea: invalidated if price trades above the sweep high (inferred mirror). Whether a wick or a close is needed is unstated; treat a trade-through as invalidation (inferred, OPEN).

### 2.22 Wyckoff accumulation / spring
- **Definition.** Consolidation → a liquidity sweep below the range (the spring) → price springs back into the range → breakout → retest of the old ceiling as a floor → continuation [o_SdawM3DIE@20:43–22:21].
- **Weight.** "Extra confluence or extra confidence" to **hold** a trade. Not ICT. Not an entry requirement [o_SdawM3DIE@21:48]. Only 1 BC2 video (plus the "Wyckoff-like" accumulation language in [IY9NJbaNyqA@05:05]).

### 2.23 Market open / price & time theory
- **Definition.** The NYSE open is when new money enters, there is usually a sweep, and orders fill. The first trade at the open is the highest-probability trade. Later trades are lower-RR retracements [4moWbfm6smw@03:48–04:57]. The majority of the S&P daily move happens in the NY session; "everything else is just chop" [sjuWqKDsQtI@05:08].

### 2.24 News bias
- **Definition.** The direction implied by actual vs. forecast plus the "usual effect" on ForexFactory. Good for USD = bad for SPX, gold, GU and BTC [w5sUCqFH3Lg@12:29–14:11]. Fraction rule for pairs [w5sUCqFH3Lg@16:57–21:58; 9sD9kTia4V4@01:09].
- **Weight.** BC1: "not the day's bias"; "price action is superior" [w5sUCqFH3Lg@15:17; @22:30]. BC2: used as a bias input [7MBD3ow7I1g@01:43; r-DdsJLUlBk@05:34] (see §11).

### 2.25 SMT divergence; other "don't use" tools
- **SMT:** "I don't trade it and I don't even know what [it] is ... something to do with the NASDAQ" [_6voYEdi5j4@05:00–05:35]. Not used anywhere in the Boot Camp.
- **Support/resistance:** "like guessing", not used [Lxnu7InGhGE@01:05; d0AxLACYaqU@01:40]. Ranging "support and resistance territory" is a no-entry zone [o_SdawM3DIE@20:09].
- **Multi-candle chart patterns, EMA crosses, indicators:** not used [bEkbNGUzQME@07:21; ESsy0uoFAz4@07:10; Xq6-oO2n6-U@12:16].
- **Trend lines:** noted visually once, "even though he does not use trend lines" [IY9NJbaNyqA@05:05].
- **Fibonacci for TPs:** don't [6zXKK3Wrusg@05:59].
- **"Divergence"** (gold daily, undefined) [9SUJfAo6Sl8@07:09]: vague, not operational.
- **ICT Silver Bullet:** "is a fair value gap"; he doesn't use it [4moWbfm6smw@14:38; _6voYEdi5j4@08:24].

### 2.26 Set lot size / risk tiers
- See §6. **Set lot size** = a size computed so that the typical **minimum** stop risks 1% [KSiWKfPOlh4@08:33–11:26]. Tiers: normal, de-risk (50%), confident (2×) [KSiWKfPOlh4@14:44].

### 2.27 "Market experience" trade
- **Definition.** A discretionary trade from experience rather than the checklist, e.g. relief at the session switch after a big London sell-off. He says these sometimes fail [o_SdawM3DIE@07:09; @09:53]. **Bot: excluded** (not codifiable, inferred).

### 2.28 Displacement / big extension
- **Definition.** A strong one-directional leg (the caption "dick" = displacement leg) [6zXKK3Wrusg@00:55]. It is the move that leaves FVGs and, in BC2, the move out of an accumulation. "Big extension up" on the 4H counts as a BOS [IY9NJbaNyqA@05:05]. No size threshold is given (OPEN).

### 2.29 Chop / bad price action
- **Definition.** Repeated BOS that turn into sweeps, sweeps both ways, "doji after doji", no clear bias, "confluences not playing out" [uGi6EeKnWSk@04:39–07:01; PyCPHiO2nj0@05:32; __fKQR5RR08@15:20].
- **Rule.** No trade on that pair. If it persists for weeks, switch instrument [PyCPHiO2nj0@01:02; @06:04]. For a single-instrument ES bot the equivalent is to stand down (inferred).

---

## 3. Daily bias procedure

### 3.1 Steps (pre-market, about 30 min before the open [uGi6EeKnWSk@01:10]; or the evening before in BC2)

1. **News check first.** Set "no trades until news" if needed [__fKQR5RR08@01:07; 4FEty6xgOc0@01:08].
2. **Monthly → weekly (context).** Eyeball the trend; a line chart is fine [sjuWqKDsQtI@00:35; UPA9LQW7phk@01:07]. The weekly decides whether a daily counter-move is a **weekly retrace**. If so, use retracement tools (weekly EQ/FVG/OB) to estimate how far the daily move goes, and use moderate targets [Y1lqifylC4s@00:33; @05:33; @14:36]. BC2: also note monthly/HTF sweeps, e.g. monthly lows swept while the monthly is still bullish means continuation [IY9NJbaNyqA@05:05; @08:26].
3. **Daily = the bias.** Bias = the direction of the most recent daily BOS (a body close beyond the last daily swing) [sjuWqKDsQtI@01:43; UPA9LQW7phk@04:02]. "Prior to this candle ... I would have been bullish, not anymore" [sjuWqKDsQtI@02:17]. Also note whether the daily is **extending or retracing** [UPA9LQW7phk@02:53].
4. **4H check.** Ideal: the 4H agrees, i.e. it has broken structure the same way. "A break of structure on the four hour means we're kind of good to go on the daily" [9SUJfAo6Sl8@03:15; sjuWqKDsQtI@02:52]. If the 4H disagrees, it is a daily retracement (see 3.3).
5. **1H check.** Agreement is "even better" [Y1lqifylC4s@05:33]. A 4H flip needs a 1H BOS first [__fKQR5RR08@04:03–05:11].
6. **"Imagine a trade on the HTF."** Ask where a daily/4H/1H swing trade in the bias direction would set up (FVG, daily/4H OB, EQ, 1H BOS). Those are the POIs [sjuWqKDsQtI@12:06–14:14; @17:04].
7. **Mark draws on liquidity and targets.** These are 4H imbalances, 4H EQ, the leg that caused the move, and daily liquidity [sjuWqKDsQtI@15:22; @17:36].
8. **Rank instruments by alignment** and drop those with a daily/4H conflict [__fKQR5RR08@05:11; -rYGugTIsbU@06:39]. For a single-instrument ES bot this step becomes go / no-go (inferred).
9. **Write the bias down**, then review it after the session [4FEty6xgOc0@13:47–14:20].

### 3.2 Decision table (ES bot form; each row cited)

| Daily | 4H | 1H | 15m/5m | Action | Cites |
|---|---|---|---|---|---|
| Bull | Bull | Bull | any | Look only for longs, at marked blocks with LTF confirmation | [UPA9LQW7phk@13:06; 9sD9kTia4V4@04:28] |
| Bull | Bull | Bear | — | Wait for a 15m high to form and a close above it (or a 1H bullish confirmation) before longs; otherwise no trade | [Oi_mK1Lt-iQ@00:35–01:07; 9sD9kTia4V4@07:29] |
| Bull | Bear (just broke) | Bear | — | Daily retracement → **no trade**. Mark the daily retrace draws (FVG/EQ/OB) for later longs; wait for a 4H and 1H BOS back up | [__fKQR5RR08@10:18; 4FEty6xgOc0@10:27–11:33; -rYGugTIsbU@05:34] |
| Bear | Bear | Bull | 15m BOS down | The 15m BOS is only a 1H retrace; wait for a 1H BOS down before shorting | [4FEty6xgOc0@07:09; @08:47] |
| Bear | Bull | Bull | — | Low odds, bottom of the list (no trade, or require clear confirmation plus tentative TPs) | [__fKQR5RR08@04:03; sjuWqKDsQtI@04:01–04:34; uGi6EeKnWSk@03:31] |
| Bear | Bear | chop | chop | No trade | [uGi6EeKnWSk@05:46] |
| Bull | Bull | Bear 1H BOS | — | Do not trade the 1H short ("breaking our trading plan") | [9sD9kTia4V4@11:57] |
| Mixed weekly/daily/4H/1H | | | | Sit out | [-rYGugTIsbU@03:51; S-scwzKRP-8@11:00] |
| Daily bull, weekly bear | | | | Trade the **daily** (longs); the weekly counts again only after a daily BOS down | [__fKQR5RR08@05:47; QRvZgj3k8pk@06:16; Oi_mK1Lt-iQ@04:29; 4FEty6xgOc0@08:47] |
| Daily bear, weekly bull | | | | Shorts allowed but expect limited downside (weekly retrace). Use daily confluences as TPs; after the weekly retrace fills (e.g. weekly EQ), a daily BOS back up resumes the weekly | [Y1lqifylC4s@11:12; 9SUJfAo6Sl8@04:21] |
| HTF has "not much to go off" | | | | Don't trade | [Y1lqifylC4s@06:06] |

**The A-setup checklist** [uGi6EeKnWSk@02:20–02:53]: daily bias bullish + 4H BOS up + price takes an hourly building block at the NY open + LTF (5m) BOS up. Anything missing means skip the pair, or the day if it is the only pair [uGi6EeKnWSk@09:47; @13:06].

### 3.3 What flips the bias
- **A daily BOS against the bias** flips the daily bias. Adapt and don't hold the old view [PyCPHiO2nj0@09:21; 9SUJfAo6Sl8@08:47].
- **A weekly trend flip** is confirmed only after a daily BOS, which then produces a weekly BOS ("we won't know when the monthly wants to push higher until we get a weekly break of structure") [9SUJfAo6Sl8@07:42–08:14; QRvZgj3k8pk@06:50].
- **Intraday re-alignment:** a 1H close above a lower high flipped S&P back to longs [-rYGugTIsbU@18:25]. A 15m high formed and closed above is the trigger to resume longs when the 1H is bearish [Oi_mK1Lt-iQ@00:00–01:07]. The topic "how daily bias changes after the NYSE open" was flagged but not taught [O_4yHzZO0u0@06:41] (OPEN).
- **The bias is never flipped by** a 1m/5m/15m BOS [uGi6EeKnWSk@12:00], by fundamentals or macro opinion [UPA9LQW7phk@04:02; Y1lqifylC4s@01:37; IY9NJbaNyqA@10:39], by "overbought" feelings [__fKQR5RR08@02:52], or (BC1) by news bias [w5sUCqFH3Lg@22:30; -rYGugTIsbU@00:00].
- **Intraday idea invalidation (BC2):** the idea dies when the sweep extreme that set it up is taken out. A stop-out alone does not invalidate the idea [ss-dZPMnjeY@04:32; SV37R6j5f4M@03:55].

### 3.4 What means "no trade"
- A news day per §8 [w5sUCqFH3Lg@06:49].
- A daily/4H/1H conflict per §3.2.
- Price never reaches a marked HTF building block ("if it's not hit → no trade") [4FEty6xgOc0@13:14; 9sD9kTia4V4@15:53].
- A zone is hit but gives no reaction or LTF confirmation: "it was never there" [Y1lqifylC4s@09:26–10:01].
- Chop or directionless price action [uGi6EeKnWSk@04:39; S-scwzKRP-8@14:35].
- No FVG, OB or EQ at the retrace: "not necessarily a good spot" [S-scwzKRP-8@14:35].
- Outside the time window, or too late in the session [065lMUrD_kg@11:18; 9sD9kTia4V4@11:26].
- RR to the first reaction area is below 1:1 [5v4G4xJVKIQ@08:52].
- Entry too close to the opposing liquidity [9sD9kTia4V4@09:46].
- A bank holiday [1FunNCUw_jM@12:24].
- The trader is emotionally compromised [_jLR3XcB5eQ@13:28; OH--4nkbXlM@16:10].
- Pre-designated risk was not set on waking [065lMUrD_kg@18:36].
- "Come to the market expecting not to trade" [339amTioakE@04:26; uGi6EeKnWSk@11:27].

---

## 4. Execution / entry models

### 4.0 How he ranks them
- **BC1 Day 20 (retracement priority):** sweep+BOS is the "start of the move". If it is missed: (1) OB, "first option every single time"; (2) FVG; (3) EQ [qhuFg_OXdmE@05:53–07:34].
- **BC1 Day 30 (formal list, by risk):** "the higher up you get on this list the more risky" [ESsy0uoFAz4@05:31–06:05]. Model 1 (sweep+BOS) is the most risky. Models 2 (OB) and 3 (FVG) are "kind of equal". Model 4 (+EQ, "ultimate confluence") is the safest and is the "foolproof plan ... if you are a beginner" (the risk ordering is inferred from garbled captions).
- **BC1 Day 41 onward:** model 1 is **retired** for his own entries [PyCPHiO2nj0@02:10–03:18; CZRs2NuLQIw@09:25].
- **BC2:** the canonical model is **4.E** (HTF block → change of trend → accumulation → third confirmation). The **Forex strategy (4.F)** coexists for FX pairs.

### 4.A Model 1: Liquidity sweep + BOS (enter on the BOS) [BC1; RETIRED for the canonical model]
- **Trigger:** a prominent high/low is swept, then a candle closes beyond the most recent opposing swing [ESsy0uoFAz4@03:18; SLhIA7vW9x8@04:36; KtC2SbemF6w@10:45].
- **Entry:** on the close of the BOS candle ("the top of the move") [ESsy0uoFAz4@03:51; qecF411R83s@03:25].
- **Stop:** beyond the sweep [1FunNCUw_jM@01:08].
- **Targets:** opposing liquidity [KtC2SbemF6w@08:28].
- **Status.** He calls it "the simplest but also ... the riskiest, the lowest confluence" [SLhIA7vW9x8@05:10]. It was dropped because "price was sweeping, breaking structure, stopping him out, then going his way" [PyCPHiO2nj0@02:10]. BC2 entries on a bare BOS are labeled mistakes [SV37R6j5f4M@05:36; o_SdawM3DIE@07:09]. Permitted only when RR is good, per BC1 [065lMUrD_kg@17:29]. **Not canonical.**
- **Variant:** "BOS while in discount" was "enough reason for me to get in" [j1pVK897oZQ@08:35]. Later downgraded [-E7plUbSJUk@07:19] (§11).

### 4.B Model 2: Sweep + BOS + order block retracement [BC1 first choice]
- **Trigger:** sweep → BOS → price retraces into the OB, i.e. the leg/candle that made the sweep [ESsy0uoFAz4@03:51–04:25; SLhIA7vW9x8@10:56–11:32].
- **Entry:**
  - "We enter at the order block" (limit on touch) [ESsy0uoFAz4@04:25; j1pVK897oZQ@14:13], or
  - on a LTF BOS after price is inside the OB. Scale 1H → 15m and enter on the candle close that breaks the LTF swing [RQSVIKddFHI@13:09; @20:42; 12_F-mIUfL0@11:58].
  - It "doesn't matter if it's exact or not" [SLhIA7vW9x8@15:16].
  - A single reaction candle suffices inside an OB [4FEty6xgOc0@04:25].
- **Stop:** "stops above the highs" (beyond the sweep) [ESsy0uoFAz4@04:25]. Alternatively beyond the LTF swing that formed the BOS, or beyond the whole OB "to play safe" [RQSVIKddFHI@20:42; @22:56]. The stop must fit the timeframe of the play: a 4H OB needs a stop beyond the 4H swing [RQSVIKddFHI@09:08–09:42].
- **Targets:** HTF liquidity, laddered TP1/TP2/TP3 [RQSVIKddFHI@09:42; @21:17].
- **No trade** if the OB is never touched [SLhIA7vW9x8@12:07].

### 4.C Model 3: Sweep + BOS + FVG fill [BC1]
- **Trigger:** sweep → BOS → the displacement leaves an FVG → price retraces into it. The steps need not be simultaneous [ESsy0uoFAz4@04:25; K8DwhtmvAW8@06:52].
- **Entry:** on a reaction "or just for it to get hit" [ESsy0uoFAz4@04:58], or better, drop to a LTF and enter on a BOS close [K8DwhtmvAW8@07:26; @09:44; S1kY3Fw6JUQ@07:57]. Multi-step drill-down: HTF FVG → 15m BOS → 5m FVG → 1m BOS for a "prime time" entry [qecF411R83s@03:25–04:00]. A sweep inside the FVG before the LTF BOS is ideal [qecF411R83s@12:33].
- **Stop:** beyond the retracement high/low formed into the FVG [qecF411R83s@06:48], or beyond the previous high [S1kY3Fw6JUQ@09:04].
- **Targets:** prior liquidity, accumulation, OB, or an imbalance's start/50%/end [qecF411R83s@10:20].
- **Labels:** "patient entry" [qecF411R83s@05:10]; "last chance" entry [K8DwhtmvAW8@19:16].

### 4.D Model 4: Sweep + BOS + (FVG or OB) + EQ ("ultimate confluence") [BC1 safest; precursor of BC2]
- **Trigger:** sweep → BOS → draw EQ on the BOS leg → wait for the overlap of EQ (premium for shorts, discount for longs) with an FVG or OB [ESsy0uoFAz4@05:31; K8DwhtmvAW8@13:52–15:00].
- **Entry:** scale down and enter on a LTF BOS [-E7plUbSJUk@06:13; @08:26; @10:42].
- **Stop:** beyond the BOS swing [-E7plUbSJUk@12:21].
- **Targets:** previous liquidity, multiple TPs [-E7plUbSJUk@16:15].
- **Examples:** stacking 7 confluences builds confidence [K8DwhtmvAW8@22:27]. The Day 41 accepted list includes "OB + FVG + EQ" [PyCPHiO2nj0@03:18].

### 4.E Model BC2: HTF block → change of trend → area of accumulation → third confirmation [**CANONICAL as of BC2**]
The sources are BC2 D5.5–D13, plus the D48–D54 rules that feed into it.
1. **Context:** HTF bias (§3) and an **HTF building block is hit**: an HTF OB, accumulation, FVG or EQ. "Areas of accumulation after our high time frame building blocks get hit" [r-DdsJLUlBk@01:40; 9sD9kTia4V4@03:56; __fKQR5RR08@22:05].
2. **Sweep:** liquidity taken at or into the block, e.g. hourly lows, London lows, pre-market or session extremes, 4H lows [Iu_v4kuFQhk@00:00; SV37R6j5f4M@00:34; 5v4G4xJVKIQ@01:06].
3. **Change of trend / BOS:** a 5m (sometimes 1H or 1m) BOS in the bias direction that breaks a **prominent** swing, or a break of the LTF mini-trend [5v4G4xJVKIQ@03:22; 6zXKK3Wrusg@02:02; ss-dZPMnjeY@01:43].
4. **Mark the area of accumulation** that caused the breakout leg (the leg down that filled the orders for the leg up), plus the 5m FVG/EQ/OB inside the leg [ss-dZPMnjeY@06:14; SV37R6j5f4M@01:07; 7MBD3ow7I1g@01:43].
5. **Third confirmation:** price revisits the area or zone and reacts (§2.19). The trigger is either a 1m BOS (or a close above a prominent 1m high) or a 5m reaction candle close [ss-dZPMnjeY@06:46; 6zXKK3Wrusg@02:34–03:07; SV37R6j5f4M@06:09]. A weak reaction means waiting for a new high and a second 1m BOS [7Q3nalPsSpk@01:09–01:44]. Waiting a couple of extra candles is allowed [oJq8egtzCto@04:44].
6. **Entry:** on the close of the trigger candle [Iu_v4kuFQhk@01:06; 5v4G4xJVKIQ@04:29; 7MBD3ow7I1g@02:16].
7. **Stop:** under the invalidation point: the sweep low, or the low of the accumulation that caused the leg [ss-dZPMnjeY@05:06; 6zXKK3Wrusg@02:34; Iu_v4kuFQhk@01:39; 7Q3nalPsSpk@07:19]. Plus a buffer (§5.1). Not a fixed "5 points" [ss-dZPMnjeY@02:50].
8. **Targets / management:** §5.
9. **Fractal note:** "we just keep scaling and keep finding these miniature trends", e.g. hourly breakout → 5m → 1m [6zXKK3Wrusg@04:50; ss-dZPMnjeY@07:21].
10. **Consolidation variant:** if price is in a range, do not enter inside it. Wait for a breakout with "very obvious volume", then a retest of the area/FVG, then a 5m reaction candle [7Q3nalPsSpk@07:19–08:26; o_SdawM3DIE@20:09].
11. **Sizing exception:** entering without full confluence was done at 50% size [o_SdawM3DIE@06:35]. This was a deviation he described, not a rule.

Pseudo-rule (long; shorts mirror) (inferred formalization):
```
PRE: bias_daily==BULL and bias_4H!=BEAR_conflict (see §3.2) and news_gate==OPEN and 9:30<=t<=11:00 ET
POI: price trades into marked HTF bullish block (1H/4H OB|accumulation|FVG|EQ<=0.5)
SWEEP: low(bar) < marked_liquidity_low  [hourly/session/pre-market/LTF prominent low]
COT: 5m close > most_recent_prominent_5m_swing_high  (after SWEEP)
ZONE: accumulation = leg_down_that_preceded_COT_leg; fvg5/eq5(0.5 of COT leg)/ob5
CONF3: price retraces into ZONE and (5m bullish reaction close  OR 1m close > 1m prominent swing high)
       if zone==EQ_only: require close > EQ
ENTRY: market at CONF3 bar close
STOP: min(sweep_low, accumulation_low) - buffer(0.5pt ES)
TP1: first opposing draw on TF one above execution, ~>=1R; else skip if <1R
```

### 4.F Forex strategy ("TJR 4X Strat") [BC1 late + BC2; FX pairs; NOT ES-canonical]
- **Trigger:** daily bias + daily POI tap (OB/30-minute high). Price sweeps a session extreme (London high/low, Asian high/low, prior NY session high/low), then a 5m BOS in the opposite direction [Oi_mK1Lt-iQ@07:57–09:05; OH--4nkbXlM@03:32; S-scwzKRP-8@07:36].
- **Entry:** on the BOS candle close [OH--4nkbXlM@03:32; G7eq6U8e3yw@02:13], on the 1m BOS candle [Oi_mK1Lt-iQ@08:31], or on the post-BOS dip ("there's usually an instant reaction ... to scare people out") [OH--4nkbXlM@04:04]. Optional: wait for an FVG fill first [OH--4nkbXlM@01:49].
- **No third confluence needed** [OH--4nkbXlM@02:23]. Near news, the session high must be taken out, not merely tapped [G7eq6U8e3yw@02:13]. A short needs price up into the OB/30-minute high; a 5m BOS alone is not enough [9sD9kTia4V4@14:45].
- **Stop:** 4 pips beyond the swept session extreme [G7eq6U8e3yw@02:13; o_SdawM3DIE@19:35].
- **Targets:** TP1 = the opposite prior-session extreme or the next OB; TP2/TP3 = Asian/London extremes at body and wick [OH--4nkbXlM@02:23–03:32; Oi_mK1Lt-iQ@08:31–09:05].
- **ES relevance (inferred):** the session-level logic (sweep of a marked session or pre-market extreme → 5m BOS) overlaps with step 2 of 4.E. The *no-third-confirmation* shortcut should **not** be transferred to ES, given the BC2 ES rule [SV37R6j5f4M@05:36; o_SdawM3DIE@07:09].
- **Origin:** the GJ London-open fake-out (sell after a high is taken, 15-pip stop) [Xq6-oO2n6-U@37:37]. An earlier version used "30 minute boxes in session" [LG_IbfjbaOo@16:17] (unexplained).

### 4.G Equilibrium-only entry [BC1 late; rare]
- **Trigger:** sweep → BOS → retrace into EQ with no OB/FVG.
- **Entry:** only after a candle **closes back beyond EQ**, plus a BOS over the new high [4FEty6xgOc0@04:25–04:59]. Day 49 version: "strong rejection closing back out of equilibrium" [__fKQR5RR08@19:18–19:52].
- **Stop:** under the sweep [4FEty6xgOc0@04:59] or under the wick [__fKQR5RR08@19:52].
- **Weight:** "EQ + only a BOS ... not much confirmation" [-E7plUbSJUk@07:19]. The Day 49 trade using it lost because of an unmarked LTF sweep [__fKQR5RR08@21:32].

### 4.H HTF continuation (FVG/OB retrace in trend, no reversal sweep) [BC1]
- **Trigger:** HTF BOS sets the direction → price retraces into the HTF FVG/OB → LTF BOS in the trend direction [d0AxLACYaqU@04:28; @06:38; RQSVIKddFHI@04:24–13:09; K8DwhtmvAW8@11:23].
- **Same stop and target logic.** A liquidity sweep inside the zone strengthens it [qecF411R83s@12:33].

### 4.I Re-entry model [BC2]
- **Conditions:** the first trade is stopped out, **the bias is not invalidated** (the sweep extreme holds), daily risk budget remains, and a new full sequence forms (BOS + FVG fill + reaction) [ss-dZPMnjeY@03:25–05:06; SV37R6j5f4M@02:48–04:27].
- **Stop:** under the invalidation point.
- He counts it as the same idea: "technically I really only took two trades within my bias" [ss-dZPMnjeY@10:40].

---

## 5. Stops, take profits, trade management

### 5.1 Stop loss
- **Default:** beyond the liquidity sweep extreme, whatever the entry type (OB or FVG). "I almost always put my stop loss above the liquidity sweep" [1FunNCUw_jM@01:08; @03:25]. In BC2 this is the invalidation point [ss-dZPMnjeY@05:06].
- **Buffer:** about **0.5 point beyond on ES**, or your spread [1FunNCUw_jM@05:44–06:50]. On forex, 4 pips [G7eq6U8e3yw@02:13; 7Q3nalPsSpk@05:08], plus an extra ~2 pips "for comfort" [7Q3nalPsSpk@07:19]. His ES example placed the stop about "four below" [1FunNCUw_jM@07:23] (ambiguous).
- **Never a fixed number of points or pips** [1FunNCUw_jM@10:43]. A fixed 5-point stop was a mistake [ss-dZPMnjeY@02:50; @05:06].
- **Exception 1:** if the sweep is so far away that RR is terrible, put the stop beyond a closer OB/FVG. He dislikes this [1FunNCUw_jM@03:59–05:09].
- **Exception 2:** use a swing one timeframe lower (vague) [1FunNCUw_jM@08:28].
- **Alternatives used:** beyond the swing that formed the BOS [-E7plUbSJUk@12:21; K8DwhtmvAW8@07:26]; beyond the whole OB [RQSVIKddFHI@22:56]; under the accumulation that caused the leg [6zXKK3Wrusg@02:34; 7Q3nalPsSpk@07:19]; under the 5m low [oJq8egtzCto@04:44].
- **Timeframe fit:** the stop must suit the timeframe of the play [RQSVIKddFHI@09:42].
- **Typical ES stop:** about **4–7 points** [KSiWKfPOlh4@08:33]. 7 points in an example [7MBD3ow7I1g@06:10].
- **Tightening while in a trade:** he moved a gold stop to above a nearer high after strong legs, keeping the day near BE [r-DdsJLUlBk@04:27]. Discretionary.

### 5.2 Take profits
- **Where:** building blocks are "price magnets": liquidity (highs/lows), OB (its top or bottom), FVG (inside or far side), liquidity voids [FjSiLFrg5fo@01:49–02:56; @07:56]. Use HTF FVGs, OBs and liquidity, never Fibonacci or random levels [6zXKK3Wrusg@05:25–07:06].
- **TP1:**
  - "The one higher time frame draw on liquidity on whatever execution time frame I'm on" (5m execution → first 15m draw) [FjSiLFrg5fo@03:29].
  - It must be at least about 1:1: "most of the time my first take profit is going to be minimum one to one" [FjSiLFrg5fo@06:15]. Typical TP1 RR is 1:1 to 1:5 [FjSiLFrg5fo@05:42].
  - BC2: TP1 = a simple 1:1 [7MBD3ow7I1g@02:16], or the nearby highs [Iu_v4kuFQhk@01:39], or pre-market lows [r-DdsJLUlBk@02:14].
  - **If TP1 RR < 1:1, skip** [5v4G4xJVKIQ@08:52].
- **TP2+:** the next building blocks, usually **3–4 TPs** (up to 5) [FjSiLFrg5fo@04:03; 6zXKK3Wrusg@03:07]. Skip an OB that envelops a high already used as a TP [FjSiLFrg5fo@06:49]. Don't base TPs on 1m confluences [FjSiLFrg5fo@09:06].
  - TP2 can be the 50% of an imbalance [RQSVIKddFHI@13:44].
  - Hourly liquidity range: target the start of the range that caused the drop, not the extreme above it [7MBD3ow7I1g@02:16–02:50].
  - A swept-then-reversed high: target the high itself, because the orders were filled from there upward [6zXKK3Wrusg@03:07–04:14].
- **Which timeframe:** the execution timeframe and one above, not 4H levels, for LTF trades [FjSiLFrg5fo@04:35–05:10]. Extended TPs are used when all biases align [z9p7OThLkr4@19:38]. Daily draws were used for a 1:13.5 plan, with partials [Y1lqifylC4s@19:43–20:48].
- **Greed rule:** don't keep extending the TP out of greed [CZRs2NuLQIw@06:42].

### 5.3 Partials and breakeven (canonical BC2)
- **At TP1:** close **50%** and move the stop to **BE**, making it a "risk-free trade" [Iu_v4kuFQhk@01:39; 7MBD3ow7I1g@02:16; Oi_mK1Lt-iQ@09:38; ss-dZPMnjeY@07:53].
- **At TP2:** close another 50% of the remainder; let TP3 run [ss-dZPMnjeY@05:06; IY9NJbaNyqA@03:59].
- BC1 statement: "when take profits were hit I moved my stop loss to break even" [z9p7OThLkr4@20:11; qecF411R83s@04:36].
- Beginners: always multiple TPs and BE [6zXKK3Wrusg@09:20].
- **BE mechanics:** drag the SL to the entry price [4aYaeI2Av2I@11:31]. Exact BE offset is unstated (OPEN).

### 5.4 Exits other than TP/SL
- **Hold rule:** don't close unless TP or SL is hit; closing early on floating P&L is emotional [z9p7OThLkr4@03:21; T4xVS7iV5d8@16:12]. He did not close 0.2 pips from TP2 [o_SdawM3DIE@26:20]. Don't exit on drawdown smaller than 50% of the stop distance [OH--4nkbXlM@08:25–10:04].
- **Exceptions he took:**
  - Closed at BE "because price was taking forever" [FjSiLFrg5fo@08:30].
  - Closed the runner on a 1m BOS against the position at HTF liquidity [ss-dZPMnjeY@05:06–05:40].
  - Exited on a 15m BOS against the position when the daily also opposed it [-rYGugTIsbU@15:08].
  - **Time exit about 2 pm ET** after 2–2.5 h of stagnation ("don't hold late in the day") [-rYGugTIsbU@17:19].
- **Counter-rule (BC2 D11):** "do not wait for a BOS against you to exit; take profit into levels, a 1m BOS can be a fake-out" [6zXKK3Wrusg@11:00–11:34]. See §11.
- **Holding period:** no holding over weekends or for 3–4 days [Y1lqifylC4s@12:55]. Asian-session holds happen with alerts at BE/TP2 [Iu_v4kuFQhk@01:39]. A within-monthly-bias trade "could have been held much further" [oJq8egtzCto@08:39] (swing context, not ES day-trade canonical).

### 5.5 Re-entry
- See 4.I. In BC1, after a loss you stop for the day [XcA0GiWZp7M@03:56; _jLR3XcB5eQ@12:21]. In BC2, re-entry is allowed under the 4.I conditions (§11).

### 5.6 Skill priority
- "The largest thing would be daily bias, then execution, then stop loss, then taking profits" [FjSiLFrg5fo@05:10]. "If you can get the bias down every single day ... that's how you're going to be a profitable trader" [7Q3nalPsSpk@11:18].

---

## 6. Risk management & sizing

| Item | Rule | Cites |
|---|---|---|
| Base risk | **1%** normal ("my normal risk is just one percent") | [KSiWKfPOlh4@14:44; TwakmPZJGJA@06:40; z9p7OThLkr4@02:48] |
| Cap | 1–3% **per day** total (the refined rule); 1–3% per trade in other places. More than 3% is "immediately doing something wrong" | [RkMBoqbeUq8@10:41; @03:26; CZRs2NuLQIw@05:36] |
| Sizing method | Set lot size: size so the **minimum typical stop** (ES ~4 pt) = 1%; then 8 pt ≈ 2%, 12 pt ≈ 3%. Or calculate per trade. Never full-port | [KSiWKfPOlh4@08:33–11:26; @01:07] |
| BC2 method | Compute contracts for 1% at the actual stop, then multiply by the tier factor | [7MBD3ow7I1g@06:10–06:43] |
| Tier: de-risk | **50%** on high-impact news days, pre/post bank holiday, anything likely to "mess up the market"; possibly a whole news-heavy week | [KSiWKfPOlh4@13:04; 1FunNCUw_jM@09:36–10:43; 7MBD3ow7I1g@04:29] |
| Tier: lesser news | **75%** (e.g. claims/PCE an hour before the open) | [7MBD3ow7I1g@04:29–05:05] |
| Tier: iffy technicals | **0.5%** instead of 1% | [7MBD3ow7I1g@07:52] |
| Tier: confident | **2×** normal: no news + favorite setup + all biases aligned. **Students must never use it until proven profitable** | [KSiWKfPOlh4@14:10–14:44; RkMBoqbeUq8@11:14; 7MBD3ow7I1g@05:38] |
| Reps | Below 1% = "reps" trades; 0.25% around Powell | [G7eq6U8e3yw@06:42; @01:41] |
| Counter-bias trade | If taken at all, about a tenth of normal size, and "don't take this trade" is the better choice | [-rYGugTIsbU@12:53; @15:41] |
| ES vs FX | He "generally risks less on S&P than forex" (habit, no reason given) | [7Q3nalPsSpk@06:14] |
| Trades/day | BC1: one trade a day, win or lose, then done; max 1–2. Beginners exactly one | [z9p7OThLkr4@05:01; 4moWbfm6smw@04:24; 065lMUrD_kg@09:05] |
| Two trades | De-risk each so the total equals one trade's risk | [065lMUrD_kg@07:59–08:32] |
| BC2 splitting | Expecting 2 trades → ~50% of the daily budget each. With 3 candidates, drop the weakest. Rank by (1) confluence, (2) daily-bias alignment, (3) RR | [5v4G4xJVKIQ@08:18; @10:03; @12:19] |
| BC2 dynamic budget | Trade 1 at 50%. After a loss (−50%) and a trade at TP1 + BE (net ~−25%), up to 75% may go on a third high-confidence setup. Worst case = 100% of the daily budget | [ss-dZPMnjeY@08:59–10:06] |
| Daily max loss | Pre-designated $/day in the trading plan (example "$100 a day while taking one trade"). His ~$10k loss ≈ 50% of his daily max ⇒ ~$20k (inferred) | [065lMUrD_kg@09:05; 5v4G4xJVKIQ@10:03] |
| Stop for the day | After a loss: done for the day (BC1/D51). BC2 allows re-entry within budget (§11) | [XcA0GiWZp7M@03:56; ss-dZPMnjeY@04:32] |
| Win → stop | After a win, don't search for more trades | [4moWbfm6smw@03:16; XcA0GiWZp7M@01:08] |
| Demo → live | Demo, one trade/day at 1%, about **3 months profitable with >10% gain** → small live account (~$100 at 1%) → funded or own capital (>$10k you can afford to lose) → payouts into live. If you blow up, go back to demo | [TwakmPZJGJA@06:40; @10:37; @12:17–13:23; @08:22] |
| Demo/live parity | Keep identical risk when going live; overconfidence trap | [4moWbfm6smw@12:12] |
| Red flag | A 10% day means you did something wrong | [TwakmPZJGJA@04:58] |
| Losing streak | Two or three losing **weeks**, not two losing days. Never change the strategy; make small tweaks only | [PyCPHiO2nj0@08:16; @01:02] |
| Pre-designate | Set risk on waking; no risk set → no trade | [065lMUrD_kg@05:50; @18:36] |

ES/MES translation (inferred, not TJR): 1% of $100k = $1,000. At a 4-pt stop: ES ($50/pt) = 5 contracts; MES ($5/pt) = 50 [KSiWKfPOlh4 notes]. Bot: size = floor(risk$ × tier / (stop_pts × $/pt)).

---

## 7. Time & session rules

- **Primary session:** NYSE open, AM session. "I take a trade within the first hour and a half." If not in a trade by **9:30 + 90 min = ~11:00 ET**, no trade that day. An open trade may run past 11:00 [065lMUrD_kg@10:12–11:18].
- **No pre-market entries:** "we're not going to take any trades that aren't off of market open or aren't after market open" [qecF411R83s@02:50; RQSVIKddFHI@12:35]. He "usually does not trade until the market opens" [7MBD3ow7I1g@06:43]. Entries are taken "when New York was actually open" [OH--4nkbXlM@05:09]. **Pre-market price action is still used for structure** (an hourly BOS up in pre-market set the bias [7MBD3ow7I1g@01:43]) and for liquidity (pre-market lows as TP [r-DdsJLUlBk@02:14]).
- **First trade is highest probability** (price & time theory). Later trades are lower-RR retracements [4moWbfm6smw@03:48–04:57].
- **Late session:** avoid. OB reactions weaken with low volume [LG_IbfjbaOo@06:20; S-scwzKRP-8@15:09; 9sD9kTia4V4@11:26]. Time exit about 2 pm ET on a stagnant trade [-rYGugTIsbU@17:19].
  - Exception: he "waited deep into the NY session" for a GU setup planned pre-market [ss-dZPMnjeY@13:25].
  - A PM-session short was floated as possible [r-DdsJLUlBk@02:14].
  - (Conflict with the 90-min rule, §11.)
- **S&P = NY session only:** "who's trading the S&P during London session" [sjuWqKDsQtI@14:48]. The majority of the S&P daily move happens in NY [sjuWqKDsQtI@05:08].
- **London:** OK for forex traders (wait for the London open) [RQSVIKddFHI@15:57; CZRs2NuLQIw@02:48]. Avoid GBP pairs around GBP news [9SUJfAo6Sl8@00:32; SV37R6j5f4M@10:03].
- **Asia:** "terrible session to trade" [065lMUrD_kg@10:47; CZRs2NuLQIw@02:48]. Nothing significant is expected there [Iu_v4kuFQhk@01:39]. Sunday Asian-open trades are mocked [XcA0GiWZp7M@06:08]. Exception: scouting Asia for GJ after London CPI [9sD9kTia4V4@12:30].
- **Execution timeframes:** S&P = **5m and 1m**; forex = 15m and 5m [UPA9LQW7phk@11:21]. He camps on the 5m to watch for a BOS [4aYaeI2Av2I@10:58]. HTF blocks on S&P: **1H preferred over 15m** [__fKQR5RR08@02:19].
- **Holidays:** no trading on US bank holidays (all markets slow) [1FunNCUw_jM@12:24; 065lMUrD_kg@19:41]. De-risk the day before [1FunNCUw_jM@09:36; KSiWKfPOlh4@13:04]. On a currency's holiday, don't trade its pairs [IY9NJbaNyqA@01:09]. He took July 4th off [KSiWKfPOlh4@00:00].
- **Session working window:** "murder it for the first hour and a half and then leave" [065lMUrD_kg@10:12]. Fully locked in for about 2 hours [OH--4nkbXlM@10:38]. Wakes about 4 hours before the open [OH--4nkbXlM@13:23].
- **Only trade what you see in session:** don't base a trade on a 4H candle that closes after the session [Oi_mK1Lt-iQ@00:35].
- **Weekly rest:** at least one full day off the charts per week [-ga9oK2bClQ@05:34].

---

## 8. News rules

1. **Never trade CPI, PPI, FOMC or NFP days.** "Those four I do not trade whatsoever ... just call it quits, sleep in" [w5sUCqFH3Lg@06:49; @22:30; qhuFg_OXdmE@11:24; S-scwzKRP-8@02:19; 7Q3nalPsSpk@12:58]. Also: Powell/Fed Chair speech days [4moWbfm6smw@16:19–18:31; sjuWqKDsQtI@04:01; K8DwhtmvAW8@06:52]; the core PPI + PPI + claims day [4FEty6xgOc0@01:08]; NFP Friday (with ISM PMI 30 minutes into the open) [IY9NJbaNyqA@02:17].
2. **Other red/orange (USD) folders:** never trade before the release. After it, wait **15–30 min** (an 8:30 release means re-evaluate around 8:45–8:50; news at 10:00 means no trade before about 10:30) [w5sUCqFH3Lg@04:02–05:41; @08:31–09:07; __fKQR5RR08@01:07; @09:45]. "Better to wait and miss the play than gamble on technicals pre-news" [__fKQR5RR08@09:12].
3. **Reaction gate:** if the news drastically moves the market (large wicks, large moves), stop for the day. If the reaction is muted, the day is lower probability: de-risk and take only a great setup [w5sUCqFH3Lg@06:16; @08:31]. Write a numeric cutoff ("if news causes an X-point spike within a 5-minute candle, I'm done"); his 5 pt / 5 min was only an example [065lMUrD_kg@12:26–13:00].
4. **Pre-open releases (BC2):** high-impact news **an hour before the open** → trade after 9:30, because the news "gives volume and direction" [IY9NJbaNyqA@01:45–02:17]. Pre-market releases 15–60 min before the open "should not do too much damage" [QRvZgj3k8pk@01:50]. But on a CPI day the pre-market news candle makes most of the move, so skip it [S-scwzKRP-8@02:19–03:24]. Unemployment claims can move the market so much pre-market that there is no reason to trade; be very selective [QRvZgj3k8pk@03:27].
5. **10:00 ET heavy news:** probably no trade, or only after the release [IY9NJbaNyqA@01:09].
6. **Sizing on news days:** 50% (high impact), 75% (lesser or pre-open), "maybe I don't even trade that day" [7MBD3ow7I1g@04:29–06:43; KSiWKfPOlh4@13:04]. Borderline setups on news days are "even more of a reason" to skip [7MBD3ow7I1g@07:16].
7. **News-heavy weeks:** "look for a reason not to trade, not a reason to trade" [w5sUCqFH3Lg@09:07]. He "might not trade for the rest of this week" [7Q3nalPsSpk@13:30].
8. **Low-impact items:** hide yellow folders [w5sUCqFH3Lg@01:42]. Consumer sentiment is tradable but wait for it [9SUJfAo6Sl8@02:07; __fKQR5RR08@01:07]. Philly Fed "doesn't do much" [QRvZgj3k8pk@03:27]. An FOMC member speech is not a concern [4FEty6xgOc0@01:08].
9. **Reading news:** actual vs. forecast plus the usual effect; good for USD = bad for SPX [w5sUCqFH3Lg@10:14–14:11]. BC1: informational only, price action is superior [w5sUCqFH3Lg@15:17]. BC2: news direction used for bias [7MBD3ow7I1g@01:43; r-DdsJLUlBk@05:34]. He let a bearish Empire print not change a structure bias [-rYGugTIsbU@00:00].
10. **Setup timing:** a setup during the release time is not tradable even if the pattern is perfect [S-scwzKRP-8@11:35]. In BC2 he was stopped by a news spike and concluded "wait for that high impact US news" [G7eq6U8e3yw@02:50].
11. **Daily routine:** check ForexFactory every morning [w5sUCqFH3Lg@24:09]. Build a weekly trading schedule from the calendar [QRvZgj3k8pk@01:50; IY9NJbaNyqA@01:09].

---

## 9. Psychology & discipline → hard bot constraints

| # | Constraint (bot form) | Source rule | Cites |
|---|---|---|---|
| P1 | Execute only if every trading-plan item is true; otherwise no trade ("does it follow your trading plan? if no, leave") | Robotic plan-following | [065lMUrD_kg@19:41; _jLR3XcB5eQ@11:48; 339amTioakE@03:22] |
| P2 | Default state = no trade; the market must supply the reason | "I do not want to trade today" | [339amTioakE@04:26; uGi6EeKnWSk@11:27] |
| P3 | Max trades/day: 1 baseline, 2 with split risk. Hard ceiling = daily risk budget | One trade a day; split | [z9p7OThLkr4@05:01; 5v4G4xJVKIQ@10:03] |
| P4 | Never increase size after a win or after a loss; tier is set pre-session only | No revenge, no overconfidence | [z9p7OThLkr4@04:29; _jLR3XcB5eQ@12:21; 4moWbfm6smw@05:29] |
| P5 | After the budget is used, or after a loss with no re-entry condition (4.I), stop for the day | "I'm done for today" | [XcA0GiWZp7M@08:53; ss-dZPMnjeY@08:59] |
| P6 | After a winning day's trade completes, no new search | Don't chase more | [4moWbfm6smw@03:16] |
| P7 | No manual early close on floating P&L; exits only by TP/SL/defined management rules | Hold to TP/SL | [z9p7OThLkr4@03:21; o_SdawM3DIE@26:20] |
| P8 | Never trade against the daily bias | Counter-bias = mistake | [uGi6EeKnWSk@02:20; -rYGugTIsbU@15:41] |
| P9 | Never enter without the third confirmation (ES) | BC2 mistake list | [SV37R6j5f4M@05:36] |
| P10 | Never use the confident tier until profitability is proven (live-validated) | Student rule | [KSiWKfPOlh4@14:44] |
| P11 | Live only after the demo criterion (~3 months profitable, >10%, 1 trade/day, 1%) | Demo → live | [TwakmPZJGJA@06:40] |
| P12 | Never full-port; never exceed 3%/day | Risk caps | [KSiWKfPOlh4@01:07; CZRs2NuLQIw@05:36] |
| P13 | Don't change the strategy on a losing streak; only targeted tweaks after ≥2–3 losing weeks with journal evidence | Losing streak | [PyCPHiO2nj0@01:02; @08:16] |
| P14 | Log every trade and no-trade with: instrument, session, risk, confluences HTF→LTF, plan followed Y/N, improvement | Journal template | [CZRs2NuLQIw@02:15–08:19; LG_IbfjbaOo@14:09] |
| P15 | Classify losses: "good loss" (all rules met, HTF reversal) vs "mistake loss" (rule skipped). Only good losses are acceptable | Best loss | [oJq8egtzCto@05:17; __fKQR5RR08@02:52; o_SdawM3DIE@15:45–17:24] |
| P16 | Evaluate on monthly/yearly %, not daily $ | Long horizon | [XcA0GiWZp7M@01:08; z9p7OThLkr4@07:16] |
| P17 | No trades from fundamentals or macro opinion | Charts over fundamentals | [UPA9LQW7phk@04:02; IY9NJbaNyqA@10:39] |
| P18 | One instrument until profitable (the bot: ES only) | One pair | [065lMUrD_kg@13:35; CZRs2NuLQIw@01:41] |
| P19 | Do not add components (indicators, SMT, etc.) | Don't over-complicate | [LG_IbfjbaOo@16:49–18:32] |
| P20 | Validate by forward/live testing; bar replay leaks HTF info (backtest without look-ahead) | Backtesting | [NPG_BZ_83fo@01:39; @04:30] |
| P21 | Process > outcome: a winning trade that broke rules counts as an error | Bad trade, made money | [7Q3nalPsSpk@10:09] |
| P22 | Don't wait so long that you settle: if the marked HTF block isn't hit, no trade (no substituting unmarked LTF sweeps) | Patience | [__fKQR5RR08@22:05] |

Human-only items (no bot equivalent): goal-setting, meditation, habits, morning routine, emotional-state days off [N7so8LEHmLA; 339amTioakE@11:36; OH--4nkbXlM@13:23–16:43].

---

## 10. Confluence inventory

"Videos" = the number of the 69 Boot Camp notes files that contain the concept. This is a keyword count (case-insensitive regex over `notes/*.md`), so it includes passing mentions and is approximate. Weight = TJR's stated importance, with the latest statement winning.

| Confluence | Videos | Stated weight (latest first) | Key cites |
|---|---|---|---|
| Break of structure (candle close) | 56 | **Required**. Confirmation and trigger; a bare BOS entry is retired for ES | [PmhuPbY8ZHo@12:57; ESsy0uoFAz4@01:38; PyCPHiO2nj0@03:18; 5v4G4xJVKIQ@03:22] |
| Liquidity sweep | ~52 | **Required** ("most essential thing") | [-ga9oK2bClQ@02:46; Lxnu7InGhGE@08:24; ss-dZPMnjeY@04:32] |
| Order block | 44 | BC1: first retracement choice. BC2: merged with accumulation, required as the zone (or an FVG/EQ) | [qhuFg_OXdmE@06:28; ESsy0uoFAz4@03:51; 9sD9kTia4V4@03:56] |
| FVG / imbalance / liquidity void | 44 | Retracement or confirmation tool. One of the third-confirmation options. "Not used for reversals." Small FVG plays: don't | [S1kY3Fw6JUQ@02:53; qecF411R83s@15:54; ss-dZPMnjeY@06:46; 9sD9kTia4V4@03:56] |
| Equilibrium / premium-discount | ~32 (strict) / 40 (incl. "50%", premium, discount) | Zone filter, the "bare minimum" for retracements. Never alone; EQ-only needs a close back | [Y1lqifylC4s@11:12; j1pVK897oZQ@08:35; 4FEty6xgOc0@04:59] |
| News filter | 36 | **Required** gate | [w5sUCqFH3Lg@06:49; 7MBD3ow7I1g@04:29] |
| 4H alignment | 31 | **Required at minimum with daily** ("at least daily and 4H in confluence") | [__fKQR5RR08@04:03; 9SUJfAo6Sl8@03:15] |
| Reaction candle / third confirmation | 27 (reaction) / 5 ("third confirmation/confluence") | **Required in BC2** (ES); not required in the Forex strategy | [ss-dZPMnjeY@06:46; SV37R6j5f4M@05:36; OH--4nkbXlM@02:23] |
| Daily bias | 26 | **Required**, the "largest thing" | [sjuWqKDsQtI@00:02; FjSiLFrg5fo@05:10] |
| Weekly context | 25 | Context only; the daily overrides it for intraday | [UPA9LQW7phk@05:11; 4FEty6xgOc0@08:47] |
| Market open timing | 24 | **Required** (NYSE open, first 90 min) | [065lMUrD_kg@10:47; 4moWbfm6smw@03:48] |
| Draw on liquidity | 18 | Targets and bias context | [KtC2SbemF6w@08:28; QRvZgj3k8pk@03:59] |
| Area of accumulation | 15 | **BC2 core zone** | [r-DdsJLUlBk@01:40; ss-dZPMnjeY@06:14] |
| Monthly context / monthly sweep | 13 | Strong bias driver in BC2 ("big picture") | [IY9NJbaNyqA@05:05; @14:34] |
| MSS / change of trend / CHoCH | 13 | Required in BC2 (as BOS/change of trend) | [ss-dZPMnjeY@01:43; S1kY3Fw6JUQ@07:57] |
| Session highs/lows (Asia/London/NY/pre-market) | 10 | Required in the Forex strategy. Liquidity and TP for ES | [OH--4nkbXlM@03:32; r-DdsJLUlBk@02:14] |
| HTF building block hit first | (in most BC2 files) | **Required** ("don't settle for anything less") | [__fKQR5RR08@22:05; 9sD9kTia4V4@03:56] |
| Prominent high/low | 4 | **Required** for BOS validity in BC2 | [5v4G4xJVKIQ@03:22; 6zXKK3Wrusg@01:27] |
| Multi-TF alignment (all TFs) | (many) | Strong; condition for the confident tier and extended TPs | [UPA9LQW7phk@13:06; KSiWKfPOlh4@14:10; z9p7OThLkr4@19:38] |
| Trending vs chop character | (many) | Strong; chop = no trade | [uGi6EeKnWSk@06:28; IY9NJbaNyqA@14:34] |
| LTF liquidity sweep inside the HTF zone | — | "Ideal extra" / strong | [qecF411R83s@12:33; K8DwhtmvAW8@07:59] |
| Base of the OB body (reaction point) | 1 | Refinement (his drawing) | [12_F-mIUfL0@11:27] |
| Nested accumulation | 1 | High confluence | [IY9NJbaNyqA@12:21] |
| News direction (actual vs forecast) | (in news files) | BC1: informational only. BC2: bias input | [w5sUCqFH3Lg@22:30; 7MBD3ow7I1g@01:43] |
| DXY inverse read | 1 | Informational | [w5sUCqFH3Lg@13:01] |
| Single-candle reads (doji, wick) | 4 | Minor, "only one confluence" | [bEkbNGUzQME@14:25] |
| Wyckoff spring / range breakout | 2 | Optional, confidence to **hold** | [o_SdawM3DIE@21:48] |
| Line chart (weekly) | 3 | Optional tool | [sjuWqKDsQtI@11:32] |
| Weekly open | 1 | Reference only | [IY9NJbaNyqA@06:12] |
| 30-minute high (forex) | 1 | Required for the forex short in that example | [9sD9kTia4V4@14:45] |
| Post-BOS dip entry | 1 | Optional refinement (forex) | [OH--4nkbXlM@04:04] |
| Fibonacci (levels other than 0.5) | 2 | **Don't use** for TPs. The 0.5 is just EQ | [6zXKK3Wrusg@05:59; -E7plUbSJUk@07:19] |
| Support / resistance | 3 | **Don't use** | [Lxnu7InGhGE@01:05; d0AxLACYaqU@01:40] |
| SMT divergence | 1 | **Don't use** ("I don't trade it") | [_6voYEdi5j4@05:00] |
| "Divergence" (gold) | 1 | Undefined | [9SUJfAo6Sl8@07:09] |
| ICT Silver Bullet | 2 | Not used ("is a fair value gap") | [4moWbfm6smw@14:38; _6voYEdi5j4@08:24] |
| Trend lines, indicators, EMA crosses, multi-candle patterns | 1–3 | **Don't use** | [IY9NJbaNyqA@05:05; ESsy0uoFAz4@07:10; bEkbNGUzQME@07:21] |
| IFVG | 0 | Not present | — |
| "Market experience" trades | 1 | Discretionary; exclude from the bot | [o_SdawM3DIE@07:09] |

---

## 11. Contradictions & evolution log

Each item gives both sides, the dates, and the resolution for the bot (later = BC2 unless noted).

1. **SMT divergence.**
   - **Side A (BC1 D7, 2023-06-01):** "I don't trade it and I don't even know what it is" [_6voYEdi5j4@05:00–05:35].
   - **Side B:** no later Boot Camp mention.
   - **Resolution:** excluded. Flag for the 250-video pass (later TJR material may use it).
2. **EQ + BOS sufficiency.**
   - **Day 26:** "even just a break of structure while in a discount — that's enough reason for me to get in" [j1pVK897oZQ@08:35].
   - **Day 28:** EQ + BOS only is "not much confirmation" [-E7plUbSJUk@07:19].
   - **Day 48 pt2:** EQ-only needs a candle close back beyond EQ plus a new BOS [4FEty6xgOc0@04:25–04:59].
   - **BC2:** EQ is one of the third-confirmation options, with a reaction [ss-dZPMnjeY@06:46].
   - **Resolution:** EQ + BOS alone is insufficient. EQ counts only with a close back beyond 0.5, or with an overlapping FVG/OB.
3. **Risk per trade vs per day.**
   - "1–3% per trade" [RkMBoqbeUq8@03:26; CZRs2NuLQIw@05:36] vs "1–3% per day, that just makes it easy" [RkMBoqbeUq8@10:41]. "1% per trade/day" [TwakmPZJGJA@06:40]. Daily $ budget [065lMUrD_kg@09:05].
   - **BC2:** daily budget split across trades (50/50, dynamic 50/25/75) [5v4G4xJVKIQ@10:03; ss-dZPMnjeY@08:59].
   - **Resolution:** a daily budget (normal 1%, cap 3%) allocated across ≤2 ideas.
4. **Entry on the BOS vs. third confirmation.**
   - **BC1 D12/D18/D30:** enter on the BOS candle close (model 1) [KtC2SbemF6w@10:45; qecF411R83s@03:25; ESsy0uoFAz4@03:18].
   - **D41 (2023-07-06):** stop entering on a bare LTF sweep + BOS [PyCPHiO2nj0@02:10].
   - **BC2 D1/D9/D12:** wait for the third confirmation; a BOS entry was the mistake [o_SdawM3DIE@07:09; ss-dZPMnjeY@06:46; SV37R6j5f4M@05:36].
   - **Counter (BC2 D2/D3, forex):** "my forex strategy doesn't necessarily need to wait for a third confluence"; entries on the BOS close [OH--4nkbXlM@02:23; G7eq6U8e3yw@02:13].
   - Also D52: a GU entry on the BOS, but that trade was a self-admitted mistake for other reasons [-rYGugTIsbU@13:28].
   - **Resolution:** ES requires the third confirmation. The forex exception stays forex-only.
5. **OB entry: touch (limit) vs reaction.**
   - "If it hits the order block I'm instantly entering" [j1pVK897oZQ@14:13]. "We enter at the order block" [ESsy0uoFAz4@04:25]. FVG "or just for it to get hit" [ESsy0uoFAz4@04:58].
   - Versus: wait for a reaction or LTF BOS [S1kY3Fw6JUQ@07:57; RQSVIKddFHI@13:09]. "Do not enter immediately on an FVG fill" [ss-dZPMnjeY@02:50].
   - **Resolution (BC2):** reaction or LTF BOS required.
6. **Order block definition.**
   - (a) The whole leg that swept liquidity before the BOS [RQSVIKddFHI@06:47].
   - (b) TJR's drawing: wick to the start of the body of the extreme candle [12_F-mIUfL0@10:20].
   - (c) "Last up-move before the bearish displacement" / "the candle that caused the highs to be taken" [o_SdawM3DIE@04:52; SLhIA7vW9x8@10:56].
   - (d) A consolidation or accumulation can be an OB [-E7plUbSJUk@10:08]; "just an area where orders were filled prior" [5v4G4xJVKIQ@06:06].
   - **Resolution:** in BC2 the OB and the area of accumulation are the same zone. Implement both the leg box and the wick-to-body refinement, and log which reacts (OPEN).
7. **One OB per trend vs. multiple/nested zones.**
   - "There's only one order block within every single trend" [qhuFg_OXdmE@09:13].
   - Versus: nested accumulations [IY9NJbaNyqA@11:47]; two accumulation areas on the 15m [SV37R6j5f4M@04:27]; 5m OB inside a 1H OB [Y1lqifylC4s@19:09]; OB-to-OB chains [12_F-mIUfL0@09:47–15:21].
   - **Resolution:** one OB per trend *per timeframe* (inferred). Many zones exist across timeframes.
8. **Trades per day.**
   - One trade/day [z9p7OThLkr4@05:01; 339amTioakE@11:03; TwakmPZJGJA@06:40]. 1–2 [4moWbfm6smw@04:24; 065lMUrD_kg@07:59]. Max 2 in the example [5v4G4xJVKIQ@11:13].
   - Three trades in a day [ss-dZPMnjeY]. "Takes up to four trades a day himself" [SV37R6j5f4M@02:13].
   - **Resolution:** the budget-limited count; bot default ≤2 ideas, with a re-entry counting within the same idea.
9. **Stop after a loss vs. same-day re-entry.**
   - "When you lose ... I'm done for today" [XcA0GiWZp7M@08:53]. Stopped after a GU loss [_jLR3XcB5eQ@12:54]. No additional trade after the $9.5k loss [__fKQR5RR08@20:58].
   - Versus BC2: re-enter if the bias is not invalidated and risk budget remains [ss-dZPMnjeY@04:32; SV37R6j5f4M@03:55].
   - **Resolution:** BC2 re-entry rule (4.I), capped by the daily budget.
10. **Time window.**
    - "Within the first hour and a half ... or else I'm done" [065lMUrD_kg@10:47]. Avoid late session [9sD9kTia4V4@11:26].
    - Versus: waited "deep into the NY session" for GU [ss-dZPMnjeY@13:25]; a PM-session short was considered [r-DdsJLUlBk@02:14]; the evening/Asian pre-market ES long [Iu_v4kuFQhk@00:00].
    - **Resolution:** the ES bot keeps 9:30–11:00 for entries. Later exceptions were forex or discretionary (OPEN).
11. **News bias as bias input.**
    - "News bias ... is not the day's bias"; "price action is superior" [w5sUCqFH3Lg@15:17; @22:30].
    - Versus BC2: "bullish news + hourly BOS up = bullish day" [7MBD3ow7I1g@01:43]; unemployment claims gave a bearish bias and he looked only for shorts [r-DdsJLUlBk@05:34].
    - **Resolution:** news direction is a secondary bias input, subordinate to structure (inferred).
12. **Trading on news days.**
    - Never CPI/PPI/FOMC/NFP [w5sUCqFH3Lg@06:49].
    - Versus: traded a GDP + NFP-week day at 50% [7MBD3ow7I1g@04:29]. "High-impact news an hour before the open → trade after the open, the news gives volume" [IY9NJbaNyqA@01:45]. Versus "most of the move has already been made" on a CPI day [S-scwzKRP-8@02:19].
    - **Resolution:** the big four (+ Fed Chair) = no trade. Other high-impact pre-open news = trade after the open at 50–75%.
13. **Stop placement.**
    - Beyond the sweep [1FunNCUw_jM@01:08] vs beyond the BOS swing [-E7plUbSJUk@12:21] vs "above the previous high" [S1kY3Fw6JUQ@09:04] vs under the 5m low [oJq8egtzCto@04:44] vs tightened to a nearer high [r-DdsJLUlBk@04:27].
    - BC2 D9 explicitly corrects a fixed tight stop to "under the invalidation point" [ss-dZPMnjeY@05:06].
    - **Resolution:** invalidation (sweep extreme or accumulation low) + buffer.
14. **Exiting on an opposing BOS.**
    - Closed the runner on a 1m BOS against [ss-dZPMnjeY@05:06]; exited on a 15m BOS against [-rYGugTIsbU@15:08].
    - Versus "do not wait for a BOS against you to exit; take profit into levels; a 1m BOS can be a fake-out" [6zXKK3Wrusg@11:00].
    - **Resolution (latest):** TP into levels. An opposing BOS is not the primary exit (OPEN for runners).
15. **TP timeframe.**
    - The execution TF and one above, not 4H levels [FjSiLFrg5fo@04:35].
    - Versus daily draws at 1:13.5 [Y1lqifylC4s@20:48]; monthly highs [IY9NJbaNyqA@14:01]; TP4/5 at HTF highs [6zXKK3Wrusg@03:07].
    - **Resolution:** TP1 on the execution TF +1; later TPs may ladder to HTF.
16. **Weekly vs daily.**
    - Day 21 journal: weekly + daily must agree [z9p7OThLkr4@19:38].
    - Versus: the daily overrides the weekly for intraday ("that don't matter because the daily is telling us bulls") [Oi_mK1Lt-iQ@04:29; 4FEty6xgOc0@08:47].
    - BC2: trade within monthly/weekly/daily sentiment [IY9NJbaNyqA@14:34].
    - **Resolution:** the daily governs direction. Weekly/monthly alignment raises quality (confident tier, extended TPs).
17. **Counter-daily retracement trades.**
    - "Never trade retraces" [4FEty6xgOc0@09:54]; a counter-daily GU trade was a mistake [-rYGugTIsbU@15:41].
    - Versus BC2 D11: a GU long with the daily bearish after an hourly breakout of prominent highs, 3 TPs hit, presented as the model [6zXKK3Wrusg@00:55; @04:05]. And D13: a GU long against the 4H, "not one he'd always take" [7Q3nalPsSpk@09:00].
    - **Resolution for ES bot:** keep the no-counter-daily rule. The D11 counter-daily case is a forex outlier (OPEN).
18. **FVG as entry.**
    - "I don't use fair value gaps for entries necessarily" [d0AxLACYaqU@03:54]; "more of a confirmation than an entry" [qecF411R83s@15:54].
    - Versus model 3 [ESsy0uoFAz4@04:25].
    - **Resolution:** FVG = zone + confirmation location, never a touch entry.
19. **BOS strictness.**
    - Body close required [PmhuPbY8ZHo@12:57] vs "big extension up" counted as a BOS [IY9NJbaNyqA@05:05].
    - BC2 adds the prominent-swing requirement [5v4G4xJVKIQ@03:22].
    - **Resolution:** a body close beyond a **prominent** swing.
20. **Sweep: wick vs close.**
    - A wick, or "a close below them — both acceptable" [UPA9LQW7phk@10:49]. Barely wicked counts [KtC2SbemF6w@13:02].
    - Versus "taken out, not just tapped" near news [G7eq6U8e3yw@02:13]; "wait for the NY lows to be fully taken out" [OH--4nkbXlM@06:14].
    - **Resolution:** require trade-through. The minimum distance is OPEN.
21. **Liquidity sweep vs. HTF block priority.**
    - The sweep is the core signal [-ga9oK2bClQ@02:46] vs the HTF block must be hit first and an unmarked LTF sweep is the error [__fKQR5RR08@21:32].
    - 7Q3n: "maybe wait for the whole 15m area of accumulation to be hit, may be higher confluence than just the sweep" [7Q3nalPsSpk@04:01].
    - **Resolution:** HTF block first, then the LTF sweep.
22. **Instrument focus.**
    - S&P is his plan instrument [065lMUrD_kg@18:03] vs moving to forex because of bad S&P price action [PyCPHiO2nj0@01:02] and "stepping away from S&P" [G7eq6U8e3yw@07:15], yet trading ES days later [Iu_v4kuFQhk; 7MBD3ow7I1g].
    - Risks less on S&P [7Q3nalPsSpk@06:14].
    - **Resolution:** the ES bot should carry a regime filter for "bad price action" (OPEN).
23. **Premium/discount wording.** He repeatedly says "discount" for a bearish retracement zone [Y1lqifylC4s@11:12; UPA9LQW7phk@08:33; o_SdawM3DIE@15:10] and "smart money ... short in a discount" [-E7plUbSJUk@01:45]. **Resolution:** use the standard definitions (shorts ≥ 0.5, longs ≤ 0.5) (inferred).
24. **Learning source.** "Did not learn from ICT" [Xq6-oO2n6-U@36:30] vs "ICT came up with this (liquidity)" [rdz6vnXb8wE@14:59]. Non-operational.
25. **Session marking.** BOS/OB logic uses wicks for swing prices [PmhuPbY8ZHo@04:25], while session highs/lows are marked as body-to-wick zones [OH--4nkbXlM@02:23]. **Resolution:** session levels are zones; swing BOS levels are wick prices.

---

## 12. Ambiguities / gaps to resolve with later videos

1. **"Prominent" swing:** no numeric definition [KtC2SbemF6w@03:28; 5v4G4xJVKIQ@03:22]. Need: size or significance criteria per timeframe.
2. **Area of accumulation boundaries:** which candles; leg vs chop; wick or body. The promised BC2 "strategy video" is not in this set [Iu_v4kuFQhk@00:32; oJq8egtzCto@03:38; ss-dZPMnjeY@01:10].
3. **Reaction candle definition:** body size, close location, how many extra candles are allowed [339amTioakE@08:21; oJq8egtzCto@04:44].
4. **Sweep depth:** minimum ticks beyond the level; wick vs close; does the sweep need to happen in session? [UPA9LQW7phk@10:49].
5. **Which liquidity counts as the LTF sweep for ES:** hourly lows, pre-market lows, session lows, 15m lows. Hierarchy unstated.
6. **Invalidation trigger:** a wick through the sweep extreme vs a close beyond it [ss-dZPMnjeY@04:32].
7. **Exact time window:** whether the entry cutoff is 11:00 ET (first 90 min) or later; PM session usage; how "late" is defined [065lMUrD_kg@10:47; 9sD9kTia4V4@11:26; -rYGugTIsbU@17:19].
8. **Session clock definitions** for Asia, London and pre-market (not stated).
9. **News volatility cutoff:** an "X-point spike in a 5-minute candle" with X unspecified for ES [065lMUrD_kg@12:26]. Wait 15 vs 20 vs 30 min [w5sUCqFH3Lg@05:08].
10. **Which news is "high impact"** beyond the big four + Powell. GDP/PCE/claims/ISM treatment varies [7MBD3ow7I1g@04:29; QRvZgj3k8pk@03:27].
11. **BE trigger and offset:** always at TP1? Exactly at entry? [7MBD3ow7I1g@02:16]. Partial % at TP3+.
12. **Number of TPs, and runner exit logic** (time exit, opposing BOS, or final HTF level) [FjSiLFrg5fo@04:03; 6zXKK3Wrusg@11:00].
13. **Intraday bias update after the open** (flagged, not taught) [O_4yHzZO0u0@06:41]. Rules seen: a 1H close above a lower high, a 15m high closed above [-rYGugTIsbU@18:25; Oi_mK1Lt-iQ@00:35].
14. **How to choose among multiple HTF zones** (pre-mark all and trade whichever is reached [UPA9LQW7phk@12:31] vs prefer 1H over 15m [__fKQR5RR08@02:19] vs prefer HTF OB over small FVG [9sD9kTia4V4@03:56]).
15. **EQ anchoring:** which swing pair to use when several legs exist; re-anchor frequency [-E7plUbSJUk@06:46].
16. **OB drawing:** whole leg vs wick-to-body; which candle is "the" OB candle when the leg is multi-candle [12_F-mIUfL0@10:20].
17. **Confident tier criteria** in operational terms ("setup he loves") [KSiWKfPOlh4@14:10].
18. **Chop / "bad price action" detection** for a regime filter [PyCPHiO2nj0@05:32; uGi6EeKnWSk@04:39].
19. **Weekly retrace extent:** how far a daily counter-move is expected to go, and TP moderation [Y1lqifylC4s@11:12].
20. **Daily max loss as % of the account** (only $ figures implied) [5v4G4xJVKIQ@10:03].
21. **Stop buffer on ES:** 0.5 pt stated, but the example mentions "four below" [1FunNCUw_jM@05:44; @07:23].
22. **Day-of-week effects, holidays list, half-days:** only US bank holidays are mentioned.
23. **SMT, IFVG, and any NQ-related tools:** absent; check later videos.
24. **Re-entry limits:** how many re-entries per idea; whether the remaining budget is a fixed % [ss-dZPMnjeY@09:34].
25. **"4H BOS confirms daily"** [9SUJfAo6Sl8@03:15]: is a 4H BOS in the bias direction required before entries, or only preferred? [uGi6EeKnWSk@02:53] lists it in the A-setup checklist.
26. **Displacement size / "very obvious volume"** for a valid breakout [7Q3nalPsSpk@07:19].

---

## 13. Trade example index

Legend. Type: **L** = live (taken), **M** = mock/paper, **H** = hindsight/backtest/hypothetical, **S** = skipped (planned but not taken), **I** = generic illustration. Outcome is as stated in the notes. "—" = not stated.

### 13.1 Boot Camp 1

| Cite | Date | Inst. | Dir | Type | Setup sequence | Outcome |
|---|---|---|---|---|---|---|
| Xq6-oO2n6-U@37:05 | historical | GJ | S | L | London open takes a high → sell; 15-pip stop | his "start to profitability" |
| bEkbNGUzQME@09:44–20:03 | — | S&P 5m; gold D/W | — | I | Candle reads: upper-wick weakness, momentum-loss doji, doji in downtrend (no long), strong close, exhaustion | no trades |
| viuGHEuv0nw@04:26 | — | Gold D | — | I | HH/HL then a lower low = BOS | — |
| viuGHEuv0nw@12:49–20:01 | ~2023-05-28 | Gold 30m | S | S | Daily bearish; consolidation broken down; wait for EQ/premium + 5m/15m shift in NY | forecast only |
| PmhuPbY8ZHo@08:54–11:15 | — | Gold W/D | both | I | Body closes below/above the most recent swing = BOS | — |
| PmhuPbY8ZHo@12:21 | — | Gold | — | I | Wick above high, no close = not a BOS; price fell | — |
| PmhuPbY8ZHo@22:47–24:33 | — | GU D/W | — | I | Daily BOS down inside bullish weekly = retrace; weekly wick below low = sweep | — |
| PmhuPbY8ZHo@25:06 | — | GJ | L-bias | I | Repeated wicks below lows, no close → trend intact | — |
| rdz6vnXb8wE@07:47 | — | S&P D | S | I | Daily highs taken → sell-off (×2) | — |
| rdz6vnXb8wE@08:20 | — | USD pair? M/Y | L | I | Monthly/yearly low swept | reversal expected |
| rdz6vnXb8wE@09:57 | — | GU 15m Asia | L | I | Lows taken → BOS up | pushed higher |
| rdz6vnXb8wE@12:46 | — | — W/M | L | I | Monthly low swept → weekly BOS up | rally |
| _jLR3XcB5eQ@01:07 | 2023-06-05 | GU | — | L | No setup details | ≈ −$9–10k; stopped for the day |
| KtC2SbemF6w@04:34–12:28 | — | S&P D | S | I | Prominent high swept → BOS (close below low) → 4H FVG entry option → prior lows; repeated | targets hit |
| KtC2SbemF6w@13:02 | — | GU 4H/1H | S | I | 4H highs unswept but 1H sweep → BOS → OB retrace → prominent low | TPs |
| KtC2SbemF6w@14:11 | — | GU 5m | S | I | Highs barely wicked → BOS → 5m imbalance fill → short | lows |
| KtC2SbemF6w@14:48 | — | Gold | L | I | Lows swept, regained close above → imbalance dip entry | previous highs |
| S1kY3Fw6JUQ@05:42–11:53 | — | n/s | both | I | BOS → FVG retrace → reaction or LTF BOS → continuation; stop beyond prior high, target lows | — |
| qecF411R83s@01:41–05:10 | ~Jun 2023 | ES | S | L | 15m BOS down; pre-market FVG tap ignored; open pushes into 5m imbalance → 1m BOS close → short; targets liquidity + small OB | TP1 + TP2, rest BE |
| qecF411R83s@05:42–07:57 | — | GJ 15m/5m | S | I | HTF highs swept → 15m BOS → 5m BOS up = retrace → FVG fill → 5m BOS down → short | all TPs |
| qecF411R83s@08:34–10:55 | — | GU (or gold) 4H | S | I | 4H BOS down; first imbalance traded through (discarded); second + liquidity spike → 15m BOS → short | targets prior liquidity |
| qecF411R83s@10:55–14:47 | — | n/s 1H/4H | L | I | Daily BOS up → 1H BOS up → refined 1H imbalance → doji → 15m BOS → long | missed TP1, then rally |
| w5sUCqFH3Lg@04:02 | 2023-06-13 CPI | GJ, gold | — | S | Massive CPI wicks | no trade |
| qhuFg_OXdmE@11:59 | 2023-06-14 PPI/FOMC | GJ 15m | — | S | 34 pips since US open | no trade |
| z9p7OThLkr4@02:15; @20:47 | ~Jun 2023 | n/s | — | L | −$14k morning; earlier ~$60k day (all aligned, rest BE) | — |
| RQSVIKddFHI@03:49–05:39 | — | forex D/1H | L | I | BOS up; OB = down candle (swept lows); retrace into OB → rally | — |
| RQSVIKddFHI@06:47–10:19 | — | 4H/1H | S | I | 4H play needs a stop beyond the 4H swing, not a 1H-BOS stop | — |
| RQSVIKddFHI@10:54–14:51 | — | GU D→15m | L | L ("we took this") | Daily OB → 4H BOS → 1H sweep + BOS up → 1H OB fill → wait 9:30 → 15m BOS long; TP1 liq, TP2 imbalance 50%, TP3 HTF highs | ~1:12 RR |
| RQSVIKddFHI@15:25–17:41 | — | forex 15m London | L | I | Sweep → BOS → 1H OB → after London open 15m BOS; second FVG respected → long | TP1 hit |
| RQSVIKddFHI@18:15 | — | GJ | L | I | Sweep, BOS, OB fill, rally | — |
| RQSVIKddFHI@20:04–21:17 | — | 4H→15m | L | I | 4H BOS up → 4H OB → 15m BOS close; stop under swing/OB | all TPs |
| RQSVIKddFHI@22:56 | — | n/s | S | I | Sweep candle = OB → BOS → OB retrace → 15m BOS short | all TPs |
| 12_F-mIUfL0@09:47–15:21 | — | forex | L | I | Sweep, leg down = OB, tap base of body → BOS up | liquidity |
| 12_F-mIUfL0@15:21–17:36 | — | Gold | L | H | Sweep lows → BOS up; FVG first, OB next; 15m BOS within smaller OB/FVG | — |
| 12_F-mIUfL0@18:16; @19:58–21:42 | — | GBP pairs | S / L | I | OB retrace → 1H BOS short; Daily BOS up → daily OB → 4H BOS → 1H OB → BOS long | liquidity |
| 12_F-mIUfL0@22:16–26:15 | — | various | both | I | Large OB, BOS only on 15m; already-inside-OB options; bearish base-of-body touch | — |
| 4moWbfm6smw@03:16 | 2023-06-21 | n/s | — | L | Same-day trade | all TPs |
| j1pVK897oZQ@13:39 | ~Jun 2023 | n/s | — | L | BOS but bad RR → wait for OB (instant) or FVG reaction | — |
| -E7plUbSJUk@05:40–06:13 | — | forex D | S | I | Above EQ, FVG fill, liquidity taken → BOS → short | all TPs |
| -E7plUbSJUk@07:53–09:34 | ~2023-06-23 | forex 15m | L | L | Re-anchor until discount; imbalance fill; BOS up → long ("caught a long off this today") | win (inferred) |
| -E7plUbSJUk@09:34–12:21 | — | various | L | I | 1H BOS bad RR → wait EQ → 15m BOS → long; EQ + imbalance + HTF OB → 1H BOS | targets liquidity |
| -E7plUbSJUk@12:55 | — | Gold M | L | H | Monthly EQ; look for FVG/OB, 4H BOS | — |
| -E7plUbSJUk@14:36–16:15 | "a while ago" | n/s | S | L (Discord) | Daily BOS down → daily EQ premium → 4H massive imbalance → 1H BOS down → short | 3 of 4 TPs |
| SLhIA7vW9x8@04:36–05:42 | — | forex | L | I | Sweep → BOS up → draws to highs; BOS-up failure because the HTF draw was below (needs daily bias) | — |
| SLhIA7vW9x8@10:20–15:50 | — | forex, GU, daily | both | I | Sweep → BOS → OB retrace entry | follow-through |
| SLhIA7vW9x8@16:27 | — | ES LTF | L | I | Sweep → BOS → weak OB, refine on 5m → rally | — |
| K8DwhtmvAW8@06:52 | ~2023-06-28 | ES 15m | L | S | Lows swept → 15m BOS up → FVG retrace → LTF BOS; stop under lows | not taken (Powell) |
| K8DwhtmvAW8@07:59–10:18 | — | ES?/HTF/1H | both | I | FVG retrace (+15m sweep) → previous liquidity; full imbalance fill | — |
| K8DwhtmvAW8@16:12–19:49 | — | Daily/HTF | L | I | EQ of the BOS leg matches FVG "on the money" | — |
| K8DwhtmvAW8@22:27 | — | n/s | L | I | Sweep, BOS, OB, EQ wick, 5m OB, 5m FVG, BOS (7 confluences) | rips |
| sjuWqKDsQtI@04:01–06:48 | 2023-06-29 | ES | S | S | Daily bear, 4H bull; hypothetical high taken → 15m BOS down → 15m OB | not traded (Powell) |
| sjuWqKDsQtI@08:27–10:45 | — | ES | L | I | Daily BOS up → 4H retrace into EQ + FVG → 1H BOS → NY open long; refine 15m/5m | — |
| sjuWqKDsQtI@14:14–18:12 | 2023-06-29 | ES | S | S/L? | 4H sweep highs → 1H BOS down (London) → FVG + OB + EQ → wait for 5m BOS | considering it; unknown |
| UPA9LQW7phk@03:29 | 2023-06-29 | ES | S | L | Daily sweep + daily BOS, no LTF confirmation | loss implied; "messed up" |
| UPA9LQW7phk@10:13–13:06 | 2023-06-30 | ES | L | S | All TFs up; zones: 1H lows, 15m OB, imbalances; 5m/1m BOS entry | see recap |
| UPA9LQW7phk@05:11–06:51 | 2023-06-30 | GU | S | S | Weekly bull, daily bear retracing; 4H FVG + OB; need 15m BOS | not triggered |
| UPA9LQW7phk@08:33 | 2023-06-30 | Gold | S | S | W/D bear retracing; EQ, FVG; wait sweep + 15m BOS | doubtful |
| Y1lqifylC4s@06:06 | ~2023-06-30 | ES | — | S | Not much 4H confluence | no trade |
| Y1lqifylC4s@12:21–14:36 | ~2023-06-29/30 | GU | S | L | Weekly up, daily down; 4H retrace past 50% into 4H OB + 1H OB → 15m/5m BOS → short; TPs low, 50%, liquidity, daily OB | took shorts |
| Y1lqifylC4s@15:44–20:48 | ~2023-07-01 | Gold | S | S | Daily down; 4H BOS up = daily retrace past 50%; 1H OB; wait 15m BOS | RR 1:4.79 / 1:13.5 planned |
| FjSiLFrg5fo@02:24–07:23 | — | various | both | I | TP illustrations (counter-trend short = "bad trade"; FVG long TP1 ≈1:1; TP ladder) | — |
| FjSiLFrg5fo@08:30 | ~2023-06-30 | ES | S | L | 1H OB → 5m BOS → 1m OB entry; TP1 5m OB | closed BE (slow) |
| 1FunNCUw_jM@05:09–12:58 | 2023-07-03 | ES | L | L | Daily bull; 5m sweep → 1m BOS close long; stop under 5m sweep; half size (news + holiday) | stopped by a wick; price then rallied |
| PyCPHiO2nj0@06:38 | ~early Jul 2023 | EU (inferred) | S | L | Bare sweep + BOS entries ×2 | both stopped; price then fell his way |
| PyCPHiO2nj0@06:38 | same | Gold / GU | S / L | L | — | deep profit / would hit TP1–2 |
| 9SUJfAo6Sl8@02:41–08:14 | wk of 2023-07-10 | S&P, GU, GJ, gold | various | S (plan) | Weekly plans: S&P buys Mon–Tue after SSL taken; GU targets imbalance/weekly liq; GJ watch 4H; gold bearish until weekly BOS up | — |
| uGi6EeKnWSk@02:20–07:33 | — | S&P / GJ / n/s | — | H | A-setup checklist; conflicting TFs avoid; daily + 4H aligned but 1H chop → no trade | — |
| CZRs2NuLQIw@00:00 | ~2023-07-11 | ES | — | L | Sweep + BOS + wait for OB/FVG entry | running to TP3 |
| S-scwzKRP-8@01:10–04:31 | ~2023-07-12 CPI | ES | L | H | All TFs bull; 5m BOS down into OB = counter-bias (skip); later 5m BOS up = possible long | small move; probably no trade |
| S-scwzKRP-8@06:31–09:17 | same | GJ | S | H | NY into London high → BOS down → short; stop above | "could have caught something good" |
| S-scwzKRP-8@09:52–14:35 | same | Gold / GU | L | H | Conflicting TFs + CPI; 4H bull/1H bear with no FVG/OB/EQ | avoided |
| 4FEty6xgOc0@02:46–05:31 | ~2023-07-13 PPI | ES | L | M | PPI sweeps 15m/1H lows → 15m BOS up → EQ retrace; wait for close back above EQ + BOS → long; stop under sweep | ~+1.6R, two TPs |
| 4FEty6xgOc0@06:04–13:14 | same | GJ / gold / GU | — | S | 1H not aligned; conflict; marked OB never hit | no trades |
| __fKQR5RR08@18:44–28:10 | 2023-07-14 | ES | L | L | All TFs bull; marked 1H OB; took an unmarked LTF sweep → BOS → EQ rejection close → long; stop below wick | ≈ −$9.5k; price later hit the marked 1H OB/FVG and rallied |
| __fKQR5RR08@03:25–11:59 | same | GJ / gold / GU | — | S | Daily/4H conflict; gold 5m BOS barely 1:1; GU daily retrace | not taken |
| QRvZgj3k8pk@03:59–09:35 | wk of 2023-07-17 | S&P, gold, GU, GJ | various | S (plan) | S&P retrace into 4H FVG + EQ + OB then highs; gold trade daily bull; GJ wait 4H BOS down → shorts to weekly EQ | — |
| -rYGugTIsbU@12:20–18:00 | 2023-07-17 | GU | S | L | Counter-daily; Asian highs swept → BOS down entry; 15-pip stop; 15 lots (~1/10); exit on 15m BOS up ~2 pm | +$199 ≈ BE; "don't take this trade" |
| -rYGugTIsbU@06:39–08:17 | same | GJ | S | S | Daily bear, daily OB tapped, 1H BOS down; price went past his level | best trade of the day, not taken |
| -rYGugTIsbU@11:46; @18:25 | same | ES / gold | — | S | 4H bear vs daily bull; 1H close above lower high → longs, no entry | no trade |
| Oi_mK1Lt-iQ@07:57–10:13 | ~2023-07-18/19 | GJ | S | L | Daily + weekly bear, daily OB tap, 4H break; London highs then Asian highs swept → 5m BOS → 1m BOS entry; TP1 at OB | TP1 ≈ +$19k (50%), BE; later rest BE [9sD9kTia4V4@00:00] |
| Oi_mK1Lt-iQ@00:00–06:48 | same | ES / gold | L | S | ES long only after a 15m high closed above; gold hourly OB after London high | — |
| 9sD9kTia4V4@02:49–11:26 | ~2023-07-19 | ES | L | S | All bull; wanted OB pullback, price ripped; late setup skipped | no trade |
| 9sD9kTia4V4@11:26–12:30 | same | Gold | S | S | 1H BOS short vs daily/4H bull = plan break | skipped (would have hit TP1, then BE) |
| 9sD9kTia4V4@14:13–14:45 | same | GJ (Asia) | S | S | Highs taken but OB/30-min high not reached; 5m BOS only | skipped |
| IFgysr8gDjc@18:27 | ~2023-07-25 | S&P | — | L | No details | ≈ +$27k |

### 13.2 Boot Camp 2.0

| Cite | Date | Inst. | Dir | Type | Setup sequence | Outcome |
|---|---|---|---|---|---|---|
| o_SdawM3DIE@04:52–07:44 | ~2023-08-24 (PMI) | ES | S | L | D/4H/1H bear; open pushes into 15m/1H OB + FVG → 1m BOS → 50% size entry (no third confluence, no hourly-high sweep) | ≈ −$13k; "wait for the third confluence" |
| o_SdawM3DIE@08:16–13:29 | ~2023-08-24 | GJ | L | L | London lows swept → 5m BOS up → sweep → BOS → OB pullback, higher closes; stop under London lows; Wyckoff spring | TP1 hit; ~+$16k floating; day ≈ −$1,954 |
| OH--4nkbXlM@01:15–04:36 | ~2023-08-24 | Gold | L | L | Prior NY lows swept → FVG fully filled → 5m BOS at NYSE open; stop under lows; TP1 prior NY highs | TP1 ≈ +$7.7k; rest BE |
| OH--4nkbXlM@04:36–06:48 | ~2023-08-24 | GU | L | L | HTF OB + prior NY lows tapped → 5m BOS at open; 24-pip stop | live, in drawdown; unknown |
| G7eq6U8e3yw@01:41–03:56 | ~2023-08-25 | GJ | S | L | London highs tapped (ignored) then taken → BOS down close entry; stop 4 pips above; 0.25% (Powell) | stopped by news spike; then hit TP1 level |
| G7eq6U8e3yw@00:00 | same | ES, gold | — | L | Scalps, not shown | big win, not endorsed |
| IY9NJbaNyqA@03:24–07:54 | 2023-08-28 | Gold | L | L | Monthly lows swept (monthly bull) → 4H big extension BOS up → FVG fill into accumulation → 1H chop → NY sweep of lows + breakout → 1m close through FVG | TP1 ≈ $11k, TP2 ≈ $8.3k; 3 TPs then runner BE, ~$30k total [Iu_v4kuFQhk@02:13] |
| IY9NJbaNyqA@09:33–13:28 | 2023-08-28 | S&P | — | S (outlook) | Monthly lows swept, weekly broke down; longs from accumulation after HTF confirmation | — |
| Iu_v4kuFQhk@00:00–02:13 | 2023-08-28 eve | ES | L | L | 4H lows swept → BOS up → extension out of accumulation; first touch fails, local lows swept → retest of OB/accumulation → 1m BOS; stop under sweep lows | TP1 (50%, BE); later TP2 + TP3 [oJq8egtzCto@01:54] |
| oJq8egtzCto@03:05–06:23 | 2023-08-29 | GJ | L | L | 1H uptrend; accumulation before breakout leg (sweep + BOS); revisit → 5m BOS → push back + reaction → waited 2 candles; stop under 5m low | ≈ −$8k; "best loss" (trend broke) |
| oJq8egtzCto@08:04 | 2023-08-28/29 | Gold 4H | L | H | After BE stop: 4H retrace into accumulation → 5m BOS → rally | could have held (monthly bias) |
| 7MBD3ow7I1g@01:43–04:29 | 2023-08-30 (GDP/NFP wk) | ES | L | L | Bullish news + 1H BOS up pre-market; 5m accumulation → draw in → 1m BOS; stop under low; TP1 1:1 (50%, BE); TP2 hourly liquidity range; 50% size | TP1 + TP2, rest BE |
| 5v4G4xJVKIQ@00:00–03:57 | ~2023-08-31 | GU | L | L | 4H up, 1H down; 15m accumulation; London lows swept → 5m BOS of non-prominent high → FVG + 1m BOS; stop moved below the sweep | ≈ −$10k; lesson: prominent high |
| 5v4G4xJVKIQ@04:29–06:38 | same | ES | L | L | Accumulation → breakout → OB → 5m BOS → leg down sweeps → 1m BOS → 5m bullish close in OB | TP1, rest BE; day ≈ −$5k (−0.25%) |
| 5v4G4xJVKIQ@07:44–09:28 | same | GJ | L | S | 4H bull, 1H bear; RR ≈ 1:0.7 to first area | skipped |
| ss-dZPMnjeY@01:43–03:25 | 2023-09-05 | ES | L | L | Downtrend broke; accumulation tapped pre-market and at open; entry at FVG fill without reaction; fixed 5-pt stop; 50% of budget | stopped; "jumped the gun" |
| ss-dZPMnjeY@03:59–05:40 | same | ES | L | L (re-entry) | Sweep low intact → BOS up + FVG fill + reaction; stop under invalidation; TP1 50%, TP2 50% of rest, rest closed on 1m BOS down | profitable day |
| ss-dZPMnjeY@06:14–08:26 | same | GU | L | L | HTF downtrend broken in NY; lows swept → 5m BOS → revisit of that BOS's accumulation → 1m BOS / 5m reaction candle; 75% of budget | TP1 (50%, BE), aiming 1:5.8; in progress |
| r-DdsJLUlBk@00:33–02:14 | 2023-09-07 | ES | S | L | Bearish bias (claims); push into HTF OB + LTF OB → BOS down / change of trend → FVG + OB + EQ reaction → short; stop above highs | TP1 at pre-market lows (50%), rest BE |
| r-DdsJLUlBk@02:48–05:01 | 2023-09-07 | Gold | S | L | 4H bear; highs swept in accumulation → change of trend → FVG fill → late entry on revisit + reaction; stop tightened | in drawdown; should have entered on close beneath FVG |
| 6zXKK3Wrusg@00:55–04:50 | 2023-09-08 (no news) | GU | L | L | Daily bear but 1H broke prominent highs (displacement); OB + sweep → 5m OB tap + sweep + mini-downtrend break → revisit → 1m close above prominent 1m high; stop under accumulation; TP1 high, TP2 swept high, TP3 liquidity, TP4/5 HTF highs | 3 TPs, rest BE |
| SV37R6j5f4M@00:34–01:39 | 2023-09-11 | ES | L | L | Hourly lows swept → 1m BOS + 5m OB → dip into OB → 1m BOS + 5m reaction; stop under reaction lows | loss |
| SV37R6j5f4M@02:48–04:27 | 2023-09-11 | ES | L | L (re-entry, private) | Lows swept again → reaction → accumulation revisit → breakout above; TP1 1m OB (50%), TP2 highs | TP1 hit, running; day red |
| SV37R6j5f4M@05:36–06:09 | 2023-09-11 | GJ | L | L | 1H downtrend broken; 15m accumulation → 5m BOS → entry on BOS (no third confirmation) | instant loss ("mistake") |
| SV37R6j5f4M@06:09–07:49 | 2023-09-11 | GJ | L | L | Second accumulation → 5m BOS → EQ/FVG retest + reaction + 1m BOS → entry on 5m down candle | chopped out (acceptable) |
| 7Q3nalPsSpk@00:35–04:34 | 2023-09-12 | ES | L | L | Daily broke downtrend; lows swept → BOS up → FVG filled too deep → new high + second 1m BOS → entry; stop under low | stopped by 2.7 pts; price then rallied from the 15m accumulation |
| 7Q3nalPsSpk@04:34–12:58 | 2023-09-12 | GU | L | L | 4H down; 15m OB; London lows swept after NY open → FVG fill, chop, minor 1m BOS → entry inside consolidation; stop 4 pips under sweep | TP1 hit after long drawdown; "bad trade" (correct: breakout + retest + 5m reaction) |

**Tally of live (L) trades with stated outcomes (inferred count):** BC1 ≈ 18 rows (including partial-detail ones); BC2 ≈ 22 rows. ES-specific live trades with full sequences: qecF411R83s, 1FunNCUw_jM, __fKQR5RR08, o_SdawM3DIE, Iu_v4kuFQhk, 7MBD3ow7I1g, 5v4G4xJVKIQ, ss-dZPMnjeY (×2), r-DdsJLUlBk, SV37R6j5f4M (×2), 7Q3nalPsSpk. These are the priority calibration set for the ES bot.
