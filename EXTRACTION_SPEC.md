# Extraction spec — TJR transcript → structured notes

Goal: capture everything TJR teaches in a video so that, later, an AI trading agent can
replicate his model exactly. Be exhaustive on trading substance, ruthless on filler
(sponsor reads, Discord plugs, banter, lifestyle).

Transcripts are YouTube auto-captions: expect mis-hearings. Common fixes:
"dick/dig/dicks" = "dip/displacement/leg", "border block" = "order block",
"fair value gap/FVG", "IFVG" = inverse FVG, "SMT", "BOS" = break of structure,
"CHOCH" = change of character, "equilibrium" = 50% of a range, "S P 500"/"SPX"/"ES",
"NQ"/"NASDAQ", "GU" = GBPUSD, "GJ" = GBPJPY, "[ __ ]" = censored profanity (ignore).
He draws on charts the transcript can't show — when he says "this high / right here",
infer what he means from context and mark it `(inferred)`.

## Output: one Markdown file per video at notes/<video_id>.md

```
---
video_id: <id>
title: <title>
upload_date: <YYYYMMDD>
duration_s: <n>
type: lesson | live_trading | recap | psychology | mixed
substance: high | medium | low      # how much trading-method content it has
---

## Summary
3-6 sentences: what this video teaches.

## Concepts & definitions
- **<Concept>** — TJR's definition/explanation, as precise as he gets. Include any
  numbers, timeframes, candle logic (wick vs body, close above/below), what counts and
  what doesn't. [mm:ss]

## Rules (model / entry / stop / target / management / filters / risk)
- <IF/THEN-style rule as close to operational as the video allows> [mm:ss]

## Process / order of operations
Numbered steps if he walks through his process (top-down analysis, bias, execution).

## Confluences mentioned
- <confluence> — how he uses it, how important he says it is (required / nice-to-have /
  "my favorite" / "don't use") [mm:ss]

## Trade examples
For each trade he shows or takes:
- date (if known) | instrument | session/time | HTF bias & why | liquidity taken |
  confirmation (timeframe + signal) | entry trigger & location | stop placement | targets |
  management (partials/BE) | outcome | his lesson [mm:ss]

## Risk & psychology rules
- <rule, with numbers if given (risk %, max trades, daily loss limit, etc.)> [mm:ss]

## Changes vs. earlier teaching / contradictions
- Anything he says is new, updated, or that conflicts with other common TJR teaching.

## Key quotes
- "<short verbatim quote where exact wording matters>" [mm:ss]   (max ~5, each < 30 words)
```

Rules for you:
- Cite a timestamp `[mm:ss]` (or `[h:mm:ss]`) for every concept, rule, and example —
  use the nearest paragraph timestamp in the transcript.
- Never invent rules or numbers he didn't state. If something is your inference, say
  `(inferred)`. If he's vague, write that he's vague.
- Use his terminology, and add the standard term in parentheses if he uses slang.
- For low-substance videos (vlogs, pure motivation), keep notes short but still record
  any trading rule or psychology rule he states.
- Instruments: note which instrument each example is on (ES/SPX/NQ/forex/gold/crypto).
