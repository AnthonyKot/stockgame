// Precompute the exit-scoped debrief for a case at given exit dates, so the campaign page never fetches a whole
// outcome file. Usage: node scripts/slice_debrief.js <opaque_id> <exit_date> [<exit_date> ...]  -> JSON on stdout:
// { "<exit_date>": { exit, reveal: {issuer, ticker}, narrative, checks: {aid: text}, assumptions, events: [...] } }
// Uses site/story.js (the same selector the standalone debrief uses), so nothing after the exit's own availability rule leaks.
const fs = require('node:fs');
const path = require('node:path');
const STORY = require('../site/story.js');
const [oid, ...exits] = process.argv.slice(2);
const dir = path.join(__dirname, '..', 'site', 'data', oid);
const outcome = JSON.parse(fs.readFileSync(path.join(dir, 'outcome.json')));
const reveal = JSON.parse(fs.readFileSync(path.join(dir, 'reveal.json')));
const out = {};
for (const exit of exits) {
  const d = STORY.atExit(outcome, exit);
  const events = (d ? d.events : []).map(e => ({ id: e.id, date: e.date, kind: e.kind, headline: e.headline, source: e.source ? { title: e.source.title, url: e.source.url, publisher: e.source.publisher, published: e.source.published } : null }));
  out[exit] = { exit, reveal: { issuer: reveal.transparent.issuer, ticker: reveal.transparent.ticker, exchange: reveal.transparent.exchange || null },
    narrative: d ? d.narrative.text : null, checks: d ? Object.fromEntries(Object.entries(d.checks).map(([k, v]) => [k, v.text])) : {},
    assumptions: (outcome.scene_check && outcome.scene_check.assumptions || []).map(a => ({ id: a.id, text: a.text })), events,
    note: 'Written from what was public by the exit date; later developments are not in this file.' };
}
process.stdout.write(JSON.stringify(out));
