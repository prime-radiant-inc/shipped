# Narrative brief — week of 2026-07-13 (through 2026-07-19)

Grounded in `data/recon-v2-8wk-20260814-CORRECTED.json` (week index 4) + `src/data/weekly-stats.json["2026-07-13"]`. Old draft: `src/content/posts/week-4.md`. No numbers below.

## FEATURED

### prime-radiant-inc/obol
Read an AI-agent transcript and estimate what it cost — a Rust core with C-ABI bindings for Python, Go, and TypeScript (Bun + Node).
**FEATURED — tagged release `v0.8.0`.**
- Pricing-data refresh: bundled snapshot updated to add the `gpt-5.6` model family, plus CI/lint repairs (cargo fmt drift, version-test expectation now derived from the workspace manifest).
No divergence vs old draft.

### prime-radiant-inc/teststrip
macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
**FEATURED — tagged release `v0.2.0`.**
- Culling-workflow redesign shipped: a dedicated culling workstation shell, simplified verdict copy ("Keep"/"Toss" instead of percentages), reads-card signal ordering, burst-rail thumbnail/caption polish.
- Persisted burst-stack capture-interval preference; run tracker with full completion summary counts.
- Fix so Library-grid activation opens the Library loupe rather than the culling loupe; RAW+JPEG badge repositioned/muted.
No divergence vs old draft — matches (old draft picked an accurate slice of this list).

### prime-radiant-inc/smevals
A framework for running evals against small (and large) models.
**FEATURED — new repo created this week + tagged releases `0.1.0` and `0.2.0`.**
- ⚠ minor divergence vs old draft: old draft framed this as "an outside maintainer taking a project from rough to releasable" (implying pre-existing code). The corrected data shows the repo was **created this week** — this is Simon Willison building the tool from scratch in-week (initial run/grade commands, Checklist→Grader rename, HTML report serve/build commands, multi-grader support, tagging) and shipping two releases off that same-week build, not polishing an existing rough project.
- Feature scope beyond old draft's "polish pass" framing: HTML report app with multiple graders and clickable tags, a terminal Markdown report command, example evals (haiku, Pelican, markdown-tables), and a README-generating docs command — a full CLI+reporting tool, not just cleanup.
- Old draft's specific details (README rewrite, `SMEVAL_*`→`SMEVALS_*` env rename, Python 3.10+ support) are accurate and still worth keeping.

### obra/blogosphere
Local-first, multi-platform blogging client for an 11ty blog that lives in a GitHub repo — the repo is the database.
**FEATURED — new repo created this week.**
- ⚠ divergence vs old draft: old draft covered only the public-launch essentials (MIT license, README, boot-failure screen, platform-honest copy) and undersold the week dramatically. The corrected commit log shows a **full application built from scratch in a single week**: Tauri v2 + Vite + React + TS-strict + Biome scaffold, a from-zero sync engine (serialized pushes, stale-head guard, activity log, partial-validation push, discard-changes), a rewritten document-style editor surface, image fetch-on-miss resolution, Android/iOS mobile builds, and a late "delight pass" (publish-URL preview, ⌘K, deploy watch, resume, versions, live view).
- An adversarial review pass fixed a batch of confirmed findings before ship (rename collisions, push/pull races, quit-flush, SSRF hardening).
- The launch-polish items old draft called out (license, README, platform-honest connect copy, boot-failure screen) did happen too — they're real, just the very last layer on top of a much bigger build.

## SECOND-TIER

### prime-radiant-inc/llm-proxy
Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
**second-tier**, no PRs (direct push).
- Response-capture/attribution work: stamp path + termination reason on every response-record exit path (including abort/dial/body-read failures), stamp `metering_provider`/`upstream`/`capture_version` on request lines, host-based provider derivation.
- Bedrock/Mantle relay-leg hardening: paired request-creation/dial-failure handling, termination-EOF stamping, added test coverage for relay legs.
No divergence vs old draft (old draft's telling of an earlier week's llm-proxy story doesn't apply here — this week's llm-proxy content is new and consistent with itself).

### prime-radiant-inc/serf
A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
**second-tier**, eight merged PRs.
- ⚠ divergence vs old draft: old draft's headline claim — a "recent projects" list prepopulating the TUI/web spawn pickers — does not appear anywhere in this week's corrected commit log. The actual merged-PR-grounded work is queue/steering message UX: edit-or-cancel an unconsumed queued message, per-message promotion of a queued follow-up to active steering, rendering user-sent steering as user messages rather than system dividers, and sticky per-session unsent composer drafts.
- Mobile web: sidebar "⋯" menus open as a full-width modal sheet on mobile; phone sidebar behaves as a drawer instead of a squeezed rail.
- Agent-side: configurable delegate-turn limits with honest occupancy/drive-budget reporting; subagent inline activity rendered as the tool call's stated purpose (guided toward gerund-form phrasing).
- The snake_case REST-contract cleanup old draft mentioned is real and does appear (a CI naming-gate fix).

### prime-radiant-inc/gauntlet
AI-powered QA testing framework that uses LLMs (Claude or GPT) to test web apps, CLI tools, and TUI programs from markdown story cards, returning structured pass/fail verdicts with evidence.
**second-tier**, one commit (outside contributor).
- LICENSE file added by an outside contributor (Eden) — housekeeping ahead of sharing the repo more widely.
No divergence vs old draft.

### prime-radiant-inc/terminal-bench-analysis
Fetches detailed JSON results from the Terminal Bench 2 leaderboard, loads them into SQLite, and publishes queryable analysis via Datasette.
**second-tier**, bot-only.
- Automated README regeneration with no new underlying data — not human work this week.
No divergence vs old draft.

### prime-radiant-inc/greenfield
A Claude Code plugin that reverse-engineers clean behavioral specs, test vectors, and acceptance criteria from any codebase, producing a provenance trail so a fresh team can reimplement without inheriting the original's internal structure.
**second-tier**, one merged PR (outside contributor).
- Skills restructured into per-skill directories with a `SKILL.md` each — a layout/structure fix, from an outside branch.
No divergence vs old draft.

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
**second-tier**, three merged PRs.
- Heavy experiment-documentation week: a large "PR #1998" verification campaign (the SDD fix-loop redesign landing in `obra/superpowers` this same week — see below) — audits, hardening, codex-precheck routes, hostile-probe verdicts, contingency reruns, final verdicts with economics.
- Infra: CI-hermeticity/container-build fixes to keep CI green; a container agent-CLI refresh.
No divergence vs old draft — old draft's "record of what was measured and why" framing is accurate; worth noting explicitly that the PR being evaluated (#1998) is the same SDD fix-loop work landing in superpowers this week.

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, bot-only.
- Routine daily chart-data rebuild.
No divergence vs old draft.

### obra/superpowers
An agentic skills framework and software-development methodology that works.
**second-tier**, zero direct commits, nine merged PRs (squash-merged).
- ⚠ note: this is where two storylines that earlier drafts misplaced actually belong. The **SDD plan-scoped workspace ledger** (per-plan artifact dirs, self-identifying ledger, end-of-plan cleanup — old draft told this story under week 3) merged this week as PR #1943. A **skills editorial pass** (stripping social-proof/self-selling/recap detritus from a dozen skills, eval-gated; reframing TDD's testing-anti-patterns; rationalization-table modernization of the branch-finishing skill — old draft told a version of this under week 2's release) also merged this week.
- Centerpiece (correctly identified by old draft, just under the wrong week previously): an SDD fix-loop redesign — resume-based fix rounds, a five-round breaker to stop endless fix cycles, controller adjudication, lifecycle restructure.
- Also: reliability fixes — dispatch the `SessionStart` hook via Git Bash on Windows, make the Codex-packaging and SDD skill test suites pass reliably off-macOS.

### obra/winpepper
Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
**second-tier**, two merged PRs, both from an outside contributor.
- Keep the app responsive during model downloads; fixed modifier-only hotkey capture and key-swallowing.
No divergence vs old draft.
