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
        all_authors.update(authors_dict.keys())

        commit_count = w.get("commit_count", len(commits))
        loc_added = w.get("loc_added", 0)
        loc_removed = w.get("loc_removed", 0)

        total_commits += commit_count
        total_prs += len(merged_prs)
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

    return {"summary": summary, "repos": repos_out}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recon_json")
    ap.add_argument("--out", default="src/data/weekly-stats.json")
    args = ap.parse_args()

    data = json.load(open(args.recon_json))
    out = {}
    for week_idx, bucket in enumerate(data["week_buckets"]):
        # Date key, not ordinal -- e.g. "2026-06-22". See module docstring.
        out[bucket["start"]] = build_week(data, week_idx, bucket)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
