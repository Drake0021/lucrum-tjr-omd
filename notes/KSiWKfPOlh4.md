---
video_id: KSiWKfPOlh4
title: "Boot Camp Day 39: Calculating Lot Size"
upload_date: 20230704
duration_s: 928
type: lesson
substance: high
---

## Summary
Position-sizing lesson (recorded on July 4th). Three approaches: (1) a set lot size (what TJR uses, as a range of set sizes), (2) calculating lot size every trade with a calculator (Stinu app for forex/gold; a website calculator that includes the S&P), (3) full-porting — never. He shows how to read stop distance from the position tool, how to check contract size per lot in MetaTrader (his broker: 10 units/lot; most offshore: 100; many prop firms: 10). His set-lot-size method: size so that 1% is risked at your typical *minimum* stop (ES: ~4 points), so a larger stop (8 pt) = 2% and 12 pt = 3%. His three tiers: normal (1% set size), de-risk (50% of normal — high-impact news / holiday conditions), confident (2× normal — no news, all biases aligned) which he forbids for unprofitable traders.

## Concepts & definitions
- **Three sizing methods** — set lot size (his), calculate every time, full port (never). [01:07]
- **Calculating lot size** — inputs: account balance, risk % (e.g., 1%), stop loss distance (pips/points), instrument, contract size per lot → lot size (rounded to 2 decimals). Example: $1,000 account, 1% risk, 30-pip stop on GBPUSD → 0.03 lots (≈$10 risk). [02:14], [03:23], [03:58]
- **Stop distance from position tool** — the number shown on the long/short position tool is the stop in pips; plug into calculator. [04:32]
- **S&P points vs "pips"** — calculator/MT uses pips; on S&P 1 point = 100 "pips" in his calculator (e.g., a 4-point stop = "400 pips"). [05:41], [08:33], [09:09]
- **Contract size per lot** — check in MetaTrader: symbol (SPX) → Details → "Contract size". His (Hankotrade) = 10 units/lot; most offshore = 100; many prop firms = 10. Check whenever you open a new account. [06:50], [07:23], [07:58]
- **Set lot size** — size computed so your typical minimum stop risks 1%; larger stops then risk 2×/3× proportionally. Rationale: speed (plug in and enter) and because stops rarely exceed 3× minimum. [08:33]–[11:26]
- **Per-instrument set size** — every pair has different volatility/volume and stop widths, so each needs its own set lot size; beginners should trade only one pair. [11:26]

## Rules (model / entry / stop / target / management / filters / risk)
- Never full-port. [01:07]
- TJR's typical ES/S&P stop: ~4 to 7 points. [08:33], [09:09]
- Set lot size: on a $100k account with 4-point minimum stop and 10 units/lot → 25 lots = 1% risk; 8-point stop → 2%; 12-point → 3% (rarely reached). [09:44], [10:19], [10:52]
- Risk tiers (TJR's personal): Normal = set lot size (1% at min stop) on days with no/low-impact news; De-risk = 50% of normal on high-impact news days, waiting for news, holidays/bank-holiday-adjacent days, anything likely to "mess up the market"; Confident = 2× normal (2% at min stop, potentially 4%+) on days with no news, a setup he loves, and all biases aligned. [12:32], [13:04], [13:36], [14:44]
- Students: use normal or de-risk only; never the confident tier until you have proof in the market (profitability). Turn profitable with calculated or set lot sizes first. [11:58], [14:10], [14:44]
- (inferred, for ES/MES translation — not stated by TJR) 1% of $100k = $1,000 at a 4-pt stop → ES ($50/pt) = 5 contracts; MES ($5/pt) = 50 contracts.

## Process / order of operations
1. Measure stop distance (position tool). 2. Determine contract size per lot for your broker/instrument. 3. Enter balance, risk %, stop into calculator → lot size. OR 4. Precompute a set lot size from your typical minimum stop at 1% and choose tier (normal / de-risk / confident) based on the day's news/conditions and setup quality. [04:32], [07:58], [09:09], [12:32]

## Confluences mentioned
- "All the biases are in line" + no news + favorite setup → criteria for the confident tier. [14:10]

## Trade examples
- 2023-07-03 ("yesterday") | ES/S&P | used de-risk lot size due to high-impact news and the following July 4th bank holiday. [13:04]

## Risk & psychology rules
- Normal risk = 1% (at min stop). [14:44]
- De-risk = 50%; confident = 2× (professionals with proof only). [14:44]
- If $14/yr for a lot-size app is a lot of money to you, you shouldn't be trading. [02:49]
- Beginners: trade only one pair. [11:26]
- He took July 4th off (holiday). [00:00]

## Changes vs. earlier teaching / contradictions
- Day 38 cited "usual 200 lots / 100 lots de-risk" on his broker (10 units/lot); here the example uses 25 lots on a hypothetical $100k account — numbers are account-dependent, not contradictory.

## Key quotes
- "you can also full port which you will never do" [01:07]
- "most of the time my stop loss on the S&P 500 is anywhere from ... four points to ... seven points" [08:33]
- "my normal risk is just one percent ... d-risk is 50% of it confident is two times it" [14:44]
- "you guys should never use a confident lot size" [14:44]
