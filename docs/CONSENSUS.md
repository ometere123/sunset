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
3. normalizes at most 12,000 decoded characters and computes the
   domain-separated `SUNSET_SOURCE_SNAPSHOT_V1` digest;
4. runs `_prompt` with the criterion and restriction inside escaped,
   explicitly untrusted source tags;
5. validates the exact JSON schema and an exact 12–220 character witness; and
6. when the primary result is positive, runs `_audit_prompt` once to search for
   exceptions, changed actors/dates/subjects, selective quotation, stale source
   context or a compatible reading that defeats persistence.

The validator does not inspect only the leader's shape. It independently
re-fetches, re-prompts and re-audits. `_valid_result` rejects extra fields,
wrong types, invalid enums, invalid hashes, missing witnesses and inconsistent
audit/retryability combinations. The validator accepts only exact equality of
the complete independently derived result. A leader claiming persistence while
the validator sees an ended, vetoed, changed or unavailable source therefore
cannot produce an accepted renewal.

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
