// Integration check for the content session's valuation framing and disclosure behavior.
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {})});
  const base = process.env.STOCKGAME_URL || 'http://127.0.0.1:8765';
  const cases = [
    {id:'146743bdc9', pipeline:true, ratio:'1.2%', years:1},
    {id:'fba30037c0', pipeline:true, ratio:'0.9%', years:1},
    {id:'b126872cae', pipeline:true, ratio:'16.8%', years:1},
    {id:'050a03b08f', pipeline:false, years:3}
  ];
  try {
    for (const width of [1280,390]) for (const c of cases) {
      const page = await browser.newPage({viewport:{width,height:900}});
      const errors = []; page.on('pageerror', e=>errors.push(e.message));
      const future = []; page.on('request', r=>{if (/outcome.json|reveal.json/.test(r.url())) future.push(r.url());});
      await page.goto(base + '/');
      await page.locator(`a[href="play.html?case=${c.id}"]`).click();
      const snapshot = page.locator('.financial-snapshot');
      await snapshot.waitFor();
      const headings = await page.locator('#main > section > h2').allTextContents();
      const position = name=>headings.findIndex(h=>h.startsWith(name));
      assert(['Market snapshot','Where the stock stands','What changed','Financial snapshot'].every(name=>position(name)>=0));
      assert(position('Market snapshot') < position('Where the stock stands'));
      assert(position('What changed') < position('Financial snapshot'));
      const panel = page.locator('.snapshot-price');
      const visible = await panel.innerText();
      if (c.pipeline) {
        assert.match(visible,/What the market pays for the pipeline/);
        assert.match(visible,/Net cash \/ market cap/);
        assert(visible.includes(c.ratio));
        assert(!visible.includes('EV / annual revenue'));
      } else assert.match(visible,/EV \/ annual revenue/);
      if (c.id === '146743bdc9') {
        assert.match(visible,/closing expected in the second quarter of 2018/);
        await panel.getByText('Valuation inputs and caveats',{exact:true}).focus();
        await page.keyboard.press('Enter');
        const expanded = await panel.innerText();
        assert.match(expanded,/78\.7×/);
        assert.match(expanded,/156\.9 m shares/);
        assert(!expanded.includes('shares: $'));
        await page.keyboard.press('Enter');
      }
      assert.equal(future.length,0);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false, JSON.stringify({case:c.id,width,overflow:await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,70),right:e.getBoundingClientRect().right})).slice(-15))}));
      await page.locator('[name=action][value=buy]').check();
      await page.locator('[name=assume][value=a1]').check();
      await page.locator(`[name=years][value="${c.years}"]`).check();
      await page.getByRole('button',{name:'Commit and reveal',exact:true}).click();
      const gate = page.getByRole('button',{name:'Show the result',exact:true});
      const debrief = page.getByRole('heading',{name:'Debrief',exact:true});
      await gate.or(debrief).first().waitFor();
      if (await gate.isVisible()) await gate.click();
      await page.getByRole('heading',{name:'Debrief',exact:true}).waitFor();
      await page.reload();
      await page.getByRole('heading',{name:'Debrief',exact:true}).waitFor();
      assert.equal(await page.locator('.later-context').getAttribute('open'),null);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false, JSON.stringify({case:c.id,width,overflow:await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,70),right:e.getBoundingClientRect().right})).slice(-15))}));
      assert.deepEqual(errors,[]);
      await page.close();
    }
    console.log('presentation UI: Nektar/Axsome/Madrigal/Target desktop/mobile framing, source units, commit and reload passed');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
