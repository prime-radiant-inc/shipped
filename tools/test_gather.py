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


# ------------------------------------------------- CUTOFF-WINDOW-NO-MERGES --
# Tests for cutoff_window_bucket() / resolve_prev_cutoff() (module docstring
# in gather.py, bug 6). Two accuracy-reviewer rules, new posts only:
#   a. cutoff-to-cutoff window: (prev_cutoff, cutoff], not calendar Mon-Sun.
#   b. merges count for neither commits nor lines (author counts included).
# These operate on plain commit dicts (the shape parse_git_log/
# git_log_numstat produce) directly -- no real git repo needed, unlike the
# shallow-clone tests above.

def _mk_commit(sha, date_iso, n_parents=1, author="Test Author", additions=10, deletions=2, subject="a commit"):
    return {
        "sha": sha, "short_sha": sha[:7], "author": author, "email": "test@example.com",
        "date": date_iso, "subject": subject, "additions": additions, "deletions": deletions,
        "files_changed": 1, "loc_untrusted": n_parents != 1, "n_parents": n_parents,
    }


def test_cutoff_window_bucket_excludes_merge_from_counts():
    """A merge commit (n_parents > 1) must contribute 0 to commit_count,
    loc_added, loc_removed, and the author's per-commit tally -- even
    though it has real (non-zero) additions/deletions attached (simulating
    fix_merge_commit_loc's GitHub-API-corrected LOC for that merge). It
    still appears in the returned commits list, flagged is_merge, for
    narrative/subject-line use."""
    prev_cutoff = datetime.datetime(2026, 11, 1, tzinfo=datetime.timezone.utc)
    cutoff = datetime.datetime(2026, 11, 8, tzinfo=datetime.timezone.utc)
    commits = [
        _mk_commit("a" * 40, "2026-11-02T00:00:00+00:00", n_parents=1, author="Ada", additions=5, deletions=1),
        _mk_commit(
            "b" * 40, "2026-11-03T00:00:00+00:00", n_parents=2, author="Ada",
            additions=630, deletions=266, subject="Merge feature into main",
        ),
        _mk_commit("c" * 40, "2026-11-04T00:00:00+00:00", n_parents=1, author="Drew", additions=7, deletions=3),
    ]
    week = gather.cutoff_window_bucket(commits, prev_cutoff, cutoff)

    assert week["commit_count"] == 2, "the merge must not add to commit_count"
    assert week["loc_added"] == 12, "the merge's 630 additions must not add to loc_added (5 + 7 only)"
    assert week["loc_removed"] == 4, "the merge's 266 deletions must not add to loc_removed (1 + 3 only)"
    assert week["authors"] == {"Ada": 1, "Drew": 1}, "the merge must not add to Ada's author tally"

    merge_entries = [c for c in week["commits"] if c["sha"] == ("b" * 40)[:7]]
    assert len(merge_entries) == 1, "the merge commit should still appear in the commits list"
    assert merge_entries[0]["is_merge"] is True
    non_merge_shas = {c["sha"] for c in week["commits"] if not c["is_merge"]}
    assert non_merge_shas == {("a" * 40)[:7], ("c" * 40)[:7]}


def test_cutoff_window_bucket_boundary_exclusive_start_inclusive_end():
    """Window is (prev_cutoff, cutoff]: a commit dated exactly AT
    prev_cutoff belongs to the PREVIOUS post and must be excluded; one
    dated exactly AT cutoff belongs to THIS post and must be included.
    Commits one second on either side of each boundary confirm the cut is
    at the boundary itself, not rounded to a day."""
    prev_cutoff = datetime.datetime(2026, 11, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    cutoff = datetime.datetime(2026, 11, 8, 18, 30, 0, tzinfo=datetime.timezone.utc)
    commits = [
        _mk_commit("1" * 40, "2026-11-01T11:59:59+00:00", subject="before prev_cutoff, excluded"),
        _mk_commit("2" * 40, "2026-11-01T12:00:00+00:00", subject="exactly at prev_cutoff, excluded"),
        _mk_commit("3" * 40, "2026-11-01T12:00:01+00:00", subject="just after prev_cutoff, included"),
        _mk_commit("4" * 40, "2026-11-08T18:29:59+00:00", subject="just before cutoff, included"),
        _mk_commit("5" * 40, "2026-11-08T18:30:00+00:00", subject="exactly at cutoff, included"),
        _mk_commit("6" * 40, "2026-11-08T18:30:01+00:00", subject="just after cutoff, excluded"),
    ]
    week = gather.cutoff_window_bucket(commits, prev_cutoff, cutoff)
    counted_shas = {c["sha"] for c in week["commits"]}

    assert counted_shas == {("3" * 40)[:7], ("4" * 40)[:7], ("5" * 40)[:7]}, (
        f"expected exactly the 3 in-(prev_cutoff, cutoff]-window commits, got {sorted(counted_shas)}"
    )
    assert week["commit_count"] == 3


def test_resolve_prev_cutoff_explicit_arg_wins(tmp_path):
    """An explicit --prev-cutoff always wins, even if a stats file with a
    recorded cutoff also exists."""
    stats_path = tmp_path / "weekly-stats.json"
    stats_path.write_text('{"2026-10-19": {"cutoff": "2026-10-23T22:10:22+00:00"}}')
    resolved = gather.resolve_prev_cutoff("2026-11-01T00:00:00Z", str(stats_path))
    assert resolved == datetime.datetime(2026, 11, 1, tzinfo=datetime.timezone.utc)


def test_resolve_prev_cutoff_reads_most_recent_recorded_value(tmp_path):
    """With no explicit --prev-cutoff, fall back to the most recently
    published week's own recorded `cutoff` field."""
    stats_path = tmp_path / "weekly-stats.json"
    stats_path.write_text(
        '{"2026-10-19": {"cutoff": "2026-10-23T22:10:22+00:00"}, '
        '"2026-10-26": {"cutoff": "2026-10-30T20:00:00+00:00"}, '
        '"2026-09-28": {"summary": {}}}'
    )
    resolved = gather.resolve_prev_cutoff(None, str(stats_path))
    assert resolved == datetime.datetime(2026, 10, 30, 20, 0, 0, tzinfo=datetime.timezone.utc)


def test_resolve_prev_cutoff_missing_raises(tmp_path):
    """No explicit --prev-cutoff AND no week in the stats file carries a
    `cutoff` field (e.g. every published week predates this mode, exactly
    today's real state of src/data/weekly-stats.json) -- must error out
    rather than invent a default window."""
    stats_path = tmp_path / "weekly-stats.json"
    stats_path.write_text('{"2026-10-19": {"summary": {}, "repos": {}}}')
    with pytest.raises(SystemExit):
        gather.resolve_prev_cutoff(None, str(stats_path))


def test_resolve_prev_cutoff_missing_file_raises(tmp_path):
    """No explicit --prev-cutoff AND the stats file doesn't exist at all --
    must still error out, not crash with an unrelated exception or silently
    pick a default."""
    missing_path = tmp_path / "does-not-exist.json"
    with pytest.raises(SystemExit):
        gather.resolve_prev_cutoff(None, str(missing_path))


# ------------------------------------------- fork compare-API n_parents --
# PR #4 review, non-blocking 1: commits arriving via the fork-ahead-of-
# parent compare-API path (process_repo's `cmp_data = get_compare(...)`
# branch) previously had no `n_parents` key at all. cutoff_window_bucket's
# merge check (`c.get("n_parents", 1) > 1`) defaults a missing key to 1, so
# a merge commit arriving via this path would be silently counted instead
# of excluded. Fix: compare_commit_to_dict() reads the compare API's own
# `parents` array (same shape GitHub's regular commits API uses) and sets
# n_parents from its length.

def _compare_api_commit(sha, n_parents, date="2026-11-02T00:00:00Z", author_name="Jesse Vincent", login="jvincent"):
    """Shape of one entry in the compare API's `commits` list (GitHub docs:
    GET /repos/{owner}/{repo}/compare/{base}...{head}), trimmed to the
    fields compare_commit_to_dict() reads."""
    return {
        "sha": sha,
        "commit": {
            "author": {"name": author_name, "email": "jesse@example.com", "date": date},
            "message": "a commit\n\nbody text",
        },
        "author": {"login": login},
        "parents": [{"sha": "p" * 40} for _ in range(n_parents)],
    }


def test_compare_commit_to_dict_sets_n_parents_from_parents_array():
    """A real merge arriving via the compare API (2 parents) must be
    tagged n_parents=2, not left unset/defaulted to 1."""
    c = _compare_api_commit("m" * 40, n_parents=2)
    stats = {"additions": 630, "deletions": 266, "files_changed": 12}
    result = gather.compare_commit_to_dict(c, c["commit"]["author"]["date"], stats)
    assert result["n_parents"] == 2


def test_compare_commit_to_dict_normal_commit_n_parents_one():
    c = _compare_api_commit("a" * 40, n_parents=1)
    stats = {"additions": 5, "deletions": 1, "files_changed": 1}
    result = gather.compare_commit_to_dict(c, c["commit"]["author"]["date"], stats)
    assert result["n_parents"] == 1


def test_compare_commit_to_dict_missing_parents_field_defaults_to_one():
    """Defensive fallback only -- not observed in practice, but if GitHub
    ever omitted `parents` entirely, assume non-merge (1) rather than
    crash."""
    c = _compare_api_commit("a" * 40, n_parents=1)
    del c["parents"]
    stats = {"additions": 5, "deletions": 1, "files_changed": 1}
    result = gather.compare_commit_to_dict(c, c["commit"]["author"]["date"], stats)
    assert result["n_parents"] == 1


def test_compare_commit_merge_excluded_from_cutoff_window_counts():
    """End-to-end through cutoff_window_bucket: a merge built via
    compare_commit_to_dict must be excluded from commit_count/loc, exactly
    like a merge from the local git-log path."""
    prev_cutoff = datetime.datetime(2026, 11, 1, tzinfo=datetime.timezone.utc)
    cutoff = datetime.datetime(2026, 11, 8, tzinfo=datetime.timezone.utc)
    normal = gather.compare_commit_to_dict(
        _compare_api_commit("a" * 40, n_parents=1, date="2026-11-02T00:00:00Z"),
        "2026-11-02T00:00:00Z", {"additions": 5, "deletions": 1, "files_changed": 1},
    )
    merge = gather.compare_commit_to_dict(
        _compare_api_commit("b" * 40, n_parents=2, date="2026-11-03T00:00:00Z"),
        "2026-11-03T00:00:00Z", {"additions": 630, "deletions": 266, "files_changed": 12},
    )
    week = gather.cutoff_window_bucket([normal, merge], prev_cutoff, cutoff)
    assert week["commit_count"] == 1, "the compare-API merge must not be counted"
    assert week["loc_added"] == 5
    assert week["loc_removed"] == 1


# --------------------------------------------- --cutoff/--prev-cutoff UTC --
# PR #4 review, non-blocking 2: WeekSummary.astro's fmtCutoff() slices the
# stored ISO string and labels it "UTC" without checking the offset. A
# --cutoff/--prev-cutoff given in a non-UTC offset (or no offset at all)
# would display the wrong wall-clock time, still labeled UTC. Fix:
# parse_utc_cutoff_arg() rejects anything but an explicit UTC offset.

def test_parse_utc_cutoff_arg_accepts_z_suffix():
    dt = gather.parse_utc_cutoff_arg("2026-11-08T18:30:00Z", "--cutoff")
    assert dt == datetime.datetime(2026, 11, 8, 18, 30, 0, tzinfo=datetime.timezone.utc)


def test_parse_utc_cutoff_arg_accepts_explicit_plus_zero_offset():
    dt = gather.parse_utc_cutoff_arg("2026-11-08T18:30:00+00:00", "--cutoff")
    assert dt == datetime.datetime(2026, 11, 8, 18, 30, 0, tzinfo=datetime.timezone.utc)


def test_parse_utc_cutoff_arg_rejects_non_utc_offset():
    with pytest.raises(SystemExit):
        gather.parse_utc_cutoff_arg("2026-11-08T13:30:00-05:00", "--cutoff")


def test_parse_utc_cutoff_arg_rejects_naive_timestamp():
    """No offset at all is ambiguous, not "assume UTC" -- reject it too."""
    with pytest.raises(SystemExit):
        gather.parse_utc_cutoff_arg("2026-11-08T18:30:00", "--cutoff")


def test_resolve_prev_cutoff_rejects_non_utc_explicit_offset(tmp_path):
    stats_path = tmp_path / "weekly-stats.json"
    stats_path.write_text("{}")
    with pytest.raises(SystemExit):
        gather.resolve_prev_cutoff("2026-11-01T00:00:00-05:00", str(stats_path))
