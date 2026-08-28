# Narrative brief — week of 2026-08-24 (through 2026-08-30)

Grounded in `data/recon-v2-1wk-20260828-CORRECTED.json` (fork-fix + merge-
commit-LOC-fix `gather.py` run, both orgs, week bucket 1, with two manual
corrections layered on top — see "Data-quality corrections this run" below)
+ `drafts/weekly-stats-2026-08-24.json` (WeekSummary/RepoStat-shaped extract,
via `tools/gen_stats.py`, staged — NOT merged into `src/data/weekly-stats.json`).
No numbers below — pure narrative themes; all figures render from the widgets.

**Window is PARTIAL.** Frozen snapshot: 2026-08-28T22:06:22Z (a Friday). The
calendar week runs 2026-08-24 through 2026-08-30 (Mon–Sun, same bucket
convention as every prior week); this data covers Monday through Friday
evening only. Say so in the post the way the last two Friday-snapshot posts
did.

**Contributor legend:** "staff" = `prime-radiant-inc` org member AT COMMIT
TIME. Current membership, confirmed live this run via
`GET /orgs/prime-radiant-inc/members`: `obra` (Jesse Vincent), `ada-sen`
(Ada Sen), `arittr` (Drew Ritter), `cadence-sen`, `kattni`, `ketted`,
`nora-primeradiant`, `renn-dray`, `simonw`. Every commit this week falls
inside the last five days, so current membership is a safe proxy for
"at commit time" here — no backfill lag to reconcile. Everyone else is
**outside**, confirmed via `GET /users/{login}` (name/company/bio) rather
than guessed. Automated/agent identities are called out separately, folded
into neither bucket. (`mhat` does not appear as a contributor anywhere this
week, so his former-staff/temporal case doesn't come up this time — noting
only because the brief brief asked me to watch for it.)

**ONE AMBIGUOUS CONTRIBUTOR THIS WEEK — flagging for Jesse, not guessing:**
`obra/toy-c-compiler`'s entire 212-commit week is authored (and committed)
under the git identity `C Compiler Builder <compiler@local>` — a brand-new
identity, never seen in this blog's data before. The `@local` email and the
complete absence of a matching GitHub account (no `login` resolves on any
of these commits) match the exact shape of `evener@local`, the established
coding-agent identity that authored part of `automatic-sshfs` last week —
so my working guess is that this is Jesse's own agent tooling working
unsupervised on a personal side project (the repo is on `obra`, has no
description, and every single commit this week is this one identity with
zero accompanying human commits — unlike `automatic-sshfs`, where `evener`
worked *alongside* Jesse's own commits, this repo has no human commit at
all to confirm who's driving). I have NOT labeled it staff, outside, or
"the evener tool" in what follows — it's written up under its own name.
**Please confirm with Jesse: is `C Compiler Builder` his own agent run, and
if so should it get the same "not an outside contributor, that's tooling"
treatment `evener` got — or is something else going on here?**

## FEATURED (new repo or tagged release)

### prime-radiant-inc/automatic-sshfs
Automatically mount remote filesystems over SSH on macOS via FUSE-T and
ControlMaster.
**FEATURED — tagged release (v0.2.0 — "reliable mounting + known_hosts +
symlinks").** Not a new repo this week (created the week before, per last
week's post); this week it's featured purely for the release.
- All four commits continue directly from last week's launch: symlinking
  hosts that share a control socket to one canonical mount, enumerating
  hosts straight from `known_hosts` for entries with no explicit config
  block, and a reliability pass on the polling/keepalive path (switching to
  `KeepAlive` + a watch daemon, fixing `StartInterval` polling, `PATH`
  handling, and `Setsid` so `sshfs` survives).
- All four commits are authored under the `evener` identity — same
  autonomous coding-agent tool covered last week (formerly `serf`), still
  working this repo without an accompanying human commit this particular
  week. Treat as tooling/dogfooding, not an outside contributor, consistent
  with last week's treatment.

### obra/winpepper
Windows-native local dictation — hold a hotkey, speak, release, get
cleaned-up words in the focused app; Parakeet TDT v3 ASR + LlamaSharp
cleanup, all local.
**FEATURED — three tagged releases (v0.7.2-alpha, v0.7.3-alpha,
v0.7.4-alpha).**
- A real feature week, not just packaging: launching the app automatically
  from the MSI installer's exit dialog (fixing a "no window ever appears"
  first-run dead end), pre-warming the WinRT OCR engine at app start,
  switching the default install to a minimal streaming-only footprint (the
  backup ASR model becomes fully opt-in), and, in the last release, making
  the backup ASR selection default to `None` outright so nothing downloads
  without an explicit gesture. A test-robustness thread runs alongside:
  deterministic test-owned-window reads for the real UIA/OCR gate facts,
  and widened scheduler-slippage margins for listen-start latency tests —
  plus one CI fix for flaky timing-sensitive tests on the GitHub-hosted
  runner.
- Every commit this week is **outside contributor `danshapiro`** (Dan
  Shapiro — CEO, Glowforge; not a `prime-radiant-inc` member, confirmed via
  GitHub profile and a 404 on org membership), committing under both
  `danshapiro` and `Dan Shapiro` identities. This remains a personal
  project of Jesse's (`obra`, not a fork) that an outside contributor is
  actively driving.

## ALSO-SHIPPED (rest — compact writeups, not omitted)

### prime-radiant-inc/evener
A coding agent: give it a prompt and it reads, writes, runs commands, and
searches code in a loop until the work is done, using native tool-calling
across OpenAI, Anthropic, and Google models.
- By far the highest-velocity repo this week, even without a release. Two
  visible threads: a REST-to-typed-AppWire migration sweeping session
  deletion/rename, project archive/favorites/deletion, navigation reads,
  the command palette, model catalog, git-HEAD lookups, and mobile pairing
  off ad-hoc REST endpoints and onto one typed transport, and a parallel
  cleanup removing the now-superseded REST surfaces (spawn, upgrade, tree
  validation, path validation) once each migration landed. Also: per-session
  vision-model configuration, inline slash-mention plugin exposure, a CI
  lint-lane split across runners, and a long tail of `fix(agent)`/
  `fix(web)` hardening (delegate-attention draining, interrupt-cleanup
  ownership, ask_user header leniency, provider-retry drain liveness).
- **The raw LOC total for this repo is misleading and should not be quoted
  as-is** — see "Data-quality corrections" below; the widget data has
  `loc_suppressed` set for this reason. Commit and merged-PR counts are
  unaffected and accurate.
- Contributors: Jesse Vincent (staff, `obra`) overwhelmingly. One outside
  contribution: **`WilliamK112`** (Ching Wei Kang — UW–Madison student,
  confirmed via GitHub profile; not an org member) landed PR #474, a fuzz-
  gap-closing test commit, merged by Jesse. Two commits from Ada Sen
  (staff) — one a release-download 404 error-message fix, one an
  `OLLAMA_HOST` normalization fix — under both her `ada-sen` and `Ada Sen`
  git identities (same person, same staff status either way).

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project.
- One continuous arc this week: a "kernel D2" provisioning + instrument-
  snapshot design that went through two competing spec revisions (a
  five-seat panel review absorbed into revision 2) before landing as a
  worktree-materializer module, itself hardened over four review rounds
  (SHA validation, symlink-safe lock reclamation, ownership-safe locking,
  loud failure reporting) and capped with attempt-scoped crash/seal-
  terminality fixes and a final multi-wave review pass (inventory-wide
  frontmatter validation, arm-harness compatibility, credential-diagnostic
  dedup). Also: a CLI projection for the superpowers-root flag, a runner-
  side threading of the superpowers spec through every provisioning check,
  and a capability-registry two-mode live-smoke test.
- Sole author: Drew Ritter (staff, `arittr`).

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
- Fully automated again this week — every commit is the daily scrape-and-
  rebuild job (`github-actions[bot]`), no human commits. Same caveat as
  the last time this repo showed up: worth the one-line mention for
  exhaustiveness, nothing more to say.

### obra/lace
Lightweight agentic coding environment.
- Six merged PRs, all internally ticket-tagged (PRI-29xx): a `file_find`
  fix for a bug that wedged a coworker session for 96 minutes (one
  container exec per entry), sizing the preserved compaction tail against
  the model's own self-reported context window instead of a guess, not
  spending a compaction breakpoint when compaction did nothing, putting
  the last-call input-context-token count on the usage wire, resolving
  personas through the session's own registry by name, and making persona
  failures loud with a bounded fallback and a progress postcondition.
- Sole author/merger: Jesse Vincent (staff, `obra`).

### obra/toy-c-compiler
No repo description set. From the commit log: a toy C compiler targeting
AArch64/ARM64 assembly output, with a self-contained IR optimizer.
- A single sustained optimization arc, entirely peephole/pattern-based:
  fixing several `movk`/`sxtb`/`sxth`/floating-point-register parsing bugs
  in the assembler, then layering on optimization pass after pass — self-
  add-chain folding, dead sign-extension elimination (`sxtw`/`sxtb`/`sxth`/
  `uxtb`/`uxth` of a known-zero value), redundant stack-pointer-restore
  elimination, load/store-pair coalescing (`str`+`str`→`stp`), mov-store
  fusion, and load-target folding — each tracked against a running
  optimization notebook logging instruction-count reduction percentages
  (documented in-repo reaching ~12%+ over the course of the week).
- Author: see the ambiguous-contributor flag at the top of this brief —
  written up here under its own commit identity, `C Compiler Builder`,
  pending Jesse's confirmation of who/what that is.

## Repos checked with zero in-window activity worth a footnote

None beyond the routine dormancy pre-filter this week — no repo that
looked plausibly active on a `pushed_at` check resolved to zero once
actually walked. (Contrast with last week's `obra/superpowers` and
`obra/remux`, which did.)

## Fork-fix confirmation

136 forks scanned across both orgs this run; every single one reported
`fork_ahead_by` either `0` or was correctly skipped as dormant (`created_at`
and `pushed_at` both outside the window) — none inherited upstream history
into this week's counts. No fork actually had in-window activity to exercise
the compare-API path end to end this particular week (contrast with prior
weeks), but the mechanism itself is confirmed present and unchanged:
`gather.py`'s fork branch calls `GET .../compare/{parent}...{fork}` and
counts only `ahead_by` commits (each fetched via the GitHub per-commit-diff
endpoint, never local `git log --numstat`), and separately, every commit
with parent-count != 1 has its LOC unconditionally replaced by that same
per-commit-diff call. Zero repos hit a `get_full_repo`/`compare` API error
this run that would have forced the zero-and-report fallback path (see
`data/coverage-report-20260828.md`).

## Data-quality corrections this run (read before authoring)

Two issues surfaced during gather that are NOT in `tools/gather.py`'s
established, already-fixed bug list (fork over-count, merge-commit LOC
grafting) — flagging both so they don't get silently re-introduced or
silently trusted:

1. **`obra/winpepper` undercounted by one commit.** `gather.py`'s
   `clone_shallow()` still passes `--single-branch` to `git clone`. That
   drops the non-first-parent ancestry of any REAL (non-squash) merge —
   exactly "BUG 2" documented in `tools/verify_ground_truth.py`'s docstring
   for the 2026-08-14 dataset, which was fixed there but never patched back
   into `gather.py`'s default path. Concretely: the merge commit "Merge
   fix/msi-launch-on-finish" brought in one feature-branch commit
   (`d86b48da`, danshapiro, +24/-0) that the shallow single-branch clone
   never fetched at all. Caught by cross-checking gather.py's per-repo
   output against a full `GET /repos/{repo}/commits?since=&until=` listing
   for every one of this week's 7 active repos (cheap at this volume); only
   winpepper showed a gap. I added the missing commit back by hand into
   `data/recon-v2-1wk-20260828-CORRECTED.json` before running
   `gen_stats.py` — the numbers in `drafts/weekly-stats-2026-08-24.json`
   already include it (16 commits, not 15; +24 LOC). **Recommend: patch
   `clone_shallow()` to drop `--single-branch` so this stops needing a
   manual per-week spot-check.**
2. **`prime-radiant-inc/evener` LOC is real-but-misleading, not
   fabricated.** This week's raw +748,646/-135,032 is dominated by large
   delegate-branch integration merges ("Merge commit `<sha>` into
   `dlg_034...`", "into `HEAD`") plus one 52,696-line self-test-coverage
   commit — reintegration diffs, not net-new authored lines. This exact
   shape (this repo, under its prior name `serf`) got `loc_suppressed:
   true` in three previous published weeks (2026-02-09, 2026-03-16,
   2026-04-13 — see `src/data/weekly-stats.json`). I set
   `loc_suppressed: true` on evener's cell in
   `drafts/weekly-stats-2026-08-24.json` to match that precedent; commit
   count (773) and merged-PR count (142) are untouched and accurate — only
   the LOC figure is suppressed. **This is a judgment call, not an
   automated one** (the flag is hand-set in the recon JSON before
   `gen_stats.py` runs, same as every prior instance) — please sanity-check
   before publishing.
3. **Minor, cosmetic:** `drafts/weekly-stats-2026-08-24.json`'s
   `summary.commit_only_bumps` is `3`, all three from `obra/winpepper`
   (`release: 0.7.4-alpha`, `release: 0.7.3-alpha`,
   `chore(release): bump version to 0.7.2-alpha`). These are NOT extra,
   untagged version bumps distinct from winpepper's three tagged releases
   — they're the very commits that produced those three tags. The
   classifier regex in `tools/gen_stats.py`/`tools/make_briefs_corrected.py`
   strips a bare `\d+\.\d+\.\d+` version out of the commit subject and
   checks it against the release-tag set verbatim, but the tags themselves
   carry a `-alpha` suffix (`v0.7.2-alpha`) that the extracted version
   (`0.7.2`) never matches — so every prerelease-tagged repo's own release
   commits will always misfire as "commit-only bumps" under the current
   regex. Not something to fix in this gather pass, but don't let the post
   imply winpepper had 3 *additional* unlisted version bumps on top of its
   3 releases — it didn't.
