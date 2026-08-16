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
tools/gen_stats.py    reads a (ground-truth-corrected) recon JSON, emits
                      src/data/weekly-stats.json
tools/repo-report     <repo> <since> <until> [-o OUTPUT] — one source-material
                      Markdown file per repo+window (full commit messages,
                      resolved GitHub-login contributors, diffstat) for
                      authoring posts/backfills/corrections from; see its own
                      docstring for the diffstat-source-of-truth details
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

```
python3 tools/gather.py --weeks 8
```

Requires a GitHub token in the `GH_TOKEN` (or `GITHUB_TOKEN`) environment
variable. This subagent's environment gets that token from Ada's credential
broker (`request_credential`, host `api.github.com`) — the script itself has
no access to the broker and expects the token to already be in the
environment when it runs; see the docstring in `tools/gather.py`. Public
repos only; forks are excluded from the "created in window" FEATURED trigger
(their `created_at` is the fork date, not the upstream project's).

`tools/repo-report` needs the same token and produces per-repo/per-window
source material (full commit list, resolved contributor logins, diffstat) —
used to hand-correct `data/recon-*.json`/`src/data/weekly-stats.json` cells
that `gather.py`'s shallow-clone numstat gets wrong (see recent commit
history for examples: merge-commit LOC grafts, fork-inherited-history).

Output: `data/recon-<N>wk-<YYYYMMDD>.json`.

### Discovery rules (finalized per Jesse's ruling, 2026-08)

"Shipped" audits **public-repo activity only** — see the block above
`INTERNAL_OWNERS` in `tools/gather.py` for the full reasoning on each rule
below, and the EXCLUSION RULES / RULE 3 blocks in `process_repo()` for the
implementation:

1. **Public only.** Org/user listing is filtered to public visibility.
2. **Never private / never private-mirror-of-public.** Currently-private
   repos are excluded at listing time; a repo whose name/description marks
   it as a mirror or private-branches/test-harness copy of a public repo is
   excluded even if it is (or later becomes) public itself — this is the
   common shape of a security-issue mirror unfrozen after disclosure.
3. **Private→public-later is a known blind spot.** `gh api` only reports
   *current* visibility, not as-of-window. A repo genuinely private during
   the window, not recreated afterward, public now, with no name/description
   marker is undetectable with certainty — such repos are flagged in
   `data/ambiguous-flags.log` for human review rather than silently kept.
4. **`temp-` prefix excluded.** Any repo name starting with `temp-` is
   provisional/scratch by convention.
5. **Internal-upstream forks are kept.** A fork is excluded only if its
   ultimate upstream owner is outside `{prime-radiant-inc, obra}` — a fork of
   one of our own repos (e.g. `superpowers-testing` → `obra/superpowers`) is
   first-party work and stays in.

Every exclusion (and every ambiguous flag) is logged with its reason —
`data/discovery-exclusions.log` and `data/ambiguous-flags.log` are written on
every `gather.py` run, never silently empty-by-omission.

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
