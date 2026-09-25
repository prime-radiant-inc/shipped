# Narrative brief — week of 2026-09-21 (through 2026-09-27)

Grounded in `data/recon-v2-1wk-20260925.json` (single-week gather.py run,
`--weeks 1 --window-end 2026-09-25T22:19:28Z`, both orgs, COMMITTED
`tools/gather.py` — i.e. WITHOUT the uncommitted author/committer-date-basis
diff; see "gather.py basis note" below) + `src/data/weekly-stats.json`'s
`2026-09-21` key (via `tools/gen_stats.py`, merged in — the only key
touched; every other week's entry diffed byte-identical against `main`
before merging). No numbers below — pure narrative themes; all figures
render from the widgets / come from the stats JSON.

**Window is PARTIAL — same pattern as the last two posts.** Frozen
snapshot: 2026-09-25T22:19:28Z (a Friday evening). The calendar week runs
2026-09-21 through 2026-09-27 (Mon–Sun); this data covers Monday through
Friday evening only, two days short of the full week. Say so in the post
the way week-of-2026-09-07 and week-of-2026-09-14 did — `pubDate` should
land on this Friday (2026-09-25), matching the established convention:
**the blog posts on the Friday of the week it covers, with partial
Mon–Fri data, not after the week closes.** Evidence for that convention,
gathered from the two prior posts' own frontmatter and prose:
- `week-of-2026-09-14.mdx`: `dateStart: 2026-09-14`, `dateEnd: 2026-09-20`,
  `pubDate: 2026-09-18` (a Friday, mid-week) — body text: "Partial week —
  data runs through Friday evening, not the full calendar week" and "This
  week is still open: the data below runs through Friday evening, not the
  full calendar week."
- `week-of-2026-09-07.mdx`: `dateStart: 2026-09-07`, `dateEnd: 2026-09-13`,
  `pubDate: 2026-09-11` (also that week's Friday) — but this one was
  actually deployed to `gh-pages` on 2026-09-21 (see `gh-pages` commit
  `0a50419`), well after its own week closed — a backfill catch-up
  following the GitHub outage around 9/11, with `pubDate` set to what it
  *would* have been under the normal cadence, not the actual (late) publish
  date.

So: this is the same shape as 09-14, done on schedule. No need to wait for
the week to close.

**gather.py basis note:** this run used `main`'s committed `tools/gather.py`
only — the uncommitted author/committer-date-basis fix (bug 4: `%aI` vs
`%cI`) was deliberately NOT applied. That fix has been moved to branch
`fix/gather-committer-date` (pushed, not merged) per this week's
instructions, since changing the counting basis is a separate decision
from this week's data. The already-committed fork-inherited-history fix
(compare-API `ahead_by`) IS in this run, same as always. One consequence
worth flagging: `week-of-2026-09-07.mdx` and `week-of-2026-09-14.mdx` were
gathered WITH the bug-4 diff applied (see their narrative briefs), so this
week's commit counts are not on a guaranteed-identical basis to the
immediately preceding two weeks — a boundary commit landing right at a
week edge could count differently. No evidence this actually bit anything
this week (no repo showed a "clock skew?" note in the coverage report),
but noting the inconsistency rather than silently smoothing over it.

**Coverage:** 281 repos scanned (55 `prime-radiant-inc`, 226 `obra`), zero
fetch/clone errors, 9 repos with in-window activity. Full detail in
`data/coverage-report-20260925.md`.

**No new repos this week.** No repo's `created_at` falls in
2026-09-21–2026-09-27.

**Three tagged releases, all from `obra`:**
- `obra/blogosphere` v0.1.0 (2026-09-24) — its first tagged release ever.
- `obra/superpowers-chrome` v3.0.6 (2026-09-23).
- `obra/superpowers` v6.4.2 (2026-09-25 — today, this same Friday).

**Contributor legend:** "staff" = `prime-radiant-inc` org member AT COMMIT
TIME. Current membership, confirmed live this run via `GET
/orgs/prime-radiant-inc/members`: `ada-sen` (Ada Sen), `arittr` (Drew
Ritter), `cadence-sen`, `kattni` (Kattni), `ketted`, `nora-primeradiant`,
`obra` (Jesse Vincent), `reeve-sen`, `simonw`.

**Roster change since the last confirmed snapshot (09-07/09-14 posts):**
`renn-dray` is no longer in the member list; `reeve-sen` appears in its
place. I did not investigate further (rename vs. departure+new-hire vs.
something else) — neither login has any commit in this week's active
repos, so it doesn't affect this week's classification, but it's a
roster diff worth someone confirming before it matters for a future week.

**ALL FIVE distinct commit-author name-strings this week resolved to FOUR
real identities, cleanly classified — but one required a real check, not
an assumption:**
- **Jesse Vincent → `obra`** (staff) — confirmed via
  `GET /repos/prime-radiant-inc/evener/commits/4e2515a9`. Authors the large
  majority of everything this week: `evener`, `blogosphere`, `lace`,
  `scan-to-model`, `superpowers`, `superpowers-chrome`.
- **Ada Sen / `ada-sen`** (staff — same person, two different
  commit-author-name spellings across repos) — confirmed via
  `GET /repos/prime-radiant-inc/shipped/commits/3f6add8` (name "Ada Sen")
  and `GET /repos/obra/lace/commits/aaa15b0` (name "ada-sen"). Contributes
  to `terminal-bench-analysis`, `shipped`, and one commit on `lace`.
- **`github-actions[bot]`** — automated, folded into neither bucket. Sole
  committer pattern on `claude-plugin-stats` (10 commits, all
  "Update plugin stats <date>" / "Rebuild chart data" — routine scheduled
  scrape output for that repo, consistent with every prior week it's
  appeared; not flagging as a LOC leak, since the magnitude here
  (+2735/-2327) is within its normal historical range, well under weeks
  like 08-10's +15364/-11596 for the same repo).
- **"Jesse" → `jtdaugh` (OUTSIDE — NOT `obra`/Jesse Vincent, despite the
  matching first name).** Five commits on `prime-radiant-inc/evener`
  (macOS code-signing/notarization CI work: importing a Developer ID
  identity, matching the configured signing identity, signing and
  notarizing release artifacts, plus two merge commits). Commit-author
  email is `jesse@Jesses-MacBook-Pro.local`, distinct from Jesse Vincent's
  `jesse@primeradiant.com`. Confirmed via
  `GET /repos/prime-radiant-inc/evener/commits/6069514e` (and all four
  other shas individually — `baf448ef`, `303ec948`, `a0a9a7ce`,
  `71285979` — all resolve to the same `jtdaugh` login, so this isn't a
  one-off git-config fluke). `jtdaugh` is not in the org member list above
  → outside contributor. **This is a name-collision trap:** a naive
  match on "Jesse" would have folded this into Jesse Vincent's staff work;
  don't do that. First appearance of this login anywhere in the repo's
  history (checked: no prior narrative or stats file mentions `jtdaugh`).

**Data-quality note, consistent with the last two weeks:** `obra/superpowers`
shows only 1 local commit despite 4 merged PRs this week — the release
merge commit itself. Same dev-branch-vs-main visibility gap flagged in the
09-07 and 09-14 briefs: most of its work still lands on `dev`, and the
local clone only walks the default branch. Merged-PR titles are the
reliable signal for this repo, not the commit count.

## FEATURED (3 repos, all for tagged releases — no new repo this week)

### obra/blogosphere
Local-first, multi-platform blogging client for an 11ty blog that lives in
a GitHub repo — the repo is the database.
**Featured — its first-ever tagged release, v0.1.0, this week.** A packed
week behind it: a signed, notarized, universal macOS release workflow
built from scratch (Developer ID signing, `.dmg` stapling/verification,
pinned actions, tag-gated so only checked commits on `main` release), a
rotated Apple app-specific password propagated to every notarizing repo
and org secret, a nightly fuzz-timeout fix for async property tests, and a
string of UI polish items (activity-popover arrow positioning, syntax
colors that respect accent-independent readable blue, draft/publish
toolbar copy, markdown line alignment).
- Sole author: **Jesse Vincent (staff, `obra`)**.

### obra/superpowers
An agentic skills framework & software development methodology.
**Featured — tagged release v6.4.2 this week**, "leaner plans from
writing-plans": a rewrite of the `writing-plans` skill's philosophy (a
plan is decisions, not a transcript — a step recipe, a proportion check, a
capable-reader assumption) behind the version bump. Locally invisible
below the release/version-bump/notes commits — see the dev-branch data
note above.
- By merged PR (not commit): sole author **Jesse Vincent (staff, `obra`)**.

### obra/superpowers-chrome
Claude Code plugin for direct Chrome browser control via DevTools
Protocol — zero dependencies.
**Featured — tagged release v3.0.6 this week**, "Secret-safe auto-capture":
a fix so the plugin never auto-captures or echoes credential-shaped page
content.
- Sole author: **Jesse Vincent (staff, `obra`)**.

## ALSO-SHIPPED

### prime-radiant-inc/evener
A coding agent: give it a prompt and it reads, writes, runs commands, and
searches code in a loop until the work is done, using native tool-calling
across OpenAI, Anthropic, and Google models.
Its busiest repo of the week by commit count, in a partial (Mon–Fri) window:
deep native/web refactor work (a pending-turn commit feed and stall
tripwire moved into the shared package, a mutation-projection fence
unified across web and native, idle-release members torn down in bounded
depth waves), a run of test-suite modernization (dropping fake-toolchain
and npm-shim tests, porting web/browser gates to Go), and fixes to raw-arg
display, doctor audit-selector collisions, and legacy-named project-bucket
lookup. Separately: macOS release-signing infrastructure work — importing
a Developer ID identity, matching the configured signing identity, and
signing/notarizing release artifacts.
- Contributors: **Jesse Vincent (staff, `obra`)** — nearly all of it — plus
  **`jtdaugh` (outside)**, who did the signing/notarization CI work. See
  the name-collision note above: `jtdaugh` is a different person from
  Jesse Vincent despite sharing a first name in the commit log.

### prime-radiant-inc/terminal-bench-analysis
Fetches detailed JSON results from the Terminal Bench 2 leaderboard, loads
them into SQLite, and publishes queryable analysis via Datasette.
One security fix: a leaked Claude OAuth token redacted from a committed
`result.json`, plus hardening of `fetch_data.py` against the same class of
leak recurring (PRI-3130), landed via a `github-actions[bot]`
scheduled-fetch commit and a human follow-up fix.
- Contributors: **Ada Sen (staff, `ada-sen`)**, plus one
  `github-actions[bot]` scheduled-fetch commit (automated, not counted as
  a contributor).

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
Routine: five days of scheduled "Update plugin stats" + "Rebuild chart
data" commit pairs, one per day in-window (9/21 through 9/25).
- Sole committer: `github-actions[bot]` (automated — no human contributor
  this week).

### prime-radiant-inc/shipped
A weekly log of what Prime Radiant and obra shipped (this repo).
Merged the weeks-of-09-07-and-09-14 posts (draft → un-gated), plus the
outside-contribution-count/attribution corrections that followed.
- Sole author: **Ada Sen (staff, `ada-sen`)**.

### obra/lace
Lightweight agentic coding environment.
A provider/catalog-heavy week: LunaRoute catalog limits fixed and max
output fit to the context window, `claude-opus-5-5` added to the static
Anthropic catalog, Responses-API tool-output ordering and stateless
coverage fixed, a finished delegate's container now releases properly on
`job_kill`, persona `connectionId` frontmatter and a `query()` connection
override added, and a `deepseek-4.1-flash-background` catalog entry added.
- Contributors: **Jesse Vincent (staff, `obra`)** — the large majority —
  and **Ada Sen (staff, `ada-sen`)** — one commit.

### obra/scan-to-model
Evidence-driven scan reconstruction skills and local tools for Codex and
Blender (new two weeks ago).
Continued build-out: recognizable room features reviewed against source
photographs, extracted captures accepted through an intake command,
reconstructions grounded in coverage with full deliveries preserved,
source tracking simplified to preserved originals and source IDs, and
packed native/still-tour/offline-viewer delivery formats added.
- Sole author: **Jesse Vincent (staff, `obra`)**.

## Repos checked with zero in-window activity worth a footnote

Nothing beyond the routine dormancy pre-filter this week — no repo that
was active in either of the last two posts (study-skills, shepherd-pr,
clearance, prime-radiant-marketplace, awesome-superpowers,
alltheagents.org, teststrip, agentic-usage-meter, github-triage, gauntlet,
superpowers-evals, episodic-memory) shows any commit, merged PR, or
release in this window. Not investigated further beyond the standard
dormancy check (created_at/pushed_at both before window start).

## Structured stat data

The `2026-09-21` key merged into `src/data/weekly-stats.json` (diffed
byte-for-byte identical against `main` for every other week before this
one was added) is the source for every number above.
