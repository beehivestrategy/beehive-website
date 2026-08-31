#!/usr/bin/env python3
"""Batch-fix layout gaps in deepseek-harness rewritten articles.

Fixes applied to every verified (harness) article across EN/zh-CN/zh-TW:
  1. Replace the harness (dark) footer with the LIVE white production footer.
  2. Fix header / CTA / mobile-menu relative links  href="contact"->/contact, href="solution"->/solution.
  3. Fix related + recommended article links to be root-relative and language-aware
     (EN -> /blog/articles/, zh-CN -> /zh-cn/blog/articles/, zh-TW -> /zh-tw/blog/articles/).

article.js (shared) is fixed separately. article.css (shared) got the live footer styles appended.
"""
import json, re, os, sys

BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
STATUS = os.path.join(BASE, "_batch_pipeline", "status.json")

LIVE_FOOTER = '''<footer class="footer" role="contentinfo">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" class="footer-logo" aria-label="Beehive Strategy Home">
            <img src="/assets/images/beehive-logo.png" alt="Beehive Strategy Logo" width="144" height="36" loading="lazy">
          </a>
          <p>Enterprise AI &amp; data analytics consulting. We deliver AI-powered conversational intelligence that transforms how businesses interact with their data.</p>
          <div class="social">
            <a href="https://www.linkedin.com/company/beehive-strategy" aria-label="LinkedIn" rel="noopener noreferrer" target="_blank"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
            <a href="/cdn-cgi/l/email-protection#b8d9dbdbd7cdd6ccf8daddddd0d1ceddcbcccad9ccdddfc196dbd7d5" aria-label="Email"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Product</h4>
          <ul>
            <li><a href="/solution">Platform</a></li>
            <li><a href="/solution">AI Agents</a></li>
            <li><a href="/case-studies">Case Studies</a></li>
            <li><a href="/security">Security</a></li>
            <li><a href="/pricing">Pricing</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Industries</h4>
          <ul>
            <li><a href="/industries">Retail &amp; E-Commerce</a></li>
            <li><a href="/industries">Financial Services</a></li>
            <li><a href="/industries">Manufacturing</a></li>
            <li><a href="/industries">Professional Services</a></li>
            <li><a href="/industries">Real Estate</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Company</h4>
          <ul>
            <li><a href="/about">About Us</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/solution">FAQ</a></li>
            <li><a href="/cdn-cgi/l/email-protection#b8999b9b978d968cb89a9d9d90918e9d8b8c8a998c9d9f81d69b9795">Careers</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2024&ndash;2026 Beehive Strategy Limited. All rights reserved.</p>
        <div class="footer-legal">
          <a href="/privacy">Privacy Policy</a>
          <a href="/terms">Terms of Service</a>
          <a href="/cookies">Cookie Policy</a>
        </div>
        <p>Built in Shenzhen, China</p>
      </div>
    </div>
  </footer>'''

FOOTER_RE = re.compile(r'<footer\b[^>]*>.*?</footer>', re.S | re.I)

LANGS = [
    ("blog/articles", ""),
    ("zh-cn/blog/articles", "zh-cn/"),
    ("zh-tw/blog/articles", "zh-tw/"),
]

def fix_one(path, prefix):
    with open(path, encoding="utf-8") as f:
        h = f.read()
    orig = h
    # 1. footer
    h, n_footer = FOOTER_RE.subn(LIVE_FOOTER, h)
    # 2. header/cta/mobile relative links
    h = h.replace('href="contact"', 'href="/contact"')
    h = h.replace('href="solution"', 'href="/solution"')
    # 3. related + recommended links (language-aware, root-relative)
    h = h.replace('href="blog/articles/', 'href="/' + prefix + 'blog/articles/')
    if h != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(h)
    return n_footer

def main():
    status = json.load(open(STATUS, encoding="utf-8"))
    slugs = [s for s, d in status["slugs"].items() if d.get("state") == "verified"]
    print(f"Verified (harness) slugs to fix: {len(slugs)}")
    total_files = 0
    footer_fixed = 0
    missing = 0
    for slug in slugs:
        for sub, prefix in LANGS:
            p = os.path.join(BASE, sub, slug + ".html")
            if not os.path.exists(p):
                missing += 1
                continue
            nf = fix_one(p, prefix)
            total_files += 1
            footer_fixed += nf
    print(f"Files processed: {total_files}")
    print(f"Footers replaced: {footer_fixed}")
    print(f"Missing files (skipped): {missing}")

if __name__ == "__main__":
    main()
