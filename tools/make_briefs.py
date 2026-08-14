#!/usr/bin/env python3
"""
make_briefs.py — turn a recon JSON (see gather.py) into per-week FACTUAL
briefs at drafts/week-<N>-brief.md.

These briefs are bullet facts only, pulled straight from the JSON — no
invented prose. Where the JSON doesn't have a human-meaningful detail (e.g.
what a release actually contains), the brief says so explicitly rather than
guessing, so whoever writes the real post knows what to go fill in by hand.

Usage:
    python3 tools/make_briefs.py data/recon-8wk.json
    python3 tools/make_briefs.py data/recon-8wk.json --out-dir drafts
"""

import argparse
import datetime
import json
import os


def parse_dt(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def week_window(bucket):
    start = datetime.datetime.fromisoformat(bucket["start"]).replace(tzinfo=datetime.timezone.utc)
    end_inclusive_date = datetime.datetime.fromisoformat(bucket["end"]).replace(tzinfo=datetime.timezone.utc)
    end_exclusive = end_inclusive_date + datetime.timedelta(days=1)
    return start, end_exclusive


def repo_line(r):
    desc = r["description"] or "[no description set on GitHub]"
    flags = []
    if r["fork"]:
        flags.append("fork")
    if r["archived"]:
        flags.append("archived")
    flag_str = f" ({', '.join(flags)})" if flags else ""
    return f"**{r['name']}**{flag_str} — {desc}"


def build_week_section(data, week_idx, bucket):
    start, end = week_window(bucket)
    featured = []
    second_tier = []

    for r in data["repos"]:
        is_fork = r["fork"]
        created_dt = parse_dt(r["created_at"])
        created_this_week = (start <= created_dt < end) and not is_fork

        releases_this_week = [
            rel for rel in r.get("releases_in_window", []) if start <= parse_dt(rel["published_at"]) < end
        ]

        commits_weekly = r.get("commits_in_window", {}).get("weekly", [])
        commit_count = commits_weekly[week_idx] if week_idx < len(commits_weekly) else 0

        prs_this_week = [
            pr
            for pr in r.get("merged_prs_in_window", {}).get("list", [])
            if start <= parse_dt(pr["merged_at"]) < end
        ]

        if created_this_week or releases_this_week:
            featured.append(
                {
                    "repo": r,
                    "created_this_week": created_this_week,
                    "releases_this_week": releases_this_week,
                    "commit_count": commit_count,
                    "prs_this_week": prs_this_week,
                }
            )
        elif commit_count > 0 or prs_this_week:
            second_tier.append(
                {
                    "repo": r,
                    "commit_count": commit_count,
                    "prs_this_week": prs_this_week,
                }
            )

    return featured, second_tier, start, end


def fmt_date(dt):
    return dt.date().isoformat()


def render_brief(week_idx, bucket, featured, second_tier, start, end):
    lines = []
    lines.append(f"# Week {bucket['index']} brief — {fmt_date(start)} to {fmt_date(end - datetime.timedelta(days=1))}")
    lines.append("")
    lines.append(
        f"**Counts:** {len(featured)} featured, {len(second_tier)} second-tier. "
        f"(Facts only below — pulled verbatim from data/recon-8wk.json. Turn into prose separately.)"
    )
    lines.append("")

    lines.append("## Featured")
    lines.append("")
    if not featured:
        lines.append("_None this week._")
        lines.append("")
    for item in featured:
        r = item["repo"]
        lines.append(f"### {repo_line(r)}")
        lines.append(f"- org: `{r['org']}` · language: {r['language'] or '[none set]'} · {r['html_url']}")
        if item["created_this_week"]:
            lines.append(f"- **created** {r['created_at']}")
        for rel in item["releases_this_week"]:
            name_part = f' "{rel["name"]}"' if rel.get("name") else ""
            pre = " (prerelease)" if rel.get("prerelease") else ""
            lines.append(f"- **release** `{rel['tag']}`{name_part}{pre} published {rel['published_at']}")
        lines.append(f"- commits to default branch this week: {item['commit_count']}")
        if item["prs_this_week"]:
            lines.append("- merged PRs this week:")
            for pr in item["prs_this_week"]:
                lines.append(f'  - #{pr["number"]} "{pr["title"]}" (merged {pr["merged_at"]})')
        else:
            lines.append("- merged PRs this week: none")
        lines.append(
            "- [needs prose/context from Ada: what shipped / why it matters — "
            "the JSON has no changelog or release-notes content]"
        )
        lines.append("")

    lines.append("## Also shipped (second-tier)")
    lines.append("")
    if not second_tier:
        lines.append("_None this week._")
        lines.append("")
    for item in second_tier:
        r = item["repo"]
        lines.append(f"### {repo_line(r)}")
        lines.append(f"- org: `{r['org']}` · language: {r['language'] or '[none set]'} · {r['html_url']}")
        lines.append(f"- commits to default branch this week: {item['commit_count']}")
        if item["prs_this_week"]:
            lines.append("- merged PRs this week:")
            for pr in item["prs_this_week"]:
                lines.append(f'  - #{pr["number"]} "{pr["title"]}" (merged {pr["merged_at"]})')
        else:
            lines.append("- merged PRs this week: none (commits only)")
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recon_json", help="path to a recon JSON produced by gather.py")
    ap.add_argument("--out-dir", default="drafts", help="output directory (default: drafts)")
    args = ap.parse_args()

    data = json.load(open(args.recon_json))
    os.makedirs(args.out_dir, exist_ok=True)

    for week_idx, bucket in enumerate(data["week_buckets"]):
        featured, second_tier, start, end = build_week_section(data, week_idx, bucket)
        text = render_brief(week_idx, bucket, featured, second_tier, start, end)
        out_path = os.path.join(args.out_dir, f"week-{bucket['index']}-brief.md")
        with open(out_path, "w") as f:
            f.write(text)
        print(f"wrote {out_path} ({len(featured)} featured, {len(second_tier)} second-tier)")


if __name__ == "__main__":
    main()
