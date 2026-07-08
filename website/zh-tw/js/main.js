/**
 * ============================================================
 * BEEHIVE STRATEGY — MAIN JAVASCRIPT
 * Interactive effects, animations, and scroll-driven experiences
 * ============================================================
 */

(function() {
  'use strict';

  // ——— Configuration ———
  const CONFIG = {
    prefersReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    isMobile: window.matchMedia('(pointer: coarse)').matches,
    isTouch: 'ontouchstart' in window || navigator.maxTouchPoints > 0,
    headerScrollThreshold: 50,
    particleCount: 0, // set dynamically
    revealThreshold: 0.15
  };

  // Determine particle count based on device capability
  CONFIG.particleCount = CONFIG.isMobile ? 80 : 150;

  // ——— DOM Cache ———
  const DOM = {
    header: document.getElementById('header'),
    hamburger: document.getElementById('hamburger'),
    mobileMenu: document.getElementById('mobile-menu'),
    heroCanvas: document.getElementById('hero-canvas'),
    revealElements: document.querySelectorAll('.reveal'),
    statCards: document.querySelectorAll('.stat-card'),
    faqItems: document.querySelectorAll('.faq-item'),
    navLinks: document.querySelectorAll('.nav-link, .mobile-menu a')
  };

  // ——— Utilities ———
  const utils = {
    throttle: function(fn, limit) {
      let inThrottle;
      return function(...args) {
        if (!inThrottle) {
          fn.apply(this, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      };
    },

    debounce: function(fn, wait) {
      let timeout;
      return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn.apply(this, args), wait);
      };
    },

    lerp: function(a, b, t) {
      return a + (b - a) * t;
    },

    random: function(min, max) {
      return Math.random() * (max - min) + min;
    }
  };

  // ——— Header Scroll Effect ———
  function initHeader() {
    if (!DOM.header) return;

    let lastScroll = 0;
    const scrollHandler = utils.throttle(() => {
      const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

      // Add/remove scrolled class
      if (currentScroll > CONFIG.headerScrollThreshold) {
        DOM.header.classList.add('scrolled');
      } else {
        DOM.header.classList.remove('scrolled');
      }

      lastScroll = currentScroll;
    }, 50);

    window.addEventListener('scroll', scrollHandler, { passive: true });
  }

  // ——— Mobile Menu ———
  function initMobileMenu() {
    if (!DOM.hamburger || !DOM.mobileMenu) return;

    DOM.hamburger.addEventListener('click', function() {
      const isExpanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', !isExpanded);
      this.classList.toggle('active');
      DOM.mobileMenu.classList.toggle('active');
      DOM.mobileMenu.setAttribute('aria-hidden', isExpanded);
      document.body.style.overflow = isExpanded ? '' : 'hidden';
    });

    // Close on link click
    DOM.mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        DOM.hamburger.setAttribute('aria-expanded', 'false');
        DOM.hamburger.classList.remove('active');
        DOM.mobileMenu.classList.remove('active');
        DOM.mobileMenu.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      });
    });
  }

  // ——— Hero Particle Network ———
  function initHeroParticles() {
    if (!DOM.heroCanvas || CONFIG.prefersReducedMotion) return;

    const canvas = DOM.heroCanvas;
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId = null;
    let mouse = { x: null, y: null, radius: 150 };

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }

    resize();
    window.addEventListener('resize', utils.debounce(resize, 200));

    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = utils.random(-0.5, 0.5);
        this.vy = utils.random(-0.5, 0.5);
        this.size = utils.random(1, 3);
        this.baseColor = Math.random() > 0.5 ? '43, 158, 139' : '212, 168, 67';
        this.opacity = utils.random(0.3, 0.8);
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off edges
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;

        // Mouse interaction
        if (mouse.x !== null && mouse.y !== null) {
          const dx = mouse.x - this.x;
          const dy = mouse.y - this.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < mouse.radius) {
            const force = (mouse.radius - distance) / mouse.radius;
            const angle = Math.atan2(dy, dx);
            this.vx -= Math.cos(angle) * force * 0.02;
            this.vy -= Math.sin(angle) * force * 0.02;
          }
        }

        // Damping
        this.vx *= 0.99;
        this.vy *= 0.99;

        // Minimum velocity
        if (Math.abs(this.vx) < 0.1) this.vx += utils.random(-0.1, 0.1);
        if (Math.abs(this.vy) < 0.1) this.vy += utils.random(-0.1, 0.1);
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${this.baseColor}, ${this.opacity})`;
        ctx.fill();
      }
    }

    function initParticles() {
      particles = [];
      for (let i = 0; i < CONFIG.particleCount; i++) {
        particles.push(new Particle());
      }
    }

    function connectParticles() {
      const maxDistance = 120;

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < maxDistance) {
            const opacity = (1 - distance / maxDistance) * 0.15;
            ctx.beginPath();
            ctx.strokeStyle = `rgba(43, 158, 139, ${opacity})`;
            ctx.lineWidth = 0.5;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw subtle radial gradient background
      const gradient = ctx.createRadialGradient(
        canvas.width / 2, canvas.height / 2, 0,
        canvas.width / 2, canvas.height / 2, canvas.width / 2
      );
      gradient.addColorStop(0, 'rgba(43, 158, 139, 0.02)');
      gradient.addColorStop(1, 'rgba(10, 14, 13, 0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      particles.forEach(p => {
        p.update();
        p.draw();
      });

      connectParticles();
      animationId = requestAnimationFrame(animate);
    }

    // Mouse interaction
    canvas.addEventListener('mousemove', utils.throttle((e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    }, 16));

    canvas.addEventListener('mouseleave', () => {
      mouse.x = null;
      mouse.y = null;
    });

    // Touch interaction
    canvas.addEventListener('touchmove', utils.throttle((e) => {
      const rect = canvas.getBoundingClientRect();
      const touch = e.touches[0];
      mouse.x = touch.clientX - rect.left;
      mouse.y = touch.clientY - rect.top;
    }, 16), { passive: true });

    canvas.addEventListener('touchend', () => {
      mouse.x = null;
      mouse.y = null;
    });

    initParticles();
    animate();

    // Cleanup on visibility change
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        cancelAnimationFrame(animationId);
      } else {
        animate();
      }
    });
  }

  // ——— Scroll Reveal Animation ———
  function initScrollReveal() {
    if (CONFIG.prefersReducedMotion) {
      DOM.revealElements.forEach(el => el.classList.add('visible'));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: CONFIG.revealThreshold,
      rootMargin: '0px 0px -50px 0px'
    });

    DOM.revealElements.forEach(el => observer.observe(el));
  }

  // ——— Counter Animation (Enhanced) ———
  function initCounterAnimation() {
    const selectors = '.stat-value[data-target], .metric-value[data-target], .sp-num[data-target], .counter-animate[data-target]';
    const statValues = document.querySelectorAll(selectors);

    const animateCounter = (el) => {
      const target = parseFloat(el.dataset.target);
      const isFloat = el.dataset.target.includes('.');
      const suffix = el.dataset.suffix || '';
      const prefix = el.dataset.prefix || '';
      const duration = parseInt(el.dataset.duration, 10) || 2000;
      const start = performance.now();

      const update = (now) => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4);
        const current = isFloat ? (eased * target).toFixed(1) : Math.round(eased * target);
        el.textContent = prefix + current + suffix;

        if (progress < 1) {
          requestAnimationFrame(update);
        }
      };

      requestAnimationFrame(update);
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    statValues.forEach(el => observer.observe(el));
  }

  // ——— New Animation Observers ———
  function initNewAnimations() {
    if (CONFIG.prefersReducedMotion) return;

    const animationClasses = ['.scale-in', '.rotate-in', '.slide-in-left', '.slide-in-right'];
    const allElements = [];

    animationClasses.forEach(cls => {
      document.querySelectorAll(cls).forEach(el => allElements.push(el));
    });

    if (!allElements.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

    allElements.forEach(el => observer.observe(el));
  }

  // ——— SVG Line Draw Animation ———
  function initLineDrawAnimation() {
    if (CONFIG.prefersReducedMotion) return;

    const lines = document.querySelectorAll('.line-draw');
    if (!lines.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    lines.forEach(el => observer.observe(el));
  }

  // ——— Bar Growth Animation ———
  function initBarGrowthAnimation() {
    if (CONFIG.prefersReducedMotion) return;

    const bars = document.querySelectorAll('.bar-grow');
    if (!bars.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    bars.forEach(el => observer.observe(el));
  }

  // ——— Sparkline Draw Animation ———
  function initSparklineDrawAnimation() {
    if (CONFIG.prefersReducedMotion) return;

    const sparklines = document.querySelectorAll('.sparkline-draw');
    if (!sparklines.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    sparklines.forEach(el => observer.observe(el));
  }

  // ——— Comparison Bar Fill Animation ———
  function initCompBarFillAnimation() {
    if (CONFIG.prefersReducedMotion) return;

    const bars = document.querySelectorAll('.comp-bar-fill');
    if (!bars.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    bars.forEach(el => observer.observe(el));
  }

  // ——— Donut Chart Draw Animation ———
  function initDonutDrawAnimation() {
    if (CONFIG.prefersReducedMotion) return;

    const donuts = document.querySelectorAll('.donut-draw');
    if (!donuts.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    donuts.forEach(el => observer.observe(el));
  }

  // ——— Reveal Manager (for dynamic content refresh) ———
  window.RevealManager = {
    refresh: function() {
      initScrollReveal();
      initNewAnimations();
    }
  };

  // ——— FAQ Accordion ———
  function initFAQ() {
    DOM.faqItems.forEach(item => {
      const question = item.querySelector('.faq-question');
      if (!question) return;

      question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        const answer = item.querySelector('.faq-answer');

        // Close all others
        DOM.faqItems.forEach(other => {
          other.classList.remove('active');
          const otherQuestion = other.querySelector('.faq-question');
          if (otherQuestion) otherQuestion.setAttribute('aria-expanded', 'false');
        });

        // Toggle current
        if (!isActive) {
          item.classList.add('active');
          question.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  // ——— Smooth Scroll for Anchor Links ———
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const target = document.querySelector(targetId);
        if (!target) return;

        e.preventDefault();
        const headerOffset = DOM.header ? DOM.header.offsetHeight : 0;
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerOffset - 20;

        window.scrollTo({
          top: targetPosition,
          behavior: CONFIG.prefersReducedMotion ? 'auto' : 'smooth'
        });
      });
    });
  }

  // ——— Parallax Tilt Effect for Cards ———
  function initTiltEffect() {
    if (CONFIG.isTouch || CONFIG.prefersReducedMotion) return;

    const cards = document.querySelectorAll('.card, .industry-card, .agent-card, .reason-card');

    cards.forEach(card => {
      card.addEventListener('mousemove', utils.throttle((e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
      }, 16));

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
      });
    });
  }

  // ——— Magnetic Button Effect ———
  function initMagneticButtons() {
    if (CONFIG.isTouch || CONFIG.prefersReducedMotion) return;

    const buttons = document.querySelectorAll('.btn-primary, .btn-accent');

    buttons.forEach(btn => {
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px) translateY(-2px)`;
      });

      btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
      });
    });
  }

  // ——— Text Scramble Effect for Hero ———
  function initTextScramble() {
    if (CONFIG.prefersReducedMotion) return;

    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const target = document.querySelector('.hero h1');
    if (!target) return;

    const originalText = target.innerHTML;
    let iteration = 0;
    let interval = null;

    function scramble() {
      clearInterval(interval);
      iteration = 0;

      interval = setInterval(() => {
        // This is a simplified scramble - just for the initial load effect
        // In a full implementation, we would parse the HTML and scramble text nodes
        iteration += 1 / 3;

        if (iteration >= 1) {
          clearInterval(interval);
          target.innerHTML = originalText;
        }
      }, 30);
    }

    // Trigger after a short delay
    setTimeout(scramble, 500);
  }

  // ——— Scroll Progress Indicator ———
  function initScrollProgress() {
    if (CONFIG.prefersReducedMotion) return;

    const progressBar = document.getElementById('scroll-progress');
    if (!progressBar) return;

    window.addEventListener('scroll', utils.throttle(() => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const progress = (scrollTop / docHeight) * 100;
      progressBar.style.width = progress + '%';
    }, 50), { passive: true });
  }

  // ——— Back to Top Button ———
  function initBackToTop() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;

    window.addEventListener('scroll', utils.throttle(() => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      if (scrollTop > 500) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }, 100), { passive: true });

    btn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: CONFIG.prefersReducedMotion ? 'auto' : 'smooth'
      });
    });
  }

  // ——— Skeleton Loading Simulation ———
  function initSkeletonLoading() {
    const lazyElements = document.querySelectorAll('img[loading="lazy"]');

    lazyElements.forEach(img => {
      if (img.complete) return;

      const skeleton = document.createElement('div');
      skeleton.className = 'skeleton';
      skeleton.style.cssText = `
        position: absolute;
        inset: 0;
        z-index: 1;
      `;
      img.parentNode.style.position = 'relative';
      img.parentNode.insertBefore(skeleton, img);

      img.addEventListener('load', () => {
        skeleton.remove();
      });

      img.addEventListener('error', () => {
        skeleton.remove();
      });
    });
  }

  // ——— Performance Monitoring ———
  function initPerformanceMonitoring() {
    // Log Core Web Vitals when available
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if (entry.entryType === 'largest-contentful-paint') {
              console.log('LCP:', entry.startTime);
            }
            if (entry.entryType === 'first-input') {
              console.log('FID:', entry.processingStart - entry.startTime);
            }
            if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
              console.log('CLS:', entry.value);
            }
          }
        });
        observer.observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift'] });
      } catch (e) {
        // Some entry types may not be supported
      }
    }

    // Report load time
    window.addEventListener('load', () => {
      setTimeout(() => {
        const timing = performance.timing;
        if (timing) {
          const pageLoadTime = timing.loadEventEnd - timing.navigationStart;
          console.log('Page load time:', pageLoadTime + 'ms');
        }
      }, 0);
    });
  }

  // ——— Bar Chart Animation ———
  function initBarChart() {
    if (CONFIG.prefersReducedMotion) {
      document.querySelectorAll('.bar[data-height]').forEach(bar => {
        bar.style.height = bar.dataset.height + '%';
      });
      return;
    }

    const bars = document.querySelectorAll('.bar[data-height]');
    if (!bars.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const bar = entry.target;
          const height = bar.dataset.height;
          // Small delay for a nice cascade effect
          setTimeout(() => {
            bar.style.height = height + '%';
          }, 50);
          observer.unobserve(bar);
        }
      });
    }, { threshold: 0.3 });

    bars.forEach(bar => observer.observe(bar));
  }

  // ——— Comparison Bars Animation ———
  function initComparisonBars() {
    if (CONFIG.prefersReducedMotion) {
      document.querySelectorAll('.comp-bar[data-width]').forEach(bar => {
        bar.style.width = bar.dataset.width + '%';
      });
      return;
    }

    const bars = document.querySelectorAll('.comp-bar[data-width]');
    if (!bars.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const bar = entry.target;
          const width = bar.dataset.width;
          setTimeout(() => {
            bar.style.width = width + '%';
          }, 100);
          observer.unobserve(bar);
        }
      });
    }, { threshold: 0.2 });

    bars.forEach(bar => observer.observe(bar));
  }

  // ——— Active Nav Link Detection (Multi-page) ———
  function initActiveSectionNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (!href || href === '#') return;

      // Check if this link matches the current page
      const linkPath = href.replace(/^\.\.\//, '').replace(/^\.\//, '');
      const pageName = currentPath.split('/').pop() || 'index.html';

      if (href === pageName || (pageName === 'index.html' && href === 'index.html') || currentPath.includes(linkPath)) {
        link.classList.add('active');
      }
    });
  }

  // ——— Initialize Everything ———
  function init() {
    initHeader();
    initMobileMenu();
    initHeroParticles();
    initScrollReveal();
    initCounterAnimation();
    initNewAnimations();
    initLineDrawAnimation();
    initBarGrowthAnimation();
    initSparklineDrawAnimation();
    initCompBarFillAnimation();
    initDonutDrawAnimation();
    initFAQ();
    initSmoothScroll();
    initTiltEffect();
    initMagneticButtons();
    initTextScramble();
    initScrollProgress();
    initBackToTop();
    initSkeletonLoading();
    initPerformanceMonitoring();
    initActiveSectionNav();
    initBarChart();
    initComparisonBars();
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
