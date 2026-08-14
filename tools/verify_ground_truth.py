#!/usr/bin/env python3
"""
verify_ground_truth.py — re-derive correct per-week commit/LOC/author data
from FULL (non-shallow) git clones, to fix two bugs found by an independent
reviewer in the original gather.py output (data/recon-v2-8wk-20260814.json):

BUG 1 — LOC INFLATION (shallow-clone grafted-root diff-against-empty-tree):
  gather.py's clone_shallow() does `git clone --single-branch --branch X
  --shallow-since=D`. If a repo's oldest commit actually included in that
  shallow fetch happens to be one of only a few commits in the whole 8-week
  lookback (i.e. a genuinely low-activity repo), git has no earlier commit
  to record as its parent and grafts it into `.git/shallow` as a PARENTLESS
  root. `git log --numstat` on a parentless commit diffs it against the
  EMPTY TREE, so its reported diff balloons to the size of the commit's
  ENTIRE file tree, not the tiny real change. Verified directly:
  prime-radiant-inc/sprout's "docs(map): refresh catalog-info.yaml" commit
  (3222dbf) reports +231613/-0 in the shallow clone gather.py used, vs the
  real +1/-1 in a full clone (git show --numstat 3222dbf in each).

BUG 2 — COMMIT UNDERCOUNT (single-branch shallow clone drops merged-branch
ancestry): the same `--single-branch --shallow-since` clone does not fetch
the non-first-parent ancestry of merge commits — i.e. the individual commits
of a feature/PR branch that was merged via a real merge commit (not squash)
never even get fetched into the shallow clone's object store. Verified
directly: obra/superpowers-chrome's PR #43 (6 commits by ada-sen, merged by
Jesse Vincent) — the shallow clone contains ZERO of ada-sen's 6 commits
(`git log --pretty=%an | grep ada-sen` => 0 hits) even with no date filter
at all, while a full clone has all 6, all reachable ancestors of the merge
commit d59fb33. Only the merge commit itself (credited to whoever clicked
merge) survived the shallow fetch.

Both bugs share one root cause: using a shallow, single-branch clone for
speed is unsafe for exact commit/LOC accounting. The fix here is to always
use a FULL clone for ground-truth re-derivation — no --shallow-since, no
--single-branch restriction on ancestry (the branch is still checked out,
but its full history, including all merged-in ancestors, is fetched).

Also fixes date-field consistency: git's own --since/--until filters by
COMMITTER date by default; this script buckets by committer date too
(rather than author date) so "which week did this land in" always matches
what git itself considers in-window — avoiding a class of bug where a
rebased/cherry-picked commit's author date and committer date disagree.

FORKS are NOT re-cloned here: gather.py's fork handling uses GitHub's
compare API (ahead_by / ahead-of-parent commit list) rather than the
shallow clone, and compare-API ancestry walks are not shallow-limited, so
that path isn't subject to either bug. It's reused as-is from the original
JSON. (Only one active fork exists in this dataset: prime-radiant-inc/
openai-codex-plugins, ahead_by=1 in week 7 — spot-checked separately.)

Usage:
    GH_TOKEN=<token> python3 tools/verify_ground_truth.py \\
        data/recon-v2-8wk-20260814.json \\
        --out data/recon-v2-8wk-20260814-CORRECTED.json
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

VERSION_BUMP_RE = re.compile(r"\b(?:v)?\d+\.\d+\.\d+\b")
RELEASE_KEYWORD_RE = re.compile(r"\b(release|bump|version)\b", re.IGNORECASE)


def parse_dt(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def bucket_index(dt, buckets):
    for i, (s, e) in enumerate(buckets):
        if s <= dt < e:
            return i
    return None


def run_git(cmd, cwd=None, timeout=300):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return False, "", "timeout"


def full_clone(clone_url, branch, dest, timeout=600):
    cmd = ["git", "clone", "--quiet", "--single-branch", "--branch", branch, clone_url, dest]
    ok, _, err = run_git(cmd, timeout=timeout)
    return ok, err


def git_log_full(repo_dir, since_dt, until_dt):
    """Full ground-truth commit log: COMMITTER date used for both the
    --since/--until filter (git's own default) and for display/bucketing,
    so there is no author/committer mismatch class of bug."""
    since_iso = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    until_iso = until_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    cmd = [
        "git", "log", "HEAD", f"--since={since_iso}", f"--until={until_iso}",
        "--numstat", "--no-color",
        "--pretty=format:COMMIT\t%H\t%h\t%an\t%cI\t%s",
    ]
    ok, out, err = run_git(cmd, cwd=repo_dir)
    if not ok:
        return None, err
    return parse_log(out), None


def parse_log(text):
    commits = []
    cur = None
    for line in text.splitlines():
        if line.startswith("COMMIT\t"):
            if cur:
                commits.append(cur)
            parts = line.split("\t", 5)
            if len(parts) < 6:
                continue
            _, sha, short, author, date, subject = parts
            cur = {
                "sha": sha, "short_sha": short, "author": author, "date": date,
                "subject": subject, "additions": 0, "deletions": 0, "files_changed": 0,
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


def get_tags(repo_dir):
    ok, out, err = run_git(["git", "tag", "--list"], cwd=repo_dir)
    if not ok:
        return set()
    return set(t.strip().lstrip("v") for t in out.splitlines() if t.strip())


def find_commit_message_only_bumps(commits, tags, tagged_release_tags_by_repo):
    """A commit whose subject mentions a semver-looking version AND a
    release/bump/version keyword, where that version string has NEITHER a
    git tag NOR a matching GitHub release object, counts as a
    commit-message-only version bump (e.g. everyharness 0.7.0/0.7.1)."""
    out = []
    for c in commits:
        if not RELEASE_KEYWORD_RE.search(c["subject"]):
            continue
        m = VERSION_BUMP_RE.search(c["subject"])
        if not m:
            continue
        version = m.group(0).lstrip("v")
        if version in tags or version in tagged_release_tags_by_repo:
            continue  # it IS tagged/released, not message-only
        out.append({"sha": c["sha"], "date": c["date"], "subject": c["subject"], "version": version})
    return out


def summarize(commits, buckets):
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recon_json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    data = json.load(open(args.recon_json))
    window_start = parse_dt(data["window_start_utc"])
    buckets = []
    for b in data["week_buckets"]:
        s = datetime.datetime.fromisoformat(b["start"]).replace(tzinfo=datetime.timezone.utc)
        e = datetime.datetime.fromisoformat(b["end"]).replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(days=1)
        buckets.append((s, e))
    # THIRD ISSUE found during verification (not one of the two originally
    # reported, but explains the serf/wk8 and clipfan/wk8 anchors): the
    # original window_end was frozen to the exact instant v1's gather.py
    # happened to run (2026-08-14T00:50:52Z), truncating week 8 to ~4.8 of
    # its 7 days while weeks 1-7 got their full range. Confirmed directly:
    # serf has exactly 18 more commits between that frozen instant and the
    # real end of week 8 (2026-08-16 23:59:59) -- 122 (truncated) vs 140
    # (full week), matching the reviewer's ACTUAL=140 exactly. Using the
    # full last bucket's end here instead of the frozen snapshot.
    window_end = buckets[-1][1] - datetime.timedelta(seconds=1)

    active = [
        r for r in data["repos"]
        if r.get("total_commits_in_window", 0) > 0 or r.get("total_merged_prs_in_window", 0) > 0
        or r.get("releases_in_window")
    ]

    tmp_root = tempfile.mkdtemp(prefix="verify-ground-truth-")
    corrected_repos = []
    try:
        for i, r in enumerate(active):
            name = r["name"]
            login = r["org"]
            print(f"[{i+1}/{len(active)}] {login}/{name}...", file=sys.stderr)
            entry = dict(r)  # start from original (carries fork/parent/release/PR data forward)

            if r["fork"]:
                # Not re-cloned: compare-API-derived ahead-of-parent commits
                # are not subject to either bug (see module docstring).
                entry["_ground_truth_method"] = "unchanged (fork; compare API, not shallow clone)"
                corrected_repos.append(entry)
                continue

            dest = os.path.join(tmp_root, name)
            ok, err = full_clone(r["html_url"] + ".git", r["default_branch"], dest)
            if not ok:
                entry["_ground_truth_error"] = err
                entry["_ground_truth_method"] = "FAILED full clone; original (buggy) data retained"
                corrected_repos.append(entry)
                continue

            commits, cerr = git_log_full(dest, window_start, window_end)
            tags = get_tags(dest)
            if cerr:
                entry["_ground_truth_error"] = cerr
            else:
                weeks, unmatched = summarize(commits or [], buckets)
                for w in weeks:
                    w["merged_prs"] = []
                    w["commit_message_only_bumps"] = find_commit_message_only_bumps(
                        w["commits"], tags,
                        set(rel["tag"].lstrip("v") for rel in r.get("releases_in_window", [])),
                    )
                # carry merged PRs over from original per-week structure (API-based, not
                # shallow-clone-based, so not subject to either bug) by re-bucketing the
                # same PR list against our (identical) week buckets.
                for pr_list_week in r.get("weeks", []):
                    idx = pr_list_week["index"] - 1
                    if 0 <= idx < len(weeks):
                        weeks[idx]["merged_prs"] = pr_list_week.get("merged_prs", [])
                entry["weeks"] = weeks
                entry["total_commits_in_window"] = sum(w["commit_count"] for w in weeks)
                entry["total_merged_prs_in_window"] = sum(len(w["merged_prs"]) for w in weeks)
                entry["total_loc_added"] = sum(w["loc_added"] for w in weeks)
                entry["total_loc_removed"] = sum(w["loc_removed"] for w in weeks)
                entry["_ground_truth_method"] = "full clone (not shallow), committer-date bucketed"
                if unmatched:
                    entry.setdefault("notes", []).append(
                        f"{len(unmatched)} commit(s) outside all buckets even in full clone"
                    )
            shutil.rmtree(dest, ignore_errors=True)
            corrected_repos.append(entry)
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    # non-active repos pass through unchanged (they were correctly zero before too)
    active_names = {(r["org"], r["name"]) for r in active}
    for r in data["repos"]:
        if (r["org"], r["name"]) not in active_names:
            corrected_repos.append(r)

    out = dict(data)
    out["repos"] = corrected_repos
    out["window_end_utc"] = window_end.isoformat()
    out["_correction_note"] = (
        "Ground-truth corrected via tools/verify_ground_truth.py: full (non-shallow) "
        "clones replace the original shallow-clone-based commit/LOC data for all "
        "non-fork active repos, fixing (1) grafted-shallow-root LOC inflation and "
        "(2) single-branch shallow clone dropping merged-branch-ancestor commits. "
        "Also fixes (3) week 8 was truncated to a frozen snapshot instant "
        "(2026-08-14T00:50:52Z), covering only ~4.8 of its 7 days while weeks 1-7 "
        "got the full week -- window_end is now the full end of week 8 "
        "(2026-08-16T23:59:59Z). Fork data (1 repo: openai-codex-plugins) is "
        "unchanged — compare-API-derived, not subject to bugs 1/2, and its one "
        "ahead-of-parent commit (week 7) predates the week-8 boundary change anyway. "
        "Bucketing now uses committer date consistently with git's own "
        "--since/--until semantics."
    )
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
