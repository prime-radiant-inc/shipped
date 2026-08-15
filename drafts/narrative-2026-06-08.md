# Narrative brief — week of 2026-06-08 (through 2026-06-14)

Grounded in `data/recon-v2-4wk-20260525-backfill.json` (week index 2) +
`src/data/weekly-stats.json["2026-06-08"]`. Backfill batch 1 (historical,
pre-launch week). No numbers below — pure narrative themes.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member (or
`mhat`, staff for this whole window per the owner). Everyone else is labeled
**outside** explicitly per repo, below.

**Cross-cutting note:** many repos independently picked up two identical CI
maintenance commits this week (`ci: bump actions/checkout to v6` / `bump
node20/node16 actions to node24` — a GitHub Actions Node-20-runner
deprecation sweep). Repos whose *only* activity this week is that sweep are
listed briefly near the end rather than repeated individually.

## FEATURED

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**FEATURED — new repo created this week.**
- Initial live scrape (`plugin-details.json` + daily GitHub Action),
  an interactive install-count chart on GitHub Pages, history builder.
- Note: this repo already had commits *dated* in prior weeks
  ("recovered from Arq backup") even though the GitHub repo object itself
  wasn't created until this week — Jesse restored older scrape history
  into a freshly created repo. Not a data bug; just worth knowing why it
  showed prior "activity" before it technically existed.
- Contributors: `github-actions[bot]` (daily scrape) and Jesse Vincent
  (staff).

### prime-radiant-inc/superpowers-autoresearch
No public description set.
**FEATURED — new repo created this week.**
- An internal research-methodology tool: a RED/GREEN evidence-battery
  campaign format (pre-registration, held-out battery, blinded re-grade)
  applied to a "writing-skills" experiment; found and reported a
  counter-intuitive "backfire" result.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/superpowers-docs
No public description set.
**FEATURED — new repo created this week.**
- A docs/brochure-generation Superpowers plugin: hub `SKILL.md` +
  dispatch, a marketing-flow and brochure-design flow, driven by the same
  RED/GREEN evidence-record method as `superpowers-autoresearch`, applied
  live to real projects (clipfan's brochure site, slackline).
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/clipfan
Clipboard sync daemon for Mac + remote tmux fleet.
**FEATURED — 12 tagged releases, crossing `v1.0.0` this week.**
- Completed the mesh self-healing feature across its remaining phases:
  daemon fleet aggregation, self-healing mesh triggered on add-host,
  mesh-state visibility + a "Repair mesh" action, and a first-run
  onboarding wizard.
- Post-1.0 hardening: large-clip sync + stream resilience fixes (SSH
  payload-size limits, no more infinite resend-on-rejection), menu-bar
  icon/animation polish, a macOS pasteboard Unicode-locale fix.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/obol
Reads an AI-agent transcript and estimates what it cost.
**FEATURED — tagged releases `v0.4.1` through `v0.2.0` (7 releases).**
- Added Pi session-file parsing and native cost support.
- Sole contributor: Matt Windbrook (staff).

### prime-radiant-inc/slackline
Slack-identity CLI for AI agents.
**FEATURED — tagged release `v0.3.4`.**
- Enforced a download-body-size cap on Slack downloads; mapped Cobra usage
  failures to a distinct exit code.
- Docs/brochure work (an "isolate the problem beat" pass, index +
  dictionary bootstrap) — the first output of the new `superpowers-docs`
  methodology, applied to slackline itself.
- Sole contributor: Jesse Vincent (staff).

## SECOND-TIER

### prime-radiant-inc/serf
Non-interactive coding agent.
**second-tier**, one merged PR, no release — by far the week's largest
commit volume.
- A major "reasoning-effort" feature: per-model effort levels controllable
  at runtime (command palette + spawn-form chip), with catalog-driven
  clamping across providers (Anthropic 1M-context handling, OpenRouter,
  dated model refs).
- Kimi coding-agent support: a `User-Agent` announcement so Kimi accepts
  requests, plus a required `serf/auth` v0.1.0 dependency bump.
- "Forced-note-at-compaction": the harness now elicits a one-shot handoff
  note before compacting context, evaluated end-to-end against a
  with/without-note comparison harness.
- Contributors: Jesse Vincent (staff) overwhelmingly; Matt Windbrook
  (staff, a handful of commits).

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum).
**second-tier**, seven merged PRs, no release.
- The week's headline: a full Quorum-to-TypeScript port, bringing the
  Python harness's Specs 1-5 (and setup-helpers) to parity in TS across
  every adapter (Claude, Codex, Copilot, Gemini, Kimi, Antigravity,
  Opencode, Pi) — credential handling, session-attribution, rate-limit
  matchers, and diagnostics redaction all re-ported one region at a time.
- Adopted `obol` for run-cost capture; fixed Claude transcript persistence
  against the latest CLI.
- Contributors: a genuine three-way staff collaboration — Jesse Vincent,
  Matt Windbrook, and Drew Ritter (all staff).

### prime-radiant-inc/stockyard
Coding-agent VM orchestrator.
**second-tier**, seven merged PRs, no release.
- Multi-image support end to end: per-task image selection, a
  Firecracker image registry (ZFS-backed, named, orderly-replace), a
  `stockyard image ls/import/rm` CLI surface.
- Removed the `stockyard exec` command-queue subsystem; qualified Apple
  container images under `stockyard.local/*` to de-noise `image ls`;
  fixed Tailscale connectivity in `stockyardd` on macOS.
- Contributors: Matt Windbrook (staff) led every PR; Jesse Vincent (staff)
  merged.

### obra/claude-session-driver
Launch, control, and monitor Claude Code sessions as workers via tmux.
**second-tier**, no release this bucket (see week 4 for the resulting
`v4.0.0`).
- Completed a full rewrite of the core from bash to TypeScript across four
  phases: claude parity, a Codex driver, a Pi driver, then docs/closeout —
  landing multi-harness support (`--harness claude/codex/pi`) and native
  Node hooks.
- Sole contributor: Jesse Vincent (staff).

### obra/lace
Lightweight agentic coding environment.
**second-tier**, four merged PRs, no release.
- Async-only delegation: removed blocking subagent waits in favor of
  snapshot-only `job_output`.
- Credential redesign Part B: delivery placeholders, broker-socket
  threading through resumed sessions, fail-closed re-resolution when a
  persisted binding disagrees with the current persona.
- "Helperless" container tools: `file_*`/`url_fetch` now go through a
  brokered `docker exec` instead of a sidecar helper.
- MCP auto-reconnect for dropped in-container servers; UTF-16
  lone-surrogate sanitization before sending to Anthropic.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers
Agentic skills framework and methodology.
**second-tier**, five merged PRs, no release.
- SDD (spec-driven development) methodology iteration: a "strict-cost"
  review-tier experiment ladder, task-scoped review dispatch (one reviewer
  per task, review-package script), reviewer-prompt hardening (forbid
  pre-judging findings, require diffs as files not pastes).
- Brainstorming visual-companion hardening: auth, lifecycle, reconnect,
  Windows browser-launcher fixes.
- Contributors: Jesse Vincent (staff) and Drew Ritter (staff).

### obra/winpepper
Windows-native local dictation.
**second-tier**, 16 merged PRs, no release this bucket — entirely
**outside**-authored.
- MSI installer improvements (registry-search replaces a VBScript custom
  action), a Fluent/Windows-11 UI polish pass, a hotkey-recording
  crash/cancel fix, tray-icon registration hardening, e2e smoke-test
  infrastructure, a real multi-resolution app icon, correct Apache-2.0
  license text in the installer.
- Sole contributor this week: danshapiro (**outside**) — every PR both
  opened and merged by him.

### prime-radiant-inc/gauntlet
AI-powered QA testing framework.
**second-tier**, three merged PRs, no release.
- Judge/verdict reliability hardening: a stall watchdog for frozen
  read-poll loops, `max_tokens`-truncation recovery instead of dying
  indeterminate, cited-per-criterion verdict requirements.
- Emits an `obol` cost sidecar (`usage.jsonl`) per LLM call.
- Contributors: Jesse Vincent (staff) and Matt Windbrook (staff).

### prime-radiant-inc/obol-go
Generated Go binding for obol.
**second-tier**, no release — mirrors `obol`'s own release train
mechanically.
- Six machine-generated release commits (`obol-release`, the automated
  release identity — not a human, do not tag as outside), tracking obol's
  `v0.2.0` through `v0.4.1`; one manual commit from Matt Windbrook (staff).

### obra/arq_restore
Fork of `arqbackup/arq_restore` with fixes for modern macOS.
**second-tier**, no PRs/release — a real fork with real ahead-of-parent
work (not one of the dormant zero-commit forks).
- Namespace-agnostic S3 XML XPath parsing, replaced `NSCalendarDate` with
  `NSCalendar`/`NSDateComponents`, pinned the SigV4 date formatter to UTC,
  added bulk-restore env hooks for Arq 7 + S3 + Glacier.
- Sole contributor: Jesse Vincent (staff).

### obra/private-journal-mcp
MCP server for a private Claude journaling capability.
**second-tier**, minimal.
- `v2.0.1` release; an ESLint config fix; a path-validation hardening fix
  on `read_journal_entry`.
- Sole contributor: Jesse Vincent (staff).

### obra/dotfiles
Jesse's personal dotfiles.
**second-tier**, minimal.
- A new `maintaining-documentation` skill (renamed from
  `auditing-documentation`): a `docmaint` scan/stamp/stale CLI for
  doc-staleness triage.
- Sole contributor: Jesse Vincent (staff).

### obra/temp-sp-codex
"Temporary Superpowers Codex marketplace test repo."
**second-tier** — ⚠ same mirror-repo anomaly as weeks 1-2: duplicates
`obra/superpowers`'s commits exactly. Not distinct work.

### CI-sweep-only repos (Node 20 runner deprecation)
The following had no activity this week beyond the `actions/checkout`
v6 / Node-24-runner bump commits (all Matt Windbrook, staff, except where
noted): `prime-radiant-inc/beeper-message-sync`, `claude-session-viewer`,
`engineering-notebook`, `gsuite-mcp` (fork), `kindle-highlight-exporter`,
`ts-libghostty`. `prime-radiant-inc/llm-proxy` and
`prime-radiant-inc/superpowers-docs`-adjacent `sprout` also had a single
docs-only commit (Jesse Vincent, staff) alongside/instead of the CI bump.
`prime-radiant-inc/terminal-bench-analysis`: bot-only Datasette
regenerations (`github-actions[bot]`, no new data), same as prior weeks.
`obra/superpowers-marketplace`: version-pin bump only.

---

## Anomalies / notes for this week
- **`obra/temp-sp-codex`** still mirroring `obra/superpowers` — third
  week running.
- **`prime-radiant-inc/claude-plugin-stats`** shows commits in weeks 1-2 of
  this backfill (dated May 30 / Jun 4) despite being *created* this week —
  explained above (Arq-backup recovery into a new repo), not a tooling
  bug.
- **`obra/winpepper`** this week is the batch's clearest single-contributor
  outside-driven week: every merged PR both opened and merged by
  danshapiro, with no staff commits at all in the bucket.
