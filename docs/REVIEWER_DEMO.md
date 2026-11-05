# Reviewer walkthrough

The deterministic walkthrough is intentionally small:

1. Register `inc42` with an immutable criterion, HTTPS source, 3,600-second
   epoch, 1,800-second window and a bounded renewal cap.
2. Read back the fingerprint and exact deadlines.
3. Before the window, `assess_renewal` rejects `TOO_EARLY`.
4. In the window, the owner submits the exact expected epoch and expiry.
5. The leader and validator each retrieve the frozen source. A positive result
   must also pass the independent adversarial compatible-reading audit.
6. A positive result advances expiry by exactly 3,600 seconds; it never uses
   transaction time plus duration and never crosses the hard stop.
7. A transient failure records `PROOF_RETRYABLE` without extending the rule;
   the owner may retry once more. Exhaustion becomes `INCONCLUSIVE`.
8. At or after expiry, `is_restricted` is false without `seal_expired`.
9. A `SunsetGate` bound to the exact registry, rule, fingerprint, executor and
   action commitment rejects while active and accepts only the exact payload
   after clearance/expiry. A changed payload, actor or replay is rejected.

Offline and Direct Mode demonstrations are not live StudioNet evidence. Real
deployment addresses, finalized transaction hashes and source parity belong in
`docs/DEPLOYMENT.md` only after independent verification.
