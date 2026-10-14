---
video_id: 4LERkD7z_w4
title: "Trading Transformation Day 6: Highs, Lows, and Trends"
upload_date: 20240213
duration_s: 832
type: lesson
substance: medium
---

## Summary
A basic market-structure lesson. A swing high is strictly a two-candle pattern (up candle then down candle) whose price is the higher of the two candles' highs. A swing low is the mirror (down then up, lowest of the two lows). Doji/flat candles are ignored. Trends are HH/HL (up) and LH/LL (down); sideways = consolidation. He demonstrates on 4H and 15m charts (instrument not named) and says trends exist on every timeframe, with "trends within trends". BOS is deferred to a later day.

## Concepts & definitions
- **High** — "a move up then a move down ... green Candlestick followed by a red Candlestick and you take the highest point of those two candles." [00:35–01:10]
- **Low** — "a move down then a move up red candle green candle and you take the lowest point of those two candlesticks." [01:10–01:44]
- **Strict colour rule** — Only the up→down (or down→up) colour sequence defines the swing. Two consecutive up candles followed by more up candles is not a high, even if a wick sticks out ("what is the next candle it's up so I don't give a [ __ ] about that"). [03:57–04:30]
- **Wick extremes of other candles don't change the rule** — "if this candle's Wick went all the way down here but it's still followed with a black candle I don't give a [ __ ]": the low is still where the down→up pair occurs. The exact chart case is unclear (vague/inferred). [04:30–05:02]
- **Doji / flat candles** — "If the candle is so minuscule ... you can't even identify the color ... just ignore it." Opened and closed at about the same price → skip it when sequencing highs and lows. [10:12–10:48; 11:55 "we see a doji candle we don't give a [ __ ] about"]
- **Uptrend** — Higher highs and higher lows. [06:10]
- **Downtrend** — Lower highs and lower lows. [06:43–07:20]
- **Consolidation** — Sideways, "no sense of direction". [07:20]
- **The market moves three ways:** up, down, sideways. [05:36]
- **Fractal** — Up/downtrends and consolidation exist on 1m, 5m, 1H, weekly...; "smaller trends within these bigger trends" on the 15m inside a 4H trend. [07:52; 11:22; 12:29]
- **Quick heuristic** — "the easiest way to see an uptrend or a downtrend look at where it's going." [08:27–09:03; 13:02]

## Rules (model / entry / stop / target / management / filters / risk)
- For swing detection (bot): swing high at the pair (bullish candle i, bearish candle i+1), price = max(high_i, high_i+1). Swing low at (bearish i, bullish i+1), price = min(low_i, low_i+1). Skip dojis (open ≈ close) when sequencing. [01:10; 10:12] The doji tolerance is not quantified.
- Trend state: compare successive swing highs and lows (HH+HL = up; LH+LL = down; otherwise sideways). [06:10–07:20]

## Process / order of operations
1. Pick a timeframe (he starts on the 4H).
2. Mark every swing high/low via the 2-candle rule, ignoring dojis.
3. Compare consecutive highs and lows → classify uptrend/downtrend/consolidation.
4. Drill down (15m, 5m) and repeat: there are trends within trends. [08:27–12:29]

## Confluences mentioned
None (structure only).

## Trade examples
- 4H chart: prior uptrend, now lower highs/lower lows = "starting a downtrend on the 4-hour". The 15m segment shows a downtrend sequence. Instrument not named (likely ES/NQ or crypto; unknown). [09:03–12:29]

## Risk & psychology rules
- "Stop trying to overcomplicate things ... green red high, red green low, simple caveman." [05:02–05:36]

## Changes vs. earlier teaching / contradictions
- Same as Boot Camp [PmhuPbY8ZHo@01:39; @04:25]. **New detail:** dojis/flat candles are ignored when identifying highs and lows. This partially addresses the swing-detection operationalization, though no numeric doji threshold is given.

## Key quotes
- "green then red green red high red green low simple caveman bro that's all we need" [05:36]
- "if the candle is so minuscule that ... you can't even identify the color within it just ignore it" [10:12]
