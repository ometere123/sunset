# SUNSET — stable StudioNet deployment and live verification ledger

This file records only observed artifacts. Historical failed or superseded
deployments are labelled as such and are not used as proof for the corrected
release.

## Locked environment

| Field | Verified value |
|---|---|
| Network | `studionet` |
| Chain ID | `61999` / `0xf22f` |
| RPC | `https://studio.genlayer.com/api` |
| Local CLI | repository-local `genlayer@0.39.1` |
| Runner | `v0.2.12` |
| Linter | `genvm-linter==0.11.0` |
| Direct Mode | `genlayer-test==0.29.2` |
| Global CLI | not used |

`node scripts/assert_studionet.mjs` independently queried `eth_chainId` and
returned `0xf22f`. No deployment or test in this ledger uses chain 61997,
Studio Dev, Studio Next or a global CLI.

## Final source artifacts

| File | SHA-256 | Deployed-byte check |
|---|---|---|
| `contracts/sunset.py` | `63611b8a9dbc0d4ba1346d9a0e46fc9e4fa8706621af5827709d73755cb207ff` | exact byte equality; 33,427 bytes |
| `contracts/sunset_gate.py` | `aecb925a4465b0977bbe9512cc9cf97056b9146e1cbe6b50fe1655c3adb9e384` | exact byte equality; 5,251 bytes |

The deployed source was read from the finalized deployment data returned by the
stable RPC and decoded before byte-for-byte comparison. The final committed
source is rechecked after the documentation closeout commit.

## Corrected primary deployment

- Final repository commit: `a37d43478ec405daf810fb9cb291a67f32adad23`
- Contract: `0x8D823Dcc31E4A3089D64D0f902927588Fb335Bb2`
- Deployment transaction: `0x6efd89aeb835b9cf4b20b578a27e863604ec8fe964201f0b0267c01a26a404f1`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; `eth_getTransactionReceipt.status = 0x1`
- Leader execution: `SUCCESS`
- Validator votes: `AGREE`, `AGREE`, `IDLE`, `IDLE`, `AGREE`

## Consumer deployments

### Positive-renewal active-rule gate

- Address: `0x7376A4BED67841C98F3061D894776b66C0Ab70F6`
- Deployment transaction: `0x0849e416e49735394adb5591be40380917d39dddbd99b2cd23f1ff7ccb476968`
- Binding: corrected primary registry; rule `sunset-iana-proof-final`; fingerprint `eb208aed6616dc48c8de610e9278d57b09125adb51af31e9a7dc4ab3877e3fbe`; executor `0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`; operation `iana-action-1`; payload `apply-iana-example-domain-policy`
- Action commitment: `6fa3e4b9a1505fa9456dccad81d5b09be4b7e050c9c9c037b230189f2a39661d`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; constructor execution `SUCCESS`

### Automatic-expiry gate

- Address: `0x50011d2Da2bb665cb79b3De45a7A4202e3b7de14`
- Deployment transaction: `0xe9280083c250d482cb80c36c6700d78d747115011627f718f7c42ae5e409f28f`
- Binding: corrected primary registry; rule `sunset-expiry-final`; fingerprint `53d5083ff75ae89f73dbbbc04556d9bdfc5bb1211b6c64357d0a29f30b2b782f`; executor `0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`; operation `iana-expiry-action-1`; payload `apply-expired-iana-fixture`
- Action commitment: `da3af418ce11b80bf37f5c86ce4535964e06c674166f43c34a1ed4023a0e1590`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; constructor execution `SUCCESS`

The explorer service returned HTTP 503 during address-page verification. No
address-specific explorer URL is therefore claimed as independently verified.

## Live StudioNet lifecycle evidence

### Positive renewal and active enforcement

Rule `sunset-iana-proof-final` was registered on the corrected primary in:

- Registration: `0x2b83915fddc2294e7da7f712ae8f412a2e43069a6703c098a10914bc88e92ab7`
- Fingerprint: `eb208aed6616dc48c8de610e9278d57b09125adb51af31e9a7dc4ab3877e3fbe`
- Source: `https://www.iana.org/help/example-domains`
- Epoch/window/cap: `900 / 720 / 1`
- Initial expiry: `1793901751`
- Hard stop: `1793902651`

The assessment finalized in:

- Assessment: `0x7c75c7c2dffc3ae5046fe2763f400ff52468b6ff160421946947b86a821408d0`
- Consensus: `MAJORITY_AGREE`
- Leader result: `JUSTIFICATION_PERSISTS`, with a source witness and `SAFE` audit
- Readback: `renewals = 1`, `assessed_epoch = 1`, `expires_at = 1793902651`, `hard_stop = 1793902651`, `status = ACTIVE`, `is_restricted = True`
- Exact extension: `1793901751` to `1793902651`, exactly one original 900-second epoch

The same active rule was bound to the positive-rule gate. The exact active
execution attempt finalized in:

- `0x7e5adf636080be0684af780847e857fd8700a37f55f39e158603b1ee63a3a874`
- Finalized/accepted `MAJORITY_AGREE`; leader execution `ERROR`
- Gate readback: `can_execute = false`, `can_execute_bound = false`, execution count `0`

The error is the expected fail-closed active restriction rejection; it is not
reported as a successful downstream action.

### Automatic expiry, exact action, substitution and replay

Rule `sunset-expiry-final` was registered with cap zero:

- Registration: `0x5b046d115d4491f34e9b36814940e7f2c9560e66f56b31deee20734cdfd5d010`
- Fingerprint: `53d5083ff75ae89f73dbbbc04556d9bdfc5bb1211b6c64357d0a29f30b2b782f`
- Epoch/window/cap: `900 / 720 / 0`
- Initial expiry and hard stop: `1793902376`
- Before expiry: bound gate `can_execute = false`

After waiting for the actual 900-second expiry without changing transaction
timestamps, the rule read back as `EXPIRED`, `is_restricted = false`, and the
gate read back `can_execute = true`.

- Wrong-payload transaction: `0xf23869e6cda96daaf9928f3998f208cc6823982f5630613dc606b685abe1f44d`; finalized/accepted, leader execution `ERROR`, expected payload mismatch, count unchanged
- Exact action transaction: `0x4755e1412544e266775d9e4d2e2452135a6ffc99085892040503e9b05ecb72e9`; finalized/accepted `MAJORITY_AGREE`, leader execution `SUCCESS`, return value `1`
- Exact readback: `get_execution_count() = 1`; `is_executed("iana-expiry-action-1") = true`
- Replay transaction: `0x177c3dcb0f7f3a9e04328cc9f707e73cd11c572113702d69d25c8fc06e609fe1`; finalized/accepted, leader execution `ERROR`, expected `REPLAY`, count remained `1`

### Bounded failure and historical evidence

Earlier corrected deployments recorded bounded `PROOF_RETRYABLE` and terminal
`INCONCLUSIVE` assessments without extending expiry. These are retained as
fail-closed historical evidence, not as successful renewals. The former
assessment transactions `0x6a105cbc898484c75b8549179be9835dd6cdee591a85e49462ffc84fc143a79c`
and `0x77fe84104999b9c7ef3d490e42c473e78da8a69a75294f28b3016bab1e12c912`
finalized `MAJORITY_DISAGREE`; no renewal was applied.

The previous `https://www.iana.org/domains/example` demonstration was not used
for the corrected positive proof. The corrected positive proof used
`https://www.iana.org/help/example-domains`, observed as HTTP 200 with no
redirect header by the pinned web observation path and containing the quoted
material. Public-page retrieval still does not prove real-world identity,
actor performance, source ownership, subjective reliance or legal liability.

An additional disposable rule `sunset-ended-final` was registered on the
corrected primary in `0xa246532188994b03a19554bff9c270d66d4daf23b5a0c888ddaff39439097651`.
Its immutable criterion asked whether the same IANA source affirmatively stated
that example domains were available for registration or transfer, while the
source said the opposite. An initial assessment
`0xd7e1a694c1f34fc8fd55e40e7459f662d5bf228a0c9469392b72228efad72118` finalized
with leader/validator agreement on the transaction but rolled back as
`TOO_EARLY` before the renewal window. A second eligible attempt
`0x813c408a85e19349d4a6d07c80601093f537fe95dd15fc0091dfa65494019fac`
finalized `MAJORITY_DISAGREE`; the leader proposed `JUSTIFICATION_ENDED`, but
the disagreement prevented any state transition. Readback remained
`ACTIVE`, `renewals = 0`, `assessed_epoch = 0`, and no assessment receipt was
created. This is live evidence of correct fail-closed disagreement handling,
not proof of early termination.

Live unauthorized-executor execution was not independently finalized because
the available funded alternate signer could not be unlocked with the authorized
disposable credential. Its rejection is covered by the offline and native
Direct Mode suites; this ledger does not convert those tests into live evidence.

## Tool and dependency evidence

- `node scripts/assert_studionet.mjs`: passed, `eth_chainId = 0xf22f`
- Local CLI: `0.39.1`
- Offline tests: 68 passed
- Direct Mode: 16 passed, including native `run_validator()` calls
- Preflight: 45 assertions passed
- GenVM lint/schema: both contracts passed under linter `0.11.0`, runner `v0.2.12`
- `pip check`: passed
- `npm audit --omit=dev --audit-level=high`: passed
- `pip-audit --strict`: not clean; 17 advisories across five pinned development-tool packages. These are documented toolchain findings, not deployed-contract findings.
- Final GitHub Actions: [run 42086395478](https://github.com/ometere123/sunset/actions/runs/42086395478), all three jobs `success` for the final commit

Only finalized receipts and readbacks above are release evidence. A submitted
transaction hash, `ACCEPTED` status without successful execution, an offline
mock or an explorer URL that was not independently reachable is not treated as
proof of a live successful operation.
