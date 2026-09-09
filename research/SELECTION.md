# Selected ten (2026-09-09)

Stage deliverable per research/SELECTION_RULES.md: 30 researched candidates (research/candidates-screened.json), a selected set of 10 (research/selected.json), and an MVP generation prompt (research/MVP_PROMPT.md). Verification records: research/verification/{clinical,commercial,growth}.json (Sonnet) and editor-checks.json (EDGAR pulls by the main session). Three Haiku attempts were rejected and kept as *.haiku-rejected.json.

## The ten

| # | id | ticker | cutoff | h | sector | CAGR | SPY cumulative | group | score | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | growth-007 | FSLR | 2022-03-02 | 1y | energy (solar manufacturing) | 185.37% | -7.68% | up | 10/10 | pass |
| 2 | growth-009 | HSY | 2023-02-03 | 1y | consumer staples | -15.15% | 21.26% | down | 10/10 | repair |
| 3 | clinical-axsm-2019 | AXSM | 2019-12-17 | 1y | biotech (clinical) | -5.0% | 18.73% | down | 9/10 | repair |
| 4 | growth-005 | DE | 2020-08-24 | 3y | industrials | 24.97% | 33.28% | up | 10/10 | repair |
| 5 | growth-004 | TGT | 2021-03-03 | 3y | retail | -2.39% | 40.41% | roughly_flat | 9/10 | repair |
| 6 | clinical-srpt-2021 | SRPT | 2021-01-08 | 3y | biotech (clinical) | 7.64% | 30.14% | up | 10/10 | repair |
| 7 | growth-008 | JPM | 2019-01-16 | 5y | finance | 13.74% | 97.47% | up | 10/10 | repair |
| 8 | commercial-gilead-2019 | GILD | 2019-02-05 | 5y | pharma (commercial) | 6.76% | 95.71% | up | 9/10 | repair |
| 9 | clinical-mdgl-2018 | MDGL | 2018-11-13 | 5y | biotech (clinical) | -0.03% | 75.88% | roughly_flat | 10/10 | repair |
| 10 | clinical-nktr-2018 | NKTR | 2018-02-15 | 5y | biotech (clinical) | -48.05% | 65.14% | down | 10/10 | repair |

Screen figures are the vendor adjusted-close proxy from scripts/screen_candidate_returns.py: no costs, no borrow, editor-only. They are never part of the player packet.

## Why these ten

- **Horizons:** 3 one-year (FSLR, HSY, AXSM), 3 three-year (DE, TGT, SRPT), 4 five-year (JPM, GILD, MDGL, NKTR).
- **Sectors:** five biotech/pharma (four clinical-uncertainty stories, one commercial-economics story), then consumer, retail, industrials, energy, finance. No software/IT case in the ten; Zoom June 2020 is the first IT alternate because it matches the original brief's mid-2020 setting despite high recognition risk.
- **Decision types:** clinical readouts (AXSM, SRPT, MDGL), a partnership-as-validation question (NKTR), a legacy-franchise value question (GILD), and five ordinary operating updates (guidance cut at FSLR, pricing-led growth at HSY, trough-or-decline at DE, no-guidance at TGT, record profit after a sell-off at JPM).
- **Outcomes:** up, down and flat all appear, but not at every horizon. See gaps.
- **Corporate actions:** none of the ten has a split, spin-off or delisting inside its window (cached vendor events checked). Dividends only for HSY, DE, TGT, JPM, GILD.

## Corrections made during verification

- Nektar: announcement was premarket 2018-02-14 (8-K accepted 08:31 ET), cutoff moved to 2018-02-15.
- Acadia (alternate): release premarket 2021-04-05 (8-K 08:08 ET), cutoff moved to 2021-04-06; screen moved from down to roughly flat.
- Exelixis (alternate): release after close 2018-02-26 (8-K 16:08 ET), cutoff moved to 2018-02-27.
- Axsome: as-of fact #2 named STRIDE-1 as the prior positive trial; the release names ASCEND. Corrected.
- Learning-tension text rewritten for HSY, DE and SRPT to remove outcome references. The field is editor-only either way.

## Gaps the pool cannot fill

- No one-year roughly-flat case. AXSM sits exactly on the -5% boundary and is labelled down.
- No three-year down case anywhere in the 30 after the Acadia correction.
- Four clinical leads (SAGE, FGEN, ICPT, BLUE) are delisted and have no price history; they need a delisted-securities price source before they can return to the pool.
- Both gaps are inputs to the next research batch, not claims of coverage.

## Open repairs on the ten (must close before quiz publication)

- **HSY:** learning_tension rewritten (editor) to remove the 2024 cocoa reference; second source (Nasdaq.com) timed out; EDGAR 8-K used instead (done)
- **AXSM:** fact #2 corrected to ASCEND (done, EDGAR); drop the Motley Fool outcome source or keep as colour only
- **DE:** learning_tension rewritten (editor) to remove "eventual agricultural upcycle"
- **TGT:** second source (CNBC) blocked 403; keep primary only or find an archive copy
- **SRPT:** learning_tension rewritten (editor) to remove the 50% single-day decline; outcome source timed out; substitute an FDA/issuer Elevidys approval source dated June 2023
- **JPM:** both worker fetches failed; EDGAR 8-K verified by editor (done)
- **GILD:** drop dead schedule URL (done, EDGAR index); outcome source dated 2026; find a source near the 2024-02-05 exit
- **MDGL:** outcome-only Lancet IR page unreachable; substitute PubMed/DOI page; exact presentation time on 2018-11-12 unconfirmed; treat as after-hours
- **NKTR:** cutoff corrected to 2018-02-15 (done, EDGAR); drop the Nasdaq.com "11% spike" source; unverified

## Alternates (score) and reserve

Alternates: ACAD 3y (9), ALNY 3y (9), NBIX 1y (9), ZM 1y (9), BMRN 3y (8), EXEL 5y (8), BIIB 3y (8), XOM 5y (8), REGN 5y (7), INCY 3y (7), HRMY 1y (7), NKE 5y (7).

Reserve with reason: SAGE: delisted, no price history; worker found fact #3 misattributed and a spoiler in learning_tension; FGEN: delisted, no price history; secondary source is post-cutoff; ICPT: delisted, no price history; approval date and vote unconfirmed verbatim; BLUE: delisted, no price history; 2seventy spin-off and reverse split inside window; spoiler words in facts; AMGN: near-duplicate of Gilead/Regeneron teaching value; fact cites a source id absent from the list; MRK: Organon spin-off 2021-06-03 inside the window needs a distributed-securities ledger before scoring; GOOGL: high recognition, IT; second source unverified.

Rejected: GE 2018. REJECT: learning_tension states the Oct 2018 outcome; facts cite an unopened source with the wrong date; 1:8 reverse split + two spin-offs inside window
