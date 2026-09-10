// Browser journey for the campaign prototype: fresh storage, three decisions, reload mid-run, closures with reveal,
// final report; no page errors. Serve site/ first; requires Playwright (or PLAYWRIGHT_MODULE) and optionally CHROMIUM_PATH.
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  try {
    const base = process.env.STOCKGAME_URL || 'http://127.0.0.1:8765';
    for (const width of [1280, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } }); const errors = []; page.on('pageerror', e => errors.push(e.message));
      const requested = []; page.on('request', r => { const u = r.url(); if (/campaigns\/|outcome\.json|reveal\.json/.test(u)) requested.push(u.replace(base, '')); });
      await page.goto(base + '/campaign.html'); await page.locator('#strip h2').waitFor();
      assert.match(await page.locator('#strip').innerText(), /15 Feb 2018, before the open[\s\S]*\$109,495[\s\S]*\$100,000[\s\S]*14 Feb 2018/);
      await page.locator('.scene-frame').waitFor(); assert.equal(await page.frameLocator('.scene-frame').locator('.scene').count(), 1);
      const early = requested.filter(u => /upto-/.test(u)); assert(early.length >= 4 && early.every(u => /upto-2018-02-14\.json$/.test(u)), 'first screen must request only slices up to 14 Feb 2018: ' + early.join(', '));
      assert.equal(await page.frameLocator('.scene-frame').locator('#ticket').count(), 0, 'embedded case page must not show its own ticket');
      if (width === 390) { const jump = page.locator('button.primary.jump'); assert(await jump.isVisible(), 'mobile Decide jump visible'); assert.match(await page.locator('#stage .card .note').first().innerText(), /decision panel is below/); await jump.click(); await page.waitForTimeout(500); }
      else assert.match(await page.locator('#stage .card .note').first().innerText(), /decide on the right/);
      const decide = async (action, size, years) => { await page.locator('.campaign-ticket [name=action][value=' + action + ']').check(); if (action === 'buy') { await page.locator('.campaign-ticket [name=years][value="' + years + '"]').check(); await page.locator('.campaign-ticket [name=size][value="' + size + '"]').check(); await page.locator('.campaign-ticket [name=assume]').first().check(); } await page.getByRole('button', { name: 'Lock in my decision' }).click(); await page.locator('#stage button.primary').waitFor(); };
      await page.locator('.campaign-ticket [name=action][value=buy]').check(); await page.locator('.campaign-ticket [name=size][value="20"]').check();
      assert.match(await page.locator('.budget').innerText(), /20% of \$109,495 equity is \$21,899/);
      await page.getByRole('button', { name: 'Lock in my decision' }).click(); assert.match(await page.locator('.campaign-ticket .err').innerText(), /one or two assumptions/);
      await decide('buy', 10, 5);
      await page.getByRole('button', { name: /Advance to story 2/ }).click(); await page.locator('.scene-frame').waitFor();
      assert.match(await page.locator('#since').innerText(), /bought 126\.91 shares[\s\S]*Bitcoin moved/);
      assert.match(await page.locator('#strip').innerText(), /13 Nov 2018[\s\S]*Open positions[\s\S]*story 1[\s\S]*closes 15 Feb 2023/);
      assert.doesNotMatch(await page.locator('#strip').innerText(), /Nektar|NKTR/, 'identity stays masked while open');
      await page.reload(); await page.locator('.scene-frame').waitFor(); assert.match(await page.locator('#strip h2').innerText(), /13 Nov 2018/);
      await decide('skip'); await page.getByRole('button', { name: /Advance to story 3/ }).click(); await page.locator('.scene-frame').waitFor();
      await decide('buy', 20, 3);
      await page.getByRole('button', { name: /next closing trade on 18 Jan 2022/ }).click(); await page.locator('#stage h3').first().waitFor();
      assert.match(await page.locator('#stage').innerText(), /Closed on 18 Jan 2022: story 3 was JPMorgan[\s\S]*dividends/);
      assert.match(await page.locator('#since').innerText(), /closed for[\s\S]*dividend payments received/);
      await page.getByRole('button', { name: /next closing trade on 15 Feb 2023/ }).click(); await page.locator('#stage h2:has-text("Final report")').waitFor();
      const rep = await page.locator('#stage').innerText();
      assert.match(rep, /story 1 was Nektar Therapeutics[\s\S]*-96\.5%[\s\S]*Final report[\s\S]*Your calls[\s\S]*Bitcoin, untouched[\s\S]*Do-nothing baseline/);
      assert.match(rep, /62\.6%/); assert.doesNotMatch(rep, /0000000/);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth), true, 'no horizontal overflow at ' + width);
      assert(!requested.some(u => /outcome\.json|reveal\.json/.test(u)), 'the campaign page must never fetch outcome or reveal files: ' + requested.filter(u => /outcome|reveal/.test(u)).join(', '));
      assert(!requested.some(u => /upto-2023-11-13|upto-2024-01-16/.test(u)), 'slices beyond the last closure must not be fetched');
      assert.deepEqual(errors, []); await page.evaluate(() => localStorage.clear()); await page.close();
    }
    console.log('campaign UI: fresh start, budgets, validation, three decisions, reload, masked strip, closures with reveal, final report at 1280 and 390 passed');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exit(1); });
