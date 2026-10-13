# Changelog

## 2026.10.2 - 2026-10-13

- Refreshed all metrics 1-4 for x402, AP2, ACP and L402 via `collect.py`; re-verified metrics 5-6 (ecosystem pages, spec version/date) by hand. New snapshot saved as `data/2026-10-13.csv`; prior snapshot preserved as `data/2026-10-09.csv`.
- Fixed a bug in `collect.py`'s `mcp_registry_count()`: a transient fetch failure against the MCP Registry API silently broke the pagination loop and returned a partial or zero count instead of retrying. Added a 3x retry with backoff, matching the existing GitHub retry pattern.
- ACP's MCP Registry raw match count rose from 8 to 10 and its manually verified count from 2 to 3 (a new entry, `com.flo-voice1/acp-sandbox`, explicitly describes an Agentic Commerce Protocol checkout flow, settled via PayPal rather than Stripe).
- x402's npm weekly downloads (sum of 5 official packages) rose from 485,082 to 494,987; its core `x402` package alone rose from 458,455 to 467,272.

## 2026.10 - 2026-10-09

- Initial publication of the Agent Payment Protocols Adoption Tracker: 68 metric rows in `tracker.csv` covering x402, AP2, ACP and L402 (plus 2 excluded-protocol rows for Visa and Mastercard), with `FINDINGS.md`, `METHODOLOGY.md`, and `WHAT_NONE_DECIDE.md`.
- Added `collect.py` (metrics 1-4, re-runnable) and `make_table.py` (regenerates the README summary table from `tracker.csv`).
