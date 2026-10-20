// Render brand/icons/src/*.svg and brand/logo/*.svg to the PNG sizes Android, iOS and the stores need.
// Usage: node brand/tools/render_icons.mjs   (needs Playwright with Chromium;
// set PLAYWRIGHT_MODULE to its entry file if it is not installed in this project)
import { readFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const BRAND = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(BRAND, 'icons', 'src');

const DENSITIES = { mdpi: 1, hdpi: 1.5, xhdpi: 2, xxhdpi: 3, xxxhdpi: 4 };
const jobs = [];
const add = (src, out, w, h = w) => jobs.push({ src, out, w, h });

// iOS (single 1024 size, Xcode generates the rest)
add(join(SRC, 'ios.svg'), 'icons/ios/AppIcon-1024.png', 1024);
add(join(SRC, 'ios-dark.svg'), 'icons/ios/AppIcon-1024-dark.png', 1024);
add(join(SRC, 'ios-tinted.svg'), 'icons/ios/AppIcon-1024-tinted.png', 1024);
// Android
for (const [d, k] of Object.entries(DENSITIES)) {
  add(join(SRC, 'android-legacy.svg'), `icons/android/mipmap-${d}/ic_launcher.png`, 48 * k);
  add(join(SRC, 'android-legacy-round.svg'), `icons/android/mipmap-${d}/ic_launcher_round.png`, 48 * k);
  add(join(SRC, 'android-foreground.svg'), `icons/android/mipmap-${d}/ic_launcher_foreground.png`, 108 * k);
  add(join(SRC, 'android-monochrome.svg'), `icons/android/mipmap-${d}/ic_launcher_monochrome.png`, 108 * k);
  add(join(SRC, 'android-notification.svg'), `icons/android/drawable-${d}/ic_stat_himma.png`, 24 * k);
}
add(join(SRC, 'play-store.svg'), 'icons/android/play-store-512.png', 512);
// Logo previews
for (const n of ['mark-on-dark', 'mark-on-light', 'mark-small-on-dark', 'mark-small-on-light', 'mark-mono-black', 'mark-mono-white']) add(join(BRAND, 'logo', `${n}.svg`), `logo/png/${n}-512.png`, 512);
for (const n of ['lockup-horizontal-on-light', 'lockup-horizontal-on-dark', 'lockup-stacked-on-light', 'lockup-stacked-on-dark', 'lockup-horizontal-mono-black']) add(join(BRAND, 'logo', `${n}.svg`), `logo/png/${n}.png`, 0);

const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const page = await browser.newPage();
for (const j of jobs) {
  let svg = readFileSync(j.src, 'utf8');
  let { w, h } = j;
  if (!w) { // lockups: 1200px wide, height from the viewBox ratio
    const [, , vw, vh] = svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
    w = 1200; h = Math.round(1200 * vh / vw);
  }
  svg = svg.replace('<svg ', `<svg width="${w}" height="${h}" `);
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  const out = join(BRAND, j.out);
  mkdirSync(dirname(out), { recursive: true });
  await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  console.log('rendered', j.out, `${w}x${h}`);
}
await browser.close();
