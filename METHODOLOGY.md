# Methodology: Agent Payment Protocols Adoption Tracker, Oct 2026

Measured: 2026-10-08 to 2026-10-09 (UTC). All commands below were actually run; see `tracker.csv` for the exact `source_url`/`method` per row, and `collect.py` for a re-runnable version of metrics 1-4.

## Canonical repo selection

For each protocol we ran a GitHub repository search first and picked the repo with the clearest claim to being the spec's official home (highest-starred repo under the protocol's own org, or explicit description naming the stewarding org):

- x402: `GET https://api.github.com/search/repositories?q=x402+in:name` → `x402-foundation/x402` (6,689 stars; org is the x402 Foundation, the spec's current steward after originating at Coinbase).
- AP2: `GET https://api.github.com/orgs/google-agentic-commerce/repos` → `google-agentic-commerce/AP2` (3,211 stars).
- ACP: `GET https://api.github.com/search/repositories?q=agentic-commerce-protocol` → `agentic-commerce-protocol/agentic-commerce-protocol` (1,568 stars; repo description explicitly says "maintained by OpenAI and Stripe").
- L402: `GET https://api.github.com/search/repositories?q=L402+in:name` surfaced two candidates: `lightninglabs/L402` (91 stars, originating org) and `l402-protocol/l402` (227 stars, independent/newer org). We measured `lightninglabs/L402` as canonical because Lightning Labs coined L402; `l402-protocol/l402`'s higher star count means L402's true combined GitHub footprint is larger than what we report. This is flagged in `tracker.csv` and FINDINGS.md.
- Visa "Trusted Agent Protocol" and Mastercard "Agent Pay": searched GitHub (`trusted agent protocol visa`, `mastercard agent pay`) and checked the official `visa` GitHub org (16 public repos). Found only third-party demo/hackathon repos, no spec or reference implementation published by Visa or Mastercard. **Excluded** per the task's own rule ("include a protocol only if it has a public spec or repo").

## Metric 1: GitHub repo stats

For each canonical repo:
- `GET /repos/{owner}/{repo}` for stars, forks, `open_issues_count` (note: this field includes open PRs, not issues alone).
- `GET /search/issues?q=repo:{owner}/{repo}+type:issue+state:closed` for closed issues (issues only, via `type:issue`).
- `GET /repos/{owner}/{repo}/contributors?per_page=100`, paginated until a page returns fewer than 100 items, items counted across all pages (`anon` not included, i.e. registered GitHub accounts only).
- `GET /repos/{owner}/{repo}/commits?since=<measured_at minus 90 days, ISO8601>&per_page=100`, paginated the same way.
- `GET /repos/{owner}/{repo}/tags?per_page=5` and `GET /repos/{owner}/{repo}/releases/latest` for the latest tag/release.

All GitHub calls used `Authorization: token $GITHUB_TOKEN` (never printed). Unauthenticated calls are rate-limited to 60/hour (10/min for search), which is why a token was required to complete this pass.

**Gotcha found and documented:** `GET /repos/{owner}/{repo}/tags` is *not* sorted by date; it returned `v1` (committed 2025-12-10) as the first item for x402 even though a much more recent tag, `pypi-x402@v2.25.0` (committed 2026-09-29), exists further down the list. We cross-checked by resolving each tag's commit SHA via `GET /repos/{owner}/{repo}/commits/{sha}` and reading `.commit.committer.date`. If re-running this metric, resolve every tag's commit date and sort, rather than trusting list order.

## Metric 2: GitHub code footprint (repo search)

`GET /search/repositories?q=<query>` per protocol. Queries used:
- x402: `x402 in:name,description,readme`
- AP2: `AP2 in:name,description,readme agent` (bare "AP2" returns 11,375 hits, most unrelated (e.g. telecom/hardware project codenames that happen to be "AP2"), so we added `agent` as a disambiguating term; this is a judgment call, not a perfect filter)
- ACP: `"agentic commerce protocol" in:name,description,readme` (bare "ACP" returns 46,405 hits and is unusable as a signal, far too generic an acronym)
- L402: `L402 in:name,description,readme`

**Limitation:** GitHub documents search result counts as approximate once results are large, and does not provide a way to retrieve more than 1,000 actual result rows even though `total_count` can be much larger. We only read `total_count`, not the underlying rows, except where noted (x402 and L402 sample spot-checks below).

## Metric 3: Package downloads

- npm: `GET https://api.npmjs.org/downloads/point/last-week/<pkg>` for each package confirmed as officially maintained inside the protocol's own monorepo (verified by reading the package's `package.json` location in the spec repo via the GitHub Contents API, e.g. `typescript/packages/x402/package.json` → name `x402`).
- PyPI: `GET https://pypistats.org/api/packages/<pkg>/recent`, reading `.data.last_month`.
- We treated a package as "official" only if its source lives inside the protocol's own canonical repo (checked via GitHub Contents API) or the protocol's own GitHub org. Where a plausible-sounding package existed but could not be tied to the canonical repo/org (e.g. PyPI's `ap2`, whose `project_urls` point to `github.com/whillhill/ap2`, an unrelated third-party repo, not `google-agentic-commerce/AP2`), we recorded `not_measurable` rather than reporting that package's numbers as if official.
- AP2 and ACP: no official npm or PyPI package could be confirmed at all (recorded as `not_applicable`/`not_measurable` with the specific check performed noted in `tracker.csv`).
- L402: a related repo `lightninglabs/L402sdk` exists, but we could not identify its published package name with confidence in the time available, so its downloads were not counted.

**Limitation:** npm/PyPI download counts include CI pipelines, mirrors, bots and reinstalls, not unique human developers.

## Metric 4: MCP Registry

`GET https://registry.modelcontextprotocol.io/v0/servers?search=<term>&limit=100`, paginating via `metadata.nextCursor` until it is null (capped at 20 pages as a safety limit; x402's search needed 7 pages / 657 raw rows). Deduplicated by `server.name` (note: the field lives at `servers[].server.name`, not top-level `servers[].name`: this is a nesting gotcha in the registry's response shape).

Search terms used: `x402`, `AP2`, `ACP`, `L402` (the literal protocol short names, as the task specified).

**"ACP" specifically is a generic acronym collision risk.** We manually read all 8 deduplicated raw matches for "ACP" and found only 2 were genuine Stripe/OpenAI Agentic Commerce Protocol integrations; the other 6 were unrelated tools (an AI social network abbreviated "ACP", an "Agentic Control Plane" cost-monitoring tool, an MCP-to-ACP coding-agent bridge, a username substring match, an unrelated banking-data server, and the unrelated PEAC protocol). We report both the raw count (8, `ACP,mcp_registry_distinct_servers_raw`) and the manually verified count (2, `ACP,mcp_registry_distinct_servers_verified`) in `tracker.csv`. We did not do the equivalent manual pass for "AP2" and "L402" beyond spot-checking (all matches for both looked genuine) because their raw counts were low enough to read in full, and did a 10-item random spot-check (not full manual read) for x402's 214 since that volume was too large to read exhaustively in the time available.

## Metric 5: Ecosystem/partner pages

Checked each protocol's own docs site for an ecosystem/partners/implementations page:
- x402: found via its README's "Ecosystem" section pointing to `docs.x402.org/dev-tools/facilitators`. The rendered page is a JS-heavy Mintlify site that doesn't expose its table in static HTML; we fetched the Mintlify plain-markdown mirror at `.../facilitators.md` (a documented Mintlify feature) and counted table rows by hand: 15 production facilitators listed.
- AP2: fetched `ap2-protocol.org/llms.txt` (a full docs-site index) and found no ecosystem/partners page in the nav. Recorded `not_found`.
- ACP: fetched `agenticcommerce.dev/llms.txt` and found no ecosystem/partners page; only a link to Stripe's own ACP integration docs and a ChatGPT-merchant application form. Recorded `not_found`.
- L402: no dedicated ecosystem page exists, but `lightninglabs/L402`'s own README has an "## Implementations" section listing 3 projects by name (Aperture, lsat-js, boltwall), counted by hand from the raw README.

**Limitation:** these are hand-counted, point-in-time reads of pages that may change; "not_found" means we did not find one after a reasonable search (repo README, llms.txt docs index, guessed common URL paths), not proof none exists anywhere.

## Metric 6: Spec version / last change date

Read directly from each repo: a version header in the spec file itself (x402: "Protocol Version: 2" in `specs/x402-specification-v2.md`), a `CHANGELOG.md` (AP2: "0.2.0 (2026-04-28)"), a dated changelog folder (ACP: `changelog/2026-04-17.md`, whose body text states "API Version: 2026-04-17"), or absence of any version marker (L402: no version field found in `protocol-specification.md`, recorded as `unversioned`). "Last changed" dates came from `GET /repos/{owner}/{repo}/commits?path=<spec file or dir>&per_page=1`, reading the first (most recent) commit's `commit.committer.date`.

## General limitations

- **Stars, forks, and repo-search hits measure visibility/naming, not production usage.** A protocol can have many stars from curiosity and few real integrations, or vice versa.
- **This is a point-in-time snapshot (2026-10-08/09).** All of these repos are under active development; re-run `collect.py` for a fresh pull.
- **No number in `tracker.csv` was invented.** Every row that could not be measured says `not_measurable` or `not_applicable` plus the specific check performed, rather than a guess.
- **Rate limits:** all GitHub REST calls used an authenticated token and none were rate-limited during this run. npm, PyPI (pypistats.org) and the MCP registry were called unauthenticated and also were not rate-limited during this run.
- We did not attempt metrics for L402 that require distinguishing `lightninglabs/L402` traffic from `l402-protocol/l402` traffic (e.g. npm downloads, MCP registry mentions), both repos use the string "L402" and our queries can't cleanly separate the two spec homes' adoption.

## Reproducing this report

```bash
export GITHUB_TOKEN=ghp_xxx   # a token with public_repo read scope is enough
python3 collect.py > tracker_rerun.csv
```

`collect.py` reproduces metrics 1-4 only (GitHub repo stats, GitHub code-footprint search, npm/PyPI downloads, MCP Registry counts). Metrics 5 (ecosystem pages) and 6 (spec version/date) require opening each protocol's own docs page and reading it, as described above, and are not automated.
