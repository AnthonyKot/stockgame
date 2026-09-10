const assert = require('node:assert/strict');
const fs = require('node:fs');
const { outcomePassages, inspectPayload } = require('./payload_checks.js');
const idx = JSON.parse(fs.readFileSync('site/data/index.json'));
const passages = idx.cases.flatMap(c => outcomePassages(JSON.parse(fs.readFileSync(`site/data/${c.id}/outcome.json`))));
for (const c of idx.cases) for (const file of ['sheet', 'market']) {
  const p = JSON.parse(fs.readFileSync(`site/data/${c.id}/${file}.json`));
  assert.deepEqual(inspectPayload(p, passages), [], `${c.id}/${file}: pre-decision spoiler`);
}
assert.deepEqual(inspectPayload(idx, passages), [], 'index: pre-decision spoiler');
// Prove the checker catches nested fields and prose copied into a harmless-looking key.
const fact = 'The larger randomized study missed both primary endpoints and the company ended the program.';
const fixture = { scene_check: { assumptions: [{text:'The candidate will succeed.'}], dated_debrief: {
  baseline: { checks: {a1:'The candidate will succeed.'} }, updates: [{narrative:fact}]
} } };
const patterns = outcomePassages(fixture);
assert(inspectPayload({notes:{help:fact.toUpperCase().replaceAll(' ', '\n')}}, patterns).length);
assert(inspectPayload({notes:{dated_debrief:{}}}, patterns).length);
assert(inspectPayload({notes:{aftermath:[]}}, patterns).length);
assert(inspectPayload({notes:{long_total_return_after_costs:0}}, patterns).length);
assert.deepEqual(inspectPayload({assumption:'The candidate will succeed.', date:'2018-02-15', value:84}, patterns), []);
assert.deepEqual(inspectPayload({notes:'A brief describes the starting evidence without a result.'}, patterns), []);
console.log(`payloads: ${idx.cases.length} sheets, ${idx.cases.length} markets, index and copy-detection fixtures passed`);
