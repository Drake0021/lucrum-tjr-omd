---
video_id: NPG_BZ_83fo
title: "Boot Camp Day 42: How to Backtest"
upload_date: 20230707
duration_s: 624
type: lesson
substance: medium
---

## Summary
TJR explains how he backtests: not with TradingView bar replay, but by scrolling back on a full chart to a random day, doing top-down analysis, and "target practice" — spotting examples of his building blocks (liquidity sweep, BOS, order block, FVG). He argues bar replay leaks/hides higher-timeframe information (full HTF candles are shown, or HTF structure changes go unnoticed while sitting on the 15m) and lacks the emotion of live candles. He judges his real ability only on live (or demo) markets.

## Concepts & definitions
- **Bar replay problem** — In bar replay on e.g. the 15m at 9:45, switching to daily/4H/1H shows the full (future-complete) HTF candle, so you cannot form an honest daily/4H/1H bias; you are effectively stuck on one timeframe. [01:39], [02:15]
- **Second bar-replay problem** — If you sit on the 15m waiting for your area, an hourly BOS against your bias may occur unseen and you'll keep looking for the wrong direction. [05:38], [06:10]
- **Third problem** — Bar replay advances bar by bar, removing the emotion of watching a live candle form wicks. [06:45], [07:20]
- **"Backtesting" / "Aimbot"/target practice** — Spotting examples of the strategy's building blocks on historical charts repeatedly until recognition is automatic ("robotic"). [02:51], [08:25]

## Rules (model / entry / stop / target / management / filters / risk)
- You need daily / high-timeframe bias to know where to take a low-timeframe trade; any testing method that hides HTF bias is flawed. [03:58]
- Judge your trading ability (win rate) purely on live markets (live or demo forward testing); bar replay likely gives a worse win rate than live. [04:30]
- Example target-practice sequence: on the daily, find BOS → mark the order block → enter in it; or liquidity sweep → BOS → order block → drop to 4H → maybe 1H to find more confluences inside the OB. [03:25], [04:30]

## Process / order of operations
1. Scroll back on the full chart to a random day (no bar replay). [01:06]
2. Analyze top-down (daily → 4H → 1H → lower). [01:39], [03:25]
3. Spot the building blocks: liquidity sweeps, BOS, order blocks, FVGs; identify where the market is drawing. [03:25], [07:53]
4. Weekend routine: go back over the previous week, every day find one or two good trades you could have taken on a pair, and mark all building blocks. [07:53]
5. Repeat the homework from the OB / FVG / liquidity sweep / BOS boot camp days. [05:04]
6. Then trade live on demo or a "baby live account" if not yet profitable. [09:31]

## Confluences mentioned
- Liquidity sweep → BOS → order block, with lower-timeframe (4H/1H) confluence inside the OB — used as the backtest example. [03:25]

## Trade examples
- None specific; generic chart illustrations of sweep/BOS/OB entries (instrument not stated). [03:25]

## Risk & psychology rules
- Live candle formation creates emotion; that psychology is the remaining missing piece once building-block recognition is automatic. [07:20], [08:25]
- Unprofitable traders should test on demo or a small live account. [09:31]

## Changes vs. earlier teaching / contradictions
- None stated; says the bulk of material has been covered and remaining videos are shorter, "chipping away" at small mistakes. [08:58]

## Key quotes
- "bar replay is not necessarily the best way to back test in in my eyes" [01:06]
- "I always like to judge my trading ability based purely off of live markets" [04:30]
- "if you don't know your daily bias ... how do you know where you're supposed to take a trade on a low time frame" [03:58]
