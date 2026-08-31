/* Width/layout audit for the CEH Diploma site.
 *   node scripts/audit_layout.js              # all four checks, six widths
 *   BREAK=padding node scripts/audit_layout.js  # sabotage one check on purpose
 *
 * Asserts, at EVERY width:
 *   1. every .wrap has the same left edge      (catches a cancelled container)
 *   2. every .wrap has paddingLeft >= 14px     (catches the padding-shorthand trap)
 *   3. no cell of >55 chars renders < 190px    (catches a squeezed prose column)
 *   4. no document h-scroll, nothing outside a scroll container
 *
 * 1920 is NOT optional: with a 1680px container cap, a rule that cancels the
 * container is invisible at 1400. That is exactly where the bug hides.
 *
 * BREAK values (each MUST fail — a check that has never failed proves nothing):
 *   edges · padding · nocolgroup · overflow · minwidth · tablemw
 * Note `cells` alone PASSES, because the per-table <colgroup> overrides
 * td:last-child{width:1%} — which is the point of having one.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const ROOT = process.env.DOCS || path.join(__dirname, '..', 'docs');
const PAGES = ['index.html', ...fs.readdirSync(ROOT)
  .filter(d => /^session-\d+$/.test(d) && fs.existsSync(path.join(ROOT, d, 'index.html')))
  .sort().map(d => `${d}/index.html`)];
const WIDTHS = [1920,1400,1100,900,700,480];
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const BREAK = process.env.BREAK || '';

const AUDIT = () => {
  const out = {edges:[], padding:[], cells:[], overflow:[], docScroll:null};
  const near = (a,b)=>Math.abs(a-b) < 1.5;
  const wraps = [...document.querySelectorAll('.wrap')].filter(el => el.offsetParent !== null || el.getClientRects().length);
  const lefts = wraps.map(el => ({sel: el.className, left: +el.getBoundingClientRect().left.toFixed(1),
                                  pl: parseFloat(getComputedStyle(el).paddingLeft)}));
  if (lefts.length) {
    const ref = lefts[0].left;
    out.edges = lefts.filter(o => !near(o.left, ref)).map(o => `${o.sel} left=${o.left} != ${ref}`);
    out.padding = lefts.filter(o => !(o.pl >= 14)).map(o => `${o.sel} paddingLeft=${o.pl}`);
  }
  for (const td of document.querySelectorAll('td,th')) {
    const txt = (td.innerText||'').trim();
    if (txt.length <= 55) continue;
    const w = td.getBoundingClientRect().width;
    if (w > 0 && w < 190) out.cells.push(`${txt.slice(0,42).replace(/\s+/g,' ')}… w=${w.toFixed(0)} chars=${txt.length}`);
  }
  out.docScroll = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  const vw = document.documentElement.clientWidth;
  const scrolls = el => { const s = getComputedStyle(el); return s.overflowX === 'auto' || s.overflowX === 'scroll'; };
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right <= vw + 1 && r.left >= -1) continue;
    let p = el.parentElement, guarded = false;
    while (p && p !== document.body) { if (scrolls(p)) { guarded = true; break; } p = p.parentElement; }
    if (!guarded) out.overflow.push(`${el.tagName}.${(el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className||'').toString().split(' ')[0]} L=${r.left.toFixed(0)} R=${r.right.toFixed(0)} vw=${vw}`);
  }
  out.overflow = [...new Set(out.overflow)].slice(0,6);
  return out;
};

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  let fails = 0, checks = 0;
  for (const p of PAGES) {
    for (const w of WIDTHS) {
      const ctx = await browser.newContext({ viewport: { width: w, height: 1000 } });  // `viewport`, NOT `viewportSize`
      const page = await ctx.newPage();
      await page.goto('file://' + path.join(ROOT, p), { waitUntil: 'load' });
      await page.addStyleTag({ content: '.page{display:block!important}' });  // one pass covers every paged section
      if (BREAK === 'edges')    await page.addStyleTag({content:'main.wrap{max-width:1100px}'});
      if (BREAK === 'padding')  await page.addStyleTag({content:'.section{padding:48px 0}'});
      if (BREAK === 'cells')    await page.addStyleTag({content:'.content table{table-layout:auto}.content td:last-child{width:1%}'});
      if (BREAK === 'minwidth') await page.addStyleTag({content:'.split>*,.grid>*,.tiles>*{min-width:auto}'});
      if (BREAK === 'tablemw')  await page.addStyleTag({content:'.tbl-scroll table{min-width:0}'});
      if (BREAK === 'overflow') await page.addStyleTag({content:'.tbl-scroll{overflow-x:visible}'});
      if (BREAK === 'nocolgroup') {
        await page.evaluate(() => document.querySelectorAll('colgroup').forEach(c => c.remove()));
        await page.addStyleTag({content:'.content table{table-layout:auto}.content td:last-child{width:1%}'});
      }
      await page.waitForTimeout(140);
      const r = await page.evaluate(AUDIT);
      const bad = [];
      if (r.edges.length)    bad.push(`EDGES(${r.edges.length}): ${r.edges[0]}`);
      if (r.padding.length)  bad.push(`PADDING(${r.padding.length}): ${r.padding[0]}`);
      if (r.cells.length)    bad.push(`CELLS(${r.cells.length}): ${r.cells[0]}`);
      if (r.docScroll > 1)   bad.push(`DOC-SCROLL: +${r.docScroll}px`);
      if (r.overflow.length) bad.push(`OUTSIDE(${r.overflow.length}): ${r.overflow[0]}`);
      checks++;
      if (bad.length) { fails++; console.log(`FAIL ${p} @${w}\n      ` + bad.join('\n      ')); }
      else console.log(`ok   ${p} @${w}`);
      await ctx.close();
    }
  }
  await browser.close();
  console.log(`\n${BREAK ? '[BREAK='+BREAK+'] ' : ''}${checks - fails}/${checks} passed`);
  process.exit(fails ? 1 : 0);
})();
