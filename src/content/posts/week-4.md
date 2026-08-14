---
title: "New tools, more contributors, and a three-million-line mirage"
week: "Week of July 13, 2026"
dateStart: 2026-07-13
dateEnd: 2026-07-19
pubDate: 2026-07-19
summary: "blogosphere goes public, obol and smevals cut releases, teststrip keeps sprinting, and the contributor list widens to Simon Willison, Eden, Dan Shapiro, and more. Fourteen repos active — and a bot that 'changed' 3.5M lines without changing anything."
---

This week the contributor list is the story as much as the code: alongside the core team, commits landed from Simon Willison, Dan Shapiro, Eden, and Gaurav Dubey. A new local-first blogging client went public, `obol` and `smevals` cut releases, and `teststrip` kept up its relentless pace. Fourteen repositories were active across both orgs — and one of them produced a line count worth explaining before we do anything else.

<section class="summary">

## The week in numbers

<ul class="stats">
<li><strong>14</strong> repos active (4 featured, 10 also shipped)</li>
<li><strong>1,035</strong> commits</li>
<li><strong>23</strong> merged PRs</li>
<li><strong>4</strong> releases cut</li>
<li><strong>7</strong> unique contributors</li>
<li><strong>+290,540 / −53,585</strong> lines changed<sup><a href="#loc-note">*</a></sup></li>
</ul>

<p class="loc-note" id="loc-note"><em>* We report <strong>+290,540</strong> — the "de-botted" figure — as the real number. The raw diff was +3,778,040, but +3,487,500 of that is a single <code>github-actions[bot]</code> commit in <code>terminal-bench-analysis</code> that regenerated a README across 33,477 files with, per its own commit message, "no new data." We exclude generated bot commits like that from the headline rather than let them inflate it. The de-botted figure is what people actually wrote.</em></p>

</section>

<section class="featured">

## Featured

<article class="repo">

### [prime-radiant-inc/obol](https://github.com/prime-radiant-inc/obol)

<p class="repo-desc">Read an AI-agent transcript and estimate what it cost — a Rust core with C-ABI bindings for Python, Go, and TypeScript.</p>

`v0.8.0` (Drew). The release refreshes the bundled price snapshot to add the gpt-5.6 family and repairs some CI lint drift. Cost estimation is only useful if the price data is current, so a steady cadence of price refreshes is exactly the maintenance this tool needs.

</article>

<article class="repo">

### [prime-radiant-inc/teststrip](https://github.com/prime-radiant-inc/teststrip)

<p class="repo-desc">macOS photo-culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.</p>

246 commits and another release. The week's work is deep in the culling UI: a persisted burst-stack capture-interval preference, standalone frames showing their own thumbnail in the cull burst rail, a repositioned muted RAW+JPEG badge, and a fix so Library-grid activation opens the Library loupe rather than the culling loupe. Detail work — the kind that separates a demo from a tool you'd trust with your photos.

</article>

<article class="repo">

### [prime-radiant-inc/smevals](https://github.com/prime-radiant-inc/smevals)

<p class="repo-desc">A framework for running evals against small (and large) models.</p>

30 commits from Simon Willison, capped by a `0.2.0` release. The week is a real polish pass: a much-improved README, an environment-variable rename (`SMEVAL_*` → `SMEVALS_*`), accepting a single string where a list was expected, and Python 3.10+ compatibility. An outside maintainer taking a project from rough to releasable.

</article>

<article class="repo">

### [obra/blogosphere](https://github.com/obra/blogosphere)

<p class="repo-desc">Local-first, multi-platform blogging client for an 11ty blog that lives in a GitHub repo — the repo is the database.</p>

New and public this week (35 commits, Jesse). The premise: a local-first blogging client where the GitHub repo *is* the database — an 11ty blog you edit from any device. The week's commits are the public-launch essentials: an MIT license, a README for the public repo, a boot-failure screen, and "platform-honest" connect copy that stops assuming you're on a Mac when you're on a phone.

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [prime-radiant-inc/llm-proxy](https://github.com/prime-radiant-inc/llm-proxy)

<p class="repo-desc">Transparent logging proxy for LLM API traffic that records every request and response for debugging, auditing, and analysis.</p>

Eleven commits from Drew, focused on the Bedrock relay and capture accuracy: stamping capture facts on mantle response records, pairing the relay's request-creation and dial failures, and stopping aborted relays from mis-stamping a clean termination. Correctness work on the audit trail.

</article>

<article class="repo">

### [prime-radiant-inc/serf](https://github.com/prime-radiant-inc/serf)

<p class="repo-desc">A non-interactive coding agent that reads, writes, runs commands, and searches code in a loop across OpenAI, Anthropic, and Google models.</p>

589 commits across eight merged PRs. The theme is quality-of-life in the spawn interface: a "recent projects" list (the 15 most recently used project dirs) prepopulating both the TUI spawn field and the web session-creation picker, plus the ability to edit or cancel an unconsumed queued message. A snake_case REST contract cleanup keeps the CI naming gate happy.

</article>

<article class="repo">

### [prime-radiant-inc/gauntlet](https://github.com/prime-radiant-inc/gauntlet)

<p class="repo-desc">AI-powered QA testing framework that drives web apps, CLI tools, and TUI programs from markdown story cards.</p>

One commit from Eden: creating the LICENSE. Small, but it's the kind of housekeeping that has to happen before a repo can be shared.

</article>

<article class="repo">

### [prime-radiant-inc/terminal-bench-analysis](https://github.com/prime-radiant-inc/terminal-bench-analysis)

<p class="repo-desc">Fetches detailed JSON results from the Terminal Bench 2 leaderboard, loads them into SQLite, and publishes queryable analysis via Datasette.</p>

One commit this week — and it's the one from the note above. `github-actions[bot]` regenerated the README across 33,477 files with, in its own words, "no new data." That's the +3.49M-line mirage we excluded from the headline. The repo itself is a genuinely useful thing (queryable Terminal Bench 2 analysis via Datasette); this particular commit just wasn't human work.

</article>

<article class="repo">

### [prime-radiant-inc/greenfield](https://github.com/prime-radiant-inc/greenfield)

<p class="repo-desc">A Claude Code plugin that reverse-engineers clean behavioral specs, test vectors, and acceptance criteria from any codebase — with a provenance trail so a fresh team can reimplement without inheriting the original's structure.</p>

One merged PR (Eden, from an outside contributor's branch) fixing the skills-directory layout. A small structural correction to a genuinely interesting plugin.

</article>

<article class="repo">

### [prime-radiant-inc/superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals)

<p class="repo-desc">Behavioral eval lab (Quorum) that drives real coding-agent CLIs through a QA agent and grades them on workflow compliance.</p>

89 commits across three merged PRs (Drew 77, Jesse 12). Mostly experiment documentation: a contingency wave of protocol re-runs, structural-blocks confirmation batches, and final verdicts with economics for a specific PR review. The lab is increasingly a record of what was measured and why, not just the harness that measures it.

</article>

<article class="repo">

### [prime-radiant-inc/claude-plugin-stats](https://github.com/prime-radiant-inc/claude-plugin-stats)

<p class="repo-desc">A daily scrape of Claude Code plugin install stats.</p>

Seven commits, all `github-actions[bot]` — the daily chart rebuild. The robot, as ever.

</article>

<article class="repo">

### [obra/dotfiles](https://github.com/obra/dotfiles)

<p class="repo-desc">Jesse's personal dotfiles.</p>

Seven commits building a safe Arq snapshot cleaner: a tested cleanup lifecycle, failing closed when APFS snapshot inspection fails, and restoring services across a bootout interruption. Careful backup tooling — "fail closed" is the right instinct for anything that deletes.

</article>

<article class="repo">

### [obra/superpowers](https://github.com/obra/superpowers)

<p class="repo-desc">An agentic skills framework and software-development methodology that works.</p>

Eleven commits across nine merged PRs (Jesse 10, Gaurav Dubey 1). The centerpiece is an SDD lifecycle restructure: a resume-based fix loop, a five-round breaker to stop endless fix cycles, and the rationalization-table pattern applied again — landed with a full design spec and implementation plan.

</article>

<article class="repo">

### [obra/winpepper](https://github.com/obra/winpepper)

<p class="repo-desc">Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.</p>

Three commits across two merged PRs, all from Dan Shapiro: keeping the app responsive during model downloads, and fixing modifier-only hotkey capture and key swallowing. Fully-local dictation on Windows, moving forward under an outside contributor's hand.

</article>

</section>
