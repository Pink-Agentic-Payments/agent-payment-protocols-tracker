# Agent Payment Protocols Adoption Tracker (October 2026): x402 vs AP2 vs ACP vs L402

> **Disclosure**: Published by PinkWallet, which builds Pink Agentic AI Payments (an agent spending-control layer). Pink is not one of the protocols measured and does not integrate with any of them today.

A monthly snapshot of public adoption signals for x402, AP2 (Agent Payments Protocol) and ACP (Agentic Commerce Protocol), plus L402 as a longer-running comparison point. Measured 2026-10-08/09. Full method in [METHODOLOGY.md](./METHODOLOGY.md), full findings in [FINDINGS.md](./FINDINGS.md), raw data in [tracker.csv](./tracker.csv).

## Summary

Generated directly from `tracker.csv` by [make_table.py](./make_table.py), run `python3 make_table.py` to reproduce.

| Protocol | GitHub stars | Contributors | Commits (90d) | Official npm downloads/week [^npm] | Official PyPI downloads/month [^pypi] | MCP Registry servers [^mcp] | Facilitators/partners listed [^fac] |
|---|---|---|---|---|---|---|---|
| x402 | 6,689 | 333 | 281 | 485,082 | 204,765 | 214 | 15 |
| AP2 | 3,211 | 19 | 0 | n/a | n/a | 3 | n/a |
| ACP | 1,568 | 26 | 1 | n/a | n/a | 2 | n/a |
| L402 | 91 | 8 | 0 | n/a | n/a | 5 | 3 |

[^npm]: Sum of official npm packages. x402: `x402`, `x402-fetch`, `x402-axios`, `x402-express`, `x402-next` (all maintained in the x402 monorepo). AP2 and ACP have no official npm package we could confirm; L402's possible SDK package could not be identified with confidence. "n/a" means not measurable, not zero.
[^pypi]: x402's official PyPI package is `x402`. AP2's and ACP's spec repos reference no official PyPI package. A PyPI package named `ap2` exists but belongs to an unrelated third-party repo, not Google's, and is excluded.
[^mcp]: Distinct server names in the official MCP Registry naming each protocol. ACP's figure is the manually verified count (2 of 8 raw matches; the other 6 are unrelated tools that also abbreviate to "ACP"). See FINDINGS.md finding 4.
[^fac]: x402's figure is its official facilitators directory (docs.x402.org). L402's figure is its README's hand-maintained "Implementations" list. AP2 and ACP publish no equivalent ecosystem/partners page as of 2026-10-08.

## Findings

1. x402 has by far the largest GitHub footprint of the three commerce-focused protocols: 6,689 stars and 333 contributors, vs. 3,211 stars / 19 contributors for AP2 and 1,568 stars / 26 contributors for ACP.
2. x402's spec repo is far more active day-to-day: 281 commits in the last 90 days, vs. 1 for ACP and 0 for AP2 (AP2's and L402's default branches had no commits in the 90 days before measurement).
3. x402 has a real, measured package-download footprint; AP2 and ACP do not, as far as we could find. The official npm package `x402` gets 458,455 downloads/week and the official PyPI package `x402` gets 204,765 downloads/month. Neither AP2 nor ACP has a confirmable official npm or PyPI package.
4. x402 also dominates the MCP ecosystem: 214 distinct registered MCP servers name it, vs. 3 for AP2 and 2 (verified, after removing false positives) for ACP. The raw unverified count for "ACP" was 8, but 6 of those are unrelated tools that happen to also abbreviate to "ACP".
5. x402's GitHub code-footprint search also leads, with 28,297 repos matching `x402 in:name,description,readme`, vs. 2,587 for `AP2 ... agent` and 977 for `"agentic commerce protocol"`. These are GitHub's own approximate search counts, not exact; see caveats below.
6. AP2 has shipped one versioned release since launch (v0.2.0, 2026-04-28); ACP ships on a rolling, date-stamped API version (latest promoted: 2026-04-17) instead of GitHub releases; x402 tags per-package version bumps instead of using GitHub Releases.
7. x402 is the only one of the three with a maintained, named facilitator/implementer directory: its official docs list 15 production facilitators (Coinbase CDP, Fireblocks, Polygon, Celo, Corbits, etc.). Neither AP2 nor ACP publishes an equivalent ecosystem or partners page as of 2026-10-08.
8. L402 (the oldest of the four, dating to 2020) is now the smallest by every GitHub metric measured: 91 stars, 8 contributors, 0 commits in the last 90 days, no confirmable official npm/PyPI package, and only 5 MCP registry servers naming it.
9. Visa's "Trusted Agent Protocol" and Mastercard's "Agent Pay" have no public spec repo or document as of 2026-10-08 and are excluded from this tracker; GitHub searches for both surface only third-party demo/hackathon repos.
10. L402 itself has two competing "canonical" homes on GitHub: `lightninglabs/L402` (91 stars, the originating org) and the independent `l402-protocol/l402` (227 stars, describing itself as a newer continuation). This tracker measured only `lightninglabs/L402`; treat L402's numbers above as a lower bound on total L402-branded GitHub activity.

Full findings with exact source rows are in [FINDINGS.md](./FINDINGS.md).

## What none of these protocols decide

We checked each spec for a standing per-agent spending budget, a general spending-policy/rules engine, or a human-approval step as a protocol primitive. x402's own spec is explicit about this:

> "Out of Scope: This specification does not include: ... Client-side budget management"
> (specs/x402-specification-v2.md, [x402-foundation/x402](https://github.com/x402-foundation/x402/blob/main/specs/x402-specification-v2.md), fetched 2026-10-08)

AP2 comes closest with per-transaction "Mandates" and a human-present/human-absent distinction, but a Mandate authorizes one cart, not a standing allowance. ACP and L402 define checkout and per-request payment flows with no budget, policy or approval concept in the spec text. Full detail per protocol, with quotes and source links, is in [WHAT_NONE_DECIDE.md](./WHAT_NONE_DECIDE.md).

## Where Pink fits

The per-agent budget, payee-rule and human-approval layer that these specs leave out is what Pink Agentic AI Payments does for payments an agent makes through Pink's own MCP server. It does not plug into x402, AP2, ACP or L402 today.

Pink Agentic AI Payments is an MCP server that checks per-agent budgets, payee rules and human-approval holds before a payment executes; try it in the public sandbox with test money: https://agentic-sandbox.pinkwallet.com

## Method

Canonical repo per protocol chosen by GitHub search plus manual verification of the stewarding org. GitHub REST API (authenticated) for repo stats, code-footprint search, and release/tag data; npm/PyPI public APIs for download counts; the official MCP Registry API for server counts, deduplicated by server name. Full method, every query used, and known limitations are in [METHODOLOGY.md](./METHODOLOGY.md).

## Rerun it

```bash
export GITHUB_TOKEN=ghp_xxx   # a token with public_repo read scope is enough
python3 collect.py > tracker_rerun.csv
python3 make_table.py
```

`collect.py` reproduces metrics 1-4 (GitHub repo stats, GitHub code-footprint search, npm/PyPI downloads, MCP Registry counts). Metrics 5 (ecosystem pages) and 6 (spec version/date) require opening each protocol's own docs page and reading it by hand; see METHODOLOGY.md. `collect.py` itself is MIT-licensed; see the License section below.

## Caveats

- Stars, forks and repo-search counts measure attention and SEO-adjacent naming, not production usage.
- GitHub's repository/code search counts are documented by GitHub as approximate for large result sets.
- npm/PyPI download counts include CI, mirrors and bots, not just human developers.
- "AP2" and especially "ACP" are generic enough strings that raw search/registry matches needed manual de-noising; see METHODOLOGY.md for exactly how each was handled.

## How to cite

See [CITATION.cff](./CITATION.cff). Short form:

> PinkWallet (2026). *Agent Payment Protocols Adoption Tracker (October 2026)*. Version 2026.10. CC BY 4.0. https://github.com/Pink-Agentic-Payments/agent-payment-protocols-tracker

## Correct a number

If a value in `tracker.csv` is wrong or out of date, open an issue using the [Correct a number](./.github/ISSUE_TEMPLATE/correct-a-number.yml) template with a public evidence URL. Corrections with a public source are merged within 7 days and noted in [CHANGELOG.md](./CHANGELOG.md).

## License

Data and markdown files (`tracker.csv`, `FINDINGS.md`, `METHODOLOGY.md`, `WHAT_NONE_DECIDE.md`, this README) are [CC BY 4.0](./LICENSE). Attribution: PinkWallet, *Agent Payment Protocols Adoption Tracker (October 2026)*. `collect.py` and `make_table.py` are MIT-licensed: you may reuse the code under the more permissive MIT terms regardless of how you use the data.

---

Links: [Payment MCP Servers Census](https://github.com/Pink-Agentic-Payments/payment-mcp-census) · [Agentic Payments Readiness](https://github.com/Pink-Agentic-Payments/agentic-payments-readiness) · [Overspend Challenge](https://github.com/Pink-Agentic-Payments/overspend-challenge)
