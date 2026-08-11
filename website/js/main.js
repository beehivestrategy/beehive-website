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
  // Reduced counts for better INP (Interaction to Next Paint) performance
  CONFIG.particleCount = CONFIG.isMobile ? 30 : 60;

  // ——— DOM Cache ———
  const DOM = {
    header: document.getElementById('header'),
    hamburger: document.getElementById('hamburger'),
    mobileMenu: document.getElementById('mobile-menu'),
    heroCanvas: document.getElementById('hero-canvas'),
    revealElements: document.querySelectorAll('.reveal'),
    statCards: document.querySelectorAll('.stat-card'),
    faqItems: document.querySelectorAll('.faq-item'),
    navLinks: document.querySelectorAll('.nav-link, .mobile-menu a'),
    langSwitcher: document.getElementById('lang-switcher'),
    langSwitcherBtn: document.getElementById('lang-switcher-btn')
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

  // ——— Consolidated Scroll Handler (reduces INP by using single rAF) ———
  let scrollTicking = false;
  let lastScrollY = 0;

  function onScroll() {
    lastScrollY = window.pageYOffset || document.documentElement.scrollTop;

    if (!scrollTicking) {
      requestAnimationFrame(() => {
        // Header effect
        if (DOM.header) {
          if (lastScrollY > CONFIG.headerScrollThreshold) {
            DOM.header.classList.add('scrolled');
          } else {
            DOM.header.classList.remove('scrolled');
          }
        }

        // Scroll progress bar
        const progressBar = document.getElementById('scroll-progress');
        if (progressBar) {
          const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
          const progress = docHeight > 0 ? (lastScrollY / docHeight) * 100 : 0;
          progressBar.style.width = progress + '%';
        }

        // Back to top button
        const backToTopBtn = document.getElementById('back-to-top');
        if (backToTopBtn) {
          if (lastScrollY > 500) {
            backToTopBtn.classList.add('visible');
          } else {
            backToTopBtn.classList.remove('visible');
          }
        }

        scrollTicking = false;
      });
      scrollTicking = true;
    }
  }

  // ——— Header Scroll Effect ———
  function initHeader() {
    if (!DOM.header) return;
    // Uses consolidated onScroll handler — no separate listener needed
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
      // Use spatial grid for O(n) connection check instead of O(n²)
      const maxDistance = 100;
      const cellSize = maxDistance;
      const cols = Math.ceil(canvas.width / cellSize) + 1;
      const rows = Math.ceil(canvas.height / cellSize) + 1;
      const grid = new Array(cols * rows);

      // Assign particles to grid cells
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        const cx = Math.max(0, Math.min(cols - 1, Math.floor(p.x / cellSize)));
        const cy = Math.max(0, Math.min(rows - 1, Math.floor(p.y / cellSize)));
        const idx = cy * cols + cx;
        if (!grid[idx]) grid[idx] = [];
        grid[idx].push(i);
      }

      // Check only neighboring cells
      for (let cy = 0; cy < rows; cy++) {
        for (let cx = 0; cx < cols; cx++) {
          const idx = cy * cols + cx;
          const cell = grid[idx];
          if (!cell) continue;

          // Check particles in current and adjacent cells
          for (let dy = 0; dy <= 1; dy++) {
            for (let dx = -1; dx <= 1; dx++) {
              if (dy === 0 && dx < 0) continue;
              const nx = cx + dx;
              const ny = cy + dy;
              if (nx < 0 || nx >= cols || ny >= rows) continue;
              const nidx = ny * cols + nx;
              const ncell = grid[nidx];
              if (!ncell) continue;

              for (let i = 0; i < cell.length; i++) {
                const pi = particles[cell[i]];
                for (let j = 0; j < ncell.length; j++) {
                  if (idx === nidx && cell[i] >= ncell[j]) continue;
                  const pj = particles[ncell[j]];
                  const ddx = pi.x - pj.x;
                  const ddy = pi.y - pj.y;
                  const distance = Math.sqrt(ddx * ddx + ddy * ddy);
                  if (distance < maxDistance) {
                    const opacity = (1 - distance / maxDistance) * 0.15;
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(43, 158, 139, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(pi.x, pi.y);
                    ctx.lineTo(pj.x, pj.y);
                    ctx.stroke();
                  }
                }
              }
            }
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
    // Support both data-target and data-counter attributes
    const selectors = '.stat-value[data-target], .stat-value[data-counter], .metric-value[data-target], .sp-num[data-target], .counter-animate[data-target]';
    const statValues = document.querySelectorAll(selectors);

    const animateCounter = (el) => {
      // Use data-counter if present, otherwise data-target
      const raw = el.dataset.counter || el.dataset.target;
      const target = parseFloat(raw);
      const isFloat = raw && raw.includes('.');
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
    // Disabled — causes scroll jank due to mousemove listeners on many elements
    return;

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

    // Fix: Use [data-magnetic] to catch ALL magnetic buttons (including .btn-ghost)
    const buttons = document.querySelectorAll('[data-magnetic]');

    buttons.forEach(btn => {
      const strength = 0.25;

      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        // Use GSAP for smoother movement if available
        if (typeof gsap !== 'undefined') {
          gsap.to(btn, {
            x: x * strength,
            y: y * strength,
            duration: 0.4,
            ease: 'power3.out'
          });
        } else {
          btn.style.transform = `translate(${x * strength}px, ${y * strength}px) translateY(-2px)`;
        }
      });

      btn.addEventListener('mouseleave', () => {
        if (typeof gsap !== 'undefined') {
          gsap.to(btn, { x: 0, y: 0, duration: 0.6, ease: 'elastic.out(1, 0.3)' });
        } else {
          btn.style.transform = '';
        }
      });
    });
  }

  // ——— GSAP Hero Entrance Animation ———
  function initGSAPHero() {
    if (CONFIG.prefersReducedMotion) return;

    // If GSAP is not loaded, skip — CSS animations serve as fallback
    if (typeof gsap === 'undefined') return;

    // Register plugins if available
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.registerPlugin(ScrollTrigger);
    }
    if (typeof ScrollToPlugin !== 'undefined') {
      gsap.registerPlugin(ScrollToPlugin);
    }

    // Initialize Splitting.js for character animation
    if (typeof Splitting !== 'undefined') {
      Splitting({
        target: '[data-splitting]',
        by: 'chars'
      });
    }

    // Clear hero-stagger CSS animation to prevent conflict with GSAP
    // The CSS animation is a fallback for no-JS; GSAP takes over when available
    const heroStagger = document.querySelector('.hero-stagger');
    if (heroStagger) {
      heroStagger.querySelectorAll(':scope > *').forEach(child => {
        child.style.animation = 'none';
        child.style.opacity = '1';
        child.style.transform = 'none';
      });
    }
    // Also clear reveal on hero-visual
    const heroVisual = document.querySelector('.hero-visual');
    if (heroVisual) {
      heroVisual.style.opacity = '1';
      heroVisual.style.transform = 'none';
      heroVisual.style.transition = 'none';
    }

    // Hero entrance timeline — staggered fade-up
    const heroTl = gsap.timeline({ delay: 0.3 });

    heroTl
      .from('.hero-badge', {
        y: 20, opacity: 0, duration: 0.6, ease: 'power3.out'
      })
      .from('.hero-title .char', {
        y: 30, opacity: 0, duration: 0.5,
        stagger: 0.03, ease: 'power3.out'
      }, '-=0.3')
      .from('.hero-tagline', {
        y: 20, opacity: 0, duration: 0.6, ease: 'power3.out'
      }, '-=0.3')
      .from('.hero-subtitle', {
        y: 20, opacity: 0, duration: 0.6, ease: 'power3.out'
      }, '-=0.4')
      .from('.hero-cta .btn', {
        y: 20, opacity: 0, duration: 0.5,
        stagger: 0.1, ease: 'power3.out'
      }, '-=0.3')
      .from('.hero-cta-note', {
        y: 10, opacity: 0, duration: 0.4, ease: 'power3.out'
      }, '-=0.2')
      .from('.hero-stat', {
        y: 20, opacity: 0, duration: 0.4,
        stagger: 0.08, ease: 'power3.out'
      }, '-=0.2')
      .from('.hero-visual', {
        y: 40, opacity: 0, duration: 0.8, ease: 'power3.out'
      }, '-=0.6');

    // Scroll parallax on hero visual
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.to('.hero-visual', {
        yPercent: 15,
        opacity: 0.7,
        ease: 'none',
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 1
        }
      });
    }
  }

  // ——— Lenis Smooth Scroll ———
  function initLenis() {
    if (CONFIG.prefersReducedMotion) return;

    // If Lenis is not loaded, skip — native scrolling works fine
    if (typeof Lenis === 'undefined') return;

    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    });

    // Connect Lenis to GSAP ScrollTrigger if both available
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((time) => lenis.raf(time * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
      }
      requestAnimationFrame(raf);
    }
  }

  // ——— Scroll Progress Indicator ———
  function initScrollProgress() {
    // Uses consolidated onScroll handler — no separate listener needed
  }

  // ——— Back to Top Button ———
  function initBackToTop() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;

    // Visibility handled by consolidated onScroll handler
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

  // ——— Language Switcher ———
  function initLangSwitcher() {
    const switcher = DOM.langSwitcher;
    const btn = DOM.langSwitcherBtn;
    const label = document.getElementById('current-lang-label');
    if (!switcher || !btn) return;

    // Auto-detect current language from URL path
    // Strip .html extension for clean URL normalization
    let path = window.location.pathname;
    if (path !== '/' && path.endsWith('.html')) {
      path = path.slice(0, -5);
    }
    let currentLang = 'en';
    let currentLabel = 'EN';
    if (path.indexOf('/zh-cn/') !== -1) {
      currentLang = 'zh-cn';
      currentLabel = '简';
    } else if (path.indexOf('/zh-tw/') !== -1) {
      currentLang = 'zh-tw';
      currentLabel = '繁';
    }

    // Update button label
    if (label) label.textContent = currentLabel;

    // Mark active item in dropdown
    const dropdownLinks = switcher.querySelectorAll('.lang-switcher-dropdown a');
    dropdownLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('data-lang') === currentLang) {
        link.classList.add('active');
      }
    });

    // Build alternate paths (always use clean URLs, no .html extension)
    const isZhCn = path.indexOf('/zh-cn/') === 0;
    const isZhTw = path.indexOf('/zh-tw/') === 0;
    let basePath = isZhCn ? path.replace(/^\/zh-cn/, '') : (isZhTw ? path.replace(/^\/zh-tw/, '') : path);
    // Normalize: strip .html, ensure trailing slash for index
    if (basePath === '' || basePath === '/') basePath = '/';
    else if (basePath === '/index') basePath = '/';
    const enPath = basePath;
    const zhCnPath = '/zh-cn' + basePath;
    const zhTwPath = '/zh-tw' + basePath;

    dropdownLinks.forEach(link => {
      const dl = link.getAttribute('data-lang');
      if (dl === 'en') link.setAttribute('href', enPath);
      else if (dl === 'zh-cn') link.setAttribute('href', zhCnPath);
      else if (dl === 'zh-tw') link.setAttribute('href', zhTwPath);
    });

    // Toggle dropdown
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const isOpen = switcher.classList.toggle('open');
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close on outside click
    document.addEventListener('click', function(e) {
      if (!switcher.contains(e.target)) {
        switcher.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    // Close on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && switcher.classList.contains('open')) {
        switcher.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
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
    // Run lang switcher FIRST — it's critical UX, must work even if other inits fail
    try { initLangSwitcher(); } catch(e) { console.warn('Lang switcher init failed:', e); }
    
    // Register consolidated scroll listener (replaces 3 separate listeners)
    window.addEventListener('scroll', onScroll, { passive: true });
    
    // Critical above-the-fold interactions — run immediately
    try { initHeader(); } catch(e) {}
    try { initMobileMenu(); } catch(e) {}
    try { initFAQ(); } catch(e) {}
    try { initActiveSectionNav(); } catch(e) {}
    
    // Defer non-critical visual enhancements to improve INP
    // Use requestIdleCallback if available, otherwise setTimeout
    const deferFn = window.requestIdleCallback || function(cb) { setTimeout(cb, 50); };
    
    deferFn(() => {
      try { initHeroParticles(); } catch(e) {}
      try { initScrollReveal(); } catch(e) {}
      try { initCounterAnimation(); } catch(e) {}
      try { initNewAnimations(); } catch(e) {}
      try { initLineDrawAnimation(); } catch(e) {}
      try { initBarGrowthAnimation(); } catch(e) {}
      try { initSparklineDrawAnimation(); } catch(e) {}
      try { initCompBarFillAnimation(); } catch(e) {}
      try { initDonutDrawAnimation(); } catch(e) {}
      try { initSmoothScroll(); } catch(e) {}
      try { initScrollProgress(); } catch(e) {}
      try { initBackToTop(); } catch(e) {}
      try { initSkeletonLoading(); } catch(e) {}
      try { initBarChart(); } catch(e) {}
      try { initComparisonBars(); } catch(e) {}
    });
    
    // Further defer heavy animation libraries
    const deferHeavyFn = window.requestIdleCallback || function(cb) { setTimeout(cb, 200); };
    deferHeavyFn(() => {
      try { initTiltEffect(); } catch(e) {}
      try { initMagneticButtons(); } catch(e) {}
      try { initGSAPHero(); } catch(e) {}
      try { initLenis(); } catch(e) {}
      try { initPerformanceMonitoring(); } catch(e) {}
    });
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
