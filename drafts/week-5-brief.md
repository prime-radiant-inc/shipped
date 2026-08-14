# Week 5 brief — 2026-07-20 to 2026-07-26

**Counts:** 2 featured, 15 second-tier. (Facts only below — pulled verbatim from data/recon-8wk.json. Turn into prose separately.)

## Featured

### **superpowers** — An agentic skills framework & software development methodology that works.
- org: `obra` · language: Shell · https://github.com/obra/superpowers
- **release** `v6.2.0` "v6.2.0" published 2026-07-24T00:28:17Z
- commits to default branch this week: 51
- merged PRs this week:
  - #2028 "Release v6.2.0" (merged 2026-07-24T00:27:17Z)
  - #2026 "Release v6.2.0 prep: release notes + version bumps" (merged 2026-07-23T23:16:32Z)
  - #2011 "fix(systematic-debugging): find-polluter.sh find -path never matches (fixes #2008)" (merged 2026-07-23T17:53:39Z)
  - #2010 "docs(using-superpowers): drop dangling subagent-support anchor" (merged 2026-07-23T17:47:44Z)
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **winpepper** — Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
- org: `obra` · language: C# · https://github.com/obra/winpepper
- **release** `v0.7.0-alpha` "v0.7.0-alpha" published 2026-07-26T17:15:29Z
- **release** `v0.6.2-alpha` "v0.6.2-alpha" published 2026-07-26T01:25:42Z
- commits to default branch this week: 369
- merged PRs this week:
  - #56 "Sleep/resume incident fixes: error taxonomy, recovery-driven clearing, hook reinstall" (merged 2026-07-25T04:50:33Z)
  - #55 "Docs: Cleanup UI scope clarification + pre-commit test policy" (merged 2026-07-24T06:40:35Z)
  - #54 "Consumer polish: toast policy, pill fixes, ASR config consolidation, live model swap" (merged 2026-07-24T06:02:36Z)
  - #53 "Dictation reliability, AssemblyAI cloud ASR, pending paste, and hardening (council-reviewed)" (merged 2026-07-23T19:00:52Z)
  - #52 "Keyboard hook fixes/hardening, per-user MSI, and cleanup-LLM fixes" (merged 2026-07-21T02:15:01Z)
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

## Also shipped (second-tier)

### **llm-proxy** — Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/llm-proxy
- commits to default branch this week: 4
- merged PRs this week:
  - #5 "fix: strip hop-by-hop headers before SigV4 signing (platform-aws 401)" (merged 2026-07-23T21:29:10Z)
  - #4 "feat: platform-aws SigV4 signing mode for anthropic passthrough" (merged 2026-07-23T20:47:22Z)
  - #3 "Add Apache-2.0 license" (merged 2026-07-23T17:32:28Z)

### **stockyard** — Coding-agent VM orchestrator: runs coding agents in isolated VMs — Firecracker micro-VMs on Linux (with ZFS-based audit-trail snapshots) and Apple's container tool on macOS.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/stockyard
- commits to default branch this week: 16
- merged PRs this week: none (commits only)

### **serf** — A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/serf
- commits to default branch this week: 1470
- merged PRs this week:
  - #62 "webui: fork any message into the composer for editing (#42)" (merged 2026-07-20T17:55:35Z)
  - #58 "webui: fold archived sessions behind one disclosure, grouped by project (#44)" (merged 2026-07-20T16:19:52Z)
  - #53 "webui,tui: prepopulate session path dropdown with 15 recent projects (#35)" (merged 2026-07-20T16:19:52Z)
  - #40 "hub: parse each job-notification block per notification turn (fixes #36)" (merged 2026-07-20T16:19:52Z)

### **terminal-bench-analysis** — Fetches detailed JSON results from the Terminal Bench 2 leaderboard, loads them into SQLite, and publishes queryable analysis via Datasette.
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/terminal-bench-analysis
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **superpowers-evals** — Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/superpowers-evals
- commits to default branch this week: 19
- merged PRs this week: none (commits only)

### **claude-plugin-stats** — Daily scrape of Claude Code plugin install stats
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/claude-plugin-stats
- commits to default branch this week: 7
- merged PRs this week: none (commits only)

### **teststrip** — macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
- org: `prime-radiant-inc` · language: Swift · https://github.com/prime-radiant-inc/teststrip
- commits to default branch this week: 3
- merged PRs this week: none (commits only)

### **smevals** — A framework for running evals against small (and large) models
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/smevals
- commits to default branch this week: 7
- merged PRs this week: none (commits only)

### **blogosphere** — Local-first, multi-platform blogging client for an 11ty blog that lives in a GitHub repo — the repo is the database
- org: `obra` · language: TypeScript · https://github.com/obra/blogosphere
- commits to default branch this week: 4
- merged PRs this week: none (commits only)

### **dotfiles** — [no description set on GitHub]
- org: `obra` · language: Shell · https://github.com/obra/dotfiles
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **lace** — Lightweight agentic coding environment
- org: `obra` · language: TypeScript · https://github.com/obra/lace
- commits to default branch this week: 5
- merged PRs this week:
  - #357 "fix(tests): skip integration suites on the model they actually use; fix compact fixture" (merged 2026-07-24T20:47:37Z)
  - #356 "fix(providers): treat SDK connection errors as retryable" (merged 2026-07-24T20:01:02Z)
  - #355 "feat(bedrock): full Anthropic parity via AnthropicBedrockMantle" (merged 2026-07-23T20:26:19Z)

### **mlx-audio-swift** (fork) — A modular Swift SDK for audio processing with MLX on Apple Silicon
- org: `obra` · language: [none set] · https://github.com/obra/mlx-audio-swift
- commits to default branch this week: 4
- merged PRs this week: none (commits only)

### **remux** (fork) — Native iOS tmux client with a mobile-first UI for persistent terminal sessions.
- org: `obra` · language: [none set] · https://github.com/obra/remux
- commits to default branch this week: 32
- merged PRs this week: none (commits only)

### **remux-ghostty** (fork) — Upstream-based Ghostty repository for embeddable tmux control mode and Remux integration
- org: `obra` · language: [none set] · https://github.com/obra/remux-ghostty
- commits to default branch this week: 5
- merged PRs this week: none (commits only)

### **superpowers-marketplace** — Curated Claude Code plugin marketplace
- org: `obra` · language: [none set] · https://github.com/obra/superpowers-marketplace
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

