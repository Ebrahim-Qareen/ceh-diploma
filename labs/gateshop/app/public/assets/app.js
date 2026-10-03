// GateShop client JS.
// Lab: xss-dom (DOM-based XSS). The server tells us the security level via data-secure.

function renderWelcome() {
  var el = document.getElementById('welcome');
  if (!el) return;
  var hash = decodeURIComponent((location.hash || '').replace(/^#/, ''));
  var m = /name=([^&]*)/.exec(hash);
  var name = m ? m[1] : 'friend';
  var secure = el.getAttribute('data-secure') === '1';

  if (secure) {
    // FIX:DOMXSS — write untrusted data as text, never as HTML.
    el.textContent = 'Hello, ' + name + '!';
  } else {
    // ===== VULN:DOMXSS | CWE-79 | LAB:xss-dom =====
    el.innerHTML = 'Hello, ' + name + '!'; // <-- the bug: fragment data flows into innerHTML
    // ===== END VULN:DOMXSS =====
  }
}
window.addEventListener('DOMContentLoaded', renderWelcome);
window.addEventListener('hashchange', renderWelcome);
