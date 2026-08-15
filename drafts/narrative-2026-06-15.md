# Narrative brief — week of 2026-06-15 (through 2026-06-21)

Grounded in `data/recon-v2-4wk-20260525-backfill.json` (week index 3) +
`src/data/weekly-stats.json["2026-06-15"]`. Backfill batch 1 (historical,
pre-launch week — the week immediately before the earliest live post,
2026-06-22). No numbers below — pure narrative themes.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member (or
`mhat`, staff for this whole window per the owner). Everyone else is labeled
**outside** explicitly per repo, below.

## FEATURED

### obra/private-journal-mcp
MCP server for a private Claude journaling capability.
**FEATURED — tagged releases `v2.0.1` and `v2.0.0`.** ⚠ Note: zero commits
and zero authors are attributed to this repo in this week's window — both
releases were tagged/published this week but the underlying commits landed
in an earlier week. Nothing to narrate beyond "two releases went out";
don't invent a feature story for this one.

### obra/superpowers
Agentic skills framework and methodology.
**FEATURED — tagged releases `v6.0.3`, `v6.0.2`, `v6.0.0`
(+ commit-only bump `v6.0.1`).**
- A full Superpowers 6 release train in one week: `v6.0.0` (evals
  submodule unified across per-agent bootstrap scenarios, visual-companion
  Prime Radiant branding), `v6.0.1` (Codex plugin-version-display fix),
  `v6.0.2` (stopped shipping the evals submodule — it was breaking plugin
  installs), `v6.0.3` (moved SDD artifacts out of the git-protected
  `.git/` path into the working tree, with per-worktree isolation tests).
- A "Job posting" commit landed mid-week (recruiting, not code).
- Contributors: Jesse Vincent (staff) and Drew Ritter (staff).

### obra/claude-session-driver
Launch, control, and monitor Claude Code sessions as workers via tmux.
**FEATURED — tagged release `v4.0.0`.**
- Merged the TypeScript core rewrite (parity + Codex + Pi drivers) begun
  the prior week — this is the release that ships it.
- Follow-on fixes: Codex `apply_patch` rendering in `read-turn`, Pi
  tool-name casing normalized to the Bash/Read convention, an
  unregistered-derive-workers listing, a `--last N` cap on `read-events
  --follow` backlog, a mixed-fleet `HARNESS` column in `list`.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/obol
Reads an AI-agent transcript and estimates what it cost.
**FEATURED — tagged releases `v0.6.0` and `v0.5.0`.**
- Added an ATIF trajectory dialect, then (breaking) removed the
  per-agent raw-log dialects entirely — ATIF + obol's own dialect become
  the only two supported formats.
- A cost-accuracy fix: an empty model now signals "unknown" rather than
  "unpriced," and an explicit `final_metrics.total_cost_usd` overrides the
  rate-table lookup when present.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/slackline
Slack-identity CLI for AI agents.
**FEATURED — tagged releases `v0.5.0` and `v0.4.0`.**
- User-facing polish: `@handle` mention linkification (in both `read` and
  `ask`), user-ID resolution, a new `users` command, an `auth whoami`
  command, message permalinks.
- Defaulted `read`/`listen` output to compact text; fixed a dropped
  `message_replied` parent-event bug and a Socket Mode listener-failure
  visibility gap.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/clipfan
Clipboard sync daemon for Mac + remote tmux fleet.
**FEATURED — tagged release `v1.0.9`.**
- Small, focused week after the `v1.0.0` push: fixed an idle-CPU
  regression and guarded tmux fanout against stale buffer hooks.
- Sole contributor: Jesse Vincent (staff).

## SECOND-TIER

### obra/lace
Lightweight agentic coding environment.
**second-tier**, one merged PR, no release.
- "Session-state architecture": an O(tail) incremental turn-projection
  cache (avoids full-log rescans), a cross-process monotonic sequence
  authority (flock + head file, self-healing pid-reuse detection on stale
  locks), and a non-lossy verbatim `event_journal` recall store.
- Prompt-cache byte-stability guardrails: golden-fixture determinism tests
  pinning exact request bytes for Anthropic, OpenAI, and Gemini, closing a
  parallel-tool-call cache-invalidation bug.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/serf
Non-interactive coding agent.
**second-tier**, no PRs/release — still the week's largest raw commit
volume even without one.
- A new `serf-doctor` diagnostic subsystem: tree/watches/transcript/
  forensics views over a session's delegate and observer state, plus a
  dedicated `doctoring-serf` skill.
- A tool-fluency experimentation framework (live harness, prompt
  iteration, fixed-prompt reruns) and passive-observer sidecars that idle
  without generating tool-call churn.
- Packaging: install now defaults to a home-prefix layout, bundling the
  doctoring skill.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum).
**second-tier**, no tagged release.
- Designed and began building a "shared eval appliance": a containerized,
  detached-worker job model with its own CLI, cancellation handling,
  git-ref preflight, and a trust-hardening pass (wrapper-environment
  trust, path validation, sanitation-bypass closure) — the eval harness's
  own container story, distinct from `stockyard`.
- Quorum dashboard decoupling: a standalone `dashboard` CLI entrypoint, an
  OS-aware eligibility grid-manifest, 5-state cells
  (pass/failed/incomplete/not_run/ineligible).
- A full-fidelity Pi normalizer (content + reasoning + linked
  observations) and early Grok target scoping.
- Contributors: Jesse Vincent (staff) and Drew Ritter (staff).

### prime-radiant-inc/llm-proxy
Transparent logging proxy for LLM API traffic.
**second-tier**, no PRs/release.
- "Mantle" telemetry contract work: run-scoped mantle routing required
  for cloud builds, telemetry-observation logging with pass-through
  provenance preserved on upstream failures, safer cloud-build run-ID
  decoding.
- Sole contributor: Drew Ritter (staff).

### obra/dotfiles
Jesse's personal dotfiles.
**second-tier**, minimal.
- Small quality-of-life fixes: Homebrew on `PATH` for non-interactive zsh,
  a guard against an inert stray root `~/.zshrc`, `kimi-code` added to the
  managed `PATH`.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers-marketplace
Curated Claude Code plugin marketplace.
**second-tier**, minimal.
- Version-pin bumps only, tracking `superpowers` v6.0.0/6.0.2/6.0.3 and
  `claude-session-driver` v4.0.0.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, bot-only activity.
- Routine daily scrape + chart rebuild, entirely `github-actions[bot]`. No
  human-authored change this week.

### prime-radiant-inc/obol-go
Generated Go binding for obol.
**second-tier**, minimal — a single machine-generated release commit
(`obol-release`, the automated release identity — not a human, do not tag
as outside).

### obra/temp-sp-codex
"Temporary Superpowers Codex marketplace test repo."
**second-tier** — ⚠ same mirror-repo anomaly as every prior week in this
batch: duplicates `obra/superpowers`'s commits exactly, including its
release-train commits. Not distinct work.

---

## Anomalies / notes for this week
- **`obra/private-journal-mcp`**: featured on tags alone, with literally no
  commits/authors in-window — a real "release cut later than the code"
  case. Say so plainly if it's covered in the published post; don't
  backfill a feature narrative that isn't in this week's data.
- **`obra/temp-sp-codex`** mirror-repo pattern holds for the fourth
  straight week — recommend Ada decide once (exclude vs. footnote) rather
  than re-deciding per post.
- This is the last of the four backfill weeks; 2026-06-22 (the earliest
  live week) picks up immediately after.
