/* Detect outcome fields or copied outcome sentences in public, pre-decision JSON.
   This catches accidental copying, not paraphrases or every possible factual spoiler. */
const OUTCOME_KEYS = new Set(['dated_debrief', 'scene_check', 'aftermath', 'thesis_check',
  'debrief_check', 'walkthrough', 'alternative_horizons', 'extended_path', 'extended_spy_path',
  'sim', 'editor_screen', 'session_returns_vs_entry_open', 'price_return_open_to_open',
  'long_total_return_after_costs', 'short_total_return_after_costs', 'borrow_fee_per_share', 'spy_open_to_open_return']);
const normalize = s => s.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
function strings(value, path = '$', result = []) {
  if (typeof value === 'string') result.push({ path, text: value });
  else if (value && typeof value === 'object') for (const [key, child] of Object.entries(value)) strings(child, `${path}.${key}`, result);
  return result;
}
function outcomePassages(outcome) {
  const texts = [];
  const scene = outcome.scene_check || {};
  // Exclude baseline/assumption/scene text, which can legitimately repeat starting evidence.
  for (const u of scene.dated_debrief?.updates || []) texts.push(u.narrative, ...Object.values(u.checks || {}));
  texts.push(...Object.values(scene.thesis_check || {}), ...Object.values(scene.debrief_check || {}));
  for (const w of scene.walkthrough || []) texts.push(w.stage_text);
  for (const e of outcome.aftermath?.events || []) texts.push(e.headline, e.detail);
  const passages = new Set();
  for (const text of texts.filter(t => typeof t === 'string')) {
    for (const sentence of [text, ...text.split(/(?<=[.!?])\s+/)]) {
      const n = normalize(sentence);
      if (n.length >= 70 && n.split(' ').length >= 12) passages.add(n);
    }
  }
  return [...passages];
}
function inspectPayload(payload, passages) {
  const problems = [];
  function keys(value, path = '$') {
    if (!value || typeof value !== 'object') return;
    for (const [key, child] of Object.entries(value)) {
      if (OUTCOME_KEYS.has(key)) problems.push(`${path}.${key}: outcome-only field`);
      keys(child, `${path}.${key}`);
    }
  }
  keys(payload);
  for (const { path, text } of strings(payload)) {
    const n = normalize(text);
    const match = passages.find(p => n.includes(p));
    if (match) problems.push(`${path}: copied outcome passage (${match.slice(0, 90)}…)`);
  }
  return problems;
}
module.exports = { outcomePassages, inspectPayload };
