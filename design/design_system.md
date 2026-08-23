# CEH Session Design System — Component Reference

> The shared visual + interaction system every session page uses.
> Files: `sessions/assets/css/ceh.css`, `sessions/assets/js/session.js`.
> **Never inline CSS/JS into a session page.** Add a component here, use it everywhere.

Session 1 is the reference implementation. A student should not be able to tell
which session a page came from by its look — only the content changes.

---

## 1. Colour tokens (CSS variables — do not invent new ones)

| Token | Value | Means |
|---|---|---|
| `--red` | `#e63946` | Brand / primary accent, headings, active state |
| `--cyan` | `#22d3ee` | Links, lab / build content |
| `--orange` | `#ff7043` | **Attacker view** — offensive action |
| `--green` | `#4ade80` | **Defender / SOC view** — detection, verified, free |
| `--purple` | `#a78bfa` | Activities, intro boxes, post-exploitation |
| `--amber` | `#fbbf24` | Recall / prior knowledge, premium tag |
| `--panel`, `--panel-2` | `#1a1f2a`, `#1f2533` | Diagram + box surfaces |
| `--line`, `--line-soft` | — | Borders |
| `--text-2/3/4` | — | Secondary → faintest text |

**Colour discipline:** orange always means the attacker is doing something,
green always means a defender can see it. Never swap them for variety.

---

## 2. Page structure

Each session page is one HTML file containing N `<section class="page" data-title="...">`
blocks. `session.js` builds the sidebar, the progress bar, and prev/next nav from
`data-title`. Only the active page is visible; the rest are `display:none`.

```html
<section class="page" data-title="Recall: Networking">
  <div class="page-head">
    <div class="kicker">
      <span class="snum">S01 · P04</span>
      <span class="tag recall">Recall</span>
      <span class="time">⏱ 10 min</span>
    </div>
    <h1>Page Title</h1>
    <p class="lede">One-sentence hook.</p>
  </div>
  <div class="content"> ... </div>
</section>
```

**Kicker tags:** `.tag.theory` `.tag.recall` `.tag.lab` `.tag.activity` `.tag.offensive`

**Page numbering:** `snum` values are sequential (`P02`, `P03`, …) and the cover
page carries no number. If you insert a page, renumber every following kicker —
they are not generated.

---

## 3. Callout boxes

```html
<div class="box intro"><span class="box-t">Why this follows the last page</span><p>…</p></div>
```

| Class | Colour | Use for |
|---|---|---|
| `.box.intro` | purple | **Required first box on every page** — ties it to the previous page |
| `.box.attacker-view` | orange | What the attacker does / thinks |
| `.box.defender-view` | green | What the SOC sees — "the SOC flip" |
| `.box.soc` | cyan | Career / industry framing |
| `.box.lab-box` | cyan | Hands-on pointer |
| `.box.key-takeaway` | red | The one thing to remember |
| `.box.warn` | orange | Scope / safety / legal warning |
| `.box.tip` | green | Practical advice |
| `.box.note` | red | Ground rule |
| `.box.recall` | amber | Prior-knowledge reminder |

**Never** use `.box.tip` for instructor-only notes. Students receive these files —
no stage directions, no "ask the room", no "what to listen for". (See DECISIONS.md,
2026-08-23.)

---

## 4. Ask-first mechanic

Opens a topic with a question before the reveal. The heading is written so it
reads correctly **out loud to students** — never as an instruction to the instructor.

```html
<div class="ask">
  <span class="ask-t">Discuss first</span>
  <p class="ask-q">The question…</p>
  <details><summary>Reveal</summary><p>The answer…</p></details>
</div>
```

Heading variants in use: `Discuss first`, `Discuss with your pair · 2 min`,
`Rapid fire — call them out`.

---

## 5. Diagrams

All diagrams are **hand-authored inline SVG** — never downloaded images.
Reason: exact control over arrow routing, and they restyle automatically with the palette.

```html
<figure class="dgm">
  <svg viewBox="0 0 920 400" role="img" aria-label="…">…</svg>
  <figcaption><b>Lead-in.</b> Explanation.</figcaption>
</figure>
```

**Hard rules:**
- **Arrows must never cross text labels.** Route them through empty gutters, below
  boxes, or in the gap between panels. This is a standing instructor requirement.
- Use the shared SVG text classes: `.d-title` `.d-lbl` `.d-sub` `.d-mono`.
- Shared arrow markers are defined once in the TCP-handshake diagram and reused by
  ID across the file: `ar-o` (orange), `ar-c` (cyan), `ar-g` (grey), `ar-r` (red).
  **If you remove that diagram, move the `<defs>` block** — every later arrow breaks.
- Everything must fit inside the `viewBox`. Verify with the Playwright bbox check (§8).

### 5a. Interactive diagrams (click-to-reveal)

Wrap each clickable element in `<g class="node" data-node="KEY" tabindex="0">`, then
add one `.dgm-detail[data-detail="KEY"]` panel per key **inside the same `<figure>`**.

```html
<figure class="dgm interactive">
  <svg …>
    <g class="node" data-node="ph2" tabindex="0">
      <rect …/><text …>Scanning</text>
    </g>
  </svg>
  <div class="dgm-hint">Click each phase — …</div>
  <div class="dgm-detail" data-detail="ph2">
    <h5><span class="dd-tag">PHASE 2 · SCANNING</span>Headline</h5>
    <p><b>Attacker does:</b> … <b>SOC sees:</b> … <b>ATT&amp;CK:</b> … <b>Taught in:</b> …</p>
  </div>
</figure>
```

Clicking a node opens its panel and closes the others; clicking the active node again
closes it. Every `data-node` **must** have a matching `data-detail` — the verify
script flags orphans.

Used in Session 1 for: CIA+AA five properties, the 5-phase methodology.

### 5b. Animated diagrams (replay)

Add `class="flow-line"` to the paths that should animate, and a replay button inside
the `<figure>`:

```html
<button type="button" class="dgm-replay" data-replay>↻ Replay the handshake</button>
```

Plays once on load, then on demand. Runs 3 cycles and stops (not infinite — a
looping animation behind a lecturer is distracting).

---

## 6. Practice blocks (external platform labs)

One per topic page, at the **end** of the page, after the takeaway.

```html
<div class="practice">
  <div class="practice-h">
    <span class="pr-t">Practice this topic</span>
    <span class="pr-plat">TryHackMe · Network Fundamentals</span>
  </div>
  <p class="pr-why">Why these rooms, for this topic, at this point in the course.</p>
  <ul class="pr-list">
    <li>
      <div class="pr-row">
        <a href="https://tryhackme.com/room/SLUG" target="_blank" rel="noopener">Room Name</a>
        <span class="res-tag free">Free</span>
        <span class="pr-meta">~30 min · easy</span>
      </div>
      <p class="pr-note">What it covers. <b>Do this one if</b> … / <b>Skip if</b> …</p>
    </li>
  </ul>
</div>
```

**Tags:** `.res-tag.free` (green) · `.res-tag.premium` (amber) · `.res-tag.freetier` (cyan, mixed access)

**Rules:**
1. **Verify every room live before linking it.** Fetch the URL and confirm the exact
   name, the free/premium tier, and the duration. Session 1 caught a dead slug
   (`osimodelfun`) and several rooms wrongly assumed to be free.
2. Every room gets a `pr-note` saying *why that room and when to do it* — never a
   bare link list.
3. Order rooms by **what to do first**, not alphabetically or by platform.
4. Each session's second-to-last page carries a consolidated practice plan table.

---

## 7. Other components

| Component | Markup | Notes |
|---|---|---|
| Lab steps | `<ol class="steps">` | Auto-numbered circles |
| Verification | `<div class="verify"><h4>✓ Verification</h4><ul>…` | Green checklist — every lab step needs one |
| Commands | `<pre><code>` | Always. Never inline a multi-line command |
| Tables | `<div class="tbl-scroll"><table>` | **Always** wrap — this is what stops page overflow |
| Screenshots | `<figure class="shot"><img …>` | Missing files degrade to a labelled placeholder |
| Quiz | `<div class="q mcq" data-correct="b" data-why="…">` | Self-scoring |
| Break timer | `<div data-timer="10">` | Ring countdown |

### The `min-width:0` trap (do not remove)

`.page-layout>*{min-width:0}` in `ceh.css` is **load-bearing**. Without it, a grid
item's implicit minimum is its content's min-content width, so one wide nested table
forces the entire page wider than the viewport instead of scrolling inside its own
`.tbl-scroll`. This was diagnosed as a real grid bug after being mistaken for a
text-wrapping problem. Never delete that rule.

---

## 8. Verification before publishing

Run the Playwright check across viewport widths — `/tmp/verify_s1.js` is the template.

```js
// CRITICAL: the option key is `viewport`, NOT `viewportSize`.
// `viewportSize` is silently ignored — every screenshot comes out at the
// default width and the test passes while proving nothing.
const page = await browser.newPage({ viewport: { width: w, height: 900 } });
```

Checks: document-level horizontal overflow at 1400/1100/900/700/480px · elements wider
than the viewport that are *not* inside a scroll container · SVG text escaping its
`viewBox` · console/page errors · every `data-node` has a `data-detail` · clicking each
node opens exactly one panel · broken images · external link hosts.

Hash navigation caveat: `page.goto(url + '#p8')` on an already-loaded document is a
same-document navigation and will **not** re-run the page script. Use a fresh page or
`reload()` per page you test.
