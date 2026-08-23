// ==UserScript==
// @name         Hyperweb Image Finder
// @namespace    Andrew4200
// @version      0.1.0
// @description  Find likely full-size images on the current webpage and show them in a visual grid.
// @match        *://*/*
// ==/UserScript==

(function () {
  'use strict';

  const ID = 'hw-image-finder';
  const MIN_W = 180;
  const MIN_H = 180;
  const BAD = /(^|[/_.-])(icon|logo|avatar|emoji|sprite|favicon|pixel|tracking|spacer)([/_.-]|$)/i;

  const absolute = (url) => {
    try { return new URL(url, location.href).href; } catch (_) { return null; }
  };

  function candidates(img) {
    const out = [];
    const add = (url, score) => {
      url = absolute(url);
      if (url && !url.startsWith('data:') && !url.startsWith('blob:')) out.push({ url, score });
    };

    add(img.currentSrc, 100);
    add(img.src, 90);
    for (const a of ['data-src', 'data-original', 'data-lazy-src', 'data-full', 'data-full-src', 'data-image', 'data-url']) add(img.getAttribute(a), 80);

    const srcset = img.getAttribute('srcset') || img.getAttribute('data-srcset');
    if (srcset) {
      for (const part of srcset.split(',')) {
        const bits = part.trim().split(/\s+/);
        const n = parseFloat(bits[1]) || 1;
        add(bits[0], 70 + Math.min(n, 20));
      }
    }

    const picture = img.closest('picture');
    if (picture) for (const s of picture.querySelectorAll('source[srcset],source[data-srcset]')) {
      for (const part of (s.getAttribute('srcset') || s.getAttribute('data-srcset') || '').split(',')) add(part.trim().split(/\s+/)[0], 75);
    }

    const link = img.closest('a[href]');
    if (link) {
      const href = absolute(link.getAttribute('href'));
      if (href && /\.(?:jpe?g|png|webp|gif|avif|bmp|tiff?)(?:[?#].*)?$/i.test(href)) add(href, 120);
    }
    return out;
  }

  function scan() {
    const map = new Map();
    for (const img of document.images) {
      const r = img.getBoundingClientRect();
      const w = img.naturalWidth || r.width;
      const h = img.naturalHeight || r.height;
      if (w < MIN_W || h < MIN_H) continue;
      const area = Math.min((w * h) / 500000, 4);
      for (const c of candidates(img)) {
        const score = c.score + area * 10 + (BAD.test(c.url) ? -100 : 0);
        const old = map.get(c.url);
        if (!old || score > old.score) map.set(c.url, { ...c, score, w, h });
      }
    }
    return [...map.values()].sort((a, b) => b.score - a.score).slice(0, 200);
  }

  function show(items) {
    document.getElementById(ID)?.remove();
    const root = document.createElement('div');
    root.id = ID;
    root.innerHTML = `<div class="hw-head"><b>Image Finder</b><span>${items.length} candidates</span><button id="hw-copy">Copy URLs</button><button id="hw-close">×</button></div><div class="hw-grid"></div>`;
    const style = document.createElement('style');
    style.textContent = `#${ID}{position:fixed;inset:12px;z-index:2147483647;background:#111;color:#fff;border:1px solid #555;border-radius:12px;box-shadow:0 8px 40px #000;display:flex;flex-direction:column;font:14px -apple-system,BlinkMacSystemFont,sans-serif}#${ID} .hw-head{display:flex;align-items:center;gap:10px;padding:10px 12px;border-bottom:1px solid #444}#${ID} .hw-head span{opacity:.65;flex:1}#${ID} button{background:#333;color:#fff;border:1px solid #666;border-radius:7px;padding:5px 9px}#${ID} .hw-grid{padding:10px;display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;overflow:auto}#${ID} figure{margin:0;background:#222;border-radius:8px;overflow:hidden}#${ID} img{display:block;width:100%;height:150px;object-fit:contain;background:#000}#${ID} figcaption{padding:5px 7px;font-size:11px;opacity:.75;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}`;
    root.prepend(style);
    const grid = root.querySelector('.hw-grid');
    for (const x of items) {
      const fig = document.createElement('figure');
      const a = document.createElement('a');
      a.href = x.url; a.target = '_blank'; a.rel = 'noopener';
      const im = new Image(); im.loading = 'lazy'; im.src = x.url;
      a.appendChild(im); fig.appendChild(a);
      const cap = document.createElement('figcaption'); cap.textContent = `${x.w}×${x.h}  ${new URL(x.url).hostname}`;
      fig.appendChild(cap); grid.appendChild(fig);
    }
    root.querySelector('#hw-close').onclick = () => root.remove();
    root.querySelector('#hw-copy').onclick = async () => {
      await navigator.clipboard?.writeText(items.map(x => x.url).join('\n'));
      root.querySelector('#hw-copy').textContent = 'Copied';
    };
    document.documentElement.appendChild(root);
  }

  function run() { show(scan()); }

  const button = document.createElement('button');
  button.textContent = 'Find Images';
  Object.assign(button.style, { position:'fixed', bottom:'18px', right:'18px', zIndex:2147483646, padding:'10px 14px', borderRadius:'999px', border:'1px solid #777', background:'#111', color:'#fff', font:'600 14px -apple-system,BlinkMacSystemFont,sans-serif', boxShadow:'0 4px 16px #0008' });
  button.onclick = run;
  document.documentElement.appendChild(button);
})();
