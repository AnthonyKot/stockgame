# Selecting the first ten stories

> Superseded product priority (9 September 2026): [MASTER_PLAN.md](../MASTER_PLAN.md) defines the main game as one chronological portfolio campaign, with a fixed historical end date and play continuing until all timed trades close. This file retains earlier work, prompts or recommendations; conflicting standalone-quiz priorities and immediate future reveals do not govern campaign development. Check current code before repeating earlier tasks.

Deliverable for this stage: 30 researched story candidates, a selected set of 10, and an MVP generation prompt containing those selections. The application is the next stage. A researched story is not yet a verified, playable financial dataset.

## Composition

- Ten quizzes total; one declared 1-, 3- or 5-calendar-year horizon per quiz.
- Target 3 one-year, 3 three-year and 4 five-year cases; adjust by one if evidence quality warrants it.
- At most two software/IT/communications cases in the final ten.
- Target four or five biotech/pharma cases, with the rest spread over consumer, retail, industrials, energy and finance.
- Include clinical uncertainty, existing commercial economics and ordinary business decisions. A company whose story is familiar can qualify when its date/horizon creates a less familiar decision, but should not dominate.
- Include positive, negative and approximately flat return screens. Aim to cover each outcome at each horizon where source quality supports it; don't claim a combination is covered without computing it.

## Selection evidence

Score 0–2 for each of: eligible contemporary-source coverage; reconstructable prices and corporate actions; a understandable economic decision; horizon-specific relevance; novelty relative to the other selections. Scores aid editorial selection and are not measurements of investing skill.

Reject or reserve cases with source errors, already-revealed event results in pre-event facts, unavailable delisted price history, excessive corporate-action reconstruction, unsupported clinical claims or near-duplicate teaching value. Keep the candidate record and rejection reason, rather than deleting inconvenient outcomes from the pool.

## Price screening convention

Candidate screening uses cached Yahoo daily adjusted-close series as an approximate total-return proxy. Order placed at the proposed premarket cutoff fills at the first available regular-session close on or after that date; exit at the first available close on or after the calendar-year anniversary of the actual entry date. Leap-day anniversaries clamp to February 28. This closing-price convention is for screening only; the final game must declare and implement its own execution contract consistently.

Calculate cumulative return, elapsed-day CAGR, maximum daily drawdown, and an identically timed SPY benchmark return. A positive/negative/flat screening label uses CAGR above +5%, below -5%, or between those bounds. This is an editorial grouping, NOT a statement that buy/short/cash was the objectively correct choice. No trading costs, borrow availability, taxes or margin constraints are included in this screen. Dividends and splits follow the vendor's adjustment factors. Spin-offs, mergers, distributed securities and delistings require a separate ledger before final scoring.

The point-in-time player chart must not use future-adjusted values or future corporate identities. The cached full series is outcome/research data and must never be shipped in a pre-decision payload.

## Source verification

Claude returns source URLs and whether it opened them. Independently check selected source content, dates, security identity, and at least one material fact per case. Verify any source identified as publication-before-cutoff rather than assuming the accounting period establishes eligibility. Store source-access failures and evidence gaps. A current news archive or a search result is only a lead until the historical document is located.

## MVP prompt

Embed the selected ten identifiers, exact proposed cutoffs and horizons, neutral decision questions, primary evidence links, screened outcomes as server/editor-only metadata, and unresolved repair tasks. Explicitly require verification of remaining gaps before quiz publication. The prompt must not instruct the model to fabricate missing financial tables, valuations, prices or news.
