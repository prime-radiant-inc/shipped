---
title: "serf goes public"
week: "Week of June 22, 2026"
dateStart: 2026-06-22
dateEnd: 2026-06-28
pubDate: 2026-06-28
summary: "serf cuts its first tagged release, toil starts up, and the superpowers plugin work begins in earnest."
---

The first week we're recapping opens with a release we'd been building toward for a while: **serf** shipped its `v0.1.0`.

<section class="featured">

## Featured

<article class="repo">

### [prime-radiant-inc/serf](https://github.com/prime-radiant-inc/serf)

<p class="repo-desc">A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done — native tool-calling across OpenAI, Anthropic, and Google models.</p>

serf tagged a `snapshot` prerelease and then its first real release, `v0.1.0`, both on June 22. Under the tag was a genuinely busy week — 414 commits to `main` — including a ~58% speed-up to session startup (memoizing per-session git/schema/uname work) and conformance fixes so orphaned tool results emit valid ATIF-v1.7. This is the agent that does the work when nobody's watching, and it's now something you can pin a version of.

</article>

<article class="repo">

### [prime-radiant-inc/toil](https://github.com/prime-radiant-inc/toil)

<p class="repo-desc">A file-defined workflow orchestrator in Go — YAML workflows and runners, disk-persisted state, resume, approvals, and live graph views.</p>

New this week. toil is the piece that turns a pile of steps into a durable, resumable workflow with approvals and a live view of the graph as it runs.

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [obra/superpowers](https://github.com/obra/superpowers)

<p class="repo-desc">An agentic skills framework and software-development methodology that actually works.</p>

A run of Codex-focused cleanup merged: removing Gemini CLI support (EOLed by Google), adding a Codex marketplace manifest, pruning per-harness tool-mapping boilerplate, and stopping the `SessionStart` bootstrap from re-firing on resume.

</article>

<article class="repo">

### [prime-radiant-inc/superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals)

<p class="repo-desc">The Quorum behavioral eval lab — drives real coding-agent CLIs through a QA agent and grades them on workflow compliance.</p>

90 commits, plus a new serf coding-agent harness and coherent `@earendil-works` pi package pins.

</article>

<article class="repo">

### [prime-radiant-inc/llm-proxy](https://github.com/prime-radiant-inc/llm-proxy) · [prime-radiant-inc/gauntlet](https://github.com/prime-radiant-inc/gauntlet) · [prime-radiant-inc/claude-plugin-stats](https://github.com/prime-radiant-inc/claude-plugin-stats)

<p class="repo-desc">Steady work across the supporting cast: the LLM logging proxy, the LLM-driven QA framework, and the daily plugin-install-stats scraper.</p>

</article>

</section>
