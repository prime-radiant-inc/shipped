# Week 4 brief — 2026-07-13 to 2026-07-19

**Counts:** 4 featured, 13 second-tier. (Facts only below — pulled verbatim from data/recon-8wk.json. Turn into prose separately.)

## Featured

### **obol** — Read an AI-agent transcript and estimate what it cost — a Rust core with C-ABI bindings for Python, Go, and TypeScript (Bun + Node).
- org: `prime-radiant-inc` · language: Rust · https://github.com/prime-radiant-inc/obol
- **release** `v0.8.0` "v0.8.0" published 2026-07-14T20:30:18Z
- commits to default branch this week: 4
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **teststrip** — macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
- org: `prime-radiant-inc` · language: Swift · https://github.com/prime-radiant-inc/teststrip
- **release** `v0.2.0` "v0.2.0" published 2026-07-13T00:32:14Z
- commits to default branch this week: 246
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **smevals** — A framework for running evals against small (and large) models
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/smevals
- **created** 2026-07-17T22:57:27Z
- **release** `0.2.0` "0.2.0" published 2026-07-18T05:52:36Z
- **release** `0.1.0` "0.1.0" published 2026-07-17T23:01:15Z
- commits to default branch this week: 30
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **blogosphere** — Local-first, multi-platform blogging client for an 11ty blog that lives in a GitHub repo — the repo is the database
- org: `obra` · language: TypeScript · https://github.com/obra/blogosphere
- **created** 2026-07-17T04:12:07Z
- commits to default branch this week: 35
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

## Also shipped (second-tier)

### **llm-proxy** — Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/llm-proxy
- commits to default branch this week: 11
- merged PRs this week: none (commits only)

### **serf** — A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/serf
- commits to default branch this week: 593
- merged PRs this week:
  - #41 "webui: edit or cancel an unconsumed queued message (fixes #23)" (merged 2026-07-19T23:42:05Z)
  - #38 "webui: per-message promote of queued follow-up to steering" (merged 2026-07-19T23:42:05Z)
  - #32 "agent: configurable delegate-turn limits, occupancy honesty, drive budget" (merged 2026-07-19T21:11:54Z)
  - #30 "web: open sidebar ⋯ menus as full-width modal sheet on mobile (#27)" (merged 2026-07-19T21:11:54Z)
  - #29 "Render subagent inline activity as the tool call's purpose" (merged 2026-07-19T21:11:54Z)
  - #28 "tool: guide purpose fields toward gerund-form activity phrases" (merged 2026-07-19T21:11:54Z)
  - #31 "webui: render user-sent steering as user messages, not system dividers" (merged 2026-07-19T21:11:54Z)
  - #16 "[codex] Render plugin-loaded events by kind" (merged 2026-07-13T03:50:21Z)

### **gauntlet** — AI-powered QA testing framework that uses LLMs (Claude or GPT) to test web apps, CLI tools, and TUI programs from markdown story cards, returning structured pass/fail verdicts with evidence.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/gauntlet
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **terminal-bench-analysis** — Fetches detailed JSON results from the Terminal Bench 2 leaderboard, loads them into SQLite, and publishes queryable analysis via Datasette.
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/terminal-bench-analysis
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **greenfield** — A Claude Code plugin that reverse-engineers clean behavioral specs, test vectors, and acceptance criteria from any codebase, producing a provenance trail so a fresh team can reimplement without inheriting the original's internal structure.
- org: `prime-radiant-inc` · language: [none set] · https://github.com/prime-radiant-inc/greenfield
- commits to default branch this week: 1
- merged PRs this week:
  - #3 "Restructure skills into directories with SKILL.md (fixes #2)" (merged 2026-07-14T19:25:29Z)

### **superpowers-evals** — Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/superpowers-evals
- commits to default branch this week: 89
- merged PRs this week:
  - #33 "PR #1998 campaign local phase: audits, hardening, codex precheck, route extension, 3 SDD probes (PRI-2650)" (merged 2026-07-17T17:50:45Z)
  - #31 "chore(container): agent-CLI refresh 2026-07-14" (merged 2026-07-14T22:09:23Z)
  - #29 "fix: make CI green — test hermeticity + container build fixes" (merged 2026-07-14T00:23:13Z)

### **claude-plugin-stats** — Daily scrape of Claude Code plugin install stats
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/claude-plugin-stats
- commits to default branch this week: 7
- merged PRs this week: none (commits only)

### **mlx-audio-swift** (fork) — A modular Swift SDK for audio processing with MLX on Apple Silicon
- org: `obra` · language: [none set] · https://github.com/obra/mlx-audio-swift
- commits to default branch this week: 4
- merged PRs this week: none (commits only)

### **msgvault** (fork) — Archive a lifetime of email and chat. Offline search, analytics, and AI query over your full message history. Powered by SQLite and DuckDB
- org: `obra` · language: [none set] · https://github.com/obra/msgvault
- commits to default branch this week: 8
- merged PRs this week: none (commits only)

### **remux** (fork) — Native iOS tmux client with a mobile-first UI for persistent terminal sessions.
- org: `obra` · language: [none set] · https://github.com/obra/remux
- commits to default branch this week: 25
- merged PRs this week: none (commits only)

### **remux-ghostty** (fork) — Upstream-based Ghostty repository for embeddable tmux control mode and Remux integration
- org: `obra` · language: [none set] · https://github.com/obra/remux-ghostty
- commits to default branch this week: 58
- merged PRs this week: none (commits only)

### **superpowers** — An agentic skills framework & software development methodology that works.
- org: `obra` · language: Shell · https://github.com/obra/superpowers
- commits to default branch this week: 0
- merged PRs this week:
  - #1998 "SDD fix-loop redesign: resume-based fix rounds, five-round breaker, controller adjudication, lifecycle restructure" (merged 2026-07-19T19:36:34Z)
  - #1994 "fix: make the codex packaging and SDD skill test suites pass reliably off-macOS" (merged 2026-07-19T19:04:46Z)
  - #1993 "fix(hooks): dispatch the SessionStart hook via Git Bash on Windows (shell: "bash")" (merged 2026-07-19T19:03:59Z)
  - #1943 "fix(sdd): plan-scoped workspace — per-plan artifact dirs, self-identifying ledger, end-of-plan cleanup" (merged 2026-07-19T19:03:19Z)
  - #1987 "test: realign antigravity + pi mapping assertions with pruned references" (merged 2026-07-15T18:10:56Z)
  - #1934 "refactor: strip social proof, self-selling, and recap detritus from 12 skills (eval-gated)" (merged 2026-07-14T22:02:17Z)
  - #1935 "refactor: reframe TDD's testing-anti-patterns as writing-good-tests" (merged 2026-07-13T21:25:56Z)
  - #1933 "refactor: modernize finishing-a-development-branch (discard demotion, worktree-path fix, rationalization table)" (merged 2026-07-13T21:25:33Z)
  - #1932 "refactor: fold index-style Integration sections into points of use" (merged 2026-07-13T21:25:09Z)

### **winpepper** — Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
- org: `obra` · language: C# · https://github.com/obra/winpepper
- commits to default branch this week: 3
- merged PRs this week:
  - #51 "Keep the app responsive during model downloads" (merged 2026-07-18T03:32:45Z)
  - #49 "Fix modifier-only hotkey capture and key swallowing" (merged 2026-07-18T03:28:07Z)

