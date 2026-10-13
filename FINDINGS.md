# Agent Payment Protocols Adoption Tracker: Findings (refreshed 2026-10-13; originally 2026-10-08/09)

Snapshot of public adoption signals for x402, AP2 and ACP (plus L402 as a longer-running comparison point). Every number below is a row in `tracker.csv`; follow the `source_url`/`method` columns there to reproduce it. All figures were measurable on 2026-10-13 (original pass: 2026-10-08/09, preserved in `data/2026-10-09.csv`).

## Findings

1. **x402 has by far the largest GitHub footprint of the three commerce-focused protocols.** x402-foundation/x402 has 6,715 stars and 334 contributors, vs. 3,226 stars / 19 contributors for AP2 (google-agentic-commerce/AP2) and 1,571 stars / 26 contributors for ACP (agentic-commerce-protocol/agentic-commerce-protocol). (`tracker.csv` rows: `x402,github_stars`; `x402,github_contributors`; `AP2,github_stars`; `AP2,github_contributors`; `ACP,github_stars`; `ACP,github_contributors`)

2. **x402's spec repo is far more active day-to-day: 278 commits in the last 90 days, vs. 1 for ACP and 0 for AP2.** AP2's and L402's default branches had no commits in the 90 days before measurement (last push 2026-06-17 and 2026-06-09 respectively); ACP had exactly one. (`tracker.csv` rows: `*,github_commits_last_90d`)

3. **x402 has a real, measured package-download footprint; AP2 and ACP do not, as far as we could find.** The sum of its five official npm packages (`x402`, `x402-fetch`, `x402-axios`, `x402-express`, `x402-next`) is 494,987 downloads/week (the core `x402` package alone is 467,272), and the official PyPI package `x402` gets 204,765 downloads/month. AP2 and ACP have no official npm or PyPI packages we could confirm: the only PyPI package named `ap2` belongs to an unrelated third-party repo (github.com/whillhill/ap2, not Google's), and ACP's own package name (`@agentic-commerce-protocol/specification`) returns 404 on the npm registry. (`tracker.csv` rows: `x402,npm_weekly_downloads:x402`; `x402,pypi_monthly_downloads:x402`; `AP2,pypi_monthly_downloads`; `ACP,npm_weekly_downloads`)

4. **x402 also dominates the MCP ecosystem: 222 distinct registered MCP servers name it, vs. 3 for AP2 and 3 (after removing false positives) for ACP.** The raw, unverified count for "ACP" was 10, but 7 of those 10 are unrelated tools that happen to also abbreviate to "ACP" (an AI social network, an "Agentic Control Plane" cost/policy tool, an MCP-to-ACP coding-agent bridge, etc.); 3 are genuine Agentic Commerce Protocol integrations (2 explicitly Stripe/OpenAI-branded, 1 a PayPal-settled ACP checkout sandbox). (`tracker.csv` rows: `x402,mcp_registry_distinct_servers`; `AP2,mcp_registry_distinct_servers`; `ACP,mcp_registry_distinct_servers_raw`; `ACP,mcp_registry_distinct_servers_verified`)

5. **x402's GitHub code-footprint search also leads**, with 29,195 repos matching `x402 in:name,description,readme`, vs. 2,640 for `AP2 ... agent` and 989 for `"agentic commerce protocol"`. These are GitHub's own approximate search counts, not exact; see caveats below and in METHODOLOGY.md. (`tracker.csv` rows: `*,github_repo_search_count`)

6. **AP2 has shipped one versioned release since launch; ACP ships on a rolling, date-stamped API version instead of GitHub releases.** AP2's only GitHub Release is v0.2.0 (2026-04-28, "Release of V2"). ACP has no GitHub tags or releases at all: its spec versions are date strings in a `changelog/` folder, the latest promoted one being `2026-04-17`, with unreleased changes already in the `spec/` directory as of 2026-07-18. x402 doesn't use GitHub Releases either; it tags per-package version bumps instead. (`tracker.csv` rows: `AP2,github_latest_release`; `ACP,spec_version`; `ACP,spec_last_changed`; `x402,github_latest_tag_by_list_order`)

7. **x402 is the only one of the three with a maintained, named facilitator/implementer directory:** its official docs list 15 production facilitators (Coinbase CDP, Fireblocks, Polygon, Celo, Corbits, etc.) at docs.x402.org/dev-tools/facilitators. Neither AP2 (ap2-protocol.org) nor ACP (agenticcommerce.dev) publishes an equivalent ecosystem or partners page as of 2026-10-13. (`tracker.csv` rows: `x402,ecosystem_facilitators_listed`; `AP2,ecosystem_partners_listed`; `ACP,ecosystem_partners_listed`)

8. **L402 (the oldest of the four, dating to 2020) is now the smallest by every GitHub metric measured**: 91 stars, 8 contributors, 0 commits in the last 90 days, no npm/PyPI package we could confirm as official, and only 5 MCP registry servers naming it. Its own README lists just 3 "Implementations" (Aperture, lsat-js, boltwall) under a hand-maintained list, not a submission-based directory. (`tracker.csv` rows: `L402,github_stars`; `L402,github_contributors`; `L402,github_commits_last_90d`; `L402,mcp_registry_distinct_servers`; `L402,ecosystem_implementations_listed`)

9. **Visa's "Trusted Agent Protocol" and Mastercard's "Agent Pay" have no public spec repo or document as of 2026-10-13 and are excluded from this tracker.** GitHub searches for both surface only third-party demo/hackathon repos (e.g. `thomaspurves/visa-tap-demo`, `plannerpenta-lang/mastercard-agent-chat`); the Visa GitHub org (16 public repos) has nothing matching. (`tracker.csv` rows: `excluded,Visa_Trusted_Agent_Protocol`; `excluded,Mastercard_Agent_Pay`)

10. **L402 itself has two competing "canonical" homes on GitHub**, which complicates any single adoption number for it: `lightninglabs/L402` (91 stars, the originating org, most recently pushed 2026-06-09) and the independent `l402-protocol/l402` (227 stars, pushed 2025-06-20, describing itself as a newer continuation). This tracker measured only `lightninglabs/L402`; treat L402's numbers above as a lower bound on total L402-branded GitHub activity. (`tracker.csv` row: `L402,canonical_repo`)

## Caveats baked into these findings (see METHODOLOGY.md for full detail)

- Stars, forks and repo-search counts measure attention and SEO-adjacent naming, not production usage.
- GitHub's repository/code search counts are documented by GitHub as approximate for large result sets.
- npm/PyPI download counts include CI, mirrors and bots, not just human developers.
- "AP2" and especially "ACP" are generic enough strings that raw search/registry matches need manual de-noising (done for the MCP registry metric; GitHub repo-search counts for AP2/ACP still carry residual noise despite added qualifier terms).
