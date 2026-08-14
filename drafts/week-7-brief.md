# Week 7 brief — 2026-08-03 to 2026-08-09

**Counts:** 4 featured, 26 second-tier. (Facts only below — pulled verbatim from data/recon-8wk.json. Turn into prose separately.)

## Featured

### **obol** — Read an AI-agent transcript and estimate what it cost — a Rust core with C-ABI bindings for Python, Go, and TypeScript (Bun + Node).
- org: `prime-radiant-inc` · language: Rust · https://github.com/prime-radiant-inc/obol
- **release** `v0.9.0` "v0.9.0" published 2026-08-05T19:03:05Z
- commits to default branch this week: 4
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **agentic-usage-meter** — macOS menu-bar meter for coding-agent subscription quotas
- org: `prime-radiant-inc` · language: Swift · https://github.com/prime-radiant-inc/agentic-usage-meter
- **release** `v0.2.4` "Agentic Usage Meter 0.2.4" published 2026-08-07T16:56:00Z
- **release** `v0.2.3` "Agentic Usage Meter 0.2.3" published 2026-08-07T00:05:34Z
- **release** `v0.2.2` "Agentic Usage Meter 0.2.2" published 2026-08-06T23:24:37Z
- **release** `v0.2.1` "Agentic Usage Meter 0.2.1" published 2026-08-05T06:52:43Z
- **release** `v0.2.0` "Agentic Usage Meter 0.2.0" published 2026-08-05T03:43:17Z
- **release** `v0.1.1` "Agentic Usage Meter 0.1.1" published 2026-08-03T02:48:04Z
- commits to default branch this week: 64
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **awesome-superpowers** — An agentic skills framework & software development methodology that works.
- org: `prime-radiant-inc` · language: [none set] · https://github.com/prime-radiant-inc/awesome-superpowers
- **created** 2026-08-04T19:51:21Z
- commits to default branch this week: 3
- merged PRs this week: none
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

### **superpowers-chrome** — Claude Code plugin for direct Chrome browser control via DevTools Protocol - zero dependencies
- org: `obra` · language: JavaScript · https://github.com/obra/superpowers-chrome
- **release** `v3.0.5` "v3.0.5 - Reliability and hardening across the MCP and CLI launch paths" published 2026-08-07T19:41:02Z
- **release** `v3.0.4` "v3.0.4 - Dependency security updates" published 2026-08-05T20:48:19Z
- **release** `v3.0.3` "v3.0.3 - Stringified JSON payloads work for structured actions" published 2026-08-05T20:34:17Z
- commits to default branch this week: 24
- merged PRs this week:
  - #43 "fix(mcp): honor stringified JSON payloads for structured actions (Postel's law)" (merged 2026-08-05T20:32:43Z)
- [needs prose/context from Ada: what shipped / why it matters — the JSON has no changelog or release-notes content]

## Also shipped (second-tier)

### **llm-proxy** — Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/llm-proxy
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **homebrew-tap** — Homebrew tap for Prime Radiant tools, including formulae for llm-proxy and beeper-message-sync.
- org: `prime-radiant-inc` · language: Ruby · https://github.com/prime-radiant-inc/homebrew-tap
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **stockyard** — Coding-agent VM orchestrator: runs coding agents in isolated VMs — Firecracker micro-VMs on Linux (with ZFS-based audit-trail snapshots) and Apple's container tool on macOS.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/stockyard
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **serf** — A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/serf
- commits to default branch this week: 1063
- merged PRs this week: none (commits only)

### **sprout** — Experimental self-improving multi-agent coding system: a root agent recursively decomposes goals and delegates to specialist subagents, learning from failures by mutating a git-backed agent genome. Supports Claude, GPT, and Gemini.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/sprout
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **gauntlet** — AI-powered QA testing framework that uses LLMs (Claude or GPT) to test web apps, CLI tools, and TUI programs from markdown story cards, returning structured pass/fail verdicts with evidence.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/gauntlet
- commits to default branch this week: 2
- merged PRs this week: none (commits only)

### **slackline** — A single-binary Go CLI that gives AI agents a Slack identity to send messages, read channels, and stream real-time events, with admin tooling to provision new bots.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/slackline
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **terminal-bench-analysis** — Fetches detailed JSON results from the Terminal Bench 2 leaderboard, loads them into SQLite, and publishes queryable analysis via Datasette.
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/terminal-bench-analysis
- commits to default branch this week: 3
- merged PRs this week: none (commits only)

### **openai-codex-plugins** (fork) — Curated collection of OpenAI Codex plugin examples (figma, notion, build-ios/macos/web-apps, expo, netlify, remotion, and more), each with a .codex-plugin manifest and optional skills, agents, commands, and MCP surfaces; forked for upstream submission.
- org: `prime-radiant-inc` · language: JavaScript · https://github.com/prime-radiant-inc/openai-codex-plugins
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **greenfield** — A Claude Code plugin that reverse-engineers clean behavioral specs, test vectors, and acceptance criteria from any codebase, producing a provenance trail so a fresh team can reimplement without inheriting the original's internal structure.
- org: `prime-radiant-inc` · language: [none set] · https://github.com/prime-radiant-inc/greenfield
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **books-for-bots** — Rust CLI that converts EPUBs into a single YAML-headed Markdown file with per-chapter byte and line offsets, giving LLM agents a navigation API for token-efficient reading.
- org: `prime-radiant-inc` · language: Rust · https://github.com/prime-radiant-inc/books-for-bots
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **superpowers-evals** — Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
- org: `prime-radiant-inc` · language: TypeScript · https://github.com/prime-radiant-inc/superpowers-evals
- commits to default branch this week: 92
- merged PRs this week:
  - #39 "Import locally-run eval results onto the appliance" (merged 2026-08-09T23:00:50Z)

### **clipfan** — Clipboard sync daemon for Mac + remote tmux fleet. Mirrors macOS pasteboard to remote OS clipboards and tmux paste buffers. Enables image paste into Claude Code/Codex over SSH without OSC 52 or Xvfb.
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/clipfan
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **superpowers-docs** — [no description set on GitHub]
- org: `prime-radiant-inc` · language: [none set] · https://github.com/prime-radiant-inc/superpowers-docs
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **superpowers-autoresearch** — [no description set on GitHub]
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/superpowers-autoresearch
- commits to default branch this week: 187
- merged PRs this week: none (commits only)

### **claude-plugin-stats** — Daily scrape of Claude Code plugin install stats
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/claude-plugin-stats
- commits to default branch this week: 8
- merged PRs this week: none (commits only)

### **toil** — File-defined workflow orchestrator in Go — YAML workflows and runners, disk-persisted state, resume, approvals, and live graph views
- org: `prime-radiant-inc` · language: Go · https://github.com/prime-radiant-inc/toil
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **agent-plugin-linear-use** — Keep AI-driven work tracked in Linear: a Claude Code / Codex skill + hook that find or create a ticket and move it through your workflow. A public example of how Prime Radiant works.
- org: `prime-radiant-inc` · language: Shell · https://github.com/prime-radiant-inc/agent-plugin-linear-use
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **teststrip** — macOS photo culling app — catalog-first, non-destructive, AI-assisted. Early development; not ready for use.
- org: `prime-radiant-inc` · language: Swift · https://github.com/prime-radiant-inc/teststrip
- commits to default branch this week: 40
- merged PRs this week: none (commits only)

### **smevals** — A framework for running evals against small (and large) models
- org: `prime-radiant-inc` · language: Python · https://github.com/prime-radiant-inc/smevals
- commits to default branch this week: 1
- merged PRs this week: none (commits only)

### **code-of-conduct** — This is the Prime Radiant Community Code of Conduct.
- org: `prime-radiant-inc` · language: [none set] · https://github.com/prime-radiant-inc/code-of-conduct
- commits to default branch this week: 3
- merged PRs this week:
  - #1 "Adapt Prime Radiant Community Code of Conduct" (merged 2026-08-03T20:44:44Z)

### **dotfiles** — [no description set on GitHub]
- org: `obra` · language: Shell · https://github.com/obra/dotfiles
- commits to default branch this week: 2
- merged PRs this week: none (commits only)

### **lace** — Lightweight agentic coding environment
- org: `obra` · language: TypeScript · https://github.com/obra/lace
- commits to default branch this week: 19
- merged PRs this week:
  - #364 "fix(catalog): a cached Anthropic catalog must not shadow new static metadata" (merged 2026-08-04T00:45:46Z)
  - #363 "feat(catalog): add claude-opus-5" (merged 2026-08-03T22:06:41Z)
  - #362 "fix(jobs): route job_kill --destroy through the shim even when untracked" (merged 2026-08-03T20:28:07Z)

### **superpowers** — An agentic skills framework & software development methodology that works.
- org: `obra` · language: Shell · https://github.com/obra/superpowers
- commits to default branch this week: 0
- merged PRs this week:
  - #2109 "docs: streamline README getting-started navigation" (merged 2026-08-08T00:37:17Z)
  - #1995 "feat: add Devin CLI support" (merged 2026-08-07T20:42:37Z)
  - #2006 "docs(brainstorming): correct Copilot CLI backgrounding guidance for Windows" (merged 2026-08-07T19:39:48Z)
  - #1919 "Docs/add grok build cli to readme" (merged 2026-08-07T19:39:06Z)
  - #2063 "feat(brainstorming): three-path router — ceremony scales, approval never does" (merged 2026-08-07T05:20:58Z)
  - #2086 "fix(planning): the spec travels with the plan" (merged 2026-08-06T22:13:54Z)
  - #2100 "fix(release): wire Hermes manifest into version bumps" (merged 2026-08-06T23:21:13Z)
  - #2089 "fix(sdd): reviewers re-read illegible evidence instead of re-running to regenerate it" (merged 2026-08-06T23:10:59Z)
  - #2024 "fix(finishing): check in with human partner when worktree removal hits untracked files" (merged 2026-08-06T19:21:46Z)
  - #1805 "fix(writing-skills): make render-graphs ESM-compatible and shell-free" (merged 2026-08-06T18:50:33Z)
  - #2064 "docs: codex-efficiency fix-cycle spec and plan (campaign record)" (merged 2026-08-06T06:17:22Z)
  - #2025 "feat(hermes): Hermes Agent harness support — eval-verified pre_llm_call bootstrap" (merged 2026-08-06T01:23:47Z)
  - #2080 "fix(sdd): preflight emits its checks as a ledger table and rules on what it surfaces" (merged 2026-08-04T21:22:58Z)
  - #2090 "docs: add README table of contents and move Community section higher" (merged 2026-08-05T03:16:47Z)
  - #2078 "fix(sdd): batch small same-shape tasks into one dispatch" (merged 2026-08-04T21:26:31Z)
  - #2077 "fix(sdd): rule and continue — non-catastrophic conflicts get ledgered rulings, not blocking questions" (merged 2026-08-04T21:16:17Z)
  - #2062 "fix(codex): explicit model+effort on every spawn, with config backstop" (merged 2026-08-04T21:04:31Z)
  - #2061 "fix(sdd,codex): event-driven bounded waits — 65-78% wait timeouts to 0%" (merged 2026-08-04T21:03:30Z)
  - #2060 "fix(codex): correct multi-agent guidance against the Codex source (V2)" (merged 2026-08-04T21:00:32Z)
  - #2059 "fix(sdd): dispatched subagents never dispatch subagents" (merged 2026-08-04T21:05:55Z)

### **superpowers-marketplace** — Curated Claude Code plugin marketplace
- org: `obra` · language: [none set] · https://github.com/obra/superpowers-marketplace
- commits to default branch this week: 3
- merged PRs this week: none (commits only)

### **winpepper** — Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
- org: `obra` · language: C# · https://github.com/obra/winpepper
- commits to default branch this week: 128
- merged PRs this week: none (commits only)

