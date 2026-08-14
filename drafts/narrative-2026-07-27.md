# Narrative brief — week of 2026-07-27 (through 2026-08-02)

Grounded in `data/recon-v2-8wk-20260814-CORRECTED.json` (week index 6) + `src/data/weekly-stats.json["2026-07-27"]`. Old draft: `src/content/posts/week-6.md`. No numbers below.

## FEATURED

### prime-radiant-inc/code-of-conduct
This is the Prime Radiant Community Code of Conduct.
**FEATURED — new repo created this week.**
- Adapted the Contributor Covenant (v3) into a Prime Radiant community code of conduct, refined after review feedback.
No divergence vs old draft.

### prime-radiant-inc/agentic-usage-meter
macOS menu-bar meter for coding-agent subscription quotas.
**FEATURED — new repo created this week.**
- Multi-provider quota tracking stood up in one week: OpenCode account qualification/profile lifecycle handling, SuperGrok credential refresh without reconnecting, sample-data marking in account settings.
- Public-release infrastructure: signed Sparkle auto-update releases with fail-closed automation, confirmation-based updates, privacy-safe product screenshots, public documentation.
No divergence vs old draft — matches.

## SECOND-TIER

### prime-radiant-inc/homebrew-tap
Homebrew tap for Prime Radiant tools, including formulae for llm-proxy and beeper-message-sync.
**second-tier**, minimal.
- Added a cask (`clearance`).
No divergence vs old draft.

### prime-radiant-inc/stockyard
Coding-agent VM orchestrator: runs coding agents in isolated VMs — Firecracker micro-VMs on Linux (with ZFS-based audit-trail snapshots) and Apple's container tool on macOS.
**second-tier**, no PRs.
- Continued fail-closed task-destruction hardening: scoping the destroy-confirmation claim to the destroy command, pinning destroy-output substrings consumed by automation.
No divergence vs old draft.

### prime-radiant-inc/serf
A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
**second-tier**, no merged PRs this week (direct push), a second consecutive four-figure-commit week.
- Dominant visible thread: the web UI's compact input footer — designed, constrained, documented, then implemented with simplified session-footer facts.
- Also: mobile viewport/shell-chrome pinning, job-notification descriptions surfaced in notifications, task mutation summaries showing task titles, shell-tool-call presentation refinement.
No divergence vs old draft.

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
**second-tier**, minimal commit count, large documentation payload.
- Closed out a "codex-efficiency" measurement campaign with a batch of experiment write-ups; bumped the pinned Codex CLI version.
No divergence vs old draft.

### prime-radiant-inc/superpowers-autoresearch
(No description set on GitHub — appears to be the automated-research harness for running experiment campaigns against the superpowers methodology, per old draft.)
**second-tier**, heavy direct-push volume.
- Closed out a "queue campaign" measuring agent cost-pathologies: pre-registered batteries and verdicts across multiple hypotheses (batching, planframed prompts, at-scale queuing), landing on a headline result that a batching arm cut cost substantially while improving completion.
- Related "cost-pathologies" research thread: parser-scope limits, an unencrypted "honoring channel" design amendment, scope-auditability notes.
No divergence vs old draft.

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, bot-only.
No divergence vs old draft.

### prime-radiant-inc/teststrip
macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
**second-tier**, heavy direct-push volume.
- Per-face report cards shipped end-to-end: sharpness/light/facing/prominence analyzer, a staleness-aware `FaceReportStore`, traffic-light chip presentation, burst-rail roll-up dots.
- A real dogfooding-found bug fixed: serialized CoreImage face detection to break a live-only deadlock blocking a culling test scenario.
- Also present (not in old draft): a separate "blaze-through" thread — sliding-window burst prefetch and a warm-set planner for the cull loupe.
No divergence vs old draft (enrichment only).

### prime-radiant-inc/smevals
A framework for running evals against small (and large) models.
**second-tier**, minimal (outside contributor).
- Added badges to the README.
No divergence vs old draft.

### obra/dotfiles
Jesse's personal dotfiles.
**second-tier.**
- A curated Brewfile for one-command new-Mac workstation bootstrap (including the `clearance` cask from Prime Radiant's own Homebrew tap), plus a Bitwarden clipboard-paste walkthrough and an Arq snapshot-cleanup utility.
No divergence vs old draft.

### obra/lace
Lightweight agentic coding environment.
**second-tier**, four merged PRs.
- Runtime-correctness fixes: stop mislabeling a notification as "a new message," never dispatch an assistant prefill while draining a mid-turn inject, keep persona MCP servers alive across session resume, forward container mounts so the mount-conflict scan sees the truth.
No divergence vs old draft.

### obra/superpowers
An agentic skills framework and software-development methodology that works.
**second-tier**, one merged PR.
- Removed the "We're Hiring" section from the README.
No divergence vs old draft.

### obra/winpepper
Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
**second-tier**, heavy volume, outside contributor (Dan Shapiro).
- Model-aware cleanup-settings honesty (graying out unsupported controls when a raw-IO cleanup model is active) and a CPU-pegged status-pill indicator.
- A multi-model ASR comparison/benchmark harness (per-model resource capture, convergence detection, aggregated comparison report) and mid-paste focus-change handling (halt/park pending click-to-paste).
- Old draft's specific claim of a "registry-driven streaming-model dropdown" / `SelectedModelsPolicy` sits in the unsampled middle of this very large week — plausible and partially corroborated ("resolve model selection by registry" appears), not contradicted, but not independently verified here.
