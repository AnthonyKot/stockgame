// Structural check of exit-scoped feedback for every built case: baseline covers all assumptions, every update's
// events exist, and each of 1/3/5-year holds (where available) sees feedback that differs from the baseline when
// any event was public by then. Run after build_bundles.py: node scripts/test_dated_debrief.js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const STORY = require('../site/story.js');
const SIM = require('../site/sim.js');
const idx = JSON.parse(fs.readFileSync('site/data/index.json'));
const cases = Array.isArray(idx) ? idx : idx.cases;
let n = 0;
for (const c of cases) {
  const o = JSON.parse(fs.readFileSync(`site/data/${c.id}/outcome.json`));
  const sheet = JSON.parse(fs.readFileSync(`site/data/${c.id}/sheet.json`));
  assert(!JSON.stringify(sheet).includes('dated_debrief'), `${c.id}: dated_debrief leaked into sheet.json`);
  const dd = o.scene_check && o.scene_check.dated_debrief;
  assert(dd, `${c.id}: no dated_debrief`);
  const aids = o.scene_check.assumptions.map(a => a.id);
  for (const aid of aids) assert(typeof dd.baseline.checks[aid] === 'string', `${c.id}: baseline lacks ${aid}`);
  for (const u of dd.updates) for (const id of u.event_ids) assert(o.aftermath.events.some(e => e.id === id), `${c.id}: unknown event ${id}`);
  for (const years of Object.keys(o.sim.horizons)) {
    const r = SIM.simulate(o.sim, { action: 'buy', size: 10, years: Number(years) });
    if (r.status !== 'ok') continue;
    const d = STORY.atExit(o, r.exit.date);
    assert(d, `${c.id}: atExit returned null for ${years}y`);
    const eligible = dd.updates.filter(u => u.event_ids.every(id => d.events.some(e => e.id === id)));
    const changed = aids.some(aid => d.checks[aid].text !== dd.baseline.checks[aid]);
    if (d.events.length) assert(eligible.length > 0 && changed, `${c.id}: ${years}y exit ${r.exit.date} has ${d.events.length} public events but no applicable update`);
    n++;
  }
}
console.log(`dated debrief: ${cases.length} cases, ${n} horizon exits checked`);
