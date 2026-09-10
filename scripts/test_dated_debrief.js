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

/* 2. Check status vocabulary, not monotonic confidence. Evidence may reopen uncertainty. */
const STATUS = /^(Supported|Partly supported|Mixed|Weakened|Not supported|Unresolved|Choosing)/;
const lastDay = d => /^\d{4}-\d{2}$/.test(d) ? new Date(Date.UTC(+d.slice(0, 4), +d.slice(5, 7), 0)).toISOString().slice(0, 10) : d;
const nextDay = d => new Date(Date.parse(d + 'T00:00:00Z') + 864e5).toISOString().slice(0, 10);
let drift = 0, boundaries = 0;
const byCase = {};
for (const c of cases) {
  const o = JSON.parse(fs.readFileSync(`site/data/${c.id}/outcome.json`)); byCase[c.id] = o;
  const dd = o.scene_check.dated_debrief; const ev = Object.fromEntries(o.aftermath.events.map(e => [e.id, e]));
  const unlock = u => u.event_ids.map(id => [lastDay(ev[id].date), lastDay(ev[id].source.published)].sort().pop()).sort().pop();
  const seq = {};
  for (const u of [...dd.updates].sort((a, b) => unlock(a).localeCompare(unlock(b)))) {
    for (const [aid, t] of Object.entries(u.checks || {})) { const m = t.match(STATUS); assert(m, `${c.id}: check for ${aid} lacks a status word`); (seq[aid] ||= []).push(m[1]); }
  }
  for (const [aid, l] of Object.entries(seq)) for (let i = 1; i < l.length; i++) {
    drift++; // Counts coverage only; transitions need evidence review, not a blanket ban.
  }
  /* 3. publication boundary: an update is hidden at an exit on its unlock date and shown the day after (Codex review item 4) */
  for (const u of dd.updates) {
    const d0 = unlock(u), d1 = nextDay(d0);
    const has = d => { const ids = new Set(STORY.atExit(o, d).events.map(e => e.id)); return u.event_ids.every(id => ids.has(id)); };
    assert(!has(d0), `${c.id}: update ${u.event_ids} visible at its own unlock date ${d0}`);
    assert(has(d1), `${c.id}: update ${u.event_ids} not visible the day after unlock ${d1}`);
    boundaries++;
  }
}
/* 4. pins for the corrected verdicts (Codex review items 1-3); a rewrite that reintroduces the error fails here */
const upd = (id, ids) => byCase[id].scene_check.dated_debrief.updates.find(u => u.event_ids.join() === ids.join());
const all = (id, aid) => byCase[id].scene_check.dated_debrief.updates.flatMap(u => u.checks && u.checks[aid] ? [u.checks[aid]] : []);
// Target 050a03b08f: guidance verdicts stay Unresolved on motive; resumption 1 Mar 2022, cuts 18 May and 7 Jun
for (const t of all('050a03b08f', 'a3')) { assert(/^Unresolved/.test(t), 'Target a3 must stay Unresolved: ' + t); assert(!/three weeks|bluff|genuine unpredictability/i.test(t), 'Target a3 reintroduces motive/chronology: ' + t); }
{ const r = SIM.simulate(byCase['050a03b08f'].sim, { action: 'buy', size: 10, years: 3 }); const d = STORY.atExit(byCase['050a03b08f'], r.exit.date); assert(/May and again in June/.test(d.checks.a3.text), 'Target 3y verdict should date the May and June cuts'); }
// First Solar 5d6cb2d76f: enactment stays Supported when durability is questioned; capacity is never read as demand
for (const ids of [['e10'], ['e11']]) assert(/^Supported/.test(upd('5d6cb2d76f', ids).checks.a3), 'First Solar a3 must stay Supported at ' + ids);
for (const t of all('5d6cb2d76f', 'a2')) assert(!/^Supported\b(?! in form)/.test(t) && !/^Partly supported/.test(t), 'First Solar a2 (demand) read from capacity: ' + t);
// Sarepta 04b88176e1: refinancing is not new funding; accelerated approval rested on a surrogate
assert(/repa(id|y)/.test(upd('04b88176e1', ['e4']).narrative) && /repay/.test(upd('04b88176e1', ['e4']).checks.a3), 'Sarepta financing must mention repayment of earlier debt');
assert(!/program(me)? need/.test(upd('04b88176e1', ['e4']).narrative), 'Sarepta financing narrative reintroduces "programme need"');
assert(/surrogate|micro-dystrophin/.test(upd('04b88176e1', ['e5']).checks.a1), 'Sarepta approval verdict must name the surrogate basis');
for (const t of all('04b88176e1', 'a1')) assert(!/full approved population/.test(t), 'Sarepta a1 drifts from the subgroup: ' + t);
// Gilead 80222fdef8: the second-engine verdict does not reset on a regulatory step
for (const t of all('80222fdef8', 'a2')) assert(!/^Unresolved/.test(t), 'Gilead a2 resets to Unresolved: ' + t);
console.log(`dated debrief: ${cases.length} cases, ${n} horizon exits, ${boundaries} publication boundaries, ${drift} status transitions inspected, 6 verdict pins checked`);
