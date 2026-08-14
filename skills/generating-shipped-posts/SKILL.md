---
name: generating-shipped-posts
description: Use when regenerating or writing weekly posts for the "Shipped" blog (prime-radiant-inc/shipped) — the canonical method for exhaustive, commit-driven data gathering and post structure
---

# Generating "Shipped" blog posts

## Purpose

"Shipped" posts are an EXHAUSTIVE public record of everything shipped
across the `prime-radiant-inc` and `obra` GitHub orgs. The goal is
completeness and showing the true volume of work — not curated highlights.
If a repo had commits in the window, it belongs in the post, full stop.

## Data gathering (`tools/gather.py`)

- Enumerate EVERY public repo in both orgs. Do not pre-filter by PRs or
  releases.
- Include any repo with at least one commit on its default branch within
  the week window. (v1's bug: it only counted repos that had a merged PR
  or a release, so repos shipped via direct push to the default branch
  vanished entirely.)
- For each active repo, per week, collect:
  - commit count
  - the full commit list (SHA, author, ISO date, subject)
  - merged PR count plus titles/numbers
  - unique authors and per-author commit counts
  - LOC added/removed via `git log --numstat`
  - any release tags cut that week (tag, name, date)
  - repo description and primary language

### Forks

Count ONLY commits the fork is *ahead* of its upstream — via GitHub's
compare API (`ahead_by` / the `commits` list in
`GET /repos/{owner}/{repo}/compare/{upstreamOwner}:{branch}...{owner}:{branch}`).
Never credit inherited upstream history to the fork owner. This is a proven
bug, not a theoretical one: v1 showed `obra/freshell` at ~90-100
commits/week even though the fork was created and never touched again —
the upstream project (`danshapiro/freshell`) was just actively developed on
its own, and a naive `git log <default-branch> --since --until` on the
fork's default branch silently counts that as the fork owner's work,
because for a fork the default branch's history *is* the upstream
project's history.

### Dormancy pre-filtering

If you pre-skip repos to save time (recommended — most repos in `obra`
particularly are dormant forks), key the skip decision ONLY on whether
there is provably zero activity *within* the window:

- Safe to skip: `created_at` is before the window start AND the repo's
  most recent push (`pushed_at`) is also before the window start. Any
  commit landing in-window is itself a push, so this can never produce a
  false negative.
- NOT safe: skipping because the most recent push is after the window's
  *end*. A repo that kept shipping after your snapshot instant is still
  fully capable of having shipped *during* the window too — the two facts
  are unrelated. This exact bug silently dropped `serf`, `clipfan`, and
  `winpepper` from a run once, because all three had continued activity
  after the frozen window closed and an `<= window_end` check on
  `pushed_at` read that as "no push in window."

### Reproducibility and accuracy

- Use a frozen window-end snapshot (an explicit timestamp, not "now" at
  run time) so re-runs of the same window are comparable.
- Prefer a shallow `git clone` (`--shallow-since`) plus local
  `git log --numstat` over the GitHub API for commit/LOC detail — it's
  exact, and avoids one API call per commit, which is prohibitively slow
  for high-velocity repos (some of these have 1000+ commits in 8 weeks).
  Fall back to a full (non-shallow) clone if `--shallow-since` fails; this
  has been observed on at least one very-small repo and is a cheap,
  reliable fallback.

## Data-integrity rules

Write these into the prose, honestly — don't just apply them silently:

- Flag and exclude/footnote generated or bot commits that inflate LOC
  (e.g. a "Regenerate README" bot commit that adds millions of lines from
  a rebuilt lockfile or dataset dump). Never quote a raw LOC number that is
  really a generated-file regen — it makes the whole post look either
  fabricated or clueless.
- Label provenance clearly, everywhere: `obra/reponame` vs.
  `prime-radiant-inc/reponame`. For forks, be explicit that the repository
  is ours but the underlying project is the wider community's.
- Only claim what the data supports. Write every change summary from
  actual commit subjects and PR titles pulled from the data. Do not invent
  changelogs, release contents, or motivations that aren't in the log.

## Post structure (long-form, exhaustive)

1. **Summary up front.** Lead with the week's totals: repos touched,
   commits, merged PRs, net LOC (+/-), contributors, releases cut.
2. **Exhaustive per-repo sections.** Every repo that was active that week
   gets a section: a real change summary written from the commit log,
   followed by that repo's stats (commits, PRs, authors, LOC +/-,
   releases). Nothing active is omitted, even if the writeup is one line.
3. **Weighting, not filtering.** New repos and repos with a release get
   fuller, featured treatment. Everything else gets a compact writeup —
   but "compact" means shorter prose, not exclusion.

## Publishing

- Build clean (`npm run build`) before deploying. Confirm the expected
  number of pages and spot-check that dynamic content (featured sections,
  repo links) actually rendered — markdown embedded in raw HTML blocks can
  silently fail to convert.
- **Current constraint:** the broker-issued GitHub token may lack
  `workflow` scope, which blocks pushing any `.github/workflows/*` file
  (GitHub rejects the push outright, not just the Action). Two workarounds:
  1. Deploy the built static site directly to a `gh-pages` branch (no
     workflow file needed at all) and point GitHub Pages at that branch —
     works with a plain repo-scoped token.
  2. Obtain a `workflow`-scoped token — requires a human to approve a
     fresh `gh auth login -h github.com -s workflow` device-flow code at
     `github.com/login/device` (the broker's placeholder token doesn't
     carry this scope and can't be upgraded in place) — then re-enroll
     that token with the credential broker so it can be requested for
     future pushes. Once available, GitHub Actions auto-deploy via
     `.github/workflows/deploy.yml` works normally on every push to `main`.
