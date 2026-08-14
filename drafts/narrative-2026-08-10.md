# Narrative brief — week of 2026-08-10 (through 2026-08-16)

Grounded in `data/recon-v2-8wk-20260814-CORRECTED.json` (week index 8) + `src/data/weekly-stats.json["2026-08-10"]`. Old draft: `src/content/posts/week-8.md`. No numbers below.

**Note on this week's data:** the correction fixed a truncation bug — the original snapshot froze partway through week 8; the corrected window now covers the full week. Some repo activity here may be slightly fuller than what the old draft saw.

## FEATURED

### prime-radiant-inc/clipfan
Clipboard sync daemon for Mac + remote tmux fleet. Mirrors macOS pasteboard to remote OS clipboards and tmux paste buffers. Enables image paste into Claude Code/Codex over SSH without OSC 52 or Xvfb.
**FEATURED — tagged release `v1.0.10`.**
- Headline: an outside contribution — cross-platform install support (per-OS tarballs, optional signing) — merged this week.
- Also: macOS mesh-onboarding repair (verify/repair the launchd daemon service during onboarding and app startup), documented manual build/signing modes, aligned release signing-gate comments.
No divergence vs old draft.

### prime-radiant-inc/agentic-usage-meter
macOS menu-bar meter for coding-agent subscription quotas.
**FEATURED — tagged release `v0.2.5`.**
- Outside contribution from a recognizable name (Joi Ito): hardened Claude's scoped per-model usage decoding, including decoding scoped per-model limits into labeled weekly windows.
- Also: moved release metadata under the Prime Radiant org.
No divergence vs old draft.

### prime-radiant-inc/everyharness
Generate a coding-agent plugin for every harness from one config file.
**FEATURED — new repo created this week + three commit-message-only version bumps (0.6.0, 0.7.0, 0.7.1).**
- Went from creation to a breaking "config v2" (tagged bootstrap, per-harness settings, a release section) in the same week, plus per-harness `emitHooks` control, exec-bit preservation checks for installed skill scripts, a `bump` command replacing per-repo version-bump scripts, and byte-exact dogfood regeneration against hand-written manifests.
- Adopted internally the same week by other repos (`the-elements-of-style`, `proving-it-works`) — already load-bearing.
No divergence vs old draft.

### prime-radiant-inc/everyharness-container
Multi-harness container: ~17 coding-agent CLIs preinstalled (shared by everyharness and superpowers-evals).
**FEATURED — new repo created this week.**
- Extracted from `superpowers-evals` into its own shared image: exact CLI inventory documented, image-size/platform note, first-build digest.
No divergence vs old draft.

### prime-radiant-inc/proving-it-works
Make a movie that proves your software actually works — three recording routes plus a checker that catches frozen pictures, desynced narration, and dropped words before you ship.
**FEATURED — new repo created this week.**
- Built end-to-end in days: three recording routes, an assembler, subtitles-by-default with a local voice fallback when there's no API key, and a checker that catches frozen frames/desynced narration/dropped words.
- Shipped the demo of itself, and picked up `everyharness` support the same week.
No divergence vs old draft.

### obra/superpowers
An agentic skills framework and software-development methodology that works.
**FEATURED — tagged release `v6.3.0`.**
- Release bundles Devin CLI and Hermes Agent support, a three-path brainstorming router, and SDD/Codex efficiency fixes; also updated to the Prime Radiant Community Code of Conduct.
No divergence vs old draft.

## SECOND-TIER

### prime-radiant-inc/serf
A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
**second-tier**, one merged PR.
- A top-to-bottom UX pass: keyboard flow, blocking-approval visibility, needs-you routing, shell chords, inline slash completion, and fixes from typical-user persona testing; dropped the old Conversation view in favor of collapsed action groups.
- Also (not in old draft): a merged PR clarifying and hardening shell execution modes.
No divergence vs old draft (enrichment only).

### prime-radiant-inc/superpowers-evals
Behavioral eval lab (Quorum) for the superpowers project.
**second-tier**, one merged PR.
- A "Quorum overhaul" program spec pushed through several reviewer rounds (column registry, quota graph, durability barriers, single sizing authority) plus an empirical OpenAI rate-limit probe showing no throttling at 20-way concurrency.
- Also: rebased its container on the new shared `everyharness-container` image, and added Claude subscription auth via OAuth token.
No divergence vs old draft.

### prime-radiant-inc/github-triage
Claude Code plugin for triaging GitHub issues and pull requests, with a security-gated PR review workflow.
**second-tier**, earliest steps.
- First two commits standing up the triage workflow.
No divergence vs old draft.

### prime-radiant-inc/slackline
A single-binary Go CLI that gives AI agents a Slack identity to send messages, read channels, and stream real-time events, with admin tooling to provision new bots.
**second-tier**, one merged PR (outside/ada-sen).
- Apache-2.0 license added.
No divergence vs old draft.

### prime-radiant-inc/awesome-superpowers
Community index for the superpowers ecosystem.
**second-tier**, two merged PRs.
- Populated with its initial curated list; an image-alignment fix followed.
No divergence vs old draft.

### obra/dotfiles
Jesse's personal dotfiles.
**second-tier.**
- Added a "proving-it-works-with-a-movie" skill, then retired it the next day once it shipped as a proper plugin.
No divergence vs old draft.

### obra/lace
Lightweight agentic coding environment.
**second-tier**, one merged PR.
- Crash-recovery centerpiece: an "interrupted" job status, a crash-recovery job listing scoped to the latest crash generation, and a per-process turn beacon (one flag file per agent process) with a regression test ensuring an idle beacon never clears a busy sibling's flag.
- Apache-2.0 license added (outside/ada-sen).
No divergence vs old draft.

### obra/private-journal-mcp
A lightweight MCP server that provides Claude with a private journaling capability to process feelings and thoughts.
**second-tier**, one merged PR (outside/ada-sen).
- MIT license added.
No divergence vs old draft.

### obra/superpowers-marketplace
Curated Claude Code plugin marketplace.
**second-tier**, minimal.
- Version bump tracking superpowers `v6.3.0`.
No divergence vs old draft.

### obra/the-elements-of-style
William Strunk Jr.'s Elements of Style (1918) in markdown format for AI agents.
**second-tier.**
- Packaged as an agent-installable plugin: adopted `everyharness` config v2, regenerated install docs, dropped the old session-start bootstrap.
No divergence vs old draft.

### obra/winpepper
Windows-native local dictation. Hold a hotkey, speak, release — cleaned-up words appear in the focused app. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.
**second-tier**, heavy volume, outside contributor (Dan Shapiro).
- ⚠ enrichment vs old draft: old draft covered only the week's last two items (dismiss pending click-to-paste on new recording, retry a flaky Windows-gate CI leg). The bulk of the week was actually a **user-configurable audio-history-retention feature** built behind an extensive fail-closed hardening effort: the history archiver now refuses destructive I/O on reparse points/junctions (so a junctioned history root can't get deleted through to an external target), validates index-writability before writing, and reports every skip rather than silently dropping recordings.
- The items old draft did name are real and are simply the most recent commits in the window.
