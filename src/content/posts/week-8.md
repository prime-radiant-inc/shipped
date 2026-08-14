---
title: "clipfan and the fleet's clipboard"
week: "Week of August 10, 2026"
dateStart: 2026-08-10
dateEnd: 2026-08-16
pubDate: 2026-08-16
summary: "clipfan ships v1.0.10 with cross-platform install, and winpepper keeps up a heavy dictation-hardening pace."
---

The most recent week in this first batch — two releases: a new version of the superpowers framework, and a small, sharp tool that solves a very specific annoyance for anyone driving coding agents over SSH.

<section class="featured">

## Featured

<article class="repo">

### [prime-radiant-inc/clipfan](https://github.com/prime-radiant-inc/clipfan) — v1.0.10

<p class="repo-desc">A clipboard-sync daemon for a Mac plus a remote tmux fleet — mirrors the macOS pasteboard to remote OS clipboards and tmux paste buffers.</p>

`v1.0.10` (Aug 13), with cross-platform install landing this week. The reason it exists is concrete: it lets you paste an image into Claude Code or Codex over SSH without OSC 52 or an Xvfb hack. If you've ever tried to get a screenshot onto a remote box mid-session, you know exactly the pain this removes.

</article>

<article class="repo">

### [obra/superpowers](https://github.com/obra/superpowers) — v6.3.0

<p class="repo-desc">An agentic skills framework and software-development methodology that actually works.</p>

`v6.3.0` (Aug 12) — the framework's release for this window, on the back of the SDD-reliability work that landed the week before (event-driven bounded waits, Hermes harness support).

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [obra/winpepper](https://github.com/obra/winpepper)

<p class="repo-desc">Windows-native local dictation — hold a hotkey, speak, release. All local.</p>

Another 79-commit week of steady hardening — the dictation-reliability push that started in July hasn't let up.

</article>

<article class="repo">

### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) · [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style)

<p class="repo-desc">The curated plugin marketplace kept moving; and Strunk's <em>The Elements of Style</em> (1918) got a markdown edition meant for AI agents to read.</p>

</article>

</section>

<p class="post-meta">This is the first eight weeks. Going forward, expect one of these a week.</p>
