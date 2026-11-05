# Threat model

## Assets and boundaries

The protected asset is the consumer's ability to observe a temporary restriction
at execution time. Sunset protects immutable rule terms, current expiry, hard
stop, assessment-head ordering and receipt history. It does not control the
external website or make a legal or real-world truth determination.

| Boundary | Contract authority | Explicit non-authority |
|---|---|---|
| Rule registration | owner identity, unique ID, immutable terms | changing an existing rule or extending directly |
| Assessment | owner-only request, expected epoch/expiry | third-party settlement or arbitrary retry manipulation |
| Evidence | leader and validator retrieve the frozen source independently | source publisher identity, DNS ownership, page permanence |
| Semantic result | bounded model classifications and audits | arbitrary model-selected expiry or beneficiary |
| Consumer gate | typed registry/rule/fingerprint/executor/payload binding | funds, custody, alternate application routes |

## Attack analysis

| Attack | Mitigation | Residual risk |
|---|---|---|
| Unauthorized rule mutation | no update method; duplicate IDs rejected | owner can register a separate rule, which consumers must not adopt accidentally |
| Owner impersonation | `gl.message.sender_address` is stored and checked for revoke/assessment | key compromise is outside contract control |
| Stale assessment replay | expected epoch/expiry and post-consensus head recheck | upstream finality/reorg semantics must still be checked in deployment |
| Consensus finishes after expiry | post-consensus `_live` check rejects the transition | execution timestamps and finalization are platform semantics |
| Temporary source/model outage | owner-only, two-attempt `PROOF_RETRYABLE` recovery with immutable receipts | a genuine emergency can still expire if recovery is exhausted |
| Third-party assessment griefing | only the registered owner can start or retry an assessment | owner availability remains a liveness dependency |
| Malicious leader fabricates persistence | validator independently fetches, classifies and positive-audits; material verdict/retryability agreement plus witness/context verification | validator-majority collusion is outside this contract's guarantee |
| Positive classification hides an exception | bounded independent compatible-reading audit; veto/uncertainty fails closed | semantic model judgment remains probabilistic |
| Source prompt injection | source is escaped and labelled untrusted; source instructions are never binding | no prompt-isolation technique is a formal proof of model behavior |
| Fabricated or selective quote | decisive results require exact source witness; audit quotes also require exact witness | a true quote can still be misleading without complete source context |
| SSRF/private source | conservative HTTPS parser, no credentials/ports/query/fragment/encoding/IP/private wrappers | GenVM response does not expose authenticated DNS owner or final redirect destination |
| Payload substitution in consumer | immutable domain-separated commitment includes registry, rule, fingerprint, operation ID and exact payload | consumer application must not add an alternate unchecked path |
| Consumer replay | operation ID is recorded and action commitment is one-shot | a separate gate can intentionally authorize a separate action |
| Wrong executor | immutable executor address checked on execute and bound views | executor key compromise remains an application risk |
| Expired storage label bypass | `is_restricted` derives from timestamp every read; sealing is archival only | consumers must call the gate at execution time |

## Consensus failure and recovery semantics

Semantic uncertainty is normalized to terminal `INCONCLUSIVE` with an empty
decisive quote. Temporary source, HTTP, model or audit infrastructure failure
is `PROOF_RETRYABLE`; it cannot extend a rule and may be retried only by the
owner, at most twice for the epoch. Exhaustion becomes terminal
`INCONCLUSIVE`. A validator disagreement never creates a positive state
transition. Assessment receipts retain each attempt, reason and expiry before
and after the decision.

The validator does not trust a leader's quote or explanation. It independently
retrieves the frozen source, verifies the leader's witness and bounded material
context, and independently runs the positive compatible-reading audit. The
validator may accept different legitimate quotes or reason codes when the
decision-bearing material classification agrees; a materially different or
unsupported result is rejected.

## Non-goals and accepted limitations

Public evidence does not independently prove real-world identity, source
ownership, that a named actor performed an action, subjective reliance, legal
liability or the truth of an external policy. The accepted demonstration uses
public source material only and does not introduce identity services, wallets,
backend attestations, escrow or custody.
