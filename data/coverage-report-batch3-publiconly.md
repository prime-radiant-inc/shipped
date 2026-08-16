# Shipped v2 recon — coverage report

Generated: 2026-08-16T02:57:48.815671+00:00
Window: 2026-03-30T00:00:00+00:00 to 2026-04-26T23:59:59+00:00

## Week boundaries

- Week 1: 2026-03-30 to 2026-04-05
- Week 2: 2026-04-06 to 2026-04-12
- Week 3: 2026-04-13 to 2026-04-19
- Week 4: 2026-04-20 to 2026-04-26

## Discovery rules applied (public-only, finalized per Jesse's ruling)

1. PUBLIC ONLY -- org/user listing filtered to public visibility (list_public_repos).
2. NEVER PRIVATE / NEVER PRIVATE-MIRROR-OF-PUBLIC -- currently-private repos excluded at listing time; name/description mirror markers + created-after-window jointly catch private-mirror-of-public repos even if since made public.
3. PRIVATE→PUBLIC-LATER LIMITATION -- gh api reports only CURRENT visibility; a repo genuinely private in-window, not recreated, now public, with no marker is UNDETECTABLE with certainty. Flagged for human review (see Ambiguous section below) rather than silently kept.
4. temp- PREFIX -- any repo whose name starts with temp- is excluded (generalizes temp-sp-codex).
5. INTERNAL-UPSTREAM FORKS KEPT -- a fork is excluded only if its ultimate upstream owner is outside {prime-radiant-inc, obra}; forks of our own repos (e.g. superpowers-testing -> obra/superpowers) are kept.

See discovery-exclusions.log for every excluded repo + reason, and ambiguous-flags.log for every repo flagged (not excluded) under rule 3.

## Per-org totals

### prime-radiant-inc
- total public repos scanned: 51
- repos with ANY in-window activity (commits/PRs/releases): 15
- provably dormant (skipped clone/API, zero possible activity): 0
- empty repos (no commits ever): 0
- repos with fetch/clone errors: 0

### obra
- total public repos scanned: 224
- repos with ANY in-window activity (commits/PRs/releases): 8
- provably dormant (skipped clone/API, zero possible activity): 70
- empty repos (no commits ever): 0
- repos with fetch/clone errors: 0

## Total distinct repos with in-window activity: 23

### KEEP set (public, first-party, in-window-active)

- obra/LLM.swift
- obra/mutter-butter
- obra/narcolepsyd
- obra/pepper-x
- obra/private-journal-mcp
- obra/superpowers
- obra/superpowers-chrome
- obra/superpowers-marketplace
- prime-radiant-inc/clearance
- prime-radiant-inc/gauntlet
- prime-radiant-inc/greenfield
- prime-radiant-inc/hearthstone
- prime-radiant-inc/iterative-development
- prime-radiant-inc/iterative-development-example-ghost-pepper
- prime-radiant-inc/kindle-highlight-exporter
- prime-radiant-inc/prime-radiant-marketplace
- prime-radiant-inc/serf
- prime-radiant-inc/slackline
- prime-radiant-inc/sprout
- prime-radiant-inc/stockyard
- prime-radiant-inc/superpowers-testing
- prime-radiant-inc/terminal-bench-analysis
- prime-radiant-inc/ts-libghostty

## Ambiguous (flagged for human review, KEPT not excluded): 0

(none in this run's active set)

## Per-week totals (both orgs combined)

| Week | Repos active | Commits | Merged PRs | LOC +/- | Contributors | Releases |
|---|---|---|---|---|---|---|
| 1 | 10 | 241 | 2 | +862656/-542719 | 4 | 2 |
| 2 | 13 | 313 | 2 | +111912/-8625 | 6 | 1 |
| 3 | 11 | 221 | 13 | +76068/-55286 | 5 | 4 |
| 4 | 10 | 469 | 1 | +208227/-75905 | 4 | 0 |
