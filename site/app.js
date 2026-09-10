/* Stockgame MVP shared code: loading, storage, formatting, charts. No dependencies. */
'use strict';
const SG = (() => {
  const JKEY = 'stockgame.journal.v1', TKEY = 'stockgame.transparent';
  const $ = (sel, root = document) => root.querySelector(sel);
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === 'class') n.className = v; else if (k === 'html') n.innerHTML = v; else if (k.startsWith('on')) n.addEventListener(k.slice(2), v); else if (v !== null && v !== undefined) n.setAttribute(k, v);
    }
    for (const k of kids.flat()) if (k !== null && k !== undefined) n.append(k.nodeType ? k : document.createTextNode(String(k)));
    return n;
  };
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  async function load(url) { const r = await fetch(url, { cache: 'no-store' }); if (!r.ok) throw new Error(url + ' ' + r.status); return r.json(); }
  const safe = fn => { try { return fn(); } catch (e) { return null; } };
  const journal = () => safe(() => JSON.parse(localStorage.getItem(JKEY) || '[]')) || [];
  const saveJournal = j => { try { localStorage.setItem(JKEY, JSON.stringify(j)); return JSON.parse(localStorage.getItem(JKEY) || '[]').length === j.length; } catch (e) { return false; } };
  const findCommit = id => journal().find(x => x.case_id === id) || null;
  const upsertCommit = entry => { const j = journal().filter(x => x.case_id !== entry.case_id); j.push(entry); return saveJournal(j); };
  const transparent = () => safe(() => localStorage.getItem(TKEY) === '1') || false;
  const setTransparent = v => safe(() => localStorage.setItem(TKEY, v ? '1' : '0'));
  const pct = (x, d = 1) => (x === null || x === undefined || isNaN(x)) ? 'n/a' : ((x * 100).toFixed(d) + '%');
  const signed = (x, d = 1) => (x === null || x === undefined || isNaN(x)) ? 'n/a' : ((x >= 0 ? '+' : '') + (x * 100).toFixed(d) + '%');
  const money = (x, unit) => {
    if (x === null || x === undefined || x === '') return 'not available';
    if (typeof x !== 'number') return String(x);
    const u = String(unit || '');
    if (/USD_millions/i.test(u)) return Math.abs(x) < 0.05 ? 'about breakeven ($' + Math.round(x * 1000) + 'k)' : (Math.abs(x) >= 1e6 ? '$' + (x / 1e6).toFixed(2) + ' tn' : Math.abs(x) >= 1000 ? '$' + (x / 1000).toFixed(2) + ' bn' : '$' + x.toFixed(1) + ' m');
    if (/USD_billions/i.test(u)) return Math.abs(x) >= 1000 ? '$' + (x / 1000).toFixed(2) + ' tn' : '$' + x.toFixed(2) + ' bn';
    if (/USD_thousands/i.test(u)) return '$' + (x / 1000).toFixed(1) + ' m';
    if (/percent|pct|%/i.test(u)) return x.toFixed(1) + '%';
    if (/shares/i.test(u)) return x.toFixed(1) + (/million/i.test(u) ? ' m shares' : ' shares');
    if (/per_share|USD\/share|EPS/i.test(u)) return '$' + x.toFixed(2);
    if (/millions/i.test(u)) return x.toFixed(1) + ' m';
    if (/^USD$/i.test(u)) return '$' + x.toLocaleString('en-US', { maximumFractionDigits: 0 });
    return x.toLocaleString('en-US', { maximumFractionDigits: 2 }) + (u ? ' ' + u : '');
  };
  const dateFmt = iso => { if (!iso) return ''; if (iso.length === 7) return new Date(iso + '-15T12:00:00Z').toLocaleDateString('en-GB', { month: 'short', year: 'numeric', timeZone: 'UTC' }); const d = new Date(iso.slice(0, 10) + 'T12:00:00Z'); return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }); };
  const horizonText = h => { const n = Number(h.count); return n + ' calendar ' + (n === 1 ? 'year' : 'years'); };
  const badge = s => el('span', { class: 'badge ' + (s || '') }, (s || '').replace('_', ' '));
  /* Cite buttons: [c3] in prose -> button opening the evidence drawer */
  function prose(text, onCite) {
    const frag = document.createDocumentFragment(); const re = /\[([a-z]\d+(?:\s*,\s*[a-z]\d+)*)\]/g; let last = 0, m;
    const t = String(text ?? '');
    while ((m = re.exec(t))) {
      frag.append(t.slice(last, m.index));
      for (const id of m[1].split(/\s*,\s*/)) frag.append(el('button', { class: 'cite', type: 'button', 'aria-label': 'Show evidence ' + id, onclick: () => onCite(id) }, '[' + id + ']'), ' ');
      last = re.lastIndex;
    }
    frag.append(t.slice(last)); return frag;
  }
  /* Line chart: series [{name, cls, points:[{d, v}]}], opts {rebase, volume:[{d,v}], yFmt, height} */
  function drawChart(host, series, opts = {}) {
    host.innerHTML = '';
    const W = 800, H = opts.height || 300, VH = opts.volume ? 60 : 0, padL = 48, padR = 34, padT = 12, padB = 26;
    const all = series.flatMap(s => s.points); if (!all.length) { host.append(el('p', { class: 'muted' }, 'No price data.')); return; }
    const dates = [...new Set(all.map(p => p.d))].sort(); const xi = new Map(dates.map((d, i) => [d, i]));
    let ss = series.map(s => ({ ...s, points: s.points.filter(p => p.v !== null && p.v !== undefined) }));
    if (opts.rebase) ss = ss.map(s => { const b = s.points[0]?.v || 1; return { ...s, points: s.points.map(p => ({ d: p.d, v: p.v / b * 100, raw: p.v })) }; });
    const vals = ss.flatMap(s => s.points.map(p => p.v)); let lo = Math.min(...vals), hi = Math.max(...vals); if (lo === hi) { lo -= 1; hi += 1; }
    const useLog = opts.rebase && lo > 0 && hi / lo > 6;
    if (useLog) { lo = lo / 1.05; hi = hi * 1.05; } else { const pad = (hi - lo) * 0.06; lo = Math.max(opts.rebase ? 0 : -Infinity, lo - pad); hi += pad; }
    const x = d => padL + (xi.get(d) / Math.max(1, dates.length - 1)) * (W - padL - padR);
    const T = v => useLog ? Math.log(v) : v;
    const y = v => padT + (1 - (T(v) - T(lo)) / (T(hi) - T(lo))) * (H - padT - padB);
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); svg.setAttribute('viewBox', `0 0 ${W} ${H + VH}`); svg.setAttribute('class', 'chart'); svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', (opts.label || 'Line chart') + (useLog ? ' (logarithmic scale)' : '')); const N = (t, a = {}) => { const n = document.createElementNS('http://www.w3.org/2000/svg', t); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); return n; };
    const g = N('g', { class: 'grid' }), ax = N('g', { class: 'axis' });
    const ticks = 4; for (let i = 0; i <= ticks; i++) { const v = useLog ? Math.exp(Math.log(lo) + (Math.log(hi) - Math.log(lo)) * i / ticks) : lo + (hi - lo) * i / ticks; g.append(N('line', { x1: padL, x2: W - padR, y1: y(v), y2: y(v) })); const t = N('text', { x: padL - 6, y: y(v) + 4, 'text-anchor': 'end' }); t.textContent = (opts.yFmt || (n => n.toFixed(0)))(v); ax.append(t); }
    const step = Math.max(1, Math.floor(dates.length / 6)); let lastLbl = '';
    let lastX = -1e9; dates.forEach((d, i) => { if (i % step === 0 || i === dates.length - 1) { const lbl = dates.length > 400 ? d.slice(0, 4) : d.slice(0, 7); if (lbl !== lastLbl && x(d) - lastX > 70) { const t = N('text', { x: x(d), y: H - 8, 'text-anchor': i === dates.length - 1 ? 'end' : 'middle' }); t.textContent = lbl; ax.append(t); lastLbl = lbl; lastX = x(d); } } });
    svg.append(g, ax);
    if (opts.volume) { const vg = N('g', { class: 'vol' }); const vmax = Math.max(...opts.volume.map(v => v.v || 0)) || 1; const bw = Math.max(1, (W - padL - padR) / dates.length - 0.5);
      for (const v of opts.volume) if (xi.has(v.d)) { const h = (v.v || 0) / vmax * (VH - 6); vg.append(N('rect', { x: x(v.d) - bw / 2, y: H + VH - h, width: bw, height: h })); } svg.append(vg); }
    for (const s of ss) { const d = s.points.map((p, i) => (i ? 'L' : 'M') + x(p.d).toFixed(1) + ' ' + y(p.v).toFixed(1)).join(' '); svg.append(N('path', { d, class: s.cls })); }
    const cross = N('g', { class: 'cross', visibility: 'hidden' }); const cl = N('line', { y1: padT, y2: H - padB }); cross.append(cl);
    const markers = ss.map(s => { const c = N('circle', { r: 4, class: 'marker', stroke: 'currentColor' }); c.style.stroke = s.cls === 's1' ? 'var(--s1)' : 'var(--s2)'; cross.append(c); return c; });
    if (useLog) host.append(el('p', { class: 'note', style: 'margin:0' }, 'Logarithmic scale: equal vertical steps are equal percentage moves.'));
    for (const mk of opts.markers || []) if (xi.has(mk.d)) { const mg = N('g', { class: 'axis' }); mg.append(N('line', { x1: x(mk.d), x2: x(mk.d), y1: padT, y2: H - padB, stroke: 'var(--axis)', 'stroke-dasharray': mk.scored ? '0' : '4 3', 'stroke-width': mk.scored ? 2 : 1 })); const num = /^\d+$/.test(mk.label); const t = N('text', { x: num ? x(mk.d) : x(mk.d) - 4, y: num ? H - padB - 4 : padT + 12, 'text-anchor': num ? 'middle' : 'end', 'font-size': num ? '10' : '11' }); t.textContent = mk.label; mg.append(t); if (num) mg.querySelector('line').setAttribute('stroke-opacity', '0.5'); svg.append(mg); }
    svg.append(cross); const wrap = el('div', { style: 'position:relative' }); const tip = el('div', { class: 'tip', hidden: '' }); wrap.append(svg, tip); host.append(wrap);
    const maps = ss.map(s => new Map(s.points.map(p => [p.d, p])));
    const show = d => { cross.setAttribute('visibility', 'visible'); cl.setAttribute('x1', x(d)); cl.setAttribute('x2', x(d)); const rows = [];
      ss.forEach((s, i) => { const p = maps[i].get(d); if (p) { markers[i].setAttribute('cx', x(d)); markers[i].setAttribute('cy', y(p.v)); markers[i].setAttribute('visibility', 'visible'); rows.push(`${esc(s.name)}: ${opts.rebase ? p.v.toFixed(1) + ' (' + (opts.rawFmt || (r => r.toFixed(2)))(p.raw) + ')' : (opts.yFmt || (n => n.toFixed(2)))(p.v)}`); } else markers[i].setAttribute('visibility', 'hidden'); });
      const vol = opts.volume && opts.volume.find(v => v.d === d); if (vol && vol.v) rows.push('Volume: ' + vol.v.toLocaleString('en-US'));
      tip.innerHTML = `<div><b>${esc(d)}</b></div>` + rows.map(r => `<div>${r}</div>`).join(''); tip.hidden = false;
      const r = svg.getBoundingClientRect(); const px = x(d) / W * r.width; tip.style.left = Math.min(px + 12, r.width - tip.offsetWidth - 4) + 'px'; tip.style.top = '8px'; };
    svg.addEventListener('mousemove', e => { const r = svg.getBoundingClientRect(); const fx = (e.clientX - r.left) / r.width * W; const i = Math.round((fx - padL) / (W - padL - padR) * (dates.length - 1)); if (i >= 0 && i < dates.length) show(dates[i]); });
    svg.addEventListener('mouseleave', () => { cross.setAttribute('visibility', 'hidden'); tip.hidden = true; });
    svg.tabIndex = 0; let ki = dates.length - 1; svg.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') { ki = Math.max(0, ki - 1); show(dates[ki]); e.preventDefault(); } if (e.key === 'ArrowRight') { ki = Math.min(dates.length - 1, ki + 1); show(dates[ki]); e.preventDefault(); } });
    /* table alternative */
    const det = el('details', {}, el('summary', {}, 'Show as table')); const tb = el('table', {}); const thead = el('tr', {}, el('th', {}, 'Date'), ...ss.map(s => el('th', { class: 'n' }, s.name + (opts.rebase ? ' (index)' : ''))), opts.volume ? el('th', { class: 'n' }, 'Volume') : null); tb.append(thead);
    const stride = Math.max(1, Math.floor(dates.length / 60)); dates.forEach((d, i) => { if (i % stride === 0 || i === dates.length - 1) tb.append(el('tr', {}, el('td', {}, d), ...ss.map((s, j) => { const p = maps[j].get(d); return el('td', { class: 'n' }, p ? p.v.toFixed(1) : ''); }), opts.volume ? el('td', { class: 'n' }, (opts.volume.find(v => v.d === d)?.v || '').toLocaleString('en-US')) : null)); });
    det.append(el('div', { class: 'scroll' }, tb)); host.append(det);
  }

  /* Controlled chart: legend toggles + relative view. series[0] is the subject, series[1] the benchmark. */
  function lineChart(host, series, opts = {}) {
    if (!opts.controls) return drawChart(host, series, opts);
    const state = { hidden: new Set(), relative: false };
    const shell = el('div'); const bar = el('div', { class: 'row legend', role: 'group', 'aria-label': 'Chart series' }); const plot = el('div'); shell.append(bar, plot); host.innerHTML = ''; host.append(shell);
    const render = () => {
      bar.innerHTML = '';
      series.forEach((s, i) => bar.append(el('button', { type: 'button', class: 'ghost lg ' + (s.cls === 's1' ? 'l1' : 'l2'), 'aria-pressed': state.hidden.has(i) ? 'false' : 'true', disabled: state.relative ? '' : null, onclick: () => { if (state.hidden.has(i)) state.hidden.delete(i); else if (state.hidden.size < series.length - 1) state.hidden.add(i); render(); } }, s.name)));
      if (series.length > 1) bar.append(el('button', { type: 'button', class: 'ghost', 'aria-pressed': state.relative ? 'true' : 'false', onclick: () => { state.relative = !state.relative; render(); } }, 'Relative to ' + series[1].name));
      let shown, o = { ...opts };
      if (state.relative) {
        const b = new Map(series[1].points.map(p => [p.d, p.v])); const b0 = series[1].points[0]?.v, s0 = series[0].points[0]?.v;
        shown = [{ name: series[0].name + ' ÷ ' + series[1].name, cls: 's1', points: series[0].points.filter(p => b.has(p.d) && b0 && s0).map(p => ({ d: p.d, v: (p.v / s0) / (b.get(p.d) / b0) * 100 })) }];
        o.rebase = false; o.yFmt = n => n.toFixed(0); o.label = (opts.label || 'Chart') + ', shown as the ratio of the two series indexed to 100: above 100 means the stock has done better than the benchmark since the start of the window';
        o.volume = null;
      } else shown = series.filter((_, i) => !state.hidden.has(i));
      drawChart(plot, shown, o);
      if (state.relative) plot.append(el('p', { class: 'note', style: 'margin:0' }, 'Ratio view: one line, stock divided by ' + series[1].name + ', both starting at 100. Rising means the stock is beating the benchmark, falling means lagging, regardless of what either did on its own.'));
    };
    render();
  }
  function rulesSection() { const s = el('section', { id: 'rules', class: 'card', style: 'margin-top:1.5rem' }); s.innerHTML = `<h2>How a case works</h2>
    <ol>
      <li><strong>The cutoff.</strong> Every case is frozen at 09:00 New York time on a stated date. Everything you see was public before that moment. Nothing later is in the packet.</li>
      <li><strong>Your call.</strong> Buy, skip or short, with a size of 5, 10 or 20% of a $100,000 account. Skip is a real choice: cash stays idle, earns nothing, and time still passes.</li>
      <li><strong>The fill.</strong> Your order executes at the opening price of the next regular session after the cutoff, not at the last close shown. The close is a reference only.</li>
      <li><strong>The exit.</strong> You hold for the stated horizon, one, three or five calendar years, and sell at the first opening price on or after the anniversary of your entry. A leap-day entry uses 28 February.</li>
      <li><strong>Costs.</strong> 10 basis points of slippage on each side. Longs receive dividends. Shorts owe dividends and pay a simulated borrow fee of 5% a year on the position's value. There are no taxes, no margin calls and no recalls in this version.</li>
      <li><strong>The benchmark.</strong> Every result is shown next to the S&amp;P 500 ETF (SPY) bought and sold on the same two dates with no costs.</li>
      <li><strong>The reveal.</strong> The company's name, the sources, the price path and the result appear only after you commit. Your commitment is saved in this browser first. You can also look at what the same call would have done over the other horizons; that is context and is never scored.</li>
    </ol>
    <p class="note">Known limits of this version: prices are vendor daily bars, not a verified corporate-action ledger. Company names and tickers are masked, but product names and some figures can still identify a company. The outcome files are separate downloads fetched after you commit; they are not access-controlled, so don't go looking.</p>`; return s; }
  function topbar(current, onRules) {
    const rules = el('a', { href: 'index.html#rules', onclick: onRules ? (e => { e.preventDefault(); onRules(); }) : null }, 'Rules');
    const fb = el('a', { href: 'https://github.com/AnthonyKot/stockgame/issues/new', target: '_blank', rel: 'noopener' }, 'Feedback');
    const t = el('header', { class: 'top' }, el('h1', {}, 'Stockgame'), el('nav', { 'aria-label': 'Main' }, el('a', { href: 'index.html', 'aria-current': current === 'play' ? 'page' : null }, 'Play'), el('a', { href: 'journal.html', 'aria-current': current === 'journal' ? 'page' : null }, 'Journal'), rules, fb));
    const meta = el('div', { class: 'meta' }); const lab = el('label', {}, el('input', { type: 'checkbox', id: 'transparent', checked: transparent() ? '' : null, onchange: e => { setTransparent(e.target.checked); location.reload(); } }), ' Transparent mode (show names before deciding)'); meta.append(lab); t.append(meta);
    return t;
  }
  return { $, el, esc, load, rulesSection, journal, saveJournal, findCommit, upsertCommit, transparent, pct, signed, money, dateFmt, horizonText, badge, prose, lineChart, topbar };
})();
