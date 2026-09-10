// Serve site/ first. Requires Playwright (or PLAYWRIGHT_MODULE) and optionally CHROMIUM_PATH.
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  try {
    const page = await browser.newPage();
    const base = process.env.STOCKGAME_URL || 'http://127.0.0.1:8765';
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.goto(base + '/play.html?case=146743bdc9');
    await page.locator('#ticket form').waitFor();
    assert.equal(await page.locator('#ticket details').getAttribute('open'), null);
    assert.equal(await page.locator('[name=reason]').getAttribute('required'), null);
    await page.locator('[name=action][value=buy]').check();
    await page.locator('[name=assume]').first().check();
    await page.getByRole('button', { name: 'Commit and reveal' }).click();
    await page.getByRole('button', { name: /Walk through what happened/ }).click();
    await page.reload();
    await page.getByRole('heading', { name: /^Stop 1 of/ }).waitFor();
    assert.match(await page.locator('#debrief').innerText(), /Your decision depended on/);
    await page.evaluate(() => { window.originalSetItem = Storage.prototype.setItem; Storage.prototype.setItem = () => { throw Error('blocked'); }; });
    await page.getByRole('button', { name: 'Weakens', exact: true }).click();
    await page.locator('.walk-error').waitFor();
    assert.match(await page.locator('#debrief h2').innerText(), /^Stop 1/);
    await page.evaluate(() => { Storage.prototype.setItem = window.originalSetItem; });
    await page.getByRole('button', { name: 'Weakens', exact: true }).click();
    await page.reload();
    await page.getByRole('heading', { name: /^Stop 2 of/ }).waitFor();
    assert.equal(await page.locator('#debrief').getByText('Debrief', { exact: true }).count(), 0);
    await page.getByRole('button', { name: 'Unresolved', exact: true }).click();
    await page.getByRole('button', { name: 'Weakens', exact: true }).click();
    await page.getByRole('heading', { name: /^Stop 4 of/ }).waitFor();
    await page.getByRole('button', { name: 'Unresolved', exact: true }).click();
    await page.getByRole('heading', { name: 'Debrief', exact: true }).waitFor();
    await page.reload();
    await page.getByRole('heading', { name: 'Debrief', exact: true }).waitFor();
    await page.goto(base + '/play.html?case=5d6cb2d76f');
    await page.locator('#ticket form').waitFor();
    await page.locator('[name=action][value=skip]').check();
    await page.locator('[name=assume]').first().check();
    await page.getByRole('button', { name: 'Commit and reveal' }).click();
    await page.getByRole('button', { name: 'Show the result', exact: true }).click();
    await page.getByRole('heading', { name: 'Debrief', exact: true }).waitFor();
    await page.goto(base + '/journal.html');
    const rows = await page.locator('#tbl tbody tr').allTextContents();
    assert(rows.some(t => t.includes('Nektar Therapeutics (NKTR)') && !t.includes('a biopharmaceutical company')));
    const skip = page.locator('#tbl tbody tr').filter({ hasText: 'No position' });
    assert.equal(await skip.locator('td').nth(6).innerText(), '—');
    for (const cfg of [
      { years: 1, width: 1280, action: 'buy', stops: 1, verdict: 'Weakened' },
      { years: 3, width: 390, action: 'buy', stops: 2, verdict: 'Mixed' },
      { years: 5, width: 1280, action: 'buy', stops: 4, verdict: 'Not supported' },
      { years: 5, width: 390, action: 'buy', stop: '20', stops: 1, verdict: 'Weakened' },
      { years: 5, width: 1280, action: 'short', tp: '50', stops: 1, verdict: 'Weakened' },
      { years: 1, width: 390, action: 'skip', stops: 1, verdict: 'Weakened' }
    ]) {
      const p = await browser.newPage({ viewport: { width: cfg.width, height: 844 } });
      p.on('pageerror', e => errors.push(e.message));
      const futureRequests = [];
      p.on('request', r => { if (/outcome.json|reveal.json/.test(r.url())) futureRequests.push(r.url()); });
      await p.goto(base + '/');
      await p.locator('a[href="play.html?case=146743bdc9"]').click();
      await p.locator('#ticket form').waitFor();
      await p.locator('[name=action][value=' + cfg.action + ']').check();
      await p.locator('[name=assume][value=a1]').check();
      await p.locator('[name=years][value="' + cfg.years + '"]').check();
      if (cfg.stop || cfg.tp) {
        await p.locator('#ticket summary').click();
        if (cfg.stop) await p.locator('[name=stop]').selectOption(cfg.stop);
        if (cfg.tp) await p.locator('[name=tp]').selectOption(cfg.tp);
      }
      assert.equal(futureRequests.length, 0);
      if (cfg.years === 1 && cfg.action === 'buy') {
        await p.evaluate(() => { window.originalSetItem = Storage.prototype.setItem; Storage.prototype.setItem = () => { throw Error('blocked'); }; });
        await p.getByRole('button', { name: 'Commit and reveal' }).click();
        await p.locator('#ticket .err').waitFor();
        assert.equal(futureRequests.length, 0);
        await p.evaluate(() => { Storage.prototype.setItem = window.originalSetItem; });
      }
      await p.getByRole('button', { name: 'Commit and reveal' }).click();
      await p.getByRole('button', { name: /Walk through what happened/ }).click();
      for (let i = 1; i <= cfg.stops; i++) {
        const heading = p.getByRole('heading', { name: new RegExp('^Stop ' + i + ' of ' + cfg.stops) });
        await heading.waitFor();
        if (i === 1 || i === 2) { await p.reload(); await heading.waitFor(); }
        await p.getByRole('button', { name: 'Unresolved', exact: true }).click();
      }
      await p.getByRole('heading', { name: 'Debrief', exact: true }).waitFor();
      await p.reload();
      await p.getByRole('heading', { name: 'Debrief', exact: true }).waitFor();
      assert.match(await p.locator('.thesis-check').innerText(), new RegExp(cfg.verdict));
      assert.equal(await p.locator('.later-context').getAttribute('open'), null);
      const visible = await p.locator('#debrief').innerText();
      if (cfg.stops < 4) assert(!/March 2022|Mar 2022|Apr 2022/.test(visible));
      if (cfg.stops === 1) assert(!visible.includes('53%'));
      const saved = await p.evaluate(() => JSON.parse(localStorage.getItem('stockgame.journal.v1'))[0]);
      assert.equal(saved.walkthrough.length, cfg.stops);
      assert(saved.walkthrough.every(w => w.date < saved.result.exit_date));
      if (cfg.stop) assert.equal(saved.result.exit_date, '2018-06-05');
      if (cfg.tp) assert.equal(saved.result.exit_date, '2018-10-23');
      await p.locator('.later-context > summary').click();
      assert.match(await p.locator('.later-context').innerText(), /March 2022|Mar 2022/);
      assert.equal(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      await p.close();
    }
    assert.deepEqual(errors, []);
    console.log('story UI: horizon/exit boundaries, desktop/mobile, reload, storage failure and journal checks passed');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
