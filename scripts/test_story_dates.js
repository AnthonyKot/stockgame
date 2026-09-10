const assert = require('node:assert/strict');
const fs = require('node:fs');
const STORY = require('../site/story.js');
const SIM = require('../site/sim.js');
const o = JSON.parse(fs.readFileSync('site/data/146743bdc9/outcome.json'));
const sheet = JSON.parse(fs.readFileSync('site/data/146743bdc9/sheet.json'));
assert(!JSON.stringify(sheet).includes('dated_debrief'));
for (const [years, stops, check] of [[1, ['e2'], /Weakened/], [3, ['e2', 'e5'], /Mixed/], [5, ['e2', 'e5', 'e7', 'e8'], /Not supported/]]) {
  const r = SIM.simulate(o.sim, {action:'buy', size:10, years});
  const d = STORY.atExit(o, r.exit.date);
  assert.deepEqual(d.stops.map(s => s.event.id), stops);
  assert.match(d.checks.a1.text, check);
  if (years < 5) assert(!d.events.some(e => ['e4','e6','e7','e8','e9'].includes(e.id)));
}
for (const opts of [{action:'buy',stop:20},{action:'short',tp:50}]) {
  const r = SIM.simulate(o.sim, {size:10,years:5,...opts});
  assert(r.stopped);
  assert.deepEqual(STORY.atExit(o,r.exit.date).stops.map(s=>s.event.id), ['e2']);
}
assert.equal(STORY.atExit(o,'2018-03-01').stops.length,0);
assert.equal(STORY.atExit(o,'2018-06-02').stops.length,0); // no intraday timestamp: not known at exit open
assert.equal(STORY.atExit(o,'2018-06-04').stops.length,1);
assert(!STORY.atExit(o,'2018-06-05').events.some(e=>e.id==='e1')); // April occurrence, August source
assert(STORY.atExit(o,'2019-02-15').events.some(e=>e.id==='e1'));
assert(!STORY.atExit(o,'2021-02-16').events.some(e=>e.id==='e6')); // financing announced the day after actual 3y exit
assert(!STORY.availableBefore({date:'2018-10',source:{published:'2018-10'}},'2018-10-15'));
assert(STORY.availableBefore({date:'2018-10',source:{published:'2018-10'}},'2018-11-01'));
assert(!STORY.availableBefore({date:'2018-10-01'},'2023-01-01'));
for(const u of o.scene_check.dated_debrief.updates) for(const id of u.event_ids) assert(o.aftermath.events.some(e=>e.id===id));
console.log('story dates: horizons, early exits, publication boundaries and payload separation passed');
