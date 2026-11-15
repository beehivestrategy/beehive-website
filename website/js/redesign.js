
(function(){
  'use strict';
  /* ---- header shadow on scroll ---- */
  var header=document.getElementById('site-header');
  function onScroll(){ if(header) header.classList.toggle('scrolled', window.scrollY>10); }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();

  /* ---- mobile nav ---- */
  var toggle=document.getElementById('nav-toggle');
  var nav=document.getElementById('nav-desktop');
  if(toggle&&nav){ toggle.addEventListener('click',function(){
    var open=nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded',open?'true':'false');
  }); }

  /* ---- language switcher dropdown ---- */
  var ls=document.getElementById('lang-switcher');
  var lb=document.getElementById('lang-switcher-btn');
  if(ls&&lb){ lb.addEventListener('click',function(e){e.stopPropagation();ls.classList.toggle('open');});
    document.addEventListener('click',function(){ls.classList.remove('open');}); }

  /* ---- scroll reveal ---- */
  var reveals=Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){ en.target.classList.add('visible'); io.unobserve(en.target); }
      });
    },{threshold:0.08,rootMargin:'0px 0px 480px 0px'});
    reveals.forEach(function(el){io.observe(el);});
  } else { reveals.forEach(function(el){el.classList.add('visible');}); }
  /* safety net: reveal anything already in viewport on load */
  window.addEventListener('load',function(){
    reveals.forEach(function(el){
      var r=el.getBoundingClientRect();
      if(r.top<window.innerHeight && r.bottom>0) el.classList.add('visible');
    });
  });

  /* ---- animated counters ---- */
  function animateCount(el){
    var target=parseFloat(el.getAttribute('data-count'));
    if(isNaN(target)) return;
    var dur=1100, start=null, suffix=el.getAttribute('data-suffix')||'';
    function frame(ts){
      if(!start) start=ts;
      var p=Math.min((ts-start)/dur,1);
      var eased=1-Math.pow(1-p,3);
      var val=target*eased;
      el.textContent=(target%1===0? Math.round(val) : val.toFixed(1))+suffix;
      if(p<1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  var counters=Array.prototype.slice.call(document.querySelectorAll('[data-count]'));
  if('IntersectionObserver' in window && counters.length){
    var co=new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){ animateCount(en.target); co.unobserve(en.target); }
      });
    },{threshold:.4});
    counters.forEach(function(el){co.observe(el);});
  } else { counters.forEach(animateCount); }

  /* ---- tabs ---- */
  document.querySelectorAll('[data-tabs]').forEach(function(group){
    var btns=group.querySelectorAll('.tab-btn');
    var panels=group.querySelectorAll('.tab-panel');
    function select(i){
      btns.forEach(function(b,j){
        b.setAttribute('aria-selected', j===i?'true':'false');
        b.setAttribute('tabindex', j===i?'0':'-1');
      });
      panels.forEach(function(p,j){ p.hidden = (j!==i); });
    }
    btns.forEach(function(b,i){
      b.addEventListener('click',function(){select(i);});
      b.addEventListener('keydown',function(e){
        if(e.key==='ArrowRight'){select((i+1)%btns.length);btns[(i+1)%btns.length].focus();}
        if(e.key==='ArrowLeft'){select((i-1+btns.length)%btns.length);btns[(i-1+btns.length)%btns.length].focus();}
      });
    });
    select(0);
  });

  /* ---- accordion ---- */
  document.querySelectorAll('.acc-item').forEach(function(item){
    var head=item.querySelector('.acc-head');
    var body=item.querySelector('.acc-body');
    if(!head||!body) return;
    head.addEventListener('click',function(){
      var isOpen=item.classList.toggle('open');
      head.setAttribute('aria-expanded',isOpen?'true':'false');
      body.style.maxHeight = isOpen ? (body.scrollHeight+'px') : '0px';
    });
    head.setAttribute('aria-expanded','false');
  });
})();
