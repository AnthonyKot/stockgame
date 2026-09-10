# Scene review: clinical-mdgl-2018 (Madrigal Pharmaceuticals, cutoff 2018-11-13)

## Confirmed defects

- **ask_friend[2].a** ("How much is already in the price?"): "The last close is $186.51, up more than 300% over twelve months but 41% below the 12-month high. Market capitalisation is about $2.9 billion with about $482 million of net cash [c10]..." — c10 only supports "Net cash ... was about $481.9 million at 30 Sep 2018"; no claim gives a share price, 12-month range, or market cap. `player.json.financial_snapshot` marks market cap `"status": "missing"`, noting "historical closing share price is not included in the eligible source packet," and the packet deliberately excluded the June offering's per-share price "to avoid disclosing a market-price-adjacent figure." Wrong: fabricates/leaks price data the packet was built to exclude. Fix: "Net cash is about $482 million [c10]; no revenue, so no multiple. Share price is not in this packet."

- **ask_friend[1].a** ("Can they fund a Phase 3?"): "...that rate predates a 900-patient Phase 3, which management says it plans to start in late 2018 or early 2019 and believes it can fund [c6][c7][c11]." — none of c6, c7, c11 states a patient count; c6 says only "We expect to begin a Phase 3 study in NASH in late 2018 or early 2019, subject to regulatory approval." "900-patient" appears only in post-cutoff walkthrough/aftermath data (e1: "the pivotal trial starts: 900 patients..."). Wrong: leaks a later-known fact, attributed to claims that don't contain it. Fix: "...that rate predates the planned Phase 3 trial, whose size and cost management has not yet disclosed [c6][c7][c11]."

- **voice**: "and the biopsies show the disease actually resolving." — c3: "NASH resolution: 27% (p=0.02) MGL-3196 vs 6.5% placebo." Wrong: generalizes a minority-subgroup result (27% of treated patients, vs 6.5% placebo) into "the disease actually resolving," implying a broad or typical outcome. Fix: "and the biopsies show NASH resolving in about a quarter of patients, versus one in fifteen on placebo."

- **voice**: "They just raised close to half a billion." — c8 (June 2018 offering) gives net proceeds of "approximately $282.8 million"; ~$488 million (c4) is the total cash-and-investments balance at 30 Sep 2018, not the amount raised, and the offering closed about five months before the 13 Nov 2018 cutoff. Wrong: conflates a stock-sale amount with a later, larger balance, and misstates the sale as recent. Fix: "They raised about $283 million in a stock sale back in June, and now hold close to half a billion in cash and investments."

- **s3**: "cash and investments of about $488 million after a June stock sale," cited to `["c8","c5"]`. c8 is the June offering (~$282.8M); c5 is "Total revenue was $0," unrelated to cash. The $488.5M figure is claim c4, not cited. Wrong: cited claims don't support the stated figure. Fix: change claim_ids to `["c4","c8"]`.

- **ask_friend[2].a**: "A second programme in an inherited cholesterol disorder has a completed Phase 2 and no Phase 3 plan yet [c19][c20]." — c20, the claim cited, says the company "was evaluating the design and objectives of a possible Phase 3 study ... that could begin in 2019." Wrong: "no Phase 3 plan yet" contradicts the cited claim, which describes an active (if unconfirmed) evaluation. Fix: "...no confirmed Phase 3 start date, though a possible Phase 3 is under design evaluation [c20]."

## Unsupported or unverifiable

- **voice**: "the plenary slot at the big liver meeting says the field is paying attention." No claim measures field attention; c1 only reports the plenary placement itself. Needed: an independent source on field/analyst reaction, not just the fact of placement.
- **s2 / ask_friend[0].a**: "fibrosis improvement" as a plain fact. c16 gives fibrosis resolution in "50% of patients," but only among those who achieved NASH resolution; the overall ≥1-point fibrosis reduction (29% drug vs 23% placebo) carries no stated p-value, unlike the NASH-resolution and NAS figures (both p=0.02). Needed: a significance figure for the overall fibrosis endpoint, or scope the claim to the NASH-resolver subgroup, as ask_friend[0].a does elsewhere.
- **ask_friend[2].a**: "...in a disease where Phase 2 signals have often failed to replicate." No claim_id covers this base rate; evidence.json's exclusions note removed general NASH Phase 2-to-3 failure-history commentary because only post-cutoff sources were found. Needed: a dated, pre-cutoff source on the field's replication track record.

## Editorial preferences (not defects)

- **question**: pairs one positive descriptor ("strong") with two hedges ("small trial," "still pending"); both hedges are accurate (c13, c12), but the asymmetry gives a mild bearish lean. A single balanced clause would read more neutrally.
- **assumption a4**: "Even if the drug works, five years is too long..." — reasonable outcome-agnostic framing, but its two-part structure differs stylistically from a1-a3; no correction needed.
- **ask_friend[0].a**: rounds 36.3% to "36%"; trivial, within source precision.
