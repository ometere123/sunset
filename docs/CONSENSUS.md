# Consensus and deterministic state machine

SUNSET asks one frozen question: does fresh, affirmative evidence at the
registered HTTPS source establish that the original continuation criterion still
holds at the assessment timestamp?

## Leader and validator paths

`Sunset._consensus` freezes URL, criterion, restriction and UTC timestamp in a
tuple before calling `gl.vm.run_nondet_unsafe`. The leader and validator each
execute `_observe` independently. `_observe`:

1. performs `gl.nondet.web.get` against the immutable URL;
2. requires HTTP 200 and rejects an explicit redirect location header;
3. decodes and whitespace-normalizes only within a bounded raw-byte budget;
   if the decoded normalized source exceeds 12,000 characters, the observation
   returns terminal `SOURCE_TOO_LARGE` and fails closed instead of silently
   truncating newer or contradictory evidence, then computes the domain-separated
   `SUNSET_SOURCE_SNAPSHOT_V1` digest for accepted snapshots;
4. runs `_prompt` with the criterion and restriction inside escaped,
   explicitly untrusted source tags;
5. validates the typed result and an exact 12–220 character witness; and
6. when the primary result is positive, runs `_audit_prompt` once to search for
   exceptions, changed actors/dates/subjects, selective quotation, stale source
   context or a compatible reading that defeats persistence; an ending result
   is independently checked with `_ending_audit_prompt` for affirmative
   resolution rather than absence of persistence evidence.

The validator does not inspect only the leader's shape. It independently
re-fetches, re-prompts and re-audits. `_valid_result` rejects extra fields,
wrong types, invalid enums, invalid hashes, missing witnesses and inconsistent
audit/retryability combinations. The validator requires agreement on the
decision-bearing verdict and retryability. It then verifies the leader's exact
witness against a fresh source fetch, recomputes its bounded material digest,
and independently runs the appropriate adversarial audit against the complete
bounded normalized source snapshot, with the leader witness highlighted. The
240-character material context is used for a tolerant material digest, not as
the full semantic audit boundary; distant newer updates, qualifications and
contradictions remain visible to validators. Repeated witnesses fail closed.
Snapshot hashes, quote selection and bounded reason codes may differ when they
do not change the material conclusion. A leader claiming persistence while
the validator sees an ended, vetoed, changed, oversized or unavailable source therefore
cannot produce an accepted renewal.

This is the stable-runtime equivalent of a substantive Equivalence Principle:
open-ended explanatory text is not compared byte-for-byte, but the validator
must independently establish the material facts needed for the state
transition. Positive persistence and affirmative resolution are never accepted
without independently satisfactory material support. Malformed, unsupported or materially divergent proposals
fail closed.

## Result mapping

| Result | Meaning | State transition |
|---|---|---|
| `JUSTIFICATION_PERSISTS` | independently supported persistence and `SAFE` audit | extend prior expiry by exactly one original epoch |
| `JUSTIFICATION_ENDED` | independently supported resolution | terminal `ENDED_EARLY`, expiry now |
| `INCONCLUSIVE` | semantic uncertainty, missing witness, audit veto, or exhausted recovery | no extension; assessment epoch is consumed |
| `PROOF_RETRYABLE` | matching transient source/model/audit infrastructure failure | no extension; bounded owner-only retry remains |

`PERSISTS` and `ENDED` are terminal for that assessment epoch. A semantic
`INCONCLUSIVE` is also terminal. Only a `PROOF_RETRYABLE` result may be retried,
and only by the registered owner, up to `MAX_RECOVERY_ATTEMPTS == 2`. A second
matching transient failure finalizes `INCONCLUSIVE`; it never becomes a
clearance. Each attempt is stored under a unique `rule:epoch:attempt` receipt.

## Deterministic enforcement

Before consensus, `assess_renewal` verifies owner identity, live status, exact
expected epoch/expiry, unused slot, cap and inclusive renewal window. After
consensus it reloads the rule and checks the same optimistic-concurrency head,
terminal status and live timestamp. This prevents a proof that finishes after
the deadline from extending an expired rule. Expiry and hard stop are ordinary
state comparisons; the model never chooses a timestamp or epoch length.

The owner may revoke early. Any caller may archive an already expired rule with
`seal_expired`, but archival history does not affect `is_restricted`. There is
no administrator override, source replacement or rule-editing method.

## Evidence boundary

The URL filter is conservative: HTTPS only; no credentials, explicit ports,
queries, fragments, percent-encoding, IP literals, local/private suffixes or
common DNS-to-private-IP wrappers. The runtime response type for pinned runner
`v0.2.12` exposes status, headers and body but not proof of DNS ownership or a
final redirect destination. Consequently source ownership, publisher identity,
real-world action, identity, subjective reliance and legal liability remain
outside the contract guarantee.

## Previous disagreement investigation

The two historical assessment transactions
`0x6a105cbc898484c75b8549179be9835dd6cdee591a85e49462ffc84fc143a79c` and
`0x77fe84104999b9c7ef3d490e42c473e78da8a69a75294f28b3016bab1e12c912`
finalized as `MAJORITY_DISAGREE`; neither renewed a rule. Stable RPC receipt
data confirms leader execution succeeded at the transaction layer but returned
malformed/retryable proof results and the state transition was not applied.
The attempted `gen_getTransactionData`, `gen_getTransactionReceipt` and
`gen_dbg_traceTransaction` methods returned `Method not found`, so exact
per-validator prompts, quotations and internal errors cannot be proven from
those receipts. Validator-level web/model divergence is an inference, not an
observed trace fact.

The corrected implementation therefore compares material verdict and
retryability, independently verifies the leader witness and bounded context,
and runs the positive or affirmative-resolution audit independently. It retains
strict typed envelopes and fail-closed disagreement semantics without requiring
open-ended quotations or reason wording to be byte-identical.

The corrected StudioNet early-ending proof used a fresh controlled fixture whose
source was first observed in an active state and then updated to an explicit
resolved state. The earlier IANA-based early-ending attempts remained
`MAJORITY_DISAGREE` and made no state transition. The fresh proof finalized
`MAJORITY_AGREE` with `JUSTIFICATION_ENDED`, and the rule read back as
`ENDED_EARLY`. This demonstrates the protocol path only; a public fixture does
not establish a real-world actor, event, source owner or legal conclusion.
