# Week 3 brief — 2026-07-06 to 2026-07-12

**Counts:** 3 featured, 14 second-tier. (Facts only below — pulled verbatim from data/recon-8wk.json. Turn into prose separately.)

## Featured

### **books-for-bots** — Rust CLI that converts EPUBs into a single YAML-headed Markdown file with per-chapter byte and line offsets, giving LLM agents a navigation API for token-efficient reading.
- org: `prime-radiant-inc` · language: Rust · https://github.com/prime-radiant-inc/books-for-bots
- **release** `v0.1.1` "v0.1.1" published 2026-07-11T19:59:09Z
- **release** `v0.1.0` "v0.1.0" published 2026-07-11T19:19:20Z
- commits to default branch this week: 8
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **obol** — Read an AI-agent transcript and estimate what it cost — a Rust core with C-ABI bindings for Python, Go, and TypeScript (Bun + Node).
- org: `prime-radiant-inc` · language: Rust · https://github.com/prime-radiant-inc/obol
- **release** `v0.7.0` "v0.7.0" published 2026-07-09T01:18:39Z
- commits to default branch this week: 2
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **teststrip** — macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
- org: `prime-radiant-inc` · language: Swift · https://github.com/prime-radiant-inc/teststrip
- **created** 2026-07-10T16:26:17Z
- **release** `v0.1.0` "v0.1.0" published 2026-07-12T14:21:11Z
- **release** `models-v1` "Model assets v1" published 2026-07-11T02:17:49Z
- commits to default branch this week: 675
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

## Also shipped (second-tier)

### **stockyard** — Coding-agent VM orchestrator: runs coding agents in isolated VMs — Firecracker micro-VMs on Linux (with ZFS-based audit-trail snapshots) and Apple's container tool on macOS.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/stockyard
- commits to default branch this week: 2
- merged PRs this week:
  - #14 "Archive VM console logs on destroy" (merged 2026-07-11T04:41:07Z)

### **serf** — A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/serf
- commits to default branch this week: 964
- merged PRs this week: none (commits only)

### **gauntlet** — AI-powered QA testing framework that uses LLMs (Claude or GPT) to test web apps, CLI tools, and TUI programs from markdown story cards, returning structured pass/fail verdicts with evidence.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/gauntlet
- commits to default branch this week: 1
- merged PRs this week:
  - #13 "fix(models): give Claude 5 named-tier the full 16384 output cap" (merged 2026-07-09T06:45:35Z)

### **superpowers-evals** — Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/superpowers-evals
- commits to default branch this week: 79
- merged PRs this week: none (commits only)

### **claude-plugin-stats** — Daily scrape of Claude Code plugin install stats
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/claude-plugin-stats
- commits to default branch this week: 7
- merged PRs this week: none (commits only)

### **smevals** — A framework for running evals against small (and large) models
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/smevals
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **dotfiles** — [no description set on GitHub]
- org: `obra` · language: Shell · https://github.com/obra/dotfiles
- commits to default branch this week: 3
- merged PRs this week: none (commits only)

### **freshell** (fork) — The Agentic IDE (or, the loving child of tmux and claude code)
- org: `obra` · language: [none set] · https://github.com/obra/freshell
- commits to default branch this week: 30
- merged PRs this week: none (commits only)

### **lace** — Lightweight agentic coding environment
- org: `obra` · language: TypeScript · https://github.com/obra/lace
- commits to default branch this week: 3
- merged PRs this week:
  - #354 "fix: terminal job notification Slack hint + success-path inject-drain watermark" (merged 2026-07-11T20:31:18Z)

### **mlx-audio-swift** (fork) — A modular Swift SDK for audio processing with MLX on Apple Silicon
- org: `obra` · language: [none set] · https://github.com/obra/mlx-audio-swift
- commits to default branch this week: 3
- merged PRs this week: none (commits only)

### **msgvault** (fork) — Archive a lifetime of email and chat. Offline search, analytics, and AI query over your full message history. Powered by SQLite and DuckDB
- org: `obra` · language: [none set] · https://github.com/obra/msgvault
- commits to default branch this week: 23
- merged PRs this week: none (commits only)

### **remux** (fork) — Native iOS tmux client with a mobile-first UI for persistent terminal sessions.
- org: `obra` · language: [none set] · https://github.com/obra/remux
- commits to default branch this week: 45
- merged PRs this week: none (commits only)

### **remux-ghostty** (fork) — Upstream-based Ghostty repository for embeddable tmux control mode and Remux integration
- org: `obra` · language: [none set] · https://github.com/obra/remux-ghostty
- commits to default branch this week: 142
- merged PRs this week: none (commits only)

### **superpowers** — An agentic skills framework & software development methodology that works.
- org: `obra` · language: Shell · https://github.com/obra/superpowers
- commits to default branch this week: 0
- merged PRs this week:
  - #1959 "Revert "Remove Gemini CLI support" (restores Gemini CLI docs, reverts 711d895)" (merged 2026-07-10T15:58:09Z)

