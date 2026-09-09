# Repeatable historical case format

Current product authority: [MASTER_PLAN.md](MASTER_PLAN.md). Cases are now scenes in one shared chronological portfolio campaign. Reuse the ten selected stories first; the 100-case production proposal below is historical, not the next task. The master plan overrides fixed presentation order, immediate outcome reveals, isolated capital, and older horizon options in this document.

This document specifies presentation and generation. `data/candidate-seeds.json` contains researched starting points, not completed cases. Prices, complete financial histories, original document versions and wider context still need acquisition. No stock-return outcome has been calculated for those seeds.

## One case, one question

The unit is a security at a precise cutoff with a fixed forward horizon. Different dates for the same company are distinct cases. For first-batch review, use one decision with a case-specific horizon fixed before research: 1 month, 3 months, 1 year, 3 years or 5 years. The longer multi-decision experience in FRAMEWORK.md can reuse these packets later.

Player question: **At the next tradable opening price, would you buy, skip or short this stock over the stated holding period?** Show the last eligible close as a reference and disclose that the fill will differ. For after-reaction cases, wait until a complete post-announcement session has occurred before freezing the chart. Never display news published after a close while letting the player trade at that already-past close.

Initially collect action, optional size, confidence, main reason and the biggest contrary fact. Keep detailed scenario modeling optional. Judge the presentation before adding elaborate scoring or portfolio mechanics.

## Horizon is part of the case identity

`security × cutoff × holding period × mandate` identifies a case. Examples requested by the user: Alphabet in 2024 for one year; Merck in 2019 for five years. Resolve Alphabet share class and whether Merck means Merck & Co. (US, MRK) or Merck KGaA (Germany); the initial pilot uses GOOGL and US MRK as explicit assumptions.

Store `horizon: {unit: trading_sessions|calendar_months|calendar_years, count: N}`, exchange calendar, entry convention and exact exit convention. A calendar year is not silently treated as 252 sessions. For calendar periods, add the period to the actual entry date (clamp a nonexistent month-end anniversary to the last date in that month), then exit at the first eligible regular-session open on or after the anniversary. Trading-session horizons exit at the open N session intervals after the entry open. Record exact timestamps and ensure complete outcome coverage.

Use the horizon to change presentation emphasis, not just the end of the chart:

| Horizon | Most relevant questions | Suggested financial history |
| --- | --- | --- |
| 1 month | Event timing, liquidity, immediate expectations, execution gaps | Latest quarter plus comparison baseline |
| 3 months | Results, clinical/regulatory milestones, financing | 4–8 quarters |
| 1 year | Guidance, demand durability, margins, dilution | 8 quarters plus annual trend |
| 3–5 years | Competitive position, patent/exclusivity timelines known then, reinvestment, portfolio economics | 3–5 annual periods plus recent quarters |

Keep core panels and provenance identical across horizons. Do not add facts from later years to make a long-horizon thesis easier. A five-year hold needs dividends, splits, acquisitions, spin-offs/distributions, delistings and terminal proceeds; preserve distributed holdings and apply their later actions through exit unless the case's predeclared mandate says otherwise. Report account total return and an identically timed benchmark, not only the original ticker's price change. Multi-year simulated shorts need accumulated borrow costs and margin/recall assumptions made explicit.

Proposed 100-case horizon mix: 15 one-month, 30 three-month, 30 one-year, 15 three-year, 10 five-year. This allocation crosses the sector/event mix below rather than adding 100 more cases. A horizon variation counts as distinct only if the decision framing and relevant evidence emphasis are updated; don't pad the batch with identical copies. Do not classify a case as success/failure without specifying whether that refers to a business event or a return over a particular horizon.

## The player sheet

Use the same order for every company. First-screen text target: 150–220 words excluding tables. Expanded research target: 600–1,000 words plus financial tables and documents. These are limits for consistency, not filler targets.

| Block | Exact content | Presentation rule |
| --- | --- | --- |
| 1. Decision header | Cutoff, security/alias, sector, horizon, last close, trade rules | Date and horizon always visible; no future-relative title |
| 2. Business in two sentences | What is sold, to whom, how revenue is earned; development-stage status where relevant | 40–60 words, concrete, factual |
| 3. Market snapshot | 12-month price/volume chart; 1/3/12-month returns; distance from trailing high; market and sector comparison | Chart ends at cutoff; mark only events already public |
| 4. Financial snapshot | Six relevant headline metrics and supporting history appropriate to the horizon | Value, prior comparable value, reporting period, publication date, definition |
| 5. What changed | Three material recent developments, or explicit absence of a material update | Each item has a date, fact and sourced relationship to the business |
| 6. Sector evidence | Biotech clinical/pipeline table or software demand/customer table | Same schema within a sector; missing entries explicit |
| 7. Upcoming and unresolved | Publicly expected catalysts, timing windows, and three unresolved questions | No precise future result date unless already announced |
| 8. Decision ticket | Buy / Skip / Short, optional exposure, confidence, reason, contrary evidence | Commit before outcome reveal |

Desktop: blocks 2–7 in the central reading area, a compact decision ticket on the right, and a sticky cutoff header. Mobile: one reading column and a button opening the ticket. Evidence opens in a drawer without losing scroll position. Avoid many competing tabs and a news terminal appearance.

Every metric and evidence item expands to its source. Every chart has a table/text alternative. Show “not available in the collected historical sources” rather than zero or an invented value. IPOs with less than a year of price history show the available interval; do not pad it.

The date is the scenario's date, not the company's fiscal-year label. For example, a Zoom release for fiscal 2021 can be published in calendar 2020.

### Financial snapshot adapters

| Operating company / software | Development-stage biotech | Commercial biotech |
| --- | --- | --- |
| Enterprise value and EV / trailing revenue | Market cap and net cash | Enterprise value and EV / trailing revenue |
| Revenue and YoY growth | Cash + liquid investments, with restrictions | Product sales and growth |
| Gross margin | Quarterly operating cash outflow | Gross/operating margin |
| Operating margin | Funding runway scenario | Operating cash flow |
| Free cash flow, explicitly defined | Debt and contractual commitments | Cash, investments and debt |
| Cash/debt and dilution context | Shares and recent financing/dilution | Revenue concentration and pipeline spending |

Headline slots can combine related measures; definitions and exact accounting basis must remain available. Always provide the supporting income statement, balance sheet, cash flow and share-count rows, even when some are not useful headline metrics.

Use shares outstanding at the relevant historical date, not a later share count or weighted-average EPS denominator, for market capitalization. Label estimate limitations between reported dates. EV conventions, currency and cash/investment treatment must be explicit. Calculate ratios from eligible inputs; never join a current vendor market cap to historical revenue.

Do not call net loss “cash burn.” Runway is a scenario calculation using disclosed liquid assets, cash outflows, financing and obligations; management's runway guidance is a separate claim. A financing facility is not equivalent to unrestricted cash. For pre-revenue firms, show revenue multiples as inapplicable.

### Biotech evidence module

For each material program show:

- Indication, drug/mechanism in plain language, development phase, ownership/economic rights, partner and commercial status.
- Trial identifier, randomized/blinded/control design, planned/enrolled/analyzed sample sizes distinguished, population, treatment duration and follow-up.
- Prespecified primary endpoint and secondary endpoints. Identify changes only if those changes were public by the cutoff.
- Latest publicly available evidence: effect size, confidence interval and p-value where reported; comparator; safety findings; missing detail. Before a readout, use earlier evidence and label it as such.
- What management says versus what a regulator or independent publication actually says. A sponsor's description of FDA discussions is not a public FDA commitment.
- Expected milestone window, its source and announcement date. Trial completion, results submission, public posting and company readout are separate events.
- Economic relevance: existing product sales, concentration, patent/royalty obligations, and cost/funding to the next milestone. Do not assign an invented percentage of enterprise value to a pipeline asset.

Explain specialist terminology inline. A player should understand whether evidence comes from a controlled trial or an uncontrolled early study without being expected to know the vocabulary already.

Do not turn a primary-endpoint miss into a generic positive headline because secondary endpoints looked favorable. Preserve prespecification and multiplicity caveats when disclosed; do not infer confirmatory significance from an isolated p-value. Do not infer clinical success from a stock move or approval probability from a p-value.

ClinicalTrials.gov provides historical record versions, but eligibility depends on public posting, not merely the date a sponsor submitted an update. Preserve the historical version and its public availability. [NLM archive guidance](https://www.nlm.nih.gov/pubs/techbull/jf20/jf20_clinicaltrials_qc.html).

FDA documents require the same care: the FDA published a batch of historical complete response letters in July 2025. A letter's original issue date does not by itself make its full text eligible for an earlier case. [FDA announcement](https://www.fda.gov/news-events/press-announcements/fda-embraces-radical-transparency-publishing-complete-response-letters).

### Software / Zoom-style evidence module

Show paying-customer counts, definitions of customer cohorts, large accounts, retention/expansion when disclosed, enterprise versus small-customer exposure, gross margin, sales spending, stock compensation and competition. Keep meeting participants, users, accounts and paying customers distinct.

Put reported revenue, prior management guidance, new management guidance and archived consensus in different rows. Missing archived consensus is not permission to claim an earnings beat. Preserve management-defined metric changes; do not silently splice unlike cohorts.

The central uncertainty can change over time: paid conversion, scalability, customer retention, growth normalization, or the valuation implied by the price. Generate that question from eligible evidence; do not label the packet “before the top,” “dead-cat bounce” or “last chance to buy.”

Use “short squeeze” only with contemporary supporting evidence about positioning/covering; an observed rally alone does not establish its cause. Before verification, label seeds by date or publication anchor.

## Editorial tone and evidence selection

Use a fixed evidence policy: all material issuer results/financing/regulatory/program announcements in the last 90 calendar days; the most relevant preceding annual/quarterly baseline; and older still-material trial or risk evidence. Summarize the most important items into the sheet, retain the rest in the source drawer. Extend the search window when the business's material baseline is older; document why.

Deduplicate syndicated copies. Record missing archives and the evidence inclusion/exclusion rationale. A ten-headline selection should not accidentally become ten copies of the same press release.

Macro context gets at most three relevant items, with their business connection stated. Avoid attaching a generic COVID essay to every 2020 company. No news does not mean no risk; state what was searched and what is missing.

The default packet presents facts and open questions. Optional “Help me weigh this” reveals evidence-based arguments for owning, staying flat and being short; do not force equally strong arguments or three bullets per side. That support is generated without future outcomes. Store hint use.

No narrative emphasis chosen because it later explains the return. No “correct action” field in the generator's instructions. A case can be useful without an ambiguous decision or a spectacular ending; the user decides whether it belongs in the game.

## Generate 100, review consistently

Proposed batch allocation, adjustable after the first review:

| Family | Candidates |
| --- | ---: |
| Biotech before a publicly expected clinical/regulatory milestone | 15 |
| Biotech after a positive/negative/mixed disclosed development | 15 |
| Biotech financing, commercialization and portfolio decisions | 15 |
| Biotech ordinary earnings/operating updates | 15 |
| Software/growth before scheduled results or following demand updates | 10 |
| Software/growth after an observed rally | 10 |
| Software/growth after an observed decline | 10 |
| Software/growth ordinary results and normalization | 10 |
| **Total** | **100** |

Use roughly 35–50 issuers, normally no more than four cases each; allow up to six Zoom dates as a deliberate comparison set. Keep multiple dates from one issuer linked by `case_family_id`. Review them far apart in the initial queue to reduce memory contamination, then compare together when assessing variety.

The user may curate known successes, failures and uneventful histories for variety. Keep those selection labels editor-only; such a curated set is a game collection, not an unbiased investment-performance study. Business-as-usual describes the information setup; it does not promise a flat subsequent stock return.

For price-based discovery, use past-only definitions, e.g. a trailing 63-session gain of at least 40% or a decline of at least 25% from the trailing 252-session high. These thresholds are proposed sampling rules, not trading signals. A future-local-maximum test is unnecessary to find interesting rally/decline cases.

Production steps:

1. Build a larger candidate queue from issuer history, event archives and price screens. Preserve the source and selection reason.
2. Acquire complete eligible evidence, prices, corporate actions and financial history for each cutoff. Missing sources create a repair task, not a made-up number.
3. Resolve dates, versions, identifiers and units; calculate metrics deterministically.
4. Generate player sheets using only the eligible packet and the fixed template.
5. Check numerical consistency, source coverage, cutoff violations, wording spoilers and duplicated cases. Keep failed candidates out of the playable review queue.
6. Separately attach future 5/21/63/126-session returns, paths, distributions and event outcomes. The case-specific decision horizon stays fixed; include its exact exit and total return as the primary outcome. Other horizons are debrief context, not a retrospective choice of the best score.
7. Present 100 completed drafts in batches of 10. Reviewer saves a first judgment before revealing outcomes, then accepts, revises or rejects. Accepted cases become the playable collection.

Do not count seed rows, broken cases or paraphrases at an identical cutoff as 100 completed examples. If an outcome interval is incomplete, label it and repair/replace the candidate rather than silently changing the horizon.

### Review interface and stored review fields

Left: actual player sheet. Right: **Keep / Edit / Reject**, interest 1–5, clarity 1–5, information sufficient yes/no, recognizable yes/no, reason and optional field-level edits.

First save those judgments without the forward path. Then “Reveal outcome” shows the actual path, horizon returns, major subsequent disclosures, source coverage and calculation details. A second judgment can record whether the debrief is useful. Preserve both judgments; changing your mind is allowed.

Useful rejection tags: obvious from memory, insufficient evidence, overly technical, repetitive, misleading summary, missing valuation, too much noise, source/time error. A lost trade is not a rejection reason by itself.

Show queue progress, family filters and next case. Autosave; allow returning to unfinished reviews. Accepted cases with later edits require renewed acceptance of that version. Human editorial judgment is the approval gate for the collection; objective data checks must still pass.

## Generation contract

Each case is a small bundle with separate access boundaries:

| Object/file | Required contents | Who can access it |
| --- | --- | --- |
| `player.json` | Opaque ID, cutoff/horizon, identity mode, business summary, market view, financial table, developments, sector module, catalysts, source handles | Player/reviewer before commitment |
| `evidence.json` | Claim/source mappings, original document versions, source locations, availability timestamps, calculation dependencies, missing-data flags | Content builder and reviewer; player gets sanitized eligible excerpts |
| `outcome.json` | Entry/exit rules and fills, subsequent prices, distributions, event outcomes and debrief sources | Server; reviewer only after explicit reveal; player at debrief |
| `review.json` | Packet version, first-pass ratings, outcome-reveal timestamp, final keep/edit/reject, edits and notes | Editor only |

Use opaque player IDs and filenames; do not expose identity through URLs in mystery mode. Original URLs and future-relative editorial labels stay out of the player bundle. Separate `candidate_id` from a published opaque `case_id`.

Every numeric cell has `value`, `unit`, `period`, `available_at`, `source_ids`, and `status` (`reported`, `management_guidance`, `derived`, `missing`, `not_applicable`). Derived cells add `formula` and `input_ids`. Missing cells use null values with a reason. Every prose factual claim maps to eligible evidence. Interpretations are explicitly labeled.

Generator prompt contract:

> Build the player sheet in the fixed eight-block order from this evidence packet only. Cite factual clauses. Keep reported values, forecasts and calculations distinct. Preserve material contrary evidence. Mark absent information. Use neutral dates and titles. Do not predict the historical outcome or infer missing figures. Return a repair request when a required block cannot be supported. Never see outcome.json.

## Researched seeds to make the format concrete

All listed decision dates below are proposed 09:00 America/New_York cutoffs; publication anchors precede them. These are source leads, not certified packets. Full cutoff audits and market/valuation data remain required.

| Seed | Proposed cutoff | Evidence anchor and question to investigate |
| --- | --- | --- |
| Zoom early demand | 2020-03-05 | March 4 results: what can become paid demand? |
| Zoom first pandemic quarter | 2020-06-03 | June 2 results: how much expansion is sustainable? |
| Zoom after next results | 2020-09-01 | August 31 results: does the new outlook justify the entry valuation? |
| Zoom after one reaction session | 2020-09-02 | Same release plus September 1 trading: has the opportunity changed? |
| Zoom later in 2020 | 2020-12-01 | November 30 results: how durable are customers and margins? |
| Zoom normalization | 2021-08-31 | August 30 results: how does slower growth change valuation? |
| Axsome before readouts | 2019-11-08 | November 7 update: several expected milestones and financing exposure |
| Axsome after GEMINI | 2019-12-17 | December 16 positive readout: remaining development and financing risk |
| Acadia before ADVANCE-2 | 2024-02-28 | February 27 update: existing sales plus an expected Q1 readout |
| Acadia after ADVANCE-2 | 2024-03-12 | March 11 endpoint miss: reassess remaining business and pipeline |
| Sarepta after EMBARK | 2023-10-31 | October 30 mixed result: primary miss, sponsor-highlighted secondary findings |
| Vertex operating update | 2022-08-05 | August 4 results: existing franchise economics and pipeline spending |

Zoom anchors: [March 2020](https://www.sec.gov/Archives/edgar/data/1585521/000158552120000056/zm-20200304ex991.htm), [June 2020](https://www.sec.gov/Archives/edgar/data/1585521/000158552120000149/zm-20200602ex991.htm), [August 2020](https://investors.zoom.us/static-files/d07fb454-828a-4db9-9d30-c719ed70a917), [November 2020](https://investors.zoom.us/static-files/292568d1-b523-4440-b8d3-11486f3c7115), [August 2021](https://investors.zoom.us/static-files/94cb6af7-675c-468b-8475-0abec4a514ee).

Biotech anchors: [Axsome November update](https://www.globenewswire.com/news-release/2019/11/07/1943005/33090/en/axsome-therapeutics-reports-third-quarter-2019-financial-results-and-provides-business-update.html), [Axsome GEMINI readout](https://www.globenewswire.com/news-release/2019/12/16/1960786/33090/en/Axsome-Therapeutics-Announces-AXS-05-Achieves-Primary-Endpoint-in-GEMINI-Phase-3-Trial-in-Major-Depressive-Disorder.html), [Acadia February update](https://acadia.com/en-us/media/news-releases/acadia-pharmaceuticals-reports-fourth-quarter-and-full-year-2023), [Acadia March readout](https://ir.acadia.com/node/17751/pdf), [Sarepta EMBARK readout](https://investorrelations.sarepta.com/news-releases/news-release-details/sarepta-therapeutics-announces-topline-results-embark-global-0), [Vertex operating update](https://investors.vrtx.com/news-releases/news-release-details/vertex-reports-second-quarter-2022-financial-results).

These anchors establish useful changes in public information. They do not establish entry prices, squeezes, market tops, future returns or the eventual quality of a playable case. A clinical success/failure category is independent of the share-price outcome.
