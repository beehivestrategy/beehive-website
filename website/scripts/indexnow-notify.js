#!/usr/bin/env node

/**
 * IndexNow Notification Script for Beehive Strategy
 *
 * Reads URLs from the local sitemap files and submits them to the
 * IndexNow API in batches of up to 10,000 URLs per request.
 *
 * Usage:
 *   node scripts/indexnow-notify.js
 *
 * The script looks for sitemap files in the website root:
 *   - sitemap-index.xml (primary)
 *   - sitemap.xml (fallback)
 *
 * IndexNow key file: b5e7a3f1c9d248e6a0b7f4e2d8c1a5b9.txt
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const INDEXNOW_KEY = 'b5e7a3f1c9d248e6a0b7f4e2d8c1a5b9';
const INDEXNOW_ENDPOINT = 'https://api.indexnow.org/IndexNow';
const HOST = 'beehivestrategy.com';
const BATCH_SIZE = 10000; // Max URLs per IndexNow request

// Paths relative to this script's location (website root)
const SCRIPT_DIR = __dirname;
const SITE_ROOT = path.resolve(SCRIPT_DIR, '..');
const SITEMAP_FILES = [
  path.join(SITE_ROOT, 'sitemap-index.xml'),
  path.join(SITE_ROOT, 'sitemap.xml'),
];

// ---------------------------------------------------------------------------
// Sitemap Parsing
// ---------------------------------------------------------------------------

/**
 * Extract all <loc> URLs from an XML string.
 * Handles both <urlset> sitemaps and <sitemapindex> files.
 */
function extractLocs(xmlContent) {
  const locRegex = /<loc>([^<]+)<\/loc>/gi;
  const urls = [];
  let match;
  while ((match = locRegex.exec(xmlContent)) !== null) {
    urls.push(match[1].trim());
  }
  return urls;
}

/**
 * Read a sitemap file and return its full content as a string.
 * Returns null if the file does not exist or cannot be read.
 */
function readSitemap(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }
  return fs.readFileSync(filePath, 'utf-8');
}

/**
 * Collect URLs from all available sitemap files, deduplicating.
 * If a sitemap is a <sitemapindex>, it will extract the nested
 * sitemap <loc> URLs but will NOT recursively fetch remote sitemaps.
 */
function collectAllUrls() {
  const urlSet = new Set();

  for (const sitemapPath of SITEMAP_FILES) {
    const content = readSitemap(sitemapPath);
    if (!content) {
      console.log(`[skip] Sitemap not found: ${path.basename(sitemapPath)}`);
      continue;
    }

    const locs = extractLocs(content);
    console.log(`[info] Found ${locs.length} URL(s) in ${path.basename(sitemapPath)}`);

    for (const loc of locs) {
      urlSet.add(loc);
    }
  }

  return Array.from(urlSet);
}

// ---------------------------------------------------------------------------
// IndexNow Submission
// ---------------------------------------------------------------------------

/**
 * Send a single batch of URLs to the IndexNow API.
 * Returns a Promise that resolves to { success, status, batchIndex, urlCount }.
 */
function submitBatch(urls, batchIndex) {
  return new Promise((resolve) => {
    const payload = JSON.stringify({
      host: HOST,
      key: INDEXNOW_KEY,
      urlList: urls,
    });

    const url = new URL(INDEXNOW_ENDPOINT);
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'User-Agent': 'BeehiveStrategy-IndexNow/1.0',
      },
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => (body += chunk));
      res.on('end', () => {
        // IndexNow returns 200 OK on success, 202 Accepted is also valid
        const success = res.statusCode === 200 || res.statusCode === 202;
        resolve({
          success,
          status: res.statusCode,
          batchIndex,
          urlCount: urls.length,
        });
      });
    });

    req.on('error', (err) => {
      resolve({
        success: false,
        status: 'ERROR',
        batchIndex,
        urlCount: urls.length,
        error: err.message,
      });
    });

    // Timeout after 30 seconds
    req.setTimeout(30000, () => {
      req.destroy();
      resolve({
        success: false,
        status: 'TIMEOUT',
        batchIndex,
        urlCount: urls.length,
      });
    });

    req.write(payload);
    req.end();
  });
}

// ---------------------------------------------------------------------------
// Key File Management
// ---------------------------------------------------------------------------

/**
 * Ensure the IndexNow key file exists at the site root.
 * The file must be accessible at https://<host>/<key>.txt for verification.
 */
function ensureKeyFile() {
  const keyFilePath = path.join(SITE_ROOT, `${INDEXNOW_KEY}.txt`);
  if (fs.existsSync(keyFilePath)) {
    console.log(`[info] Key file already exists: ${INDEXNOW_KEY}.txt`);
    return;
  }
  fs.writeFileSync(keyFilePath, INDEXNOW_KEY, 'utf-8');
  console.log(`[info] Created key file: ${INDEXNOW_KEY}.txt`);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log('=== IndexNow Notification for beehivestrategy.com ===\n');

  // Ensure the key file exists
  ensureKeyFile();

  // Collect all URLs from sitemaps
  const allUrls = collectAllUrls();
  if (allUrls.length === 0) {
    console.log('\n[warn] No URLs found in any sitemap. Nothing to submit.');
    process.exit(1);
  }

  console.log(`\n[info] Total unique URLs to submit: ${allUrls.length}`);

  // Split into batches
  const batches = [];
  for (let i = 0; i < allUrls.length; i += BATCH_SIZE) {
    batches.push(allUrls.slice(i, i + BATCH_SIZE));
  }

  console.log(`[info] Split into ${batches.length} batch(es) (max ${BATCH_SIZE} per batch)\n`);

  // Submit each batch and log results
  let totalSuccess = 0;
  let totalFailed = 0;

  for (let i = 0; i < batches.length; i++) {
    const result = await submitBatch(batches[i], i + 1);

    if (result.success) {
      totalSuccess += result.urlCount;
      console.log(
        `[ok]   Batch ${result.batchIndex}/${batches.length}: ` +
          `${result.urlCount} URL(s) submitted (HTTP ${result.status})`
      );
    } else {
      totalFailed += result.urlCount;
      console.log(
        `[fail] Batch ${result.batchIndex}/${batches.length}: ` +
          `${result.urlCount} URL(s) failed (HTTP ${result.status})` +
          (result.error ? ` - ${result.error}` : '')
      );
    }

    // Small delay between batches to avoid rate limiting
    if (i < batches.length - 1) {
      await new Promise((resolve) => setTimeout(resolve, 500));
    }
  }

  // Summary
  console.log('\n--- Summary ---');
  console.log(`Key:        ${INDEXNOW_KEY}`);
  console.log(`Host:       ${HOST}`);
  console.log(`Submitted:  ${totalSuccess} URL(s)`);
  console.log(`Failed:     ${totalFailed} URL(s)`);
  console.log(`Total:      ${allUrls.length} URL(s)`);

  if (totalFailed > 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(`[fatal] ${err.message}`);
  process.exit(1);
});