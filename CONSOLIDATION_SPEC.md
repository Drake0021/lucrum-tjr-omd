# Consolidation spec — notes → per-topic knowledge base (Phase 6)

Inputs (working dir /tmp/claude-0/-home-user-ccm-publish-tmp/08ff72fb-35eb-5eb7-ad13-6c359018fd5a/scratchpad/omd):
- notes/*.md — one per video (front matter has video_id, title, upload_date, type, substance)
- kb/framework_v1.md — bootcamp-only framework (2023)
- catalog/selection.csv — id, rank (1 = newest), duration, title, playlists, tier
- catalog/dates.tsv — id → upload_date (YYYYMMDD) where known

## Eras (use upload_date; fall back to catalog rank)
- E1 Pre-bootcamp: before 2023-06
- E2 Boot Camp 1 & 2.0: 2023-06 → 2023-10
- E3 Late 2023 / early 2024 (Sep 2023 strategy, Jan 2024 daily-bias, Trading Transformation 2024)
- E4 2025 (order-flow model, 5h guide, IFVG/SMT core, OBs dropped ~mid-2025)
- E5 2026 (Path to Profitability Jan 2026, 2026 tutorial May 2026, Jun–Oct 2026 videos) — CANONICAL

## Rules
- The canonical rule = what the most recent era with clear evidence says AND does (live
  trades outweigh statements when they conflict; flag the conflict).
- Earlier versions go into the evolution log with dates; never silently drop them.
- Every claim carries ≥1 citation [video_id@mm:ss]; prefer E5/E4 citations for canonical rules.
- Count evidence: for each rule, how many videos state it, by era.
- Never invent numbers. Inferences marked (inferred). Gaps marked OPEN.
- Use grep to find relevant passages across all notes, then READ the matching notes
  sections fully — don't rely on grep snippets alone.

## Output per topic: kb/<topic>.md
1. Canonical rule(s) — operational, machine-checkable (parameters, candle logic, timeframe).
2. Evidence table — rule variant | era | #videos | key citations.
3. Evolution — dated changes.
4. Edge cases, invalidation, exceptions.
5. Contradictions & how resolved (or OPEN + recommended bot default + rationale).
6. Worked examples relevant to the topic (cite).
