// Optional browser smoke test: npm install --no-save playwright
// Run: node verify-diagrams.cjs [customer-journey URL]
const assert = require('node:assert/strict');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}),
  });
  try {
    const page = await browser.newPage();
    await page.goto(process.argv[2] || 'https://devdogfish.github.io/cityhelpers/customer-journey.html');
    await page.locator('.mermaid svg .node').first().waitFor({ timeout: 20000 });
    assert.equal(await page.locator('code.language-mermaid, .language-mermaid code').count(), 0,
      'Mermaid source was left unrendered');
    assert.equal(await page.locator('.mermaid svg').count(), 1);
    assert.ok(await page.locator('.mermaid svg .node').count() > 0);
    console.log('Verified customer journey renders as an SVG diagram.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
