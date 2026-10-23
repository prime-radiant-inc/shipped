# Narrative brief — week of 2026-10-19 (through 2026-10-23 afternoon/evening)

Grounded in `tools/gather.py --weeks 1 --window-end 2026-10-23T22:10:22Z`
(both orgs, `main`'s already-committed `gather.py` — the fork-inherited-
history compare-API fix (`c091ceb`) and the author/committer-date-basis fix
are both already in; nothing cherry-picked) + `tools/gen_stats.py`'s
extract, merged into `src/data/weekly-stats.json` as the single new
`2026-10-19` key (diffed against `main` before merging: 838 insertions, 0
deletions, confirmed no existing week's data touched) + 10 per-repo
`repo-report` runs (one per active repo) for full commit messages, PR
bodies, and release text. No numbers below — pure narrative; every figure
in the post renders from the `WeekSummary`/`RepoStat` widgets off
`src/data/weekly-stats.json`.

**Window is PARTIAL.** Frozen snapshot: 2026-10-23T22:10:22Z (today, Friday
afternoon/evening Pacific). The calendar week runs 2026-10-19 through
2026-10-25 (Mon–Sun); this data covers Monday through Friday evening only —
same partial-week pattern as every recent post.

**No gap week.** `week-of-2026-10-12.mdx` (post-accuracy-pass, at
`ffae15d`) is the newest post on `main`. This week is the very next
calendar week.

**Coverage:** 286 repos scanned (57 `prime-radiant-inc`, 229 `obra`), zero
fetch/clone errors, 10 repos with in-window activity — noticeably broader
than last week's 7: `prime-radiant-inc/llm-proxy` and
`prime-radiant-inc/github-triage` are new to this window (both have
appeared in earlier, non-consecutive weeks; neither was active last week),
and `obra/superpowers` + `obra/superpowers-marketplace` are active again
after being quiet recently.

**Org roster check:** live `GET /orgs/prime-radiant-inc/members` this run
returns the same eight logins as every recent week's check — `ada-sen`,
`arittr`, `cadence-sen`, `ketted`, `nora-primeradiant`, `obra`, `reeve-sen`,
`simonw`. No change.

**Contributor attribution, this week — resolved identities:**
- `obra` → **Jesse Vincent**, in-org (`prime-radiant-inc` member).
- `ada-sen` → **Ada Sen**, in-org.
- `arittr` → **Drew Ritter**, in-org.

All three are confirmed members of `prime-radiant-inc` at commit time (live
roster check, and every commit this window falls inside the last five
days, so current membership is a safe proxy for "at commit time" here, same
reasoning as recent weeks). **No outside human contributor landed or merged
anything this window.** `mhat` (former employee, staff only for his own
employed weeks) does not appear as a contributor anywhere this window —
checked, no commits under "mhat" or any variant name.

**Bot / unresolved identities, excluded from human attribution (same
treatment as prior weeks):**
- `dependabot[bot]`: 2 commits on `prime-radiant-inc/evener` (GitHub
  Actions version bumps, PRs #4639/#4641). Scheduled dependency bot, not a
  person.
- `github-actions[bot]`: all commits on `prime-radiant-inc/claude-plugin-stats`
  (8 commits — daily install-stats scrape + chart rebuild) and
  `prime-radiant-inc/terminal-bench-analysis` (2 commits — "Regenerate
  README (no new data)"). Scheduled bots, not people.
- `file-integrity <file-integrity@local>`: all 4 commits on
  `obra/muse-skills`. `GET /users/file-integrity` 404s — no GitHub account
  behind this identity, same automated daily-snapshot pattern flagged and
  left unattributed in the 2026-09-28, 2026-10-05, and 2026-10-12 briefs.
  Not confirmed as any specific human; not folded into "staff" or
  "outside."

**ZERO AMBIGUOUS CONTRIBUTORS THIS WEEK — nothing to list under ASK JESSE.**
Every human commit identity resolves cleanly to a confirmed
`prime-radiant-inc` member.

**One non-committer external mention, not a contributor:** `@tothanh317`
opened (but did not merge) PR #2610 against `obra/superpowers`
("docs(writing-skills): restructure SKILL.md...") — still open at snapshot
time. Not counted as a contributor since nothing of theirs shipped. Same
treatment as `sophieow`'s unmerged PR in the 2026-09-28 brief.

**Two tagged releases this week, very different in kind:**
- `prime-radiant-inc/evener` cut **three** releases this window —
  v0.3.14 (2026-10-19T03:19:22Z), v0.3.15 (2026-10-19T15:58:19Z), and
  v0.3.16 (2026-10-23T06:37:04Z). All three are bare version-number tags
  with GitHub's standard auto-generated "What's Changed" PR-list body (no
  hand-written notes) — consistent with every prior evener release
  checked. `gen_stats.py`'s featured-rule only needs one tagged release to
  flag a repo; evener qualifies on all three.
- `obra/superpowers` tagged **v7.0.1** (2026-10-21T21:05:11Z) with a real,
  hand-written release body (not auto-generated): a brainstorming-flow
  retune after user feedback on v7.0.0 (credits the issue reporter
  `@mbcrawfo` and a list of community testers by GitHub handle — none of
  whom have any commits in this window, so none are contributors, just
  acknowledged issue/testing credits), three long skills restructured to
  survive Claude Code's 20k-character compaction cutoff, and a
  contribution-template change requiring a human-written PR/issue summary.

**LOC suppression, applied per the established mechanical rule** (churn/
commits > 3000, or total churn > 100000 with min(add,rem)/max(add,rem) >
0.5 — rule from commit `02a56bd`, reused verbatim since):
- `obra/superpowers`: 2 commits, +927/-14379 = 15,306 churn ÷ 2 commits ≈
  7,653/commit — flagged. This is NOT a bot dump or vendored import like
  the muse-skills/evener-client-playdate precedents — it's a real
  `dev`→`main` release merge (PR #2581) that squash-merged ~12 PRs'
  worth of skills-directory restructuring (moving supporting docs into
  `references/` across three skills) into one commit, deleting far more
  than it added. Real work, but the mechanical per-commit-average rule
  catches it regardless of cause, same as it's meant to. `RepoStat`'s
  chip for this cell shows commit/PR/release counts only, no LOC diff.
  No other (week, repo) cell this window crosses either threshold —
  checked all 10 active repos; `prime-radiant-inc/evener` itself (94
  commits, +125,858/-15,075, ≈1,499/commit, total churn 140,933 but
  min/max = 15,075/125,858 ≈ 0.12, well under 0.5) does NOT trigger
  suppression despite its volume.

Applied by setting `loc_suppressed: true` on that one cell in the
machine-generated stats file and then running `python3 tools/gen_stats.py
--recompute-summaries src/data/weekly-stats.json` (recomputed only this
week's `summary.loc_added`/`loc_removed`; every other week's stored
numbers untouched, confirmed via the script's own diff output).

**No new repos created this week** (mechanical rule: `created_at` inside
the window, not a fork). Checked every active repo's `created_at` against
the 2026-10-19T00:00–2026-10-25T00:00 UTC window — none qualify. The two
"new to recent coverage" repos (`llm-proxy`, `github-triage`) were both
created well before this window (2026-01-13 and 2026-02-25 respectively);
they're just newly active again, not new repos, so they get the standard
"also shipped" treatment, not the featured new-repo slot.

**Featured this week (both via the release trigger, no new-repo trigger
fired): `prime-radiant-inc/evener` and `obra/superpowers`.**

**Window timezone, confirmed UTC** (same as every prior week's gather run
— `week_buckets()` anchors Monday 00:00 in `datetime.timezone.utc`
explicitly). No boundary-adjacent near-misses to flag this week — no repo
sits within a couple hours of the Monday 00:00 UTC cutoff the way
`maintaining-documentation`/`evener-client-playdate` did last week.

**`gather.py` vs `repo-report` commit-count mismatches, expected and
understood, not a bug:** `repo-report` buckets by **author date**;
`gather.py` deliberately buckets by **committer date** (fixed in
`15abdcb`/`6bd312d`, specifically to avoid dropping squash/rebase-merged
commits whose author date predates the window). This produces small,
expected differences this week — e.g. `prime-radiant-inc/llm-proxy` shows
7 commits in `gather.py`'s output vs 8 in `repo-report`'s, and
`prime-radiant-inc/evener` shows 94 vs 95. The widgets render `gather.py`'s
committer-date numbers (the canonical basis for this blog); `repo-report`
is used here only for narrative commit/PR/release content, not counts.

---

## Per-repo notes (source material for the post's prose)

### prime-radiant-inc/evener — FEATURED (3 tagged releases)

By far the most active repo again. Sole human author: Jesse Vincent
(`obra`, staff), plus 2 `dependabot[bot]` version-bump commits. 95 merged
PRs (repo-report count; `gather.py`'s committer-date count is what the
widget shows). Themes, grouped from the full merged-PR list:

- **LLM-gateway compatibility, a cluster of related PRs**: reading a
  gateway's per-model reasoning-effort ladder from `/models`, honoring a
  gateway's per-model "no-effort" verdict, reading a gateway's per-model
  dialect/token spelling, retrying a gateway in-band error frame instead
  of treating it as permanent, and recovering rejected JPEGs without
  losing the original image.
- **Provider-connection UI**: one card for provider connection in every
  state, plus two same-week fast-follow fixes (retry source + a race
  test, and further follow-ups).
- **A test-hardening sweep across many small, numbered backlog issues** —
  branch names are almost all `issue-NNNN-...`, each landing a targeted
  fix or test: transcript virtualizer prepend-measurement loop, memory
  search-result path scoping, duplicate overlay notices after Stop,
  notification body-entity escaping, mobile Back history-transition
  count, shellguard witness-failure sharing, cascadeguard's dotted
  ancestor spine, cross-tab display sync, composer async-projection
  timing (three separate PRs settling the same class of race before
  assertions run), activity-view geometry at phone widths, comment
  eviction beyond the reading cache limit, context-manager parked-search
  summaries, result-tool schema preservation across renames, detached
  TMPDIR handling, and a turn-gate revalidation race against a replaced
  transcript writer.
- **Delegate/plan work**: giving a delegate its whole plan at startup,
  then refactoring to one prompt per current step plus one plan per root
  workflow.
- **Native client**: iOS share-sheet session-attachment sharing, an
  Apple-convention iPhone design refinement, file links in assistant
  prose opening the Reader/document pane, queued-message edit/remove
  across browser and native, draft ownership preserved through an
  identity-changing resume, and resume/retry-recovery edge cases around
  queued/uncertain sends.
- **Hub**: endpoint configuration cleanup (plus a same-week fast-follow
  fixing "Low" findings from that cleanup), binary-install/restart split,
  connecting compatible hosts without forcing deployment.
- **Marketplace/plugins**: letting marketplace-add name a branch or tag,
  a fix keeping source-ref refusals typed through marketplace edits,
  preserving published plugin revisions for existing sessions, and
  keeping managed git metadata private.
- **Perf trims**: sharing immutable catalog capability maps, sharing
  floating-label pointer tracking and scoping hovercard cancellation to
  active gestures, deduplicating failed project lookups per capture,
  checking saved-session existence without hydration, skipping discarded
  totals on history pages, sizing transcript-index scan buffers to
  unread bytes, removing an unused request-history snapshot, and
  sampling context metrics/pressure once per publication.
- **Docs**: an audit of user guides publishing tested CLI/web tutorial
  tours, plus a same-week follow-up repairing the audit's own gaps.
- **Misc fixes**: onboarding auto-completes back to the draft after
  credential verification, SSH connections upgrade hosts reporting an
  incompatible protocol, paused attention no longer masks a failed turn,
  retirement admission skipped for superseded retry ticks, sessions
  restored when their temp dir is gone, and Send always resumes a fenced
  session on web/phone.

Three releases landed: v0.3.14, v0.3.15, v0.3.16 — all bare version tags,
auto-generated changelogs, no hand-written notes (standard evener pattern).

### obra/superpowers — FEATURED (1 tagged release, v7.0.1)

Sole author: Jesse Vincent (`obra`, staff). Only 2 commits land on `main`
in-window (12 PRs merged, but almost all target `dev`; see LOC-suppression
note above for why this cell's raw numbers are hidden). v7.0.1 retunes the
brainstorming skill after v7.0.0 user feedback: it now digs for existing
project/spec context before asking anything, asks better-targeted
follow-up questions instead of repeating a generic opener, only offers to
skip its questions when it started unprompted, and now lays out 2-3
approaches plus a short design doc before building (cut unapproved-build
skips from 24/24 to 3/24 in testing per the release notes). Three long
skills (`subagent-driven-development`, `writing-skills`,
`executing-plans`) had supporting docs moved into `references/` so they
survive Claude Code's 20k-character compaction cutoff intact. Issue/PR
templates now require a human-written summary, and the project will no
longer accept agent-written PRs fixing someone else's issue unless a
maintainer asked for one. Release notes credit issue-reporter
`@mbcrawfo` and community testers by handle — acknowledgments, not code
contributors; none of them have commits in this window.

### prime-radiant-inc/llm-proxy

Contributors: Ada Sen (`ada-sen`, staff) and Drew Ritter (`arittr`, staff).
3 merged PRs. Log-pruning defaults flipped to fully OFF (0 days / 0 bytes)
in the bare binary — Jesse's call that pruning should only be on by
default for colleague boxes via sen-core's docker-compose, which sets it
explicitly; previously 0/0 was still a live no-op (a background goroutine
still ran a pointless hourly sweep). Optional model-call correlation
(session/turn/logical-call IDs) is now carried through request-logging
captures, stripped from upstream/Platform-signed headers but preserved in
the local log. A real file-descriptor leak fixed: the Logger never closed
a per-session log file once opened, so descriptors grew unbounded and a
pruned/deleted file's disk space was never actually reclaimed while the
descriptor stayed open; files now close after 15 minutes idle or when a
session's date directory rolls over, reopening on the next write.

### prime-radiant-inc/github-triage

Contributors: Drew Ritter (`arittr`, staff) and Jesse Vincent (`obra`,
staff). 2 merged PRs. `apply-triage-actions` can now close an item as
completed or duplicate (previously everything closed as "not planned,"
losing the real reason and never linking duplicates to their canonical).
The session-id lookup now reads `CLAUDE_CODE_SESSION_ID` directly instead
of a fragile `ps|awk` pipeline that both mis-parsed Claude Code's `$N`
argument substitution and only worked when `claude` was launched with an
explicit `--session-id`. Jesse's commits add a label-proposal checker that
catches contradictions in cheap-model labelers' output before applying
them (found roughly 1-in-12 contradictions invisible by eye in a 343-item
pass), exempts maintainers from quality labels while still topically
labeling their items, and hardens the checker against silently-vanishing
corrections (typo'd override keys, type mismatches, last-wins collisions
on items proposed twice).

### prime-radiant-inc/prime-radiant-marketplace

Sole author: Jesse Vincent (`obra`, staff). 1 merged PR. Added the
`maintaining-documentation` plugin to the marketplace catalog, and fixed
two other entries (`shepherd-pr`, `study-skills`) that were added in
parallel with an earlier HTTPS fix and kept GitHub-SSH-style sources,
which fail to clone for anyone without a configured GitHub SSH key.

### obra/lace

Contributors: Drew Ritter (`arittr`, staff) and Jesse Vincent (`obra`,
staff). 5 merged PRs. Diagnostic model/worker-turn correlation IDs minted
at the conversation boundary and carried through provider retries and
compaction. Persona `@includes` can now fall back to embedder-supplied
default files when a user persona's include is missing locally (and the
fallback now correctly forwards to delegated subagents, a follow-up fixing
a gap the first version missed). Claude Haiku 5.5 added to the model
catalog and made the new default small model. Trusted execution-context
metadata (session/turn IDs) is forwarded to opted-in host MCP servers,
fails closed when the trusted IDs are absent, and was moved to a
runtime-owned namespace (`io.lace.execution`) rather than a shared one.

### prime-radiant-inc/claude-plugin-stats and prime-radiant-inc/terminal-bench-analysis

Bot-only again this window — `github-actions[bot]`'s daily scrape/rebuild
(claude-plugin-stats, 8 commits) and daily README regen with no new data
(terminal-bench-analysis, 2 commits). No human commits to attribute,
same treatment as every prior week these repos have appeared.

### obra/muse-skills

All 4 commits under the unresolved `file-integrity@local` identity — same
automated daily-snapshot pattern as every prior week. No human commits to
attribute.

### obra/superpowers-marketplace

Sole author: Jesse Vincent (`obra`, staff). 1 commit, no PRs: bumped the
pinned `superpowers` entry to v7.0.1 to match that repo's release this
window.
