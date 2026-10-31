"""Tests for tools/gen_stats.py's main() merge behavior.

Focus: the WEEK-COLLAPSE BUG flagged in PR #4 review. main() used to start
from `out = {}` and write ONLY the weeks present in the given recon's
`week_buckets`. A `--cutoff`-mode recon (tools/gather.py) always produces
exactly ONE bucket, so running gen_stats.py with a cutoff recon against the
real, many-week src/data/weekly-stats.json silently collapsed all other
weeks out of the file -- no error, no warning, published history just gone
on the next build.

Fix, two parts:
1. `merge_weeks()` -- main() now loads the existing --out file (if any)
   and merges the recon's weeks into it (pure key-set union: a week not
   present in the recon is left byte-for-byte untouched; a week present in
   both is replaced by the recon's version).
2. `guard_against_shrink()` -- an independent, defense-in-depth backstop
   that refuses (non-zero exit, clear message) to WRITE a result with
   fewer weeks than the existing file, unless --force is passed. Note:
   `merge_weeks` is a pure union, so it can never by itself produce a
   shrink -- this guard protects every OTHER way main() could end up
   pointed at a mismatched --out/recon pair (now, or after some future
   change to the merge itself).

Run with: python3 -m pytest tools/test_gen_stats.py -v
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
import gen_stats  # noqa: E402


def _recon(tmp_path, week_buckets, repos=None, name="recon.json"):
    recon = {
        "generated_at_utc": "2026-10-26T00:00:00+00:00",
        "window_start_utc": week_buckets[0]["start"] + "T00:00:00+00:00",
        "window_end_utc": week_buckets[-1]["end"] + "T00:00:00+00:00",
        "weeks_requested": len(week_buckets),
        "week_buckets": week_buckets,
        "accounts_queried": {},
        "repos": repos if repos is not None else [],
    }
    p = tmp_path / name
    p.write_text(json.dumps(recon))
    return str(p)


def _trivial_week():
    return {
        "summary": {
            "repos_active": 0, "featured_count": 0, "second_tier_count": 0,
            "commits": 0, "merged_prs": 0, "loc_added": 0, "loc_removed": 0,
            "contributors": 0, "tagged_releases": 0, "commit_only_bumps": 0,
        },
        "repos": {},
    }


def _write_existing(path, week_keys):
    data = {wk: _trivial_week() for wk in week_keys}
    with open(path, "w") as f:
        json.dump(data, f)
    return data


def _run_main(argv):
    old_argv = sys.argv
    sys.argv = ["gen_stats.py"] + argv
    try:
        gen_stats.main()
    finally:
        sys.argv = old_argv


EXISTING_WEEKS = [
    "2026-01-05", "2026-01-12", "2026-01-19", "2026-01-26",
    "2026-02-02", "2026-02-09", "2026-02-16", "2026-02-23",
]


# --------------------------------------------------------- end-to-end bug --

def test_single_bucket_cutoff_recon_preserves_all_existing_weeks(tmp_path):
    """The exact reported bug: feed a single-bucket (--cutoff-mode-shaped)
    recon against a multi-week existing weekly-stats.json. Every existing
    week must survive the run, plus the new week from the recon."""
    out_path = str(tmp_path / "weekly-stats.json")
    _write_existing(out_path, EXISTING_WEEKS)

    recon_path = _recon(tmp_path, [
        {"index": 1, "start": "2026-03-02", "end": "2026-03-08",
         "cutoff": "2026-03-08T20:00:00+00:00", "prev_cutoff": "2026-03-01T20:00:00+00:00"},
    ])

    _run_main([recon_path, "--out", out_path])

    with open(out_path) as f:
        result = json.load(f)

    for wk in EXISTING_WEEKS:
        assert wk in result, f"existing week {wk} was dropped by the merge"
    assert "2026-03-02" in result, "the new recon week must be present"
    assert len(result) == len(EXISTING_WEEKS) + 1, (
        f"expected {len(EXISTING_WEEKS) + 1} total weeks, got {len(result)}: {sorted(result)}"
    )


def test_recon_week_overlapping_existing_is_replaced_not_duplicated(tmp_path):
    """A recon week whose key already exists in --out replaces that week's
    data (e.g. a correction run) rather than being skipped or duplicated."""
    out_path = str(tmp_path / "weekly-stats.json")
    _write_existing(out_path, EXISTING_WEEKS)

    recon_path = _recon(tmp_path, [
        {"index": 1, "start": "2026-01-19", "end": "2026-01-25",
         "cutoff": "2026-01-25T20:00:00+00:00", "prev_cutoff": "2026-01-18T20:00:00+00:00"},
    ])

    _run_main([recon_path, "--out", out_path])

    with open(out_path) as f:
        result = json.load(f)

    assert len(result) == len(EXISTING_WEEKS), "overlapping key must replace, not add"
    assert result["2026-01-19"].get("cutoff") == "2026-01-25T20:00:00+00:00", (
        "the replaced week should carry the recon's own cutoff field, proving it was regenerated"
    )


# ----------------------------------------------------- merge_weeks() unit --

def test_merge_weeks_is_pure_union():
    existing = {"2026-01-05": {"v": "old"}, "2026-01-12": {"v": "old"}}
    new_weeks = {"2026-01-12": {"v": "new"}, "2026-01-19": {"v": "new"}}
    merged = gen_stats.merge_weeks(existing, new_weeks)
    assert merged == {
        "2026-01-05": {"v": "old"},
        "2026-01-12": {"v": "new"},
        "2026-01-19": {"v": "new"},
    }
    # must not mutate the input
    assert existing == {"2026-01-05": {"v": "old"}, "2026-01-12": {"v": "old"}}


# ------------------------------------------- guard_against_shrink() unit --

def test_guard_against_shrink_refuses_without_force():
    """Direct unit test of the backstop: if the about-to-be-written result
    has fewer weeks than what's already on disk, refuse with a non-zero
    exit -- no --force given."""
    existing = {wk: {} for wk in EXISTING_WEEKS}
    merged = {wk: {} for wk in EXISTING_WEEKS[:-1]}  # one week short
    with pytest.raises(SystemExit) as exc_info:
        gen_stats.guard_against_shrink(merged, existing, force=False)
    assert exc_info.value.code != 0


def test_guard_against_shrink_allows_with_force():
    """Same shrink, but --force is set -- must NOT raise."""
    existing = {wk: {} for wk in EXISTING_WEEKS}
    merged = {wk: {} for wk in EXISTING_WEEKS[:-1]}
    gen_stats.guard_against_shrink(merged, existing, force=True)  # must not raise


def test_guard_against_shrink_allows_equal_or_growing():
    existing = {wk: {} for wk in EXISTING_WEEKS}
    same = dict(existing)
    grown = dict(existing)
    grown["2026-03-02"] = {}
    gen_stats.guard_against_shrink(same, existing, force=False)
    gen_stats.guard_against_shrink(grown, existing, force=False)


# ---------------------------------------- corrupt/unreadable --out file --
# Reeve's re-review of d48d8a3: main() turned ANY read error on --out
# (OSError OR json.JSONDecodeError) into `existing = {}`, so a corrupt or
# unreadable file was treated exactly like "first run, nothing published
# yet" -- which hands guard_against_shrink an empty `existing` and makes it
# compare against 0, so it can never fire. Reproduced by appending one
# garbage line to a copy of a real multi-week file and running a one-week
# recon against it: wrote 1 week, no error, no --force needed.
#
# Fix: only FileNotFoundError (the legitimate "nothing here yet" case) is
# treated as empty. Any other read/parse error exits non-zero, names the
# file, and writes nothing.

def test_corrupt_existing_file_refuses_and_leaves_file_untouched(tmp_path):
    out_path = str(tmp_path / "weekly-stats.json")
    good_data = _write_existing(out_path, EXISTING_WEEKS)
    with open(out_path, "a") as f:
        f.write("\nthis is not json at all {{{\n")  # corrupt it, like Reeve's repro
    corrupt_bytes = open(out_path, "rb").read()

    recon_path = _recon(tmp_path, [
        {"index": 1, "start": "2026-03-02", "end": "2026-03-08",
         "cutoff": "2026-03-08T20:00:00+00:00", "prev_cutoff": "2026-03-01T20:00:00+00:00"},
    ])

    with pytest.raises(SystemExit) as exc_info:
        _run_main([recon_path, "--out", out_path])
    assert exc_info.value.code != 0

    # file on disk must be byte-for-byte untouched by the refused write
    assert open(out_path, "rb").read() == corrupt_bytes


def test_unreadable_existing_file_refuses_and_leaves_file_untouched(tmp_path):
    """A file that exists but can't be opened (permission denied, not a
    parse error) must also refuse, not get treated as empty."""
    out_path = str(tmp_path / "weekly-stats.json")
    _write_existing(out_path, EXISTING_WEEKS)
    before_bytes = open(out_path, "rb").read()
    os.chmod(out_path, 0o000)
    try:
        if os.access(out_path, os.R_OK):
            pytest.skip("running as a user that bypasses file permissions (e.g. root)")

        recon_path = _recon(tmp_path, [
            {"index": 1, "start": "2026-03-02", "end": "2026-03-08",
             "cutoff": "2026-03-08T20:00:00+00:00", "prev_cutoff": "2026-03-01T20:00:00+00:00"},
        ])

        with pytest.raises(SystemExit) as exc_info:
            _run_main([recon_path, "--out", out_path])
        assert exc_info.value.code != 0
    finally:
        os.chmod(out_path, 0o644)

    assert open(out_path, "rb").read() == before_bytes


def test_missing_existing_file_is_still_treated_as_empty(tmp_path):
    """The legitimate case -- --out doesn't exist yet (first run) -- must
    still work with no --force, unaffected by the corrupt-file fix."""
    out_path = str(tmp_path / "weekly-stats.json")
    assert not os.path.exists(out_path)

    recon_path = _recon(tmp_path, [
        {"index": 1, "start": "2026-03-02", "end": "2026-03-08",
         "cutoff": "2026-03-08T20:00:00+00:00", "prev_cutoff": "2026-03-01T20:00:00+00:00"},
    ])
    _run_main([recon_path, "--out", out_path])

    with open(out_path) as f:
        result = json.load(f)
    assert list(result) == ["2026-03-02"]


# --------------------------------------- bug 7: week_label vs start key --
# The exact reported bug: week-of-2026-10-26's cutoff-mode recon had
# "start": "2026-10-23" (prev_cutoff's date, a Friday -- the real window
# boundary) but belonged to the week labeled "2026-10-26" (the Monday of
# the week containing the cutoff). Keying by "start" produced the wrong
# key and had to be renamed by hand in src/data/weekly-stats.json. A
# bucket that carries "week_label" (tools/gather.py's fix) must be keyed by
# THAT, not by "start".

def test_cutoff_bucket_with_week_label_is_keyed_by_week_label_not_start(tmp_path):
    out_path = str(tmp_path / "weekly-stats.json")

    recon_path = _recon(tmp_path, [
        {
            "index": 1,
            "start": "2026-10-23",  # prev_cutoff's date -- NOT the week key
            "end": "2026-10-30",
            "cutoff": "2026-10-30T23:01:41+00:00",
            "prev_cutoff": "2026-10-23T22:10:22+00:00",
            "week_label": "2026-10-26",  # the Monday of the cutoff's week -- the correct key
        },
    ])
    _run_main([recon_path, "--out", out_path])

    with open(out_path) as f:
        result = json.load(f)
    assert list(result) == ["2026-10-26"], (
        "must be keyed by week_label (the post's own Monday), not by start "
        "(prev_cutoff's date) -- this is the exact bug 7 regression"
    )
    assert result["2026-10-26"]["cutoff"] == "2026-10-30T23:01:41+00:00"
    assert result["2026-10-26"]["prev_cutoff"] == "2026-10-23T22:10:22+00:00"


def test_cutoff_bucket_without_week_label_still_keys_by_start(tmp_path):
    """Backward compatibility: a bucket with no "week_label" key at all
    (every existing recon file, and any future calendar-mode run) must
    still key by "start" exactly as before -- byte-identical."""
    out_path = str(tmp_path / "weekly-stats.json")

    recon_path = _recon(tmp_path, [
        {"index": 1, "start": "2026-03-02", "end": "2026-03-08",
         "cutoff": "2026-03-08T20:00:00+00:00", "prev_cutoff": "2026-03-01T20:00:00+00:00"},
    ])
    _run_main([recon_path, "--out", out_path])

    with open(out_path) as f:
        result = json.load(f)
    assert list(result) == ["2026-03-02"]
