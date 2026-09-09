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
    await page.getByRole('heading', { name: 'Debrief', exact: true }).waitFor();
    await page.reload();
    await page.getByRole('heading', { name: 'Debrief', exact: true }).waitFor();
    await page.goto(base + '/play.html?case=5d6cb2d76f');
    await page.locator('#ticket form').waitFor();
    await page.locator('[name=action][value=skip]').check();
    await page.getByRole('button', { name: 'Commit and reveal' }).click();
    await page.getByRole('heading', { name: 'Debrief', exact: true }).waitFor();
    await page.goto(base + '/journal.html');
    const rows = await page.locator('#tbl tbody tr').allTextContents();
    assert(rows.some(t => t.includes('Nektar Therapeutics (NKTR)') && !t.includes('a biopharmaceutical company')));
    const skip = page.locator('#tbl tbody tr').filter({ hasText: 'No position' });
    assert.equal(await skip.locator('td').nth(6).innerText(), '—');
    assert.deepEqual(errors, []);
    console.log('story UI: resume, completion, storage failure, optional reason and journal checks passed');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
