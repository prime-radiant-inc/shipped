# Narrative brief — week of 2026-11-02 (cutoff-to-cutoff)

Grounded in `tools/gather.py --cutoff 2026-11-06T23:17:46Z` (prev-cutoff
auto-resolved from `src/data/weekly-stats.json["2026-10-26"]["cutoff"]` =
`2026-10-30T23:01:41Z`, exactly the value handed down from last week —
confirmed automatic, no `--prev-cutoff` override needed) on
`fix/cutoff-week-label-and-header` at `96c1aea` (both orgs; the week-label
and header fixes already in) + `tools/gen_stats.py`'s extract, merged into
`src/data/weekly-stats.json` + `gh api` pulls (release bodies, per-commit
file lists) for narrative/editorial detail. No numbers in the post are
hand-typed; every figure renders from the `WeekSummary`/`RepoStat` widgets
off `src/data/weekly-stats.json`.

**Window:** `(2026-10-30T23:01:41Z, 2026-11-06T23:17:46Z]` — exclusive
start, inclusive end. Key/label: `2026-11-02` (the Monday of the calendar
week containing the cutoff), produced automatically by the
`week_label_for_cutoff()` fix — no hand-renaming needed this time, unlike
week-of-2026-10-26.

**Coverage: clean.** 63 `prime-radiant-inc` repos + 229 `obra` repos
scanned, zero fetch/clone errors, 19 repos with in-window activity (13 + 6).
See `data/coverage-report-20261106.md`.

**Org roster check:** live `GET /orgs/prime-radiant-inc/members` this run
returns `ada-sen`, `arittr`, `cadence-sen`, `ketted`, `nora-primeradiant`,
`obra`, `reeve-sen`, `simonw` — same eight logins as every recent week's
check.

## Contributor attribution — resolved identities (by GitHub login)

| Identity (login) | Resolves to | Classification | Repo(s) this window |
|---|---|---|---|
| `obra` | Jesse Vincent | **in-org** (`prime-radiant-inc` member, staff) | evener, shepherd-pr, agent-session-archiver, toolsmith, prime-radiant-marketplace, obra/dotfiles, obra/lace, obra/superpowers, obra/superpowers-marketplace |
| `ada-sen` | Ada Sen | **in-org** (staff; owner) | prime-radiant-inc/shipped |
| `simonw` | Simon Willison | **in-org / staff, this week only** (see correction below) | external-sandbox-container, external-sandbox-v86, external-sandbox, external-sandbox-quicksand |
| `wemcdonald` | Will McDonald | **outside** | clipfan |

No ambiguous identities this window — every human commit resolves to a
clean GitHub login. `simonw` was initially drafted outside, per the prior
weeks' precedent below, then corrected after Jesse confirmed directly
(not a guess either way).

`obra` and `ada-sen` are confirmed `prime-radiant-inc` members at commit
time (live roster check; every commit this window falls inside the last
seven days, so current membership is a safe proxy for "at commit time,"
same reasoning as every prior week's brief). `mhat` (former employee,
staff only for his own employed weeks) does not appear as a contributor
anywhere this window — checked, no commits under "mhat" or any variant
name, so his employment window never came into play.

**CORRECTION, post-Cadence-accuracy-pass on `a79eec1`: `simonw` (Simon
Willison) is in-house, per Jesse directly.** This draft originally
classified him **outside**, on this blog's long-established precedent
(see `drafts/narrative-2026-10-26.md` and `drafts/narrative-2026-10-19.md`,
both of which list him in the same live org-members roster check and then
classify him outside "on the same single signal, no ASK JESSE needed") —
that precedent turns out to have been wrong, or at least stale: Jesse
confirmed Simon Willison is in-house/staff. Corrected here to **in-org /
staff, this week only** (per Ada's instruction — not asserting he was
staff for any other week this blog has covered, since those weren't
re-confirmed and aren't being revised). The prose in
`src/content/posts/week-of-2026-11-02.mdx` now reads e.g. "Sole author:
**Simon Willison (staff, \`simonw\`)**." on all four `external-sandbox-*`
articles, matching the existing in-org phrasing pattern (cf. "Jesse
Vincent (staff, \`obra\`)"), with "outside contributor" removed
everywhere it applied to him (the four per-repo attribution lines plus
the summary frontmatter and intro paragraph). Past posts are NOT being
edited — this correction is scoped to week-of-2026-11-02 only. He
authored 100% of the commits on all four `external-sandbox-*` repos this
window — a connected family of sandbox-wrapper tools (Apple Containers,
v86/Alpine, Microsoft Quicksand) that are legitimately owned by
`prime-radiant-inc` (not forks), under a personal `@gmail.com` address.
Flagging for whoever reviews future weeks: the "outside, despite being in
the org roster" precedent this blog relied on for several weeks running
should probably be revisited rather than assumed next time his login
shows up, now that it's been contradicted by a direct answer from Jesse.

`wemcdonald` (Will McDonald) merged `clipfan`'s v1.0.13 release PR himself
this window (as well as authoring the fix inside it) — a personal
`@gmail.com` address, not an org member, consistent with his outside
classification on this repo since 2026-10-26.

## Bot / unresolved identities — not attributed to a person

- `github-actions[bot]`: `prime-radiant-inc/claude-plugin-stats` (chart-data
  rebuilds) and `prime-radiant-inc/terminal-bench-analysis` (a README
  regen with no new data) — same bot-only repos as every recent week.
- `Journal automation` (no linked GitHub login): all of
  `obra/model-training-journal`'s commits this window, same as its launch
  week.
- `file-integrity` (no linked GitHub login): all of `obra/muse-skills`'
  commits this window, same unconfirmed-automation treatment as recent
  weeks. Mixed content this time — routine dependency/config bumps plus
  what reads like a new Home Assistant integration (`home-assistant/`
  added wholesale) — still no signal pointing to a human behind the
  identity, so still excluded from human attribution.

## Editorial LOC-suppression calls (hand-set `loc_suppressed`, not
   detected automatically — see `tools/gen_stats.py`'s comment on this
   field)

Two cells this window have their raw LOC numbers dominated by non-authored
content and are hand-flagged `loc_suppressed: true` in
`data/recon-cutoff-20261106.json` before running `gen_stats.py`, exactly
as `RepoStat.astro`/`WeekSummary.astro` expect:

1. **`obra/model-training-journal`** (+5,629/−2,890 raw): per-commit file
   lists confirm each commit touches ~85-94 generated `docs/2026/10/26/.../
   index.html` pages for a snapshot-age clock (±5 lines each) plus
   `dashboard-data.json`/`progress.json` regen — same pattern, same call,
   as week-of-2026-10-26's treatment of this repo.
2. **`prime-radiant-inc/shipped`** (+23,507/−10 raw, this repo): dominated
   by committing `data/recon-cutoff-20261030.json` (~20k lines) wholesale
   as part of drafting last week's post — a raw data dump, not prose or
   code.

Spot-checked and NOT suppressed: `prime-radiant-inc/evener`'s large diff
(+137,847/−38,014) includes some vendored license/model files in one
commit (~1,800 of 5,408 lines in that commit) but the bulk is real source
across many files/commits — not "almost entirely generated," left as-is.
`prime-radiant-inc/external-sandbox-v86`'s diff likewise includes a
third-party-license-notices commit and a file-move commit, both real
structural changes, not data dumps — left as-is.

## Featured / also-shipped split (from `gen_stats.py`'s `featured` flag:
   new repo OR has a release this window — not an editorial choice)

**Featured (8):** evener (6 releases), clipfan (1 release), shepherd-pr (2
releases), external-sandbox-container (1st release), external-sandbox-
quicksand (1st release), agent-session-archiver (new repo), toolsmith (new
repo), obra/superpowers (1 release).

**Also shipped, full write-up (7):** prime-radiant-marketplace,
external-sandbox-v86, external-sandbox, obra/dotfiles, obra/lace,
obra/model-training-journal, obra/superpowers-marketplace.

**Also shipped, caveat-footnote only (4):** claude-plugin-stats,
terminal-bench-analysis, muse-skills, shipped — same "no attributable
human, or this blog's own tooling" bucket as every recent week, same 4
repo names as week-of-2026-10-26's caveat paragraph.

## Build verification

`npm run build`: 47 pages (46 existing + 1 new), zero errors. Diffed
`dist/posts/` against a clean `main` build: all 45 posts with no recorded
cutoff are byte-identical; `week-of-2026-10-26` (which DOES carry a
recorded cutoff) now shows the correct cutoff window in its header instead
of the calendar `dateStart`–`dateEnd` range — the header fix's documented,
intended effect, not a regression. `week-of-2026-11-02` renders with all
widgets populated (19 repos active, 152 commits, 110 merged PRs,
+168,817/−41,988 lines, 7 commit identities, 12 tagged releases) and the
cutoff-note footer reads "Commits from 2026-10-30 23:01 to 2026-11-06
23:17 UTC on default branches; merge commits not counted." `python3 -m
pytest tools/ -v`: 36 passed.

Not merged to main, not deployed, not pushed to gh-pages.
