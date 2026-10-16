# Narrative brief — week of 2026-10-12 (through 2026-10-16 evening)

Grounded in `tools/gather.py --weeks 1 --window-end 2026-10-16T22:08:30Z`
(both orgs, `main`'s already-committed `gather.py` — the fork-inherited-
history compare-API fix is already in, per its own docstring; not
re-verified line-by-line this week since last week's brief already did
that and nothing in `gather.py` changed since) + `repo-report` runs against
each of the 7 active repos for the exact same window, used for commit
bodies, PR titles, and GitHub-login-resolved contributor attribution. No
numbers in this brief — pure narrative; every figure in the post renders
from the `WeekSummary`/`RepoStat` widgets off `src/data/weekly-stats.json`.

**Window is PARTIAL.** Frozen snapshot: 2026-10-16T22:08:30Z (today,
Friday evening). The calendar week runs 2026-10-12 through 2026-10-18
(Mon–Sun); this data covers Monday through Friday evening only — same
partial-week pattern as every recent post.

**No gap week.** `week-of-2026-10-05.mdx` is the newest post on `main`
(and deployed to `gh-pages`). This week is the very next calendar week.

**Coverage:** 286 repos scanned (57 `prime-radiant-inc`, 229 `obra`), zero
fetch/clone errors, 7 repos with in-window activity.

**Org roster check:** live `GET /orgs/prime-radiant-inc/members` this run
returns the same eight logins as last week's check — `ada-sen`, `arittr`,
`cadence-sen`, `ketted`, `nora-primeradiant`, `obra`, `reeve-sen`,
`simonw`. No change.

**Contributor attribution, this week:** every human commit across all 7
active repos this window was authored by **Jesse Vincent**, GitHub login
`obra` — confirmed in-org (member of `prime-radiant-inc`, employed at the
time of every one of these commits) via `repo-report`'s per-repo
contributor table on each of the 7 repos below. No outside contributor
landed or merged anything this window. No ambiguous identity requiring a
judgment call — **nothing to list under ASK JESSE this week.**

**Two bot-only / unresolved-identity repos, excluded from human
attribution (same treatment as prior weeks):**
- `prime-radiant-inc/claude-plugin-stats`: all 10 commits are
  `github-actions[bot]` (the daily install-stats scrape + chart rebuild).
  Flagged EXTERNAL by `repo-report`'s org-membership check, but it's the
  scheduled bot, not a person — no human to attribute.
- `obra/muse-skills`: all 4 commits are under git identity
  `file-integrity <file-integrity@local>`, UNRESOLVED (no linked GitHub
  account) — same automated daily-cadence identity flagged and left
  unattributed in the 2026-09-28 and 2026-10-05 briefs. Not confirmed as
  any specific human. No human commits to attribute.

**New repo this week (featured trigger):**
`prime-radiant-inc/evener-client-playdate`, created 2026-10-12 (first day
of window) — a native Playdate handheld client for evener, with voice
composition and direct Tailscale connectivity. Sole author: Jesse Vincent
(`obra`).

**No tagged releases this week.** Zero releases, zero tags landed in any
of the 7 active repos in-window (confirmed both via `gather.py`'s
`releases_in_window` field and `repo-report`'s per-repo releases/tags
sections — all read "(none)").

**Two near-misses on the "new repo" window, NOT featured:** both
`prime-radiant-inc/maintaining-documentation` (created 2026-10-11T22:46:05Z)
and `obra/picksandshovels` (created 2026-10-11T22:31:49Z) were created
roughly 1–1.5 hours before the Monday 00:00 UTC window-start cutoff —
correctly excluded by the mechanical rule, not a judgment call, but worth
knowing why they read as "also shipped" below rather than "featured."

**LOC suppression, applied per the established mechanical rule** (commit
02a56bd's rule, reused verbatim in 42f4a95: flag any (week, repo) cell
whose churn/commits > 3000, or whose total churn > 100000 with
min(add,rem)/max(add,rem) > 0.5):
- `prime-radiant-inc/evener-client-playdate`: churn 98,088 over 18
  commits (≈5,449/commit) — flagged. This is a brand-new repo's initial
  import plus first week of work, not representative "churn," so its
  `RepoStat` chip shows commit/PR counts only, no LOC diff.
- `obra/muse-skills`: churn 42,332 over 4 commits (≈10,583/commit) —
  flagged, consistent with every prior week this repo has appeared.

Applied by setting `loc_suppressed: true` on those two cells in the
machine-generated stats file and then running
`python3 tools/gen_stats.py --recompute-summaries src/data/weekly-stats.json`
to regenerate the week's summary LOC totals via the tool — never by hand
arithmetic.

---

## Per-repo narrative material

### prime-radiant-inc/evener

188 commits, 187 merged PRs, sole author Jesse Vincent (`obra`, in-org).
No releases this week (first evener week in a while with no tag). The
week's PRs cluster into a few sustained threads rather than one single
feature:

- **A large, sustained "copy-oracle" test-hardening campaign** spanning
  nearly the whole week and touching almost every subsystem — web, native,
  hub, agent, TUI, sandbox, frontend, appwire-client — converting tests
  that asserted on literal copy/wording into tests that assert on
  structural state, markers, error sentinels/types, or toast kinds
  instead. Accompanied by new tooling to catch regressions of the same
  kind: a "copy-oracle" inventory of wording-only tests, a CI ratchet
  against *new* copy-only tests, and that inventory tool itself later
  ported from Python to Go and TypeScript (retiring the original
  `inventory.py`).
- **Web UI migration onto the shared widget library**, done in explicit
  waves (an initial wave, a fast-follow, waves 2–3, a final follow-up, and
  "last leftovers") — moving web-frontend surfaces off bespoke markup and
  onto the shared widget components.
- **Device/mobile pairing work**: shared device invitations plus native
  Hub pairing, pairing destinations and device labels kept visible on
  narrow screens, automatic Hub destination discovery for mobile pairing
  without manual configuration, and clarified phone QR / sound-pairing
  comparison codes.
- **A per-test timing-budget "gate" hardened incrementally across the
  week**: failing loudly (instead of silently) on a malformed
  `testing-budget.json` — a non-object `packages` value, non-numeric
  package budgets, a non-object `perTestCeilingClasses`, an unusable class
  `ceilingSeconds` — then segmenting the per-test timing ceiling by test
  class and enforcing it, with a couple of runner-bound test classes
  returned to warn-only per a dated ruling (2026-10-14).
- **Entry-backed background transcripts**, landed as a feature through the
  legacy-retirement path and then followed by a repair pass addressing
  eleven defects the branch review found.

Alongside those: memory work (pages that say when to recall themselves,
`memory_write` taking `when`/`body` as fields, memory index lines linking
the page path instead of the title), execenv/sandbox read-capping (a
shared capped-read helper, budgeted/cancelable `list_dir` walks, capped
per-file reads in grep walks, pseudo-filesystem roots skipped), several
LLM/vision provider fixes (BMP/TIFF-to-PNG conversion for provider image
blocks, a single shared rule for wire image detail, sending
`thinkingLevel` vs. `thinkingBudget` to the right Google row shapes), hub
reliability fixes (breaking a relay read-acknowledgement deadlock,
preserving heartbeat writes during request intake, repairing
transcript-index sidecars off the daemonless read path), and a pair of
native UI changes landing right at the end of the window: Stop taking the
composer's slot with the status line lifting to the title, and a floating
compose button on the Board replacing its bottom bar.

Sole author throughout: **Jesse Vincent (`obra`, in-org)**.

### prime-radiant-inc/evener-client-playdate

New repo, created 2026-10-12 (Monday, first day of window) — a native
Playdate handheld client for evener, built via a `codex/...`-branched PR
workflow (14 merged PRs across the week, each opened and merged same-day
or next-day). The work: an initial qualified import of the native client
made independent of the main evener checkout, keeping enrollment
follow-up commands on the selected identity, documenting the public repo
with independent build-verification instructions, then a long run of
`codex/`-prefixed PRs refining device pairing (a shared full
device-pairing fingerprint, documented automatic Hub destinations,
clarified sound-pairing comparison codes), investigating and fixing
Playdate TCP stalls with work preserved across runtime recovery, reducing
read/send delays and idle redraws, loading conversation content through
history-inclusion flags, making long conversations readable sooner with
adjustable text, showing microphone input during setup-sound pairing,
decoding acoustic setup across symbol-timing offsets, and — toward the
end — producing and publishing onboarding media (a recorded walkthrough,
promo footage rendered from captured clips, the Playdate crank rendered
in its correct side-wall plane, both films embedded as inline README
video players). LOC is suppressed on this cell (new-repo import skews the
ratio) — see the "LOC suppression" note above; commit/PR counts are not
suppressed. No releases yet. Sole author: **Jesse Vincent (`obra`,
in-org)**.

### prime-radiant-inc/maintaining-documentation

Not a new repo by the mechanical rule (created ~1.5 hours before the
window-start cutoff — see note above), but a young one (7 total commits
in its history, 4 of which fall in this window) and the only repo this
week with a tagged minor-version PR (0.2.0). It's a coding-agent skill
for keeping a project's docs honest against the code. This window: a
copyedit pass that runs a fresh subagent against the project's bundled
Strunk guide and then a second pass checking the resulting word-diff for
changed claims (eval'd against 8 docs: the copyedited version won all 8
blind reader comparisons, and the drift check flagged 7 of roughly 210
changed sentences); the `writing-clearly-and-concisely` skill bundled in
wholesale from `obra/the-elements-of-style` (public-domain Strunk text);
that bundled skill then renamed to `copyediting-docs` to avoid colliding
with the standalone skill of a similar name, and its guide cut by about a
third (composition rules kept word-for-word, punctuation/usage trimmed by
deletion only, reaching parity against full-text copyedits in blind
judging). One merged PR (#1, "Reader-centered doc writing: reader brief,
doc types, reader test," tagging 0.2.0). Sole author: **Jesse Vincent
(`obra`, in-org)**.

### obra/lace

Small week: 2 commits, 2 merged PRs. A fix so a prompt retried after the
agent process died mid-turn gets a new turn run instead of being treated
as already-handled (the crash-recovery path's synthetic `process_died`
turn-end was shadowing the retry). And namespaced skill directories:
`SkillRegistry` now accepts `{ dir, namespace }` entries alongside bare
strings, every parsed skill version is kept under its qualified
(`namespace:name`) form, the embedder can pass namespaced `skillDirs`,
plugin skill dirs keep their plugin namespace while persona/bundled-core
dirs stay un-namespaced, and `<available_skills>`/`use_skill` resolve
either bare or qualified names (subagents inherit the parent's entries,
namespaces included). Sole contributor: **Jesse Vincent (`obra`,
in-org)**.

### obra/muse-skills

4 commits, all under the automated `file-integrity` identity (no linked
GitHub account) — same daily-cadence skills-snapshot pattern flagged and
left unattributed the last two weeks running. Not confirmed as any
specific human; no human commits to attribute. (For color, not
attribution: the snapshots this window touch consent-card wording
hardening across several app manifests, HealthKit/Health Connect doc
rewrites around the permission model, a booking-checkout policy rewrite
with explicit rules against collecting payment/document info in chat, and
a large filesystem reorg — `/opt/muse/skills` and
`/opt/hatch/workflow-skills` removed in favor of a new `/opt/muse/assets`
layout — which is the source of this repo's LOC-suppressed cell, not
newly-authored content.)

### obra/picksandshovels

Not a new repo by the mechanical rule (created ~2 hours before the
window-start cutoff), but young (first real week in its history) and a
personal project, not a company product — a pixel-art game ("sell the
GPUs, keep p(doom) under 100%"). 7 commits, no PRs (direct commits), no
releases. Work this window: sharing (one-click copy of image + linked
caption, separated image/text copy, a visible caption, native share
sheet) and analytics wiring — production-only Google Analytics with
game_start/game_end/share events, fuller journey analytics (screen views,
run milestones, yearly checkpoints, choices, bosses, quits/abandons, user
properties), moved onto a dedicated GA property, and a fix for a
double-counted page-view (the tag's automatic page_view alongside the
journey's own named screen-view). Sole author: **Jesse Vincent (`obra`,
in-org)**.
