/* مدرسه شهدای ادب — static/js/main.js (Vanilla JS، بدون وابستگی) */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- سال شمسی فوتر ---------- */
  try {
    const y = new Intl.DateTimeFormat('fa-IR-u-ca-persian', { year: 'numeric' }).format(new Date());
    const el = $('#year'); if (el) el.textContent = y;
  } catch (e) { /* مقدار پیش‌فرض می‌ماند */ }

  /* ---------- جایگزین تصویر ---------- */
  const markMissing = img => img.closest('.media')?.classList.add('is-missing');
  $$('.media img').forEach(img => {
    if (img.complete && img.naturalWidth === 0) markMissing(img);
    img.addEventListener('error', () => markMissing(img));
  });

  /* ---------- هدر چسبان ---------- */
  const header = $('#siteHeader');
  if (header) {
    const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- برگهٔ «بیشتر» (منوی موبایل) ---------- */
  const sheet = $('#menuSheet');
  const toggles = $$('[data-menu-toggle]');
  let menuOpener = null;
  const setMenu = open => {
    if (!sheet) return;
    sheet.classList.toggle('is-open', open);
    sheet.setAttribute('aria-hidden', String(!open));
    toggles.forEach(t => t.setAttribute('aria-expanded', String(open)));
    document.body.classList.toggle('is-locked', open);
    if (open) setTimeout(() => $('a', sheet)?.focus(), 60);
    else if (menuOpener) { menuOpener.focus(); menuOpener = null; }
  };
  toggles.forEach(t => t.addEventListener('click', () => {
    const willOpen = !sheet.classList.contains('is-open');
    if (willOpen) menuOpener = t;
    setMenu(willOpen);
  }));
  if (sheet) {
    $$('[data-menu-close]', sheet).forEach(el => el.addEventListener('click', () => setMenu(false)));
    $$('a', sheet).forEach(a => a.addEventListener('click', () => { menuOpener = null; setMenu(false); }));
  }
  window.matchMedia('(min-width: 1024px)').addEventListener('change', e => { if (e.matches) setMenu(false); });

  /* ---------- لینک فعال بر اساس اسکرول ---------- */
  const spyLinks = $$('[data-spy]');
  const spyTargets = ['top', 'about', 'news', 'achievements', 'gallery', 'contact']
    .map(id => document.getElementById(id)).filter(Boolean);
  if ('IntersectionObserver' in window && spyTargets.length) {
    const spy = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        spyLinks.forEach(a => {
          if (a.hash === '#' + en.target.id) a.setAttribute('aria-current', 'page');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    spyTargets.forEach(s => spy.observe(s));
  }

  /* ---------- نمایش تدریجی بخش‌ها (یک‌بار) ---------- */
  const reveals = $$('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-visible'); obs.unobserve(en.target); } });
    }, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => io.observe(el));
  } else reveals.forEach(el => el.classList.add('is-visible'));

  /* ---------- جستجو ---------- */
  const search = $('#search');
  if (!search) return;
  const input = $('#searchInput');
  const clearBtn = $('#searchClear');
  const form = $('#searchForm');
  const suggest = $('#searchSuggest');
  const results = $('#searchResults');
  const states = { loading: $('#stLoading'), empty: $('#stEmpty'), error: $('#stError') };
  const endpoint = document.body.dataset.searchEndpoint;
  let lastFocus = null, timer = null, controller = null;

  const showState = name => {
    Object.entries(states).forEach(([k, el]) => el.classList.toggle('is-visible', k === name));
    suggest.hidden = name !== 'idle';
    results.replaceChildren();
  };
  const openSearch = () => {
    lastFocus = document.activeElement;
    setMenu(false);
    search.classList.add('is-open');
    search.setAttribute('aria-hidden', 'false');
    document.body.classList.add('is-locked');
    setTimeout(() => input.focus(), 60);
  };
  const closeSearch = () => {
    search.classList.remove('is-open');
    search.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('is-locked');
    controller?.abort();
    lastFocus?.focus();
  };
  const renderResults = items => {
    results.replaceChildren(...items.map(it => {
      const a = document.createElement('a');
      a.className = 'result'; a.href = it.url || '#';
      const t = document.createElement('span'); t.className = 'result__type'; t.textContent = it.type || '';
      const h = document.createElement('span'); h.className = 'result__title'; h.textContent = it.title || '';
      const s = document.createElement('span'); s.className = 'result__summary'; s.textContent = it.summary || '';
      a.append(t, h, s); return a;
    }));
    suggest.hidden = true;
    Object.values(states).forEach(el => el.classList.remove('is-visible'));
  };
  // خروجی مورد انتظار از Django: { "results": [ { "title", "url", "type", "summary" } ] }
  const runSearch = async q => {
    if (!q) { showState('idle'); return; }
    if (!endpoint) { $('#stErrorText').textContent = 'سرویس جستجو هنوز به سایت متصل نشده است.'; showState('error'); return; }
    controller?.abort(); controller = new AbortController();
    showState('loading');
    try {
      const res = await fetch(`${endpoint}?q=${encodeURIComponent(q)}`, { signal: controller.signal, headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error('bad status');
      const data = await res.json();
      const items = Array.isArray(data.results) ? data.results : [];
      items.length ? renderResults(items) : showState('empty');
    } catch (err) {
      if (err.name !== 'AbortError') { $('#stErrorText').textContent = 'خطایی رخ داد. لطفاً دوباره تلاش کنید.'; showState('error'); }
    }
  };
  const onInput = () => {
    clearBtn.classList.toggle('is-visible', input.value.length > 0);
    clearTimeout(timer);
    timer = setTimeout(() => runSearch(input.value.trim()), 300);
  };

  $$('[data-search-open]').forEach(b => b.addEventListener('click', openSearch));
  $('#searchClose').addEventListener('click', closeSearch);
  search.addEventListener('click', e => { if (e.target === search) closeSearch(); });
  input.addEventListener('input', onInput);
  form.addEventListener('submit', e => { e.preventDefault(); clearTimeout(timer); runSearch(input.value.trim()); });
  clearBtn.addEventListener('click', () => { input.value = ''; onInput(); input.focus(); });
  $$('[data-suggest]').forEach(c => c.addEventListener('click', () => { input.value = c.dataset.suggest; onInput(); input.focus(); }));
  showState('idle');

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (search.classList.contains('is-open')) { closeSearch(); return; }
      if (sheet?.classList.contains('is-open')) { setMenu(false); return; }
    }
    if (e.key === 'Tab' && search.classList.contains('is-open')) {
      const f = $$('button, input, a[href]', search).filter(el => !el.hidden && el.offsetParent !== null);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
})();
