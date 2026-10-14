---
video_id: 1FunNCUw_jM
title: "Boot Camp Day 38: Stop Losses"
upload_date: 20230703
duration_s: 795
type: mixed
substance: high
---

## Summary
Stop-loss lesson recorded on a Discord Zoom, using that day's stopped-out ES/S&P long as the example. Default rule: stop goes beyond the liquidity sweep (above it for shorts, below for longs), regardless of whether you enter on an OB or FVG, plus a buffer for spread (~0.5 point on ES or your broker's spread). The stop is the invalidation point: if price returns beyond the swept extreme, the sweep wasn't valid. Exception (which he dislikes): if the sweep is so far away that R:R is terrible, place the stop beyond a closer building block (OB/FVG). Stops should be based on invalidation and risk tolerance, never a fixed number of points/pips. He also reveals he cut size in half that day due to high-impact news and the next-day bank holiday, and says not to trade on US bank holidays.

## Concepts & definitions
- **Stop loss = invalidation point** — placed where the setup is proven wrong; beyond the liquidity sweep, because if the sweep was real price "has no reason to come back above this high"; if it does, the sweep wasn't valid (not enough volume/orders). [01:08], [01:41], [02:15]
- **Spread buffer** — never place the stop exactly on the swept price; put it ~0.5 points beyond (ES) or account for your broker's spread for the pair, so the bid/ask spread doesn't stop you out. [05:44], [06:18], [06:50]
- **Liquidity sweep reference for stop can be LTF** — in the day's trade he treated a 5m liquidity sweep (with a 1m BOS) as "the" sweep and put the stop under it. [07:23]
- **Set lot size + confidence scaling** — he uses a set lot size and scales it by confidence/conditions for the day (to be covered in next video). [09:36]

## Rules (model / entry / stop / target / management / filters / risk)
- Default: stop beyond the liquidity sweep extreme (short: above the sweep high; long: below the sweep low), whether entry is OB or FVG — NOT just beyond the nearest high/low near entry. [01:08], [03:25]
- Add ~0.5 pt (ES) / spread buffer beyond the sweep. [06:18]
- Exception: IF the sweep is so far that R:R becomes terrible, THEN place the stop beyond a closer confluence (above the OB / FVG). He dislikes it because price can take you out and still go in your bias direction. [03:59], [04:33], [05:09]
- Exception 2 (HTF trade / no clean sweep): with a 15m sweep + BOS where the stop beyond the sweep would make R:R poor, scale to a different timeframe and find a swing low (one scale lower) beneath — he's vague; "if you want to be extra safe". [08:28], [09:03]
- Stop placement must not be based purely on points or pips; based on where bias/setup is invalidated plus your risk tolerance. [10:43], [11:18]
- Rarely uses an "elongated" (wide) stop. [01:08]
- Risk sizing: on high-impact-news days and before bank holidays (low volatility, choppy), halve size; he planned to de-risk the whole week of high-impact news. [09:36], [10:10], [10:43]
- Don't trade on a US bank holiday — US bank holidays slow all markets, including forex pairs. [12:24]

## Process / order of operations
1. Identify the liquidity sweep your trade is based on. 2. Stop beyond its extreme + spread buffer (~0.5 pt ES). 3. Check R:R; if unacceptable, consider closer OB/FVG as invalidation (less preferred) or skip. 4. Size position per set lot size × confidence/conditions. [01:08]–[06:18], [09:36]

## Confluences mentioned
- Liquidity sweep — defines stop location (required). [01:08]
- OB/FVG — alternative tighter stop location (exception). [04:33]

## Trade examples
- 2023-07-03 | ES/S&P | daily bias bullish | 5m liquidity sweep then 1m BOS up | entered on candle close of the BOS | stop under the 5m sweep low with buffer (~"four below") | stopped out by a wick, then price moved higher and would likely hit all TPs (5m BOS up formed after) | Risked 100 lots (half his usual 200 on his broker, where 1 lot = 10 units ≈ 20 standard offshore lots) due to high-impact news and next-day bank holiday | Lesson: the stop was at invalidation; being wicked out while the bias plays out is acceptable — "maybe we should have covered ourselves by putting price lower". [05:09], [05:44], [07:23], [07:57], [09:36], [11:18], [12:58]

## Risk & psychology rules
- Stop-outs where the bias later proves correct are "nothing to cry about" — bias was right. [05:09]
- De-risk (half size) on high-impact-news days, choppy pre-holiday days; possibly whole news-heavy week. [10:10], [10:43]
- No trading on US bank holidays. [12:24]
- Stop size is a function of your own risk tolerance. [09:36]

## Changes vs. earlier teaching / contradictions
- None explicit. Lot-size numbers are specific to his broker (10 units/lot).

## Key quotes
- "I almost always put my stop loss above the liquidity sweep" [01:08]
- "our stop loss always has a purpose our stop loss is essentially our invalidation area" [02:15]
- "point five points below the actual price point or figure out what your spread is" [05:44]
- "your stop loss should never be ... based purely off of points or pips it should be based off of where price is then invalidated" [10:43]
- "don't trade tomorrow ... it's a bank holiday" [12:24]
