#!/usr/bin/env python3
"""Regenerate the README summary table from tracker.csv. Run: python3 make_table.py"""
import csv

rows = list(csv.DictReader(open("tracker.csv")))
by_key = {(r["protocol"], r["metric"]): r["value"] for r in rows}

PROTOCOLS = ["x402", "AP2", "ACP", "L402"]

NPM_PACKAGES = {
    "x402": ["x402", "x402-fetch", "x402-axios", "x402-express", "x402-next"],
    "AP2": [],
    "ACP": [],
    "L402": [],
}

PYPI_PACKAGES = {
    "x402": ["x402"],
    "AP2": [],
    "ACP": [],
    "L402": [],
}


def fmt_na(value):
    if value in ("not_applicable", "not_found", "not_measurable", None, ""):
        return "n/a"
    return value


def npm_total(proto):
    pkgs = NPM_PACKAGES[proto]
    if not pkgs:
        return fmt_na(by_key.get((proto, "npm_weekly_downloads"), "not_applicable"))
    total = 0
    for pkg in pkgs:
        v = by_key.get((proto, f"npm_weekly_downloads:{pkg}"))
        if v is None:
            return "n/a"
        total += int(v)
    return f"{total:,}"


def pypi_total(proto):
    pkgs = PYPI_PACKAGES[proto]
    if not pkgs:
        return fmt_na(by_key.get((proto, "pypi_monthly_downloads"), "not_applicable"))
    total = 0
    for pkg in pkgs:
        v = by_key.get((proto, f"pypi_monthly_downloads:{pkg}"))
        if v is None:
            return "n/a"
        total += int(v)
    return f"{total:,}"


def mcp_servers(proto):
    if proto == "ACP":
        return fmt_na(by_key.get((proto, "mcp_registry_distinct_servers_verified")))
    return fmt_na(by_key.get((proto, "mcp_registry_distinct_servers")))


def facilitators(proto):
    key = "ecosystem_facilitators_listed" if proto == "x402" else (
        "ecosystem_implementations_listed" if proto == "L402" else "ecosystem_partners_listed"
    )
    return fmt_na(by_key.get((proto, key)))


def comma(v):
    try:
        return f"{int(v):,}"
    except (TypeError, ValueError):
        return fmt_na(v)


lines = []
lines.append("| Protocol | GitHub stars | Contributors | Commits (90d) | Official npm downloads/week [^npm] | Official PyPI downloads/month [^pypi] | MCP Registry servers [^mcp] | Facilitators/partners listed [^fac] |")
lines.append("|---|---|---|---|---|---|---|---|")
for proto in PROTOCOLS:
    stars = comma(by_key.get((proto, "github_stars")))
    contributors = comma(by_key.get((proto, "github_contributors")))
    commits = comma(by_key.get((proto, "github_commits_last_90d")))
    npm = npm_total(proto)
    pypi = pypi_total(proto)
    mcp = mcp_servers(proto)
    fac = facilitators(proto)
    lines.append(f"| {proto} | {stars} | {contributors} | {commits} | {npm} | {pypi} | {mcp} | {fac} |")

print("\n".join(lines))
