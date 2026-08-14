---
title: "superpowers v6.2 and winpepper's alphas"
week: "Week of July 20, 2026"
dateStart: 2026-07-20
dateEnd: 2026-07-26
pubDate: 2026-07-26
summary: "superpowers ships v6.2.0, winpepper cuts its first two alphas, and lace gets full Anthropic-on-Bedrock parity."
---

A quieter week for new projects, a busy one for releases — and a big reliability push on winpepper.

<section class="featured">

## Featured

<article class="repo">

### [obra/superpowers](https://github.com/obra/superpowers) — v6.2.0

<p class="repo-desc">An agentic skills framework and software-development methodology that actually works.</p>

`v6.2.0` (Jul 24), on 51 commits. Alongside the release prep and notes, a real bug got fixed in systematic-debugging: `find-polluter.sh` had a `find -path` that never matched.

</article>

<article class="repo">

### [obra/winpepper](https://github.com/obra/winpepper) — v0.6.2-alpha, v0.7.0-alpha

<p class="repo-desc">Windows-native local dictation — hold a hotkey, speak, release. Parakeet TDT v3 ASR + LlamaSharp cleanup, all local.</p>

The heaviest week in the window for a single repo: 369 commits and two alphas on Jul 26. The merged work reads like a product hardening in real time — sleep/resume incident fixes with an error taxonomy, a council-reviewed dictation-reliability pass with AssemblyAI cloud ASR as a fallback, per-user MSI packaging, and keyboard-hook hardening.

</article>

</section>

<section class="second-tier">

## Also shipped

<article class="repo">

### [prime-radiant-inc/serf](https://github.com/prime-radiant-inc/serf)

<p class="repo-desc">The non-interactive coding agent.</p>

1,470 commits. Fork any message into the composer for editing, fold archived sessions behind one disclosure grouped by project, and prepopulate the session-path dropdown with recent projects.

</article>

<article class="repo">

### [obra/lace](https://github.com/obra/lace)

<p class="repo-desc">A lightweight agentic coding environment.</p>

Full Anthropic parity on AWS Bedrock via a new `AnthropicBedrockMantle`, plus treating SDK connection errors as retryable.

</article>

<article class="repo">

### [prime-radiant-inc/llm-proxy](https://github.com/prime-radiant-inc/llm-proxy)

<p class="repo-desc">The transparent LLM logging proxy.</p>

Added a SigV4 signing mode for the Anthropic-on-AWS passthrough (and an Apache-2.0 license).

</article>

<article class="repo">

### [prime-radiant-inc/stockyard](https://github.com/prime-radiant-inc/stockyard) · [prime-radiant-inc/superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals)

<p class="repo-desc">Steady work on the VM orchestrator and the eval lab.</p>

</article>

</section>
