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
| `contracts/sunset.py` | `9b6f1191f1cfef3adb052a77bcae1c03b11326c769a61f82cd9ff12cddbd3879` | exact byte equality; 36,193 bytes |
| `contracts/sunset_gate.py` | `aecb925a4465b0977bbe9512cc9cf97056b9146e1cbe6b50fe1655c3adb9e384` | exact byte equality; 5,251 bytes |

The deployed source was read from the finalized deployment data returned by the
stable RPC and decoded before byte-for-byte comparison. The final committed
source is rechecked after the documentation closeout commit.

## Current corrected primary deployment

- Contract: `0x0Fd9A98eC49Ea04c2b71D7552B62F603D1b12970`
- Deployment transaction: `0xfda08077d1e2570d8ab9114fab3a5fce1cb44f0cdaae142bf81fedbd1859a6be`
- Receipt: finalized; `MAJORITY_AGREE`; `eth_getTransactionReceipt.status = 0x1`
- Leader execution: `SUCCESS`
- Deployed source: 36,193 bytes; SHA-256 exactly matches the final committed `contracts/sunset.py`.

## Consumer deployments

### Ended-rule gate

- Address: `0x0351CFA149FeB4090Bff1D9EBaDAF77a6badF11F`
- Deployment transaction: `0x7395649e06c4b59c0c42301a4ed9276bfa667e761f9afac95f3e4e701d8ae96b`
- Binding: current primary; rule `sunset-fixture-ended-v2`; fingerprint `e18606f5fbd4cec96b0f0e062808306d0562a7e1e7cdb3dde8462bd64c7c5fbd`; executor `0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`; operation `ended-fixture-action-1`; payload `apply-ended-fixture-policy`
- Action commitment: `1633c2596d70235d82071711c0048ed29e1c39b4442f2130d6e48bb0777810e8`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; constructor execution `SUCCESS`

### Positive-renewal active-rule gate

- Address: `0xcd69aF94ED4C3CD40bcB3226F46CF4133d6C857C`
- Deployment transaction: `0x004d9a5c3211902069748aff38a98bc2daee1a4ade2894961d9ed2f61f60d91f`
- Binding: current primary; rule `sunset-positive-v2`; fingerprint `a6c935db116a2ffc6f89341dfc14f03c8675e54f07492193648ff9d95575fedf`; executor `0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`; operation `positive-v2-action-1`; payload `apply-positive-fixture-policy`
- Action commitment: `fc90e93411add3d3503746940230dc23a0feb86be736844c0cb8447af8fe6ce3`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; constructor execution `SUCCESS`

### Automatic-expiry gate

- Address: `0xbb98ad6d84bAd27cA2F51A5c5FEF545b72C40c3E`
- Deployment transaction: `0x139ddd5b7965550f622bbc4d07d318a0809901a102f01579ed63b3b34256fb52`
- Binding: current primary; rule `sunset-expiry-v2`; fingerprint `6300306882480b1ed4babe412cad53f585864758a4f32d339b32ce901437b41d`; executor `0x0d5540e0aD4B92Aa0ad4e5F1b8cD645ee1E363E7`; operation `expiry-v2-action-1`; payload `apply-expiry-v2-policy`
- Action commitment: `5f87e9bd3b672b18a769de9169de65740eec97b762a8e9528668c49edb63edeb`
- Receipt: finalized/accepted; `MAJORITY_AGREE`; constructor execution `SUCCESS`

The explorer service returned HTTP 503 during address-page verification. No
address-specific explorer URL is therefore claimed as independently verified.

## Live StudioNet lifecycle evidence

### Corrected deployment live proofs

These proofs use the current primary `0x0Fd9A98eC49Ea04c2b71D7552B62F603D1b12970`
and the three current gates listed above. The controlled fixture files are
protocol-mechanics fixtures, not evidence of unrelated real-world incidents,
identity, source ownership, actor action or legal facts.

#### Affirmative early termination

- Rule registration `sunset-fixture-ended-v2`: `0x0e341ef2dafd58137bcb498786c03125db6166807af9a2bf229bc72d0f05569e`; fingerprint `e18606f5fbd4cec96b0f0e062808306d0562a7e1e7cdb3dde8462bd64c7c5fbd`; source `https://raw.githubusercontent.com/ometere123/sunset/main/docs/fixtures/sunset-demo-status-early.txt`; epoch/window/cap `900 / 720 / 1`; initial expiry `1793911952`.
- The source was first observed in its ACTIVE state, then committed and independently retrieved in its RESOLVED state; the no-redirect raw response was confirmed before assessment.
- Assessment `0xb17f12513c6f2702593a04c18fb7b7e86f892ef8a6accc04e50d8ad4f8c7a6d2`: finalized `MAJORITY_AGREE`, leader execution `SUCCESS`, leader result `JUSTIFICATION_ENDED`.
- Readback: `status = ENDED_EARLY`, `last_verdict = JUSTIFICATION_ENDED`, `renewals = 0`, `is_restricted = false`, `expires_at = 1793911519`.
- Ended-rule gate `0x0351CFA149FeB4090Bff1D9EBaDAF77a6badF11F`: `can_execute = true`, exact bound predicate `true`.
- Authorized exact action `0x0fb2430bd893409f63180e7a32e6ce5d979bb1d330b7c70af24b25de7fd7cf0f` finalized with return value `1`; `get_execution_count() = 1`.
- Unauthorized executor `0xf7aa4bcfca965e77bfbf3fdf79057755b09f8ec8e6058b5b5422e1f9eab70298` finalized with leader rollback `ONLY_EXECUTOR`; count remained `1`.
- Replay `0x9298e860ac9e52ab36fd40879ea01742e2c28236019d762c59bcaae95a42a1da` finalized with rollback `REPLAY`; count remained `1`.
- Substituted payload `0x371971d7680bc629f9acecd038221fb85a7e52a5cf3d4f2e88683c49ca2a92a7` finalized with rollback `ACTION_COMMITMENT_MISMATCH`; count remained `1`.

#### Positive renewal and active enforcement

- Rule registration `sunset-positive-v2`: `0x2bda0aa11ad024f35d95a328a496fc5edfdf7510faa0e82ecc45791d040af42b`; fingerprint `a6c935db116a2ffc6f89341dfc14f03c8675e54f07492193648ff9d95575fedf`; source `https://raw.githubusercontent.com/ometere123/sunset/main/docs/fixtures/sunset-demo-status-positive.txt`; epoch/window/cap `900 / 720 / 1`; initial expiry `1793913590`; hard stop `1793914490`.
- Assessment `0x40e377b37d31a307fbf2e0ceb5045ded7b4b345b2d5ea3e7456761f95df04f30`: finalized `MAJORITY_AGREE`, leader execution `SUCCESS`, `JUSTIFICATION_PERSISTS`, `SAFE` audit.
- Readback: `renewals = 1`, `assessed_epoch = 1`, `expires_at = 1793914490`, `hard_stop = 1793914490`, `status = ACTIVE`, `is_restricted = true`; exact extension was one 900-second epoch.
- Positive gate `0xcd69aF94ED4C3CD40bcB3226F46CF4133d6C857C`: `can_execute = false`, bound predicate `false`, count `0`.
- Active exact-action rejection `0x95cfbd5fb8d6e529cf5f1bb824e229dcc79ff68fb3bd5106019f0404d893a0e0` finalized with the expected active/unverifiable restriction rollback; count remained `0`.

#### Fail-closed live negative

- IANA rule registration `sunset-iana-renewed-v2`: `0x64f4ac600b41beb5941070c1b3d5d160cdc91749db7d89d8ccbfa44021e12a3c`.
- Assessment `0xf88aef75a8d46ac1052224ade1133f3493a7803f2650c151cc913a0240e0aead` finalized `MAJORITY_AGREE` at the transaction layer, but the leader result was `INCONCLUSIVE/NO_SOURCE_WITNESS`; no extension occurred. Later readback was `INCONCLUSIVE`, `renewals = 0`, and the rule expired normally. This is not counted as a positive renewal.

#### Automatic expiry

- Rule registration `sunset-expiry-v2`: `0x5ada80000a1644916e37c03a5b5a2bff5bcb423a777778784273f8983e4dee2c`; fingerprint `6300306882480b1ed4babe412cad53f585864758a4f32d339b32ce901437b41d`; epoch/window/cap `900 / 720 / 0`; initial expiry and hard stop `1793913991`.
- Before expiry, gate `0xbb98ad6d84bAd27cA2F51A5c5FEF545b72C40c3E` read `can_execute = false` and exact bound predicate `false`.
- After the real chain clock reached `1793913991`, the rule read back `status = EXPIRED`, `is_restricted = false`; the gate read `can_execute = true` and its exact bound predicate `true`.
- Exact post-expiry action `0x09ea163c7db1ca40e144e5eb67e7faa6fe52e27771f05a3791e206c07669c250` finalized `MAJORITY_AGREE` with leader `SUCCESS` and return value `1`.
- Readback after the exact action: `get_execution_count() = 1`; `is_executed("expiry-v2-action-1") = true`.
- Replay attempt using the same operation with a substituted payload `0xba0190a110d7c9de239f2e75d27b733a01b4164acf45158bfed2dbc8d315ac88` finalized with rollback `REPLAY`; count remained `1`.
- New-operation payload substitution `0xf07c3f32aa2e03d08c0f4370a271f4496d6d4d9f0851bae9ff05cef0d1c13478` finalized with rollback `ACTION_COMMITMENT_MISMATCH`; count remained `1`.

### Historical superseded deployment: positive renewal and active enforcement

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

### Historical superseded deployment: automatic expiry, exact action, substitution and replay

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

### Historical bounded failure and prior deployment evidence

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

The older deployment lacked a finalized unauthorized-executor transaction
because its available funded alternate signer could not be unlocked. The
corrected deployment proof above supersedes that limitation: the disposable
alternate signer `0xf240e6cf640d782415494d1b35bb570ab6e37781` produced the
finalized `ONLY_EXECUTOR` rollback and the bound gate counter remained `1`.

## Tool and dependency evidence

- `node scripts/assert_studionet.mjs`: passed, `eth_chainId = 0xf22f`
- Local CLI: `0.39.1`
- Offline tests: 58 passed
- Direct Mode: 16 passed, including native `run_validator()` calls
- Preflight: 45 assertions passed
- GenVM lint/schema: both contracts passed under linter `0.11.0`, runner `v0.2.12`
- `pip check`: passed
- `npm audit --omit=dev --audit-level=high`: passed
- `pip-audit --strict`: not clean; 17 advisories across five pinned development-tool packages. These are documented toolchain findings, not deployed-contract findings.
- Final GitHub Actions: the final successful run is recorded in the release
  report and linked from the repository Actions history after closeout.

Only finalized receipts and readbacks above are release evidence. A submitted
transaction hash, `ACCEPTED` status without successful execution, an offline
mock or an explorer URL that was not independently reachable is not treated as
proof of a live successful operation.
