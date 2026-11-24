/* Article layout v9 — enhances the shared ar-* shell.
   article.js remains responsible for share buttons, FAQ accordion and
   the legacy reading-progress bar. This file only handles the v9 rail TOC. */
(function () {
    'use strict';

    var links = Array.prototype.slice.call(document.querySelectorAll('.ar-toc a[href^="#"]'));
    if (!links.length) return;

    var targets = links
        .map(function (link) {
            var id = decodeURIComponent(link.getAttribute('href').slice(1));
            return { link: link, node: document.getElementById(id) };
        })
        .filter(function (item) { return !!item.node; });

    if (!targets.length) return;

    // Smooth scroll with a header offset.
    targets.forEach(function (item) {
        item.link.addEventListener('click', function (e) {
            e.preventDefault();
            var header = document.getElementById('header');
            var offset = header ? header.offsetHeight + 20 : 90;
            var top = item.node.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top: top, behavior: 'smooth' });
        });
    });

    // Active link by scroll position — deterministic and observer-free.
    function updateActive() {
        var marker = window.scrollY + 140;
        var active = targets[0];
        targets.forEach(function (item) {
            if (item.node.getBoundingClientRect().top + window.scrollY <= marker) active = item;
        });
        targets.forEach(function (item) {
            item.link.classList.toggle('active', item === active);
        });
    }

    var ticking = false;
    window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(function () {
            updateActive();
            ticking = false;
        });
    }, { passive: true });

    updateActive();
})();
