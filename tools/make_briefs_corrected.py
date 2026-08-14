#!/usr/bin/env python3
"""
make_briefs_corrected.py — render the ground-truth-corrected recon JSON
(see verify_ground_truth.py) into drafts/week-<N>-brief-CORRECTED.md, and
print a diff summary against the original (buggy) recon JSON.

Same rendering conventions as make_briefs.py (exhaustive per-repo coverage,
full commit lists, bot-commit LOC flagging, featured/second-tier split) plus:
  - releases split into TAGGED (git tag / GitHub release object) vs
    COMMIT-MESSAGE-ONLY (a version-bump-looking commit subject with no
    corresponding tag or release object) per week, per repo.
  - a diff summary vs the original JSON: for every repo/week where the
    commit count or net LOC differs materially, print old -> new.

Usage:
    python3 tools/make_briefs_corrected.py \\
        data/recon-v2-8wk-20260814.json \\
        data/recon-v2-8wk-20260814-CORRECTED.json \\
        --out-dir drafts
"""

import argparse
import datetime
import json
import os

BOT_LOC_THRESHOLD = 10_000
BOT_DELETION_RATIO = 0.02

# Refined release-detection regexes (tighter than verify_ground_truth.py's
# first pass, which false-positived on dependency bumps like "chore(deps):
# bump @primeradianthq/obol to 0.7.0" or "bump codex CLI 0.142.5 -> 0.144.3"
# -- those are routine dependency maintenance, not the repo's own release).
import re

VERSION_RE = re.compile(r"\b(?:v)?\d+\.\d+\.\d+\b")
DEP_BUMP_RE = re.compile(r"\(deps\)|dependab|\bsdk\b|\bcli\b|@[a-z0-9_.\-]+/", re.IGNORECASE)
SELF_RELEASE_RE = re.compile(r"\brelease[:\s]+v?\d|\bchore\(release\)|\bbump version\b", re.IGNORECASE)


def find_commit_message_only_bumps(commits, release_tags):
    """A commit whose subject looks like the REPO'S OWN release/version bump
    (matches SELF_RELEASE_RE, not a dependency bump) with a semver-looking
    version that has NO corresponding tagged release this repo cut, counts
    as commit-message-only."""
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


def fmt_date(dt):
    return dt.date().isoformat()


def is_bot_commit(commit):
    author = commit.get("author", "")
    if "[bot]" not in author.lower():
        return False
    additions = commit.get("additions", 0)
    deletions = commit.get("deletions", 0)
    if additions < BOT_LOC_THRESHOLD:
        return False
    if deletions > additions * BOT_DELETION_RATIO:
        return False
    return True


def repo_provenance_line(r):
    desc = r["description"] or "[no description set on GitHub]"
    flags = []
    if r["fork"]:
        flags.append("fork")
    if r["archived"]:
        flags.append("archived")
    flag_str = f" ({', '.join(flags)})" if flags else ""
    return f"**{r['org']}/{r['name']}**{flag_str} — {desc}"


def fork_note(r):
    if not r["fork"]:
        return None
    parent = r.get("fork_parent")
    ahead = r.get("fork_ahead_by")
    if parent:
        return (
            f"FORK of `{parent}`. This repository is `{r['org']}`'s; the underlying project is "
            f"the community's (upstream: `{parent}`). Commit/LOC/author stats count ONLY commits "
            f"`{r['org']}`'s fork is ahead of upstream on (compare ahead_by="
            f"{ahead if ahead is not None else '[unknown]'}) — never inherited upstream history. "
            f"Not re-verified against ground truth in this pass (compare-API-derived, not "
            f"shallow-clone-based, so not subject to either bug being fixed here)."
        )
    return (
        "FORK with no accessible parent info. Stats may include inherited history — treat with caution."
    )


def build_week_data(data, week_idx, bucket):
    start, end = week_window(bucket)
    featured = []
    second_tier = []
    bot_commits_this_week = []
    tagged_releases_this_week = []
    message_only_bumps_this_week = []

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
            continue

        is_fork = r["fork"]
        created_dt = parse_dt(r["created_at"])
        created_this_week = (start <= created_dt < end) and not is_fork
        created_this_week_fork_raw = (start <= created_dt < end) and is_fork

        bot_flags = [is_bot_commit(c) for c in commits]
        for c, is_bot in zip(commits, bot_flags):
            if is_bot:
                bot_commits_this_week.append((r["full_name"], c))
        for rel in releases_this_week:
            tagged_releases_this_week.append((r["full_name"], rel))
        for bump in bumps_this_week:
            message_only_bumps_this_week.append((r["full_name"], bump))

        loc_added_raw = sum(c["additions"] for c in commits)
        loc_removed_raw = sum(c["deletions"] for c in commits)
        loc_added_debotted = sum(c["additions"] for c, b in zip(commits, bot_flags) if not b)
        loc_removed_debotted = sum(c["deletions"] for c, b in zip(commits, bot_flags) if not b)

        authors = w.get("authors", {})

        item = {
            "repo": r,
            "created_this_week": created_this_week,
            "created_this_week_fork_raw": created_this_week_fork_raw,
            "releases_this_week": releases_this_week,
            "message_only_bumps": bumps_this_week,
            "commits": commits,
            "bot_flags": bot_flags,
            "commit_count": len(commits),
            "merged_prs": merged_prs,
            "authors": authors,
            "loc_added_raw": loc_added_raw,
            "loc_removed_raw": loc_removed_raw,
            "loc_added_debotted": loc_added_debotted,
            "loc_removed_debotted": loc_removed_debotted,
        }

        if created_this_week or releases_this_week:
            featured.append(item)
        else:
            second_tier.append(item)

    return (
        featured, second_tier, bot_commits_this_week,
        tagged_releases_this_week, message_only_bumps_this_week, start, end,
    )


def render_repo_section(item, featured):
    r = item["repo"]
    lines = []
    lines.append(f"### {repo_provenance_line(r)}")
    lines.append(f"- language: {r['language'] or '[none set]'} · {r['html_url']}")

    fnote = fork_note(r)
    if fnote:
        lines.append(f"- {fnote}")

    if featured:
        why = []
        if item["created_this_week"]:
            why.append(f"created this week ({r['created_at']})")
        if item["created_this_week_fork_raw"]:
            why.append("NOTE: fork created this week — NOT counted as \"new project\"")
        for rel in item["releases_this_week"]:
            name_part = f' "{rel["name"]}"' if rel.get("name") else ""
            why.append(f'TAGGED release `{rel["tag"]}`{name_part} published {rel["published_at"]}')
        lines.append(f"- **FEATURED because:** {'; '.join(why)}")
    else:
        lines.append(
            "- **second-tier:** had commits/merged PRs this week but was not created this week and "
            "cut no TAGGED release this week"
        )

    if item["message_only_bumps"]:
        lines.append(f"- COMMIT-MESSAGE-ONLY version bump(s) this week (no tag/release object):")
        for bump in item["message_only_bumps"]:
            lines.append(f'  - `{bump["sha"]}` {bump["date"]} — "{bump["subject"]}" (version {bump["version"]})')

    lines.append(f"- commits this week: {item['commit_count']}")
    if item["merged_prs"]:
        lines.append(f"- merged PRs this week ({len(item['merged_prs'])}):")
        for pr in item["merged_prs"]:
            lines.append(f'  - #{pr["number"]} "{pr["title"]}" (merged {pr["merged_at"]})')
    else:
        lines.append("- merged PRs this week: none")

    if item["authors"]:
        author_str = ", ".join(f"{name} ({count})" for name, count in sorted(item["authors"].items(), key=lambda x: -x[1]))
        lines.append(f"- authors this week: {author_str}")
    else:
        lines.append("- authors this week: none (no commits)")

    raw_a, raw_d = item["loc_added_raw"], item["loc_removed_raw"]
    deb_a, deb_d = item["loc_added_debotted"], item["loc_removed_debotted"]
    if (raw_a, raw_d) != (deb_a, deb_d):
        lines.append(f"- LOC this week: +{raw_a}/-{raw_d} raw, +{deb_a}/-{deb_d} de-botted (see excluded commits below)")
    else:
        lines.append(f"- LOC this week: +{raw_a}/-{raw_d}")

    if item["commits"]:
        lines.append(f"- full commit list ({len(item['commits'])}):")
        for c, is_bot in zip(item["commits"], item["bot_flags"]):
            bot_tag = " [FLAGGED AS BOT/GENERATED]" if is_bot else ""
            lines.append(
                f"  - `{c['sha']}` {c['author']} {c['date']} — {c['subject']} "
                f"(+{c['additions']}/-{c['deletions']}, {c['files_changed']} file(s)){bot_tag}"
            )
    else:
        lines.append("- full commit list: none (release/PR only this week)")

    lines.append(
        "- [needs prose/context from Ada: what this release/these commits actually mean for users — "
        "the JSON has no changelog or release-notes content]"
    )
    lines.append("")
    return lines


def render_brief(bucket, featured, second_tier, bot_commits, tagged_releases, message_bumps, start, end):
    lines = []
    lines.append(
        f"# Week {bucket['index']} brief (CORRECTED) — {fmt_date(start)} to {fmt_date(end - datetime.timedelta(days=1))}"
    )
    lines.append("")
    lines.append(
        "Ground-truth corrected (full git clone, not shallow — see tools/verify_ground_truth.py for the "
        "root-cause of what changed vs the original briefs). Facts only below; turn into prose separately."
    )
    lines.append("")

    all_items = featured + second_tier
    total_commits_raw = sum(item["commit_count"] for item in all_items)
    total_prs = sum(len(item["merged_prs"]) for item in all_items)
    total_loc_added_raw = sum(item["loc_added_raw"] for item in all_items)
    total_loc_removed_raw = sum(item["loc_removed_raw"] for item in all_items)
    total_loc_added_debotted = sum(item["loc_added_debotted"] for item in all_items)
    total_loc_removed_debotted = sum(item["loc_removed_debotted"] for item in all_items)
    all_authors = set()
    for item in all_items:
        all_authors.update(item["authors"].keys())

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- repos active: {len(all_items)} ({len(featured)} featured, {len(second_tier)} second-tier)")
    lines.append(f"- commits: {total_commits_raw}")
    lines.append(f"- merged PRs: {total_prs}")
    lines.append(f"- LOC: +{total_loc_added_raw}/-{total_loc_removed_raw} raw")
    if (total_loc_added_raw, total_loc_removed_raw) != (total_loc_added_debotted, total_loc_removed_debotted):
        lines.append(f"- LOC (de-botted): +{total_loc_added_debotted}/-{total_loc_removed_debotted}")
        lines.append(f"- excluded bot/generated commits ({len(bot_commits)}):")
        for full_name, c in bot_commits:
            lines.append(
                f"  - `{full_name}` `{c['sha']}` {c['author']} {c['date']} — {c['subject']} "
                f"(+{c['additions']}/-{c['deletions']})"
            )
    else:
        lines.append("- LOC (de-botted): same as raw — no bot/generated commits detected this week")
    lines.append(f"- unique contributors: {len(all_authors)}")
    lines.append(f"- releases cut — TAGGED (git tag/GitHub release object): {len(tagged_releases)}")
    for full_name, rel in tagged_releases:
        lines.append(f'  - `{full_name}` `{rel["tag"]}` published {rel["published_at"]}')
    lines.append(f"- releases cut — COMMIT-MESSAGE-ONLY (version bump, no tag/release object): {len(message_bumps)}")
    for full_name, bump in message_bumps:
        lines.append(f'  - `{full_name}` `{bump["sha"]}` "{bump["subject"]}" (version {bump["version"]})')
    lines.append("")

    lines.append("## Featured (created this week, or cut a TAGGED release this week)")
    lines.append("")
    if not featured:
        lines.append("_None this week._")
        lines.append("")
    for item in featured:
        lines.extend(render_repo_section(item, featured=True))

    lines.append("## Also shipped (second-tier)")
    lines.append("")
    if not second_tier:
        lines.append("_None this week._")
        lines.append("")
    for item in second_tier:
        lines.extend(render_repo_section(item, featured=False))

    return "\n".join(lines) + "\n"


def diff_summary(original, corrected):
    lines = ["# Diff summary: original briefs vs ground-truth-corrected", ""]
    orig_by_key = {(r["org"], r["name"]): r for r in original["repos"]}
    for r in corrected["repos"]:
        key = (r["org"], r["name"])
        orig = orig_by_key.get(key)
        if not orig or not r.get("weeks") or not orig.get("weeks"):
            continue
        for wi in range(len(r["weeks"])):
            ow = orig["weeks"][wi]
            cw = r["weeks"][wi]
            if ow["commit_count"] != cw["commit_count"] or (ow["loc_added"], ow["loc_removed"]) != (cw["loc_added"], cw["loc_removed"]):
                loc_flag = ""
                if ow["loc_added"] > 0 and cw["loc_added"] > 0 and ow["loc_added"] / max(cw["loc_added"], 1) > 50:
                    loc_flag = "  <-- WHOLE-REPO-SIZE LOC INFLATION (bug 1)"
                lines.append(
                    f"- {r['org']}/{r['name']} week {wi+1}: commits {ow['commit_count']}->{cw['commit_count']}, "
                    f"LOC +{ow['loc_added']}/-{ow['loc_removed']} -> +{cw['loc_added']}/-{cw['loc_removed']}{loc_flag}"
                )
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original_json")
    ap.add_argument("corrected_json")
    ap.add_argument("--out-dir", default="drafts")
    args = ap.parse_args()

    original = json.load(open(args.original_json))
    corrected = json.load(open(args.corrected_json))
    os.makedirs(args.out_dir, exist_ok=True)

    for week_idx, bucket in enumerate(corrected["week_buckets"]):
        featured, second_tier, bot_commits, tagged_releases, message_bumps, start, end = build_week_data(
            corrected, week_idx, bucket
        )
        text = render_brief(bucket, featured, second_tier, bot_commits, tagged_releases, message_bumps, start, end)
        out_path = os.path.join(args.out_dir, f"week-{bucket['index']}-brief-CORRECTED.md")
        with open(out_path, "w") as f:
            f.write(text)
        print(f"wrote {out_path} ({len(featured)} featured, {len(second_tier)} second-tier)")

    diff_text = diff_summary(original, corrected)
    diff_path = os.path.join(args.out_dir, "..", "data", "correction-diff-summary.md")
    diff_path = os.path.normpath(diff_path)
    with open(diff_path, "w") as f:
        f.write(diff_text)
    print(f"wrote {diff_path}")


if __name__ == "__main__":
    main()
