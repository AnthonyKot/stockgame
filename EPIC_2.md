# Epic 2: investigate by asking, not by reading a dossier

Drafted 10 September 2026 from [RAG.md](RAG.md) and the user's direction: the current case page overloads a player with numbers and terms. Replace the wall of cards with one story, the friend's leads, and a way to ask questions that are answered only from the packet. [MASTER_PLAN.md](MASTER_PLAN.md) still owns product scope; this epic changes how a player discovers evidence inside a scene, not what the game is. [EPIC_1.md](EPIC_1.md) (campaign) and [EPIC_3.md](EPIC_3.md) (quest presentation) share the content layer defined in section 3.

## 1. The player's view

A case opens on one screen, not eight cards:

1. **The story.** The dated morning, the friend's message or the headline, in the current voice. Three or four sentences.
2. **The friend's leads.** The claims inside the pitch, listed as leads to check: "a major pharma is putting in $1 billion", "38 patients in an uncontrolled study". Each lead is a click that answers itself from the packet.
3. **The chart** to the cutoff, with the date and the horizon visible.
4. **The question box.** "What do you want to find out?" A player types in their own words. The answer comes from the packet only, with its date and source, or the honest reply "this packet doesn't cover that".
5. **My notes.** Anything the player pins from an answer. On commit, the pinned facts are offered as the beliefs the decision rests on, replacing the fixed assumption list where the player has pinned something.
6. **The decision**, in plain words (the ticket wording from EPIC_3 section 4 applies here too).

The full packet stays one click away under "everything in the file", for players who want to read it all. Nothing is removed from the game; the default view stops showing it.

## 2. Two stages, the second only if needed

**Stage A, local search, no model at runtime.** Each case carries a small collection of answer units (section 3). The question box does lexical search over titles, text, tags and authored synonyms, and returns the best two or three units as answers. This is RAG.md's first prototype and needs no network call, so it deploys on GitHub Pages as today.

**Stage B, a grounded assistant.** If playtests show that real questions miss the units too often, add a model that rewrites the question, retrieves units, and synthesises a short answer that cites them, abstains when nothing supports it, and never uses its own memory. The runtime dependency is real (a key, a proxy or a local model) and is the reason B waits for evidence from A. An offline model may help author and tag units at any time, with editorial review.

The bot never sees post-cutoff material. The retrieval index is built per case from pre-decision files only, and the payload checker runs on it.

## 3. The content layer, shared by all three epics

An **answer unit** is the smallest thing a player can find: one titled fact or explanation, dated, cited, in plain language.

```json
{"id": "u07", "title": "How many patients were in the trial?", "answer": "38 patients, in an open-label study with no control arm; response rates were 14% to 75% across small cohorts [c3][c4].",
 "kind": "reported | derived | editorial", "available_at": "2017-11-11", "source_ids": ["nktr-asco-2017"], "claim_ids": ["c3", "c4"],
 "tags": ["trial", "patients", "evidence"], "synonyms": ["how big was the study", "sample size", "how many people"], "section": "clinical"}
```

Rules: one question per unit; answer at most 60 words; every clause cited to an evidence claim; derived numbers keep their formula and dated inputs; editorial explanation labelled; masked-mode role labels ("the partner") used consistently. Ten to fifteen units per case, starting from what already exists: the three friend answers, the six headline tiles with their presentation context, what-changed items, catalysts, unresolved questions and the valuation panel are units already, in different shapes.

The same units are the nodes EPIC_3 shows one at a time, and the dated material EPIC_1's clock gates. Author them once, in `cases/<id>/units.json`, validated by the builder.

## 4. Stories and acceptance criteria

**S1 Answer units for one case (Nektar).** 10 to 15 units written from the existing packet, no new research; a validator checks citations, word limits, dates before the cutoff, and that no unit text appears in any outcome file.

**S2 Search page for one case.** The six-part view above; lexical search with synonyms; results show title, date, source type, snippet, expandable excerpt, claim ids; empty box shows three broad suggestions (business, money, recent news) and hides case-specific hints behind "need a hint?".
- The four example queries in RAG.md return different units.
- A question the packet cannot answer gets the honest reply, not the nearest unit.
- Informal wording ("is it pricey", "how much cash") hits the right unit.

**S3 Notes and commitment.** Pin any answer to notes; pinned facts keep their citations; the ticket offers pinned facts as the beliefs the call rests on; the journal stores which units were opened and pinned.

**S4 Debrief revisit.** After the reveal, the debrief connects the pinned facts to what followed and lists relevant units the player never opened, without claiming they would have changed the result. Reuses the dated verdict mechanism.

**S5 Leakage and boundary tests.** The unit index for a case contains only units with `available_at` before the cutoff; the payload checker covers `units.json` and the built index; a unit citing a later-published source is rejected at build.

**S6 Playtest on Nektar** against RAG.md's six questions: useful retrieval from informal wording, snippets understood without the dossier, both sides findable, felt like investigating, can name the discovery that mattered, gaps stated honestly. Decision point for Stage B and for the other nine cases.

**S7 Stage B, grounded assistant** (only after S6 says search is not enough). Answers cite units, abstain on no support, and pass an evaluation set built from every authored unit (question in, expected unit ids out) plus a leakage set of post-cutoff questions that must be refused. Runtime choice documented; falls back to Stage A when unavailable.

**S8 Rollout to ten cases**, with the unit validator in `scripts/run_checks.sh`.

## 5. Decisions to settle

1. Whether the friend's leads replace or sit beside the three authored friend questions.
2. Whether pinned facts replace the fixed assumption list or add to it (affects the dated verdicts, which are keyed to assumption ids).
3. Stage B runtime, if it comes: hosted API through a small proxy, or a local model; who pays; how a key stays out of a static site.
4. Whether search is optional (RAG.md's position) or the only route to the packet in the default view.

## 6. Dependencies and order

- Depends on nothing in EPIC_1. Works on the standalone cases first.
- Shares the content layer with EPIC_3; whichever epic starts first authors `units.json`.
- Recommended order across the three epics: EPIC_3 first (cheapest, no runtime dependency, answers "cryptic" directly and produces the units), then EPIC_2 Stage A over the same units, then EPIC_1 on top of whichever presentation the playtests prefer.

## 7. Definition of done

A first-time player can open a case, ask three questions in their own words, get packet-only answers with dates and sources, pin one, decide, and see the debrief tie that pin to what happened, without reading a card they did not ask for. The full packet remains reachable. No post-cutoff text can be retrieved, by test.
