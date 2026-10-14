# Lucrum SPX — TJR One Massive Doc (OMD)

**`TJR_OMD.md`** is the deliverable: TJR's (@TJRTrades) day-trading model written for the Lucrum SPX bot (ES/MES), 331 KB, sections 0–20, 1,642 citations.

Coverage: all Boot Camp + Boot Camp 2.0 videos (69/70; Day 48 Pt.1 has no audio, and its re-upload is included) = 22.1 h, plus 191 other TJR videos = 114.1 h. That's 136.2 h in total, read from full transcripts.

| Path | What |
|---|---|
| `TJR_OMD.md` | Final document |
| `CANONICAL.md` | Binding decisions used by all section writers |
| `draft/` | Section drafts (A–D), header, source index, writers' gap lists |
| `notes/` | 260 per-video structured notes (definitions, rules, trades, timestamps) |
| `kb/framework_v1.md` | Boot Camp–only framework (≈540 citations) |
| `catalog/` | Channel catalog, selection, batches, dates, failures |
| `*.py`, `fetch.sh` | Pipeline: catalog → select → fetch captions (yt-dlp) → json3→md |
| `EXTRACTION_SPEC.md`, `AGENT_BRIEF.md`, `CONSOLIDATION_SPEC.md` | Instructions used by extraction agents |
| `FOLLOWUP.md` | Work deliberately deferred for budget |
| `BOT_SPEC.md` | Build brief for the AI that codes the offline bot |
| `DEPLOYMENT.md` | Cloud architecture: AI-built, not AI-run |

Raw transcripts are not committed: they're TJR's copyrighted material. Re-create them with `fetch.sh`, which needs the YouTube domains allowed in the network settings.
