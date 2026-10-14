# Running Lucrum SPX as a deterministic cloud bot (AI-built, not AI-run)

## Why this design
Running an AI on every bar is expensive, slow, non-deterministic and hard to backtest. TJR's model as written in the OMD is rules plus parameters, so it can be **compiled once into ordinary code**. The AI's job moves to *building, testing and updating* that code. Daily operation costs only a small server and a market-data feed. No AI usage is needed to trade.

```
          ┌─────────── build / update time (AI, occasional) ───────────┐
OMD + BOT_SPEC ──► AI coding agent ──► code + config.yaml ──► tests (§19 cases + backtest) ──► git tag release
          └────────────────────────────────────────────────────────────┘
                                                │ deploy (CI)
          ┌────────────── run time (no AI, every trading day) ─────────┐
market data (ES+NQ 1m) ─► engine (state machine §16) ─► risk gate ─► broker API (ES/MES orders)
calendar.yaml (news, FOMC, holidays) ─┘            └─► logs / trade journal / daily report
          └────────────────────────────────────────────────────────────┘
```

## Components
| Component | What it is | Notes |
|---|---|---|
| Strategy engine | Python (or similar) service implementing `BOT_SPEC.md`: bar builder → detectors → state machine → orders | Deterministic: the same bars give the same decisions. The same code runs live and in backtests. |
| Config | `config.yaml` with every switch and DEFAULT from the OMD (§0.1, §18) | Most behaviour changes are a config edit, not a code change. |
| Calendar | `calendar.yaml`: CPI/PPI/NFP/FOMC dates and times, US holidays, early closes | Edited weekly or monthly, by hand or by a small script. No live news feed needed. |
| Market data | Real-time CME futures data for **ES and NQ** (1m bars, or ticks built into bars), plus history for backtests | Use a CME data vendor or your broker's feed. NQ is required even though only ES is traded. |
| Broker / execution | A futures broker with an API that supports ES/MES bracket orders (entry + stop + multiple targets) | Start on the broker's **paper/sim account**. |
| Host | Small Linux VM (2 vCPU / 4 GB is plenty), preferably in a US-east or Chicago region | Run as a Docker container under a process supervisor (systemd), with auto-restart. |
| Storage | SQLite/Postgres for trade journal, signals and every DEFAULT that decided a trade | This is the data the AI reviews later. |
| Alerts | Email, SMS or Discord webhook for: trade opened/closed, daily summary, errors, kill-switch | |

## Daily operation (no AI)
1. **07:00 ET:** container health check. Load config and calendar. If today is a no-trade day (§12 / §0.1), log it and idle.
2. **Pre-open (by 09:25):** compute draws on liquidity (DOLs: Asia/London/pre-market/PDH/PDL/1H/4H levels), the bias inputs and the news gates.
3. **09:30–10:30:** run the state machine on closed 1m/5m bars. The engine has the right to submit orders only while the risk gate passes.
4. **Manage open trades** to their targets and stop. Flatten by the hard exit time (§18 default).
5. **End of day:** write the journal and send a one-message daily report: setups seen, A+ or not, trades, P&L, which defaults fired.

## Safety rails (non-negotiable, enforced in code outside the strategy)
- **Max loss:** a daily and a weekly loss limit. Breaching either disables trading until a human re-enables it.
- **Order and position caps:** max contracts per order, max open position, max orders per day.
- **Data-staleness guard:** if no bar arrives for N seconds or ES/NQ feeds desync, cancel working entries and flatten per config.
- **Clock check:** NTP-synced, with exchange-time sanity checks.
- **Kill-switch:** a file flag or API endpoint that flattens and halts.
- **Paper first:** go live only after the paper-trading criteria in §10 are met. Then start at MES size.

## How AI updates the bot (cheap, occasional)
- **Weekly or monthly review:** an AI session reads the journal export and the OMD. It flags rule misfires and proposes config or code changes as a pull request. A human approves and merges.
- **Every change** must pass: (1) unit tests, (2) the §19 worked-example tests, (3) a backtest comparison against the previous release. Deploy by git tag through CI (e.g. GitHub Actions → build image → restart container).
- **When TJR's model changes** (new videos): run the `fetch.sh` + extraction pipeline on just the new videos and update the OMD. Re-derive the config and code diffs from the updated OMD.
- Optional: a **once-a-day async AI review** of the daily report, not real-time. It costs pennies and never touches orders.

## Cost profile
- **Running the bot:** a small VM plus a data subscription plus broker fees. No AI cost per trading day.
- **AI cost** happens only when you build or change the bot.

## FOMC afternoons (requested)
FOMC needs only the calendar, because release dates and times are published in advance. TJR never taught a defined afternoon FOMC model, though. It is implemented as `FOMC_PM_SESSION: false` with an optional `FOMC_PM_WINDOW: ["14:05","14:45"]`. That window is a DEFAULT, not TJR-stated. It reuses the same §8 sequence after the 14:00 release, with half risk. Enable it only after backtesting FOMC days.
