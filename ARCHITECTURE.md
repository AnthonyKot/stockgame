# Stockgame: how the pieces fit (living doc, update on every structural change)

## Product direction versus implementation

[MASTER_PLAN.md](MASTER_PLAN.md) is authoritative. The existing static quiz pipeline described below is a foundation, not an implemented campaign. The next major architecture work is a shared portfolio ledger, chronological event processing, historical end-date eligibility, and time-gated reveals. A commit must no longer unlock a trade's entire future in campaign mode. The campaign has $100,000 cash plus 1 BTC and runs until all timed trades close. Existing UI/search proposals are subordinate.


Purpose: one map of the repo for anyone (Claude, Codex, a human) picking the project up. The product authority is MASTER_PLAN.md; FRAMEWORK.md and CASE_FORMAT.md provide supporting material. Start sessions with research/START_HERE.md; research/PAUSED.md includes older progress notes. This file describes what exists and how it connects.

## Pipeline in one line

```
research (30 candidates) -> verification -> selection (10) -> writers (player.json + evidence.json per case)
   -> aftermath research (aftermath.json per case, outcome-only)
   -> scripts/build_bundles.py -> site/data/<opaque_id>/{market,sheet,reveal,outcome}.json -> static site
```

## Directory map

| Path | What it is | Who writes it |
| --- | --- | --- |
| `MASTER_PLAN.md` | Product authority: the chronological portfolio campaign. Wins on conflict. Not yet implemented. | user |
| `FRAMEWORK.md`, `CASE_FORMAT.md` | Earlier product and presentation contracts; evidence principles still apply. | humans / editor session |
| `research/SELECTION_RULES.md` | Rules for choosing the ten. | editor |
| `research/PAUSED.md` | Live handover: status, what is running, next steps. Read first. | every session, on pause |
| `research/candidates.json` | 30 candidates extracted verbatim from the three research runs. | scripts (one-off) |
| `research/candidates-screened.json` | Same plus `price_screen` and editor corrections (cutoff fixes). | `scripts/screen_candidate_returns.py` + editor |
| `research/selected.json`, `research/SELECTION.md` | The ten, alternates, reserve, rejected, with scores and reasons. | editor |
| `research/MVP_PROMPT.md` | Generation prompt for the ten cases (hard rules, per-case evidence, repairs). | editor |
| `research/verification/*.json` | Source verification per batch (Sonnet). `*.haiku-rejected.json` kept as record. `editor-checks.json` = EDGAR pulls by the editor. | workers + editor |
| `research/sources/*.txt` | Local copies of EDGAR filings used for checks. | editor (curl) |
| `research/prices/<TICKER>.json` | Cached Yahoo chart bars 2015 to 2026-09-09 with dividends and splits. Outcome data; never shipped raw. | `scripts/fetch_candidate_prices.py` |
| `research/runs/*.stdout.json` | Raw output of the three headless research runs. | `scripts/run_story_research.py` |
| `cases/BRIEF.md` | Brief and JSON schema for the case writers (player.json, evidence.json). | editor |
| `cases/AFTERMATH_BRIEF.md` | Brief and schema for the post-cutoff timeline (aftermath.json). | editor |
| `cases/<candidate_id>/xbrl-facts.json` | SEC XBRL facts filed on/before the cutoff, `filed` = availability anchor. | `scripts/fetch_xbrl_facts.py` |
| `cases/<candidate_id>/player.json` | Pre-decision sheet: masked + transparent blocks, six headline metrics, history, what changed, sector module, catalysts, help-me-weigh, missing data. | Sonnet writers |
| `cases/<candidate_id>/evidence.json` | Sources with availability basis and excerpts, claims (c1..cn) cited from player.json, search log, exclusions, repairs_needed. | Sonnet writers |
| `cases/<candidate_id>/aftermath.json` | Dated, sourced events after the cutoff plus horizon notes. Outcome material. | Sonnet workers |
| `cases/scenes.json` | Opening scene per case: setup type (friend_pitch, friend_warning, bad_news_headline, analysts_disagree, familiar_product), the pitch text, its claims mapped to evidence claim ids, the framing question, and `debrief_check` (per-claim verdict written from aftermath.json; outcome-only). Investigation fields, authored for all ten cases: `ask_label`, `ask_friend` (three questions with sourced answers, cite claim ids), `assumptions` (selectable 'my decision depends on' items), `thesis_check` (per-assumption verdict, outcome-only), `walkthrough` (ordered aftermath event ids with stage-safe text for the 'live through it' reveal, outcome-only). | editor |
| `site/` | Static app. No build step, no dependencies. | editor |
| `site/data/index.json` | Case list with opaque ids only. | `scripts/build_bundles.py` |
| `site/data/<opaque>/market.json` | Pre-cutoff bars (3 years), returns, SPY. Player-visible. | builder |
| `site/data/<opaque>/sheet.json` | player.json minus the transparent block and URLs, names masked, plus `neutral_title` and `player_question` from research/selected.json, claims, source handles with masked excerpts, derived valuation. Player-visible. | builder |
| `site/data/<opaque>/reveal.json` | Transparent block, sources with URLs and excerpts, repairs. Fetched after commit. | builder |
| `site/data/<opaque>/outcome.json` | Fills, path, dividends, per-action results, alternative horizons, extended path, aftermath. Fetched after commit. | builder |

## Scripts

| Script | Input | Output | Notes |
| --- | --- | --- | --- |
| `scripts/run_story_research.py <batch>` | `research/prompts/<batch>.md` | `research/runs/<batch>.stdout.json` | Headless `claude -p` on Sonnet, web tools only. |
| `scripts/fetch_candidate_prices.py` | tickers | `research/prices/*.json` | Yahoo chart API; delisted tickers 404. |
| `scripts/screen_candidate_returns.py` | candidates.json + prices | candidates-screened.json | Editor-only outcome screen, adjusted close, no costs. |
| `scripts/fetch_xbrl_facts.py` | selected.json | `cases/<id>/xbrl-facts.json` | SEC companyfacts; filters by `filed <= cutoff`. |
| `scripts/verify_cases.py` | cases/*/player.json, evidence.json | exit code | Banned future-relative words, future years without guidance wording, six headline tiles, three unresolved questions, claim/source integrity, masked-block leak. |
| `scripts/build_bundles.py` | selected.json, prices, cases/* | `site/data/**` | See below. Run after any change to cases/ or prices. |
| `scripts/test_returns.py` | none | exit code | Arithmetic tests for fills, dividends, borrow, leap day, sizes. Run after touching `outcome()`. |
| `scripts/test_simulate.js` | site/data | exit code | Node test: site/sim.js reproduces the builder for every case and horizon; stop/target behaviour on Nektar. Run after touching sim.js or the builder. |

## Builder rules (scripts/build_bundles.py)

- Opaque id = sha1("stockgame-mvp-1" + candidate_id)[:10].
- Price levels: Yahoo closes are split-adjusted for all later splits; the builder multiplies each bar back by every split after that bar so charts show the historical trading price. Dividends are never folded into levels.
- Market view ends at the last complete session before the cutoff day.
- Execution contract: entry at the open of the first session on/after the cutoff day; exit at the open of the first session on/after the calendar anniversary (leap day clamps to 28 Feb); 10 bp slippage per side; longs receive dividends in (entry, exit]; shorts owe them and pay 5%/yr borrow on daily close; idle cash 0%; sizes 5/10/20% of $100,000.
- Benchmark: SPY on the same two opens, fixed shares, cash dividends in (entry, exit] added, no costs (`spy_open_to_open_return` is total return; `spy_price_return` kept for reference). "Beats SPY" = stock long total return after costs > SPY total return. Tests: `python3 scripts/test_returns.py`.
- `alternative_horizons`: the other two of {1,3,5} under the same rules, `unavailable` when the exit is past the cached data. `extended_path` runs to the longest available anniversary with `horizon_markers`.
- `sim`: opens and closes to the longest available anniversary, stock and SPY dividends, horizon exit dates, cost parameters. `site/sim.js` (pure, browser + node) replays the contract client-side for the player's chosen horizon, size and optional stop loss / take profit (trigger on a close, fill at the next open). `node scripts/test_simulate.js` checks it against the builder's numbers for all ten cases and both alternative horizons. `sheet.horizons_available` lists the horizons a case can score.
- Masking: issuer name variants, ticker, and any per-case `mask_terms` listed in research/selected.json (strings, replaced by "the company", or {term, with} pairs for partner names and partner drugs) are replaced in every string of sheet.json; a ticker inside a drug code becomes `candidate-NNN`. Other brand names are not masked (known limit).
- Valuation (`sheet.valuation`): market cap = latest XBRL share count filed before the cutoff x last eligible close; net cash from the writer's tiles (net cash tile, or cash tile minus debt tile / XBRL long-term debt); EV = market cap minus net cash; multiples on the last full fiscal-year revenue from XBRL. Banks get market cap only. Every input carries its date and source; caveats list staleness. The missing "Enterprise value" headline tile is replaced by the derived market cap tile.
- Aftermath: `cases/<id>/aftermath.json` is copied into outcome.json as `aftermath` when present.
- Scenes: `scene` (setup, voice, claims, question, ask_friend, assumptions; masked) goes to sheet.json; `scene_check` (voice, claims, debrief_check, assumptions, thesis_check, walkthrough with resolved events) goes to outcome.json only.

## Site (site/)

- `index.html` case list + rules section (rules come from `SG.rulesSection()` in app.js so the case page can show the same text in a side panel).
- `play.html?case=<opaque>`: header, blocks 2 to 7 from sheet.json (sector evidence and history collapsed by default), chart from market.json, evidence drawer (claims with masked source handles and masked excerpts before commit; URLs after commit), decision ticket, and on narrow screens a fixed "Decide" button that jumps to the ticket. On commit: entry saved to `localStorage["stockgame.journal.v1"]` and read back; if the save fails the form stays, an error is shown and nothing is fetched. Then outcome.json and reveal.json are fetched and the debrief renders above the sheet: result tiles, forecast line (no per-case score), path chart with numbered event markers, other-horizons reveal, 'checking the pitch' (scene claims with verdicts), aftermath horizon notes and dated events, sources, open repairs. Page order: scene card (setup, question, real masked headlines, ask-your-friend, first reaction), case title and investment question, business, 'where the stock stands' (alias, sector, cutoff, horizon, last close, 1/3/12-month returns vs SPY), market chart, financial snapshot, what changed, sector evidence (collapsed), upcoming and unresolved, optional arguments, gaps. Rules open from the top menu as a side panel on every page.
- Journal entry fields: case_id, alias, cutoff, horizon, horizon_years (chosen at the ticket, case default preselected), stop_pct, tp_pct (the only folded 'Exit levels' fields), action, size, p_beats_spy (null since 2026-09-09 late; the probability question was removed, older entries keep theirs and the journal's calibration table uses only those), p_beats_spy, reason, contrary, change, hint_used, scene_setup, instinct (interested | unconvinced | against), asked_friend (indices), assumptions (ids), walkthrough ([{event_id, date, view}] reflections keyed by event), walkthrough_started, walkthrough_complete, walkthrough_skipped (a reload resumes at the first unanswered stop; identity and result stay hidden until complete or skipped; stops are limited to events inside the chosen holding period), result {position_return, portfolio_return, spy_return, brier, beat_spy}, reveal_name. Identity stays masked in the header until the walk is finished or skipped.
- `journal.html`: all commitments, export to JSON, calibration table after five revealed decisions (three confidence buckets).
- `app.js`: `SG` namespace: loading, storage, formatting, `lineChart` (inline SVG, crosshair, keyboard, table alternative, log scale when range > 6x, legend toggles, relative-to-benchmark view, vertical markers), `rulesSection`, `topbar`.
- `style.css`: theme tokens (light and dark), chart colors validated for colorblind separation (stock #2a78d6/#3987e5, SPY #eb6834/#d95926).
- Transparent mode (checkbox in the top bar, `localStorage["stockgame.transparent"]`) fetches reveal.json before the decision and shows names.
- Serve: `cd site && python3 -m http.server 8765`. Screenshot: the Playwright headless shell under `~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell --headless --screenshot=out.png --virtual-time-budget=5000 URL`.

## Conventions

- Nothing published after the cutoff may reach sheet.json or market.json. If you add a field to player.json, decide whether it is player-visible and add it to `strip_urls`/masking accordingly.
- Numbers come from a source with a date or they are `null` with a reason. Derived values carry formula and inputs.
- Cheap models: Haiku 4.5 is fine for pure extraction but not for verification or writing (three batches were rejected). Sonnet is the floor for anything that must report what it did not check.
- Update this file and research/PAUSED.md whenever files, scripts or schemas change.

## Story UI patch — 9 September 2026

- Decision ticket keeps action, horizon, size and reasoning visible; optional exit rules, probability and extra thesis fields live in a closed “Add detail” section. Free-text reasoning is optional; authored assumption selection keeps its existing validation.
- Walkthrough records `walkthrough_started` and `walkthrough_complete`, resumes the first unanswered event, and refuses to advance on failed persistence. Existing completed results remain accessible. Selected assumptions appear beside each event.
- Journal uses the revealed name without repeating the alias; skipped positions show a dash for position return, while portfolio return remains numeric. A compact Exit column shows the exit category, with the full reason in its title.
- Browser regression: `scripts/test_story_ui.cjs`. Serve `site/`, then run with Playwright installed or set `PLAYWRIGHT_MODULE`; optional `CHROMIUM_PATH` and `STOCKGAME_URL` configure the browser and server. Tests use fresh browser storage.
- This patch does not alter story wording, scope walkthrough events to horizons, or implement campaign integration. Full future payload loading remains the standalone app's existing limitation.
