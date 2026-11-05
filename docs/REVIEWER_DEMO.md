# Reviewer walkthrough

The deterministic walkthrough is intentionally small:

1. For a disposable StudioNet demonstration, register a rule with an immutable
   criterion, HTTPS source, 900-second epoch, 720-second renewal window and a
   renewal cap of 1 or 2. These values are intentionally accelerated.
2. Read back the fingerprint and exact deadlines.
3. Before the window, `assess_renewal` rejects `TOO_EARLY`.
4. In the window, the owner submits the exact expected epoch and expiry.
5. The leader and validator each retrieve the frozen source. A positive result
   must also pass the independent adversarial compatible-reading audit; an
   ending result must pass a separate affirmative-resolution audit. They must
   agree on the material verdict while the validator independently checks the
   leader witness and complete bounded source; quote and reason wording may differ.
6. A positive result advances expiry by exactly one original epoch; it never uses
   transaction time plus duration and never crosses the hard stop.
7. A transient failure records `PROOF_RETRYABLE` without extending the rule;
   the owner may retry once more. Exhaustion becomes `INCONCLUSIVE`.
8. At or after expiry, `is_restricted` is false without `seal_expired`.
9. A `SunsetGate` bound to the exact registry, rule, fingerprint, executor and
   action commitment rejects while active and accepts only the exact payload
   after clearance/expiry. A changed payload, actor or replay is rejected.
10. An oversized source is not truncated: `SOURCE_TOO_LARGE` is terminal for the
    assessment, so an old witness cannot hide a newer contradiction beyond the
    former 12,000-character cutoff. Offline and native Direct Mode regressions
    cover both persistence and early-ending attempts.

Offline and Direct Mode demonstrations are not live StudioNet evidence. Real
deployment addresses, finalized transaction hashes and source parity belong in
`docs/DEPLOYMENT.md` only after independent verification.

Short, bounded 15-minute epochs were selected for reproducible StudioNet
lifecycle verification without waiting for production-scale restriction
periods. These values demonstrate protocol behavior and do not constitute a
recommended production timing policy. Production epoch and renewal-window
durations should reflect application risk, evidence-update cadence, operator
availability and measured GenLayer consensus/finality latency.
