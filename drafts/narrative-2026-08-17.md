# Narrative brief — week of 2026-08-17 (through 2026-08-23)

Grounded in `data/recon-v2-1wk-20260821.json` (fork-fix + merge-commit-LOC-fix
gather.py run, both orgs, week bucket 1) + `drafts/weekly-stats-2026-08-17.json`
(WeekSummary/RepoStat-shaped extract, via `tools/gen_stats.py`, staged — NOT
merged into `src/data/weekly-stats.json`). No numbers below — pure narrative
themes; all figures render from the widgets.

**Window is PARTIAL.** Frozen snapshot: 2026-08-21T22:08:25Z (a Friday). The
calendar week runs 2026-08-17 through 2026-08-23; this data covers Monday
through midday Friday only, same as the prior post's mid-week convention.
Say so in the post the way 2026-08-10's did.

**Contributor legend:** "staff" = current `prime-radiant-inc` org member,
confirmed live via `GET /orgs/prime-radiant-inc/members` this run (`obra`
[Jesse Vincent], `ada-sen`, `arittr` [Drew Ritter], `cadence-sen`, `kattni`,
`ketted`, `nora-primeradiant`, `renn-dray`, `simonw`). Applied AT COMMIT TIME,
not just at query time — every commit this week falls inside the last five
days, so current membership is a safe proxy for this window (unlike a
backfilled week, there's no meaningful lag between "current" and
"at-commit-time" here). Everyone else is **outside**, confirmed via
`GET /users/{login}` (company/bio) and an explicit `orgs/.../members/{login}`
404 check — not guessed. Automated identities (GitHub Actions, Dependabot,
and one repo's own agent-tool commit identity — see `evener` note below) are
called out separately, not folded into either bucket.

No AMBIGUOUS contributors this week — every author who touched an active
repo resolved cleanly to staff, outside, or automation. (Flagging this
explicitly since last week's brief had none to report either; if that
changes in a future week, they go here for Jesse.)

## Two renames collided this week — the throughline

Worth a sentence up top because it touches four of the eleven active repos:
**`prime-radiant-inc/serf` was renamed to `prime-radiant-inc/evener`**
(GitHub confirms — the old `serf` path now 302s to `evener`) — same repo,
same coding-agent-that-does-the-work project covered in past posts as
"serf," just wearing its new name from this week on. Separately and
unrelatedly, **the `ledger` tool is being renamed to `chit`** at the
packaging/binary layer (the GitHub repo itself is still named `ledger`) —
`homebrew-tap` retired the `ledger` Homebrew formula in favor of `chit`
(explicitly because the bare `ledger` name collided with homebrew-core's
`ledger-cli`), and `ledger-memory` shipped a release note about following
suit. Keep the two renames straight in the prose — they are not the same
rename and don't share a cause.

## FEATURED (new repo or tagged release)

### prime-radiant-inc/automatic-sshfs
Automatically mount remote filesystems over SSH on macOS via FUSE-T and
ControlMaster.
**FEATURED — new repo, created this week.**
- Built start-to-finish in about a day: SSH-config enumeration (with
  `Include` directive support), a pure reconcile diff of desired vs. actual
  mount sets, `sshoracle` control-path resolution, FUSE-T mount/unmount
  wiring, a `launchd` install/uninstall path with `WatchPaths`, and a CLI
  `list`/reconcile flow — capped with a review-findings cleanup pass (cycle
  guard, prereq check, ControlPath detection, naming).
- Notable authorship split: most feature commits are Jesse Vincent, but a
  meaningful share of the docs/fix commits (the spec-and-implementation-plan
  doc, README passes, a FUSE-T path-detection fix) are authored under the
  `evener` GitHub identity — i.e., the (recently renamed, see above)
  `evener` coding-agent tool itself, committing autonomously while helping
  build this repo. Worth naming explicitly in the post as dogfooding, not as
  an outside human contributor — `evener` the account has no name/company/
  bio set and isn't an org member; it reads as a tool identity, not a person.

### prime-radiant-inc/ledger
Durable, git-backed working-state for coding agents: append-only ledgers
with identity, evidence, cursors, and agent-curated roll-ups.
**FEATURED — two tagged releases (v0.2.0, v0.3.0).**
- The headline is the in-flight rename to `chit` (see above) landing across
  the CLI surface, release assets, and doctrine harnesses in the same
  window as a large "issues tracker" feature arc: a self-service cycle-
  breaker for a deadlocked board (holder-blind detection, paste-ready break
  suggestions), a GitHub-issues bridge (`ledger-gh`) built through several
  spec revision rounds with a live acceptance trial and an unsynced-replica
  hazard writeup, and an offline-first sync design (git-remote-based,
  deterministic merge + lease-push) that went through two corrective
  rewrite rounds before landing.
- Sole author this week: Jesse Vincent (staff).

### obra/winpepper
Windows-native local dictation — hold a hotkey, speak, release, get cleaned-
up words in the focused app; Parakeet TDT v3 ASR + LlamaSharp cleanup, all
local.
**FEATURED — tagged release (v0.7.1-alpha).**
- Small alpha bump: dropped the Windows 11 22H2+ install gate, packaging
  fix.
- Both commits this week are from **outside contributor `danshapiro`**
  (Dan Shapiro — CEO, Glowforge; not a `prime-radiant-inc` member, confirmed
  via GitHub profile and a 404 on org membership). This is a personal
  project of Jesse's (`obra`, not a fork) that an outside contributor is
  actively shipping into.

## ALSO-SHIPPED (rest — compact writeups, not omitted)

### prime-radiant-inc/evener (formerly serf)
A coding agent: give it a prompt and it reads, writes, runs commands, and
searches code in a loop until the work is done, using native tool-calling
across OpenAI, Anthropic, and Google models.
- By far the highest-velocity repo this week, and the biggest story of the
  bunch even without a release: the **serf → evener rename** swept the
  entire codebase (Go module path, identifiers, `cmd/` dirs, frontend
  package/manifest, markdown docs — several of the largest diffs this week
  are this mechanical rename, not net-new feature lines; say so plainly in
  the post rather than let the raw LOC number imply otherwise).
- Underneath the rename: a Makefile decomposition into self-documenting
  per-family targets, an inline-subagent widget redesign ("Rail × Quote"
  card), transcript-autoscroll fixes, an OpenAI Responses effort-ladder
  catalog resolution, a hub-frontend sidebar chrome pass, dependency bumps
  across the GitHub Actions pipeline, fuzz-coverage ratchet work, and a
  string of `Fixes #NNN` issue closures.
- Every commit and every sampled merged PR this week resolves to Jesse
  Vincent (staff, `obra`) as author/merger, plus routine Dependabot bumps —
  no outside PR authors found in a spot-check across the range.

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project.
- Two threads: an "F13" env-credential-scoping arc (scoped container leases,
  immutable rollback, canonical `GEMINI_AUTH_TYPE` validation, several
  review-driven fix rounds) and a "quorum campaign platform" spec that went
  through an adversarial multi-reviewer round before an expected-check
  manifest extractor and multiset-compare feature landed on top of it.
- Sole author: Drew Ritter (staff, `arittr`).

### prime-radiant-inc/homebrew-tap
Homebrew tap for Prime Radiant tools.
- Retired the `ledger` formula in favor of `chit` (name collision with
  homebrew-core's `ledger-cli`) — tied directly to the `ledger` rename
  above. The two version-bump commits are the release-automation bot
  picking up `ledger`'s last release under the old name and `chit`'s first
  release under the new one.
- Authors: Jesse Vincent (staff) for the rename commit; `github-actions[bot]`
  for the automated version-bump commits.

### prime-radiant-inc/teststrip
macOS photo culling app — catalog-first, non-destructive, AI-assisted;
early development, not ready for use.
- A debt-cull pass closing out a batch of tracked issues: import-test
  flakiness, a stack-partition cache, saved-search wording, a dead
  `timelineDays` field, a scenario/test-fixture consolidation into one
  shared support file, a persistence hazard in `replaceAssets`, and a
  `LibraryGridView` modifier-chain refactor.
- Sole author: Jesse Vincent (staff).

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
- Fully automated this week — every commit is the daily scrape-and-rebuild
  job (`github-actions[bot]`), no human commits. Worth a one-line mention
  for completeness per the exhaustiveness rule, not more.

### prime-radiant-inc/shipped
This blog's own repo — a weekly log of what Prime Radiant and `obra`
shipped.
- Self-referential this week: backfill work landed for earlier historical
  weeks (batch-3 content plus a fix for a week-total LOC leak where
  `WeekSummary` was summing `loc_suppressed`-flagged cells it should have
  excluded).
- Sole author: Ada Sen (staff — current `prime-radiant-inc` member; note
  that the immediately preceding live post, week-of-2026-08-10, listed an
  `ada-sen` merged PR as **outside** — she was not yet an org member as of
  that window. She is now. That's the "AT COMMIT TIME" rule working exactly
  as intended, not a contradiction to reconcile.)

### prime-radiant-inc/ledger-memory
Ledger-backed persistent memory plugin for Claude Code.
- One commit, itself a small release (0.1.4) whose whole content is
  following the `ledger` → `chit` rename: binary resolution now prefers
  `chit` with a `ledger` fallback, and the raw-write guard was extended to
  deny both binary names.
- Sole author: Jesse Vincent (staff).

### obra/lace
Lightweight agentic coding environment.
- Five merged PRs, all internally ticket-tagged (PRI-29xx): pinning what
  bare model aliases/defaults mean in the catalog, sizing the preserved
  compaction tail to a model's real context window, letting an
  over-context-window session compact itself back out, marking which
  restart interrupted a job so the job list stays readable, and a lint-
  breaking unused-import cleanup.
- Sole author/merger: Jesse Vincent (staff, `obra`).

## Repos checked with zero in-window activity worth a footnote

`obra/superpowers` and `obra/remux` both passed the dormancy pre-filter
(recent `pushed_at`) but resolved to zero commits, zero merged PRs, and zero
releases once actually checked — correctly excluded, not a gap. (Last
week's `obra/superpowers` release, v6.3.0, was the prior window; nothing new
this week.)

## Fork-fix confirmation

No forks turned up any in-window activity this run to exercise the compare-
API path end to end (all fork hits in both orgs were zero-`ahead_by`
dormant forks, correctly reported as zero rather than inheriting upstream
history) — but the fix is confirmed present and used: `gather.py`'s fork
branch calls `GET .../compare/{parent}...{fork}` and only counts
`ahead_by` commits, fetching each one's stats via the GitHub per-commit
diff endpoint (never local `git log --numstat`), and separately, every
commit with parent-count != 1 (real merges and shallow-clone synthetic-root
grafts alike) has its LOC unconditionally replaced by that same GitHub
per-commit-diff call rather than trusted from local numstat. Both fixes are
live in the codebase as of this run's `git pull`, and zero repos this week
hit a `get_full_repo`/`compare` API error that would have forced the
zero-and-report fallback path (see `data/coverage-report-20260821.md`:
0 fetch/clone errors across both orgs).
