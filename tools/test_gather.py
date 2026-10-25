"""Tests for tools/gather.py's shallow-clone commit counting.

Focus: the SHALLOW-BOUNDARY MERGE COMMIT UNDERCOUNT BUG (module docstring in
gather.py, bug 5; see clone_shallow()/_shallow_boundary_unsafe()). Found
2026-10-23 while fixing the week-of-2026-10-19 post (marketplace, llm-proxy,
github-triage all undercounted that week; hand-patched in commit ca8f10f,
which flagged the general case for a proper fix in this file rather than
per-week patching).

Run with: python3 -m pytest tools/test_gather.py -v
(needs a real `git` on PATH; builds and clones real temp repos under
file://, no network access).
"""
import datetime
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
import gather  # noqa: E402


def _run(cmd, cwd, env=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, timeout=60)
    assert r.returncode == 0, f"cmd failed: {cmd}\nstdout={r.stdout}\nstderr={r.stderr}"
    return r.stdout


def _commit(repo_dir, files, message, when_iso):
    env = dict(os.environ, GIT_AUTHOR_DATE=when_iso, GIT_COMMITTER_DATE=when_iso)
    for fname, content in files.items():
        with open(os.path.join(repo_dir, fname), "w") as f:
            f.write(content)
        _run(["git", "add", fname], repo_dir)
    _run(["git", "commit", "-q", "-m", message], repo_dir, env=env)
    return _run(["git", "rev-parse", "HEAD"], repo_dir).strip()


@pytest.fixture
def boundary_merge_repo(tmp_path):
    """Build a repo shaped exactly like the bug: a merge whose two parent
    chains need very different amounts of history, such that
    `--shallow-since` grafts the MERGE ITSELF as a parentless boundary
    commit. One parent (`main1`) -- dated INSIDE the reporting window, and
    reachable ONLY through the edge the graft erases -- goes missing from
    the commit walk entirely, not just mis-counted.

    Returns (origin_dir, window_start, window_end, dict of named commit SHAs).
    """
    origin = tmp_path / "origin"
    origin.mkdir()
    origin = str(origin)
    _run(["git", "init", "-q"], origin)
    _run(["git", "config", "user.email", "test@example.com"], origin)
    _run(["git", "config", "user.name", "Test"], origin)
    _run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], origin)

    shas = {}
    shas["base"] = _commit(origin, {"a.txt": "base\n"}, "base", "2026-01-01T00:00:00")

    _run(["git", "checkout", "-q", "-b", "feature"], origin)
    for i in range(1, 4):
        shas[f"feature{i}"] = _commit(
            origin, {f"feat{i}.txt": f"feat{i}\n"},
            f"feature commit {i} (old, outside window)",
            f"2026-01-0{i}T00:00:00",
        )

    _run(["git", "checkout", "-q", "main"], origin)
    # main1: dated INSIDE the window. This is the commit the bug drops --
    # reachable only via the merge's first-parent edge, which the graft
    # erases along with the second-parent edge to the feature chain.
    shas["main1"] = _commit(
        origin, {"main1.txt": "main1\n"}, "main commit 1 in-window", "2026-10-20T00:00:00"
    )

    env = dict(os.environ, GIT_AUTHOR_DATE="2026-10-21T00:00:00", GIT_COMMITTER_DATE="2026-10-21T00:00:00")
    _run(["git", "merge", "--no-ff", "-q", "-m", "Merge feature into main", "feature"], origin, env=env)
    shas["merge"] = _run(["git", "rev-parse", "HEAD"], origin).strip()

    shas["main2"] = _commit(
        origin, {"main2.txt": "main2\n"},
        "main commit 2 in-window, behind the merge", "2026-10-22T00:00:00",
    )

    window_start = datetime.datetime(2026, 10, 19, tzinfo=datetime.timezone.utc)
    window_end = datetime.datetime(2026, 10, 26, tzinfo=datetime.timezone.utc)
    return origin, window_start, window_end, shas


def test_raw_shallow_since_clone_grafts_merge_as_boundary(boundary_merge_repo, tmp_path):
    """Sanity check on the underlying git behavior this bug depends on:
    confirms the fixture actually reproduces a shallow clone that grafts
    the merge commit as a parentless boundary (not just a generic shallow
    clone) -- i.e. that this is testing the real bug, not a strawman."""
    origin, window_start, _window_end, shas = boundary_merge_repo
    dest = str(tmp_path / "raw_clone")
    since_str = (window_start - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    _run(
        [
            "git", "clone", "--quiet", "--single-branch", "--branch", "main",
            f"--shallow-since={since_str}", f"file://{origin}", dest,
        ],
        cwd=str(tmp_path),
    )
    shallow_path = os.path.join(dest, ".git", "shallow")
    assert os.path.isfile(shallow_path), "expected a shallow boundary to exist"
    with open(shallow_path) as f:
        boundary_shas = {line.strip() for line in f if line.strip()}
    assert shas["merge"] in boundary_shas, (
        "fixture didn't reproduce the bug precondition: the merge commit "
        "must itself be grafted as a boundary (0 parents), not its parents"
    )
    parents = _run(["git", "log", "-1", "--format=%P", shas["merge"]], dest).strip()
    assert parents == "", f"expected the merge's parents to be erased by the graft, got {parents!r}"


def test_clone_shallow_counts_all_in_window_commits_across_merge_boundary(boundary_merge_repo, tmp_path):
    """The actual regression test. Before the fix, `clone_shallow` returns
    a clone with the merge grafted (see test above), and `main1` --
    dated inside the window, reachable only via the erased edge -- is
    completely absent from `git_log_numstat`'s walk: the window's commit
    count is 3 (merge, main2, and... missing main1) instead of 4, and
    `main1` doesn't appear in the commit list at all, not even with wrong
    stats.

    After the fix, `clone_shallow` detects the unsafe boundary and
    unshallows before returning, so the full parent graph is intact and
    all four in-window-reachable commits show up."""
    origin, window_start, window_end, shas = boundary_merge_repo
    dest = str(tmp_path / "clone")

    ok, err = gather.clone_shallow(f"file://{origin}", "main", window_start, dest)
    assert ok, f"clone_shallow failed: {err}"

    commits, log_err = gather.git_log_numstat(dest, window_start, window_end)
    assert log_err is None, f"git_log_numstat failed: {log_err}"

    counted_shas = {c["sha"] for c in commits}

    assert shas["main1"] in counted_shas, (
        "main1 (in-window, reachable only through the edge the shallow-clone "
        "merge graft erases) is missing from the commit walk -- this is the "
        "undercount bug: commits behind a grafted merge boundary go uncounted."
    )
    assert shas["main2"] in counted_shas
    assert shas["merge"] in counted_shas
    # The window should see exactly the 3 commits reachable in-window on
    # main's line (main1, merge, main2) -- the old feature-branch commits
    # are dated in January, outside the window, correctly excluded.
    assert len(commits) == 3, f"expected 3 in-window commits, got {len(commits)}: {sorted(counted_shas)}"


def test_shallow_boundary_unsafe_detects_graft_inside_window(boundary_merge_repo, tmp_path):
    """Unit-level check on the detector itself: a raw (unfixed) shallow
    clone of the boundary_merge_repo fixture must be flagged unsafe."""
    origin, window_start, _window_end, _shas = boundary_merge_repo
    dest = str(tmp_path / "raw_clone2")
    since_str = (window_start - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    _run(
        [
            "git", "clone", "--quiet", "--single-branch", "--branch", "main",
            f"--shallow-since={since_str}", f"file://{origin}", dest,
        ],
        cwd=str(tmp_path),
    )
    assert gather._shallow_boundary_unsafe(dest, window_start) is True


def test_shallow_boundary_unsafe_false_when_no_shallow_file(tmp_path):
    """A full (non-shallow) clone has no `.git/shallow` at all -- never
    flagged unsafe."""
    repo = str(tmp_path / "full")
    os.makedirs(repo)
    _run(["git", "init", "-q"], repo)
    assert gather._shallow_boundary_unsafe(repo, datetime.datetime.now(datetime.timezone.utc)) is False


def test_shallow_boundary_unsafe_false_for_boundary_safely_before_window(boundary_merge_repo, tmp_path):
    """A shallow clone whose boundary lands comfortably before the window
    (no merge-chain asymmetry forcing a graft onto the merge) must NOT be
    flagged -- the detector shouldn't force unnecessary unshallowing on the
    common, uncorrupted case."""
    origin, window_start, _window_end, _shas = boundary_merge_repo
    dest = str(tmp_path / "safe_clone")
    # A much earlier cutoff than the window: old feature-branch commits
    # (Jan 2026) are still comfortably included, so no asymmetric graft is
    # needed and the boundary (base commit) sits in Dec 2025 territory --
    # i.e. before window_start.
    _run(
        [
            "git", "clone", "--quiet", "--single-branch", "--branch", "main",
            "--shallow-since=2025-12-01", f"file://{origin}", dest,
        ],
        cwd=str(tmp_path),
    )
    assert gather._shallow_boundary_unsafe(dest, window_start) is False
