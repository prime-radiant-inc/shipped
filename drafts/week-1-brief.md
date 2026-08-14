# Week 1 brief — 2026-06-22 to 2026-06-28

**Counts:** 3 featured, 14 second-tier. (Facts only below — pulled verbatim from data/recon-8wk.json. Turn into prose separately.)

## Featured

### **serf** — A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/serf
- **release** `snapshot` "Serf snapshot" (prerelease) published 2026-06-22T17:37:49Z
- **release** `v0.1.0` "v0.1.0" published 2026-06-22T19:16:15Z
- commits to default branch this week: 414
- merged PRs this week:
  - #11 "test(agent): maintainability cleanup — shared helpers, table-driving, file splits" (merged 2026-06-24T18:22:37Z)
  - #10 "perf(session): memoize per-session git/schema/uname work (~58% faster NewSession)" (merged 2026-06-24T05:57:34Z)
  - #8 "fix(atif): emit ATIF-v1.7 and make orphaned tool results conformant" (merged 2026-06-22T17:36:27Z)
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **toil** — File-defined workflow orchestrator in Go — YAML workflows and runners, disk-persisted state, resume, approvals, and live graph views
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/toil
- **created** 2026-06-23T02:16:47Z
- commits to default branch this week: 2
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **temp-sp-codex** — Temporary Superpowers Codex marketplace test repo
- org: `obra` · language: Shell · https://github.com/obra/temp-sp-codex
- **created** 2026-06-22T17:40:06Z
- commits to default branch this week: 2
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

## Also shipped (second-tier)

### **llm-proxy** — Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/llm-proxy
- commits to default branch this week: 7
- merged PRs this week: none (commits only)

### **gauntlet** — AI-powered QA testing framework that uses LLMs (Claude or GPT) to test web apps, CLI tools, and TUI programs from markdown story cards, returning structured pass/fail verdicts with evidence.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/gauntlet
- commits to default branch this week: 2
- merged PRs this week: none (commits only)

### **superpowers-evals** — Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/superpowers-evals
- commits to default branch this week: 90
- merged PRs this week:
  - #26 "fix(pi): coherent @earendil-works pi packages + drift-free eval-agent pins" (merged 2026-06-24T00:13:41Z)
  - #25 "Fix truncated sdd-svelte-todo-elicited plan; re-elicit with opus 4.8 and rename to -opus48" (merged 2026-06-23T02:01:53Z)
  - #24 "Add serf coding-agent harness" (merged 2026-06-23T02:01:50Z)

### **superpowers-autoresearch** — [no description set on GitHub]
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/superpowers-autoresearch
- commits to default branch this week: 5
- merged PRs this week: none (commits only)

### **claude-plugin-stats** — Daily scrape of Claude Code plugin install stats
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/claude-plugin-stats
- commits to default branch this week: 14
- merged PRs this week: none (commits only)

### **agent-building-playbook** (fork) — [no description set on GitHub]
- org: `obra` · language: [none set] · https://github.com/obra/agent-building-playbook
- commits to default branch this week: 6
- merged PRs this week: none (commits only)

### **freshell** (fork) — The Agentic IDE (or, the loving child of tmux and claude code)
- org: `obra` · language: [none set] · https://github.com/obra/freshell
- commits to default branch this week: 108
- merged PRs this week: none (commits only)

### **lace** — Lightweight agentic coding environment
- org: `obra` · language: TypeScript · https://github.com/obra/lace
- commits to default branch this week: 2
- merged PRs this week: none (commits only)

### **mlx-audio-swift** (fork) — A modular Swift SDK for audio processing with MLX on Apple Silicon
- org: `obra` · language: [none set] · https://github.com/obra/mlx-audio-swift
- commits to default branch this week: 5
- merged PRs this week: none (commits only)

### **msgvault** (fork) — Archive a lifetime of email and chat. Offline search, analytics, and AI query over your full message history. Powered by SQLite and DuckDB
- org: `obra` · language: [none set] · https://github.com/obra/msgvault
- commits to default branch this week: 16
- merged PRs this week: none (commits only)

### **narcolepsyd** — Idle power optimizer for Linux laptops with Intel hybrid CPUs
- org: `obra` · language: Rust · https://github.com/obra/narcolepsyd
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **remux** (fork) — Native iOS tmux client with a mobile-first UI for persistent terminal sessions.
- org: `obra` · language: [none set] · https://github.com/obra/remux
- commits to default branch this week: 15
- merged PRs this week: none (commits only)

### **remux-ghostty** (fork) — Upstream-based Ghostty repository for embeddable tmux control mode and Remux integration
- org: `obra` · language: [none set] · https://github.com/obra/remux-ghostty
- commits to default branch this week: 20
- merged PRs this week: none (commits only)

### **superpowers** — An agentic skills framework & software development methodology that works.
- org: `obra` · language: Shell · https://github.com/obra/superpowers
- commits to default branch this week: 0
- merged PRs this week:
  - #1846 "Remove Gemini CLI support (EOLed by Google)" (merged 2026-06-25T02:34:41Z)
  - #1829 "Add Codex marketplace manifest" (merged 2026-06-22T18:51:29Z)
  - #1847 "Prune per-harness tool-mapping boilerplate" (merged 2026-06-25T02:35:20Z)
  - #1845 "Remove Codex hooks" (merged 2026-06-25T02:33:57Z)
  - #1848 "Compress the using-superpowers bootstrap" (merged 2026-06-25T02:35:58Z)
  - #1838 "fix(codex): stop SessionStart bootstrap re-firing on resume (match Claude startup|clear|compact)" (merged 2026-06-23T23:15:57Z)

