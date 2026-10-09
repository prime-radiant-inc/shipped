# Narrative brief — week of 2026-10-05 (through 2026-10-09 evening)

Grounded in a fresh `tools/gather.py --weeks 1 --window-end 2026-10-09T22:36:19Z`
run (both orgs, origin/main's already-committed `gather.py` — the
fork-inherited-history compare-API fix is confirmed in effect, see below; no
cherry-pick needed) + manual `gh api` spot-checks for PR authorship/base-branch
(`gather.py`'s merged-PR count doesn't carry an author field, and doesn't
filter by base branch — see the `obra/superpowers` note below). No numbers
in this brief — pure narrative; all figures render from the widgets / come
from `src/data/weekly-stats.json`.

**Window is PARTIAL.** Frozen snapshot: 2026-10-09T22:36:19Z (today, Friday
evening). The calendar week runs 2026-10-05 through 2026-10-11 (Mon–Sun);
this data covers Monday through Friday evening only, two days short of the
full week — same pattern as the last several Friday-snapshot posts.

**No gap week.** The newest post live on `gh-pages` (and present on
`origin/main`, confirmed against the live site at primeradiant.com/shipped/
— 41 posts, newest first) is `week-of-2026-09-28.mdx`. This week
(2026-10-05) is the very next calendar week; no missed week in between, and
no gap between it and the full Mon-anchored run back to 2025-12-22 either
(all 41 weeks present, none in draft).

**Fork over-count fix: CONFIRMED in effect.** Read `tools/gather.py` on
`main` directly: `process_repo()` branches on `is_fork`, and for a fork with
resolvable parent info calls the compare API
(`get_compare` → `repos/{owner}/{repo}/compare/{parentOwner}:{branch}...{owner}:{branch}`)
and counts only `cmp_data["commits"]` within the window — never a raw
`git log` of the fork's own default branch, which for a fork is upstream's
history. The no-parent fallback also only does the unfiltered clone/log
path for a *confirmed* missing parent, not any `get_full_repo` error
(`c091ceb`'s fix). Live spot-check against the fix's own worked example,
`obra/freshell` (forked from `danshapiro/freshell`): `pushed_at` and
`created_at` are both 2026-07-18, both well before this window, so it's
correctly caught by the dormancy pre-filter and never even reaches the
compare-API path — consistent with "created and never touched again."
Separately: of the 283 repos scanned this run, zero forks had any in-window
commits, so the compare-API path itself wasn't exercised live this week —
but the code is unambiguously present and matches the documented fix.

**Coverage:** 283 repos scanned (55 `prime-radiant-inc`, 228 `obra`), zero
fetch/clone errors, 10 repos with in-window activity.

**Roster note (not a content fact, flagging for Ada):** live
`GET /orgs/prime-radiant-inc/members` this run returns `ada-sen`, `arittr`,
`cadence-sen`, `ketted`, `nora-primeradiant`, `obra`, `reeve-sen`,
`simonw` — eight names. The 2026-09-28 post's roster (just last week) also
listed `kattni`. `kattni` has no commits or PRs anywhere in this window, so
it doesn't change any classification below, but the membership list itself
shrank by one name since last week's check — worth confirming with Ada
whether that's an intentional departure or a token-scope/visibility
artifact, independent of this week's post.

**One new repo this week:** `obra/morning-routine-board`, created
2026-10-09 (today, mid-window) — a personal project (a chore-checklist PWA
for two kids on a wall-mounted iPad), not a company product, but it meets
the same "new repo" featured trigger as anything else under the `obra`
account per this blog's remit.

**Two tagged releases this week:**
- `prime-radiant-inc/evener` v0.3.7 (bare version-number release, no further
  release-note text — same pattern as prior evener releases).
- `obra/superpowers-chrome` v3.0.11 — real release-note text: "Default
  redaction for secrets present at page load; known-sensitive URLs
  suppressed outright."

**Contributor legend:** "staff" = `prime-radiant-inc` org member AT COMMIT
TIME. Every commit/PR this week falls inside the last five days, so current
membership (confirmed live this run, see roster note above) is a safe
proxy for "at commit time." Everyone who shipped anything this week —
`obra` (Jesse Vincent), `ada-sen` (Ada Sen), `reeve-sen`, and `arittr`
(merged one PR, didn't author it) — is a current org member. **No outside
human contributor landed or merged anything this window.** That is itself
notable: this is an all-internal week, a contrast with recent weeks that
usually had at least one outside PR in flight.

**One UNRESOLVED identity, continuing from last week — flagging for Jesse,
not guessing:** `obra/muse-skills`'s entire five-commit week is again
authored under the git identity `file-integrity <file-integrity@local>`
(no GitHub account — `login` is null, same as last week's check). Same
daily-cadence, mechanical-subject shape ("skills snapshot 2026-10-05"
through "...-10-09") as last week's unresolved finding. Carrying the same
open question forward: **please confirm with Jesse whether `file-integrity`
is his own automation and gets the "tooling, not an outside contributor"
treatment.**

One more automated identity, unambiguous: `github-actions[bot]` drives all
of `prime-radiant-inc/claude-plugin-stats`'s activity this week (the daily
install-stats scrape and chart rebuild) — no human commits there.

**Data-quality footnote (LOC provenance, muse-skills):** one of the five
daily snapshot commits (2026-10-07) removed roughly 20x the lines any other
day in the window touched — a bulk prune, not incremental hand-authored
work. Treat muse-skills' LOC figure as "size of a periodic bulk snapshot,"
the same caution as last week and the skill notes' standing guidance on
bot/regen-style commits.

**Data-integrity footnote (merged-PR base-branch gap in `gather.py`, not a
content fact — flagging for whoever next touches the tool):**
`obra/superpowers` shows 0 in-window commits but 4 "merged PRs" in the raw
recon JSON. Checked each PR directly (`gh api .../pulls/{n}`): all four
merged into `dev`, not `main` (the repo's default branch) —
`get_merged_prs()` in `gather.py` has no base-branch filter at all, so it
surfaces PRs merged to *any* branch, while the commit/LOC counting path
only ever looks at the default branch. For `superpowers` specifically this
is a known, intentional repo workflow (per its own commit history: `dev`
accumulates PRs between periodic "Release vX.Y.Z" commits that squash-merge
into `main`) — nothing merged to `main` this week, so nothing from
`superpowers` actually shipped to users this window, even though the raw
data has a nonzero "merged PRs" count. Treated below as NOT shipped/not
featured, written up only in this footnote. This is a gap worth closing in
`gather.py` itself (filter `get_merged_prs` to `base.ref == default_branch`)
but that's tooling work, out of scope for this brief.

## FEATURED (new repo or tagged release)

### prime-radiant-inc/evener
A coding agent: give it a prompt and it reads, writes, runs commands, and
searches code in a loop until the work is done, using native tool-calling
across OpenAI, Anthropic, and Google models.
**FEATURED — tagged release v0.3.7.** By far the week's highest-volume
repo, entirely the work of Jesse Vincent (`obra`) — every commit and every
merged PR this week carries his name, no other author appears. The PRs
cluster into a few clear threads:
- A **generated memory index**, built out end-to-end this week as a
  numbered series (through its final "8/8" review-fixes PR): memory pages
  now project a generated index from page frontmatter instead of relying on
  a hand-written one, with overflow handling, a projected-size cap, and the
  index gated on whether the pointed-to skill is actually loadable.
- A **notification-semantics cleanup**, also a completed short series: a
  reply is only treated as "needs your reply" when it reads like an actual
  question, a plain reply no longer notifies, and a "needs response" state
  now waits out a quiet period before resting, rather than firing
  immediately.
- A **delegate reply-threading fix cluster** (several PRs referencing the
  same tracking issue): a `delegate_send` reply or wait can now carry
  earlier queued results instead of losing them, delegate updates route to
  each live ancestor subagent's own thread, and a nested stable delegate is
  correctly attributed to its parent delegate's session rather than a
  sibling's.
- A broad **native test-hardening pass**: a long tail of `test(native)`
  commits wrapping previously-unwrapped synchronous store/controller
  updates in `act()` across many screens and suites (hub settings, queue
  sheet, model picker, new-session sheet, projects screen, and others) —
  infrastructure cleanup rather than a user-facing feature, but a
  substantial share of the week's commit volume.
- Smaller, continuing threads: dropping the Board's manual "mark as
  read"/"mark as unread" controls now that read-state tracks automatically
  on the phone, a fix for reading a `SKILL.md` missing its opening
  frontmatter delimiter, and further iPhone-redesign spec cleanup
  (dropping now-shared artifacts from the written spec).
- One tagged release, v0.3.7 — a bare version-number release with no
  further release-note text attached, same as prior evener releases.

### obra/superpowers-chrome
Claude Code plugin for direct Chrome browser control via DevTools Protocol
— zero dependencies.
**FEATURED — tagged release v3.0.11.** Sole author of this window's one
commit: Ada Sen (staff, `ada-sen`).
- A real security fix, with release notes to match: secrets present at
  page *load* time — a hidden `#init_key_code` field, and known-sensitive
  URLs — were not being redacted by default the way secrets revealed
  later in a session were; now both are suppressed outright rather than
  relying only on later-triggered capture logic. Substantial accompanying
  test coverage landed in the same commit (new tests for the credential
  guard, the HTML-scrub page script, the secret-pattern matcher, and the
  sensitive-URL matcher) — checked the file-level diff directly; this is
  real new library and test code, not a vendored or generated dump
  inflating the LOC count.
- Several other PRs remain open against this repo but did not merge this
  window, including two from Ada Sen and others from outside contributors
  (e.g. `sophieow`'s standing `CHROME_WS_HEADLESS` addition, still open)
  — not counted as shipped since nothing of theirs merged this window.

### obra/morning-routine-board
Morning routine checklist for two kids on a wall-mounted iPad.
**FEATURED — new repo, created this week (2026-10-09, today).** A personal
project, not a company product, but public and under the `obra` account,
so it meets this blog's own inclusion bar. Built essentially start-to-
(mostly)-finish today: a config model for kids and tasks, a localStorage-
backed store for config and daily check-offs, day-boundary logic for when
the board resets, a board view-model and screen with a daily reset, a
hidden settings screen behind a long-press gesture, offline support via a
service worker plus Home Screen metadata, a README with iPad setup and
deploy notes, and a same-day review-findings fix (single service-worker
registration, a storage-access guard, and a Safari 12 settings-launch
fix). Sole author: Jesse Vincent (staff, `obra`). No PRs (committed
directly), no releases.

## ALSO SHIPPED

### prime-radiant-inc/terminal-bench-analysis
Fetches detailed JSON results from the Terminal Bench 2 leaderboard, loads
them into SQLite, and publishes queryable analysis via Datasette.
One merged PR: serving Datasette Lite from the project root (via a
`codex/`-prefixed branch — an agent-assisted change, authored and merged
by Jesse Vincent).
- Sole contributor: Jesse Vincent (staff, `obra`).

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
Routine: five days of scheduled "Update plugin stats" + "Rebuild chart
data" commit pairs, one per day in-window (10/5 through 10/9).
- Sole committer: `github-actions[bot]` (automated — no human contributor
  this week).

### prime-radiant-inc/everyharness
Generate a coding-agent plugin for every harness from one config file.
One merged PR: wiring npm publish on `v*` tags via OIDC trusted publishing
(a CI/release-plumbing change, not a product feature).
- Sole contributor: Jesse Vincent (staff, `obra`).

### obra/claude-session-driver
Launch, control, and monitor other Claude Code sessions as workers via
tmux.
One merged PR: a launch fix so the trust dialog is accepted correctly even
when it defaults to "No, exit."
- Sole contributor: Jesse Vincent (staff, `obra`).

### obra/lace
Lightweight agentic coding environment.
A smaller week than usual: a new `glm-5.3-vision`/`glm-5.3-vision-
background` pair added to the LunaRoute model catalog, an MCP fix so an
incomplete MCP discovery no longer gets cached as the final tool list, a
projection fix to stop warning on an intentional persona re-render inside a
compaction era, and a new RPC (`session/rerender_persona`) to re-render a
session's frozen prompt without a full compaction.
- Contributors: **Jesse Vincent (staff, `obra`)** — three PRs — and
  **reeve-sen (staff)** — one PR (the LunaRoute catalog addition).

### obra/superpowers
An agentic skills framework & software development methodology that works.
**Not counted as shipped this window** — see the data-integrity footnote
above. Four PRs merged this week, but all four into the `dev` branch, not
`main`; nothing landed on the default branch, and no release was cut.
Author/merger breakdown for the record only, since nothing here actually
shipped: PR authors were Ada Sen (staff) and Jesse Vincent (staff);
merged by Jesse Vincent (staff) and Drew Ritter/`arittr` (staff).

## Repos checked with zero in-window activity worth a footnote

Nothing beyond the routine dormancy pre-filter — of the 283 repos scanned
(55 `prime-radiant-inc`, 228 `obra`), 272 were provably dormant
(`created_at` and `pushed_at` both before window start) and correctly
skipped, and the remaining checked-but-inactive repos (including
`agentic-usage-meter`, featured just last week) show no commit, merged PR,
or release in this window.

## Ambiguous contributors — ASK JESSE, not resolved here

- **`file-integrity <file-integrity@local>`** (`obra/muse-skills`, all five
  commits this week). No linked GitHub account; can't be placed in either
  the staff or outside bucket because there's no account to look up, not
  because it's genuinely ambiguous between the two. Same open question as
  last week's post, now two weeks running — worth a definitive answer:
  is this Jesse's own daily automation?

No other contributor this week is ambiguous — every named human identity
(`obra`/Jesse Vincent, `ada-sen`/Ada Sen, `reeve-sen`, `arittr`/Drew Ritter)
resolved cleanly to a current `prime-radiant-inc` org member via GitHub
login, and no outside human landed or merged anything this window.

## Structured stat data

Generated this run: `data/recon-v2-1wk-20261009.json` (raw recon),
`data/coverage-report-20261009.md` (coverage summary), and the new
`2026-10-05` key merged into `src/data/weekly-stats.json` (diffed
byte-for-byte identical against `main` for every other week before this one
was added) — the source for every number that would render in the actual
post via `WeekSummary`/`RepoStat`.
