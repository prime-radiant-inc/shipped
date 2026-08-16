#!/usr/bin/env python3
"""
gather.py (v2) — EXHAUSTIVE commit-driven recon for the "Shipped" blog.

Pulls public-repo activity across:
  - prime-radiant-inc (a real GitHub *organization*)
  - obra              (a GitHub *user* account, NOT an org — GET /orgs/obra
                        404s; this script queries /users/obra/repos instead.)

for N calendar weeks (Mon-Sun buckets; see --window-end below for how the
window is anchored) and writes:
  - data/recon-v2-<weeks>wk-<YYYYMMDD>.json  (full per-repo, per-week data)
  - data/coverage-report.md                  (human-readable summary)

WHY v2 EXISTS — THE BUGS THIS FIXES
----------------------------------------
1. EXHAUSTIVENESS. v1 fetched commit/PR/release detail only for repos whose
   `pushed_at`/`created_at` looked like they might have activity, which is a
   *safe* filter (any push updates pushed_at, so pushed_at before the window
   guarantees zero in-window activity on any branch) — but v1's downstream
   reporting leaned on releases/PRs as the main signal and under-surfaced
   commit-only work. v2 enumerates EVERY repo and, for every repo not
   provably dormant, walks its actual commit log — not just PRs/releases —
   so a repo shipped via direct pushes to the default branch is counted.

2. FORK-INHERITED-HISTORY BUG. v1 asked GitHub's commits API for
   "commits on the default branch since/until X" — for a FORK, the default
   branch's history *is* the upstream project's history (that's what a fork
   is), so this counted upstream's ongoing development as the fork owner's
   own activity. Proven on `obra/freshell`: v1 showed ~90-100 commits/week
   even though the fork was created and never touched again. The real
   number, confirmed via GitHub's compare API
   (`repos/obra/freshell/compare/danshapiro:main...obra:main`), is
   ahead_by=0 — zero commits actually authored to the fork.
   v2's fix: for forks, only count commits *ahead of the parent's default
   branch* (via the compare API), never the shared/inherited history. A
   dormant fork now correctly reports zero commits regardless of how much
   the upstream project has shipped in the same window.

   HARDENING (this fix): the original v2 code only took this safe path when
   the per-repo GET returned a `parent` field. If that GET call itself
   *failed* (rate limit, transient network error, revoked scope — `ferr` in
   process_repo), the old code treated the failure identically to "no
   parent info" and fell back to an unfiltered `git log` of the whole
   default branch — silently reintroducing the exact v1 bug on every
   transient API hiccup. Fixed to: (a) never fall back to the unfiltered
   log on a fetch *error* — report zero and note the error instead; (b) for
   the genuinely-no-parent case (upstream deleted), bound the fallback log
   to commits authored after the fork's own creation date, since a fork's
   history before that date is by definition inherited, not fixing the
   fallback's blind spot to synced-after-creation history but closing the
   dominant "created once, never touched" overcount case.

3. MERGE-COMMIT LOC BUG. Local `git log --numstat` for a merge commit is
   normally empty (its content is fully represented by the non-merge
   commits on the branch it merged, which get their own correct numstat in
   the same walk) — but `clone_shallow`'s `--shallow-since` boundary is a
   calendar cutoff over the WHOLE reachable graph, and a merge's two parent
   chains can need different amounts of history to satisfy it. When one
   side needs more history than the shallow boundary allows, git's shallow
   negotiation can graft the merge commit itself as a synthetic root (no
   parents) instead of cutting cleanly behind both parents. `git log
   --numstat` diffs a parentless commit against an empty tree, so EVERY
   file in the repo at that point shows as a fresh addition — the whole
   tree's line count gets attributed to one commit, not a small overcount.
   Proven on `obra/lace`@`ad01889` (week of 2026-05-11): local numstat
   reported 459,422 additions / 0 deletions; GitHub's own commit API
   reports the real diff as 630/266. See fix_merge_commit_loc()'s docstring
   for the full diagnosis and why the fix is a GitHub-API-per-merge-commit
   fallback rather than `--no-merges`.

   The graft ERASES the real parent list, so detection can't be "does %P
   show 2+ hashes" (confirmed: inside the actual shallow clone, `ad01889`'s
   `%P` comes back empty, not two hashes) — it has to be "parent count !=
   1", catching both the 2-parent case (an untouched, correctly-diffless
   real merge) and the 0-parent graft case in one rule.
   v2's fix: every commit's parent count is captured from `git log`'s `%P`
   (see parse_git_log's `loc_untrusted` flag), and any commit whose parent
   count isn't exactly one has its local additions/deletions/files_changed
   UNCONDITIONALLY replaced by GitHub's own per-commit diff stats
   (fix_merge_commit_loc, called from both the non-fork and
   fork-no-parent-fallback clone paths — the only two paths that trust
   local `git log --numstat` at all; the fork-with-parent path already
   always uses the commits API and was never affected).

APPROACH
--------
- Non-fork repos: shallow `git clone --shallow-since=<window start - 3d>`
  of the default branch, then local `git log --numstat` for exact
  commit/author/date/LOC data. Cloning avoids one API call per commit for
  stats (`GET /commits/{sha}`), which would be prohibitively slow for
  high-velocity repos (some of these have 1000+ commits in 8 weeks). Merge
  commits are the one exception: their LOC always comes from a per-commit
  API call (fix_merge_commit_loc), never local numstat — see bug 3 above.
  Cheap in practice since merges are a small fraction of weekly commits.
- Fork repos: no clone of the (often much larger, unrelated-velocity)
  upstream. Uses the compare API to get the exact list of commits ahead of
  parent; only fetches per-commit stats for those (usually zero, sometimes
  a handful) via the commits API — cheap because ahead-of-parent commit
  counts are small even when the underlying fork's total history is huge.
- Releases: checked for every repo unconditionally (cheap; can exist
  without a fresh push if a human/script tags & publishes off an old ref).
- Merged PRs: only checked for non-dormant repos (a merge always produces a
  push, so this can't miss anything — same safe-filter logic as above).

WINDOW
------
Default: N Mon-Sun week buckets ending "now" (partial final week). For this
project we froze the window to match v1's original run exactly — pass
--window-end explicitly to reproduce or extend a specific dataset instead of
drifting with wall-clock time on every re-run.

CREDENTIALS
-----------
Same as v1: this script does not talk to the credential broker. Export
GH_TOKEN or GITHUB_TOKEN before running (obtained via the broker beforehand).

USAGE
-----
    GH_TOKEN=<token> python3 tools/gather.py --weeks 8 \\
        --window-end 2026-08-14T00:50:52Z

Requires `gh` and `git` on PATH.
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

ACCOUNTS = [
    {"login": "prime-radiant-inc", "kind": "org"},
    {"login": "obra", "kind": "user"},
]

# Owners we consider "ours" for fork-upstream purposes. A fork whose
# ultimate upstream owner is outside this set is EXTERNAL and gets excluded
# at discovery time -- see EXCLUSION RULES in process_repo() below. Per
# Jesse's directive (2026-08): work landing on a vendored/forked external
# codebase doesn't count as our shipping. KEEPS forks whose upstream is
# still one of these owners (e.g. prime-radiant-inc/superpowers-testing ->
# obra/superpowers) -- that's internal work moved between our own accounts,
# not adoption of someone else's project.
INTERNAL_OWNERS = {"prime-radiant-inc", "obra"}

# --- PUBLIC-ONLY / PRIVATE-MIRROR FINALIZATION (2026-08, per Jesse's ruling) ---
# Jesse's ruling on the batch-3 discovery rework: "Shipped" audits
# PUBLIC-repo activity only. The type=all experiment (see list_public_repos()
# below) that pulled private org repos into discovery is REVERTED here --
# it was explored to avoid under-counting real work, but the ruling is that
# a repo currently private is out of scope full stop, and a repo that is
# private-during-the-window-then-later-made-public is *still* out of scope
# for the window it was private in (most commonly: a private incident/
# security-issue mirror of a public repo, unfrozen and made public well
# after the fact). Two independent, fail-closed mechanisms enforce this:
#
#   (a) NEVER PRIVATE: the org/user listing itself is filtered to public
#       visibility only (list_public_repos), PLUS a defensive per-repo
#       filter right after fetch (see the `visibility_dropped` handling in
#       list_public_repos) in case a caller ever passes type=all again --
#       belt-and-suspenders, not just a query-string change.
#
#   (b) NEVER PRIVATE-MIRROR-OF-PUBLIC: even a repo that reads as public
#       RIGHT NOW can be a private mirror that was only unfrozen later
#       (these are often security-issue repos: embargoed while the issue is
#       live, made public post-disclosure). Two signals catch this, used
#       TOGETHER since neither alone is complete:
#         1. NAME_MIRROR_MARKERS / DESC_MIRROR_MARKERS (below): a repo whose
#            name or description says outright that it's a mirror/private
#            copy of something public.
#         2. The existing CREATED-AFTER-WINDOW rule (Rule 2 in process_repo):
#            most real-world private-mirror-made-public-later repos were
#            RE-CREATED (not just re-visibilitied) after the window, so
#            created_after_window already catches them without any name
#            heuristic at all.
#
#       HONEST LIMITATION (see AMBIGUOUS_SIGNALS below): `gh api` only ever
#       reports a repo's CURRENT visibility -- there is no general API for
#       "was this repo private on date X" short of an enterprise audit log
#       (checked: GET /orgs/{org}/audit-log 404s for this org's plan). So a
#       repo that was genuinely private during the window, was NOT recreated
#       (created_at predates the window), is public now, and carries none of
#       the name/description markers is UNDETECTABLE by this tool with
#       certainty. Rule 3 below flags such repos for a human rather than
#       silently keeping them.

# Rule 4: any repo whose name starts with this prefix is provisional/scratch
# by convention (generalizes the one-off "temp-sp-codex" case rather than
# hardcoding that single name) and is excluded regardless of visibility,
# fork status, or dates.
TEMP_NAME_PREFIX = "temp-"

# Rule 2b markers -- NAME is matched as case-insensitive SUBSTRING (a repo
# literally named e.g. "foo-private" or "security-mirror-bar"). DESCRIPTION
# is matched only against the specific curated PHRASE below, not the bare
# word "mirror": a bare-substring check on description text produced real
# false positives when validated against the live org/user listing --
# prime-radiant-inc/clipfan ("Mirrors macOS pasteboard to remote OS
# clipboards") and obra/wayback-restorer ("Wayback Machine mirror recovery
# toolkit") both use "mirror" as an ordinary English verb/noun describing
# what the TOOL does, not a marker that the REPO is a private mirror of a
# public one. obra/mirror-quickstart-go (a literal fork-flavored copy of a
# Google Mirror API quickstart) DOES legitimately fire the NAME rule below --
# accepted fail-closed, since it's an ancient, unrelated, ours-owned repo
# with no batch-3 relevance either way.
NAME_MIRROR_MARKERS = ("mirror", "-private", "private-branches", "-test-harness")
DESC_MIRROR_MARKERS = ("mirrors the public",)

# Rule 3 (ambiguous-flag, NOT an exclusion): weak, narrow signals that a
# public/pre-window repo might have been private in-window without tripping
# the hard markers above. Deliberately short and specific (not "security",
# which also matches ordinary security-tooling PRODUCTS like
# prime-radiant-inc/scenarios or .../github-triage) to keep the false-positive
# rate low enough that a flagged repo is actually worth a human's time.
AMBIGUOUS_NAME_DESC_SIGNALS = ("embargo", "disclosure", "cve-", "redacted", "incident-response")

# Populated by process_repo() every time it excludes a repo at discovery
# time. Dumped into the recon JSON's top-level "discovery_exclusions" key
# and a human-readable log file by main() -- never silent.
EXCLUSIONS = []

# Populated by process_repo() every time Rule 3 flags a KEPT repo as
# ambiguous (public now, pre-window created_at, no hard marker, but a weak
# signal or no signal at all was available to rule out an in-window private
# period with certainty). Never auto-excluded on this basis alone -- dumped
# for human review, same never-silent treatment as EXCLUSIONS.
AMBIGUOUS = []


# ---------------------------------------------------------------- plumbing --

def get_token():
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not tok:
        sys.exit(
            "ERROR: no GitHub token found in GH_TOKEN or GITHUB_TOKEN.\n"
            "Obtain one via Ada's credential broker (request_credential, "
            "host api.github.com, use=http) and export it before running "
            "this script."
        )
    return tok


def parse_dt(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def week_buckets(n_weeks, window_end):
    """Return n_weeks (start, end_exclusive) datetime tuples, Mon-Sun, the
    last one ending at window_end (partial week if window_end isn't a
    Monday 00:00)."""
    monday_this_week = (window_end - datetime.timedelta(days=window_end.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    buckets = []
    for i in range(n_weeks):
        start = monday_this_week - datetime.timedelta(weeks=(n_weeks - 1 - i))
        end = start + datetime.timedelta(days=7)  # exclusive
        buckets.append((start, end))
    return buckets


def bucket_index(dt, buckets):
    for i, (s, e) in enumerate(buckets):
        if s <= dt < e:
            return i
    return None


def gh_api(path, token, paginate=True):
    """Call `gh api <path>`, returning (data, error). data is always a list."""
    cmd = ["gh", "api", path]
    if paginate:
        cmd.append("--paginate")
    env = dict(os.environ)
    env["GH_TOKEN"] = token
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    if r.returncode != 0:
        if "404" in r.stderr:
            return None, "404"
        return None, r.stderr.strip()[:300]
    txt = r.stdout.strip()
    if not txt:
        return [], None
    try:
        data = json.loads(txt)
        return (data if isinstance(data, list) else [data]), None
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        out, idx = [], 0
        while idx < len(txt):
            chunk = txt[idx:].lstrip()
            if not chunk:
                break
            obj, end = decoder.raw_decode(chunk)
            out.extend(obj if isinstance(obj, list) else [obj])
            idx = len(txt) - len(chunk) + end
        return out, None


def run_git(cmd, cwd=None, timeout=180):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return False, "", "timeout"


# ------------------------------------------------------------- GitHub data --

def list_public_repos(login, kind, token):
    """REVERTED (2026-08, per Jesse's ruling finalizing batch-3 discovery):
    a prior version of this function hard-coded type=all for the org
    endpoint specifically to pull ~68 private prime-radiant-inc repos
    (brainstorm, drill, terminus, wishsong, superpowers-private, ...) into
    discovery, reasoning that Shipped should audit private org repos too.
    Jesse's ruling overrides that: Shipped is PUBLIC-repo activity only,
    full stop -- see the PUBLIC-ONLY / PRIVATE-MIRROR block above
    INTERNAL_OWNERS for the full reasoning (private-mirror-of-public repos,
    often security-issue mirrors, are exactly the case this reverts to
    excluding). Back to type=public for the org endpoint.

    User endpoint (/users/{user}/repos) -> type=owner (NOT all): tried
    all once and found it pulls in repos the user is a MEMBER of but
    doesn't own -- concretely, users/obra/repos?type=all returns
    prime-radiant-inc/agentic-usage-meter, .../github-triage, .../scribble,
    .../streamlinear (org repos obra has member access to). Those are
    already covered by the prime-radiant-inc org's own listing; including
    them again here would double-process and double-attribute them under
    org=obra in the output. owner restricts to repos obra actually owns.
    Separately verified (2026-08) that obra the user account owns zero
    private repos (type=all on the user endpoint returns 248 with zero
    private, vs. 224 under type=owner -- the extra 24 are exactly the
    member-access org repos above, all public), so type=owner was never
    silently hiding a private repo the way org type=public was.

    WHY THE ORG SIDE STILL FETCHES type=all AND FILTERS IN PYTHON, NOT
    type=public IN THE QUERY STRING: a query-string type=public silently
    omits every private repo with NO record that it ever existed --
    correct for what gets PROCESSED, but it means "never silent" (every
    exclusion logged with repo + reason) is unenforceable for the ~68
    currently-private prime-radiant-inc repos, since gather.py never even
    learns their names. So for the ORG we fetch the full type=all listing
    (same one the reverted version used) and apply the public-only filter
    ourselves, logging every private repo dropped to EXCLUSIONS exactly
    like any other discovery-time exclusion. Net effect on what gets
    PROCESSED is identical to type=public; the difference is purely that
    every drop now has a name and a reason instead of being invisible.
    """
    if kind == "org":
        endpoint, repo_type = f"orgs/{login}/repos", "all"
    else:
        endpoint, repo_type = f"users/{login}/repos", "owner"
    data, err = gh_api(f"{endpoint}?type={repo_type}&per_page=100", token)
    if err:
        sys.exit(f"ERROR: could not list repos for {login} ({kind}): {err}")

    public_only = []
    for r in data:
        is_private = r.get("private", False) or r.get("visibility") == "private"
        if is_private:
            reason = (
                f"not_public: repo is currently private (visibility={r.get('visibility')!r}) "
                "-- public-only discovery policy (Jesse's ruling); enumerated via type=all so this "
                "exclusion has a name and reason instead of being an invisible query-string omission, "
                "never silently skipped"
            )
            EXCLUSIONS.append({"repo": r["full_name"], "reason": reason})
            print(f"[discovery] EXCLUDE {r['full_name']}: {reason}", file=sys.stderr)
            continue
        public_only.append(r)
    return public_only


def get_full_repo(login, name, token):
    """Single-repo GET — needed for `parent` info on forks (the list
    endpoint doesn't include it)."""
    data, err = gh_api(f"repos/{login}/{name}", token, paginate=False)
    if err:
        return None, err
    return data[0], None


def get_releases(login, name, token, window_start, window_end):
    data, err = gh_api(f"repos/{login}/{name}/releases?per_page=100", token)
    if err:
        return [], err
    out = []
    for rel in data:
        pub = rel.get("published_at")
        if not pub:
            continue
        dt = parse_dt(pub)
        if window_start <= dt <= window_end:
            out.append(
                {
                    "tag": rel.get("tag_name"),
                    "name": rel.get("name"),
                    "published_at": pub,
                    "prerelease": rel.get("prerelease"),
                    "draft": rel.get("draft"),
                }
            )
    return out, None


def get_merged_prs(login, name, token, window_start, window_end):
    page = 1
    out = []
    while True:
        path = (
            f"repos/{login}/{name}/pulls?state=closed&sort=updated"
            f"&direction=desc&per_page=100&page={page}"
        )
        data, err = gh_api(path, token, paginate=False)
        if err:
            return None, err
        if not data:
            break
        stop = False
        for pr in data:
            merged_at = pr.get("merged_at")
            if merged_at:
                mdt = parse_dt(merged_at)
                if window_start <= mdt <= window_end:
                    out.append({"number": pr["number"], "title": pr["title"], "merged_at": merged_at})
            upd = pr.get("updated_at")
            if upd and parse_dt(upd) < window_start:
                stop = True
        if stop or len(data) < 100 or page > 10:
            break
        page += 1
    return out, None


def get_compare(login, name, base_owner, base_branch, head_branch, token):
    path = f"repos/{login}/{name}/compare/{base_owner}:{base_branch}...{login}:{head_branch}"
    data, err = gh_api(path, token, paginate=False)
    if err:
        return None, err
    return data[0], None


def get_commit_stats(login, name, sha, token):
    data, err = gh_api(f"repos/{login}/{name}/commits/{sha}", token, paginate=False)
    if err:
        return None, err
    d = data[0]
    stats = d.get("stats", {})
    return {
        "additions": stats.get("additions", 0),
        "deletions": stats.get("deletions", 0),
        "files_changed": len(d.get("files", []) or []),
    }, None


# ------------------------------------------------------------------ git log --

def clone_shallow(clone_url, branch, since_dt, dest):
    """Shallow-clone since (window start - 3 days). Falls back to a full
    clone if the shallow-since clone fails — observed on at least one small
    repo (`fatal: error processing shallow info: 4`), apparently a
    server-side quirk with very short histories; a full clone of a small
    repo is cheap anyway."""
    since_str = (since_dt - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    cmd = [
        "git", "clone", "--quiet", "--single-branch", "--branch", branch,
        f"--shallow-since={since_str}", clone_url, dest,
    ]
    ok, _, err = run_git(cmd, timeout=180)
    if ok:
        return True, None
    if os.path.isdir(dest):
        shutil.rmtree(dest, ignore_errors=True)
    # Fallback: full clone, no shallow-since.
    cmd_full = ["git", "clone", "--quiet", "--single-branch", "--branch", branch, clone_url, dest]
    ok2, _, err2 = run_git(cmd_full, timeout=180)
    if ok2:
        return True, None
    if os.path.isdir(dest):
        shutil.rmtree(dest, ignore_errors=True)
    return False, f"shallow_failed=({err.strip()[:120]}) full_failed=({err2.strip()[:120]})"


def git_log_numstat(repo_dir, since_dt, until_dt, ref_range="HEAD"):
    since_iso = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    until_iso = until_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    # %P (parent hashes) is included so parse_git_log can flag merge commits
    # (2+ parents) -- see MERGE-COMMIT LOC BUG in fix_merge_commit_loc()'s
    # docstring for why that flag matters: local numstat is not trustworthy
    # for merges.
    cmd = [
        "git", "log", ref_range, f"--since={since_iso}", f"--until={until_iso}",
        "--numstat", "--no-color",
        "--pretty=format:COMMIT\t%H\t%h\t%an\t%aI\t%P\t%s",
    ]
    ok, out, err = run_git(cmd, cwd=repo_dir, timeout=120)
    if not ok:
        return None, err
    return parse_git_log(out), None


def parse_git_log(text):
    commits = []
    cur = None
    for line in text.splitlines():
        if line.startswith("COMMIT\t"):
            if cur:
                commits.append(cur)
            parts = line.split("\t", 6)
            if len(parts) < 7:
                continue
            _, sha, short, author, date, parents, subject = parts
            n_parents = len(parents.split())
            cur = {
                "sha": sha, "short_sha": short, "author": author, "date": date,
                "subject": subject, "additions": 0, "deletions": 0, "files_changed": 0,
                # A normal, non-merge commit has EXACTLY one parent. Anything
                # else is untrustworthy for local-numstat LOC purposes:
                #   - 2+ parents: a real merge (git shows no diff for these
                #     locally without -m/-c, which is fine -- but flag it
                #     anyway so a genuine local diff, should one somehow
                #     appear, never gets trusted either).
                #   - 0 parents: EITHER the repo's real first-ever commit
                #     (rare, and cheap to re-verify) OR -- the actual bug
                #     this guards against -- a merge that a `--shallow-since`
                #     clone grafted as a synthetic root because one of its
                #     parent chains needed more history than the shallow
                #     boundary allowed. The graft ERASES the real parent
                #     list, so a plain "2+ parents" check can never catch
                #     this case -- it has to be "parents != 1". See
                #     fix_merge_commit_loc() for the full diagnosis.
                "loc_untrusted": n_parents != 1,
            }
        elif line.strip() and cur is not None:
            fields = line.split("\t")
            if len(fields) == 3:
                add, dele, _path = fields
                if add.isdigit():
                    cur["additions"] += int(add)
                if dele.isdigit():
                    cur["deletions"] += int(dele)
                cur["files_changed"] += 1
    if cur:
        commits.append(cur)
    return commits


def fix_merge_commit_loc(commits, login, name, token):
    """Replace the local (untrustworthy) numstat for every commit flagged
    `loc_untrusted` (parent count != 1) with GitHub's own per-commit diff
    stats, via the same `get_commit_stats` API call already used for fork
    ahead-of-parent commits.

    WHY THIS EXISTS -- MERGE-COMMIT LOC BUG
    ---------------------------------------
    `git log --numstat` (no `-m`/`-c`/`--diff-merges`) normally prints NO
    diff at all for an ordinary merge commit -- its content is already fully
    represented by the non-merge commits on the branch that got merged in,
    which appear separately in the same log walk with their own correct
    numstat. That's the normal, correct case, and it's why v2 never added
    `--no-merges`: doing so would also drop merge commits from the commit
    list entirely (subject lines used in the narrative briefs, commit
    counts, etc.), not just their (already-empty) diff.

    But `clone_shallow`'s `--shallow-since` boundary is a CALENDAR cutoff
    applied across the whole reachable graph, and a merge has two parent
    chains that can need very different amounts of history to satisfy it.
    When one side needs to go back further than the shallow boundary allows,
    git's shallow negotiation can land the graft point ON the merge commit
    itself rather than cleanly behind both parents -- i.e. the merge commit
    gets grafted as if it had NO parents (a synthetic root). `git log
    --numstat` for a parentless commit diffs it against an EMPTY tree, so
    EVERY file in the repo at that point shows as a fresh 100% addition --
    not a small double-count, but the entire tree's line count attributed to
    one commit.

    Proven on `obra/lace`@`ad01889` (week of 2026-05-11): local numstat
    reported 459,422 additions / 0 deletions for that merge; `.git/shallow`
    in the shallow clone showed it grafted as a root (`git log -1 --format
    %P` on it, INSIDE the shallow clone, returns empty -- zero parents, not
    two); GitHub's own commit API reports its real diff as 630 additions /
    266 deletions. Confirmed isolated to commits that hit this graft case --
    a full (non-shallow) clone of the same repo shows the merge itself
    contributing zero numstat lines, as normal, with the real 630/266
    correctly attributed to its actual second-parent commit instead.

    THE DETECTION HAS TO BE "parents != 1", NOT "parents >= 2": the whole
    point of the graft is that it ERASES the merge's real parent list down
    to zero, so a naive "does %P show 2+ hashes" check never fires for the
    exact commit that needs fixing -- confirmed empirically (see gather.py's
    test history / PR description): checking `%P` inside the actual shallow
    clone for `ad01889` returns an EMPTY string, not two hashes. Flagging
    every non-exactly-one-parent commit (0 or 2+) closes that gap. A 0-parent
    commit that's genuinely the repo's real first-ever commit gets the same
    treatment (one harmless extra API call that confirms the same small,
    correct number) rather than trying to cheaply distinguish the two cases
    locally, which the shallow clone doesn't have enough information for.

    FIX CHOICE: exclude-from-numstat (`--no-merges`) vs. GitHub-API fallback
    --------------------------------------------------------------------
    Both were considered. `--no-merges` is simpler (one flag) but (a) also
    removes merges from the commit walk entirely -- losing subject-line
    material like "Merge plan-6/packaging: ..." that the narrative briefs
    already lean on -- and (b) in the shallow-graft case, the merge's real
    content is on a now-*unreachable* second parent, so the corrected total
    would be 0, not the true 630/266: an undercount, not a match to GitHub's
    numbers. The API fallback here is more code but is the only option that
    actually satisfies "LOC matches GitHub's reported diff" for a merge
    commit, and it costs one extra API call per flagged commit found in a
    week's window (small: most weeks have a handful of merges, not
    thousands) -- the same amortized cost model the fork path already uses.
    """
    fixed, failed = [], []
    for c in commits:
        if not c.get("loc_untrusted"):
            continue
        stats, err = get_commit_stats(login, name, c["sha"], token)
        if err:
            # Do not fall back to the local (untrusted-for-merges) numstat --
            # that's the exact silent-reintroduction mistake this function
            # exists to avoid. Zero it out and record the miss instead.
            c["additions"] = 0
            c["deletions"] = 0
            c["files_changed"] = 0
            failed.append((c["short_sha"], err))
        else:
            c["additions"] = stats["additions"]
            c["deletions"] = stats["deletions"]
            c["files_changed"] = stats["files_changed"]
            fixed.append(c["short_sha"])
    return fixed, failed


# --------------------------------------------------------------- per-repo --

def summarize_commits(commits, buckets):
    """Bucket a flat commit list into per-week structures with author
    rollups and LOC totals."""
    weeks = [
        {"index": i + 1, "commit_count": 0, "commits": [], "authors": {}, "loc_added": 0, "loc_removed": 0}
        for i in range(len(buckets))
    ]
    unmatched = []
    for c in commits:
        dt = parse_dt(c["date"])
        bi = bucket_index(dt, buckets)
        if bi is None:
            unmatched.append(c)
            continue
        w = weeks[bi]
        w["commit_count"] += 1
        w["commits"].append(
            {
                "sha": c["short_sha"], "author": c["author"], "date": c["date"],
                "subject": c["subject"], "additions": c["additions"],
                "deletions": c["deletions"], "files_changed": c["files_changed"],
            }
        )
        w["authors"][c["author"]] = w["authors"].get(c["author"], 0) + 1
        w["loc_added"] += c["additions"]
        w["loc_removed"] += c["deletions"]
    return weeks, unmatched


def process_repo(login, kind, repo, token, buckets, window_start, window_end, tmp_root):
    name = repo["name"]
    is_fork = repo["fork"]
    is_archived = repo["archived"]
    default_branch = repo.get("default_branch")
    created_dt = parse_dt(repo["created_at"])
    pushed_at = repo.get("pushed_at")
    pushed_dt = parse_dt(pushed_at) if pushed_at else None

    created_in_window = window_start <= created_dt <= window_end
    # NOTE: intentionally NO upper bound (`<= window_end`) here. pushed_at
    # only needs to be >= window_start to prove in-window activity is
    # POSSIBLE — a push that happened well AFTER window_end (e.g. because
    # this script runs hours/days after the window closed and the repo kept
    # moving) says nothing about whether it was also active DURING the
    # window, so it must not be treated as a dormancy signal. Bug found via
    # obra/winpepper: its latest push (03:10 UTC) landed after this run's
    # frozen window_end (00:50 UTC same day), which an `<= window_end` check
    # wrongly read as "no push in window" and skipped a genuinely active
    # repo. Only `pushed_at < window_start` is a safe "definitely dormant"
    # signal (any commit in-window would itself be a push at/after
    # window_start).
    pushed_in_window = bool(pushed_dt and pushed_dt >= window_start)
    # Safe exhaustiveness filter — see module docstring point 1. This can
    # only ever skip repos with PROVABLY zero in-window activity.
    non_dormant = created_in_window or pushed_in_window

    entry = {
        "org": login,
        "name": name,
        "full_name": repo["full_name"],
        "description": repo.get("description"),
        "language": repo.get("language"),
        "html_url": repo["html_url"],
        "created_at": repo["created_at"],
        "created_in_window": created_in_window,
        "pushed_at": pushed_at,
        "fork": is_fork,
        "archived": is_archived,
        "default_branch": default_branch,
        "non_dormant": non_dormant,
        "fork_parent": None,
        "fork_ahead_by": None,
        "excluded": False,
        "exclude_reason": None,
        "fork_upstream": None,
        "ambiguous_flag": False,
        "ambiguous_reason": None,
        "notes": [],
    }

    errors = {}

    # ---------------------------------------------------------- EXCLUSION RULES --
    # Applied at DISCOVERY time, before any window/commit/PR/release analysis,
    # so an excluded repo never makes it into weekly-stats.json "by
    # construction" -- not because it happens to have zero commits, but
    # because we refuse to attribute ANY of its activity to us. Every drop is
    # logged (never silent): see EXCLUSIONS / main()'s exclusions log file.
    exclude_reason = None
    fetched_full = None  # cache: reused below by the ahead-of-parent path so a
                          # KEPT (internal-upstream) fork isn't double-fetched.

    # Rule 4: TEMP-PREFIX. Any repo whose name starts with "temp-" is
    # provisional/scratch by naming convention and is never our shipped work,
    # regardless of what its commits look like. Generalizes the earlier
    # one-off exclusion of obra/temp-sp-codex to the whole naming pattern --
    # also catches obra/temp-jifty-angular-demo and obra/temp-lufa-hacking,
    # found when validating this rule against the live obra listing.
    name_lower = name.lower()
    if name_lower.startswith(TEMP_NAME_PREFIX):
        exclude_reason = f"temp_prefix: name starts with {TEMP_NAME_PREFIX!r} -- provisional/scratch repo by convention"

    # Rule 2b: PRIVATE-MIRROR NAME/DESCRIPTION MARKER. See the PUBLIC-ONLY /
    # PRIVATE-MIRROR block above INTERNAL_OWNERS for why this exists and why
    # description matching is deliberately narrowed to one curated phrase
    # rather than a bare "mirror" substring.
    if exclude_reason is None:
        desc_lower = (repo.get("description") or "").lower()
        name_hit = next((m for m in NAME_MIRROR_MARKERS if m in name_lower), None)
        desc_hit = next((m for m in DESC_MIRROR_MARKERS if m in desc_lower), None)
        if name_hit or desc_hit:
            where = f"name (marker {name_hit!r})" if name_hit else f"description (marker {desc_hit!r})"
            exclude_reason = (
                f"private_mirror_marker: {where} signals this may be a private mirror of a public "
                "repo (often a security-issue mirror unfrozen after the fact) -- excluding fail-closed"
            )

    # Rule 2: CREATED-AFTER-WINDOW. A repo can't have produced in-window work
    # before it existed. Catches re-hosted/vendored external history landing
    # under historical commit dates -- e.g. prime-radiant-inc/shisad: GitHub
    # reports fork=false (it's a manually re-hosted copy, not a GitHub-button
    # fork), but it was created 2026-05-13 and its git history is a wholesale
    # import of shisa-ai/shisad's own commits/dates from before that. Without
    # this rule those commits would land in whatever window their dates fall
    # into even though prime-radiant-inc/shisad didn't exist yet.
    if exclude_reason is None and created_dt > window_end:
        exclude_reason = (
            f"created_after_window: created_at={created_dt.isoformat()} is after "
            f"this window's end={window_end.isoformat()} -- repo did not exist "
            "during the window being audited; any in-window-dated commits are "
            "imported/vendored history, not first-party work done in this window"
        )

    # Rule 1: EXTERNAL FORK. fork=true and the ultimate upstream owner
    # (.source.full_name, falling back to .parent.full_name) is NOT
    # prime-radiant-inc/obra. KEEPS forks whose upstream is still internal
    # (e.g. prime-radiant-inc/superpowers-testing -> obra/superpowers).
    if exclude_reason is None and is_fork:
        fetched_full, ferr = get_full_repo(login, name, token)
        if ferr:
            # Can't resolve the upstream -- fail CLOSED (exclude) rather than
            # silently keep a fork whose provenance we couldn't verify.
            exclude_reason = (
                f"fork_upstream_unresolvable: get_full_repo failed ({ferr}) -- "
                "excluding fail-closed pending manual check"
            )
        else:
            upstream = (fetched_full or {}).get("source") or (fetched_full or {}).get("parent")
            if upstream:
                upstream_full_name = upstream["full_name"]
                upstream_owner = upstream_full_name.split("/")[0]
                entry["fork_upstream"] = upstream_full_name
                if upstream_owner not in INTERNAL_OWNERS:
                    exclude_reason = (
                        f"external_fork: upstream={upstream_full_name} (owner "
                        f"{upstream_owner!r} is outside {sorted(INTERNAL_OWNERS)})"
                    )
            # else: genuinely no parent/source (upstream deleted) -- not
            # excluded by THIS rule; the existing ahead-of-parent-or-fallback
            # commit-counting logic further down still handles that case.

    if exclude_reason:
        entry["excluded"] = True
        entry["exclude_reason"] = exclude_reason
        entry["notes"].append(f"EXCLUDED at discovery: {exclude_reason}")
        entry["weeks"] = [
            {"index": i + 1, "commit_count": 0, "commits": [], "authors": {}, "loc_added": 0, "loc_removed": 0,
             "merged_prs": []}
            for i in range(len(buckets))
        ]
        entry["releases_in_window"] = []
        EXCLUSIONS.append({"repo": repo["full_name"], "reason": exclude_reason})
        print(f"[discovery] EXCLUDE {repo['full_name']}: {exclude_reason}", file=sys.stderr)
        return entry
    # ------------------------------------------------------ end EXCLUSION RULES --

    # -------------------------------------------------- RULE 3: AMBIGUOUS FLAG --
    # NOT an exclusion -- this repo survived every hard rule above (public,
    # not a temp-/marker-named mirror, not created after the window, not an
    # external fork) and stays KEPT. But per the HONEST LIMITATION documented
    # above INTERNAL_OWNERS, `gh api` only reports CURRENT visibility, so a
    # repo created before the window that was genuinely private DURING the
    # window and made public later without leaving any name/description
    # trace is invisible to every rule above. Flag it for a human instead of
    # silently trusting the absence of evidence as evidence of absence.
    if not created_in_window and created_dt < window_start:
        weak_hit = next(
            (m for m in AMBIGUOUS_NAME_DESC_SIGNALS if m in name_lower or m in (repo.get("description") or "").lower()),
            None,
        )
        if weak_hit:
            entry["ambiguous_flag"] = True
            entry["ambiguous_reason"] = (
                f"weak_signal_marker: {weak_hit!r} found in name/description -- possible embargoed/"
                "incident-mirror history; gh api cannot confirm historical visibility, flagging for "
                "human review rather than silently keeping"
            )
        else:
            # No marker at all -- this is the honest-limitation default case,
            # not a detected signal. Recorded on the entry (visible in the
            # recon JSON / coverage report) but NOT pushed into the AMBIGUOUS
            # list, which is reserved for repos with an actual, if weak,
            # signal -- otherwise every one of the ~300+ pre-window public
            # repos would be "flagged" and the list would be useless noise.
            entry["notes"].append(
                "no historical-visibility signal available (gh api reports current visibility only) -- "
                "kept on the strength of current public status + no mirror markers + pre-window created_at; "
                "see Rule 3 / HONEST LIMITATION in gather.py"
            )
        if entry["ambiguous_flag"]:
            AMBIGUOUS.append({"repo": repo["full_name"], "reason": entry["ambiguous_reason"]})
            print(f"[discovery] AMBIGUOUS {repo['full_name']}: {entry['ambiguous_reason']}", file=sys.stderr)
    # ---------------------------------------------------- end RULE 3: AMBIGUOUS --

    # Releases: unconditional, cheap.
    rels, err = get_releases(login, name, token, window_start, window_end)
    if err:
        errors["releases"] = err
        rels = []
    entry["releases_in_window"] = rels

    if not default_branch:
        entry["notes"].append("empty repo (no default branch / no commits ever) — skipped commit analysis")
        entry["weeks"] = [
            {"index": i + 1, "commit_count": 0, "commits": [], "authors": {}, "loc_added": 0, "loc_removed": 0,
             "merged_prs": []}
            for i in range(len(buckets))
        ]
        if errors:
            entry["_errors"] = errors
        return entry

    if not non_dormant:
        entry["notes"].append(
            "dormant: created_at and pushed_at both outside the window — "
            "provably zero commits/PRs in-window on any branch, skipped clone/API calls"
        )
        entry["weeks"] = [
            {"index": i + 1, "commit_count": 0, "commits": [], "authors": {}, "loc_added": 0, "loc_removed": 0,
             "merged_prs": []}
            for i in range(len(buckets))
        ]
        if errors:
            entry["_errors"] = errors
        return entry

    # Merged PRs — safe to skip only when dormant (see above); fetch now.
    prs, perr = get_merged_prs(login, name, token, window_start, window_end)
    if perr:
        errors["merged_prs"] = perr
        prs = []

    commits = []
    if is_fork:
        # Reuse the fetch done by the EXCLUSION RULES block above (which ran
        # for every fork, dormant or not) instead of hitting the API again.
        # We only get here at all when that fetch succeeded (a failure would
        # have set exclude_reason and returned early above).
        full, ferr = fetched_full, None
        if ferr:
            # get_full_repo FAILED (network blip, rate limit, transient 5xx,
            # revoked scope, ...) — this is NOT the same thing as "no parent".
            # The old code treated any failure here identically to "no parent
            # info" and fell back to an unfiltered default-branch git log —
            # i.e. exactly the fork-inherited-history bug this script exists
            # to avoid (see module docstring: v1 reported ~90-100 commits/wk
            # for the dormant obra/freshell fork this way). Surface the error
            # and count zero rather than silently re-introduce that bug.
            errors["get_full_repo"] = ferr
            entry["notes"].append(
                f"fork: could not fetch parent info ({ferr}) — counting zero "
                "in-window commits rather than risk inheriting upstream history"
            )
        else:
            parent = (full or {}).get("parent")
            if not parent:
                # Genuinely no parent (e.g. upstream repo deleted). Without a
                # parent to compare against we can't use the compare-API
                # ahead-of-parent approach below, but we can still rule out
                # the dominant inheritance case: a fork's default branch is
                # frozen at whatever upstream looked like at fork time unless
                # the owner later synced/pushed, so pre-fork-creation commits
                # are never this fork's own work. Bound the raw log to commits
                # authored strictly after the fork's creation date — weaker
                # than the compare-API method (a manual post-creation sync
                # from upstream could still slip through) but far safer than
                # the old unfiltered fallback, and correctly zeroes a fork
                # that was created and never touched again.
                entry["notes"].append(
                    "fork with no accessible parent info (deleted upstream?) — "
                    "falling back to default-branch log bounded to commits after "
                    "the fork's creation date, to avoid counting pre-fork inherited history"
                )
                dest = os.path.join(tmp_root, name)
                ok, cerr0 = clone_shallow(repo["clone_url"], default_branch, window_start, dest)
                if ok:
                    commits, cerr = git_log_numstat(dest, window_start, window_end)
                    if cerr:
                        errors["git_log"] = cerr
                        commits = []
                    else:
                        commits = [c for c in commits if parse_dt(c["date"]) > created_dt]
                        merge_fixed, merge_failed = fix_merge_commit_loc(commits, login, name, token)
                        if merge_failed:
                            errors["merge_loc"] = f"{len(merge_failed)} merge commit(s) LOC lookup failed, zeroed"
                else:
                    errors["clone"] = cerr0
                if os.path.isdir(dest):
                    shutil.rmtree(dest, ignore_errors=True)
            else:
                parent_full_name = parent["full_name"]
                parent_owner = parent_full_name.split("/")[0]
                parent_branch = parent.get("default_branch") or default_branch
                entry["fork_parent"] = parent_full_name
                cmp_data, cerr = get_compare(login, name, parent_owner, parent_branch, default_branch, token)
                if cerr:
                    errors["compare"] = cerr
                else:
                    entry["fork_ahead_by"] = cmp_data.get("ahead_by", 0)
                    ahead_commits = cmp_data.get("commits", []) or []
                    for c in ahead_commits:
                        cdate = c.get("commit", {}).get("author", {}).get("date")
                        if not cdate:
                            continue
                        dt = parse_dt(cdate)
                        if not (window_start <= dt <= window_end):
                            continue
                        sha = c["sha"]
                        stats, serr = get_commit_stats(login, name, sha, token)
                        if serr:
                            stats = {"additions": 0, "deletions": 0, "files_changed": 0}
                        commits.append(
                            {
                                "sha": sha, "short_sha": sha[:7],
                                "author": c.get("commit", {}).get("author", {}).get("name", "unknown"),
                                "date": cdate,
                                "subject": (c.get("commit", {}).get("message") or "").split("\n", 1)[0],
                                **stats,
                            }
                        )
    else:
        dest = os.path.join(tmp_root, name)
        ok, cerr0 = clone_shallow(repo["clone_url"], default_branch, window_start, dest)
        if ok:
            commits, cerr = git_log_numstat(dest, window_start, window_end)
            if cerr:
                errors["git_log"] = cerr
                commits = []
            else:
                # MERGE-COMMIT LOC BUG fix -- see fix_merge_commit_loc()
                # docstring. Local numstat is untrustworthy for merges (a
                # shallow-clone graft can turn one into a synthetic root and
                # attribute the whole tree to it); always replace with
                # GitHub's own per-commit diff instead.
                merge_fixed, merge_failed = fix_merge_commit_loc(commits, login, name, token)
                if merge_failed:
                    errors["merge_loc"] = f"{len(merge_failed)} merge commit(s) LOC lookup failed, zeroed"
        else:
            errors["clone"] = cerr0
        if os.path.isdir(dest):
            shutil.rmtree(dest, ignore_errors=True)

    weeks, unmatched = summarize_commits(commits, buckets)
    if unmatched:
        entry["notes"].append(f"{len(unmatched)} commit(s) had dates outside all buckets (clock skew?), excluded")

    # Attach merged PRs to their week bucket.
    for w in weeks:
        w["merged_prs"] = []
    for pr in prs:
        bi = bucket_index(parse_dt(pr["merged_at"]), buckets)
        if bi is not None:
            weeks[bi]["merged_prs"].append(pr)

    entry["weeks"] = weeks
    entry["total_commits_in_window"] = sum(w["commit_count"] for w in weeks)
    entry["total_merged_prs_in_window"] = sum(len(w["merged_prs"]) for w in weeks)
    entry["total_loc_added"] = sum(w["loc_added"] for w in weeks)
    entry["total_loc_removed"] = sum(w["loc_removed"] for w in weeks)
    if errors:
        entry["_errors"] = errors
    return entry


def process_account(login, kind, token, buckets, window_start, window_end, tmp_root, log=sys.stderr):
    repos = list_public_repos(login, kind, token)
    results = []
    for i, r in enumerate(repos):
        entry = process_repo(login, kind, r, token, buckets, window_start, window_end, tmp_root)
        results.append(entry)
        tc = entry.get("total_commits_in_window", 0)
        print(f"[{login}] {i + 1}/{len(repos)} {r['name']} commits={tc} fork={r['fork']}", file=log)
    return results


# ---------------------------------------------------------------- report --

def build_coverage_report(data):
    lines = []
    lines.append("# Shipped v2 recon — coverage report")
    lines.append("")
    lines.append(f"Generated: {data['generated_at_utc']}")
    lines.append(f"Window: {data['window_start_utc']} to {data['window_end_utc']}")
    lines.append("")
    lines.append("## Week boundaries")
    lines.append("")
    for b in data["week_buckets"]:
        lines.append(f"- Week {b['index']}: {b['start']} to {b['end']}")
    lines.append("")

    repos = data["repos"]
    by_org = {}
    for r in repos:
        by_org.setdefault(r["org"], []).append(r)

    week_bucket_ranges = [
        (parse_dt(b["start"] + "T00:00:00Z"), parse_dt(b["end"] + "T00:00:00Z") + datetime.timedelta(days=1))
        for b in data["week_buckets"]
    ]

    lines.append("## Discovery rules applied (public-only, finalized per Jesse's ruling)")
    lines.append("")
    lines.append("1. PUBLIC ONLY -- org/user listing filtered to public visibility (list_public_repos).")
    lines.append("2. NEVER PRIVATE / NEVER PRIVATE-MIRROR-OF-PUBLIC -- currently-private repos excluded "
                 "at listing time; name/description mirror markers + created-after-window jointly catch "
                 "private-mirror-of-public repos even if since made public.")
    lines.append("3. PRIVATE\u2192PUBLIC-LATER LIMITATION -- gh api reports only CURRENT visibility; a repo "
                 "genuinely private in-window, not recreated, now public, with no marker is UNDETECTABLE "
                 "with certainty. Flagged for human review (see Ambiguous section below) rather than "
                 "silently kept.")
    lines.append("4. temp- PREFIX -- any repo whose name starts with temp- is excluded (generalizes "
                 "temp-sp-codex).")
    lines.append("5. INTERNAL-UPSTREAM FORKS KEPT -- a fork is excluded only if its ultimate upstream owner "
                 "is outside {prime-radiant-inc, obra}; forks of our own repos (e.g. superpowers-testing -> "
                 "obra/superpowers) are kept.")
    lines.append("")
    lines.append("See discovery-exclusions.log for every excluded repo + reason, and "
                 "ambiguous-flags.log for every repo flagged (not excluded) under rule 3.")
    lines.append("")

    lines.append("## Per-org totals")
    lines.append("")
    total_active_all = 0
    all_active = []
    for org, rs in by_org.items():
        active = [r for r in rs if r.get("total_commits_in_window", 0) > 0
                  or r.get("total_merged_prs_in_window", 0) > 0 or r.get("releases_in_window")]
        dormant = [r for r in rs if any("dormant" in n for n in r.get("notes", []))]
        empty = [r for r in rs if any("empty repo" in n for n in r.get("notes", []))]
        errored = [r for r in rs if r.get("_errors")]
        total_active_all += len(active)
        all_active.extend(active)
        lines.append(f"### {org}")
        lines.append(f"- total public repos scanned: {len(rs)}")
        lines.append(f"- repos with ANY in-window activity (commits/PRs/releases): {len(active)}")
        lines.append(f"- provably dormant (skipped clone/API, zero possible activity): {len(dormant)}")
        lines.append(f"- empty repos (no commits ever): {len(empty)}")
        lines.append(f"- repos with fetch/clone errors: {len(errored)}")
        if errored:
            for r in errored:
                lines.append(f"  - {r['name']}: {r['_errors']}")
        lines.append("")

    lines.append(f"## Total distinct repos with in-window activity: {total_active_all}")
    lines.append("")
    lines.append("### KEEP set (public, first-party, in-window-active)")
    lines.append("")
    for r in sorted(all_active, key=lambda r: r["full_name"]):
        flag = " [AMBIGUOUS -- see ambiguous-flags.log]" if r.get("ambiguous_flag") else ""
        lines.append(f"- {r['full_name']}{flag}")
    lines.append("")

    ambiguous_active = [r for r in all_active if r.get("ambiguous_flag")]
    lines.append(f"## Ambiguous (flagged for human review, KEPT not excluded): {len(ambiguous_active)}")
    lines.append("")
    if not ambiguous_active:
        lines.append("(none in this run's active set)")
    else:
        for r in ambiguous_active:
            lines.append(f"- {r['full_name']}: {r.get('ambiguous_reason')}")
    lines.append("")

    lines.append("## Per-week totals (both orgs combined)")
    lines.append("")
    lines.append("| Week | Repos active | Commits | Merged PRs | LOC +/- | Contributors | Releases |")
    lines.append("|---|---|---|---|---|---|---|")
    n_weeks = len(data["week_buckets"])
    for wi in range(n_weeks):
        repos_active = 0
        commits = 0
        prs = 0
        loc_add = 0
        loc_del = 0
        authors = set()
        releases = 0
        for r in repos:
            rweeks = r.get("weeks")
            w = rweeks[wi] if rweeks and wi < len(rweeks) else None
            if w:
                if w["commit_count"] > 0 or w["merged_prs"]:
                    repos_active += 1
                commits += w["commit_count"]
                prs += len(w["merged_prs"])
                loc_add += w["loc_added"]
                loc_del += w["loc_removed"]
                authors.update(w["authors"].keys())
            for rel in r.get("releases_in_window", []):
                dt = parse_dt(rel["published_at"])
                s, e = week_bucket_ranges[wi]
                if s <= dt < e:
                    releases += 1
        lines.append(
            f"| {wi + 1} | {repos_active} | {commits} | {prs} | +{loc_add}/-{loc_del} | {len(authors)} | {releases} |"
        )
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------- main --

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weeks", type=int, default=8, help="number of week buckets (default 8)")
    ap.add_argument(
        "--window-end", type=str, default=None,
        help="ISO8601 UTC timestamp to anchor the window's end (default: now). "
        "Pass this to reproduce a specific historical dataset instead of drifting with wall-clock time.",
    )
    ap.add_argument("--orgs", type=str, default=None, help="comma-separated subset of account logins to scan")
    ap.add_argument("--out", type=str, default=None, help="output JSON path")
    ap.add_argument("--report-out", type=str, default="data/coverage-report.md", help="coverage report path")
    args = ap.parse_args()

    token = get_token()
    window_end = parse_dt(args.window_end) if args.window_end else datetime.datetime.now(datetime.timezone.utc)
    buckets = week_buckets(args.weeks, window_end)
    window_start = buckets[0][0]

    accounts = ACCOUNTS
    if args.orgs:
        wanted = set(x.strip() for x in args.orgs.split(","))
        accounts = [a for a in ACCOUNTS if a["login"] in wanted]

    tmp_root = tempfile.mkdtemp(prefix="gather-clones-")
    try:
        all_results = []
        for acct in accounts:
            all_results.extend(
                process_account(acct["login"], acct["kind"], token, buckets, window_start, window_end, tmp_root)
            )
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    out_path = args.out or f"data/recon-v2-{args.weeks}wk-{window_end.strftime('%Y%m%d')}.json"
    out = {
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "window_start_utc": window_start.isoformat(),
        "window_end_utc": window_end.isoformat(),
        "weeks_requested": args.weeks,
        "week_buckets": [
            {"index": i + 1, "start": s.date().isoformat(), "end": (e - datetime.timedelta(days=1)).date().isoformat()}
            for i, (s, e) in enumerate(buckets)
        ],
        "accounts_queried": {a["login"]: a["kind"] for a in accounts},
        "repos": all_results,
        # Every repo dropped by the discovery-time exclusion rules (temp-
        # prefix / private-mirror-marker / created-after-window /
        # external-fork / not-public), with its reason. Never silent -- see
        # EXCLUSIONS / process_repo()'s EXCLUSION RULES block.
        "discovery_exclusions": EXCLUSIONS,
        # Every KEPT repo Rule 3 flagged as ambiguous (public now,
        # pre-window created_at, no hard marker, but a weak signal) for
        # human review. NOT excluded on this basis alone. Never silent.
        "ambiguous_flags": AMBIGUOUS,
    }
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {out_path} ({len(all_results)} repos, {len(EXCLUSIONS)} excluded)", file=sys.stderr)

    report = build_coverage_report(out)
    os.makedirs(os.path.dirname(args.report_out) or ".", exist_ok=True)
    with open(args.report_out, "w") as f:
        f.write(report)
    print(f"wrote {args.report_out}", file=sys.stderr)

    # Standalone human-readable exclusions log, next to the coverage report --
    # the durable, always-produced record of every drop and why. Never
    # silent: this file exists (possibly empty-bodied) on every run.
    exclusions_log_path = os.path.join(os.path.dirname(args.report_out) or ".", "discovery-exclusions.log")
    with open(exclusions_log_path, "w") as f:
        f.write(f"# Discovery exclusions -- window {window_start.date()} to {window_end.date()}\n")
        f.write(f"# Generated {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n")
        f.write(f"# {len(EXCLUSIONS)} repo(s) excluded (of {len(all_results)} discovered)\n\n")
        if not EXCLUSIONS:
            f.write("(none)\n")
        else:
            for ex in EXCLUSIONS:
                f.write(f"{ex['repo']}: {ex['reason']}\n")
    print(f"wrote {exclusions_log_path} ({len(EXCLUSIONS)} exclusion(s))", file=sys.stderr)

    # Standalone human-readable ambiguous-flags log, same never-silent
    # treatment as the exclusions log above -- these repos are KEPT, but
    # Rule 3 could not rule out an in-window private period with certainty
    # (see HONEST LIMITATION above INTERNAL_OWNERS), so they need a human's
    # judgment call, not a silent auto-include.
    ambiguous_log_path = os.path.join(os.path.dirname(args.report_out) or ".", "ambiguous-flags.log")
    with open(ambiguous_log_path, "w") as f:
        f.write(f"# Ambiguous (KEPT, flagged for human review) -- window {window_start.date()} to {window_end.date()}\n")
        f.write(f"# Generated {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n")
        f.write(f"# {len(AMBIGUOUS)} repo(s) flagged (of {len(all_results)} discovered)\n\n")
        if not AMBIGUOUS:
            f.write("(none)\n")
        else:
            for amb in AMBIGUOUS:
                f.write(f"{amb['repo']}: {amb['reason']}\n")
    print(f"wrote {ambiguous_log_path} ({len(AMBIGUOUS)} ambiguous flag(s))", file=sys.stderr)


if __name__ == "__main__":
    main()
