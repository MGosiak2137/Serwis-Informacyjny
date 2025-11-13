const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function scrape(url = 'https://www.przegladsportowy.pl/') {
  const headlessEnv = process.env.PUPPETEER_HEADLESS;
  const headless = headlessEnv === undefined ? true : !(headlessEnv === '0' || headlessEnv.toLowerCase() === 'false');
  const browser = await puppeteer.launch({ headless, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(30000);

  try {
    console.log('Navigating to', url, 'headless=', headless);
    await page.goto(url, { waitUntil: 'networkidle2' });
    // Delay dla dynamicznego kontentu, zmienic jak nie dziala cos
    await new Promise((resolve) => setTimeout(resolve, 2000));



    const items = await page.evaluate(() => {
      const seen = new Set();
      const out = [];

      const containers = Array.from(document.querySelectorAll('article, [class*="article"], [data-article], [role="article"], .news-item'));
      for (const c of containers) {
        if (out.length >= 50) break;
        try {
          const titleEl = c.querySelector('h1, h2, h3, [class*="title"], [data-testid*="title"]');
          const anchor = c.querySelector('a');
          const summaryEl = c.querySelector('p, [class*="summary"], [class*="excerpt"]');

          const title = titleEl ? titleEl.textContent.trim() : (anchor ? anchor.textContent.trim() : '');
          const link = anchor ? anchor.href : '';
          const summary = summaryEl ? summaryEl.textContent.trim() : '';

          if (title && !seen.has(title)) {
            seen.add(title);
            out.push({ title, link, summary });
          }
        } catch (e) {
        }
      }

      if (out.length === 0) {
        const anchors = Array.from(document.querySelectorAll('a'));
        for (const a of anchors) {
          if (out.length >= 100) break;
          try {
            const href = a.href || '';
            const text = (a.textContent || a.getAttribute('title') || '').trim();
            if (!text || text.length < 10) continue;
            if (/\/(sport|p|artykul|news)\b/i.test(href) || /sport/i.test(text)) {
              if (!seen.has(text)) {
                seen.add(text);
                out.push({ title: text, link: href, summary: '' });
              }
            }
          } catch (e) {}
        }
      }

      return out.slice(0, 100);
    });

    console.log('Collected', items.length, 'candidates');

    const normalized = items.map((it, idx) => ({
      id: idx + 1,
      title: it.title.substring(0, 300),
      summary: (it.summary || '').substring(0, 500),
      published_at: new Date().toISOString(),
      source_name: new URL(url).hostname.replace('www.', ''),
      source_url: it.link || url,
      category: 'sport',
      league: null,
      content: null
    }));

    await browser.close();
    return normalized;
  } catch (err) {
    await browser.close();
    throw err;
  }
}

async function runAndSave(url) {
  const articles = await scrape(url);

  const localPath = path.join(__dirname, 'sport_news_data.json');
  fs.writeFileSync(localPath, JSON.stringify(articles, null, 2), 'utf8');
  console.log('Saved', articles.length, 'articles to', localPath);

  try {
    const rootPath = path.join(__dirname, '..', '..', '..', 'sport_news_data.json');
    fs.writeFileSync(rootPath, JSON.stringify(articles, null, 2), 'utf8');
    console.log('Also saved copy to', rootPath);
  } catch (e) {
    console.warn('Could not write copy to repo root:', e.message);
  }

  return articles;
}

if (require.main === module) {
  const argvUrl = process.argv[2];
  const envUrl = process.env.SPORT_SCRAPE_URL;
  const url = argvUrl || envUrl || 'https://www.przegladsportowy.pl/';
  runAndSave(url).catch(err => {
    console.error('Scraper failed:', err && err.message ? err.message : err);
    process.exit(1);
  });
}

module.exports = { scrape, runAndSave };
