# Search-led investigation — proposal for later consideration

Product priority: [MASTER_PLAN.md](MASTER_PLAN.md) governs the game. This search-led investigation is an optional supporting interaction within each campaign scene, not a competing main plan. Any future retrieval must respect the campaign clock and fixed historical boundary.

Status: idea recorded on 9 September 2026. Not approved for implementation. The user is currently working on other UX proposals; this document should not redirect that work.

## Concept

Hide complex financial and sector data from the default view. Start with a role-play scene, a historical chart, and an in-app search box. The player can “Google” questions inside a bounded historical evidence collection before choosing Buy / Skip / Short.

Choosing what to investigate becomes part of the game. The player assembles an argument rather than following a prescribed dossier from top to bottom.

Proposed opening flow:

1. Friend's message or another case-specific scene.
2. Historical chart ending at the decision cutoff, with the date and holding horizon clearly visible.
3. Search box: “What do you want to find out?”
4. Search results and a small personal notes area.
5. Buy / Skip / Short, followed by the existing outcome reveal.

## First prototype: no live LLM required

Try one case before changing all ten. Nektar is a candidate because its partnership, clinical evidence, financing and valuation invite different questions.

Turn existing verified evidence into roughly 10–15 short searchable documents per case. This is a starting estimate, not a quota: do not invent material to fill the collection. Documents might cover earnings, trial results, partnership terms, valuation, financing and risks.

Use local text search over titles, text, tags and authored synonyms. Return documents rather than generated answers. Each result should include:

- A headline or clearly labeled editorial title.
- Publication/availability date and source type.
- A short relevant snippet.
- An expandable supporting excerpt, with any editorial explanation kept distinct.
- Source and claim identifiers for traceability.

Example player queries:

- “Why did big pharma invest?”
- “How many patients?”
- “Cash runway”
- “Is it expensive?”

These should lead to different evidence, not all return the same general briefing. Natural synonyms and informal wording should work. Any derived financial calculation must retain its formula, dated inputs and caveats.

## Interaction ideas

**Optional starting help.** Show broad suggestions such as Business, Financial health and Recent news when the search box is empty. Put more pointed case-specific questions behind a hint so the interface does not prescribe the investigation.

**Pin discoveries.** Let players pin a sentence or number to “My notes.” On commitment, they can select which discovery mattered most instead of writing a required essay. Preserve source links with pinned facts.

**Honest missing coverage.** Say “This historical packet doesn't cover that question” when retrieval fails. Do not imply that no information existed historically, and do not generate an answer to fill a gap.

**Revisit the investigation.** In the reveal, connect the player's selected evidence to subsequent developments. Offer relevant evidence they did not open without claiming it would have guaranteed a correct trade. Searching or opening a document is not proof that the player understood or believed it.

**Keep research optional.** Do not impose search budgets, mandatory document counts or artificial penalties in the first prototype. A player can decide immediately or investigate deeply.

## Historical and factual boundaries

- Only information publicly available at or before the decision cutoff belongs in search results, snippets, suggestions or pre-decision payloads.
- Keep future documents, aftermath narratives and outcome-based interpretation in the separate outcome bundle. Filtering them visually is insufficient.
- Distinguish original quotations, paraphrases, editorial explanations and fictional role-play framing.
- Preserve the existing masked/transparent mode policy. In masked mode, use consistent role labels such as “the company” and “the partner” so redaction does not make evidence ambiguous. Label edited headlines as edited rather than presenting them as verbatim originals.
- This is a curated historical collection, not the whole web. Make its coverage limit clear.
- Retain access to the deeper evidence; this proposal changes how players discover it, not whether contrary information is available.

## Possible later LLM/RAG layer

If local search struggles with real player questions, consider semantic retrieval or an LLM that interprets questions and synthesizes short answers from retrieved case documents. Add this only after observing a concrete need.

Any generated answer must cite supporting evidence, distinguish inference from reported fact, and abstain when the packet lacks support. Model memory and live web search must not supply future knowledge to a historical decision. Test retrieval quality and cutoff leakage before enabling generated answers.

An LLM could help author or tag documents offline first, with editorial verification, without adding a runtime model dependency.

## How to evaluate the prototype

Ask the user to play one case using their own natural questions. Check:

- Do their questions retrieve useful, relevant evidence despite informal wording?
- Can they understand source snippets without opening the full dossier?
- Can they find both supporting and contrary evidence?
- Do they feel they investigated a decision, rather than guessed what the search engine expects?
- Can they explain which discovery influenced their action?
- Are missing coverage and historical availability represented honestly?

If this works, expand to the remaining cases. Do not begin by building a general RAG platform, chat character engine, new research pipeline or live financial-data integration.
