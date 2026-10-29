# Reviewer walkthrough — two worlds, one deadline

Use stable **StudioNet 61999** and record real transactions in
`docs/DEPLOYMENT.md`. For a fast time-warped demonstration, Direct Mode runs
the same contract functions without waiting for real-world hours.

1. **Register** `inc42` with a 3,600-second epoch, 1,800-second renewal
   window and two possible renewals. Record the immutable fingerprint.
2. **Bind** a `SunsetGate` to Sunset's address, `inc42`, and that fingerprint.
   `can_execute() = false` while the restriction is live.
3. **Before the window** an assessment is rejected as `TOO_EARLY`.
4. **Inside the window**, use a frozen public evidence page that affirmatively
   says the incident remains unresolved. Leader and validator agree: one
   `JUSTIFICATION_PERSISTS` receipt extends the *original* deadline by 3,600
   seconds. A duplicate assessment for the old head fails.
5. In a second fixture return `INCONCLUSIVE`. Show the deadline **unchanged**,
   then advance time exactly to expiry. Without calling `seal_expired`,
   `is_restricted = false`, `SunsetGate.can_execute() = true`, and a
   previously unseen operation ID is accepted.
6. In a third fixture return `JUSTIFICATION_ENDED`; the restriction terminates
   early. A later attempt to renew fails.
7. **Adversarial validator demo:** leader says PERSISTS, validator says ENDED;
   validator rejects. Changed source digests also fail consensus.
8. **Hard cap:** two successful extensions exhaust the allowance. The third
   cannot be requested; expiry at the absolute maximum needs no cleanup.

The evidence demo must use an actual controllable test page or recorded
non-sensitive fixture. Do not label mocked verdicts or a local shim as
five-validator production consensus.

## What to inspect

- `Sunset.assess_renewal` — epoch lock, bounded consensus, exact deadline.
- `Sunset.is_restricted` — direct expiration independent of writes.
- `SunsetGate._allowed` — immutable consumer binding and fail-closed read.
- `tests/test_offline.py` — deterministic/adversarial state transitions.
- `tests/direct/test_sunset_direct.py` — official SDK runtime suite.

The key distinction from a generic policy adjudicator: **no semantic result can
override an elapsed deadline or an exhausted absolute lifetime cap.**
