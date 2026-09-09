/* Pure simulation of one decision on a case: horizon choice, optional stop loss and take profit.
   Same contract as scripts/build_bundles.py: entry at first open, exit at the horizon anniversary open,
   10 bp slippage per side, longs receive dividends in (entry, exit], shorts owe them and pay borrow on daily close.
   A stop or target triggers when a CLOSE crosses the level and fills at the NEXT session's open (gap risk included).
   Works in the browser (window.SIM) and in node (module.exports). */
(function (root, factory) { if (typeof module === 'object' && module.exports) module.exports = factory(); else root.SIM = factory(); })(typeof self !== 'undefined' ? self : this, function () {
  function simulate(sim, opts) {
    const p = sim.params || {}; const S = p.slippage ?? 0.001, B = p.borrow_annual ?? 0.05, EQ = p.start_equity ?? 100000;
    const path = sim.path; const action = opts.action; const size = action === 'skip' ? 0 : (opts.size || 0) / 100;
    const years = String(opts.years); const horizonExit = sim.horizons[years];
    if (!horizonExit) return { status: 'unavailable', reason: 'no ' + years + '-year exit in the cached data' };
    const entry = path[0]; const hIdx = path.findIndex(b => b.d === horizonExit); if (hIdx < 0) return { status: 'unavailable', reason: 'exit date not in path' };
    const days = (a, b) => Math.round((Date.parse(b) - Date.parse(a)) / 86400000);
    let exitIdx = hIdx, reason = 'held to the ' + years + '-year anniversary';
    if (action !== 'skip' && (opts.stop || opts.tp)) {
      const isLong = action === 'buy'; const e = entry.o;
      for (let i = 1; i < hIdx; i++) {   // check closes from the entry day on; fill next open
        const c = path[i].c; const ret = isLong ? c / e - 1 : 1 - c / e;
        if (opts.stop && ret <= -opts.stop / 100) { exitIdx = i + 1; reason = `stop loss hit on ${path[i].d} close (${(ret * 100).toFixed(1)}%), filled at the next open`; break; }
        if (opts.tp && ret >= opts.tp / 100) { exitIdx = i + 1; reason = `take profit hit on ${path[i].d} close (+${(ret * 100).toFixed(1)}%), filled at the next open`; break; }
      }
    }
    const exit = path[exitIdx]; const held = path.slice(0, exitIdx + 1);
    const divs = (sim.dividends || []).filter(x => x.d > entry.d && x.d <= exit.d).reduce((s, x) => s + x.a, 0);
    const spyDivs = (sim.spy_dividends || []).filter(x => x.d > entry.d && x.d <= exit.d).reduce((s, x) => s + x.a, 0);
    const sp = sim.spy_path; const spE = sp.find(b => b.d === entry.d), spX = sp.find(b => b.d === exit.d);
    const spyRet = spE && spX ? (spX.o + spyDivs) / spE.o - 1 : null;
    let borrow = 0; for (let i = 0; i < held.length - 1; i++) borrow += held[i].c * B / 365 * days(held[i].d, held[i + 1].d);
    const longRet = (exit.o * (1 - S) + divs) / (entry.o * (1 + S)) - 1;
    const shortRet = (entry.o * (1 - S) - exit.o * (1 + S) - divs - borrow) / entry.o;
    let peak = held[0].c, dd = 0; for (const b of held) { peak = Math.max(peak, b.c); dd = Math.min(dd, b.c / peak - 1); }
    const posRet = action === 'buy' ? longRet : action === 'short' ? shortRet : 0;
    return { status: 'ok', action, size, years: Number(years), entry: { date: entry.d, open: entry.o }, exit: { date: exit.d, open: exit.o }, exit_reason: reason, stopped: exitIdx !== hIdx,
      calendar_days: days(entry.d, exit.d), dividends_per_share: divs, borrow_fee_per_share: borrow, long_return: longRet, short_return: shortRet,
      position_return: posRet, portfolio_return: size * posRet, end_equity: EQ * (1 + size * posRet), spy_return: spyRet, max_drawdown: dd,
      held_to_horizon: { exit: path[hIdx].d, long_return: (path[hIdx].o * (1 - S) + (sim.dividends || []).filter(x => x.d > entry.d && x.d <= path[hIdx].d).reduce((s, x) => s + x.a, 0)) / (entry.o * (1 + S)) - 1 } };
  }
  return { simulate };
});
