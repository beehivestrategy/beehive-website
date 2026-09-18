/* article-anim.js — Beehive Strategy "New Version" motion + UX layer.
   Loaded (defer) on article pages alongside article.js.
   - reading progress bar
   - scroll-reveal of article body blocks (staggered)
   - TOC active-section highlight (only if not already handled)
   - magnetic CTA button
   - locale-consistency safety net for internal links
   Defensive: every feature is wrapped so a missing element never throws. */
(function () {
  'use strict';
  var reduce = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- reading progress ---- */
  var bar = document.querySelector('.reading-progress-bar');
  function onScroll() {
    if (!bar) return;
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var p = max > 0 ? (h.scrollTop || document.body.scrollTop) / max : 0;
    bar.style.width = (Math.min(1, Math.max(0, p)) * 100).toFixed(2) + '%';
  }
  if (bar && !reduce) {
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---- scroll reveal of body blocks ---- */
  var content = document.querySelector('.article-content');
  if (content && !reduce) {
    var blocks = content.children;
    for (var i = 0; i < blocks.length; i++) {
      var el = blocks[i];
      if (el.classList.contains('article-figure')) continue;
      el.classList.add('reveal');
      el.style.transitionDelay = Math.min(i * 35, 350) + 'ms';
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add('is-visible');
            io.unobserve(e.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
      for (var j = 0; j < blocks.length; j++) io.observe(blocks[j]);
    } else {
      for (var k = 0; k < blocks.length; k++) blocks[k].classList.add('is-visible');
    }
  }

  /* ---- TOC active highlight (only if not already handled) ---- */
  var tocLinks = Array.prototype.slice.call(
    document.querySelectorAll('.toc-sidebar .toc-link, .toc-links .toc-link'));
  if (tocLinks.length && !document.querySelector('.toc-link.active') && !reduce) {
    var map = {};
    tocLinks.forEach(function (a) {
      var id = a.getAttribute('href');
      if (id && id.charAt(0) === '#') map[id.slice(1)] = a;
    });
    var sections = Object.keys(map).map(function (id) {
      return document.getElementById(id);
    }).filter(Boolean);
    if (sections.length && 'IntersectionObserver' in window) {
      var tio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            tocLinks.forEach(function (l) { l.classList.remove('active'); });
            var act = map[e.target.id];
            if (act) act.classList.add('active');
          }
        });
      }, { rootMargin: '-15% 0px -70% 0px', threshold: 0 });
      sections.forEach(function (s) { tio.observe(s); });
    }
  }

  /* ---- magnetic CTA ---- */
  if (!reduce) {
    Array.prototype.slice.call(document.querySelectorAll('.article-cta-btn'))
      .forEach(function (btn) {
        btn.addEventListener('mousemove', function (ev) {
          var r = btn.getBoundingClientRect();
          var x = (ev.clientX - r.left) / r.width - 0.5;
          var y = (ev.clientY - r.top) / r.height - 0.5;
          btn.style.transform = 'translate(' + (x * 10).toFixed(1) + 'px,' +
            (y * 8).toFixed(1) + 'px)';
        });
        btn.addEventListener('mouseleave', function () {
          btn.style.transform = '';
        });
      });
  }

  /* ---- locale-consistency safety net (internal links) ---- */
  var loc = (document.documentElement.getAttribute('lang') || '').toLowerCase();
  if (loc === 'zh-cn' || loc === 'zh-tw') {
    var safe = /^\/(blog\/articles|contact|solution|fde|services|about|blog)\/?/;
    Array.prototype.slice.call(document.querySelectorAll('a[href^="/"]'))
      .forEach(function (a) {
        var h = a.getAttribute('href');
        if (!h || h.indexOf('/' + loc + '/') === 0) return;
        if (a.closest('.lang-switcher')) return;
        if (/^(\/assets|\/css|\/js|\/images|\/img|\/favicon)/.test(h)) return;
        if (safe.test(h)) a.setAttribute('href', '/' + loc + h);
      });
  }
})();
