# Narrative brief — week of 2026-05-04 (through 2026-05-10)

Grounded in `data/recon-v2-4wk-20260427-batch2.json` (week index 1) +
`src/data/weekly-stats.json["2026-05-04"]`. Backfill batch 2 (historical,
pre-launch week). No numbers below — pure narrative themes.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member (or
`mhat`, staff for this whole window per the owner). Everyone else is labeled
**outside** explicitly per repo, below.

## FEATURED

### prime-radiant-inc/bot-toolkit
Reusable TypeScript core for building unattended Claude-powered chat agents.
**FEATURED — new repo created this week + tagged releases `v1.0.0` and
`v1.0.1`.**
- Stood up and shipped to npm in the same week: sealed public SDK/route
  boundaries, an allowlisted Claude-SDK environment, npm-provenance-gated
  release publishing, a public-package quality gate in CI.
- Sole contributor: Drew Ritter (staff).

### obra/episodic-memory
Memory/recall layer for coding-agent sessions.
**FEATURED — tagged release `v1.2.0`.**
- Swapped in the `bge-small-en-v1.5` encoder with auto-migration for
  existing databases; an end-user-facing changelog rewrite (Strunk pass),
  including a self-correction of the model's file-size claim (22 MB → 34
  MB actual).
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers
Agentic skills framework and methodology.
**FEATURED — tagged release `v5.1.0`.**
- Lifted the `drill` eval tool into superpowers proper as an `evals/`
  harness — the seed of what becomes the standalone
  `superpowers-evals` repo the following week.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/parallel-adversarial-review
Two Claude Code skills for adversarial code review (single-model PAR and
multi-model MMAR with cross-critique to catch hallucinations), plus a
fixture-based eval suite.
**FEATURED — new repo created this week.**
- Initial plugin commit followed same-week by a self-review pass (findings
  from the plugin's own MMAR review applied to itself) and an adapter-roster
  update (dropped aider/cursor-agent, added Pi and Droid).
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/streamlinear
Lightweight Linear MCP server for Claude Code.
**FEATURED — tagged release `v1.1.3`.**
- First npm-packaged release: package metadata, rebuilt dist artifacts, npm
  trusted publishing wired into CI, plus a `v1.1.2` release the same week.
- Sole contributor: Drew Ritter (staff).

## SECOND-TIER

### prime-radiant-inc/gauntlet
AI-powered QA testing framework.
**second-tier**, no release.
- Adopted `chrome-ws-lib`'s new flatten-mode + browser-WS bridge (landed
  upstream in `superpowers-chrome` the same week); tightened the
  `report_result` observations schema to discourage stringified payloads.
- Contributors: Matt Windbrook (staff) led; Jesse Vincent (staff)
  co-committed.

### prime-radiant-inc/serf
Non-interactive coding agent.
**second-tier**, no PRs/release.
- Web slash-command palette for `serf-hub`; a mobile-responsive pass
  (off-canvas sidebar, stacked controls); transcript-fork drafts and a live
  dashboard for `serf-tui`.
- Sole contributor: Jesse Vincent (staff).

### obra/superpowers-chrome
Chrome-control plugin via DevTools Protocol.
**second-tier**, one merged PR, no release (bumped to `2.0.0` as a
commit-message-only version bump).
- The `createSession()`/`createOverride()` factory migration (started last
  week) landed fully: CDP timeout/error propagation hardening, cross-platform
  PID lookup, a large Tier-A/B/C test-suite build-out, Biome lint adoption.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/scribble
Self-hosted Slack knowledge bot.
**second-tier**, no PRs/release — heavy OSS-readiness push.
- Policy hardening: log-payload scrubbing, input validation/clamping across
  every tool (`wiki_search`, `conversation_search`, `log_decision`,
  `slack_reply`), path-traversal rejection on malformed channel IDs.
- Prepared for public install: Docker-first setup, tenant-configured
  runtime, a required `WIKI_REPO` (dropped the silent
  `prime-radiant-inc/scribble-wiki` fallback), adopted the newly-published
  `bot-toolkit` package.
- Sole contributor: Drew Ritter (staff).

### prime-radiant-inc/llm-proxy
Transparent logging proxy for LLM API traffic.
**second-tier**, minimal — one commit.
- Default the log directory to `~/.llm-provider-logs` in non-service mode.
- Sole contributor: Matt Windbrook (staff).

### obra/superpowers-marketplace
Curated Claude Code plugin marketplace.
**second-tier**, minimal — version-pin bumps only (superpowers-chrome
`v2.0.0`, superpowers `v5.1.0`, episodic-memory `v1.2.0`).
- Sole contributor: Jesse Vincent (staff).

### obra/temp-sp-codex
"Temporary Superpowers Codex marketplace test repo."
**second-tier** — ⚠ same mirror-repo anomaly as prior weeks: its one commit
this week (a `v5.1.0` release-note bump) duplicates `obra/superpowers`
exactly. Not distinct work.

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, minimal — one data-recovery commit ("recovered from Arq
backup").

### prime-radiant-inc/ts-libghostty
TypeScript bindings around Ghostty's VT state machine.
**second-tier**, one merged PR, no release — two commit-message-only
version bumps (`v0.6.0`, `v0.6.1`).
- Continued the "bobbihack" NetHack-agent demo through several more phases
  (danger-classification, modal-prediction, predict-and-avoid); merged a
  Linux-portability PR adding a portable C shim for `linux-{x64,arm64}` ×
  {glibc,musl}; switched release publishing to npm OIDC trusted publishing.
- Contributors: Matt Windbrook (staff) — including the Linux-portability
  PR (#1), authored by Matt Windbrook himself, not an outside contributor.

---

## Anomalies / notes for this week
- No bot-driven LOC spikes, zero-commit tagged releases, or org-wide
  sweeps this week.
- `obra/temp-sp-codex` mirror artifact recurs for the second straight
  week (see batch 1 and the prior week's brief).
