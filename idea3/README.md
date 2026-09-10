# Idea 3: the case as a quest

Product-owner assessment, 10 September 2026. Scenario and stories in [EPIC.md](EPIC.md). Comparison: [IDEAS.md](../IDEAS.md).

## 1. In one paragraph

A case plays like a text quest. A picture and three lines set the scene: a morning in February 2018, a message from a friend about a biotech. Then choices: ask the friend what the partner bought, open the laptop and look at the chart, check what the trial showed, look at the money, or decide now. Each choice shows one screen with one fact, dated and sourced, and new choices that fit where you are. Decide in plain words whenever you like. The walk and the debrief come in the same one-screen voice, and the debrief knows what you looked at.

## 2. How it is built on today's code

Reused unchanged: scenes, evidence, aftermath, the dated debrief, the chart widget, the valuation panel, the simulator, the builder's masking, the payload checker, the CI gate.

Shared with idea 2: the answer units in `cases/<id>/units.json` and their validator. A quest does not author facts; it authors the path through them.

New: `cases/<id>/quest.json` (nodes, choices, scene ids), a graph validator in the build (every target exists, every unit predates the cutoff, "decide" reachable from every node, every unit reachable within four choices, text and choice limits), `site/quest.html` (one column, picture or scene line, node text, big choice buttons, back, a one-line status, the plain-language decision screen), journal fields for visited nodes, and a front-page mode switch so the quest and the current page coexist for comparison. Pictures: a small fixed set of scenes (kitchen, commute, office, trading screen, hospital corridor), reused across cases, never anything that identifies an issuer; the first version ships without them.

The plain-language decision screen and the three-line opener also apply to the existing page whether or not the quest ships.

## 3. Effort

| Milestone | Sessions | Who |
|---|---|---|
| Units for Nektar plus validator (shared with idea 2) | 1 | schema by the main session, units by a Sonnet writer |
| Quest schema, validator, renderer, decision screen | 1 | Claude |
| Nektar quest graph, playtest with the "cryptic" friend | 0.5 plus the user's time | pause |
| Nine more graphs from their units, reviewed | 1 | nine Sonnet writers, one reviewer pass |
| Pictures | 0.5, later | needs an art source decision |

About three and a half sessions to ten playable quests without pictures. The smallest of the three ideas.

## 4. Pros and cons

Pros
- No runtime dependency; static site as today.
- Phone-native: one column, big buttons, no typing.
- The format forces plain language and one idea per screen, which is the direct fix for "cryptic".
- Visited nodes give the debrief something specific to say: "you never looked at the trial size".
- Its units and its playtest feed idea 2; nothing is thrown away if search comes later.
- Cheap to compare against the current page behind a mode switch.

Cons
- Less freedom than a search box; the player can only ask what the graph offers.
- Can feel railroaded or childish to a finance-literate player.
- Path authoring needs taste: which fact comes first, what a curious player finds in four clicks, what an impatient one misses.
- Pictures need a source and carry masking risk; without them the first version is a menu, not a scene.
- More authoring per case than the search idea: a graph as well as units.

## 5. Chance it works

- **Built correctly: 90%.** A JSON graph, a validator and a renderer over content that exists.
- **Preferred to today's page: 70% among newcomers, lower among experienced investors**, who may want the dossier. The mode switch keeps both.

Evidence that moves it: one session with the friend who said "cryptic". If they can say what the game asked of them after the first screen, the idea has done its job.

## 6. Risks and unknowns

- Railroading: mitigate with "decide now" everywhere and a "look at everything" node that opens the full packet.
- Tone: scene text must stay adult; the fiction label from the current scene card carries over.
- Picture source: drawn set, generated set, or none; decide before any picture ships, and never a logo or product.
- Walk after commit: same renderer or the current one; recommendation is the same renderer.

## 7. First milestone and its playtest

Nektar as a quest without pictures, reachable from the front page as a mode. The friend who said "cryptic" plays it, then answers: what did the game ask you to do, and what did you find out before deciding?

## 8. Kill criteria

Stop if that friend still cannot describe the task after one screen, or clicks to "decide now" without opening a single fact and says the choices did not interest them. Reshape rather than stop if experienced players want the dossier: that is what the mode switch is for.
