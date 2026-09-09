# MVP generation prompt: ten historical investing quizzes

> Superseded product priority (9 September 2026): [MASTER_PLAN.md](../MASTER_PLAN.md) defines the main game as one chronological portfolio campaign, with a fixed historical end date and play continuing until all timed trades close. This file retains earlier work, prompts or recommendations; conflicting standalone-quiz priorities and immediate future reveals do not govern campaign development. Check current code before repeating earlier tasks.

You are generating the first ten playable cases for a historical investing game. Read FRAMEWORK.md and CASE_FORMAT.md first; CASE_FORMAT.md is the presentation contract. This prompt fixes WHICH ten cases, their exact cutoffs and horizons, the evidence you may use, and the repairs that must be closed before any case is published. Selection record: research/SELECTION.md and research/selected.json.

## Hard rules

1. **Point-in-time invariant.** Every fact in a player packet must have been public before the case's cutoff. The reporting period does not establish this; the publication timestamp does. When only a date is known, the fact is eligible from the next regular session.
2. **No fabrication.** Do not invent financial tables, valuations, consensus estimates, prices, volumes, news or URLs. If a data point is missing, write `null` with a reason and add it to `missing_data`. A case with missing core price or financial evidence is `status: blocked`, never `playable`.
3. **No outcome leakage.** Nothing under `outcome` (screens, retrospective story, later filings) may appear in the briefing, evidence cards, chart, peer table, title or question. Do not use future-relative words (later, eventually, subsequently, ultimately, ahead of, before the crash) anywhere in player-visible text.
4. **Sources.** Use the primary sources listed per case, plus SEC EDGAR filings for the same issuer dated before the cutoff. Local copies of several filings are in research/sources/. Every factual clause in a briefing cites a source id. Uncited claims fail publication.
5. **Execution contract.** Decision at cutoff (09:00 America/New_York); fill at the next regular-session open; exit at the first regular-session open on or after the calendar anniversary of the entry date, leap days clamp to Feb 28. State this in every packet. The editor-only screen below uses closes, not opens, and is not the game's scoring.
6. **Identity masking.** Produce both a transparent and a masked variant of each briefing. In the masked variant remove issuer name, ticker, product brand names, executive names and identifiable URLs; keep sector, economics, dates and macro context. Never alter numbers or dates to hide identity.
7. **Output.** One JSON file per case following the eight-block structure in CASE_FORMAT.md, with `status` one of research_draft | blocked | review_ready. Nothing is `published` from this prompt; a human reviews every case.

## The ten cases

Fields: security, cutoff (ISO with offset), horizon, proposed exit date, neutral title, player question, as-of facts with sources, primary evidence, editor-only outcome metadata, open repairs.

### 1. growth-007

- **Security:** First Solar, Inc., FSLR (NASDAQ), common stock
- **Cutoff:** 2022-03-02T09:00:00-05:00  **Horizon:** 1 calendar year(s)  **Proposed exit:** 2023-03-02 (first session on/after)
- **Sector:** energy (solar manufacturing)  **Recognition risk:** low
- **Neutral title:** A solar panel manufacturer guides next-year earnings sharply lower than the year just reported
- **Player question:** When a solar manufacturer reports full-year EPS of $4.38 but guides next-year EPS to a range of $0.00-$0.60 -- implying a steep earnings decline -- does the market treat this as a temporary cost/input squeeze or a structural margin problem?
- **As-of facts (verified to source unless noted in repairs):**
  - Full-year 2021 net sales were about $2.9 billion with diluted EPS of $4.38; Q4 2021 net sales were $0.9 billion with diluted EPS of $1.23. [s1, 2022-03-01]
  - 2022 guidance: net sales of $2.4-$2.6 billion and diluted EPS of only $0.00-$0.60, alongside gross profit guidance of $155-$215 million including $10-15 million of underutilization losses. [s1, 2022-03-01]
  - Full-year 2021 EPS came in above the midpoint of guidance given at the Q3 2021 call and within the original February 2021 guidance range. [s1, 2022-03-01]
- **Primary evidence (as-of role only):**
  - s1: https://www.sec.gov/Archives/edgar/data/1274494/000127449422000008/ex991pressreleaseq4-2021fi.htm (published 2022-03-01, opened by verifier=True)
  - s2: https://www.globenewswire.com/news-release/2022/03/01/2394850/0/en/First-Solar-Inc-Announces-Fourth-Quarter-and-Full-Year-2021-Financial-Results-and-2022-Guidance.html (published 2022-03-01, opened by verifier=False)
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2022-03-02 → exit 2023-03-02, CAGR 185.37%, cumulative 185.17%, SPY -7.68%, max drawdown -27.41%, group up; vendor adjusted close, no costs.
- **Learning tension (editor only):** A sharp forward EPS guidance cut (roughly 90%+ at the low end) from a company that just beat its own prior guidance; tests whether players weight management's own forward number over the trailing beat.
- **Open repairs before publication:** none recorded

### 2. growth-009

- **Security:** The Hershey Company, HSY (NYSE), common stock
- **Cutoff:** 2023-02-03T09:00:00-05:00  **Horizon:** 1 calendar year(s)  **Proposed exit:** 2024-02-03 (first session on/after)
- **Sector:** consumer staples  **Recognition risk:** low
- **Neutral title:** A confectionery company reports strong pricing-driven growth and guides for continued but slower expansion
- **Player question:** When a consumer packaged-goods company posts double-digit sales and EPS growth driven mainly by price increases, and guides next year to single-digit sales growth with margin pressure from cost inflation still expected, does the pricing strategy have more room to run or is it approaching its limit?
- **As-of facts (verified to source unless noted in repairs):**
  - Q4 2022 net sales were $2,652.3 million, up 14.0%, with adjusted diluted EPS of $2.02, up 19.5%; full-year 2022 net sales were $10,419.3 million, up 16.1%. [s1, 2023-02-02]
  - 2023 guidance called for net sales growth of 6-8% and adjusted EPS growth of 9-11%, versus the much higher 2022 growth rates. [s1, 2023-02-02]
  - The release attributed 2022 growth primarily to 'net price realization' offsetting 'broad-based cost of goods inflation,' without singling out cocoa costs specifically at this release. [s1, 2023-02-02]
- **Primary evidence (as-of role only):**
  - s1: https://www.prnewswire.com/news-releases/hershey-reports-fourth-quarter-and-full-year-2022-financial-results-provides-2023-outlook-301736709.html (published 2023-02-02, opened by verifier=True)
  - s2: https://www.nasdaq.com/press-release/hershey-reports-fourth-quarter-and-full-year-2022-financial-results-provides-2023 (published 2023-02-02, opened by verifier=False)
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2023-02-03 → exit 2024-02-05, CAGR -15.15%, cumulative -15.22%, SPY 21.26%, max drawdown -34.03%, group down; vendor adjusted close, no costs.
- **Learning tension (editor only):** Double-digit growth driven mainly by price increases, with management guiding to single-digit sales growth and continued cost inflation: is the deceleration ordinary normalisation or the first sign that pricing power is running out?
- **Open repairs before publication:** learning_tension rewritten (editor) to remove the 2024 cocoa reference; second source (Nasdaq.com) timed out; EDGAR 8-K used instead (done)

### 3. clinical-axsm-2019

- **Security:** Axsome Therapeutics, Inc., AXSM (NASDAQ), common stock
- **Cutoff:** 2019-12-17T09:00:00-05:00  **Horizon:** 1 calendar year(s)  **Proposed exit:** 2020-12-17 (first session on/after)
- **Sector:** biotech (clinical)  **Recognition risk:** medium
- **Neutral title:** A small depression-drug developer reports its first pivotal Phase 3 result
- **Player question:** A clinical-stage biotech with one approved franchise attempt (none yet) reports that its lead combination drug hit its primary endpoint in a pivotal MDD trial. Does a single positive pivotal readout in a company with no approved products yet justify taking a position, given remaining regulatory and commercial risk?
- **As-of facts (verified to source unless noted in repairs):**
  - On December 16, 2019, Axsome announced AXS-05 (dextromethorphan-bupropion) achieved the primary endpoint (MADRS score reduction) versus placebo in the pivotal Phase 3 GEMINI trial in major depressive disorder. [axsm-pr-1, 2019-12-16]
  - GEMINI was the second positive well-controlled trial of AXS-05 in MDD, following the previously completed ASCEND study; the company said the two trials together were expected to support an NDA submission. [axsm-pr-1, 2019-12-16]
  - As of Q3 2019 (reported November 7, 2019), Axsome had no FDA-approved products and stated GEMINI topline results were expected in Q4 2019. [axsm-q3-2019, 2019-11-07]
- **Primary evidence (as-of role only):**
  - axsm-pr-1: https://www.globenewswire.com/news-release/2019/12/16/1960786/33090/en/Axsome-Therapeutics-Announces-AXS-05-Achieves-Primary-Endpoint-in-GEMINI-Phase-3-Trial-in-Major-Depressive-Disorder.html (published 2019-12-16, opened by verifier=True)
  - axsm-q3-2019: https://www.globenewswire.com/news-release/2019/11/07/1943005/0/en/Axsome-Therapeutics-Reports-Third-Quarter-2019-Financial-Results-and-Provides-Business-Update.html (published 2019-11-07, opened by verifier=True)
- **Editor correction:** as_of_facts[1].fact: 8-K 0001558370-19-011521 (accepted 2019-12-16 08:25 ET) names ASCEND, not STRIDE-1, as the prior positive trial; STRIDE-1 was still ongoing in TRD
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2019-12-17 → exit 2020-12-17, CAGR -5.0%, cumulative -5.01%, SPY 18.73%, max drawdown -61.22%, group down; vendor adjusted close, no costs.
- **Learning tension (editor only):** A second positive pivotal trial materially de-risks an NDA-track asset, but the stock had already run up sharply on anticipation and on an earlier positive trial, so the marginal informational value of a 'confirming' readout versus price already paid is the real tension.
- **Open repairs before publication:** fact #2 corrected to ASCEND (done, EDGAR); drop the Motley Fool outcome source or keep as colour only

### 4. growth-005

- **Security:** Deere & Company, DE (NYSE), common stock
- **Cutoff:** 2020-08-24T09:00:00-04:00  **Horizon:** 3 calendar year(s)  **Proposed exit:** 2023-08-24 (first session on/after)
- **Sector:** industrials  **Recognition risk:** medium
- **Neutral title:** An agricultural and construction equipment maker reports a sales decline alongside a restructuring plan
- **Player question:** When a cyclical industrial reports an 11% revenue decline, forecasts a full-year sales drop across most segments, and announces cost-cutting layoffs, is this a trough signaling recovery or a cyclical business in genuine decline?
- **As-of facts (verified to source unless noted in repairs):**
  - Q3 FY2020 (ended Aug 2, 2020) net income was $811 million, or $2.57 per diluted share, down from $899 million a year earlier; net sales and revenues fell 11% to $8.925 billion. [s1, 2020-08-21]
  - Company forecast full-year FY2020 net income of approximately $2.25 billion, with agriculture and turf equipment sales expected down about 10%. [s1, 2020-08-21]
  - Deere announced broad employee-separation programs for Q4 2020 with about $175 million in pretax charges and an estimated $175 million in annual savings. [s1, 2020-08-21]
- **Primary evidence (as-of role only):**
  - s1: https://www.sec.gov/Archives/edgar/data/315189/000155837020010785/de-20200821xex99d1.htm (published 2020-08-21, opened by verifier=True)
  - s2: https://www.prnewswire.com/news-releases/deere-reports-third-quarter-net-income-of-811-million-301116126.html (published 2020-08-21, opened by verifier=False)
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2020-08-24 → exit 2023-08-24, CAGR 24.97%, cumulative 95.1%, SPY 33.28%, max drawdown -33.81%, group up; vendor adjusted close, no costs.
- **Learning tension (editor only):** A declining-revenue quarter paired with proactive cost cuts and cautious commentary; tests whether players read restructuring as weakness or as prudent management of a cyclical business whose next turn is not yet visible.
- **Open repairs before publication:** learning_tension rewritten (editor) to remove "eventual agricultural upcycle"

### 5. growth-004

- **Security:** Target Corporation, TGT (NYSE), common stock
- **Cutoff:** 2021-03-03T09:00:00-05:00  **Horizon:** 3 calendar year(s)  **Proposed exit:** 2024-03-03 (first session on/after)
- **Sector:** retail  **Recognition risk:** medium
- **Neutral title:** A big-box retailer reports a pandemic-year sales surge but declines to give forward guidance
- **Player question:** When a retailer posts historic comparable-sales and digital growth for the pandemic year but explicitly withholds forward guidance due to uncertainty, how should investors price a business with no visible forward anchor?
- **As-of facts (verified to source unless noted in repairs):**
  - Q4 FY2020 comparable sales grew 20.5%, with digital comparable sales up 118%; full-year digital sales grew 145%. [s1, 2021-03-02]
  - Full-year FY2020 GAAP EPS from continuing operations was $8.64, versus $6.34 in FY2019. [s1, 2021-03-02]
  - Target explicitly stated it was 'not providing sales and EPS guidance for Fiscal 2021 and beyond' due to continued COVID-19 uncertainty. [s1, 2021-03-02]
- **Primary evidence (as-of role only):**
  - s1: https://www.sec.gov/Archives/edgar/data/27419/000002741921000007/a2020q4ex-99.htm (published 2021-03-02, opened by verifier=True)
  - s2: https://www.cnbc.com/2021/03/02/target-tgt-earnings-q4-2020.html (published 2021-03-02, opened by verifier=False)
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2021-03-03 → exit 2024-03-04, CAGR -2.39%, cumulative -7.01%, SPY 40.41%, max drawdown -58.87%, group roughly_flat; vendor adjusted close, no costs.
- **Learning tension (editor only):** A record year with an explicit 'no guidance' disclaimer; tests whether players treat absence of guidance as a red flag or ignore it given strong trailing results.
- **Open repairs before publication:** second source (CNBC) blocked 403; keep primary only or find an archive copy

### 6. clinical-srpt-2021

- **Security:** Sarepta Therapeutics, Inc., SRPT (NASDAQ), common stock
- **Cutoff:** 2021-01-08T09:00:00-05:00  **Horizon:** 3 calendar year(s)  **Proposed exit:** 2024-01-08 (first session on/after)
- **Sector:** biotech (clinical)  **Recognition risk:** medium
- **Neutral title:** A gene therapy hits its biological target but misses the functional goal in a placebo-controlled trial
- **Player question:** A Duchenne muscular dystrophy gene therapy meets its primary biological endpoint (protein expression) but misses statistical significance on the primary functional motor-score endpoint in a randomized, placebo-controlled trial -- though a pre-specified age subgroup (4-5 year-olds) does show significance. Note: this record replaces the originally suggested 2020 date; the actual topline announcement was January 7, 2021. Does a mechanistically-confirmed but functionally-inconclusive readout, rescued only by a subgroup analysis, represent a real efficacy signal or a statistical near-miss dressed up as one?
- **As-of facts (verified to source unless noted in repairs):**
  - On January 7, 2021, Sarepta announced Part 1 topline results of Study SRP-9001-102 (41 patients): the trial met its primary biological endpoint (micro-dystrophin expression at 12 weeks) but did not achieve statistical significance on the primary functional endpoint (NSAA total score at 48 weeks). [srpt-pr-1, 2021-01-07]
  - In the pre-specified 4-5 year-old age subgroup, SRP-9001-treated patients showed a statistically significant 4.3-point NSAA improvement versus age-matched placebo at 48 weeks. [srpt-pr-1, 2021-01-07]
  - No new safety signals were identified in the trial, per the same release; the company said imbalance between treatment arms may have undermined the overall functional result. [srpt-pr-1, 2021-01-07]
- **Primary evidence (as-of role only):**
  - srpt-pr-1: https://www.globenewswire.com/news-release/2021/01/07/2155237/0/en/Sarepta-Therapeutics-Announces-Top-line-Results-for-Part-1-of-Study-102-Evaluating-SRP-9001-its-Investigational-Gene-Therapy-for-the-Treatment-of-Duchenne-Muscular-Dystrophy.html (published 2021-01-07, opened by verifier=False)
  - srpt-fool-1: https://www.fool.com/investing/2021/01/08/why-sarepta-therapeutics-stock-is-crashing-today (published 2021-01-08, opened by verifier=False)
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2021-01-08 → exit 2024-01-08, CAGR 7.64%, cumulative 24.69%, SPY 30.14%, max drawdown -57.18%, group up; vendor adjusted close, no costs.
- **Learning tension (editor only):** A result that is scientifically ambiguous rather than a clean failure (biological endpoint met, functional endpoint missed, one pre-specified subgroup significant); tests whether headline endpoint-miss framing crowds out the harder question of what the data actually support over a multi-year horizon.
- **Open repairs before publication:** learning_tension rewritten (editor) to remove the 50% single-day decline; outcome source timed out; substitute an FDA/issuer Elevidys approval source dated June 2023

### 7. growth-008

- **Security:** JPMorgan Chase & Co., JPM (NYSE), common stock
- **Cutoff:** 2019-01-16T09:00:00-05:00  **Horizon:** 5 calendar year(s)  **Proposed exit:** 2024-01-16 (first session on/after)
- **Sector:** finance  **Recognition risk:** medium
- **Neutral title:** A large bank reports record annual profit at the end of a rate-hiking cycle amid a volatile quarter for markets
- **Player question:** When the largest U.S. bank reports record full-year net income and a 17% return on tangible common equity, but the quarter closed during a sharp market sell-off (Q4 2018), does record profitability or the deteriorating trading/market backdrop matter more for a multi-year holding?
- **As-of facts (verified to source unless noted in repairs):**
  - Q4 2018 net income was $7.1 billion ($1.98/share) on revenue of nearly $27 billion; full-year 2018 net income was a record $32.5 billion ($9.00/share) on revenue of $111.5 billion. [s1, 2019-01-15]
  - Full-year 2018 return on tangible common equity was 17%, versus 14% for the fourth quarter alone. [s1, 2019-01-15]
  - Management cited solid underlying drivers -- core loan and deposit growth, consumer spending, and credit performance -- despite the Q4 market volatility. [s1, 2019-01-15]
- **Primary evidence (as-of role only):**
  - s1: https://www.businesswire.com/news/home/20190115005414/en/JPMorgan-Chase-Reports-Fourth-Quarter-Full-Year-2018-Financial (published 2019-01-15, opened by verifier=False)
  - s2: https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2018/4th-quarter/4q18-earnings-press-release.pdf (published 2019-01-15, opened by verifier=False)
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2019-01-16 → exit 2024-01-16, CAGR 13.74%, cumulative 90.36%, SPY 97.47%, max drawdown -43.63%, group up; vendor adjusted close, no costs.
- **Learning tension (editor only):** Record annual results announced right after a sharp Q4 2018 equity sell-off; tests whether players separate a bank's fundamental earnings power from a market-wide volatility episode occurring in the same reporting period.
- **Open repairs before publication:** both worker fetches failed; EDGAR 8-K verified by editor (done)

### 8. commercial-gilead-2019

- **Security:** Gilead Sciences, Inc., GILD (NASDAQ), common stock
- **Cutoff:** 2019-02-05T09:00:00-05:00  **Horizon:** 5 calendar year(s)  **Proposed exit:** 2024-02-05 (first session on/after)
- **Sector:** pharma (commercial)  **Recognition risk:** medium
- **Neutral title:** An HIV/HCV giant closes out the year with a new launch ramping
- **Player question:** Gilead's FY2018 results were shaped by Biktarvy's HIV launch offsetting a declining, saturated hepatitis-C franchise; is a cash-rich, largely single-therapeutic-area (virology) major pharma set for renewed growth, or is it a value trap facing HCV cliff and thin late-stage oncology diversification?
- **As-of facts (verified to source unless noted in repairs):**
  - Gilead released fourth-quarter and full-year 2018 financial results on Monday, February 4, 2019, after market close. [gild-q4-2018-schedule, 2019-01-XX]
  - Growth in Q4 2018 total revenue was attributed primarily to the 2018 launch of Biktarvy (bictegravir/emtricitabine/tenofovir alafenamide) in HIV. [gild-q4-2018-pr, 2019-02-04]
  - Gilead's hepatitis C (HCV) franchise continued a multi-year secular decline as the curable-patient pool shrank, a known structural headwind heading into 2019. [gild-q4-2018-pr, 2019-02-04]
- **Primary evidence (as-of role only):**
  - gild-q4-2018-schedule: http://investors.gilead.com/news-releases/news-release-details/gilead-sciences-release-fourth-quarter-and-full-year-2018 (published 2019-01-XX, opened by verifier=False)
  - gild-q4-2018-pr: https://www.gilead.com/news/news-details/2019/gilead-sciences-announces-fourth-quarter-and-full-year-2018-financial-results (published 2019-02-04, opened by verifier=False)
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2019-02-05 → exit 2024-02-05, CAGR 6.76%, cumulative 38.7%, SPY 95.71%, max drawdown -30.47%, group up; vendor adjusted close, no costs.
- **Learning tension (editor only):** A cash-generative franchise leader with a declining legacy segment (HCV) versus an unproven pipeline/M&A diversification strategy (oncology) whose payoff took years to show up.
- **Open repairs before publication:** drop dead schedule URL (done, EDGAR index); outcome source dated 2026; find a source near the 2024-02-05 exit

### 9. clinical-mdgl-2018

- **Security:** Madrigal Pharmaceuticals, Inc., MDGL (NASDAQ), common stock
- **Cutoff:** 2018-11-13T09:00:00-05:00  **Horizon:** 5 calendar year(s)  **Proposed exit:** 2023-11-13 (first session on/after)
- **Sector:** biotech (clinical)  **Recognition risk:** medium
- **Neutral title:** A small-cap presents positive Phase 2 liver-disease data in a high-profile conference plenary session
- **Player question:** A small biotech's NASH candidate hits its primary endpoint (liver fat reduction) and shows biopsy-based secondary benefits in a 125-patient Phase 2 trial, presented in a Presidential Plenary session at the field's top annual conference -- a mark of scientific prominence. Does high-profile conference placement plus statistically significant Phase 2 data on a surrogate/biopsy endpoint justify treating a NASH drug as substantially de-risked, given the field's history of Phase 3 failures?
- **As-of facts (verified to source unless noted in repairs):**
  - On November 12, 2018, Madrigal presented Phase 2 results for MGL-3196 (resmetirom) in a Presidential Plenary Clinical Session at The Liver Meeting 2018 (AASLD), reporting statistically significant reduction in hepatic fat (MRI-PDFF) at week 12, the primary endpoint, sustained through week 36. [mdgl-liver-meeting, 2018-11-12]
  - Secondary endpoints included statistically significant reduction/resolution of NASH on liver biopsy and improvement in fibrosis biomarkers and liver enzymes, per the same release. [mdgl-liver-meeting, 2018-11-12]
  - The trial also reported an LDL-cholesterol-lowering effect (18.8% overall, 21% in the optimal-dose subgroup), a secondary metabolic signal beyond the liver-specific endpoints. [mdgl-liver-meeting, 2018-11-12]
- **Primary evidence (as-of role only):**
  - mdgl-liver-meeting: https://www.globenewswire.com/news-release/2018/11/12/1649875/0/en/Phase-2-Results-for-Madrigal-s-MGL-3196-in-Non-Alcoholic-Steatohepatitis-NASH-Presented-during-Presidential-Plenary-Clinical-Session-of-The-Liver-Meeting-2018.html (published 2018-11-12, opened by verifier=False)
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2018-11-13 → exit 2023-11-13, CAGR -0.03%, cumulative -0.16%, SPY 75.88%, max drawdown -61.78%, group roughly_flat; vendor adjusted close, no costs.
- **Learning tension (editor only):** Phase 2 surrogate-endpoint success (fat reduction, biopsy improvement) in NASH has historically had a poor track record of translating into Phase 3 approval across the industry; the tension is whether strong biomarker data plus prominent conference placement should outweigh base-rate skepticism about NASH drug development.
- **Open repairs before publication:** outcome-only Lancet IR page unreachable; substitute PubMed/DOI page; exact presentation time on 2018-11-12 unconfirmed; treat as after-hours

### 10. clinical-nktr-2018

- **Security:** Nektar Therapeutics, NKTR (NASDAQ), common stock
- **Cutoff:** 2018-02-15T09:00:00-05:00  **Horizon:** 5 calendar year(s)  **Proposed exit:** 2023-02-15 (first session on/after)
- **Sector:** biotech (clinical)  **Recognition risk:** medium
- **Neutral title:** A mid-cap biotech signs a multibillion-dollar oncology partnership with a major pharma
- **Player question:** Bristol-Myers Squibb pays $1 billion upfront plus an $850 million equity stake at a large premium for rights to a Phase 1/2 immuno-oncology candidate (NKTR-214) being tested across 20+ tumor indications, before any pivotal data exists. Does a large pharma's willingness to pay a premium validate the science enough to buy in, or does the deal price mostly reflect optionality on unproven early-stage data?
- **As-of facts (verified to source unless noted in repairs):**
  - On February 13, 2018 (effective April 3, 2018), Nektar and Bristol-Myers Squibb announced a Strategic Collaboration Agreement for NKTR-214 (bempegaldesleukin): $1.0 billion upfront cash plus an $850 million equity investment (8,284,600 shares at $102.60/share), and up to $1.78 billion in additional milestones. [nktr-pr-1, 2018-02-13]
  - The companies planned to jointly develop NKTR-214 in combination with Opdivo and Opdivo+Yervoy across more than 20 indications in 9 tumor types, with Nektar retaining 65% and BMS 35% of U.S. profit/loss share. [nktr-pr-1, 2018-02-13]
  - At the time of the deal, NKTR-214 had only Phase 1/2 data; no pivotal Phase 3 trial had yet read out. [nktr-fool-2018, 2018-10-02]
- **Primary evidence (as-of role only):**
  - nktr-pr-1: https://ir.nektar.com/news-releases/news-release-details/bristol-myers-squibb-and-nektar-therapeutics-announce-global (published 2018-02-13, opened by verifier=False)
  - nktr-nasdaq-1: https://www.nasdaq.com/articles/megadeal-caused-nektar-therapeutics-11-spike-today-2018-02-14 (published 2018-02-14, opened by verifier=False)
- **Editor correction:** proposed_cutoff: 8-K 0001193125-18-044320 accepted 2018-02-14 08:31 ET (premarket); agreement dated Feb 13, announced Feb 14 premarket, so next session is Feb 15
- **Editor-only outcome metadata (server side, never in the packet):** screen entry 2018-02-15 → exit 2023-02-15, CAGR -48.05%, cumulative -96.21%, SPY 65.14%, max drawdown -98.13%, group down; vendor adjusted close, no costs.
- **Learning tension (editor only):** A large pharma paying a premium for early-stage data is a strong signal but not proof of eventual efficacy; the multi-year gap between deal signing and pivotal readout is exactly the kind of horizon where 'smart money validation' can still be wrong.
- **Open repairs before publication:** cutoff corrected to 2018-02-15 (done, EDGAR); drop the Nasdaq.com "11% spike" source; unverified

## Repairs that apply to every case

- Verify the exact public release time of each as-of source against the EDGAR acceptance timestamp or the wire dateline; the cutoff rule is next session after an after-close release, or the session after next for a premarket same-day release.
- Build the player chart from prices adjusted only for actions effective by the cutoff; the cached full series in research/prices/ is outcome data and must not ship.
- Replace any secondary source that could not be opened (CNBC, Nasdaq.com, BusinessWire 403s) with an archive copy or the SEC exhibit, or drop it. A search snippet is a lead, not a source.
- For GILD, DE, TGT, JPM and HSY, list every dividend inside the window from the cached vendor events and mark them as vendor data pending a corporate-action ledger.
- Peer tables: only peers whose comparable figures were public before the cutoff, each with its own source id. If no clean peer set exists, omit the table and say so.

## What not to do

- Do not backfill guidance from later actuals, do not quote today's restated figures for a historical period, and do not describe an observed move as a short squeeze without positioning evidence.
- Do not balance or reorder the ten by outcome. The set was frozen before this prompt; outcome groups are recorded above only so the editor can check coverage.
- Do not draft cases for the alternates or reserve list (see research/selected.json) unless one of the ten is blocked and the editor swaps it in explicitly.
