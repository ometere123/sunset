# SUNSET — consensus-backed expiry for temporary restrictions

## Reviewer description

Sunset is a reusable GenLayer Intelligent Contract that makes temporary restrictions expire by default. An owner commits an immutable continuation criterion, public HTTPS source, renewal window and lifetime cap. GenLayer leader and validator paths independently fetch and semantically assess the frozen source, then run a bounded adversarial audit before any positive renewal. Deterministic state logic alone applies one fixed epoch, ends early on affirmative resolution, or fails closed on ambiguity, outage and exhausted recovery. SunsetGate proves typed cross-contract consumption with immutable registry/rule/fingerprint/executor/action-payload bindings and replay protection. It does not claim website ownership, real-world identity, action completion, legal liability or external truth. The project is contract-only: no frontend, backend, database, Docker, custody or wallet UI.

Character count, including spaces: 884.

## Links

- Repository: https://github.com/ometere123/sunset
- Network: StudioNet, chain 61999, `https://studio.genlayer.com/api`
- Primary contract: `0x0Fd9A98eC49Ea04c2b71D7552B62F603D1b12970`
- Consumer contracts: `0x0351CFA149FeB4090Bff1D9EBaDAF77a6badF11F` (ended-rule gate); `0xcd69aF94ED4C3CD40bcB3226F46CF4133d6C857C` (positive gate); `0xbb98ad6d84bAd27cA2F51A5c5FEF545b72C40c3E` (expiry gate)
- Explorer: https://genlayer-explorer.vercel.app (address pages returned HTTP 503 during independent verification)

## GenLayer-native mechanism

The contract uses `gl.vm.run_nondet_unsafe` with a leader and an independent
validator that each retrieve and classify the frozen evidence source. The
validator compares decision-bearing material verdicts and retryability, then
independently verifies the leader's source witness, bounded context and positive
compatible-reading audit. Different legitimate quotations or reason codes do
not automatically disagree; unsupported material conclusions do. Deterministic
GenVM state, timestamps, hashes, owner identity, optimistic head checks,
hard-stop arithmetic and the consumer's exact action commitment decide
enforcement.

## Evidence status

The final verification records 58 offline pytest tests, 16 native Direct Mode
tests (74 total), 45 preflight assertions, two focused mutation tests and both contracts
passing GenVM lint and schema validation under linter 0.11.0 and runner
v0.2.12. Finalized StudioNet deployment, source-parity and consumer receipts
are recorded in `docs/DEPLOYMENT.md`. No simulated result is presented as live
consensus. Public source material does not independently prove a real-world
actor, identity, action, source ownership, subjective reliance, legal liability
or external truth.
