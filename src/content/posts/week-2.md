---
title: "Two new repos, two superpowers releases, and a lot of Swift"
week: "Week of June 29, 2026"
dateStart: 2026-06-29
dateEnd: 2026-07-05
pubDate: 2026-07-05
summary: "A Linear-tracking plugin and a native-Linux terminal workspace manager both go public, superpowers cuts v6.1.0 and v6.1.1, and serf and teststrip each land hundreds of commits. Ten repos active across both orgs."
---

The second week we're recapping opens two brand-new repositories to the public — a Linear work-tracking plugin and a native Linux terminal workspace manager — while **superpowers** cut two releases (`v6.1.0` and `v6.1.1`). Underneath those headlines, `serf` and `teststrip` each logged several hundred commits of steady product work. Ten repositories saw activity across `prime-radiant-inc` and `obra`.

<section class="summary">

## The week in numbers

<ul class="stats">
<li><strong>10</strong> repos active (3 featured, 7 also shipped)</li>
<li><strong>1,120</strong> commits</li>
<li><strong>10</strong> merged PRs</li>
<li><strong>2</strong> releases cut</li>
<li><strong>3</strong> unique contributors</li>
<li><strong>+923,062 / −19,970</strong> lines changed<sup><a href="#loc-note">*</a></sup></li>
</ul>

<p class="loc-note" id="loc-note"><em>* This week's added-line count is dominated by vendored dependencies, assets, and initial imports — most of it is <code>serf</code>'s +826k, which is vendored code and generated assets rather than hand-written diff. We report the raw figure and flag it rather than silently trimming it.</em></p>

</section>

<section class="featured">

## Featured

<article class="repo">

### [prime-radiant-inc/agent-plugin-linear-use](https://github.com/prime-radiant-inc/agent-plugin-linear-use)

<p class="repo-desc">Keep AI-driven work tracked in Linear: a Claude Code / Codex skill + hook that finds or creates a ticket and moves it through your workflow.</p>

A new public repo (created June 30). The initial commit lands the linear-use plugin itself — a skill plus a hook that automatically finds or creates a Linear ticket for the work an agent is doing and moves it through its workflow states, so AI-driven work stays tracked without a human babysitting the board. The two follow-up commits are an adversarial-review pass and an author-email fix — this one is deliberately public as a worked example of how we run Prime Radiant.

</article>

<article class="repo">

### [obra/insanitty](https://github.com/obra/insanitty)

<p class="repo-desc">Native Linux (GTK4 / libadwaita) terminal workspace manager — a port of Fantastty, built on embedded Ghostty with tmux-backed workspaces and a QUIC remote engine.</p>

Another repo created June 30, and it arrived in a hurry: 90 commits in its first week, all from Jesse. It's a native Linux port of Fantastty — a GTK4/libadwaita terminal workspace manager built on an embedded Ghostty terminal, with tmux-backed workspaces and a QUIC-based remote engine. The week's commits are the shape of a project standing itself up: CI for the Swift toolchain, `.tar.gz` and `.rpm` package targets, an MIT license matching Fantastty, and refreshed end-to-end regression screenshots.

</article>

<article class="repo">

### [obra/superpowers](https://github.com/obra/superpowers)

<p class="repo-desc">An agentic skills framework and software-development methodology that works.</p>

Thirty-six commits across seven merged PRs (Jesse Vincent 27, Drew Ritter 9), and two releases cut this week — `v6.1.0` and `v6.1.1`. The commit run is a concentrated editorial pass on the skills themselves: folding "why order matters" rebuttals into a rationalization table, converting guard sections to that same table format, dropping redundant "Bottom Line" and "Remember" recaps, and compressing bootstrap prose. The theme is density — saying the same things in fewer, sharper words so the skills cost less context to load.

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [prime-radiant-inc/llm-proxy](https://github.com/prime-radiant-inc/llm-proxy)

<p class="repo-desc">Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response for debugging, auditing, and analysis.</p>

Eight commits from Drew, all landing one theme: a config-driven upstream allowlist (default-open) wired into the proxy at construction, plus run-envelope-attributed logging so requests carry provenance through the synthetic-session path. A no-pollution test was made load-bearing to keep the attribution honest.

</article>

<article class="repo">

### [prime-radiant-inc/serf](https://github.com/prime-radiant-inc/serf)

<p class="repo-desc">A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.</p>

371 commits from Jesse — though as the note above flags, the +826k line count is mostly vendored icons and assets, not hand-written change. The actual product work is a polish pass on how serf presents itself: a provider-grouped, prettified, badged model picker in the TUI; a colorblind-safe status vocabulary with distinct shapes rather than color alone; the Lucide icon set vendored for a unified status language across TUI and web; and an amber→blue recolor sweep for "needs you" states.

</article>

<article class="repo">

### [prime-radiant-inc/superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals)

<p class="repo-desc">Behavioral eval lab (Quorum) that drives real coding-agent CLIs through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.</p>

Six commits across two merged PRs (Jesse 4, Drew 2). The scenario work this week is about evidence: scaffolding end-to-end evidence scenarios with a shared shoplist fixture, then a matched pair — a "working feature, verified proof" scenario and a "broken feature, honest report" scenario — that grade whether an agent tells the truth about what it built. Drew added pinned Claude credentials for the harness.

</article>

<article class="repo">

### [prime-radiant-inc/teststrip](https://github.com/prime-radiant-inc/teststrip)

<p class="repo-desc">macOS photo-culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.</p>

589 commits from Jesse — this is a project in the thick of early development. The week's work is squarely about the culling workflow: top-ranked stack culling, signal-backed compare recommendations, a compact rapid-cull rationale, typed smart-collection rules, People face-review status, and a source-availability benchmark verifier. Not ready for use yet, but moving fast.

</article>

<article class="repo">

### [prime-radiant-inc/claude-plugin-stats](https://github.com/prime-radiant-inc/claude-plugin-stats)

<p class="repo-desc">A daily scrape of Claude Code plugin install stats.</p>

Fourteen commits, all from `github-actions[bot]` — the daily scrape and chart-data rebuild doing its job. Included for completeness; it's the robot, not a person.

</article>

<article class="repo">

### [obra/dotfiles](https://github.com/obra/dotfiles)

<p class="repo-desc">Jesse's personal dotfiles.</p>

One commit: a snapshot of 80 files. Housekeeping, but it's real activity in the window, so it's on the list.

</article>

<article class="repo">

### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)

<p class="repo-desc">Curated Claude Code plugin marketplace.</p>

Two commits, both version bumps tracking the superpowers releases: pointing the marketplace at `v6.1.0` and then `v6.1.1`.

</article>

</section>
