# Threat model and non-goals

## Assets and trust boundaries

The protected asset is the consumer's ability to execute an operation after a
temporary restriction's originally committed deadline. The rule owner controls
only the initial rule and early voluntary revocation. A permissionless caller
may fund a renewal assessment. A GenLayer leader proposes a classification;
validators independently re-fetch and classify. The external source publisher
is **not** under contract control.

| Attack | Contract defence | Residual risk |
|---|---|---|
| Emergency power persists by administrator inaction | Time-dependent `is_restricted` | Consumers must call the gate at execution time |
| Owner edits continuation criterion or source | No mutation API; immutable fingerprint | Owner can register a separate rule, which consumer must explicitly adopt |
| Incrementally stretches expiry | Exactly original epoch; immutable absolute cap | Time is the GenVM transaction timestamp |
| Replays assessment from older epoch | Expected epoch + expiry and after-consensus recheck | Upstream reorg/finality still needs verification |
| Repeatedly prompts until favourable outcome | One assessment slot per epoch, even inconclusive | One bad assessment can use up a slot; fails toward expiry |
| Malicious leader says PERSISTS | Validators independently fetch and classify; digest + witness | Majority-validator collusion is outside single-contract guarantees |
| Website injects instructions into prompt | Explicit untrusted-data boundary and escaped tags | Language-model prompt isolation is probabilistic, not formal |
| Evidence is unavailable or contradictory | INCONCLUSIVE or consensus failure; never renew | A real emergency might expire while still ongoing |
| Private/intranet URL used as evidence | Public HTTPS and hostname screening | URL screening is not a DNS-level SSRF guarantee |
| User points gate to different registry | Immutable address, ID, fingerprint | Consumer still trusts target GenLayer registry runtime |
| Owner bypasses gate | No gate admin or source-switch method | Real integration may add another route unless audited |
| Stored LIVE label outlives deadline | Dynamic time-based read ignores stale label | Historical labels require `get_rule` to interpret dynamic status |

## Scope limitations

No oracle can guarantee truthful news. Sunset establishes a *consensus-backed
bounded evidence procedure*, not an external legal/operational truth certificate.
Use dedicated signed sources for consequential real-world decisions.

The `SunsetGate` example increments a counter; it does **not** send GEN, manage
treasury custody, or enforce rules on third-party contracts. Production consumers
must authorize the rule registration, verify the fingerprint, and avoid alternate
operations that skip the check.
