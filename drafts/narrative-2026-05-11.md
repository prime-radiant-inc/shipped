# Narrative brief — week of 2026-05-11 (through 2026-05-17)

Grounded in `data/recon-v2-4wk-20260427-batch2.json` (week index 2) +
`src/data/weekly-stats.json["2026-05-11"]`. Backfill batch 2 (historical,
pre-launch week). No numbers below — pure narrative themes.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member (or
`mhat`, staff for this whole window per the owner). Everyone else is labeled
**outside** explicitly per repo, below.

**⚠ Read the anomalies section before using this week's aggregate LOC
figure** — it is dominated by two artifacts, not real shipped code (see
bottom of this brief).

## FEATURED

### obra/claude-session-driver
Launch, control, and monitor other Claude Code sessions as workers via
tmux.
**FEATURED — tagged releases `v2.0.1` and `v2.0.0`** (plus commit-message-
only bumps `v1.1.0` and `v1.0.2` earlier in the week).
- `v2.0.0` dropped the "fake tool-approval gate"; `v2.0.1` disallows
  `AskUserQuestion` inside workers. Three rounds of user-feedback fixes in
  between: a universal worker handle, spec-aligned paths, status/handoff
  commands, a default worker listing.
- Contributors: Jesse Vincent (staff). One commit is attributed to the
  git-config identity `jesse` (email `jesse@fsck.com`-style but from a
  different machine) rather than the linked `obra` account — almost
  certainly Jesse under an unlinked local git identity, given it's
  interleaved with his own commits in the same file/feature, but GitHub's
  API doesn't resolve it to any account, so flagging rather than silently
  merging the credit.

### obra/episodic-memory
Memory/recall layer for coding-agent sessions.
**FEATURED — tagged releases `v1.4.1`, `v1.4.0`, `v1.3.1`, `v1.3.0`.**
- Codex support landed end-to-end: transcript parsing, session
  summarization, plugin packaging, hook synchronicity, production
  hardening (raw-HTML escaping, local-shell-output handling).
- Reliability: `v1.4.1` drains a zero-exchange sync backlog that had been
  silently stalling summarization; recall-trigger reliability improved,
  the `/search-conversations` slash command dropped.
- Contributors: Jesse Vincent (staff); one commit from **outside**
  contributor `minyek`.

### obra/superpowers-chrome
Chrome-control plugin via DevTools Protocol.
**FEATURED — tagged release `v2.1.0`.**
- Dialog handling landed as a first-class concern: a `DialogRefusedError`
  thrown (not silently swallowed) on browser dialogs, a permission shim
  registered at attach, dialog-awareness threaded through mouse/keyboard/
  capture/cdp-connection attachers, Tier-C smoke tests against real Chrome.
- Sole contributor: Jesse Vincent (staff).

### obra/winpepper
Windows-native local dictation.
**FEATURED — new repo created this week + tagged release
`v0.6.0-alpha`.** ⚠ Note: this is the actual creation week (later weeks'
briefs, already published, cover its ongoing life) — and unlike every
subsequent week, **100% of this week's 156 commits are Jesse Vincent
(staff)**, not the external contributors who join afterward.
- Loud upfront about its own provenance ("entirely agentic, never
  human-tested") in the README. Built out in plan-numbered milestones in a
  single week: Plan 4 (history/lab/models tab + downloader), Plan 5
  (post-paste learning, Diagnostics page, crash handling via
  `MiniDumpWriter`), Plan 6 (WiX MSI packaging, autostart, code-signing
  wrapper, nightly CI smoke).
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project.
**FEATURED — new repo created this week.**
- Split out of the `drill`/`evals/` harness lifted into superpowers the
  prior week; shipped a Codex-native-hook eval backend and Pi backend
  support in the same week, plus initial security hardening.
- Contributors: Drew Ritter (staff) and Matt Windbrook (staff) — including
  three merged PRs, one of which (Codex security controls) explicitly
  targeted hardening ahead of wider use.

## SECOND-TIER

### obra/lace
Lightweight agentic coding environment.
**second-tier**, no PRs/release. ⚠ **LOC-figure caveat**: gather.py's
local `git log --numstat` reports one merge commit this week
(`ad01889`, "Merge branch 'fix/provider-tool-name-sanitization' into dev")
at ~459K added lines — but GitHub's own commit API reports that same
commit's real diff at 630 additions / 266 deletions. This is a tooling
artifact isolated to this one commit (verified other large merges this
week diff correctly); don't use this week's raw LOC total for `lace` or
for the week's aggregate.
- The real work: persona-bundle support prep (Ent initialize + `session/
  create` accepting persona config, ordered user search paths,
  frontmatter+body parsing), a provider tool-name sanitizer (the actual
  content of the inflated merge commit).
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/gauntlet
AI-powered QA testing framework.
**second-tier**, no release — very large commit volume.
- A `bash` tool for agents (allow-listed env, output caps, process-tree
  reaping) plus a "shell-as-session" model for the TUI and CLI adapters
  (spawn bash in a tmux pane / scratch cwd, single-SIGKILL close
  escalation).
- A `fetch_credential` tool threaded through the orchestrator, and an
  eight-story-card TodoMVC example fixture (CLI/TUI/Web frontends).
- Sole contributor: Matt Windbrook (staff).

### prime-radiant-inc/greenfield
Claude Code plugin that reverse-engineers behavioral specs from a codebase.
**second-tier**, minimal — one commit, from **outside** contributor
`uwumarogie`: restructured skills into per-skill directories with a
`SKILL.md` each.

### prime-radiant-inc/bot-toolkit
Reusable TypeScript core for building unattended Claude-powered chat
agents.
**second-tier**, tagged as a commit-message-only bump (`v1.0.2`), no
GitHub Release object.
- Small config addition: an `autoMemory` opt-out for the Claude Agent SDK's
  built-in auto-memory (the same knob `scribble` uses this same week to
  disable it entirely).
- Sole contributor: Drew Ritter (staff).

### obra/superpowers-marketplace
Curated Claude Code plugin marketplace.
**second-tier**, minimal — version-pin bumps only (claude-session-driver
`v1.0.2`, episodic-memory `v1.3.0`).
- Contributors: Jesse Vincent (staff); one commit carries the unlinked
  `jesse` git identity flagged elsewhere in this brief.

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, minimal — one data-recovery commit ("recovered from Arq
backup"). Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/scribble
Self-hosted Slack knowledge bot.
**second-tier**, one merged PR, no release.
- Public-repo hardening merged (pinned Actions, Dependabot, CODEOWNERS,
  trimmed internal references) alongside disabling the Claude Agent SDK's
  built-in auto-memory (Scribble owns its own wiki-backed memory) and an
  OpenTelemetry advisory patch.
- Sole contributor: Drew Ritter (staff).

### prime-radiant-inc/serf
Non-interactive coding agent.
**second-tier**, no PRs/release — the week's largest raw commit count.
- A JSON-naming convention pass (camelCase JSON, kebab-case TOML/CLI,
  enforced by a new `serf-namingcheck` lint); OpenAI device-code login for
  headless sessions; OAuth-state-over-env-var precedence fixes.
- Contributors: Jesse Vincent (staff). A large share of commits carry the
  unlinked `jesse` git identity discussed above (same flag applies) rather
  than the linked `obra` account.

### prime-radiant-inc/slackline
Slack-identity CLI for AI agents.
**second-tier**, minimal — two commits, no release.
- A Node-24 CI runtime bump and a provisioning fix (verify the registered
  app name; team-scope the OAuth authorize URL).
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/terminal-bench-analysis
Fetches Terminal Bench 2 leaderboard results into SQLite, publishes via
Datasette.
**second-tier**, bot-only activity — ⚠ **this is the week's dominant LOC
figure**: a single `github-actions[bot]` commit ("Add 13795 trials for 30
submissions...") adding roughly 1.5M lines of generated/data content. Not
human-authored work; exclude from any "biggest week" framing, same caveat
as batch 1's week-1 anomaly.

### prime-radiant-inc/ts-libghostty
TypeScript bindings around Ghostty's VT state machine.
**second-tier**, minimal — two commits, no release.
- Two more "bobbihack" fixes (a lock-cleanup bug that was deleting level
  data; a v2.5 golem-glyph/pet-swap/door-predict fix).
- Sole contributor: Matt Windbrook (staff).

### obra/superpowers
Agentic skills framework and methodology.
**second-tier** — eleven merged PRs, but **zero commits with an in-window
author date** (same pattern flagged in the prior two weeks' briefs: PR
merge date falls in-window, underlying commit dates don't).
- Real shipped work per the PRs: cross-platform skill-compatibility prose
  (agent-neutral, source-verified per-runtime tool references), a Pi
  extension + eval backend, several Codex-track fixes (submodule bumps,
  native plugin hooks, moving the eval harness to a submodule).
- Contributors (by PR, not commit-date): Jesse Vincent (staff, several
  merges) plus **two distinct outside contributors**, each with one PR:
  fuleinist (stale `.cursor-plugin` reference cleanup) and stablegenius49
  (writing-skills `@`-reference fix).

### obra/ghost-pepper
Hold-to-talk speech-to-text for macOS (fork).
**second-tier**, minimal — two commits, no release.
- A usage report, model-sidebar buttons, Granola auto-import, and an IDE
  rename.
- Sole contributor: **outside** contributor Matt Hartman (`matthartman`).

---

## Anomalies / notes for this week
- **Two LOC-inflation artifacts drive this week's aggregate `loc_added`
  figure** — do not use it at face value:
  1. `prime-radiant-inc/terminal-bench-analysis`: a single bot commit
     adding ~1.5M generated lines.
  2. `obra/lace`: one merge commit (`ad01889`) that `git log --numstat`
     reports at ~459K added lines, versus GitHub's own API reporting the
     real diff at 630/266. Verified this is isolated to this one commit
     (other large merges this week check out correctly against the API).
- **Two contributor-identity flags**, both pointing to the same likely
  explanation: commits authored under the display name `jesse` (email
  `jesse@fsck.com`-pattern but unlinked to any GitHub account) appear
  alongside `Jesse Vincent`/`obra` commits in `serf` and
  `claude-session-driver` this week. Very likely Jesse himself on a
  second machine with an unconfigured git email, but GitHub's API can't
  confirm it — flagging per the "don't guess" rule rather than merging
  the credit.
- **`obra/superpowers`** continues the "many merged PRs, zero in-window
  commit authors" pattern from the prior two weeks — the credit lines
  above are PR-author-derived, not commit-rollup-derived.
- `obra/winpepper`'s creation week is a genuine outlier vs. every
  subsequent week already covered by earlier live/backfilled posts: 100%
  staff-authored here, before outside contributors (Nat Torkington,
  danshapiro) join in later weeks.
