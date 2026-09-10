# Three ideas, one recommendation

Product-owner page, 10 September 2026. Each idea has a folder with a scenario (`EPIC.md`) and an assessment (`README.md`): [idea1](idea1/README.md) the campaign, [idea2](idea2/README.md) investigate by asking, [idea3](idea3/README.md) the case as a quest. [MASTER_PLAN.md](MASTER_PLAN.md) remains the product authority; ideas 2 and 3 change how a scene is played, idea 1 connects the scenes.

## Side by side

| | Idea 1: campaign | Idea 2: ask the packet | Idea 3: quest |
|---|---|---|---|
| Player value | Decisions with consequences, a final report | Investigate in your own words | One screen, one fact, plain choices |
| Answers "cryptic"? | No, inherits today's page | Yes, if questions land | Yes, most directly |
| Effort (prototype estimates; ten reviewed cases roughly double them, review is not parallel) | 8 to 12 sessions, 3 to 4 weeks | Stage A: 1 to 2 sessions for Nektar; Stage B +2 to 3 plus infrastructure | 1.5 to 2 sessions for Nektar; 6 to 8 for ten reviewed quests |
| Runtime dependency | None | None for Stage A; a model and a proxy for Stage B | None |
| New data needed | Bitcoin series, dividend dates, split audit, calendar | None | None (pictures optional) |
| Confidence we can build it (gate: the epic's acceptance criteria pass in `run_checks.sh`) | Medium: engine plan is thorough, data is the risk | High for search; medium for a grounded assistant | High |
| Confidence players prefer it (hypothesis until a playtest; one friend's "cryptic" justifies testing clarity, not a preference) | Low until presentation is fixed | Untested | Untested; most direct test of clarity |
| First playtest | Three stories with overlap | Nektar with search and notes | Nektar as a quest, with the "cryptic" friend |
| Kill criteria | Prototype no more engaging than three standalone cases; ledger needs invented data | Under half of natural questions land; "felt like guessing the engine" | Friend still cannot say what the game asks; clicks through without opening a fact |

## The shared first task, kept small

Ideas 2 and 3 both use **answer units**: one question, one cited answer under 60 words, dated, tagged (`cases/<id>/units.json`, schema in [idea2/EPIC.md](idea2/EPIC.md) section 3). Build only what one Nektar experiment needs, not a framework for ten cases: the validator checks publication dates and source support, nothing more. Units may legitimately recur in a debrief; the boundary is the date, not the text.

## Recommendation

**Branch `idea3` first.** It is the smallest, has no runtime dependency, is the direct answer to the only feedback we have, and everything it produces (units, the plain-language decision screen, the visited-node debrief) is reused by the other two. Its playtest is one evening with one friend.

**Then decide whether `idea2` earns a place.** If the quest makes investigation clear and enjoyable, a search box may add little and idea 1, the intended product, comes next. Idea 2 proceeds only if the quest playtest shows players wanting to ask things the graph does not offer. Stage B waits for evidence from Stage A.

**Then `idea1`** on top of whichever presentation the playtests prefer. Its seven open decisions can be settled in the meantime, and the Bitcoin and dividend data fetched, so that the engine work starts with nothing missing.

## Branch plan

- `main` stays deployable; the CI gate runs the twelve suites on every push to it.
- The content layer (`units.json`, validator, builder emission) is developed on `idea3` and merged to `main` as soon as Nektar's units pass, so `idea2` branches from it.
- Each idea lives on its own branch and merges behind a front-page mode switch, never replacing the current page until a playtest says so.
- Engine and scripts are Codex's lane; content, screens and copy are Claude's; both run `scripts/run_checks.sh` before pushing.

## Next step

One Nektar quest, without pictures, on the existing simulator and assumption-based debrief, compared with the current page including its recent presentation improvements. Agreed by both sessions on 10 September 2026.
