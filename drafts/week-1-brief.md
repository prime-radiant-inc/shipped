# Week 1 brief — 2026-06-22 to 2026-06-28

Facts only below, pulled verbatim from data/recon-v2-8wk-20260814.json. Every repo with ANY in-window activity this week is listed — this is exhaustive, not curated. Turn into prose separately; do not invent changelog content beyond what's here.

## Summary

- repos active: 11 (3 featured, 8 second-tier)
- commits: 133
- merged PRs: 12
- LOC: +445270/-5675 raw
- LOC (de-botted): same as raw — no bot/generated commits detected this week
- unique contributors: 4
- releases cut: 2

## Featured (created this week, or cut a release this week)

### **prime-radiant-inc/serf** — A non-interactive coding agent: give it a prompt and it reads, writes, runs commands, and searches code in a loop until the work is done, using native tool-calling across OpenAI, Anthropic, and Google models.
- language: Go · https://github.com/prime-radiant-inc/serf
- **FEATURED because:** release `snapshot` "Serf snapshot" (prerelease) published 2026-06-22T17:37:49Z; release `v0.1.0` "v0.1.0" published 2026-06-22T19:16:15Z
- commits this week: 0
- merged PRs this week (3):
  - #11 "test(agent): maintainability cleanup — shared helpers, table-driving, file splits" (merged 2026-06-24T18:22:37Z)
  - #10 "perf(session): memoize per-session git/schema/uname work (~58% faster NewSession)" (merged 2026-06-24T05:57:34Z)
  - #8 "fix(atif): emit ATIF-v1.7 and make orphaned tool results conformant" (merged 2026-06-22T17:36:27Z)
- authors this week: none (no commits)
- LOC this week: +0/-0
- full commit list: none (release/PR only this week)
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **prime-radiant-inc/toil** — File-defined workflow orchestrator in Go — YAML workflows and runners, disk-persisted state, resume, approvals, and live graph views
- language: Go · https://github.com/prime-radiant-inc/toil
- **FEATURED because:** created this week (2026-06-23T02:16:47Z)
- commits this week: 2
- merged PRs this week: none
- authors this week: Jesse Vincent (2)
- LOC this week: +111939/-32
- full commit list (2):
  - `6186901` Jesse Vincent 2026-06-23T11:32:54-07:00 — Rewrite `toil help` in tgwm style, grouped by audience (+101/-32, 1 file(s))
  - `2dfffe6` Jesse Vincent 2026-06-22T19:02:17-07:00 — Initial public release (+111838/-0, 519 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **obra/temp-sp-codex** — Temporary Superpowers Codex marketplace test repo
- language: Shell · https://github.com/obra/temp-sp-codex
- **FEATURED because:** created this week (2026-06-22T17:40:06Z)
- commits this week: 2
- merged PRs this week: none
- authors this week: Jesse Vincent (2)
- LOC this week: +35084/-9
- full commit list (2):
  - `23f3499` Jesse Vincent 2026-06-22T11:14:09-07:00 — Keep Codex hooks manifest in plugin metadata (+5/-9, 2 file(s))
  - `b27a590` Jesse Vincent 2026-06-22T10:32:59-07:00 — Add Codex marketplace manifest (+35079/-0, 175 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

## Also shipped (second-tier — active but not new/released this week)

### **prime-radiant-inc/llm-proxy** — Transparent logging proxy for LLM API traffic that auto-configures clients and records every request and response to Claude, OpenAI, and other providers for debugging, auditing, and analysis.
- language: Go · https://github.com/prime-radiant-inc/llm-proxy
- **second-tier:** had commits/merged PRs this week but was not created this week and cut no release this week
- commits this week: 7
- merged PRs this week: none
- authors this week: Drew Ritter (7)
- LOC this week: +34427/-135
- full commit list (7):
  - `72fa195` Drew Ritter 2026-06-28T16:49:24-07:00 — feat: route generic providers through run attribution envelope (+296/-27, 2 file(s))
  - `aef4ac9` Drew Ritter 2026-06-28T16:41:15-07:00 — feat: support canonical run envelope for mantle (+123/-30, 3 file(s))
  - `82eed86` Drew Ritter 2026-06-28T16:33:47-07:00 — feat: route bedrock traffic through run attribution envelope (+250/-8, 3 file(s))
  - `7d11c07` Drew Ritter 2026-06-28T16:27:55-07:00 — feat: support neutral run attribution metadata (+97/-15, 4 file(s))
  - `262c5b7` Drew Ritter 2026-06-28T16:23:07-07:00 — feat: add neutral run attribution envelope parser (+116/-0, 2 file(s))
  - `3a7dfcf` Drew Ritter 2026-06-22T17:28:49-07:00 — fix: log bedrock run provenance (+200/-55, 4 file(s))
  - `bacf5f3` Drew Ritter 2026-06-22T17:00:36-07:00 — fix: preserve configured log directory (+33345/-0, 85 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **prime-radiant-inc/gauntlet** — AI-powered QA testing framework that uses LLMs (Claude or GPT) to test web apps, CLI tools, and TUI programs from markdown story cards, returning structured pass/fail verdicts with evidence.
- language: TypeScript · https://github.com/prime-radiant-inc/gauntlet
- **second-tier:** had commits/merged PRs this week but was not created this week and cut no release this week
- commits this week: 2
- merged PRs this week: none
- authors this week: Jesse Vincent (2)
- LOC this week: +119822/-8
- full commit list (2):
  - `2449dfe` Jesse Vincent 2026-06-23T13:59:34-07:00 — fix(auth): pin apiKey:null in OAuth mode so the SDK sends Bearer only (+43/-8, 2 file(s))
  - `979a013` Jesse Vincent 2026-06-23T13:40:58-07:00 — feat(auth): support Claude subscription OAuth for the Anthropic client (+119779/-0, 567 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **prime-radiant-inc/superpowers-evals** — Behavioral eval lab (Quorum) for the superpowers project that drives real coding-agent CLIs (Claude, Codex, Gemini, Kimi, and more) through a QA agent and grades them on workflow compliance against scenario criteria and deterministic post-checks.
- language: TypeScript · https://github.com/prime-radiant-inc/superpowers-evals
- **second-tier:** had commits/merged PRs this week but was not created this week and cut no release this week
- commits this week: 91
- merged PRs this week (3):
  - #26 "fix(pi): coherent @earendil-works pi packages + drift-free eval-agent pins" (merged 2026-06-24T00:13:41Z)
  - #25 "Fix truncated sdd-svelte-todo-elicited plan; re-elicit with opus 4.8 and rename to -opus48" (merged 2026-06-23T02:01:53Z)
  - #24 "Add serf coding-agent harness" (merged 2026-06-23T02:01:50Z)
- authors this week: Jesse Vincent (75), Drew Ritter (16)
- LOC this week: +13483/-2912
- full commit list (91):
  - `aeeaeda` Jesse Vincent 2026-06-25T19:22:31-07:00 — fix(normalize/codex): attach usage per-turn so obol tiers each request correctly (+97/-44, 2 file(s))
  - `3053bf8` Jesse Vincent 2026-06-25T14:22:36-07:00 — fix(normalize/codex): attribute per-subagent token usage by model (+65/-4, 2 file(s))
  - `5ff3530` Jesse Vincent 2026-06-25T11:34:08-07:00 — test(appliance): poll for streamed chunks instead of a fixed 50ms delay (+18/-4, 1 file(s))
  - `793bffb` Jesse Vincent 2026-06-25T11:27:46-07:00 — fix(costs): never report gauntlet QA spend as the task's eval cost (+68/-25, 7 file(s))
  - `8d89fea` Drew Ritter 2026-06-25T09:53:38-07:00 — docs(experiments): dev full-suite 5-agent perf run (raw grid + costs) (+401/-0, 1 file(s))
  - `cfc2e3a` Drew Ritter 2026-06-24T22:03:43-07:00 — feat(credential): raise opencode_gpt5 max_concurrency to 5 (+3/-1, 1 file(s))
  - `92e618e` Jesse Vincent 2026-06-24T21:38:45-07:00 — test(setup-step): assert runSetup forwards QUORUM_SCENARIO_DIR (+14/-0, 1 file(s))
  - `94907cc` Jesse Vincent 2026-06-24T21:35:32-07:00 — refactor(quorum-check): match dispatched helper tokens, not raw substring (+24/-10, 2 file(s))
  - `6ea8d26` Jesse Vincent 2026-06-24T21:25:17-07:00 — docs: describe scenario-local fixtures and init_repo_from_fixtures (+15/-8, 2 file(s))
  - `2a59226` Jesse Vincent 2026-06-24T21:22:32-07:00 — feat(quorum-check): require fixtures/ for init_repo_from_fixtures scenarios (+40/-0, 2 file(s))
  - `ec8ddd5` Jesse Vincent 2026-06-24T21:18:03-07:00 — refactor(scenarios): move SDD fixtures into scenario dirs via init_repo_from_fixtures (+13/-83, 15 file(s))
  - `5cfa786` Jesse Vincent 2026-06-24T21:10:24-07:00 — feat(setup-helpers): plumb QUORUM_SCENARIO_DIR + register init_repo_from_fixtures (+78/-6, 7 file(s))
  - `0853f90` Jesse Vincent 2026-06-24T21:03:38-07:00 — feat(setup-helpers): add generic initRepoFromFixtures (+123/-3, 2 file(s))
  - `7912025` Jesse Vincent 2026-06-24T20:55:22-07:00 — docs(plan): scenario-local fixtures implementation plan (+740/-0, 1 file(s))
  - `7069b6b` Jesse Vincent 2026-06-24T20:48:21-07:00 — docs(spec): scenario-local fixtures design (+163/-0, 1 file(s))
  - `c984703` Drew Ritter 2026-06-24T19:01:04-07:00 — docs(experiments): f/codex-no-hooks release test + global-tool-mapping fix (+117/-0, 1 file(s))
  - `1939fbf` Drew Ritter 2026-06-24T18:31:50-07:00 — fix(scenario): global-tool-mapping passes native/no-file platforms (+33/-23, 1 file(s))
  - `41a8bb8` Drew Ritter 2026-06-24T18:27:16-07:00 — feat(credential): default proxied-endpoint concurrency to 5 (+7/-7, 1 file(s))
  - `d9ca7cc` Drew Ritter 2026-06-24T16:10:38-07:00 — docs(experiments): compress-bootstrap release test (4-agent sentinel + main baseline) (+139/-0, 1 file(s))
  - `e939254` Drew Ritter 2026-06-24T13:41:05-07:00 — fix(credential): cap proxied-endpoint concurrency at 2 to avoid throttle hangs (+7/-5, 1 file(s))
  - `2902723` Drew Ritter 2026-06-24T12:45:35-07:00 — feat(credential): raise openai_responses max_concurrency to 4 (+4/-1, 1 file(s))
  - `75ae750` Jesse Vincent 2026-06-24T08:57:47-07:00 — Merge wip/glm-load: fractals post() asserts checkout is on main (+0/-0, 0 file(s))
  - `d85bd1a` Jesse Vincent 2026-06-23T20:29:53-07:00 — fix(scenario): fractals post() asserts checkout is on main (+2/-0, 2 file(s))
  - `e9ddcf8` Drew Ritter 2026-06-23T17:40:07-07:00 — image: install serf from source (+25/-1, 3 file(s))
  - `0b3988d` Jesse Vincent 2026-06-23T17:33:57-07:00 — feat(pi): default pi to OpenAI gpt-5.5 (openai-codex), not OpenRouter GLM (+10/-10, 2 file(s))
  - `019820d` Jesse Vincent 2026-06-23T17:27:42-07:00 — feat(credential): pin pi OAuth provider (default pi -> openai gpt-5.5) (+36/-12, 4 file(s))
  - `bce82e1` Drew Ritter 2026-06-23T17:19:52-07:00 — test: align pi Dockerfile assertions (+2/-1, 1 file(s))
  - `50db9c1` Drew Ritter 2026-06-23T17:16:55-07:00 — evals: default pi to openrouter glm 5.2 (+59/-9, 5 file(s))
  - `25fe203` Jesse Vincent 2026-06-23T16:07:03-07:00 — chore(image): pin eval-agent CLI versions for a drift-free pi rebuild (+3/-3, 1 file(s))
  - `0833c7e` Jesse Vincent 2026-06-23T15:44:40-07:00 — fix(pi): install coherent @earendil-works/pi-coding-agent + pi-subagents in image (+2/-1, 1 file(s))
  - `e5621bd` Jesse Vincent 2026-06-23T15:27:11-07:00 — test(scenarios): C-visual no-visual-companion override pair (+113/-0, 7 file(s))
  - `2a23a70` Jesse Vincent 2026-06-23T15:22:04-07:00 — test(scenarios): pin OUT-path + E-sdd override spikes into the suite (+14/-12, 3 file(s))
  - `c7cc993` Jesse Vincent 2026-06-23T15:00:48-07:00 — test(scenarios): output-location + execution-mode override spikes (+105/-0, 6 file(s))
  - `a369d3d` Jesse Vincent 2026-06-23T14:49:41-07:00 — test(scenarios): add subagent-dispatch + global-tool-mapping scenarios (+120/-0, 6 file(s))
  - `e8031a8` Jesse Vincent 2026-06-23T14:49:41-07:00 — fix(pi): read workdir context files (drop obsolete --no-context-files) (+8/-2, 2 file(s))
  - `c9974a1` Jesse Vincent 2026-06-23T14:49:41-07:00 — test(scenarios): user-preference-overrides-skill eval suite (+420/-0, 22 file(s))
  - `24b0828` Jesse Vincent 2026-06-23T14:49:40-07:00 — feat(setup-helpers): inject-user-preference verb for ambient-file overrides (+171/-5, 6 file(s))
  - `7967d13` Jesse Vincent 2026-06-23T14:49:40-07:00 — test(scenarios): probe each harness's ambient instructions file (+57/-0, 3 file(s))
  - `502860d` Jesse Vincent 2026-06-23T15:01:31-07:00 — docs(glm): 2026-06-23 full-suite benchmark writeup + gauntlet OAuth host-env note (+108/-0, 2 file(s))
  - `ba6ff6c` Jesse Vincent 2026-06-23T15:01:30-07:00 — fix(scenario): sdd-svelte-todo post-check installs chromium first (+2/-2, 2 file(s))
  - `dd3d22d` Jesse Vincent 2026-06-23T15:01:30-07:00 — feat(matrix): scenario-level '# os:' eligibility; tag windows scenario (+87/-22, 5 file(s))
  - `af01c64` Jesse Vincent 2026-06-23T15:01:30-07:00 — fix(opencode): raise capture timeout 30s->90s for high concurrency (+7/-3, 2 file(s))
  - `ccadcc6` Jesse Vincent 2026-06-23T11:50:32-07:00 — fix(opencode): pass real provider through + let obol price (no $0 costs) (+118/-73, 5 file(s))
  - `1e665cf` Jesse Vincent 2026-06-23T11:19:31-07:00 — Merge origin/main (appliance run-all status) into main (+0/-0, 0 file(s))
  - `eac2026` Jesse Vincent 2026-06-23T11:16:15-07:00 — fix(opencode): route OpenAI first-party endpoint to @ai-sdk/openai (+111/-4, 3 file(s))
  - `33cf773` Jesse Vincent 2026-06-23T10:46:41-07:00 — Merge credential-axis (worktree-glm-benchmark) into main (+0/-0, 0 file(s))
  - `c92c787` Jesse Vincent 2026-06-23T10:28:11-07:00 — fix(credential): real pi_default model (gpt-5.5); opencode_gpt5 base_url; add openai_responses (codex-responses validation) (+18/-5, 1 file(s))
  - `c416ee1` Drew Ritter 2026-06-23T10:21:53-07:00 — appliance: keep run-all status usable while active (+165/-27, 10 file(s))
  - `d06ba96` Jesse Vincent 2026-06-23T10:14:06-07:00 — fix(antigravity): seed agy's real oauth token (antigravity-cli/antigravity-oauth-token), not oauth_creds.json (+106/-35, 2 file(s))
  - `dd165c5` Jesse Vincent 2026-06-23T09:33:02-07:00 — fix(credential): restore per-agent concurrency caps on credentials (incl. antigravity 429 protection) (+31/-0, 3 file(s))
  - `9736269` Jesse Vincent 2026-06-23T00:00:44-07:00 — docs(credential): correct limiterKey formula (base_url-or-name|api); add serf_default to README list (+7/-5, 2 file(s))
  - `418194f` Jesse Vincent 2026-06-22T23:55:57-07:00 — docs(credential): credential axis usage + GLM-5.2 experiment log (+237/-27, 6 file(s))
  - `7dfb126` Jesse Vincent 2026-06-22T23:44:26-07:00 — chore(credential): claude validation on default_credential; drop dead legacy auth branch (+72/-70, 5 file(s))
  - `aa53c37` Jesse Vincent 2026-06-22T23:32:26-07:00 — feat(credential)!: collapse claude-sonnet/claude-haiku into claude harness + credentials (+3/-43, 5 file(s))
  - `1864ad0` Jesse Vincent 2026-06-22T23:27:06-07:00 — fix(credential): dashboard places legacy os-less verdicts (default linux); credential-aware column highlight (+34/-7, 3 file(s))
  - `85b68af` Jesse Vincent 2026-06-22T23:18:53-07:00 — refactor(credential): identity from verdict.json/phase.json; delete run-dir name parsers; credential in dashboard/cost/grid (+1161/-547, 27 file(s))
  - `eeebeb4` Jesse Vincent 2026-06-22T22:47:27-07:00 — fix(credential): write credential into results.jsonl; parse agent YAML once per agent (+68/-25, 4 file(s))
  - `59ca614` Jesse Vincent 2026-06-22T22:38:54-07:00 — feat(credential): run-all matrix expands + skips on harnesses/os (+406/-72, 7 file(s))
  - `3609ce7` Jesse Vincent 2026-06-22T22:22:57-07:00 — feat(credential): scheduler keys on per-endpoint limiterKey; caps from credential (+354/-122, 7 file(s))
  - `8221422` Jesse Vincent 2026-06-22T22:04:12-07:00 — fix(credential): restore claude apiKeyHelper seeding (macOS prompt suppression) in both auth branches (+161/-16, 2 file(s))
  - `1b4c3a8` Jesse Vincent 2026-06-22T21:54:41-07:00 — feat(credential): claude/gemini model+auth from credential (+234/-30, 10 file(s))
  - `871a676` Drew Ritter 2026-06-22T21:47:31-07:00 — appliance: keep detached run-all alive across hup (+79/-9, 4 file(s))
  - `adbda10` Jesse Vincent 2026-06-22T21:36:51-07:00 — feat(credential): codex translator (subscription + api-key branches from credential) (+513/-69, 6 file(s))
  - `8ccbf23` Jesse Vincent 2026-06-22T21:19:18-07:00 — test(credential): opencode preflight config genuinely asserted (provider block + 0600 + model ref) (+53/-6, 1 file(s))
  - `5e33775` Jesse Vincent 2026-06-22T21:14:07-07:00 — feat(credential): opencode translator builds provider config from credential (+510/-84, 2 file(s))
  - `09aca0b` Jesse Vincent 2026-06-22T21:04:02-07:00 — fix(credential): pi maps missing-key to setup ProvisionError; omit empty model compat (+17/-9, 1 file(s))
  - `d4f91ca` Jesse Vincent 2026-06-22T20:57:29-07:00 — feat(credential): pi translator builds provider config from credential (+526/-324, 2 file(s))
  - `99ba032` Jesse Vincent 2026-06-22T20:47:57-07:00 — test(credential): split glm per-protocol (chat/responses); add ollama_local live-validation cred (+26/-2, 1 file(s))
  - `671936a` Jesse Vincent 2026-06-22T20:26:13-07:00 — fix(credential): resolve credentials.yaml via repoRoot; static Credential import (+7/-5, 1 file(s))
  - `fae2c51` Jesse Vincent 2026-06-22T20:17:23-07:00 — feat(credential): thread credential through run + verdict + run-dir (+212/-25, 9 file(s))
  - `0c93d23` Jesse Vincent 2026-06-22T19:58:32-07:00 — test(credential): clean up runtime_family check test; assert parse-error name (+12/-37, 1 file(s))
  - `75a1bdb` Jesse Vincent 2026-06-22T19:54:43-07:00 — feat(credential): quorum check validates credentials.yaml + default_credential (+359/-39, 3 file(s))
  - `9978bb3` Jesse Vincent 2026-06-22T19:43:49-07:00 — feat(credential): credentials.yaml + default_credential field (+102/-23, 20 file(s))
  - `a29458b` Jesse Vincent 2026-06-22T19:31:37-07:00 — test(credential): cover oauth + empty-explicit; simplify resolveCredentialName (+7/-3, 2 file(s))
  - `053e831` Jesse Vincent 2026-06-22T19:28:45-07:00 — feat(credential): name/api-key/limiterKey resolution (+102/-0, 3 file(s))
  - `b2fe94f` Drew Ritter 2026-06-22T19:22:25-07:00 — docs: keep appliance access details private (+35/-19, 4 file(s))
  - `b7f3807` Jesse Vincent 2026-06-22T19:20:43-07:00 — feat(credential): schema + credentials file parser (+86/-0, 2 file(s))
  - `f78a143` Jesse Vincent 2026-06-22T18:45:33-07:00 — plan: credential axis implementation (4 phases, TDD, from rev3 spec) (+479/-0, 1 file(s))
  - `7e8038e` Jesse Vincent 2026-06-22T18:42:29-07:00 — spec: credential axis — record sign-off on migration + run-id consolidation (+9/-6, 1 file(s))
  - `1bcfb75` Jesse Vincent 2026-06-22T18:39:52-07:00 — spec: credential axis design (rev3, post two adversarial reviews) (+386/-0, 1 file(s))
  - `b5a6f99` Jesse Vincent 2026-06-23T01:10:08+00:00 — refactor(scenario): rename sdd-svelte-todo-elicited -> sdd-svelte-todo-opus48 (+9/-9, 8 file(s))
  - `7725e3b` Jesse Vincent 2026-06-23T00:39:16+00:00 — fix(fixtures): re-elicit truncated sdd-svelte-todo-elicited plan with opus 4.8 (+1283/-775, 1 file(s))
  - `5ac10b8` Jesse Vincent 2026-06-23T01:55:48+00:00 — fix(capture): derive serf coding duration_ms from single-object ATIF export (+79/-16, 2 file(s))
  - `1f9a979` Jesse Vincent 2026-06-22T19:09:29+00:00 — fix(normalize/serf): price serf cache-creation tokens (+79/-2, 2 file(s))
  - `acbd2f6` Jesse Vincent 2026-06-22T18:01:20+00:00 — fix(checks): treat serf as a no-dedicated-install-check agent (+13/-0, 2 file(s))
  - `d6afdec` Jesse Vincent 2026-06-22T17:59:34+00:00 — docs: point Gauntlet location at the canonical repo, not a personal checkout (+3/-3, 3 file(s))
  - `2fb3024` Jesse Vincent 2026-06-22T17:52:53+00:00 — feat(agents): add serf coding-agent harness (+1057/-2, 13 file(s))
  - `84ee32a` Drew Ritter 2026-06-22T18:46:45-07:00 — appliance: wait for terminal live artifacts (+205/-12, 2 file(s))
  - `b7cc3dd` Drew Ritter 2026-06-22T18:12:48-07:00 — evals: make codex windows hook setup executable (+0/-0, 1 file(s))
  - `d15eece` Jesse Vincent 2026-06-22T18:11:34-07:00 — evals: require codex Windows hook override (+79/-16, 2 file(s))
  - `a13cd21` Jesse Vincent 2026-06-22T17:23:48-07:00 — evals: cover codex windows hook execution (+350/-2, 7 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **prime-radiant-inc/superpowers-autoresearch** — [no description set on GitHub]
- language: Python · https://github.com/prime-radiant-inc/superpowers-autoresearch
- **second-tier:** had commits/merged PRs this week but was not created this week and cut no release this week
- commits this week: 5
- merged PRs this week: none
- authors this week: Jesse Vincent (5)
- LOC this week: +90512/-0
- full commit list (5):
  - `4c48b5c` Jesse Vincent 2026-06-23T15:28:48-07:00 — feat(variants): bootstrap compression variant files (a-z) (+1523/-0, 17 file(s))
  - `bbd6f95` Jesse Vincent 2026-06-23T15:28:47-07:00 — docs(bootstrap-compression): experiment log + findings report (+746/-0, 2 file(s))
  - `22b75d7` Jesse Vincent 2026-06-23T15:28:47-07:00 — feat(harnesses): bootstrap-compression eval harness tooling (+1865/-0, 20 file(s))
  - `6164cae` Jesse Vincent 2026-06-23T15:00:48-07:00 — docs(user-override-evals): Phase 3 spike results (OUT + E reachable + honored) (+17/-0, 1 file(s))
  - `f7d57d8` Jesse Vincent 2026-06-23T14:50:55-07:00 — docs(user-override-evals): design, ambient-file probe runner, image-version snapshot (+86361/-0, 357 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **prime-radiant-inc/claude-plugin-stats** — Daily scrape of Claude Code plugin install stats
- language: Python · https://github.com/prime-radiant-inc/claude-plugin-stats
- **second-tier:** had commits/merged PRs this week but was not created this week and cut no release this week
- commits this week: 14
- merged PRs this week: none
- authors this week: github-actions[bot] (14)
- LOC this week: +3401/-2167
- full commit list (14):
  - `8d44f56` github-actions[bot] 2026-06-28T10:01:01+00:00 — Rebuild chart data (+1/-1, 1 file(s))
  - `aa5ff0d` github-actions[bot] 2026-06-28T10:01:00+00:00 — Update plugin stats 2026-06-28 (+92/-85, 1 file(s))
  - `e9af1cc` github-actions[bot] 2026-06-27T09:43:55+00:00 — Rebuild chart data (+1/-1, 1 file(s))
  - `41c7efd` github-actions[bot] 2026-06-27T09:43:55+00:00 — Update plugin stats 2026-06-27 (+694/-254, 1 file(s))
  - `00cbbe6` github-actions[bot] 2026-06-26T10:05:54+00:00 — Rebuild chart data (+1/-1, 1 file(s))
  - `072bb92` github-actions[bot] 2026-06-26T10:05:54+00:00 — Update plugin stats 2026-06-26 (+938/-591, 1 file(s))
  - `690d4ee` github-actions[bot] 2026-06-25T10:04:42+00:00 — Rebuild chart data (+1/-1, 1 file(s))
  - `5b158f5` github-actions[bot] 2026-06-25T10:04:42+00:00 — Update plugin stats 2026-06-25 (+591/-305, 1 file(s))
  - `80645a5` github-actions[bot] 2026-06-24T10:05:45+00:00 — Rebuild chart data (+1/-1, 1 file(s))
  - `c064eaf` github-actions[bot] 2026-06-24T10:05:44+00:00 — Update plugin stats 2026-06-24 (+576/-492, 1 file(s))
  - `48ba8b7` github-actions[bot] 2026-06-23T10:16:38+00:00 — Rebuild chart data (+1/-1, 1 file(s))
  - `5542cd1` github-actions[bot] 2026-06-23T10:16:38+00:00 — Update plugin stats 2026-06-23 (+450/-380, 1 file(s))
  - `0171cb3` github-actions[bot] 2026-06-22T10:54:57+00:00 — Rebuild chart data (+1/-1, 1 file(s))
  - `cd38dfc` github-actions[bot] 2026-06-22T10:54:52+00:00 — Update plugin stats 2026-06-22 (+53/-53, 1 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **obra/lace** — Lightweight agentic coding environment
- language: TypeScript · https://github.com/obra/lace
- **second-tier:** had commits/merged PRs this week but was not created this week and cut no release this week
- commits this week: 2
- merged PRs this week: none
- authors this week: Jesse Vincent (2)
- LOC this week: +105/-3
- full commit list (2):
  - `a8791b5` Jesse Vincent 2026-06-23T23:13:20+00:00 — merge: flip bare-text stop reminder to a directive on mid-turn inject (Slack steering fix A opt4) (+0/-0, 0 file(s))
  - `46346c2` Jesse Vincent 2026-06-23T22:26:14+00:00 — runner: flip bare-text stop reminder to a directive when a mid-turn inject was seen (+105/-3, 2 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **obra/narcolepsyd** — Idle power optimizer for Linux laptops with Intel hybrid CPUs
- language: Rust · https://github.com/obra/narcolepsyd
- **second-tier:** had commits/merged PRs this week but was not created this week and cut no release this week
- commits this week: 1
- merged PRs this week: none
- authors this week: Jesse Vincent (1)
- LOC this week: +1390/-0
- full commit list (1):
  - `11bbb09` Jesse Vincent 2026-06-28T16:36:13-07:00 — Suspend USB devices that report only a model number (+1390/-0, 8 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

### **obra/superpowers** — An agentic skills framework & software development methodology that works.
- language: Shell · https://github.com/obra/superpowers
- **second-tier:** had commits/merged PRs this week but was not created this week and cut no release this week
- commits this week: 7
- merged PRs this week (6):
  - #1846 "Remove Gemini CLI support (EOLed by Google)" (merged 2026-06-25T02:34:41Z)
  - #1829 "Add Codex marketplace manifest" (merged 2026-06-22T18:51:29Z)
  - #1847 "Prune per-harness tool-mapping boilerplate" (merged 2026-06-25T02:35:20Z)
  - #1845 "Remove Codex hooks" (merged 2026-06-25T02:33:57Z)
  - #1848 "Compress the using-superpowers bootstrap" (merged 2026-06-25T02:35:58Z)
  - #1838 "fix(codex): stop SessionStart bootstrap re-firing on resume (match Claude startup|clear|compact)" (merged 2026-06-23T23:15:57Z)
- authors this week: Jesse Vincent (6), Ada Sen (1)
- LOC this week: +35107/-409
- full commit list (7):
  - `777cc2f` Jesse Vincent 2026-06-24T19:23:47-07:00 — Compress the using-superpowers bootstrap (+16/-75, 1 file(s))
  - `e7ddc25` Jesse Vincent 2026-06-24T19:23:35-07:00 — Prune per-harness tool-mapping boilerplate (+2/-219, 5 file(s))
  - `711d895` Jesse Vincent 2026-06-24T19:23:23-07:00 — Remove Gemini CLI support (+4/-88, 6 file(s))
  - `640ce6c` Jesse Vincent 2026-06-24T19:23:09-07:00 — Remove Codex hooks (+0/-17, 2 file(s))
  - `879ae59` Ada Sen 2026-06-23T22:57:31+00:00 — fix(codex): stop bootstrap re-firing on resume (match Claude startup|clear|compact) (+1/-1, 1 file(s))
  - `d376057` Jesse Vincent 2026-06-22T11:14:09-07:00 — Keep Codex hooks manifest in plugin metadata (+5/-9, 2 file(s))
  - `add6a28` Jesse Vincent 2026-06-22T10:32:59-07:00 — Add Codex marketplace manifest (+35079/-0, 175 file(s))
- [needs prose/context from Ada: what this release/these commits actually mean for users — the JSON has no changelog or release-notes content, only commit subjects and PR titles]

