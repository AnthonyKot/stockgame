# Scene review: commercial-gilead-2019 (Gilead Sciences, cutoff 2019-02-05)

## Confirmed defects

- **ask_friend[2].a** ("Is it cheap enough to be a trap?"): "The last close is $70.05, down 14% over twelve months and 15% below the 12-month high. Market capitalisation is about $91 billion... net cash is about $4 billion and enterprise value about $86 billion, roughly 3.3 times 2017 revenue [g6]." — g6's excerpt covers only cash/investments ($31.5B), OCF, debt repaid, dividends and buybacks — no price, range, market cap, net cash or EV. `player.json`'s own headline metric here is `"value": null, "status": "missing", "definition": "requires historical share price / market capitalization, which is not in this evidence packet"`, and `missing_data` repeats that no historical share price exists in the packet. What's wrong: a full valuation stack is invented and attached to a claim that doesn't cover it. Fix: drop the price/cap/EV sentences; keep "With $31.5 billion of cash and investments at year-end 2018, against undisclosed period-end debt [g6]."

- **ask_friend[2].a**: "Operating cash flow was $8.4 billion after $3.0 billion of dividends and $2.9 billion of buybacks." — g6 lists OCF ($8.4B), debt repaid ($6.3B), dividends ($3.0B) and buybacks ($2.9B) as four separate items, not a sequence where OCF is net of the other two; $3.0B+$2.9B+$6.3B alone exceeds $8.4B. What's wrong: "after" implies OCF nets out shareholder returns and silently drops the debt repayment, overstating residual cash generation. Fix: "The company generated $8.4 billion of operating cash flow during 2018 and also paid $3.0 billion of dividends, spent $2.9 billion on buybacks and repaid $6.3 billion of debt [g6]."

- **ask_friend[0].a** ("How fast is the old business shrinking?"): "...guidance... explicitly assumes US generic competition for two older products [g7][g14]." — g7 (evidence.json's own text: "two of its non-antiviral products") is the guidance-embedded assumption; g14 is a separate forward-looking risk line naming two different, antiviral HIV products, unconnected to the guidance figures. What's wrong: conflates two unrelated product pairs from two different disclosures into one "two older products." Fix: "...guidance explicitly assumes US generic competition for two of its non-antiviral products [g7]; separately, the company flags future generic risk to two older HIV antivirals [g14]."

- **ask_friend[1].a** ("What is growing?"): "...two-year follow-up data and an early study in a second leukaemia population [g10][g11]." — g11 is two-year follow-up in "refractory large B-cell lymphoma" (a lymphoma); g10, the only leukaemia population cited, is the early ALL study. What's wrong: mislabels the approved product's lymphoma population as a second leukaemia population, conflating disease types. Fix: "...two-year follow-up data in its approved lymphoma indication and an early study in a leukaemia population [g10][g11]."

- **ask_friend[1].a**: "Three early immuno-oncology collaborations were signed in the quarter [g9]." — g9 lists one "immuno-oncology partnership," one collaboration for "the treatment of fibrotic diseases," and one immuno-oncology deal. Only two of three are immuno-oncology. What's wrong: mischaracterizes all three as immuno-oncology when the cited claim itself distinguishes "immuno-oncology and fibrotic-disease." Fix: "Three early research collaborations were signed in the quarter, two in immuno-oncology and one in fibrotic disease [g9]."

- **assumption a5**: "My friend is right: shrinking revenue and a written-off bet make this a trap." — Already contains its own verdict ("My friend is right... a trap") rather than a single proposition a later event could support or weaken, and bundles two facts as joint justification. Fix: "Shrinking total revenue and the written-off oncology program mean this business is now in structural decline."

- **assumption a3**: "A 3x revenue multiple with $31 billion of cash is already a floor." — Same unsupported multiple flagged above; no claim in evidence.json or player.json (EV/multiple marked "missing") supplies it. Fix: "A large cash balance relative to the business's shrinking size is already a floor on the shares."

## Unsupported or unverifiable

- **question**: "...or a business already priced for decline?" — no claim_id; presupposes the same missing share-price/valuation evidence flagged above. Needed: a cited historical price or valuation claim, absent from this packet.
- **voice**: "they just wrote off an $820 million oncology bet" — g19 gives no month or quarter for the impairment within FY2018, so "just" (implying right before the release) isn't verifiable from the cited claim. Needed: a dated disclosure of when the impairment was recorded.

## Editorial preferences (not defects)

- **ask_friend[0].a**: "a decline management attributes to fewer patients starting treatment and lower prices [g4]" drops "increased competition," one of three factors g4's excerpt lists; incomplete, not wrong.
- **assumption a2**: "The cash pile and new CEO will buy or build a second growth engine." The "buy or build" disjunction packs two resolution paths into one assumption.
