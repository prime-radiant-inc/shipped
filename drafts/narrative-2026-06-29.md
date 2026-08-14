# Narrative brief — week of 2026-06-29 (through 2026-07-05)

Grounded in `data/recon-v2-8wk-20260814-CORRECTED.json` (week index 2) + `src/data/weekly-stats.json["2026-06-29"]`. Old draft: `src/content/posts/week-2.md`. No numbers below — pure narrative themes.

## FEATURED

### prime-radiant-inc/agent-plugin-linear-use
Keep AI-driven work tracked in Linear: a Claude Code / Codex skill + hook that finds or creates a ticket and moves it through your workflow. A public example of how Prime Radiant works.
**FEATURED — new repo created this week.**
- Initial public release of the linear-use plugin: a skill + hook that auto-finds-or-creates a Linear ticket for agent work and drives it through workflow states.
- Immediate adversarial-review pass tightened the initial cut.
- Housekeeping fix to the commit author email (deliberately public repo, so attribution matters).
No divergence vs old draft — matches.

### obra/insanitty
Native Linux (GTK4/libadwaita) terminal workspace manager — a port of Fantastty, built on embedded Ghostty with tmux-backed workspaces and a QUIC remote engine.
**FEATURED — new repo created this week.**
- Project stood up fast: Swift/GTK4 app skeleton, embedded Ghostty terminal, tmux control-mode protocol as the foundation.
- Core workspace features landed same-week: splits, tabs, browser tabs, session/layout persistence across restart, workspace rename/archive/trash, drag-reorder.
- Remote engine work: native Swift QUIC client, remote grid protocol port, remote workspace rendered in-GUI, interop-tested against the real helper.
- Packaging/CI stood up in parallel: Swift toolchain CI, `.tar.gz`/`.rpm` targets, MIT license matched to Fantastty, e2e regression screenshots refreshed repeatedly as features landed.
No divergence vs old draft — matches closely.

### obra/superpowers
An agentic skills framework and software-development methodology that works.
**FEATURED — tagged releases `v6.1.0` and `v6.1.1` this week.**
- ⚠ divergence vs old draft: old draft told this as an editorial density pass on the skill docs ("rationalization tables," trimming "Bottom Line"/"Remember" recaps). The corrected commit log shows the week's actual releases were about **Codex integration**, not prose editing: `v6.1.0` shipped a leaner per-session bootstrap, Codex marketplace install support, and removal of Gemini CLI support; `v6.1.1` followed with fixes to Codex `SessionStart` hook re-registration and new Codex portal packaging.
- Release v6.1.0 also pruned per-harness tool-mapping boilerplate and compressed the "using superpowers" bootstrap prose — this is the one thread that overlaps with the old draft's density narrative, but it's a minor part of the week, not the throughline.
- Release v6.1.1 was a run of small Codex-hook correctness fixes: manifest category, suppressing hook auto-discovery when the hooks object is empty, preserving hooks in the packaged manifest, portal package defaults.

## SECOND-TIER

### prime-radiant-inc/llm-proxy
Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
**second-tier** (commits/no tagged release, not created this week).
- Config-driven upstream allowlist (default-open) wired into the proxy at construction.
- Run-envelope-attributed logging routed through the synthetic-session path so requests carry attribution/provenance.
- Hardening: a "no-pollution" test for run-envelope attribution made load-bearing; review-driven follow-up fix.
No divergence vs old draft — matches.

### prime-radiant-inc/serf
A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
**second-tier** — one merged PR this week: "Corpus refresh + coverage-floor ratchet (lifted off the crash branch)."
- ⚠ divergence vs old draft: old draft told this week purely as a UI polish story (model picker, colorblind-safe status shapes, amber→blue recolor, Lucide icons). That work is real and did happen (dated at the very tail end of the week), but the corrected log shows it was a small slice of a much larger week dominated by a **fuzzing/coverage campaign**: a multi-phase push (schema-aware tool-arg fuzzing, failure→regression promoter, real-traffic corpus harvesting, whole-module coverage ratchets across llm/auth/agent/hub/TUI packages) that culminated in the merged "corpus refresh + coverage-floor ratchet" PR — the one actual merged PR of the week and the throughline the featured_reason data points to.
- Secondary, real thread: TUI/web polish — provider-grouped/prettified/badged model picker, colorblind-safe status vocabulary, recolor sweep, vendored Lucide icons. Landed but secondary to the coverage push.
- Also: settings UI refactor split into smaller per-concern files (appearance, notifications, transcript toggles), plus early self-healing tool-call repair work.

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
**second-tier**, two merged PRs this week (both credential additions).
- ⚠ divergence vs old draft: old draft described a "shoplist fixture / evidence scenario / honest-report scenario" storyline for this week. The corrected log shows none of that this week — the only actual work is two small PRs adding pinned Claude credentials (claude-sonnet-5, claude-sonnet-4-6) for the harness. The evidence-scenario story likely belongs to a different week and got misattributed under the old (buggy shallow-clone) data.
- What actually shipped: pinned-credential support so the eval harness can target specific Claude model versions reliably.

### prime-radiant-inc/claude-plugin-stats
Daily scrape of Claude Code plugin install stats.
**second-tier**, bot-only activity.
- Routine daily scrape + chart-data rebuild, entirely `github-actions[bot]`. No human-authored change this week.
No divergence vs old draft — matches.

### prime-radiant-inc/teststrip
macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
**second-tier** (heavy direct-push volume, no PRs/release yet).
- Week spans the project's earliest foundation work (Swift package bootstrap, asset/catalog domain model, SQLite catalog repository, decode/preview pipeline, folder-ingest planning) through to user-facing culling features by week's end.
- Core culling workflow matured fast: stack culling, signal-backed compare recommendations, compare "keep all," rapid-cull rationale copy.
- People/face-review workflow: manual review actions, naming selected photos, persisting confirmed people groups.
- Smart Collections became contextual and actionable (suggestion engine, preset composition, typed rules).
- Ongoing plan-doc discipline: "alpha plan" refreshed after nearly every feature slice, plus a source-availability/catalog benchmark harness.
No divergence vs old draft — matches (old draft's account, drawn from a smaller commit slice, is consistent with the fuller corrected picture).

### obra/dotfiles
Jesse's personal dotfiles (no description set on GitHub).
**second-tier**, minimal activity.
- Single snapshot commit; housekeeping, not feature work.
No divergence vs old draft.

### obra/superpowers-marketplace
Curated Claude Code plugin marketplace.
**second-tier**, minimal activity.
- Two version-bump commits pointing the marketplace listing at superpowers `v6.1.0` then `v6.1.1`.
No divergence vs old draft.
