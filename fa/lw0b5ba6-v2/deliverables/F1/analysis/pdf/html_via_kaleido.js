// Stand-in for plotly.js: lets the headless Chromium bundled with kaleido 0.2.1 (a) print an arbitrary HTML document to PDF and
// (b) rasterise it to PNG for layout checks.  kaleido calls Plotly.toImage(); this file answers that call with our own document.
(function () {
  function b64utf8(s) { return btoa(unescape(encodeURIComponent(s))); }
  function ensureHolder(meta, W) {
    if (window.__holder && window.__holderKey === meta.key) return Promise.resolve(window.__holder);
    if (window.__holder) window.__holder.remove();
    var holder = document.createElement('div');
    holder.setAttribute('xmlns', 'http://www.w3.org/1999/xhtml');
    holder.style.cssText = 'width:' + W + 'px;position:absolute;left:0;top:0;background:white;margin:0;padding:0;';
    holder.innerHTML = meta.html;
    document.body.appendChild(holder);
    window.__holder = holder; window.__holderKey = meta.key;
    var imgs = Array.prototype.slice.call(holder.querySelectorAll('img'));
    return Promise.all(imgs.map(function (im) {
      return new Promise(function (res) { if (im.complete) res(); else { im.onload = res; im.onerror = res; } });
    })).then(function () { return holder; });
  }
  window.Plotly = {
    version: '2.35.0',
    toImage: function (fig, opts) {
      var meta = fig.layout.meta, W = opts.width, H = opts.height, scale = opts.scale || 1;
      if (opts.format === 'svg') {            // kaleido's PDF path: put the document into normal flow and let Chromium print it
        if (window.__holder) { window.__holder.remove(); window.__holder = null; }
        var doc = document.createElement('div'); doc.innerHTML = meta.html; document.body.appendChild(doc); window.__holder = doc; window.__holderKey = null;
        var st = document.createElement('style'); st.textContent = '#kaleido-image{position:absolute;left:0;top:0;width:1px;height:1px;opacity:0;}'; document.head.appendChild(st);
        var imgs2 = Array.prototype.slice.call(doc.querySelectorAll('img'));
        return Promise.all(imgs2.map(function (im) { return new Promise(function (res) { if (im.complete) res(); else { im.onload = res; im.onerror = res; } }); }))
          .then(function () { return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>'); });
      }
      return ensureHolder(meta, W).then(function (holder) {
        var totalH = Math.ceil(holder.getBoundingClientRect().height);
        if (meta.mode === 'measure') {
          var sel = meta.selector || 'h1,h2,h3,p,li,tr,figure,hr,table';
          var els = Array.prototype.slice.call(holder.querySelectorAll(sel)).map(function (e) {
            var r = e.getBoundingClientRect(); return [e.tagName, Math.round(r.top), Math.round(r.bottom), Math.round(r.left), Math.round(r.right)];
          });
          return b64utf8(JSON.stringify({ totalHeight: totalH, width: W, scrollWidth: holder.scrollWidth, elements: els }));
        }
        var off = meta.offset || 0;
        var xml = new XMLSerializer().serializeToString(holder);
        var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H + '">' +
                  '<foreignObject x="0" y="' + (-off) + '" width="' + W + '" height="' + totalH + '">' + xml + '</foreignObject></svg>';
        return new Promise(function (resolve, reject) {
          var img = new Image();
          img.onload = function () {
            try {
              var c = document.createElement('canvas'); c.width = Math.round(W * scale); c.height = Math.round(H * scale);
              var ctx = c.getContext('2d'); ctx.fillStyle = 'white'; ctx.fillRect(0, 0, c.width, c.height); ctx.scale(scale, scale); ctx.drawImage(img, 0, 0);
              resolve(c.toDataURL('image/png').replace(/^data:image\/png;base64,/, ''));
            } catch (e) { reject(e); }
          };
          img.onerror = function () { reject(new Error('svg image failed to load')); };
          img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
        });
      });
    }
  };
})();
