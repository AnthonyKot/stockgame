// Campaign engine checks: (1) the engine plan's arithmetic fixture (long part) on synthetic data, (2) event ordering,
// eligibility, idempotency and replay, (3) the built proto-3 campaign played end to end and cross-checked against the
// standalone simulator (same conventions, so every closed position's return must match SIM.simulate to the basis point)
// and against the ledger identity. Run after build_campaign.py: node scripts/test_campaign.js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const C = require('../site/campaign-engine.js');
const SIM = require('../site/sim.js');

/* ---------- 1. synthetic fixture ---------- */
const cal = ['2020-01-02', '2020-01-03', '2020-01-06', '2020-01-07', '2020-01-08', '2021-01-04', '2021-01-05', '2021-01-06'];
const man = { campaign_id: 'fx', content_version: 'x', start_date: '2020-01-02', end_session: '2021-01-06', actions: ['buy', 'skip'], calendar: cal,
  rules: { rules_version: 'fx', starting_cash_usd: 100000, starting_btc: 1, sizes_pct: [5, 10, 20], horizons_years: [1], slippage_per_side: 0 },
  scenes: [{ index: 0, opaque_id: 'A', cutoff_date: '2020-01-02', entry_session: '2020-01-02', horizons: { '1': '2021-01-04' }, default_horizon: '1' },
           { index: 1, opaque_id: 'B', cutoff_date: '2020-01-07', entry_session: '2020-01-07', horizons: { '1': '2021-01-06' }, default_horizon: '1' }] };
const data = { prices: { A: [{ d: '2020-01-02', o: 100, c: 105 }, { d: '2020-01-03', o: 106, c: 120 }, { d: '2020-01-06', o: 121, c: 122 }, { d: '2020-01-07', o: 122, c: 125 }, { d: '2020-01-08', o: 125, c: 126 }, { d: '2021-01-04', o: 130, c: 131 }, { d: '2021-01-05', o: 131, c: 132 }, { d: '2021-01-06', o: 132, c: 133 }],
                        B: [{ d: '2020-01-07', o: 50, c: 51 }, { d: '2020-01-08', o: 51, c: 52 }, { d: '2021-01-04', o: 60, c: 60 }, { d: '2021-01-05', o: 60, c: 60 }, { d: '2021-01-06', o: 40, c: 41 }] },
  dividends: { A: [{ d: '2020-01-03', a: 1 }, { d: '2020-01-02', a: 9 }], B: [] },     // the 01-02 dividend is on the entry date: not entitled
  btc: [{ d: '2020-01-01', c: 10000 }, { d: '2020-01-02', c: 9000 }, { d: '2020-01-05', c: 8000 }, { d: '2021-01-03', c: 8000 }] };
let s = C.createState(man);
assert.equal(C.equity(s, man, data).total, 110000);                       // $100,000 + BTC at the 01-01 close (last completed before 01-02)
let r = C.decide(s, man, data, { action: 'buy', size_pct: 10, years: 1 }); assert(!r.error, r.error); s = r.state;
assert.equal(s.cash, 89000); assert.equal(s.reserved, 11000); assert.equal(C.equity(s, man, data).total, 110000);   // a reservation changes buying power, not equity
assert.equal(C.decide(s, man, data, { action: 'buy', size_pct: 10, years: 1 }).error, 'no decision is due now');
r = C.advance(s, man, data, { date: '2020-01-02', phase: 'closed' }); s = r.state;
assert.equal(s.positions[0].shares, 110); assert.equal(s.reserved, 0);     // 11,000 / 100 = 110 shares at the open
assert.equal(s.cash, 89000);                                               // ex-date on the entry date: no dividend
r = C.advance(s, man, data, { date: '2020-01-06', phase: 'closed' }); s = r.state;
assert.equal(s.cash, 89110);                                               // $1 x 110 on 01-03
let eq = C.equity(s, man, data);
assert.equal(eq.btc_value, 8000); assert.equal(eq.long_value, 110 * 122); assert.equal(eq.total, 89110 + 13420 + 8000);
assert.equal(C.advance(s, man, data, { date: '2020-01-08', phase: 'closed' }).error, 'decide the next story before advancing past 2020-01-07');
r = C.advance(s, man, data, { date: '2020-01-07', phase: 'pre-open' }); s = r.state; assert.equal(s.status, 'deciding');
assert.equal(C.decide(s, man, data, { action: 'buy', size_pct: 20, years: 3 }).error, 'this horizon does not fit the campaign\'s data coverage');
assert.match(C.decide(s, man, data, { action: 'buy', size_pct: 20, years: 1 }).error || '', /^$/);   // affordable: 20% of equity < cash
const equityBefore = C.equity(s, man, data).total;
r = C.decide(s, man, data, { action: 'buy', size_pct: 20, years: 1 }); s = r.state; assert.equal(r.order.budget, Math.round(equityBefore * 20) / 100);
assert.equal(s.cash + s.reserved, 89110);
const stop = C.nextStop(s, man); assert.deepEqual(stop, { kind: 'closure', date: '2021-01-04', phase: 'closed' });
r = C.advance(s, man, data, stop); s = r.state;
assert.equal(s.positions[0].status, 'closed'); assert.equal(s.positions[0].exit.proceeds, 110 * 130);
assert.equal(r.notices.filter(n => n.kind === 'closure').length, 1);
const again = C.advance(s, man, data, stop).state; assert.deepEqual(again.ledger, s.ledger); assert.equal(again.cash, s.cash);   // idempotent: no duplicate fills
r = C.advance(s, man, data, C.nextStop(s, man)); s = r.state; assert.equal(s.status, 'finished');
const rep = C.report(s, man, data); assert(rep.identity_ok, 'ledger identity'); assert.equal(rep.trades[0].result, 110 * 130 + 110 - 11000);
assert.equal(C.replay(man, data, s.log).cash, s.cash); assert.deepEqual(C.replay(man, data, s.log).ledger, s.ledger);
{ let a = C.createState(man); a = C.decide(a, man, data, { action: 'skip' }).state; a = C.advance(a, man, data, C.nextStop(a, man)).state; a = C.decide(a, man, data, { action: 'skip' }).state;
  assert.equal(a.status, 'finished'); assert.deepEqual(a.clock, { date: '2020-01-07', phase: 'pre-open' }); assert.equal(C.nextStop(a, man).kind, 'finished'); assert.equal(C.report(a, man, data).equity.total, 100000 + 8000); }   // all-skip ends at the last decision
console.log('fixture: reservations, fills, ex-date rule, BTC marks, eligibility, ordering, idempotency, replay, identity and all-skip ending passed');

/* ---------- 2. the built campaign, played end to end ---------- */
const dir = path.join('site', 'data', 'campaigns', 'proto-3');
const M = JSON.parse(fs.readFileSync(path.join(dir, 'manifest.json')));
const D = { prices: {}, dividends: {}, btc: [] };
for (const [oid, ins] of Object.entries(M.instruments)) { D.prices[oid] = []; D.dividends[oid] = []; let prev = ''; for (const b of ins.slices) { const f = JSON.parse(fs.readFileSync(path.join(dir, 'prices', oid, 'upto-' + b + '.json'))); assert(f.bars.every(x => x.d <= b && x.d > prev), `${oid} slice ${b} holds a bar outside (${prev}, ${b}]`); D.prices[oid].push(...f.bars); D.dividends[oid].push(...f.dividends); prev = b; } }
{ let prev = ''; for (const b of M.btc.slices) { const f = JSON.parse(fs.readFileSync(path.join(dir, 'prices', 'BTC', 'upto-' + b + '.json'))); assert(f.bars.every(x => x.d <= b && x.d > prev), `BTC slice ${b} out of range`); D.btc.push(...f.bars); prev = b; } }
// boundaries are exactly the possible stops: the session before each cutoff and every offered exit
const sessionBefore = d => M.calendar.filter(s => s < d).pop();
assert.deepEqual(M.instruments[M.scenes[0].opaque_id].slices, [...new Set([...M.scenes.map(s => sessionBefore(s.cutoff_date)), ...M.scenes.flatMap(s => Object.values(s.horizons))])].sort());
for (const s of M.scenes) for (const exit of Object.values(s.horizons)) { const db = JSON.parse(fs.readFileSync(path.join(dir, 'debrief', s.opaque_id, exit + '.json'))); assert.equal(db.exit, exit); assert(db.events.every(e => e.date < exit && (!e.source || !e.source.published || e.source.published < exit)), `${s.opaque_id} debrief ${exit} carries a later event`); assert(db.reveal.ticker); }
assert.equal(M.scenes.length, 3); assert.equal(M.scenes[2].horizons['3'], '2022-01-18');   // Sunday anniversary then MLK holiday
assert.equal(M.scenes[1].horizons['3'], '2021-11-15');                                        // Saturday anniversary
const plays = [{ action: 'buy', size_pct: 10, years: 5 }, { action: 'skip' }, { action: 'buy', size_pct: 20, years: 3 }];
let st = C.createState(M); const expectEntry = ['2018-02-15', null, '2019-01-16'];
for (let i = 0; i < 3; i++) {
  assert.equal(st.status, 'deciding'); assert.equal(st.clock.date, M.scenes[i].cutoff_date);
  const rr = C.decide(st, M, D, plays[i]); assert(!rr.error, rr.error); st = rr.state;
  const next = C.nextStop(st, M); const a = C.advance(st, M, D, next); assert(!a.error, a.error); st = a.state;
  if (expectEntry[i]) assert.equal(st.positions.find(p => p.order_id === 'o' + i).entry.date, expectEntry[i]);
}
let guard = 0;
while (st.status !== 'finished' && guard++ < 10) { const next = C.nextStop(st, M); assert.equal(next.kind, 'closure'); const a = C.advance(st, M, D, next); assert(!a.error, a.error); st = a.state; }
assert.equal(st.status, 'finished'); assert.equal(st.clock.date, '2023-02-15');             // last closure: Nektar 5y (JPM 3y closed 2022-01-18 before it)
const R = C.report(st, M, D); assert(R.identity_ok, 'ledger identity on real data');
assert(R.dividends > 0, 'JPMorgan paid dividends');
// cross-check every closed position against the standalone simulator on the same case and horizon
for (const t of R.trades.filter(t => t.exit)) {
  const oid = M.scenes[t.scene_index].opaque_id; const o = JSON.parse(fs.readFileSync(path.join('site', 'data', oid, 'outcome.json')));
  const sim = SIM.simulate(o.sim, { action: 'buy', size: t.size_pct, years: t.years }); assert.equal(sim.status, 'ok');
  assert.equal(sim.exit.date, t.exit.date, oid + ' exit date'); assert(Math.abs(sim.long_return * 100 - t.result_pct) < 0.06, `${oid}: engine ${t.result_pct}% vs simulator ${(sim.long_return * 100).toFixed(2)}%`);
}
const p0 = st.positions[0]; assert(p0.entry.open > 80 && p0.entry.open < 90, 'Nektar entry level is un-adjusted for the 2025 reverse split: ' + p0.entry.open);
assert(R.btc_start.c > 8000 && R.btc_start.c < 9500 && R.btc_start.d === '2018-02-14', 'BTC start mark is the completed 14 Feb UTC close');
assert(R.baseline !== null && R.calls_contribution !== null);
console.log(`slices: every stock and BTC slice stays inside its boundary; boundaries match the possible stops; ${M.scenes.length * 3} debrief slices hold nothing after their exit`);
console.log(`proto-3: 3 decisions, ${R.trades.filter(t => t.exit).length} closures, finished ${st.clock.date}; equity $${R.equity.total.toLocaleString()} vs baseline $${R.baseline.toLocaleString()} (BTC ${R.btc_start.c} -> ${R.btc_end.c}); calls ${R.calls_contribution >= 0 ? '+' : ''}$${R.calls_contribution.toLocaleString()}; simulator agreement and ledger identity passed`);
