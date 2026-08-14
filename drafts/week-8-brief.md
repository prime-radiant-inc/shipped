# Week 8 brief — 2026-08-10 to 2026-08-16

**Counts:** 6 featured, 14 second-tier. (Facts only below — pulled verbatim from data/recon-8wk.json. Turn into prose separately.)

## Featured

### **clipfan** — Clipboard sync daemon for Mac + remote tmux fleet. Mirrors macOS pasteboard to remote OS clipboards and tmux paste buffers. Enables image paste into Claude Code/Codex over SSH without OSC 52 or Xvfb.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/clipfan
- **release** `v1.0.10` "v1.0.10" published 2026-08-13T17:44:24Z
- commits to default branch this week: 14
- merged PRs this week:
  - #2 "release: v1.0.10" (merged 2026-08-13T17:39:44Z)
  - #1 "Feat/cross platform install" (merged 2026-08-13T17:37:00Z)
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **agentic-usage-meter** — macOS menu-bar meter for coding-agent subscription quotas
- org: `prime-radiant-inc` · language: Swift · https://github.com/prime-radiant-inc/agentic-usage-meter
- **release** `v0.2.5` "Agentic Usage Meter 0.2.5" published 2026-08-13T17:48:04Z
- commits to default branch this week: 2
- merged PRs this week:
  - #10 "Decode Claude's scoped per-model limits into labeled weekly windows" (merged 2026-08-13T17:28:57Z)
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **everyharness** — Generate a coding-agent plugin for every harness from one config file
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/everyharness
- **created** 2026-08-11T00:02:23Z
- commits to default branch this week: 149
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **everyharness-container** — Multi-harness container: ~17 coding-agent CLIs preinstalled (shared by everyharness and superpowers-evals)
- org: `prime-radiant-inc` · language: Dockerfile · https://github.com/prime-radiant-inc/everyharness-container
- **created** 2026-08-11T08:12:04Z
- commits to default branch this week: 3
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **proving-it-works** — Make a movie that proves your software actually works — three recording routes plus a checker that catches frozen pictures, desynced narration, and dropped words before you ship
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/proving-it-works
- **created** 2026-08-11T17:55:45Z
- commits to default branch this week: 9
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **superpowers** — An agentic skills framework & software development methodology that works.
- org: `obra` · language: Shell · https://github.com/obra/superpowers
- **release** `v6.3.0` "v6.3.0" published 2026-08-12T16:58:30Z
- commits to default branch this week: 1
- merged PRs this week:
  - #2122 "Update to Prime Radiant Community Code of Conduct." (merged 2026-08-12T22:31:43Z)
  - #2125 "Release v6.3.0: Devin CLI and Hermes Agent support, brainstorming three-path router, SDD/Codex efficiency fixes" (merged 2026-08-12T16:53:22Z)
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

## Also shipped (second-tier)

### **homebrew-tap** — Homebrew tap for Prime Radiant tools, including formulae for llm-proxy and beeper-message-sync.
- org: `prime-radiant-inc` · language: Ruby · https://github.com/prime-radiant-inc/homebrew-tap
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **serf** — A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/serf
- commits to default branch this week: 122
- merged PRs this week:
  - #64 "Clarify and harden shell execution modes" (merged 2026-08-10T03:35:03Z)

### **github-triage** — Claude Code plugin for triaging GitHub issues and pull requests, with a security-gated PR review workflow.
- org: `prime-radiant-inc` · language: [none set] · https://github.com/prime-radiant-inc/github-triage
- commits to default branch this week: 2
- merged PRs this week: none (commits only)

### **slackline** — A single-binary Go CLI that gives AI agents a Slack identity to send messages, read channels, and stream real-time events, with admin tooling to provision new bots.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/slackline
- commits to default branch this week: 2
- merged PRs this week:
  - #2 "chore: add Apache-2.0 LICENSE" (merged 2026-08-11T18:23:40Z)

### **superpowers-evals** — Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/superpowers-evals
- commits to default branch this week: 34
- merged PRs this week:
  - #42 "Rebase container on shared everyharness-container image" (merged 2026-08-12T06:16:50Z)

### **claude-plugin-stats** — Daily scrape of Claude Code plugin install stats
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/claude-plugin-stats
- commits to default branch this week: 6
- merged PRs this week: none (commits only)

### **smevals** — A framework for running evals against small (and large) models
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/smevals
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **awesome-superpowers** — An agentic skills framework & software development methodology that works.
- org: `prime-radiant-inc` · language: [none set] · https://github.com/prime-radiant-inc/awesome-superpowers
- commits to default branch this week: 5
- merged PRs this week:
  - #2 "Fixes image alignment" (merged 2026-08-12T04:38:33Z)
  - #1 "Create and populate Awesome Superpowers initial list" (merged 2026-08-11T04:06:47Z)

### **dotfiles** — [no description set on GitHub]
- org: `obra` · language: Shell · https://github.com/obra/dotfiles
- commits to default branch this week: 2
- merged PRs this week: none (commits only)

### **lace** — Lightweight agentic coding environment
- org: `obra` · language: TypeScript · https://github.com/obra/lace
- commits to default branch this week: 18
- merged PRs this week:
  - #365 "Add Apache-2.0 LICENSE" (merged 2026-08-11T18:23:03Z)

### **private-journal-mcp** — A lightweight MCP server that provides Claude with a private journaling capability to process feelings and thoughts
- org: `obra` · language: TypeScript · https://github.com/obra/private-journal-mcp
- commits to default branch this week: 2
- merged PRs this week:
  - #26 "Add MIT license file" (merged 2026-08-11T18:24:14Z)

### **superpowers-marketplace** — Curated Claude Code plugin marketplace
- org: `obra` · language: [none set] · https://github.com/obra/superpowers-marketplace
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **the-elements-of-style** — William Strunk Jr.'s Elements of Style (1918) in markdown format for AI agents
- org: `obra` · language: HTML · https://github.com/obra/the-elements-of-style
- commits to default branch this week: 5
- merged PRs this week: none (commits only)

### **winpepper** — Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
- org: `obra` · language: C# · https://github.com/obra/winpepper
- commits to default branch this week: 79
- merged PRs this week: none (commits only)

