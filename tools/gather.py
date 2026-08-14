#!/usr/bin/env python3
"""
gather.py — regenerate the "Shipped" recon data.

Pulls public-repo activity across:
  - prime-radiant-inc (a real GitHub *organization*)
  - obra              (a GitHub *user* account, NOT an org — GET /orgs/obra
                        404s; this script queries /users/obra/repos instead.
                        Verify this hasn't changed if obra activity looks
                        emptier than expected.)

for the last N calendar weeks (Mon-Sun buckets, ending "now"; the final
bucket is a partial week if today isn't a Sunday) and writes a structured
JSON file to data/recon-<weeks>wk-<YYYYMMDD>.json.

CLASSIFICATION (inputs only — this script computes a `tier` field but the
blog is free to re-derive it from the raw counts):
  FEATURED     = created in-window (non-fork) OR had >=1 release in-window
  SECOND-TIER  = had commits to the default branch and/or merged PRs
                 in-window, but doesn't qualify as FEATURED
  SKIP         = no activity in-window

Forks are EXCLUDED from the "created in window" trigger for FEATURED: a
fork's `created_at` is when *that account* forked it, not when the upstream
project was created, so a freshly-forked old project would otherwise look
like a "new project" incorrectly. A fork can still be FEATURED via a
release it published itself, and can still be SECOND-TIER via commits/PRs.

CREDENTIALS
-----------
This script does NOT talk to Ada's credential broker itself — it can't; the
broker is a tool available to the *agent* driving this box (via
`request_credential` in that agent's toolset), not a public API this script
can call. Whoever runs this script is responsible for obtaining a GitHub
token through that flow first and exporting it as GH_TOKEN or GITHUB_TOKEN
before invoking gather.py. If neither is set, this script fails closed with
a clear error rather than silently trying anonymous/unauthenticated calls
(which would hit GitHub's much lower unauthenticated rate limit and likely
fail partway through a 200+ repo org/user).

USAGE
-----
    GH_TOKEN=<token> python3 tools/gather.py --weeks 8
    GH_TOKEN=<token> python3 tools/gather.py --weeks 4 --orgs prime-radiant-inc
    GH_TOKEN=<token> python3 tools/gather.py --weeks 8 --out data/custom.json

Requires the `gh` CLI on PATH (used as the HTTP client for convenience —
it already knows how to paginate and how to read GH_TOKEN).
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

# Org/user accounts to scan. `kind` controls which REST endpoint enumerates
# public repos: organizations use /orgs/{org}/repos, plain user accounts use
# /users/{user}/repos. (`obra` is a user account; see module docstring.)
ACCOUNTS = [
    {"login": "prime-radiant-inc", "kind": "org"},
    {"login": "obra", "kind": "user"},
]


def get_token():
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not tok:
        sys.exit(
            "ERROR: no GitHub token found in GH_TOKEN or GITHUB_TOKEN.\n"
            "Obtain one via Ada's credential broker (request_credential, "
            "host api.github.com, use=http) and export it before running "
            "this script. Refusing to proceed with unauthenticated calls."
        )
    return tok


def week_buckets(n_weeks, now=None):
    """Return n_weeks (start, end_exclusive) datetime tuples, Mon-Sun, the
    last one ending at `now` (today's Monday..today, i.e. partial)."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    monday_this_week = (now - datetime.timedelta(days=now.weekday())).replace(
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
    """Call `gh api <path>`, returning (data, error). data is always a list
    for the endpoints this script uses (repos/commits/pulls/releases)."""
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
        # `gh --paginate` can concatenate multiple JSON arrays/objects for
        # some endpoints; stream-decode instead of assuming one JSON blob.
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


def list_public_repos(login, kind, token):
    endpoint = f"orgs/{login}/repos" if kind == "org" else f"users/{login}/repos"
    data, err = gh_api(f"{endpoint}?type=public&per_page=100", token)
    if err:
        sys.exit(f"ERROR: could not list public repos for {login} ({kind}): {err}")
    return data


def get_releases(owner, name, token, window_start, now):
    data, err = gh_api(f"repos/{owner}/{name}/releases?per_page=100", token)
    if err:
        return [], err
    out = []
    for rel in data:
        pub = rel.get("published_at")
        if not pub:
            continue
        dt = datetime.datetime.fromisoformat(pub.replace("Z", "+00:00"))
        if window_start <= dt <= now:
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


def get_commits(owner, name, default_branch, token, window_start, now, buckets):
    since = window_start.strftime("%Y-%m-%dT%H:%M:%SZ")
    until = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    path = f"repos/{owner}/{name}/commits?sha={default_branch}&since={since}&until={until}&per_page=100"
    data, err = gh_api(path, token)
    if err:
        return None, err
    weekly = [0] * len(buckets)
    total = 0
    for c in data:
        commit = c.get("commit", {})
        cd = (commit.get("committer") or {}).get("date") or (commit.get("author") or {}).get("date")
        if not cd:
            continue
        dt = datetime.datetime.fromisoformat(cd.replace("Z", "+00:00"))
        if dt < window_start or dt > now:
            continue
        bi = bucket_index(dt, buckets)
        if bi is not None:
            weekly[bi] += 1
            total += 1
    return {"total": total, "weekly": weekly}, None


def get_merged_prs(owner, name, token, window_start, now, buckets):
    """Closed PRs sorted by `updated` desc; stop paging once updated_at
    drops below window_start (merged_at <= updated_at always holds, so once
    updated_at is out of range no further page can contain an in-window
    merge)."""
    page = 1
    out = []
    while True:
        path = (
            f"repos/{owner}/{name}/pulls?state=closed&sort=updated"
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
                mdt = datetime.datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
                if window_start <= mdt <= now:
                    out.append({"number": pr["number"], "title": pr["title"], "merged_at": merged_at})
            upd = pr.get("updated_at")
            if upd:
                udt = datetime.datetime.fromisoformat(upd.replace("Z", "+00:00"))
                if udt < window_start:
                    stop = True
        if stop or len(data) < 100 or page > 10:
            break
        page += 1
    weekly = [0] * len(buckets)
    for pr in out:
        dt = datetime.datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
        bi = bucket_index(dt, buckets)
        if bi is not None:
            weekly[bi] += 1
    return {"total": len(out), "list": out, "weekly": weekly}, None


def process_account(login, kind, token, window_start, now, buckets, only_candidates_get_detail=True):
    repos = list_public_repos(login, kind, token)
    results = []
    for r in repos:
        name = r["name"]
        created_dt = datetime.datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
        created_in_window = window_start <= created_dt <= now
        is_fork = r["fork"]
        # A fork's created_at is fork date, not upstream birth date — never
        # let a fork trigger FEATURED via "created in window".
        created_in_window_for_featured = created_in_window and not is_fork

        pushed_at = r.get("pushed_at")
        pushed_dt = datetime.datetime.fromisoformat(pushed_at.replace("Z", "+00:00")) if pushed_at else None
        pushed_in_window = bool(pushed_dt and window_start <= pushed_dt <= now)

        candidate_for_detail = created_in_window or pushed_in_window

        entry = {
            "org": login,
            "name": name,
            "full_name": r["full_name"],
            "description": r.get("description"),
            "language": r.get("language"),
            "html_url": r["html_url"],
            "created_at": r["created_at"],
            "created_in_window": created_in_window,
            "created_in_window_for_featured": created_in_window_for_featured,
            "pushed_at": pushed_at,
            "fork": is_fork,
            "archived": r["archived"],
            "default_branch": r.get("default_branch"),
            "candidate_for_detail": candidate_for_detail,
        }

        errors = {}

        rels, err = get_releases(login, name, token, window_start, now)
        if err:
            errors["releases"] = err
            rels = []
        entry["releases_in_window"] = rels

        if candidate_for_detail or not only_candidates_get_detail:
            commits, cerr = get_commits(
                login, name, r.get("default_branch") or "main", token, window_start, now, buckets
            )
            if cerr:
                errors["commits"] = cerr
                commits = {"total": 0, "weekly": [0] * len(buckets)}
            prs, perr = get_merged_prs(login, name, token, window_start, now, buckets)
            if perr:
                errors["merged_prs"] = perr
                prs = {"total": 0, "list": [], "weekly": [0] * len(buckets)}
        else:
            note = "skipped detail fetch: pushed_at and created_at both outside window"
            commits = {"total": 0, "weekly": [0] * len(buckets), "note": note}
            prs = {"total": 0, "list": [], "weekly": [0] * len(buckets), "note": note}

        entry["commits_in_window"] = commits
        entry["merged_prs_in_window"] = prs

        has_release = len(rels) > 0
        has_activity = commits.get("total", 0) > 0 or prs.get("total", 0) > 0
        if created_in_window_for_featured or has_release:
            tier = "FEATURED"
        elif has_activity:
            tier = "SECOND-TIER"
        else:
            tier = "SKIP"
        entry["tier"] = tier
        if errors:
            entry["_errors"] = errors

        results.append(entry)
        print(f"[{login}] {name}: tier={tier} detail={candidate_for_detail}", file=sys.stderr)
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weeks", type=int, default=8, help="number of week buckets (default 8)")
    ap.add_argument(
        "--orgs",
        type=str,
        default=None,
        help="comma-separated subset of account logins to scan (default: all of "
        + ", ".join(a["login"] for a in ACCOUNTS)
        + ")",
    )
    ap.add_argument("--out", type=str, default=None, help="output path (default: data/recon-<weeks>wk-<date>.json)")
    ap.add_argument(
        "--all-detail",
        action="store_true",
        help="fetch commit/PR detail for every repo, not just ones created or pushed in-window "
        "(much slower; mainly useful for auditing the candidate-filter heuristic)",
    )
    args = ap.parse_args()

    token = get_token()
    now = datetime.datetime.now(datetime.timezone.utc)
    buckets = week_buckets(args.weeks, now)
    window_start = buckets[0][0]

    accounts = ACCOUNTS
    if args.orgs:
        wanted = set(x.strip() for x in args.orgs.split(","))
        accounts = [a for a in ACCOUNTS if a["login"] in wanted]
        missing = wanted - {a["login"] for a in accounts}
        if missing:
            sys.exit(f"ERROR: unknown account(s) requested: {', '.join(missing)}")

    all_results = []
    for acct in accounts:
        all_results.extend(
            process_account(
                acct["login"],
                acct["kind"],
                token,
                window_start,
                now,
                buckets,
                only_candidates_get_detail=not args.all_detail,
            )
        )

    out_path = args.out or f"data/recon-{args.weeks}wk-{now.strftime('%Y%m%d')}.json"
    out = {
        "generated_at_utc": now.isoformat(),
        "window_start_utc": window_start.isoformat(),
        "window_end_utc": now.isoformat(),
        "weeks_requested": args.weeks,
        "week_buckets": [
            {
                "index": i + 1,
                "start": s.date().isoformat(),
                "end": (e - datetime.timedelta(days=1)).date().isoformat(),
            }
            for i, (s, e) in enumerate(buckets)
        ],
        "accounts_queried": {a["login"]: a["kind"] for a in accounts},
        "repos": all_results,
    }
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {out_path} ({len(all_results)} repos)", file=sys.stderr)


if __name__ == "__main__":
    main()
