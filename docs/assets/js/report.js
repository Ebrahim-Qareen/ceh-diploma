/* ==========================================================================
   CEH Diploma — cumulative team report engine
   Each session's report is the running engagement: it shows every session up to
   and including this one. Earlier sessions render collapsed at the top; the
   current session is open.

   Storage is SHARED across all report pages on this origin under one key, so what
   a team fills in the Session 2 report already appears in Session 3 and 4 (same
   browser). Saving MERGES — a page only touches the ids it shows, never wiping
   another session's answers. Nothing is uploaded.

   Markup:  <div data-report="s4-access" data-report-title="…" data-current="s4">
     .rep-head   inputs with [data-field] + [data-label]      (shared team header)
     .rep-bar    [data-progress] [data-progress-bar] [data-saved] + buttons
     [data-report-body] > .rep-group (details=prior | section.current)
        each .rep-group has [data-group-title]; inside: .rep-sec | .rep-step | .rep-free
        .rep-step has input[data-check] (+ [data-active][data-current] on the current
        session's active steps), a .rep-name, optional .rep-cmd, [data-notes]
   ========================================================================== */
(function () {
  'use strict';
  var root = document.querySelector('[data-report]');
  if (!root) return;
  var KEY = 'ceh-diploma-engagement';                 // shared across every report page on this origin
  var CUR = root.getAttribute('data-current') || '';  // current session prefix, e.g. "s4"

  var fields = [].slice.call(root.querySelectorAll('[data-field]'));
  var checks = [].slice.call(root.querySelectorAll('input[data-check]'));
  var notes  = [].slice.call(root.querySelectorAll('[data-notes]'));

  /* ---------- shared, merge-safe storage ---------- */
  function loadRaw() { try { var r = localStorage.getItem(KEY); return r ? JSON.parse(r) : null; } catch (e) { return null; } }
  function save() {
    var s = loadRaw() || {}; s.f = s.f || {}; s.c = s.c || {}; s.n = s.n || {};
    fields.forEach(function (el) { s.f[el.getAttribute('data-field')] = el.value; });
    checks.forEach(function (el) { s.c[el.getAttribute('data-check')] = el.checked; });
    notes.forEach(function (el)  { s.n[el.getAttribute('data-notes')]  = el.value; });
    try { localStorage.setItem(KEY, JSON.stringify(s)); flash(); } catch (e) {}
    updateProgress(); refreshGate();
  }
  function load() {
    var s = loadRaw();
    if (s) {
      fields.forEach(function (el) { var k = el.getAttribute('data-field'); if (s.f && k in s.f) el.value = s.f[k]; });
      checks.forEach(function (el) { var k = el.getAttribute('data-check'); if (s.c && k in s.c) el.checked = !!s.c[k]; syncStep(el); });
      notes.forEach(function (el)  { var k = el.getAttribute('data-notes'); if (s.n && k in s.n) el.value = s.n[k]; autoGrow(el); });
    }
    updateProgress(); refreshGate();
  }

  function syncStep(cb) { var step = cb.closest('.rep-step'); if (step) step.classList.toggle('done', cb.checked); }

  /* ---------- progress (all steps shown on the page) ---------- */
  var pill = root.querySelector('[data-progress]');
  var bar  = root.querySelector('[data-progress-bar]');
  function updateProgress() {
    var total = checks.length, done = 0;
    checks.forEach(function (el) { if (el.checked) done++; });
    if (pill) pill.textContent = done + ' / ' + total + ' steps';
    if (bar)  bar.style.width = total ? (100 * done / total).toFixed(1) + '%' : '0%';
  }

  /* ---------- scope gate: only the CURRENT session's active steps vs its scope check ---------- */
  var gate = root.querySelector('[data-gate]');
  function refreshGate() {
    if (!gate) return;
    var scope = root.querySelector('input[data-check="' + gate.getAttribute('data-gate') + '"]');
    var ok = scope && scope.checked;
    var jumped = checks.some(function (el) {
      return el.hasAttribute('data-active') && el.hasAttribute('data-current') && el.checked && !ok;
    });
    gate.classList.toggle('show', !!jumped);
  }

  /* ---------- saved flash ---------- */
  var saved = root.querySelector('[data-saved]'), st;
  function flash() { if (!saved) return; saved.classList.add('show'); clearTimeout(st); st = setTimeout(function () { saved.classList.remove('show'); }, 1200); }

  /* ---------- expand / collapse a step's reference panel ---------- */
  [].forEach.call(root.querySelectorAll('.rep-step .rep-toggle'), function (btn) {
    btn.addEventListener('click', function () {
      var step = btn.closest('.rep-step');
      btn.setAttribute('aria-expanded', step.classList.toggle('open') ? 'true' : 'false');
    });
  });

  function autoGrow(el) { el.style.height = 'auto'; el.style.height = (el.scrollHeight + 2) + 'px'; }

  fields.forEach(function (el) { el.addEventListener('input', save); });
  notes.forEach(function (el)  { el.addEventListener('input', function () { autoGrow(el); save(); }); });
  checks.forEach(function (el) { el.addEventListener('change', function () { syncStep(el); save(); }); });

  /* ---------- export (cumulative, in session order) ---------- */
  function esc(s) { return (s || '').replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function nl2br(s) { return esc(s).replace(/\n/g, '<br>'); }
  function slug(s) { return (s || '').trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40); }

  var EXPORT_CSS =
    'body{font:14px/1.6 -apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#1a1f2b;background:#fff;max-width:900px;margin:32px auto;padding:0 24px}' +
    'h1{font-size:23px;margin:0 0 4px;border-bottom:3px solid #e63946;padding-bottom:10px}' +
    'h2{font-size:17px;margin:30px 0 4px;color:#111;border-bottom:1px solid #e3e7ec;padding-bottom:5px}' +
    'h3{font-size:14px;margin:18px 0 8px;color:#b3202c;letter-spacing:.3px}' +
    'h4{font-size:14px;margin:16px 0 6px}' +
    'table.meta{border-collapse:collapse;margin:12px 0 4px;font-size:13px}' +
    'table.meta th{text-align:left;padding:4px 16px 4px 0;color:#555;font-weight:600;vertical-align:top;white-space:nowrap}' +
    'table.meta td{padding:4px 0}' +
    '.step{margin:0 0 14px;padding:0 0 12px;border-bottom:1px solid #eceff3}' +
    '.s-h{margin:0 0 6px;font-weight:600;font-size:14px}' +
    '.s-h .bx{display:inline-block;width:16px;height:16px;line-height:16px;text-align:center;border:1px solid #9aa4b2;border-radius:3px;margin-right:8px;font-size:11px;color:#0a8f3c}' +
    '.step.done .s-h .bx{background:#0a8f3c;border-color:#0a8f3c;color:#fff}' +
    '.step.done .s-h{color:#0a5}' +
    'pre{background:#0d1117;color:#d7dee8;padding:9px 12px;border-radius:6px;overflow-x:auto;font:12.5px/1.6 Consolas,monospace;margin:6px 0}' +
    '.s-f{white-space:normal;font-size:13.5px;color:#2a3240;background:#f6f8fa;border-left:3px solid #22a;padding:8px 12px;border-radius:0 5px 5px 0}' +
    '.s-f em{color:#98a2b3}' +
    'footer{margin-top:34px;padding-top:12px;border-top:1px solid #e3e7ec;color:#8a94a2;font-size:11.5px}';

  function emitStep(node, out) {
    var cb = node.querySelector('[data-check]'), done = cb && cb.checked;
    var name = (node.querySelector('.rep-name') || {}).textContent || '';
    var cmd = (node.querySelector('.rep-cmd') || {}).textContent || '';
    var note = (node.querySelector('[data-notes]') || {}).value || '';
    out.push('<div class="step' + (done ? ' done' : '') + '">');
    out.push('<p class="s-h"><span class="bx">' + (done ? '&#10003;' : '&nbsp;') + '</span>' + esc(name.trim()) + '</p>');
    if (cmd) out.push('<pre>' + esc(cmd.trim()) + '</pre>');
    out.push('<div class="s-f">' + (note ? nl2br(note) : '<em>— not recorded —</em>') + '</div>');
    out.push('</div>');
  }

  function buildExport() {
    var title = root.getAttribute('data-report-title') || document.title;
    var out = ['<h1>' + esc(title) + '</h1>'];
    var meta = [];
    fields.forEach(function (el) {
      var label = el.getAttribute('data-label') || el.getAttribute('data-field');
      if (el.value) meta.push('<tr><th>' + esc(label) + '</th><td>' + nl2br(el.value) + '</td></tr>');
    });
    if (meta.length) out.push('<table class="meta">' + meta.join('') + '</table>');

    var groups = root.querySelectorAll('[data-report-body] .rep-group');
    [].forEach.call(groups, function (g) {
      out.push('<h2>' + esc(g.getAttribute('data-group-title') || '') + '</h2>');
      [].forEach.call(g.querySelectorAll('.rep-sec, .rep-step, .rep-free'), function (node) {
        if (node.classList.contains('rep-sec')) out.push('<h3>' + esc(node.textContent.trim()) + '</h3>');
        else if (node.classList.contains('rep-step')) emitStep(node, out);
        else { // rep-free
          var lab = (node.querySelector('.rep-free-label') || {}).textContent || '';
          var val = (node.querySelector('[data-notes]') || {}).value || '';
          out.push('<h4>' + esc(lab.trim()) + '</h4>');
          out.push('<div class="s-f">' + (val ? nl2br(val) : '<em>— not recorded —</em>') + '</div>');
        }
      });
    });
    return '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
      '<meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<title>' + esc(title) + '</title><style>' + EXPORT_CSS + '</style></head><body>' +
      out.join('\n') +
      '<footer>Generated ' + esc(new Date().toLocaleString()) + ' · CEH Diploma · ITGate Academy</footer>' +
      '</body></html>';
  }

  function download() {
    var teamField = root.querySelector('[data-field="team"]');
    var name = 'CEH-' + (root.getAttribute('data-report') || 'report') + '-' +
               (slug(teamField && teamField.value) || new Date().toISOString().slice(0, 10)) + '.html';
    var blob = new Blob([buildExport()], { type: 'text/html' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(url); a.remove(); }, 200);
  }
  var dl = root.querySelector('[data-export-html]'); if (dl) dl.addEventListener('click', download);
  var pf = root.querySelector('[data-export-pdf]');  if (pf) pf.addEventListener('click', function () { window.print(); });

  /* ---------- clear THIS session only (two-click confirm, no browser dialog) ---------- */
  var clr = root.querySelector('[data-clear]');
  if (clr) {
    var armed = false, ct, original = clr.textContent;
    clr.addEventListener('click', function () {
      if (!armed) {
        armed = true; clr.textContent = 'Erase this session?'; clr.classList.add('arm');
        ct = setTimeout(function () { armed = false; clr.textContent = original; clr.classList.remove('arm'); }, 3000);
        return;
      }
      clearTimeout(ct); armed = false; clr.textContent = original; clr.classList.remove('arm');
      var s = loadRaw() || { f: {}, c: {}, n: {} }; s.c = s.c || {}; s.n = s.n || {};
      checks.forEach(function (el) {
        if (el.hasAttribute('data-current')) { el.checked = false; syncStep(el); delete s.c[el.getAttribute('data-check')]; }
      });
      notes.forEach(function (el) {
        var k = el.getAttribute('data-notes');
        if (CUR && k.indexOf(CUR + '-') === 0) { el.value = ''; autoGrow(el); delete s.n[k]; }
      });
      try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {}
      updateProgress(); refreshGate();
    });
  }

  load();
})();
