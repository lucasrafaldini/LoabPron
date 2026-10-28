(function () {
  'use strict';
  var doc = document;
  function el(t, c, p) { var e = doc.createElement(t); if (c) e.className = c; if (p) p.appendChild(e); return e; }
  function pct(v, d) { return (v == null ? d : v) + '%'; }
  var LANG = (function () {
    try { var s = localStorage.getItem('loab-lang'); if (s && I18N[s]) return s; } catch (e) { /* sem storage */ }
    return /^pt/i.test(navigator.language || '') ? 'pt' : 'en';
  })();
  function L(k) { return I18N[LANG][k]; }
  function fmt(s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k] != null ? o[k] : ''; }); }
  var NAME = '', ACC = '', JOKES = [];  // /api/presence: nome de pessoa, ou conta compartilhada e piadas sobre ela

  /* ---------- DOM ---------- */
  var B = doc.body;
  var root = el('div', 'root', B), hd = el('div', 'hd', root), stage = el('div', 'stage', root);
  var frm = el('form', 'frm', root), inp = el('input', 'pw', frm), btn = el('button', 'go', frm);
  var wb = el('div', 'wb', root), ot = el('button', 'ot', root), mt = el('button', 'mt', B);
  inp.type = 'text'; inp.autocomplete = 'off'; inp.spellcheck = false; inp.autofocus = true;
  btn.type = 'submit'; ot.type = 'button';
  mt.type = 'button'; mt.textContent = '\u266a';

  var oc = el('div', 'oc hide', B), och = el('div', 'och', oc), ocb = el('div', 'ocb', oc), oci = el('form', 'oci', oc);
  var ocq = el('input', '', oci), ocs = el('button', '', oci), ocx = el('button', '', och);
  el('span', '', och);
  och.insertBefore(och.lastChild, ocx);
  ocx.type = 'button'; ocx.textContent = '\u2715'; ocs.type = 'submit'; ocs.textContent = '>';
  ocq.autocomplete = 'off'; ocq.spellcheck = false;
  var ocHello = el('div', '', ocb), ocTitle = och.firstChild;
  function applyLang(l) {
    LANG = l; DE.lang = l === 'pt' ? 'pt-BR' : 'en';
    try { localStorage.setItem('loab-lang', l); } catch (e) { /* sem storage */ }
    ot.textContent = L('oracle'); ocTitle.textContent = L('mirror'); ocq.placeholder = L('mirrorPh');
    ocHello.textContent = L('mirrorHello'); btn.textContent = L('enter'); inp.placeholder = ph = L('password');
  }

  var prog = 0, playing = false;
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE = window.matchMedia && matchMedia('(pointer: fine)').matches;
  el('div', 'crt', B); el('div', 'roll', B);
  var HER = '/static/img/7f4eab87de.jpg';  // ela: a aparicao recorrente (tools/aparicao.py)
  var GHOSTS = [HER, HER, HER, '/static/img/82f58cc804.jpg', '/static/img/73d893fec0.jpg', '/static/img/7c6ac70649.jpg'];
  GHOSTS.forEach(function (u) { new Image().src = u; });

  /* ---------- vento ---------- */
  var Snd = (function () {
    var ctx, master, gWind, gDrone, gChoir, started = false, muted = false;
    function brown(c) {
      var n = c.sampleRate * 4, b = c.createBuffer(1, n, c.sampleRate), d = b.getChannelData(0), l = 0;
      for (var i = 0; i < n; i++) { var w = Math.random() * 2 - 1; l = (l + 0.02 * w) / 1.02; d[i] = l * 3.5; }
      return b;
    }
    function lfo(param, hz, depth) {
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.frequency.value = hz; g.gain.value = depth; o.connect(g); g.connect(param); o.start();
    }
    function start() {
      if (started) { if (ctx.state === 'suspended') ctx.resume(); return; }
      var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
      ctx = new AC(); started = true;
      master = ctx.createGain(); master.gain.value = muted ? 0 : 0.6; master.connect(ctx.destination);
      var buf = brown(ctx);
      var s1 = ctx.createBufferSource(); s1.buffer = buf; s1.loop = true;
      var f1 = ctx.createBiquadFilter(); f1.type = 'bandpass'; f1.frequency.value = 380; f1.Q.value = 0.9;
      gWind = ctx.createGain(); gWind.gain.value = 0.45;
      s1.connect(f1); f1.connect(gWind); gWind.connect(master); s1.start();
      lfo(f1.frequency, 0.06, 220); lfo(gWind.gain, 0.045, 0.22);
      var s2 = ctx.createBufferSource(); s2.buffer = buf; s2.loop = true; s2.playbackRate.value = 1.7;
      var f2 = ctx.createBiquadFilter(); f2.type = 'bandpass'; f2.frequency.value = 1150; f2.Q.value = 9;
      var g2 = ctx.createGain(); g2.gain.value = 0.05;
      s2.connect(f2); f2.connect(g2); g2.connect(master); s2.start();
      lfo(f2.frequency, 0.03, 320); lfo(g2.gain, 0.11, 0.04);
      gDrone = ctx.createGain(); gDrone.gain.value = 0.05; gDrone.connect(master);
      [[48, 'sine'], [72.4, 'triangle'], [96.3, 'sine']].forEach(function (p) {
        var o = ctx.createOscillator(); o.type = p[1]; o.frequency.value = p[0]; o.connect(gDrone); o.start();
      });
      lfo(gDrone.gain, 0.05, 0.025);
      gChoir = ctx.createGain(); gChoir.gain.value = 0; gChoir.connect(master);
      [110, 130.8, 164.8, 174.6].forEach(function (f, i) {
        var o = ctx.createOscillator(); o.type = 'sawtooth'; o.frequency.value = f * 0.5; o.detune.value = i * 7 - 10;
        var lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 520;
        o.connect(lp); lp.connect(gChoir); o.start(); lfo(o.frequency, 4.6 + i * 0.3, 1.2);
      });
      (function thud() {
        setTimeout(function () {
          if (!muted && ctx.state === 'running') {
            var o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime;
            o.frequency.value = 38; g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.35, t + 0.05);
            g.gain.exponentialRampToValueAtTime(0.0001, t + 1.6); o.connect(g); g.connect(master); o.start(t); o.stop(t + 1.7);
          }
          thud();
        }, 18000 + Math.random() * 24000);
      })();
    }
    function ramp(p, v, s) { if (p) p.linearRampToValueAtTime(v, ctx.currentTime + s); }
    return {
      start: start,
      level: function (r) { if (!started) return; ramp(gWind.gain, 0.35 + r * 0.55, 3); ramp(gDrone.gain, 0.04 + r * 0.08, 3); ramp(gChoir.gain, r > 0.85 ? 0.05 : 0, 4); },
      tone: function (f, d, type, v) {
        if (!started || muted) return;
        var o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime;
        o.type = type || 'sine'; o.frequency.value = f; g.gain.setValueAtTime(v || 0.08, t);
        g.gain.exponentialRampToValueAtTime(0.0001, t + d); o.connect(g); g.connect(master); o.start(t); o.stop(t + d);
      },
      toggle: function () { muted = !muted; if (master) master.gain.value = muted ? 0 : 0.6; return muted; },
      isMuted: function () { return muted; },
      morse: function (code) {
        if (!started || muted) return 0;
        var u = 0.085, t = ctx.currentTime + 0.1, g = ctx.createGain(), o = ctx.createOscillator();
        o.frequency.value = 640; g.gain.value = 0; o.connect(g); g.connect(master);
        code.split('').forEach(function (c) {
          if (c === '.' || c === '-') {
            var d = c === '.' ? u : 3 * u;
            g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.16, t + 0.005);
            g.gain.setValueAtTime(0.16, t + d - 0.005); g.gain.linearRampToValueAtTime(0, t + d); t += d + u;
          } else t += c === '/' ? 4 * u : 2 * u;
        });
        o.start(); o.stop(t + 0.1);
        return (t - ctx.currentTime) * 1000;
      },
      hum: (function () {
        var timer = null;
        function one() {
          if (!started || muted || ctx.state !== 'running') return;
          var o = ctx.createOscillator(), f = ctx.createBiquadFilter(), g = ctx.createGain(), t = ctx.currentTime;
          o.type = 'sawtooth'; o.frequency.value = 118; f.type = 'lowpass'; f.frequency.value = 900;
          g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.06, t + 0.03); g.gain.setValueAtTime(0.06, t + 0.85); g.gain.linearRampToValueAtTime(0, t + 0.9);
          o.connect(f); f.connect(g); g.connect(master); o.start(t); o.stop(t + 0.95);
        }
        return function (on) { clearInterval(timer); timer = on ? setInterval(one, 1900) : null; if (on) one(); };
      })(),
      on: function () { return started; },
      whisper: (function () {
        var white = null, VOW = [[700, 1150], [480, 1750], [300, 2300], [450, 880], [340, 720]];
        return function () {
          if (!started || muted || ctx.state !== 'running') return;
          if (!white) {
            white = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
            var d = white.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
          }
          var t = ctx.currentTime, tt = t, n = 4 + Math.floor(Math.random() * 8);
          var src = ctx.createBufferSource(); src.buffer = white; src.loop = true;
          var f1 = ctx.createBiquadFilter(), f2 = ctx.createBiquadFilter(), g = ctx.createGain();
          f1.type = f2.type = 'bandpass'; f1.Q.value = 5; f2.Q.value = 7; g.gain.value = 0;
          src.connect(f1); src.connect(f2); f1.connect(g); f2.connect(g);
          var out = g;
          if (ctx.createStereoPanner) { var pn = ctx.createStereoPanner(); pn.pan.value = (Math.random() < 0.5 ? -1 : 1) * (0.5 + Math.random() * 0.5); g.connect(pn); out = pn; }
          out.connect(master);
          for (var k = 0; k < n; k++) {
            var v = VOW[Math.floor(Math.random() * VOW.length)], dd = 0.07 + Math.random() * 0.17;
            f1.frequency.setValueAtTime(v[0], tt); f2.frequency.setValueAtTime(v[1], tt);
            g.gain.setValueAtTime(0, tt); g.gain.linearRampToValueAtTime(0.22 + Math.random() * 0.18, tt + dd * 0.3);
            g.gain.linearRampToValueAtTime(0, tt + dd); tt += dd + (Math.random() < 0.2 ? 0.2 : 0.03);
          }
          src.start(t); src.stop(tt + 0.1);
        };
      })(),
      sigh: function () {  // um suspiro de verdade: inspira curto, solta longo, o tom cai
        if (!started || muted || ctx.state !== 'running') return;
        var t = ctx.currentTime, s = ctx.createBufferSource(), lp = ctx.createBiquadFilter(), bp = ctx.createBiquadFilter(), g = ctx.createGain();
        s.buffer = brown(ctx); s.playbackRate.value = 2.2; lp.type = 'lowpass'; bp.type = 'bandpass'; bp.Q.value = 1.4;
        lp.frequency.setValueAtTime(900, t); lp.frequency.linearRampToValueAtTime(1500, t + 0.5); lp.frequency.exponentialRampToValueAtTime(320, t + 2.2);
        bp.frequency.setValueAtTime(700, t); bp.frequency.exponentialRampToValueAtTime(380, t + 2.2);
        g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.12, t + 0.35); g.gain.linearRampToValueAtTime(0.03, t + 0.55);
        g.gain.linearRampToValueAtTime(0.32, t + 0.75); g.gain.exponentialRampToValueAtTime(0.0001, t + 2.3);
        var out = g;
        if (ctx.createStereoPanner) { var pn = ctx.createStereoPanner(); pn.pan.value = Math.random() * 1.6 - 0.8; g.connect(pn); out = pn; }
        s.connect(lp); lp.connect(bp); bp.connect(g); out.connect(master); s.start(t); s.stop(t + 2.4);
      },
      scrape: function () {
        if (!started || muted) return;
        var t = ctx.currentTime, s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
        s.buffer = brown(ctx); s.playbackRate.value = 4; f.type = 'bandpass'; f.frequency.value = 2400; f.Q.value = 3;
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.25, t + 0.04); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.28);
        s.connect(f); f.connect(g); g.connect(master); s.start(t); s.stop(t + 0.3);
      },
      heart: (function () {
        var bpm = 0, vol = 0.5, timer = null;
        function beat(t, v) {
          var o = ctx.createOscillator(), g = ctx.createGain();
          o.frequency.setValueAtTime(62, t); o.frequency.exponentialRampToValueAtTime(34, t + 0.16);
          g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + 0.015); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.22);
          o.connect(g); g.connect(master); o.start(t); o.stop(t + 0.25);
        }
        function loop() {
          if (!bpm) { timer = null; return; }
          if (!muted && ctx.state === 'running') {
            var t = ctx.currentTime; beat(t, vol); beat(t + 0.19, vol * 0.65);
            if (bpm > 110 && Math.random() < 0.25) beat(t + 0.42, vol * 0.4);  // arritmia perto do fim
          }
          timer = setTimeout(loop, (60000 / bpm) * (bpm > 100 ? 0.9 + Math.random() * 0.2 : 1));
        }
        return function (b, v) { bpm = b; if (v) vol = v; if (started && bpm && !timer) loop(); };
      })(),
      noise: function (d, v) {
        if (!started || muted) return;
        var s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain(), t = ctx.currentTime;
        s.buffer = brown(ctx); s.playbackRate.value = 3; f.type = 'highpass'; f.frequency.value = 900;
        g.gain.setValueAtTime(v || 0.5, t); g.gain.exponentialRampToValueAtTime(0.0001, t + d);
        s.connect(f); f.connect(g); g.connect(master); s.start(t); s.stop(t + d);
      },
      scream: function () {
        if (!started) return;
        var t = ctx.currentTime;
        ramp(gChoir.gain, 0.22, 3);
        setTimeout(function () {
          var c = ctx.currentTime, sh = ctx.createWaveShaper(), k = new Float32Array(256);
          for (var i = 0; i < 256; i++) { var x = i / 128 - 1; k[i] = Math.tanh(x * 4); }
          sh.curve = k;
          var g = ctx.createGain(); g.gain.setValueAtTime(0, c); g.gain.linearRampToValueAtTime(0.28, c + 0.25);
          g.gain.exponentialRampToValueAtTime(0.0001, c + 2.6);
          sh.connect(g); g.connect(master);
          [['sawtooth', 1], ['square', 1.5]].forEach(function (p) {
            var o = ctx.createOscillator(); o.type = p[0];
            o.frequency.setValueAtTime(380 * p[1], c); o.frequency.exponentialRampToValueAtTime(1900 * p[1], c + 1.1);
            o.frequency.exponentialRampToValueAtTime(240 * p[1], c + 2.5); o.connect(sh); o.start(c); o.stop(c + 2.7);
          });
          var ns = ctx.createBufferSource(); ns.buffer = brown(ctx); var nf = ctx.createBiquadFilter(); nf.type = 'highpass'; nf.frequency.value = 1800;
          ns.connect(nf); nf.connect(g); ns.start(c); ns.stop(c + 2.6);
        }, 3200);
        setTimeout(function () { ramp(gChoir.gain, 0, 3); ramp(gWind.gain, 0.05, 6); ramp(gDrone.gain, 0.0, 6); }, 6800);
        return t;
      }
    };
  })();
  ['pointerdown', 'keydown'].forEach(function (ev) { doc.addEventListener(ev, function () { Snd.start(); }, { once: false, passive: true }); });
  mt.addEventListener('click', function () { Snd.start(); mt.style.opacity = Snd.toggle() ? 0.4 : 1; });

  /* ---------- tela cheia ---------- */
  var DE = doc.documentElement, reqFs = DE.requestFullscreen || DE.webkitRequestFullscreen;
  var fsb = el('button', 'mt fsb', B); fsb.type = 'button'; fsb.textContent = '\u26f6';
  if (!reqFs) fsb.style.display = 'none';
  function isFs() { return !!(doc.fullscreenElement || doc.webkitFullscreenElement); }
  function fullscreen(on) {
    try {
      if (on && !isFs() && reqFs) { var pr = reqFs.call(DE); if (pr && pr.catch) pr.catch(function () {}); }
      else if (!on && isFs()) (doc.exitFullscreen || doc.webkitExitFullscreen).call(doc);
    } catch (e) { /* navegador recusou: segue em janela */ }
  }
  function onFs() {
    var on = isFs(); B.classList.toggle('fsm', on);
    setTimeout(function () { stage.style.setProperty('--u', (stage.clientWidth / 640) + 'px'); }, 80);
    if (!on && playing && !busy) { wb.style.color = '#5a5a5a'; wb.textContent = L('window'); }
  }
  doc.addEventListener('fullscreenchange', onFs); doc.addEventListener('webkitfullscreenchange', onFs);
  fsb.addEventListener('click', function () { fullscreen(!isFs()); inp.focus(); });

  /* ---------- cena ---------- */
  var grainTimer = null;
  function grain(parent) {
    var c = el('canvas', 'gr', parent); c.width = 160; c.height = 107;
    var x = c.getContext('2d'), im = x.createImageData(160, 107);
    function draw() {
      for (var i = 0; i < im.data.length; i += 4) { var v = Math.random() * 255; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
      x.putImageData(im, 0, 0);
    }
    draw(); clearInterval(grainTimer); grainTimer = setInterval(draw, 110);
  }

  function place(e, L) {
    e.style.left = pct(L.x, 0); e.style.top = pct(L.y, 0);
    if (L.k !== 'tape') { e.style.width = pct(L.w, 100); e.style.height = pct(L.h, 100); }
    if (L.r != null) e.style.setProperty('--r', L.r + 'deg');
    if (L.o != null) { e.style.opacity = L.o; e.style.setProperty('--o', L.o); }
    if (L.f) e.style.filter = L.f;
    if (L.m) e.style.mixBlendMode = L.m;
    if (L.c) e.style.clipPath = L.c;
    if (L.a) e.classList.add('a-' + L.a);
  }

  function layer(L, parent) {
    var e, k = L.k || 'img';
    if (k === 'tape') e = el('div', 'tp', parent);
    else if (k === 'box') { e = el('div', 'bx', parent); e.style.background = L.bg; }
    else {
      e = el('div', 'l' + (L.fr ? ' fr' : ''), parent);
      if (k === 'svg') e.innerHTML = L.svg;
      if (L.i) e.style.backgroundImage = 'url(/static/img/' + L.i + ')';
      if (L.bg) e.style.background = L.bg;
      if (L.bs) e.style.backgroundSize = L.bs;
      if (L.bp) e.style.backgroundPosition = L.bp;
    }
    place(e, L);
    if (k === 'grp' && L.kids) L.kids.forEach(function (c) { layer(c, e); });
    return e;
  }

  var commentNode = null, sigilNode = null, sigil = '';
  function paint(sc, comment) {
    stage.innerHTML = '';
    stage.style.setProperty('--u', (stage.clientWidth / 640) + 'px');
    (sc.layers || []).forEach(function (L) { layer(L, stage); });
    (sc.caps || []).forEach(function (C) {
      var e = el('div', 'cp ' + (C.ff || 'm') + (C.bd ? ' bd' : ''), stage);
      e.textContent = (LANG === 'en' && C.en) || C.t; e.style.left = C.x + '%'; e.style.top = C.y + '%';
      e.style.setProperty('--s', C.s || 14); e.style.color = C.k || '#ccc';
      if (C.ls) e.style.letterSpacing = C.ls + 'px';
      if (C.r != null) e.style.setProperty('--r', C.r + 'deg');
      if (C.o != null) { e.style.opacity = C.o; e.style.setProperty('--o', C.o); }
      if (C.a) e.classList.add('a-' + C.a);
    });
    var fx = sc.fx || [];
    if (fx.indexOf('gr') > -1) grain(stage);
    if (fx.indexOf('sc') > -1) el('div', 'sc', stage);
    if (fx.indexOf('vg') > -1) el('div', 'vg', stage);
    if (prog > 0.5 && FINE) { var dk = el('div', 'dk', stage); dk.style.setProperty('--dk', Math.min(0.82, 0.3 + (prog - 0.5) * 1.1)); }
    if (commentNode && commentNode.parentNode) commentNode.parentNode.removeChild(commentNode);
    commentNode = doc.createComment(' ' + comment + ' '); B.appendChild(commentNode);
    if (sigilNode) { sigilNode.remove(); sigilNode = null; }
    if (sigil) {  // escondido no DOM: so quem inspeciona encontra
      sigilNode = el('div', '', B); sigilNode.id = 'sigillum'; sigilNode.hidden = true; sigilNode.innerHTML = sigil;
      B.appendChild(doc.createComment(' sigillum · vii · ∴ '));
    }
  }
  window.addEventListener('resize', function () { stage.style.setProperty('--u', (stage.clientWidth / 640) + 'px'); });
  doc.addEventListener('pointermove', function (ev) {
    var r = stage.getBoundingClientRect();
    stage.style.setProperty('--mx', ((ev.clientX - r.left) / r.width * 100) + '%');
    stage.style.setProperty('--my', ((ev.clientY - r.top) / r.height * 100) + '%');
  }, { passive: true });
  setInterval(function () {
    if (RM) return;
    var ls = stage.querySelectorAll('.l'), cs = stage.querySelectorAll('.cp');
    if (ls.length) { var e = ls[Math.floor(Math.random() * ls.length)]; e.classList.add('gl'); setTimeout(function () { e.classList.remove('gl'); }, 200); }
    if (cs.length && Math.random() < prog + 0.2) { var c = cs[Math.floor(Math.random() * cs.length)]; c.classList.add('ca'); setTimeout(function () { c.classList.remove('ca'); }, 160); }
  }, 5200);

  /* ---------- a casa observa ---------- */
  var lastAct = Date.now(), lastKey = 0, ghost = null, haunting = false, ph = 'password';
  var nextFlash = Date.now() + 90000 + Math.random() * 90000, nextHaunt = Date.now() + 35000 + Math.random() * 30000;
  function rnd(a) { return a[Math.floor(Math.random() * a.length)]; }
  function post(path, body) {
    return fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(function (r) { return r.json(); });
  }
  function flash(ms, kind) {
    if (RM || doc.hidden) return;
    var f = el('div', 'flash', B), r = Math.random();
    if (kind === 'sigil' || (sigil && r < 0.5)) { f.className = 'flash fs'; f.innerHTML = sigil; }
    else if (kind === 'name' || ((NAME || ACC) && r < 0.18)) { f.className = 'flash fw'; f.textContent = (NAME || ACC).toUpperCase() + (ACC ? '?' : ''); }
    else if (r < 0.35) { f.className = 'flash fw'; f.textContent = rnd(L('flash')); }
    else f.style.backgroundImage = 'url(' + rnd(GHOSTS) + ')';
    Snd.noise(0.25, 0.35); setTimeout(function () { B.removeChild(f); }, ms || 70);
  }
  /* ela aparece de relance nas bordas: nunca no centro, nunca por muito tempo */
  function vulto(strong) {
    if (RM || doc.hidden) return;
    var v = el('div', 'vulto', B), left = Math.random() < 0.5;
    v.style.backgroundImage = 'url(' + HER + ')';
    v.style[left ? 'left' : 'right'] = (-8 - Math.random() * 10) + 'vw';
    v.style.setProperty('--vo', strong ? 0.55 : 0.18 + Math.random() * 0.14);
    if (!left) v.style.transform = 'scaleX(-1)';
    if (Math.random() < 0.5) (Math.random() < 0.5 ? Snd.sigh : Snd.whisper)();
    setTimeout(function () { v.remove(); }, 2600);
  }
  function eyes() {
    var R = root.getBoundingClientRect(), w = innerWidth, h = innerHeight;
    for (var n = 0; n < 12; n++) {
      var x = 20 + Math.random() * (w - 60), y = 20 + Math.random() * (h - 40);
      if (x > R.left - 40 && x < R.right && y > R.top - 20 && y < R.bottom) continue;
      var e = el('div', 'eyes', B); e.style.left = x + 'px'; e.style.top = y + 'px';
      setTimeout(function () { if (e.parentNode) B.removeChild(e); }, 2700); return;
    }
  }

  /* o campo de senha como prancheta: alguem escreve por voce */
  function ghostLine() {
    if (NAME && prog > 0.15 && Math.random() < 0.3) return fmt(rnd(L('ghostName')), { name: NAME });
    if (JOKES.length && Math.random() < 0.3) return rnd(JOKES);
    return rnd(L('ghost'));
  }
  function stopGhost() {
    if (!ghost) return;
    clearTimeout(ghost.t); inp.value = ghost.restore; inp.placeholder = ph; inp.classList.remove('gh'); ghost = null;
  }
  function ghostWrite(text, hold) {
    if (ghost || busy) return;
    var base = inp.value, start = text.indexOf(base) === 0 ? base.length : 0;
    ghost = { restore: base, t: null }; inp.placeholder = ''; inp.classList.add('gh');
    if (!start) inp.value = '';
    var i = start;
    (function step() {
      if (!ghost) return;
      if (i <= text.length) {
        inp.value = text.slice(0, i++);
        ghost.t = setTimeout(step, (Math.random() < 0.12 ? 420 : 70) + Math.random() * 150); return;
      }
      ghost.t = setTimeout(function back() {
        if (!ghost) return;
        if (inp.value.length > ghost.restore.length) { inp.value = inp.value.slice(0, -1); ghost.t = setTimeout(back, 40); return; }
        var g = ghost; ghost = null; inp.value = g.restore; inp.placeholder = ph; inp.classList.remove('gh');
        lastAct = Date.now() - 15000;  // o silencio volta a contar, mas a casa nao repete na hora
      }, hold || 1800);
    })();
  }
  function wake(ev) {
    lastAct = Date.now(); if (ev.type === 'keydown') lastKey = Date.now();
    stopGhost();
  }
  ['keydown', 'pointerdown'].forEach(function (ev) { doc.addEventListener(ev, wake, true); });

  /* tabuleiro ouija: a prancheta soletra sobre a cena */
  var board = null, spots = {};
  function buildBoard() {
    board = el('div', 'ouija', stage);
    function put(ch, x, y, cls) { var s = el('div', 'ol' + (cls ? ' ' + cls : ''), board); s.textContent = ch; s.setAttribute('data-c', ch); s.style.left = x + '%'; s.style.top = y + '%'; spots[ch] = [x, y]; }
    var A = 'ABCDEFGHIJKLM', Z = 'NOPQRSTUVWXYZ', i;
    for (i = 0; i < 13; i++) { var t = i / 12; put(A[i], 12 + t * 76, 40 - Math.sin(Math.PI * t) * 14); put(Z[i], 14 + t * 72, 58 - Math.sin(Math.PI * t) * 11); }
    for (i = 0; i < 10; i++) put('1234567890'[i], 27 + i * 5.2, 74);
    put(L('yes'), 14, 14, 'ow'); put(L('no'), 86, 14, 'ow'); put(L('bye'), 50, 89, 'ow');
    spots[' '] = [50, 50];
    board.pl = el('div', 'pl', board);
  }
  function ouija(word, done) {
    if (RM || haunting || mode === 'pin') { if (done) done(); return; }
    haunting = true;
    if (!board || !board.parentNode) buildBoard();
    var r0 = Math.random();
    word = (word || (r0 < 0.15 ? hour().replace(':', '') : NAME && r0 < 0.4 ? NAME : rnd(L('ouija'))))
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/[^A-Z0-9 ]/g, '').slice(0, 10);
    board.classList.add('on'); Snd.sigh();
    var seq = word.split(''), k = 0, pl = board.pl, lit = null;
    function go(p, fast) {  // arranco: rapido demais, passa do ponto e volta
      pl.style.transition = fast ? 'left .12s cubic-bezier(.9,0,.3,1.6),top .12s cubic-bezier(.9,0,.3,1.6)' : 'left .28s cubic-bezier(.85,0,.25,1.5),top .28s cubic-bezier(.85,0,.25,1.5)';
      pl.style.left = p[0] + '%'; pl.style.top = (p[1] + 4) + '%'; Snd.scrape();
    }
    go([50, 46]);
    (function hop() {
      if (lit) lit.classList.remove('hit');
      if (k >= seq.length) {
        go(spots[L('bye')]);
        setTimeout(function () { go([110, -20], true); }, 1400);  // a prancheta e arrancada do tabuleiro
        setTimeout(function () { board.classList.remove('on'); haunting = false; if (done) done(); }, 1700);
        return;
      }
      var ch = seq[k++], p = spots[ch] || spots[' '];
      if (Math.random() < 0.2 && ch !== ' ') {  // hesita numa letra errada antes
        var keys = Object.keys(spots); go(spots[rnd(keys)], true);
        setTimeout(function () { go(p); }, 260);
      } else go(p);
      setTimeout(function () {
        lit = board.querySelector('.ol[data-c="' + ch + '"]'); if (lit) lit.classList.add('hit');
        Snd.tone(52, 0.5, 'sine', 0.18);
        setTimeout(hop, 500 + Math.random() * 1100);
      }, 420);
    })();
  }

  /* o mouse e tomado: o cursor escreve sozinho e devolve o controle */
  var mx = innerWidth / 2, my = innerHeight / 2;
  doc.addEventListener('pointermove', function (ev) { mx = ev.clientX; my = ev.clientY; }, { passive: true });
  function possess(text) {
    if (!FINE || RM || haunting) return;
    haunting = true;
    var lay = el('div', 'pos', B), w = el('div', 'pw2', lay), cur = el('div', 'fcur', lay);
    w.textContent = text || (NAME && Math.random() < 0.3 ? NAME : ACC && Math.random() < 0.3 ? ACC + '?' : rnd(L('possess')));
    var R = root.getBoundingClientRect();
    var x = Math.max(20, Math.min(innerWidth - 360, R.left + Math.random() * Math.max(40, R.width - 300)));
    var y = R.top + R.height * (0.2 + Math.random() * 0.4);
    w.style.left = x + 'px'; w.style.top = y + 'px';
    cur.style.left = mx + 'px'; cur.style.top = my + 'px';
    B.classList.add('noc');
    setTimeout(function () { cur.style.transition = 'left .35s ease-in,top .35s ease-in'; cur.style.left = x + 'px'; cur.style.top = (y + 30) + 'px'; }, 30);
    setTimeout(function () {
      var wr = w.getBoundingClientRect(), t0 = Date.now(), dur = 900 + wr.width * 2;
      w.classList.add('wr'); w.style.animationDuration = dur + 'ms'; cur.style.transition = 'none';
      Snd.noise(dur / 1000, 0.05);
      (function trace() {
        var f = Math.min(1, (Date.now() - t0) / dur);
        cur.style.left = (wr.left + wr.width * f) + 'px';
        cur.style.top = (wr.top + wr.height * (0.55 + 0.25 * Math.sin(f * 40))) + 'px';
        if (f < 1) return requestAnimationFrame(trace);
        setTimeout(function () {
          cur.style.transition = 'left .5s,top .5s'; cur.style.left = mx + 'px'; cur.style.top = my + 'px';
          setTimeout(function () { B.classList.remove('noc'); cur.remove(); }, 520);
          lay.classList.add('fade'); setTimeout(function () { lay.remove(); haunting = false; }, 2200);
        }, 900);
      })();
    }, 420);
  }

  function speak(text) {
    try {
      if (!window.speechSynthesis || Snd.isMuted() || !Snd.on()) return;
      var u = new SpeechSynthesisUtterance(text), re = new RegExp('^' + LANG, 'i');
      var vs = speechSynthesis.getVoices().filter(function (v) { return re.test(v.lang); });
      if (vs.length) u.voice = vs[0];
      u.lang = L('voice'); u.pitch = 0.05; u.rate = 0.62; u.volume = 0.16;
      speechSynthesis.speak(u);
    } catch (e) { /* sem voz */ }
  }

  function haunt() {
    var r = Math.random();
    if (r < 0.22) ouija();
    else if (r < 0.4) possess();
    else if (r < 0.52) vulto();
    else if (r < 0.78) { if (!inp.value) ghostWrite(ghostLine()); else ghostWrite(inp.value + rnd(L('tails')), 900); }
    else if (r < 0.88) { Snd.sigh(); if (NAME && Math.random() < 0.3) speak(NAME); }
    else { Snd.whisper(); if (Math.random() < 0.35) speak(NAME && Math.random() < 0.3 ? NAME : rnd(L('spoken'))); }
  }
  setInterval(function () {
    if (!playing || doc.hidden || busy) return;
    var now = Date.now(), idle = now - lastAct;
    if (idle > 40000 && !ghost && !inp.value) ghostWrite(ghostLine());
    if (inp.value && !ghost && now - lastKey > 2500 && now - lastKey < 3500 && Math.random() < 0.08) ghostWrite(inp.value + rnd(L('tails')), 700);
    if (idle > 20000 && Math.random() < 0.04 + prog * 0.05) eyes();
    if (idle > 15000 && Math.random() < 0.012) (Math.random() < 0.5 ? Snd.sigh : Snd.whisper)();
    if (now > nextFlash) { flash(); nextFlash = now + 120000 + Math.random() * 120000; }
    if (now > nextHaunt && !ghost && !haunting) { haunt(); nextHaunt = now + (75000 - prog * 40000) * (0.5 + Math.random()); }
  }, 1000);
  var titleT = null, here = '·';
  doc.addEventListener('visibilitychange', function () {
    clearInterval(titleT);
    var T = L('titles').concat(NAME ? [NAME + '?'] : ACC ? [ACC + '?'] : []);
    if (doc.hidden) { var k = 0; doc.title = T[0]; titleT = setInterval(function () { doc.title = T[++k % T.length]; }, 6000); }
    else { doc.title = here; if (playing && !busy) { wb.style.color = '#5a5a5a'; wb.textContent = L('back'); Snd.tone(55, 1.4, 'sine', 0.12); Snd.sigh(); } }
  });

  /* ---------- o espirito fala (gemma) ---------- */
  var sp = el('div', 'sp', root), spTok = 0;
  root.insertBefore(sp, ot);
  function spell(text) {
    var tok = ++spTok, i = 0; sp.textContent = '';
    (function next() {
      if (tok !== spTok || i >= text.length) return;
      var s = el('span', 'pj', sp); s.textContent = text.charAt(i++);
      setTimeout(next, text.charAt(i - 1) === ' ' ? 160 : 55 + Math.random() * 110);
    })();
  }
  function spirit(outcome, guess) {
    var t0 = Date.now();
    post('/api/react', { outcome: outcome, guess: guess || '' }).then(function (d) {
      var r = (d && d.reply) || ''; if (!r) return;
      setTimeout(function () {
        if (outcome !== 'win' && r.length <= 30 && Math.random() < 0.3 && !ghost) { sp.textContent = ''; ghostWrite(r, 2400); }
        else spell(r);
        if (Math.random() < 0.25) Snd.whisper();
      }, Math.max(0, (outcome === 'win' ? 1600 : 900) - (Date.now() - t0)));
    }).catch(function () {});
  }

  /* ---------- jogo ---------- */
  var busy = false, fails = 0, mode = 'text';
  function pulse() {  // o coracao comeca a bater no primeiro terco e acelera ate o fim
    if (prog < 0.3) return Snd.heart(0);
    var f = (prog - 0.3) / 0.7;
    Snd.heart(Math.min(150, Math.round(48 + f * 70 + Math.min(fails, 12) * 3)), 0.28 + f * 0.6);
  }
  function load() {
    return fetch('/api/current').then(function (r) { return r.json(); }).then(function (d) {
      if (d.finished) return end();
      prog = d.n / d.total; fails = 0; mode = d.mode || 'text';
      sound = d.scene.sound || null; Snd.hum(!!(sound && sound.buzz)); morseUntil = 0; sigil = d.sigil || '';
      stage.classList.toggle('listen', !!sound);
      hd.textContent = d.title; doc.title = here = 'level ' + d.n;
      board = null; paint(d.scene, d.comment); stage.classList.remove('cut'); stage.classList.toggle('pinmode', mode === 'pin');
      ph = mode === 'pin' ? L('pinPh') : L('password');
      wb.textContent = ''; inp.value = ''; inp.placeholder = ph; inp.focus();
      Snd.level(prog); pulse();
      if (Math.random() < 0.12 + prog * 0.1) setTimeout(function () { if (playing && !busy) ouija(); }, 4000 + Math.random() * 4000);
      else if (Math.random() < 0.1 + prog * 0.25) setTimeout(function () { if (playing) vulto(prog > 0.85); }, 2500 + Math.random() * 6000);
      if (sigil) setTimeout(function () { if (playing) flash(70, 'sigil'); }, 5000 + Math.random() * 10000);
      if ((NAME || ACC) && d.n > 3 && Math.random() < 0.08) setTimeout(function () { if (playing) flash(60, 'name'); }, 8000 + Math.random() * 20000);
      if (JOKES.length && d.n > 2 && Math.random() < 0.15) setTimeout(function () { if (playing && !busy) spell(rnd(JOKES)); }, 6000 + Math.random() * 15000);
    });
  }
  function hour() {
    var t = new Date(), p = function (n) { return (n < 10 ? '0' : '') + n; };
    return p(t.getHours()) + ':' + p(t.getMinutes());
  }
  function judge(d, guess) {
    if (d.success) {
      Snd.tone(196, 1.2, 'sine', 0.1); Snd.tone(294, 1.6, 'sine', 0.05);
      if (d.ritual) return banish(d.stats);
      wb.style.color = '#6a7a6a'; wb.textContent = '...'; sp.textContent = '';
      stage.classList.add('cut'); Snd.noise(0.6, 0.4);
      if (Math.random() < 0.35 + prog * 0.4) setTimeout(function () { flash(60); }, 260);
      spirit('win');
      setTimeout(function () { load(); }, 900);
      return;
    }
    Snd.tone(70, 0.5, 'sawtooth', 0.12);
    if (!d.echo) fails++;
    var w = d.whisper || '';
    if (fails && fails % 5 === 0) w = fmt(L('late'), { h: hour() });
    wb.style.color = d.echo ? '#8a8478' : '#b3202a'; wb.textContent = w; pulse();
    if (!d.echo) spirit('fail', guess);
    if (fails >= 8 && Math.random() < 0.3) eyes();
    if (fails >= 3 && Math.random() < 0.12 + prog * 0.15) setTimeout(function () { vulto(); }, 1200);
    if (fails >= 4 && Math.random() < 0.15) setTimeout(function () { possess(); }, 3000);
    stage.classList.remove('sh'); void stage.offsetWidth; stage.classList.add('sh');
  }
  frm.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var v = inp.value.trim(); if (!v || busy) return;
    busy = true;
    post('/api/check', { password: v })
      .then(function (d) { judge(d, v); })
      .catch(function () { wb.textContent = '...'; })
      .then(function () { busy = false; });
  });
  var sound = null, morseUntil = 0;
  function playMorse() {
    if (!sound || !sound.morse || Date.now() < morseUntil) return;
    Snd.start(); Snd.hum(false);
    var ms = Snd.morse(sound.morse); morseUntil = Date.now() + ms;
    setTimeout(function () { if (sound && sound.buzz) Snd.hum(true); }, ms + 600);
  }
  stage.addEventListener('click', function (ev) {
    if (sound && mode !== 'pin') return playMorse();
    if (mode !== 'pin' || busy || !playing) return;
    var r = stage.getBoundingClientRect(), fx = (ev.clientX - r.left) / r.width, fy = (ev.clientY - r.top) / r.height;
    var p = el('div', 'pin', stage); p.style.left = (fx * 100) + '%'; p.style.top = (fy * 100) + '%';
    busy = true; Snd.tone(110, 0.4, 'triangle', 0.1);
    post('/api/pin', { lat: 90 - fy * 180, lon: fx * 360 - 180 })
      .then(function (d) { judge(d, ''); if (!d.success) setTimeout(function () { p.classList.add('gone'); }, 1400); })
      .catch(function () { wb.textContent = '...'; })
      .then(function () { busy = false; });
  });

  /* ---------- or\u00e1culo ---------- */
  var warned = false;
  ot.addEventListener('click', function () {
    oc.classList.toggle('hide'); if (oc.classList.contains('hide')) return;
    ocq.focus();
    if (!warned) api('/api/summon').then(function (st) {
      if (st.present) return; warned = true;
      el('div', '', ocb).textContent = st.pulling ? L('mirrorCrossing') : L('mirrorEmpty');
    }).catch(function () {});
  });
  ocx.addEventListener('click', function () { oc.classList.add('hide'); inp.focus(); });
  oci.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var q = ocq.value.trim(); if (!q) return; ocq.value = '';
    var u = el('div', 'u', ocb); u.textContent = '> ' + q; ocb.scrollTop = ocb.scrollHeight;
    var w = el('div', '', ocb); w.textContent = '...';
    fetch('/api/oracle', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: q }) })
      .then(function (r) { return r.json(); })
      .then(function (d) { w.textContent = d.reply; ocb.scrollTop = ocb.scrollHeight; })
      .catch(function () { w.textContent = '...'; });
  });

  /* ---------- o ritual final ---------- */
  var FACE = __FACE__;
  var CHANT = [
    'Exorcizamus te, omnis immunde spiritus,',
    'omnis satanica potestas, omnis incursio infernalis adversarii,',
    'omnis legio, omnis congregatio et secta diabolica.',
    'Ergo, draco maledicte, et omnis legio diabolica, adjuramus te:',
    'cessa decipere humanas creaturas, eisque aeternae perditionis venenum propinare.',
    'Vade, Satana, inventor et magister omnis fallaciae.',
    'Recede ab hac imagine.'
  ];
  function banish(stats) {
    var r = el('div', 'rit', B), pre = el('pre', '', r), ch = el('div', 'ch', r);
    pre.textContent = FACE; Snd.scream();
    setTimeout(function () { r.classList.add('sh'); }, 3200);
    setTimeout(function () { r.classList.remove('sh'); }, 6800);
    var i = 0;
    (function say() {
      if (i >= CHANT.length) return;
      var line = CHANT[i++], j = 0; ch.textContent = '';
      var t = setInterval(function () { ch.textContent = line.slice(0, ++j); if (j >= line.length) clearInterval(t); }, 38);
      setTimeout(say, 1100 + line.length * 38);
    })();
    var chars = FACE.split('');
    setTimeout(function () {
      var d = setInterval(function () {
        var left = 0;
        for (var n = 0; n < 40; n++) { var k = Math.floor(Math.random() * chars.length); if (chars[k] !== ' ' && chars[k] !== '\n') chars[k] = ' '; }
        for (var q = 0; q < chars.length; q++) if (chars[q] !== ' ' && chars[q] !== '\n') left++;
        pre.textContent = chars.join('');
        if (left < 8) { clearInterval(d); setTimeout(function () { r.parentNode.removeChild(r); end(); }, 1800); }
      }, 90);
    }, 7000);
  }
  function end() {
    clearInterval(grainTimer); root.style.display = 'none'; mt.style.display = 'none'; playing = false; Snd.heart(0); Snd.hum(false);
    var box = el('div', 'end', B);
    el('h2', '', box).textContent = L('endTitle');
    var wait = el('div', 'en-wait', box); wait.textContent = L('judging');
    api('/api/profile').then(function (p) {
      wait.remove();
      var m = p.metrics, card = el('div', 'st', box);
      el('div', 'en-who', card).textContent = p.title + (NAME ? ' · ' + NAME : ACC ? ' · ' + ACC + ' (& co.)' : '');
      el('div', 'en-desc', card).textContent = p.desc;
      ['bruta', 'lenta', 'esperta'].forEach(function (k) {
        var row = el('div', 'en-row', card), v = m.pct[k];
        row.textContent = (L('paths')[k] + '            ').slice(0, 10) + ' ' + new Array(Math.round(v / 5) + 1).join('█') + new Array(21 - Math.round(v / 5)).join('░') + ' ' + v + '%';
      });
      var tbl = el('div', 'en-tbl', card);
      [[L('statDoors'), m.doors], [L('statAttempts'), m.attempts], [L('statAvg'), m.avg_fails], [L('statOracle'), m.oracle],
        [L('statNight'), m.night_pct + '%'], [L('statTime'), m.minutes]].forEach(function (r) {
        var row = el('div', '', tbl); el('span', '', row).textContent = r[0]; el('b', '', row).textContent = r[1];
      });
      if (m.worst) el('div', 'en-worst', card).textContent = L('statWorst') + ': ' + m.worst.n + ' · ' + ((LANG === 'en' && m.worst.tema_en) || m.worst.tema) + ' (' + m.worst.fails + ')';
      el('div', 'en-by', box).textContent = L('by')[p.by] || '';
      var v = el('div', 'en-verdict', box), i = 0;
      (function next() { if (i < p.verdict.length) { v.textContent += p.verdict.charAt(i++); setTimeout(next, 45 + Math.random() * 70); } })();
      var cb = el('button', 'en-cb', box); cb.textContent = L('credits');
      cb.addEventListener('click', function () {  // so agora a casa revela de onde vieram os rostos
        cb.remove();
        api('/api/credits').then(function (c) {
          var ul = el('div', 'en-credits', box);
          (c.images || []).forEach(function (im) {
            var a = el('a', '', ul); a.href = im.url; a.target = '_blank'; a.rel = 'noopener';
            a.textContent = im.title + ' · ' + (im.author || '?') + ' · ' + im.license;
          });
          box.appendChild(b);
        });
      });
      var b = el('button', '', box); b.textContent = L('restart');
      b.addEventListener('click', function () { fetch('/api/reset', { method: 'POST' }).then(function () { location.reload(); }); });
    }).catch(function () { wait.textContent = '...'; });
  }

  /* ---------- o console tambem e assombrado ---------- */
  try {
    var omen = null;
    for (var ci = 0; ci < doc.childNodes.length; ci++) if (doc.childNodes[ci].nodeType === 8) { omen = doc.childNodes[ci].nodeValue; break; }
    var hello = function () {
      console.log('%c' + L('console1'), 'color:#b3202a;font:14px Courier New,monospace');
      console.log('%c' + L('console2'), 'color:#555;font:11px Courier New,monospace');
      if (omen) console.log('%c' + omen, 'color:#7a1a1a;font:11px/1.3 Courier New,monospace');
    };
    Object.keys(I18N.pt.traps).forEach(function (k) {
      Object.defineProperty(window, k, { configurable: true, get: function () { var t = L('traps')[k]; Snd.whisper(); if (playing && Math.random() < 0.5) ghostWrite(t, 1400); return t; } });
    });
    window.ouija = function (q) {
      if (!q) return L('ouijaAsk');
      post('/api/oracle', { question: String(q) }).then(function (d) {
        var r = d.reply || '...';
        console.log('%c' + r, 'color:#cdbfa0;font:italic 13px Georgia,serif');
        var w = r.normalize('NFD').replace(/[̀-ͯ]/g, '').toUpperCase().match(/[A-Z]{3,}/);
        if (playing && w) ouija(w[0].slice(0, 8));
      });
      return L('ouijaMoves');
    };
    DE.setAttribute('data-ela', 'está aqui');
  } catch (e) { /* o console resiste */ }

  /* ---------- invocação ---------- */
  function api(path, post) {
    return fetch(path, post ? { method: 'POST' } : undefined).then(function (r) { return r.json(); });
  }
  function bar(p) {
    var n = Math.round(p * 24), s = '';
    for (var i = 0; i < 24; i++) s += i < n ? '▓' : '░';
    return '[' + s + '] ' + Math.floor(p * 100) + '%';
  }
  var watching = null;
  function watchSummon(onTick) {
    clearInterval(watching);
    watching = setInterval(function () {
      api('/api/summon').then(function (st) {
        onTick(st);
        ocTitle.textContent = st.pulling ? L('summoning') + Math.floor(st.progress * 100) + '%' : L('mirror');
        if (!st.pulling) clearInterval(watching);
      }).catch(function () {});
    }, 1200);
  }

  /* ---------- abertura ---------- */
  function presence() {
    return api('/api/presence').then(function (p) { NAME = p.name || ''; ACC = p.account || ''; JOKES = p.jokes || []; }).catch(function () {});
  }
  function setLang(l) {
    applyLang(l);
    return post('/api/lang', { lang: l }).catch(function () {});
  }
  function boot() {
    var bx = el('div', 'boot', B), pre = el('pre', '', bx), bt = el('div', 'bt', bx), bb = el('div', 'bb', bx);
    var bn = el('div', 'bn', bx), bw = el('div', 'bw', bx);
    var now = new Date().toTimeString().slice(0, 8), queue = [], typing = false;
    function type(line, cb) {
      queue.push([line, cb]); if (typing) return;
      (function next() {
        var it = queue.shift(); if (!it) { typing = false; return; }
        typing = true; var j = 0;
        if (RM || doc.hidden) { pre.textContent += it[0] + '\n'; if (it[1]) it[1](); return next(); }
        var base = pre.textContent, t0 = Date.now();
        var t = setInterval(function () {  // pelo relogio: timers estrangulados nao travam a abertura
          j = Math.min(it[0].length, Math.ceil((Date.now() - t0) / 16));
          pre.textContent = base + it[0].slice(0, j);
          if (j >= it[0].length) { clearInterval(t); pre.textContent += '\n'; if (it[1]) it[1](); setTimeout(next, 160); }
        }, 16);
      })();
    }
    function btn(label, fn) {
      var b = el('button', '', bb); b.type = 'button'; b.textContent = '[ ' + label + ' ]';
      b.addEventListener('click', fn); return b;
    }
    function enter() {
      Snd.start(); fullscreen(true); bx.classList.add('out'); playing = true; lastAct = Date.now();
      setTimeout(function () { if (bx.parentNode) B.removeChild(bx); }, 1500);
      try { hello(); } catch (e) { /* sem console */ }
      load();
    }
    function choices(st) {
      bb.innerHTML = ''; bn.textContent = '';
      if (st.present) { btn(L('go'), enter).focus(); return; }
      if (st.pulling) {
        bn.className = 'bn bp'; bn.textContent = (st.phase || '...') + '\n' + bar(st.progress);
        btn(L('goWhile'), enter).focus();
        watchSummon(function (s2) {
          if (s2.pulling) { bn.textContent = (s2.phase || '...') + '  ' + bar(s2.progress); return; }
          bn.className = 'bn';
          if (s2.error) { bn.textContent = L('failed') + s2.error; bb.innerHTML = ''; btn(L('goWithout'), enter).focus(); return; }
          if (bx.parentNode) { bn.textContent = L('here'); bb.innerHTML = ''; btn(L('go'), enter).focus(); Snd.tone(41, 3, 'sine', 0.2); }
        });
        return;
      }
      if (st.ollama) {
        var size = st.model === 'gemma2:2b' ? ' · 1.6 GB' : '';
        bn.textContent = fmt(L('needBody'), { m: st.model });
        btn(L('invoke') + size, function () {
          Snd.start(); Snd.tone(55, 2.5, 'sine', 0.15);
          api('/api/summon', true).then(function (r) { choices({ pulling: true, phase: r.phase, progress: 0 }); });
        }).focus();
        btn(L('goWithout'), enter);
        return;
      }
      bn.innerHTML = st.binary ? L('shellSleeps') : L('noShell');
      btn(L('goWithout'), enter).focus();
    }
    function ritual() {
      bb.innerHTML = '';
      bt.innerHTML = '<b>LOABPRON</b>' + L('tagline') + '<small>' + L('sub') + '</small>';
      bw.textContent = L('warn');
      type('speculum 0.6.6.6');
      type(L('session') + now);
      type(L('searching'));
      api('/api/summon').then(function (st) {
        type('ollama .......... ' + (st.ollama ? L('awake') : st.binary ? L('asleep') : L('absent')));
        type(st.model + ' ' + '.'.repeat(Math.max(2, 16 - st.model.length)) + ' ' + (st.present ? L('present') : st.pulling ? L('arriving') : L('notSummoned')), function () {
          setTimeout(function () { bt.classList.add('on'); }, 300);
          setTimeout(function () { choices(st); }, RM ? 0 : 2400);
        });
      }).catch(function () {
        type(L('mute'), function () { bt.classList.add('on'); btn(L('go'), enter); });
      });
    }
    // o primeiro gesto: escolher a lingua em que a casa vai falar
    bt.innerHTML = '<b>LOABPRON</b>'; bt.classList.add('on');
    [['pt', 'português'], ['en', 'english']].forEach(function (o) {
      var b = btn(o[1], function () { Snd.start(); setLang(o[0]).then(presence).then(ritual); });
      if (o[0] === LANG) setTimeout(function () { b.focus(); }, 50);
    });
  }

  applyLang(LANG);
  if (location.hash === '#dev') {  // desenvolvimento: pula a abertura e expoe as assombracoes
    playing = true; setLang(LANG).then(presence).then(load);
    window.__haunt = { ouija: ouija, possess: possess, vulto: vulto, ghostWrite: ghostWrite, flash: flash, eyes: eyes, spell: spell,
      whisper: function () { Snd.whisper(); }, sigh: function () { Snd.sigh(); }, lang: setLang };
  } else boot();
})();
