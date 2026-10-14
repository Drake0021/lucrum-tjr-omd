# TJR One Massive Doc (OMD) — TJR's day-trading model, written for Lucrum SPX

**Version:** 1.0 · **Compiled:** 2026-10-14 · **Subject:** TJR (YouTube @TJRTrades)
**Instrument target:** ES / MES (CME E-mini and Micro E-mini S&P 500 futures). NQ is used as a correlation and confirmation feed.

---

## 0. How to use this document (instructions to the trading agent)

**What this is.** This is the only source of truth for how Lucrum SPX replicates TJR's model. It was compiled from the full transcripts of every TJR Boot Camp video (Boot Camp 1, Days 1–55, and Boot Camp 2.0), plus 100+ hours of his other content from 2022 to October 2026. Section 20 lists every source, with coverage totals.

**Which version of TJR you are replicating.** TJR's model changed a lot between 2022 and 2026. He has said himself that the Boot Camp is "dated" [7a8tAGkVJac@01:41] and that his older strategy videos are "pretty dated" [TEp3a-7GUds@01:06]. This document makes his **2026 model (era E5) canonical**. Earlier versions are kept only so you understand the history (§14) and can tell old teaching apart from current rules.

The Boot Camp still supplies the foundational definitions he continues to use: swings, break of structure, liquidity, FVG and equilibrium.

**How to read it.**
1. **Definitions** (§2–§7) are binding. Every rule elsewhere uses those terms exactly as defined.
2. **The trading procedure** is §8 (the model in order) and §16 (state machine and pseudocode). If prose and pseudocode disagree, stop and flag it. Do not guess.
3. **Hard constraints** are §10–§13: risk, management, no-trade filters and psychology. They override any signal.
4. **Discretionary points** are listed in §18, the ambiguity register. Wherever TJR uses judgement, the register gives a **DEFAULT (not TJR-stated)**. Use the default unless your operator configures something else, and log every time a default decides a trade.
5. **Test cases** are in §19, worked examples drawn from his real trades. Use them to check your implementation before trading.

**Citations.** `[video_id@mm:ss]` means `https://www.youtube.com/watch?v=video_id` at that timestamp. Every rule carries at least one citation. Anything marked *(inferred)* was deduced by the compiler, not said by TJR.

**Configuration switches you must expose:**
- **`NEWS_MODE`**:
  - `STRICT` (recommended default; his long-standing rule) skips CPI, PPI, FOMC and NFP days, Fed-chair speech days and US bank holidays.
  - `CURRENT` (his 2025–2026 practice) is more permissive.
  - See §12.
- **`RISK_PER_TRADE`, `MAX_TRADES_PER_DAY`, `DAILY_LOSS_LIMIT`.** Defaults are in §10. Follow his *teaching*, never his live-stream behaviour (§10, §15).
- **`STOP_MODE`**: `INVALIDATION_1M` (the E5 canonical stop) or `SWEEP_EXTREME` (conservative). See §11.

**Honest limits of this document.**
- TJR describes his 2026 model as a discretionary toolbox, and has said he deliberately leaves some details out [yiuFUp0kFz8@6:03:43]. No document can reproduce his judgement perfectly. This one turns every rule he states into an explicit, testable rule and makes every judgement call visible in §18.
- The sources are auto-generated captions. Charts he drew on screen were inferred from his narration, not seen directly.
- The performance figures here are TJR's own unaudited claims. **Nothing in this document shows the model is profitable.** Backtest it and paper trade it on Lucrum SPX before risking capital.

### Contents
1. Philosophy and core principles · 2. Glossary (operational definitions) · 3. Market structure · 4. Liquidity · 5. Time · 6. PD arrays and imbalances · 7. SMT divergence and index selection · 8. The full model, in order · 9. Master confluence list, ranked · 10. Risk management · 11. Trade management and exits · 12. No-trade filters · 13. Psychology as hard constraints · 14. Model evolution timeline · 15. Why it works (TJR's claims) · 16. Decision procedure (state machine and pseudocode) · 17. Applying it to ES/MES · 18. Ambiguity register · 19. Worked examples (test cases) · 20. Source index

---
