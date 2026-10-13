#!/usr/bin/env python3
"""
Agent Payment Protocols Adoption Tracker - metric collector.

Re-collects metrics 1-4 from tracker.csv (GitHub repo stats, GitHub code
footprint search, npm/PyPI package downloads, MCP Registry server counts)
for x402, AP2, ACP and L402. Metrics 5 (ecosystem/partner pages) and 6
(spec version) are NOT automated here because they require reading and
hand-counting an official docs page per protocol (see METHODOLOGY.md) -
this script prints a reminder to update those by hand.

Usage:
    GITHUB_TOKEN=ghp_xxx python3 collect.py > tracker_rerun.csv

Stdlib only. GITHUB_TOKEN is optional but without it GitHub's unauthenticated
rate limit (60 req/hour, 10 req/min for search) will be hit quickly.
"""
import csv
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
TODAY = datetime.datetime.utcnow().strftime("%Y-%m-%d")

PROTOCOLS = {
    "x402": {
        "repo": "x402-foundation/x402",
        "repo_search_query": "x402 in:name,description,readme",
        "npm_packages": ["x402", "x402-fetch", "x402-axios", "x402-express", "x402-next"],
        "pypi_packages": ["x402"],
        "mcp_search_term": "x402",
    },
    "AP2": {
        "repo": "google-agentic-commerce/AP2",
        "repo_search_query": "AP2 in:name,description,readme agent",
        "npm_packages": [],
        "pypi_packages": [],  # the only PyPI pkg named "ap2" is unofficial (github.com/whillhill/ap2)
        "mcp_search_term": "AP2",
    },
    "ACP": {
        "repo": "agentic-commerce-protocol/agentic-commerce-protocol",
        "repo_search_query": '"agentic commerce protocol" in:name,description,readme',
        "npm_packages": [],  # @agentic-commerce-protocol/specification is not published to the npm registry
        "pypi_packages": [],
        "mcp_search_term": "ACP",
    },
    "L402": {
        "repo": "lightninglabs/L402",
        "repo_search_query": "L402 in:name,description,readme",
        "npm_packages": [],
        "pypi_packages": [],
        "mcp_search_term": "L402",
    },
}


def gh_get(url):
    req = urllib.request.Request(url)
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                headers = dict(r.getheaders())
                body = json.load(r)
                return body, headers
        except urllib.error.HTTPError as e:
            if e.code == 403 and attempt < 2:
                time.sleep(5)
                continue
            return {"error": str(e), "code": e.code}, {}
    return {"error": "rate_limited"}, {}


def count_paginated(url_tmpl, per_page=100, max_pages=10):
    total = 0
    page = 1
    while page <= max_pages:
        body, _ = gh_get(url_tmpl.format(per_page=per_page, page=page))
        if isinstance(body, dict) and body.get("error"):
            break
        n = len(body) if isinstance(body, list) else 0
        total += n
        if n < per_page:
            break
        page += 1
    return total


def repo_metrics(repo):
    out = {}
    data, _ = gh_get(f"https://api.github.com/repos/{repo}")
    if data.get("error"):
        out["error"] = data["error"]
        return out
    out["stars"] = data.get("stargazers_count")
    out["forks"] = data.get("forks_count")
    out["open_issues"] = data.get("open_issues_count")  # includes PRs
    out["created_at"] = data.get("created_at")
    out["pushed_at"] = data.get("pushed_at")

    closed, _ = gh_get(
        "https://api.github.com/search/issues?q=" + urllib.parse.quote(
            f"repo:{repo} type:issue state:closed"
        )
    )
    out["closed_issues"] = closed.get("total_count") if isinstance(closed, dict) else None

    out["contributors"] = count_paginated(
        f"https://api.github.com/repos/{repo}/contributors?per_page={{per_page}}&page={{page}}"
    )

    since = (datetime.datetime.utcnow() - datetime.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    out["commits_90d"] = count_paginated(
        f"https://api.github.com/repos/{repo}/commits?since={since}&per_page={{per_page}}&page={{page}}",
        max_pages=10,
    )

    tags, _ = gh_get(f"https://api.github.com/repos/{repo}/tags?per_page=5")
    out["latest_tag"] = tags[0]["name"] if isinstance(tags, list) and tags else None

    rel, _ = gh_get(f"https://api.github.com/repos/{repo}/releases/latest")
    out["latest_release_tag"] = rel.get("tag_name") if isinstance(rel, dict) else None
    out["latest_release_date"] = rel.get("published_at") if isinstance(rel, dict) else None

    return out


def repo_search_count(query):
    data, _ = gh_get(
        "https://api.github.com/search/repositories?q=" + urllib.parse.quote(query)
    )
    return data.get("total_count") if isinstance(data, dict) else None


def npm_weekly_downloads(pkg):
    try:
        with urllib.request.urlopen(
            f"https://api.npmjs.org/downloads/point/last-week/{urllib.parse.quote(pkg)}",
            timeout=20,
        ) as r:
            d = json.load(r)
            return d.get("downloads")
    except Exception as e:
        return None


def pypi_monthly_downloads(pkg):
    try:
        with urllib.request.urlopen(
            f"https://pypistats.org/api/packages/{urllib.parse.quote(pkg)}/recent", timeout=20
        ) as r:
            d = json.load(r)
            return d.get("data", {}).get("last_month")
    except Exception:
        return None


def mcp_registry_count(term):
    names = set()
    cursor = None
    pages = 0
    while pages < 20:
        url = (
            "https://registry.modelcontextprotocol.io/v0/servers?search="
            + urllib.parse.quote(term)
            + "&limit=100"
        )
        if cursor:
            url += "&cursor=" + urllib.parse.quote(cursor)
        d = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=20) as r:
                    d = json.load(r)
                break
            except Exception:
                if attempt < 2:
                    time.sleep(3)
        if d is None:
            break
        for s in d.get("servers", []):
            nm = s.get("server", {}).get("name")
            if nm:
                names.add(nm)
        new_cursor = d.get("metadata", {}).get("nextCursor")
        pages += 1
        if not new_cursor or new_cursor == cursor:
            break
        cursor = new_cursor
    return len(names)


def main():
    rows = []
    for proto, cfg in PROTOCOLS.items():
        rm = repo_metrics(cfg["repo"])
        base_url = f"https://api.github.com/repos/{cfg['repo']}"
        if "error" not in rm:
            rows.append((proto, "github_stars", rm["stars"], "count", base_url, "GET /repos/{owner}/{repo}"))
            rows.append((proto, "github_forks", rm["forks"], "count", base_url, "GET /repos/{owner}/{repo}"))
            rows.append((proto, "github_open_issues_prs", rm["open_issues"], "count", base_url, "GET /repos/{owner}/{repo} .open_issues_count (includes PRs)"))
            rows.append((proto, "github_closed_issues", rm["closed_issues"], "count", base_url, "GET /search/issues?q=repo:{repo}+type:issue+state:closed"))
            rows.append((proto, "github_contributors", rm["contributors"], "count", base_url, "GET /repos/{owner}/{repo}/contributors (paginated, per_page=100)"))
            rows.append((proto, "github_commits_90d", rm["commits_90d"], "count", base_url, "GET /repos/{owner}/{repo}/commits?since=<90d ago> (paginated)"))
            rows.append((proto, "github_latest_tag", rm.get("latest_tag"), "tag", base_url, "GET /repos/{owner}/{repo}/tags (first of list, most recent)"))
            rows.append((proto, "github_latest_release", rm.get("latest_release_tag"), "tag", base_url, "GET /repos/{owner}/{repo}/releases/latest"))
        else:
            rows.append((proto, "github_repo_error", rm["error"], "error", base_url, "GET /repos/{owner}/{repo}"))

        search_count = repo_search_count(cfg["repo_search_query"])
        rows.append((
            proto, "github_repo_search_count", search_count, "count (approximate)",
            "https://api.github.com/search/repositories?q=" + urllib.parse.quote(cfg["repo_search_query"]),
            f"GET /search/repositories?q={cfg['repo_search_query']}",
        ))

        for pkg in cfg["npm_packages"]:
            dl = npm_weekly_downloads(pkg)
            rows.append((
                proto, f"npm_weekly_downloads:{pkg}", dl, "downloads/week",
                f"https://api.npmjs.org/downloads/point/last-week/{pkg}",
                "GET api.npmjs.org/downloads/point/last-week/<pkg>",
            ))
        for pkg in cfg["pypi_packages"]:
            dl = pypi_monthly_downloads(pkg)
            rows.append((
                proto, f"pypi_monthly_downloads:{pkg}", dl, "downloads/month",
                f"https://pypistats.org/api/packages/{pkg}/recent",
                "GET pypistats.org/api/packages/<pkg>/recent .data.last_month",
            ))

        mcp_count = mcp_registry_count(cfg["mcp_search_term"])
        rows.append((
            proto, "mcp_registry_distinct_servers", mcp_count, "count",
            "https://registry.modelcontextprotocol.io/v0/servers?search=" + urllib.parse.quote(cfg["mcp_search_term"]),
            f"GET registry.modelcontextprotocol.io/v0/servers?search={cfg['mcp_search_term']}&limit=100, paginate via metadata.nextCursor, dedupe by server.name",
        ))

    writer = csv.writer(sys.stdout)
    writer.writerow(["protocol", "metric", "value", "unit", "measured_at", "source_url", "method"])
    for proto, metric, value, unit, url, method in rows:
        writer.writerow([proto, metric, value, unit, TODAY, url, method])

    print(
        "# NOTE: metrics 5 (ecosystem/partner page counts) and 6 (spec version/date) "
        "are not automated - they require opening the protocol's own docs page and "
        "counting by hand. See METHODOLOGY.md.",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
