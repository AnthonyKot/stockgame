/* Campaign ledger engine (idea 1, long and skip). Pure: no DOM, network, randomness or wall clock.
   The caller loads the manifest and the dated price slices and passes them as `data`:
     data = { prices: { <instrument>: [{d, o, c}, ...] }, dividends: { <instrument>: [{d, a}, ...] }, btc: [{d, c}, ...] }
   sorted by date. The engine only ever reads bars at or before its clock, so slices may stop at the clock.
   Clock = { date: 'YYYY-MM-DD', phase: 'pre-open' | 'closed' }. A scene stop is (cutoff_date, pre-open); a closure stop
   is (exit_session, closed). Every ledger event has a stable id and is applied at most once.
   Works in the browser (window.CAMPAIGN) and in node (module.exports). */
(function (root, factory) { if (typeof module === 'object' && module.exports) module.exports = factory(); else root.CAMPAIGN = factory(); })(typeof self !== 'undefined' ? self : this, function () {
  const clone = x => JSON.parse(JSON.stringify(x));
  const r2 = x => Math.round(x * 100) / 100;
  const cmpClock = (a, b) => a.date === b.date ? (a.phase === b.phase ? 0 : a.phase === 'pre-open' ? -1 : 1) : (a.date < b.date ? -1 : 1);

  function createState(manifest) {
    return { campaign_id: manifest.campaign_id, content_version: manifest.content_version, rules_version: manifest.rules.rules_version, revision: 0,
      clock: { date: manifest.start_date, phase: 'pre-open' }, scene_index: 0,
      cash: manifest.rules.starting_cash_usd, reserved: 0, btc_qty: manifest.rules.starting_btc,
      orders: [], positions: [], ledger: [], processed: {}, status: 'deciding', log: [] };
  }

  function lastBar(bars, clock, inclusiveOnClosed) {
    let out = null;
    for (const b of bars || []) { if (b.d < clock.date || (inclusiveOnClosed && clock.phase === 'closed' && b.d === clock.date)) out = b; else if (b.d > clock.date) break; }
    return out;
  }
  const btcMark = (data, clock) => lastBar(data.btc, clock, false);           // last completed UTC close strictly before the date
  const stockMark = (data, inst, clock) => lastBar(data.prices[inst], clock, true);

  function equity(state, manifest, data) {
    const btc = btcMark(data, state.clock); const btc_value = btc ? r2(state.btc_qty * btc.c) : 0;
    const positions = state.positions.filter(p => p.status === 'open').map(p => {
      const m = stockMark(data, p.instrument, state.clock); const value = m ? r2(p.shares * m.c) : p.cost;
      return { ...p, mark: m, value, gain: r2(value + p.dividends_received - p.cost) };
    });
    const long_value = r2(positions.reduce((s, p) => s + p.value, 0));
    return { cash: r2(state.cash), reserved: r2(state.reserved), long_value, btc_value, btc_mark: btc, total: r2(state.cash + state.reserved + long_value + btc_value), positions };
  }

  function sceneAt(manifest, clock) { return manifest.scenes.find(s => s.cutoff_date === clock.date) || null; }

  function decide(state0, manifest, data, cmd) {
    const state = clone(state0); const scene = manifest.scenes[state.scene_index];
    if (state.status !== 'deciding' || !scene) return { error: 'no decision is due now' };
    if (state.clock.date !== scene.cutoff_date || state.clock.phase !== 'pre-open') return { error: 'the clock is not at this scene\'s cutoff' };
    if (!manifest.actions.includes(cmd.action)) return { error: 'action not available in this campaign: ' + cmd.action };
    const years = String(cmd.years || scene.default_horizon);
    if (cmd.action !== 'skip' && !scene.horizons[years]) return { error: 'this horizon does not fit the campaign\'s data coverage' };
    const eq = equity(state, manifest, data);
    const pct = cmd.action === 'skip' ? 0 : Number(cmd.size_pct);
    if (cmd.action !== 'skip' && !manifest.rules.sizes_pct.includes(pct)) return { error: 'size must be one of ' + manifest.rules.sizes_pct.join('/') + '%' };
    const budget = r2(eq.total * pct / 100);
    if (cmd.action === 'buy' && budget > state.cash + 1e-9) return { error: `not enough free cash: this size needs $${budget.toLocaleString()} and you have $${r2(state.cash).toLocaleString()} free` };
    const order = { id: 'o' + state.scene_index, scene_index: state.scene_index, instrument: scene.opaque_id, action: cmd.action, size_pct: pct, years: cmd.action === 'skip' ? null : Number(years),
      budget, equity_at_decision: eq.total, entry_session: scene.entry_session, exit_session: cmd.action === 'skip' ? null : scene.horizons[years],
      decided_at: clone(state.clock), assumptions: cmd.assumptions || [], reason: cmd.reason || '', status: cmd.action === 'skip' ? 'skipped' : 'pending' };
    if (cmd.action === 'buy') { state.cash = r2(state.cash - budget); state.reserved = r2(state.reserved + budget); }
    state.orders.push(order); state.ledger.push({ id: 'decide:' + order.id, date: state.clock.date, kind: 'decision', order: order.id, cash_delta: cmd.action === 'buy' ? -budget : 0, note: `${cmd.action}${pct ? ' ' + pct + '%' : ''}${order.years ? ' for ' + order.years + 'y' : ''}, budget $${budget}` });
    state.scene_index += 1; state.revision += 1; state.status = 'advancing';
    state.log.push({ type: 'decide', cmd: { action: cmd.action, size_pct: pct, years: order.years, assumptions: order.assumptions, reason: order.reason } });
    return { state, order };
  }

  function nextStop(state, manifest) {
    const cands = [];
    if (state.scene_index < manifest.scenes.length) { const s = manifest.scenes[state.scene_index]; cands.push({ kind: 'scene', index: s.index, date: s.cutoff_date, phase: 'pre-open' }); }
    const exits = [...state.positions.filter(p => p.status === 'open').map(p => p.exit_session), ...state.orders.filter(o => o.status === 'pending').map(o => o.exit_session)].filter(Boolean).sort();
    if (exits.length) cands.push({ kind: 'closure', date: exits[0], phase: 'closed' });
    if (!cands.length) return { kind: 'finished', date: manifest.end_session, phase: 'closed' };
    cands.sort(cmpClock); return cands[0];
  }

  function processSession(state, manifest, data, s, notices) {
    const S = manifest.rules.slippage_per_side; const bar = inst => (data.prices[inst] || []).find(b => b.d === s);
    const apply = (id, fn) => { if (state.processed[id]) return; fn(); state.processed[id] = true; };
    // 1. scheduled exits at the open
    for (const p of state.positions) if (p.status === 'open' && p.exit_session === s) apply('exit:' + p.id, () => {
      const b = bar(p.instrument); if (!b) throw new Error('no bar for exit ' + p.instrument + ' ' + s);
      const proceeds = r2(p.shares * b.o * (1 - S)); p.status = 'closed'; p.exit = { date: s, open: b.o, proceeds, slippage: r2(p.shares * b.o * S) };
      state.cash = r2(state.cash + proceeds);
      state.ledger.push({ id: 'exit:' + p.id, date: s, kind: 'exit', position: p.id, cash_delta: proceeds, note: `sold ${p.shares.toFixed(4)} shares at $${b.o} open, ${manifest.rules.slippage_per_side * 1e4} bp slippage` });
      notices.push({ date: s, kind: 'closure', position: p.id, order: p.order_id, scene_index: p.scene_index, proceeds, result: r2(proceeds + p.dividends_received - p.cost) });
    });
    // 2. pending entries at the open
    for (const o of state.orders) if (o.status === 'pending' && o.entry_session === s) apply('entry:' + o.id, () => {
      const b = bar(o.instrument); if (!b) throw new Error('no bar for entry ' + o.instrument + ' ' + s);
      const shares = o.budget / (b.o * (1 + S)); const p = { id: 'p' + o.id.slice(1), order_id: o.id, scene_index: o.scene_index, instrument: o.instrument, shares, cost: o.budget,
        entry: { date: s, open: b.o, slippage: r2(shares * b.o * S) }, exit_session: o.exit_session, years: o.years, dividends_received: 0, status: 'open' };
      state.reserved = r2(state.reserved - o.budget); o.status = 'filled'; o.position_id = p.id; state.positions.push(p);
      state.ledger.push({ id: 'entry:' + o.id, date: s, kind: 'entry', position: p.id, cash_delta: 0, note: `bought ${shares.toFixed(4)} shares at $${b.o} open for the reserved $${o.budget}` });
      notices.push({ date: s, kind: 'fill', position: p.id, order: o.id, scene_index: o.scene_index, shares, open: b.o });
    });
    // 3. ex-date dividends: entitled if entry date < ex-date <= exit date (same rule as the standalone simulator)
    for (const p of state.positions) for (const d of (data.dividends[p.instrument] || [])) if (d.d === s && p.entry && p.entry.date < s && (p.status === 'open' || (p.exit && p.exit.date === s))) apply(`div:${p.id}:${s}`, () => {
      const amt = r2(p.shares * d.a); p.dividends_received = r2(p.dividends_received + amt); state.cash = r2(state.cash + amt);
      state.ledger.push({ id: `div:${p.id}:${s}`, date: s, kind: 'dividend', position: p.id, cash_delta: amt, note: `$${d.a} per share on ${p.shares.toFixed(4)} shares (ex-date cash)` });
      notices.push({ date: s, kind: 'dividend', position: p.id, amount: amt });
    });
    // 4. close marks are computed on demand from the slices; nothing accrues for long/skip.
  }

  function advance(state0, manifest, data, target) {
    const state = clone(state0); const notices = [];
    if (cmpClock(target, state.clock) < 0) return { error: 'the clock never moves backward' };
    const pendingScene = state.scene_index < manifest.scenes.length ? manifest.scenes[state.scene_index] : null;
    if (pendingScene && cmpClock(target, { date: pendingScene.cutoff_date, phase: 'pre-open' }) > 0) return { error: 'decide the next story before advancing past ' + pendingScene.cutoff_date };
    if (target.date > manifest.end_session) return { error: 'beyond the campaign end ' + manifest.end_session };
    for (const s of manifest.calendar) {
      const due = s > state.clock.date || (s === state.clock.date && state.clock.phase === 'pre-open');
      if (!due) continue;
      if (s > target.date || (s === target.date && target.phase === 'pre-open')) break;
      processSession(state, manifest, data, s, notices);
    }
    state.clock = clone(target); state.revision += 1;
    const open = state.positions.some(p => p.status === 'open') || state.orders.some(o => o.status === 'pending');
    state.status = (pendingScene && target.date === pendingScene.cutoff_date && target.phase === 'pre-open') ? 'deciding' : (!pendingScene && !open) ? 'finished' : 'advancing';
    state.log.push({ type: 'advance', target: clone(target) });
    return { state, notices };
  }

  function replay(manifest, data, log) {
    let state = createState(manifest);
    for (const entry of log) {
      const r = entry.type === 'decide' ? decide(state, manifest, data, entry.cmd) : advance(state, manifest, data, entry.target);
      if (r.error) throw new Error('replay failed: ' + r.error); state = r.state;
    }
    return state;
  }

  function report(state, manifest, data) {
    const eq = equity(state, manifest, data); const rules = manifest.rules;
    const btc0 = btcMark(data, { date: manifest.start_date, phase: 'pre-open' });
    const trades = state.orders.map(o => { const p = state.positions.find(x => x.id === o.position_id);
      return { order: o.id, scene_index: o.scene_index, action: o.action, size_pct: o.size_pct, years: o.years, budget: o.budget, status: p ? p.status : o.status,
        entry: p ? p.entry : null, exit: p ? p.exit : null, dividends: p ? p.dividends_received : 0,
        result: p && p.exit ? r2(p.exit.proceeds + p.dividends_received - p.cost) : null, result_pct: p && p.exit ? Math.round(((p.exit.proceeds + p.dividends_received) / p.cost - 1) * 1000) / 10 : null,
        slippage: p ? r2(p.entry.slippage + (p.exit ? p.exit.slippage : 0)) : 0 }; });
    const realized = r2(trades.reduce((s, t) => s + (t.result || 0), 0)); const dividends = r2(trades.reduce((s, t) => s + t.dividends, 0)); const slippage = r2(trades.reduce((s, t) => s + t.slippage, 0));
    const btc_gain = btc0 && eq.btc_mark ? r2(state.btc_qty * (eq.btc_mark.c - btc0.c)) : 0;
    const baseline = btc0 && eq.btc_mark ? r2(rules.starting_cash_usd + rules.starting_btc * eq.btc_mark.c) : null;
    return { clock: state.clock, equity: eq, trades, realized, dividends, slippage, btc_start: btc0, btc_end: eq.btc_mark, btc_gain, baseline,
      starting_total: btc0 ? r2(rules.starting_cash_usd + rules.starting_btc * btc0.c) : null, calls_contribution: baseline !== null ? r2(eq.total - baseline) : null,
      identity_ok: Math.abs(eq.total - (rules.starting_cash_usd + rules.starting_btc * (eq.btc_mark ? eq.btc_mark.c : 0) + realized + eq.long_value - state.positions.filter(p => p.status === 'open').reduce((s, p) => s + p.cost - p.dividends_received, 0))) < 0.05 };
  }

  return { createState, decide, advance, nextStop, equity, report, replay, btcMark, stockMark, sceneAt, cmpClock };
});
