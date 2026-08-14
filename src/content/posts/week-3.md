---
title: "A week of first releases"
week: "Week of July 6, 2026"
dateStart: 2026-07-06
dateEnd: 2026-07-12
pubDate: 2026-07-12
summary: "books-for-bots and teststrip both cut v0.1.0, obol reaches v0.7.0, and teststrip lands as a new repo the same week it ships."
---

Three first-or-early releases this week, two of them from tools built specifically for the way agents read and cost out their work.

<section class="featured">

## Featured

<article class="repo">

### [prime-radiant-inc/books-for-bots](https://github.com/prime-radiant-inc/books-for-bots) — v0.1.0, v0.1.1

<p class="repo-desc">A Rust CLI that converts EPUBs into a single YAML-headed Markdown file with per-chapter byte and line offsets — a navigation API that lets an LLM agent read a book token-efficiently.</p>

First releases, `v0.1.0` and `v0.1.1`, both on July 11. The idea is simple and useful: instead of dumping a whole book into context, give the agent offsets so it can jump straight to the chapter it needs.

</article>

<article class="repo">

### [prime-radiant-inc/obol](https://github.com/prime-radiant-inc/obol) — v0.7.0

<p class="repo-desc">Read an AI-agent transcript and estimate what it cost — a Rust core with C-ABI bindings for Python, Go, and TypeScript (Bun + Node).</p>

`v0.7.0` (Jul 9). obol answers the question every agent operator eventually asks: what did that run actually cost? The Rust core with cross-language bindings means you can ask it from whatever stack you're already in.

</article>

<article class="repo">

### [prime-radiant-inc/teststrip](https://github.com/prime-radiant-inc/teststrip) — v0.1.0

<p class="repo-desc">A macOS photo-culling app: catalog-first, non-destructive, AI-assisted. Early development, not ready for use.</p>

Created and shipped in the same week — the repo went public on Jul 10, followed by a `models-v1` asset release and `v0.1.0` on Jul 12, on the back of 675 commits. Still early, but moving.

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [prime-radiant-inc/serf](https://github.com/prime-radiant-inc/serf)

<p class="repo-desc">The non-interactive coding agent.</p>

Another ~960-commit week.

</article>

<article class="repo">

### [prime-radiant-inc/stockyard](https://github.com/prime-radiant-inc/stockyard)

<p class="repo-desc">A coding-agent VM orchestrator: runs agents in isolated Firecracker micro-VMs on Linux (with ZFS audit-trail snapshots) and Apple's container tool on macOS.</p>

Now archives VM console logs on destroy — so a torn-down VM still leaves an audit trail.

</article>

<article class="repo">

### [obra/lace](https://github.com/obra/lace) · [prime-radiant-inc/gauntlet](https://github.com/prime-radiant-inc/gauntlet) · [prime-radiant-inc/smevals](https://github.com/prime-radiant-inc/smevals)

<p class="repo-desc">lace fixed a terminal job-notification Slack hint and an inject-drain watermark; gauntlet gave the Claude 5 named tier its full 16,384-token output cap.</p>

</article>

</section>
