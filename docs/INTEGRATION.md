# Consumer integration

`SunsetGate` is a deliberately small cross-contract consumer proof. It does
not move assets or replace an application's own authorization.

## Constructor binding

Deploy with five typed arguments:

```text
registry: Address
rule_id: string
fingerprint: string
executor: Address
action_commitment: string
```

The constructor reads `rule_exists` and `rule_fingerprint` through the typed
`ISunset` interface and rejects an unknown or mismatched rule. It stores the
registry, exact rule ID, fingerprint and executor immutably.

The action commitment is the Keccak-256 hash of compact, sorted-key JSON:

```json
{"domain":"SUNSET_GATE_ACTION_V1","fingerprint":"...","operation_id":"...","payload":"...","registry":"0x...","rule_id":"..."}
```

`scripts/action_commitment.mjs` computes this exact value. The operation ID and
payload are therefore not free-form permission supplied at execution time;
they must match the frozen commitment for this gate instance.

## Execution behavior

`can_execute()` is a base status view. `can_execute_bound(operation_id, payload)`
checks executor, rule status, replay and exact payload binding. The write method
`execute_once(operation_id, payload)` repeats all checks, records the operation
ID and increments the local counter. A blocked, stale, substituted, malformed,
unauthorized or replayed call fails closed.

An independently cleared SUNSET rule can permit the exact bound action after its
expiry or terminal ended state. A blocked rule, unknown registry, wrong
fingerprint, wrong actor or wrong payload cannot. A different rule/attempt or a
different downstream action needs a separately constructed gate; one clearance
is not blanket authorization.

The current release deployment uses `0x5Ed933fc2992d466cCa5157160AB9a5d53A7b045`
for the ended-rule gate, `0x3770b26E4377FF920867A8cfF2A14da18A4d1B93` for the
positive-rule gate and `0x3A6C995b1A41daf1DbBC5B72c02b2dd4826fB812` for the
separate expiry gate. All are bound to the hardened SUNSET registry deployment
recorded in `docs/DEPLOYMENT.md`.

## Live proof policy

Only finalized successful StudioNet transactions may be recorded as live
interoperability evidence. A local Direct Mode gate test demonstrates typed
logic and replay behavior but is not a live cross-contract receipt. The final
addresses, transaction hashes and readbacks belong in `docs/DEPLOYMENT.md` only
after independently checking the exact stable RPC and execution result.
