---
title: "smevals and blogosphere arrive"
week: "Week of July 13, 2026"
dateStart: 2026-07-13
dateEnd: 2026-07-19
pubDate: 2026-07-19
summary: "Two new projects — smevals and blogosphere — plus obol v0.8.0 and teststrip v0.2.0, and a heavy week of serf webui work."
---

Two more repos went public this week, and the eval tooling picked up a dedicated home for small-model work.

<section class="featured">

## Featured

<article class="repo">

### [prime-radiant-inc/smevals](https://github.com/prime-radiant-inc/smevals) — v0.1.0, v0.2.0

<p class="repo-desc">A framework for running evals against small (and large) models.</p>

Created Jul 17 and shipped `v0.1.0` and `v0.2.0` within a day, on 30 commits. A focused home for the small-model eval work that had been living inside the larger eval lab.

</article>

<article class="repo">

### [obra/blogosphere](https://github.com/obra/blogosphere)

<p class="repo-desc">A local-first, multi-platform blogging client for an 11ty blog that lives in a GitHub repo — the repo is the database.</p>

New this week. The premise is nice: no separate CMS, no database — your Git repo *is* the store, and the client is just a good editor on top of it.

</article>

<article class="repo">

### [prime-radiant-inc/obol](https://github.com/prime-radiant-inc/obol) — v0.8.0

<p class="repo-desc">Transcript cost estimation with a Rust core and cross-language bindings.</p>

`v0.8.0` (Jul 14), continuing the steady release cadence.

</article>

<article class="repo">

### [prime-radiant-inc/teststrip](https://github.com/prime-radiant-inc/teststrip) — v0.2.0

<p class="repo-desc">The macOS photo-culling app.</p>

`v0.2.0` (Jul 13) on 246 commits — a fast follow to the previous week's debut.

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [prime-radiant-inc/serf](https://github.com/prime-radiant-inc/serf)

<p class="repo-desc">The non-interactive coding agent.</p>

A big webui week (593 commits): edit or cancel a queued message before it's consumed, promote a queued follow-up to steering, configurable delegate-turn limits, and a mobile full-width modal sheet for the sidebar menus.

</article>

<article class="repo">

### [obra/winpepper](https://github.com/obra/winpepper)

<p class="repo-desc">Windows-native local dictation — hold a hotkey, speak, release, and cleaned-up words appear in the focused app. All local.</p>

Kept the app responsive during model downloads and fixed modifier-only hotkey capture.

</article>

<article class="repo">

### [prime-radiant-inc/greenfield](https://github.com/prime-radiant-inc/greenfield)

<p class="repo-desc">A Claude Code plugin that reverse-engineers clean behavioral specs, test vectors, and acceptance criteria from any codebase — with a provenance trail so a fresh team can reimplement without inheriting the original's structure.</p>

Restructured its skills into `SKILL.md` directories.

</article>

<article class="repo">

### [obra/superpowers](https://github.com/obra/superpowers) · [prime-radiant-inc/superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals) · [prime-radiant-inc/terminal-bench-analysis](https://github.com/prime-radiant-inc/terminal-bench-analysis)

<p class="repo-desc">superpowers landed an SDD fix-loop redesign (resume-based fix rounds, a five-round breaker, controller adjudication); the eval lab ran a hardening campaign; and terminal-bench-analysis kept pulling Terminal Bench 2 results into queryable SQLite.</p>

</article>

</section>
