# BOT_SPEC: build brief for the AI that codes Lucrum SPX

You are an AI coding agent building a **deterministic, offline** trading bot from `TJR_OMD.md`. The finished bot must run with **no AI at runtime** (see `DEPLOYMENT.md`). Read this file first, then the OMD.

## 1. How to read the OMD as a builder
| OMD part | Treat as |
|---|---|
| §0.1 Operator configuration | **Binding overrides.** Beats everything else. |
| §2–§7 definitions | Normative. Each becomes a pure function or detector with unit tests. |
| §8 model + §16 state machine/pseudocode | Normative control flow. If §8 and §16 differ, §16 wins. Log the difference in `BUILD_NOTES.md`. |
| §10–§13 risk, management, filters, psychology | Normative hard constraints, implemented in the risk gate (they veto signals). |
| §18 ambiguity register, "DEFAULT (not TJR-stated)", "(inferred)" | **Config parameters, never hard-coded.** Every one gets a key in `config.yaml` with the OMD default. |
| §14 evolution, §15 why-it-works, historical items (order blocks, breakers, accumulation) | Informational. Do not implement unless a config flag asks for it. |
| §19 worked examples | Acceptance tests (see §6 below). |
| §20 sources | Not code. |
| Citations `[id@mm:ss]` | Put them in code comments next to the rule they implement. |

Known caveat: §1–§19 were drafted in parallel by four writers. If two sections conflict, apply §0.1 first, then §16, then the more specific rule. Record each conflict in `BUILD_NOTES.md`. Never silently pick one.

## 2. Architecture (modules)
```
data/        feed adapters (live + historical) → normalized 1m bars for ES and NQ, exchange-time aware
bars/        resample 1m → 5m, 15m, 1H, 4H, D (4H/D anchored per OMD §5/§17, configurable)
levels/      session & DOL builder: Asia, London, NY pre-market, PDH/PDL, 1H/4H highs/lows, equal highs/lows, news-candle H/L; pruning (§4)
detect/      swings (two-candle rule), BOS (body close strictly beyond), FVG + stacks, IFVG, EQ, 79% close, sweep (+reaction), SMT (ES vs NQ)
bias/        pre-open + 09:50 bias logic, ES–NQ 5m agreement (§8, §7)
engine/      state machine §16: IDLE → PREP → WAIT_SWEEP → WAIT_CONFIRM_5M → WAIT_CONTINUATION → WAIT_TRIGGER_1M → IN_TRADE → DONE
risk/        conviction gate (A+), stop tiers (§0.1 STOP_MODE=TIERED), sizing, daily/weekly limits, re-entry rules, news/time filters
exec/        broker adapter: bracket orders (entry, stop, TP ladder), breakeven move, partials, flatten; paper and live modes
journal/     every signal, every rejected setup (and why), every DEFAULT that fired, every order/fill
backtest/    event-driven replay of historical 1m bars through the SAME engine/risk/exec (sim broker)
```
Rule: the strategy core (`levels/ detect/ bias/ engine/ risk/`) is pure and deterministic. It does no I/O and has no wall-clock calls; time comes from the bars. That makes backtests and live runs identical.

## 3. config.yaml (minimum keys; values from §0.1 and the OMD defaults)
```yaml
instrument: {trade: ES, contract: MES_or_ES, tick: 0.25, point_value: {ES: 50, MES: 5}, confirm_feed: NQ}
es_when_nq_leads: SKIP
news_mode: CURRENT            # §12 table, CURRENT column
fomc_pm_session: false        # optional; window below is DEFAULT not TJR-stated
fomc_pm_window: ["14:05", "14:45"]
time: {no_entry_before: "09:50", primary_window: ["09:50", "10:10"], last_entry: "10:30", hard_flat: "<§18 default>"}
stop: {mode: TIERED, buffer_pts: 0.5, min_rr_tp1: 1.0}
conviction_gate: A_PLUS        # §0.1
reentry: {mode: STRONG_ONLY, max: 1, before: "10:30"}
risk: {per_trade_pct: <§10>, daily_loss_pct: <§10>, weekly_loss_pct: <§10 default>, max_contracts: <operator>}
management: {tp1_close_pct: <§11>, move_be_at: TP1, be_offset_ticks: 1, runner_exit: <§11 default>}
detectors: {equal_level_tolerance_pts: <§18>, sweep_reaction_bars: <§18>, smt_swing_window_bars: <§18>, chop_filter: <§18>}
calendar_file: calendar.yaml
```
Every `<…>` value must be filled from the cited OMD section during the build. Record the source line in a comment.

## 4. Data requirements
- **Historical:** ES and NQ 1m OHLCV, at least 2 years, continuous back-adjusted **and** raw front-month (sweeps and levels use raw prices), with exchange timestamps. Also historical event dates for CPI/PPI/NFP/FOMC and holidays.
- **Live:** ES and NQ 1m bars (or ticks), with a latency budget of seconds. The bot acts on bar closes only.
- Times in ET, with DST handled. Sessions per OMD §5 (Asia 18:00–03:00, London 03:00–08:30, NY pre-market 08:30–09:30, RTH 09:30).

## 5. Order logic (per trade)
1. **Entry:** a market order on the close of the 1m trigger bar, or a limit at the trigger close if `entry_type: LIMIT`.
2. **Stop:** apply STOP_MODE=TIERED, then size: `contracts = floor(risk_$ / (stop_pts × point_value))`. If the result is 0, or reward-to-risk to TP1 is under `min_rr_tp1`: **no trade**.
3. **Bracket:** place the stop and the TP ladder from the §11 DOL targets. At TP1, close `tp1_close_pct` and move the stop to breakeven + offset. Apply the runner rules. Flatten at `hard_flat`.
4. **Re-entry:** only via the §0.1 conditions. All of them are checked in `risk/`.

## 6. Acceptance tests (must pass before paper trading)
- **Unit tests** for every detector, using synthetic bar sequences built from the OMD definitions, including the edge cases listed in §2 (wick vs body, equal close, stacked FVGs, doji).
- **§19 replay tests:** for each worked example with a known date, load that day's ES/NQ data. Assert the engine's bias, sweep, confirmation, trigger window and direction match TJR's. Assert the "negative test" examples are **rejected**. Report a match rate. Mismatches go to `BUILD_NOTES.md` with a diagnosis (data issue, DEFAULT choice, or OMD gap).
- **Backtest report:** trades, win rate, average R, max drawdown, no-trade-day count, setups rejected by each filter. Run it on the in-sample period and on a held-out period.
- **Determinism test:** running the same input twice gives an identical journal.

## 7. Go-live gates
Paper trade until the §10 criteria are met (e.g. 3 consecutive green months). Then go live on **MES**, with the safety rails from `DEPLOYMENT.md` active. Scale only by an explicit config change.

## 8. Deliverables from the build session
A repo with the code, `config.yaml`, `calendar.yaml` (current year), Dockerfile, CI workflow, tests, `BUILD_NOTES.md` (every conflict and assumption), the backtest report, and a `RUNBOOK.md` (start, stop, kill-switch, update procedure).
