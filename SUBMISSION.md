# SUNSET — consensus-backed expiry for temporary restrictions

## Reviewer description

Sunset is a reusable GenLayer Intelligent Contract that makes temporary restrictions expire by default. An owner commits an immutable continuation criterion, public HTTPS source, renewal window and lifetime cap. GenLayer leader and validator paths independently fetch and semantically assess the frozen source, then run a bounded adversarial audit before any positive renewal. Deterministic state logic alone applies one fixed epoch, ends early on affirmative resolution, or fails closed on ambiguity, outage and exhausted recovery. SunsetGate proves typed cross-contract consumption with immutable registry/rule/fingerprint/executor/action-payload bindings and replay protection. It does not claim website ownership, real-world identity, action completion, legal liability or external truth. The project is contract-only: no frontend, backend, database, Docker, custody or wallet UI.

Character count, including spaces: 884.

## Links

- Repository: https://github.com/ometere123/sunset
- Network: StudioNet, chain 61999, `https://studio.genlayer.com/api`
- Primary explorer: NOT YET VERIFIED
- Consumer explorer: NOT YET VERIFIED

## GenLayer-native mechanism

The contract uses `gl.vm.run_nondet_unsafe` with a leader and an independent
validator that each retrieve and classify the frozen evidence source. The
validator compares the complete typed result, including source digest, quote,
retryability and an independent positive compatible-reading audit. Deterministic
GenVM state, timestamps, hashes, owner identity, optimistic head checks,
hard-stop arithmetic and the consumer's exact action commitment decide
enforcement.

## Evidence status

The exact offline/Direct Mode/linter/CI counts and any finalized StudioNet
addresses or receipts are recorded only after execution in `docs/DEPLOYMENT.md`.
No simulated result is presented as live consensus. Public source material does
not independently prove a real-world actor, identity, action, source ownership,
subjective reliance, legal liability or external truth.
