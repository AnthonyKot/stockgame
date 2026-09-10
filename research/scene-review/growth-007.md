# Scene review: growth-007 (First Solar, cutoff 2022-03-02)

## Confirmed defects

- **ask_friend[2].a** ("What is the stock already pricing?"): "The last close is $75.62, down 38% from the 12-month high and down 27% over three months. Market capitalisation is about $8.0 billion, or $6.5 billion after $1.6 billion of net cash, which is roughly 2.2 times 2021 revenue [c2]." — c2's excerpt is only "Full-year 2021 net sales were $2,923.4 million, up 7.8% from $2,711.3 million in 2020"; nothing about price, 12-month high, or market cap. `player.json.missing_data` explicitly states "Historical share price, market capitalization and enterprise value are not available in this evidence packet." What's wrong: fabricates unsourced price/market-cap figures and cites a revenue claim as if it covers them. Minimal fix: drop the price/cap sentences; keep only "Market data is not available in this record; net cash was $1,579.3 million and FY2021 net sales were $2,923.4 million [c2]."

- **ask_friend[1].a** ("Is demand the problem?"): "...which is more than two years of the guided 2022 shipments [c7]." — 17.5 GW-DC of bookings against c6's guided 2022 shipments of "8.9GW to 9.4GW" is about 1.9 years, not more than two (even the low end, 8.9×2=17.8, exceeds 17.5). What's wrong: overstates the multiple. Fix: "...which is close to two years of the guided 2022 shipments."

- **ask_friend[1].a**: "India has just imposed 40% module tariffs [c12]." — c12: "India introduced import tariffs of 40% on solar modules and 25% on solar cells effective April 2022." At the 2022-03-02 cutoff the tariff had been announced but was not yet in effect. What's wrong: states a not-yet-effective tariff as already imposed (point-in-time error). Fix: "India has announced 40% module tariffs taking effect in April 2022 [c12]."

- **ask_friend[0].a** ("Why is next year's profit guided so low?"): "The company's own explanation inside the release: $10 to 15 million of underutilisation losses tied to the capacity transition, freight and input costs, and a smaller sales volume while new plants are built [c6]." — c6's excerpt states only the guidance figures, including "$10-15 million of underutilization losses"; it contains no mention of freight, input costs, or reduced sales volume as stated reasons, and no other claim covers them. What's wrong: attributes a causal explanation to "the release" that the cited evidence doesn't contain (motive/causation not supported). Fix: "The company's own explanation inside the release: $10-15 million of underutilisation losses tied to the capacity transition [c6]."

- **assumption a5**: "Module pricing is under structural pressure and the cut will not be the last." — Compound: bundles a claim about pricing structure with a separate prediction about future guidance actions; a later event could support one half and weaken the other independently. Fix: split into "Module pricing is under structural pressure" and, separately, "The 2022 guidance cut will not be the last one."

## Unsupported or unverifiable

- **s2** / **ask_friend[1].a**: "about double 2021" / "roughly double 2021" (2022 capex of $850M-$1.1B vs. 2021). Cited to c6 and c10, but c6 only states the 2022 guided figure and c10 only describes the two new facilities — neither gives the FY2021 comparison base. That figure (actual 2021 capex of $540.3 million) is claim c14, which isn't cited here. Needed: cite c14 alongside c6.
- **assumption a4**: "After a 38% fall the price already reflects the guidance cut." Rests on the same unsourced 38%-fall figure flagged above; no claim in evidence.json or player.json supplies any share-price data. Needed: a cited price-history claim, which does not exist in this packet.
- **question**: "a 90% guided profit drop" carries no claim_id. Midpoint-to-midpoint math (c4/c6) gives roughly 93%; low-end gives 100%; high-end gives roughly 86%. "90%" sits inside that range but matches no specific cited figure. Needed: cite c4 and c6, or align with the packet's own "roughly 93%" (used in `help_me_weigh`).

## Editorial preferences (not defects)

- **s3**: "a guided $1.1 to 1.35 billion year-end net cash" doesn't state which year-end; "guided" implies forward (2022) rather than the 2021 bookings figure in the same sentence, but spelling out "2022 year-end" would remove any ambiguity.
- **ask_friend[1].a** packs bookings-to-shipments math, the capex step-up, the US sales share, and the India tariff into one dense paragraph; splitting would make each claim easier to check independently.
- The "90%" figure in `question` is a reasonable rounding for a headline but sits below the packet's own "roughly 93%" framing elsewhere; consistency across the case would help.
