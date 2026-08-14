# Narrative brief — week of 2026-07-20 (through 2026-07-26)

Grounded in `data/recon-v2-8wk-20260814-CORRECTED.json` (week index 5) + `src/data/weekly-stats.json["2026-07-20"]`. Old draft: `src/content/posts/week-5.md`. No numbers below.

## FEATURED

### obra/superpowers
An agentic skills framework and software-development methodology that works.
**FEATURED — tagged release `v6.2.0`.**
- Release rolls up work that merged over the prior weeks: the SDD plan-scoped workspace + resume-based fix loop, a skills-compression sweep, and the Windows `SessionStart` Git-Bash dispatch fix.
- Two outside contributors landed fixes in the same release: a `find-polluter.sh` path-matching fix, and a dangling-docs-anchor cleanup.
No divergence vs old draft — matches well.

### obra/winpepper
Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
**FEATURED — tagged releases `v0.7.0-alpha` and `v0.6.2-alpha`, plus a commit-message-only version bump.**
- ⚠ divergence vs old draft: old draft covered this week purely as a "reliability pass" (hardened implementation plans, eval infra) and never mentioned that the week culminated in **two tagged releases**, including a streaming release. The merged-PR-grounded headline is bigger: AssemblyAI cloud ASR added alongside the local engine, sleep/resume incident fixes (error taxonomy, recovery-driven clearing, hook reinstall), keyboard-hook hardening, a per-user MSI installer, and consumer polish (toast policy, pill fixes, ASR config consolidation, live model swap).
- Old draft's reliability-pass details (load-bearing-validation hardening for midpaste/settings races) are real and still worth keeping as the engineering-diligence angle underneath the release.
- Contributors again mostly outside the core team (danshapiro/Dan Shapiro), with AI coding agents (Codex, Amplifier) committing alongside him.

## SECOND-TIER

### prime-radiant-inc/llm-proxy
Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
**second-tier**, three merged PRs.
- AWS SigV4 signing mode added for the Anthropic passthrough (lets the proxy front Bedrock), with hop-by-hop headers stripped before signing and a clean mode-based rollback; Apache-2.0 license added.
No divergence vs old draft.

### prime-radiant-inc/stockyard
Coding-agent VM orchestrator: runs coding agents in isolated VMs — Firecracker micro-VMs on Linux (with ZFS-based audit-trail snapshots) and Apple's container tool on macOS.
**second-tier**, no PRs (direct push).
- Safe task-destruction work: requiring names to destroy named tasks, failing closed on identity errors, safely quoting destroy-confirmation names, hardened orphan-audit reconciliation and durable IP allocation.
No divergence vs old draft.

### prime-radiant-inc/serf
A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
**second-tier**, four merged PRs, very heavy direct-push volume.
- ⚠ correction vs old drafts: the "prepopulate the session-path dropdown with recent projects" feature — which an earlier draft (week 4) told as that week's story — actually merged **this week** (PR #53). This week's real merged-PR set: fork any message into the composer for editing, fold archived sessions behind one disclosure grouped by project, the recent-projects dropdown, and per-turn job-notification parsing.
- Old draft's framing of the broader week as a session/UI architecture rebuild (delegate-transcript UI audit, pane-routing repairs, nested-session owner promotion, settings/session-routing placement contracts) is accurate and consistent with the sampled commit log — keep it, just anchor the four concrete merged features above as the "shipped" list.
- Also present: model-switch replay-parity work (asserting the same event kind in both live and replay paths) and serffuzz compile-gate fixes.

### prime-radiant-inc/terminal-bench-analysis
Fetches detailed JSON results from the Terminal Bench 2 leaderboard, loads them into SQLite, and publishes queryable analysis via Datasette.
**second-tier**, bot-only.
- Automated README regeneration, no new data.
No divergence vs old draft.

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
**second-tier**, no merged PRs (direct push).
- Hermes-4 coding-agent bring-up: a RED bootstrap verdict and mechanism autopsy, a clone-faithful plugin-staging fix, hardened plugin staging (reject symlinks, expand `~`), a HermesAgent provisioning adapter, and the honest negative finding that Hermes-4 via OpenRouter is structurally impossible to eval (no tool-use endpoints exposed).
- ⚠ correction vs old drafts: the "shoplist fixture" evidence-scenario work — a matched pair of e2e scenarios grading whether an agent tells the truth about what it built ("working feature, verified proof" vs. "broken feature, honest report") — which an earlier draft (week 2) told as that week's story, actually landed **this week**. Old draft for this week covered only the Hermes thread and omitted this; both are real and both belong here.

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, bot-only.
No divergence vs old draft.

### prime-radiant-inc/teststrip
macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
**second-tier**, quiet week.
- Two small merges: compiling Core ML face models once (perf), and a round of dogfood culling/library fixes.
No divergence vs old draft.

### prime-radiant-inc/smevals
A framework for running evals against small (and large) models.
**second-tier**, outside contributor (Simon Willison).
- Per-task detail-view page, a `run -n X` flag to repeat runs and distinguish errors from failures, GitHub Actions CI workflows, a path-traversal bug fix in the serve command.
No divergence vs old draft.

### obra/blogosphere
Local-first, multi-platform blogging client for an 11ty blog that lives in a GitHub repo — the repo is the database.
**second-tier**, durability-focused week.
- Fixed a "database is locked" publish failure via single-statement rename pairs; hardened against hard kills (Windows PAT persistence, bounded typing-buffer loss).
No divergence vs old draft.

### obra/dotfiles
Jesse's personal dotfiles.
**second-tier**, minimal.
No divergence vs old draft.

### obra/lace
Lightweight agentic coding environment.
**second-tier**, three merged PRs.
- Bedrock provider rewritten on `AnthropicBedrockMantle` for full Anthropic parity, SDK connection errors now treated as retryable, integration-suite test-hygiene fix. Thematically paired with `llm-proxy`'s SigV4 work this same week — both pushing Anthropic-via-AWS support.
No divergence vs old draft.

### obra/superpowers-marketplace
Curated Claude Code plugin marketplace.
**second-tier**, minimal.
- Version bump tracking superpowers `v6.2.0`.
No divergence vs old draft.
