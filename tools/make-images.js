// Renders raster brand assets from the SVG sources using Playwright's Chromium.
// Usage: node tools/make-images.js, then build favicon.ico with ImageMagick (see docs/DEPLOYMENT.md).
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

const IMG = path.resolve(__dirname, '..', 'site', 'assets', 'images');
const FONT = path.resolve(__dirname, '..', 'site', 'assets', 'fonts', 'barlow-condensed-700.woff2');
const logo = 'file://' + path.join(IMG, 'cherry-logo.svg');
const hero = 'file://' + path.join(IMG, 'cherry-hero.svg');

const iconPage = (size, pad, bg) => `<!doctype html><html><body style="margin:0;background:${bg}">
  <div style="width:${size}px;height:${size}px;display:grid;place-items:center">
    <img src="${logo}" style="width:${size - pad * 2}px;height:${size - pad * 2}px">
  </div></body></html>`;

const socialPage = `<!doctype html><html><head><style>
  @font-face { font-family: BC; src: url("file://${FONT}") format("woff2"); font-weight: 700; }
  body { margin: 0; }
  .card { width: 1200px; height: 630px; position: relative; overflow: hidden;
    background: linear-gradient(135deg, #ffffff 0%, #ffffff 48%, #FFF0F6 100%); font-family: BC, sans-serif; }
  .bar { position: absolute; left: 0; top: 0; bottom: 0; width: 18px; background: #FF4693; }
  .copy { position: absolute; left: 90px; top: 110px; width: 600px; }
  .brand { display: flex; align-items: center; gap: 22px; }
  .brand img { width: 120px; height: 120px; }
  .name { font-size: 84px; line-height: .95; color: #26232A; }
  .name span { color: #C2185B; }
  .tag { margin-top: 44px; font-size: 54px; line-height: 1.08; color: #26232A; }
  .tag span { color: #C2185B; }
  .url { margin-top: 40px; font-family: system-ui, sans-serif; font-size: 28px; color: #625B66; font-weight: 600; }
  .art { position: absolute; right: 10px; top: 0; width: 520px; height: 585px; }
</style></head><body><div class="card"><div class="bar"></div>
  <div class="copy">
    <div class="brand"><img src="${logo}"><div class="name">Cherry App<br><span>Agency</span></div></div>
    <div class="tag">Host &amp; agency<br><span>registration guide</span></div>
    <div class="url">cherryappagency.com</div>
  </div>
  <img class="art" src="${hero}">
</div></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const shoot = async (html, w, h, file, transparent) => {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    // Loading from a file:// page lets the local SVG and font URLs resolve.
    const tmp = path.join(os.tmpdir(), 'cherry-render-' + file + '.html');
    fs.writeFileSync(tmp, html);
    await page.goto('file://' + tmp, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(IMG, file), omitBackground: transparent });
    await page.close();
    fs.unlinkSync(tmp);
    console.log('wrote', file);
  };
  await shoot(iconPage(512, 0, 'transparent'), 512, 512, 'cherry-logo.png', true);
  await shoot(iconPage(512, 56, '#ffffff'), 512, 512, 'icon-512.png', false);
  await shoot(iconPage(192, 20, '#ffffff'), 192, 192, 'icon-192.png', false);
  await shoot(iconPage(180, 18, '#ffffff'), 180, 180, 'apple-touch-icon.png', false);
  await shoot(iconPage(64, 0, 'transparent'), 64, 64, 'favicon-64.png', true);
  await shoot(socialPage, 1200, 630, 'cherry-social-preview.png', false);
  await browser.close();
})();
