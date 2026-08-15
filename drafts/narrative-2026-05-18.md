# Narrative brief — week of 2026-05-18 (through 2026-05-24)

Grounded in `data/recon-v2-4wk-20260427-batch2.json` (week index 3) +
`src/data/weekly-stats.json["2026-05-18"]`. Backfill batch 2 (historical,
pre-launch week — the week immediately before batch 1's earliest week,
2026-05-25). No numbers below — pure narrative themes.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member (or
`mhat`, staff for this whole window per the owner). Everyone else is labeled
**outside** explicitly per repo, below.

## FEATURED

### obra/episodic-memory
Memory/recall layer for coding-agent sessions.
**FEATURED — tagged release `v1.4.2`.**
- Cross-platform install fixes: a postinstall script fixed for
  non-macOS/Linux, a single-instance lock for `sync --background`, and
  per-required-package manifest probing before launching the MCP server.
- A retryable-error sentinel written on summarizer failure, closing a
  silent-failure gap.
- Contributors: Jesse Vincent (staff) drove the release; two **outside**
  contributors landed fixes in the same week — Andy Wright (GitHub login
  `minyek` — the same account credited as `minyek` in the prior week's
  brief, just a different display name on this commit) fixed a
  summarizer-cwd/resume-fallback bug, and `K. Z.` (`monsterxz9`) fixed the
  Codex summarizer ignoring a deprecated model from history.

### prime-radiant-inc/slackline
Slack-identity CLI for AI agents.
**FEATURED — tagged releases `v0.2.2` and `v0.2.1`.**
- A default-recipient fix (thread replies to bot-authored messages now
  emit by default) alongside a lint-warning cleanup pass that named several
  previously-magic wire-format error codes and Slack scopes as exported
  constants.
- Sole contributor: Jesse Vincent (staff).

## SECOND-TIER

### obra/lace
Lightweight agentic coding environment.
**second-tier**, no PRs/release — the week's largest raw commit count by
far.
- Security/reliability hardening on the `recall` subsystem: file modes
  (`0o600`/`0o700`) applied to the SQLite index and transcript files,
  SQLite `busy_timeout` set so contending writers wait instead of erroring,
  FTS5 query-error wrapping, persona-name validation (reject leading dash/
  whitespace/control chars), a `search order: recent` option.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/serf
Non-interactive coding agent.
**second-tier**, no PRs/release — very large commit volume.
- A TUI visual-redesign wave: theme tokens replacing legacy `colorTheme`/
  `tuiStyles`, terminal-native fg/bg painting via OSC 10/11 to match the
  active theme, WCAG-contrast rebalancing, a large "roborev" fix-response
  sweep (multiple numbered review rounds addressed in sequence).
- Contributors: Jesse Vincent (staff). As in the prior week, a large share
  of commits carry the unlinked `jesse` git identity (email pattern
  `jesse@<hostname>`, no linked GitHub account) rather than the `obra`
  account — very likely the same person on a second machine, flagged
  rather than assumed (see prior week's brief for the same note).

### prime-radiant-inc/gauntlet
AI-powered QA testing framework.
**second-tier**, no release.
- A static single-file HTML build target: `gauntlet render <run-id>`
  renders a run to a portable page (no server needed), reusing the same
  React components as the live UI via a static-payload mode.
- Contributors: Matt Windbrook (staff) led; Jesse Vincent (staff)
  co-committed.

### prime-radiant-inc/sprout
Experimental self-improving multi-agent coding system.
**second-tier**, no PRs/release — heavy commit volume.
- An OpenAI/Codex OAuth provider end-to-end: credential lifecycle
  management, refresh-race hardening, macOS-keychain-direct secret writes
  (kept out of argv), a Codex adapter with stream-tool-call handling.
- Active-subagent status surfaced in both terminal and web UIs, scoped
  correctly per session (fixing several status-leak-across-sessions bugs).
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/stockyard
Coding-agent VM orchestrator.
**second-tier**, one merged PR, no release.
- Added Apple's `container` tool as a third macOS VM backend (alongside
  Firecracker and the outgoing vfkit path): a full `AppleContainerBackend`
  (start/stop/delete/list, log-follower, PTY-backed exec session), plus
  fixes for real-world container-CLI JSON quirks and multi-arch image
  builds caught by an actual arm64 build.
- Sole contributor: Matt Windbrook (staff).

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum).
**second-tier**, one merged PR, no release.
- README/harness documentation expansion, Codex-auth-per-run seeding (no
  more checked-in fixture), and a wave of scenario ports into the
  `setup-helpers`/preflight.sh shape.
- Sole contributor: Matt Windbrook (staff).

### prime-radiant-inc/llm-proxy
Transparent logging proxy for LLM API traffic.
**second-tier**, one merged PR, no release.
- Fixed gzipped responses being written to JSONL logs uncompressed.
- Sole contributor: Jesse Vincent (staff).

### obra/claude-session-driver
Launch, control, and monitor Claude Code sessions as workers via tmux.
**second-tier**, tagged as a commit-message-only bump (`v3.0.0`), no
GitHub Release object.
- A CLI redesign: legacy scripts and tests dropped in favor of a unified
  CLI, an end-to-end integration test through the shim, a round-trip
  test-drive polish pass.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers-chrome
Chrome-control plugin via DevTools Protocol.
**second-tier**, no PRs — two commit-message-only bumps (`v2.2.0`,
`v3.0.1`, the latter a lint-fix-only hotfix release).
- A flatten-mode bridge migration: every module (mouse, keyboard, capture,
  console-logging, navigation, file-upload, select-option, screenshot)
  moved onto a shared `pageSession` model, retiring the old per-page CDP
  connection pool.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers-marketplace
Curated Claude Code plugin marketplace.
**second-tier**, minimal — version-pin bumps only (superpowers-chrome
`v3.0.0`/`v3.0.1`, episodic-memory `v1.4.2`, claude-session-driver
`v3.0.0`).

### obra/ghost-pepper
Hold-to-talk speech-to-text for macOS (fork).
**second-tier**, minimal — one commit, from **outside** contributor Matt
Hartman (`matthartman`): a `v2.4.0` release cut.

### obra/superpowers
Agentic skills framework and methodology.
**second-tier** — two merged PRs, but **zero commits with an in-window
author date** (same pattern flagged the past three weeks running).
- One PR fixes a false-trigger in the "ultrathink" keyword scanner for the
  systematic-debugging skill; the other responds to an `mhat` (staff)
  bug report about Claude getting confused by "debugging" being treated
  as a noun vs. verb.
- Contributor (by PR): **outside** contributor `ngalatis` authored the
  keyword-scanner fix; Jesse Vincent (staff) authored/merged the other.

---

## Anomalies / notes for this week
- **`obra/superpowers`** continues the "merged PRs, zero in-window commit
  authors" pattern for a fourth consecutive week — see the prior three
  briefs for the same caveat.
- **The unlinked `jesse` git identity** (flagged in last week's brief)
  recurs again this week in `serf`. Same read: very likely Jesse Vincent
  under an unconfigured git email on a second machine, not confirmable via
  the GitHub API, not merged into the `obra` tally without confirmation.
- **`minyek`/"Andy Wright" are the same GitHub account**, credited under
  two different commit display names across this week and last —
  resolved via `gh api` commit lookup, not a guess.
- No bot-driven LOC spikes or org-wide sweeps this week.
- This is the last of batch 2's four weeks; batch 1's earliest week
  (2026-05-25, already live) picks up immediately after.
