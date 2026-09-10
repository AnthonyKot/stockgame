# Scene review: growth-008

## Confirmed defects

- **s1** — text: "record full-year net income of $32.5 billion and 17% ROTCE", cited to `[c1][c12]`. c1 supports the net-income figure, but c12's excerpt is "Net interest income 55,059 50,097 10" — full-year net interest income, not ROTCE. Nothing in c12 mentions ROTCE. What's wrong: the ROTCE clause is cited to the wrong claim; the actual ROTCE claim (c2: "Return on tangible common equity 14 17 8") isn't cited at all. Fix: change claim_ids to `[c1][c2]`.

- **s2** — text: "Q4 Markets revenue down 11% and full-year expense up 7%", cited to `[c2]`. c2's excerpt is "Return on tangible common equity 14 17 8" — it says nothing about Markets revenue or expense. What's wrong: wrong claim cited; the correct claims are c6 ("Markets & Investor Services revenue was $4.0 billion, down 11%") and c23 (full-year noninterest expense rose 7% to $63.4 billion). Fix: change claim_ids to `[c6][c23]`.

- **s3** — text: "provision for credit losses up 63% quarter on quarter on reserve builds", cited to `[c9]`. c9's excerpt is "Assets under management were $2.0 trillion, down 2%" — unrelated to provisions. What's wrong: wrong claim cited; the 63% QoQ figure is in c18 ("PROVISION FOR CREDIT LOSSES ... 1,548 948 ... 63"), with the reserve-build driver language in c8. Fix: change claim_ids to `[c8][c18]`.

- **voice**, sentence 1 — "...the top investment bank in the world." The only supporting evidence is c4: "#1 Global Investment Banking fees with 8.7% wallet share for the year, up 60 bps." That is a #1 ranking in IB fees specifically, not a claim about being the top investment bank overall (trading, size, or otherwise). What's wrong: population/scope overreach — a fee-wallet-share ranking is generalized into a sweeping firm-wide claim no cited evidence makes. Fix: "...#1 in global investment-banking fees, with an 8.7% wallet share."

- **voice**, sentence 2 — "trading revenue fell 11% in a bad quarter." The cited evidence for the -11% figure is c6: "Markets & Investor Services revenue was $4.0 billion, down 11%." Markets & Investor Services includes securities-services/custody revenue alongside trading (Fixed Income and Equities Markets). What's wrong: population mismatch — a broader reported segment is relabeled as pure "trading revenue." Fix: "Markets & Investor Services revenue fell 11% in a bad quarter."

- **ask_friend[1]** (q: "How bad was the quarter, really?") — "Against the third quarter, net income fell 16% as Markets revenue dropped 11% to $4.0 billion in the December sell-off and the provision for credit losses rose 63% on reserve builds..." The net-income (c22) and provision (c18) figures are explicitly quarter-over-quarter (Q3→Q4). But the cited Markets-revenue figure, c6, states "down 11% year over year" — Q4 2018 vs. Q4 2017, not vs. Q3 2018. What's wrong: a year-over-year figure is nested inside a sentence structured around sequential (QoQ) comparisons, implying all three moves are on the same quarter-over-quarter basis when one is not. Fix: "Against the third quarter, net income fell 16% as the provision for credit losses rose 63% on reserve builds in cards and commercial loans; Markets revenue was down 11% year over year to $4.0 billion in the December sell-off."

## Unsupported or unverifiable

- **ask_friend[2]** (q: "What does the full year say?") — "net interest income up 10% to $55.1 billion on higher rates and loan growth." The $55.1B/10% figure is supported by c12, and loan growth is supported by c14, but no cited claim (c1, c2, c12, c13, c14) states "higher rates" as a driver of the net-interest-income increase. Would need a management statement or source excerpt explicitly attributing the NII rise to rate increases.

- **ask_friend[4]** (q: "Is it expensive?") — "The last close is $101.68, down 10% over twelve months and 14% below the 12-month high after the December sell-off." None of the cited claims (c15, c19, c20) or any other evidence claim contains a stock price, a 12-month return, or a 12-month high. Would need a dated price source (e.g., a market-data claim with source and date) not present in evidence.json.

- **ask_friend[4]** — "Market capitalisation is about $348 billion." Cited claim c15 gives $319.8 billion at year-end 2018 (correctly reflected in the following clause, "$320 billion at year end"). The $348 billion figure has no citation and does not reconcile with either the cited $319.8B figure or the uncited close price in the same paragraph (3,275.8M shares × $101.68 ≈ $333B, not $348B). Would need a dated, sourced market-cap or price figure to support this specific number.

## Editorial preferences (not defects)

- Voice's "return on tangible equity" drops "common" from the formal metric name (ROTCE = return on tangible *common* equity); minor simplification.
- ask_friend[1]'s "home lending revenue fell 8% on thinner margins" drops the second cited driver in c10 ("and lower origination volumes"); incomplete but not incorrect.
- c7 ($2.4B net-income reduction, Q4 2017, TCJA) and c17 ($1.9B tax expense, Q4/FY2017, TCJA) give different dollar figures for what reads as the same one-time item; the scene text (ask_friend[1]) is faithful to its own cited source (c7), but a reviewer may want the two source excerpts reconciled.
- Assumption a1 ("market noise, not the credit cycle turning") is essentially the logical converse of a4 ("mark the top of the earnings cycle"); a legitimate bull/bear pairing but slightly redundant as worded.
