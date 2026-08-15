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
    endpoint = f"orgs/{login}/repos" if kind == "org" else f"users/{login}/repos"
    data, err = gh_api(f"{endpoint}?type=public&per_page=100", token)
    if err:
        sys.exit(f"ERROR: could not list public repos for {login} ({kind}): {err}")
    return data


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
        "notes": [],
    }

    errors = {}

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
        full, ferr = get_full_repo(login, name, token)
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

    lines.append("## Per-org totals")
    lines.append("")
    total_active_all = 0
    for org, rs in by_org.items():
        active = [r for r in rs if r.get("total_commits_in_window", 0) > 0
                  or r.get("total_merged_prs_in_window", 0) > 0 or r.get("releases_in_window")]
        dormant = [r for r in rs if any("dormant" in n for n in r.get("notes", []))]
        empty = [r for r in rs if any("empty repo" in n for n in r.get("notes", []))]
        errored = [r for r in rs if r.get("_errors")]
        total_active_all += len(active)
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
    }
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {out_path} ({len(all_results)} repos)", file=sys.stderr)

    report = build_coverage_report(out)
    os.makedirs(os.path.dirname(args.report_out) or ".", exist_ok=True)
    with open(args.report_out, "w") as f:
        f.write(report)
    print(f"wrote {args.report_out}", file=sys.stderr)


if __name__ == "__main__":
    main()
