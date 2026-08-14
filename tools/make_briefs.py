#!/usr/bin/env python3
"""
make_briefs.py (v2) — turn a v2 recon JSON (see gather.py) into per-week
FACTUAL briefs at drafts/week-<N>-brief.md.

These briefs are bullet facts only, pulled straight from the JSON — no
invented prose. Where the JSON doesn't have a human-meaningful detail (e.g.
what a release actually contains), the brief says so explicitly rather than
guessing, so whoever writes the real post knows what to go fill in by hand.

Ported from v1 to the v2 exhaustive/commit-driven schema
(`repo['weeks'][i]['commits']`, full per-commit sha/author/date/subject/LOC,
no PR/release-only filtering — see gather.py's docstring). Differences from
v1's briefs:

  - EXHAUSTIVE per-repo coverage: every repo with any in-window activity
    that week gets a section, not just ones with a PR or release.
  - Every repo section includes the FULL list of that week's commit
    subjects + short SHA + author + date (not just a count) — this is the
    material a real change summary gets written from.
  - Bot/generated-commit detection: a commit is flagged as likely
    bot-generated noise (and excluded from "de-botted" LOC totals, though
    never hidden — it's always listed) if ALL of:
      * author name contains "[bot]" (the standard GitHub bot suffix), AND
      * additions >= BOT_LOC_THRESHOLD, AND
      * deletions <= additions * BOT_DELETION_RATIO (i.e. almost pure
        addition, characteristic of a regenerated lockfile/dataset/README
        rather than an edit).
    Both the raw and de-botted LOC figures are printed everywhere, with the
    excluded commit(s) listed explicitly (repo, sha, author, +/-, subject)
    so nothing is silently hidden — this is a presentation choice for the
    humans writing prose from these briefs, not a claim that the commit
    didn't happen.
  - FEATURED = created in-window this specific week (non-fork — a fork's
    created_at is the fork date, not the upstream project's birth, so forks
    never trigger "new" on their own) OR had >=1 release published this
    specific week. Everything else with activity is "second-tier" (not
    absent — v2's whole point is exhaustiveness).

Usage:
    python3 tools/make_briefs.py data/recon-v2-8wk-20260814.json
    python3 tools/make_briefs.py data/recon-v2-8wk-20260814.json --out-dir drafts
"""

import argparse
import datetime
import json
import os

BOT_LOC_THRESHOLD = 10_000  # additions at/above this size, from a [bot] author, are suspect
BOT_DELETION_RATIO = 0.02  # deletions must be <= this fraction of additions to count as "regen-shaped"


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
    """Flag commits that look like an automated regen/dump rather than
    real authored work: [bot] author, huge additions, near-zero deletions."""
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
            f"the community's (upstream: `{parent}`). Commit/LOC/author stats below count ONLY "
            f"commits `{r['org']}`'s fork is ahead of upstream on "
            f"(compare ahead_by={ahead if ahead is not None else '[unknown]'}) — never inherited "
            f"upstream history."
        )
    return (
        "FORK with no accessible parent info (upstream may be deleted/renamed). Commit stats below "
        "could NOT be filtered against upstream and may include inherited history — treat with caution."
    )


def build_week_data(data, week_idx, bucket):
    start, end = week_window(bucket)
    featured = []
    second_tier = []
    bot_commits_this_week = []  # (repo_full_name, commit) for the summary block

    for r in data["repos"]:
        weeks = r.get("weeks")
        if not weeks or week_idx >= len(weeks):
            continue
        w = weeks[week_idx]
        commits = w.get("commits", [])
        merged_prs = w.get("merged_prs", [])
        if not commits and not merged_prs:
            # also check releases separately below; repos with ONLY a release
            # this week (no commits/PRs) still need to show up.
            pass

        releases_this_week = [
            rel for rel in r.get("releases_in_window", []) if start <= parse_dt(rel["published_at"]) < end
        ]

        if not commits and not merged_prs and not releases_this_week:
            continue  # genuinely nothing this week for this repo

        is_fork = r["fork"]
        created_dt = parse_dt(r["created_at"])
        created_this_week = (start <= created_dt < end) and not is_fork
        created_this_week_fork_raw = (start <= created_dt < end) and is_fork

        bot_flags = [is_bot_commit(c) for c in commits]
        for c, is_bot in zip(commits, bot_flags):
            if is_bot:
                bot_commits_this_week.append((r["full_name"], c))

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

    return featured, second_tier, bot_commits_this_week, start, end


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
            why.append(
                f"NOTE: fork was created this week ({r['created_at']}) but that is NOT counted as "
                f"\"new project\" (fork date != upstream project's birth)"
            )
        for rel in item["releases_this_week"]:
            name_part = f' "{rel["name"]}"' if rel.get("name") else ""
            pre = " (prerelease)" if rel.get("prerelease") else ""
            why.append(f'release `{rel["tag"]}`{name_part}{pre} published {rel["published_at"]}')
        lines.append(f"- **FEATURED because:** {'; '.join(why)}")
    else:
        lines.append(
            "- **second-tier:** had commits/merged PRs this week but was not created this week and "
            "cut no release this week"
        )
        if item["releases_this_week"]:
            # shouldn't happen given build_week_data logic, but guard anyway
            for rel in item["releases_this_week"]:
                lines.append(f'  - release `{rel["tag"]}` published {rel["published_at"]}')

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

    if not item["releases_this_week"] and featured is False:
        pass  # releases already shown above for featured items

    if item["commits"]:
        lines.append(f"- full commit list ({len(item['commits'])}):")
        for c, is_bot in zip(item["commits"], item["bot_flags"]):
            bot_tag = " [FLAGGED AS BOT/GENERATED — see summary]" if is_bot else ""
            lines.append(
                f"  - `{c['sha']}` {c['author']} {c['date']} — {c['subject']} "
                f"(+{c['additions']}/-{c['deletions']}, {c['files_changed']} file(s)){bot_tag}"
            )
    else:
        lines.append("- full commit list: none (release/PR only this week)")

    lines.append(
        "- [needs prose/context from Ada: what this release/these commits actually mean for users — "
        "the JSON has no changelog or release-notes content, only commit subjects and PR titles]"
    )
    lines.append("")
    return lines


def render_brief(bucket, featured, second_tier, bot_commits_this_week, start, end):
    lines = []
    lines.append(f"# Week {bucket['index']} brief — {fmt_date(start)} to {fmt_date(end - datetime.timedelta(days=1))}")
    lines.append("")
    lines.append(
        "Facts only below, pulled verbatim from data/recon-v2-8wk-20260814.json. "
        "Every repo with ANY in-window activity this week is listed — this is exhaustive, not curated. "
        "Turn into prose separately; do not invent changelog content beyond what's here."
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
    total_releases = sum(len(item["releases_this_week"]) for item in all_items)

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- repos active: {len(all_items)} ({len(featured)} featured, {len(second_tier)} second-tier)")
    lines.append(f"- commits: {total_commits_raw}")
    lines.append(f"- merged PRs: {total_prs}")
    lines.append(f"- LOC: +{total_loc_added_raw}/-{total_loc_removed_raw} raw")
    if (total_loc_added_raw, total_loc_removed_raw) != (total_loc_added_debotted, total_loc_removed_debotted):
        lines.append(f"- LOC (de-botted): +{total_loc_added_debotted}/-{total_loc_removed_debotted}")
        lines.append(f"- excluded bot/generated commits ({len(bot_commits_this_week)}):")
        for full_name, c in bot_commits_this_week:
            lines.append(
                f"  - `{full_name}` `{c['sha']}` {c['author']} {c['date']} — {c['subject']} "
                f"(+{c['additions']}/-{c['deletions']})"
            )
    else:
        lines.append("- LOC (de-botted): same as raw — no bot/generated commits detected this week")
    lines.append(f"- unique contributors: {len(all_authors)}")
    lines.append(f"- releases cut: {total_releases}")
    lines.append("")

    lines.append("## Featured (created this week, or cut a release this week)")
    lines.append("")
    if not featured:
        lines.append("_None this week._")
        lines.append("")
    for item in featured:
        lines.extend(render_repo_section(item, featured=True))

    lines.append("## Also shipped (second-tier — active but not new/released this week)")
    lines.append("")
    if not second_tier:
        lines.append("_None this week._")
        lines.append("")
    for item in second_tier:
        lines.extend(render_repo_section(item, featured=False))

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recon_json", help="path to a v2 recon JSON produced by gather.py")
    ap.add_argument("--out-dir", default="drafts", help="output directory (default: drafts)")
    args = ap.parse_args()

    data = json.load(open(args.recon_json))
    os.makedirs(args.out_dir, exist_ok=True)

    for week_idx, bucket in enumerate(data["week_buckets"]):
        featured, second_tier, bot_commits_this_week, start, end = build_week_data(data, week_idx, bucket)
        text = render_brief(bucket, featured, second_tier, bot_commits_this_week, start, end)
        out_path = os.path.join(args.out_dir, f"week-{bucket['index']}-brief.md")
        with open(out_path, "w") as f:
            f.write(text)
        size_kb = len(text) / 1024
        print(
            f"wrote {out_path} ({len(featured)} featured, {len(second_tier)} second-tier, "
            f"{size_kb:.1f} KB)"
        )


if __name__ == "__main__":
    main()
