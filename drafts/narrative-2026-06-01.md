# Narrative brief — week of 2026-06-01 (through 2026-06-07)

Grounded in `data/recon-v2-4wk-20260525-backfill.json` (week index 1) +
`src/data/weekly-stats.json["2026-06-01"]`. Backfill batch 1 (historical,
pre-launch week). No numbers below — pure narrative themes.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member (or
`mhat`, staff for this whole window per the owner). Everyone else is labeled
**outside** explicitly per repo, below.

**Cross-cutting note:** a large batch of otherwise-quiet repos in both orgs
picked up an identical single commit this week — `docs: add project-map
catalog-info.yaml and ABOUT.md` (an org-wide project-catalog rollout, not
per-project feature work). Repos whose *only* activity this week is that
commit are listed briefly at the end rather than repeated individually.

## FEATURED

### obra/homedir-manager
Symlink-deploy and audit tool for dotfiles content repos, plus a macOS
defaults helper (POSIX sh + Swift; "AI-written, unreviewed").
**FEATURED — new repo created this week.**
- Split out of `obra/dotfiles`'s "management machinery" into its own
  standalone engine: multi-repo discovery, deploy/audit engines, a
  marker-based content-repo registry.
- `merge-children` manifest directive for expanding a directory's children
  into a symlink target (with drift-check + orphan detection).
- Shellcheck-clean CI (Linux/macOS/Swift), pre-push secret-audit hook,
  vendored `macos-defaults` Swift helper.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/obol
Reads an AI-agent transcript and estimates what it cost — Rust core with
C-ABI bindings for Python, Go, and TypeScript.
**FEATURED — new repo created this week + tagged release `v0.1.1`.**
- Launched and immediately built out a full multi-channel release pipeline
  in the same week: PyPI (4 platform wheels + OIDC), crates.io (OIDC trusted
  publishing), and npm (`@primeradianthq/obol`), plus a CI foundation.
- Contributors: Matt Windbrook (staff) led; Jesse Vincent (staff)
  co-committed. Two commits from **"Mario"** (`mario@bobiverse.local`) — no
  linked GitHub account found; **flagging as unclassifiable rather than
  guessing** staff/outside.

### prime-radiant-inc/obol-go
Generated Go binding for obol; loads the native library at runtime via
`purego`, no cgo.
**FEATURED — new repo created this week.**
- Bootstrap of the Go binding publish target, tag-generated from
  `prime-radiant-inc/obol` releases.
- Contributors: `obol-release` (an automated release-bot identity —
  commits are machine-generated "Release vX.Y.Z (generated from
  obol@<sha>)", not a human; do not label as outside contributor) and Matt
  Windbrook (staff).

### prime-radiant-inc/clearance
Clearance product workspace — Markdown viewer monorepo.
**FEATURED — tagged releases `v1.3.5` and `v1.3.4`.**
- Local CLI install option added; macOS download instructions clarified.
- Native-appearance and UI polish: standard zoom shortcut, transparent
  icon corners preserved, dark-appearance handling fixed, bundled release
  notes opened read-only.
- Contributors: Jesse Vincent (staff); one PR (`#51`, a macOS open-app fix)
  came in via a Codex-authored branch, and Jonah (**outside**, GitHub
  login `alibi85`) is credited on one commit.

### prime-radiant-inc/slackline
Single-binary Go CLI giving AI agents a Slack identity.
**FEATURED — tagged releases `v0.3.3`, `v0.3.2`, `v0.3.0`, `v0.2.3`
(+ commit-only bump `v0.3.1`).**
- Cut jq-friction: `listen --type` allowlist filter, unified
  `reaction_added`/`removed` into one `reaction` event with an action
  field, a distinct timeout exit code for `ask`.
- Consolidated the Slack skill set: folded `slackline-provision-bot` into
  `using-slack`, made the plugin self-distributing.
- Fixed a `read --thread` tail-omission bug and validated security
  findings.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/clipfan
Clipboard sync daemon for Mac + remote tmux fleet.
**FEATURED — 29 tagged patch releases this week (`v0.3.1` through
`v0.3.29`).** ⚠ Note the release count: this project tags a release per
merged change, so the number is a packaging-cadence artifact, not 29
distinct features.
- The week's real headline: a self-healing SSH mesh (`mesh-heal`) —
  decentralized roster discovery, host-key trust hardening (closed a
  TOCTOU + truncation gap), resilient sync-pin host-prep, Go-daemon
  restart recovery.
- Fleet UX: an "About" window, explicit Add-Peer success state, SSH-aware
  fleet-outbound indicators.
- Reliability fixes: launchd `PATH`/`tmux`-path resolution, atomic
  session-current SSH-receive handling, stale-session guards.
- Sole contributor: Jesse Vincent (staff).

## SECOND-TIER

### prime-radiant-inc/serf
Non-interactive coding agent.
**second-tier**, no PRs/release this week.
- A "goal" objective engine: persists across restart/resume, live status
  chip in both TUI and web hub, re-injected on compaction, hardened per
  adversarial review.
- Resumed-session fixes (active turn id preserved, task-status UI
  cleanup).
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum).
**second-tier**, no tagged release.
- Onboarded two new eval targets into the harness: Copilot and Kimi
  (isolated auth/session preflight, capture diagnostics, rate-limit
  handling for each).
- `agy` fail-fast reliability work: rate-limit detection/kill/verdict path
  with credential backup+restore around mid-run kills.
- A suite-tiering mechanism (sentinel/adhoc tiers, `run-all --tier`
  filtering).
- Contributors: Drew Ritter (staff) drove most of this week; Jesse Vincent
  (staff) co-committed.

### obra/lace
Lightweight agentic coding environment.
**second-tier**, four merged PRs, no release.
- Environment-based container-role refactor: role→environment resolution
  drives the container spec, replacing ad hoc identity params; the
  credential-broker socket now threads through `ToolContext` per
  environment.
- Removed the now-redundant `sen-cred` mount gate and vestigial
  `containerExecutionIdentity`.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers
Agentic skills framework and methodology.
**second-tier**, ten merged PRs, no release — the week's most
outside-heavy repo.
- Multi-harness expansion: Antigravity CLI (`agy`) support and a Kimi Code
  plugin manifest added.
- Windows polyglot-hook fixes (foreground-mode PID handling, doc
  corrections) and a WebSocket-frame-payload cap fix in brainstorming.
- Contributors: Drew Ritter (staff) dominant. **Five distinct outside
  contributors**, each with a small fix/manifest addition: Matt Van Horn
  (`mvanhorn`), `dev_Hakaze` (`arimu1`), `nestorluiscamachopaz`, `nawfal`
  (`nawfalaf`), and `qer` (`wbxl2000`). A sixth outside contributor, Rahul
  (`therahul-yo`), opened the WebSocket-frame-payload-cap PR (#1555).

### prime-radiant-inc/gauntlet
AI-powered QA testing framework.
**second-tier**, minimal — one commit.
- Housekeeping only this week (the project-map commit); no feature work.
- Sole contributor: Jesse Vincent (staff).

### obra/dotfiles
Jesse's personal dotfiles.
**second-tier** — the week's biggest "quiet" repo by volume.
- A secrets-management overhaul: adopted `fnox` as the single lazy
  per-command secret mechanism, replacing the old by-title resolver; a
  vault-agnostic (`op`/`rbw`/`bw`) dispatch helper.
- Cross-OS shell refactor: zsh config moved under `ZDOTDIR`, a Linux
  drop-in added, `gh` used for the git credential helper cross-platform.
- New `auditing-documentation` skill (later renamed
  `maintaining-documentation`).
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/superpowers-testing
Development/testing marketplace for Superpowers.
**second-tier**, minimal — one commit (housekeeping only).

### Housekeeping-only repos (org-wide project-map rollout)
The following repos had **no activity this week beyond** the single
`docs: add project-map catalog-info.yaml and ABOUT.md` commit (all Jesse
Vincent, staff) — no feature work, no PRs, no releases:
`prime-radiant-inc/beeper-message-sync`, `books-for-bots`, `bot-toolkit`,
`claude-plugin-cxdb-integration`, `claude-plugin-stats`,
`claude-session-viewer`, `engineering-notebook`, `github-triage`,
`gsuite-mcp` (a fork), `harbor-eval-analysis-dashboard`, `hearthstone`,
`homebrew-tap`, `iterative-development`,
`iterative-development-example-ghost-pepper`, `kindle-highlight-exporter`,
`llm-proxy`, `parallel-adversarial-review` (plus a project-map ownership
tweak), `prime-radiant-marketplace`, `scenarios`, `scribble`, `sprout`,
`stockyard`, `streamlinear`, `terminal-bench-analysis`, `ts-libghostty`,
and `obra/superpowers-lab` (a version-bump commit only, removing the
`slack-messaging` skill in favor of slackline's `using-slack`),
`obra/superpowers-chrome` (v3.0.2 release note only), `obra/claude-session-driver`
(v3.0.2 release, a stale-env fix on worker adopt), and
`obra/superpowers-marketplace` (two version-pin bumps only: `superpowers-lab`
to 0.5.0, `claude-session-driver` to v3.0.2).

### obra/temp-sp-codex
"Temporary Superpowers Codex marketplace test repo."
**second-tier** — ⚠ same mirror-repo anomaly as week 1: commit history
duplicates `obra/superpowers` exactly (including its outside contributors)
despite this repo's own `created_at` being four weeks after this bucket.
Not distinct work; already covered under `obra/superpowers` above.

---

## Anomalies / notes for this week
- **"Mario"** (`prime-radiant-inc/obol`, email `mario@bobiverse.local`) —
  no linked GitHub account; genuinely unclear whether staff, outside, or a
  test/internal identity. Flagging rather than guessing.
- **`obol-release`** (`prime-radiant-inc/obol-go`) — a release-automation
  identity (noreply email, machine-generated commit messages), not a human
  contributor. Do not tag as "outside."
- **`obra/temp-sp-codex`** continues to mirror `obra/superpowers` — see
  week-1 brief for the same caveat.
- The org-wide project-map commit sweep inflates this week's "repos
  active" count substantially (43) relative to actual feature throughput —
  worth calling out if the published post leans on that number.
