# Brief for extraction agents (non-bootcamp TJR videos)

You extract structured trading-method notes from TJR (YouTube @TJRTrades) transcripts.
The notes feed a master document that teaches an AI trading bot (ES/MES S&P 500 futures)
to replicate TJR exactly — accuracy, completeness and timestamps matter.

Working dir: /tmp/claude-0/-home-user-ccm-publish-tmp/08ff72fb-35eb-5eb7-ad13-6c359018fd5a/scratchpad/omd

1. Read EXTRACTION_SPEC.md and follow it exactly.
2. Read sections 1, 2, 11 and 12 of kb/framework_v1.md (model from his 2023 Boot Camp,
   contradictions, OPEN questions).
3. Know the model's timeline so you can place each video:
   - 2023 Boot Camp / Boot Camp 2.0: daily bias; sweep → BOS → OB/FVG/EQ retrace; trade
     within ~90 min of the 9:30 ET open; no CPI/PPI/FOMC/NFP days; 1%/day risk.
   - Early 2024–2025 Trading Transformation: 4H trend = bias, 1H picks execution TF
     (agree → 5m exec/1m trigger; disagree → 15m exec/5m trigger); HTF point of interest =
     1H/4H liquidity sweep; then BOS → "third confluence" (OB/FVG/breaker/EQ) → reaction or
     lower-TF BOS; 9:50–10:10 ET window; breakers, BPR; skeptical of IFVG.
   - 2026 Path to Profitability / 2026 tutorial (CANONICAL): sweep of significant high/low
     → 5m BOS or IFVG → retrace into FVG/EQ → 1m BOS/IFVG trigger → targets at draws on
     liquidity (session H/L, PDH/PDL, hourly H/L); SMT ES vs NQ (trade the index that
     failed to make the new extreme); 9:30–9:50 manipulation, 9:50–10:10 entries, done by
     10:30; fixed contract sizing; order blocks no longer mentioned.
4. Read the ENTIRE transcript of each assigned video (chunks if long; never skim) and
   write notes/<video_id>.md per the spec.
5. In "Changes vs. earlier teaching", place the video on that timeline and note what it
   confirms, changes, or contradicts; note answers to framework §12 OPEN items as
   "answers OPEN: <item>". Always record, if present: news-day behavior (does he trade
   CPI/FOMC/NFP?), SMT index choice, take-profit timeframe, order-block usage, entry time
   of day, stop size in points/ticks, contracts/risk, daily trade/loss limits.
6. For live-trading videos: log EVERY trade as a trade example (time ET, instrument,
   direction, the exact sequence of confluences he cites, entry, stop, TPs, outcome, his
   post-mortem). These become test cases.
7. Don't edit or delete other files; no network.

Reply: ids processed, anything unprocessable, and 5–10 bullets of the most important
rules (video_id@timestamp), especially updates vs. the timeline and answers to OPEN items.
