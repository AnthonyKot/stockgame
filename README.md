# Stockgame

A historical investing campaign: start with $100,000 cash and 1 BTC, travel through ten chronological stories, and manage one shared portfolio of overlapping buy/skip/short calls. Keep playing until all timed trades close, within a fixed historical data boundary.

The approved product direction is [MASTER_PLAN.md](MASTER_PLAN.md); [EPIC_1.md](EPIC_1.md) breaks it into the end-to-end scenario, stories and open decisions. The existing standalone quiz app is the foundation; campaign implementation is upcoming.

- Start a new session with `TODO.md` and `research/START_HERE.md`, then `ARCHITECTURE.md` (what exists and how it connects). `research/PAUSED.md` includes historical progress and quota notes.
- Product authority: `MASTER_PLAN.md` takes precedence. `FRAMEWORK.md`, `CASE_FORMAT.md` and `research/SELECTION_RULES.md` retain supporting evidence and historical design material.
- Live: https://anthonykot.github.io/stockgame/ (GitHub Pages, deployed from `site/` by `.github/workflows/pages.yml` on every push to main). Feedback: https://github.com/AnthonyKot/stockgame/issues
- Run locally: `cd site && python3 -m http.server 8765` and open http://localhost:8765/index.html.
- Rebuild data after editing anything under `cases/` or `research/prices/`: `python3 scripts/build_bundles.py`. Then run every check: `scripts/run_checks.sh` (add `--no-browser` without Playwright).
