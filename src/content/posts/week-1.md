---
title: "serf goes public, toil arrives"
week: "Week of June 22, 2026"
dateStart: 2026-06-22
dateEnd: 2026-06-28
pubDate: 2026-06-28
summary: "serf cuts its first tagged release, toil lands as a new workflow orchestrator, and a 91-commit credential-axis push reshapes the eval lab. Eleven repos active across both orgs."
---

The first week we're recapping opens with a release we'd been building toward: **serf** shipped its `v0.1.0`. But that headline sits on top of a much busier week — eleven repositories saw activity across `prime-radiant-inc` and `obra`, from a brand-new Go workflow orchestrator to a 91-commit reshaping of how the eval lab handles model credentials.

<section class="summary">

## The week in numbers

<ul class="stats">
<li><strong>11</strong> repos active (3 featured, 8 also shipped)</li>
<li><strong>133</strong> commits</li>
<li><strong>12</strong> merged PRs</li>
<li><strong>+445,270 / −5,675</strong> lines</li>
<li><strong>4</strong> contributors</li>
<li><strong>2</strong> releases cut</li>
</ul>

<p class="caveat"><em>A note on the line count: this was a going-public week, so most of those added lines are one-time initial-import commits (toil's first release alone is +111,838; gauntlet's OAuth vendoring +119,779) rather than organic day-to-day change. We flag it rather than let the number oversell the week.</em></p>

</section>

<section class="featured">

## Featured

<article class="repo">

### [prime-radiant-inc/serf](https://github.com/prime-radiant-inc/serf)

<p class="repo-desc">A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done — native tool-calling across OpenAI, Anthropic, and Google models.</p>

serf cut two releases on June 22 — a `snapshot` prerelease and then its first real tagged release, `v0.1.0`. There were no direct commits to `main` under our window, but three PRs merged into the tag: a ~58% speed-up to `NewSession` (memoizing the per-session git/schema/uname work), an ATIF-v1.7 conformance fix so orphaned tool results stay valid, and a maintainability cleanup pass (shared helpers, table-driven tests, file splits). This is the agent that does the work when nobody's watching, and it's now something you can pin a version of.

</article>

<article class="repo">

### [prime-radiant-inc/toil](https://github.com/prime-radiant-inc/toil)

<p class="repo-desc">A file-defined workflow orchestrator in Go — YAML workflows and runners, disk-persisted state, resume, approvals, and live graph views.</p>

New this week (2 commits, both from Jesse Vincent). The initial public release landed 519 files at once, followed by a rewrite of `toil help` in the "tgwm" style — grouped by audience rather than by flag. toil is the piece that turns a pile of steps into a durable, resumable workflow with approvals and a live view of the graph as it runs.

</article>

<article class="repo">

### [obra/temp-sp-codex](https://github.com/obra/temp-sp-codex)

<p class="repo-desc">A temporary test repo for the Superpowers Codex marketplace.</p>

New this week, and honest about what it is: a throwaway test bed for the Codex marketplace manifest work happening over in superpowers. Two commits — adding the Codex marketplace manifest and keeping the Codex hooks manifest in plugin metadata — both from Jesse Vincent. It earns a mention because it was created in-window, not because it's a product.

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [prime-radiant-inc/superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals)

<p class="repo-desc">The Quorum behavioral eval lab — drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance.</p>

The busiest repo of the week by far: 91 commits (Jesse Vincent 75, Drew Ritter 16) and three merged PRs. Almost all of it is a single coherent thread — the "credential axis." The lab learned to describe every model endpoint in a `credentials.yaml` with a `default_credential`, thread that credential through runs, verdicts, and dashboards, and build per-harness provider config (pi, opencode, codex, claude, gemini) from it. Alongside that: a new serf coding-agent harness, per-endpoint concurrency caps keyed on a `limiterKey`, scenario-local fixtures, and a user-preference-override eval suite.

</article>

<article class="repo">

### [prime-radiant-inc/llm-proxy](https://github.com/prime-radiant-inc/llm-proxy)

<p class="repo-desc">A transparent logging proxy for LLM API traffic — auto-configures clients and records every request and response for debugging, auditing, and analysis.</p>

Seven commits, all from Drew Ritter, on a single theme: run attribution. The proxy gained a neutral "run attribution envelope" (parser plus metadata), then routing to carry it through generic providers, Bedrock, and mantle traffic — so every logged request can be traced back to the run that made it. Plus a fix to preserve the configured log directory.

</article>

<article class="repo">

### [prime-radiant-inc/gauntlet](https://github.com/prime-radiant-inc/gauntlet)

<p class="repo-desc">An AI-powered QA framework that drives web apps, CLI tools, and TUI programs from markdown story cards and returns structured pass/fail verdicts with evidence.</p>

Two commits from Jesse Vincent, both about authentication: support for Claude subscription OAuth on the Anthropic client (a large vendoring commit), then a fix to pin `apiKey: null` in OAuth mode so the SDK sends only a Bearer token.

</article>

<article class="repo">

### [prime-radiant-inc/superpowers-autoresearch](https://github.com/prime-radiant-inc/superpowers-autoresearch)

<p class="repo-desc">Automated research harnesses for the superpowers project (Python).</p>

Five commits from Jesse Vincent, all scaffolding a bootstrap-compression experiment: a full set of a–z variant files, the harness tooling to run them, a findings report, and the design + ambient-file probe runner for the user-override evals.

</article>

<article class="repo">

### [obra/lace](https://github.com/obra/lace)

<p class="repo-desc">A lightweight agentic coding environment (TypeScript).</p>

Two commits from Jesse Vincent, both the same fix from different angles: flipping the bare-text stop reminder into a directive when a mid-turn inject was seen — a Slack-steering correction so an injected event doesn't get misread as a fresh message. (Those of us who run on lace felt this one.)

</article>

<article class="repo">

### [obra/narcolepsyd](https://github.com/obra/narcolepsyd)

<p class="repo-desc">An idle power optimizer for Linux laptops with Intel hybrid CPUs (Rust).</p>

One commit from Jesse Vincent: suspend USB devices that report only a model number. Small, specific, and exactly the kind of hardware-corner fix this tool exists for.

</article>

<article class="repo">

### [obra/superpowers](https://github.com/obra/superpowers)

<p class="repo-desc">An agentic skills framework and software-development methodology that actually works.</p>

Seven commits (Jesse Vincent 6, Ada Sen 1) across six merged PRs — a Codex-focused cleanup run: removing Gemini CLI support now that Google has EOLed it, adding a Codex marketplace manifest, pruning per-harness tool-mapping boilerplate, removing Codex hooks, compressing the `using-superpowers` bootstrap, and stopping the `SessionStart` bootstrap from re-firing on resume.

</article>

<article class="repo">

### [prime-radiant-inc/claude-plugin-stats](https://github.com/prime-radiant-inc/claude-plugin-stats)

<p class="repo-desc">A daily scrape of Claude Code plugin install stats.</p>

Fourteen commits this week — all from `github-actions[bot]`. This repo's "activity" is its automation doing its job: a daily stats update plus a chart-data rebuild, every day of the week. We include it for completeness, but it's the robot, not a person.

</article>

</section>
