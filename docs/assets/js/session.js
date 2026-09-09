/* ==========================================================================
   ITGate Academy — CEH Diploma session engine
   Paged navigation · sidebar · progress · keyboard · break timer · MCQ quiz
   Shared by every session page.
   ========================================================================== */
(function () {
  'use strict';

  var pages = [], idx = 0;

  document.addEventListener('DOMContentLoaded', function () {
    pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
    if (!pages.length) return;

    buildSidebar();
    buildProgress();
    wireButtons();
    wireKeyboard();
    wireTimers();
    wireMCQ();
    wireShots();
    wireInteractiveDiagrams();
    wireReplay();
    wireSims();
    wirePacketFlows();

    var start = parseInt((location.hash || '').replace('#p', ''), 10);
    go(isNaN(start) ? 0 : start - 1, true);
  });

  /* ---------- navigation ---------- */
  function go(n, silent) {
    if (n < 0 || n >= pages.length) return;
    idx = n;

    pages.forEach(function (p, i) { p.classList.toggle('active', i === idx); });
    var _ap = pages[idx];
    if (_ap) setTimeout(function () {
      _ap.querySelectorAll('.sim[data-animate]').forEach(function (s) {
        if (s.__simPlay && !s.__simPlayed) {
          var r = s.getBoundingClientRect();
          if (r.top < (window.innerHeight || 800) && r.bottom > 0) s.__simPlay();
        }
      });
    }, 80);

    document.querySelectorAll('#sessionNav li').forEach(function (li, i) {
      li.classList.toggle('now', i === idx);
      li.classList.toggle('seen', i < idx);
    });

    var bar = document.getElementById('progressBar');
    if (bar) bar.style.width = (((idx + 1) / pages.length) * 100) + '%';
    var lbl = document.getElementById('progressLabel');
    if (lbl) lbl.textContent = 'Page ' + (idx + 1) + ' / ' + pages.length;

    var prev = document.getElementById('btnPrev'), next = document.getElementById('btnNext');
    if (prev) {
      prev.classList.toggle('disabled', idx === 0);
      prev.querySelector('.lbl').textContent = idx === 0 ? '—' : title(idx - 1);
    }
    if (next) {
      next.classList.toggle('disabled', idx === pages.length - 1);
      next.querySelector('.lbl').textContent = idx === pages.length - 1 ? 'End of session' : title(idx + 1);
    }

    if (!silent) history.replaceState(null, '', '#p' + (idx + 1));
    window.scrollTo({ top: 0, behavior: silent ? 'auto' : 'smooth' });
  }

  function title(i) { return pages[i].getAttribute('data-title') || ('Page ' + (i + 1)); }

  function buildSidebar() {
    var nav = document.getElementById('sessionNav');
    if (!nav) return;
    pages.forEach(function (p, i) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#p' + (i + 1);
      a.textContent = p.getAttribute('data-title') || ('Page ' + (i + 1));
      a.addEventListener('click', function (e) { e.preventDefault(); go(i); });
      li.appendChild(a);
      nav.appendChild(li);
    });
  }

  function buildProgress() {
    var host = document.getElementById('progressHost');
    if (!host) return;
    host.innerHTML =
      '<div class="pbar"><div class="pbar-fill" id="progressBar"></div></div>' +
      '<span class="pbar-label" id="progressLabel"></span>';
  }

  function wireButtons() {
    var prev = document.getElementById('btnPrev'), next = document.getElementById('btnNext');
    if (prev) prev.addEventListener('click', function (e) { e.preventDefault(); go(idx - 1); });
    if (next) next.addEventListener('click', function (e) { e.preventDefault(); go(idx + 1); });
  }

  function wireKeyboard() {
    document.addEventListener('keydown', function (e) {
      if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); go(idx + 1); }
      if (e.key === 'ArrowLeft'  || e.key === 'PageUp')   { e.preventDefault(); go(idx - 1); }
      if (e.key === 'Home') { e.preventDefault(); go(0); }
      if (e.key === 'End')  { e.preventDefault(); go(pages.length - 1); }
    });
  }

  /* ---------- break timer ---------- */
  function wireTimers() {
    document.querySelectorAll('[data-timer]').forEach(function (host) {
      var total = (parseInt(host.getAttribute('data-timer'), 10) || 15) * 60;
      var left = total, tick = null, running = false;

      var display = host.querySelector('.timer-display');
      var ring    = host.querySelector('.timer-ring-fill');
      var btnS    = host.querySelector('[data-act="start"]');
      var btnR    = host.querySelector('[data-act="reset"]');
      var note    = host.querySelector('.timer-note');
      var CIRC    = 2 * Math.PI * 54;

      if (ring) { ring.style.strokeDasharray = CIRC; ring.style.strokeDashoffset = 0; }
      render();

      btnS && btnS.addEventListener('click', function () { running ? pause() : start(); });
      btnR && btnR.addEventListener('click', reset);

      function start() {
        running = true;
        host.classList.add('running'); host.classList.remove('finished');
        btnS.textContent = '⏸ Pause';
        if (note) note.textContent = 'Break in progress — see you back on time.';
        tick = setInterval(function () { left--; if (left <= 0) { left = 0; finish(); } render(); }, 1000);
      }
      function pause() {
        running = false; clearInterval(tick);
        host.classList.remove('running');
        btnS.textContent = '▶ Resume';
        if (note) note.textContent = 'Paused.';
      }
      function reset() {
        running = false; clearInterval(tick); left = total;
        host.classList.remove('running', 'finished');
        btnS.textContent = '▶ Start break';
        if (note) note.textContent = 'Press start when the break begins.';
        render();
      }
      function finish() {
        running = false; clearInterval(tick);
        host.classList.remove('running'); host.classList.add('finished');
        btnS.textContent = '▶ Start break';
        if (note) note.textContent = '⏰ Break is over — welcome back!';
        flash();
      }
      function flash() {
        var n = 0, id = setInterval(function () {
          host.classList.toggle('flash');
          if (++n > 7) { clearInterval(id); host.classList.remove('flash'); }
        }, 400);
      }
      function render() {
        var m = Math.floor(left / 60), s = left % 60;
        if (display) display.textContent = m + ':' + (s < 10 ? '0' : '') + s;
        if (ring) ring.style.strokeDashoffset = CIRC * (1 - left / total);
        host.classList.toggle('warning', left <= 60 && left > 0);
      }
    });
  }

  /* ---------- MCQ quiz ---------- */
  function wireMCQ() {
    var all = document.querySelectorAll('.q.mcq');
    if (!all.length) return;
    var total = all.length, answered = 0, right = 0;
    var score = document.getElementById('quizScore');
    if (score) score.innerHTML = 'Answered <b>0</b> / ' + total;

    all.forEach(function (q) {
      var correct = q.getAttribute('data-correct');
      var opts = q.querySelectorAll('.opts li');
      var fb = q.querySelector('.mcq-fb');
      var why = q.getAttribute('data-why') || '';

      opts.forEach(function (li) {
        li.addEventListener('click', function () {
          if (q.classList.contains('answered')) return;
          q.classList.add('answered');
          answered++;

          var picked = li.getAttribute('data-opt');
          if (picked === correct) {
            right++;
            li.classList.add('correct');
            if (fb) { fb.className = 'mcq-fb show ok'; fb.innerHTML = '<b>Correct.</b> ' + why; }
          } else {
            li.classList.add('wrong');
            opts.forEach(function (o) {
              if (o.getAttribute('data-opt') === correct) o.classList.add('correct');
              else if (o !== li) o.classList.add('muted-opt');
            });
            if (fb) { fb.className = 'mcq-fb show no'; fb.innerHTML = '<b>Not quite.</b> ' + why; }
          }

          if (score) {
            score.innerHTML = 'Answered <b>' + answered + '</b> / ' + total +
                              ' · Correct <b>' + right + '</b>' +
                              (answered === total ? ' — ' + Math.round(right / total * 100) + '%' : '');
          }
        });
      });
    });
  }

  /* ---------- interactive diagrams (click a node, reveal its detail panel) ---------- */
  function wireInteractiveDiagrams() {
    document.querySelectorAll('.dgm.interactive').forEach(function (dgm) {
      var nodes = dgm.querySelectorAll('[data-node]');
      if (!nodes.length) return;
      nodes.forEach(function (node) {
        node.addEventListener('click', function () {
          var key = node.getAttribute('data-node');
          var already = node.classList.contains('active');
          nodes.forEach(function (n) { n.classList.remove('active'); });
          dgm.querySelectorAll('.dgm-detail').forEach(function (d) { d.classList.remove('open'); });
          if (already) return; // clicking the active node again just closes it
          node.classList.add('active');
          var panel = dgm.querySelector('.dgm-detail[data-detail="' + key + '"]');
          if (panel) panel.classList.add('open');
        });
      });
    });
  }

  /* ---------- replayable animated diagrams ---------- */
  function wireReplay() {
    document.querySelectorAll('[data-replay]').forEach(function (btn) {
      var dgm = btn.closest('.dgm');
      if (!dgm) return;
      btn.addEventListener('click', function () { replay(dgm); });
      replay(dgm); // play once on load
      function replay(el) {
        el.classList.remove('animate-run');
        void el.offsetWidth; // restart CSS animation
        el.classList.add('animate-run');
      }
    });
  }

  /* ---------- sim screens (animated tool/terminal windows) ----------
     Lines are visible by default; when a sim scrolls into view (or its page
     opens) they replay in sequence. Never leaves a blank terminal.        */
  function wireSims() {
    Array.prototype.slice.call(document.querySelectorAll('.sim[data-animate]')).forEach(function (sim) {
      var lines = Array.prototype.slice.call(sim.querySelectorAll('.sim-body .l'));
      var btn = sim.querySelector('.sim-replay'); var timers = [];
      function reset() { timers.forEach(clearTimeout); timers = []; lines.forEach(function (l) { l.classList.remove('shown'); }); }
      function play() {
        reset(); sim.__simPlayed = true; sim.classList.add('playing'); var t = 0;
        lines.forEach(function (l) { t += l.classList.contains('cmd') ? 300 : 150; timers.push(setTimeout(function () { l.classList.add('shown'); }, t)); });
        timers.push(setTimeout(function () { sim.classList.remove('playing'); }, t + 260));
      }
      sim.__simPlay = play;
      if (btn) btn.addEventListener('click', play);
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting && !sim.__simPlayed) play(); }); }, { threshold: 0.25 }).observe(sim);
      }
    });
  }

  /* ---------- screenshot slots ----------
     Photos are dropped in by the instructor. Until a file exists, show a
     labelled placeholder instead of a broken-image icon.                     */
  function wireShots() {
    document.querySelectorAll('.shot img').forEach(function (img) {
      img.addEventListener('error', function () {
        var cap = img.parentNode.querySelector('figcaption');
        var name = (img.getAttribute('src') || '').split('/').pop();
        var ph = document.createElement('div');
        ph.style.cssText = 'border:1px dashed var(--line-soft);border-radius:8px;padding:34px 18px;text-align:center;' +
                           'color:var(--text-4);font-family:var(--mono);font-size:12.5px;background:var(--panel-2);line-height:1.8';
        ph.innerHTML = '🖼 screenshot not added yet<br><span style="color:var(--text-3)">' + name + '</span>';
        img.parentNode.replaceChild(ph, img);
        if (cap) cap.style.opacity = '.6';
      });
    });
  }


  /* ---------- packet-flow player (step through what happens on the wire) ----------
     Markup contract (see design/design_system.md §5c):
       <figure class="dgm pktflow">
         <svg …>  <g class="pf-step" data-step="1">…</g>  … </svg>
         <div class="pf-ctl">
           <button data-pf="prev">…</button>
           <button data-pf="play">…</button>
           <button data-pf="next">…</button>
           <span class="pf-count"></span>
         </div>
         <div class="pf-cap" data-cap="1">…</div>  (one per step)
       </figure>
     Steps are cumulative: at step N, steps 1..N are visible and N animates in.  */
  function wirePacketFlows() {
    document.querySelectorAll('.dgm.pktflow').forEach(function (dgm) {
      var steps = Array.prototype.slice.call(dgm.querySelectorAll('.pf-step'));
      if (!steps.length) return;
      var caps  = Array.prototype.slice.call(dgm.querySelectorAll('.pf-cap'));
      var total = steps.length;
      var cur = 1, timer = null;   // land on step 1 so the figure is never blank

      var ctl   = dgm.querySelector('.pf-ctl');
      var bPrev = ctl && ctl.querySelector('[data-pf="prev"]');
      var bNext = ctl && ctl.querySelector('[data-pf="next"]');
      var bPlay = ctl && ctl.querySelector('[data-pf="play"]');
      var count = ctl && ctl.querySelector('.pf-count');

      function render(animateLast) {
        steps.forEach(function (g, i) {
          var on = (i < cur);
          g.classList.toggle('on', on);
          g.classList.remove('now');
          if (on && animateLast && i === cur - 1) {
            void g.offsetWidth;
            g.classList.add('now');
          }
        });
        caps.forEach(function (c) {
          c.classList.toggle('open', String(c.getAttribute('data-cap')) === String(cur));
        });
        if (count) count.textContent = cur + ' / ' + total;
        if (bPrev) bPrev.disabled = (cur === 0);
        if (bNext) bNext.disabled = (cur === total);
      }
      function stop() { if (timer) { clearInterval(timer); timer = null; } if (bPlay) bPlay.textContent = '▶ Play'; }
      function play() {
        if (timer) { stop(); return; }
        if (cur >= total) { cur = 0; render(false); }
        if (bPlay) bPlay.textContent = '❚❚ Pause';
        timer = setInterval(function () {
          if (cur >= total) { stop(); return; }
          cur++; render(true);
        }, 1400);
      }
      bPrev && bPrev.addEventListener('click', function () { stop(); if (cur > 0) { cur--; render(false); } });
      bNext && bNext.addEventListener('click', function () { stop(); if (cur < total) { cur++; render(true); } });
      bPlay && bPlay.addEventListener('click', play);
      render(false);
    });
  }

})();
