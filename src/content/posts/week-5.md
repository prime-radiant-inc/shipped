---
title: "serf's 1,467-commit week, superpowers v6.2.0, and winpepper ships"
week: "Week of July 20, 2026"
dateStart: 2026-07-20
dateEnd: 2026-07-26
pubDate: 2026-07-26
summary: "serf logs 1,467 commits, superpowers cuts v6.2.0, winpepper ships after a 368-commit sprint, and outside contributors land on superpowers. Fourteen repos active, nine contributors, three releases."
---

If one number captures this week it's `serf`'s 1,467 commits — a genuinely enormous push on the coding agent's session and pane architecture. Around it, `superpowers` cut `v6.2.0`, `winpepper` shipped after a 368-commit sprint, and the contributor list kept widening, with outside developers landing fixes on `superpowers`. Fourteen repositories active across both orgs.

<section class="summary">

## The week in numbers

<ul class="stats">
<li><strong>14</strong> repos active (2 featured, 12 also shipped)</li>
<li><strong>1,902</strong> commits</li>
<li><strong>19</strong> merged PRs</li>
<li><strong>3</strong> releases cut</li>
<li><strong>9</strong> unique contributors</li>
<li><strong>+318,281 / −98,332</strong> lines changed<sup><a href="#loc-note">*</a></sup></li>
</ul>

<p class="loc-note" id="loc-note"><em>* No bot mega-commits this week, so raw equals de-botted. Some of the added lines are still license text and vendored files (llm-proxy's Apache-2.0 license alone is +29k across 77 files) rather than logic, but the bulk this week is real change.</em></p>

</section>

<section class="featured">

## Featured

<article class="repo">

### [obra/superpowers](https://github.com/obra/superpowers)

<p class="repo-desc">An agentic skills framework and software-development methodology that works.</p>

`v6.2.0` shipped this week, rolling up the plan-scoped SDD workspace and resume-based fix loop from the previous weeks, a skills compression sweep, and a Windows `SessionStart` fix. Four commits across four merged PRs — and notably two of them came from outside the core team: dev_Hakaze fixed `find-polluter.sh` to match `find -path ./` prefixes, and Mark Rada dropped a dangling docs anchor. A framework people outside the building are now contributing to.

</article>

<article class="repo">

### [obra/winpepper](https://github.com/obra/winpepper)

<p class="repo-desc">Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.</p>

A 368-commit week (danshapiro 350, plus AI agents Codex and Amplifier committing alongside him, and one from Jesse) across five merged PRs. The work is a serious reliability pass: implementation plans hardened from "load-bearing validation" findings for midpaste focus, paste pacing, and settings lost-update races, plus eval infrastructure with deterministic delete-drain, argument validation, and loud driver failures. Local dictation on Windows is maturing fast under an outside maintainer.

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [prime-radiant-inc/serf](https://github.com/prime-radiant-inc/serf)

<p class="repo-desc">A non-interactive coding agent that reads, writes, runs commands, and searches code in a loop across OpenAI, Anthropic, and Google models.</p>

1,467 commits from Jesse — the week's headline volume. The work is deep in session and UI architecture: a delegate-transcript UI audit, pane-routing repairs, fixing nested-session owner promotion from a secondary, and nailing down settings and session-routing placement contracts. This is the kind of week where a tool's multi-session model gets rebuilt underneath it.

</article>

<article class="repo">

### [prime-radiant-inc/llm-proxy](https://github.com/prime-radiant-inc/llm-proxy)

<p class="repo-desc">Transparent logging proxy for LLM API traffic that records every request and response for debugging, auditing, and analysis.</p>

Four commits across three merged PRs (Jesse): an AWS SigV4 signing mode for the Anthropic passthrough (so the proxy can front Bedrock), stripping hop-by-hop headers before signing with a clean mode-based rollback, and an Apache-2.0 license. The SigV4 work is the interesting part — it lets the proxy sign requests to AWS-hosted models.

</article>

<article class="repo">

### [prime-radiant-inc/stockyard](https://github.com/prime-radiant-inc/stockyard)

<p class="repo-desc">Coding-agent VM orchestrator: runs coding agents in isolated Firecracker micro-VMs on Linux and Apple's container tool on macOS.</p>

Sixteen commits from Drew, all on safe task destruction: requiring names to destroy named tasks, failing closed on identity errors, and safely quoting destroy-confirmation names. When you're tearing down VMs, "fail closed" is exactly the posture you want.

</article>

<article class="repo">

### [prime-radiant-inc/superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals)

<p class="repo-desc">Behavioral eval lab (Quorum) that drives real coding-agent CLIs through a QA agent and grades them on workflow compliance.</p>

Fourteen commits (Jesse), documenting a Hermes-4 bring-up: a RED bootstrap verdict and mechanism autopsy, a clone-faithful plugin-staging fix, and then a full RED-to-GREEN pair — with the honest finding that Hermes-4 via OpenRouter is structurally impossible to eval because it exposes no tool-use endpoints. Negative results, recorded as carefully as positive ones.

</article>

<article class="repo">

### [obra/lace](https://github.com/obra/lace)

<p class="repo-desc">Lightweight agentic coding environment.</p>

Five commits across three merged PRs (Jesse): rewriting the Bedrock provider on `AnthropicBedrockMantle` for full Anthropic parity, treating SDK connection errors as retryable, and a test-hygiene fix so integration suites run on the model they actually use. Bedrock parity is the throughline with llm-proxy's SigV4 work — a coordinated push to run Anthropic models through AWS.

</article>

<article class="repo">

### [prime-radiant-inc/smevals](https://github.com/prime-radiant-inc/smevals)

<p class="repo-desc">A framework for running evals against small (and large) models.</p>

Seven commits from Simon Willison: a per-task view page for a specific eval, a `run -n X` flag to run an eval X times and distinguish errors from failures, GitHub Actions workflows, and a traversal-bug fix in `smevals serve`. Steady, practical iteration from an outside maintainer.

</article>

<article class="repo">

### [obra/blogosphere](https://github.com/obra/blogosphere)

<p class="repo-desc">Local-first, multi-platform blogging client for an 11ty blog that lives in a GitHub repo.</p>

Four commits (Jesse) on durability: fixing a "database is locked" publish failure with single-statement rename pairs, and surviving hard kills via Windows PAT persistence and a bounded typing-buffer. The unglamorous work of not losing someone's draft.

</article>

<article class="repo">

### [prime-radiant-inc/teststrip](https://github.com/prime-radiant-inc/teststrip)

<p class="repo-desc">macOS photo-culling app — catalog-first, non-destructive, AI-assisted. Early development.</p>

A quiet week — three commits merging earlier work: compiling Core ML face models once, and a round of dogfood culling and library fixes.

</article>

<article class="repo">

### [prime-radiant-inc/terminal-bench-analysis](https://github.com/prime-radiant-inc/terminal-bench-analysis)

<p class="repo-desc">Queryable Terminal Bench 2 leaderboard analysis via SQLite + Datasette.</p>

One `github-actions[bot]` commit regenerating the README — this week a trivial two-line change, unlike last week's mirage. Included for completeness.

</article>

<article class="repo">

### [prime-radiant-inc/claude-plugin-stats](https://github.com/prime-radiant-inc/claude-plugin-stats)

<p class="repo-desc">A daily scrape of Claude Code plugin install stats.</p>

Seven `github-actions[bot]` commits — the daily chart rebuild.

</article>

<article class="repo">

### [obra/dotfiles](https://github.com/obra/dotfiles)

<p class="repo-desc">Jesse's personal dotfiles.</p>

One commit, titled "ADHD instructions." Personal, but on the list for completeness.

</article>

<article class="repo">

### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)

<p class="repo-desc">Curated Claude Code plugin marketplace.</p>

One commit: bumping the marketplace to superpowers `v6.2.0`.

</article>

</section>
