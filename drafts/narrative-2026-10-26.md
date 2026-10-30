# Narrative brief — week of 2026-10-26 (cutoff-to-cutoff, PR #4 rules)

Grounded in `tools/gather.py --cutoff 2026-10-30T23:01:41Z --prev-cutoff
2026-10-23T22:10:22Z --out data/recon-cutoff-20261030.json --report-out
data/coverage-report-20261030.md` (main at `12751b5`, both orgs; PR #3's
shallow-clone/graft fix and PR #4's cutoff-to-cutoff-with-merges-excluded
mode both already in, nothing cherry-picked) + `tools/gen_stats.py`'s
extract, merged into `src/data/weekly-stats.json` + 10 per-repo `gh api`
pulls (commit lists, merged-PR titles, release bodies, README/tree
content) for full narrative detail. No numbers below — pure narrative;
every figure in the post renders from the `WeekSummary`/`RepoStat` widgets
off `src/data/weekly-stats.json`.

**Window, per PR #4's cutoff-to-cutoff rule:** `(2026-10-23T22:10:22Z,
2026-10-30T23:01:41Z]` — exclusive start, inclusive end. The start is the
value Ada's accuracy reviewer (Cadence) confirmed as last week's real
gather-run instant; it does not appear anywhere in `src/data/weekly-
stats.json` yet because the 2026-10-19 post was generated the old
calendar (`--weeks`) way, which doesn't record a `cutoff` field — so
`--prev-cutoff` had to be passed explicitly (`resolve_prev_cutoff()` would
otherwise have had nothing to read and erred out). This run's own
`--cutoff` (2026-10-30T23:01:41Z, this gather run's wall-clock instant) is
now recorded on the `2026-10-26` week entry and becomes the next post's
`--prev-cutoff` once published. **Merge commits count for nothing this
week** (commits, lines, or authors) — PR #4's rule, exercised for real on
`obra/lace` (5 merge commits in its raw list, 0 of them counted) and
`prime-radiant-inc/clipfan` (2 merge commits landing Will McDonald's 2
PRs, same treatment). `WeekSummary.astro`'s cutoff-note footer (`Commits
from 2026-10-23 22:10 to 2026-10-30 23:01 UTC on default branches; merge
commits not counted.`) renders on this post from the stored
`cutoff`/`prev_cutoff` fields.

**Week-label key, a deliberate renaming, flagging for Ada/Cadence:**
`gather.py --cutoff` mode keys the new `week_buckets` entry (and
`gen_stats.py` in turn keys `weekly-stats.json`) by `window_start.date()`
— i.e. the *previous* cutoff's calendar date, `2026-10-23` (a Friday) in
this run. Every post on this blog, calendar-mode or not, is filed and
dated by the calendar Monday it covers (`week-of-YYYY-MM-DD`,
`dateStart`), so leaving the stats key as the mechanical `2026-10-23`
would silently desync the widgets from the post's own frontmatter/URL
(`week-of-2026-10-26`, `dateStart: 2026-10-26`) — the exact failure mode
`WeekSummary.astro` is built to hard-fail on for LOC, but there's no
equivalent guard for the week-key string itself. After confirming the
full recon payload was correct, I renamed just that one top-level key
from `2026-10-23` to `2026-10-26` in `src/data/weekly-stats.json` (data
unchanged, including `cutoff`/`prev_cutoff`) and used `2026-10-26`
throughout the MDX's widget calls. Diffed against `main`: only one key
added, byte-identical otherwise (2806 insertions, 1 deletion — the
deletion is the old file's closing `}` growing a trailing comma). This is
a tooling gap worth fixing properly in `gather.py`/`gen_stats.py` (e.g. an
explicit `--week-label` override) rather than hand-patched every cutoff
run; flagging it rather than silently doing it quietly.

**Coverage: clean.** 57 `prime-radiant-inc` repos + 229 `obra` repos
scanned, zero fetch/clone errors, 10 repos with in-window activity (7 +
3). See `data/coverage-report-20261030.md`.

**Org roster check:** live `GET /orgs/prime-radiant-inc/members` this run
returns the same eight logins as every recent week's check — `ada-sen`,
`arittr`, `cadence-sen`, `ketted`, `nora-primeradiant`, `obra`,
`reeve-sen`, `simonw`. No change. `arittr` (Drew Ritter) has zero commits
this window — not a contributor this week, just not active.

## Contributor attribution — resolved identities

| Identity (login / display) | Resolves to | Classification | Repo(s) this window |
|---|---|---|---|
| `obra` | Jesse Vincent | **in-org** (`prime-radiant-inc` member) | streamlinear, evener, shepherd-pr, lace, clipfan (2 merge commits, 0 counted) |
| `ada-sen` | Ada Sen | **in-org** | shipped, streamlinear, lace |
| `wemcdonald` | Will McDonald | **outside** | clipfan |
| `anubhavgupta121` | anubhavgupta121 (no display name on file) | **outside** | evener |
| `wangyusheng1985` | 玉升 | **outside** | evener |

`obra` and `ada-sen` are confirmed `prime-radiant-inc` members at commit
time (live roster check; every commit this window falls inside the last
seven days, so current membership is a safe proxy for "at commit time,"
same reasoning as every prior week's brief).

`wemcdonald` (Will McDonald, personal `@gmail.com` address) opened and had
merged two small Mac-client bugfix PRs (#10, #11) on
`prime-radiant-inc/clipfan` — not in the org roster, no prior appearance
in any brief. Classified **outside contributor**, consistent with this
blog's established precedent for a clean non-member GitHub login with no
other signal (Dan Shapiro, Simon Willison, Eden, `jtdaugh`, etc. were all
classified the same way on the same single signal, no `ASK JESSE` needed
for any of them). `clipfan` has taken outside contributions before (an
outside cross-platform-install PR in the 2026-08-10 week), so this isn't
a new pattern for this repo.

`anubhavgupta121` and `wangyusheng1985` (display name 玉升) each landed one
small, PR-tracked fix on `prime-radiant-inc/evener` (`#4739`/`#4561`
bounded-hook-output-capture fix, `#4647` a `.gitignore` trailing-slash
fix, `#4664` a diagnostic-test IndexedDB wedge reuse) — neither is an org
member, both via the same clean-signal non-member pattern as `wemcdonald`.
Classified **outside**, same reasoning, no ambiguity.

## Bot / unresolved identities — not attributed to a person

- `dependabot[bot]`: 12 commits on `prime-radiant-inc/streamlinear`
  (dependency bumps in `/mcp` — `ajv`, `@hono/node-server`, `zod`,
  `fast-uri`, `hono`, `@modelcontextprotocol/sdk`, `esbuild`, `qs`,
  `path-to-regexp`) + 2 on `prime-radiant-inc/evener`. Scheduled
  dependency bot, not a person.
- `github-actions[bot]`: all commits on `prime-radiant-inc/claude-plugin-
  stats` (7 — daily install-stats chart rebuild) and `prime-radiant-inc/
  terminal-bench-analysis` (2 — "Regenerate README (no new data)").
  Scheduled bots, not people.

## Ambiguous contributors — ASK JESSE, not resolved here

- **`file-integrity <file-integrity@local>`** (`obra/muse-skills`, all
  five commits this week — "skills snapshot 2026-10-24/27/28/29/30," same
  daily-cadence pattern as every prior week). No linked GitHub account
  (`GET /users/file-integrity` 404s); can't be placed in either the staff
  or outside bucket because there's no account to look up. Same open
  question carried forward unresolved since at least the 2026-10-05 brief
  — now four-plus weeks running: **is this Jesse's own automation?**
- **"Journal automation" `<journal@users.noreply.github.com>`**
  (`obra/model-training-journal`, all 22 commits this week — the repo's
  entire history so far). Same shape as `file-integrity`: no linked
  GitHub login, a noreply-style commit email, mechanical "Publish
  reviewed ..." subjects consistent with the repo's own documented build
  pipeline (`README.md`: "The generated pages are committed so they can
  be reviewed before publication," via `scripts/build.py`). This is a
  brand-new repo under Jesse's personal `obra` account (not a fork, not a
  company product — same "new repo under `obra` still gets the blog's
  new-repo featured trigger" precedent as `obra/morning-routine-board` in
  the 2026-10-05 brief), so almost certainly Jesse's own publishing
  automation rather than a third party — but per the same "no account to
  look up" rule applied to `file-integrity`, not resolving it by guess.
  **ASK JESSE: is "Journal automation" your own tooling?**
- **Kattni — checked, still unresolved, no commits this window either
  way.** Zero commits/PRs/releases under "Kattni" or any known variant
  anywhere in this window (confirmed: not in the 9 distinct commit
  identities this week). Re-checked every prior coverage report and
  narrative brief for a stated last day: none exists. The only prior
  record is the 2026-10-05 brief's **unconfirmed** roster-shrink
  observation — the live `GET /orgs/prime-radiant-inc/members` check
  dropped her name between the 2026-09-28 and 2026-10-05 checks, flagged
  then as "worth confirming with Ada whether that's an intentional
  departure or a token-scope/visibility artifact" and never resolved in
  any later brief. She remains absent from this week's roster check too
  (8 names, same as every week since). Since no coverage report ever
  recorded an actual last day, and the task's framing ("Kattni has left
  the company") isn't independently confirmable from this blog's own
  data: **ASK JESSE for Kattni's actual last day**, so a future week where
  she does have a commit near that boundary can be classified correctly
  instead of guessed. Not a blocker for this week's post — she has no
  activity here regardless of classification.

## Featured: two tagged releases with real release notes, one bare-tag
## release, and one brand-new repo

- **`prime-radiant-inc/streamlinear` v1.2.0 and v1.2.1** — both real,
  hand-written release notes. v1.2.0: labels wired into create/update
  (names resolve against the workspace label list; clearing on update;
  unknown labels error with the available options), state and UUID
  assignee support on create/update, a `STREAMLINEAR_POST_ONLY` mode so
  an agent can create/update issues without ever reading issue content,
  `@mention`-to-Linear-profile-link conversion, a dependency refresh
  (zod 4, MCP SDK 1.32) clearing every open Dependabot advisory, and a new
  end-to-end stdio test suite. v1.2.1, same day: labels/state/assignee
  added to the CLI's create/update to match the MCP tool, a UUID-accepting
  assignee search filter, a CLI crash fix when `--labels` is omitted, and
  a Windows build fix (building `dist` through a Node/esbuild script
  instead of a shell pipeline that mis-quoted on Windows). One commit
  (`132653c`, "Fix create/update to honor assignee, state, and UUID
  assignees") is Ada Sen's — the only non-Jesse, non-bot commit on this
  repo this window.
- **`prime-radiant-inc/evener` v0.3.17** — bare version tag, GitHub's
  auto-generated "What's Changed" PR-list body, no hand-written notes,
  consistent with every prior evener release. By far the most active repo
  again. The dominant pattern this week is a large two-track internal
  refactor (`W1-*`/`W2-*` branch-tagged PRs) across `agent`, `hub`, `web`,
  `native`, and `appwire-client`: splitting long functions into named
  phases, extracting leaf packages, consolidating duplicated test
  fixtures/helpers (one shared `connectFakeClient`/`connectReadyFakeClient`
  replacing dozens of hand-rolled copies across test files), and a
  parallel "Wave 2 audit" documentation review. Outside that: host-record
  storage consolidated into the operation store (hub.toml keeps only the
  hosts), a provider-connection-card fast-follow, queued-message
  edit/remove unified across browser and native, a shared single-owner
  Retry-eligibility path, small web-UI additions (a "Comic Chat" client,
  floating next-needs-you controls, a compact activity sidebar), and two
  small outside-contributed fixes (see above). Sole in-org author: Jesse
  Vincent, plus the two outside fixes and 2 `dependabot[bot]` commits.
- **`prime-radiant-inc/shepherd-pr` v0.3.2** — real, short hand-written
  release note: `roborev-review.sh` now counts findings under severity
  headings in the shape RoboRev's combined comment actually uses (`###
  High`, etc.) instead of reporting `severities=-` on every review with
  findings; `pr-settle.sh` and `stale-prs.sh` consume the same corrected
  counts. Sole author: Jesse Vincent.
- **`obra/model-training-journal`** — brand-new repo, created
  2026-10-26 (mid-window), meets the blog's new-repo featured trigger.
  "An AI-assisted engineering journal about training a small language
  model from scratch," per its own README: public entries separate
  observed results from plans, preserve failures/limitations, omit
  private operational details, and publish to GitHub Pages as static,
  deterministic, no-CDN/no-tracking HTML with static SVG charts (no raw
  logs, model weights, dataset copies, or credentials committed). 22
  commits this week are its entire history so far — "Publish the initial
  reviewed model training journal" through several numbered checkpoint
  updates, a plain-language-companion/evidence-dashboard addition, and a
  "V6 first checkpoint and run boundary" post. **LOC chip suppressed**:
  churn is 163,165 added / 7,432 removed across 22 commits (~7,754
  LOC/commit) — well over this blog's established mechanical
  churn/commit>3000 flag — and inspection of the actual tree confirms why:
  the bulk of every commit's diff is generated checkpoint/dashboard
  artifacts (`assets/charts/*.svg`, `assets/*checkpoint-history.json`,
  per-checkpoint `.txt`/`.json` data dumps), not hand-written prose or
  code, exactly the "data-dump/vendored/generated-artifact" case the rule
  targets. Flagged mechanically regardless of legitimacy, same as
  `obra/superpowers`'s real release-merge commit in the 2026-10-19 post.
  All 22 commits are under the unresolved "Journal automation" identity
  (see ASK JESSE above) — noted plainly in the post's attribution line
  rather than guessed into staff or outside.

## Also shipped

- **`prime-radiant-inc/clipfan`** — two outside-contributed Mac-client
  fixes from Will McDonald (`wemcdonald`), merged by Jesse: the Add Peer
  sheet now scrolls for large tailnets, and the command panel's history
  refreshes every time it opens. The two merge commits that landed them
  count for nothing under PR #4's rule (not in the 2-commit chip, not in
  the author list) — only Will McDonald's two authored commits do.
- **`prime-radiant-inc/claude-plugin-stats`** and **`prime-radiant-inc/
  terminal-bench-analysis`** — both entirely `github-actions[bot]`
  (daily install-stats scrape/chart rebuild; README regen with no new
  data). No human commits — folded into the bot-only caveat line, not
  given their own `RepoStat` widget, same established rule as
  `obra/muse-skills` in the 2026-10-19 post.
- **`obra/muse-skills`** — same caveat-line treatment, same unresolved
  `file-integrity` identity as every week since this was first flagged
  (see ASK JESSE above).
- **`obra/lace`** — a real memory subsystem landing in three stages this
  week (ownership/permissions foundation, then automatic extraction and
  recall built on top, including a same-week fix to the automatic-
  extraction image/search/sidecar boundaries and a fencing pass over
  memory-metadata writes for lifecycle races), a sticky temporary request-
  context API over Ent (preserving request context through OpenAI
  streaming fallback, plus two small provider/tool-ordering fixes folded
  in), a Gemini-gateway 404 retry-on-custom-base-URL fix, a new catalog
  entry (LunaRoute's `glm-5.3`/`glm-5.3-background`), and three small
  `todo_write`/`job_output` tool-contract fixes (job-id case-insensitive
  matching, refusing an id the session never returned, accepting
  `read_tool_result`'s slicing params) plus an idle-session-inject fix.
  Five of this week's raw commits are merges (0 counted, per PR #4's
  rule) — the 17-commit chip and the two-person author split (Jesse
  Vincent, Ada Sen as `ada-sen`) are built only from the 17 non-merge
  commits.
- **`prime-radiant-inc/shipped`** (this repo) — self-referential: PR #3
  (the shallow-clone/graft merge-boundary undercount fix, plus the
  `week-of-2026-09-28` terminal-bench-analysis correction it enabled) and
  PR #4 (cutoff-to-cutoff windowing with merges excluded from every
  count) both merged to `main` this window. Sole author: Ada Sen.

## Structured stat data

Generated this run: `data/recon-cutoff-20261030.json` (raw recon, with
one hand-added `loc_suppressed: true` flag on `obra/model-training-
journal`'s week-0 entry, applied before `gen_stats.py` ran — see Featured
above), `data/coverage-report-20261030.md` (coverage summary, clean,
zero errors), and the new `2026-10-26` key merged into `src/data/weekly-
stats.json` (diffed byte-for-byte identical against the pre-existing 44
weeks; only the new key added) — the source for every number that
renders in the actual post via `WeekSummary`/`RepoStat`.
