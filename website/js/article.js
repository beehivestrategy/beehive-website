(function() {
    'use strict';

    // ---- Elements ----
    var progressBar = document.getElementById('readingProgress');
    var header = document.getElementById('header');
    var hamburger = document.getElementById('hamburger') || document.getElementById('hamburger-btn');
    var mobileMenu = document.getElementById('mobile-menu');
    var langSwitcher = document.getElementById('lang-switcher');
    var langBtn = langSwitcher.querySelector('.lang-switcher-btn');
    var langDropdown = langSwitcher.querySelector('.lang-switcher-dropdown') || langSwitcher.querySelector('.lang-dropdown');
    var backToTop = document.getElementById('backToTop');
    var articleContent = document.getElementById('article-content');
    var tocLinks = document.querySelectorAll('.toc-sidebar .toc-link');
    var tocMobile = document.getElementById('toc-mobile');
    var tocMobileToggle = tocMobile.querySelector('.toc-mobile-toggle');
    var toast = document.getElementById('toast');
    var faqItems = document.querySelectorAll('.faq-item');

    // ---- 1. Reading Progress Bar ----
    function updateProgress() {
        var article = articleContent;
        if (!article) return;
        var rect = article.getBoundingClientRect();
        var articleTop = rect.top + window.scrollY;
        var articleHeight = article.offsetHeight;
        var scrolled = window.scrollY;
        var viewHeight = window.innerHeight;
        var progress = ((scrolled - articleTop) + viewHeight * 0.3) / articleHeight;
        progress = Math.max(0, Math.min(1, progress));
        progressBar.style.width = (progress * 100) + '%';
    }

    // ---- 2. Header Shadow on Scroll ----
    function handleHeaderScroll() {
        if (window.scrollY > 10) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    // ---- 3. Back to Top ----
    function handleBackToTop() {
        if (window.scrollY > 400) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    }

    backToTop.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ---- 4. Hamburger Menu ----
    hamburger.addEventListener('click', function() {
        var isOpen = mobileMenu.classList.toggle('open');
        hamburger.classList.toggle('active');
        hamburger.setAttribute('aria-expanded', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // ---- 5. Language Switcher ----
    langBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        var isOpen = langDropdown.classList.toggle('open');
        langBtn.setAttribute('aria-expanded', isOpen);
    });

    document.addEventListener('click', function(e) {
        if (!langSwitcher.contains(e.target)) {
            langDropdown.classList.remove('open');
            langBtn.setAttribute('aria-expanded', 'false');
        }
    });

    // ---- 5b. Desktop Services dropdown (click + keyboard, parity with main.js) ----
    function closeAllNavDropdowns(except) {
        document.querySelectorAll('.nav-item-dropdown.open').forEach(function(d) {
            if (d === except) return;
            d.classList.remove('open');
            var t = d.querySelector(':scope > .nav-link');
            if (t) t.setAttribute('aria-expanded', 'false');
        });
    }
    document.querySelectorAll('.nav-item-dropdown').forEach(function(dropdown) {
        var trigger = dropdown.querySelector(':scope > .nav-link');
        if (!trigger) return;
        trigger.setAttribute('aria-haspopup', 'true');
        trigger.setAttribute('aria-expanded', 'false');
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            var willOpen = !dropdown.classList.contains('open');
            closeAllNavDropdowns(dropdown);
            dropdown.classList.toggle('open', willOpen);
            trigger.setAttribute('aria-expanded', String(willOpen));
        });
        trigger.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeAllNavDropdowns();
        });
    });
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.nav-item-dropdown')) closeAllNavDropdowns();
    });

    // ---- 5c. Mobile submenu toggles ----
    mobileMenu.querySelectorAll('.mobile-submenu-toggle').forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            var submenu = this.closest('.mobile-submenu');
            if (submenu) submenu.classList.toggle('open');
        });
    });

    // ---- 6. FAQ Accordion (one at a time) ----
    faqItems.forEach(function(item) {
        var question = item.querySelector('.faq-question');
        var answer = item.querySelector('.faq-answer');
        var inner = answer.querySelector('.faq-answer-inner');

        question.addEventListener('click', function() {
            var isOpen = item.classList.contains('open');

            // Close all other items
            faqItems.forEach(function(otherItem) {
                if (otherItem !== item) {
                    otherItem.classList.remove('open');
                    var otherAnswer = otherItem.querySelector('.faq-answer');
                    var otherQuestion = otherItem.querySelector('.faq-question');
                    otherAnswer.style.maxHeight = '0';
                    otherQuestion.setAttribute('aria-expanded', 'false');
                }
            });

            // Toggle current item
            if (isOpen) {
                item.classList.remove('open');
                answer.style.maxHeight = '0';
                question.setAttribute('aria-expanded', 'false');
            } else {
                item.classList.add('open');
                answer.style.maxHeight = inner.scrollHeight + 'px';
                question.setAttribute('aria-expanded', 'true');
            }
        });
    });

    // ---- 7. Mobile TOC Toggle ----
    tocMobileToggle.addEventListener('click', function() {
        var isOpen = tocMobile.classList.toggle('open');
        tocMobileToggle.setAttribute('aria-expanded', isOpen);
    });

    // ---- 8. TOC Active Link Tracking (IntersectionObserver) ----
    var sectionIds = [];
    tocLinks.forEach(function(link) {
        var href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
            sectionIds.push(href.substring(1));
        }
    });

    var sectionObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var id = entry.target.getAttribute('id');
                tocLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, {
        rootMargin: '-80px 0px -70% 0px',
        threshold: 0
    });

    sectionIds.forEach(function(id) {
        var section = document.getElementById(id);
        if (section) {
            sectionObserver.observe(section);
        }
    });

    // ---- 9. TOC Click -> Smooth Scroll ----
    var allTocLinks = document.querySelectorAll('.toc-link, .toc-mobile-link');
    allTocLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var href = link.getAttribute('href');
            var target = document.querySelector(href);
            if (target) {
                var offset = header.offsetHeight + 20;
                var top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top: top, behavior: 'smooth' });
            }
            // Close mobile TOC if open
            if (tocMobile.classList.contains('open')) {
                tocMobile.classList.remove('open');
                tocMobileToggle.setAttribute('aria-expanded', 'false');
            }
        });
    });

    // ---- 10. Share Buttons ----
    var articleUrl = window.location.href;
    var articleTitle = (window.__ARTICLE_TITLE__) || document.title || 'Beehive Strategy';

    var shareLinkedin = document.getElementById('share-linkedin');
    if (shareLinkedin) {
        shareLinkedin.addEventListener('click', function() {
            window.open('https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(articleUrl), '_blank', 'width=600,height=500');
        });
    }

    var shareX = document.getElementById('share-x');
    if (shareX) {
        shareX.addEventListener('click', function() {
            window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(articleTitle) + '&url=' + encodeURIComponent(articleUrl), '_blank', 'width=600,height=400');
        });
    }

    var shareWechat = document.getElementById('share-wechat');
    if (shareWechat) {
        shareWechat.addEventListener('click', function() {
            alert('WeChat sharing requires the WeChat app. Copy the link and share it in a WeChat conversation.');
        });
    }

    var shareCopy = document.getElementById('share-copy');
    if (shareCopy) {
        shareCopy.addEventListener('click', function() {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(articleUrl).then(function() {
                showToast('Link copied to clipboard!');
            });
        } else {
            var temp = document.createElement('textarea');
            temp.value = articleUrl;
            document.body.appendChild(temp);
            temp.select();
            document.execCommand('copy');
            document.body.removeChild(temp);
            showToast('Link copied to clipboard!');
        }
    });
    }

    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.add('show');
        setTimeout(function() {
            toast.classList.remove('show');
        }, 2000);
    }

    // ---- 11. Scroll Listener (debounced) ----
    var scrollTicking = false;
    window.addEventListener('scroll', function() {
        if (!scrollTicking) {
            window.requestAnimationFrame(function() {
                updateProgress();
                handleHeaderScroll();
                handleBackToTop();
                scrollTicking = false;
            });
            scrollTicking = true;
        }
    }, { passive: true });

    // Initial call
    updateProgress();
    handleHeaderScroll();
    handleBackToTop();

})();
