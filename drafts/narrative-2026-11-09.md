# Narrative brief — week of 2026-11-09 (cutoff-to-cutoff)

Grounded in `tools/gather.py --cutoff 2026-11-13T23:55:21Z` (prev-cutoff
auto-resolved from `src/data/weekly-stats.json["2026-11-02"]["cutoff"]` =
`2026-11-06T23:17:46Z`, confirmed automatic — matches `resolve_prev_cutoff()`
walking the file for the lexicographically-last key carrying a `cutoff`
field) on `main` at `8a6b2b9`, both orgs, fork-overcount fix and merge-LOC
fix both confirmed present in this checkout's `tools/gather.py` (verified by
reading the module docstring and the `n_parents != 1` / `fix_merge_commit_loc`
logic before running — see the "Gather confirmation" section below) +
`tools/gen_stats.py`'s extract, merged into `src/data/weekly-stats.json`.
Per-repo narrative detail below is from `repo-report` (one run per active
repo, window `2026-11-06T23:17:46Z` to `2026-11-13T23:55:22Z` — the `until`
bound nudged one second past the gather cutoff because `repo-report`'s
`until` is EXCLUSIVE and gather's cutoff is INCLUSIVE; this is a reporting
convenience only and changed no commit's bucket assignment, confirmed by
matching commit counts against `data/recon-cutoff-20261113.json` for every
repo). Reports saved under `/work/shipped-task-20261113/reports/` (not
committed — narrative source only, not repo content).

**This brief is number-free by instruction: no commit/PR/LOC counts are
quoted here.** Those render from the `WeekSummary`/`RepoStat` widgets off
`src/data/weekly-stats.json` once the post itself is drafted (not done in
this pass — steps 1-2 only, no `.mdx` authored, nothing deployed, nothing
posted).

## Window and label convention

**Window:** `(2026-11-06T23:17:46Z, 2026-11-13T23:55:21Z]` — exclusive
start, inclusive end. This is a **partial week**: the post's nominal
calendar bucket is Monday 2026-11-09 through Sunday 2026-11-15, but
(consistent with every cutoff-mode post since week-of-2026-10-26) the
actual data window ends at a **Friday-evening snapshot**, not Sunday
night. The cutoff landed this run at Friday 2026-11-13, 23:55 UTC — this
week's post, like the last two, will cover Monday through Friday evening
only, with Saturday/Sunday's activity (if any) rolling into next week's
`(this cutoff, next cutoff]` window. **Key/label: `2026-11-09`** (the
Monday of the calendar week containing the cutoff, per
`week_label_for_cutoff()`), matching the task's expectation.

## Gather confirmation (fork over-count + merge-LOC fixes)

Confirmed present in `tools/gather.py` before running, not assumed:

- **Fork over-count fix:** forks are counted only via GitHub's compare API
  (`ahead_by`/`commits` list), never via a naive `git log` on the fork's own
  default branch — see the module docstring's bug-2 writeup and
  `fork_ahead_by` plumbing. (Moot for this window's own repo set — none of
  the 11 active repos are forks, see Exclusions below — but the fix is in
  the checkout, not reverted.)
- **Merge-LOC/graft fix:** `n_parents != 1` (not just `> 1`) is distrusted
  for local numstat, covering both real merges and the shallow-clone graft
  case; `fix_merge_commit_loc()` is present and called from both the
  non-fork and fork-no-parent-fallback paths.
- Coverage: `data/coverage-report-20261113.md` — **clean**, zero fetch/clone
  errors across both orgs (64 `prime-radiant-inc` repos + 229 `obra` repos
  scanned; 11 repos with in-window activity, 7 + 4).

## Org roster check

Live `GET /orgs/prime-radiant-inc/members` this run returns `ada-sen`,
`arittr`, `cadence-sen`, `ketted`, `nora-primeradiant`, `obra`, `reeve-sen`,
`simonw` — same eight logins as every recent week's check, unchanged.

## Active repos this window (11)

| Repo | New repo? | Release this window? | Featured? |
|---|---|---|---|
| `prime-radiant-inc/evener` | no | yes — 7 patch tags, v0.3.24–v0.3.30 | **yes** |
| `prime-radiant-inc/external-sandbox-pi` | **yes** (created 2026-11-06T23:46:03Z, ~29 min after prev-cutoff — inside this window) | no | **yes** |
| `prime-radiant-inc/shepherd-pr` | no | no (two internal version bumps, 0.4.2→0.4.3, but no GitHub Release cut) | no |
| `prime-radiant-inc/external-sandbox` | no | no | no |
| `prime-radiant-inc/external-sandbox-v86` | no | no | no |
| `obra/lace` | no | no | no |
| `obra/winpepper` | no | no | no |
| `obra/private-journal-mcp` | no | no (one `commit_only_bump` to v2.0.2, no formal GitHub Release) | no |
| `obra/muse-skills` | no | no | no |
| `prime-radiant-inc/claude-plugin-stats` | no | no | no |
| `prime-radiant-inc/shipped` | no | no | no |

## Per-repo: what shipped (qualitative, from real commit/PR text)

### Featured

**`prime-radiant-inc/evener`** — seven patch releases (v0.3.24 through
v0.3.30) landing across the window. By theme, not count: a round of
hub/plugin-UI unification (one marketplace screen for installing plugins
and managing sources, plugin details expanding inline instead of a
slide-out sheet), a web/phone design convergence (one shared palette,
folding the resting composer to one line, a single pending-message stack
for undelivered messages, landscape support with safe-area insets on
native), voice-surface consolidation (one status line/action for voice),
agent-side reliability work (coordinating rate-limit storms across
sessions, waiting for quota instead of re-kicking failing turns, telling
callers how to recover a failed model provider, configurable context-
compaction thresholds), and a large tail of fixes/tests spanning agent,
web, hub, native, sandbox, execenv, and CI lanes. Primary author: Jesse
Vincent (`obra`). Four other identities touched this repo this window,
each a single or low-digit-commit contribution: `NopeCharon` (Asish),
`jay23606` (Jay), `mikemikimike`, and `dependabot[bot]` (routine dependency
bump) — none are `prime-radiant-inc` org members; all four classified
**outside**.

**`prime-radiant-inc/external-sandbox-pi`** — brand-new repo this window: a
Pi coding-agent extension that routes Pi's bash/read/write/edit/grep/find/
ls tools and `!` commands through an External Sandbox server over its
health/exec-websocket protocol, failing closed when the sandbox is
unavailable. Built for Pi 1.5; initial commit plus small follow-ups
(tightening an error-message's punctuation, adding/then trimming README
badges pending a first GitHub release). Sole author: Simon Willison
(`simonw`) — see **ASK JESSE** below; not classified here.

### Also shipped — full write-up

**`prime-radiant-inc/shepherd-pr`** — two merged PRs teaching the plugin to
end its own turn once CI is merely *running* rather than polling it to
completion (reading only the failed job's filtered log instead of pulling
multi-megabyte CI logs into context), plus a settle-detection fix that
stops treating a stale pre-push `CHANGES_REQUESTED` review decision as
still blocking, and that waits for required checks which haven't yet
reported instead of treating their absence as "settled." Internal version
bumped 0.4.2 → 0.4.3 inside those same commits, but no GitHub Release was
cut this window (so not featured, despite the version bump). Sole author:
Jesse Vincent (`obra`) — in-org.

**`prime-radiant-inc/external-sandbox`** — one commit: removing the
now-redundant `pi` folder from this repo now that it has its own
standalone `external-sandbox-pi` package. Pure repo-hygiene/reorg following
from the new-repo launch above. Sole author: Simon Willison (`simonw`) —
**ASK JESSE**, same open question as `external-sandbox-pi`.

**`prime-radiant-inc/external-sandbox-v86`** — two small commits: adding
README badges, then removing the changelog badge specifically pending an
actual GitHub release existing to link to. Sole author: Simon Willison
(`simonw`) — **ASK JESSE**.

**`obra/lace`** — continues building out an automatic/semantic memory-recall
subsystem: indexing and catch-up resuming from committed file offsets,
bounding recall to one indexed shortlist, scoring/ranking passes over full-
text-search pages, closing memory-index connections after each response,
avoiding double-loading of recall originals, and keeping the main thread
responsive during local embedding. Alongside that: reporting OpenAI's
cached-input-token usage correctly, compacting past a breakpoint after a
failed turn, reporting the model's context window on turn-end usage, and
adding Claude Sonnet 5.5 to the shared Anthropic model catalog. Primary
author: Jesse Vincent (`obra`, in-org); one commit from Drew Ritter
(`arittr`, also `prime-radiant-inc` org member — in-org).

**`obra/winpepper`** — one commit, a README trim (removing a "Try it
risk-free" section). Author: Dan Shapiro (`danshapiro`) — not a
`prime-radiant-inc` org member, personal account; classified **outside**.

**`obra/private-journal-mcp`** — a release-adjacent week: a fix so a failed
journal-entry embedding-index write is reported rather than silently
claimed successful, a test-suite portability fix for Windows, a
`.claude-plugin/plugin.json` addition for marketplace validation, a fix
that stops blocking the MCP `initialize` handshake on embedding warm-up,
and (merged same day) a v2.0.2 release bundling those fixes plus dependency
updates — tagged (`v2.0.2` @ `c70aecd0`) but **not** published as a formal
GitHub Release (hence not featured; tracked as a `commit_only_bump` in the
recon). **Attribution note:** the three fixes above were authored by
external contributors on their own branches and landed via merge commits;
because merges are excluded from gather.py's per-commit author counting
*and* their underlying branch commits predate this window (so they're not
separately walked), `repo-report`'s naive commit-author table shows only
the two people who did the merging (Ada Sen `ada-sen`, Jesse Vincent
`obra` — both in-org/staff). The real authors, read off the merged-PR
list, are: `AndrewSpell` (Windows test-suite fix, plus an earlier-PR
adaptation), `arimu1` (plugin manifest fix), and `hxzmn7f5dp-jpg`
(MCP-handshake fix) — none are `prime-radiant-inc` org members; all three
classified **outside**. Flagging this pattern for whoever authors the post:
credit the PR authors by login, not just whoever clicked merge.

### Also shipped — caveat-footnote only (no attributable human, or this
   blog's own tooling)

- **`prime-radiant-inc/claude-plugin-stats`** — all activity is
  `github-actions[bot]` chart-data rebuilds (`Rebuild chart data`, repeated).
  Same bot-only treatment as every recent week; not a person, not
  attributed.
- **`obra/muse-skills`** — all commits are dated `skills snapshot
  YYYY-MM-DD` entries under the `file-integrity` identity, which has no
  linked GitHub account (`repo-report` flags it UNRESOLVED, not silently
  guessed at). Same unconfirmed-automation treatment as recent weeks.
- **`prime-radiant-inc/shipped`** — this repo's own commits this window are
  Ada Sen drafting/fixing last week's post (week-of-2026-11-02) and its
  `simonw`-attribution correction, plus a test hardening commit. This
  blog's own tooling/authorship, not product work; footnote-only, same
  bucket as every recent week.

## Contributor attribution — resolved identities (by GitHub login)

| Identity (login) | Resolves to | Classification | Repo(s) this window |
|---|---|---|---|
| `obra` | Jesse Vincent | **in-org** (`prime-radiant-inc` member, staff) | evener, shepherd-pr, lace, private-journal-mcp (merge-author only) |
| `ada-sen` | Ada Sen | **in-org** (staff; owner) | shipped, private-journal-mcp |
| `arittr` | Drew Ritter | **in-org** (`prime-radiant-inc` member, staff) | lace |
| `simonw` | Simon Willison | **ASK JESSE** — see below, not guessed | external-sandbox-pi, external-sandbox, external-sandbox-v86 |
| `NopeCharon` | Asish | **outside** | evener |
| `jay23606` | Jay | **outside** | evener |
| `mikemikimike` | (no full name given) | **outside** | evener |
| `danshapiro` | Dan Shapiro | **outside** | winpepper |
| `AndrewSpell` | Andrew Spell | **outside** | private-journal-mcp |
| `arimu1` | (no full name given) | **outside** | private-journal-mcp |
| `hxzmn7f5dp-jpg` | (no full name given) | **outside** | private-journal-mcp |
| `dependabot[bot]` | — (bot) | not attributed to a person | evener |

`mhat` (former employee, staff only for his own employed weeks) does not
appear as a contributor anywhere this window — checked, no commits under
"mhat" or any variant identity, so his employment window never comes into
play.

## ASK JESSE

**`simonw` (Simon Willison).** He is, once again, the sole author across
all three `external-sandbox-*` repos active this window — including the
brand-new `external-sandbox-pi` launch. He is literally present in the
live `prime-radiant-inc` org-members roster (as every week this blog has
checked). Two conflicting signals exist in this blog's own history and
neither is being guessed from here:

1. **Long-standing precedent** (`drafts/narrative-2026-10-26.md`,
   `drafts/narrative-2026-10-19.md`, and others): classify him **outside**
   despite org membership, on the theory that org-membership here reflects
   repo-administration access, not employment — he authors 100% of the
   commits on the `external-sandbox-*` family under a personal `@gmail.com`
   address, with no other `prime-radiant-inc` commits anywhere in the
   blog's history under his login.
2. **Direct correction from Jesse** (`drafts/narrative-2026-11-02.md`,
   commit `8a6b2b9`): Jesse confirmed he is in-house/staff — but that
   correction was explicitly scoped by Ada's own instruction to **"this
   week only"** (week-of-2026-11-02), not asserted for any other week, and
   the correction note itself flagged that the old "outside despite being
   in the roster" precedent "should probably be revisited rather than
   assumed next time his login shows up."

This week is exactly "next time his login shows up." Per instruction not to
guess either way: **do not classify `simonw` as staff or outside for
week-of-2026-11-09 without asking Jesse directly** whether his in-house
status from the 11-02 week continues, lapsed, or was never meant to
generalize. This affects attribution on all three `external-sandbox-*`
repos, including whether the new `external-sandbox-pi` launch reads as an
in-house product launch or an outside contributor's repo hosted under the
org.

No other contributor is ambiguous this window — every other human commit
resolves to a clean GitHub login with an unambiguous classification (org
roster membership, or a personal non-org account with no other signal).

## Exclusions

**Nothing was hard-excluded this window.** Checked explicitly:

- **Forks:** none of the 11 active repos this window are forks (`fork:
  false` for all 11 in `data/recon-cutoff-20261113.json`) — so the
  fork-ahead-by logic never had anything to exclude here, and there are no
  dormant-fork "mirror" artifacts in this week's active set at all.
- **Bot-only / unresolved-identity repos:** `prime-radiant-inc/claude-
  plugin-stats` (github-actions[bot] only) and `obra/muse-skills`
  (unresolved `file-integrity` automation) are **not** dropped from the
  post — per this blog's existing, repeatedly-applied convention (see
  week-of-2026-11-02 and every week before it), they're kept in the active
  count and get caveat-footnote treatment only (no attributable human, no
  full write-up), not full exclusion.
- **This blog's own repo** (`prime-radiant-inc/shipped`) is likewise kept
  in, footnote-only, same as every recent week — it's "this blog's own
  tooling," not a mirror or a bot, just not product work.

## Build/test verification

`python3 -m pytest tools/ -v`: 36 passed, before and after this run (no
code changes to `tools/`, data-only change). No `npm run build` run this
pass — out of scope for steps 1-2 (no `.mdx` authored).

Not merged to main, not deployed, not pushed to `gh-pages`, nothing posted
anywhere.
