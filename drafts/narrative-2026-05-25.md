# Narrative brief — week of 2026-05-25 (through 2026-05-31)

Grounded in `data/recon-v2-4wk-20260525-backfill.json` (week index 0) +
`src/data/weekly-stats.json["2026-05-25"]`. Backfill batch 1 (historical,
pre-launch week). No numbers below — pure narrative themes.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member (or
`mhat`, a former employee who was on staff for this whole window per the
owner). Everyone else is labeled **outside** explicitly per repo, below.

## FEATURED

### prime-radiant-inc/clipfan
Clipboard sync daemon for Mac + remote tmux fleet — mirrors macOS pasteboard
to remote OS clipboards and tmux paste buffers, enabling image paste into
Claude Code/Codex over SSH without OSC 52 or Xvfb.
**FEATURED — new repo created this week + tagged release `v0.3.0`.**
- Launched and shipped its first tagged release in the same week: daemon +
  menubar app with clip-ID-based recirculation prevention (mint at origin,
  suppress echoes of your own writes, dedup by clip-ID).
- Menubar UI overhaul (Group A): Settings window with Fleet/General/
  Diagnostics tabs, per-Mac fleet rows, daemon version reporting.
- Configurable settings (Group B): history-limit stepper, global shortcut
  recorder (dropped the old Carbon hotkey for `KeyboardShortcuts`),
  authenticated config endpoint.
- CI sign/notarize + Sparkle auto-update shipped in the same week (Group C):
  Developer ID signing, notarization, auto-update feed.
- Security hardening pass on sync/install paths ahead of the public release.
- Sole contributor: Jesse Vincent (staff).

### obra/winpepper
Windows-native local dictation — hold a hotkey, speak, release; Parakeet
TDT v3 ASR + LlamaSharp cleanup, all local.
**FEATURED — tagged release `v0.6.1-alpha`.**
- Its first full week after creation (created 2026-05-17): a "Lab" test
  harness (media transport controls, custom prompt cleanup, minimal
  play/mute/seek control), About-screen activation fix, local-time diagnostic
  timestamps, CI hardening (fixed three pre-existing failures, skip CI for
  doc-only PRs), a debounce-coalesce test flake fix.
- Contributors: mostly **outside** — Nat Torkington (`njt`) opened and
  authored the bulk of this week's merged PRs; Jesse Vincent (staff) reviewed
  and merged them.

## SECOND-TIER

### prime-radiant-inc/serf
A non-interactive coding agent: give it a prompt and it reads, writes, runs
commands, and searches code in a loop using native tool-calling across
OpenAI, Anthropic, and Google models.
**second-tier** — no releases/PRs this week, but the single busiest commit
volume of the week.
- A large internal-refactor push ("Phase 6"): cluster-internalization of
  the subagent, hook-runner, tool-registry/MCP, context-strategy, and
  prompt-composition machinery; removal of the dormant `serfeval` harness.
- Error-hygiene pass (sentinels over substring matching, `errors.As`),
  provider god-file splits, a permanent `-race` CI gate, and streaming-code
  decomposition across providers.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/stockyard
Coding-agent VM orchestrator — Firecracker micro-VMs on Linux (ZFS
audit-trail snapshots) and Apple's container tool on macOS.
**second-tier**, no release.
- Removed the vfkit VM backend entirely, de-Firecracker-izing the macOS
  path in favor of Apple's native container tool.
- Swapped to a pure-Go SQLite driver so the `CGO_ENABLED=0` daemon release
  build works; added a macOS CI job (build/vet/test).
- Contributors: Matt Windbrook (staff) led; Jesse Vincent (staff) merged.

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project.
**second-tier**, no tagged release.
- Renamed the harness twice in-week (`harness`→`barf`→`quorum`) and retired
  the legacy `drill` runner.
- Shipped per-agent run economics (real per-model published pricing,
  per-run/batch cost totals, an Economics pane in the report viewer).
- Added a `run-all` batch orchestrator with live progress and a
  scenario×agent matrix view; `watch_logs`/`wake_on_idle_log` tooling to
  replace sleep-polling.
- Contributors: Matt Windbrook (staff) dominant; Drew Ritter (staff, one
  commit).

### obra/lace
Lightweight agentic coding environment.
**second-tier**, five merged PRs, no release.
- Multi-tenant container-network isolation work (PRI-1919): `netns-init`
  sidecar for subagent↔subagent isolation, gateway-routed persona DNS,
  cross-boundary network-state forwarding.
- Structured-output support landed natively in the Anthropic provider
  (PRI-1902); tool allowlists tightened to be verbatim, not additive
  (PRI-1900).
- A large compaction rewrite: dropped the legacy `summarize`/
  `trim-tool-results` strategies for track-based compaction throughout
  (Slack-salience formatting, per-track LLM fallback, markdown rendering).
- Wire-protocol rename (`truncate`→`trim-tool-results`) and real
  cache-token/cost persistence (PRI-1817).
- Sole contributor: Jesse Vincent (staff).

### obra/claude-session-driver
Launch, control, and monitor other Claude Code sessions as workers via
tmux.
**second-tier**, tagged as a commit-message-only bump (`v3.0.1`), no
GitHub Release object.
- `adopt` command added to recover workers after a host reboot; converse
  diagnostics dump on timeout; event-driven (not poll-driven) prompt
  submission confirmation with retry.
- Contributors: Jesse Vincent (staff); one fix (`#20`) from **outside**
  contributor Patrick MacMurchy.

### prime-radiant-inc/clearance
Clearance product workspace — a monorepo for the Markdown viewer, currently
a native Swift/macOS app.
**second-tier**, one merged PR, no release.
- Single fix this week: a single-dollar math-delimiter bug, from
  **outside** contributor Aaron Weiss (PR #50).

### prime-radiant-inc/gauntlet
AI-powered QA testing framework that drives LLMs through markdown story
cards.
**second-tier**, no PRs/release.
- `watch_logs`/`wake_on_idle_log` shared tooling plus a per-tool
  max-execution-time guard and an empty-`end_turn` safety net (PRI-1864).
- A TUI `type_and_submit` atomic tool, now the default text-entry path for
  adapters (PRI-1849/1852).
- Sole contributor: Matt Windbrook (staff).

### prime-radiant-inc/llm-proxy
Transparent logging proxy for LLM API traffic.
**second-tier**, no PRs/release.
- API token substitution feature: a resolver-command + TTL/size-cached
  substituter that swaps the resolved key in after header-copy, fail-closed
  on every endpoint; new `listen_host` config binding (defaults to
  localhost) closing a security gap.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers
An agentic skills framework and software-development methodology.
**second-tier**, one merged PR, no release.
- New contribution policy: contributors must now disclose their authoring
  environment (human vs. which agent), and target the `dev` branch.
- A "Porting Superpowers to a New Harness" guide added; a Codex
  plugin-sync fix (stop leaking the `.pi/` extension into the Codex
  package).
- Contributors: Jesse Vincent (staff); one commit from **outside**
  contributor `nawfal`.

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, minimal — one commit.
- A single data-recovery commit ("recovered from Arq backup"), restoring a
  day's lost scrape rather than shipping anything new.
- Sole contributor: Jesse Vincent (staff).

### obra/dotfiles
Jesse's personal dotfiles (no description set on GitHub).
**second-tier**, minimal.
- tmux integration for clipfan's new copy-mode bindings.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers-chrome
Claude Code plugin for direct Chrome browser control via DevTools Protocol.
**second-tier**, minimal — one commit.
- Small fix: stop treating an unavailable IPv6 loopback as a port conflict.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers-marketplace
Curated Claude Code plugin marketplace.
**second-tier**, minimal — one commit.
- Version-pin bump only (points at `claude-session-driver` v3.0.1).
- Sole contributor: Jesse Vincent (staff).

### obra/temp-sp-codex
"Temporary Superpowers Codex marketplace test repo."
**second-tier** — ⚠ **data anomaly, not real distinct work**: this repo's
own `created_at` is 2026-06-22 (a full four weeks after this bucket), yet
its commit history — identical subjects, identical authors, identical
counts — exactly mirrors `obra/superpowers`'s activity in this same week.
It's a copy/mirror repo whose git history carries the original (older)
commit dates. Treat it as noise; the real work is already covered under
`obra/superpowers` above. Recommend excluding it from the published post
entirely, or footnoting it as a test artifact.

### prime-radiant-inc/terminal-bench-analysis
Fetches Terminal Bench 2 leaderboard results into SQLite, publishes via
Datasette.
**second-tier**, bot-only activity — ⚠ **this is the source of the week's
outsized LOC-added figure** (millions of added lines) in the raw stats: a
single `github-actions[bot]` "Regenerate README (no new data)" commit that
rewrites a large generated/data file. Not human-authored work; exclude
from any "biggest week" framing.

---

## Anomalies / notes for this week
- **clipfan's LOC delta is real work** (131 commits, genuinely the biggest
  human-authored week) — don't confuse it with terminal-bench-analysis's
  bot-driven LOC spike above.
- **obra/temp-sp-codex** is a mirror/test artifact every week it appears in
  this backfill batch (see above) — same caveat applies in later weeks too.
- No unclassifiable contributors this week (Patrick MacMurchy, Aaron Weiss,
  Nat Torkington, and `nawfal` all resolved to GitHub logins outside the
  current org member list — see report for exact logins).
