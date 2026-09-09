// Checks site/sim.js against the builder's numbers for every case (no stop) and exercises a stop. Run: node scripts/test_simulate.js
const fs = require('fs'), path = require('path');
const SIM = require(path.join(__dirname, '..', 'site', 'sim.js'));
const root = path.join(__dirname, '..', 'site', 'data'); const idx = JSON.parse(fs.readFileSync(path.join(root, 'index.json')));
let fails = 0; const close = (a, b, tol = 2e-4) => Math.abs(a - b) < tol;
for (const c of idx.cases) {
  const o = JSON.parse(fs.readFileSync(path.join(root, c.id, 'outcome.json'))); const y = Number(c.horizon.count);
  const r = SIM.simulate(o.sim, { action: 'buy', size: 10, years: y }); const s = SIM.simulate(o.sim, { action: 'short', size: 10, years: y });
  const ok = r.exit.date === o.exit.date && close(r.long_return, o.long_total_return_after_costs) && close(s.short_return, o.short_total_return_after_costs) && close(r.spy_return, o.spy_open_to_open_return) && close(r.max_drawdown, o.max_drawdown_from_entry_path, 1e-3);
  for (const [k, v] of Object.entries(o.alternative_horizons || {})) if (v.exit) { const a = SIM.simulate(o.sim, { action: 'buy', size: 10, years: Number(k) }); if (!(a.exit.date === v.exit.date && close(a.long_return, v.long_total_return_after_costs))) { console.log(o.ticker, k + 'y alt mismatch', a.long_return, v.long_total_return_after_costs); fails++; } }
  console.log(o.ticker.padEnd(5), ok ? 'OK  ' : 'FAIL', 'long', r.long_return.toFixed(4), 'vs', o.long_total_return_after_costs, '| short', s.short_return.toFixed(4), 'vs', o.short_total_return_after_costs); if (!ok) fails++;
}
// stop-loss behaviour on Nektar: -20% stop must exit early at an open, and give a better result than holding
const nk = JSON.parse(fs.readFileSync(path.join(root, idx.cases.find(c => c.sector_hint.startsWith('biotech') && c.horizon.count == 5 && c.cutoff.startsWith('2018-02')).id, 'outcome.json')));
const st = SIM.simulate(nk.sim, { action: 'buy', size: 10, years: 5, stop: 20 });
console.log('NKTR stop 20%:', st.exit_reason, '| position', st.position_return.toFixed(4), '| held to horizon', st.held_to_horizon.long_return.toFixed(4));
if (!(st.stopped && st.position_return > st.held_to_horizon.long_return)) fails++;
const tp = SIM.simulate(nk.sim, { action: 'short', size: 10, years: 5, tp: 50 }); console.log('NKTR short tp 50%:', tp.exit_reason, '| position', tp.position_return.toFixed(4)); if (!tp.stopped) fails++;
console.log(fails ? `FAILURES: ${fails}` : 'test_simulate: all cases match the builder');
process.exit(fails ? 1 : 0);
