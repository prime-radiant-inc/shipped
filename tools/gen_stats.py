#!/usr/bin/env python3
"""
gen_stats.py — reads the ground-truth-corrected recon JSON and emits
src/data/weekly-stats.json, the single source of truth the Astro components
(WeekSummary.astro, RepoStat.astro) read at build time. No post should ever
hand-type a commit count, LOC figure, or release count again.

WEEKS ARE KEYED BY ISO START DATE (e.g. "2026-06-22"), NOT ORDINAL INDEX.
This is deliberate: ordinal week numbers ('week-1', 'week-2', ...) make
backfilling an older week later a renumbering exercise across every post,
component call, and slug. A date key is stable forever — a newly-backfilled
week just drops in at its own date, nothing else shifts.

Classification logic here is a DELIBERATE, exact match of
tools/make_briefs_corrected.py's build_week_data()/find_commit_message_only_bumps()
— same regexes, same featured/second-tier rule, same tagged-vs-message-only
release split. If you change one, change both (or better: factor this into
a shared module next time).

Usage:
    python3 tools/gen_stats.py data/recon-v2-8wk-20260814-CORRECTED.json \\
        --out src/data/weekly-stats.json
"""

import argparse
import datetime
import json
import os
import re
import sys
import tempfile

# ---- exact copies from tools/make_briefs_corrected.py — keep in sync ----

VERSION_RE = re.compile(r"\b(?:v)?\d+\.\d+\.\d+\b")
DEP_BUMP_RE = re.compile(r"\(deps\)|dependab|\bsdk\b|\bcli\b|@[a-z0-9_.\-]+/", re.IGNORECASE)
SELF_RELEASE_RE = re.compile(r"\brelease[:\s]+v?\d|\bchore\(release\)|\bbump version\b", re.IGNORECASE)


def find_commit_message_only_bumps(commits, release_tags):
    out = []
    for c in commits:
        subj = c["subject"]
        if DEP_BUMP_RE.search(subj):
            continue
        if not SELF_RELEASE_RE.search(subj):
            continue
        vm = VERSION_RE.search(subj)
        if not vm:
            continue
        version = vm.group(0).lstrip("v")
        if version in release_tags:
            continue
        out.append({"sha": c["sha"], "date": c["date"], "subject": subj, "version": version})
    return out


def parse_dt(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


# KNOWN-IDENTITY EMAIL ALIASES: for a handful of emails GitHub can never
# resolve to a login (no linked account -- `author.login` is permanently
# null for these, confirmed by direct query), so contributor_identity()'s
# login-then-email fallback would otherwise treat them as their own
# separate, unlinkable identity forever. Add an entry here ONLY after a
# human confirms the real person out-of-band (never guess from name
# similarity alone -- see the jtdaugh case, a different real person who
# happened to share Jesse Vincent's first name).
#
# jesse@magic-kingdom -> obra (Jesse Vincent): confirmed by Jesse himself.
# Seen on `jesse`-authored commits across obra/superpowers,
# obra/superpowers-lab, obra/superpowers-marketplace,
# obra/claude-session-driver, and prime-radiant-inc/serf (now evener) in
# weeks 2026-03-09, 03-16, 03-23, 05-11, and 05-18 -- every single commit
# under that email in those weeks (not just a sample; paginated through
# the full commits list for each repo/week) uses this exact address, no
# exceptions found.
#
# Deliberately NOT aliased (same investigation, different outcome):
# jesse@localhost and jesse@paradise-park.local (both seen on
# prime-radiant-inc/evener, week 2026-08-03, under "Jesse"/"jesse") --
# also login-less, but NOT confirmed as Jesse Vincent (or as each other:
# the two differ), so left as their own separate, unmerged identities.
EMAIL_ALIASES = {
    "jesse@magic-kingdom": "login:obra",
}


def contributor_identity(c):
    """Resolve a commit to a stable per-person identity for CONTRIBUTOR
    COUNTING (the week summary's `contributors` figure) -- NOT the same
    thing as the per-repo `authors` display list below, which stays
    keyed by git-config display name on purpose (it's meant to show the
    name as it actually appears in the log).

    CONTRIBUTOR-COUNTING DEDUPE FIX: the same person can commit under
    different git-config display names in different repos -- e.g. Ada
    Sen's commits show up as "Ada Sen" in one repo and "ada-sen" in
    another, same email (ada.sen@primeradiant.com) and GitHub login
    (ada-sen) both times. Counting by name double-counted her. Prefer
    GitHub login (only available for fork-with-parent/compare-API-
    sourced commits -- see gather.py), fall back to a normalized email
    (available for local-git-log-sourced commits via %ae, added
    alongside this fix), and fall back to the raw author name only for
    recon JSON generated before this fix added login/email capture (so
    old cached recon files don't crash, though a *report* run against
    one won't get the fix's benefit -- regenerate the recon JSON to get
    deduped counts for a given week).

    Bots are NOT special-cased here, deliberately: they keep counting as
    contributors, matching week-of-2026-09-14's already-committed value
    (10 contributors including `github-actions[bot]` and
    `dependabot[bot]` -- confirmed by recomputing that week's distinct
    author-name count against its stored weekly-stats.json entry, which
    matches exactly, i.e. that week had no same-person/different-name
    collision to begin with). Each bot's email is consistent across
    repos (e.g. `github-actions[bot]@users.noreply.github.com`), so it
    still dedupes to exactly one identity per bot account, same as
    before.
    """
    login = c.get("login")
    if login:
        return f"login:{login}"
    email = c.get("email")
    if email:
        email = email.strip().lower()
        if email in EMAIL_ALIASES:
            return EMAIL_ALIASES[email]
        return f"email:{email}"
    return f"name:{c['author']}"


def week_window(bucket):
    start = datetime.datetime.fromisoformat(bucket["start"]).replace(tzinfo=datetime.timezone.utc)
    end_inclusive_date = datetime.datetime.fromisoformat(bucket["end"]).replace(tzinfo=datetime.timezone.utc)
    end_exclusive = end_inclusive_date + datetime.timedelta(days=1)
    return start, end_exclusive


# ---------------------------------------------------------------------- --


def build_week(data, week_idx, bucket):
    start, end = week_window(bucket)
    repos_out = {}
    featured_count = 0
    second_tier_count = 0
    total_commits = 0
    total_prs = 0
    total_loc_added = 0
    total_loc_removed = 0
    all_authors = set()
    tagged_release_count = 0
    commit_only_bump_count = 0

    for r in data["repos"]:
        weeks = r.get("weeks")
        if not weeks or week_idx >= len(weeks):
            continue
        w = weeks[week_idx]
        commits = w.get("commits", [])
        merged_prs = w.get("merged_prs", [])

        releases_this_week = [
            rel for rel in r.get("releases_in_window", []) if start <= parse_dt(rel["published_at"]) < end
        ]
        all_release_tags = set(rel["tag"].lstrip("v") for rel in r.get("releases_in_window", []))
        bumps_this_week = find_commit_message_only_bumps(commits, all_release_tags)

        if not commits and not merged_prs and not releases_this_week and not bumps_this_week:
            continue  # no activity this week -> not in output at all

        is_fork = r["fork"]
        created_dt = parse_dt(r["created_at"])
        created_this_week = (start <= created_dt < end) and not is_fork

        featured = bool(created_this_week or releases_this_week)
        if featured:
            featured_count += 1
            reasons = []
            if created_this_week:
                reasons.append(f"created this week ({r['created_at']})")
            for rel in releases_this_week:
                reasons.append(f"tagged release {rel['tag']} published {rel['published_at']}")
            featured_reason = "; ".join(reasons)
        else:
            second_tier_count += 1
            featured_reason = None

        authors_dict = w.get("authors", {})
        authors_list = [{"name": name, "count": count} for name, count in
                        sorted(authors_dict.items(), key=lambda x: -x[1])]
        # Contributor COUNTING dedupes by identity (login/email), not by
        # display name -- see contributor_identity()'s docstring. The
        # authors_list above stays name-keyed; it's a display list, not
        # a count.
        all_authors.update(contributor_identity(c) for c in commits)

        commit_count = w.get("commit_count", len(commits))
        loc_added = w.get("loc_added", 0)
        loc_removed = w.get("loc_removed", 0)
        # loc_suppressed: a ground-truth call that this cell's churn is a
        # data-dump / vendored / generated-artifact / revert-of-revert and
        # not real authored work (see RepoStat.astro, which hides the
        # +/- LOC chip for these cells). Historically this flag was
        # hand-added directly to the emitted weekly-stats.json AFTER this
        # script ran, and the week summary was "recomputed" by a second,
        # easy-to-forget manual pass -- which is exactly how the week-total
        # leak happened: build_week() summed every cell's raw LOC into
        # total_loc_added/total_loc_removed with zero awareness the flag
        # existed. Honor it HERE, at the point of aggregation, if the recon
        # week dict already carries it (e.g. hand-annotated recon input).
        # Raw per-cell numbers are still recorded and still visible to
        # RepoStat.astro -- only the week TOTAL excludes them.
        loc_suppressed = bool(w.get("loc_suppressed", False))

        total_commits += commit_count
        total_prs += len(merged_prs)
        if not loc_suppressed:
            total_loc_added += loc_added
            total_loc_removed += loc_removed
        tagged_release_count += len(releases_this_week)
        commit_only_bump_count += len(bumps_this_week)

        key = r["full_name"]
        repos_out[key] = {
            "commits": commit_count,
            "authors": authors_list,
            "loc_added": loc_added,
            "loc_removed": loc_removed,
            "merged_prs": merged_prs,
            "tagged_releases": releases_this_week,
            "commit_only_bumps": bumps_this_week,
            "featured": featured,
            "featured_reason": featured_reason,
            "description": r.get("description"),
            "html_url": r["html_url"],
        }
        if loc_suppressed:
            repos_out[key]["loc_suppressed"] = True

    summary = {
        "repos_active": len(repos_out),
        "featured_count": featured_count,
        "second_tier_count": second_tier_count,
        "commits": total_commits,
        "merged_prs": total_prs,
        "loc_added": total_loc_added,
        "loc_removed": total_loc_removed,
        "contributors": len(all_authors),
        "tagged_releases": tagged_release_count,
        "commit_only_bumps": commit_only_bump_count,
    }

    result = {"summary": summary, "repos": repos_out}
    # CUTOFF-WINDOW-NO-MERGES MODE (see tools/gather.py module docstring,
    # bug 6): a recon bucket produced by `gather.py --cutoff` carries exact
    # `cutoff`/`prev_cutoff` timestamps (added there, not just a calendar
    # start/end date). Carry them straight through onto this week's own
    # entry in weekly-stats.json -- this IS the "record it going forward"
    # field rule 2 asks for: once a week has these, the NEXT invocation of
    # `gather.py --cutoff` (via resolve_prev_cutoff) can read `cutoff` back
    # out as its own --prev-cutoff, without a human re-typing or guessing
    # it. A bucket without these keys (every existing recon file, and any
    # future calendar-mode run) adds NEITHER key here -- this is exactly
    # why every already-published week's weekly-stats.json entry stays
    # byte-identical: the key is only ever added, never defaulted in.
    if bucket.get("cutoff"):
        result["cutoff"] = bucket["cutoff"]
    if bucket.get("prev_cutoff"):
        result["prev_cutoff"] = bucket["prev_cutoff"]
    return result


def atomic_write(path, content):
    """Write `content` (a str) to `path` without ever leaving a partial or
    corrupt file behind if the process dies mid-write: write to a temp
    file in the same directory, then atomically `os.replace` it into
    place. (PR #4 re-review, non-blocking: a plain `open(path, 'w')`
    truncates the file immediately, before any new content lands -- a
    crash or kill between the truncate and the write leaves exactly the
    kind of corrupt file the --out guard above now refuses to paper over
    as "empty". This closes the most likely way to ever get there.)
    """
    directory = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=os.path.basename(path) + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise


def merge_weeks(existing, new_weeks):
    """Merge a recon's weeks into an existing weekly-stats.json's data.

    A pure key-set union: any week in `existing` that is NOT present in
    `new_weeks` is carried through untouched (byte-for-byte, since we never
    even look at its value); any week present in `new_weeks` -- whether or
    not it was already in `existing` -- takes the new value. This is what
    makes a `--cutoff`-mode recon (tools/gather.py), which always produces
    exactly ONE week bucket, safe to run against the full multi-week
    weekly-stats.json: it can only ever ADD or REPLACE its own single
    week, never drop any other week.

    KEY ORDER (PR #4 review, non-blocking): `dict.update` appends any
    brand-new key (a week not already in `existing`, e.g. a backfilled
    older week published out of order) at the END of iteration order --
    so the resulting dict's key order is insertion order, not
    chronological. Harmless today: both gen_stats.py's own callers and
    the Astro components that read weekly-stats.json look a week up by
    its date-string key, never by position. Noted here so a future reader
    doesn't assume (or rely on) chronological file order.

    Does not mutate either input.
    """
    merged = dict(existing)
    merged.update(new_weeks)
    return merged


def guard_against_shrink(merged, existing, force):
    """Refuse (SystemExit, non-zero) to proceed if `merged` would have
    FEWER weeks than `existing` already has -- i.e. writing it would
    silently drop already-published weeks -- unless `force` is true.

    This is a defense-in-depth backstop, independent of `merge_weeks`
    above: a pure key-set union can never by itself produce a shrink, so
    under normal operation this guard should never fire. It exists for
    every OTHER way `main()` could end up writing a smaller result (a
    stale/misconfigured --out, a future change to the merge itself, a
    hand-edited recon) -- see PR #4 review: "the next step of this feature
    wipes published history."
    """
    if len(merged) < len(existing) and not force:
        sys.exit(
            f"ERROR: refusing to write {len(merged)} week(s) -- the "
            f"existing file already has {len(existing)}. This would "
            f"silently drop {len(existing) - len(merged)} already-published "
            "week(s). Pass --force if this is deliberate."
        )


def recompute_summaries(weekly_stats):
    """Belt-and-suspenders regen mode: operates directly on an EXISTING
    src/data/weekly-stats.json (as opposed to the full recon-json pipeline
    above), recomputing only summary.loc_added/summary.loc_removed for
    every week to exclude any repo cell with loc_suppressed: true.

    Why this exists as a separate path from build_week(): the merged
    weekly-stats.json on disk is the union of many backfill batches, each
    generated from its OWN recon-*.json at a different point in time (not
    all of which are still on disk, and none of which carried a
    loc_suppressed field in their source data -- that flag was applied by
    hand directly to the emitted JSON, per-batch, after generation). This
    mode re-derives every week's stored total straight from the per-cell
    loc_added/loc_removed/loc_suppressed values already sitting in the
    merged file, so a from-scratch recon re-run is never required to fix
    a stale/leaked total. commits, merged_prs, contributors,
    featured/second_tier counts, releases, and all per-repo cell data are
    left byte-for-byte untouched.
    """
    changed = []
    for week_key, week_data in weekly_stats.items():
        repos = week_data.get("repos", {})
        new_added = sum(r["loc_added"] for r in repos.values() if not r.get("loc_suppressed"))
        new_removed = sum(r["loc_removed"] for r in repos.values() if not r.get("loc_suppressed"))
        summary = week_data["summary"]
        old_added, old_removed = summary["loc_added"], summary["loc_removed"]
        if old_added != new_added or old_removed != new_removed:
            suppressed_repos = [name for name, r in repos.items() if r.get("loc_suppressed")]
            changed.append((week_key, old_added, old_removed, new_added, new_removed, suppressed_repos))
        summary["loc_added"] = new_added
        summary["loc_removed"] = new_removed
    return changed


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recon_json", nargs="?", help="omit when using --recompute-summaries")
    ap.add_argument("--out", default="src/data/weekly-stats.json")
    ap.add_argument(
        "--recompute-summaries",
        metavar="WEEKLY_STATS_JSON",
        help=(
            "Skip the recon pipeline; load an existing weekly-stats.json, "
            "recompute every week's summary.loc_added/loc_removed to "
            "exclude loc_suppressed cells, and write back to --out "
            "(defaults to the input path, i.e. in place)."
        ),
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help=(
            "Allow writing --out with fewer weeks than it currently has "
            "(see guard_against_shrink). Only needed if you deliberately "
            "intend to drop already-published week(s); normal incremental "
            "(--cutoff-mode) runs never need this."
        ),
    )
    args = ap.parse_args()

    if args.recompute_summaries:
        with open(args.recompute_summaries) as f:
            weekly_stats = json.load(f)
        changed = recompute_summaries(weekly_stats)
        out_path = args.out if args.out != "src/data/weekly-stats.json" else args.recompute_summaries
        atomic_write(out_path, json.dumps(weekly_stats, indent=2) + "\n")
        print(f"recomputed summaries -> {out_path}")
        for week_key, old_a, old_r, new_a, new_r, sup in changed:
            print(
                f"  {week_key}: loc_added {old_a} -> {new_a}, "
                f"loc_removed {old_r} -> {new_r} (suppressed: {', '.join(sup)})"
            )
        if not changed:
            print("  no week needed correction")
        return

    if not args.recon_json:
        ap.error("recon_json is required unless --recompute-summaries is given")

    data = json.load(open(args.recon_json))
    new_weeks = {}
    for week_idx, bucket in enumerate(data["week_buckets"]):
        # Date key, not ordinal -- e.g. "2026-06-22". See module docstring.
        # Cutoff-window buckets (tools/gather.py --cutoff) carry an
        # explicit "week_label" -- the Monday of the calendar week
        # containing the cutoff -- distinct from "start" (the real,
        # sub-week window boundary build_week() uses above for its
        # created-this-week/released-this-week filtering). Keying by
        # "start" in that mode keys by the PREVIOUS cutoff's date instead
        # of the post's own week (bug 7: week-of-2026-10-26 got keyed
        # "2026-10-23", a Friday, and had to be renamed by hand). A
        # calendar-mode bucket (or any older recon file) carries no
        # "week_label" key at all, so it falls back to "start" exactly as
        # before -- byte-identical.
        key = bucket.get("week_label") or bucket["start"]
        new_weeks[key] = build_week(data, week_idx, bucket)

    # MERGE, DON'T REPLACE (PR #4 review, blocking): load whatever is
    # already at --out (if anything) and merge this recon's weeks into it,
    # rather than starting from `{}`. A full from-scratch recon (every
    # week_buckets entry covering the repo's whole history) still produces
    # the complete file either way, since its new_weeks IS the full set;
    # an incremental --cutoff recon (one bucket) now only ever touches its
    # own week. See merge_weeks()/guard_against_shrink() above.
    #
    # CORRUPT/UNREADABLE --out FIX (PR #4 re-review): only a genuinely
    # MISSING file (FileNotFoundError -- the legitimate "nothing published
    # yet" first run) is treated as empty. Any other read failure --
    # json.JSONDecodeError (corrupt contents) or any other OSError (e.g.
    # PermissionError) -- used to also fall through to `existing = {}`,
    # which handed guard_against_shrink an empty baseline it can never
    # shrink below, silently defeating it. Reproduced: append one garbage
    # line to a real multi-week file, run a one-week recon against it --
    # old code wrote 1 week, no error, no --force. Now it exits non-zero,
    # names the file, and writes nothing.
    try:
        with open(args.out) as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = {}
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(
            f"ERROR: could not read existing {args.out} to merge into "
            f"({type(e).__name__}: {e}). Refusing to treat an unreadable "
            "or corrupt file as empty -- that would silently defeat "
            "guard_against_shrink (it would have nothing to compare "
            "against). Fix or remove the file by hand if starting fresh "
            "is actually what you want."
        )

    merged = merge_weeks(existing, new_weeks)
    guard_against_shrink(merged, existing, args.force)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    atomic_write(args.out, json.dumps(merged, indent=2))
    print(
        f"wrote {args.out} ({len(new_weeks)} week(s) from recon merged into "
        f"{len(existing)} existing -> {len(merged)} total)"
    )


if __name__ == "__main__":
    main()
