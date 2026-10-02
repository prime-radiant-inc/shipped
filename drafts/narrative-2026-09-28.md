# Narrative brief — week of 2026-09-28 (through 2026-10-04)

Grounded in a fresh `tools/gather.py --weeks 1` run (both orgs, origin/main's
already-committed `gather.py` — the fork-inherited-history compare-API fix
and the author/committer-date-basis fix are both already merged into
`main`, so no cherry-pick was needed this time, unlike the last two posts)
+ `tools/gen_stats.py`'s extract, merged into `src/data/weekly-stats.json`
as the single new `2026-09-28` key (every other week diffed byte-identical
against `main` before merging — pure addition, confirmed via `git diff
--stat`: insertions only, zero deletions outside the new key) + six
per-repo `repo-report` runs (one per active repo) for full commit messages,
PR bodies, and release text. No numbers below — pure narrative themes; all
figures render from the widgets / come from the stats JSON.

**Window is PARTIAL — same Friday-snapshot pattern as the last several
posts.** Frozen snapshot: 2026-10-02T22:20:09Z (today, Friday evening). The
calendar week runs 2026-09-28 through 2026-10-04 (Mon–Sun); this data covers
Monday through Friday evening only, two days short of the full week. Say so
in the post the way the last several Friday-snapshot posts did —
`pubDate` should land on this Friday (2026-10-02).

**No gap week.** The newest post live on `gh-pages` (and present on
`origin/main`) is `week-of-2026-09-21.mdx`; this week (2026-09-28) is the
very next calendar week with no missed week in between.

**Coverage:** 282 repos scanned (55 `prime-radiant-inc`, 227 `obra`), zero
fetch/clone errors, 6 repos with in-window activity.

**Credential note (tooling provenance, not a content fact):** the broker-
issued placeholder for the `github-token` credential came back with a
genuine upstream 401 ("Bad credentials", real GitHub response headers
including `X-GitHub-Request-Id` — not a broker-shaped denial) on every
host/header combination tried. Cross-checked against a known-good
baseline: this box's own already-authenticated `gh` session (account
`ada-sen`, scopes `gist, read:org, repo`) succeeds against the identical
endpoint with no token override. Ran `gather.py` and every `repo-report`
call on that existing `gh` session instead (no `GH_TOKEN`/`GITHUB_TOKEN`
override — consistent with "use `gh` normally with those unset"), via a
local, uncommitted one-line fallback in the gather script (falls back to
`gh`'s own session if no env token is set and `gh auth status` succeeds).
Flagging the broken broker credential for Ada; the workaround is not part
of any committed change.

**One new repo this week:** `obra/muse-skills`, created 2026-09-29.

**Three tagged releases landing this week across two repos, plus a burst
of eleven more from one repo (see `evener` below):**
- `obra/superpowers-chrome` v3.0.8.
- `prime-radiant-inc/agentic-usage-meter` v0.2.7.
- `prime-radiant-inc/evener` v0.2.0 through v0.3.4 (eleven releases this
  week alone — version numbering skips straight from v0.2.5 to v0.3.0,
  nothing missing on this end, just not sequential by tenths).

**Contributor legend:** "staff" = `prime-radiant-inc` org member AT COMMIT
TIME. Current membership, confirmed live this run via `GET
/orgs/prime-radiant-inc/members`: `ada-sen` (Ada Sen), `arittr` (Drew
Ritter), `cadence-sen`, `kattni` (Kattni), `ketted`, `nora-primeradiant`,
`obra` (Jesse Vincent), `reeve-sen`, `simonw` — unchanged from the
2026-09-21 post's roster. Every commit this week falls inside the last
five days, so current membership is a safe proxy for "at commit time"
here. `mhat` (a former employee, staff only for his own employed weeks,
long since passed at this point in the blog's history) does not appear as
a contributor anywhere this window — checked, no commits under "mhat" or
any variant name — so his former-staff/temporal case doesn't come up this
week either.

**Two human commit identities this week, both staff, cleanly resolved:**
`obra` (Jesse Vincent) and `ada-sen` (Ada Sen). No outside human
contributor landed a commit this week. One external login, `sophieow`,
opened (but did not merge) a PR against `obra/superpowers-chrome` — see
that repo's section below; not counted as a contributor since nothing of
theirs shipped.

**One UNRESOLVED identity (not the same thing as ambiguous) — flagging for
Jesse, not guessing:** `obra/muse-skills`'s entire six-commit week is
authored under the git identity `file-integrity <file-integrity@local>`.
`GET /users/file-integrity` 404s — there is no GitHub account at all behind
this identity, so it cannot be placed in either the staff or outside
bucket; it isn't ambiguous between the two, it simply has no account to
look up. The `@local` email and the mechanical, dated commit subjects
("skills snapshot 2026-09-28", "skills snapshot 2026-09-29", ...) match the
shape of prior weeks' local agent-tooling identities (`evener@local`, `C
Compiler Builder <compiler@local>`) rather than a human contributor — my
working read is that this is an automated daily snapshot job, not a
person — but it is written up under its own name below, not folded into
"staff" or "outside." **Please confirm with Jesse: is `file-integrity` his
own automation, and does it belong under the same "tooling, not an outside
contributor" treatment the earlier `@local` identities got?**

One more automated identity, unambiguous this time: `github-actions[bot]`
drives all of `prime-radiant-inc/claude-plugin-stats`'s activity this week
(a daily scheduled scrape-and-rebuild job) — not folded into staff or
outside, called out on its own in that repo's section.

**Data-quality footnote (LOC provenance, muse-skills):** the large majority
of `muse-skills`' added-line count this week is one single daily snapshot
commit, not incremental hand-authored diffs — treat the LOC figure as "size
of a periodic bulk snapshot," not as a measure of a week of organic
feature work, the same caution the skill notes ask for with any bot/
regen-style commit that can inflate a raw LOC count.

## FEATURED (new repo or tagged release)

### obra/muse-skills
No repository description set.
**FEATURED — new repo, created this week (2026-09-29).**
A new repo that exists solely to snapshot something named "skills" on a
recurring schedule: six commits, five of them dated subjects like "skills
snapshot <date>" landing roughly once a day across the week, each
rewriting a large slice of the tree's files; plus one small, separate "Add
README" commit. All six commits are authored under the unresolved
`file-integrity <file-integrity@local>` identity described above — no
human commit in the repo this week to confirm intent beyond what the
commit subjects say. No merged or opened PRs, no releases. Whether this is
Jesse's own agent tooling (as its shape suggests) is for him to confirm,
not for this brief to assert.

### prime-radiant-inc/evener
A coding agent: give it a prompt and it reads, writes, runs commands, and
searches code in a loop until the work is done, using native tool-calling
across OpenAI, Anthropic, and Google models.
**FEATURED — eleven tagged releases this week (v0.2.0 through v0.3.4).**
By far the week's highest-volume repo, entirely the work of Jesse Vincent
(`obra`) — every commit and every merged PR this week carries his name, no
other author appears. The week's PR titles cluster into a few clear
threads rather than one single feature:
- A large **native/mobile** push: an in-progress iPhone redesign (handoff
  memos, phase-by-phase screenshots and device checks, planning docs for
  upcoming server-side slices), a "Board" notices/search feature built out
  over several phased PRs, changes to session/hub navigation (hub pairing
  and first run, hosts in the hub, "display in the hub"), and a long tail
  of fast-follow fixes against RoboRev review findings and earlier phases
  of the same redesign.
- A **hub/appwire/sdk refactor** thread: typed receipt fields for mutation
  IDs, scoped activity invalidations, shared host-forwarding/task-list/job
  -detail result types, and classifying remote mutation errors by
  provenance — reads as a sustained push toward stronger typing across the
  client/server boundary rather than a single PR.
- **Credential/auth handling in the hub:** a refreshed launch model list
  pushed to clients, a session's refused credential surfacing as an error
  immediately, and auth status reporting a credential the provider
  rejected — several PRs reference the same underlying tracking issue.
- Smaller but notable: web composer UI cleanup (removing mobile footer
  clutter, scoping activity footers to session panes, simplifying the
  session menu), and a performance pass (caching the model picker's launch
  list, computing hub tree-sort titles once instead of per comparison,
  bounding a directory walk by budget).
- Eleven releases cut over the week (v0.2.0 through v0.3.4, skipping
  straight from v0.2.5 to v0.3.0) — titles are bare version numbers with no
  further release notes attached, so there's nothing past the version
  sequence itself to report about the releases as such.

### prime-radiant-inc/agentic-usage-meter
macOS menu-bar meter for coding-agent subscription quotas.
**FEATURED — tagged release v0.2.7.** Sole author: Jesse Vincent (`obra`,
staff).
- Added visibility into "banked" subscription resets for Codex and Claude:
  documented what verified banked-reset data looks like for both, then
  shipped fetching the banked reset counts and individual grants and
  showing them as an expandable list with expiry dates.
- Tightened existing UI: collapsed banked resets into a single
  subscription count row instead of a sprawling list, and kept credit
  balances readable in account rows.
- A packaging fix: preserved structured SwiftPM resource-bundle metadata
  that was apparently getting lost.
- Shipped v0.2.7 as "production release," then one more commit after the
  tag: clearing live browser session data before removing a profile (a
  cleanup/security fix, not part of the tagged release itself).

### obra/superpowers-chrome
Claude Code plugin for direct Chrome browser control via DevTools Protocol
— zero dependencies.
**FEATURED — tagged release v3.0.8.** Both merged PRs and the release
itself are Ada Sen (staff, `ada-sen`).
- A real security fix: the existing `data-sen-secret` DOM-marker guard
  only caught credential-shaped content when the caller read back full
  serialized HTML — `eval`, `extract`, and `attr` calls that returned
  plain text or a bare attribute value could still leak a marked secret's
  value verbatim (reported by a downstream user, confirmed reproducible on
  v3.0.6). Fixed by having a new live-DOM marker check run before those
  code paths return anything, rather than relying only on the
  content-shape heuristic.
- A follow-up rendering fix: when an action triggers a native browser
  dialog mid-flight (click/select/eval), the response-formatting code was
  reading dialog/URL/size fields off the wrong shape and showing "unknown"
  and "???" placeholders instead of the actual dialog text and
  accept/dismiss instructions — including silently dropping the
  credential-suppression notice when the dialog message itself was
  secret-shaped. Fixed to recognize and render that shape correctly.
- Two PRs opened but **not merged** this window, both still open as of the
  snapshot: Ada Sen's own follow-up (password/one-time-code fields no
  longer copied to disk when mirrored into an attribute) and an external
  contributor's (`sophieow`, not a `prime-radiant-inc` org member —
  **outside**) adding a `CHROME_WS_HEADLESS` env var for servers with a
  fixed command line. Neither counts toward this week's shipped work since
  neither merged, but both are worth watching for next week.

## ALSO SHIPPED

### obra/lace
Lightweight agentic coding environment.
Two small, unrelated docs PRs, both Ada Sen (staff) with Jesse Vincent
co-authoring both: a CONTRIBUTING.md (including a correction to match the
actual pre-commit hook config, and review follow-ups scoping the
self-merge rule and documenting prerequisites/skip conditions for the live
test suite), and documentation for the repo's `recall` tool (correcting
its advertised exclusion syntax from a leading `-` to the actual `NOT`
operator, and documenting read/thread size caps and what the redaction
list actually matches).

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
Purely mechanical this week: `github-actions[bot]` (automation, not staff
or outside) ran its daily "update plugin stats" + "rebuild chart data"
commit pair once a day, every day, all week. No human commit, no PR, no
release — the routine scheduled job this repo exists to run, nothing more
to narrate.

## Repos checked with zero in-window activity worth a footnote

Nothing beyond the routine dormancy pre-filter this week. Not investigated
further beyond the standard dormancy check (`created_at`/`pushed_at` both
before window start).

## Structured stat data

The `2026-09-28` key merged into `src/data/weekly-stats.json` (diffed
byte-for-byte identical against `main` for every other week before this
one was added) is the source for every number above.
