# Shipped

A weekly recap of public-repo activity across the `prime-radiant-inc` GitHub
org and the `obra` GitHub user account. Built with [Astro](https://astro.build)
(pinned to the `4.16.19` "legacy" release — see *Why Astro 4* below),
deployed to GitHub Pages.

## Layout

```
src/content/posts/   weekly posts (markdown, one per week bucket)
src/content/config.ts  content-collection schema for posts
src/layouts/          shared page chrome
src/pages/            index + per-post routes
src/styles/           global.css (featured vs second-tier styling lives here)
data/                 recon JSON (raw activity data pulled from the GitHub API)
tools/gather.py       regenerates data/recon-*.json for an arbitrary N-week window
drafts/               per-week FACTUAL briefs (bullet facts, not prose) —
                      turn these into the actual posts in src/content/posts/
```

## Post frontmatter schema

```yaml
title: string          # post title
week: string            # human label, e.g. "Week 32, 2026"
dateStart: date         # first day of the week bucket
dateEnd: date           # last day of the week bucket
pubDate: date           # publish date
summary: string         # index-page teaser
draft: boolean          # optional, default false — true hides from the index
```

Within a post body, wrap featured items in `<section class="featured">` and
second-tier items in `<section class="second-tier">` — see
`src/content/posts/week-00-example.md` for the pattern. That example post is
scaffold-only (fake repo names, obviously placeholder copy) and should be
deleted once real weekly posts exist.

## Commands

| Command | Action |
|---|---|
| `npm install` | install dependencies |
| `npm run dev` | local dev server |
| `npm run build` | build to `./dist/` |
| `npm run preview` | preview the built site |

## Regenerating data

Two modes, both in `tools/gather.py`:

**Calendar mode (original, full/backfill recons)** — N calendar (Mon-Sun)
week buckets ending at `--window-end` (default: now):

```
python3 tools/gather.py --weeks 8
```

Output: `data/recon-<N>wk-<YYYYMMDD>.json`.

**Cutoff-window mode (`--cutoff`, current/ongoing posts)** — one bucket
covering `(--prev-cutoff, --cutoff]` instead of a calendar week, with merge
commits excluded from commit/line/author counts (see the gather.py module
docstring, bug 6):

```
python3 tools/gather.py --cutoff 2026-11-08T18:30:00Z \
    [--prev-cutoff 2026-11-01T12:00:00Z]
```

- `--cutoff`/`--prev-cutoff` **must be UTC** — `Z` suffix or an explicit
  `+00:00` offset. Any other offset, or a naive timestamp with no offset at
  all, is rejected with a non-zero exit: `WeekSummary.astro`'s
  `fmtCutoff()` displays the stored value labeled "UTC" verbatim with no
  offset conversion, so anything else would show the wrong wall-clock time
  on the published post.
- `--prev-cutoff` is optional. If omitted, it's resolved from the most
  recently published week's own recorded `cutoff` field in `--stats-json`
  (default `src/data/weekly-stats.json`) — see `resolve_prev_cutoff()`. If
  no week there has one yet (nothing has been published under this mode),
  the run errors rather than guessing a window.

Output: `data/recon-cutoff-<YYYYMMDD>.json`.

Requires a GitHub token in the `GH_TOKEN` (or `GITHUB_TOKEN`) environment
variable. This subagent's environment gets that token from Ada's credential
broker (`request_credential`, host `api.github.com`) — the script itself has
no access to the broker and expects the token to already be in the
environment when it runs; see the docstring in `tools/gather.py`. Public
repos only; forks are excluded from the "created in window" FEATURED trigger
(their `created_at` is the fork date, not the upstream project's).

### Turning a recon into `weekly-stats.json` (`tools/gen_stats.py`)

```
python3 tools/gen_stats.py data/recon-cutoff-20261108.json --out src/data/weekly-stats.json
```

`gen_stats.py` **merges** the recon's weeks into the existing `--out` file
rather than replacing it outright: any week already in `--out` that isn't
in this recon's `week_buckets` is left completely untouched; any week that
IS in the recon (new or already-published) is added/replaced. This is what
makes it safe to run a `--cutoff` recon — which always has exactly ONE week
bucket — against the full, many-week `weekly-stats.json`: it can only ever
touch its own week.

As a second, independent safety net, `gen_stats.py` **refuses to write**
(non-zero exit) if the result would have fewer weeks than the file already
had — pass `--force` if shrinking the file is actually what you want (e.g.
deliberately dropping a week). See `merge_weeks()`/`guard_against_shrink()`
in `tools/gen_stats.py` and `tools/test_gen_stats.py` for the tests.

### Tests

```
python3 -m pytest tools/ -v
```

## Deploy target

GitHub Pages, project page at `prime-radiant-inc/shipped` →
`https://prime-radiant-inc.github.io/shipped/`. `astro.config.mjs` sets
`site` + `base: '/shipped'` accordingly.

**If this ever moves to a custom domain**, add a `public/CNAME` file with the
domain and change `base` to `'/'` in `astro.config.mjs` (project-page Pages
sites are served under `/<repo-name>/` unless a custom domain is set).

`.github/workflows/deploy.yml` builds and deploys on push to `main` via
[`withastro/action`](https://github.com/withastro/action) + GitHub's official
Pages actions. It won't run anywhere until this repo is pushed to GitHub and
Pages is enabled (Settings → Pages → Source: GitHub Actions) — neither of
which this subagent has done.

## Status

Scaffold + data tooling only. Blog prose is Ada's; the 8 per-week factual
briefs in `drafts/` are inputs for that, not finished posts. No GitHub repo
has been created and nothing has been pushed anywhere from this box.
