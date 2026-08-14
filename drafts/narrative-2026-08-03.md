# Narrative brief — week of 2026-08-03 (through 2026-08-09)

Grounded in `data/recon-v2-8wk-20260814-CORRECTED.json` (week index 7) + `src/data/weekly-stats.json["2026-08-03"]`. Old draft: `src/content/posts/week-7.md`. No numbers below.

**Context for the whole week:** on August 6, an org-wide sweep added a service-catalog entry (`catalog-info.yaml` + `ABOUT.md`) to nearly every repo at once — a single "docs(map)" commit each. Old draft already calls this out correctly and excludes it from per-repo product narratives; this brief does the same. Repos whose only activity this week is that catalog commit are noted as such below and otherwise have nothing to report.

## FEATURED

### prime-radiant-inc/obol
Read an AI-agent transcript and estimate what it cost — a Rust core with C-ABI bindings for Python, Go, and TypeScript (Bun + Node).
**FEATURED — tagged release `v0.9.0`.**
- Pricing refresh adding `claude-opus-5`, plus a CI repair (stale dialects, a clippy lint).
No divergence vs old draft.

### prime-radiant-inc/agentic-usage-meter
macOS menu-bar meter for coding-agent subscription quotas.
**FEATURED — six tagged releases this week (`v0.1.1` through `v0.2.4`).**
- ⚠ divergence vs old draft: old draft names only the `v0.2.4` push and describes it narrowly (multi-org accounts, a provider-request link, Node 24 release artifacts). The corrected log shows a much bigger concurrency-hardening arc across all six releases: serializing every persisted-state write through one mutation queue, reference-counting reconnect-refresh blocking, draining in-flight refreshes before reconnects touch shared state, and closing out account-removal/cancellation races. This was a week of fixing account-management race conditions under rapid iteration, not just a single feature add.
No new divergence beyond that.

### prime-radiant-inc/awesome-superpowers
An agentic skills framework and software-development methodology that works (community index repo).
**FEATURED — new repo created this week.**
- Initial commit + README from an outside contributor (Kattni), picked up by the catalog sweep.
No divergence vs old draft.

### obra/superpowers-chrome
Claude Code plugin for direct Chrome browser control via DevTools Protocol - zero dependencies.
**FEATURED — tagged releases `v3.0.3`, `v3.0.4`, `v3.0.5`.**
- `v3.0.3`: honor stringified JSON payloads for structured actions (Postel's law) — contributed by an outside/ada-sen branch, with added behavioral test coverage.
- `v3.0.4`: pure dependency-security release, resolving all open Dependabot alerts.
- `v3.0.5`: reliability/hardening across MCP and CLI launch paths — pass image-tool/port-lookup args directly instead of via a shell, report *why* Chrome failed to launch, keep Chrome's sandbox on except where it truly can't work, surface spawn failures instead of crashing the server, isolate test profile/cache paths from the user's real cache dir.
- Old draft's details are accurate but omits that `v3.0.4` was a dedicated security-patch release and that an outside contributor authored the `v3.0.3` fix — worth adding.

## SECOND-TIER

### prime-radiant-inc/serf
A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
**second-tier**, no merged PRs (direct push), a third consecutive four-figure-commit week.
- Task-list panel redesign in the web UI: grouped rows by status, latest updates shown inline, progress header, timezone-safe timestamps.
- Recoverable/retained tool output for the agent: bounded retained-output readers, paging and search over retained output, artifacts scoped to session trees, hardened artifact-lifecycle cleanup.
No divergence vs old draft.

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project.
**second-tier**, one merged PR.
- A statistical self-correction: Fisher tests, a matched-cell token median, and an explicit retraction of an earlier overclaim, alongside token/wall-time deltas showing an opus-5 arm carrying real overhead.
- Also (not in old draft): shipped a way to import locally-run eval results onto the shared eval appliance — a scrubbed-bundle export/import path (merged PR) — plus a fix excluding vendored dependencies from campaign exports (the source of this week's LOC bulge).
No divergence vs old draft (enrichment only).

### prime-radiant-inc/superpowers-autoresearch
Automated-research harness for running experiment campaigns against the superpowers methodology (no description set on GitHub).
**second-tier**, heavy direct-push volume.
- A "compounding-trap" experiment battery with signature-first designs and binary ground truth; an anti-appeasement probe that returned an honest "INCONCLUSIVE-BY-BASE-RATE" verdict rather than forcing a result.
No divergence vs old draft.

### prime-radiant-inc/teststrip
macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
**second-tier.**
- A "unified shell" design spec and a multi-task implementation plan to consolidate the app's various views into one shell — planned out before the build.
- Also (not in old draft): an autopilot "ghost" derivation refactor — dropped a persisted `autopilot_proposals` table in favor of deriving suggestion badges/review-queue state directly from asset metadata (a run persists nothing; undo just replays the in-memory group).
No divergence vs old draft (enrichment only).

### obra/lace
Lightweight agentic coding environment.
**second-tier**, three merged PRs.
- Container-lifecycle work: kill the in-container process tree on abort, adopt existing containers on resume, allow empty-workspace resume, pin persona across delegate resume.
- Model-catalog: added `claude-opus-5`; fixed a cached Anthropic catalog shadowing new static metadata.
No divergence vs old draft (old draft covered the container-lifecycle half; catalog work is additive detail).

### obra/superpowers
An agentic skills framework and software-development methodology that works.
**second-tier**, zero direct commits, twenty merged PRs (squash-merged).
- ⚠ correction vs old draft: old draft noted only that a batch of PRs merged, without naming any content. The real throughline: **Hermes Agent harness support** (eval-verified bootstrap) and a run of SDD reliability fixes — event-driven bounded waits that drove wait-timeouts down to effectively none, batching small same-shape tasks into one dispatch, "rule and continue" so non-catastrophic conflicts get ledgered rulings instead of blocking questions, and a guard so dispatched subagents never dispatch further subagents.
- Also: added Devin CLI support, corrected multi-agent guidance against the Codex source, and several README/docs navigation improvements.

### obra/winpepper
Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
**second-tier**, heavy volume, outside contributor (Dan Shapiro).
- ⚠ divergence vs old draft: old draft covered only the tail-end cleanup (deleting dead provisioning services, an engine-load failure message fix, evidence-backed verification). The bigger story earlier in the week is an **ASR engine switch**: moving to a "nemotron-first" pipeline (multilingual Nemotron 3.5 as the primary streaming model, Parakeet demoted to an optional backup), a new worker-process architecture with kill/respawn supervision, and an onboarding model-picker with background downloads.
- The cleanup work old draft described did happen too, at week's end, once the new pipeline had landed.

### prime-radiant-inc/clipfan, prime-radiant-inc/superpowers-docs, prime-radiant-inc/homebrew-tap, prime-radiant-inc/llm-proxy, prime-radiant-inc/stockyard, prime-radiant-inc/sprout, prime-radiant-inc/slackline, prime-radiant-inc/openai-codex-plugins, prime-radiant-inc/greenfield, prime-radiant-inc/books-for-bots, prime-radiant-inc/toil, prime-radiant-inc/agent-plugin-linear-use, prime-radiant-inc/smevals, prime-radiant-inc/terminal-bench-analysis, prime-radiant-inc/code-of-conduct, obra/dotfiles, obra/superpowers-marketplace
All **second-tier**, minimal-to-catalog-only activity this week:
- Most of these repos' only commit this week is the August 6 catalog-sweep commit (`docs(map): bootstrap/refresh catalog-info.yaml + ABOUT.md`) — no product content to report.
- Exceptions with a little real content: `gauntlet`-adjacent fix in tui grace-period (actually filed under gauntlet: grace descendants after kill-server before SIGKILL); `code-of-conduct` merged the prior week's Contributor Covenant adaptation PR and refined the README; `terminal-bench-analysis` and `claude-plugin-stats` had their usual bot-only chart/README rebuilds; `dotfiles` iterated on Jesse's `CLAUDE.md` instructions; `superpowers-marketplace` tracked the `superpowers-chrome` releases (`v3.0.3`→`v3.0.5`).
No divergence vs old draft — old draft handles this long tail correctly and already flags the catalog sweep explicitly.
