# Idea 2: investigate by asking

Product-owner assessment, 10 September 2026. Scenario and stories in [EPIC.md](EPIC.md); origin in [RAG.md](../RAG.md). Comparison: [IDEAS.md](../IDEAS.md).

## 1. In one paragraph

A case opens with one story and the friend's leads, a chart, and a box that asks "what do you want to find out?". You type in your own words and get an answer from the packet only, dated and sourced, or an honest "this packet doesn't cover that". You pin what matters, and on commit those pins become the beliefs your decision rests on. The full dossier is one click away but never shown by default. Later, if typed questions miss too often, a grounded assistant rewrites the question and answers in a sentence with citations.

## 2. How it is built on today's code

Reused unchanged: scenes, evidence, the chart, the ticket, the walk and the dated debrief, the builder's masking, the payload checker, the CI gate.

New content layer, shared with idea 3: `cases/<id>/units.json`, ten to fifteen answer units per case (one question, one cited answer under 60 words, availability date, tags, synonyms), authored from text that already exists: the three friend answers, the six tiles with their presentation context, what-changed items, catalysts, unresolved questions, the valuation panel.

New code, Stage A: a validator for units in the build (citations resolve, availability dates before the cutoff; a fact may legitimately recur in a debrief, so text overlap is not a failure), a search index per case emitted by the builder, a lexical search with synonym matching in `site/play.html` or a new `site/ask.html`, a notes panel, and journal fields for opened and pinned units. No runtime dependency; deploys on Pages as today.

New code, Stage B: a model behind a small proxy (or a local model) that retrieves units and writes a cited answer or abstains; an evaluation set built from every authored unit plus post-cutoff questions that must be refused. This breaks the pure static site: a key, a proxy, a budget.

## 3. Effort

| Milestone | Sessions | Who |
|---|---|---|
| Units for Nektar plus validator | 1 | main session for the schema, a Sonnet writer for the units |
| Stage A search, notes, commit link, leakage test, on Nektar | 1 | Claude |
| Playtest and decision on Stage B | the user's time | pause |
| Units for the other nine | 1 | nine Sonnet writers, merge script pattern |
| Stage B assistant, proxy, evaluation set | 2 to 3 plus infrastructure | later, only on evidence |

Stage A end to end for ten cases: about three sessions. Stage B roughly doubles it and adds an operating cost.

## 4. Pros and cons

Pros
- Matches how people actually research: ask, read, ask again.
- Hides the number wall without deleting anything; the dossier stays reachable.
- "Not in this packet" is an honest, teachable answer.
- Units are reused by idea 3 as screens and by idea 1 as clock-gated material; authoring is paid once.
- Choosing what to investigate becomes play.

Cons
- Lexical search is literal. "Is it pricey" must map to the valuation unit by an authored synonym or it fails, and every miss feels like the game's fault.
- Typing on a phone is friction; the current buttons are one tap.
- Empty-result moments are dead ends unless the suggestions are good.
- Stage B needs a key and a server piece, and a wrong retrieval can leak or invent; grounding must be tested before it is switched on.
- Stage B can answer questions the packet does not, from model memory, unless refusal is enforced.

## 5. Confidence

Judgments, not measured probabilities.

- **We can build Stage A: high.** Gate: the RAG.md example queries return distinct units and the leakage test passes. It is a small index over content we have.
- **We can build Stage B well: medium.** Gate: the evaluation set passes with zero post-cutoff leakage. Refusal quality is the risk, not fluency.
- **Players prefer it: untested.** Players who like to ask may love it; players who want to be told what matters may bounce off an empty box. The friend's leads are the hedge. Idea 2 only earns its place if the quest playtest shows players wanting to ask what the graph does not offer.

Evidence that moves it: the Nektar playtest with the RAG.md questions, especially "did it feel like investigating or like guessing what the search wants?".

## 6. Risks and unknowns

- Synonym coverage: author from real player questions after the first playtest, not from guesses.
- Assumption ids: pinned facts replacing the fixed list changes what the dated verdicts key on; decide in the epic's open item 2 before Stage A ships.
- Stage B runtime and cost: who pays, where the key lives, what happens when it is down (fall back to Stage A).
- Masking: units must use consistent role labels or a search hit can unmask by inconsistency.

## 7. First milestone and its playtest

Nektar with Stage A search, the friend's leads, notes and pinning. Ask the player to use their own words for four questions, then: which discovery decided it, and did anything they wanted go unanswered?

## 8. Kill criteria

Stop or move to Stage B if fewer than half of a player's natural questions reach a useful unit, or if the player says the box felt like guessing the engine. Stop Stage B if the evaluation set shows any post-cutoff leakage that cannot be closed by retrieval rules.
