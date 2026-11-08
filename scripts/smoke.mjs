import { chromium } from 'playwright';

const base = new URL(process.argv[2] ?? process.env.SMOKE_URL ?? 'http://127.0.0.1:1313/');
const failures = [];
const check = (ok, message) => {
  if (!ok) failures.push(message);
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${message}`);
};
const sameOrigin = (url) => {
  try {
    return new URL(url).origin === base.origin;
  } catch {
    return false;
  }
};
const ignoredRequest = (url) => /google-analytics|googletagmanager|doubleclick/.test(url);

const browser = await chromium.launch();
const context = await browser.newContext({ serviceWorkers: 'block' });

async function visit(path, { width = 1280, height = 800 } = {}) {
  const page = await context.newPage();
  await page.setViewportSize({ width, height });
  const problems = [];
  page.on('response', (r) => {
    const type = r.request().resourceType();
    if (r.status() >= 400 && !ignoredRequest(r.url()) && (sameOrigin(r.url()) || ['stylesheet', 'script'].includes(type))) {
      problems.push(`${r.status()} ${r.url()}`);
    }
  });
  page.on('requestfailed', (r) => {
    if (!ignoredRequest(r.url()) && (sameOrigin(r.url()) || ['stylesheet', 'script'].includes(r.resourceType()))) {
      problems.push(`failed ${r.url()} (${r.failure()?.errorText})`);
    }
  });
  page.on('pageerror', (e) => problems.push(`page error: ${e.message}`));
  page.on('console', (m) => {
    if (m.type() === 'error' && !ignoredRequest(m.location().url || '')) problems.push(`console: ${m.text()}`);
  });
  const url = new URL(path, base).href;
  const response = await page.goto(url, { waitUntil: 'load' });
  check(response?.status() === 200, `GET ${path} returns 200 (got ${response?.status()})`);
  const title = (await page.title()).trim();
  check(title.length > 0 && !title.endsWith('-'), `${path} has a complete <title> ("${title}")`);
  return { page, problems, url };
}

async function finish({ page, problems }, label) {
  await page.waitForLoadState('networkidle').catch(() => {});
  check(problems.length === 0, `${label}: no broken styles, scripts, same-origin resources or errors ${problems.join(' | ')}`);
  await page.close();
}

try {
  const home = await visit('/');
  const sheets = await home.page.evaluate(() =>
    [...document.styleSheets]
      .filter((s) => s.href && new URL(s.href).origin === location.origin)
      .map((s) => ({ href: new URL(s.href).pathname, rules: s.cssRules.length })),
  );
  const empty = sheets.filter((s) => s.rules === 0).map((s) => s.href);
  const bundles = ['theme', 'site'].filter((name) => sheets.some((s) => new RegExp(`/css/${name}\\.min\\.[0-9a-f]+\\.css$`).test(s.href)));
  check(bundles.length === 2 && empty.length === 0, `theme and site stylesheet bundles are applied (${sheets.map((s) => s.href).join(', ')}${empty.length ? `; empty: ${empty.join(', ')}` : ''})`);
  const navbarHeight = await home.page.$eval('.navbar', (el) => el.getBoundingClientRect().height).catch(() => 0);
  check(navbarHeight >= 40, `Bootstrap styles the navbar (${navbarHeight}px tall)`);
  const menu = await home.page.$$eval('.navbar a', (as) =>
    as.filter((a) => a.offsetParent !== null && a.getBoundingClientRect().width > 0).map((a) => a.textContent.trim().toUpperCase()),
  );
  check(['POSTS', 'SERIES', 'PORTUGUÊS'].every((item) => menu.includes(item)), `desktop menu shows Posts, Series and Português (${menu.join(', ')})`);
  const postLinks = await home.page.$$eval('a[href*="/posts/"]', (as) => [...new Set(as.map((a) => a.href))]);
  check(postLinks.length >= 10, `home lists posts (${postLinks.length} links)`);
  await finish(home, 'home');

  const ptHome = await visit('/pt/');
  check((await ptHome.page.$$('a[href*="/pt/posts/"]')).length >= 10, 'Portuguese home lists posts');
  await finish(ptHome, 'Portuguese home');

  const post = await visit(new URL(postLinks[0]).pathname);
  const words = await post.page.$eval('article', (el) => el.innerText.split(/\s+/).length).catch(() => 0);
  check(words > 100, `latest post renders its article (${words} words)`);
  const images = await post.page.$$eval('article img', (imgs) =>
    imgs.filter((i) => i.loading !== 'lazy').map((i) => ({ src: i.src, ok: i.complete && i.naturalWidth > 0 })),
  );
  check(images.every((i) => i.ok), `post images load ${images.filter((i) => !i.ok).map((i) => i.src).join(', ')}`);
  const translation = await post.page.$eval('a[href*="/pt/posts/"]', (a) => a.getAttribute('href')).catch(() => null);
  check(Boolean(translation), `post links to its Portuguese version (${translation})`);
  await finish(post, 'latest post');

  if (translation) {
    const ptPost = await visit(new URL(translation, base).pathname);
    check(((await ptPost.page.$eval('article', (el) => el.innerText).catch(() => '')) || '').length > 500, 'Portuguese post renders its article');
    await finish(ptPost, 'Portuguese post');
  }

  for (const path of ['/tags/', '/series/', '/index.xml', '/sitemap.xml']) {
    const r = await context.request.get(new URL(path, base).href);
    check(r.status() === 200, `${path} returns 200 (got ${r.status()})`);
  }

  const phone = await visit('/', { width: 390, height: 844 });
  const overflow = await phone.page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  check(overflow <= 0, `no horizontal scroll on a phone-sized screen (overflow ${overflow}px)`);
  await phone.page.click('.navbar-toggle');
  const phoneMenu = await phone.page
    .waitForSelector('#main-navbar a[title="Series"]', { state: 'visible', timeout: 5000 })
    .then(() => true)
    .catch(() => false);
  check(phoneMenu, 'the phone menu opens and shows its links');
  await finish(phone, 'home on a phone');
} finally {
  await browser.close();
}

if (failures.length) {
  console.error(`smoke: ${failures.length} check(s) failed for ${base.href}`);
  process.exit(1);
}
console.log(`smoke: all checks passed for ${base.href}`);
