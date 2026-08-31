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

`.page-layout>*{min-width:0}` and `.split>*,.grid>*,.tiles>*,.stats>*,.bio>*{min-width:0}`
in `ceh.css` are **load-bearing**. Without them, a grid item's implicit minimum is its
content's min-content width, so one wide nested table — or a single long `<pre>` command
line — forces the entire page wider than the viewport instead of scrolling inside its own
`.tbl-scroll`. First diagnosed on `.page-layout` (mistaken for a text-wrapping problem);
the `.split` half was found on Session 3 on 2026-08-31 by the width audit below, where a
`<pre>` pushed a `.split` track to 639px and the document 100–393px wide. Never delete
either rule.

---

## 7b. Width discipline (added 2026-08-31 — the page must FILL the browser)

**One container, and only one.** `.wrap` is it: `max-width:var(--maxw)` (1680px),
`margin-inline:auto`, `padding-inline:var(--gutter)` = `clamp(16px,3vw,40px)`. Header,
progress bar, hero, main and footer all use it, so every left edge lines up.
*Nothing else in the stylesheet may set `max-width` on a layout element.* A later
`main{max-width:none}` or `.content{max-width:1100px}` silently cancels the container and
you get two alignments on one page — and it is invisible below the cap, which is why the
audit runs at **1920**, not just 1400.

**Never use the `padding` shorthand for section spacing.** `padding-block` only.
`.section{padding:48px 0}` overrides `.wrap`'s horizontal padding and the text lands on
the screen edge at 480px. This was a live bug on three elements —
`main.wrap.section`, `section.wrap.section-sm`, `div.wrap.progress-inner` — all fixed
2026-08-31.

**Cap prose, not objects.** `.content p`, `.content>ul`, `.content>ol` and the lede cap at
`var(--prose)` = 96ch. Tables, grids, figures, cards, boxes and practice blocks fill the
whole container — they are explicitly reset to `max-width:none`. A 170-character line is
not "using the width".

**Grids use `auto-fit`, never `auto-fill`**, with `minmax(min(100%,X),1fr)`:
cards 350px, tiles 236px, stat tiles 178px. `auto-fill` leaves dead empty tracks when a
section has fewer items than the row can hold.

**Tables are rules, not a grid of boxes.** `.tbl-scroll` is a rounded, bordered,
shadowed panel with `overflow-x:auto`; the table is `border-collapse:separate`,
`table-layout:fixed`, `min-width:660px`, no vertical borders, a 1px hairline under each
row, a small uppercase **monospace** header on `--panel-2`, and a subtle row hover.
Column widths are declared **per table** via `<colgroup><col style="width:N%">` —
generated from that table's own content by `scripts/gen_table_colgroups.py`, which weights
each column by `max(avg, header*0.85, maxCell*0.45)` so a single long outlier still earns
width. Never use a blanket `td:last-child{width:1%}` — it reads fine on a three-column
table and crushes the prose column of a two-column one. Where a table's widest prose
column would still render under 190px at 660px, the generator writes that table its own
`style="min-width:NNNpx"`.

**Diagrams scale with the page.** Inline SVG keeps `viewBox` and carries no `width`/
`height` attributes; `.dgm svg{width:100%;height:auto;min-width:780px}` inside the
`overflow-x:auto` panel, so a diagram grows with the page and scrolls on a phone instead
of shrinking its labels to 7px.

**Section headings** are `display:flex` with an `::after` that is a 1px gradient rule
running to the right edge — this one detail is most of what separates "designed" from
"stretched". Inline children inside an `h2` must stay in normal flow, so the heading's
text is wrapped in `<span class="h-t">`; the flex `gap` would otherwise open a hole
between the text and any nested `<span>`/`<em>`.

**One shared depth token.** `--depth` (inset top highlight + soft drop shadow) is used by
every raised surface; `--depth-hi` is the hover state on cards and tiles, which also
raise 3px and change border colour. Nothing else glows, pulses or animates.
`.card` is `display:flex;flex-direction:column` with `.card-meta{margin-top:auto}` so
badge rows pin to the card bottom instead of leaving ragged space.

---

## 8. Verification before publishing

Run the Playwright check across viewport widths — `/tmp/verify_s1.js` is the template.

```js
// CRITICAL: the option key is `viewport`, NOT `viewportSize`.
// `viewportSize` is silently ignored — every screenshot comes out at the
// default width and the test passes while proving nothing.
const page = await browser.newPage({ viewport: { width: w, height: 900 } });
```

Checks: document-level horizontal overflow at **1920**/1400/1100/900/700/480px ·
elements wider than the viewport that are *not* inside a scroll container · SVG text
escaping its `viewBox` · console/page errors · every `data-node` has a `data-detail` ·
clicking each node opens exactly one panel · broken images · external link hosts.

### The four width assertions (added 2026-08-31) — `scripts/audit_layout.js`

At **every** width, programmatically assert:

1. every `.wrap` has the same `getBoundingClientRect().left` — catches a cancelled container;
2. every `.wrap` has `paddingLeft >= 14px` — catches the padding-shorthand trap;
3. no `td`/`th` holding more than 55 characters renders narrower than 190px — catches a squeezed prose column;
4. the document does not scroll horizontally, and no element sits outside a scroll container.

Run with `.page{display:block!important}` injected so one pass covers every paged section.
**1920 is not optional.** With a 1680px cap, any rule that cancels the container is
invisible at 1400 — that is exactly where the bug hides.

**Then break each check on purpose and confirm it fails.** A check that passes the first
time has proven nothing. `audit_layout.js` takes `BREAK=` for this; all six sabotages are
known-failing as of 2026-08-31:

| `BREAK=` | Sabotage | Must fail |
|---|---|---|
| `edges` | `main.wrap{max-width:1100px}` | 1920 + 1400 only |
| `padding` | `.section{padding:48px 0}` | every width |
| `nocolgroup` | strip `<colgroup>`, `table-layout:auto`, `td:last-child{width:1%}` | every width, 25–43 cells |
| `overflow` | `.tbl-scroll{overflow-x:visible}` | 480/700/1100 |
| `minwidth` | `.split>*{min-width:auto}` | S3 at 4 widths |
| `tablemw` | `.tbl-scroll table{min-width:0}` | 480 on all sessions |

A sabotage that does *not* fail is itself a finding: `td:last-child{width:1%}` alone
passes, because the per-table `<colgroup>` overrides it — which is the point of having one.

Hash navigation caveat: `page.goto(url + '#p8')` on an already-loaded document is a
same-document navigation and will **not** re-run the page script. Use a fresh page or
`reload()` per page you test.
