# Narrative brief — week of 2026-04-27 (through 2026-05-03)

Grounded in `data/recon-v2-4wk-20260427-batch2.json` (week index 0) +
`src/data/weekly-stats.json["2026-04-27"]`. Backfill batch 2 (historical,
pre-launch week). No numbers below — pure narrative themes.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member (or
`mhat`, staff for this whole window per the owner). Everyone else is labeled
**outside** explicitly per repo, below.

## FEATURED

### obra/episodic-memory
No public description set on GitHub (a memory/recall layer for coding-agent
sessions, per its commit history).
**FEATURED — tagged releases `v1.1.2`, `v1.1.1`, `v1.1.0`.**
- Search filters by project/session/git-branch, a schema migration, and
  summarizer-hygiene fixes (stop polluting `~/.claude/projects` with
  summarizer session JSONLs, cascade-delete on the tool-calls FK).
- `v1.1.2` was an emergency hotfix for a recursive process cascade, following
  hot on `v1.1.1`'s "single source of truth for version numbers."
- Contributors: Jesse Vincent (staff) drove the week; one PR each from two
  **outside** contributors — Matt Van Horn (`mvanhorn`, npm-install flag fix)
  and Asish Kumar (`officialasishkumar`, Windows SessionStart hook path
  quoting fix).

### prime-radiant-inc/books-for-bots
Rust CLI that converts EPUBs into a single YAML-headed Markdown file with
per-chapter byte and line offsets, giving LLM agents a navigation API for
token-efficient reading.
**FEATURED — new repo created this week.**
- Full v1 built and merged in one push: heading/whitespace normalization,
  duplicate-heading and running-header detection, cross-chapter link
  slugging, byte/line offset verification, a determinism test (two runs
  byte-identical).
- Vendored Project Gutenberg's *Alice in Wonderland* as the in-repo example.
- Sole contributor: Jesse Vincent (staff).

## SECOND-TIER

### obra/ghost-pepper
Hold-to-talk speech-to-text for macOS — 100% local, WhisperKit + local LLM
cleanup.
**second-tier** (this is a real fork with genuine ahead-of-parent work, not
a dormant one) — no release/PR this bucket.
- Agentic meeting Q&A: a tool-using agent (grep/read_file/list_dir,
  path-sandboxed to the archive root) that answers questions across loaded
  meeting transcripts, backed by Anthropic's Messages API with SSE
  accumulation.
- A People/meeting indexing system: incremental index builder, sidebar
  browsing, markdown-rendered "dossier" pages with wikilinks, an "Apply to
  dossier" two-step LLM-merge flow.
- Google Calendar OAuth integration (today's-meetings list) and a Cmd+K
  command palette.
- Contributors: **outside** contributor Matt Hartman (`matthartman`) did
  the overwhelming majority of this week's work; Jesse Vincent (staff)
  contributed a handful of commits (including merging in a
  diarization-duplicate-speakers fix and briefly reverting/re-merging a PR
  from Matt Van Horn, **outside**, on sidebar hit targets).

### obra/superpowers
Agentic skills framework and software-development methodology.
**second-tier** — eleven merged PRs, but **zero commits with an in-window
author date** (their commit dates land outside this bucket even though the
merges themselves happened this week) — see anomaly note below.
- Real shipped work this week per the merged PRs: Gemini CLI subagent
  support, a Factory Droid plugin, a session-transcript requirement for
  new-harness PRs, and several Codex-track fixes (install guidance,
  marketplace-metadata preservation, OpenCode integration tests).
- Contributors (by PR, not commit-date): Jesse Vincent (staff, several
  merges) plus **four distinct outside contributors**, each with one PR:
  Sathvik-1007 (Gemini CLI subagent support), starumiQAQ (Windows
  SessionStart hook fix), leonsong09 (Codex subagent-wait-mapping doc fix),
  and Skyline-9 (Factory Droid plugin support).

### obra/superpowers-chrome
Claude Code plugin for direct Chrome browser control via DevTools Protocol.
**second-tier**, no release/PR.
- Migrated all consumers onto a `createSession()` factory (from a
  module-level singleton) ahead of adding a per-session `createOverride()`
  factory for isolation — foundational refactor, not user-facing yet.
- Sole contributor: Matt Windbrook (staff).

### obra/temp-sp-codex
"Temporary Superpowers Codex marketplace test repo."
**second-tier** — ⚠ same mirror-repo anomaly flagged in batch 1: appears
here with a single commit ("Require session transcript for new-harness
PRs") that exactly duplicates a commit already counted under
`obra/superpowers`. Not distinct work; recommend excluding from the
published post.

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, minimal — one commit.
- A single data-recovery commit ("recovered from Arq backup"). No new
  feature work.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/gauntlet
AI-powered QA testing framework.
**second-tier**, no release/PR.
- Multi-pass runs: a `RunSet` orchestrator (cards × attempts loop),
  set-level WebSocket broadcasting, cancel-token registry, a `--passes`
  CLI flag, and a `/run-sets/:id` web page.
- Sole contributor: Matt Windbrook (staff).

### prime-radiant-inc/github-triage
Claude Code plugin for triaging GitHub issues/PRs.
**second-tier**, minimal — one commit.
- A framing fix: bug reports are treated as bug reports, not product
  defects, in the triage prompt.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/sprout
Experimental self-improving multi-agent coding system.
**second-tier**, no release/PR — substantial commit volume.
- Continuation of its memory-relationship work: atomic extracted-memory
  incorporation, relationship classification during incorporation, link
  direction preservation, discovery of links for new memory batches.
- Sole contributor: Jesse Vincent (staff).

### prime-radiant-inc/ts-libghostty
TypeScript bindings around Ghostty's VT state machine.
**second-tier**, no release/PR.
- "bobbihack": a NetHack-playing coding-agent demo built in phases —
  journal/query tools, autopilot navigation, a compaction+cost module, a
  51-turn periodic-compaction integration test.
- Sole contributor: Matt Windbrook (staff).

---

## Anomalies / notes for this week
- **`obra/superpowers`'s eleven merged PRs with zero in-window commit
  authors**: the commits behind those PRs carry dates outside this bucket
  (a common squash-merge/backdate pattern this tool surfaces); the credit
  above is derived from each PR's actual GitHub author, not the (empty)
  commit-author rollup for the week.
- **`obra/temp-sp-codex`** mirror artifact recurs — see batch 1's caveat.
- No bot-driven LOC spikes or zero-commit tagged releases this week.
