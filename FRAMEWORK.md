# Historical investing game — proposed framework

Historical design draft. [MASTER_PLAN.md](MASTER_PLAN.md) is now the authoritative product direction: one chronological campaign, $100,000 cash plus 1 BTC, overlapping positions, and play until all timed trades close within a fixed historical boundary. Retain the evidence principles below; old isolated-case loops, optional campaign language, horizon menus and implementation proposals are superseded where they conflict.

## Product premise and evidence

Play an investor at a particular historical moment: investigate the evidence available then, commit capital and a thesis, respond to subsequent developments, and compare reasoning with outcomes.

**Current foundation:** the workspace contains a ten-case static quiz app and evidence bundles. The connected campaign is the approved next product direction; this older draft does not describe current implementation status.

**Research-backed:** the source capabilities and historical facts below are linked to primary documentation. Vendor coverage claims still need sample-level verification.

**Proposed defaults / hypotheses:** a 10–15 minute session, US equities first, case-specific holding periods, optional multiple decisions, and identity masking. These are starting product choices, not validated user preferences.

Player job: “When I encounter an uncertain market situation, I want to form and test an investment thesis using the evidence available then, so I can enjoy making decisions and understand which parts of my reasoning held up.”

Observable progress: identify relevant evidence, state a falsifiable thesis, size exposure consistently with downside, and explain a later revision. Profit alone cannot establish decision quality.

## The playable loop

1. **Enter a case.** Show historical date, mandate, remaining time, cash, permitted instruments and execution assumptions. A daily case is a way to distribute historical cases; it need not depict today's markets.
2. **Investigate.** Read a short briefing, inspect the chart and financials, compare peers, and pin evidence into a thesis.
3. **Commit.** Choose buy, skip or short; exposure; probabilities; and one condition that would change the decision.
4. **Advance.** Reveal only newly available evidence and the intervening price path. At predetermined checkpoints, hold, resize, close or reverse.
5. **Debrief.** Show portfolio return, benchmark, risk, original reasoning and what changed. Reveal identity in mystery mode. Recommend a case testing a similar decision in a different context.

Skip keeps capital in the declared cash asset and still advances time. It is a legitimate decision. Selling an owned position and opening a short are distinct actions. Closing a short is “cover.”

### Initial game contract

- Virtual starting equity: $100,000. No deposits during an episode.
- Horizon: fixed per case before the player sees the company, from one month to five years. Exact calendar and execution conventions are defined in CASE_FORMAT.md. Three-month episodes may optionally review after sessions 21 and 42; the initial review batch uses one decision per packet.
- Position choices: flat, 5%, 10% or 20% of current portfolio equity, long or short. Long purchases use cash. Short proceeds are restricted collateral, never extra spending money.
- Decide using a packet frozen after a completed market session; transact at the next eligible regular-session open. Display the prior close as a reference, never a guaranteed fill.
- Proposed simulated slippage: 10 basis points against each transaction. Label this as a game assumption; validate sensitivity before ranking players.
- Idle cash earns 0% in the first version. Later, add a specified historical cash vehicle rather than silently assuming Treasury yield equals an investable return.
- Daily closes mark equity. Longs receive distributions; shorts owe them. Splits change shares and prices consistently. Terminal proceeds, cancellations and delistings require explicit handling.
- First-version shorts are a **simulated short exposure** with a declared fixed borrow fee, for example 5% annualized on daily short market value, actual calendar days / 365. Historical availability, fees and recalls are not claimed to be reconstructed.
- Define an educational margin rule before shipping: maintenance equity at least 30% of short market value; breach detected at close causes covering at the next tradable open. This is a game rule, not a reconstruction of a historical broker. Gaps can cause losses beyond the threshold or starting equity.
- In a future historically executable mode, require borrow availability and terms; disable shorting when that evidence is missing.
- If the market is halted, show a pending order; do not fabricate a price. A case needs complete valuation/settlement handling to be eligible for scoring.

The default checkpoint schedule is fixed, even when nothing dramatic happens. Optional event-driven scenarios must use predeclared triggers, such as the next public earnings release, not hindsight-selected turning points.

## UI and navigation

Only two durable navigation destinations are needed initially: **Play** and **Journal**. The debrief belongs to the episode. A large discovery catalog and portfolio dashboard can wait.

### Play workspace

Desktop layout:

```text
Date + information cutoff | Horizon | Cash | Position | Account value
-------------------------------------------------------------------
Briefing / Evidence / Financials / Peers / My thesis | Decision ticket
                                                   | Buy / Skip / Short
Price chart, ending at the information cutoff       | Position size
                                                   | Confidence
Short briefing + unresolved questions               | Thesis / Change if
Evidence cards and source drawer                   | Commit & advance
```

The first view contains a brief situation description, a chart, 4–6 material facts and 2–3 uncertainties. More evidence is available through progressive disclosure. Do not require reading an entire filing to take a first position.

| Surface | Player job and action | Necessary states | Evidence of success |
| --- | --- | --- | --- |
| Entry | Understand the mandate; start/resume | New, resumed, case unavailable | Player sees cutoff and rules before research |
| Briefing and chart | Orient; inspect past changes | Loading, complete, stale, missing | Can distinguish current evidence from history |
| Evidence drawer | Verify a claim; pin or unpin | Original, amended, disputed, unavailable | Pinned evidence retains provenance |
| Financials and peers | Compare risks and expectations | Comparable, inapplicable, missing | Metric definitions and dates remain visible |
| Decision ticket | Commit action, size and reasoning | Draft, invalid, saving, saved, pending fill | Immutable decision exists before reveal |
| Review checkpoint | React to new information | No update, material update, halt, forced cover | Reason for maintaining/changing position saved |
| Debrief and journal | Assess and transfer reasoning | Complete, replay, insufficient scoring data | Player can compare original and revised thesis |

Each evidence card has a publication date, reporting period where relevant, claim type, source and expandable excerpt. Clearly distinguish **reported result**, **management forecast**, **analyst estimate**, **player assumption**, and **game calculation**. Preserve conflicts between sources instead of silently choosing a preferred narrative.

Financial cards explain the implication without issuing a recommendation: “Debt due within 12 months” can link to “Compare with available liquidity.” Avoid green buy signals, red sell signals and a hidden universal investment rating.

On mobile, stack content and keep a compact decision button visible; open the complete ticket in a drawer. Support keyboard operation, visible focus, text descriptions/tables for charts, and reduced motion. Direction and confidence must not depend on color.

Autosave research and drafts. Only advance once the decision is persisted. Failed persistence leaves the cutoff unchanged and offers retry. Missing optional data is labeled; missing core financial/price evidence makes the case unavailable and offers another. Replays are marked as informed by the previous reveal.

## A reusable investment decision framework

Use the same questions everywhere; adapt the measurements to the instrument.

| Question | Evidence to examine | What the player records |
| --- | --- | --- |
| What am I buying or shorting? | Business model, security rights, revenue/profit drivers | One-sentence exposure description |
| What is changing? | New information versus the prior public baseline | Catalyst or structural change |
| What does this price require? | Valuation, prior returns, peers, contemporaneous guidance | Assumptions needed to justify price |
| Can the position survive until the thesis plays out? | Cash, burn, maturities, refinancing, dilution; short costs | Main failure mechanism |
| What can happen within this horizon? | Bear/base/bull operating and valuation assumptions | Probabilities totaling 100%, return ranges |
| Is the potential payoff worth the risk? | Scenario returns, costs, correlation, alternatives | Direction and position size |
| What would change my mind? | Observable milestone, financial threshold or contrary evidence | Review/exit condition |

“Priced in” is an interpretation, not an observable fact. Label reverse valuations and scenario probabilities as estimates. Expected scenario return is the probability-weighted sum of scenario returns minus modeled costs; it is not an automatic buy rule.

Provide a short guided version for the first case: choose the main risk, pin supporting evidence, and write one sentence. Advanced mode exposes the full scenario table. Do not grade prose length or require an essay to play.

Instrument adapters preserve the questions but change inputs: operating companies use cash flows and financing; banks require capital/funding/credit measures; REITs require property cash flows and debt; bonds require contractual payments, priority and maturity; ETFs require holdings, fees and methodology. Options and futures additionally require contract specifications, expiry, margin and suitable historical quotes. They are outside the first implementation.

## Point-in-time data contract

The core invariant is **the exact information version used by the game was public by the decision cutoff**. A reporting period ending before that cutoff is insufficient.

Store at least:

```text
instrument_id, issuer_id, historical_symbol, symbol_valid_from/to
source_id, original_url, document_hash, source_version
period_start/end or event_at
published_at, available_at, timestamp_precision, timezone
retrieved_at, supersedes_id, extraction_version
claim_type, value, unit, original_excerpt, source_location
```

`retrieved_at` is when our system acquired the record. It is not when a historical investor could know it. A present-day retrieval can support a historical claim when its original version and public availability are established. If only a publication date is known, conservatively allow it starting the following market session. Verify source timezone semantics before normalizing to UTC.

Never overwrite an old fact with a restatement. Resolve the latest eligible version as of the cutoff within matching accounting period, scope and unit. Distinguish an earnings release from a later formal filing. Preserve amendments and conflicting claims with their own availability timestamps.

### Source framework

| Layer | Starting source | Limits and implementation decision |
| --- | --- | --- |
| Daily prices, corporate actions, security history | Evaluate Massive for an API workflow; Norgate for an end-of-day research alternative | Verify sampled 2020 bars, inactive securities, dividends, splits and identifier histories before choosing |
| Reported financials and disclosures | SEC EDGAR submissions, original filings and XBRL | Use filing-linked evidence; normalize only facts eligible at the cutoff |
| Management guidance | Historical issuer releases and filing exhibits | Keep original ranges and withdrawals; do not backfill guidance from later actuals |
| Macro data | ALFRED vintages plus original release calendars | Query the vintage known then; validate intraday release availability separately |
| Government and regulation | Original Fed, Treasury, agency and legislative announcements | Store public release time; distinguish proposals, announcements and effective dates |
| News | Issuer/regulator primary documents first; GDELT archives for discovery; licensed archive later | Verify original article version and publication time; discovery records are not a complete full-text archive |
| Analyst consensus, transcripts, borrow terms | Optional licensed providers | Missing means unavailable; never substitute today's estimates or invented history |

Massive documents date-based ticker lookup and aggregate price retrieval. These provide useful primitives, not a complete guarantee that every returned field is a preserved historical vintage. [Ticker history](https://www.massive.com/blog/new-point-in-time-tickers-api), [aggregate bars](https://massive.com/docs/rest/stocks/aggregates/custom-bars).

Norgate supplies delisted-security support and stable asset IDs but says it does not supply prior company names/tickers; another historical identity source would be needed. Its standard license restricts redistribution, so it should not be assumed suitable for a public game's data delivery. [Data FAQ](https://norgatedata.com/data-package-faq.php), [license](https://norgatedata.com/subscribe/eula.php).

EDGAR offers submissions and company facts, but its frames endpoint selects recently filed facts for calendar periods. Use original filing accessions and eligibility rules instead of treating a current frames response as a historical snapshot. [SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces).

ALFRED's real-time periods retrieve what was known in a historical period rather than today's revisions. [FRED/ALFRED documentation](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html).

GDELT offers bulk and BigQuery historical data. Its DOC API documents a rolling search window; a date filter alone does not establish access to arbitrary old news. Use archive datasets to discover 2020 sources. A URL discovered then may serve an edited page today. [Archive access](https://gdeltproject.org/data.html), [DOC API](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/).

For any chosen vendor, confirm the actual historical depth and rights to store/display the proposed data before integrating it into a shared game. No provider purchase is selected in this draft.

### Pipeline and architecture

Start with an offline Python content pipeline, immutable raw documents, normalized tables (SQLite is sufficient for a local pilot), and versioned episode packets. A small server serves the current packet to a web client and owns progression and scoring. This is a proposed stack, not a repository constraint.

Pipeline: acquire → preserve original → normalize identities/times/units → select eligible versions → calculate features from eligible inputs → assemble briefing → review evidence and spoilers → publish versioned case.

Separate the visible evidence packet from future prices, later disclosures, identity mapping and debrief. Do not deliver future data in client JSON, hidden DOM, preload requests or chart axes. Evidence links in mystery mode open sanitized excerpts; original names and URLs unlock at identity reveal. Transparent mode can expose originals immediately.

Price treatment needs two views: player charts rebased or adjusted only for actions effective by the cutoff, and a complete corporate-action ledger for realized holdings and returns. Today's fully adjusted prices can reveal later actions and must not be mixed with historical share counts to calculate valuation.

An LLM may summarize provided evidence with citations, but asking it to “pretend it is 2020” does not remove knowledge of the future. Generate from a bounded source packet, require source references for factual clauses, validate numerical outputs deterministically, and manually review pilot briefings. Outcome information is excluded from briefing generation. Uncited historical claims fail publication.

## Choosing interesting cases without hindsight selection

Treat the content unit as **instrument × cutoff × horizon × mandate**, rather than company alone.

1. Build the universe from securities that existed at that date, including subsequently failed or delisted securities. Require sufficient trading and source coverage.
2. Find candidate cutoffs using information already observable then: public results, guidance changes, financing announcements, regulatory changes, or trailing price/volume movement.
3. Assess candidates without future returns: evidence completeness, competing defensible theses, a meaningful driver within the horizon, and distinct risk/reward tradeoffs. Have reviewers read only the frozen packet where practical.
4. Sample across sectors, dates, event types and past-only market conditions. Include uneventful periods and “skip” opportunities; every case need not end in a surprise.
5. Freeze the candidate set before attaching outcomes. Reject cases later only for objective data/execution defects, with the exclusion reason recorded.
6. Attach future prices and developments for simulation and debrief. Do not balance the default evaluation set into equal future winners/losers or select only dramatic reversals.

An explicitly curated “famous market stories” collection can use hindsight for teaching, but keep it separate from performance evaluation. Its returns cannot establish general investing skill.

### Reducing memorized answers

- **Mystery mode:** hide names, ticker, logos, executive names and identifiable links; preserve sector, business economics and relevant historical macro context. Rebase charts to 100 without changing returns. Do not falsify financial values or dates to conceal the case.
- **Finite horizons:** a company's eventual success does not answer a 63-session entry, sizing or exit question.
- **Repeated decisions:** the player must respond to information as it arrives rather than holding indefinitely until a remembered outcome.
- **Relative choices:** later add two contemporaneous peers plus cash with a shared capital budget. Measure opportunity cost using identical horizons and execution rules.
- **Multiple entry dates:** different packets for the same issuer test different information sets. Count only an unseen first attempt in calibration statistics.
- **Recognition control:** “I know this story” swaps the case before commitment and records the exclusion. Recognition cannot be fully eliminated in real history.
- **Synthetic mode, later:** explicitly fictional branches can remove exact historical recall, but require a separately labeled model and scoring system. Do not blend simulated paths into historical outcomes.

Hypothesis to test: masking plus finite horizons reduces recognition enough to improve play. Pilot both masked and transparent cases; measure self-reported recognition, decision changes and enjoyment. Do not assume more disagreement automatically means a better case.

## Scoring and debrief

Keep three separate readouts; do not collapse them into an authoritative “investor skill” score.

1. **Outcome:** net portfolio return, cash and market/sector comparisons, drawdown and exposure. Show both full benchmark return and an exposure-matched comparison so a small position is not treated as a fully invested portfolio. Define comparison construction before play.
2. **Forecast calibration:** ask the probability that the instrument's total return exceeds a declared benchmark over the episode horizon. Score the observed binary event with Brier loss, `(p - y)^2`, and report calibration across many unseen cases. A single realization cannot validate a probability or reveal true expected value.
3. **Decision review:** compare the saved thesis with eligible evidence, cited risks, position sizing and later revision. Use a transparent checklist and evidence references. Automated prose feedback is coaching, not ground truth.

Show the actual path and the modeled alternatives under identical rules. Identify whether a forecasted catalyst occurred and whether the thesis addressed it; do not confidently assign each price move a single cause. Highlight where reasoning was contradicted even when the trade made money, and where a defensible risk occurred even when it lost.

End with one transferable observation and one related case. The journal preserves all decision versions, packets, fills and game-rule versions so an episode is reproducible.

## Initial content collection

Use the repeatable eight-block template and 100-case batch plan in [CASE_FORMAT.md](CASE_FORMAT.md). The collection includes biotech clinical successes, failures, mixed findings, financing and ordinary commercial updates, plus software/growth companies such as Zoom at different dates. Horizon is an explicit part of every case. Carnival is not the proposed introductory case.

The user will manually judge candidates through Keep / Edit / Reject with evidence sufficiency, clarity, interest and recognition flags. Preserve a first judgment before outcome reveal and a second editorial decision afterward. Repeated issuer/date families stay linked so the collection has substantive variety rather than cosmetic duplicates.

## First build and acceptance gates

Generate 100 reviewable drafts from the agreed presentation contract, using a small format-validation batch to catch systematic issues before completing the rest. The user curates the collection. Primary-source and numerical checks remain required for each completed case; researched seeds do not count as completed drafts.

Required first-release gates:

- A filing published after the cutoff cannot affect visible facts, derived metrics, briefings or peer comparisons.
- A later restatement cannot replace the value in an earlier episode packet.
- No future data or identity secrets are delivered before their intended reveal.
- Buy, skip, short, close and cover produce reproducible fills, cash flows and distributions under the saved rule version.
- Split and delisting examples reconcile shares and terminal portfolio value; short fees and forced-cover behavior have meaningful arithmetic tests.
- Decision state survives reload; network failure cannot reveal the next packet before commitment.
- The same decision sequence and packet version replay to the same result.
- Missing material evidence blocks publication; optional gaps remain visible.
- Chart data, evidence and commitment are accessible by keyboard and at mobile widths.
- Every financial or news claim has an eligible source; every editorial calculation exposes its inputs.

Open product hypotheses: preferred session length, acceptable short-selling simplification, usefulness of identity masking, appetite for numerical probability forecasts, and private-only versus shared distribution. These affect implementation priorities; they do not block defining or prototyping the first loop.
