# What none of these protocols decide (checked against each spec, 2026-10-08)

Question asked of each spec: does it define (a) a standing per-agent spending budget, (b) a general spending policy/rules engine, or (c) a human-approval step as a protocol primitive, as opposed to a one-off, per-transaction authorization?

## x402

**Not in spec, explicitly out of scope.** The spec's own "Document Scope" section lists what it excludes:

> "Out of Scope: This specification does not include: ... Client-side budget management ... Session handling mechanisms"
> (Source: specs/x402-specification-v2.md, x402-foundation/x402, fetched 2026-10-08)

x402 defines a per-request payment authorization/settlement handshake (`PaymentRequirements` / `PaymentPayload` / `/verify` / `/settle`) between a client, a resource server and a facilitator. It has no concept of a standing budget across multiple payments, no spending-policy object, and no human-in-the-loop approval step: those are explicitly pushed to whatever wraps the client.

## AP2 (Agent Payments Protocol)

**Partially addressed, but scoped to a single transaction's consent, not a standing budget.** AP2 defines "Mandates": cryptographically signed objects that capture a user's authorization for one checkout:

> "The 'Checkout Mandate' signed by the user now contains the list of conditions under which the SA can fulfill the user's order. This mandate is in an 'Open' state while the Agent tries to meet the user's requirements. Once the SA determines that the requirements can be met, the mandate is 'Closed'."
> (Source: docs/overview.md, section 4.2 Human Not Present Transaction, google-agentic-commerce/AP2, fetched 2026-10-08)

AP2 does include a human-approval primitive for the "Human Present" flow (in-session biometric/auth confirmation) and a per-transaction price ceiling example ("don't spend more than $1000" on one purchase). What it does not define is a standing, protocol-level object representing an agent's ongoing budget across many transactions, categories of allowed/disallowed payees, or an org-wide spending policy engine (a Mandate authorizes one task/cart, not a continuing allowance).

## ACP (Agentic Commerce Protocol)

**Not in spec.** ACP's README and spec define REST endpoints for creating, updating and completing a `checkout_session` (cart state, line items, payment token handoff) between an agent, a business and a payment processor. We found no mention of budgets, spending limits, or human-approval steps as protocol primitives anywhere in the README, the dated spec folders, or a targeted GitHub code search for "budget" (7 hits, all either RFC examples of a *user's own* abandoned-cart reasoning, e.g. `"trace_summary": "$10 shipping fee pushes total cost beyond user's budget"`, or unrelated example data, not a protocol field for agent spending control) and "spending_limit" (0 hits).

> "Developed by Stripe and OpenAI to define a common language for open, secure AI commerce. ACP coordinates checkout experiences and securely shares payment credentials between agents and businesses."
> (Source: agenticcommerce.dev/llms.txt, fetched 2026-10-08)

ACP is a checkout/commerce-flow protocol; it assumes the payment credential handed to it is already something the merchant's PSP (e.g. Stripe) is willing to charge, and has nothing to say about who decided that, or under what per-agent limit.

## L402

**Not in spec.** L402's protocol-specification.md defines an HTTP 402 challenge/response flow using Lightning invoices and macaroons for per-request API payment authentication. No budget, policy or approval concept appears in the spec text (checked via keyword search for "budget", "spending limit", "approval", "policy": zero matches).

## Where a governance layer fits

Across all four specs, the common pattern holds: each protocol defines how a single payment gets authorized and moved, not how an organization decides in advance what an agent is allowed to spend, on what, or whether a human needs to sign off before it happens. AP2 comes closest with per-transaction Mandates and an explicit human-present/human-absent distinction, but even AP2's Mandate is scoped to one cart, not a standing allowance.

This is a factual gap in all four specs as written on 2026-10-08, not a claim about what any particular product does. Pink Agentic AI Payments does not integrate with x402, AP2, ACP or L402 today, as far as we know; this section is included because it is the gap a per-agent budget/rules/approval layer would need to fill if someone built one on top of any of these protocols.
