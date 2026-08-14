# Week 2 brief — 2026-06-29 to 2026-07-05

**Counts:** 3 featured, 13 second-tier. (Facts only below — pulled verbatim from data/recon-8wk.json. Turn into prose separately.)

## Featured

### **agent-plugin-linear-use** — Keep AI-driven work tracked in Linear: a Claude Code / Codex skill + hook that find or create a ticket and move it through your workflow. A public example of how Prime Radiant works.
- org: `prime-radiant-inc` · language: Shell · https://github.com/prime-radiant-inc/agent-plugin-linear-use
- **created** 2026-06-30T17:52:10Z
- commits to default branch this week: 3
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **insanitty** — Native Linux (GTK4/libadwaita) terminal workspace manager — a port of Fantastty, built on embedded Ghostty with tmux-backed workspaces and a QUIC remote engine.
- org: `obra` · language: Swift · https://github.com/obra/insanitty
- **created** 2026-06-30T17:04:35Z
- commits to default branch this week: 90
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **superpowers** — An agentic skills framework & software development methodology that works.
- org: `obra` · language: Shell · https://github.com/obra/superpowers
- **release** `v6.1.1` "v6.1.1" published 2026-07-02T21:58:30Z
- **release** `v6.1.0` "v6.1.0" published 2026-06-30T18:42:18Z
- commits to default branch this week: 19
- merged PRs this week:
  - #1897 "Release v6.1.1: fix Codex SessionStart hook re-registration, add Codex portal packaging" (merged 2026-07-02T21:56:56Z)
  - #1874 "Release v6.1.0" (merged 2026-06-30T18:29:15Z)
  - #1881 "[codex] Preserve hooks in Codex package manifest" (merged 2026-07-01T00:48:33Z)
  - #1880 "chore(codex): remove orphaned session-start-codex hook + refresh hook docs" (merged 2026-07-01T00:28:14Z)
  - #1877 "[codex] Fix plugin manifest category" (merged 2026-07-01T00:27:34Z)
  - #1876 "[codex] Add Codex portal package script" (merged 2026-07-01T00:02:57Z)
  - #1879 "fix(codex): suppress SessionStart hook auto-discovery with empty hooks object" (merged 2026-06-30T22:52:20Z)
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

## Also shipped (second-tier)

### **llm-proxy** — Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/llm-proxy
- commits to default branch this week: 8
- merged PRs this week: none (commits only)

### **serf** — A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/serf
- commits to default branch this week: 959
- merged PRs this week:
  - #12 "Corpus refresh + coverage-floor ratchet (lifted off the crash branch)" (merged 2026-06-30T18:45:26Z)

### **superpowers-evals** — Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/superpowers-evals
- commits to default branch this week: 2
- merged PRs this week:
  - #28 "feat(credential): add pinned claude-sonnet-4-6 credential for the claude harness" (merged 2026-07-01T00:08:27Z)
  - #27 "feat(credential): add pinned claude-sonnet-5 credential for the claude harness" (merged 2026-06-30T22:47:38Z)

### **claude-plugin-stats** — Daily scrape of Claude Code plugin install stats
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/claude-plugin-stats
- commits to default branch this week: 14
- merged PRs this week: none (commits only)

### **teststrip** — macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
- org: `prime-radiant-inc` · language: Swift · https://github.com/prime-radiant-inc/teststrip
- commits to default branch this week: 589
- merged PRs this week: none (commits only)

### **agent-building-playbook** (fork) — [no description set on GitHub]
- org: `obra` · language: [none set] · https://github.com/obra/agent-building-playbook
- commits to default branch this week: 2
- merged PRs this week: none (commits only)

### **dotfiles** — [no description set on GitHub]
- org: `obra` · language: Shell · https://github.com/obra/dotfiles
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **freshell** (fork) — The Agentic IDE (or, the loving child of tmux and claude code)
- org: `obra` · language: [none set] · https://github.com/obra/freshell
- commits to default branch this week: 89
- merged PRs this week: none (commits only)

### **mlx-audio-swift** (fork) — A modular Swift SDK for audio processing with MLX on Apple Silicon
- org: `obra` · language: [none set] · https://github.com/obra/mlx-audio-swift
- commits to default branch this week: 4
- merged PRs this week: none (commits only)

### **msgvault** (fork) — Archive a lifetime of email and chat. Offline search, analytics, and AI query over your full message history. Powered by SQLite and DuckDB
- org: `obra` · language: [none set] · https://github.com/obra/msgvault
- commits to default branch this week: 12
- merged PRs this week: none (commits only)

### **remux** (fork) — Native iOS tmux client with a mobile-first UI for persistent terminal sessions.
- org: `obra` · language: [none set] · https://github.com/obra/remux
- commits to default branch this week: 6
- merged PRs this week: none (commits only)

### **remux-ghostty** (fork) — Upstream-based Ghostty repository for embeddable tmux control mode and Remux integration
- org: `obra` · language: [none set] · https://github.com/obra/remux-ghostty
- commits to default branch this week: 48
- merged PRs this week: none (commits only)

### **superpowers-marketplace** — Curated Claude Code plugin marketplace
- org: `obra` · language: [none set] · https://github.com/obra/superpowers-marketplace
- commits to default branch this week: 2
- merged PRs this week: none (commits only)

