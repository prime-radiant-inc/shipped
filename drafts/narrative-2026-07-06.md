# Narrative brief — week of 2026-07-06 (through 2026-07-12)

Grounded in `data/recon-v2-8wk-20260814-CORRECTED.json` (week index 3) + `src/data/weekly-stats.json["2026-07-06"]`. Old draft: `src/content/posts/week-3.md`. No numbers below.

## FEATURED

### prime-radiant-inc/books-for-bots
Rust CLI that converts EPUBs into a single YAML-headed Markdown file with per-chapter byte and line offsets, giving LLM agents a navigation API for token-efficient reading.
**FEATURED — tagged releases `v0.1.0` and `v0.1.1` this week.**
- Shipped the first tagged releases: CI + tag-triggered release workflow building binaries for six platforms, MIT license added.
- Lint/format cleanup (clippy + `cargo fmt`) so CI can enforce both going forward.
- Follow-up `v0.1.1` added a `--version` flag so agents can self-identify their build; fixed EPUB-internal path normalization (forward slashes at the load boundary) and a retired macOS CI runner label.
No divergence vs old draft — matches.

### prime-radiant-inc/obol
Read an AI-agent transcript and estimate what it cost — a Rust core with C-ABI bindings for Python, Go, and TypeScript (Bun + Node).
**FEATURED — tagged release `v0.7.0`.**
- Pure pricing-data release: refreshed the bundled model-price snapshot and added `claude-sonnet-5` pricing.
No divergence vs old draft.

### prime-radiant-inc/teststrip
macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
**FEATURED — new repo created this week (GitHub repo object created 2026-07-10) + tagged releases `models-v1` and `v0.1.0`.**
- Note: the GitHub repo itself was created/made-public this week per the `created_this_week` signal, but the project already had a full week of commit history the prior week (week of 06-29) — read "created this week" as "went public this week," not "started this week."
- Import-pipeline reliability hardening: preflight destination free-space checks before card import, heartbeated import/scan progress so the watchdog survives slow phases, persisted default card-import destination, time-bounded import preview scan so the shown photo count is accurate.
- Security-scoped source-bookmark handling: persist/restore/repair bookmarked source access across reconnects and app relaunch.
- Similarity/culling signal work: Apple feature-print extraction wired into similarity filters, signal-backed visual-similarity stacks, Smart Collection suggestions driven by provider signals, keyword-suggestion review flows.
- First tagged model-asset release (`models-v1`) plus a `v0.1.0` app release.
No divergence vs old draft — old draft's account (import-pipeline trust work) is accurate, just a partial slice of the fuller corrected picture.

## SECOND-TIER

### prime-radiant-inc/stockyard
Coding-agent VM orchestrator: runs coding agents in isolated VMs — Firecracker micro-VMs on Linux (with ZFS-based audit-trail snapshots) and Apple's container tool on macOS.
**second-tier**, one merged PR.
- Archives VM console logs on destroy so the audit trail survives VM teardown.
No divergence vs old draft.

### prime-radiant-inc/serf
A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
**second-tier**, heavy direct-push volume, no merged PRs/release this week.
- ⚠ divergence vs old draft: old draft claimed the week's "big theme" was making the spawn web interface work on mobile (viewport-guarded textareas, mobile row styling, CSS-token cleanup). That mobile work is real but tiny — a handful of commits. The corrected log shows the actual dominant work, continuing straight from last week, is the **fuzz/coverage completion campaign**: a very large share of the week's commits close out fuzz-reachable coverage gaps package-by-package (agent, hub, doctor, contextmgr, execenv, TUI, appsource, jobstore) toward an exact-coverage target.
- Second real feature thread: model-switching support — validating switches up front, gating them on turn state, broadcasting model/effort changes, persisting switch markers, and enforcing replay provenance when a session's model changes mid-run.
- Minor mobile-web polish did land (viewport height/fallback handling, composer dock anchoring for the mobile spawn UI) — real, but a footnote next to the coverage push and model-switching feature.

### prime-radiant-inc/gauntlet
AI-powered QA testing framework that uses LLMs (Claude or GPT) to test web apps, CLI tools, and TUI programs from markdown story cards, returning structured pass/fail verdicts with evidence.
**second-tier**, one merged PR.
- Single targeted fix: give the Claude 5 named tier its full max-output-token cap.
No divergence vs old draft.

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
**second-tier**, no merged PRs (all direct push).
- Deepened serf-as-harness model coverage: OpenRouter preset-identity attestation + BYOK, materialized campaign-level model compatibility, a serf provider-compatibility grid, and a pinned streamed-response-ID fix for serf.
- Mantle/Bedrock credential handling for the launcher: default Claude calls to Bedrock (Mantle) with a direct-opt-out path, scrub host `ANTHROPIC_API_KEY`/AWS creds from the environment so seeded credentials win, reject Mantle credentials on Windows Claude.
- Grader tooling: `--grader-model` CLI flag (defaults to claude-sonnet-5), a Sonnet 4.6→5 drift screen showing no behavioral drift, pinned grader model for the eval agent itself.
No divergence vs old draft — matches (old draft covered a slice of this correctly).

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, bot-only.
- Routine daily scrape + chart rebuild, `github-actions[bot]` only.
No divergence vs old draft.

### prime-radiant-inc/smevals
A framework for running evals against small (and large) models.
**second-tier**, one commit — from an outside contributor (Simon Willison).
- Small vocabulary addition. Notable mainly for the outside contribution.
No divergence vs old draft.

### obra/dotfiles
Jesse's personal dotfiles.
**second-tier**, minimal activity.
- New `/story-loop` command (an agentic goal loop with end-to-end scenario cards) plus its design spec; a small shell-env export for a keyring-backed CLI.
No divergence vs old draft.

### obra/lace
Lightweight agentic coding environment.
**second-tier**, one merged PR (from an outside/ada-sen branch).
- Reliability fixes to background-job notifications: a Slack follow-up hint added to all terminal job notifications, and the runner's last-seen event sequence used as the success-path inject-drain watermark.
No divergence vs old draft.

### obra/superpowers
An agentic skills framework and software-development methodology that works.
**second-tier** — zero commits this week, one merged PR.
- ⚠ divergence vs old draft: old draft told this week's superpowers story as SDD plan-scoped durable-progress-ledger work (one workspace directory per plan, RED/GREEN evals, claim-narrowing writeup) with twelve commits from three contributors. The corrected data shows **zero commits** this week; the only activity is a single merged PR reverting last week's Gemini CLI removal ("Revert 'Remove Gemini CLi support'"), restoring Gemini CLI docs. The SDD-ledger story does not appear in this week's corrected log — it likely belongs to a different week, misattributed under the old shallow-clone data.
- What actually shipped: Gemini CLI support (removed the prior week) came back.
