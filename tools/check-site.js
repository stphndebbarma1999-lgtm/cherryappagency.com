// Automated checks for the built site. Start the preview server first:
//   python3 tools/serve.py 8765 &   then   node tools/check-site.js http://127.0.0.1:8765
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const BASE = (process.argv[2] || 'http://127.0.0.1:8765').replace(/\/$/, '');
const DOMAIN = 'https://cherryappagency.com';
const PAGES = ['/', '/cherry-agency/', '/cherry-app/', '/cherry-host/', '/cherry-earnings/',
  '/cherry-withdrawal/', '/cherry-policy/', '/about/', '/contact/'];
const WIDTHS = [360, 390, 768, 1024, 1280];
const WA = {
  host: 'https://wa.me/919233262700?text=Hi%2C%20I%20want%20information%20about%20joining%20Cherry%20App%20as%20a%20host.',
  agency: 'https://wa.me/919233262700?text=Hi%2C%20I%20want%20information%20about%20Cherry%20agency%20registration.',
  general: 'https://wa.me/919233262700?text=Hi%2C%20I%20have%20a%20question%20about%20Cherry%20App.',
};

let failures = 0;
const fail = (msg) => { failures++; console.log('FAIL', msg); };
const pass = (msg) => console.log('ok  ', msg);
const check = (cond, msg) => (cond ? pass(msg) : fail(msg));

(async () => {
  const browser = await chromium.launch();
  const titles = new Set();
  const descriptions = new Set();
  const internal = new Set();

  for (const p of PAGES) {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const res = await page.goto(BASE + p, { waitUntil: 'networkidle' });
    check(res.status() === 200, `${p} returns 200`);
    // Scroll to the end so lazy-loaded images (footer logo) are fetched before checking them.
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(300);
    const info = await page.evaluate(() => ({
      h1: document.querySelectorAll('h1').length,
      title: document.title,
      desc: document.querySelector('meta[name="description"]')?.content,
      canonical: document.querySelector('link[rel="canonical"]')?.href,
      ogUrl: document.querySelector('meta[property="og:url"]')?.content,
      hrefs: [...document.querySelectorAll('a')].map((a) => a.getAttribute('href')),
      buttonsWithoutHref: [...document.querySelectorAll('a.btn')].filter((a) => !a.getAttribute('href')).length,
      brokenImgs: [...document.images].filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.src),
      float: document.querySelector('.wa-float')?.getAttribute('href'),
      ld: [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => { try { JSON.parse(s.textContent); return true; } catch (e) { return false; } }),
      lorem: /lorem ipsum|TODO|placeholder text/i.test(document.body.innerText),
    }));
    check(info.h1 === 1, `${p} has exactly one h1`);
    check(!titles.has(info.title), `${p} title unique: ${info.title}`);
    titles.add(info.title);
    check(info.desc && !descriptions.has(info.desc), `${p} description unique`);
    descriptions.add(info.desc);
    check(info.canonical === DOMAIN + p && info.ogUrl === DOMAIN + p, `${p} canonical/og:url self-referencing`);
    check(!info.hrefs.some((h) => h === '#' || h === '' || h === null || /^javascript:/i.test(h)), `${p} no dummy/empty hrefs`);
    check(info.buttonsWithoutHref === 0, `${p} all buttons-as-links have hrefs`);
    check(info.brokenImgs.length === 0, `${p} all images load ${info.brokenImgs.join(' ')}`);
    check(info.ld.length > 0 && info.ld.every(Boolean), `${p} JSON-LD parses`);
    check(!info.lorem, `${p} no placeholder text`);
    const expectedFloat = p === '/cherry-host/' ? WA.host : p === '/cherry-agency/' ? WA.agency : WA.general;
    check(info.float === expectedFloat, `${p} floating WhatsApp uses the right message`);
    for (const h of info.hrefs) {
      if (h.startsWith('https://wa.me/')) {
        check(Object.values(WA).includes(h), `${p} WhatsApp link is one of the three approved URLs`);
      } else if (h.startsWith('/')) {
        internal.add(h.split('#')[0]);
      } else if (!h.startsWith('#')) {
        fail(`${p} unexpected external link ${h}`);
      }
    }
    for (const w of WIDTHS) {
      await page.setViewportSize({ width: w, height: 900 });
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      check(overflow <= 0, `${p} @${w}px no horizontal overflow (${overflow})`);
    }
    await page.close();
  }

  // Every internal link target resolves.
  for (const href of internal) {
    const r = await (await browser.newContext()).request.get(BASE + href, { maxRedirects: 0 });
    check(r.status() === 200, `internal link ${href} -> ${r.status()}`);
  }

  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

  // Homepage hero: exactly two CTAs to the internal guides.
  await page.goto(BASE + '/');
  const hero = await page.$$eval('.hero a.btn', (as) => as.map((a) => [a.textContent.trim(), a.getAttribute('href')]));
  check(JSON.stringify(hero) === JSON.stringify([['Join as a Host', '/cherry-host/'], ['Join as an Agency', '/cherry-agency/']]),
    `homepage hero CTAs ${JSON.stringify(hero)}`);
  await page.click('.hero a.btn >> text=Join as a Host');
  check(page.url() === BASE + '/cherry-host/', 'clicking Join as a Host opens /cherry-host/');
  await page.goto(BASE + '/');
  await page.click('.hero a.btn >> text=Join as an Agency');
  check(page.url() === BASE + '/cherry-agency/', 'clicking Join as an Agency opens /cherry-agency/');

  // Contextual enquiry buttons.
  await page.goto(BASE + '/cherry-host/');
  const hostBtns = await page.$$eval('a.btn', (as) => as.filter((a) => a.textContent.includes('Enquire About Host Registration')).map((a) => a.href));
  check(hostBtns.length >= 1 && hostBtns.every((h) => h === WA.host), `host enquiry buttons (${hostBtns.length}) use host message`);
  await page.goto(BASE + '/cherry-agency/');
  const agencyBtns = await page.$$eval('a.btn', (as) => as.filter((a) => a.textContent.includes('Enquire About Agency Registration')).map((a) => a.href));
  check(agencyBtns.length >= 1 && agencyBtns.every((h) => h === WA.agency), `agency enquiry buttons (${agencyBtns.length}) use agency message`);
  const tiers = await page.$$eval('#agency-tier-caption ~ tbody tr', (rows) => rows.map((r) => r.innerText.replace(/\s+/g, ' ').trim()));
  check(JSON.stringify(tiers) === JSON.stringify(['Level A $300+ 15%', 'Level B $600+ 18%', 'Level C $1,000+ 20%',
    'Level D $2,000+ 25%', 'Level E $5,000+ 35%', 'Level F $10,000+ 40%']), 'agency commission table matches the supplied tiers');

  // Converter.
  await page.goto(BASE + '/cherry-earnings/');
  await page.fill('#diamonds', '250,000');
  let out = await page.textContent('#converter-result');
  check(out.includes('$25.00') && out.includes('above'), `converter 250,000 -> ${out.slice(0, 60)}`);
  await page.fill('#diamonds', '1000');
  out = await page.textContent('#converter-result');
  check(out.includes('$0.10') && out.includes('below'), 'converter 1,000 -> $0.10, below minimum');
  await page.fill('#diamonds', '-5');
  check((await page.getAttribute('#diamonds', 'aria-invalid')) === 'true', 'converter rejects negative input');
  await page.fill('#diamonds', 'abc');
  check((await page.textContent('#converter-result')).includes('whole number'), 'converter rejects text input');

  // Keyboard: skip link and mobile menu.
  const m = await browser.newPage({ viewport: { width: 360, height: 740 } });
  await m.goto(BASE + '/cherry-policy/');
  await m.keyboard.press('Tab');
  check(await m.evaluate(() => document.activeElement.classList.contains('skip-link')), 'first Tab focuses skip link');
  await m.keyboard.press('Tab');
  await m.keyboard.press('Tab');
  check(await m.evaluate(() => document.activeElement.classList.contains('nav-toggle')), 'Tab reaches menu toggle');
  check(!(await m.isVisible('#site-nav a[href="/contact/"]')), 'mobile nav collapsed by default');
  await m.keyboard.press('Enter');
  check(await m.isVisible('#site-nav a[href="/contact/"]'), 'Enter opens mobile nav');
  await m.keyboard.press('Escape');
  check(!(await m.isVisible('#site-nav a[href="/contact/"]')), 'Escape closes mobile nav');

  // Content without JavaScript.
  const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 360, height: 740 } });
  const n = await noJs.newPage();
  await n.goto(BASE + '/cherry-agency/');
  check(await n.isVisible('#site-nav a[href="/contact/"]'), 'without JS the nav links are visible');
  check((await n.textContent('main')).includes('Level F'), 'without JS the commission table is present');

  // 404.
  const r404 = await page.goto(BASE + '/does-not-exist/');
  check(r404.status() === 404 && (await page.textContent('h1')) === 'Page not found', '404 page returns 404 status');

  // Sitemap matches the canonical pages.
  const sm = fs.readFileSync(path.join(__dirname, '..', 'site', 'sitemap.xml'), 'utf8');
  const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((x) => x[1]);
  check(JSON.stringify(locs.sort()) === JSON.stringify(PAGES.map((p) => DOMAIN + p).sort()), 'sitemap lists exactly the canonical pages');

  await browser.close();
  console.log(failures ? `\n${failures} check(s) failed` : '\nAll checks passed');
  process.exit(failures ? 1 : 0);
})();
