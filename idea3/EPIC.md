# Epic 3: the case as a quest

Drafted 10 September 2026 from the user's direction: present each case the way a text quest does (Space Rangers style). A picture, a short description of where you are, and a choice of what to do next: go to the PC and check the price history, call the friend back, read the press release, look at the cash. One thing at a time, until the player decides. This is the presentation answer to "the interface is cryptic". [MASTER_PLAN.md](../MASTER_PLAN.md) owns scope; [idea2/EPIC.md](../idea2/EPIC.md) shares the content layer; [idea1/EPIC.md](../idea1/EPIC.md) can run on top of this presentation later.

## 1. The player's experience

**Morning of 15 February 2018.** A picture: a kitchen table, a phone, a laptop. Text: your friend has messaged you about a biotech stock, a big pharma is putting a billion dollars in. What do you do?

- Read the message again
- Ask your friend what the partner actually bought
- Open the laptop and look at the price chart
- Look up what the company earns
- Check what the trial actually showed
- Decide now

Each choice opens one short screen: the answer, in plain words, with its date and source, and a new set of choices that fit where you are. From the chart you can "look at the last twelve months" or "compare with the market". From the trial screen you can "how many patients?" or "who ran it?". "Decide now" is always available. Nothing is forced; a player who wants only the pitch and the chart can decide in two clicks.

The decision screen asks in plain words: buy it, do nothing, or bet against it; for how long; with how much of your $100,000; and which belief the choice rests on. Then the walk and the debrief as today, in the same one-screen voice.

## 2. What it is technically

A **quest graph** per case: nodes and choices. Node content is the answer units from EPIC_2 section 3 (`cases/<id>/units.json`), so a quest does not author facts; it authors the path through them.

```json
{"start": "n_kitchen",
 "nodes": {
   "n_kitchen": {"scene": "kitchen_phone", "text": "…", "choices": [{"label": "Ask your friend what the partner actually bought", "to": "n_ask_partner"}, {"label": "Open the laptop", "to": "n_laptop"}, {"label": "Decide now", "to": "decide"}]},
   "n_ask_partner": {"unit": "u03", "choices": [{"label": "How many patients?", "to": "n_patients"}, {"label": "Back to the kitchen", "to": "n_kitchen"}]},
   "n_laptop": {"widget": "chart", "choices": [{"label": "Compare with the market", "to": "n_chart_spy"}, {"label": "Look up what the company earns", "to": "n_money"}]}
 }}
```

Rules: a node shows one unit or one widget (chart, valuation panel, headline list); at most six choices; "Decide now" reachable from every node; every unit in the case reachable from the start within four choices; text at most 120 words per node; no node reveals anything dated after the cutoff (build check). Visited nodes are recorded in the journal, so the debrief can say what the player looked at.

**Pictures.** Scenes, not companies: a kitchen, a commute, an office, a trading screen, a hospital corridor for clinical cases. A small fixed set, reused across cases, drawn or generated once and labelled fiction. Never a logo, product, building or person that could identify the issuer, because masking is the game. First version can ship with no pictures and a scene line instead; pictures are polish.

**Difficulty, later.** The quest form allows a morning budget ("you have time for five things before the market opens") or a cost per action. Not in the first version; RAG.md's rule against artificial penalties stands until a playtest asks for it.

## 3. Stories and acceptance criteria

**S1 Quest schema and validator.** `cases/<id>/quest.json`, validated in the build: every `to` exists, every unit exists and predates the cutoff, "decide" reachable from every node, every unit reachable within four choices, choice and text limits. Added to `scripts/run_checks.sh`.

**S2 Quest renderer.** One-column page (`site/quest.html`): scene picture or line, node text, choices as large buttons, a back choice, a persistent one-line status (date, "you have not decided yet"), and the plain-language decision screen. Works at 390px. Keyboard reachable.

**S3 Answer units for Nektar** (shared with EPIC_2 S1) and **the Nektar quest graph**: a path that lets a curious player reach the partner terms, the trial evidence, the money and the price in under ten clicks, and an impatient player decide in two.

**S4 Plain-language decision screen and onboarding.** Applies to the existing case page as well, whether or not the quest ships: a three-line "you are here, decide this, then find out" opener; "Buy it / Do nothing / Bet against it" with a one-line explanation of betting against; "How long would you hold?"; "How much of your $100,000?"; "Which belief does your choice rest on?"; "Lock in my decision". Citation tags hidden in prose by default with a toggle.

**S5 Debrief in the same voice.** One sentence first ("You lost 5.8% over three years; the market gained 37.6%"), then the tiles; the thesis check names what the player looked at and did not look at, from the visited nodes.

**S6 Playtest on Nektar** with the friend who said "cryptic": can they describe what the game asked of them; did they find the trial size and the money without help; did the decision screen need explanation; second word of feedback recorded.

**S7 Ten quest graphs**, one Sonnet writer per case from the same units, validated, then a second playtest.

## 4. Decisions to settle

1. Does the quest replace the case page or sit beside it as a mode? Recommendation: a mode at first, selected on the front page, so the two can be compared with real players.
2. Pictures now or later, and their source (drawn set, generated set, none).
3. Whether visited nodes affect the debrief text beyond listing them.
4. Whether the walk after commit also becomes quest screens (one stop, one choice: strengthens, weakens, unresolved) or stays as is. Recommendation: same renderer, since the stops are already one-at-a-time.

## 5. Dependencies and order

- Needs the answer units (shared with EPIC_2). Authoring them for Nektar is the first task of whichever epic starts.
- Does not need EPIC_1. When the campaign comes, the portfolio strip becomes the status line and "advance time" becomes a choice.
- Recommended first among the three: it has no runtime dependency, it is the direct response to the only feedback received, and its units and playtest feed EPIC_2.

## 6. Definition of done

A first-time player opens Nektar, understands within one screen what is being asked, reaches the three facts that matter through choices they chose, decides in plain words, and reads a one-sentence result before any tile. The full packet remains reachable through choices. Build checks prove no post-cutoff text is in any node.
